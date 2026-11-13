# -*- coding: utf-8 -*-
"""067 期：把本期补入的 3 条完整原文追加到《第四章表体明细附录》"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
APP = WS + "第四章表体明细附录.md"
MD = WS + "AI免费内容与权益速递-第067期-2026-11-13.md"

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
rows = [l for l in md.split("\n") if l.startswith("| ") and "067 期补入" in l]
assert len(rows) == 3, ("补入行数应为 3，实际 %d" % len(rows))

SEC = ["## 第 067 期（2026-11-13）", "",
       "> **本期表体是原地改写**：改写 `55` 行状态列、补入 `3` 行、归档 `0` 行"
       "（`Figma Code Layers` 已过 `9` 天但状态列未写收口语，按纪律留在表体）。"
       "**下面三条是本期补入的全部条目的完整状态原文**（表体里是同一条的呈现形态，未裁字）。", ""]

for r in rows:
    c = r.strip().strip("|").split("|")
    assert len(c) == 3, ("字段数应为 3，实际 %d" % len(c))
    name = c[0].strip()
    st = c[2].strip()
    assert st, name
    SEC.append("### " + name)
    SEC.append("")
    SEC.append("**表体精简后**：" + st)
    SEC.append("")
    SEC.append("**完整原文**：")
    SEC.append("")
    SEC.append("> " + st)
    SEC.append("")

app = io.open(APP, encoding="utf-8").read().replace("\r\n", "\n")
assert "## 第 067 期" not in app, "附录里已有 067 段，重跑会重复追加"
app = app.rstrip("\n") + "\n\n" + "\n".join(SEC) + "\n"
io.open(APP, "w", encoding="utf-8", newline="\n").write(app)

disk = io.open(APP, encoding="utf-8").read()
assert "## 第 067 期（2026-11-13）" in disk
assert disk.count("## 第 067 期") == 1
tail = disk[disk.index("## 第 067 期"):]
assert tail.count("### ") == 3, tail.count("### ")
for r in rows:
    nm = r.strip().strip("|").split("|")[0].strip()
    assert nm in tail, nm
print("appendix ok | bytes", len(disk.encode()), "| 067 小节", tail.count("### "))
