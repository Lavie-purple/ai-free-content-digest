# -*- coding: utf-8 -*-
"""060 期：① 正文〔附录 060〕链接化 ② 补瘦身导语 ③ 附录 060 段内指针标签重贴。

纪律：
  · 059 期⑥：附录「原文」里的指针标签会停在上期期号，当期段内必须重贴。
  · 049 期起：正文每行末尾带 [附录 NNN](details.html)。
  · 055 期：分类统计在 slim 之后取 —— 本脚本不动状态列语义。
"""
import io, re

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第060期-2026-11-06.md"
DETAIL = WS + "第四章表体明细附录.md"

# ① 正文指针链接化
s = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
n = s.count("〔附录 060〕")
assert n > 0, "正文没有待链接指针（命中 0 条不是通过，是没找到对象 —— 避坑 257）"
s = s.replace("〔附录 060〕", "[附录 060](details.html)")
assert s.count("[附录 060](details.html)") == n
assert "〔附录 060〕" not in s

# ② 补瘦身导语（split_ledger 不写这句，往期靠 run0NN.sh 补）
anchor = "> **本章只留两类**"
i = s.index(anchor)
j = s.index("\n", i)
lead = ("\n>\n> **049 期起第四章表体已瘦身**：**每行只留「谁 / 到什么时候 / 要不要动手」+ 一句边界**，"
        "**被裁掉的长论证一字未删地存放在 [`details.html`](details.html)（《第四章表体明细附录》，本期 %d 行）**"
        " —— **「表体里没有」不等于「没有写过」。**" % n)
# 若已存在则替换，否则插入
m = re.search(r"\n>\n> \*\*049 期起第四章表体已瘦身\*\*[^\n]*\n", s)
if m:
    s = s[:m.start()] + lead + "\n" + s[m.end():]
else:
    s = s[:j] + lead + s[j:]

io.open(MD, "w", encoding="utf-8", newline="\n").write(s)
print("正文：链接化 %d 处，导语已就位" % n)

# ③ 附录 060 段内指针标签重贴（历史段不回改）
d = io.open(DETAIL, encoding="utf-8").read().replace("\r\n", "\n")
k = d.index("## 第 060 期（2026-11-06）")
head, sec = d[:k], d[k:]
old_n = sec.count("[附录 059](details.html)")
sec = sec.replace("[附录 059](details.html)", "[附录 060](details.html)")
assert sec.count("[附录 060](details.html)") == old_n, (old_n, sec.count("[附录 060](details.html)"))
assert "[附录 059](details.html)" not in sec
io.open(DETAIL, "w", encoding="utf-8", newline="\n").write(head + sec)
print("附录：060 段内重贴 %d 处标签；历史段未改动" % old_n)
print("历史段 059 标签仍存：", head.count("[附录 059](details.html)"), "处")
