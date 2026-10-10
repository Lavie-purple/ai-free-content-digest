# -*- coding: utf-8 -*-
"""把 .workbuddy/tmp_table030.md 注入 030 期 md 的 <<<TABLE4>>> 占位符。"""
import re
MD = "AI免费内容与权益速递-第030期-2026-10-11.md"
TBL = ".workbuddy/tmp_table030.md"
s = open(MD, encoding="utf-8").read()
assert s.count("<<<TABLE4>>>") == 1, s.count("<<<TABLE4>>>")
tbl = open(TBL, encoding="utf-8").read().rstrip("\n")
s = s.replace("<<<TABLE4>>>", tbl)
# 占位符守卫
assert "<<<" not in s and ">>>" not in s, "占位符残留"
open(MD, "w", encoding="utf-8").write(s)
print("injected. md bytes:", len(s.encode("utf-8")))
