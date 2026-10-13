# -*- coding: utf-8 -*-
"""把 .workbuddy/tmp_table034.md 注入 034 期 md 的 <<<TABLE4>>> 占位符，并断言占位符残留为 0。"""
SRC = "AI免费内容与权益速递-第034期-2026-10-13.md"
TABLE = ".workbuddy/tmp_table034.md"

md = open(SRC, encoding="utf-8").read()
tbl = open(TABLE, encoding="utf-8").read().rstrip("\n")
assert md.count("<<<TABLE4>>>") == 1, md.count("<<<TABLE4>>>")
md = md.replace("<<<TABLE4>>>", tbl)
assert "<<<TABLE4>>>" not in md
open(SRC, "w", encoding="utf-8").write(md)
print("injected; placeholder remaining:", md.count("<<<TABLE4>>>"))
