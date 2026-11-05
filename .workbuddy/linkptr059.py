# -*- coding: utf-8 -*-
"""059 期：1) 补回「049 期起表体已瘦身」导语；2) 把 〔附录 059〕 指针链接化。

纪律：
  · 必须在 slim_table.py 两轮跑完之后执行（slim 会重写表体、把指针原样保留但不带链接）
  · 改写后必须重新读回落盘文件再断言（059 期纪律：断言要校验落盘文件，不是内存结果）
"""
import io, os, re

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(WS, "AI免费内容与权益速递-第059期-2026-11-05.md")
APPX = os.path.join(WS, "第四章表体明细附录.md")

with io.open(APPX, encoding="utf-8") as f:
    _a = f.read()
# 「本期 97 行」= 附录 059 段被瘦身的行数（不是 md 总行数 —— md 有 7,700+ 行，
#   059 期第一次跑时误用了总行数，导语写成「本期 7736 行」）
_ai = _a.find("## 第 059 期")
appx_lines = _a[_ai:].count("\n### ")

with io.open(MD, encoding="utf-8") as f:
    s = f.read()

# ---------- 1) 导语 ----------
anchor = "—— 规则见脚注 ④。\n"
assert s.count(anchor) == 1, ("导语锚点数量异常", s.count(anchor))
GUIDE = (
    "\n> **049 期起第四章表体已瘦身**：**每行只留「谁 / 到什么时候 / 要不要动手」+ 一句边界**，"
    "**被裁掉的长论证一字未删地存放在 [`details.html`](details.html)（《第四章表体明细附录》，本期 %d 行）** "
    "—— **「表体里没有」不等于「没有写过」。**\n" % appx_lines
)
if "049 期起第四章表体已瘦身" not in s:
    s = s.replace(anchor, anchor + GUIDE, 1)

# ---------- 2) 指针链接化 ----------
before = s.count("〔附录 059〕")
s = s.replace("〔附录 059〕", "[附录 059](details.html)")
after = s.count("〔附录 059〕")
linked = s.count("[附录 059](details.html)")

with io.open(MD, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)

# ---------- 3) 读回落盘文件复核 ----------
with io.open(MD, encoding="utf-8") as f:
    disk = f.read()

assert disk.count("〔附录 059〕") == 0, "落盘文件仍残留裸指针"
assert disk.count("[附录 059](details.html)") == linked, "落盘文件链接数不符"
assert "049 期起第四章表体已瘦身" in disk, "导语未落盘"
assert "（《第四章表体明细附录》，本期 %d 行）" % appx_lines in disk, "附录行数未写入导语"

# 表体字段数分布（指针链接化后仍必须是 3）—— 只统计第四章区间
import collections
lines = disk.splitlines()
i41 = next(i for i, l in enumerate(lines) if l.startswith("### 4.1"))
iend = next(i for i, l in enumerate(lines) if l.startswith("### ④"))
body = [l for l in lines[i41:iend] if l.startswith("| ")]
body = [l for l in body if not set(l.replace("|", "").strip()) <= set("-: ")]
dist = collections.Counter(l.strip().strip("|").count("|") for l in body)
print("指针链接化：%d → %d（链接 %d 处）" % (before, after, linked))
print("附录行数：%d" % appx_lines)
print("表体行数：%d  字段数分布：%s" % (len(body), dist))
assert dist == collections.Counter({2: 97 + 2}), ("表体字段数分布异常（含两个表头共 99 行）", dist)
