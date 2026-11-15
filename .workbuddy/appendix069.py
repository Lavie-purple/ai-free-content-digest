# -*- coding: utf-8 -*-
"""069 期：把本期瘦身掉的 8 条完整原文追加到《第四章表体明细附录》。

输入是 slim069.py 落盘的 tmp_069_slim.json（含 before/after 与旧原文），
不从日报里反推 —— 日报上已经只剩精简版了。
"""
import io, json

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
APP = WS + "第四章表体明细附录.md"
JS = WS + ".workbuddy/tmp_069_slim.json"

items = json.load(io.open(JS, encoding="utf-8"))
assert len(items) == 8, len(items)

SEC = ["## 第 069 期（2026-11-15）", "",
       "> **本期表体是原地改写**：语义改写 `41` 行状态列、`25` 行仅天数推进、补入 `3` 行、移出 `0` 行"
       "（`LongCat-2.5` / `PEAR` / `Runware` 分发层促销）。"
       "**下面 `8` 条是本期为压回 200 字阈值而裁掉论证的行**：表体是精简形态，"
       "「完整原文」是本期末裁字的状态列，一字未删。", ""]

for it in items:
    assert it["old"] != it["new"]
    assert " [附录 069](details.html)" in it["new"] or "附录 069" not in it["old"]
    SEC.append("### " + it["name"])
    SEC.append("")
    SEC.append("**表体精简后**（`%d` 字 → `%d` 字，`lint_table` R1 口径）：%s"
               % (it["before"], it["after"], it["new"]))
    SEC.append("")
    SEC.append("**完整原文**：")
    SEC.append("")
    SEC.append("> " + it["old"])
    SEC.append("")

app = io.open(APP, encoding="utf-8").read().replace("\r\n", "\n")
assert "## 第 069 期" not in app, "附录里已有 069 段，重跑会重复追加"
app = app.rstrip("\n") + "\n\n" + "\n".join(SEC) + "\n"
io.open(APP, "w", encoding="utf-8", newline="\n").write(app)

# ---- 回读落盘 ----
disk = io.open(APP, encoding="utf-8").read()
assert disk.count("## 第 069 期") == 1
tail = disk[disk.index("## 第 069 期"):]
assert tail.count("### ") == 8, tail.count("### ")
for it in items:
    assert it["name"] in tail, it["name"]
    assert it["old"] in tail, "原文未落盘：" + it["name"]
print("appendix ok | bytes", len(disk.encode()), "| 069 小节", tail.count("### "))
