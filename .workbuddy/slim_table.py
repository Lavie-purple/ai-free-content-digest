# -*- coding: utf-8 -*-
"""第四章表体瘦身 MVP（047 期答应用户、048/049 两期顺延，049 期落地）。

病根（047 期立）：**不是行数变多，是行内膨胀 + 快照式重印**。
    040→047 期行均字数单调上升 336 → 513；048 期实测 4.1 行均 545、4.2 行均 1569。

本脚本做什么（只动第四章，不改事实）：
    对第四章 4.1 / 4.2 的每一行，把状态列裁剪成「结论首句 + 一句边界」，
    论证部分**一个字不删地移进**：
      ① 根目录《第四章表体明细附录.md》—— 给人读的完整原文，按期号分节
      ② .workbuddy/data/table_full.md —— 给下期 gen_table 用的完整表体存档
    表体行末加指针，读者可点回完整原文。

为什么必须有 ②：
    `gen_table` 的输入是「上期 4.1 表体 + 《常驻权益总账》全量表体」。
    **4.1 的限时行动不进总账** —— 若只瘦身不留档，下期 gen_table 取到的就是瘦身后的行，
    **论证会逐期流失**。table_full.md 就是这条链的存档点（与 OpenRouter 两层存档同族）。

裁剪规则（只切句、不切半句）：
    ① 保留第一句（结论）
    ② 保留第一句含 ⚠️ 的句子（边界/风险）
    ③ 若仍超阈值，**从最长的论证句开始逐句丢弃**，直到达标；被丢的句子进附录
    ④ 活动名列与截止列**一字不改**

用法：
    python slim_table.py <md> --issue NNN [--max 200]
"""
import io
import os
import re
import sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DETAIL_NAME = "第四章表体明细附录.md"
FULL_PATH = os.path.join(WS, ".workbuddy", "data", "table_full.md")

SEP_RE = re.compile(r"^\|[\s:\-\|]+\|$")
PIT_RE = re.compile(r"避坑\s*\d+")
ISSUE_RE = re.compile(r"(?<!NNN)(0\d{2})\s*期")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def split_sentences(text):
    """按句切分，保留句末标点。中文句号/问号/叹号/分号都算句界。"""
    out, cur = [], ""
    for ch in text:
        cur += ch
        if ch in "。！？；":
            out.append(cur)
            cur = ""
    if cur.strip():
        out.append(cur)
    return out


def visible_len(s):
    return len("".join(s.split()))


def strip_bold(s):
    """剥掉 markdown 强调标记（**），避免裁剪在标记中间切断、留下破碎的加粗。"""
    return s.replace("**", "")


def split_by_punct(text, limit):
    """按标点递归切段，每段 <= limit 字。切不动时（无标点）返回原串。"""
    parts = re.split(r"(?<=[，、；：:（）()／/])", text)
    out, cur = [], ""
    for p in parts:
        if visible_len(cur + p) > limit and cur:
            out.append(cur)
            cur = p
        else:
            cur += p
    if cur:
        out.append(cur)
    final = []
    for seg in out:
        if visible_len(seg) > limit:
            sub = re.split(r"(?<=[\s·|｜])", seg)
            acc = ""
            for sp in sub:
                if visible_len(acc + sp) > limit and acc:
                    final.append(acc)
                    acc = sp
                else:
                    acc += sp
            if acc:
                final.append(acc)
        else:
            final.append(seg)
    return final


def slim_status(status, maxc, issue):
    """返回 (裁剪后的状态文本, 被裁掉的句子列表)。**重建式裁剪，不做原地修补。**

    049 期定稿（三个实测样本驱动）：
      ① **先剥 markdown 强调标记再切** —— 原实现在带 `**` 的原文上切，
         切出了 `**」**` 这种破碎加粗，渲染是脏的。
      ② **首句超长要递归切** —— 原实现只切一层逗号，且只在「dropped 为空」时才走，
         `Anthropic` 那一行 1089 字连续两次漏过。
      ③ **边界句只在装得下时才加** —— 装不下就进附录，不做「先加后砍」的往返。
    """
    plain = strip_bold(status)
    sents = split_sentences(plain)
    if not sents:
        return status, []
    dropped = []

    # ---- ① 结论首句 ----
    first = sents[0]
    if visible_len(first) > maxc:
        segs = split_by_punct(first, maxc)
        if len(segs) > 1:
            dropped.append(first[len(segs[0]):])
            first = segs[0]
            # 再兜一层：仍超长则继续切
            if visible_len(first) > maxc:
                segs2 = split_by_punct(first, maxc)
                if len(segs2) > 1:
                    dropped.append(first[len(segs2[0]):])
                    first = segs2[0]
    out = first.strip()

    # ---- ② 边界句：优先选**含状态语义词**的那句，其次选含 ⚠️ 的那句 ----
    # ⚠️ 049 期实测：`extract_deadlines.classify()` 判状态靠一组**关键词**：
    #   「已结束」/「未开始」/「今天换挡」/「口径 + 冲突·存疑·澄清」/ 色标 / 「生效中」。
    #   **这些词一旦被裁掉，状态判定就会漂移**（本期实测 `unclear` 5 → 4）。
    #   修法：**含状态语义词的句子优先保留**，宁可让 ⚠️ 边界句进附录。
    STATE_RE = re.compile(r"已结束|未开始|今天换挡|生效中|已过期|已收口|倒计时中|已开启|口径|冲突|存疑|澄清")
    boundary = ""
    state_sent = None
    for s in sents[1:]:
        if STATE_RE.search(s):
            state_sent = s
            break
    for cand_s in ([state_sent] if state_sent else []) + [s for s in sents[1:] if "⚠️" in s]:
        if not cand_s:
            continue
        s2 = cand_s.strip()
        if visible_len(out) + visible_len(s2) + 1 <= maxc:
            out = out + " " + s2
            boundary = s2
            break
        # ⚠️ 049 期实测：状态语义句装不下时，**不能整句丢掉**（会改判定），
        #   也不能整句硬塞（会破 R1）—— **按标点切成段，只取含判定词的那一段**。
        if cand_s is state_sent:
            segs = split_by_punct(s2, max(60, maxc - visible_len(out) - 1))
            for sg in segs:
                if STATE_RE.search(sg) and visible_len(out) + visible_len(sg) + 1 <= maxc:
                    out = out + " " + sg
                    boundary = sg
                    break
            if boundary:
                break
        dropped.append(s2 + "（超预算，未入表体；完整原文见附录）")
    if state_sent and state_sent.strip() != boundary and state_sent.strip() not in out:
        # 状态语义句没装下 → 追加一个短提示，保留判定所需的最少信息
        hint = "**（口径见附录）**"
        if visible_len(out) + visible_len(hint) + 1 <= maxc:
            out = out + " " + hint

    # ---- ③ 其余句子全部进附录 ----
    for s in sents[1:]:
        if s.strip() and s.strip() not in out:
            dropped.append(s)

    # ---- ④ R3：单行历史期号 ≤ 1 处 ----
    # ⚠️ 049 期实测：期号往往**不在括注里**，而是在边界句的句内文字里
    #   （如「044 期该行写…、047 期重算为 0，048 期与 049 期按基准日…」）。
    #   故先试「砍掉边界句」；砍完仍 ≥2 处，再删括注里的期号。
    hist = re.compile(r"(?<!%s)(0\d{2})\s*期" % issue)
    if len(hist.findall(out)) >= 2 and boundary and boundary in out:
        dropped.append(boundary + "（含多处历史期号，随沿革移入附录）")
        out = out.replace(boundary, "").strip()
    if len(hist.findall(out)) >= 2:
        pat = re.compile(r"[（(]\s*(?<!%s)(0\d{2})\s*期[^）)]{0,40}[）)]" % issue)
        for _ in range(12):
            if len(hist.findall(out)) < 2:
                break
            new_out, n = pat.subn("", out)
            if n == 0:
                break
            dropped.append("（删去历史期号括注）")
            out = new_out
    # 兜底：句内期号（不在括注里）—— 删掉「期号 + 后面最多 12 字」的片段，直到 ≤1 处
    guard = 0
    while len(hist.findall(out)) >= 2 and guard < 12:
        guard += 1
        m = hist.search(out)
        if not m:
            break
        seg = out[m.start():m.start() + 18]
        # 切在下一个标点处
        cut = re.split(r"[，、。；：]", seg)[0]
        out = (out[:m.start()] + out[m.start() + len(cut):]).strip()
        dropped.append("（删去句内历史期号片段：%s）" % cut)

    # ---- ⑤ 结论句重新加粗（**行首色标必须留在加粗之外**）----
    # ⚠️ 049 期实测（两处）：
    #   ① 原实现把整句包进 `**…**`，于是行首变成 `**⚪ 已过期（…）`，
    #      而 `extract_deadlines.classify()` 判状态靠 **`t.startswith("⚪")`** ——
    #      **色标被包进加粗标记后，判定落空、状态从 over 变成 other**，
    #      表现为「【C】已结束 9 条 → 8 条、【A】2 条 → 3 条」的静默漂移。
    #   ② 色标 `⚠️` 是**两个码位**（U+26A0 + U+FE0F）—— 原来按「一个字符」切，
    #      把 VS16 甩到了加粗标记之后，`verify_web.py` 判「裸 VS16」= 1 → NEEDS REVIEW。
    #   修法：**按「非文字非空白字符簇」取色标**（emoji 及其变体选择符整体取出）。
    out = out.strip()
    # ---- ⑤-补 最终硬裁（保证状态列 ≤ maxc）----
    # ⚠️ 049 期实测：`split_by_punct` 遇到「整段没有标点可切」的长句时会原样保留，
    #   于是状态列仍可 >200 字（R1 命中 5 条）。
    #   修法：**在标点全用尽时按字符硬切到预算内**，切掉的部分进附录（内容不丢）。
    if visible_len(out) > maxc:
        acc = ""
        for ch in out:
            if visible_len(acc + ch) > maxc:
                break
            acc += ch
        # 尽量退到最近的标点，读起来不突兀
        cut = max(acc.rfind(ch) for ch in "，、；：。 ")
        if cut > len(acc) * 0.5:
            acc = acc[:cut + 1]
        dropped.append(out[len(acc):] + "（超预算硬切，完整原文见附录）")
        out = acc
    if out:
        m = re.match(r"^((?:[^\w\s\u3000-\u9FFF\uFF00-\uFFEF]){1,3})\s*(.*)$", out, re.S)
        if m:
            out = "%s **%s**" % (m.group(1), m.group(2).strip())
        else:
            out = "**%s**" % out
    return out, [d for d in dropped if d.strip()]


def slim_name(name, maxc=40):
    """裁剪活动名列：保留主名 + 括号里最前的一个短标记，其余进附录。

    为什么活动名列也要裁：
        R1（单行超长）与 R3（单行含 ≥2 处历史期号）的主因在活动名列本身 ——
        很多行的名字里塞了「（040 期最高优先级运维项）」「（040 期全漏登）」这类**历史沿革**，
        而沿革按 047 期的设计本就该折进附录，不该占表体。
        **主名（括号之前）一个字不动** —— 它是跨期引用的主键。

    ⚠️ 049 期修（实测样本）：原实现用非贪婪正则 `^(.*?)（(.*?)）` 匹配，
    **遇到嵌套括号会从内层开始切** —— 实测把
    「`百度智能云`「文档解析（Unlimited-OCR）」API」切成了
    「`百度智能云`「文档解析」……」，**主名被破坏了**。
    修法：**做括号配对扫描，只切最后一个配对的括号组**。
    """
    plain = strip_bold(name).strip()
    # 括号配对扫描（支持中文与英文括号嵌套）
    stack = []
    pairs = []
    open_ch = {"（": "）", "(": ")"}
    close_ch = {"）": "（", ")": "("}
    for idx, ch in enumerate(plain):
        if ch in open_ch:
            stack.append((idx, ch))
        elif ch in close_ch:
            if stack and stack[-1][1] == close_ch[ch]:
                oi, oc = stack.pop()
                pairs.append((oi, idx))
    if not pairs:
        return name, []
    oi, ci = pairs[-1]                 # 最后一个配对的括号组
    head = plain[:oi].strip()
    tail = plain[oi + 1:ci].strip()
    if not head:
        return name, []
    # 括号里若只含「本期」类短标记，整段保留
    if len(tail) <= 18 and "期" not in tail:
        return name, []
    # 否则只保留括号里第一段短标记（≤14 字、不含「期」），其余进附录
    seg = re.split(r"[·、，,]", tail)
    keep_seg = ""
    for sgm in seg:
        sgm = sgm.strip()
        if sgm and len(sgm) <= 14 and "期" not in sgm:
            keep_seg = sgm
            break
    if keep_seg:
        new = "%s（%s）" % (head, keep_seg)
    else:
        new = head
    dropped = ["（活动名括注移入附录：%s）" % tail]
    # 重建强调：主名加粗
    new = "**%s**" % new.strip("*")
    return new, dropped


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    issue = None
    maxc = 200
    for a in sys.argv[1:]:
        if a.startswith("--issue"):
            issue = a.split("=")[1] if "=" in a else None
        if a.startswith("--max"):
            maxc = int(a.split("=")[1]) if "=" in a else maxc
    if not args:
        raise SystemExit("用法：python slim_table.py <md> --issue NNN")
    src = args[0]
    if not issue:
        m = re.search(r"第\s*(\d{3})\s*期", os.path.basename(src))
        issue = m.group(1) if m else "???"

    md = io.open(src, encoding="utf-8").read().replace("\r\n", "\n")

    # 第四章区间
    m = re.search(r"(?m)^##\s*四、[^\n]*$", md)
    if not m:
        raise SystemExit("没找到第四章")
    nxt = re.search(r"(?m)^##\s", md[m.end():])
    e = m.end() + nxt.start() if nxt else len(md)
    sec = md[m.start():e]

    lines = sec.split("\n")
    changed = 0
    detail = []          # (活动名, 完整状态原文, 裁剪后状态, 丢弃的句子)
    full_rows = []       # 完整表体行（用于 table_full.md）

    out_lines = []
    in_tbl = False
    for ln in lines:
        st = ln.strip()
        if st.startswith("### 4.1") or st.startswith("### 4.2"):
            in_tbl = True
        elif st.startswith("### ") and not (st.startswith("### 4.1") or st.startswith("### 4.2")):
            in_tbl = False
        if not (in_tbl and st.startswith("| ") and not SEP_RE.match(st)
                and not st.startswith("| 活动 |")):
            out_lines.append(ln)
            continue
        c = cells(ln)
        if len(c) < 3:
            out_lines.append(ln)
            continue
        full_rows.append(ln)
        status = c[2]
        new_status, dropped = slim_status(status, maxc, issue)
        # ⚠️ 049 期修（实测样本）：**活动名列一律不改**。
        #   原实现也裁活动名的括注（想压 R1/R3），结果：
        #   ① `extract_deadlines.py` 是从「第四章 + 《常驻权益总账》」两处取行再按**活动名去重**的 ——
        #      **活动名一改，去重就失效**，CSV 从 189 条涨到 204 条（多出 15 条重复）；
        #   ② 主名被破坏（实测把「`百度智能云`「文档解析（Unlimited-OCR）」API」切坏了）。
        #   修法：**活动名是跨期引用的主键，一个字不动**；R1/R3 已改为只看状态列，不需要动它。
        if not dropped and new_status == status:
            out_lines.append(ln)
            continue
        changed += 1
        detail.append((c[0], status, new_status, dropped))
        note = "〔附录 %s〕" % issue
        new_line = "| %s | %s | %s %s |" % (c[0], c[1], new_status.rstrip(), note)
        out_lines.append(new_line)

    new_sec = "\n".join(out_lines)
    new_md = md[:m.start()] + new_sec + md[e:]

    # ---- 写附录（给人读） ----
    if os.path.exists(os.path.join(WS, DETAIL_NAME)):
        old = io.open(os.path.join(WS, DETAIL_NAME), encoding="utf-8").read()
    else:
        old = "# 第四章表体明细附录\n\n> **这是什么**：日报第四章表体在「瘦身」时被裁掉的长论证原文，**逐字保存、不改写、不删条**。\n"
    if ("第 %s 期" % issue) not in old:
        parts = [
            "",
            "## 第 %s 期（%s）" % (issue, re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(src)).group(1)
                                  if re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(src)) else ""),
            "",
            "> **本期共 %d 行被瘦身**，表体行只留「谁 / 到什么时候 / 要不要动手」+ 一句边界；下面的原文一字未改。" % len(detail),
            "",
        ]
        for name, old_st, new_st, dropped in detail:
            parts.append("### %s" % re.sub(r"\*+", "", name).strip())
            parts.append("")
            parts.append("**表体精简后**：%s" % re.sub(r"\*+", "", new_st).strip())
            parts.append("")
            parts.append("**完整原文**：")
            parts.append("")
            parts.append("> " + old_st.replace("\n", " "))
            parts.append("")
        old = old.rstrip("\n") + "\n" + "\n".join(parts) + "\n"
        io.open(os.path.join(WS, DETAIL_NAME), "w", encoding="utf-8", newline="\n").write(old)

    # ---- 写机器存档（给下期 gen_table 用） ----
    os.makedirs(os.path.dirname(FULL_PATH), exist_ok=True)
    if os.path.exists(FULL_PATH):
        full = io.open(FULL_PATH, encoding="utf-8").read()
    else:
        full = ("# 第四章完整表体存档（机器用）\n\n"
                "> **用途**：下期 `gen_table` 的输入之一 —— **表体瘦身只砍日报里的展示长度，"
                "这里的完整行才是下期的事实底座**。4.1 的限时行动不进《常驻权益总账》，"
                "所以必须在这里留档，否则论证会逐期流失。\n")
    if ("## 第 %s 期" % issue) not in full:
        sec_text = ("\n## 第 %s 期（%d 行）\n\n" % (issue, len(full_rows))
                    + "\n".join(full_rows) + "\n")
        io.open(FULL_PATH, "w", encoding="utf-8", newline="\n").write(full.rstrip("\n") + "\n" + sec_text)

    io.open(src, "w", encoding="utf-8", newline="\n").write(new_md)

    print("src        : %s" % os.path.basename(src))
    print("第四章行  : %d（其中被瘦身 %d 行）" % (len(full_rows), changed))
    print("附录      : %s（本期节已写）" % DETAIL_NAME)
    print("机器存档  : .workbuddy/data/table_full.md（本期 %d 行）" % len(full_rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
