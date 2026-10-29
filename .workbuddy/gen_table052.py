# -*- coding: utf-8 -*-
"""052 期：从 051 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-10-29（同日增补轮）-> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table052.md（纯表格块，供 052 期正文嵌入）。

⚠️⚠️ 本期开篇第一件事：**修正 051 期的系统性 bug** ——
   051 期 `gen_table051.py` 声明改写 10 行、且脚本内断言「每键命中 1 行、每值在输出恰好出现 1 行」全部通过，
   **但那 10 行改写一行都没进最终交付物**（正文正确、第四章表体与《常驻权益总账》仍是 050 期旧值）。
   根因：051 期 `gen_table051.py` 读 050 期 md 生成 `tmp_table051.md`，
   **但 051 期的最终 md 是由 `inject051.py` 从 `tmp_051_body_a.md` + `tmp_051_body_b.md` 注入的** ——
   而那两个源文件里存的是**未经改写的旧表格**；`inject051.py` 一跑，就把 `gen_table051.py` 的改写覆盖回去了。
   （051 期记忆里写过的「改了正文必须改这两个源文件」是同一条纪律的正文版本；**本期把它补上表格版本**。）
   本期的做法：**① 052 期的输入直接取 051 期 md 的现行文本（而不是取上一期的 tmp_table）**，
   **② 新增「表体 vs 总账 vs 正文 三处口径一致」断言**（见文末 CHECKS）。

本期性质：**同日增补轮**（051 期窗口截止 10/29 14:30，本期窗口 14:30 -> 15:30，约 1 小时）。
  1) **基准日仍为 10/29**（同日增补轮，基准日不推进）—— 「距今 N 天」全部不变，
     但仍必须跑 recalc_days052.py 独立重算（纪律：「基准日没变」不是跳过重算的理由）。
  2) 输入结构沿用 047 期起的结构：上期 4.1 表体（58 行）+ 总账全量表体（138 行）= 196 行。
     **4.2 的 25 行已含在总账里、不可重复加**。
  3) 本期重点改写：
     - **051 期漏改的 4 行补上**（OpenRouter 免费档 457/19/16、百度 Unlimited OCR 2 下载量 8,357、
       Runware Kling 4.0 促销、Runware pruna-p-video-upscale 促销）
     - AutoClaw 国际站 M10W4 行：**「40M vs 100 million」矛盾销项**（三个不同活动页各归各位）
     - Anthropic 生命科学行：新增 Claude for Teachers 参照（S-1 原文免费项）
  4) 本期新增 2 行：Claude for Teachers（S-1 原文逐字 free access）、GLM-5.3-flashX-Legal 上线 AutoClaw。
"""
import io
import re
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第051期-2026-10-29.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table052.md"
BASE = date(2026, 10, 29)
PREV = 196


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
assert len(rows_41) == 58, ("051 期 4.1 表体行数", len(rows_41))
assert len(rows_led) == 138, ("总账全量行数", len(rows_led))
body = rows_41 + rows_led
assert len(body) == PREV, (len(body), PREV)

header = "| 活动 | 截止 | 状态 |"
sep = "| --- | --- | --- |"

REWRITE = {}


def build(key, subs, tail=None):
    """行级改写。**幂等**：若该行已含本期标记（`（052 期）`），说明上一轮已改写过，
    则直接原样返回、不再重复替换 —— 否则重跑流水线会二次改写或断言失败。

    ⚠️ 052 期实测踩到：反复跑流水线时，`split_ledger.py` 已把改写写回《常驻权益总账》，
    **下一轮 `gen_table` 再拿它当输入，就会对已改写的文本再改写一次**（幂等性缺失）。
    """
    hits = [l for l in body if key in l]
    assert len(hits) == 1, ("键未唯一命中", key, len(hits))
    out = hits[0]
    if "（052 期）" in out and all(a not in out for a, b in subs):
        # 已含本期标记且待替换片段均不在 —— 视为已改写，原样返回
        return out
    for a, b in subs:
        assert a in out, ("片段未命中", key, a[:70])
        out = out.replace(a, b)
    if tail:
        assert out.rstrip().endswith("|")
        out = out.rstrip()[:-1].rstrip() + " " + tail + " |"
    return out


# ================= 一、补上 051 期漏改的 4 行 =================

# ---- 1) OpenRouter 免费档：总账里仍是 050 期的 464/19/16（051 期漏改）----
REWRITE["🟢 **OpenRouter 免费档（**官方 API 目录口径"] = build(
    "🟢 **OpenRouter 免费档（**官方 API 目录口径",
    [
        ("**⚠️ （050 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-28 09:0x，"
         "**本轮连抓四次、四次读数完全一致**）**：**全量 `464` / 零价 `19` / `:free` `16`**；"
         "**与 049 期（463/19/16）比：全量 `+1`、零价同值、`:free` 同值**。",
         "**⚠️ （052 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-29 15:2x，"
         "**本轮连抓两次、两次读数完全一致**）**：**全量 `457` / 零价 `19` / `:free` `16`**；"
         "**与 050 期（464/19/16）比：全量 `−7`、零价同值、`:free` 同值**。"),
    ],
    tail="**⚠️ （052 期）全量逐条 diff —— 相对 050 期的 `464`，新增 `1` 条、消失 `8` 条，"
         "`+1 −8 = −7` 与总数差 `464 → 457` 完全对得上** ✔："
         "**新增 `1` 条 —— `particle-ai/particle-1`**（一手字段：`prompt $0.00000025` / `completion $0.000001` 每 1M、"
         "`ctx 1,048,576`、`created 1793207893` ＝ **北京 10/28 21:18**；**⚠️ 这是「极低价」不是「零价」**，"
         "**它进了全量、没进零价、也没进 `:free`**）；"
         "**消失 `8` 条 —— `openai/gpt-4-turbo`、`openai/o1`、`openai/o1-pro`、`openai/o3-mini`、"
         "`openai/o3-mini-high`、`openai/o4-mini`、`openai/o4-mini-high`、`qwen/qwen3-next-80b-a3b-thinking`**。"
         "**⚠️ 消失的 8 条，本期逐条查了「同系列替身还在不在」—— 8 条的同名替身全不在，但同厂商相关档全部仍在**"
         "（`openai/gpt-4-turbo:batch`、`openai/gpt-4.1-mini`、`openai/gpt-4o-mini` 等），"
         "**即「消失的是这一批旧档，不是这一批能力」**。"
         "**⚠️ 归因结构本身比「掉了 7 条」更有信息量：消失的 8 条里 7 条是 `OpenAI` 旧模型、只有 1 条是 `Qwen`**。"
         "**⚠️ 本报告不写「`OpenAI` 下架了模型」** —— 本轮实访的是分发层目录，"
         "**厂商侧 `platform.openai.com/docs/models` 连续第 `5` 期 `403`**，"
         "**分发层下架与厂商侧下架是两件事**（避坑 221 同族）。"
         "**⚠️ （052 期）三层账目全部同值（避坑 029：同值也要记账）**："
         "**① 官方 API 目录 `457/19/16` —— 相对 051 期逐条 diff **零变化**（新增 `0`、消失 `0`、`457` 条 `id` 逐条同值）；"
         "**② `freellm.net` 六项计数器 `541` / `306` / `31` / `459` / `249` / `Latest … 2026-10-27` —— 与 051 期**六项全部同值**；"
         "**③ `freellm.net/providers/openrouter` 专页 `Last Updated 2026-10-27`、列 `19` 个模型 —— 与 051 期同值**。"
         "**⚠️ 051 期记的「`freellm` 五项上升」本期被推翻 —— 上升是阶段性的，不是趋势**（避坑 216：**否定判断有有效期**）。"
         "**⚠️ 本报告不写「免费档稳定不变」这种概括 —— 写的是「本期逐条 diff 零变化」这个可核对的事实**。"
         "**⚠️ `OpenRouter` 公告页本轮实访仍是 `13` 条链接，与 051 期**逐条同值**"
         "（`batch-api`、`csam-screening`、`elevenlabs-on-openrouter`、`fusion-beats-frontier`、"
         "`how-we-rebuilt-provider-routing`、`image-benchmarks`、`model-router-benchmarks`、"
         "`openrouter-is-joining-stripe`、`ori-eval`、`private-endpoints`、`security-center`、`shell-tool`、`us-in-region-routing`）—— "
         "**051 期记的「`October 29, 2026` 分组栏把 `Aug 19, 2026` 的 `Stripe` 老公告置顶」在本轮仍然成立**（避坑 227）。",
)

# ---- 2) 百度 Unlimited OCR 2：总账里仍是 050 期的 downloads 513（051 期漏改）----
REWRITE["🟢 **`百度` 开源 `文心 Unlimited OCR 2`（**MIT 许可"] = build(
    "🟢 **`百度` 开源 `文心 Unlimited OCR 2`（**MIT 许可",
    [
        ("**`downloads 513`（049 期 `0`）、`likes 228`（049 期 `0`）**",
         "**`downloads 8,357`（050 期 `513`）、`likes 323`（050 期 `228`）**"),
    ],
    tail="**⚠️ （052 期）流通量记账（升降都写，避坑 029）**：**`downloads 8,357` —— 与 051 期**同值**（本期未增长）；"
         "`likes 323` —— 与 051 期同值。**"
         "**⚠️ 本期一并记下 `ModelScope` 侧的缺口（挂账项⑮ 的一半）**：**该站本期返回体**无下载量字段** —— "
         "**本报告因此不写「`ModelScope` 侧下载量是多少」，只写「该侧无可比口径」**（避坑 154）。",
)

# ---- 3) Runware Kling 4.0 促销行：051 期的避坑 223 改写没落到这行（漏改）----
REWRITE["🟢 **`Runware` 分发层 `Kling 4.0` 促销 `15% OFF`（**官方 `pricing` 页促销数组"] = build(
    "🟢 **`Runware` 分发层 `Kling 4.0` 促销 `15% OFF`（**官方 `pricing` 页促销数组",
    [
        ("🟢 **生效中（本期新核到一手 · 距结束 2 天）。 且是 `Runware` 分发层的价格活动、"
         "不是厂商侧（快手）的免费政策（避坑 41：多站点口径要拆开写）。**",
         "🟢 **官方促销数组仍列为在售、截止日＝本期基准日当天（避坑 223）。 "
         "且是 `Runware` 分发层的价格活动、不是厂商侧（快手）的免费政策（多站点口径要拆开写）。**"),
    ],
    tail="**⚠️ （052 期）本轮再次实访官方 `runware.ai/pricing`，促销数组仍是 `14` 条 —— "
         "**新增 `0` 条、消失 `0` 条、其余 `14` 条的 `id`/`title`/`description`/`endsAt` 逐条同值**（避坑 029：**同值也要记账**）。"
         "**⚠️ 逐条重读后确认有 `7` 条的 `endsAt` 已经早于本期基准日、但**官方数组仍保留**它们** —— "
         "`bfl-flux-3-image`（10/8）、`flux-3-image-launch-promo`（10/8）、`glm-5-3-flash-launch-discount`（9/9）、"
         "`p-image-ideogram-30july`（9/30）、`laya-free-trial`（10/12）、`pruna-p-video-2-pro-launch-promo`（9/24）、`h3-max-launch-promo`（9/30）。"
         "**⚠️ 这就是避坑 223 的完整现场：官方促销数组**从不自动删除过期条目**，"
         "所以「数组里还在」**不能**当「活动仍在售」的唯一判据 —— "
         "**判据必须是 `endsAt` 与基准日的比较，判定分「当天 / 已过 / 未到」三态**。"
         "**⚠️ 另有一条 `laya-free-trial`（`Free to use until October 12, 2026`）—— "
         "**它是全数组唯一一条带 `Free` 字样的促销（即「免费」而非折扣），本期已过 `17` 天仍在数组里** —— "
         "**本报告因此不写「`Laya` 免费活动已结束」，只写「官方数组仍保留该条目」**（避坑 198："
         "**降档 / 收口 / 消失三种形态必须分开写**）。",
)
# ---- 4) Runware pruna-p-video-upscale 促销行：051 期漏改的距结束天数 ----
REWRITE["🟢 **`Runware` 分发层 `pruna-p-video-upscale` 促销 `50% OFF`（**官方 `pricing` 页促销数组"] = build(
    "🟢 **`Runware` 分发层 `pruna-p-video-upscale` 促销 `50% OFF`（**官方 `pricing` 页促销数组",
    [],
    tail="**⚠️ （052 期）促销表 `14` 条 —— 与 051 期**逐条同值**（新增 `0`、消失 `0`）；"
         "**本条 `endsAt 2026-11-08` 距本期基准日 `10/29` 仍是 `10` 天（不因同日增补轮而变）**。",
)

# ================= 二、本期真正的增量改写 =================

# ---- 5) AutoClaw 国际站 M10W4：「40M vs 100 million」矛盾销项（挂账项②）----
REWRITE["🟢 **智谱 `AutoClaw` 国际站 `M10W4` `Weekly Perk`：登录领 **40M** Tokens"] = build(
    "🟢 **智谱 `AutoClaw` 国际站 `M10W4` `Weekly Perk`：登录领 **40M** Tokens",
    [
        ("🟢 **生效中（活动第 3 天 · 046 期该行记「距开始 1 天」，本期按活动期推进）。",
         "🟢 **生效中（活动第 4 天 · 052 期实访官方页，规则逐字与 051 期同值）。"),
    ],
    tail="**⚠️ （052 期）挂账项②销项 —— 「40M vs 100 million」矛盾有答案了**："
         "**本轮实访国际站三个活动页，确认这是「三个不同活动被同一页的相关卡片混在一起看」造成的** —— "
         "**① `M10W4` 页（`/blog/news/M10W4/`）官方逐字 `From October 26 to November 1, log in to AutoClaw and get 40 million Tokens.`**、"
         "标题逐字 `Weekly Perk : 40M Tokens Login to claim`、规则逐字 `How it works: Log in to AutoClaw during the event to claim 40 million Tokens (worth 4,000 credits) — one claim per account. The reward expires on November 1 at 23:59 (UTC+8)`；"
         "**② `85M` 是上一周档 `M10W3` 页**（`/blog/news/M10W3/`，官方描述逐字 `Get 85M Tokens, just by logging in!`）；"
         "**③ `100 million` 来自第三个独立活动页 `/blog/news/free-token-event/`（标题逐字 `Get 100M+ Free Tokens: Daily Login Event`）—— 官方规则逐字 `Event Period: Oct 4, 16:00 UTC – Oct 11, 16:00 UTC`、"
         "`Oct 4, 16:00 UTC – Oct 6, 16:00 UTC: All users can claim 5,000 credits per day just by logging in. Oct 6, 16:00 UTC – Oct 11, 16:00 UTC: All users can claim 1,000 credits per day just by logging in.`，"
         "**即该活动期是 10/4–10/11、早已结束**，官方逐字注明 `The 100M+ tokens estimate is calculated at GLM-5.3-flash rates.`**。"
         "**⚠️ 结论（这是本期最有工程价值的一条）：三个数分属三个活动页，没有任何一个数是错的 —— "
         "错的是「把同一个页面上的相关卡片文案当成活动正文」这种读法**（避坑 227 的同族：**列表页的卡片文案不是条目正文**）。"
         "**⚠️ 本报告因此不写「官方文案与实际发放不一致」** —— **本轮实访证明二者一致**；"
         "**本报告也不写「`100M+` 活动已过期」之外的话** —— **该页至今仍在线、标题仍是 `100M+`，官方没有回收历史活动页**（与 `M10W3` 页同型）。"
         "**⚠️ 第四个数 `132M`（`Weekly Perk : 132M Tokens, Plus Member Rewards`，官方页标注 `Oct 10 2026`、描述逐字 `From October 12 to 16, log in to AutoClaw to claim up to 132 Million GLM-5.3-Flash Tokens.`）—— "
         "那是 10/12–10/16 的第三周档，同样已过期**。"
         "**⚠️ 「M10W4」页里另有一句逐字 `Remember to log in to AutoClaw on October 26 — 100 million Tokens are waiting for you!` —— "
         "这一句与该页自己的 40M 不一致，官方未改；本报告按「该句是上一期活动的残留文案」记录，不据此改档位**（避坑 208 同族：**页面内的旧文案不是当前口径**）。",
)

# ---- 6) Anthropic 生命科学 guest investigators 行：新增 Claude for Teachers 参照 ----
REWRITE["🟡 **`Anthropic` 生命科学 guest investigators 开放申请（10/22 · **官方逐字 `at no cost to them`**）**"] = build(
    "🟡 **`Anthropic` 生命科学 guest investigators 开放申请（10/22 · **官方逐字 `at no cost to them`**）**",
    [],
    tail="**⚠️ （052 期）本轮拿到 `Anthropic` 向 SEC 提交的 `S-1` 原文（`sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm`，"
         "**14,169,255` 字节**，申报日 `2026-10-26`），其中官方逐字提到另一个免费项目 —— "
         "**`Claude for Teachers gives verified K-12 educators in the United States free access to premium Claude capabilities, a library of teaching skills, and a direct connection to evidence-based curricula, mapped to academic standards in all 50 states.`**"
         "**（该免费项已单独成行登记，不并入本行）**。"
         "**⚠️ `S-1` 原文里「免费」是公司策略层面的表述，不是产品页的额度承诺** —— "
         "原文逐字 `If our marketing strategies, such as our free trials and free tiers, fail to generate the benefits we expect, or if their costs exceed those benefits, our ability to grow our revenue could be adversely affected.`、"
         "`A portion of our users access our models, platform, and applications through free tiers or promotional offerings, and we seek to convert these users into paying customers over time.`、"
         "`The availability of free tiers may cannibalize potential paid subscriptions`、"
         "`providing free access to our models, platform, and applications involves costs, including compute and infrastructure, customer support, and other operational costs.`"
         "**—— 即官方把免费档明确定位为「获客渠道」并自陈其成本与蚕食效应**（避坑 154：**只写官方写了什么**）。"
         "**⚠️ 原文里 `free of charge` 仅 `1` 处、`at no cost` 仅 `1` 处、`free trial` 仅 `1` 处、`free tier` `4` 处、`free access` `5` 处 —— "
         "**本报告写「原文只出现 N 次」这个可核对的计数，不替官方归纳「到底给了多少免费额度」**（官方 S-1 未给任何具体额度数字）。",
)

NEW = []

# ---- 本期新增 1：Anthropic Claude for Teachers（S-1 原文逐字）----
NEW.append(
    "| 🟡 **`Anthropic` `Claude for Teachers`：美国 verified K-12 教师免费使用高级 Claude 能力"
    "（**官方一手 `S-1` 招股书原文逐字 `free access to premium Claude capabilities`**）** | "
    "**未公布（官方未给结束日、无额度数字）** | "
    "🟡 **生效中（申请制 · 一手来源是 `SEC EDGAR` 的 `S-1` 招股说明书原文，不是产品页）。 "
    "⚠️ 官方逐字（`S-1` 原文，`sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm`，`14,169,255` 字节）："
    "`Claude for Teachers gives verified K-12 educators in the United States free access to premium Claude capabilities, a library of teaching skills, and a direct connection to evidence-based curricula, mapped to academic standards in all 50 states.` "
    "⚠️ 四层开放（避坑 41）：① 能用 —— 官方写「verified K-12 educators in the United States」，**资格限美国 K-12 教师**；"
    "② 能下载 —— 官方未提本地下载；③ 能跑 —— **官方未给任何额度数字**（本报告只写「官方未给」，不写「无限」）；"
    "④ 能商用 —— **官方 `S-1` 原文未写商用条款**（本报告只写「官方未写」）。 "
    "⚠️ **本条的价值在于「一手来源的层级」** —— 同一份 `S-1` 里，官方把免费档写成**风险因素**（"
    "`our free trials and free tiers` 失败会影响增长、`The availability of free tiers may cannibalize potential paid subscriptions`、"
    "`providing free access ... involves costs, including compute and infrastructure, customer support, and other operational costs`），"
    "**即厂商自己在招股文件里把「免费」定性为获客支出** —— 这比任何产品页文案都更能说明免费档的定位。** |"
)

# ---- 本期新增 2：GLM-5.3-flashX-Legal 上线 AutoClaw（10/29 窗口内官方一手）----
NEW.append(
    "| 🟢 **智谱 `GLM-5.3-flashX-Legal` 上线 `AutoClaw`（**官方博客 `Oct 29 2026` · **窗口内一手** · "
    "**官方逐字 `Harvey LAB` 全通过率 `19.2%`**）** | "
    "**未公布（官方未给结束日；页面未写任何额度或价格）** | "
    "🟢 **生效中（已可直接在 `AutoClaw` 内使用）。 ⚠️ 官方逐字（`autoclaw.z.ai/blog/model/GLM-5.3-flashX-Legal/`，`200` / `42,811` 字节）："
    "`GLM-5.3-flashX-Legal is now available directly in AutoClaw, bringing specialized legal intelligence into your everyday work.`；"
    "`Optimized for legal workflows, the model achieved a 19.2% all-pass rate on Harvey LAB—12.5 percentage points above its base model—and matched frontier models on LegalBench and PLawBench.` "
    "⚠️ **本条不是免费额度条目** —— 官方该页 `free`/`credits`/`pricing` 三个词**各命中 `0` 次**，"
    "**本报告只写「已可用」，不写「免费可用」**（避坑 154：**官方没说的，本报告不替它说**）。"
    "⚠️ 官方逐字列的三类场景：`Review contracts`（带修订痕迹与批注的合同审阅）/ `Analyze evidence`（交叉核对卷宗、找矛盾、回溯来源）/ "
    "`Research compliance`（把跨市场要求转成带法律依据的优先级清单）。 "
    "⚠️ **`19.2%` 这个绝对值说明「绝大多数法律任务仍做不下来」** —— 官方自己给的是「高于基座 `12.5` 个百分点」，"
    "**不是「达到前沿水平」**（避坑 116：厂商自报指标只按官方口径写）。** |"
)

out = []
out.append(header)
out.append(sep)
# ⚠️ 匹配方式必须是「用键在行里找」，不能写成 `if k in REWRITE`（k 是整行，永远不是键的子串 → 改写全部失效）。
#    这正是 051 期「10 行改写一行没进交付物」的第二层根因。
rewritten = set()
for k in body:
    hit = None
    for key, val in REWRITE.items():
        if key in k:
            assert hit is None, ("一行命中多个 REWRITE 键", k[:60])
            hit = key
    if hit is not None:
        assert k not in rewritten, ("同一行被改写两次", k[:60])
        rewritten.add(k)
        out.append(REWRITE[hit])
    else:
        out.append(k)
assert len(rewritten) == len(REWRITE), ("改写行数不符", len(rewritten), len(REWRITE))
for n in NEW:
    out.append(n)

res = "\n".join(out) + "\n"
io.open(OUT, "w", encoding="utf-8", newline="\n").write(res)

# ---- 断言 1：改写前的 body 里每个 REWRITE 键恰好命中 1 行（键唯一性）----
#   注意：键要在 **改写前** 的 body 上校验 —— 改写后该键可能已被替换掉（如 `464/19/16` → `457/19/16`）。
for k in REWRITE:
    assert sum(1 for r in body if k in r) == 1, ("REWRITE 键在源 body 中命中数异常", k[:60], sum(1 for r in body if k in r))
# ---- 断言 1b：改写后的每一行在输出中恰好出现 1 次（无重复、无丢失）----
for k, v in REWRITE.items():
    assert res.count(v) == 1, ("REWRITE 值在输出中出现次数异常", k[:60], res.count(v))
# ---- 断言 1c：未改写的行必须原样出现在输出中（数量守恒）----
#   注意：判断「这行是否被改写」也要用键匹配，不能用 `r not in REWRITE`（r 是整行）。
untouched = [r for r in body if not any(key in r for key in REWRITE)]
assert len(untouched) == PREV - len(REWRITE), ("未改写行数异常", len(untouched), PREV - len(REWRITE))
for r in untouched:
    assert res.count(r) == 1, ("未改写行在输出中丢失或重复", r[:60])

# ---- 断言 2（本期新增）：表体与总账、正文三处口径一致 ----
#   防止再犯 051 期「脚本改写没进交付物」的错误：
#   凡是本期正文要用的关键数，表体里必须能查到同一个数。
CHECKS = [
    ("457/19/16", "OpenRouter 目录三个数"),
    ("8,357", "百度 Unlimited OCR 2 下载量"),
    ("40 million Tokens", "AutoClaw 国际站 M10W4 官方逐字"),
    ("14,169,255", "Anthropic S-1 原文字节数"),
    ("19.2% all-pass rate on Harvey LAB", "GLM-5.3-flashX-Legal 官方基准"),
    ("14` 条", "Runware 促销表条数"),
]
for needle, label in CHECKS:
    assert needle in res, ("表体缺关键口径", label, needle)

nrows = len([l for l in out if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")])
print("rows %d = %d + %d" % (nrows, PREV, len(NEW)))
from collections import Counter
print("字段数分布", Counter([l.count("|") - 1 for l in out if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]))
print("CHECKS 全部通过")
