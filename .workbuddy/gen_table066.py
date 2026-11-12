# -*- coding: utf-8 -*-
"""066 期：在 065 期现行 4.1/4.2 表体上做行级改写 + 移出归档 1 行 + 补入 3 行。

纪律（055–065 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；
  ③ 断言用逐字短语；④ 全表字段数分布断言；⑤ 补入行必须带「066 期」标记；
  ⑥ 状态列整体替换；⑦ 单元格不许出现 `|`；⑧ 天数一律由基准日实算。
"""
import io
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第066期-2026-11-12.md"
PTR = " [附录 066](details.html) |"
TODAY = date(2026, 11, 12)

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")


def rows_of(text, start, end):
    i = text.index(start)
    j = text.index(end)
    return [l for l in text[i:j].split("\n")
            if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]


r41 = rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
r42 = rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("输入行数：4.1 = %d，4.2 = %d" % (len(r41), len(r42)))
assert len(r41) == 57, ("065 期 4.1 行数", len(r41))
assert len(r42) == 31, ("065 期 4.2 行数", len(r42))


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


# ------------------------------------------------------------------ 归档
ARCH = [r for r in r41 if "AutoClaw" in name_of(r) and "第二期" in name_of(r)]
assert len(ARCH) == 1, len(ARCH)
r41.remove(ARCH[0])
print("移出归档 1 行：智谱 AutoClaw 第二期")

# ------------------------------------------------------------------ 4.1 改写
edit("腾讯老混元", "🔴 **腾讯老混元大模型平台停服**",
     "🔴 **必办（已过 `%d` 天，Q04 连续第 `40` 期未决 · 高危窗口第 `31` 天）。 厂商仍只给「9 月底」这一模糊口径，"
     "未给确切停服日。 迁移目标 `TokenHub` 的两个入口本期均未给出新的迁移截止。**" % past("09/30"), r41)

edit("WorkBuddy Hy3", "🟢 **腾讯 WorkBuddy Hy3 限免",
     "🟢 **已过 `%d` 天（`10/31` 到期，官方未给延长口径）。 050 期实访的限免口径到 `10/31` 为止，本期未见续期公告；"
     "`Hy4 preview` 夜间限免同批到期 —— **⚠️ 但 `Hy4-preview` 的权重属于另一条线（`Apache-2.0`、免申请），"
     "「限免结束」不等于「权重撤回」。**" % past("10/31"), r41)

edit("Claude Code credit", "🟢 **Claude Code 云会话 credit",
     "🟢 **已过 `%d` 天（`11/5` 到期，官方未给延长口径）。 本报告只记日期，不推断 `credit` 是否仍可领。**" % past("11/05"), r41)

edit("Laya", "🟢 **Laya 决策模型",
     "🟢 **已过 `%d` 天（`10/31` 到期）。 该条自 049 期起未再复核到活动页，保留待查、不销项。**" % past("10/31"), r41)

edit("Runware Kling", "🟢 **`Runware` 分发层 `Kling 4.0`",
     "🟢 **官方促销数组仍保留该条目、但 `endsAt` 已过 `%d` 天 —— 「数组里还在」不等于「活动还在售」（避坑 230）。 "
     "且是 `Runware` 分发层的价格活动、不是厂商侧（快手）的免费政策（多站点口径要拆开写）。**" % past("10/29"), r41)

edit("Runware upscale", "🟢 **`Runware` 分发层 `pruna-p-video-upscale`",
     "🟢 **已过 `%d` 天（`11/8` 到期）。 促销数组本期 `19 → 19`、新增 `0`、消失 `0`、`endsAt` 变化 `0`；"
     "按 `11/12` 基准仍在售 `4` 条（`11/15` / `11/19` / `11/30` / `12/31`），**已过期但仍在数组里 `15` 条**。 "
     "「数组里还在 ≠ 在售」第六次实证**（本期并纠正上一期「`19 → 20`」的误报，见第五章纠错③）。" % past("11/08"), r41)

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
     "🟢 **生效中（距今 `%d` 天）。 免费领一个月轻量应用服务器，需实名与专家认证。**" % left("11/13"), r41)

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
     "🟢 **今日（`11/12`）生效 —— 本期是生效日当天。 ⚠️ 官方明确：普通反驳、表达不满、研究测试、暗黑题材创作都不在禁止范围。**", r41)

edit("火山方舟 Agent Plan", "🟢 **火山方舟 Agent Plan 个人版",
     "🟢 **已过 `%d` 天（`11/8` 到期）。 「数据调用次数」不是「模型 token」—— 两类额度不能相加。**" % past("11/08"), r41)

edit("HeyGen", "🟢 **HeyGen Voice",
     "🟢 **已过 `%d` 天（官方促销期至 `10/31`）。 ⚠️ 榜首为单一榜单口径（避坑 116）。**" % past("10/31"), r41)

edit("Gemini 4 Argon", "🟠 **Google `Gemini 4 Argon`",
     "🟠 **`GA` 已生效、首发优惠价倒计时中（距今 `%d` 天）。 ⚠️ `87%%` 是单一基准、纯推理口径、官方自披露（避坑 116）。**" % left("11/30"), r41)

edit("腾讯元器", "🔴 **腾讯智能体平台「元器」停止服务",
     "🔴 **停服日（`11/9`）截至本期基准日已满 `%d` 天。 三个日期继续分开排**：`10/29` 已停止新建、**`11/9` 停止服务**、"
     "`2027-01-09` 数据导出截止。 **本报告只报日期，不报「已停 / 未停」**。**" % past("11/09"), r41)

edit("Google AI Plus", "🟠 **Google AI Plus 失去 Pro 模型选择权",
     "🟠 **倒计时中（距今 `%d` 天）。 ⚠️ 官方支持文档此前写 `10/9`、邮件改口 `11/13`，两次日期差未说明原因。**" % left("11/13"), r41)

edit("DeepSeek Search", "🟡 **`DeepSeek Search` / `Fetch`",
     "🟡 **已过 `%d` 天（免费窗口至 `11/1 00:00`）。 ⚠️ 「开源框架不改变 API 价格」这条既有结论不变："
     "`DeepInfer` 与官方 API 计费是两本账。**" % past("11/01"), r41)

edit("WorkBuddy Intl", "🟢 **`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017`",
     "🟢 **已过 `%d` 天（官方限免期至 `10/31` · 工作区自有产品线）。**" % past("10/31"), r41)

edit("MiniMax 退役", "⚠️ **MiniMax `M2.5` / `M2.7` 系列退役",
     "⚠️ **分两个节点、不是一天，距今 `%d` 天。 ⚠️「自动改路由」对做对比测试的人是陷阱："
     "你以为在测 `M2.7`，实际测的是 `M3.1 Flash Preview`（避坑 186）。**" % left("11/18"), r41)

edit("天猫 AI 空间站", "🟡 **天猫「AI 空间站」Token 充值中心",
     "🟡 **生效中（已开卖 · 价保至 `11/28 23:59`，距今 `%d` 天）。 双 11 当天五家厂商在天猫会场打折（见第二章第 3 条），"
     "**折的是付费卡、不是免费额度**。**" % left("11/28"), r41)

edit("AutoClaw 国内 M10W4", "🟢 **智谱 `AutoClaw` 国内站 `M10W4`",
     "🟢 **已过 `%d` 天（活动期 `10/26–11/1`）。 一周一档，官方未见新档公告。**" % past("11/01"), r41)

edit("Kimi K3.1 Pro 发布", "🟢 **`Moonshot` `Kimi K3.1 Pro` 发布",
     "🟢 **已兑现（权重 `11/2` 建仓、`gated: false`、`downloads 33,617`）。 本期把 `license` 逐条读完：默认免费商用，"
     "另有 `MaaS` 年营收 `$20M` 与「月活 `1` 亿 / 月营收 `$20M`」两条门槛（见第三章第 5 条）。**", r41)

edit("K2 停新", "🔴 **`Moonshot` `K2` 系列",
     "🔴 **已过 `%d` 天（`10/31` 停止向新注册用户开放）；`12` 月底计划下线，官方未给确切日**。 迁移口径见附录。**" % past("10/31"), r41)

edit("AutoClaw 国际 M10W4", "🟢 **智谱 `AutoClaw` 国际站 `M10W4`",
     "🟢 **已过 `%d` 天（活动期 `10/26–11/1`，`UTC+8`）。 国际站与国内站两套积分不可互转。**" % past("11/01"), r41)

edit("Figma", "🟢 **Figma `Code Layers`",
     "🟢 **已过 `%d` 天（`11/4` 到期）。 已超出 `7` 天宽限期，下期按规则归档。**" % past("11/04"), r41)

edit("Runware edit", "🟢 **`Runware` 分发层 `pruna-p-video-edit`",
     "🟢 **已过 `%d` 天（官方 `endsAt 2026-11-03`）。 ⚠️ 这是 `Runware` 分发层的价格活动、不是厂商侧（`Pruna`）的免费政策。**" % past("11/03"), r41)

edit("国家超算", "🟠 **`国家超算互联网` 夜间限时免费调用",
     "🟠 **已过 `%d` 天（官方逐字 `10月21日至10月30日`）。 本期页面 `132,924` 字节、四项关键词仍零命中 —— "
     "连续第 `16` 期未复核到活动页留痕。**" % past("10/30"), r41)

edit("AutoClaw 国际 M11W1", "🟢 **智谱 `AutoClaw` 国际站 `M11W1`",
     "🟢 **已过 `%d` 天（`11/8 23:59` 到期）。 国际站博客页本期未再取到（`000`）。 活动结束后页面不留痕。**" % past("11/08"), r41)

edit("AutoClaw 国内 M11W1", "🟢 **智谱 `AutoClaw` 国内站 `M11W1`",
     "🟢 **已过 `%d` 天（`11/8 23:59` 到期）。 国内站页本期未取（`000`）。 活动结束后页面不留痕。**" % past("11/08"), r41)

edit("Ollie 关停", "⚠️ **`Ollie`（隐私向 AI 助手）宣布关停",
     "⚠️ **停服日已过 `%d` 天（`11/6` 起）。 告别信三页本期仍 `md5` 全 SAME 在线**（`39,747` / `41,791` / `107,182`）；"
     "**页面在线不等于服务在线**，官方无逐字口径。**" % past("11/06"), r41)

edit("Ollie Free", "⚠️ **`Ollie` 的 `Free` 档",
     "⚠️ **停服日已过 `%d` 天。 定价页 `41,791` 字节七期同值**，`50 messages … per month` 逐字仍在；"
     "**`Free` 档是否一并停服仍无官方口径。**" % past("11/06"), r41)

edit("鲸锐", "🟢 **虎鲸文娱「鲸锐 AI 创作大赛」",
     "🟢 **生效中（距截止 `%d` 天）。 ⚠️（063 期新登记 · 媒体口径）** 总奖金池 `1000` 万元、`265` 个获奖名额、"
     "单项最高 `200` 万元。 **官方报名页本期仍未核到**。**" % left("11/22"), r41)

edit("Fable 5.2", "🟢 **Anthropic `Claude Fable 5.2`",
     "🟢 **生效中（距第一个截止 `%d` 天）。 定价页对比表里 `Fable` × `Free` 连续第二期是逐字 `No`**；"
     "`Sheets` / `Whiteboards` 两行 `Free` 也是 `No`，`Claude Meetings` 仍未进表。**" % left("11/16"), r41)

# ------------------------------------------------------------------ 4.1 补入
NEW41 = ("| 🟢 **百度 `ERNIE 5.5 Flash Preview` 发布（**`280B` 总参 / `14B` 激活 / `1M` 上下文 · "
         "官方逐字「权重将于 `11月25日前` 开源」· 同日在 `OpenRouter` 出现 `:free` 零价条目**）** | "
         "**`11/25` 前（官方逐字 `权重将于11月25日前开源` —— 是「前」不是「当天」；媒体统一写成 `11月25日`）** | "
         "🟢 **生效中（距承诺日 `" + str(left("11/25")) + "` 天）。 （066 期补入）官方发布页 `限时` / `免费` 各 `0` 命中**；"
         "千帆侧「输入忙时 `2` 元 / 闲时 `1` 元、输出忙时 `8` 元 / 闲时 `4` 元、限时五折」**只有媒体口径**"
         "（三家转述一致，千帆计费文档里该模型 `0` 命中）。 **`OpenRouter` 的 `:free` 条目 `context_length 1,024,000`、"
         "纯文本、输入输出全 `0`。**" + PTR)
r41.insert(1, NEW41)
EDITED.append("文心 5.5 Flash Preview（补入）")

# ------------------------------------------------------------------ 4.2 指针与改写
for k, r in enumerate(r42):
    if " [附录 065](details.html) |" in r:
        r42[k] = r.replace(" [附录 065](details.html) |", PTR)

edit("OpenRouter 免费档", "🟢 **OpenRouter 免费档",
     "🟢 **生效中（动态目录）。 （066 期）`469 → 467`（`−2`）、零价 `15 → 16`、`:free` `12 → 13`、`?max_price=0` `14 → 15`；"
     "**`2` 进 `4` 出**：进 `baidu/ernie-5.5-flash-preview:free`、`unbiased/pareto-26.10-preview`；"
     "出付费 `baidu/ernie-5.5-flash-preview` 与 `bytedance-seed` 三条。**「条数净增」来自一次 `SKU` 迁移，不是新模型（避坑 289）。**", r42)

edit("OpenCode", "🟡 **`OpenCode` 免费模型清单",
     "🟡 **生效中（清单动态）。 （066 期）三套口径 `13/13/13` 连续第 `3` 期不变，整页 `md5` 逐字节相同**"
     "（`91,792` 字节）；`-free` 后缀 `13` 个 `ID`，`tml-free` 仍是条款 `PDF` 文件名子串、不计入。", r42)

edit("小浣熊免费版", "🟢 **商汤 `小浣熊`（Raccoon）免费版",
     "🟢 **生效中。 （066 期）页面 `188,107` 字节与 `md5` 均与上一期相同 —— 双十一价第 `2` 天未回落**，"
     "`免费版` `2` / `¥ 0` `2` / `/永久` `2` / `300` 积分/日逐字仍在。 **折扣折的是会员，免费版一个字没动。**", r42)

edit("小浣熊双十一", "🟡 **商汤 `小浣熊`「双十一限时特惠」",
     "🟡 **生效中（第 `2` 天，未回落）。 （066 期）`¥29.9 → ¥11.11`、原价 `¥48.0` 逐字仍在**，页面 `md5` 同值；"
     "**页面仍未给截止时点，本报告不推断几点结束。**", r42)

edit("Token 羊毛", "🟡 **`AIHOT` 的「Token 羊毛」",
     "🟡 **生效中（第三方聚合，非厂商一手）。 （066 期连续第 `4` 期实测）页头「今天还能领 ¥598」**（`599 → 598`，"
     "**首次下降**）、**「卡册 56 张」**（`54 → 56`）、核实标注正文口径 **`116` 处**（`112 → 116`）；"
     "**但 `11/12` 当天只新增 `4` 条核实、`11/11` 的 `94` 条一条没重核**。", r42)

edit("Ripple", "🟢 **`Ripple-65B Preview` 开放权重",
     "🟢 **生效中。 （066 期）主仓 `downloads 6,480 → 7,112`（`+632`）、`likes 490 → 518`**；"
     "`lastModified` 仍停在 `2026-11-10T09:31:23Z`（**第 `2` 期未动**）。 **⚠️ 三个变体仓本期不报数 —— "
     "列表端点有缓存滞后（避坑 290）。**", r42)

edit("ERNIE", "🟢 **百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **生效中。 （066 期第 `6` 次复核）`FP8` `downloads 2,111 → 2,551`（`+440`）、`likes 252 → 282`；"
     "`BF16` `755 → 891`（`+136`）、`likes 387 → 389`。 **`LICENSE` 仍恰为 `25,619` 字节（第 `7` 天）**、"
     "两仓 `lastModified` 仍停在 `11/05`。", r42)

edit("AXON", "🟢 **`AXON Developer Edition`",
     "🟢 **生效中。 （066 期）`20,111` 字节与 `md5` 均同值 —— 连续第 `9` 期无许可证与版本号**，仍标 `Free forever`。", r42)

edit("商汤 Token Plan", "🟢 **商汤 `日日新 SenseNova` Token Plan",
     "🟢 **生效中。 （066 期）`20,820` 字节、`md5` 同值 —— 连续第 `10` 期逐字节相同**，"
     "`公测期完全免费开放` / `限时放量` / `¥ 0` 各 `1` 次，**`截止` 仍 `0` 命中。**", r42)

edit("商汤 6.8", "⚠️ **商汤 `SenseNova 6.8 Flash` 上线",
     "⚠️ **生效中（口径）。 （066 期）`sensetime.com/cn/news` `111,705 → 111,103` 字节（`−602`）**，"
     "`SenseNova 6.8` 命中 `2` 次仍在；**`限时` 与 `免费` 仍各 `0` 命中 —— 连续第 `10` 期只有媒体口径。**", r42)

edit("AMD", "⚠️ **`AMD` `Radeon Token Factory`",
     "⚠️ **生效中（线索，额度仍未确认）。 （066 期第 `4` 期）官方页 `200` / `201,631` 字节（`+1,059`，壳未变）**，"
     "正文仍是 `Loading Radeon Cloud…`，`Free` / `免费` / `quota` / `Daily` / `USD` **各 `0` 命中**。 三份来源冲突未解。", r42)

edit("Antigravity 免费档", "🟢 **`Google Antigravity` 个人免费档",
     "🟢 **生效中（官方定价页逐字，上一期口径）。 （066 期）`pricing` / `models` / `docs/models` / 首页四个 `URL` 全部 `000`**"
     " —— **站点级不可达，不是路径错**；`$0/month` 等逐字沿用上一期（`142,604` 字节）的读数。", r42)

edit("豆包工作", "🟢 **豆包工作 30 天订阅",
     "🟢 **生效中（早期登记）。 第三方整理口径，以客户端订阅页为准。 （066 期）两页继续分裂**："
     "`doubao-work` `169,630` 字节同、`md5` 不同（第 `3` 次）；`doubao.com/work` `57,784 → 58,479`，"
     "`免费` / `30 天` / `订阅` / `额度` **四项仍各 `0` 命中 —— 连续第 `22` 期无一手。**", r42)

edit("Claude 工作台", "🟢 **`Anthropic` 把 `Claude` 扩成工作台",
     "🟢 **生效中（官方定价页一手）。 （066 期连续第 `2` 期）`1,344,061` 字节（与上一期同字节、`md5` 不同）**，"
     "`Claude Sheets (beta)` / `Claude Whiteboards (beta)` 两行 `Free` 列**仍是逐字 `No`**，`Fable` × `Free` 也是 `No`；"
     "**`Claude Meetings` 在整页 `0` 命中 —— 上线后没有变成第三行。**", r42)

edit("Xing4.0", "🟡 **中国电信 `Xing4.0-29B-A4B`",
     "⚪ **已从 `OpenRouter` 目录下架（第 `2` 期未回归）。 （066 期）`?search=xingchen` 与全量 `ID` 逐条比对，"
     "`xingchen-agi` 仍 `0` 命中**；厂商侧仍无说明。 **⚠️ 本期发现 `OpenRouter` 的 `?search=` 参数不生效（`search=xingchen` 也返回全量 `842,603` 字节），"
     "下期起改用全量 `ID` 过滤。**", r42)

# ------------------------------------------------------------------ 4.2 补入
NEW42 = [
    ("| 🟢 **`OpenAI` 退伍军人 / 现役军人一年 `ChatGPT Plus` 免费（**官方逐字 `a year of ChatGPT Plus at no cost` · "
     "`Veterans Day` `2026-11-11` 发布 · 累计 `20,000` 人已领**）** | **未公布（官方页无申请截止日、无名额上限表述）** | "
     "🟢 **生效中（066 期补入 · 官方页一手）。 页面逐字「more than `20,000` ... have claimed a year of ChatGPT Plus at no cost」，"
     "文末入口「See if you're eligible for a free year of ChatGPT Plus」**；**资格细则不在本页，本报告不转述未读到的条款**。"
     " **⚠️ `20,000` 是累计口径，不是剩余名额。**"),
    ("| 🟢 **豆包 `Seedream 5.0` 系列「输入图免费 / 首张免费」（**`doubao-seedream-5-0-flash` 输入图逐字 `免费`、输出 `0.12` 元/张；"
     "`-pro` 输入图首张免费、第 `2` 张起 `0.02` 元/张**）** | **无结束日（按张计价的常规价目，非活动；官方未给任何活动期）** | "
     "🟢 **生效中（066 期补入 · 火山引擎计费文档一手）。 `volcengine.com/docs/82379/1099320`（`1,779,461` 字节）图片生成模型表逐字**："
     "`flash` 输入图 `免费`、输出 `0.12`；`pro` 输入图 `首张免费` / 第 `2` 张起 `0.02`，输出按像素档 `0.30` / `0.60`、"
     "图层拆分 `0.15` / `0.30`。 **⚠️「免费」是输入图、不是生成；按张计价、无每日额度字段。**"),
]
for row in NEW42:
    r42.append(row + PTR)
    EDITED.append("补入：" + name_of(row)[:14])

# ------------------------------------------------------------------ 写回
assert len(r41) == 57, ("4.1 行数", len(r41))
assert len(r42) == 33, ("4.2 行数", len(r42))
for r in r41 + r42:
    assert r.count("|") == 4, ("字段数异常", r[:50], r.count("|"))
for n in ("066 期补入", "文心", "退伍军人", "Seedream 5.0"):
    assert any(n in r for r in r41 + r42), ("补入行缺失", n)

out = []
mode = None
done41 = done42 = False
for line in md.split("\n"):
    if line.startswith("### 4.1 限时动作"):
        mode = "41"
        out.append(line)
        continue
    if line.startswith("### 4.2 常驻权益本期变更"):
        mode = "42"
        out.append(line)
        continue
    if line.startswith("### ④ 本期第四章脚注"):
        mode = None
        out.append(line)
        continue
    if mode == "41" and line.startswith("| ") and not line.startswith("| 活动 |") and not line.startswith("| --- |"):
        if not done41:
            out.extend(r41)
            done41 = True
        continue
    if mode == "42" and line.startswith("| ") and not line.startswith("| 活动 |") and not line.startswith("| --- |"):
        if not done42:
            out.extend(r42)
            done42 = True
        continue
    out.append(line)

new_md = "\n".join(out)
new_md = new_md.replace("### 4.1 限时动作（有确切截止日 · 57 条）", "### 4.1 限时动作（有确切截止日 · 57 条）")
new_md = new_md.replace("### 4.2 常驻权益本期变更（无截止日 · 本期有变化 31 条）",
                        "### 4.2 常驻权益本期变更（无截止日 · 本期有变化 33 条）")
new_md = new_md.replace("## 四、限时活动与截止时间表（正文之后 · 11/11 14:00 复核）",
                        "## 四、限时活动与截止时间表（正文之后 · 11/12 12:55 复核）")
new_md = new_md.replace("全量 173 条移入《[常驻权益总账](常驻权益总账.md)》",
                        "全量 175 条移入《[常驻权益总账](常驻权益总账.md)》")
new_md = new_md.replace("> **其余 142 条常驻权益本期无变化**，不逐期重印：全量 **173** 条（含本节 31 条）",
                        "> **其余 142 条常驻权益本期无变化**，不逐期重印：全量 **175** 条（含本节 33 条）")
new_md = new_md.replace("其中 **31** 条有变化（见上表）、**142** 条口径与上期一致",
                        "其中 **33** 条有变化（见上表）、**142** 条口径与上期一致")
io.open(MD, "w", encoding="utf-8", newline="\n").write(new_md)

disk = io.open(MD, encoding="utf-8").read()
d41 = rows_of(disk, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
d42 = rows_of(disk, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
assert len(d41) == 57, ("落盘 4.1", len(d41))
assert len(d42) == 33, ("落盘 4.2", len(d42))
for phrase in ("今天还能领 ¥598", "卡册 56 张", "`469 → 467`", "`15 → 16`", "`12 → 13`",
               "`19 → 19`", "`7,112`", "`2,551`", "`201,631`", "downloads 33,617", "`11/25` 前"):
    assert phrase in disk, ("落盘缺短语", phrase)
print("改写/补入：%d 条 -> %s" % (len(EDITED), "、".join(EDITED)))
print("written:", len(disk.encode("utf-8")), "bytes | 4.1=%d 4.2=%d" % (len(d41), len(d42)))
io.open(WS + ".workbuddy/tmp_arch066.txt", "w", encoding="utf-8", newline="\n").write(ARCH[0])
