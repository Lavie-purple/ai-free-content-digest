# -*- coding: utf-8 -*-
"""064 期：1) 补回「049 期起表体已瘦身」导语；2) 把 〔附录 064〕 指针链接化。
纪律：必须在 slim_table 之后执行；改写后读回落盘文件再断言（052/059）。
"""
import io, collections
WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第064期-2026-11-10.md"

s = io.open(MD, encoding="utf-8").read()
lines = s.split("\n")
body = [l for l in lines if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
n_rows = len(body)

anchor = "—— 规则见脚注 ④。\n"
assert s.count(anchor) == 1, ("导语锚点数量异常", s.count(anchor))
GUIDE = (
    "\n> **049 期起第四章表体已瘦身**：**每行只留「谁 / 到什么时候 / 要不要动手」+ 一句边界**，"
    "**被裁掉的长论证一字未删地存放在 [`details.html`](details.html)（《第四章表体明细附录》，本期 %d 行）** "
    "—— **「表体里没有」不等于「没有写过」。**\n" % n_rows
)
if "049 期起第四章表体已瘦身" not in s:
    s = s.replace(anchor, anchor + GUIDE, 1)

before = s.count("〔附录 064〕")
s = s.replace("〔附录 064〕", "[附录 064](details.html)")
after = s.count("〔附录 064〕")
linked = s.count("[附录 064](details.html)")
io.open(MD, "w", encoding="utf-8", newline="\n").write(s)

disk = io.open(MD, encoding="utf-8").read()
assert disk.count("〔附录 064〕") == 0, "落盘仍残留裸指针"
assert disk.count("[附录 064](details.html)") == linked
assert "049 期起第四章表体已瘦身" in disk
assert "（《第四章表体明细附录》，本期 %d 行）" % n_rows in disk
lines = disk.split("\n")
i41 = next(i for i, l in enumerate(lines) if l.startswith("### 4.1"))
iend = next(i for i, l in enumerate(lines) if l.startswith("### ④"))
seg = [l for l in lines[i41:iend] if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
dist = collections.Counter(l.strip().strip("|").count("|") for l in seg)
print("指针链接化：%d -> %d（链接 %d 处）" % (before, after, linked))
print("表体行数：%d（4.1+4.2）  字段数分布：%s" % (len(seg), dist))
assert dist == collections.Counter({2: len(seg)}), ("字段数分布异常", dist)
print("OK")
