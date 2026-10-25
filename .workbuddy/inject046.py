# -*- coding: utf-8 -*-
"""把 .workbuddy/tmp_table046.md 注入第046期正文的 <<<TABLE4>>> 占位符。"""
import io, os

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(WS, "AI免费内容与权益速递-第046期-2026-10-25.md")
TBL = os.path.join(WS, ".workbuddy", "tmp_table046.md")

s = io.open(MD, encoding="utf-8").read()
t = io.open(TBL, encoding="utf-8").read().strip()

assert s.count("<<<TABLE4>>>") == 1, "占位符必须恰好 1 个，实为 %d" % s.count("<<<TABLE4>>>")
assert t.startswith("| 活动 |"), "表文件必须以表头开始"
rows = [l for l in t.split("\n") if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(rows) == 238, "行数必须 238，实为 %d" % len(rows)

s = s.replace("<<<TABLE4>>>", t)
io.open(MD, "w", encoding="utf-8", newline="").write(s)
assert "<<<TABLE4>>>" not in io.open(MD, encoding="utf-8").read()
print("injected OK; md now", len(s), "chars")
