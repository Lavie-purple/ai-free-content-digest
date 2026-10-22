# -*- coding: utf-8 -*-
"""把 .workbuddy/tmp_table044.md 注入 044 期正文的 <<<TABLE4>>> 占位符。
不可重复运行（断言占位符恰好 1 次）。"""
import io

MD = "AI免费内容与权益速递-第044期-2026-10-22.md"
TBL = ".workbuddy/tmp_table044.md"

md = io.open(MD, encoding="utf-8").read()
tbl = io.open(TBL, encoding="utf-8").read().rstrip("\n")

assert md.count("<<<TABLE4>>>") == 1, ("占位符数量不为 1", md.count("<<<TABLE4>>>"))
md = md.replace("<<<TABLE4>>>", tbl)
assert "<<<TABLE4>>>" not in md

io.open(MD, "w", encoding="utf-8", newline="\n").write(md)
print("injected, bytes =", len(md.encode("utf-8")))
