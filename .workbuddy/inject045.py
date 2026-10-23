# -*- coding: utf-8 -*-
import io
md = "AI免费内容与权益速递-第045期-2026-10-23.md"
tbl = ".workbuddy/tmp_table045.md"
s = open(md, encoding="utf-8").read()
assert s.count("<<<TABLE4>>>") == 1, s.count("<<<TABLE4>>>")
t = open(tbl, encoding="utf-8").read().rstrip("\n")
s = s.replace("<<<TABLE4>>>", t)
open(md, "w", encoding="utf-8", newline="\n").write(s)
print("injected; rows:", t.count("\n") - 1)
