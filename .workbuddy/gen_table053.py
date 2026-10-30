# -*- coding: utf-8 -*-
"""053 期：从 052 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-10-30（隔日出刊）-> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table053.md（纯表格块，供 053 期正文嵌入）。

⚠️ 052 期立的纪律，本期全部沿用并加严：
   ① 输入直接取 **052 期 md 的现行文本**（不是取上一期的 tmp_table）——
      052 期栽在「inject 从存着旧表格的 body_a 注入，把 gen_table 的改写覆盖回去」。
   ② 写出循环必须是「**用键在行里找**」，不能写成 `if k in REWRITE`（k 是整行，永远不是键）。
   ③ 三条断言全加：键唯一命中 / 值在输出恰好出现一次 / 未改写行数守恒。
   ④ **052 期新立、本期加严**：写盘后**重新读回落盘文件**再断言一遍（052 期的断言只校验字典本身）。
   ⑤ **053 期新立（避坑 239）**：断言全过 ≠ 事实全对 —— 新增「表体关键口径 == 正文关键口径」
      与「本期新增的每个截止日都必须能在表体里查到」两条断言。

本期性质：**隔日出刊**（052 期是 10/29 同日增补轮，窗口 10/29 14:30→15:30；
  本期窗口 10/29 15:30 → 10/30 09:30，约 18.0 小时）。
  1) **基准日推进到 2026-10-30**（052 期基准日是 10/29）—— 「距今 N 天」逐行重算，
     **断言是「天数 == 截止日 − 基准日」，不是「推进一天就 −1」**。
  2) 输入结构沿用 047 期起的结构：上期 4.1 表体（58 行）+ 总账全量表体（140 行）= 198 行。
     **4.2 的 25 行已含在总账里、不可重复加**。
  3) 本期改写 6 行（OpenRouter 目录、百度 OCR 2 下载量、Runware Kling 4.0、Runware pruna-upscale、
     Mistral Large 4 公开预览行、Google Nano Banana 2 停用行）
  4) 本期新增 4 行：Mistral Large 4 权重公开 + 首周免费预算、国家超算互联网夜间免费、
     MOSS-Image 开放权重、OpenAI 付费档翻倍（Plus 不变）。
"""
import io
import re
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第052期-2026-10-29.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table053.md"
BASE = date(2026, 10, 30)
PREV = 198


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
assert len(rows_41) == 58, ("052 期 4.1 表体行数", len(rows_41))
assert len(rows_led) == 140, ("总账全量行数", len(rows_led))
body = rows_41 + rows_led
assert len(body) == PREV, (len(body), PREV)

header = "| 活动 | 截止 | 状态 |"
sep = "| --- | --- | --- |"

REWRITE = {}


def build(key, subs, tail=None):
    """行级改写。**幂等**：若该行已含本期标记（`（053 期）`），说明上一轮已改写过，
    则直接原样返回、不再重复替换 —— 否则重跑流水线会二次改写或断言失败。
    """
    hits = [l for l in body if key in l]
    assert len(hits) == 1, ("键未唯一命中", key, len(hits))
    out = hits[0]
    if "（053 期）" in out and all(a not in out for a, b in subs):
        return out
    for a, b in subs:
        assert a in out, ("片段未命中", key, a[:70])
        out = out.replace(a, b)
    if tail:
        assert out.rstrip().endswith("|")
        out = out.rstrip()[:-1].rstrip() + " " + tail + " |"
    return out


# ================= 一、OpenRouter 目录（全量 457 → 456） =================
# ⚠️ 052 期的表体与总账写的是 457/19/16（051 期的改正已进正文，但表体漏改）；
#    本期把三个数一并推进到 456/19/16，并把「零价 19」与「:free 16」拆开写（避坑 161）。
REWRITE["🟢 **OpenRouter 免费档（**官方 API 目录口径"] = build(
    "🟢 **OpenRouter 免费档（**官方 API 目录口径",
    [
        ("**⚠️ （052 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-29 15:2x，"
         "**本轮连抓两次、两次读数完全一致**）**：**全量 `457` / 零价 `19` / `:free` `16`**；"
         "**与 050 期（464/19/16）比：全量 `−7`、零价同值、`:free` 同值**。",
         "**⚠️ （053 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-30 09:1x，"
         "**本轮连抓两次、两次读数完全一致**）**：**全量 `456` / 零价 `19` / `:free` `16`**；"
         "**与 052 期（457/19/16）比：全量 `−1`、零价同值、`:free` 同值**。"),
    ],
    tail="**⚠️ （053 期）全量逐条 diff —— 相对 052 期的 `457`，新增 `0` 条、消失 `1` 条，"
         "`+0 −1 = −1` 与总数差 `457 → 456` 完全对得上** ✔："
         "**消失 `upstage/solar-pro-3`** —— ⚠️ **逐条查了「同系列替身还在不在」（避坑 225）**："
         "`upstage/solar-pro4` 仍在目录内（逐字 `prompt $0.000003` / `completion $0.000015` 每 1M）、"
         "`upstage/solar-mini4` 仍在（`$0.00000005` / `$0.00000025`）—— "
         "**即「消失的是这一档旧型号，不是这一家的能力」**。"
         "**⚠️ 「零价 `19`」与「`:free` `16`」本期仍差 `3` 个 —— "
         "`google/lyria-3-pro-preview`、`google/lyria-3-clip-preview`、`openrouter/free`（路由器）**"
         "（**这 `3` 条是零价但不带 `:free` 后缀** —— 避坑 161：**两套口径不可互相代替**）。"
         "**⚠️ 本期用第三方站做了交叉验证**：`freellm.net/providers/openrouter` 专页逐字写 "
         "`Free Tier 19 free models online`、逐字写 `Supported Models 19 models`，"
         "**其列出的 `19` 条与官方零价集合逐条完全一致、与官方 `:free` 集合不一致** —— "
         "**即第三方口径跟的是「零价」不是「`:free` 后缀」**。"
         "**⚠️ 一条工程记录（新立避坑 237）**：`openrouter.ai/api/v1/models?maxPrice=0` 这个参数"
         "**本期已不生效** —— 返回体 `768,365` 字节与不带参数的全量请求逐字节相同；"
         "**本报告的免费档统计因此改为「从全量响应里按 `pricing` 字段自行判定零价 + 按 ID 后缀判定 `:free`」**，"
         "**不再依赖那个查询参数**。"
         "**⚠️ `freellm.net` 六项计数器本期六项全部同值（避坑 029）**："
         "`541` / `306` / `31` / `459` / `249` / `Latest … 2026-10-27` —— "
         "**051 期记的「`freellm` 五项上升」本期连续第二期被推翻（避坑 216：否定判断有有效期）**。"
         "**⚠️ `freellm.net/providers/openrouter` 专页逐字 `Free Tier 200 req/day (free tier)` —— "
         "与官方口径（`50` 请求每日 / 充值满 `10 credits` 后 `1,000` 请求每日、`20` 次每分）冲突，"
         "两个口径都写、不取其一**（避坑 161）。",
)

# ================= 二、百度 Unlimited OCR 2 下载量（8,357 → 18,141） =================
REWRITE["🟢 **`百度` 开源 `文心 Unlimited OCR 2`（**MIT 许可"] = build(
    "🟢 **`百度` 开源 `文心 Unlimited OCR 2`（**MIT 许可",
    [
        ("**`downloads 8,357`（050 期 `513`）、`likes 323`（050 期 `228`）**",
         "**`downloads 18,141`（052 期 `8,357`）、`likes 383`（052 期 `323`）**"),
    ],
    tail="**⚠️ （053 期）流通量记账（升降都写，避坑 029）**："
         "**`downloads 18,141` —— 相对 052 期的 `8,357` 涨 `9,784`（涨 `117%`）；"
         "`likes 383` —— 相对 052 期的 `323` 涨 `60`** —— "
         "**这是 052 期记的「连续两期同值」之后的首次增长，且幅度很大**。"
         "**⚠️ 052 期挂账项⑯问的是「是否继续增长」—— 本期答案是「增长了」**（该问项本期销项）。"
         "**⚠️ 逐条实读的官方 API 字段（一手）**："
         "`baidu/Unlimited-OCR-2`（`createdAt 2026-10-26T03:57:46Z`）· "
         "上一代 `baidu/Unlimited-OCR`（`downloads 3,535,406` · `likes 4,931` · `createdAt 2026-06-19`）· "
         "`AtomicChat/Unlimited-OCR-2-GGUF`（`2,523`）· `RX5950XT/Unlimited-OCR-2-GGUF`（`2,783`）· "
         "`p4ulbr4dl3y/unlimited-ocr-2-ru-gguf`（`376`）· `mlx-community/Unlimited-OCR-2-8bit`（`355`）。"
         "**⚠️ `ModelScope` 侧本期返回体仍无下载量字段 —— 仍写「该侧无可比口径」（避坑 154）**。",
)

# ================= 三、Runware Kling 4.0 促销（endsAt 10/29 → 相对 10/30 已过期） =================
REWRITE["🟢 **`Runware` 分发层 `Kling 4.0` 促销 `15% OFF`（**官方 `pricing` 页促销数组"] = build(
    "🟢 **`Runware` 分发层 `Kling 4.0` 促销 `15% OFF`（**官方 `pricing` 页促销数组",
    [
        ("🟢 **官方促销数组仍列为在售、截止日＝本期基准日当天（避坑 223）。 "
         "且是 `Runware` 分发层的价格活动、不是厂商侧（快手）的免费政策（多站点口径要拆开写）。**",
         "🟢 **官方促销数组仍保留该条目、但 `endsAt` 已早于本期基准日 `1` 天 —— "
         "即「数组里还在」不等于「活动还在售」（避坑 230）。 "
         "且是 `Runware` 分发层的价格活动、不是厂商侧（快手）的免费政策（多站点口径要拆开写）。**"),
    ],
    tail="**⚠️ （053 期）这条的截止日跨过了基准日 —— 三态要分开写**："
         "052 期（基准日 `10/29`）它属「截止日当天」（避坑 223），"
         "**本期（基准日 `10/30`）它变成「已过期 `1` 天」**。"
         "**⚠️ 本期实访 `runware.ai/pricing`（`200` / `748,098` 字节）确认：官方促销数组仍是 `14` 条、"
         "逐条 `id`/`title`/`description`/`models`/`endsAt` 全部同值 —— "
         "**即官方没有清理这条已过期的促销**（避坑 230）。"
         "**⚠️ 052 期挂账项⑨问的是「那 `7` 条已过期仍在数组里的条目会不会被清理」—— 本期销项，答案是「一条都没清理」**；"
         "**且「已过期条目数」从 052 期的 `7` 条变成了 `9` 条 —— "
         "多出的两条是 `endsAt` 恰为 `10/29` 的 `klingai-video-4-0-launch-promo` 与 "
         "`pruna-p-video-2-pro-references-launch-promo`（052 期属「截止日当天」、本期转「已过期」）** —— "
         "**⚠️ 这个 `7 → 9` 不是官方新增了什么、也不是官方清理了什么，是基准日推进的自然结果**"
         "（新立避坑 238）。",
)

# ================= 四、Runware pruna-p-video-upscale（距今天数由重算器处理） =================
# ⚠️ 只做「本期实访同值」的记账，天数由 recalc_days053.py 独立重算（不靠批量减一）。

# ================= 五、Mistral Large 4 公开预览行 → 权重已公开 =================
REWRITE["🟢 **Mistral Large 4 公开预览（含 OpenRouter 五折）**"] = build(
    "🟢 **Mistral Large 4 公开预览（含 OpenRouter 五折）**",
    [
        ("**权重月底（官方口径「十月底」；媒体口径 10/27）；五折限前两周**",
         "**未公布（权重已于官方一手 `Hugging Face` 提交记录 `Initial release` 逐字 `2026-10-29T14:11:16Z` 公开 —— "
         "**原登记的权重截止日已兑现**；五折限前两周，官方未给确切日历日）**"),
    ],
    tail="**⚠️ （053 期）本行的截止日兑现了 —— 官方权重已公开（一手）**："
         "**`Hugging Face` 官方仓库 `mistralai/Mistral-Large-4-1T-A52B`（模型页 `200` / `291,884` 字节）**："
         "**提交历史只有 `3` 条 —— `Initial release`（`2026-10-29T14:11:16Z`）+ 两次 `Update README.md`；"
         "文件树 `67` 个文件、含 `54` 个 `consolidated-*-of-00054.safetensors` 分片（单片约 `19.97` GB）**；"
         "**`tags` 里带 `license:other`**。"
         "**⚠️ 官方逐字（`README.md`）**：`Official demos run on the Mistral API with a small shared free budget "
         "per visitor for the first week of the release, so you can try the model without paying.` —— "
         "**这是本报告至今第一次从「权重发布公告本身」读到「明写期限 + 明写免费」的免费额度**"
         "（此前只有 `Google Antigravity` 的科研 6 个月档与个人 `$0/month` 档两条，且都出自定价页）。"
         "**⚠️ 但官方给的是「发布后第一周」这个相对期限、没给具体日历日，"
         "且额度只写「`a small shared free budget`」没给数字 —— 本报告因此不推算截止日、不写「无限」**（避坑 154）。"
         "**⚠️ 许可证全文已核到（`LICENSE` `200` / `2,632` 字节）**："
         "`Mistral Ecosystem Open-Weight License` 逐字 `a modified version of the MIT license`、"
         "逐字 `for both commercial and non-commercial use — operating a Model-as-a-Service business "
         "requires a separate commercial license with Mistral` —— "
         "**即「能商用、但 `MaaS` 要另签」；官方对 `MaaS` 的定义逐字排除了两种情形"
         "（嵌进自己产品、转手转发别人托管的模型）**（新立避坑 235）。"
         "**⚠️ 官方域名 `mistral.ai` 本期仍全站不可达（连续第 `13` 次）—— "
         "本期全部一手证据取自 `Hugging Face` 上的官方权重仓库与 `GitHub` 上的官方 `Mistral Vibe` 仓库**"
         "（新立避坑 234）。"
         "**⚠️ 社区量化生态（发布后 `7` 小时内已铺开）**："
         "`unsloth/Mistral-Large-4-1T-A52B-GGUF`（`createdAt 2026-10-29T11:24:56Z`）逐字 "
         "`Run the smallest 1-bit (233 GB) on a 256GB RAM device, 2-bit (302-378 GB) on 384-512GB, "
         "or near full precision (Q8, 1.1 TB) on 1.2TB+.`、"
         "`mlx-community` 的 `Text-2bit` / `Text-3bit` / `Text-4bit`（`10/29` 15:47 / 15:56 / 16:05 UTC）、"
         "`akhaliq/…-LeTrim-NVFP4`（`10/29` 16:13 UTC）—— "
         "**⚠️ 这些都是社区仓库、不是官方发布（`Mistral` 官方只发了 `…-1T-A52B` 与 `…-NVFP4` 两个仓库）**（避坑 195）。",
)

# ================= 六、Google Nano Banana 2 停用（10/29 → 相对 10/30 已过期 1 天） =================
REWRITE["🟢 **Google Nano Banana 2 停用（Gemini API）**"] = build(
    "🟢 **Google Nano Banana 2 停用（Gemini API）**",
    [
        ("🟢 **未开始（距今 0 天）。 ⚠️ Google 未公布具体停机时刻；**",
         "🟢 **生效中（停用日 10/29 已过 · 本期基准日 10/30 已过 1 天 · "
         "**官方未公布具体停机时刻，故本报告不写「已停用」**）。 ⚠️ Google 未公布具体停机时刻；**"),
    ],
    tail="**⚠️ （053 期）这条的截止日跨过了基准日 —— 三态要分开写**："
         "052 期（基准日 `10/29`）它属「截止日当天」（避坑 223），"
         "**本期（基准日 `10/30`）真值是「停用日已过 `1` 天」**。"
         "**⚠️ 本报告只写「停用日已过」，不写「已停用」** —— **官方未公布具体停机时刻、"
         "本轮 `Google` 一手全线不可达（`ai.google.dev` / `aistudio.google.com` / `blog.google` / "
         "`deepmind.google` 全部不可达，连续第 `3` 期）** —— "
         "**「截止日已过」与「已确认停用」是两件事**（避坑 154）。",
)

NEW = []

# ---- 本期新增 1：Mistral Large 4 官方 demo 首周免费预算 ----
NEW.append(
    "| 🟡 **`Mistral Large 4`（`Le Chonk`）官方 demo 首周共享免费预算"
    "（**官方一手逐字 `a small shared free budget per visitor for the first week of the release`**）** | "
    "**未公布（官方逐字 `for the first week of the release` —— **相对期限，官方未给具体日历日**）** | "
    "🟡 **生效中（**限时免费 · **官方一手来源是 `Hugging Face` 模型卡的 `Demo Gallery` 段，"
    "不是定价页、不是新闻稿**）。 "
    "⚠️ 官方逐字（`huggingface.co/mistralai/Mistral-Large-4-1T-A52B/raw/main/README.md`，`200` / `19,063` 字节）："
    "`Official demos run on the Mistral API with a small shared free budget per visitor for the first week "
    "of the release, so you can try the model without paying. You can also use your own Mistral API key.` "
    "⚠️ 四层开放（避坑 41）：① 能用 —— 官方 demo（`Spaces`）逐字 `run on the Mistral API`；"
    "② 能下载 —— 权重已公开（`54` 个 safetensors 分片在线）；"
    "③ 能跑 —— **官方未给额度数字**（逐字只写 `a small shared free budget`，本报告不写「无限」、不写数字）；"
    "④ 能商用 —— 官方 demo 与自备 key 两条路径都可用（**但 `MaaS` 另签商业许可**，见 `Mistral` 许可证那行）。 "
    "⚠️ **三条边界**：① **资格逐字是 `per visitor`（每位访客），不是「每个账号」**；"
    "② **官方用词是 `small` + `shared` 双重限定**（所有访客共享的一个小池子），"
    "**本报告不写「人人有份无限额度」**（避坑 154）；"
    "③ **官方给的是「发布后第一周」这个相对期限、没给日历日 —— 本报告不替它推算截止日**。 "
    "⚠️ **本条的价值在「取数路径」而非「额度数字」** —— 这条带期限的免费额度公告"
    "**在官方定价页（`mistral.ai` 本期不可达）、在聚合器、在 `TechCrunch` 报道里全部没有出现**"
    "（**新立避坑 233：权重发布类事件必须去读官方模型卡全文**）。** |"
)

# ---- 本期新增 2：国家超算互联网夜间限时免费 ----
NEW.append(
    "| 🟠 **`国家超算互联网` 夜间限时免费调用 `Auto` 模型"
    "（**官方逐字 `10月21日至30日，每晚21:00至次日09:00`** · **⚠️ 官方页未核到，媒体转述**）** | "
    "**10/30（官方逐字「`10月21日至30日`」—— **截止日＝本期基准日当天**）** | "
    "🟠 **生效中（限时免费 · **资格限「订阅 `TokenPlan` 用户」**）。 "
    "⚠️ 官方逐字（**媒体转述官方公告**，`leiphone.com/category/industrynews/tZQilZ5sagKCk1Sm.html`，"
    "`200` / `47,685` 字节，雷峰网 `2026-10-29 17:03`）："
    "`订阅TokenPlan用户还可享限时夜间免费模型权益：10月21日至30日，每晚21:00至次日09:00，Auto模型可免费调用。` "
    "⚠️ 四层开放（避坑 41）：① 能用 —— 逐字 `Auto模型可免费调用`；"
    "② 能下载 —— **不适用**（云端调用服务、不是可下载的模型）；"
    "③ 能跑 —— **时段与截止日都明确，额度数字官方未给**；"
    "④ 能商用 —— **官方口径未涉及**。 "
    "⚠️ **三条边界**：① **资格不是「所有人」** —— 逐字 `订阅TokenPlan用户`（**必须先订阅 `TokenPlan`**）；"
    "② **截止日 `10/30` ＝ 本期基准日当天** —— **既不是「已过」也不是「未到」，是第三个状态**（避坑 223）；"
    "③ **另有一条 `0.1元5000万tokens限时秒杀`（`DeepSeek-V4.1-Flash-1017`、`GLM-5.3-Flash`）—— "
    "**那是付费特惠不是免费、且官方同样没给它的截止日**。 "
    "⚠️ **取证缺口如实写**：本轮实访 `www.scnet.cn`（`200` / `132,762` 字节）—— "
    "**「`TokenPlan`」「夜间」「`21:00`」「`0.1元`」「免费」五个词在该页各命中 `0` 次** —— "
    "**官方页未核到，本条是媒体转述**（避坑 154）。** |"
)

# ---- 本期新增 3：MOSS-Image 开放权重（052 期挂账项②销项） ----
NEW.append(
    "| 🟢 **`MOSS-Image` 开放权重图像生成系统"
    "（**`5B` 单流 `DiT` · **`Apache-2.0` 商用许可** · `Diffusers`/`Gradio`/`ComfyUI` 三条路径**）** | "
    "**无结束日（权重永久开放，`Apache-2.0`；官方未给任何活动期或截止日）** | "
    "🟢 **已开放权重（第 ④ 级已到 · **052 期挂账项②销项 · 官方一手页全文本期补登**）。 "
    "⚠️ 官方一手（`openmoss.ai/blog/cn/moss-image/`，`200` / `17,457` 字节）："
    "`一个 5B 开放权重图像生成系统`、`Base 与 SFT 权重采用 Apache-2.0，提供 Diffusers、Gradio 和 ComfyUI 路径，"
    "并支持 LoRA 与全量微调`、`96.3 LLTB Mean-6，开放权重模型最高`、`0.8786 7Bench mIoU det`、"
    "`1698.70 RLA 端到端 Elo`、`4K 最长提示词 token 上限`。 "
    "⚠️ 四层开放（避坑 41）：① 能用 —— 逐字 `提供 Diffusers、Gradio 和 ComfyUI 路径`；"
    "② 能下载 —— **是**（`Base` 与 `SFT` 两套权重，`HF` 实读 `OpenMOSS-Team/MOSS-Image-Base`（`9,725` 下载）"
    "与 `…-SFT`（`14,950` 下载）、`Comfy-Org/MOSS-Image`（`3,401,045` 下载））；"
    "③ 能跑 —— 逐字 `支持 LoRA 与全量微调`；④ 能商用 —— **逐字 `Apache-2.0`**"
    "（**本报告至今少见的「开放权重 + 明确商用许可」组合**）。 "
    "⚠️ **官方自报指标的限定语照录**：逐字 `排名第二`（`RLA` 端到端 `1698.70`，`GPT Image 2` 是 `1844.35`）"
    "—— **本报告不写「第一」**（避坑 116）；逐字 `LLTB 衡量的是文字覆盖与渲染质量，"
    "不能直接等同于 OCR 编辑距离或语义事实准确率`。 "
    "⚠️ **归期**：官方页按 `publishedAt 10/28` 属 051 期窗口 —— **052 期已定位链接、本期按其挂账项②补登全文**"
    "（避坑 229：**聚合站的收录时间不是发布时间**）。** |"
)

# ---- 本期新增 4：OpenAI 付费档翻倍（Plus 不变） ----
NEW.append(
    "| 🟡 **`OpenAI` 付费档用量上限翻倍（**`Pro 100` / `Pro 500` 翻倍 · `Pro 200` 翻倍并撤回原计划下调**）"
    "—— **⚠️ `Plus` 档不变（免费读者唯一相关的一条）** | "
    "**未公布（官方未给任何活动期或截止日）** | "
    "🟡 **生效中（**付费档变动 · **不是免费额度条目**）。 "
    "⚠️ 官方逐字（**媒体转述官方公告**，`the-decoder.com/openai-doubles-usage-limits-on-pro-plans-as-competition-with-anthropic-heats-up/`，"
    "`200` / `117,469` 字节，`The Decoder` `Oct 29, 2026`，**页面标注来源为 `OpenAI`**）："
    "`OpenAI has doubled usage limits for several paid tiers. The changes affect Work and Codex quotas "
    "on the Pro 100 and Pro 500 plans, which both get twice the previous allotment. On Pro 200, OpenAI doubled "
    "the lower quota and reversed a planned cut after user pushback. The Plus plan stays the same.` "
    "⚠️ **本报告只登记「`Plus` 档不变」这一条** —— **被改的三档都是付费档**（避坑 41：**多档位口径要拆开写**）。 "
    "⚠️ **三条边界**：① **改的是 `Work` 与 `Codex` 两类配额、不是消息条数**；"
    "② **官方自己说了「翻倍 ≠ 任务数翻倍」** —— 逐字 `Doubling a quota doesn't mean twice as many completed tasks, "
    "OpenAI says, since consumption varies by model, task type, and settings.`；"
    "③ **`Pro 200` 那条是「翻倍 + 撤回原计划的下调」两件事**。 "
    "⚠️ **取证缺口如实写**：官方 `platform.openai.com/docs/models` 本期仍 `403`（连续第 `6` 期）、"
    "`openai.com/api/pricing/` 虽 `200` 但 `free tier` 零命中 —— **本条是媒体转述**（避坑 154）。** |"
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
for k in REWRITE:
    assert sum(1 for r in body if k in r) == 1, ("REWRITE 键在源 body 中命中数异常", k[:60], sum(1 for r in body if k in r))
# ---- 断言 1b：改写后的每一行在输出中恰好出现 1 次（无重复、无丢失）----
for k, v in REWRITE.items():
    assert res.count(v) == 1, ("REWRITE 值在输出中出现次数异常", k[:60], res.count(v))
# ---- 断言 1c：未改写的行必须原样出现在输出中（数量守恒）----
untouched = [r for r in body if not any(key in r for key in REWRITE)]
assert len(untouched) == PREV - len(REWRITE), ("未改写行数异常", len(untouched), PREV - len(REWRITE))
for r in untouched:
    assert res.count(r) == 1, ("未改写行在输出中丢失或重复", r[:60])

# ---- 断言 2（052 期立的，本期加严）：**重新读回落盘文件**再断言 ----
#   ⚠️ 052 期的断言只校验字典本身（值在「输出」中恰好出现一次 —— 那个「输出」是字典值、不是落盘文件），
#   所以 051 期的「10 行改写一行没进交付物」能一路通过断言。本期必须读回落盘文件。
disk = io.open(OUT, encoding="utf-8").read().replace("\r\n", "\n")
assert disk == res, ("落盘文件与内存结果不一致", len(disk), len(res))
for k, v in REWRITE.items():
    assert disk.count(v) == 1, ("REWRITE 值未真正进落盘文件", k[:60], disk.count(v))
for r in untouched:
    assert disk.count(r) == 1, ("未改写行在落盘文件中丢失或重复", r[:60])
print("断言 2 通过：改写已真正进落盘文件（复读校验）")

# ---- 断言 3：表体关键口径 == 正文关键口径（避坑 239：断言全过 ≠ 事实全对）----
CHECKS = [
    ("456", "OpenRouter 全量目录数"),
    ("18,141", "百度 Unlimited OCR 2 下载量"),
    ("upstage/solar-pro-3", "OpenRouter 本期消失的条目"),
    ("Initial release", "Mistral ML4 权重发布提交"),
    ("a small shared free budget", "Mistral 官方免费预算逐字"),
    ("Mistral Ecosystem Open-Weight License", "Mistral 许可证名"),
    ("10月21日至30日", "国家超算互联网夜间免费逐字"),
    ("Apache-2.0", "MOSS-Image 许可"),
    ("The Plus plan stays the same", "OpenAI Plus 档不变逐字"),
    ("18,141", "百度下载量"),
]
for needle, label in CHECKS:
    assert needle in disk, ("表体缺关键口径", label, needle)

# ---- 断言 4：本期新增的每个截止日都必须能在表体里查到（防「正文写了、表体没有」）----
for needle in ["10/30", "发布后第一周", "无结束日", "未公布"]:
    assert needle in disk, ("新增行截止列口径缺失", needle)

nrows = len([l for l in out if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")])
print("rows %d = %d + %d" % (nrows, PREV, len(NEW)))
from collections import Counter
print("字段数分布", Counter([l.count("|") - 1 for l in out if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]))
print("CHECKS 全部通过")
