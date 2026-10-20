# -*- coding: utf-8 -*-
import io, re
P = "AI信息源分级清单-T0-T4.md"
t = io.open(P, encoding="utf-8").read()
lines = t.split("\n")
cur = None      # current section header
tbl = None
out = []
i = 0
sec = ""
for ln in lines:
    s = ln.strip()
    if s.startswith("## "):
        sec = s
        tbl = None
        continue
    if s.startswith("### "):
        sec = sec.split("\n")[0] + " / " + s
        tbl = None
        continue
    if not s.startswith("|"):
        tbl = None
        continue
    cells = [c.strip() for c in s.strip("|").split("|")]
    if tbl is None:
        tbl = {"hdr": cells[:2], "rows": [], "sec": sec}
        out.append(tbl)
        continue
    if set("".join(cells)) <= set("-: "):
        continue
    tbl["rows"].append(cells)
for tb in out:
    urls = sum(1 for r in tb["rows"] if len(r) >= 2 and r[1].startswith("http"))
    nonurl = len(tb["rows"]) - urls
    print("%-58s | %-14s | rows=%3d url=%3d nonurl=%d" % (tb["sec"][:58], str(tb["hdr"]), len(tb["rows"]), urls, nonurl))
print()
tot = sum(len(tb["rows"]) for tb in out)
totu = sum(1 for tb in out for r in tb["rows"] if len(r) >= 2 and r[1].startswith("http"))
print("TOTAL rows=%d url=%d" % (tot, totu))
