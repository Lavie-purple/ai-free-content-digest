# -*- coding: utf-8 -*-
import io, re, sys

def sec_counts(P):
    t = io.open(P, encoding="utf-8").read()
    lines = t.split("\n")
    secs = []   # (title, bracket, rows)
    cur = None
    prev_pipe = False
    for ln in lines:
        s = ln.strip()
        m = re.match(r"^(#{2,3})\s+(.*)$", s)
        if m:
            cur = {"title": m.group(2), "rows": 0, "hdr": 0, "sep": 0, "orphan": 0, "intbl": False, "insec": True}
            secs.append(cur)
            prev_pipe = False
            continue
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cur is None:
                prev_pipe = True
                continue
            if not prev_pipe:
                # 新表块的第一行 = 表头（或孤立行）
                if cells[:2] == ["信源", "地址"]:
                    cur["hdr"] += 1
                    cur["intbl"] = True
                else:
                    cur["orphan"] += 1
                    cur["inbl"] = False
                    cur["intbl"] = False
            else:
                if cur.get("inbl"):
                    if set("".join(cells)) <= set("-: "):
                        cur["sep"] += 1
                    else:
                        cur["rows"] += 1
                else:
                    # 孤立行块内部后续行
                    if set("".join(cells)) <= set("-: "):
                        cur["sep"] += 1
                    else:
                        cur["orphan"] += 1
            prev_pipe = True
            continue
        prev_pipe = False
    return secs

for tag, P in [("HEAD(035)", ".workbuddy/tmp_ledger_head.md"), ("当前(036)", "AI信息源分级清单-T0-T4.md")]:
    print("==== %s ====" % tag)
    tot_b = tot_r = 0
    for s in sec_counts(P):
        b = re.search(r"（(\d+)）", s["title"])
        b = int(b.group(1)) if b else None
        actual = s["rows"] + s["orphan"]
        flag = ""
        if b is not None and b != actual:
            flag = "   <<< 括号 %d vs 实际 %d（表内 %d + 表外 %d）" % (b, actual, s["rows"], s["orphan"])
        if b is not None:
            tot_b += b; tot_r += actual
        print("  %-30s 括号=%-5s 实际=%-4d（表内 %d + 表外 %d）%s" % (s["title"][:30], b, actual, s["rows"], s["orphan"], flag))
    print("  ---- 括号合计 %d vs 实际合计 %d" % (tot_b, tot_r))
