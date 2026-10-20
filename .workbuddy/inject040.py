# -*- coding: utf-8 -*-
"""把 .workbuddy/tmp_table040.md 注入 040 期 md 的 <<<TABLE4>>> 占位符，并断言占位符残留为 0。
⚠️ **注入脚本不可重复运行**（护栏非 bug，037 期已记）：重跑前必须先把第四章整块还原成占位符。
"""
SRC = "AI免费内容与权益速递-第040期-2026-10-18.md"
TABLE = ".workbuddy/tmp_table040.md"

md = open(SRC, encoding="utf-8").read()
tbl = open(TABLE, encoding="utf-8").read().rstrip("\n")
assert md.count("<<<TABLE4>>>") == 1, md.count("<<<TABLE4>>>")
md = md.replace("<<<TABLE4>>>", tbl)
assert "<<<TABLE4>>>" not in md
open(SRC, "w", encoding="utf-8", newline="\n").write(md)
print("injected; TABLE4 remaining:", md.count("<<<TABLE4>>>"))