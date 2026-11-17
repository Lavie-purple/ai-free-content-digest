# -*- coding: utf-8 -*-
"""071 期表体复核（只读）：行数 / 字段数 / 天数带符号 / 方向 / 禁词 / 期号标记。"""
import io
import re
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第071期-2026-11-17.md"
TODAY = date(2026, 11, 17)
md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")


def rows_of(text, start, end):
    i = text.index(start)
    j = text.index(end)
    return [l for l in text[i:j].split("\n")
            if l.startswith("|") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]


r41 = rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
r42 = rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("行数：4.1 = %d，4.2 = %d，合计 %d" % (len(r41), len(r42), len(r41) + len(r42)))
assert (len(r41), len(r42)) == (65, 42)

cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
dist = Counter(len(cells(r)) for r in r41 + r42)
print("字段数分布：", dict(dist))
assert set(dist) == {3}


def days_of(deadline):
    m = re.search(r"(\d{1,2})\s*/\s*(\d{1,2})", deadline)
    if not m:
        return None
    mo, d = int(m.group(1)), int(m.group(2))
    try:
        return (date(TODAY.year, mo, d) - TODAY).days
    except ValueError:
        return None


bad, conflict, forbid = [], [], []
for r in r41 + r42:
    c = cells(r)
    delta = days_of(c[1])
    if delta is not None:
        for m in re.finditer(r"(已过|距截止|距承诺日)\s*`(\d+)`\s*天", c[2]):
            val = int(m.group(2))
            ok = (delta < 0 and val == -delta) if m.group(1) == "已过" else (val == delta and delta >= 0)
            if not ok:
                bad.append((c[0][:24], m.group(0), delta))
        if "已过" in c[1] and re.search(r"距截止\s*`\d+`\s*天", c[2]):
            conflict.append(c[0][:24])
    if "未开始" in c[2] or "已结束" in c[2]:
        forbid.append(c[0][:30])

assert not bad, bad
assert not conflict, conflict
assert not forbid, forbid
print("天数带符号 / 方向 / 禁词：全部通过")

# ⚠️ 只数**表体行**里的标记：脚注 ④ 会引用这个短语本身（「分别带 `071 期补入` 标记」），
#    用全文 count 会得到 3+1=4，从而把一条正确的脚注读成「多补了一行」。
_n_row = sum(1 for l in md.splitlines() if l.startswith("|") and "071 期补入" in l)
assert _n_row == 3, ("表体 071 期补入 行数", _n_row)
assert "M11W3" in md and "Will be removed on November 18, 2026" in md
assert "附录 070" not in md[md.index("## 四、"):], "第四章仍有旧期指针"
print("期号标记 / 附录指针：通过")
