# -*- coding: utf-8 -*-
"""把 .workbuddy/tmp_table064.md 注入 064 期 md 的 <<<TABLE4>>> 占位符。"""
import io
WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第064期-2026-11-10.md"
TBL = WS + ".workbuddy/tmp_table064.md"
md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
tbl = io.open(TBL, encoding="utf-8").read().replace("\r\n", "\n").strip()
assert md.count("<<<TABLE4>>>") == 1, md.count("<<<TABLE4>>>")
md = md.replace("<<<TABLE4>>>", tbl)
assert "<<<TABLE4>>>" not in md
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)
print("injected; placeholder remaining:", md.count("<<<TABLE4>>>"), "| bytes:", len(md.encode()))
