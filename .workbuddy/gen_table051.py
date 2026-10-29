# -*- coding: utf-8 -*-
"""051 期：从 050 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-10-29 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table051.md（纯表格块，供 051 期正文嵌入）。

本期（051）与 050 的差别：
  1) **基准日 10/29（隔日出刊，窗口约 29.4 小时）** —— 「距今 N 天」按「截止日 − 基准日」重算。
  2) 输入结构沿用 047 期起的结构：上期 4.1 表体（57 行）+ 总账全量表体（135 行）= 192 行。
     **4.2 的 24 行已含在总账里、不可重复加**。
  3) 本期重点改写：OpenRouter 免费档（464→457/19/16、8 条消失逐条归因）、Kling 4.0 促销（截止 10/29＝基准日当天）、
     Runware 促销表 13→14、百度 Unlimited OCR 2 流通量（513→8357）、MiniMax M3.1 Flash 流通量（11075→13247）、
     Kimi K3.1 Pro（官方文档确认发布 + 权重 11/4 前）、K2 停新（官方 NOTE 确认）、豆包工作（连续第 5 期空壳）。
  4) 本期新增 5 行：Google Antigravity 个人免费档、Antigravity 科研/安全 6 个月免费档、Gemini 4 Carbon 发布、
     Kimi 文件接口限时免费、Runware pruna-p-video-edit 25% 促销（至 11/3）。
"""
import io
import re
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第050期-2026-10-28.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table051.md"
BASE = date(2026, 10, 29)
PREV = 192


def rows_of(md, start_marker, end_marker=None):
    i = md.index(start_marker)
    j = md.index(end_marker) if end_marker else len(md)
    seg = md[i:j]
    return [l for l in seg.split("\n")
            if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]


md = io.open(SRC_MD, encoding="utf-8").read().replace("\r\n", "\n")
led = io.open(SRC_LED, encoding="utf-8").read().replace("\r\n", "\n")

rows_41 = rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
rows_led = rows_of(led, "## 一、全量表")
assert len(rows_41) == 57, ("050 期 4.1 表体行数", len(rows_41))
assert len(rows_led) == 135, ("总账全量行数", len(rows_led))
body = rows_41 + rows_led
assert len(body) == PREV, (len(body), PREV)

header = "| 活动 | 截止 | 状态 |"
sep = "| --- | --- | --- |"

REWRITE = {}


def build(key, subs, tail=None):
    hits = [l for l in body if key in l]
    assert len(hits) == 1, ("键未唯一命中", key, len(hits))
    out = hits[0]
    for a, b in subs:
        assert a in out, ("片段未命中", key, a[:70])
        out = out.replace(a, b)
    if tail:
        assert out.rstrip().endswith("|")
        out = out.rstrip()[:-1].rstrip() + " " + tail + " |"
    return out


# ---- 1) OpenRouter 免费档：本期 457/19/16，全量 −7、:free 与零价同值 ----
REWRITE["🟢 **OpenRouter 免费档（**官方 API 目录口径"] = build(
    "🟢 **OpenRouter 免费档（**官方 API 目录口径",
    [
        ("**官方 API 目录口径 · `464/19/16`**", "**官方 API 目录口径 · `457/19/16`**"),
        ("**⚠️ （050 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-28 09:0x，"
         "**本轮连抓四次、四次读数完全一致**）**：**全量 `464` / 零价 `19` / `:free` `16`**；"
         "**与 049 期（463/19/16）比：全量 `+1`、零价同值、`:free` 同值**。",
         "**⚠️ （051 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-29 14:0x，"
         "**本轮连抓三次、三次读数完全一致**）**：**全量 `457` / 零价 `19` / `:free` `16`**；"
         "**与 050 期（464/19/16）比：全量 `−7`、零价同值、`:free` 同值**。"),
    ],
    tail="**⚠️ （051 期）全量逐条 diff（本期新立避坑 224/225）**：**新增 `1` 条 —— `particle-ai/particle-1`**"
         "（一手字段：`prompt $0.00000025` / `completion $0.000001` 每 1M、`ctx 1,048,576`、"
         "`created 1793207893` ＝ **北京 10/28 21:18**；**⚠️ 这是「极低价」不是「零价」**，"
         "**它进了全量、没进零价、也没进 `:free`**）；"
         "**消失 `8` 条 —— `openai/gpt-4-turbo`、`openai/o1`、`openai/o1-pro`、`openai/o3-mini`、"
         "`openai/o3-mini-high`、`openai/o4-mini`、`openai/o4-mini-high`、`qwen/qwen3-next-80b-a3b-thinking`**；"
         "**`+1 −8 = −7`，与总数差 `464 → 457` 完全对得上** ✔。"
         "**⚠️ 消失的 8 条，本期逐条查了「同系列替身还在不在」（避坑 214 的正确用法）—— "
         "8 条的同名替身全不在，但同厂商相关档全部仍在**（`openai/gpt-4-turbo:batch`、`openai/gpt-4.1-mini`、"
         "`openai/gpt-4o-mini` 等），**即「消失的是这一批旧档，不是这一批能力」**。"
         "**⚠️ 归因结构本身是本期最有价值的信息：消失的 8 条里 7 条是 `OpenAI` 旧模型、只有 1 条是 `Qwen`** —— "
         "**只报「掉了 7 条」等于把结构信息丢掉**（避坑 224）。"
         "**⚠️ 本报告不写「`OpenAI` 下架了模型」** —— 本期实访的是分发层目录，"
         "**厂商侧 `platform.openai.com/docs/models` 连续第 4 期 `403`**，"
         "**分发层下架与厂商侧下架是两件事**（避坑 221 同族）。"
         "**⚠️ `freellm.net` 首页计数器（读于 2026-10-29 14:0x）逐项记账**："
         "**`Models Tracked` `541`（050 期 `534`，`+7`）、`Free & Online` `306`（`303`，`+3`）、"
         "`Providers` `31`（同值）、`No Credit Card` `459`（`452`，`+7`）、"
         "「经实时 API 验证」`249`（`243`，`+6`）** —— "
         "**五项上升、一项同值，即 050 期记的「六项全部同值、048→049 是一次性推进」本期被推翻**（避坑 216）。"
         "**⚠️ 但 `freellm` 的 `Latest free LLM API model update` 仍写 `2026-10-27` —— "
         "即它自己记的「最近一次模型更新」比本期基准日早两天**（避坑 208 同族："
         "**日期字段要连着「这个数字代表什么」一起读**）。",
)

# ---- 2) Kling 4.0 的 15% 促销：截止 10/29 ＝ 本期基准日当天（新立避坑 223）----
REWRITE["🟢 **`Runware` 分发层 `Kling 4.0` 促销 `15% OFF`（**官方 `pricing` 页促销数组"] = build(
    "🟢 **`Runware` 分发层 `Kling 4.0` 促销 `15% OFF`（**官方 `pricing` 页促销数组",
    [
        ("🟢 **生效中（本期新核到一手 · 距结束 2 天）。 且是 `Runware` 分发层的价格活动、不是厂商侧（快手）的免费政策（避坑 41：多站点口径要拆开写）。**",
         "🟢 **官方数组仍列为在售、截止日＝本期基准日当天（新立避坑 223）。 且是 `Runware` 分发层的价格活动、"
         "不是厂商侧（快手）的免费政策（避坑 41：多站点口径要拆开写）。**"),
    ],
    tail="**⚠️ （051 期）截止日＝基准日当天，判定必须分「当天」与「已过」两态** —— "
         "**`endsAt` 是 `2026-10-29`、本期基准日也是 `2026-10-29`，官方促销数组在这一刻仍把它列为在售**；"
         "**本报告因此既不写「已结束」也不写「已过期」**（避坑 223）。"
         "**⚠️ 促销数组逐条 diff（两期同一套结构化解析，避坑 212）：`13` 条 → `14` 条** —— "
         "**新增 `1` 条、消失 `0` 条、其余 `13` 条的 `id`/`title`/`endsAt` 逐条同值**。",
)

# ---- 3) Runware 促销表 13 -> 14：新增 pruna-p-video-edit 25% 至 11/3 ----
REWRITE["🟢 **`Runware` 分发层 `pruna-p-video-upscale` 促销 `50% OFF`（**官方 `pricing` 页促销数组"] = build(
    "🟢 **`Runware` 分发层 `pruna-p-video-upscale` 促销 `50% OFF`（**官方 `pricing` 页促销数组",
    [
        ("🟢 **生效中（本期新核到一手 · 距结束 11 天）。 且是 `Runware` 分发层的价格活动、不是厂商侧（`Pruna`）的免费政策（避坑 41：多站点口径要拆开写）。**",
         "🟢 **生效中（距结束 10 天）。 且是 `Runware` 分发层的价格活动、不是厂商侧（`Pruna`）的免费政策（避坑 41：多站点口径要拆开写）。**"),
    ],
    tail="**⚠️ （051 期）促销表 `13` 条 → `14` 条（新增 `1` 条、消失 `0` 条、其余逐条同值）—— "
         "**新增的那一条是 `pruna-p-video-edit-launch-promo`（`25% OFF`，`endsAt: \"2026-11-03\"`），已单独成行登记**。",
)

# ---- 4) 百度 Unlimited OCR 2：流通量 513 -> 8357 ----
REWRITE["🟢 **`百度` 开源 `文心 Unlimited OCR 2`（**MIT 许可"] = build(
    "🟢 **`百度` 开源 `文心 Unlimited OCR 2`（**MIT 许可",
    [
        ("**`lastModified 2026-10-27T13:35:48Z`（北京 10/27 21:35，落在本期窗口内）**、"
         "**`downloads 513`（049 期 `0`）、`likes 228`（049 期 `0`）**",
         "**`lastModified 2026-10-28T11:28:23Z`（北京 10/28 19:28，落在本期窗口内）**、"
         "**`downloads 8,357`（050 期 `513`）、`likes 323`（050 期 `228`）**"),
    ],
    tail="**⚠️ （051 期）流通量记账（升降都写）**：**`downloads 513 → 8,357`（`+7,844`）、"
         "`likes 228 → 323`（`+95`）** —— **050 期记的「`downloads 0` 是仓库创建不足一天，不是没人用」"
         "（避坑 165）本期得到实证**。"
         "**⚠️ 但 `lastModified` 落在窗口内只说明「仓库有更新」，不说明「下载增长发生在窗口内」** —— "
         "**本报告因此写「本期读数」，不写「窗口内下载增长 `+7,844`」**（避坑 211：目录层时间戳 ≠ 事件时间）。"
         "**⚠️ 另注：`ModelScope` 侧本期返回体无 `downloads`/`likes` 字段，上期记的 `416` 本期无同口径读数可比 —— "
         "**本报告本期不写 `ModelScope` 的下载量**（避坑 210）。",
)

# ---- 5) MiniMax M3.1 Flash：流通量 11075 -> 13247 ----
REWRITE["🟢 **`MiniMax` `M3.1 Flash` 开放权重（**权重 10/17 就已在 `HF`"] = build(
    "🟢 **`MiniMax` `M3.1 Flash` 开放权重（**权重 10/17 就已在 `HF`",
    [
        ("**⚠️ （050 期）`HF` 字段重取（`hf-mirror.com`，读于 2026-10-28 09:0x，"
         "**详情端点连读两次** + 列表端点各一次）**：**详情 `downloads` `8,782` / `likes` `371`（两次读数完全一致）；"
         "列表端点仍为 `22` 个仓库**",
         "**⚠️ （051 期）`HF` 字段重取（`hf-mirror.com`，读于 2026-10-29 14:0x，"
         "**详情端点连读两次** + 列表端点各一次）**：**详情 `downloads` `13,247` / `likes` `450`（两次读数完全一致）；"
         "列表端点仍为 `22` 个仓库**"),
    ],
    tail="**⚠️ （051 期）流通量记账（升降都写）**：**`downloads 11,075 → 13,247`（`+2,172`）、"
         "`likes 413 → 450`（`+37`）**；`createdAt` `2026-10-17T06:37:50Z` 与 `lastModified` "
         "`2026-10-26T07:08:15Z` **均未变**（⚠️ 即本期增长没有伴随仓库更新）。"
         "**⚠️ 与 050 期同款的提醒**：`HF` 的 `likes` 在列表端点与详情端点仍可能有差（本报告取详情端点），"
         "**两个口径不合并取中间值**（避坑 161）。",
)

# ---- 6) Kimi K3.1 Pro：官方文档确认发布 + 权重 11/4 前 ----
REWRITE["🟢 **`Moonshot` `Kimi K3.1 Pro` 发布（10/23 晚–10/24"] = build(
    "🟢 **`Moonshot` `Kimi K3.1 Pro` 发布（10/23 晚–10/24",
    [
        ("**11/4 前（官方逐字 `The full model weights will be released by Nov 4.` —— 是「by」不是「on」，未给确切日）**",
         "**11/4 前（官方逐字 `The full model weights will be released by Nov 4.` —— 是「by」不是「on」，未给确切日）**"),
        ("🟢 **已发布可用、权重未落地（第 ④ 级未到）。 ⚠️ 参数口径两个数：官方英文博客与中文文档都写「3T 级 / 3 万亿级」，"
         "而聚合站转引的官方社媒帖写「2.8T 总参数 / 104B 激活」 —— 「级」是约数、社媒数未经本报告一手核实，两个都写、不合并（避坑 161）。**",
         "🟢 **已发布可用、权重未落地（第 ④ 级未到）。 ⚠️ 参数口径两个数：官方英文博客与中文文档都写「3T 级 / 3 万亿级」，"
         "而聚合站转引的官方社媒帖写「2.8T 总参数 / 104B 激活」 —— 「级」是约数、社媒数未经本报告一手核实，两个都写、不合并（避坑 161）。**"),
    ],
    tail="**⚠️ （051 期）官方文档一手复核（050 期挂账项④的部分销项）**："
         "**一手 `platform.kimi.com/docs/guide/kimi-k3-1-pro-quickstart.md`（`200` / `24,922` 字节）逐字** —— "
         "「**Kimi K3.1 Pro 是全新 K3.1 系列的第一个模型，也是我们迄今能力最强的 3 万亿级参数模型，支持 100 万上下文。**」"
         "／「**我们同步推出高速版模型 Kimi K3.1 Pro Highspeed，同等智能，输出速度约 2\\~3 倍。"
         "完整模型权重将于 11 月 4 日前发布。**」／"
         "**`Terminal-Bench 4.0` 得分 `65.7%`，超过 `GPT-6 Astra`（`58.2%`），"
         "与 `Claude Opus 5.5`（`66.4%`）仅有微弱差距**。"
         "**⚠️ 但权重本身尚未放出**：**本期两次实访 `HF` `author=moonshotai` 仍为 `19` 个仓库、"
         "其中只有 `moonshotai/Kimi-K3`（`createdAt 2026-06-13`）、无 `K3.1` 权重仓** —— "
         "**「已发布」与「权重已放出」是两件事**（避坑 219）。"
         "**⚠️ API 侧已可用**：模型 ID `kimi-k3.1-pro` 与 `kimi-k3.1-pro-highspeed`，"
         "`reasoning_effort` 支持 `low`/`high`/`max`（**默认 `max`**），"
         "`Chat Completions` / `Responses` / `Messages` 三种 API 均可用"
         "（一手 `platform.kimi.com/docs/guide/model-list.md`）。"
         "**⚠️ 具体价格表本期仍未取到** —— `Mintlify` 文档站的 `.md` 副本里 `<table>` 是空壳（避坑 212 同族）。",
)

# ---- 7) K2 系列停新：官方 NOTE 确认 ----
REWRITE["🔴 **`Moonshot` `K2` 系列模型停新注册与计划下线（公告见于 `Kimi` 定价页"] = build(
    "🔴 **`Moonshot` `K2` 系列模型停新注册与计划下线（公告见于 `Kimi` 定价页",
    [],
    tail="**⚠️ （051 期）官方口径一手确认（050 期挂账项⑤的部分销项）**："
         "**一手 `platform.kimi.com/docs/pricing/chat.md`（`200` / `3,227` 字节）的 `NOTE` 逐字** —— "
         "「**尊敬的 Kimi 用户，K2 系列模型将于 2026 年 10 月 31 日起停止向新注册用户开放，"
         "已注册用户不受影响；我们计划在 12 月底下线所有 K2 系列模型，请提前做好迁移准备。**」"
         "**⚠️ 销的是「官方口径确认」这一项，「是否如期执行」这一项仍挂账** —— "
         "**要等到 10/31 之后才能核**。"
         "**⚠️ 同期确认的一条免费项**：官方同页逐字「**文件相关接口（文件内容抽取/文件存储）限时免费**，"
         "即您只上传并抽取文档时，文件接口本身不产生费用」—— **但官方未给截止日**，"
         "**本报告不替它排日**（避坑 154/166）；**且 `Kimi API` 整体是「按量计费、不提供订阅制」**，"
         "**所以这一条免费的不是模型调用、是那两个功能接口**（避坑 41：按功能拆开写）。",
)

# ---- 8) 豆包工作 30 天订阅：连续第 5 期未拿到一手 ----
REWRITE["🟢 **豆包工作 30 天订阅（新一轮）**"] = build(
    "🟢 **豆包工作 30 天订阅（新一轮）**",
    [
        ("⚠️ （050 期）本轮实访 `volcengine.com/activity/doubao` 返回 `200` / `67,651` 字节，"
         "但页面是 React 空壳、正文仅 `176` 字、无任何可读字段 —— 连续第 4 期只推天数，本期仍未拿到一手**（避坑 180）",
         "⚠️ （051 期）本轮实访 `volcengine.com/activity/doubao` 返回 `200` / `67,651` 字节，"
         "但页面是 React 空壳、正文仅 `178` 字、无任何可读字段 —— 连续第 5 期只推天数，本期仍未拿到一手；"
         "**本期改访火山方舟文档站 `docs/82379/1399008`（`200` / `949,496` 字节、正文 `27,523` 字），"
         "`免费`/`额度`/`赠送`/`试用` 四词在该页正文零命中** —— **换路径也没拿到，追踪项不销项**（避坑 180）"),
    ],
)

# ---- 9) Anthropic 新版使用政策：标题栏日期推进到 October 29（避坑 208 连续第 3 期）----
REWRITE["🟢 **Anthropic 新版使用政策（含首次禁止虐待模型）**"] = build(
    "🟢 **Anthropic 新版使用政策（含首次禁止虐待模型）**",
    [],
    tail="**⚠️ （051 期）避坑 208 连续第 3 期命中同一处** —— "
         "**`anthropic.com/news` 的 `Latest news` 区块标题栏日期由 `October 28` 推进到 `October 29`，"
         "但列表里的最新条目仍是 `Oct 27, 2026`**（050 期记的是「标题栏 `October 28`、列表最新 `Oct 27`」）；"
         "**标题栏日期会随出刊日逐日推进，它不是任何条目的日期**。"
         "**⚠️ 窗口内 `Anthropic` 一手新增条目数 `0`** —— **本报告写「本期未核到窗口内的新公告」，"
         "不写「本期没有发布」**（避坑 116 同族：「未核到」只说明本报告还没去看）。",
)

# ---- 10) 百度智能云「文档解析（Unlimited-OCR）」API：官方文档更新时间 ----
REWRITE["🟢 **`百度智能云`「文档解析（Unlimited-OCR）」API（**基于 `文心 Unlimited OCR 2`"] = build(
    "🟢 **`百度智能云`「文档解析（Unlimited-OCR）」API（**基于 `文心 Unlimited OCR 2`",
    [
        ("🟢 **生效中（官方文档标注「更新时间：2026-10-27」· 本期新上线）。",
         "🟢 **生效中（官方文档标注「更新时间：2026-10-27」· 050 期新上线）。"),
    ],
)

# ====================== 本期新增 5 行 ======================
# ⚠️ NEW 行末尾必须带 " |"（否则字段数是 2 而不是 3）
NEW = []

NEW.append(
    "| 🟢 **`Google Antigravity` 个人免费档（**官方定价页逐字 `$0/month` · **本报告至今唯一一条「免费上限被官方写明」的额度**）** | "
    "**无结束日（长期免费档 · 官方未给任何活动期或截止日）** | "
    "🟢 **生效中（`antigravity.google/pricing`，`200` / `137,500` 字节）。** "
    "⚠️ 官方逐字：`$0/month`、`Access to a variety of agent models`、`Unlimited Tab completions`、"
    "`Unlimited Command requests`、`Basic weekly rate limits`。** "
    "⚠️ 三条边界：① **只有 `Tab completions` 与 `Command requests` 写 `Unlimited`**，"
    "**`agent models` 本身是 `Basic weekly rate limits`（官方未给具体数字）**；"
    "② **官方未逐个列名免费档可用哪些模型**，本报告不替它列（避坑 116）；"
    "③ **旗舰 `Gemini 4 Argon` 官方写明挂 `Google AI Pro` 与 `Ultra` 两个付费档** —— "
    "**本报告不写「`Antigravity` 免费提供 `Gemini 4`」**（避坑 41）。 "
    "⚠️ 付费三档逐字：`Pro`（`Google AI Pro` · `More rate limits` · `Flexible AI credit pool`）、"
    "`Ultra`（`Google AI Ultra` · `Even more rate limits`）、"
    "组织档（`Business plan via Google Cloud` · `Standard/Plus` 起 `$30 USD per seat per month` · "
    "另有 `Pay-as-you-go plan with $0 seat fee`）。 |"
)

NEW.append(
    "| 🟡 **`Google Antigravity` 科研 / 安全 6 个月免费档（**官方逐字 `for 6 months` · "
    "**本报告至今唯一一条「官方明写期限 + 明写条件」的免费额度**）** | "
    "**6 个月（官方逐字 `free of charge for 6 months` · 起点是获批日，非固定日历日）** | "
    "🟡 **生效中（申请制 · `deepmind.google/models/gemini/`，`200` / `251,576` 字节）。** "
    "⚠️ 官方逐字：「**Academic and independent scientists can apply to get the highest usage tier in "
    "Google Antigravity free of charge for 6 months (subject to eligibility, capacity, and selection) "
    "and cybersecurity defenders can apply to join the Fairwind Program.**」 "
    "⚠️ 三个条件必须原样写出：**① `for 6 months`（期限）② `subject to eligibility, capacity, and selection`"
    "（资格/容量/选拔，三项并列）③ `can apply`（需申请，非自动获得）**。"
    "**⚠️ 网络安全防守方另有一条独立通道 `Fairwind Program`**（官方给 `Join the Fairwind Program` 入口）。 "
    "⚠️ 本报告不写「人人可领 6 个月」—— **这是给特定人群的定向通道，不是普惠额度**（避坑 41）。 |"
)

NEW.append(
    "| 🟠 **`Google` `Gemini 4 Carbon` 发布（**官方逐字 `October 2026` · **闭源旗舰 · 权重不发**）** | "
    "**未公布（官方只给到月份精度 `October 2026`；`Google` 一手本期全线 `000`，具体发布日未核到）** | "
    "🟠 **已发布（官方 `deepmind.google/models/gemini/` 的 `Announcements` 区逐字「**Gemini 4 Carbon: "
    "Our next frontier model — October 2026**」）。** "
    "⚠️ 官方自带**五模型对照表**（`Gemini 4 Carbon` / `Gemini 4 Argon` / `GPT-6 Astra` / `Claude Opus 5.5` / "
    "`Claude Fable 5.1`），逐条实测：**`AA Index v5.0` `59` / `50` / `57` / `58` / `49`**；"
    "**`Terminal-Bench 4.0 (AA)` `65.2%` / `57.1%` / `59.1%` / `59.6%` / `52.0%`**；"
    "**`Agents' Last Exam v1.1` `77.4%` / `69.0%` / `73.1%` / `71.6%` / —**；"
    "**`OSWorld-2.1` `81.5%` / `74.7%` / `80.9%` / `87.2%` / `76.8%`**；"
    "**`Vending-Bench 2` 余额 `$16,484` / `$13,718` / `$15,515` / `$9,235` / `$5,422`**；"
    "**`GraphWalks 256k to 1M` `96.2%` / `84.2%` / `71.8%` / `66.8%` / `65.0%`**；"
    "**`CWE-bench` `71.0%` / `68.0%` / `68.0%` / `67.0%` / `58.0%`**；"
    "**`SEC-bench Pro` `88.2%` / `83.4%` / `85.4%` / — / —**。 "
    "⚠️ **它并非每一项都第一** —— **`OSWorld-2.1` 一栏 `Claude Opus 5.5`（`87.2%`）高于它（`81.5%`）**，"
    "**`FrontierSWE 2` 一栏 `GPT-6 Astra`（`65.5%`）高于它（`61.2%`）** —— "
    "**「哪些第一、哪些不是第一」一起写**（避坑 116：单一榜单口径不等于全面领先）。 "
    "⚠️ 第三方 `Artificial Analysis` 侧同口径 `Intelligence Index` 也是 `59`、排名 `# 1 / 52`，"
    "但 `AA` 自评「`very verbose`（`200M` tokens vs 中位数 `64M`）」—— **两个口径并列、不合并成一个「综合领先」**。 "
    "⚠️ **闭源 · 权重不发** —— **本报告不写「`Gemini 4 Carbon` 可下载」**（避坑 41）。 |"
)

NEW.append(
    "| 🟢 **`Kimi` 文件相关接口限时免费（**官方逐字「文件内容抽取 / 文件存储」· **但 `Kimi API` 整体是按量计费**）** | "
    "**未公布（官方逐字只写「限时免费」，未给截止日；本报告不替它排日）** | "
    "🟢 **生效中（一手 `platform.kimi.com/docs/pricing/chat.md`，`200` / `3,227` 字节）。** "
    "⚠️ 官方逐字：「**文件相关接口（文件内容抽取/文件存储）限时免费，即您只上传并抽取文档时，"
    "文件接口本身不产生费用。**」 "
    "⚠️ 三条边界：① **免费的是「这两个功能接口」，不是模型调用** —— "
    "**官方同一页明确「`Kimi API` 开放平台提供的模型推理服务是『按量计费』模式，不提供订阅制方案」**；"
    "② **官方未给截止日**（避坑 154/166）；③ **文件抽取出的文档内容作为 Input 传输给模型时，"
    "仍按量计费**（官方逐字）—— **两类账不能合并**（避坑 54 同源）。 |"
)

NEW.append(
    "| 🟢 **`Runware` 分发层 `pruna-p-video-edit` 促销 `25% OFF`（**官方 `pricing` 页促销数组 · "
    "**一手核到 · 截止 `11/3`**）** | "
    "**11/3（官方促销数组 `endsAt: \"2026-11-03\"` 逐字）** | "
    "🟢 **生效中（本期新核到一手 · 距结束 5 天）。** "
    "⚠️ **本期 `Runware` 促销表由 `13` 条变成 `14` 条** —— 新增 `1` 条、消失 `0` 条、"
    "**其余 `13` 条的 `id`/`title`/`endsAt` 逐条同值**（两期同一套结构化解析，避坑 212）。 "
    "⚠️ **这是 `Runware` 分发层的价格活动、不是厂商侧（`Pruna`）的免费政策**（避坑 41：多站点口径要拆开写）。 |"
)

# ====================== 组装输出 ======================
out = [header, sep]
for l in body:
    out.append(l)
for l in NEW:
    out.append(l)

text = "\n".join(out) + "\n"
io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)

# 断言：字段数分布
from collections import Counter
cnt = Counter()
for l in out:
    if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |"):
        cnt[len(l.split("|")) - 2] += 1
print("rows:", len(out) - 2, "= %d + %d" % (PREV, len(NEW)))
print("字段数分布:", dict(cnt))
assert set(cnt) == {3}, ("字段数不是全 3", dict(cnt))
print("rewrites:", len(REWRITE))
print("OK ->", OUT)
