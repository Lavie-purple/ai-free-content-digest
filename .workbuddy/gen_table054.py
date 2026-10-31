# -*- coding: utf-8 -*-
"""054 期：从 053 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-10-31（隔日出刊）-> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table054.md（纯表格块，供 054 期正文嵌入）。

⚠️ 053 期立的纪律，本期全部沿用并加严：
   ① 输入直接取 **053 期 md 的现行文本**（不是取上一期的 tmp_table）——
      053 期栽在「inject 从存着旧表格的 body_a 注入，把 gen_table 的改写覆盖回去」。
   ② 写出循环必须是「**用键在行里找**」，不能写成 `if k in REWRITE`（k 是整行，永远不是键）。
   ③ 三条断言全加：键唯一命中 / 值在输出恰好出现一次 / 未改写行数守恒。
   ④ **053 期新立**：写盘后**重新读回落盘文件**再断言一遍。
   ⑤ **053 期新立（避坑 239）**：断言全过 ≠ 事实全对 —— 新增「表体关键口径 == 正文关键口径」
      与「本期新增的每个截止日都必须能在表体里查到」两条断言。
   ⑥ **054 期新立（避坑 243）**：`grep` 零命中 ≠ 官方没写 —— 本期对 `K2` 停新公告
      做了**同义表述多组检索**，并在表体行内写明「同一份文件上实读命中」。

本期性质：**隔日出刊**（053 期是 10/30 第一轮，窗口 10/29 15:30 → 10/30 09:30，约 18.0 小时；
  本期窗口 10/30 09:30 → 10/31 19:00，约 33.5 小时，跨越两个美西日）。
  1) **基准日推进到 2026-10-31**（053 期基准日是 10/30）—— 「距今 N 天」逐行重算，
     **断言是「天数 == 截止日 − 基准日」，不是「推进一天就 −1」**。
  2) 输入结构沿用 047 期起的结构：上期 4.1 表体（55 行）+ 总账全量表体（144 行）= 199 行。
     **4.2 的 29 行已含在总账里、不可重复加**。
  3) 本期改写 8 行（OpenRouter 目录三个数、百度 OCR 2 下载量、Runware Kling 4.0、
     Runware pruna-upscale、Runware pruna-edit、Runware heygen 促销延长、国家超算互联网、
     Moonshot K2 停新、Claude Max/Ultra 档 —— 共 9 行，见下）
  4) 本期新增 6 行：OXR 免费 API + OXR 开放权重、AutoClaw M11W1 国际站、AutoClaw M11W1 国内站、
     Anthropic Ultra 档、Open-H3-Regenerate-2K 开放权重、Ollie 关停。
"""
import io
import re
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第053期-2026-10-30.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table054.md"
BASE = date(2026, 10, 31)
PREV = 199


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
assert len(rows_41) == 55, ("053 期 4.1 表体行数", len(rows_41))
assert len(rows_led) == 144, ("总账全量行数", len(rows_led))
body = rows_41 + rows_led
assert len(body) == PREV, (len(body), PREV)

header = "| 活动 | 截止 | 状态 |"
sep = "| --- | --- | --- |"

REWRITE = {}


def build(key, subs, tail=None):
    """行级改写。**幂等**：若该行已含本期标记（`（054 期）`），说明上一轮已改写过，
    则直接原样返回、不再重复替换 —— 否则重跑流水线会二次改写或断言失败。
    """
    hits = [l for l in body if key in l]
    assert len(hits) == 1, ("键未唯一命中", key, len(hits))
    out = hits[0]
    if "（054 期）" in out and all(a not in out for a, b in subs):
        return out
    for a, b in subs:
        assert a in out, ("片段未命中", key, a[:70])
        out = out.replace(a, b)
    if tail:
        assert out.rstrip().endswith("|")
        out = out.rstrip()[:-1].rstrip() + " " + tail + " |"
    return out


# ================= 一、OpenRouter 目录（464/19/16 → 456/19/16 + 全量逐条 diff） =================
# ⚠️ 053 期的正文写 `456/19/16`，但表体那行仍是 `464/19/16`（047 期旧数）—— 表体层慢一拍。
#    本期一并补上并推进到今天的真实值；且本期把 053 期挂账项⑪「全量 456 逐条 diff」做完。
REWRITE["🟢 **OpenRouter 免费档（**官方 API 目录口径"] = build(
    "🟢 **OpenRouter 免费档（**官方 API 目录口径",
    [
        ("**官方 API 目录口径 · `464/19/16`**",
         "**官方 API 目录口径 · `456/19/16`**"),
    ],
    tail="**⚠️ （054 期）流通量与目录口径记账（避坑 029：升/降/同值都要记账）**："
         "**本期实访 `openrouter.ai/api/v1/models`（本轮连抓三次 —— `or_models.json` / `or_models2.json` / "
         "`or_models4.json`，**三次读数完全一致**）：全量 `456` / 零价 `19` / `:free` `16`。**"
         "⚠️ 三个数全部逐条零变化**。"
         "**⚠️ 053 期记的「`464/19/16`」是 047 期的旧数 —— 本期已补正并推进到 `456/19/16`"
         "（053 期正文写对了、表体没跟上，**表体层比正文层慢一拍**，避坑 239）。**"
         "**⚠️ 本期把 053 期挂账项⑪「`OpenRouter` 全量 `456` 逐条 diff」做完了**："
         "053 期把 `456` 条全量 ID 存档于 `.workbuddy/data/tmp_or_all_2026-10-30_053.txt`（`456` 行），"
         "本期存档于 `.workbuddy/data/tmp_or_all_2026-10-31_054.txt`（`456` 行），"
         "**逐条 `diff` 结果：新增 `0` 条、消失 `0` 条 —— 全部 `456` 条逐条同值**（避坑 212）。"
         "**⚠️ 本期把两套口径彻底拆成两个独立存档文件**（053 期的 `tmp_or_free_*_053.txt` 实际存的是**零价集合**）："
         "`tmp_or_zero_2026-10-31_054.txt`（`19` 条零价）＋ `tmp_or_free_2026-10-31_054.txt`（`16` 条 `:free`）"
         "—— **两套口径各自逐条 diff 均为零变化**。"
         "**⚠️ 零价 `19` 与 `:free` `16` 差的 `3` 条仍是同三条**：`google/lyria-3-clip-preview`、"
         "`google/lyria-3-pro-preview`、`openrouter/free`（**零价但不带 `:free` 后缀** —— "
         "避坑 161：**两套口径不可互相代替**）。"
         "**⚠️ 第三方口径与官方冲突照旧两个都写**：`freellm.net/providers/openrouter` 专页逐字 "
         "`Free OpenRouter API Key, Base URL & Rate Limits: ... 19 Models` —— **与官方零价 `19` 一致、"
         "与官方 `:free` `16` 不一致**；该页另逐字 `200 req/day (free tier)`，与官方口径"
         "（`50` 请求每日 / 充值满 `10 credits` 后 `1,000` 请求每日、`20` 次每分）冲突，"
         "**两个口径都写、不取其一**（避坑 161）。",
)

# ================= 二、百度 Unlimited OCR 2 下载量（18,141 → 69,231） =================
# ⚠️ 053 期那条表体行**已被 `slim_table.py` 裁掉了 `downloads` / `likes` 数字**
#    （`slim` 只在状态列保留「谁 / 到什么时候 / 要不要动手」+ 一句边界）——
#    **但流通量是避坑 029 要求的必记账项，不能因为被裁就不记**。
#    因此本期**不改写片段、直接在 tail 里追加本期实读的流通量**。
#    ⚠️ 这也正是 053 期记的「表体层比正文层慢一拍」的**第三种形态**：
#    不是「数字写错了」，是「数字被裁掉了、读者在表体里看不到」。
REWRITE["🟢 **`百度` 开源 `文心 Unlimited OCR 2`（**MIT 许可"] = build(
    "🟢 **`百度` 开源 `文心 Unlimited OCR 2`（**MIT 许可",
    [],
    tail="**⚠️ （054 期）流通量记账（避坑 029：升/降/同值都要记账）**："
         "**`downloads 69,231`（053 期 `18,141`）、`likes 468`（053 期 `383`）** —— "
         "**相对 053 期涨 `51,090`（涨 `281%`）**。"
         "**⚠️ 053 期挂账项⑳问的「是否继续增长」—— 本期答案是「继续增长，且涨幅比上期还大」**"
         "（**053 期是 `8,357` → `18,141`、涨 `9,784`；本期是 `18,141` → `69,231`、涨 `51,090`**）"
         "—— **该问项本期销项**。"
         "**⚠️ 本轮连抓两次 —— `hf_ocr2_re1.json` 与 `hf_ocr2_re2.json`，两次读数完全一致**"
         "（`downloads 69,231` / `likes 468` / `lastModified 2026-10-29T09:18:46Z` / "
         "`createdAt 2026-10-26T03:57:46Z`）。"
         "**⚠️ 上一代 `baidu/Unlimited-OCR` 的 `downloads` 是 `3,535,406`（053 期）→ `3,966,076`（本期），"
         "涨 `430,670` —— 两个模型必须分开读、不可合并**。"
         "**⚠️ `ModelScope` 侧本期返回体仍无下载量字段 —— 仍写「该侧无可比口径」**（避坑 154）。"
         "**⚠️ 本报告不追 `HF` 下载量跳涨的成因**（官方没给口径），**只记数**。"
         "**⚠️ 一条方法论记录**：**053 期这条表体行的 `downloads` / `likes` 被 `slim_table.py` 裁掉了** "
         "—— **「表体层比正文层慢一拍」除了「数字写错」还有「数字被裁掉」这一种形态**"
         "（避坑 239 的延伸）。",
)

# ================= 三、Runware Kling 4.0 促销（endsAt 10/29 → 相对 10/31 已过期 2 天） =================
REWRITE["🟢 **`Runware` 分发层 `Kling 4.0` 促销 `15% OFF`（**官方 `pricing` 页促销数组"] = build(
    "🟢 **`Runware` 分发层 `Kling 4.0` 促销 `15% OFF`（**官方 `pricing` 页促销数组",
    [
        ("🟢 **官方促销数组仍保留该条目、但 `endsAt` 已早于本期基准日 `1` 天 —— "
         "即「数组里还在」不等于「活动还在售」（避坑 230）。",
         "🟢 **官方促销数组仍保留该条目、但 `endsAt` 已早于本期基准日 `2` 天 —— "
         "即「数组里还在」不等于「活动还在售」（避坑 230）。"),
    ],
    tail="**⚠️ （054 期）这条的截止日跨过了基准日 —— 三态要分开写**："
         "052 期（基准日 `10/29`）它属「截止日当天」（避坑 223），"
         "053 期（基准日 `10/30`）它变成「已过期 `1` 天」，"
         "**本期（基准日 `10/31`）它变成「已过期 `2` 天」**。"
         "**⚠️ 本期实访 `runware.ai/pricing`（`200` / `748,098` 字节）确认：官方促销数组仍是 `14` 条 —— "
         "**⚠️ 但本期不是「逐条零变化」**：有一条在售促销的 `endsAt` 被官方延长了 `30` 天"
         "（见本期改写的 `Runware` `heygen` 那行）。"
         "**⚠️ 052 期挂账项⑨「那 `7` 条已过期仍在数组里的条目会不会被清理」—— 本期是连续第 `2` 次销项、"
         "答案仍是「一条都没清理」**（避坑 230）。",
)

# ================= 四、Runware pruna-upscale（距今天数由重算器处理） =================
# ⚠️ 只做「本期实访同值」的记账，天数由 recalc_days054.py 独立重算（不靠批量减一）。

# ================= 五、Runware pruna-edit（同上） =================

# ================= 六、Runware heygen 促销：官方把 endsAt 从 10/31 延长到 11/30 =================
# ⚠️ 这是本期唯一一条「条数不变、过期数不变、单条内容变了」的记录 —— 053 期与 052 期连续两期写的
#    「逐条零变化」在本期被打破。
REWRITE["🟢 **HeyGen Voice（AA 语音合成榜首，促销五折）**"] = build(
    "🟢 **HeyGen Voice（AA 语音合成榜首，促销五折）**",
    [
        ("🟢 **生效中（距今 1 天）。 ⚠️ 榜首为单一榜单口径（避坑 116）；",
         "🟢 **生效中（距今 1 天）。 ⚠️ 榜首为单一榜单口径（避坑 116）；"),
    ],
    tail="**⚠️ （054 期）本行对应的 `Runware` 促销数组条目（`heygen-video-1-0-launch-promo`）"
         "本期出现变更 —— 官方把截止日往后延了 `30` 天**："
         "**053 期实读 `endsAt: \"2026-10-31\"`、描述逐字「`50% off all generations until October 31, 2026`」；"
         "本期实读 `endsAt: \"2026-11-30\"`、描述逐字「`50% off all generations until November 30, 2026`」** —— "
         "**即「条数不变（`14` 条）、已过期条数不变、单条内容可变」是第三种变化形态**"
         "（避坑 238 的新变体，详见第五章纠错第 1 条）。"
         "**⚠️ 相对新基准日 `10/31`，本行距结束 `30` 天**（截止日 `11/30`）。"
         "**⚠️ 一次实读两个文件才敢下这个结论**：`runware_pricing5.html`（本期）与 "
         "`tmp_053/runware_pricing5.html`（053 期存档）逐字段比对。",
)

# ================= 七、国家超算互联网夜间免费（10/30 → 相对 10/31 已过期 1 天） =================
REWRITE["🟠 **`国家超算互联网` 夜间限时免费调用 `Auto` 模型"] = build(
    "🟠 **`国家超算互联网` 夜间限时免费调用 `Auto` 模型",
    [
        ("**10/30（官方逐字「`10月21日至30日`」—— **截止日＝本期基准日当天**）**",
         "**10/30（官方逐字「`10月21日至30日`」—— **截止日已早于本期基准日 `1` 天**）**"),
        ("🟠 **生效中（限时免费 · 资格限「订阅 `TokenPlan` 用户」）。",
         "🟠 **截止日已过（限时免费 · 资格限「订阅 `TokenPlan` 用户」）。"),
    ],
    tail="**⚠️ （054 期）这条的截止日跨过了基准日 —— 三态要分开写**："
         "053 期（基准日 `10/30`）它属「截止日当天」（避坑 223），"
         "**本期（基准日 `10/31`）它变成「截止日已过 `1` 天」**。"
         "**⚠️ 本报告只写「截止日已过」，不写收口字样**（**⚠️ 这句话本身必须绕开 `classify()` 的判定词 —— "
         "**避坑 239：状态列里一旦出现判定词的字面文本，整行就会被归进对应桶**，**"
         "本期初稿正是这么写的、自己把这一行误判成了 `over`**）—— "
         "**官方未公布停用时刻，且本轮实访 `www.scnet.cn`（`200` / `132,762` 字节，与 053 期抓取字节数完全相同）—— "
         "「`TokenPlan`」「夜间」「`21:00`」「`0.1元`」「免费」「`Auto模型`」六个词仍各命中 `0` 次** "
         "—— **官方页连续第 `2` 期未核到，053 期挂账项②不销项**（避坑 154）。",
)

# ================= 八、Moonshot K2 停新：官方定价页逐字核到（被追 7 期的挂账项本期销项） =================
REWRITE["🔴 **`Moonshot` `K2` 系列模型停新注册与计划下线"] = build(
    "🔴 **`Moonshot` `K2` 系列模型停新注册与计划下线",
    [
        ("🔴 **生效中（义务性变更，不是活动）。",
         "🔴 **截止日当天（义务性变更，不是活动）。"),
    ],
    tail="**⚠️ （054 期）官方一手逐字核到了 —— 053 期挂账项⑩的「公告原文」这一半本期销项**："
         "**一手 `platform.moonshot.cn/docs/pricing/chat` 与 `platform.kimi.com/docs/pricing/chat`"
         "（各 `200` / `1,701` 字节，两个域名内容一致），官方逐字**："
         "`K2 系列模型将于 2026 年 10 月 31 日起停止向新注册用户开放，已注册用户不受影响；"
         "我们计划在 12 月底下线所有 K2 系列模型，请提前做好 迁移准备 。` "
         "**⚠️ 053 期记的是「四个候选文档页的 `停新` 相关词各命中 `0` 次 → 未核到」—— "
         "本期在同一份 `kimi_pricing2.html` 上实读，`停止`/`下线`/`2026 年 10 月 31 日`/`10 月 31` "
         "**各命中 `1` 次** —— **即 053 期是「当期没读到那一段」，不是「官方没写」**（新立避坑 243）。**"
         "**⚠️ 本期是「截止日当天」（`10/31` ＝ 基准日当天，避坑 223）—— "
         "既不是「已过期」也不是「未到」。**"
         "**⚠️ 三个日期仍要拆开**：**① `10/31` 停新注册（新用户受影响）② `12 月底` 计划下线"
         "（已注册用户受影响、官方只给到月份精度，本报告不替它排到 `12/31`）③ 「停止向新注册用户开放」≠「下线」**。"
         "**⚠️ 同期核到同页另一条免费口径（官方逐字）**："
         "`文件相关接口（文件内容抽取/文件存储） 限时免费 ，即您只上传并抽取文档时，文件接口本身不产生费用。` "
         "—— **官方逐字写「限时免费」但没给结束日，本行不替它排日**（避坑 154）。"
         "**⚠️ 挂账项⑩的另一半「停新当日新用户能否注册」需登录态实测，本期不做** —— "
         "官方公告原文已核到，但「如期执行」未验证，两件事不合并。",
)

# ================= 九、Google Nano Banana 2 停用（10/29 → 相对 10/31 已过期 2 天） =================
REWRITE["🟢 **Google Nano Banana 2 停用（Gemini API）**"] = build(
    "🟢 **Google Nano Banana 2 停用（Gemini API）**",
    [
        ("🟢 **生效中（停用日 10/29 已过 · 本期基准日 10/30 已过 1 天 · "
         "官方未公布具体停机时刻，故本报告不写「已停用」）。",
         "🟢 **生效中（停用日 10/29 已过 · 本期基准日 10/31 已过 2 天 · "
         "官方未公布具体停机时刻，故本报告不写「已停用」）。"),
    ],
    tail="**⚠️ （054 期）这条的停用日跨过了基准日 —— 三态要分开写**："
         "053 期（基准日 `10/30`）写「已过 `1` 天」，"
         "**本期（基准日 `10/31`）真值是「已过 `2` 天」**。"
         "**⚠️ 本报告只写「停用日已过」，不写「已停用」** —— "
         "**官方未公布具体停机时刻，本轮 `Google` 一手仍全线不可达**"
         "（`ai.google.dev` / `aistudio.google.com` / `blog.google` 不可达）—— "
         "**「截止日已过」与「已确认停用」是两件事**（避坑 154）。",
)

# ================= 十、Claude Max/Ultra 档改版（新增 4.2 行，不改写 4.1 行） =================
# ⚠️ Claude Max/Ultra 是「常驻权益本期变更」（无结束日），按 047 期起的结构进 4.2，
#    故本期是**新增行**而非改写行 —— 见 NEW。

NEW = []

# ---- 本期新增 1：OXR 官方免费 API（本报告至今第一次读到「免注册免 key + 明写数字」的免费 API）----
NEW.append(
    "| 🟢 **`OXR` 官方「免费 API」（**`SoMark` 团队 · 开放权重文档解析模型 `1.3B` · "
    "**官方逐字免注册免 `API key`** · **官方写明 `500` 页/日 ＋ `2,000` 页/月**）** | "
    "**未公布（官方逐字 `We'll keep the free API online until we can no longer afford to run it.` "
    "—— **没有日期的期限，本报告不替它排日**）** | "
    "🟢 **生效中（限时免费 · **官方一手来源是 `docs.somark.ai` 的 `.md` 原文直链，不是聚合器**）。 "
    "⚠️ 官方逐字（`docs.somark.ai/en/documentation/free-tier-rules.md`，`200` / `1,290` 字节）："
    "`Daily free quota` 一行：`Up to 500 pages of free quota per day`、"
    "`Monthly free quota` 一行：`Up to 2000 pages of free quota per month`、"
    "`Daily reset time` 一行：`Daily free quota resets at 00:00 each day`、"
    "`Monthly reset time` 一行：`Monthly free quota resets at 00:00 on the 1st of each month`、"
    "`Free quota is consumed first. After the free quota is exhausted, the system automatically "
    "starts consuming paid quota.` "
    "⚠️ 官方逐字（`docs.somark.ai/en/api-reference/oxr/index.md`，`200` / `4,580` 字节）："
    "`OXR provides a free API so you can test parsing on your own documents without registering "
    "or requesting an API key.`、`The Free OXR API requires no authentication. Set api_key to any "
    "value, such as dummy.`、`Up to 10MB per file` / `Up to 20 pages per request`、"
    "`Files over these limits are rejected.` "
    "⚠️ 四层开放（避坑 41）：① 能用 —— 逐字 `without registering or requesting an API key`；"
    "② 能下载 —— 是（`HF` 实读 `SoMarkAI/OXR-1.0`，`gated false`、`downloads 3,180`）；"
    "③ 能跑 —— **官方给了数字**（`500` 页/日 ＋ `2,000` 页/月）；"
    "④ 能商用 —— ⚠️ **见本期新增的 `OXR` 开放权重那行**（`LICENSE` 有 `$2,000,000` 双阈值）。 "
    "⚠️ **四条必须写清的边界**：① **官方自己劝你别上生产** —— 逐字 "
    "`We do not recommend using the Free OXR API in production. We do not guarantee service stability, "
    "and requests are queued, so processing speed may vary slightly.`；"
    "② **超额自动扣付费额度**（逐字 `the system automatically starts consuming paid quota`）—— "
    "**「超额就免费停服」官方没写，本报告不推断**；"
    "③ **`api_key` 字段仍要传、填 `dummy` 即可**（**不是「完全不传 key」**）；"
    "④ **免费档上限只有付费档的一小截** —— 官方逐字对照 `10MB` / `20` 页 vs 付费档 `200MB` / `300` 页。 "
    "⚠️ **归期**：官方 `README.md` 的 `Free API` 段**最早见于提交 `0245ee0e`（`2026-10-19T10:11:58Z`）** "
    "—— 本报告实读逐 commit 的 `README.md` 内容确认（`8532b8cb` / `614f0ecb` / `207d8bec` 三版均无该段）—— "
    "**落在 051 期窗口之前，本报告此前从未覆盖过它，本期按「首次登记的往期事件」写入**（避坑 229）。 "
    "⚠️ **本条的取数路径值得记住（新立避坑 241）**：**官方文档站 `docs.somark.ai/llms.txt`"
    "（`200` / `6,561` 字节）里有一行 `- [Free tier rules](...)` 直链 —— "
    "**顺着它拿到的 `.md` 原文是纯文本、网页版正文却是 JS 渲染的**。** |"
)

# ---- 本期新增 2：OXR 开放权重（Apache-2.0 底子 + 三条附加条款）----
NEW.append(
    "| 🟢 **`OXR-1.0` 开放权重文档解析模型（**`1.3B` · 单流 `DiT` 之外的自研架构 · "
    "**`Apache-2.0` 底子 ＋ 三条附加条款** · `HF` `gated false`**）** | "
    "**无结束日（权重永久开放；官方未给任何活动期或截止日）** | "
    "🟢 **已开放权重（第 ④ 级已到 · **本期首次登记的往期事件** · **⚠️ 商用许可有金额门槛**）。 "
    "⚠️ 一手（`github.com/SoMarkAI/OXR`，仓库 `200`；`README.md` `200` / `19,333` 字节；"
    "`LICENSE` `200` / `2,394` 字节；`HF` `SoMarkAI/OXR-1.0`：`downloads 3,180` / `likes 132` / "
    "`lastModified 2026-10-24T15:59:48Z` / `gated false`）："
    "`Pretrained from scratch, OXR uses a recursive self-improvement (RSI) loop during post-training`、"
    "`OXR can recognize 13 document element types`、"
    "`GPU memory to get started: 24GB on a single GPU`、"
    "`Recommended GPU memory: ≥48GB on a single GPU`。 "
    "⚠️ **许可证必须逐条读完（避坑 242）** —— 官方逐字 "
    "`OXR is licensed under the Apache License, Version 2.0, subject to the additional terms below. "
    "These additional terms take precedence in the event of a conflict` —— **三条附加条款**："
    "**① 商用免单独许可有双阈值** —— 逐字 `only while you and your Affiliates, on a consolidated basis, "
    "do not exceed either of the following thresholds: (a) USD 2,000,000 in Total Funding; or "
    "(b) USD 2,000,000 in Annual Revenue`，**超任一条要另签商业许可**；"
    "**② 对外提供在线服务必须显著署名** —— 逐字 `you must prominently identify SoMark OXR in the "
    "service's user interface or publicly accessible documentation`；"
    "**③ 禁止做竞品托管 API** —— 逐字 `you may not use OXR or its Derivative Works to offer, operate, "
    "or make available to third parties a hosted API service that competes with a hosted API service "
    "offered by SoMark Team or its Affiliates`。 "
    "⚠️ **官方自报指标的限定语照录** —— 逐字 `OXR ranks #1 on olmOCR-Bench, OmniDocBench, and "
    "DocParsingBench`、速度第一的限定语是逐字 `among open-source document parsing models` "
    "—— **本报告不把它扩写成「全部模型最快」**（避坑 116）。"
    "**⚠️ 媒体（量子位 `10/30 13:52`）给的三个具体分（`97.18`/`87.84`/`87.76`）在官方 `README.md` 里零命中**"
    "（一手 README 只说「`#1`」不给分值）—— **本报告只写「官方自述 #1」、不写具体分值、也不采信媒体分值**"
    "（避坑 154）。** |"
)

# ---- 本期新增 3：AutoClaw M11W1 国际站 ----
NEW.append(
    "| 🟢 **智谱 `AutoClaw` 国际站 `M11W1` 万圣节档：登录领 **40M** Tokens"
    "（**`autoclaw.z.ai` · 10/31–11/8 · 上周未领可叠加至 80M**）** | "
    "**11/8 23:59（`UTC+8`）失效（官方逐字 `Event period: October 31, 00:00 – November 8, 23:59 (UTC+8)` "
    "· **距结束 8 天**）** | "
    "🟢 **生效中（限时免费 · **⚠️ 国际站与国内站是两个不同的数，新立避坑 240**）。 "
    "⚠️ 一手（`autoclaw.z.ai/blog/news/M11W1/`，`200` / `42,467` 字节，官方 `datePublished "
    "`2026-10-30T08:17:44Z` ＝ 北京 `10/30 16:17`，**落在本期窗口内**）："
    "标题逐字 `Halloween Surprise: Claim Up to 80M Tokens!`、"
    "逐字 `From October 31 to November 8 , log in to AutoClaw and get 40 million Tokens !`、"
    "逐字 `Starting October 31 (UTC+8), you can claim a new 40M Tokens (4,000 credits) reward. "
    "If you haven't claimed last week's reward yet, you can claim both rewards for up to 80M Tokens "
    "(8,000 credits) in total!`、逐字 `one claim per account`、"
    "逐字 `These credits expire on November 8 at 23:59 (UTC+8).` "
    "⚠️ 四层开放（避坑 41）：① 能用 —— 逐字 `log in to AutoClaw during the event to claim`；"
    "② 能下载 —— 不适用（积分档）；③ 能跑 —— 给了 `Tokens` 数与 `credits` 当量、也给了到期时刻；"
    "④ 能商用 —— 官方口径未涉及。 "
    "⚠️ **四条边界**：① **「`80M`」是条件量** —— 逐字 `If you haven't claimed last week's reward yet`"
    "（**上周没领才能叠到 80M**）；② **每账号一次** —— 逐字 `one claim per account`；"
    "③ **与上期 `M10W4` 的奖励是两个到期日**（`11/1` 与 `11/8`）—— **两笔账不可相加**（避坑 117 同族）；"
    "④ **国际站起始日是 `10/31`、国内站是 `11/2`** —— 逐字 `Starting October 31 (UTC+8)`。 "
    "⚠️ **053 期强制动作⑧「`AutoClaw` 国内站 `M10W5` 是否发布」的答案**："
    "**国内站博客列表实读 —— 没有 `M10W5` 这个编号，国内站直接发了 `M11W1`**"
    "（**该挂账项本期销项，但销项答案是「那个编号不存在」而不是「那个编号发布了」**）。** |"
)

# ---- 本期新增 4：AutoClaw M11W1 国内站 ----
NEW.append(
    "| 🟢 **智谱 `AutoClaw` 国内站 `M11W1` 万圣节档：登录领 **50M** Tokens"
    "（**`autoclaw.zhipuai.cn` · 11/2–11/8 · **与国际站三个数都不同**）** | "
    "**11/8 23:59（北京时间）失效（官方逐字 `活动时间 11 月 2 日（周一）00:00—11 月 8 日（周日）23:59"
    "（北京时间）` · **距结束 8 天**）** | "
    "🟢 **生效中（限时免费 · **⚠️ 与国际站是两个活动，新立避坑 240**）。 "
    "⚠️ 一手（`autoclaw.zhipuai.cn/blog/news/M11W1/`，`200` / `47,058` 字节，官方 `datePublished "
    "`2026-10-30T10:07:34Z` ＝ 北京 `10/30 18:07`，**落在本期窗口内**）："
    "标题逐字 `每周福利：50M Tokens 等你领取！`（日期 `2026年10月30日`）、"
    "逐字 `11 月 2 日至 11 月 8 日 ，登录 AutoClaw，即得 50M Tokens 。`、"
    "逐字 `活动时间 11 月 2 日（周一）00:00—11 月 8 日（周日）23:59（北京时间）`、"
    "逐字 `登录 AutoClaw，即可领取 50M Tokens（相当于 5,000 积分），每个账号限领一次。`、"
    "逐字 `奖励将在 11 月 8 日 23:59 失效`。 "
    "⚠️ **与国际站逐项对照（避坑 240 的核心样本）**："
    "**① 标题标的量 `50M` vs `Claim Up to 80M Tokens!`；② 本周可领量 `50M`（`5,000` 积分）vs `40M`"
    "（`4,000` credits）；③ 起始日 `11/2` vs `10/31`（**晚两天**）；④ 积分当量 `5,000` vs `8,000`；"
    "⑤ 到期日两者相同（`11/8`）**。**⚠️ 本报告五个数全写、不替官方取一个代表值。** "
    "⚠️ 四层开放（避坑 41）：① 能用 —— 逐字 `登录 AutoClaw，即可领取`；② 能下载 —— 不适用；"
    "③ 能跑 —— 给了 `Tokens` 数与积分当量；④ 能商用 —— 官方口径未涉及。 "
    "⚠️ **边界**：**每账号限领一次**（逐字 `每个账号限领一次`）；**国内站无「叠加到 80M」的说法** —— "
    "**国际站那句 `If you haven't claimed last week's reward yet` 在国内站页面零命中**。** |"
)

# ---- 本期新增 5：Anthropic Ultra 档（Max 20x 更名 + 取消 5 小时限制 + 月度 credits 翻倍）----
NEW.append(
    "| 🟡 **`Anthropic` 订阅档改版：`Max 5x`→`Max`、`Max 20x`→**`Ultra`**"
    "（**`$200`/月 · 取消 5 小时限制 · 周额度 `10x` Pro · 月度 API credits `$100`→`$200`**）** | "
    "**未公布（官方未给任何活动期或截止日）** | "
    "🟡 **生效中（**付费订阅附带的权益，不是免费额度** · **本期改版**）。 "
    "⚠️ 一手（`claude.com/pricing`，`200` / `1,323,504` 字节；`support.claude.com/en/articles/"
    "11175166-about-claude-pro-max-and-ultra-plans`，`200` / `254,392` 字节）官方逐字："
    "`Ultra For your longest tasks $200 Per month Try Claude Everything in Max, plus: No 5-hour limit "
    "‡ 10x Pro usage every week* $200 a month in API credits, up from $100 on Max † New`、"
    "脚注逐字 `‡ No 5-hour limit for verified accounts.`、"
    "**官方对照表逐字**（`Limit every 5 hours` 一行四格：`Free`=`Limited`／`Pro`=`1x`／`Max`=`5x`／`Ultra`=`No 5-hour limit ‡`）" + 
    "（`Limit every week` 一行四格：`Free`=`Limited`／`Pro`=`1x`／`Max`=`5x`／`Ultra`=`10x`）。 "
    "⚠️ **与免费读者相关的那一条只有 `Free` 档** —— 对照表第 1 列两格**都逐字写 `Limited`**"
    "（**不是 `1x`、官方也没给数字**）；**`Pro`/`Max`/`Ultra` 三档全是付费档，本报告只登记其中"
    "「订阅送 API credits」这一条与读者算账直接相关的口径**（避坑 41：多档位口径要拆开写）。 "
    "⚠️ **四条边界**：① **月度 API credits 不是免费额度** —— 官方支持页逐字 "
    "`Monthly API credits: Claude Max, Ultra, and Team plans include monthly credits for the Claude API.`"
    "—— **官方这句里没有 `Pro`**，即 **`Pro` 档没有这一项**；"
    "② **「取消 5 小时限制」有前提** —— 逐字 `for verified accounts`；"
    "③ **官方自己写了这个前提** —— 逐字 `* Usage limits apply. How fast you reach a limit depends on "
    "the model you use, how long your chats are, and how large your files are.`；"
    "④ **官方页面不带发布日期** —— 本报告据「官方定价页实读 ＋ 媒体在窗口内报道（量子位 `10/31 13:05`）」"
    "两者并写，不替官方补日期。** |"
)

# ---- 本期新增 6：Ollie 关停（付费订阅制产品，非免费额度，但「工具消失」是读者要知道的）----
NEW.append(
    "| ⚠️ **`Ollie`（隐私向 AI 助手）宣布关停（**`11/6` 正式停服 · 付费订阅制、非免费额度**）** | "
    "**11/6（媒体转述官方公告逐字 `the app will officially shut down on November 6`）** | "
    "⚠️ **生效中（**关停倒计时 · **如果你是用户，这几天要导出数据**）。 "
    "⚠️ 逐字（**媒体转述**，`techcrunch.com/2026/10/30/ollie-a-privacy-focused-ai-assistant-is-"
    "shutting-down/`，`200` / `233,563` 字节，`Lucas Ropek 3:56 PM PDT · October 30, 2026` —— "
    "**落在本期窗口内**）：`it will be shutting down in a week`、`the app will officially shut down "
    "on November 6`、`Ollie, which discussed its $7.5 million seed round led by Khosla Ventures with "
    "TechCrunch in September, offered a subscription-based model.`、"
    "CEO `Bill Lennon` 逐字 `We got close, but ultimately couldn't keep up`、"
    "逐字 `Ollie's customers will receive instructions on how to export data and receive refunds "
    "in the coming days`。 "
    "⚠️ **三条边界**：① **这是付费订阅制产品、不是免费额度条目** —— 本报告如实登记、"
    "**但它是一个「低价 AI 工具消失」的事实**；② **官方一手未核到** —— CEO 原帖在 `X` 上，本期未抓；"
    "③ **关停日 `11/6` 距今 `6` 天** —— **官方给的窗口是「一周内」不是确切到日的承诺**，"
    "本报告写的是媒体逐字引用的 `November 6`。** |"
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
    ("69,231", "百度 Unlimited OCR 2 下载量"),
    ("Up to 500 pages of free quota per day", "OXR 免费额度逐字"),
    ("Up to 2000 pages of free quota per month", "OXR 月度免费额度逐字"),
    ("without registering or requesting an API key", "OXR 免注册免 key 逐字"),
    ("the system automatically starts consuming paid quota", "OXR 超额扣费逐字"),
    ("USD 2,000,000 in Total Funding", "OXR 许可双阈值逐字"),
    ("Claim Up to 80M Tokens!", "AutoClaw 国际站标题逐字"),
    ("11 月 2 日至 11 月 8 日", "AutoClaw 国内站逐字"),
    ("2026-11-30", "Runware heygen 促销延长后的截止日"),
    ("2026-10-31", "Moonshot K2 停新日"),
    ("No 5-hour limit for verified accounts", "Claude Ultra 5 小时限制逐字"),
    ("the app will officially shut down on November 6", "Ollie 关停逐字"),
]
for needle, label in CHECKS:
    assert needle in disk, ("表体缺关键口径", label, needle)

# ---- 断言 4b（054 期新立）：**每条 NEW 行都必须带「本期」或「054 期」标记** ----
# ⚠️ `split_ledger.py` 靠 `CHANGE_RE = (本期|<期号> 期)` 判断「这一行本期有变化」→ 留在 4.2；
#    **不带标记的新增行会被当成「无变化的常驻权益」移进《常驻权益总账》—— 读者在 4.2 看不到它。**
#    本期就踩了：`Anthropic` `Ultra` 档那行没写标记 → 被移进总账 → 4.2 少一行。
_change_re = re.compile(r"(本期|054\s*期)")
for _n in NEW:
    assert _change_re.search(_n), ("NEW 行缺「本期」标记，会被 split_ledger 移进总账", _n[:70])
print("断言 4b 通过：%d 条 NEW 行均带本期标记" % len(NEW))

# ---- 断言 4：本期新增的每个截止日都必须能在表体里查到（防「正文写了、表体没有」）----
for needle in ["11/8", "11/6", "未公布", "无结束日"]:
    assert needle in disk, ("新增行截止列口径缺失", needle)

nrows = len([l for l in out if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")])
print("rows %d = %d + %d" % (nrows, PREV, len(NEW)))
from collections import Counter
print("字段数分布", Counter([l.count("|") - 1 for l in out if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]))
print("CHECKS 全部通过")
