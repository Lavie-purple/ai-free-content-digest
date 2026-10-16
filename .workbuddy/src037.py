# -*- coding: utf-8 -*-
"""037 期台账（信源分级清单）更新：新增 3 条信源行 + 同步 4 处手写计数。

⚠️ **本期一处「差点重复登记」被逐节核对当场抓住**：
   原计划往 T4 加 `freetokens.custats.info`，核对时发现**该源早在 012 期就已登记在 T4**
   （「逐条带 `Last checked` 日期的免费 AI 额度条目」那一行），本期只是**再次命中**它、
   不是新增信源 → **T4 本期 +0**，全表 253 → **256**（不是 257）。
   这正是 036 期写的「加行与加行加对节是两件事」的同族纪律：**先核「这一行是不是已经有了」**。

纪律：① 每行必须落在正确小节；② 改完跑「逐节括号数 vs 实际行数」核对，且**与基线对比增量**而非看绝对值
（顶层标题 T0/T3 本身不带数据行、T4 含表外补登行，两处「不符」是既有正确口径，不是错）。
"""
import io, os, re

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(WS, "AI信息源分级清单-T0-T4.md")
BAK = os.path.join(WS, ".workbuddy", "tmp_src_bak037.md")


def audit(txt, label):
    sec_re = re.compile(r"^(#{2,3}) (.+?)（(\d+)）\s*$")
    cur = cur_decl = None
    cur_n = 0
    rep = []
    tops = []

    def flush():
        if cur:
            rep.append((cur, cur_decl, cur_n))

    for l in txt.split("\n"):
        m = sec_re.match(l)
        if m:
            flush()
            cur, cur_decl, cur_n = m.group(2).strip(), int(m.group(3)), 0
            if l.startswith("## "):
                tops.append((m.group(2).strip().split()[0], cur_decl))
            continue
        if l.startswith("| ") and not l.startswith("| 信源 ") and "---" not in l:
            if cur:
                cur_n += 1
    flush()
    if label:
        print("\n=== %s ===" % label)
        for name, d, c in rep:
            # 顶层标题不带数据行；T4 含表外补登行 —— 这两处是既有正确口径，标 n/a
            if c == 0:
                tag = "n/a（顶层，本身不带数据行）"
            elif name.startswith("T4"):
                tag = "n/a（含表外补登行，括号口径≠表内行数）"
            else:
                tag = "OK" if d == c else "<<< MISMATCH"
            print("  %-28s 括号 %3d / 实际 %3d  %s" % (name[:28], d, c, tag))
    return dict((n, (d, c)) for n, d, c in rep), dict(tops)


base_rep, base_tops = audit(io.open(BAK, encoding="utf-8").read(), None)
txt = io.open(F, encoding="utf-8").read()


def insert_after(anchor, row):
    global txt
    assert txt.count(anchor) == 1, ("anchor not unique", anchor[:60], txt.count(anchor))
    idx = txt.index(anchor)
    end = txt.index("\n", idx) + 1
    txt = txt[:end] + row + "\n" + txt[end:]


# ---- 1) T0 官方一手 · 国外：+2 行（6 列：信源 | 地址 | 状态 | 分类 | 首登期 | 行号）----
insert_after(
    "| Google Research Blog | https://research.google/blog/ | ✅ | 论文一手 | 036 | 111 |",
    "| **🆕 Meta AI Research 官方博客** | https://research.meta.ai/blog | — | "
    "**开源权重发布正文一手** | **037** | 0 |"
    " |",
)
insert_after(
    "| Google Research Blog | https://research.google/blog/ | ✅ | 论文一手 | 036 | 111 |",
    "| **🆕 Hugging Face `meta-models` 组织页与模型集合页**（含 LICENSE.md 与 gated 访问表单） | https://huggingface.co/meta-models | — | "
    "**「下载闸门」的第一现场** | **037** | 0 |"
    " |",
)

# ---- 2) T3 媒体 · 国外：+1 行（5 列：信源 | 地址 | 状态 | 首登期 | 行号）----
insert_after(
    "| The Decoder | https://the-decoder.com/ | ✅ | 033 | 19 |",
    "| **🆕 The AI Adventurer**（读码实测型博客） | https://theaiadventurer.com | — | **037** | 0 |",
)

# ---- 3) T4：+0 行（freetokens 已在 012 期登记，本期只是再次命中）----

# ---- 4) 同步 4 处手写计数 ----
COUNT_FIX = [
    ("## T0 · 根节点（145）", "## T0 · 根节点（147）"),
    ("### 官方一手 · 国外（37）", "### 官方一手 · 国外（39）"),
    ("## T3 · 媒体（40）", "## T3 · 媒体（41）"),
    ("### 国外（22）", "### 国外（23）"),
]
for old, new in COUNT_FIX:
    n = txt.count(old)
    assert n == 1, ("count-anchor not unique", old, n)
    txt = txt.replace(old, new)

io.open(F, "w", encoding="utf-8", newline="\r\n").write(txt)

# ---- 5) 逐节核对：本期增量必须恰好等于「有意图的插入数」----
new_rep, new_tops = audit(txt, "037 期台账逐节核对")
print("\n顶层求和 = %d（基线 %d，增量 %+d）" % (
    sum(new_tops.values()), sum(base_tops.values()),
    sum(new_tops.values()) - sum(base_tops.values())))

bad = []
EXPECT = {"官方一手 · 国外": 2, "国外": 1}
for name, (d, c) in new_rep.items():
    if c == 0 or name.startswith("T4"):
        continue
    bd, bc = base_rep[name]
    want = EXPECT.get(name, 0)
    # 括号数与实际行数必须仍然相等（内部自洽），且两者都必须比基线多出 want 行
    if d != c or (d - bd) != want or (c - bc) != want:
        bad.append((name, (bd, bc), (d, c), "want +%d" % want))

if bad:
    for b in bad:
        print("  MISMATCH", b)
    raise SystemExit("逐节核对不过")
print("\n逐节增量核对：ALL GREEN（官方一手·国外 +2、国外 +1，其余不变）")
print("顶层：", new_tops)