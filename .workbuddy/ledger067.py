# -*- coding: utf-8 -*-
"""067 期：总账补 2 条 + 表头更新（不归档：本期无「过期 >7 天且已收口」的新条目）"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
LED = WS + "常驻权益总账.md"

led = io.open(LED, encoding="utf-8").read().replace("\r\n", "\n")
before = len([l for l in led.split("\n") if l.startswith("| ")])
assert before == 177, ("总账 | 行数", before)  # 175 条 + 表头 2 行

NEW = [
    ("| 🟢 **`Gemini 4 Hydrogen` 对免费用户开放（**官方逐字 `free users will get access ... via auto model selection` · "
     "`$1.50` / `$7.50` 每百万 · `1M` 上下文 · `blog.google` `Nov 12, 2026`**）** | "
     "**无结束日（产品能力，非活动；官方未给任何期限）** | "
     "🟢 **生效中（067 期补入 · 官方博客一手）。 免费路径两条：`Gemini` 应用（**自动选模，模型下拉里点不到**）与 "
     "`Google Search`（全部用户）。** ⚠️ 无额度、无次数、无开关；`Antigravity` 里只给付费 `AI Pro` / `Ultra`。 "
     "[附录 067](details.html)  |"),
    ("| 🟢 **`thinkingmachines/Inkling-2-Small` 开放权重（**`Apache-2.0` · `gated: false` · `36` 个文件 / `24` 个 "
     "`safetensors` 分片 · `image-text-to-text` 通用多模态**）** | **无结束日（`Apache-2.0` 开放权重，无活动期）** | "
     "🟢 **已开放权重（第 ④ 级已到 · 067 期补入 · `HF` 单仓端点一手）。 `downloads 12` / `likes 166`**；"
     "建仓 `11/04`、`lastModified` `11/13 03:42 UTC`、**本期才进 `?author=` 公开列表** —— 三个时间点分开写。 "
     "[附录 067](details.html)  |"),
]

led = led.rstrip("\n") + "\n" + "\n".join(NEW) + "\n"
led = led.replace("**最后全量复核**：2026-11-12（第 066 期）", "**最后全量复核**：2026-11-13（第 067 期）")
led = led.replace("**条目数**：175", "**条目数**：177")
led = led.replace("这 175 条里本期真正发生变化的只有 33 条，其余 142 条",
                  "这 177 条里本期真正发生变化的只有 35 条，其余 142 条")
led = led.replace("这 175 条里本期真正发生变化的只有 33 条，其余 142 条逐字重印",
                  "这 177 条里本期真正发生变化的只有 35 条，其余 142 条逐字重印")
led = led.replace("## 一、全量表（173 条 · 按原文顺序）", "## 一、全量表（177 条 · 按原文顺序）")
io.open(LED, "w", encoding="utf-8", newline="\n").write(led)

disk = io.open(LED, encoding="utf-8").read()
rows = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows == 179, ("落盘 | 行数", rows)
for p in ("Gemini 4 Hydrogen", "Inkling-2-Small", "第 067 期", "**条目数**：177", "全量表（177 条"):
    assert p in disk, ("总账缺", p)
print("ledger rows=%d | bytes=%d" % (rows, len(disk.encode())))
