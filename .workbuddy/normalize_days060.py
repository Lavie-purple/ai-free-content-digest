# -*- coding: utf-8 -*-
"""060 期：把表体里所有「已过 / 已早于 / 距结束 / 距开卖 / 距今 N 天」按基准日 2026-11-06 归一。

为什么单独写一个：056 期是让 gen_table 逐条手改这些数字，本期行数多、且
`recalc_days057.py` 的全表复核会把「截止列里那份副本」也一起检查 ——
所以先把所有 token 归一，再让 recalc 做独立复核（它只改「距今」）。
"""
import io
import re
import sys
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第060期-2026-11-06.md"
BASE = date(2026, 11, 6)

ISO_RE = re.compile(r'(?<![0-9])(20\d{2})-(\d{2})-(\d{2})(?![0-9])')
CN_MD_RE = re.compile(r'(?<![0-9])(\d{1,2})\s*月\s*(\d{1,2})\s*日')
MD_RE = re.compile(r'(?<![0-9])(\d{1,2})\s*/\s*(\d{1,2})(?![0-9])')

PAST_RE = re.compile(r'已(?:早于|过)本期基准日\s*`?(\d+)`?\s*天')
PAST2_RE = re.compile(r'已过\s*`?(\d+)`?\s*天')
END_RE = re.compile(r'距结束\s*`?(\d+)`?\s*天')
SELL_RE = re.compile(r'距开卖\s*`?(\d+)`?\s*天')
NOW_RE = re.compile(r'距今\s*`?(\d+)`?\s*天')


def last_date(col):
    """取截止列里的「收官日」。

    ⚠️ 优先级：ISO（20xx-xx-xx） > 斜杠（10/30） > 中文（10 月 30 日）。
    同一优先级内取**位置最靠后**的那个（区间活动取收官日）。
    059 期踩过的坑：`国家超算` 那行写的是 `10/30（官方逐字 \`10月21日至30日\`…）`，
    若不分优先级、只按位置取最后，会把中文里的 `10月21日` 当成截止日（真值 −13 而实际 −4）。
    """
    buckets = {0: [], 1: [], 2: []}
    for m in ISO_RE.finditer(col):
        buckets[0].append((m.start(), date(int(m.group(1)), int(m.group(2)), int(m.group(3)))))
    for m in MD_RE.finditer(col):
        mo, dy = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12 and 1 <= dy <= 31:
            try:
                buckets[1].append((m.start(), date(BASE.year, mo, dy)))
            except ValueError:
                pass
    for m in CN_MD_RE.finditer(col):
        try:
            buckets[2].append((m.start(), date(BASE.year, int(m.group(1)), int(m.group(2)))))
        except ValueError:
            pass
    for k in (0, 1, 2):
        if buckets[k]:
            buckets[k].sort()
            return buckets[k][-1][1]
    return None


md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
lines = md.split("\n")
out = []
changed = []
skipped = []

for l in lines:
    if not (l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")):
        out.append(l)
        continue
    cols = l.split("|")
    if len(cols) < 5:
        out.append(l)
        continue
    dead, stat = cols[2], cols[3]
    d = last_date(dead)
    if d is None:
        # 没有可解析日期：只跳过，不报错（长期档本来就无日期）
        out.append(l)
        continue
    truth = (d - BASE).days
    name = cols[1].strip()[:48]
    new = l

    if truth < 0:
        n = -truth
        new = PAST_RE.sub("已过本期基准日 `%d` 天" % n, new)
        new = PAST2_RE.sub("已过 `%d` 天" % n, new)
    else:
        new = NOW_RE.sub("距今 `%d` 天" % truth, new)
        new = END_RE.sub("距结束 `%d` 天" % truth, new)
        new = SELL_RE.sub("距开卖 `%d` 天" % truth, new)
    if new != l:
        # 归一后仍要能按字段数解析
        if len(new.split("|")) != len(cols):
            skipped.append((name, "字段数变化"))
            out.append(l)
            continue
        changed.append((name, d.isoformat(), truth))
        out.append(new)
    else:
        out.append(l)

io.open(MD, "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("天数 token 归一：改写 %d 行、跳过 %d 行" % (len(changed), len(skipped)))
for name, d, t in changed:
    print("   %-48s | 截止 %s | 真值 %+d" % (name, d, t))
for s in skipped:
    print("   ⚠️ 跳过", s)
if skipped:
    sys.exit(1)
