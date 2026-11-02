# -*- coding: utf-8 -*-
"""056 期：从 055 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-11-02（隔日出刊）
-> 行级改写 -> 追加本期新行。输出 .workbuddy/tmp_table056.md（纯表格块）。

⚠️ 055 期及此前各期的纪律，本期全部沿用并加严：
   ① 输入直接取 **055 期 md 的现行文本**（不是取上一期的 tmp_table）。
   ② 写出循环必须是「用键在行里找」，不能写成 `if k in REWRITE`。
   ③ 断言：键唯一命中 / 值在输出恰好出现一次 / 未改写行数守恒 / **落盘文件复读校验**。
   ④ **避坑 239**：断言全过≠事实全对 -> 新增「表体关键口径 == 正文关键口径」断言。
   ⑤ **避坑 248**：断言一律用「逐字短语」，不用「裸数字」。
   ⑥ **避坑 249（056 期新立）**：**「流通量」类字段必须先确认官方口径再记账**。
      本期查明 `HF` 的 `downloads` 是**近 `30` 天滚动窗口**、另有独立字段 `downloadsAllTime`
      —— **往期多期写的「单期涨 `X`」全部作废**（详见正文第五章纠错第 1 条）。
   ⑦ **避坑 250（056 期新立）**：**「上期给的结论」必须与「上期自己的归档文件」对账**。
      055 期第五章纠错第 4 条写「`heygen` 促销 `endsAt` 回到 `2026-10-31`」，
      **但 055 期自己归档的 `tmp_055/runware_pricing6.html` 里写的就是 `2026-11-30`**。
   ⑧ **056 期新立的一条工程纪律**：`recalc_days` 只重算**状态列**的「距今 N 天」；
      **截止列里的「距结束 N 天」与状态列里的「已过 N 天」从来没人重算过** ——
      本期实跑发现这些数字**从 049 期起就冻结着**（`距结束 11 天` / `距结束 5 天` / `距结束 8 天`），
      **而基准日一直在推进**。本期把这三处逐条改写成 11/2 的真值（新立避坑 252）。

本期性质：**隔日出刊**（055 期是 11/1 第一轮，窗口 10/31 19:00 -> 11/1 13:30，约 18.5 小时；
  本期窗口 11/1 13:30 -> 11/2 16:00，约 26.5 小时，**完全落在美西 11/1 与 11/2 两个日历日内**）。
  1) **基准日推进到 2026-11-02**（055 期基准日是 11/1）。
  2) 输入结构：上期 4.1 表体（57 行）+ 总账全量表体（151 行）= 208 行。
  3) 本期改写 22 行（见下）。
  4) 本期新增 6 行：OpenAI 额度合池文档、OpenAI 设备/支付卡上限文档、
     小米 HachimoDock 开源硬件、HF downloads 口径说明、
     Anthropic Claude Code 游戏复刻禁令、OpenRouter 目录同值记账。
"""
import io
import re
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第055期-2026-11-01.md"
SRC_LED = WS + ".workbuddy/tmp_056_led055.md"
OUT = WS + ".workbuddy/tmp_table056.md"
BASE = date(2026, 11, 2)
PREV = 208


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
assert len(rows_41) == 57, ("055 期 4.1 表体行数", len(rows_41))
assert len(rows_led) == 151, ("总账全量行数", len(rows_led))
body = rows_41 + rows_led
assert len(body) == PREV, (len(body), PREV)

header = "| 活动 | 截止 | 状态 |"
sep = "| --- | --- | --- |"

REWRITE = {}


def build(key, subs, tail=None):
    """行级改写。**幂等**：若该行已含本期标记（`（056 期）`），说明上一轮已改写过，
    则直接原样返回、不再重复替换。
    """
    hits = [l for l in body if key in l]
    assert len(hits) == 1, ("键未唯一命中", key, len(hits))
    out = hits[0]
    if "（056 期）" in out and all(a not in out for a, b in subs):
        return out
    for a, b in subs:
        assert a in out, ("片段未命中", key, a[:70])
        out = out.replace(a, b)
    if tail:
        assert out.rstrip().endswith("|")
        out = out.rstrip()[:-1].rstrip() + " " + tail + " |"
    return out


# ============ 一、OpenRouter 目录：452/17/14 连续第二期逐条零变化 ============
# ⚠️ **055 期立的避坑 247 说过「同一家厂商整批撤下」这一形态** —— 本期实测：
#    消失的 4 条没有继续扩大（新增 0 / 消失 0），即「整批撤下」是一次性事件，
#    **不是持续衰减**。本期把这写进表体尾部。
REWRITE["🟢 **OpenRouter 免费档（**官方 API 目录口径"] = build(
    "🟢 **OpenRouter 免费档（**官方 API 目录口径",
    [],
    tail="**⚠️ （056 期）本期逐条 diff：全量 `452` → `452`、零价 `17` → `17`、`:free` `14` → `14` "
         "—— **新增 `0` 条、消失 `0` 条，三档全部逐条同值（连续第二期「逐条零变化」）**。"
         "**⚠️ 即 055 期记的「`Poolside` 的 `Laguna` 系列 `4` 条整批撤下」是**一次性事件**、"
         "**不是持续衰减** —— 本期实测那 `4` 条没有继续扩大（避坑 247 的补充形态："
         "**整批撤下与持续衰减要分开判断，连续两期同值才算前者**）。"
         "**⚠️ 第三方口径本期仍未跟上**：`freellm.net/providers/openrouter` 专页仍逐字写 "
         "`19 free models online`，而官方零价档是 `17` —— **两个数都带来源、不折算**（避坑 161）。"
         "**⚠️ 「零价 `17`」与「`:free` `14`」仍差 `3` 个** —— `google/lyria-3-pro-preview`、"
         "`google/lyria-3-clip-preview`、`openrouter/free`（路由器）—— 零价但不带 `:free` 后缀**"
         "（避坑 161：**两套口径不可互相代替**）。"
         "**⚠️ （056 期）**一手 `openrouter.ai/api/v1/models`（`200` / `804,780` 字节）。"
)

# ============ 二、Runware heygen 促销：055 期的结论被 055 期自己的归档文件推翻 ============
# ⚠️ **056 期新立避坑 250 的来源**。055 期写「`endsAt` 回到 `2026-10-31`」，
#    但 055 期自己归档的那份文件里逐字写的就是 `2026-11-30`。
#    本期把 050–056 七期的归档逐期列出，并**把 055 期那行尾注的结论改写掉**。
REWRITE["🟢 **快手可灵 Kling 4.0（**`fal` 四端点"] = build(
    "🟢 **快手可灵 Kling 4.0（**`fal` 四端点",
    [
        # ⚠️ **055 期那整段尾注必须被替换掉、不能只在后面追加** ——
        #    055 期的尾注里写着「`endsAt` 在本期回到 `2026-10-31`」，
        #    **那与 055 期自己的归档文件矛盾**（见下面 056 期尾注）。
        ("**⚠️ （055 期）本期推翻 054 期的「`heygen` 促销延长 `30` 天」**："
         "**本期实读 `runware.ai/pricing`（`200` / `745,859` 字节，054 期同源文件 `747,303` 字节）"
         "逐条 diff：`14` 条全部同值、`0` 条新增、`0` 条消失、`0` 条 `endsAt` 改动** —— "
         "**即那条 `heygen-video-1-0-launch-promo` 的 `endsAt` 在本期回到 `2026-10-31`**"
         "（⚠️ 054 期记的是 `2026-11-30`）。**⚠️ 两种解释本报告都不替官方选边**："
         "**① 054 期读到的是一个短暂的中间状态；② 官方随后把促销改回原值 —— "
         "本报告只记「本期实读的逐条结果」**（避坑 243 的同族：**单期一次 diff 结果不足以断言趋势，"
         "至少要连续两期**）。**⚠️ 官方数组里那 `9` 条已过期条目本期仍一条未清**。",
         "**⚠️ （056 期）本期更正 055 期那段尾注 —— 055 期的结论与 055 期自己的归档文件不一致**："
         "055 期写「`endsAt` 在本期回到 `2026-10-31`」，理由是「逐条 diff `0` 条 `endsAt` 改动」—— "
         "**这两句话自相矛盾**（若 `0` 条改动，054 期的 `11/30` 就原样延续）。"
         "**⚠️ 本期实读 055 期自己归档的 `tmp_055/runware_pricing6.html`（`745,859` 字节）**："
         "逐字就是 `until November 30, 2026` 与 `endsAt: \"2026-11-30\"` —— "
         "**即 055 期读到的值与它写出的结论相反**。"
         "**⚠️ 本期把 050–056 七期归档逐期列出**：`050`–`053` 四期全是 `2026-10-31`、"
         "**`054` 起变成 `2026-11-30`、`055` 与 `056` 都是 `2026-11-30`** —— "
         "**即 054 期记的「官方延长了 `30` 天」是对的，055 期「推翻」它才是错的**"
         "（新立避坑 250：**「上期给的结论」必须与「上期自己的归档文件」对账，不能直接继承**）。"
         "**⚠️ 官方数组里那 `9` 条已过期条目本期仍一条未清（连续第三期）。**"),
    ],
)

# ============ 三、Ollie 关停：本期复核同值 + 首页无信息 ============
REWRITE["⚠️ **`Ollie`（隐私向 AI 助手）宣布关停"] = build(
    "⚠️ **`Ollie`（隐私向 AI 助手）宣布关停",
    [],
    tail="**⚠️ （056 期）本期复核同值**：一手 `ollie.ai/farewell`（`200` / `39,733` 字节）"
         "逐字 `Ollie is sunsetting on Nov 6, 2026`（命中 `8` 次）、"
         "`effective Nov 6, 2026.`（命中 `2` 次）。"
         "**⚠️ 一条新的实测记录**：一手 `ollie.ai/` 首页（`200` / `107,008` 字节）实读 "
         "`sunsetting on Nov 6, 2026` 命中 **`0` 次** —— "
         "**即关停公告只在 `/farewell` 子页上、首页没有**"
         "（避坑 230 的同族：**信息分散在子页，首页不代表全站**）。"
)

# ============ 四、Ollie Free 档：本期复核同值 ============
REWRITE["⚠️ **`Ollie` 的 `Free` 档（**官方逐字 `50 messages"] = build(
    "⚠️ **`Ollie` 的 `Free` 档（**官方逐字 `50 messages",
    [],
    tail="**⚠️ （056 期）本期复核同值**：一手 `ollie.ai/pricing`（`200` / `41,749` 字节）"
         "逐字 `50 messages from Ollie per month`（命中 `6` 次）、"
         "`6 free additional messages from Ollie every day`（命中 `3` 次）—— "
         "**与 055 期逐字相同**。**⚠️ 距 `11/6` 关停只剩 `4` 天** —— "
         "**只用 `Free` 档的用户，这个免费档在 `11/6` 一并消失**（避坑 246 的读者视角）。"
)

# ============ 五、百度 Unlimited OCR 2：downloads 口径纠错（避坑 249）============
REWRITE["🟢 **`百度` 开源 `文心 Unlimited OCR 2"] = build(
    "🟢 **`百度` 开源 `文心 Unlimited OCR 2",
    [],
    tail="**⚠️ （056 期）流通量记账 —— 本期把口径改正了（避坑 249）**：一手 "
         "`hf-mirror.com/baidu/Unlimited-OCR-2` 模型页（`200` / `573,278` 字节量级）实读："
         "**`downloads`（官方标签逐字 `Downloads last month`）= `109,519`**、"
         "**`downloadsAllTime`（累计值）= `109,519`**、"
         "`likes` = `520`（055 期 `480`，涨 `40`）。"
         "**⚠️ 关键：官方把这一栏的标签逐字写成 `Downloads last month` —— "
         "它是「近 `30` 天滚动窗口值」，不是累计量**；**同一个页面的数据块里另有独立字段 "
         "`downloadsAllTime`**。**⚠️ 因此 055 期及更早各期写的「`downloads` 单期涨 `9,784` / "
         "涨 `51,090` / 涨 `281%`」全部作废** —— **那是滚动窗口的差值，不是累计增长**"
         "（**本期新立避坑 249**，详见正文第五章纠错第 1 条）。"
         "**⚠️ 本期实读的第二个证据**：把 055 期与本期两期归档的 `HF` 模型列表逐条 diff，"
         "**可比模型 `347` 个 —— 上升 `136` 个、下降 `169` 个、同值 `42` 个** —— "
         "**一个累计计数器不可能下降**。"
         "**⚠️ `likes` 与 `downloads` 是两个独立字段、本报告不合并计算**（避坑 054 同源：口径不同不可相减）。"
)

# ============ 六、Moonshot K3.1 Pro：权重仍未放出（离 11/4 只剩 2 天）============
REWRITE["🟢 **`Moonshot` `Kimi K3.1 Pro` 发布（10/23 晚–10/24"] = build(
    "🟢 **`Moonshot` `Kimi K3.1 Pro` 发布（10/23 晚–10/24",
    [],
    tail="**⚠️ （056 期）权重仍未放出 —— 而官方承诺的时点只剩 `2` 天**：一手 "
         "`hf-mirror.com/api/models?author=moonshotai&limit=100&sort=createdAt&direction=-1`"
         "（`200` / `8,969` 字节）实读 —— 官方 `moonshotai` 名下 **`19` 个模型**、"
         "最新仍是 `moonshotai/Kimi-K3`（`createdAt 2026-06-13T06:42:57.000Z`）、"
         "**含 `K3.1` 字样的官方条目 `0` 条**。"
         "**⚠️ 官方逐字是「`11 月 4 日前`」（是「前」不是「当天」）—— 本期实访仍在窗口内、"
         "尚未到时点，本期不销项**（**离时点只剩 `2` 天，是下期最紧的一条**）。"
         "**⚠️ 官方访问条件逐字本期未复核**（`kimi-k3-1-pro-quickstart` 页本期未单独重取，"
         "沿用 055 期实读的 `最低充值金额 10 元` ＋ `15 元代金券不可用于 Kimi K3.1 Pro`）—— "
         "**这是「沿用」不是「本期复核」，本报告如实标注**。"
)

# ============ 七、K2 系列停新：截止日跨过基准日（10/31 -> 11/2 = 已过 2 天）============
REWRITE["🔴 **`Moonshot` `K2` 系列模型停新注册与计划下线"] = build(
    "🔴 **`Moonshot` `K2` 系列模型停新注册与计划下线",
    [
        ("**10/31（停止向新注册用户开放）；12 月底（计划下线，官方未给确切日）**",
         "**10/31（停止向新注册用户开放）；12 月底（计划下线，官方未给确切日）—— "
         "**已过本期基准日 `2` 天**）**"),
    ],
    tail="**⚠️ （056 期）这条的截止日已跨过基准日 `2` 天**："
         "**053 期（基准日 `10/30`）它是「截止日当天」（避坑 223）、"
         "054 期是「已过 `1` 天」、055 期是「已过 `1` 天」、"
         "本期（基准日 `11/2`）是「已过 `2` 天」**。"
         "**⚠️ 本报告只写「截止日已过」，不写收口字样**（避坑 239）。"
         "**⚠️ 「停新当日新用户能否注册」仍需登录态实测，本报告本期不做、也不合并。**"
)

# ============ 八、国家超算互联网：10/30 -> 已过 3 天 ============
REWRITE["🟠 **`国家超算互联网` 夜间限时免费调用 `Auto` 模型"] = build(
    "🟠 **`国家超算互联网` 夜间限时免费调用 `Auto` 模型",
    [
        ("**截止日已早于本期基准日 `2` 天**", "**截止日已早于本期基准日 `3` 天**"),
    ],
    tail="**⚠️ （056 期）这条的截止日再跨过基准日一天 —— 三态仍要分开写**："
         "**053 期（基准日 `10/30`）它是「截止日当天」、054 期「已过 `1` 天」、"
         "055 期「已过 `2` 天」、本期（基准日 `11/2`）是「已过 `3` 天」**。"
         "**⚠️ 官方页仍连续第 `4` 期零命中**：本期实访 `www.scnet.cn`"
         "（`200` / `128,776` 字节，与 055 期字节数完全相同），"
         "`夜间` / `21:00` / `09:00` / `每晚` / `限时` **各命中 `0` 次** —— **本期不销项**。"
)

# ============ 九、Google Nano Banana 2：10/29 -> 已过 4 天 ============
REWRITE["🟢 **Google Nano Banana 2 停用（Gemini API）**"] = build(
    "🟢 **Google Nano Banana 2 停用（Gemini API）**",
    [
        ("本期基准日 11/1 已过 3 天", "本期基准日 11/2 已过 4 天"),
    ],
)

# ============ 十、Runware pruna upscale：截止列的「距结束 N 天」从 049 期起就冻结着 ============
# ⚠️ **056 期新立避坑 252 的来源**：`recalc_days` 只重算**状态列**的「距今 N 天」，
#    **截止列里的「距结束 N 天」从来没人重算过** —— 实测该值自 049 期写入后就没变过。
#    真值（11/8 − 11/2）= 6 天，而表体写的是 11 天。
REWRITE["🟢 **`Runware` 分发层 `pruna-p-video-upscale` 促销 `50% OFF`"] = build(
    "🟢 **`Runware` 分发层 `pruna-p-video-upscale` 促销 `50% OFF`",
    [
        ("**11/8（官方促销数组 `endsAt: \"2026-11-08\"` 逐字；描述逐字「until November 8, 2026」）**",
         "**11/8（官方促销数组 `endsAt: \"2026-11-08\"` 逐字；描述逐字「until November 8, 2026」）"
         "—— **距结束 6 天**）**"),
        ("生效中（本期新核到一手 · 距结束 11 天）", "生效中（本期新核到一手 · 距结束 6 天）"),
    ],
    tail="**⚠️ （056 期）本行的「距结束 N 天」此前是冻结值 —— 本期改成了真值**："
         "**该值自 049 期写入后就没再变过（`050`–`055` 六期逐期实读都是 `11` 天），"
         "而基准日一直在推进** —— **真值（`11/8` − `11/2`）是 `6` 天**。"
         "**⚠️ 根因：`recalc_days` 只重算**状态列**的「距今 N 天」，"
         "**截止列里的「距结束 N 天」与状态列里的「已过 N 天」从来没人重算过**"
         "（**本期新立避坑 252**）。**⚠️ 本期该促销数组逐条 diff 与 055 期全部同值**"
         "（`14` 条、`0` 新增、`0` 消失、`0` 条 `endsAt` 改动）。"
)

# ============ 十一、Runware pruna edit：同上（11/3 − 11/2 = 1 天）============
REWRITE["🟢 **`Runware` 分发层 `pruna-p-video-edit` 促销 `25% OFF`"] = build(
    "🟢 **`Runware` 分发层 `pruna-p-video-edit` 促销 `25% OFF`",
    [
        ("**11/3（官方促销数组 `endsAt: \"2026-11-03\"` 逐字）**",
         "**11/3（官方促销数组 `endsAt: \"2026-11-03\"` 逐字）—— **距结束 1 天**）**"),
        ("生效中（本期新核到一手 · 距结束 5 天）", "生效中（本期新核到一手 · 距结束 1 天）"),
    ],
    tail="**⚠️ （056 期）本行的「距结束 N 天」此前同样是冻结值 —— 本期改成真值 `1` 天**"
         "（`11/3` − `11/2`；055 期及此前写的是 `5` 天，**自 051 期写入后没变过**）。"
         "**⚠️ 这是本报告至今离截止日最近的 `Runware` 促销 —— 下期基准日推进一天就是「已过期」**。"
)

# ============ 十二、AutoClaw 国内站 M10W4：距结束 5 天（冻结值）-> 真值 ============
# 真值：活动期 10/26 00:00 — 11/1 23:59（北京时间）。基准日 11/2 -> **已过期 1 天**。
REWRITE["🟢 **智谱 `AutoClaw` 国内站 `M10W4` 一周福利：登录领 **1 亿** Tokens"] = build(
    "🟢 **智谱 `AutoClaw` 国内站 `M10W4` 一周福利：登录领 **1 亿** Tokens",
    [
        ("**10/26（周一）00:00 — 11/1（周日）23:59（北京时间）；奖励 11/1 23:59 失效（距结束 5 天）**",
         "**10/26（周一）00:00 — 11/1（周日）23:59（北京时间）；奖励 11/1 23:59 失效"
         "（**已过本期基准日 `1` 天**）**"),
        ("🟢 **已开启（活动第 2 天）。", "🟢 **截止日已过（活动期 10/26–11/1 已走完，"),
    ],
    tail="**⚠️ （056 期）这个「距结束 5 天」是自 049 期写入后就没再变过的冻结值**："
         "**真值是「活动期已于 `11/1 23:59` 走完、本期基准日 `11/2` 已过 `1` 天」**。"
         "**⚠️ 同样地，「活动第 2 天」也是冻结值**（该活动 `10/26` 开场、"
         "`11/1` 收官，共 `7` 天；055 期写「活动第 2 天」是 049 期的值）—— "
         "**本期一并改正**（避坑 252）。"
         "**⚠️ 官方页仍保留该活动（页面不回收历史活动页）—— 「数组/页面里还在」不等于「活动还在售」**"
         "（避坑 230 的同族）。"
)

# ============ 十三、AutoClaw 国际站 M10W4：同上 ============
REWRITE["🟢 **智谱 `AutoClaw` 国际站 `M10W4` `Weekly Perk`：登录领 **"] = build(
    "🟢 **智谱 `AutoClaw` 国际站 `M10W4` `Weekly Perk`：登录领 **",
    [
        ("**10/26（周一）00:00 — 11/1（周日）23:59（UTC+8）；奖励 11/1 23:59 失效（距结束 5 天）**",
         "**10/26（周一）00:00 — 11/1（周日）23:59（UTC+8）；奖励 11/1 23:59 失效"
         "（**已过本期基准日 `1` 天**）**"),
        ("生效中（活动第 4 天 ·", "截止日已过（活动期 10/26–11/1 已走完 ·"),
    ],
    tail="**⚠️ （056 期）本行的「距结束 5 天」与「活动第 4 天」都是自 049–051 期写入后就没再变过的冻结值**："
         "**真值是「活动期已于 `11/1 23:59` 走完、本期基准日 `11/2` 已过 `1` 天」**（避坑 252）。"
         "**⚠️ 本期实访官方页确认活动期逐字未变**（`Event period: October 31, 00:00 – November 8, 23:59 (UTC+8)` "
         "是 `M11W1` 那一档、不是本行）。"
)

# ============ 十四、AutoClaw M11W1 国际站：距结束 8 天（冻结值）-> 真值 6 天 ============
REWRITE["🟢 **智谱 `AutoClaw` 国际站 `M11W1` 万圣节档：登录领 **40M** Tokens"] = build(
    "🟢 **智谱 `AutoClaw` 国际站 `M11W1` 万圣节档：登录领 **40M** Tokens",
    [
        ("· **距结束 8 天**）**", "· **距结束 6 天**）**"),
    ],
    tail="**⚠️ （056 期）本行的「距结束 8 天」是 054 期写入的冻结值 —— 真值（`11/8` − `11/2`）是 `6` 天**"
         "（避坑 252）。**⚠️ 官方活动期逐字本期复核同值**：一手 `autoclaw.z.ai/blog/news/M11W1/`"
         "（`200` / `42,427` 字节）逐字 `Event period: October 31, 00:00 – November 8, 23:59 (UTC+8)`。"
         "**⚠️ 与国内站仍是两个不同的活动、两个数**（国际站 `40M` ／ 国内站 `50M`，避坑 240）。"
)

# ============ 十五、AutoClaw M11W1 国内站：同上 ============
REWRITE["🟢 **智谱 `AutoClaw` 国内站 `M11W1` 万圣节档：登录领 **50M** Tokens"] = build(
    "🟢 **智谱 `AutoClaw` 国内站 `M11W1` 万圣节档：登录领 **50M** Tokens",
    [
        ("· **距结束 8 天**）**", "· **距结束 6 天**）**"),
    ],
    tail="**⚠️ （056 期）本行的「距结束 8 天」是 054 期写入的冻结值 —— 真值（`11/8` − `11/2`）是 `6` 天**"
         "（避坑 252）。**⚠️ 官方活动期逐字本期复核同值**：一手 "
         "`autoclaw.zhipuai.cn/blog/news/M11W1/`（`200` / `43,495` 字节）逐字 "
         "`活动时间 11 月 2 日（周一）00:00—11 月 8 日（周日）23:59（北京时间）`。"
         "**⚠️ 与国际站的起始日仍不对齐**（国际站 `10/31` 起、国内站 `11/2` 起 —— "
         "**官方自己仍不对齐，本报告不替官方对齐**，避坑 240）。"
)

# ============ 十六、Runware Kling 4.0：截止列里的「已早于本期基准日 2 天」是错的 ============
# 真值：10/29 − 11/2 = 已过 4 天。055 期写的「2 天」在 055 期就算错（10/29 − 11/1 = 3 天）。
REWRITE["🟢 **`Runware` 分发层 `Kling 4.0` 促销 `15% OFF`"] = build(
    "🟢 **`Runware` 分发层 `Kling 4.0` 促销 `15% OFF`",
    [
        ("`endsAt` 已早于本期基准日 `2` 天", "`endsAt` 已早于本期基准日 `4` 天"),
    ],
    tail="**⚠️ （056 期）本行的「已早于本期基准日 N 天」此前也是冻结值、且 055 期就算错**："
         "**真值（`10/29` − `11/2`）是已过 `4` 天** —— "
         "**055 期写的 `2` 天在 055 期的基准日（`11/1`）上就已经错了（真值是 `3` 天）**，"
         "**根因与「距结束 N 天」同族：状态列里的「已过 N 天」从来没人重算过**（避坑 252）。"
         "**⚠️ 官方促销数组本期逐条 diff 与 055 期全部同值**（`14` 条、`0` 新增、`0` 消失、"
         "`0` 条 `endsAt` 改动）。"
)

# ============ 十七、腾讯老混元 Q04：连续第 44 期未决 ============
REWRITE["🔴 **腾讯老混元大模型平台停服"] = build(
    "🔴 **腾讯老混元大模型平台停服",
    [],
    tail="**⚠️ （056 期）这条的截止日是「`2026 年 9 月底`」—— 距本期基准日已过 `64` 天，"
         "**是本报告至今仍未收口、且逾期最久的一条**（连续第 `44` 期未决）。"
         "**⚠️ 本期实访 `hunyuan.tencent.com`（`200` / 页面可达）仍未见官方停服公告的到期收口说明** —— "
         "**逾期不等于收口，故本行继续留在表体**（避坑 230 的同族：**「已过期」与「已收口」是两件事**）。"
)

# ============ 十八、天猫 AI 空间站：距开卖 0 天是 043 期写入的冻结值 ============
# 真值：11/28 − 11/2 = 26 天。表体写「距开卖 0 天」是 043 期（10/20 开卖当天）的值。
REWRITE["🟡 **天猫「AI 空间站」Token 充值中心双 11 开卖"] = build(
    "🟡 **天猫「AI 空间站」Token 充值中心双 11 开卖",
    [
        ("**11/28 23:59（价保截止）**", "**11/28 23:59（价保截止 · **距开卖 26 天**）**"),
        # ⚠️ 状态列里那个「距开卖 0 天」同样是 043 期（10/20 开卖当天）写入的冻结值。
        ("🟡 **生效中（距开卖 0 天 · 本轮出刊时点 10/20 午间，尚未开卖）。",
         "🟡 **生效中（**已开卖** · 官方逐字 `10 月 20 日 20:00` 正式开卖、"
         "价保至 `11/28 23:59`；本期基准日 `11/2`，距价保截止还有 `26` 天**）。"),
    ],
    tail="**⚠️ （056 期）本行的「距开卖 0 天」是 043 期（`10/20` 开卖当天）写入的冻结值 —— "
         "**真值（`11/28` − `11/2`）是 `26` 天**（避坑 252）。"
         "**⚠️ 原状态列那句「本轮出刊时点 10/20 午间，尚未开卖」也是 043 期的原文 —— "
         "本期一并改写成「已开卖」**（**活动已于 `10/20 20:00` 开始，本期再写「尚未开卖」是错的**）。"
)

# ============ 十九点五、Ollie 之后的空行占位（保持编号连续）============

# ============ 十九、OpenRouter 官方公告 CSAM：在途筛查 ============
REWRITE["🟡 **`OpenRouter` 的 `CSAM` 在途筛查与 `ZDR` 例外"] = build(
    "🟡 **`OpenRouter` 的 `CSAM` 在途筛查与 `ZDR` 例外",
    [],
    tail="**⚠️ （056 期）本期复核：官方公告页仍取不到正文** —— 一手 "
         "`openrouter.ai/announcements/csam-screening` 与 `/blog/csam-screening` 本期均为 "
         "`404` / 重定向壳，**官方对具体模型的适用差异仍未核到**（挂账项⑭ 不销项）。"
)

# ============ 二十、Mistral Large 4 Le Chonk demo 免费预算：mistral.ai 连续第 16 次不可达 ============
REWRITE["🟡 **`Mistral Large 4`（`Le Chonk`）官方 demo 首周共享免费预算"] = build(
    "🟡 **`Mistral Large 4`（`Le Chonk`）官方 demo 首周共享免费预算",
    [],
    tail="**⚠️ （056 期）本期复核：该官方逐字口径本期未复核 —— `mistral.ai/news/` 连续第 `16` 次 `000`"
         "（**含 `/news/mistral-large-4-oss/`、`console.mistral.ai`、`docs.mistral.ai`**）。"
         "**⚠️ 055 期记的官方逐字（`a small shared free budget per visitor for the first week of the "
         "release`）在本期未获复核** —— **本报告如实标注「本期未复核」，不把它当作本期确认的事实**。"
         "**⚠️ 「发布后第一周」这个相对期限仍没有日历日**（本报告不替它推算）。"
)

# ============ 二十一、Anthropic 订阅档改版 Ultra：本期补记 Codex 覆盖 Free 档的官方逐字 ============
REWRITE["🟡 **`Anthropic` 订阅档改版：`Max 5x`→`Max`、`Max 20x`→**"] = build(
    "🟡 **`Anthropic` 订阅档改版：`Max 5x`→`Max`、`Max 20x`→**",
    [],
    tail="**⚠️ （056 期）本期把「`Free` 档能用什么」这一层单独补记**（避坑 251）：一手 "
         "`help.openai.com/en/articles/11369540-codex-in-chatgpt`（`200` / `128,587` 字节，"
         "官方 `Updated: 8 days ago`）逐字 `Codex is included across ChatGPT plans, including Free and Go.` "
         "与 `Codex Cloud is available to eligible Plus, all Pro tiers, Business, Enterprise, "
         "Health, and Education accounts… It is not included with Free or Go.` —— "
         "**即 `Free` 档能用 `Codex`（本地 `CLI` / `IDE` / `web`）、但不能用 `Codex Cloud`**。"
         "**⚠️ 这与「`Free` 档不受 12 月额度合池影响」是两件事**（另一份官方文档 "
         "`20001625` 只覆盖 `Plus/Pro/Business`）—— **本报告把这两句分开写、不合并**（避坑 251）。"
)

# ============ 二十二、OXR 免费 API：规则页本期 404 ============
REWRITE["🟢 **`OXR` 官方「免费 API」"] = build(
    "🟢 **`OXR` 官方「免费 API」",
    [],
    tail="**⚠️ （056 期）本期官方规则页不可达 —— 该条的额度数字本期未复核**：一手 "
         "`docs.somark.ai/free-tier-rules.md` 本期 `404`（055 期为 `200` / `576` 字节）。"
         "**⚠️ 055 期记的官方逐字（`Up to 500 pages of free quota per day` ／ "
         "`Up to 2000 pages of free quota per month`）在本期未获复核** —— "
         "**本报告如实标注「本期未复核」**。"
         "**⚠️ 「超额怎么扣」仍需真调一次 API 才算实测**（挂账项㉗ 不销项）。"
)

# ============ 二十三、可灵「看见微光」：截止日 11/1 跨过基准日 -> 已过 1 天 ============
# ⚠️ **055 期立的工程纪律（本期沿用）**：`recalc_days056.py` 对「截止日已过、真值为负」的行
#    **报错退出（这是对的）** —— 负天数不该被写进表体。
#    **但这行确实需要留在表体里**（它是「刚过期、还没收口」的待办，`KEEP-3` 保留规则要求留），
#    **处置是「改写状态列、把「距今 0 天」换成「已过 1 天」这种不含判定词的表述，再由独立重算器复核」**。
REWRITE["🟢 **可灵「看见微光」AI 公益影像大赛作品征集**"] = build(
    "🟢 **可灵「看见微光」AI 公益影像大赛作品征集**",
    [
        ("**11/1**", "**11/1（**已过本期基准日 `1` 天**）**"),
        ("🟢 **生效中（距今 0 天），现在就能投稿**",
         "🟢 **截止日已过（官方征集期至 `11/1`，本期基准日 `11/2`，**已过 `1` 天**）**"),
    ],
    tail="**⚠️ （056 期）这条的截止日跨过了基准日**："
         "**055 期（基准日 `11/1`）它是「截止日当天」（避坑 223）、本期（基准日 `11/2`）"
         "变成「已过 `1` 天」**。**⚠️ 本报告只写「截止日已过」，不写收口字样**"
         "（**避坑 239：状态列里一旦出现判定词的字面文本，整行就会被 `classify()` 归进对应桶**）。"
         "**⚠️ 本期未核到官方是否延期或另开新期 —— 本行只是「截止日已过、尚未收口」**。"
)

# ============ 二十四、DeepSeek Search / Fetch：截止日 11/1 跨过基准日 -> 已过 1 天 ============
REWRITE["🟡 **`DeepSeek Search` / `Fetch` 两个 API 开放（10/17"] = build(
    "🟡 **`DeepSeek Search` / `Fetch` 两个 API 开放（10/17",
    [
        ("**11/1 00:00（北京）起按请求计费**",
         "**11/1 00:00（北京）起按请求计费（**已过本期基准日 `1` 天**）**"),
        ("🟡 **生效中（免费窗口内 · 距今 0 天）。",
         "🟡 **截止日已过（免费窗口至 `11/1 00:00`，本期基准日 `11/2`，**已过 `1` 天**）。"),
    ],
    tail="**⚠️ （056 期）这条的免费窗口跨过了基准日**："
         "**055 期（基准日 `11/1`）它是「免费窗口内」、本期（基准日 `11/2`）变成「已过 `1` 天」**。"
         "**⚠️ 本报告只写「截止日已过」，不写收口字样**（避坑 239）。"
         "**⚠️ 「开源框架不改变 API 价格」这条既有结论本期不变**："
         "10/20 开源的 `DeepInfer` 与官方 API 计费是两本账。"
)

# ============ 二十五、AutoClaw 2.2.0 升级礼：领取后 7 天内有效（相对日期，不改）============
# ⚠️ 相对期限没有日历日 -> 不该硬塞进 4.1 的「距今 N 天」体系（055 期立的纪律③）。

# ============ 二十六、HeyGen Voice：已过 1 天 -> 已过 2 天 ============
REWRITE["🟢 **HeyGen Voice（AA 语音合成榜首，促销五折）**"] = build(
    "🟢 **HeyGen Voice（AA 语音合成榜首，促销五折）**",
    [
        ("**10/31（**已过本期基准日 `1` 天**）**", "**10/31（**已过本期基准日 `2` 天**）**"),
        ("🟢 **截止日已过（官方促销期至 `10/31`，本期基准日 `11/1`，已过 `1` 天）。",
         "🟢 **截止日已过（官方促销期至 `10/31`，本期基准日 `11/2`，已过 `2` 天）。"),
    ],
)

# ============ 二十七、WorkBuddy Intl DeepSeek 限免：已过 1 天 -> 已过 2 天 ============
REWRITE["🟢 **`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免（10/31）**"] = build(
    "🟢 **`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免（10/31）**",
    [
        ("**10/31（**已过本期基准日 `1` 天**）**", "**10/31（**已过本期基准日 `2` 天**）**"),
        ("🟢 **截止日已过（官方限免期至 `10/31`，本期基准日 `11/1`，已过 `1` 天 · 工作区自有产品线）。",
         "🟢 **截止日已过（官方限免期至 `10/31`，本期基准日 `11/2`，已过 `2` 天 · 工作区自有产品线）。"),
    ],
)

# ============ 二十八、腾讯 Step 5 Preview（⚪ 已收口）：基准日写的是 10/27，已过 2 天 -> 8 天 ============
# ⚠️ **这条是「⚪ 已收口」的老行** —— 055 期抄的是 049 期（基准日 10/27）的表述。
#    真值（`10/25` − `11/2`）是已过 `8` 天。
REWRITE["⚪ **腾讯 `Step 5 Preview` × WorkBuddy 独家限免**"] = build(
    "⚪ **腾讯 `Step 5 Preview` × WorkBuddy 独家限免**",
    [
        ("⚪ **已结束（截止 10/25，本期基准日 10/27 已过 2 天）。",
         "⚪ **已结束（截止 10/25，本期基准日 11/2 已过 8 天）。"),
    ],
    tail="**⚠️ （056 期）本行的「本期基准日 `10/27` 已过 `2` 天」是 049 期抄下来的、此后一直没更新**："
         "**真值（`10/25` − `11/2`）是已过 `8` 天**（避坑 252）。"
         "**⚠️ 这条已过期超过 `7` 天宽限期、且状态已是「⚪ 已收口」—— "
         "本期由 `prune_table.py` 移出表体、原文逐行归档**（避坑 230）。"
)

# ============ 二十九、AutoClaw 国际站 M10W3（⚪ 已收口）：同族 ============
REWRITE["⚪ **智谱 `AutoClaw` 国际站 `M10W3` 每日登录送 Token（`z.ai` ·"] = build(
    "⚪ **智谱 `AutoClaw` 国际站 `M10W3` 每日登录送 Token（`z.ai` ·",
    [
        ("本期基准日 10/27 已过 2 天", "本期基准日 11/2 已过 8 天"),
    ],
    tail="**⚠️ （056 期）本行的「本期基准日 `10/27` 已过 `2` 天」同样是 049 期抄下来的冻结值**："
         "**真值（`10/25` − `11/2`）是已过 `8` 天**（避坑 252）。"
         "**⚠️ 这条已过期超过 `7` 天宽限期、且状态已是「⚪ 已收口」—— "
         "本期由 `prune_table.py` 移出表体、原文逐行归档**。"
)

# ============ 三十、湖北算力券：已过 1 天 -> 已过 2 天 ============
REWRITE["🟢 **湖北算力券年度申领**"] = build(
    "🟢 **湖北算力券年度申领**",
    [
        ("**10/31（**已过本期基准日 `1` 天**）**", "**10/31（**已过本期基准日 `2` 天**）**"),
        ("🟢 **截止日已过（官方活动期至 `10/31`，本期基准日 `11/1`，已过 `1` 天）。",
         "🟢 **截止日已过（官方活动期至 `10/31`，本期基准日 `11/2`，已过 `2` 天）。"),
    ],
)

# ============ 三十一、WorkBuddy 学生版：已过 1 天 -> 已过 2 天 ============
REWRITE["🟢 **WorkBuddy 学生版 1,000 积分 / ChatGPT 学生促销**"] = build(
    "🟢 **WorkBuddy 学生版 1,000 积分 / ChatGPT 学生促销**",
    [
        ("**10/31（**已过本期基准日 `1` 天**）**", "**10/31（**已过本期基准日 `2` 天**）**"),
        ("🟢 **截止日已过（官方活动期至 `10/31`，本期基准日 `11/1`，已过 `1` 天）",
         "🟢 **截止日已过（官方活动期至 `10/31`，本期基准日 `11/2`，已过 `2` 天）"),
        ("⚠️ 这条的截止日跨过了基准日：054 期它是「截止日当天」，本期是「已过 `1` 天」。",
         "⚠️ 这条的截止日跨过了基准日：054 期它是「截止日当天」、055 期是「已过 `1` 天」、"
         "本期是「已过 `2` 天」。"),
    ],
)

# ---- 本期新增 6 行 ----
NEW = []

# 新增 1：OpenAI 官方「ChatGPT 与 Codex 额度合池」文档
NEW.append(
    "| ⚠️ **`OpenAI` 官方「`ChatGPT` 与 `Codex` 额度从 12 月起合并成一个 `token` 池」"
    "（**官方帮助中心独立文档 · 本报告至今第一次拿到 `OpenAI` 官方就「合池」写成的明文** · "
    "**⚠️ 覆盖范围只有 `Plus` / `Pro` / `Business` 三档 —— `Free` 档不在其中**）** | "
    "**未公布（官方逐字 `Starting in December` —— **没有确切日历日、没有给任何一档的 `token` 配额数字**）** | "
    "⚠️ **生效中（**变更已公告、尚未生效**）。 ⚠️ 四条边界："
    "① 官方逐字 `Starting in December, Plus, Pro, and Business plans' usage allowance will be "
    "shared across ChatGPT and Codex as we bring the agentic capabilities of Work into the main "
    "ChatGPT experience.` —— **⚠️ 覆盖范围只有三档付费**；"
    "② 官方逐字 `Your usage for ChatGPT and Codex will be measured in tokens, the units of "
    "information a model processes and generates.` ＋ `Instant chat will not draw from your usage.` "
    "—— **计量单位从消息条数改成 `token`、但 `Instant` 聊天仍不扣额度**；"
    "③ 官方逐字 `If you reach your limit, you can wait for it to reset, upgrade your plan, or buy "
    "credits to continue using eligible features.` —— **耗尽后只有三条路**；"
    "④ **官方没有公布任何一档的 `token` 配额数字、也没给确切上线日** —— "
    "**本报告不替官方推算**。"
    "**⚠️ 与免费读者直接相关的那一句在另一份官方文档里**：一手 "
    "`help.openai.com/en/articles/11369540-codex-in-chatgpt` 逐字 "
    "`Codex is included across ChatGPT plans, including Free and Go.` —— "
    "**即「`Codex` 能用」覆盖 `Free`、「额度合池」不覆盖 `Free`，这是两件事**（新立避坑 251）。 "
    "**⚠️ （056 期）**一手 `help.openai.com/en/articles/20001625-understanding-chatgpt-and-codex-"
    "usage-limits`（`200` / `49,809` 字节，官方 `Updated: 11 hours ago`）"
    "（⚠️ 归期如实写：**官方只标 `Updated`、没标首次发布日**，本报告只写官方自己标的时点）。 |"
)

# 新增 2：OpenAI 官方「设备 / 支付卡上限」文档
NEW.append(
    "| ⚠️ **`OpenAI` 官方「付费账号的设备 / 支付卡上限」（**官方帮助中心独立文档 · "
    "**⚠️ `Free` 档与 `Business/Enterprise/Edu` 一并豁免 —— 官方逐字 `do not count toward the limit`**）** | "
    "**未公布（官方未给生效日、也未给任何数字阈值）** | "
    "⚠️ **生效中（**限制已上线**）。 ⚠️ 四条边界："
    "① 官方逐字 `Device limits apply to ChatGPT Go, ChatGPT Plus, ChatGPT Pro 100, ChatGPT Pro 200, "
    "and ChatGPT Pro 500 plans. ChatGPT Free and ChatGPT Business, Enterprise, and Edu workspace "
    "plans do not count toward the limit.` —— **⚠️ 免费读者完全不受这条限制**；"
    "② 官方逐字 `Device limits are separate from the number of accounts signed in at the same time - "
    "signing out of an account does not guarantee that another paid account becomes eligible.` —— "
    "**退出登录不释放名额**；"
    "③ 官方逐字 `Buying credits or resetting usage won't clear a card or device restriction.` —— "
    "**买 credits 或重置用量都不解除限制**；"
    "④ **官方没有公布具体数字阈值** —— 逐字只有 `Device limit reached` 与 "
    "`Too many subscriptions associated with this card or device. We can't complete this purchase,`，"
    "**本报告不替官方猜数字**。"
    "**⚠️ 官方把它定位为「隐私与安全保护」**（逐字 `as part of its privacy and security protections`）—— "
    "**本报告如实写官方定位、不替官方改成别的说法**。"
    "**⚠️ （056 期）**一手 `help.openai.com/en/articles/20001559-understanding-card-and-device-limits-"
    "in-chatgpt`（`200` / `71,201` 字节，官方 `Updated: 2 days ago`）。 |"
)

# 新增 3：小米 HachimoDock 开源硬件
NEW.append(
    "| 🟢 **小米孵化、已开源的 `HachimoDock`（哈基米机）· 桌面 Agent 状态宠物 + 开源硬件方案"
    "（**⚠️ 许可证是「非商业」自有许可 —— 能免费用、不能商用**）** | "
    "**无结束日（开源项目，无活动期；官方未给任何截止日）** | "
    "🟢 **已开放（**第 ④ 级已到 · **本期首次登记的往期事件**）。 ⚠️ 四层开放（避坑 41）："
    "① **能用** —— 官方 `README.md` 逐字 `把 ChatGPT（Codex）、Claude 等 Agent 的实时工作状态变成"
    "桌上宠物的表情、动作、Session 气泡和提醒`；"
    "② **能下载** —— 官方逐字 `你可以在这里下载 Windows/macOS 客户端和 ESP32-P4 完整烧录包，"
    "也可以获取源码自行构建。硬件资料与装配教程见 OSHWHub。`；"
    "③ **能跑** —— `GitHub Releases` 最新 `v0.1.168`（官方 `published_at 2026-10-29T12:41:26Z`）"
    "的 `13` 个资产含 `HachimiDock_0.1.168_macOS-arm64.dmg`（`128,398,705` 字节）、"
    "`HachimoDock_0.1.168_Windows-x64-setup.exe`（`113,759,140` 字节）、"
    "`HachimoDock-P4-v1_0.7.103-p4-r2_Factory-Flasher.zip`（`25,747,936` 字节）；"
    "④ **能商用** —— ⚠️ **不能**：官方 `LICENSE` 逐字 `有限、非排他、免费且不可转授权的许可，"
    "允许为非商业目的学习、运行、复制、修改和再分发授权作品`，而逐字禁止 "
    "`收费销售、出租、付费服务、商业产品集成、预装销售、委托生产销售`。"
    "**⚠️ 三条边界：① 家居控制那一块另用小米自己的 `Xiaomi Miloco License`**（官方逐字 "
    "`相关 MiLoCo 授权作品的版权归小米所有`）；**② 硬件侧走 `OSHWHub` 的「硬件复刻」路径**"
    "（官方逐字 `PCB、BOM、结构/装配和硬件复刻资料`）—— **不是电子物料清单直接开放下载**；"
    "**③ 媒体口径里的「硬件自制成本约 `150` 元」不是官方数字**（官方 `README.md` 与仓库元数据里都没有它）"
    "—— **本报告不把它写进表体**（避坑 154/161）。 "
    "**⚠️ （056 期）**一手 `api.github.com/repos/YizhengWw/HachimoDock`（`200` / `5,866` 字节）："
    "`stargazers_count 642` / `forks_count 60` / `open_issues_count 7` / "
    "`created_at 2026-06-10T10:30:51Z` / `pushed_at 2026-10-29T12:45:10Z`、"
    "许可 `spdx_id: NOASSERTION`（自有许可 `版本 1.0 — 2026-09-04`、"
    "`Copyright (C) 2026 Yizheng Wang`）。 |"
)

# 新增 4：HF downloads 口径（避坑 249 的表体落地）
NEW.append(
    "| ⚠️ **⚠️ 口径更正（避坑 249）：`Hugging Face` 的 `downloads` 字段是「近 `30` 天滚动窗口」，"
    "不是累计量 —— 官方模型页逐字 `Downloads last month`，另有独立字段 `downloadsAllTime`**"
    "（**这一条影响本报告全部 `HF` 流通量记账**）** | "
    "**未公布（口径说明，无活动期）** | "
    "⚠️ **生效中（**口径更正，本期起对全表 `HF` 流通量重新记账**）。 ⚠️ 四条边界："
    "① **官方页面把这一栏的标签逐字写成 `Downloads last month`** —— "
    "**同一个页面的数据块里另有独立字段 `downloadsAllTime`**（一手 `hf-mirror.com/moonshotai/Kimi-K3`："
    "`downloads 813134` ＋ `downloadsAllTime 5997142`）；"
    "② **本期实测的第二个证据**：把 055 期与本期两期归档的 `HF` 模型列表逐条 diff，"
    "**可比模型 `347` 个 —— 上升 `136` 个、下降 `169` 个、同值 `42` 个** —— "
    "**一个累计计数器不可能下降**；"
    "③ **往期多期写的「单期涨 `X`」「涨 `Y%`」全部作废** —— **那是滚动窗口的差值、不是累计增长**"
    "（053 期「涨 `9,784`」、054 期「涨 `51,090` / 涨 `281%`」、055 期「增量 `0`」）；"
    "④ **「`downloads` 下降」不等于「这个模型没人用了」** —— "
    "**它只说明「近 `30` 天的下载次数比上一个 `30` 天窗口少」** —— "
    "**本报告本期起不对 `downloads` 的升降写「热度上升 / 下降」这类结论**。"
    "**⚠️ （056 期）**一手 `hf-mirror.com/moonshotai/Kimi-K3`（`200` / `573,278` 字节）"
    "＋ `hf-mirror.com/baidu/Unlimited-OCR-2`（`200`）＋ `hf-mirror.com/docs/hub/models-download-stats`"
    "（`200` / `200,835` 字节，官方文档标题逐字 `Models Download Stats`）。 |"
)

# 新增 5：Anthropic Claude Code 游戏复刻禁令（工具能力边界，不进 4.1）
NEW.append(
    "| ⚠️ **`Anthropic` 在 `Opus 5.5` 的 `Claude Code` 提示词里加了两句话、禁止复刻已存在的游戏"
    "（**⚠️ 官方文档页读不到这两句、确认人是 `Anthropic` 技术员工在 `X` 上的回复** · "
    "**属「工具能力边界」，不是免费额度条目**）** | "
    "**未公布（无活动期；官方未给任何截止日或生效日）** | "
    "⚠️ **生效中（**服务端下发、用户侧无开关**）。 ⚠️ 四条边界："
    "① 官方页面读不到这两句 —— 一手 `anthropic.com/claude-code`（`200` / `1,199,755` 字节）实读 "
    "`recreate` / `original game` / `existing game` / `reverse engineer` / `game` **各命中 `0` 次**；"
    "② **官方确认人不是官方文档页，而是 `Anthropic` 技术员工 `Addy Osmani` 在 `X` 上的回复** —— "
    "多家媒体逐字引用同一句 `We added two sentences to Claude Code's prompt on Opus 5.5 to steer it "
    "away from recreating someone else's specific game because using Claude to infringe IP is against "
    "our usage policy` —— **本报告只采用这句逐字，不采用媒体的机制描述**（避坑 243）；"
    "③ **它约束的是「做什么内容」而不是「有多少额度」** —— 对本报告三条线属于「工具能力边界」；"
    "④ **但它对免费读者有实际影响** —— `Claude Code` 的免费使用方式会少一类场景"
    "（写原创游戏仍可，复刻某个具体游戏不行）。"
    "**⚠️ （056 期）**一手 `anthropic.com/legal/aup`（`200` / `992,178` 字节）实读 "
    "`intellectual property` 命中 `1` 次、`infring` 命中 `0` 次；"
    "媒体一手 `qbitai.com/2026/11/507038.html`（`200` / `61,514` 字节，"
    "窗口内 `pubDate` ＝ 北京 `11/1 21:09`）。 |"
)

# 新增 6：Ollie 首页无信息（一条「信息分散在子页」的实证）
NEW.append(
    "| ⚠️ **一条「信息分散在子页」的实证：`Ollie` 的关停公告与 `Free` 档信息**"
    "**都只在子页上、首页一个字都没有**（**读者只看首页会完全错过关停**）** | "
    "**未公布（口径记录，无活动期）** | "
    "⚠️ **生效中（**关停倒计时**）。 ⚠️ 三条边界："
    "① 一手 `ollie.ai/` 首页（`200` / `107,008` 字节）实读 `sunsetting on Nov 6, 2026` 命中 **`0` 次**、"
    "`50 messages from Ollie per month` 命中 **`0` 次**；"
    "② **而同样两个逐字在 `ollie.ai/farewell`（`200` / `39,733` 字节，命中 `8` 次）与 "
    "`ollie.ai/pricing`（`200` / `41,749` 字节，命中 `6` 次）上都能读到** —— "
    "**即「官网首页可达」不等于「官网首页有该信息」**（避坑 230 的同族）；"
    "③ **本报告记一条是因为它对读者有实际后果** —— 官方关停在 `11/6`（距本期基准日 `4` 天），"
    "**只用 `Free` 档的用户，这个免费档会一并消失**。"
    "**⚠️ （056 期）**一手 `ollie.ai/` ＋ `ollie.ai/farewell` ＋ `ollie.ai/pricing` 三页实读。 |"
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
# ⚠️ **056 期沿用避坑 248**：断言一律用「逐字短语」，不用裸数字。
CHECKS = [
    ("Starting in December, Plus, Pro, and Business plans' usage allowance will be shared",
     "OpenAI 合池文档的覆盖范围逐字"),
    ("Instant chat will not draw from your usage.", "OpenAI 合池文档的 Instant 例外逐字"),
    ("Your usage for ChatGPT and Codex will be measured in tokens",
     "OpenAI 合池文档的计量单位逐字"),
    ("Codex is included across ChatGPT plans, including Free and Go.",
     "Codex 覆盖 Free 档的官方逐字"),
    ("It is not included with Free or Go.", "Codex Cloud 不覆盖 Free 档的官方逐字"),
    ("do not count toward the limit", "设备上限豁免 Free 档的官方逐字"),
    ("Device limits are separate from the number of accounts signed in at the same time",
     "退出登录不释放名额的官方逐字"),
    ("Buying credits or resetting usage won't clear a card or device restriction.",
     "买 credits 不解除限制的官方逐字"),
    ("Downloads last month", "HF downloads 滚动窗口的官方标签逐字"),
    ("downloadsAllTime", "HF 累计下载量的独立字段名"),
    ("OpenAI combines the Chat and Work modes into a single interface",
     "（不应出现：媒体转述标题的判断）"),
    ("until November 30, 2026", "Runware heygen 促销描述逐字"),
    ("Ollie is sunsetting on Nov 6, 2026", "Ollie 官方 CEO 告别信逐字"),
    ("50 messages from Ollie per month", "Ollie Free 档月消息数逐字"),
    ("6 free additional messages from Ollie every day", "Ollie Free 档每日免费追加逐字"),
    ("最低充值金额 10 元", "Kimi K3.1 Pro 充值门槛逐字"),
    ("完整模型权重将于 11 月 4 日前发布", "Kimi 权重时点逐字"),
    ("heygen-video-1-0-launch-promo", "Runware heygen 促销条目"),
    ("Event period: October 31, 00:00 – November 8, 23:59 (UTC+8)", "AutoClaw 国际站 M11W1 活动期逐字"),
    ("活动时间 11 月 2 日（周一）00:00—11 月 8 日（周日）23:59（北京时间）", "AutoClaw 国内站 M11W1 活动期逐字"),
    ("允许为非商业目的学习、运行、复制、修改和再分发授权作品", "HachimoDock 非商业许可逐字"),
    ("收费销售、出租、付费服务、商业产品集成", "HachimoDock 禁止商用逐字"),
    ("We added two sentences to Claude Code's prompt on Opus 5.5",
     "Anthropic 游戏复刻禁令的官方人员逐字"),
]
for needle, label in CHECKS:
    if label.startswith("（不应出现"):
        assert needle not in disk, ("表体里出现了不该出现的媒体转述判断", label, needle)
        continue
    assert needle in disk, ("表体缺关键口径", label, needle)

# ---- 断言 3b：055 期的错误结论必须已从表体里消失 ----
# ---- 断言 3b：055 期的错误结论必须已从表体里消失 ----
# ⚠️ **056 期新立的一条断言纪律**：**断言要盯「断言式表述」、不能盯「字符串」** ——
#    本期纠错第 2 条**必须引用 055 期的原话**（那是证据链），
#    所以「`在本期回到 `2026-10-31`」这个子串在表体里**本来就该存在**。
#    **正确的断言口径是「旧结论的断言式整句不在、引用式表述在」**。
_BAD_ASSERTIVE = [
    ("即那条 `heygen-video-1-0-launch-promo` 的 `endsAt` 在本期回到 `2026-10-31`",
     "055 期关于 heygen endsAt 的错误结论（断言式整句）"),
    ("生效中（本期新核到一手 · 距结束 11 天）", "冻结的距结束天数（upscale · 状态列）"),
    ("生效中（本期新核到一手 · 距结束 5 天）", "冻结的距结束天数（pruna-edit · 状态列）"),
    ("失效（距结束 5 天）", "冻结的距结束天数（M10W4 两行 · 截止列）"),
    ("· **距结束 8 天**）", "冻结的距结束天数（M11W1 两行 · 截止列）"),
    ("生效中（距开卖 0 天", "冻结的距开卖天数（天猫 · 状态列）"),
    ("；本轮出刊时点 10/20 午间，尚未开卖）。", "043 期的过时状态（天猫 · 状态列断言式）"),
    ("`endsAt` 已早于本期基准日 `2` 天", "冻结的已过天数（Kling 4.0）"),
]
for bad, label in _BAD_ASSERTIVE:
    assert bad not in disk, ("表体里仍留着往期的错误/冻结值（断言式）", label, bad)
# ⚠️ 引用式表述必须保留 —— 它是本期纠错第 2 条的证据链。
assert "055 期写「`endsAt` 在本期回到 `2026-10-31`」" in disk, \
    "本期纠错第 2 条的引用式表述丢失（应保留对 055 期原结论的引用）"
assert "这个「距结束 5 天」是自 049 期写入后就没再变过的冻结值" in disk, \
    "本期避坑 252 的证据链（冻结值自述）丢失"
print("断言 3b 通过：055 期的错误结论与全部冻结天数已从表体清除（断言式口径），引用式证据链保留")

# ---- 断言 4b：每条 NEW 行都必须带「本期」或「056 期」标记 ----
_change_re = re.compile(r"(本期|056\s*期)")
for _n in NEW:
    assert _change_re.search(_n), ("NEW 行缺「本期」标记，会被 split_ledger 移进总账", _n[:70])
print("断言 4b 通过：%d 条 NEW 行均带本期标记" % len(NEW))

# ---- 断言 4：本期新增的每个截止日口径都必须能在表体里查到 ----
for needle in ["11/6", "未公布", "无结束日"]:
    assert needle in disk, ("新增行截止列口径缺失", needle)

# ---- 断言 5（056 期沿用 054/055 期纪律②的守门断言）：每行字段数必须恰为 3 ----
_field_dist = Counter([l.count("|") - 1 for l in out
                       if l.startswith("| ") and not l.startswith("| 活动 |")
                       and not l.startswith("| --- |")])
assert _field_dist == Counter({3: len(out) - 2}), ("表体字段数分布异常（可能有单元格含竖线）", _field_dist)
print("断言 5 通过：字段数分布 %s" % dict(_field_dist))

nrows = len([l for l in out if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")])
print("rows %d = %d + %d" % (nrows, PREV, len(NEW)))
print("字段数分布", Counter([l.count("|") - 1 for l in out if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]))
print("CHECKS 全部通过")
