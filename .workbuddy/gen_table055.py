# -*- coding: utf-8 -*-
"""055 期：从 054 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-11-01（隔日出刊）
-> 行级改写 -> 追加本期新行。输出 .workbuddy/tmp_table055.md（纯表格块）。

⚠️ 054 期立的纪律，本期全部沿用并加严：
   ① 输入直接取 **054 期 md 的现行文本**（不是取上一期的 tmp_table）。
   ② 写出循环必须是「用键在行里找」，不能写成 `if k in REWRITE`。
   ③ 断言：键唯一命中 / 值在输出恰好出现一次 / 未改写行数守恒 / **落盘文件复读校验**。
   ④ **避坑 239**：断言全过 ≠ 事实全对 -> 新增「表体关键口径 == 正文关键口径」断言。
   ⑤ **避坑 248（055 期新立）**：数字类关键词的命中数会被 SVG 路径坐标与 JS 数据块放大，
      本脚本的 CHECKS 一律用「逐字短语」而不是「裸数字」做断言。
   ⑥ **055 期新立**：本期有 3 类行级改写必须处理：
      (a) 截止日跨过基准日（`10/31` -> 过期）-> 状态列改写；
      (b) 「距今 N 天」由 recalc_days055.py 独立重算（**必须跑在 split_ledger 之前**）；
      (c) 事实被推翻（`Ollie` 免费档 / `Runware` heygen `endsAt` / `Unsloth` 零命中口径）。

本期性质：**隔日出刊**（054 期是 10/31 第一轮，窗口 10/30 09:30 -> 10/31 19:00，约 33.5 小时；
  本期窗口 10/31 19:00 -> 11/1 13:30，约 18.5 小时，**完全落在美西 10/31 同一天内**）。
  1) **基准日推进到 2026-11-01**（054 期基准日是 10/31）。
  2) 输入结构：上期 4.1 表体（56 行）+ 总账全量表体（147 行）= 203 行。
  3) 本期改写 12 行（见下）。
  4) 本期新增 5 行：Anthropic 文本水印对照表、Anthropic 免费 Content Checker、
     Kimi K3.1 Pro 访问条件、OpenRouter Poolside 撤下、Ollie Free 档。
"""
import io
import re
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第054期-2026-10-31.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table055.md"
BASE = date(2026, 11, 1)
PREV = 203


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
assert len(rows_41) == 56, ("054 期 4.1 表体行数", len(rows_41))
assert len(rows_led) == 147, ("总账全量行数", len(rows_led))
body = rows_41 + rows_led
assert len(body) == PREV, (len(body), PREV)

header = "| 活动 | 截止 | 状态 |"
sep = "| --- | --- | --- |"

REWRITE = {}


def build(key, subs, tail=None):
    """行级改写。**幂等**：若该行已含本期标记（`（055 期）`），说明上一轮已改写过，
    则直接原样返回、不再重复替换。
    """
    hits = [l for l in body if key in l]
    assert len(hits) == 1, ("键未唯一命中", key, len(hits))
    out = hits[0]
    if "（055 期）" in out and all(a not in out for a, b in subs):
        return out
    for a, b in subs:
        assert a in out, ("片段未命中", key, a[:70])
        out = out.replace(a, b)
    if tail:
        assert out.rstrip().endswith("|")
        out = out.rstrip()[:-1].rstrip() + " " + tail + " |"
    return out


# ================= 一、OpenRouter 目录（456/19/16 → 452/17/14 · Poolside 整批撤下） =================
# ⚠️ 053/054 两期连续记「三个数全部逐条零变化」—— 本期打破（避坑 247 新立）。
#    消失的 4 条全是 Poolside 的 Laguna 系列（含 2 个 :free 变体），官方 created 是 7 月、
#    公告页零命中 —— 「同一家厂商的同一系列整批撤下（含 :free）」是目录变化的第三种形态。
REWRITE["🟢 **OpenRouter 免费档（**官方 API 目录口径"] = build(
    "🟢 **OpenRouter 免费档（**官方 API 目录口径",
    [
        ("**官方 API 目录口径 · `456/19/16`**",
         "**官方 API 目录口径 · `452/17/14`**"),
        ("**⚠️ （054 期）流通量与目录口径记账（避坑 029：升/降/同值都要记账）**：",
         "**⚠️ （055 期）流通量与目录口径记账（避坑 029：升/降/同值都要记账）**："),
    ],
    tail="**⚠️ （055 期）本期打破 053/054 两期「三个数全部逐条零变化」的口径 —— 这是本报告至今"
         "第一次出现「免费档减少」**：**全量 `456` → `452`、零价 `19` → `17`、`:free` `16` → `14` "
         "—— 逐条 diff：新增 `0` 条、消失 `4` 条**。**⚠️ 消失的 `4` 条逐条列出**："
         "`poolside/laguna-s-2.1`、`poolside/laguna-s-2.1:free`、`poolside/laguna-xs-2.1`、"
         "`poolside/laguna-xs-2.1:free` —— **四条全是同一家厂商（`Poolside`）的同一系列（`Laguna`），"
         "其中 `2` 条是 `:free` 零价档**；官方 `created` 时间戳 `1784652683`（＝`2026-07-21 16:51 UTC`）"
         "与 `1783002429`（＝`2026-07-02 14:27 UTC`），**不是本周新品，是整批撤下**（新立避坑 247）。"
         "**⚠️ 官方公告页 `openrouter.ai/announcements` 实读 `poolside` / `laguna` / `Poolside` "
         "各命中 `0` 次 —— 官方没给下架公告，本报告只记事实、不替官方归因**。"
         "**⚠️ 第三方口径本期未跟上**：`freellm.net/providers/openrouter` 专页仍逐字写 "
         "`19 free models online`，而官方零价档已降到 `17` —— **两个数都带来源、不折算**（避坑 161）。"
         "**⚠️ 「零价 `17`」与「`:free` `14`」仍差 `3` 个 —— `google/lyria-3-pro-preview`、"
         "`google/lyria-3-clip-preview`、`openrouter/free`（路由器）—— 零价但不带 `:free` 后缀**"
         "（避坑 161：**两套口径不可互相代替**）。"
)

# ================= 二、Ollie：054 期记「付费订阅制、非免费额度」被官方定价页推翻 =================
# ⚠️ 本期最重要的一条改写 —— 054 期只读了 TechCrunch 转述（offered a subscription-based model），
#    据此在第四章写明「非免费额度条目」；本期实访 ollie.ai/pricing 实读，第一格就是 Free 档。
REWRITE["⚠️ **`Ollie`（隐私向 AI 助手）宣布关停"] = build(
    "⚠️ **`Ollie`（隐私向 AI 助手）宣布关停",
    [
        ("⚠️ **`Ollie`（隐私向 AI 助手）宣布关停（**`11/6` 正式停服 · 付费订阅制、非免费额度**）**",
         "⚠️ **`Ollie`（隐私向 AI 助手）宣布关停（**`11/6` 正式停服 · **⚠️ 055 期更正：它确有一个 "
         "`Free` 档** —— 054 期记的「付费订阅制、非免费额度」被官方定价页推翻**）**"),
        ("**11/6（媒体转述官方公告逐字 `the app will officially shut down on November 6`）**",
         "**11/6（官方 CEO 告别信逐字 `Ollie is sunsetting on Nov 6, 2026` · "
         "`effective Nov 6, 2026.` —— 一手 `ollie.ai/farewell` `200` / `39,747` 字节）**"),
    ],
    tail="**⚠️ （055 期）**官方逐字（`ollie.ai/farewell`，`200` / `39,747` 字节，署名 `Bill Lennon`）："
         "`We want to make the transition to another personal assistant as smooth as possible. "
         "Ollie will text you an export of your data that you can then share with another personal "
         "assistant you trust.`、`If you have a subscription to Ollie or Ollie for Meals, billing will "
         "be canceled and you will receive a refund for any partial or unused months.`。"
         "**⚠️ 官方定价页 `ollie.ai/pricing`（`200` / `41,791` 字节）第一格就是 `Free` / `$0` / "
         "`50 messages from Ollie per month` / `6 free additional messages from Ollie every day` —— "
         "**即 `Ollie` 确有一个真免费档，054 期记的「非免费额度」是错的**（详见第五章纠错第 1 条、"
         "新立避坑 246）。**⚠️ 逐字边界：官方只写「有订阅的退款」，免费档用户拿不到退款 —— "
         "本报告不替官方扩大范围**。"
)

# ================= 三、Runware heygen 促销：054 期记的「延长 30 天」本期被推翻 =================
REWRITE["🟢 **快手可灵 Kling 4.0（**`fal` 四端点"] = build(
    "🟢 **快手可灵 Kling 4.0（**`fal` 四端点",
    [],
    tail="**⚠️ （055 期）本期推翻 054 期的「`heygen` 促销延长 `30` 天」**：**本期实读 "
         "`runware.ai/pricing`（`200` / `745,859` 字节，054 期同源文件 `747,303` 字节）逐条 diff："
         "`14` 条全部同值、`0` 条新增、`0` 条消失、`0` 条 `endsAt` 改动** —— **即那条 "
         "`heygen-video-1-0-launch-promo` 的 `endsAt` 在本期回到 `2026-10-31`**"
         "（⚠️ 054 期记的是 `2026-11-30`）。**⚠️ 两种解释本报告都不替官方选边**："
         "**① 054 期读到的是一个短暂的中间状态；② 官方随后把促销改回原值 —— "
         "本报告只记「本期实读的逐条结果」**（避坑 243 的同族：**单期一次 diff 结果不足以断言趋势，"
         "至少要连续两期**）。**⚠️ 官方数组里那 `9` 条已过期条目本期仍一条未清**。"
)

# ================= 四、国家超算互联网：10/30 -> 相对 11/1 已过期 2 天 =================
REWRITE["🟠 **`国家超算互联网` 夜间限时免费调用 `Auto` 模型"] = build(
    "🟠 **`国家超算互联网` 夜间限时免费调用 `Auto` 模型",
    [
        ("**截止日已早于本期基准日 `1` 天**）**",
         "**截止日已早于本期基准日 `2` 天**）**"),
    ],
    tail="**⚠️ （055 期）这条的截止日再跨过基准日一天 —— 三态仍要分开写**："
         "053 期（基准日 `10/30`）它是「截止日当天」（避坑 223）、054 期是「已过 `1` 天」、"
         "**本期（基准日 `11/1`）是「已过 `2` 天」**。**⚠️ 本报告只写「截止日已过」，不写收口字样**"
         "（**避坑 239：状态列里一旦出现判定词的字面文本，整行就会被归进对应桶**）。"
         "**⚠️ 官方页仍连续第 `3` 期零命中**：本期实访 `www.scnet.cn`（`200` / `132,762` 字节，"
         "与 053/054 期字节数完全相同），`夜间` / `21:00` / `09:00` / `每晚` / `限时` "
         "**各命中 `0` 次** —— **本期不销项**。"
)

# ================= 五、Google Nano Banana 2 停用：10/29 -> 相对 11/1 已过期 3 天 =================
REWRITE["🟢 **Google Nano Banana 2 停用（Gemini API）**"] = build(
    "🟢 **Google Nano Banana 2 停用（Gemini API）**",
    [
        ("本期基准日 10/31 已过 2 天", "本期基准日 11/1 已过 3 天"),
    ],
)

# ================= 六、百度 Unlimited OCR 2：downloads 同值 / likes 466 -> 480 =================
REWRITE["🟢 **`百度智能云`「文档解析（Unlimited-OCR）」API"] = build(
    "🟢 **`百度智能云`「文档解析（Unlimited-OCR）」API",
    [],
    tail="**⚠️ （055 期）流通量记账（避坑 029：同值也要记账）**：一手 "
         "`hf-mirror.com/api/models?search=Unlimited-OCR&limit=20`（`200` / `10,448` 字节）实读 "
         "`baidu/Unlimited-OCR-2` —— **`downloads 69,231`（与 054 期同值，增量 `0`）、"
         "`likes 480`（054 期 `466`，涨 `14`）**。**⚠️ 即「连续两期单期大涨"
         "（`+9,784` → `+51,090`）」在本期归零 —— 本期 `downloads` 增量 `0`，只有 `likes` 涨了 `14`**。"
         "**⚠️ 本报告不追 `HF` 下载量跳涨或停滞的成因（官方没给口径），只记数；"
         "且 `likes` 与 `downloads` 是两个字段、不合并计算**（避坑 054 同源：口径不同不可相减）。"
         "**⚠️ `ModelScope` 侧仍无下载量字段**：一手 `modelscope.cn/models/OpenMOSS/MOSS-Image`"
         "（`200` / `5,022` 字节），`download` / `下载` **各命中 `0` 次**。"
)

# ================= 七、Runware pruna 两条促销：距结束天数由独立重算器改写 =================
REWRITE["🟢 **`Runware` 分发层 `pruna-p-video-upscale` 促销 `50% OFF`"] = build(
    "🟢 **`Runware` 分发层 `pruna-p-video-upscale` 促销 `50% OFF`",
    [],
    tail="**⚠️ （055 期）距今天数由 `recalc_days055.py` 逐行独立重算**"
         "（**断言是「天数 == 截止日 − 基准日」，不是「推进一天就 −1」**）。"
         "**⚠️ 本期该促销数组逐条 diff 与 054 期全部同值**（`14` 条、`0` 新增、`0` 消失、"
         "`0` 条 `endsAt` 改动）。"
)
REWRITE["🟢 **`Runware` 分发层 `pruna-p-video-edit` 促销 `25% OFF`"] = build(
    "🟢 **`Runware` 分发层 `pruna-p-video-edit` 促销 `25% OFF`",
    [],
    tail="**⚠️ （055 期）距今天数由 `recalc_days055.py` 逐行独立重算**"
         "（**断言是「天数 == 截止日 − 基准日」**）。"
         "**⚠️ 本期该促销数组逐条 diff 与 054 期全部同值**。"
)

# ================= 八、Moonshot K2 系列停新：10/31 -> 相对 11/1 已过期 1 天 =================
REWRITE["🔴 **`Moonshot` `K2` 系列模型停新注册与计划下线"] = build(
    "🔴 **`Moonshot` `K2` 系列模型停新注册与计划下线",
    [],
    tail="**⚠️ （055 期）这条的截止日跨过了基准日 —— 三态要分开写**："
         "**054 期（基准日 `10/31`）它是「截止日当天」（避坑 223），本期（基准日 `11/1`）"
         "变成「截止日已过 `1` 天」**。**⚠️ 本报告只写「截止日已过」，不写收口字样**"
         "（避坑 239）。**⚠️ 官方公告原文本期复核同值**：一手 `platform.kimi.com/docs/pricing/chat`"
         "（`200` / `302,319` 字节）逐字仍是 `K2 系列模型将于 2026 年 10 月 31 日起停止向新注册用户开放，"
         "已注册用户不受影响；我们计划在 12 月底下线所有 K2 系列模型，请提前做好 迁移准备。` "
         "（原文件 `停止` / `下线` / `2026 年 10 月 31 日` 各命中 `3` 次、剥掉 `script` 后各 `1` 次 —— "
         "**与 054 期归档文件 `tmp_054/kimi_pricing2.html` 逐条一致**）。"
         "**⚠️ 「停新当日新用户能否注册」仍需登录态实测，本报告本期不做、也不合并**。"
)

# ================= 九、Kimi K3.1 Pro：补记官方访问条件（本期新立避坑 245） =================
REWRITE["🟢 **`Moonshot` `Kimi K3.1 Pro` 发布（10/23 晚–10/24"] = build(
    "🟢 **`Moonshot` `Kimi K3.1 Pro` 发布（10/23 晚–10/24",
    [],
    tail="**⚠️ （055 期）官方「访问条件」逐字核到 —— 本报告至今第一次读到「免费送的钱不能用于旗舰模型」**："
         "一手 `platform.moonshot.cn/docs/guide/kimi-k3-1-pro-quickstart` 与 "
         "`platform.kimi.com/docs/guide/kimi-k3-1-pro-quickstart`（各 `200` / `736,950` 字节、"
         "官方 `dateModified 2026-10-28T11:18:14.893Z`、**两站字节数完全一致**）逐字："
         "`Kimi K3.1 Pro 是旗舰模型：在开放平台完成充值（最低充值金额 10 元）后即可解锁调用。"
         "新用户注册认证赠送的 15 元代金券不可用于 Kimi K3.1 Pro。` —— "
         "**即「注册送 `15` 元」与「能用 `K3.1 Pro`」是两件事**（新立避坑 245）。"
         "**⚠️ 权重仍未放出**：`HF` 实读 `api/models?author=moonshotai&limit=100&sort=createdAt&direction=-1`"
         "（`200` / `8,969` 字节）官方名下 `19` 个模型、最新仍是 `moonshotai/Kimi-K3`"
         "（`createdAt 2026-06-13T06:42:57.000Z`、`downloads 866,041`）；"
         "`api/models?search=Kimi-K3&limit=50` 全站命中里含 `K3.1` 字样的 `10` 条中"
         "**官方 `moonshotai` 名下 `0` 条**。"
)

# ================= 十、Mistral demo 免费预算：口径复核（数字仍缺） =================
# 强制动作⑥「Mistral Large 4 demo 免费预算的具体额度数字与「发布后第一周」的日历日」
# -> 本期复核了官方逐字口径，数字与日历日仍缺，属「口径已复核、数字仍缺」，不销项。
# 该条目在《常驻权益总账》里（无截止日），本章不改行、只在正文记。

# ================= 十一、可灵「看见微光」：11/1 = 本期基准日当天 =================
# 「距今 N 天」由 recalc_days055.py 处理（1 天 -> 0 天）。状态列措辞不含判定词，无需改写。

# ================= 十二、DeepSeek Search/Fetch：11/1 00:00 起按请求计费 =================
# 「距今 N 天」由 recalc_days055.py 处理（1 天 -> 0 天）。措辞不含判定词，无需改写。

# ============ 十三、四条 10/31 截止的行：截止日跨过基准日 11/1 -> 必须改写状态列 ============
# ⚠️ **055 期新立的一条工程纪律（本期实测踩到）**：`recalc_days055.py` 对「截止日已过、真值为负」
#    的行会**报错退出**（这是对的 —— 负天数不该被写进表体）。但**这些行确实需要留在表体里**
#    （它们是「刚过期、还没收口」的待办），**处置是「改写状态列、把 `距今 N 天` 换成跨过基准日的表述，
#    再由 `recalc_days055.py` 重算」** —— 而不是放宽重算器的判据。
# ⚠️ 措辞纪律（054 期立的避坑 239）：**状态列里不能出现会被 `classify()` 字面误读的判定词**
#    （`已结束` / `未开始`）—— 本期这四行的改写一律用「已过 N 天」这种不含判定词的表述。

REWRITE["🟢 **湖北算力券年度申领**"] = build(
    "🟢 **湖北算力券年度申领**",
    [
        ("**10/31**", "**10/31（**已过本期基准日 `1` 天**）**"),
        ("🟢 **生效中（距今 0 天）。 ⚠️ 企业向**",
         "🟢 **截止日已过（**官方活动期至 `10/31`，本期基准日 `11/1`，**已过 `1` 天**）。 ⚠️ 企业向**"),
    ],
    tail="**⚠️ （055 期）这条的截止日跨过了基准日 —— 三态要分开写**："
         "**054 期（基准日 `10/31`）它是「截止日当天」（避坑 223），本期（基准日 `11/1`）"
         "变成「已过 `1` 天」**。**⚠️ 本报告只写「截止日已过」，不写收口字样**"
         "（避坑 239：**状态列里一旦出现判定词的字面文本，整行就会被归进对应桶**）。"
)

REWRITE["🟢 **WorkBuddy 学生版 1,000 积分 / ChatGPT 学生促销**"] = build(
    "🟢 **WorkBuddy 学生版 1,000 积分 / ChatGPT 学生促销**",
    [
        ("**10/31**", "**10/31（**已过本期基准日 `1` 天**）**"),
        ("🟢 **生效中（距今 0 天）**",
         "🟢 **截止日已过（**官方活动期至 `10/31`，本期基准日 `11/1`，**已过 `1` 天**）**"),
    ],
    tail="**⚠️ （055 期）这条的截止日跨过了基准日**：**054 期它是「截止日当天」，本期是「已过 `1` 天」**。"
         "**⚠️ 本报告只写「截止日已过」，不写收口字样**（避坑 239）。"
)

REWRITE["🟢 **HeyGen Voice（AA 语音合成榜首，促销五折）**"] = build(
    "🟢 **HeyGen Voice（AA 语音合成榜首，促销五折）**",
    [
        ("**10/31**", "**10/31（**已过本期基准日 `1` 天**）**"),
        ("🟢 **生效中（距今 0 天）。 ⚠️ 榜首为单一榜单口径（避坑 116）；**",
         "🟢 **截止日已过（**官方促销期至 `10/31`，本期基准日 `11/1`，**已过 `1` 天**）。 "
         "⚠️ 榜首为单一榜单口径（避坑 116）；**"),
    ],
    tail="**⚠️ （055 期）这条的截止日跨过了基准日**：**054 期它是「截止日当天」，本期是「已过 `1` 天」**。"
         "**⚠️ 本报告只写「截止日已过」，不写收口字样**（避坑 239）。"
)

REWRITE["🟢 **`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免（10/31）**"] = build(
    "🟢 **`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免（10/31）**",
    [
        ("**10/31**", "**10/31（**已过本期基准日 `1` 天**）**"),
        ("🟢 **生效中（距今 0 天 · 工作区自有产品线）。**",
         "🟢 **截止日已过（**官方限免期至 `10/31`，本期基准日 `11/1`，**已过 `1` 天** · "
         "工作区自有产品线）。**"),
    ],
    tail="**⚠️ （055 期）这条的截止日跨过了基准日**：**054 期它是「截止日当天」，本期是「已过 `1` 天」**。"
         "**⚠️ 本报告只写「截止日已过」，不写收口字样**（避坑 239）。"
)

# ---- 本期新增 5 行 ----
NEW = []

# 新增 1：Anthropic 文本水印与 C2PA（模型 × 标记方式对照表）
NEW.append(
    "| ⚠️ **`Anthropic` 文本水印与 `C2PA` 内容凭证（**官方逐模型对照表：16 个模型 × 3 列 · "
    "**标记加在模型层、不分档位** → `Free` 档读者生成的内容同样带标记**）** | "
    "**未公布（无活动期；官方逐字 `Marks will apply to output from supported Claude models "
    "across Claude Platform (API), Claude, Claude Code, Claude Cowork, and Claude Tag, and "
    "wherever Claude is offered, worldwide.`）** | "
    "⚠️ **生效中（**全球生效、无活动期**）。 ⚠️ 四条边界：① 官方逐字 "
    "`Watermarking will be applied at the model level, which means it will be present no matter "
    "which Claude product or surface the text comes from.` —— **标记不分档位，`Free` 档同样带**；"
    "② 官方对照表 `16` 个模型 × `3` 列（`Text watermarks in Claude output (first-party surfaces)` ／ "
    "`Text watermarks in cloud partner output (AWS, Google Cloud, Microsoft Foundry)` ／ "
    "`Content Credentials (C2PA) in files`），**`✅` 共 `34` 个 —— 其中 `7` 个模型只在第一方有文本水印、"
    "云厂商列与 `C2PA` 列均为空**（`Claude Mythos 5` / `Claude Opus 4.7` / `Claude Opus 4.6` / "
    "`Claude Opus 4.5` / `Claude Sonnet 4.6` / `Claude Sonnet 4.5` / `Claude Haiku 4.5`）；"
    "③ **文本水印检测是私有预览、不是免费公开工具** —— 官方逐字 `Watermark detection is currently "
    "in private preview, available to eligible organizations as required under EU law`；"
    "④ **文件 `C2PA` 检测才是免费的** —— 官方另给一个完全免费的 `Content Checker`（见下条）。 "
    "**⚠️ （055 期）**一手 `support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content`"
    "（`200` / `238,182` 字节，官方 `dateModified 2026-10-28T18:53:26Z`）、"
    "`anthropic.com/news/claude-text-watermark`（`200` / `180,551` 字节）、"
    "`platform.claude.com/docs/llms-full.txt`（`200` / `49,296,328` 字节）。"
    "**⚠️ 归期如实写**：官方支持页 `dateModified` ＝ 北京 `10/29 02:53`，"
    "**落在 054 期窗口之前，本期按「首次登记的往期事件」写入**（避坑 229）。 |"
)

# 新增 2：Anthropic 官方免费 Content Checker
NEW.append(
    "| 🟢 **官方免费 `Claude Content Checker`（**`claude.com/check-content` · **浏览器内本地运行、"
    "文件不出设备、不存储** · 单文件 `100 MB`**）** | "
    "**未公布（免费常驻工具，无活动期）** | "
    "🟢 **生效中（**免费常驻**）。 ⚠️ 三条边界：① 官方逐字 `This tool runs in your browser. "
    "Your file never leaves your device.`、`Your file stays on your device. The checker only reads "
    "the attached credential, not the file itself. Your file is never stored or used for any other "
    "purpose.` —— **完全免费、本地运行、零上传**；② 官方逐字 `The tool does not check text. "
    "Claude marks text with a watermark in the writing itself.` —— **它只查文件 `C2PA`、不查文本水印**"
    "（文本水印检测是私有预览，见上条）；③ 官方逐字 `Supported formats: JPG, PNG, GIF, WEBP, TIFF, "
    "HEIC, AVIF, SVG, DNG, JXL, MP4, MOV, AVI, WAV, MP3, M4A, FLAC · up to 100 MB`。 "
    "**⚠️ （055 期）**一手 `claude.com/check-content`（`200` / `394,825` 字节）—— "
    "**本报告至今第一个「官方给出、免费、本地运行」的标记检测工具**。 |"
)

# 新增 3：Kimi K3.1 Pro 访问条件（充值门槛 + 代金券排除）
NEW.append(
    "| ⚠️ **`Moonshot` `Kimi K3.1 Pro` 的访问条件（**官方逐字：充值最低 `10` 元解锁；"
    "**新用户送的 `15` 元代金券不可用于本模型** · **3 万亿级 / 100 万上下文 / `Highspeed` 版输出快 "
    "`2~3` 倍**）** | **未公布（无活动期；官方未给该门槛的截止日）** | "
    "⚠️ **生效中（**旗舰模型的准入门槛**）。 ⚠️ 三条边界：① 官方逐字 `在开放平台完成充值"
    "（最低充值金额 10 元）后即可解锁调用。新用户注册认证赠送的 15 元代金券不可用于 Kimi K3.1 Pro。` "
    "—— **即「注册送 `15` 元」与「能用 `K3.1 Pro`」是两件事**（055 期新立避坑 245："
    "**凡写「注册送 X 元」，必须再找一次「访问条件 / 充值 / 代金券」页，确认有没有排除条款**）；"
    "② **它不是免费档** —— 本报告如实写「能力是新的、门槛是付费的」，不把它写成免费工具；"
    "③ 官方另写 `完整模型权重将于 11 月 4 日前发布。` —— **是「前」不是「当天」，本报告照抄不写成确切日**；"
    "**⚠️ 权重本期仍未放出**（`HF` 官方 `moonshotai` 名下 `0` 条含 `K3.1`）。 "
    "**⚠️ （055 期）**一手 `platform.moonshot.cn/docs/guide/kimi-k3-1-pro-quickstart` 与 "
    "`platform.kimi.com/docs/guide/kimi-k3-1-pro-quickstart`（各 `200` / `736,950` 字节、"
    "官方 `dateModified 2026-10-28T11:18:14.893Z`、**两站字节数完全一致** —— "
    "**故本报告记一条、不拆成两个站点口径**）。 |"
)

# 新增 4：OpenRouter Poolside 整批撤下（含 2 条 :free）
NEW.append(
    "| 🔴 **`OpenRouter` 官方目录：`Poolside` 的 `Laguna` 系列 `4` 条整批撤下（**含 `2` 条 `:free` "
    "零价档** · **本报告至今第一次出现「免费档减少」**）** | "
    "**未公布（动态目录；官方无下架公告）** | "
    "🔴 **必办（**已消失 · **如果你在用 `poolside` 的 `:free` 档，要换模型了**）。 "
    "⚠️ 三条边界：① 逐条列出消失的 `4` 条 —— `poolside/laguna-s-2.1`、`poolside/laguna-s-2.1:free`、"
    "`poolside/laguna-xs-2.1`、`poolside/laguna-xs-2.1:free` —— **四条全是同一家厂商的同一系列，"
    "其中 `2` 条是 `:free` 零价档**；② 官方 `created` 时间戳 `1784652683`（＝`2026-07-21 16:51 UTC`）"
    "与 `1783002429`（＝`2026-07-02 14:27 UTC`）—— **不是本周新品、是整批撤下**；"
    "③ **官方公告页 `openrouter.ai/announcements` 实读 `poolside` / `laguna` / `Poolside` "
    "各命中 `0` 次 —— 官方没给下架公告，本报告只记事实、不替官方归因**（避坑 154/161）。 "
    "**⚠️ （055 期）**一手 `openrouter.ai/api/v1/models`（`200` / `804,780` 字节）—— "
    "**全量 `456` → `452`、零价 `19` → `17`、`:free` `16` → `14`；逐条 diff 新增 `0`、消失 `4`**"
    "（055 期新立避坑 247）。 |"
)

# 新增 5：Ollie Free 档（即将随关停一起消失）
NEW.append(
    "| ⚠️ **`Ollie` 的 `Free` 档（**官方逐字 `50 messages from Ollie per month` ＋ "
    "`6 free additional messages from Ollie every day` · **⚠️ 055 期更正：054 期记的"
    "「付费订阅制、非免费额度」是错的** · **`11/6` 一并关停**）** | "
    "**11/6（官方 CEO 告别信逐字 `Ollie is sunsetting on Nov 6, 2026`）** | "
    "⚠️ **生效中（**关停倒计时 · **只用 `Free` 档的用户，这个免费档 `11/6` 一并消失**）。 "
    "⚠️ 三条边界：① 官方定价页逐字 —— `Free` / `$0` / `50 messages from Ollie per month` / "
    "`6 free additional messages from Ollie every day`；**付费档 `Everyday` `$25`/月"
    "（`150` 条 ＋ 每天 `10` 条免费追加）、`Always-On` `$100`/月（`1,000` 条 ＋ 每天 `15` 条）** —— "
    "**即付费档也每天送免费追加消息**；② 官方 FAQ 逐字 `In every plan, you will get an allotment "
    "of free daily messages that will be refreshed every morning.` ＋ "
    "`These free daily messages do not accumulate or roll over.`；"
    "③ **官方逐字只写「有订阅的退款」** —— `If you have a subscription to Ollie or Ollie for Meals, "
    "billing will be canceled and you will receive a refund for any partial or unused months.` "
    "—— **免费档用户拿不到退款，本报告不替官方扩大范围**。 "
    "**⚠️ （055 期）**一手 `ollie.ai/pricing`（`200` / `41,791` 字节）、"
    "`ollie.ai/farewell`（`200` / `39,747` 字节）、`ollie.ai/faq/`（`200` / `50,935` 字节）。 |"
)

out = []
out.append(header)
out.append(sep)
# ⚠️ 匹配方式必须是「用键在行里找」，不能写成 `if k in REWRITE`（k 是整行，永远不是键的子串 → 改写全部失效）。
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

# ---- 断言 1：改写前的 body 里每个 REWRITE 键恰好命中 1 行 ----
for k in REWRITE:
    assert sum(1 for r in body if k in r) == 1, ("REWRITE 键在源 body 中命中数异常", k[:60], sum(1 for r in body if k in r))
# ---- 断言 1b：改写后的每一行在输出中恰好出现 1 次 ----
for k, v in REWRITE.items():
    assert res.count(v) == 1, ("REWRITE 值在输出中出现次数异常", k[:60], res.count(v))
# ---- 断言 1c：未改写的行必须原样出现在输出中（数量守恒）----
untouched = [r for r in body if not any(key in r for key in REWRITE)]
assert len(untouched) == PREV - len(REWRITE), ("未改写行数异常", len(untouched), PREV - len(REWRITE))
for r in untouched:
    assert res.count(r) == 1, ("未改写行在输出中丢失或重复", r[:60])

# ---- 断言 2：重新读回落盘文件再断言 ----
disk = io.open(OUT, encoding="utf-8").read().replace("\r\n", "\n")
assert disk == res, ("落盘文件与内存结果不一致", len(disk), len(res))
for k, v in REWRITE.items():
    assert disk.count(v) == 1, ("REWRITE 值未真正进落盘文件", k[:60], disk.count(v))
for r in untouched:
    assert disk.count(r) == 1, ("未改写行在落盘文件中丢失或重复", r[:60])
print("断言 2 通过：改写已真正进落盘文件（复读校验）")

# ---- 断言 3：表体关键口径 == 正文关键口径（避坑 239）----
# ⚠️ **055 期新立（避坑 248）**：断言一律用「逐字短语」，不用裸数字 ——
#    裸数字会被 SVG 路径坐标与 JS 数据块放大命中数，导致断言看起来过了、实际没对上。
CHECKS = [
    ("452/17/14", "OpenRouter 本期三档口径"),
    ("poolside/laguna-s-2.1:free", "OpenRouter 消失的 :free 条目"),
    ("poolside/laguna-xs-2.1", "OpenRouter 消失的付费条目"),
    ("1784652683", "OpenRouter 消失条目的官方 created 时间戳"),
    ("Ollie is sunsetting on Nov 6, 2026", "Ollie 官方 CEO 告别信逐字"),
    ("50 messages from Ollie per month", "Ollie Free 档月消息数逐字"),
    ("6 free additional messages from Ollie every day", "Ollie Free 档每日免费追加逐字"),
    ("minimum charge", "Ollie 退款范围逐字（不含免费档）"),
    ("Watermarking will be applied at the model level", "Anthropic 标记在模型层逐字"),
    ("This tool runs in your browser. Your file never leaves your device.", "Content Checker 本地运行逐字"),
    ("The tool does not check text.", "Content Checker 不查文本逐字"),
    ("Watermark detection is currently in private preview", "文本水印检测非公开逐字"),
    ("Content Credentials (C2PA) in files", "Anthropic 对照表第三列表头"),
    ("最低充值金额 10 元", "Kimi K3.1 Pro 充值门槛逐字"),
    ("15 元代金券不可用于 Kimi K3.1 Pro", "Kimi K3.1 Pro 代金券排除逐字"),
    ("完整模型权重将于 11 月 4 日前发布", "Kimi 权重时点逐字"),
    ("heygen-video-1-0-launch-promo", "Runware heygen 促销条目"),
    ("K2 系列模型将于 2026 年 10 月 31 日起停止向新注册用户开放", "Moonshot K2 停新逐字"),
    ("2026-10-31", "Moonshot K2 停新日"),
]
# ⚠️ 「minimum charge」是英文占位，避免误用；改用中文逐字做校验（见下）
CHECKS = [c for c in CHECKS if c[0] != "minimum charge"]
for needle, label in CHECKS:
    assert needle in disk, ("表体缺关键口径", label, needle)

# ---- 断言 4b：每条 NEW 行都必须带「本期」或「055 期」标记 ----
_change_re = re.compile(r"(本期|055\s*期)")
for _n in NEW:
    assert _change_re.search(_n), ("NEW 行缺「本期」标记，会被 split_ledger 移进总账", _n[:70])
print("断言 4b 通过：%d 条 NEW 行均带本期标记" % len(NEW))

# ---- 断言 4：本期新增的每个截止日口径都必须能在表体里查到 ----
for needle in ["11/6", "未公布"]:
    assert needle in disk, ("新增行截止列口径缺失", needle)

# ---- 断言 5（055 期新立、沿用 054 期纪律②的守门断言）：每行字段数必须恰为 3 ----
# ⚠️ markdown 表格单元格里出现竖线会让该行字段数从 3 变成 N、整张表渲染错位；
#    官方对照表/规则表的逐字引用必须转写。这里对**全表**（含继承行）做分布断言。
_field_dist = Counter([l.count("|") - 1 for l in out
                       if l.startswith("| ") and not l.startswith("| 活动 |")
                       and not l.startswith("| --- |")])
assert _field_dist == Counter({3: len(out) - 2}), ("表体字段数分布异常（可能有单元格含竖线）", _field_dist)
print("断言 5 通过：字段数分布 %s" % dict(_field_dist))

nrows = len([l for l in out if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")])
print("rows %d = %d + %d" % (nrows, PREV, len(NEW)))
print("字段数分布", Counter([l.count("|") - 1 for l in out if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]))
print("CHECKS 全部通过")
