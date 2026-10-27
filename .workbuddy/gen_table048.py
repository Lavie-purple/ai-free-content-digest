# -*- coding: utf-8 -*-
"""从 047 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-10-27 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table048.md（纯表格块，供 048 期正文嵌入）。

本期（048）与 047 的差别：
  1) **基准日与 047 期同为 10/27**（同日第二轮增补轮）—— 「距今 N 天」全部不变，
     recompute 断言仍然逐行验「天数 == 截止日 − 基准日」，但预期 diff 为空。
  2) 输入结构变化：047 期起第四章已拆 4.1/4.2，未变动的常驻权益在《常驻权益总账》；
     本脚本的输入 = 上期 4.1 表体（55 行）+ 总账全量表体（130 行）= 185 行。
  3) 10 行显式 REWRITE + 1 行新增（OpenAI Signals v3.0 数据集）。
  4) 本脚本的 REWRITE 一律「源行 + 精确片段替换 + 本期新增段落」，
     替换前逐条 assert 命中，避免「静默没改」。
"""
import io
import re
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第047期-2026-10-27.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table048.md"
BASE = date(2026, 10, 27)
PREV = 185


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
assert len(rows_41) == 55, ("047 期 4.1 表体行数", len(rows_41))
assert len(rows_led) == 130, ("总账全量行数", len(rows_led))
body = rows_41 + rows_led
assert len(body) == PREV, (len(body), PREV)

header = "| 活动 | 截止 | 状态 |"
sep = "| --- | --- | --- |"

REWRITE = {}


def build(key, subs, tail=None):
    """按唯一子串定位源行 -> 逐条精确替换 -> 可选在状态列末尾追加 -> 返回新整行。"""
    hits = [l for l in body if key in l]
    assert len(hits) == 1, ("键未唯一命中", key, len(hits))
    out = hits[0]
    for a, b in subs:
        assert a in out, ("片段未命中", key, a[:40])
        out = out.replace(a, b)
    if tail:
        assert out.rstrip().endswith("|")
        out = out.rstrip()[:-1].rstrip() + " " + tail + " |"
    return out


# ---- 1) 老混元 Q04：连续第 35 期 -> 36（基准日不变，故「第 27 天」不变）----
REWRITE["🔴 **腾讯老混元大模型平台停服**"] = build(
    "🔴 **腾讯老混元大模型平台停服**",
    [
        ("Q04 连续第 35 期未决", "Q04 连续第 36 期未决"),
        ("**⚠️ （047 期）本轮仍未实访", "**⚠️ （048 期）本轮仍未实访"),
        ("只按基准日推进「连续第 35 期 / 第 27 天」两个由脚本重算的数",
         "只按基准日推进「连续第 36 期 / 第 27 天」两个由脚本重算的数"),
    ],
    tail="**⚠️ 本期基准日与 047 期同为 10/27 —— 「高危窗口第 27 天」不变是对的：天数按「截止日 − 基准日」算，"
         "期数按「连续第 N 期」算，两者是两套计数器**（避坑 208 同源：**同一个数字，两种口径，别混**）。",
)

# ---- 2) ZCode / BigModel：域名仍是博彩停放页（字节数变了，性质没变）----
REWRITE["⚪ **ZCode / BigModel 新用户试用**"] = build(
    "⚪ **ZCode / BigModel 新用户试用**",
    [
        ("**（045 期）本轮实访 `zcode.ai/`**：**返回 `1,043,615` 字节",
         "**（048 期）本轮实访 `zcode.ai/`**：**返回 `993,914` 字节"),
    ],
    tail="**⚠️ （048 期）复读结论：字节数由 045 期的 `1,043,615` 变为 `993,914`（**变的是页面体积，不是站点性质** —— "
         "正文仍是体育博彩停放页，`sports betting` 相关字样 199 处），**「登记项已失效（域名变更）」这一状态不变**。"
         "**⚠️ 本行那句「`ZCode 月报连续第 19 期未见`」是 045 期写入的历史表述**：047 期已把该待办改为"
         "「等域名/产品是否重新上线」，**本期起不再续计「未见」的期数**（续计一个已经不存在的产物的期数没有意义）。",
)

# ---- 3) AutoClaw「每日登录领 credits」第二期：第三期连续第 4 期未见 -> 第 5 期----
REWRITE["⚪ **智谱 AutoClaw「每日登录领 credits」第二期**"] = build(
    "⚪ **智谱 AutoClaw「每日登录领 credits」第二期**",
    [
        ("**⚠️ （040 期）第三期是否接上：本期仍未见公告 —— 连续第 4 期未见**",
         "**⚠️ （048 期）第三期是否接上：本期仍未见公告 —— 连续第 5 期未见**"),
        ("（037、038、039 期已连续记三次「本期未见公告」）",
         "（037、038、039 期已连续记三次「本期未见公告」）"),
    ],
    tail="**⚠️ （048 期）本轮未实访该站公告列表 —— 「连续第 5 期」是按期数推进的，不是按本轮实访结果重数的；"
         "**本轮实访的是国内站 `M10W4` 活动页（见下），不是第三期公告页**（避坑 180）。",
)

# ---- 4) DeepSeek：连续第 6 期无新发布 -> 第 7 期（本期未复访 Change Log）----
REWRITE["🟡 **`DeepSeek Search` / `Fetch` 两个 API 开放"] = build(
    "🟡 **`DeepSeek Search` / `Fetch` 两个 API 开放",
    [
        ("**（045 期）回扫 `api-docs.deepseek.com/updates`（Change Log）实访**",
         "**（045 期）回扫 `api-docs.deepseek.com/updates`（Change Log）实访；048 期本轮未复访该页**"),
        ("**即 `DeepSeek` 侧连续第 6 期无新发布**", "**即 `DeepSeek` 侧连续第 7 期无新发布**"),
    ],
    tail="**⚠️ （048 期）本轮未实访该 Change Log —— 「连续第 7 期」按期数推进，不按实访结果重数**（避坑 180）。",
)

# ---- 5) OpenRouter 的 MiniMax M3.1 Flash (free)：免费档结束状态延续 ----
REWRITE["⚪ **`OpenRouter` 的 `MiniMax M3.1 Flash (free)` 免费档"] = build(
    "⚪ **`OpenRouter` 的 `MiniMax M3.1 Flash (free)` 免费档",
    [
        ("**（045 期）本轮实访 `openrouter.ai/minimax/minimax-m3.1-flash:free`（读于 2026-10-23）**",
         "**（045 期）本轮实访 `openrouter.ai/minimax/minimax-m3.1-flash:free`（读于 2026-10-23；048 期复读官方目录结论一致）**"),
    ],
    tail="**⚠️ （048 期）本轮复读 `openrouter.ai/api/v1/models` 全量 `463` 条：付费档 `minimax/minimax-m3.1-flash` 仍在，"
         "`:free` 后缀仍不在 `:free` 清单 `17` 条里 —— **免费档结束状态延续，结论不变**。"
         "**⚠️ 但本期新立避坑 211：`created` 是「加入目录时间」不是「厂商发布时间」** —— "
         "**判断「什么时候免费」要看官方横幅（`The free launch period ended Oct 22, 2026.`），不看目录字段**。",
)

# ---- 6) AutoClaw 国内站 M10W4：本期未复访正文，只推进状态 ----
REWRITE["🟢 **智谱 `AutoClaw` 国内站 `M10W4` 一周福利"] = build(
    "🟢 **智谱 `AutoClaw` 国内站 `M10W4` 一周福利",
    [
        ("**⚠️ （047 期）本轮未再实访该页正文（046 期已逐字核过），只按活动期推进状态 —— 如实写「未复访」**",
         "**⚠️ （048 期）本轮未再实访该页正文（046 期已逐字核过、047 期未复访），只按活动期推进状态 —— 如实写「未复访」**"),
    ],
    tail="**⚠️ （048 期）本轮实访清单：本轮抓取了该站与国际站的列表页，但 `M10W4` 的活动正文页本轮未取到可读文本 —— "
         "**故本行一个事实字段都不更新，只推进「活动第 3 天」**（避坑 180）。",
)

# ---- 7) AutoClaw 国际站 M10W4：矛盾第 3 次未改（本期未实访）----
REWRITE["🟢 **智谱 `AutoClaw` 国际站 `M10W4` `Weekly Perk`"] = build(
    "🟢 **智谱 `AutoClaw` 国际站 `M10W4` `Weekly Perk`",
    [
        ("**⚠️ 同页「正文 40 million vs 结尾句 100 million」的矛盾第 2 次实读仍未改正**（避坑 202 追踪项，本期不销项）",
         "**⚠️ 同页「正文 40 million vs 结尾句 100 million」的矛盾第 2 次实读仍未改正**（避坑 202 追踪项，048 期本轮未实访该页、**矛盾是否已改本轮未核到**，追踪项不销项）"),
    ],
    tail="**⚠️ （048 期）本轮未实访该活动正文页 —— 「矛盾第几次」这个计数本期**不推进**（避坑 180：**未实访就不许把观察计数加一**）。",
)

# ---- 8) OpenRouter 免费档（本期头条之二）：三个计数同值 + 成分换血 ----
REWRITE["🟢 **OpenRouter 免费档（**官方 API 目录口径"] = build(
    "🟢 **OpenRouter 免费档（**官方 API 目录口径",
    [
        ("**⚠️ （047 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-27 06:2x）**："
         "**全量 `463` / 零价 `20` / `:free` `17`**；**与 046 期（467/20/17）比：全量 `−4`，零价与 `:free` 同值**。",
         "**⚠️ （048 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-27 10:1x）**："
         "**全量 `463` / 零价 `20` / `:free` `17`**；**与 047 期（463/20/17）比：三个数全部同值**。"),
        ("**⚠️ `:free` 17 条逐条 diff：无新增、无消失（连续第 2 期）**",
         "**⚠️ `:free` 17 条逐条 diff：无新增、无消失（连续第 3 期）**"),
    ],
    tail="**⚠️ （048 期）本期最重要的一条：三个数全部同值，但成分换了 —— 逐条 diff 定位到 "
         "**新增 `openai/gpt-6.1-terra-pro`、消失 `ibm-granite/granite-4.0-h-micro`，`+1 −1 = 0` 与总数一致** ✔"
         "（046 期立的存档机制连续第二期生效；**「总量同值」绝不等于「没变化」，必须逐条 diff 才敢说这句话**）。"
         "**⚠️ 新条目 `gpt-6.1-terra-pro` 的一手字段**：与 `gpt-6.1-terra` **同价**（`$1` 输入 / `$5` 输出 每 1M、"
         "缓存输入 `$0.05`、`ctx 1,050,000`）、**API 侧无 `:free` 档**、目录里也**没有** `gpt-6.1-terra-pro:batch`。"
         "**⚠️ 新立避坑 211：它的 `created` 是 `2026-10-26T18:15:56Z`（＝北京 10/27 02:15），落在 047 期窗口内** —— "
         "**即「047 期窗口内发布、048 期才在目录层挂出」，`created` 是「加入目录的时间」不是「厂商发布的时间」**。"
         "**⚠️ 消失的 `ibm-granite/granite-4.0-h-micro`：本轮该 ID 已不在全量目录中，但本报告不写「下线」「停服」「退役」** —— "
         "**目录层消失 ≠ 厂商撤下模型，官方 `IBM` 侧状态本轮未实访，如实记「未核到」**（避坑 154/161）。"
         "**⚠️ `freellm.net` 首页六项计数器（读于 2026-10-27 09:2x）**：**六项**全部与 047 期同值** —— "
         "`531+` / `300` / `31` / `449` / `243`，`Latest free LLM API model update: 2026-10-26`。"
         "**⚠️ 同值也要记账（避坑 029），但「同值」只说明这六个数没动**（避坑 207 同族）；"
         "**047 期记的 `Models Tracked` `−9` 本期维持 `300`、未回升，那 9 条仍定位不到**（`freellm` 不提供 ID 清单，不猜）。"
         "**⚠️ `openrouter.ai/announcements` 本轮实访仍停在 `October 14, 2026`**（041–048 连续八期无新限免公告）。",
)

# ---- 9) Kling 4.0（本期头条之二）：路径迁移 + 0.133 归属 ----
REWRITE["🟢 **快手可灵 Kling 4.0"] = build(
    "🟢 **快手可灵 Kling 4.0",
    [
        ("**⚠️ （047 期）新增事实（一手：`runware.ai/models/klingai`，读于 2026-10-27 06:2x）**："
         "**`Runware` 模型页出现 `Kling 4.0`，页面含 `native audio` 字样 8 处、`audio` 79 处**",
         "**⚠️ （048 期）更正 047 期的取数路径（一手：`runware.ai/kling-4`，读于 2026-10-27 10:2x，两次抓取长度与关键字段完全一致）**："
         "**`Kling 4.0` 的真实模型页路径是 `runware.ai/kling-4`（`200`，529,847 字节），其中 `native audio` 11 处、`audio` 89 处**；"
         "**047 期记的「8 处 / 79 处」取自已失效的旧路径 `runware.ai/models/klingai`** —— "
         "**「8 → 11」是换了 URL，不是内容增加**（本期新立避坑 210）"),
        ("**本轮在 `runware.ai/models/klingai` 与 `runware.ai/pricing` 两页均未核到 `0.133` 与 `7 days` 字样**，"
         "**故 `$0.133/秒` 与「15% × 7 天」不进本报告价格位，只作「社媒口径、一手未核到」登记**（避坑 200 同族）。",
         "**本轮在正确路径 `runware.ai/kling-4` 与 `runware.ai/pricing` 两页均未核到 `0.133` 与 `7 days` 字样**，"
         "**故 `$0.133/秒` 与「15% × 7 天」不进本报告价格位，只作「社媒口径、一手未核到」登记**（避坑 200 同族）。"
         "**⚠️ 本期新立避坑 209 并更正 047 期的理由**：**`$0.133` 在一手页上其实出现了 —— 但它属于 `sync-3`（唇形同步）模型，不是 `Kling 4.0`**："
         "该页 JSON 逐字 `\"pricingRates\":[{\"amount\":0.133,\"unit\":\"durationSecond\"}]`，其同一条记录的 `coverImage` 指向 `sync-3.jpg`、"
         "`capabilities` 含 `io:audio-to-video`、`pricingExamples` 的两个配置是 `segmented-lip-sync` 与 `audio-driven`。"
         "**故结论不变（不进价格位），但理由从「页面上没有这个数」改成「这个数属于另一个模型」** —— "
         "**前者会诱导下期反复重抓，后者是已经抓到并确认了归属**。"),
        ("**⚠️ 三条分发层的同步差（本期可直接观察）**：",
         "**⚠️ （048 期）旧路径 `runware.ai/models/klingai` 本轮返回 HTTP `404`，但返回体仍是 845,983 字节的完整 SPA 页面** —— "
         "**这是「软 404」：状态码说没有、正文说有**（本期新立避坑 209）；**该返回体里 `native audio` 47 处 / `audio` 631 处 是整站页量级，"
         "与本行记的 11 / 89 不同源、不可相减**。"
         "**⚠️ 三条分发层的同步差（本期可直接观察）**："),
    ],
    tail="**⚠️ `fal` 侧口径（046 期已固化，本期未复访，沿用并标注）**：四端点 `status public` / `licenseType commercial`、"
         "**`$0.157 / $0.235`（720p/1080p）与带参考档 `$0.094 / $0.141`（最少 2 倍产出计费）**、3–30 秒、最高 1080p。",
)

# ---- 10) MiniMax M3.1 Flash 开放权重：本期两端点 downloads 同值 ----
REWRITE["🟢 **`MiniMax` `M3.1 Flash` 开放权重"] = build(
    "🟢 **`MiniMax` `M3.1 Flash` 开放权重",
    [
        ("**⚠️ （047 期）`HF` 字段重取（`hf-mirror.com`，读于 2026-10-27 06:2x，详情端点 + 列表端点各一次）**："
         "**详情 `downloads` `8,782` / `likes` `371`；列表 `downloads` `7,355` / `likes` `360`**",
         "**⚠️ （048 期）`HF` 字段重取（`hf-mirror.com`，读于 2026-10-27 09:3x，**详情端点连读两次** + 列表端点 + 按 `downloads` 排序的列表端点各一次）**："
         "**详情 `downloads` `8,782` / `likes` `371`（两次读数完全一致）；列表 `downloads` `8,782` / `likes` `382`**"),
        ("**⚠️ 流通量记账（升降都写）**：**详情 `5,789 → 8,782`（升 `2,993`）；列表 `7,355 → 7,355`（同值）；"
         "`likes` 详情 `317 → 371`（升 `54`）、列表 `360`（046 期未取列表 likes，本期起两端都记）**。",
         "**⚠️ 流通量记账（升降都写）**：**详情 `downloads` `8,782 → 8,782`（同值）；列表 `7,355 → 8,782`（升 `1,427`）；"
         "`likes` 详情 `371 → 371`（同值）、列表 `360 → 382`（升 `22`）**。"),
        ("**⚠️ 对照组 `MiniMax-H3`**：**详情 `5,173,270`（046 期 `5,099,332`，升 `73,938`）、`likes` `6,364`（列表 `6,370`）**、"
         "`lastModified` `2026-08-13T01:46:29Z`（不变）。",
         "**⚠️ 对照组 `MiniMax-H3`**：**本期取到的是「按 `downloads` 排序的列表端点」读数 `5,285,319` / `likes` `6,379`；"
         "047 期记的是「详情端点」`5,173,270` —— ⚠️ **两个数来自不同端点、不可相减**（避坑 210 同源），"
         "本期只报列表端点读数、不写涨跌**。"),
    ],
    tail="**⚠️ 本期不再复述 047 期「详情 > 列表」的方向**：047 期已把它降级为「当期读数」（避坑 207），"
         "**本期遵守 —— 只写「本期读到 A=`8,782`、B=`8,782`」，不写方向**。"
         "**⚠️ 另立一条取数纪律（本期新记）**：`hf-mirror.com/api/models?sort=trending` 本轮返回 "
         "`{\"error\":\"✖ Invalid sort parameter: trending\"}` —— **该排序参数已失效**，"
         "**本报告因此不写「本期 trending 榜前 N 名」**（与 045 期 `M3.1 Flash` 权重「取数方法错了」是同一族坑）。",
)

# ---- 11) `o4-mini` API 停用：状态列里那句「044 期记为『距今 1 天』」是**历史引述**，不是本行倒计时 ----
# ⚠️ 脚本的 DAYS_RE 会把它当成活字段重算成负值 —— 这就是「内嵌形态脚本管不到、需显式 REWRITE 兜底」的标准样本。
REWRITE["⚪ **OpenAI `o4-mini` API 停用**"] = build(
    "⚪ **OpenAI `o4-mini` API 停用**",
    [
        ("**已结束（停用日即本期基准日 10/23 · 044 期记为「距今 1 天」）**",
         "**已结束（停用日 10/23，本期基准日 10/27 已过 4 天）**"),
        ("**044 期该行写「距今 1 天」，本期重算为 `0`，按脚本口径归 `over` 档**",
         "**044 期该行写「距今 1 天」、047 期重算为 `0`，048 期按基准日 10/27 距停用日 4 天，仍归 `over` 档**"),
    ],
    tail="**⚠️ （048 期）本行显式改写的原因**：状态列里那句「044 期记为『距今 1 天』」是**引述历史**，"
         "**不是本行的活倒计时** —— 脚本的 `DAYS_RE` 会把它当成活字段重算成「距今 −4 天」（负值）。"
         "**内嵌形态脚本管不到，由每期显式 `REWRITE` 兜底**（与 `AgentCore` 同一处置）。",
)

# ---- 12) 腾讯元器：截止列三个日期，状态列三个「距今」—— 逐条手算，不让脚本重算 ----
REWRITE["🔴 **腾讯智能体平台「元器」停止服务"] = build(
    "🔴 **腾讯智能体平台「元器」停止服务",
    [
        ("🔴 **倒计时中，四个日期必须分开排（047 期逐行手算，不用脚本）**",
         "🔴 **倒计时中，四个日期必须分开排（048 期逐行手算，不用脚本）**"),
    ],
    tail="**⚠️ （048 期）本期基准日与 047 期同为 10/27，故三个「距今」数（`2 / 13 / 74`）全部不变 —— "
         "**这是「同基准日就不变」的正常结果，不是漏改**。"
         "**⚠️ 本行仍是「脚本解析不到状态列倒计时」的标准样本**：截止列有三个日期，"
         "`DAYS_RE.sub` 会把状态列三个「距今」全部替换成截止列第一个日期算出的同一个值，"
         "**故每期显式 `REWRITE`、按基准日逐条手算**。",
)

# ---- NEW 行：OpenAI Signals v3.0 数据集（047 期漏登，本期补登）----
NEW = [
    "| 🟢 **`OpenAI` `Signals v3.0` 数据集（**165 类工作活动 · 近 100 国 · 2025 Q1–2026 Q3 季度序列 · "
    "`CC BY 4.0` · **047 期漏登，本期补登**· 官方发布日 10/26**）** | "
    "**无结束日（公开数据集，无期限、无额度、无门槛；官方未给任何活动期或截止日）** | "
    "🟢 **已公开可下载（本期补登 · 四层全通）**。"
    "**官方一手（`openai.com/index/chatgpt-expanding-world-of-work`，页面标注 `October 26, 2026`）逐字**："
    "「**Today, we are releasing OpenAI Signals data that explores 165 work activities across nearly 100 countries, "
    "revealing how consumers use ChatGPT for work.**」"
    "**官方一手（`openai.com/signals/data-download/`，读于 2026-10-27 10:2x）逐字**："
    "「**Download CSV files of the data**」／「**Data dictionary**」／"
    "「**All Signals data is licensed for use under the Creative Commons `CC BY 4.0` license, which allows you to use, share, "
    "and adapt the data but requires attribution or citation.**」；"
    "另给引用格式 `@online{openaiecon2026signalsdata, …, title = {{OpenAI} Signals v3.0}, year = {2026}, "
    "urldate = {2026-10-26}, note = {Data download and methodology}}`，"
    "以及第二个下载口「**Download data for the AI Jobs Transition Framework**」。"
    "**⚠️ 四层开放（避坑 41）**：**① 能用 —— 免登录直接下载，未要求注册/订阅/填表（订阅提醒表单在页面下半部，与下载口分离）"
    "② 能下载 —— CSV + 数据字典 + AI Jobs Transition Framework 数据 ③ 能跑 —— CSV 可直接用 Excel/R/Python 打开 "
    "④ 能商用 —— `CC BY 4.0` 允许使用/分享/改编，**但须署名或引用**（官方逐字 `requires attribution or citation`）**。"
    "**⚠️ 覆盖范围有限（官方逐字）**：**「covers work-related messages on individual ChatGPT plans and does not include "
    "enterprise messages or Codex messages」—— 不含企业版消息、不含 `Codex` 消息**。"
    "**⚠️ 两个厂商自报的可核对数（避坑 116）**：**① 「Across 74 countries observed in every quarter, the ten most common "
    "activities represented an average of 51.1% of each country's classified work messages in Q3 2026, down from 56.0% in Q1 2025」"
    "—— 74 国头部 10 类活动占比均值 `56.0% → 51.1%`（−4.9 个百分点）；"
    "② 「about 43% of the employment-weighted task mix for mapped U.S. occupations falls into Other IWAs」—— "
    "**约 `43%` 的美国就业加权任务结构落在「Other IWAs」（搬运物料、操作车辆、维护健康或病历等），因未达一致性门槛而未单独报出**。"
    "**⚠️ 期号与窗口归属必须写清**：**官方发布日 `2026-10-26`（下载页 `urldate` 逐字为 `2026-10-26`）落在 **047 期窗口**内，"
    "**047 期正文与表格均未登记它**（本期经 `git show HEAD` 与全文检索逐行核过，047 期 md 中 `Signals` 命中 0 次）—— "
    "**故本行是「往期漏项补登」，不是「048 期新发布」**（避坑 44）。"
    "**⚠️ 「免费数据」不等于「官方结论」**：本行登记的是「可下载、许可清晰」这个事实，数据能读出什么结论是研究者的事（避坑 116）。 |",
]

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

# ---- 天数重算：基准日与 047 期同为 10/27，预期无变化，但断言逐行成立 ----
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
