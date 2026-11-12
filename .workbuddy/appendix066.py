# -*- coding: utf-8 -*-
"""066 期：把本期补入的 3 条完整原文追加到《第四章表体明细附录》"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
APP = WS + "第四章表体明细附录.md"
MD = WS + "AI免费内容与权益速递-第066期-2026-11-12.md"

md = io.open(MD, encoding="utf-8").read()
rows = [l for l in md.split("\n") if l.startswith("| ") and "066 期补入" in l]
assert len(rows) == 3, len(rows)

SEC = ["## 第 066 期（2026-11-12）", "",
       "> **本期表体是原地改写**：改写 `56` 行状态列、补入 `3` 行、移出归档 `1` 行（智谱 `AutoClaw` 第二期）。"
       "**下面三条是本期补入的全部条目的完整状态原文**（表体里是同一条的精简形态）。", ""]

for r in rows:
    c = r.strip().strip("|").split("|")
    name = c[0].strip()
    st = c[2].strip()
    SEC.append("### " + name)
    SEC.append("")
    SEC.append("**表体精简后**：" + st)
    SEC.append("")
    SEC.append("**完整原文**：")
    SEC.append("")
    SEC.append("> " + st)
    SEC.append("")

app = io.open(APP, encoding="utf-8").read().replace("\r\n", "\n")
app = app.rstrip("\n") + "\n\n" + "\n".join(SEC) + "\n"
io.open(APP, "w", encoding="utf-8", newline="\n").write(app)

disk = io.open(APP, encoding="utf-8").read()
assert "## 第 066 期（2026-11-12）" in disk
assert disk.count("## 第 066 期") == 1
print("appendix ok | bytes", len(disk.encode()), "| sections 066:", disk.count("### 🟢"))
