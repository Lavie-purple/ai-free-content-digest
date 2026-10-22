# -*- coding: utf-8 -*-
import io, re
MD="AI免费内容与权益速递-第044期-2026-10-22.md"
TBL=".workbuddy/tmp_table044.md"
md=io.open(MD,encoding="utf-8").read()
tbl=io.open(TBL,encoding="utf-8").read().rstrip("\n")
i=md.index("## 四、")
hdr="| 活动 | 截止 | 状态 |"
s=md.index(hdr,i)
e = s
off = 0
for l in md[s:].split("\n"):
    if l.startswith("|"):
        off += len(l) + 1
        e = s + off
    else:
        break
new = md[:s] + tbl + md[e:]
assert new.count("TABLE4")==0
io.open(MD,"w",encoding="utf-8",newline="\n").write(new)
print("reinjected, bytes=",len(new.encode("utf-8")))
