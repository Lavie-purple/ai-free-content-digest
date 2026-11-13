# -*- coding: utf-8 -*-
"""067 期：在 066 期现行 4.1/4.2 表体上做行级改写 + 补入 1 行 4.1 + 2 行 4.2。

纪律（055–066 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；
  ③ 断言用逐字短语；④ 全表字段数分布断言；⑤ 补入行必须带「067 期」标记；
  ⑥ 状态列整体替换；⑦ 单元格不许出现 `|`；⑧ 天数一律由基准日实算。
"""
import io
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第067期-2026-11-13.md"
PTR = " [附录 067](details.html) |"
TODAY = date(2026, 11, 13)

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")


def rows_of(text, start, end):
    i = text.index(start)
    j = text.index(end)
    return [l for l in text[i:j].split("\n")
            if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]


r41 = rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
r42 = rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("输入行数：4.1 = %d，4.2 = %d" % (len(r41), len(r42)))
assert len(r41) == 57, ("066 期 4.1 行数", len(r41))
assert len(r42) == 33, ("066 期 4.2 行数", len(r42))


def past(s):
    m, d = s.split("/")
    return (TODAY - date(2026, int(m), int(d))).days


def left(s):
    m, d = s.split("/")
    return (date(2026, int(m), int(d)) - TODAY).days


def name_of(r):
    return r.strip().strip("|").split("|")[0].strip()


def set_status(row, status):
    cells = row.strip().rstrip("|").split("|")
    assert len(cells) == 4, ("字段数异常", len(cells), row[:40])
    assert "|" not in status, ("状态列里出现竖线", status[:40])
    return "|%s|%s| %s%s" % (cells[1], cells[2], status, PTR)


EDITED = []


def edit(tag, prefix, status, bucket):
    hits = [k for k, r in enumerate(bucket) if prefix in name_of(r)]
    assert len(hits) == 1, ("命中数不是 1", tag, len(hits))
    old = bucket[hits[0]]
    new = set_status(old, status)
    assert new != old, ("改写未生效", tag)
    bucket[hits[0]] = new
    EDITED.append(tag)


# ------------------------------------------------------------ 4.1：补入 1 行
MINIMAX = ("| 🟠 **MiniMax `H3-Image` `4K` 生图限时 `5` 折（**官方定价页横幅逐字「4K 生图限时 5 折」·"
           " 要求最终交付图片宽 × 高 ≥ 1660 万像素**）** | **`11/18 00:00`（北京时间 · 官方逐字"
           "「即日起至 2026 年 11 月 18 日 00:00（北京时间，结束时刻不含）」）** | 🟠 **生效中（距截止 `5` 天）。"
           " （067 期补入）标准版 `4K` 单张 `0.4522 → 0.2261` 元、极速版 `0.8550 → 0.4275`；"
           "`1K` `0.1430` 与 `2K` `0.1531` **不打折**。 `Runware` 同名促销 `endsAt 2026-11-17`"
           "（`UTC`）＝北京 `11/18 00:00`，双源对齐。** ⚠️ 折的是按张单价、不是额度；"
           "权重虽开放，但许可把欧盟 / 英国 / 韩国 / 美国划为排除地域。 [附录 067](details.html) |")

idx = [k for k, r in enumerate(r41) if "百度 `ERNIE 5.5 Flash Preview` 发布" in name_of(r)]
assert len(idx) == 1, idx
r41.insert(idx[0] + 1, MINIMAX)
EDITED.append("补入 MiniMax H3-Image")

# ------------------------------------------------------------ 4.1：逐行改写
edit("腾讯老混元", "🔴 **腾讯老混元大模型平台停服**",
     "🔴 **必办（已过 `%d` 天，Q04 连续第 `41` 期未决 · 高危窗口第 `32` 天）。 厂商仍只给「9 月底」这一模糊口径，"
     "未给确切停服日。 迁移目标 `TokenHub` 的两个入口本期均未给出新的迁移截止；`hunyuan.tencent.com` 本期仍是 `6,893` 字节的 "
     "`app-skeleton` 骨架屏，六项关键词各 `0` 命中。**" % past("09/30"), r41)

edit("ERNIE 5.5", "🟢 **百度 `ERNIE 5.5 Flash Preview` 发布",
     ("🟢 **生效中（距承诺日 `%d` 天）。 （066 期补入）官方发布页 `限时` / `免费` 各 `0` 命中**；"
      "`11/25 前` 这四个字本期仍在（`11月25日前` `1` 命中）。 **权重尚未放**：`hf-mirror` 的 `?author=baidu` 仍 `39` 个仓库、"
      "`Preview` 仓 `0` 命中；`OpenRouter` 的 `:free` 条目仍在（`1,024,000` 上下文、纯文本）。**") % left("11/25"), r41)

edit("WorkBuddy Hy3", "🟢 **腾讯 WorkBuddy Hy3 限免",
     "🟢 **已过 `%d` 天（`10/31` 到期，官方未给延长口径）。 `Hy4 preview` 夜间限免同批到期 —— "
     "**⚠️ `Hy4-preview` 的权重属于另一条线（`Apache-2.0`、免申请），「限免结束」不等于「权重撤回」。**" % past("10/31"), r41)

edit("Claude Code credit", "🟢 **Claude Code 云会话 credit",
     "🟢 **已过 `%d` 天（`11/5` 到期，官方未给延长口径）。 本报告只记日期，不推断 `credit` 是否仍可领。**" % past("11/05"), r41)

edit("Laya", "🟢 **Laya 决策模型",
     "🟢 **已过 `%d` 天（`10/31` 到期）。 该条自 049 期起未再复核到活动页，保留待查、不销项。**" % past("10/31"), r41)

edit("Runware Kling", "🟢 **`Runware` 分发层 `Kling 4.0`",
     "🟢 **官方促销数组仍保留该条目、但 `endsAt` 已过 `%d` 天 —— 「数组里还在」不等于「活动还在售」（避坑 230）。 "
     "且是 `Runware` 分发层的价格活动、不是厂商侧（快手）的免费政策。**" % past("10/29"), r41)

edit("Runware upscale", "🟢 **`Runware` 分发层 `pruna-p-video-upscale`",
     "🟢 **已过 `%d` 天（`11/8` 到期）。 促销数组 `20 → 20`、新增 `0`、消失 `0`；按 `11/13` 基准仍在售 `5` 条"
     "（`11/15` / `11/17` / `11/19` / `11/30` / `12/31`），**已过期但仍在数组里 `15` 条**。 "
     "「数组里还在 ≠ 在售」第七次实证**（`19` 与 `20` 之争本期定案：`20` 对，见第五章纠错①）。" % past("11/08"), r41)

edit("湖北算力券", "🟢 **湖北算力券年度申领**",
     "🟢 **已过 `%d` 天（`10/31` 到期，官方活动期未延长）。**" % past("10/31"), r41)

edit("WorkBuddy 学生版", "🟢 **WorkBuddy 学生版 1,000 积分",
     "🟢 **已过 `%d` 天（`10/31` 到期）。 两项学生促销同批到期，官方未给延长口径。**" % past("10/31"), r41)

edit("可灵看见微光", "🟢 **可灵「看见微光」",
     "🟢 **已过 `%d` 天（`11/1` 征集截止，官方未给延长口径）。**" % past("11/01"), r41)

edit("MiniMax M3", "🟢 **MiniMax 开放平台 M3 / M2 免费试用**",
     "🟢 **已过 `%d` 天（`11/7` 到期，官方未给延长口径）。 该条仍留在 4.1 —— 归档规则是「过期 >7 天且已收口」，"
     "本期只过 `%d` 天。**" % (past("11/07"), past("11/07")), r41)

edit("火山 Coding", "🟢 **火山 Coding Plan 2.5 折**",
     "🟢 **已过 `%d` 天（`11/8` 到期，官方未给延长口径）。 `Pro` 首购 `49.9` 元为**首月价**，续费按原价。**" % past("11/08"), r41)

edit("腾讯轻量云", "🟢 **腾讯轻量云专家限量",
     "🟢 **今日（`11/13`）为截止日 —— 本期是最后一天。 免费领一个月轻量应用服务器，需实名与专家认证。**", r41)

edit("杭州 Coding", "🟢 **杭州全城 Coding 计划**",
     "🟢 **生效中（距今 `%d` 天）。**" % left("12/09"), r41)

edit("Gemini 3.8", "🟢 **Gemini 3.8 Flash 促销价",
     "🟢 **生效中（距今 `%d` 天）。 ⚠️ 这是付费价而非免费额度。**" % left("12/31"), r41)

edit("TokenHub 新人包", "🟢 **腾讯云 TokenHub 新人免费包",
     "🟢 **生效中（距今 `%d` 天）。 五条同批到 `12/31`，额度各自独立、不可互转。**" % left("12/31"), r41)

edit("TokenHub 国际站", "🟢 **腾讯云 TokenHub 国际站促销",
     "🟢 **已过 `%d` 天（`10/30 12:00` 北京到期）。 ⚠️ 国际站与国内 WorkBuddy / 国内 TokenHub 的限免是两条线，不可混算。**" % past("10/30"), r41)

edit("智谱清言", "🟢 **智谱清言「双节消耗积分",
     "🟢 **已过 `%d` 天（`10/31` 为领取窗口末日）。 返还是「消耗积分」，不是「送积分」。**" % past("10/31"), r41)

edit("Nano Banana", "🟢 **Google Nano Banana 2 停用",
     "🟢 **已过 `%d` 天（停用日 `10/29`）。 官方未公布具体停机时刻，故本报告不写「已停用」。**" % past("10/29"), r41)

edit("Anthropic 使用政策", "🟢 **Anthropic 新版使用政策",
     "🟢 **昨日（`11/12`）生效 —— 本期是生效后第 `1` 天。 ⚠️ 官方明确：普通反驳、表达不满、研究测试、"
     "暗黑题材创作都不在禁止范围。**", r41)

edit("火山方舟 Agent Plan", "🟢 **火山方舟 Agent Plan 个人版",
     "🟢 **已过 `%d` 天（`11/8` 到期）。 「数据调用次数」不是「模型 token」—— 两类额度不能相加。**" % past("11/08"), r41)

edit("HeyGen", "🟢 **HeyGen Voice",
     "🟢 **已过 `%d` 天（官方促销期至 `10/31`）。 ⚠️ 榜首为单一榜单口径（避坑 116）。**" % past("10/31"), r41)

edit("Gemini 4 Argon", "🟠 **Google `Gemini 4 Argon`",
     "🟠 **`GA` 已生效、首发优惠价倒计时中（距今 `%d` 天）。 ⚠️ `87%%` 是单一基准、纯推理口径、官方自披露（避坑 116）。**"
     % left("11/30"), r41)

edit("腾讯元器", "🔴 **腾讯智能体平台「元器」停止服务",
     "🔴 **停服日（`11/9`）截至本期基准日已满 `%d` 天。 三个日期继续分开排**：`10/29` 已停止新建、**`11/9` 停止服务**、"
     "`2027-01-09` 数据导出截止。 **本报告只报日期，不报「已停 / 未停」**。**" % past("11/09"), r41)

edit("Google AI Plus", "🟠 **Google AI Plus 失去 Pro 模型选择权",
     "🟠 **今日（`11/13`）为截止日。 ⚠️ 官方支持文档此前写 `10/9`、邮件改口 `11/13`，两次日期差未说明原因。**", r41)

edit("DeepSeek Search", "🟡 **`DeepSeek Search` / `Fetch`",
     "🟡 **已过 `%d` 天（免费窗口至 `11/1 00:00`）。 ⚠️ 「开源框架不改变 API 价格」这条既有结论不变："
     "`DeepInfer` 与官方 API 计费是两本账。**" % past("11/01"), r41)

edit("WorkBuddy Intl", "🟢 **`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017`",
     "🟢 **已过 `%d` 天（官方限免期至 `10/31` · 工作区自有产品线）。**" % past("10/31"), r41)

edit("MiniMax 退役", "⚠️ **MiniMax `M2.5` / `M2.7` 系列退役",
     "⚠️ **分两个节点、不是一天，距今 `%d` 天。 ⚠️「自动改路由」对做对比测试的人是陷阱："
     "你以为在测 `M2.7`，实际测的是 `M3.1 Flash Preview`（避坑 186）。**" % left("11/18"), r41)

edit("天猫 AI 空间站", "🟡 **天猫「AI 空间站」Token 充值中心",
     "🟡 **生效中（已开卖 · 价保至 `11/28 23:59`，距今 `%d` 天）。 双 11 当天五家厂商在天猫会场打折（见 066 期第二章），"
     "**折的是付费卡、不是免费额度**。**" % left("11/28"), r41)

edit("AutoClaw 国内 M10W4", "🟢 **智谱 `AutoClaw` 国内站 `M10W4`",
     "🟢 **已过 `%d` 天（活动期 `10/26–11/1`）。 一周一档，官方未见新档公告。**" % past("11/01"), r41)

edit("Kimi K3.1 Pro 发布", "🟢 **`Moonshot` `Kimi K3.1 Pro` 发布",
     "🟢 **已兑现（权重 `11/2` 建仓、`gated: false`、`downloads 37,486` / `likes 1,991`）。 `license` 逐条读过："
     "默认免费商用，另有 `MaaS` 年营收 `$20M` 与「月活 `1` 亿 / 月营收 `$20M`」两条门槛。**", r41)

edit("K2 停新", "🔴 **`Moonshot` `K2` 系列",
     "🔴 **已过 `%d` 天（`10/31` 停止向新注册用户开放）；`12` 月底计划下线，官方未给确切日**。 迁移口径见附录。**" % past("10/31"), r41)

edit("AutoClaw 国际 M10W4", "🟢 **智谱 `AutoClaw` 国际站 `M10W4`",
     "🟢 **已过 `%d` 天（活动期 `10/26–11/1`，`UTC+8`）。 国际站与国内站两套积分不可互转。**" % past("11/01"), r41)

edit("Figma", "🟢 **Figma `Code Layers`",
     "🟢 **已过 `%d` 天（`11/4` 到期）。 已超出 `7` 天宽限期；因状态列未写收口口径，按纪律仍留在 4.1、不归档。**" % past("11/04"), r41)

edit("Runware edit", "🟢 **`Runware` 分发层 `pruna-p-video-edit`",
     "🟢 **已过 `%d` 天（官方 `endsAt 2026-11-03`）。 ⚠️ 这是 `Runware` 分发层的价格活动、不是厂商侧（`Pruna`）的免费政策。**" % past("11/03"), r41)

edit("国家超算", "🟠 **`国家超算互联网` 夜间限时免费调用",
     "🟠 **已过 `%d` 天（官方逐字 `10月21日至10月30日`）。 本期页面 `132,924` 字节、四项关键词仍零命中 —— "
     "连续第 `17` 期未复核到活动页留痕。**" % past("10/30"), r41)

edit("AutoClaw 国际 M11W1", "🟢 **智谱 `AutoClaw` 国际站 `M11W1`",
     "🟢 **已过 `%d` 天（`11/8 23:59` 到期）。 国际站博客页本期未再取到（`000`）。 活动结束后页面不留痕。**" % past("11/08"), r41)

edit("AutoClaw 国内 M11W1", "🟢 **智谱 `AutoClaw` 国内站 `M11W1`",
     "🟢 **已过 `%d` 天（`11/8 23:59` 到期）。 国内站页本期未取（`000`）。 活动结束后页面不留痕。**" % past("11/08"), r41)

edit("Ollie 关停", "⚠️ **`Ollie`（隐私向 AI 助手）宣布关停",
     "⚠️ **停服日已过 `%d` 天（`11/6` 起）。 告别信三页本期仍 `md5` 全 SAME 在线**（`39,747` / `41,791` / `107,182`）；"
     "**页面在线不等于服务在线**，官方无逐字口径。**" % past("11/06"), r41)

edit("Ollie Free", "⚠️ **`Ollie` 的 `Free` 档",
     "⚠️ **停服日已过 `%d` 天。 定价页 `41,791` 字节八期同值**，`50 messages … per month` 逐字仍在；"
     "**`Free` 档是否一并停服仍无官方口径。**" % past("11/06"), r41)

edit("虎鲸文娱", "🟢 **虎鲸文娱「鲸锐 AI 创作大赛」",
     "🟢 **生效中（距截止 `%d` 天）。 ⚠️（063 期新登记 · 媒体口径）** 总奖金池 `1000` 万元、`265` 个获奖名额、"
     "单项最高 `200` 万元。 **官方报名页本期仍未核到**。**" % left("11/22"), r41)

edit("Claude Fable 5.2", "🟢 **Anthropic `Claude Fable 5.2`",
     "🟢 **生效中（距第一个截止 `%d` 天）。 定价页对比表里 `Fable` × `Free` 连续第三期是逐字 `No`**；"
     "`Sheets` / `Whiteboards` 两行 `Free` 也是 `No`；**`Claude Meetings` 已上线但仍未进表（只给 `Team` / `Enterprise` beta）。**"
     % left("11/16"), r41)

# ------------------------------------------------------------ 4.2：补入 2 行
G4H = ("| 🟢 **`Gemini 4 Hydrogen` 对免费用户开放（**官方逐字 `free users will get access ... via auto model selection` · "
       "`$1.50` / `$7.50` 每百万 · `1M` 上下文**）** | **无结束日（产品能力，非活动；官方未给任何期限）** | "
       "🟢 **生效中（067 期补入 · `blog.google` 一手）。 免费路径只有两条：`Gemini` 应用（**自动选模，下拉里点不到**）与 "
       "`Google Search`（全部用户）。** ⚠️ 无额度、无次数、无开关；`Antigravity` 里只给付费 `AI Pro` / `Ultra`。 "
       "[附录 067](details.html) |")

INK = ("| 🟢 **`thinkingmachines/Inkling-2-Small` 开放权重（**`Apache-2.0` · `gated: false` · `36` 个文件 / `24` 个分片 · "
       "`image-text-to-text` · 通用多模态**）** | **无结束日（`Apache-2.0` 开放权重，无活动期）** | "
       "🟢 **已开放权重（第 ④ 级已到 · 067 期补入 · `HF` 单仓端点一手）。 `downloads 12` / `likes 166`**（相差 `13` 倍，"
       "是「刚公开、还没被拉」的形状）；建仓 `11/04`、`lastModified` `11/13 03:42 UTC`、**本期才进 `?author=` 公开列表**。 "
       "[附录 067](details.html) |")

r42.append(G4H)
r42.append(INK)
EDITED.append("补入 Gemini 4 Hydrogen")
EDITED.append("补入 Inkling-2-Small")

# ------------------------------------------------------------ 4.2：逐行改写
edit("OpenRouter 免费档", "🟢 **OpenRouter 免费档",
     "🟢 **生效中（动态目录）。 （067 期）`467 → 472`、零价 `16 → 17`、`:free` `13 → 14`；`5` 进 `0` 出，"
     "进 `gemini-4-hydrogen`（含 `:batch`）、`kimi-k3.1-pro:batch`、`inkling-2-small`、`particle-1:free`。** "
     "**`particle-1:free` 与付费 `particle-1` 并排存在、`created` 相同 —— 是「并排多开」不是「换档」（避坑 289 第二种形态）。**", r42)

edit("OpenCode 清单", "🟡 **`OpenCode` 免费模型清单",
     "🟡 **生效中（清单动态）。 （067 期）三套口径 `13/13/13` 连续第 `4` 期不变**，但整页 `md5` 变了"
     "（`91,792 → 98,175` 字节）：**新增 `gemini-4-hydrogen` 一行（`$1.50` / `$7.50`，全站唯一不带 `(50% off)` 的）**；"
     "`tml-free` 仍是条款 `PDF` 文件名子串、不计入。", r42)

edit("豆包工作", "🟢 **豆包工作 30 天订阅",
     "🟢 **生效中（早期登记）。 （067 期）两页继续分裂**：`doubao-work` `169,757` 字节（`+127`）；`doubao.com/work` "
     "`58,748`（`+269`），`免费` / `30 天` / `订阅` / `额度` **四项仍各 `0` 命中 —— 连续第 `23` 期无一手。**", r42)

edit("商汤 Token Plan", "🟢 **商汤 `日日新 SenseNova` Token Plan",
     "🟢 **生效中。 （067 期）`20,820` 字节、`md5` 同值 —— 连续第 `11` 期逐字节相同**，`公测期完全免费开放` / `限时放量` / "
     "`¥ 0` 各 `1` 次，**`截止` 仍 `0` 命中。**", r42)

edit("小浣熊免费版", "🟢 **商汤 `小浣熊`（Raccoon）免费版",
     "🟢 **生效中。 （067 期）页面 `188,107` 字节与上期相同、`md5` 不同 —— 同页两个会员价并存**：卡片 `¥11.11`（兑换码）、"
     "对比表 `¥29.9`（标准价）。 免费版 `¥0 / 永久` + `300` 积分/日 逐字仍在。 **折扣折的是会员，免费版一个字没动。**", r42)

edit("商汤 6.8", "⚠️ **商汤 `SenseNova 6.8 Flash` 上线",
     "⚠️ **生效中（口径）。 （067 期）`sensetime.com/cn/news` `111,103 → 111,247` 字节（`+144`）**，"
     "`SenseNova 6.8` 命中 `8` 次；**`限时` 与 `免费` 仍各 `0` 命中 —— 连续第 `11` 期只有媒体口径。**", r42)

edit("ERNIE Base", "🟢 **百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **生效中。 （067 期第 `7` 次复核）`FP8` `downloads 2,551 → 2,963`（`+412`）、`likes 282 → 299`；"
     "`BF16` `891 → 1,021`（`+130`）、`likes 389 → 390`。 **`LICENSE` 仍恰为 `25,619` 字节（第 `8` 天）**、"
     "两仓 `lastModified` 仍停在 `11/05`。", r42)

edit("Ripple", "🟢 **`Ripple-65B Preview` 开放权重",
     "🟢 **生效中。 （067 期）主仓 `downloads 7,112 → 7,667`（`+555`）、`likes 518 → 544`**；`lastModified` 仍停在 "
     "`2026-11-10T09:31:23Z`（**第 `3` 期未动**）。 **⚠️ `?author=` 列表端点本期 `503`，三个变体仓一个数都不报（避坑 290）。**", r42)

edit("AXON", "🟢 **`AXON Developer Edition`",
     "🟢 **生效中。 （067 期）`20,111` 字节与 `md5` 均同值 —— 连续第 `10` 期无许可证与版本号**，仍标 `Free forever`。", r42)

edit("Token 羊毛", "🟡 **`AIHOT` 的「Token 羊毛」",
     "🟡 **生效中（第三方聚合，非厂商一手）。 （067 期连续第 `5` 期实测）页头「今天还能领 ¥598」持平**、"
     "**「卡册 57 张」**（`56 → 57`）、核实标注正文口径 **`118` 处**（`116 → 118`）；**`11/12` 定格在 `80` 条、"
     "`11/13` 已核 `12` 条**（066 期看到的「当天 `4` 条」是进行值，见第五章纠错②）。", r42)

edit("AMD", "⚠️ **`AMD` `Radeon Token Factory`",
     "⚠️ **生效中（线索，额度仍未确认）。 （067 期第 `5` 期）官方页 `200` / `147,147` 字节（`−54,484`）**，"
     "`Loading` `35` 处，`Free` / `免费` / `quota` / `Daily` / `USD` **各 `0` 命中**。 三份来源冲突未解。", r42)

edit("Antigravity 个人免费档", "🟢 **`Google Antigravity` 个人免费档",
     "🟢 **生效中（官方定价页逐字，066 期口径）。 （067 期）`pricing` / `models` / `docs/models` / 首页四个 `URL` 全部 `000`** —— "
     "**整站不可达第 `2` 期，不是路径错**；`$0/month` 等逐字沿用 `142,604` 字节那一期的读数。 "
     "**⚠️ 同日官方宣布 `Gemini 4 Hydrogen` 在 `Antigravity` 里只给付费 `AI Pro` / `Ultra`** —— 免费档还在，新模型不在免费档里。", r42)

edit("Claude 工作台", "🟢 **`Anthropic` 把 `Claude` 扩成工作台",
     "🟢 **生效中（官方定价页一手）。 （067 期连续第 `3` 期）`1,344,061` 字节（与上两期同字节、`md5` 第三次不同）**，"
     "`Claude Sheets (beta)` / `Claude Whiteboards (beta)` 两行 `Free` 列**仍是逐字 `No`**，`Fable` × `Free` 也是 `No`；"
     "**`Claude Meetings` 整页 `0` 命中 —— 它上线了（只给 `Team` / `Enterprise` beta），仍没有变成第三行。**", r42)

edit("小浣熊双十一", "🟡 **商汤 `小浣熊`「双十一限时特惠」",
     "🟡 **生效中（第 `3` 天，未回落）。 （067 期）卡片 `¥11.11`（兑换码）、原价 `¥48.0` 逐字仍在，同时对比表里 "
     "`¥29.9 / 月` 也在** —— **同一页两个价，不是价格变了**；页面仍未给截止时点，本报告不推断几点结束。", r42)

edit("Seedream", "🟢 **豆包 `Seedream 5.0`「输入图免费",
     "🟢 **生效中（066 期补入 · 火山引擎计费文档一手）。 （067 期）文档 `1,742,699 → 1,771,134` 字节（`+28,435`），"
     "两行与两个「免费」格子逐字未变**：`flash` 输入图 `免费` / 输出 `0.12`；`pro` 输入图 `首张免费` / 第 `2` 张起 `0.02`。 "
     "⚠️「免费」是输入图、不是生成；按张计价、无每日额度。", r42)

print("改写/补入：", len(EDITED), "处")

# ------------------------------------------------------------ 回写
assert len(r41) == 58, len(r41)
assert len(r42) == 35, len(r42)
for r in r41 + r42:
    assert len(r.strip().rstrip("|").split("|")) == 4, ("字段数", r[:40])

head41 = "| 活动 | 截止 | 状态 |\n| --- | --- | --- |\n" + "\n".join(r41) + "\n"
head42 = "| 活动 | 截止 | 状态 |\n| --- | --- | --- |\n" + "\n".join(r42) + "\n"

i = md.index("### 4.1 限时动作")
j = md.index("### 4.2 常驻权益本期变更")
k = md.index("### ④ 本期第四章脚注")

new = (md[:i]
       + "### 4.1 限时动作（有确切截止日 · 58 条）\n\n" + head41 + "\n"
       + "### 4.2 常驻权益本期变更（无截止日 · 本期有变化 35 条）\n\n" + head42 + "\n"
       + md[k:])
io.open(MD, "w", encoding="utf-8", newline="\n").write(new)

disk = io.open(MD, encoding="utf-8").read()
assert "（有确切截止日 · 58 条）" in disk
assert "（无截止日 · 本期有变化 35 条）" in disk
assert "MiniMax `H3-Image` `4K` 生图限时" in disk
assert "`Gemini 4 Hydrogen` 对免费用户开放" in disk
assert "`thinkingmachines/Inkling-2-Small` 开放权重" in disk
assert disk.count("067 期补入") == 3, disk.count("067 期补入")
print("table written | 4.1=%d 4.2=%d | bytes %d" % (len(r41), len(r42), len(disk.encode())))
print("字段数分布 4.1:", Counter(len(r.strip().rstrip("|").split("|")) for r in r41))
print("字段数分布 4.2:", Counter(len(r.strip().rstrip("|").split("|")) for r in r42))
