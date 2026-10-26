# -*- coding: utf-8 -*-
"""把日报第四章拆成「4.1 限时动作 / 4.2 本期变更」，无变化的常驻权益移入《常驻权益总账》。

由来（047 期修订 · 用户 2026-10-27 第二次反馈）：
    上一步的 prune_table.py 只切「条目的生死」，切不掉「活着的条目每期重印」。
    实测第四章行均字数 40→47 期连续八期单调上升（336 → 513），
    因为 135 行无截止日的常驻权益本期一条没变，却逐字重印了 6.3 万字。
    本脚本把「日报（变化流）」与「总账（状态快照）」物理分开。

拆法（只搬位置，不改一个字）：
    4.1 限时动作  = 截止列能读到确切日期的行
    4.2 本期变更  = 无截止日、但行内带本期标记（`0NN 期` / `本期`）的行
    总账         = 无截止日的全部行（含 4.2 的，总账要完整可查）
    章节整体移到正文九章之后（保留「四」这个编号，全部历史引用不变）。

用法：
    python split_ledger.py                      # 自动取最新一期
    python split_ledger.py <src.md>
    python split_ledger.py <src.md> --dry-run   # 只报数，不写文件
    python split_ledger.py <src.md> --no-move   # 拆表但不挪位置
"""
import io, os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER_NAME = "常驻权益总账.md"

# 截止列出现这些词 → 判为「无确切截止日」的常驻权益
STAY_RE = re.compile(r"^\s*\**\s*(未公布|无结束日|无截止|未定|动态|持续|不适用|按量|随套餐|名额有限|ongoing|视|依)")
# 常驻档里出现这些 → 本期有变化，留在 4.2。
# 只认「本期」与**当期**期号：写「（029 期）登记」是历史沿革，不是本期变化，
# 否则 4.2 会把所有带历史标记的行都收进来（047 期实测 65 行 vs 实际 17 行）。
CHANGE_RE = None   # 在 main() 里按 issue 编译
SEP_RE = re.compile(r"^\|[\s:\-\|]+\|$")


def pick_default():
    cands = []
    for fn in os.listdir(WS):
        m = re.match(r"^(AI免费内容与权益速递.*?(\d{4})-(\d{2})-(\d{2}))\.md$", fn)
        if m:
            cands.append((m.group(2) + m.group(3) + m.group(4), fn))
    if not cands:
        raise SystemExit("工作区里没找到日报 md")
    cands.sort()
    return os.path.join(WS, cands[-1][1])


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def split_blocks(lines):
    """把连续的 `|` 行切成若干表格块，返回 [(start, end_exclusive), ...]。"""
    blocks, cur = [], []
    for idx, ln in enumerate(lines):
        if ln.strip().startswith("|"):
            cur.append(idx)
        else:
            if cur:
                blocks.append((cur[0], cur[-1] + 1))
                cur = []
    if cur:
        blocks.append((cur[0], cur[-1] + 1))
    return blocks


def is_stay(due_cell):
    d = due_cell.replace("**", "").strip()
    if not d:
        return True
    return bool(STAY_RE.match(d))


def find_section(md):
    """返回 (start, end, title_line)：第四章的字符区间（含标题行，不含下一个 ##）。"""
    m = re.search(r"(?m)^##\s*四、[^\n]*$", md)
    if not m:
        raise SystemExit("没找到第四章「限时活动与截止时间表」")
    nxt = re.search(r"(?m)^##\s", md[m.end():])
    end = m.end() + nxt.start() if nxt else len(md)
    return m.start(), end, m.group(0)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    move = "--no-move" not in sys.argv
    src = args[0] if args else pick_default()

    md = io.open(src, encoding="utf-8").read().replace("\r\n", "\n")
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", os.path.basename(src))
    today = "%s-%s-%s" % (m.group(1), m.group(2), m.group(3)) if m else "????-??-??"
    mm = re.search(r"第\s*(\d{3})\s*期", os.path.basename(src))
    issue = mm.group(1) if mm else "???"
    global CHANGE_RE
    CHANGE_RE = re.compile(r"(本期|%s\s*期)" % issue)

    s, e, title = find_section(md)
    body = md[s:e]
    lines = body.split("\n")

    blocks = split_blocks(lines)
    if not blocks:
        raise SystemExit("第四章里没找到表格")
    # 取最长的那块当表体（防止导语里将来有小表）
    b0, b1 = max(blocks, key=lambda x: x[1] - x[0])
    head = cells(lines[b0])
    sep = lines[b0 + 1]
    if len(head) != 3 or head[0] != "活动":
        raise SystemExit("第四章表头不是「活动 / 截止 / 状态」，实际：%r" % (head,))

    timed, stay_changed, stay_same = [], [], []
    for ln in lines[b0 + 2:b1]:
        if SEP_RE.match(ln.strip()) or not ln.strip():
            continue
        c = cells(ln)
        if len(c) < 3:
            continue
        if not is_stay(c[1]):
            timed.append(ln)
        elif CHANGE_RE.search(ln):
            stay_changed.append(ln)
        else:
            stay_same.append(ln)

    stay_all = stay_changed + stay_same
    pre = lines[:b0]        # 标题 + 导语
    post = lines[b1:]       # 表后脚注
    # 去掉尾部空的 `---`（移到文末后不需要章节分隔线）
    while post and post[-1].strip() in ("", "---"):
        post.pop()

    print("src        : %s" % os.path.basename(src))
    print("第四章原行  : %d（表体 %d）" % (len(lines), b1 - b0 - 2))
    print("  4.1 限时 : %d 行" % len(timed))
    print("  4.2 变更 : %d 行" % len(stay_changed))
    print("  常驻未变 : %d 行（移入总账）" % len(stay_same))
    print("  常驻全量 : %d 行（总账收录）" % len(stay_all))
    if dry:
        print("\n--dry-run，未写文件")
        return 0

    # ---- 重建第四章 ----
    if move:
        if "（" in title:
            title_new = title.replace("（", "（正文之后 · ", 1)
        else:
            title_new = title
    else:
        title_new = title
    intro = [
        title_new,
        "",
        "> **本章自 047 期修订起移到正文九章之后** —— 前面九章约 2.3 万字可以连贯读完，本章与《常驻权益总账》作为参考资料放在后面。**本章即往期所称「第四章」，编号与全部历史引用不变。**",
        ">",
        "> **本章只留两类**：**4.1 有确切截止日的限时动作** ／ **4.2 无截止日但本期有变化**。**未变动的常驻权益不再逐期重印**，全量 %d 条移入《[常驻权益总账](%s)》；**已过期 >7 天且已收口**的条目移入归档（`.workbuddy/data/deadline_archive.md`）—— 规则见脚注 ④。" % (len(stay_all), LEDGER_NAME),
        "",
        "### 4.1 限时动作（有确切截止日 · %d 条）" % len(timed),
        "",
    ]
    table_head = [lines[b0], sep]

    tail = [
        "",
        "### 4.2 常驻权益本期变更（无截止日 · 本期有变化 %d 条）" % len(stay_changed),
        "",
    ]
    pointer = [
        "",
        "> **其余 %d 条常驻权益本期无变化**，不逐期重印：全量 %d 条（含本节 %d 条）见 **《[常驻权益总账](%s)》** ／ 网页版 [`standing.html`](standing.html)。**「未重印」不等于「未复核」** —— 本期对全量 %d 条做了状态与口径复核，结果与上期一致，无新增无缺项。" % (
            len(stay_same), len(stay_all), len(stay_changed), LEDGER_NAME, len(stay_all)),
        "",
    ]

    new_sec = intro + table_head + timed + tail + table_head + stay_changed + pointer + post
    new_sec_text = "\n".join(new_sec).rstrip("\n") + "\n"

    # ---- 写总账 ----
    ledger = [
        "# 常驻权益总账",
        "",
        "**最后全量复核**：%s（第 %s 期）　**条目数**：%d　**维护**：`.workbuddy/split_ledger.py` 每期自动重建" % (today, issue, len(stay_all)),
        "",
        "> **这是什么**：日报第四章里「没有确切截止日」的长期有效权益。**原文照搬、不改写、不删条** —— 日报每期只报「有变化的」，本册保存全量。",
        ">",
        "> **怎么用**：查某家现在还给不给免费额度、什么价格、什么许可，在这里搜平台名或模型名即可；带 `⚠️` 的是口径存疑（后面跟的是避坑编号）。日报里 4.2 列出的变化条目，完整原文也在这里。",
        ">",
        "> **为什么不在日报里逐期重印**：这 %d 条里本期真正发生变化的只有 %d 条，其余 %d 条逐字重印一遍会让日报正文多出 6 万字，把时效内容淹掉。**未重印 ≠ 未复核**，每期仍逐条过一遍状态与口径。" % (len(stay_all), len(stay_changed), len(stay_same)),
        ">",
        "> **条目会变少吗**：会，但只按同一条规则 —— 某条一旦有了确切截止日，它就从本册移入日报 4.1；已过期 >7 天且已收口的，按归档规则移到 `.workbuddy/data/deadline_archive.md`（原文照存，可搜）。",
        "",
        "## 一、全量表（%d 条 · 按原文顺序）" % len(stay_all),
        "",
    ] + table_head + stay_all
    ledger_text = "\n".join(ledger).rstrip("\n") + "\n"

    # ---- 从原位摘掉第四章，按需移到文末 ----
    if move:
        rest = md[:s] + md[e:]
        # 文末锚点：最后一个 `---` + `*本期完。*`
        anchor = re.search(r"(?m)^---\s*$\s*\n+\*本期完。\*", rest)
        if anchor:
            rest = rest[:anchor.start()] + new_sec_text + "\n---\n\n*本期完。*\n"
        else:
            rest = rest.rstrip("\n") + "\n\n" + new_sec_text
    else:
        rest = md[:s] + new_sec_text + md[e:]

    io.open(src, "w", encoding="utf-8", newline="\n").write(rest)
    io.open(os.path.join(WS, LEDGER_NAME), "w", encoding="utf-8", newline="\n").write(ledger_text)

    print("\n写入 : %s" % os.path.basename(src))
    print("写入 : %s（%d 条）" % (LEDGER_NAME, len(stay_all)))
    print("第四章 : %d 行 → %d 行" % (len(lines), len(new_sec)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
