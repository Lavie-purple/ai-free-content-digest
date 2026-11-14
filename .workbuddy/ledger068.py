# -*- coding: utf-8 -*-
"""068 期：总账补 2 条 + 表头更新（本期无「过期 >7 天且已收口」的新条目可归档）"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
LED = WS + "常驻权益总账.md"

led = io.open(LED, encoding="utf-8").read().replace("\r\n", "\n")
before = len([l for l in led.split("\n") if l.startswith("| ")])
assert before == 179, ("总账 | 行数", before)  # 177 条 + 表头 2 行

NEW = [
    ("| 🟡 **`inclusionAI` `Ling 3.2 Flash` 进入 `OpenRouter` 免费区（**`:free` 零价 · `1,048,576` 上下文 · "
     "文本 + 图片 · 单次最多 `200` 张图 · `created 1794591958`**）** | "
     "**未公布（动态目录 · 官方未给上下线时间）** | "
     "🟡 **生效中（068 期补入 · `OpenRouter` 两个端点一手）。 三层只开一层：列表有、"
     "`/models/<slug>/endpoints` 返回 `\"endpoints\":[]`、`hugging_face_id` 指向的 `inclusionAI/Ling-3.2-flash` 在 `HF` 是 `404`。** "
     "⚠️ 全量 `471` 条里只有 `:free` 一条、没有付费档 —— 「只登免费档」的第三种形态。 "
     "[附录 068](details.html)  |"),
    ("| 🟢 **Runway `Praxis-1` 开放权重（**`Apache-2.0` · `27B` 混合专家扩散 Transformer · 权重 + 推理 + 微调代码 · "
     "`GitHub runwayml/praxis-1-oss`**）** | **无结束日（`Apache-2.0` 开放权重，无活动期）** | "
     "🟢 **已开放权重（068 期补登 · 官方页 + `HF` 集合 + `GitHub` `API` 三处一手）。 `RoboLab-120` `46.2%`（`1,200` 回合，官方自测）；"
     "`SimplerEnv` `80.0%`（`RT-1` 机体微调后）。** ⚠️ 三个时间点（官方页 `11/11 15:00Z` / `HF` 集合 `11/12 20:22Z` / "
     "`GitHub` `11/12 22:14Z`）都在 066–067 期窗口内，两期漏报 —— **本期按「补登」收录**。 标准版 `80 GB` 显存。 "
     "[附录 068](details.html)  |"),
]

led = led.rstrip("\n") + "\n" + "\n".join(NEW) + "\n"
led = led.replace("**最后全量复核**：2026-11-13（第 067 期）", "**最后全量复核**：2026-11-14（第 068 期）")
led = led.replace("**条目数**：177", "**条目数**：179")
led = led.replace("这 177 条里本期真正发生变化的只有 35 条，其余 142 条",
                  "这 179 条里本期真正发生变化的只有 37 条，其余 142 条")
led = led.replace("## 一、全量表（177 条 · 按原文顺序）", "## 一、全量表（179 条 · 按原文顺序）")
io.open(LED, "w", encoding="utf-8", newline="\n").write(led)

disk = io.open(LED, encoding="utf-8").read()
rows = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows == 181, ("落盘 | 行数", rows)
for p in ("Praxis-1", "Ling 3.2 Flash", "第 068 期", "**条目数**：179", "全量表（179 条"):
    assert p in disk, ("总账缺", p)
print("ledger rows=%d | bytes=%d" % (rows, len(disk.encode())))
