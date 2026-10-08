# -*- coding: utf-8 -*-
import io, re, collections
src = "AI免费内容与权益速递-第027期-2026-10-08.md"
lines = io.open(src, encoding="utf-8").read().split("\n")
# locate chapter 4 table
start = next(i for i,l in enumerate(lines) if l.startswith("## 四、"))
end = next(i for i,l in enumerate(lines) if i>start and l.startswith("## 五、"))
rows = [l for l in lines[start:end] if l.startswith("|")]
body = rows[2:]
print("chapter4 rows:", len(body))
EMO = ["🔴","🟠","🟡","🟢","⚪","⚠️"]
first = collections.Counter()
anyc  = collections.Counter()
for r in body:
    cells = [c.strip() for c in r.strip().strip("|").split("|")]
    status = cells[-1]
    hit = [e for e in EMO if e in status]
    if hit:
        first[hit[0]] += 1
    else:
        first["(none)"] += 1
    for e in set([x for x in EMO if x in r]):
        anyc[e]+=1
print("首个色标记:", dict(first))
print("任意位置出现:", dict(anyc))
# clarify the ⚠️ rows and none rows
print("--- 状态列首个标记非 emoji 或为 ⚠️ 的行 ---")
for r in body:
    cells = [c.strip() for c in r.strip().strip("|").split("|")]
    status = cells[-1]
    if not re.match(r"^[🔴🟠🟡🟢⚪]", status):
        print("   [%s] %s" % (status[:14], cells[0][:46]))
