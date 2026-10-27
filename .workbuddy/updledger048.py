# -*- coding: utf-8 -*-
"""048 期：就地更新台账 3 行（不加信源行、手写括号计数不变）。
⚠️ 台账是内部台账，不对外展示；本脚本只改「用途」列的说明文字，
   「上次命中 / 命中次数」两列由 build_source_hits.py 自动回写，不要在这里动。
"""
import io

F = "AI信息源分级清单-T0-T4.md"
s = io.open(F, encoding="utf-8").read()

# ---- 1) Runware：路径迁移 + 0.133 归属 ----
old1 = "**047 期首次命中（10/27）**：`Kling 4.0` 的 `native audio` 就是在本站模型页一手核到的（`native audio` × 8、`audio` × 79），**而 `fal` 的四个端点描述里没有音频字段** —— **同一模型、两个分发层、字段不同步**（047 期避坑 204 的直接样本）。⚠️ **但本站缺定价字段**：社媒称「`$0.133`/秒起、未来 7 天 15% 折扣」，**`models/klingai` 与 `pricing` 两页均未出现 `0.133` 与 `7 days`**，故该价格只作社媒口径、不进价格位（避坑 200 同族）。"
new1 = ("**047 期首次命中（10/27）**：`Kling 4.0` 的 `native audio` 就是在本站模型页一手核到的（`native audio` × 8、`audio` × 79），**而 `fal` 的四个端点描述里没有音频字段** —— **同一模型、两个分发层、字段不同步**（047 期避坑 204 的直接样本）。"
        "⚠️ **但本站缺定价字段**：社媒称「`$0.133`/秒起、未来 7 天 15% 折扣」，**`models/klingai` 与 `pricing` 两页均未出现 `0.133` 与 `7 days`**，故该价格只作社媒口径、不进价格位（避坑 200 同族）。"
        "**⚠️ 048 期就地更新三件事**：**① 模型页路径已迁移** —— 旧路径 `runware.ai/models/klingai` 本轮返回 **HTTP 404 但返回体仍是 845,983 字节的完整 SPA 页面（软 404）**，真实路径是 **`runware.ai/kling-4`**（`200`、529,847 字节、两次抓取关键字段一致）；"
        "**② `$0.133/秒` 的归属被核到** —— 它在一手页上确实存在，逐字 `\"pricingRates\":[{\"amount\":0.133,\"unit\":\"durationSecond\"}]`，但其记录 `coverImage` 指向 `sync-3.jpg`、`capabilities` 含 `io:audio-to-video`、`pricingExamples` 配置为 `segmented-lip-sync` / `audio-driven` —— **属于唇形同步模型 `sync-3`，不是 `Kling 4.0`**；**047 期「不进价格位」的结论不变、理由改为「这个数属于另一个模型」**（048 期避坑 209）；"
        "**③ 047 期记的 `native audio` × 8 / `audio` × 79 取自已失效的旧路径**，正确路径 `/kling-4` 上是 **× 11 / × 89** —— **换 URL 不是「增加」，不同 URL 的字段计数不可相减**（048 期避坑 210）。")

# ---- 2) OpenRouter Models：两层存档连续第二期兑现 + created 语义 ----
old2 = "| OpenRouter Models | https://openrouter.ai/models | — | 一个 Key 试几个模型，看免费档与价格对比 | 048 |"
new2 = "| OpenRouter Models | https://openrouter.ai/models | — | 一个 Key 试几个模型，看免费档与价格对比。**⚠️ 048 期就地更新**：**两层存档机制连续第二期兑现** —— 全量 `463` 与上期**同值**但逐条 diff 定位到 `+openai/gpt-6.1-terra-pro / −ibm-granite/granite-4.0-h-micro`（`+1 −1`）；**并首次明确目录层 `created` =「加入目录时间」而非「厂商发布时间」**（048 期避坑 211） | 048 |"

# ---- 3) OpenAI News RSS：RSS 不是公告全集 ----
old3 = "| **🆕 `OpenAI News RSS`**（`openai.com/news/rss.xml`） | https://openai.com/news/rss.xml"
new3 = "| **🆕 `OpenAI News RSS`**（`openai.com/news/rss.xml`） | https://openai.com/news/rss.xml。**⚠️ 048 期就地更新：RSS 不是公告全集** —— `Addendum to GPT‑6 Astra System Card: GPT‑6.1 Terra`（`Publication` / `Oct 26, 2026`）**只在列表页出现、RSS 里没有**；**RSS 仍是公告时间戳的最优一手源，但要配列表页补全**"

for old, new in ((old1, new1), (old2, new2), (old3, new3)):
    assert old in s, ("台账片段未命中", old[:50])
    s = s.replace(old, new, 1)

io.open(F, "w", encoding="utf-8", newline="").write(s)
print("台账 3 行就地更新完成；条目数未变（282），手写括号计数未动")
