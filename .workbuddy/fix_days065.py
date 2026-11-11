# -*- coding: utf-8 -*-
"""065 期：把表体里**所有**天数 token 按「截止日 − 基准日」重算一遍（不只「距今」）。

由来：056 期避坑 252 —— `recalc_days` 只重算状态列的「距今 N 天」，
      截止列的「已过本期基准日 N 天」与状态列的「已过 N 天」从来没人重算，
      它们自写入那天起就冻结着，而基准日一直在推进。
      065 期实测：26 处「已过」全部停在 11/9 的口径上。

做法：
  1) 逐行解析截止列里**最后一个** `月/日`（与 recalc_days 的复核口径一致）。
  2) 「已过 (本期基准日 )? N 天」→ 真值 = 基准日 − 截止日。
  3) 「距开卖 N 天」→ 该活动已开卖，「距」这个说法本身失效 → **去掉数字、改成「已开卖」**
     （不改语义、不编新数字）。
  4) 多日期行（腾讯元器）单独改写：避免「已过 N 天」被绑到最后一个日期上。
  5) 写完复读落盘再断言。
"""
import io
import re
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第065期-2026-11-11.md"
BASE = date(2026, 11, 11)

MD_RE = re.compile(r'(?<![0-9])(\d{1,2})\s*/\s*(\d{1,2})(?![0-9])')
PAST_RE = re.compile(r'已过(?:本期基准日)?\s*`?(\d+)`?\s*天')
OPEN_RE = re.compile(r'距开卖\s*`?(\d+)`?\s*天')

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
lines = md.split("\n")

changed = []
removed = []

# ---- 多日期行：先把「已过 1 天」改成不带 token 的写法 ----
for i, l in enumerate(lines):
    if l.startswith("| ") and "腾讯智能体平台「元器」停止服务" in l:
        new = l.replace("停服日已过 `1` 天（`11/9` 为官方停服日）。",
                        "停服日（`11/9`）截至本期基准日已满 `1` 天。")
        if new != l:
            lines[i] = new
            changed.append(("腾讯元器（多日期行改写）", "已过 `1` 天", "已满 `1` 天"))

for i, l in enumerate(lines):
    if not (l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")):
        continue
    cols = l.split("|")
    if len(cols) < 5:
        continue
    dead = cols[2]
    # ① 距开卖：不论截止日是否已过，先把「距」这个说法去掉（活动已于 10/20 开卖）
    if OPEN_RE.search(l):
        lines[i] = OPEN_RE.sub("已开卖", l)
        removed.append(("距开卖", l[:40]))
        l = lines[i]
        cols = l.split("|")
        dead = cols[2]
    ms = MD_RE.findall(dead)
    if not ms:
        continue
    mo, dy = int(ms[-1][0]), int(ms[-1][1])
    if not (1 <= mo <= 12 and 1 <= dy <= 31):
        continue
    try:
        d = date(BASE.year, mo, dy)
    except ValueError:
        continue
    truth = (BASE - d).days
    if truth < 0:
        continue
    new = l
    # ② 已过 N 天（截止列 + 状态列）
    if PAST_RE.search(new):
        before = PAST_RE.findall(new)
        new = PAST_RE.sub("已过 `%d` 天" % truth, new)
        if before and before[0] != str(truth):
            changed.append((cols[1].strip()[:40], before[0], truth))
    if new != l:
        lines[i] = new

out = "\n".join(lines)
io.open(MD, "w", encoding="utf-8", newline="\n").write(out)

# 落盘复读（052 期纪律）
disk = io.open(MD, encoding="utf-8").read()
assert "已过 `1` 天（`11/9` 为官方停服日）" not in disk
assert not [l for l in disk.splitlines() if l.startswith("| ") and "距开卖" in l]

print("改写 %d 处「已过 N 天」：" % len(changed))
for name, old, new in changed:
    print("   %-40s %s -> %s" % (name, old, new))
print("去掉「距开卖」数字 %d 处" % len(removed))
print("written:", MD, len(disk.encode("utf-8")), "bytes")
