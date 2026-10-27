# -*- coding: utf-8 -*-
"""从 048 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-10-27 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table049.md（纯表格块，供 049 期正文嵌入）。

本期（049）与 048 的差别：
  1) **基准日与 048 期同为 10/27**（同日第三轮）—— 「距今 N 天」按「截止日 − 基准日」重算，预期不变；
     但 048 期实测「基准日没变 ≠ 不用重算」（`gen_table` 的 diff 是唯一发现手段）。
  2) 输入结构沿用 047 期起的结构：上期 4.1 表体（55 行）+ 总账全量表体（131 行）= 186 行。
     **4.2 的 18 行已含在总账里、不可重复加**。
  3) 本期重点改写：OpenRouter 免费档（463/19/16，:free 净减 1）、Kling 4.0（15% 折扣上页，
     截止日 10/29 而非社媒的「7 天」）、AutoClaw 两站 M10W4（本轮实访正文页，销项挂账②）、
     MiniMax M3.1 Flash（Unsloth GGUF 一手销项）、freellm 计数器回升。
  4) 本期新增 3 行：文心 Unlimited OCR 2（开源 + 百度云限时免费）、文心 Unlimited OCR 2 的
     百度云 API 免费额度、Runware 的 Kling 4.0 15% 促销（至 10/29）。
"""
import io
import re
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第048期-2026-10-27.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table049.md"
BASE = date(2026, 10, 27)
PREV = 186


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
assert len(rows_41) == 55, ("048 期 4.1 表体行数", len(rows_41))
assert len(rows_led) == 131, ("总账全量行数", len(rows_led))
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
        assert a in out, ("片段未命中", key, a[:50])
        out = out.replace(a, b)
    if tail:
        assert out.rstrip().endswith("|")
        out = out.rstrip()[:-1].rstrip() + " " + tail + " |"
    return out


# ---- 1) OpenRouter 免费档：本期 463/19/16，:free 净减 1，差额 3 条归属已定位 ----
REWRITE["🟢 **OpenRouter 免费档（**官方 API 目录口径"] = build(
    "🟢 **OpenRouter 免费档（**官方 API 目录口径",
    [
        ("**官方 API 目录口径 · `463/20/17`**", "**官方 API 目录口径 · `463/19/16`**"),
        ("**⚠️ （048 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-27 10:1x）**："
         "**全量 `463` / 零价 `20` / `:free` `17`**；**与 047 期（463/20/17）比：三个数全部同值**。",
         "**⚠️ （049 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-27 19:4x，"
         "**本轮连抓三次、三次读数完全一致**）**：**全量 `463` / 零价 `19` / `:free` `16`**；"
         "**与 048 期（463/20/17）比：全量同值、零价 `−1`、`:free` `−1`**。"),
        ("**⚠️ `:free` 17 条逐条 diff：无新增、无消失（连续第 3 期）**；"
         "**「零价 20」与「`:free` 17」仍差 3 个 —— `google/lyria-3-pro-preview`、`google/lyria-3-clip-preview`、"
         "`openrouter/free`（路由器）**（避坑 161）。",
         "**⚠️ `:free` 16 条逐条 diff：消失 `1` 条 —— `nvidia/nemotron-3-super-120b-a12b:free`、无新增**；"
         "**「零价 19」与「`:free` 16」差 `3` 个 —— `google/lyria-3-pro-preview`、`google/lyria-3-clip-preview`、"
         "`openrouter/free`（路由器）**（避坑 161）。"
         "**⚠️ （049 期）销项：这条三期待办的「差额归属」本期第一次说清 —— "
         "本轮实跑逐条定位差额为 `google/lyria-3-clip-preview`（`ctx 1,048,576`）、"
         "`google/lyria-3-pro-preview`（`ctx 1,048,576`）、`openrouter/free`（`ctx 200,000`）—— "
         "**前两条是 `google` 的预览档、第三条是 `OpenRouter` 自己的路由别名、不是第三方模型**；"
         "**另已验证反向差集为空 —— 所有 `:free` 后缀模型的 `prompt` 与 `completion` 都确实是 `0`，"
         "没有「挂着 `:free` 名字但按量收费」的条目** ✔。"),
        ("**⚠️ `freellm.net` 首页计数器（读于 2026-10-27 06:2x）逐项记账**："
         "**Hero `530+ → 531+`；`Models Tracked` `309 → 300`（−9，本期最大单项变动）；"
         "`Providers` `31 → 31`；`No Credit Card` `448 → 449`；「经实时 API 验证」`243 → 243`**",
         "**⚠️ `freellm.net` 首页计数器（读于 2026-10-27 19:5x）逐项记账**："
         "**Hero `531+ → 534+`；`Models Tracked` `300 → 303`（升 `3`）；"
         "`Providers` `31 → 31`；`No Credit Card` `449 → 452`（升 `3`）；「经实时 API 验证」`243 → 243`**"),
        ("**⚠️ `Models Tracked −9` 本报告定位不到具体是哪 9 条**（`freellm` 不提供可存档的模型 ID 清单，只有计数）"
         "—— **如实记「未定位」，不猜**（避坑 44）。",
         "**⚠️ `Models Tracked −9` 本报告定位不到具体是哪 9 条**（`freellm` 不提供可存档的模型 ID 清单，只有计数）"
         "—— **如实记「未定位」，不猜**（避坑 44）。"
         "**⚠️ （049 期）更正 048 期的判断**：048 期记「`Models Tracked` 本期维持 `300`、未回升」—— "
         "**本期已回升到 `303`，该判断本期就地更正**（避坑 216：**「未见回升」是有时效的判断，不是永久结论**）。"
         "**⚠️ 但口径必须写清**：`−9` 是 046→047 的一次性落差、`+3` 是 048→049 的逐期回升，"
         "**两者不是同一口径、不能相减成一个净值** —— **正确表述是「一次性落差未逐条归因」**。"),
        ("**⚠️ `openrouter.ai/announcements` 本轮实访仍停在 `October 14, 2026`**（041–048 连续八期无新限免公告）。",
         "**⚠️ `openrouter.ai/announcements` 本轮实访仍停在 `October 14, 2026`**（041–049 连续九期无新限免公告）。"),
    ],
    tail="**⚠️ （049 期）本期最重要的一条：`nemotron-3-super-120b-a12b:free` 从目录消失，而它的付费档仍在** —— "
         "**仍在目录中**：`nvidia/nemotron-3-super-120b-a12b`（`created 1773245239`、`prompt $0.30` / `completion $2.40` 每 1M、"
         "缓存读 `$0.15`、`ctx 262,144`）；**消失的**：`nvidia/nemotron-3-super-120b-a12b:free`（048 期时是 `prompt 0` / `completion 0`）。"
         "**同系列其余 `:free` 档全部健在**（`nemotron-3-nano-omni-30b-a3b-reasoning:free`、`nemotron-3-ultra-550b-a55b:free`、"
         "`nemotron-3.5-content-safety:free`、`nemotron-3.5-lightning:free`、`nemotron-3.5-super-vl:free`）—— "
         "**消失的是这一系列里唯一「没有付费替身」的那一条**（避坑 214）。"
         "**⚠️ 本报告不写「下架」「停服」「退役」**：**目录层消失 ≠ 厂商撤下模型**，"
         "`NVIDIA` 官方侧状态本轮未实访，如实记「未核到」（避坑 154/161）。"
         "**⚠️ 全量清单同期 `+1 −1`：新增 `openai/gpt-6.1-terra-pro:batch`（`$0.50` / `$2.50` 每 1M，"
         "是 `terra-pro` 的半价批处理档、与 `terra:batch` 同价）、消失 `nvidia/nemotron-3-super-120b-a12b:free`** —— "
         "**`+1 −1 = 0` 与全量总数同值一致** ✔（046 期立的存档机制连续第三期生效）。"
         "**⚠️ 新立避坑 215：差集个数不变 ≠ 没变化** —— 零价 `20` vs `:free` `17` 变成零价 `19` vs `:free` `16`，"
         "**差额个数都是 `3`、但两个集合的绝对值各降了 `1`**（掉的那条同时在两个集合里）；"
         "**报差集时必须同时报两个集合的绝对值**。",
)

# ---- 2) Kling 4.0：本期 15% 折扣在一手页读到，截止日是 10/29 不是社媒的「7 天」 ----
REWRITE["🟢 **快手可灵 Kling 4.0（**"] = build(
    "🟢 **快手可灵 Kling 4.0（**",
    [
        ("**本轮在正确路径 `runware.ai/kling-4` 与 `runware.ai/pricing` 两页均未核到 `0.133` 与 `7 days` 字样**，"
         "**故 `$0.133/秒` 与「15% × 7 天」不进本报告价格位，只作「社媒口径、一手未核到」登记**（避坑 200 同族）。",
         "**本轮在正确路径 `runware.ai/kling-4` 上 `0.133` 与 `7 days` 仍各 `0` 处**（**模型页本身没有这两个数**），"
         "**但 `runware.ai/pricing` 的促销数组里逐字读到了 `15%` 折扣条目 —— "
         "`\"id\":\"klingai-video-4-0-launch-promo\",\"title\":\"15% OFF\","
         "\"description\":\"15% off all generations until October 29, 2026\","
         "\"models\":[\"klingai-video-4-0\"],\"endsAt\":\"2026-10-29\"`**（本期新立避坑 212）。"
         "**⚠️ 更正 047、048 两期的取数方式**：那两期用的是「在页面上数关键词出现几次」，"
         "**而 `048` 期自己的快照 `tmp_048/runware_pricing.html` 里就写着这条促销**"
         "（本期对比：两份文件字节数完全相同 `744,814`、促销数组 `12` 条逐条一致、`15%` 两版各出现 `2` 次）—— "
         "**那两期是「抓到了却没读出来」，不是「这期没找到」**（避坑 212：**关键词计数法会漏掉嵌在 JSON 数组里的结构化字段**）。"
         "**⚠️ 官方给的截止日是 `10 月 29 日`，不是社媒口径的「7 天」** —— "
         "社媒说的是「未来 7 天在常规定价上再享 15% 折扣」（相对、从首发日算），"
         "官方促销数组写的是绝对日期 `October 29, 2026` 且带机器可读的 `endsAt` —— "
         "**两个口径对不上，本报告以官方 `endsAt` 为准、社媒口径原样引录、不取中间值**（本期新立避坑 213）。"
         "**⚠️ 但这是「打 85 折」、不是免费 —— 本行进价格位、不进免费额度位**；"
         "**且该折扣是 `Runware` 分发层的价格活动、不是厂商侧的免费政策**。"),
    ],
    tail="**⚠️ （049 期）本轮一手复读（`runware.ai/kling-4`，读于 2026-10-27 19:5x）**："
         "**`200`、`529,811` 字节、`native audio` 11 处 / `audio` 89 处 / `0.133` 0 处 / `7 days` 0 处 / `15%` 0 处** "
         "—— **与 048 期读数一致**（048 期为 `529,847` 字节，**字节数有微差、字段计数完全一致**，**按避坑 210 只在同 URL 同取法内比**）。"
         "**⚠️ 旧路径 `runware.ai/models/klingai` 本轮返回 `404` + `844,236` 字节完整 SPA（软 404 延续）** —— "
         "**该返回体里 `0.133` 仍指向 `sync-3`（`coverImage` 为 `sync-3.jpg`、`capabilities` 含 `io:audio-to-video`），归属不变**。"
         "**⚠️ 本轮新查：`runware.ai/sync-3` 独立路径返回 `404`（该路径不存在）** —— "
         "**`sync-3` 的定价只能从整站返回体里读到，这正是「按端点找、不要按路径找」的又一例**（避坑 199 同族）。"
         "**⚠️ `Runware` 的新用户额度（本轮一手，`pricing` 页 FAQ）**：逐字「**Yes. New users who sign up with a business email "
         "receive $2 in free credits to explore the platform and test various models.**」—— **注册商业邮箱得 `$2` 免费额度**。",
)

# ---- 3) AutoClaw 国际站 M10W4：本轮实访正文页，矛盾第 3 次仍未改正（销项挂账②的前半） ----
REWRITE["🟢 **智谱 `AutoClaw` 国际站 `M10W4` `Weekly Perk`"] = build(
    "🟢 **智谱 `AutoClaw` 国际站 `M10W4` `Weekly Perk`",
    [
        ("**⚠️ 同页「正文 40 million vs 结尾句 100 million」的矛盾第 2 次实读仍未改正**"
         "（避坑 202 追踪项，048 期本轮未实访该页、**矛盾是否已改本轮未核到**，追踪项不销项）",
         "**⚠️ 同页「正文 40 million vs 结尾句 100 million」的矛盾第 3 次实读仍未改正**"
         "（避坑 202 追踪项，**本期已实访该页正文**，**追踪项不销项**）"),
    ],
    tail="**⚠️ （049 期）本期实访销项（048 期挂账项②）：`autoclaw.z.ai/blog/news/M10W4/` 正文页本轮实访成功** —— "
         "**注意尾斜杠：不带尾斜杠会 `301`，不跟随重定向会拿到 0 字节空文件；空页 ≠ 活动已撤**（避坑 194）。"
         "**本轮取到 `116,957` 字节、正文规则逐字可读**："
         "「**From October 26 to November 1, log in to AutoClaw and get 40 million Tokens.**」／"
         "「**Log in to AutoClaw during the event to claim 40 million Tokens (worth 4,000 credits) — one claim per account.**」；"
         "**结尾句仍是「**Remember to log in to AutoClaw on October 26 — 100 million Tokens are waiting for you!**」"
         "—— 同页两处数字打架，第 3 次实读未改**。"
         "**判定仍以结构化规则（`40M` + `4,000 credits`）为准，结尾句原样引录、不取中间值**。"
         "**⚠️ 048 期那句「本轮未实访该页、矛盾是否已改本轮未核到」本期更正为「已实访、矛盾仍在」**。",
)

# ---- 4) AutoClaw 国内站 M10W4：本轮实访正文页，规则逐字未变（销项挂账②的后半） ----
REWRITE["🟢 **智谱 `AutoClaw` 国内站 `M10W4` 一周福利"] = build(
    "🟢 **智谱 `AutoClaw` 国内站 `M10W4` 一周福利",
    [
        ("**⚠️ （048 期）本轮未再实访该页正文（046 期已逐字核过、047 期未复访），只按活动期推进状态 —— 如实写「未复访」**",
         "**⚠️ （049 期）本轮已实访该页正文（`autoclaw.zhipuai.cn/blog/news/M10W4/`，同样需带尾斜杠），"
         "**规则逐字未变** —— 048 期记的「未复访」本期补上**"),
    ],
    tail="**⚠️ （049 期）本期实访销项（048 期挂账项②）：`autoclaw.zhipuai.cn/blog/news/M10W4/` 正文页本轮实访成功** —— "
         "**取到 `120,337` 字节**，逐字："
         "「**10 月 26 日至 11 月 1 日，登录 AutoClaw，即得 1 亿 Tokens。**」／"
         "「**活动时间：10 月 26 日（周一）00:00—11 月 1 日（周日）23:59（北京时间）**」／"
         "「**活动规则：登录 AutoClaw，即可领取 1 亿 Tokens（相当于 10,000 积分），每个账号限领一次。**」；"
         "**国内站同页无「40M vs 100M」那处矛盾**（结尾句「1 亿 Tokens 等你领取！」与正文一致）。"
         "**⚠️ 048 期那句「本轮实访清单：抓取了列表页但正文页未取到可读文本」本期更正为「正文页已实访」**（避坑 194 同族）。",
)

# ---- 5) MiniMax M3.1 Flash 开放权重：本期详情端点两次一致 + Unsloth GGUF 一手销项 ----
REWRITE["🟢 **`MiniMax` `M3.1 Flash` 开放权重"] = build(
    "🟢 **`MiniMax` `M3.1 Flash` 开放权重",
    [
        ("**⚠️ （048 期）`HF` 字段重取（`hf-mirror.com`，读于 2026-10-27 09:3x，**详情端点连读两次** + 列表端点 + 按 `downloads` 排序的列表端点各一次）**："
         "**详情 `downloads` `8,782` / `likes` `371`（两次读数完全一致）；列表 `downloads` `8,782` / `likes` `382`**",
         "**⚠️ （049 期）`HF` 字段重取（`hf-mirror.com`，读于 2026-10-27 19:4x，**详情端点连读两次** + 列表端点各一次）**："
         "**详情 `downloads` `8,782` / `likes` `371`（两次读数完全一致）；列表端点仍为 `22` 个仓库**"),
        ("**⚠️ 流通量记账（升降都写）**：**详情 `downloads` `8,782 → 8,782`（同值）；列表 `7,355 → 8,782`（升 `1,427`）；"
         "`likes` 详情 `371 → 371`（同值）、列表 `360 → 382`（升 `22`）**。",
         "**⚠️ 流通量记账（升降都写）**：**详情 `downloads` `8,782 → 8,782`（同值）、`likes` `371 → 371`（同值）、"
         "`lastModified 2026-10-26T07:08:15Z` 不变**；**列表端点 `22` 个仓库（与 048 期同值）**。"),
        ("**⚠️ 本期新增一条「能跑」侧的第三方证据**：**`Unsloth` 10/26 发布 `MiniMax-M3.1-Flash` 的 GGUF 量化**"
         "（2-bit 体积 −45%、保留 91.5% top-1；1-bit 约 89.9%；4-bit `UD-Q4_K_XL` 达 98.0%；**可在 150GB 内存上本地运行**）"
         "—— **这是「开放权重」从「能下载」走到「能在本地跑」的一手旁证，但它是第三方量化、不是官方权重本身**（避坑 197 四层结构）。",
         "**⚠️ 「能跑」侧的第三方证据（本期补上一手仓库，048 期挂账项⑨销项）**："
         "**`hf-mirror.com/api/models?author=unsloth&search=MiniMax-M3.1-Flash` 本轮返回 `2` 个仓库** —— "
         "`unsloth/MiniMax-M3.1-Flash-GGUF`（`downloads 7,179`、`createdAt 2026-10-23`）与 "
         "`unsloth/MiniMax-M3.1-Flash`（`downloads 399`、`createdAt 2026-10-23`）。"
         "**⚠️ 但 048 期转述的那组数（2-bit 体积 −45%、保留 91.5% top-1、1-bit 约 89.9%、4-bit `UD-Q4_K_XL` 达 98.0%、"
         "可在 150GB 内存上本地运行）本轮只核到「仓库存在」这一层 —— 模型卡正文未读，那组数仍是转述**（避坑 200）。"
         "**⚠️ 另注意一个日期差**：048 期写「`Unsloth` 10/26 发布」，而一手 `createdAt` 是 **`2026-10-23`** —— "
         "**仓库创建在 10/23，「发布」与「创建」不是同一个时刻**（避坑 211 同源）。"
         "**这仍是「开放权重」从「能下载」走到「能在本地跑」的一手旁证，但它是第三方量化、不是官方权重本身**（避坑 197 四层结构）。"),
    ],
    tail="**⚠️ （049 期）另记一条取数纪律的延续**：`hf-mirror.com/api/models?sort=trending` 本轮**仍**返回 "
         "`{\"error\":\"✖ Invalid sort parameter: trending\"}` —— **连续第 2 期失效**，"
         "**本报告因此继续不写「trending 榜前 N 名」**（避坑 44 同族）。"
         "**⚠️ 但本期新开了 `search=` 形态的搜索端点并取到了新数据** —— "
         "`hf-mirror.com/api/models?search=Unlimited-OCR` 返回 `30` 条结果，"
         "**用途是「查某模型有没有官方仓库、有哪些第三方量化版」，比逐个猜 `author` 快得多**。",
)

# ---- 6) o4-mini：状态列那句「距今 −4 天」是**解释性引述**，不是活倒计时；本期仍需显式 REWRITE ----
# ⚠️ 048 期把它改写成了「脚本会把它算成『距今 −4 天』」这句说明 —— 这句里的负值会被 049 期的负值断言当成真负值，
# 所以本期必须再改一次（把负值写成「负 4 天」的文字形式）。**这是「非幂等改写的连锁反应」：改一次留个坑，下一期还得再改。**
REWRITE["⚪ **OpenAI `o4-mini` API 停用**"] = build(
    "⚪ **OpenAI `o4-mini` API 停用",
    [
        ("**044 期该行写「距今 1 天」、047 期重算为 `0`，048 期按基准日 10/27 距停用日 4 天，仍归 `over` 档**",
         "**044 期该行写「距今 1 天」、047 期重算为 `0`，048 期与 049 期按基准日 10/27 距停用日 4 天，仍归 `over` 档**"),
        ("**⚠️ （048 期）本行显式改写的原因**：状态列里那句「044 期记为『距今 1 天』」是**引述历史**，"
         "**不是本行的活倒计时** —— 脚本的 `DAYS_RE` 会把它当成活字段重算成「距今 −4 天」（负值）。"
         "**内嵌形态脚本管不到，由每期显式 `REWRITE` 兜底**（与 `AgentCore` 同一处置）。",
         "**⚠️ （049 期）本行仍需显式改写**：状态列里那句「044 期记为『距今 1 天』」是**引述历史**，"
         "**不是本行的活倒计时** —— 脚本的 `DAYS_RE` 会把它当成活字段重算成一个负值天数。"
         "**内嵌形态脚本管不到，由每期显式 `REWRITE` 兜底**（与 `AgentCore` 同一处置）。"
         "**⚠️ 本期顺手修掉 048 期留下的一处自伤**：048 期把改写理由写成「会把它算成『距今 −4 天』（负值）」—— "
         "**那句里的负值字面量本身就会被本期脚本的负值断言当成真负值**，**本行因此连续两期被显式改写**。"
         "**教训**（避坑 217）：**在一行里写出「某个数是负的」这句话，那个数就会真的被读成负数** —— "
         "**说明性文字里的数字照样会被解析器看见**。"),
    ],
)

# ---- 7) 腾讯元器：截止列三个日期，状态列三个手算的「距今」—— 逐条手算，不让脚本重算 ----
REWRITE["🔴 **腾讯智能体平台「元器」停止服务"] = build(
    "🔴 **腾讯智能体平台「元器」停止服务",
    [
        ("🔴 **倒计时中，四个日期必须分开排（048 期逐行手算，不用脚本）**",
         "🔴 **倒计时中，四个日期必须分开排（049 期逐行手算，不用脚本）**"),
    ],
    tail="**⚠️ （049 期）本期基准日与 048 期同为 10/27，故三个「距今」数（`2 / 13 / 74`）全部不变 —— "
         "**这是「同基准日就不变」的正常结果，不是漏改**。"
         "**⚠️ 本行仍是「脚本解析不到状态列倒计时」的标准样本**：截止列有三个日期，"
         "`DAYS_RE.sub` 会把状态列三个「距今」全部替换成截止列第一个日期算出的同一个值，"
         "**故每期显式 `REWRITE`、按基准日逐条手算**。",
)

# ---- 8) DeepSeek Search/Fetch：048 期未重算的继承误差（脚本 diff 抓出）+ 期数推进 ----
# ⚠️ 基准日与 048 期同为 10/27，但 048 期这一行写的是「距今 9 天」—— 那是 047 期基准日（10/23）算出来的值，
# **048 期没有重算就沿用了**。**这正是「基准日没变 ≠ 不用重算」的第二个样本**：
# 基准日没变不代表上期算对了，上期可能压根没算。
REWRITE["🟡 **`DeepSeek Search` / `Fetch` 两个 API 开放"] = build(
    "🟡 **`DeepSeek Search` / `Fetch` 两个 API 开放",
    [
        ("🟡 **生效中（免费窗口内 · 距今 9 天）**",
         "🟡 **生效中（免费窗口内 · 距今 5 天）**"),
        ("**（045 期）回扫 `api-docs.deepseek.com/updates`（Change Log）实访；048 期本轮未复访该页**："
         "**最新条目仍是 `Date: 2026-10-17`（`Opening up the in-house search API` + `DeepSeek-V4.1-Flash-1017 Update`），"
         "其后无任何新条目** —— **即 `DeepSeek` 侧连续第 7 期无新发布**。",
         "**（045 期）回扫 `api-docs.deepseek.com/updates`（Change Log）实访；048/049 两期均未复访该页**："
         "**最新条目仍是 `Date: 2026-10-17`（`Opening up the in-house search API` + `DeepSeek-V4.1-Flash-1017 Update`），"
         "其后无任何新条目** —— **即 `DeepSeek` 侧连续第 8 期无新发布**。"),
        ("**⚠️ （048 期）本轮未实访该 Change Log —— 「连续第 7 期」按期数推进，不按实访结果重数**（避坑 180）。",
         "**⚠️ （049 期）本轮仍未实访该 Change Log —— 「连续第 8 期」按期数推进，不按实访结果重数**（避坑 180）。"),
    ],
    tail="**⚠️ （049 期）本行的「距今 N 天」是 048 期漏重算的继承误差，本期由 `gen_table` 的 diff 输出抓出并修正**："
         "**截止列 `11/1`、基准日 `10/27` → 真值 `5` 天，而 048 期写的是 `9` 天（那是 047 期基准日 `10/23` 算出来的值）**。"
         "**⚠️ 这是「基准日没变 ≠ 不用重算」的第二个样本** —— **基准日没变不代表上期算对了，上期可能压根没算**；"
         "**`gen_table` 的 diff 输出是唯一发现手段**（040 期滚雪球教训，048 期脚注已立，本期再度实测命中）。",
)

# ---- NEW 行 1：文心 Unlimited OCR 2 开源（权重侧，MIT，无结束日） ----
NEW = []

# ---- NEW 行 2：文心 Unlimited OCR 2 的百度云 API 免费额度（限时免费 + 明确页数，有额度无结束日） ----
NEW.append(
    "| 🟢 **`百度` 开源 `文心 Unlimited OCR 2`（**MIT 许可 · 权重 `HF` 已上架 · 官方模型卡 Release 行 `[2026/10/27]` · "
    "`SR-SWA` 任意页数文档解析**）** | "
    "**无结束日（权重永久开放，`MIT` 许可；官方未给任何活动期或截止日）** | "
    "🟢 **已开放权重（第 ④ 级已到 · 本期新发布）**。"
    "**官方一手（`huggingface.co/baidu/Unlimited-OCR-2`，本轮实访）**：`license: mit`、`gated: false`、"
    "**`26` 个文件**（含 `model-00001-of-00002.safetensors`、`model-00002-of-00002.safetensors`、"
    "技术报告 `Unlimited-OCR-2.pdf`、`wheel/` 下的 `SGLang` 定制 wheel）、"
    "`createdAt 2026-10-26T03:57:46Z`（＝北京 10/26 11:57）、`lastModified 2026-10-26T14:05:44Z`、"
    "`pipeline_tag image-text-to-text`、tags 含 `baidu` / `vision-language` / `ocr` / `custom_code`。"
    "**官方一手（`github.com/baidu/Unlimited-OCR` 与 `api.github.com/repos/baidu/Unlimited-OCR`）**："
    "`license.spdx_id = MIT`、`stargazers_count 28,923`、`forks_count 3,067`、`open_issues_count 93`、"
    "**`pushed_at 2026-10-27T02:47:43Z`（＝北京 10/27 10:47，落在本期窗口内）**。"
    "**官方模型卡逐字（`## Release` 首行）**：「**We release Unlimited OCR 2, achieving unlimited-horizon parsing with SR-SWA.**」"
    "**⚠️ 四层开放（避坑 41）**：**① 能用 —— 权重免登录直接下载、`gated: false` "
    "② 能下载 —— 两个 `safetensors` 分片 + 技术报告 + `ModelScope` 同步上架（`PaddlePaddle/Unlimited-OCR-2`，`license: mit`）"
    "③ 能跑 —— 官方逐字「**supports Transformers (native, for quick tests) and SGLang (recommended for serving)**」，"
    "实测环境逐字「**Tested with Python 3.10, `torch==2.13.0`, `transformers==4.52.1`, `huggingface-hub==0.36.0`, "
    "`tokenizers==0.21.4`, on an NVIDIA A800-80GB**」"
    "④ 能商用 —— `MIT`（`HF` 模型卡与 `GitHub` API 两处独立来源一致）**。"
    "**⚠️ 机制与官方逐字**：**`Sparse Reference Sliding Window Attention (SR-SWA)`** —— "
    "「**Compresses text-visual attention interactions from ultra-long sequences down to a fixed-size set of working "
    "references (e.g., 512 tokens). This bounds computational complexity, keeping per-step decoding latency and memory "
    "footprint nearly constant regardless of document length.**」；"
    "「**achieves true, unbounded document parsing within a finite context window**」。"
    "**⚠️ 三条边界**：**① 「任意页数」≠「无限上下文」** —— 官方自己写的是「有限上下文窗口内的无界解析」；"
    "**② 官方基准分只在 `assets/leaderboard.png` 图片里，正文无数字** —— "
    "「`MPDocBench` / `MarathonDocBench` 达 SOTA」是官方定性表述，"
    "「`84.6` / `77.1` 分」与被超越模型清单目前只有媒体转述（避坑 116）；"
    "**③ `HF` 上 `downloads 0` 是仓库创建不足一天，不是没人用**（避坑 165；对照上一代 `baidu/Unlimited-OCR` "
    "已 `2,771,148` 下载 / `4,901` like）**。"
    "**⚠️ 显存调参（官方逐字，对本报告读者最有用的一段）**："
    "「**`--mem-fraction-static` … `0.75` leaves too little headroom at 32+ concurrent requests; `0.7` is stable.**」／"
    "「**`--max-prefill-tokens` … `4096 -> 2048` halves that peak.**」／"
    "「**The built-in default (512) allows a single ~462 MiB allocation and can OOM; 64 is equivalent with a lower peak.**」。"
    "**⚠️ 窗口归属**：`HF` 仓库 `createdAt` 是 10/26 11:57（**落在 048 期窗口内**），"
    "但**官方 Release 行、`GitHub` `pushed_at`（10/27 10:47）、百度云文档「更新时间：2026-10-27」三处一致落在本期窗口内** —— "
    "**发布日以厂商一手为准（避坑 211）**。 |",
)

# ---- NEW 行 3：百度云「文档解析（Unlimited-OCR）」API 限时免费 + 明确免费页数额度 ----
NEW.append(
    "| 🟢 **`百度智能云`「文档解析（Unlimited-OCR）」API（**基于 `文心 Unlimited OCR 2` · **限时免费** · "
    "**个人实名 200 页 / 企业实名 1000 页** · 免部署**）** | "
    "**官方未给结束日（逐字只写「接口限时免费」，未写截止日；免费额度按页数计）** | "
    "🟢 **生效中（官方文档标注「更新时间：2026-10-27」· 本期新上线）**。"
    "**官方一手（`cloud.baidu.com/doc/OCR/s/fmr1p39gb`，本轮实访 `200` / `229,454` 字节）逐字**："
    "「**更新时间：2026-10-27**」；「**文档解析（Unlimited-OCR）：基于最新 文心Unlimited-OCR 2 ，"
    "提供开箱即用、免部署的API调用服务，跨页表格、段落自动合并，标题层级精准解析，"
    "可直接返回 JSON/Markdown 结构化输出**」；"
    "「**接口限时免费，欢迎进行体验与咨询反馈！个人实名可获取免费测试资源 200 页，"
    "企业实名可获取免费测试资源 1000 页。**」；"
    "「**文档解析（Unlimited-OCR）API服务为异步接口，需要先调用提交请求接口获取 task_id，"
    "然后调用获取结果接口进行结果轮询，建议提交请求后 5～10 秒轮询。提交请求接口 QPS为2，获取结果接口 QPS为5。**」"
    "**⚠️ 四层开放（避坑 41）**：**① 能用 —— 免部署、免训练、官方 API 直连，**限时免费且有明确免费页数额度**"
    "（个人实名 `200` 页 / 企业实名 `1,000` 页）② 能下载 —— 对应权重另见上一行（`MIT` 开放）"
    "③ 能跑 —— 免部署、异步提交 + 轮询（QPS 2 / 5），**本地无需 GPU** ④ 能商用 —— API 侧官方未写商用条款，"
    "**权重侧 `MIT` 覆盖商用（两者是不同物、不可混）**。"
    "**⚠️ 三条必须写清的边界**：**① 官方只写「限时免费」、没给结束日 —— 本行不替它排日**（避坑 154/166）；"
    "**② 免费资源是「页数」不是「次数」** —— 与 `OpenRouter` 的「50 次/日」是两种计量，不可换算（避坑 41/161）；"
    "**③ 实名认证是前置门槛** —— **个人实名 `200` 页、企业实名 `1,000` 页**，**企业额度是个人额度的 5 倍**；"
    "**「免费测试资源」这个措辞本身暗示它是测试额度而非长期免费额度**（避坑 154）。"
    "**⚠️ 本行与权重行是两条独立的开放路径** —— **权重是永久 `MIT` 开放、API 是限时免费且有额度**，"
    "**不可合并成一句「免费无限用」**。 |",
)

# ---- NEW 行 4：Runware 的 Kling 4.0 15% 促销（至 10/29，有确切截止日） ----
NEW.append(
    "| 🟢 **`Runware` 分发层 `Kling 4.0` 促销 `15% OFF`（**官方 `pricing` 页促销数组 · **一手核到** · "
    "**截止 `10/29` —— 与社媒口径的「7 天」不同**）** | "
    "**10/29（官方促销数组 `endsAt: \"2026-10-29\"` 逐字；描述逐字「until October 29, 2026」）** | "
    "🟢 **生效中（本期新核到一手 · **距结束 2 天**）**。"
    "**官方一手（`runware.ai/pricing`，本轮实访）逐字**："
    "`\"id\":\"klingai-video-4-0-launch-promo\",\"title\":\"15% OFF\","
    "\"description\":\"15% off all generations until October 29, 2026\","
    "\"models\":[\"klingai-video-4-0\"],\"endsAt\":\"2026-10-29\"`。"
    "**⚠️ 这是「打 85 折」、不是免费** —— **进价格位、不进免费额度位**；"
    "**且是 `Runware` 分发层的价格活动、不是厂商侧（快手）的免费政策**（避坑 41：多站点口径要拆开写）。"
    "**⚠️ 与社媒口径的差异（避坑 213）**：社媒口径是「**未来 7 天**在常定期价上再享 `15%` 折扣」（相对、从首发日算），"
    "官方促销数组给的是绝对日期 `October 29, 2026` 且带机器可读 `endsAt` —— "
    "**两者对不上（首发 10/26 前后 +7 天 ≈ 11/2，官方写 10/29，差 3–4 天）**；"
    "**本报告以官方 `endsAt` 为准、社媒口径原样引录、不取中间值、不擅自换算**（避坑 161）。"
    "**⚠️ 更正 047、048 两期**：那两期连续写下「一手未核到、不进价格位」—— "
    "**本期证实 `048` 期自己的快照 `tmp_048/runware_pricing.html` 里就写着这条促销**"
    "（两份文件字节数完全相同 `744,814`、促销数组 `12` 条逐条一致）—— "
    "**那是「抓到了却没读出来」，不是「这期没找到」**（避坑 212）。"
    "**⚠️ `Runware` 的新用户免费额度（本轮一手，`pricing` 页 FAQ）逐字**："
    "「**Yes. New users who sign up with a business email receive $2 in free credits to explore the platform "
    "and test various models.**」 —— **注册商业邮箱得 `$2` 免费额度**（**这是另一条线，不要与本行的 `15%` 折扣相加**）。 |",
)

# ---- 应用 REWRITE ----
out = []
rw = 0
for l in body:
    hit = None
    for k, v in REWRITE.items():
        if k in l:
            assert hit is None, ("一行命中多个 REWRITE 键", k)
            hit = (k, v)
    if hit:
        assert hit[1] != l, ("REWRITE 与源行相同（等于没改）", hit[0][:40])
        out.append(hit[1])
        rw += 1
    else:
        out.append(l)
assert rw == len(REWRITE), ("命中的 REWRITE 数量不对", rw, len(REWRITE))
for k, v in REWRITE.items():
    assert sum(1 for l in out if l == v) == 1, ("REWRITE 值未唯一出现在输出中", k[:40])

# ---- 天数重算：基准日与 048 期同为 10/27，预期无变化，但断言逐行成立 ----
DAYS_RE = re.compile(r"距今\s*(-?\d+)\s*天")


def parse_cut(l):
    cells = [c.strip() for c in l.strip().strip("|").split("|")]
    if len(cells) < 2:
        return None
    due = cells[1].replace("**", "")
    for pat in (r"(\d{4})[-年](\d{1,2})[-月](\d{1,2})", r"(\d{1,2})/(\d{1,2})"):
        m = re.search(pat, due)
        if m:
            try:
                if m.group(0)[0].isdigit() and len(m.group(0)) > 4 and "/" in m.group(0):
                    return date(2026, int(m.group(1)), int(m.group(2)))
                if len(m.groups()) == 3:
                    return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                return date(2026, int(m.group(1)), int(m.group(2)))
            except ValueError:
                continue
    return None


def recompute(l):
    if "距今" not in l:
        return l
    d = parse_cut(l)
    if d is None:
        return l
    return DAYS_RE.sub("**距今 %d 天**" % (d - BASE).days, l)


before_snapshot = list(out)
out = [recompute(l) if l not in REWRITE.values() else l for l in out]

diff = []
for before, after in zip(before_snapshot, out):
    m = DAYS_RE.search(before)
    if not m or before in REWRITE.values():
        continue
    d = parse_cut(before)
    if d is None:
        continue
    truth = (d - BASE).days
    if int(m.group(1)) != truth:
        diff.append((after.split("|")[1][:46].strip(), m.group(1), truth))

bad = []
for l in out:
    m = DAYS_RE.search(l)
    if not m or l in REWRITE.values():
        continue
    d = parse_cut(l)
    if d is None:
        continue
    truth = (d - BASE).days
    if int(m.group(1)) != truth:
        bad.append((m.group(1), truth, l.split("|")[1][:40]))

neg = [l.split("|")[1][:40] for l in out
       if "距今 -" in l and l not in REWRITE.values() and l not in NEW]
assert not neg, ("出现负值天数", neg)

print("recomputed rows with 距今:", len([l for l in out if DAYS_RE.search(l)]))
print("before -> after diff (行名 / 旧值 -> 真值), 共 %d 行:" % len(diff))
for name, a, b in diff:
    print("   %-46s %s -> %s" % (name, a, b))
assert not bad, ("重算结果不等于按截止列算出的真值", bad)

# ---- 新行插在 ⚪ 存档块锚点之前 ----
anchor_idx = None
for i, l in enumerate(out):
    if l.startswith("| ⚪ **DeepSeek 10/15"):
        anchor_idx = i
        break
if anchor_idx is None:
    for i, l in enumerate(out):
        if l.startswith("| ⚪ **"):
            anchor_idx = i
            break
assert anchor_idx is not None, "未找到 ⚪ 存档块锚点"
out = out[:anchor_idx] + NEW + out[anchor_idx:]

assert len(out) == PREV + len(NEW), (len(out), PREV + len(NEW))

from collections import Counter

print("field-count distribution:", Counter(len(l.split("|")) - 2 for l in out))

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(header + "\n" + sep + "\n")
    f.write("\n".join(out) + "\n")

print("rows: %d (%d + %d new) / rewrites: %d" % (len(out), PREV, len(NEW), rw))
