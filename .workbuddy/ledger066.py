# -*- coding: utf-8 -*-
"""066 期：总账补 2 条 + 表头更新；归档 1 条（智谱 AutoClaw 第二期）"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
LED = WS + "常驻权益总账.md"
ARCH = WS + ".workbuddy/data/deadline_archive.md"

led = io.open(LED, encoding="utf-8").read().replace("\r\n", "\n")
before = len([l for l in led.split("\n") if l.startswith("| ")])
assert before == 175, ("总账 | 行数", before)  # 173 条 + 表头 2 行

NEW = [
    ("| 🟢 **`OpenAI` 退伍军人 / 现役军人一年 `ChatGPT Plus` 免费（**官方逐字 `a year of ChatGPT Plus at no cost` · "
     "`Veterans Day` `2026-11-11` 发布 · 累计 `20,000` 人已领**）** | **未公布（官方页无申请截止日、无名额上限表述）** | "
     "🟢 **生效中（066 期补入 · 官方页一手）。 页面逐字「more than `20,000` ... have claimed a year of ChatGPT Plus at no cost」，"
     "文末入口「See if you're eligible for a free year of ChatGPT Plus」**；**资格细则不在本页，本报告不转述未读到的条款**。 "
     "**⚠️ `20,000` 是累计口径，不是剩余名额。** [附录 066](details.html)  |"),
    ("| 🟢 **豆包 `Seedream 5.0` 系列「输入图免费 / 首张免费」（**`doubao-seedream-5-0-flash` 输入图逐字 `免费`、输出 `0.12` 元/张；"
     "`-pro` 输入图首张免费、第 `2` 张起 `0.02` 元/张**）** | **无结束日（按张计价的常规价目，非活动；官方未给任何活动期）** | "
     "🟢 **生效中（066 期补入 · 火山引擎计费文档一手）。 `volcengine.com/docs/82379/1099320`（`1,779,461` 字节）图片生成模型表逐字**："
     "`flash` 输入图 `免费`、输出 `0.12`；`pro` 输入图 `首张免费` / 第 `2` 张起 `0.02`，输出按像素档 `0.30` / `0.60`、"
     "图层拆分 `0.15` / `0.30`。 **⚠️「免费」是输入图、不是生成；按张计价、无每日额度字段。** [附录 066](details.html)  |"),
]

led = led.rstrip("\n") + "\n" + "\n".join(NEW) + "\n"
led = led.replace("**最后全量复核**：2026-11-11（第 065 期）", "**最后全量复核**：2026-11-12（第 066 期）")
led = led.replace("**条目数**：173", "**条目数**：175")
led = led.replace("这 173 条里本期真正发生变化的只有 31 条，其余 142 条", "这 175 条里本期真正发生变化的只有 33 条，其余 142 条")
io.open(LED, "w", encoding="utf-8", newline="\n").write(led)

disk = io.open(LED, encoding="utf-8").read()
rows = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows == 177, ("落盘 | 行数", rows)
for p in ("退伍军人", "Seedream 5.0", "第 066 期", "**条目数**：175"):
    assert p in disk, ("总账缺", p)

# ---------------- 归档
row = io.open(WS + ".workbuddy/tmp_arch066.txt", encoding="utf-8").read().strip()
arch = io.open(ARCH, encoding="utf-8").read().replace("\r\n", "\n")
sec = ("\n## 066 期（归档日 2026-11-12 · 移出 1 条）\n\n"
       "| 活动 | 截止 | 状态 |\n| --- | --- | --- |\n" + row + "\n")
arch = arch.rstrip("\n") + "\n" + sec
io.open(ARCH, "w", encoding="utf-8", newline="\n").write(arch)
a2 = io.open(ARCH, encoding="utf-8").read()
assert "066 期（归档日 2026-11-12" in a2 and row in a2
print("ledger rows=%d | archive ok | ledger bytes=%d" % (rows, len(disk.encode())))
