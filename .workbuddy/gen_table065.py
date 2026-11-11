# -*- coding: utf-8 -*-
"""065 期：在上期（064）现行 4.1/4.2 表体上做行级改写 + 补入本期新增行。

纪律（055–064 沿用，一条不改）：
  ① 输入取上期 md 的**现行文本**（不取上期的 tmp_table）。
  ② 写出后**复读落盘文件**再断言。
  ③ 断言用**逐字短语**，不用裸数字。
  ④ 全表字段数分布断言 Counter({3: N})。
  ⑤ 新增行必须带「本期」或「065 期」标记。
  ⑥ 状态列用整体替换，不用追加。
  ⑦ 单元格里不许出现 `|`（守门断言＝字段数分布）。
"""
import io
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第065期-2026-11-11.md"
PTR = " [附录 065](details.html) |"

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")


def rows_of(text, start, end):
    i = text.index(start)
    j = text.index(end)
    return [l for l in text[i:j].split("\n")
            if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]


r41 = rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
r42 = rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("输入行数：4.1 = %d，4.2 = %d，合计 = %d" % (len(r41), len(r42), len(r41) + len(r42)))
assert len(r41) == 57, ("064 期 4.1 行数", len(r41))
assert len(r42) == 49, ("064 期 4.2 行数", len(r42))

EDITED = []


def set_status(row, status):
    cells = row.strip().rstrip("|").split("|")
    assert len(cells) == 4, ("字段数异常", len(cells), row[:40])
    st = " %s%s" % (status, PTR)
    return "|%s|%s|%s" % (cells[1], cells[2], st)


def name_of(r):
    return r.strip().strip("|").split("|")[0].strip()


def edit(tag, pred, status, bucket=None):
    hits = [k for k, r in enumerate(bucket) if pred(r)]
    assert len(hits) == 1, ("命中数不是 1", tag, len(hits))
    old = bucket[hits[0]]
    new = set_status(old, status)
    assert new != old, ("改写未生效", tag)
    bucket[hits[0]] = new
    EDITED.append(tag)


# ---------------------------------------------------------------- 4.1
edit("腾讯老混元", lambda r: name_of(r).startswith("🔴 **腾讯老混元大模型平台停服**"),
     "🔴 **必办（已过 `42` 天，Q04 连续第 `39` 期未决 · 高危窗口第 `30` 天）。 厂商仍只给「9 月底」这一模糊口径，"
     "未给确切停服日。 迁移目标 `TokenHub` 的两个入口本期均未给出新的迁移截止。**", r41)

edit("Claude Code credit", lambda r: name_of(r).startswith("🟢 **Claude Code 云会话 credit"),
     "🟢 **已过 `6` 天（`11/5` 到期，官方未给延长口径）。 本报告只记日期，不推断 `credit` 是否仍可领。**", r41)

edit("Runware upscale", lambda r: name_of(r).startswith("🟢 **`Runware` 分发层 `pruna-p-video-upscale`"),
     "🟢 **已过 `3` 天（`11/8` 到期）。 促销数组本期 `19 → 20` 条（新增一条 `endsAt: \"2026-11-17\"`），"
     "`11/8` 那条**仍原样保留**、新增 `0`、消失 `0`。 按 `11/11` 基准仍在售 `7` 条，**已过期但仍在数组里 `13` 条**。 "
     "「数组里还在 ≠ 在售」第五次实证。**", r41)

edit("MiniMax M3/M2", lambda r: name_of(r).startswith("🟢 **MiniMax 开放平台 M3 / M2 免费试用**"),
     "🟢 **已过 `4` 天（`11/7` 到期，官方未给延长口径）。 该条仍留在 4.1 —— 归档规则是「过期 >7 天且已收口」，"
     "本期只过 `4` 天。**", r41)

edit("火山 Coding Plan", lambda r: name_of(r).startswith("🟢 **火山 Coding Plan 2.5 折**"),
     "🟢 **已过 `3` 天（`11/8` 到期，官方未给延长口径）。 `Pro` 首购 `49.9` 元为**首月价**，续费按原价。**", r41)

edit("火山方舟 Agent Plan", lambda r: name_of(r).startswith("🟢 **火山方舟 Agent Plan 个人版"),
     "🟢 **已过 `3` 天（`11/8` 到期）。 「数据调用次数」不是「模型 token」—— 两类额度不能相加。**", r41)

edit("腾讯元器", lambda r: name_of(r).startswith("🔴 **腾讯智能体平台「元器」停止服务"),
     "🔴 **停服日已过 `2` 天（`11/9` 为官方停服日）。 三个日期继续分开排**：`10/29` 已停止新建、"
     "**`11/9` 停止服务**、`2027-01-09` 数据导出截止。 **本报告只报日期，不报「已停 / 未停」**。**", r41)

edit("AutoClaw 国际站 M11W1", lambda r: name_of(r).startswith("🟢 **智谱 `AutoClaw` 国际站 `M11W1`"),
     "🟢 **已过 `3` 天（`11/8 23:59` 到期）。 国际站博客页本期未再取到（`000`），`M11W1` 与 `40M` 的命中数沿用 064 期。 "
     "**活动结束后页面不留痕这条结论不再追加新证据。**", r41)

edit("AutoClaw 国内站 M11W1", lambda r: name_of(r).startswith("🟢 **智谱 `AutoClaw` 国内站 `M11W1`"),
     "🟢 **已过 `3` 天（`11/8 23:59` 到期）。 国内站页本期 `70,615` 字节（064 期同值），`M11W1` 仍 `0` 命中。 "
     "**活动结束后页面不留痕。**", r41)

edit("Ollie 关停", lambda r: name_of(r).startswith("⚠️ **`Ollie`（隐私向 AI 助手）宣布关停"),
     "⚠️ **停服日已过 `5` 天（`11/6` 起）。 告别信三页本期仍逐字节同值在线**（`39,747` / `41,791` / `107,182`，`md5` 全 SAME）；"
     "**页面在线不等于服务在线**，官方无逐字口径。**", r41)

edit("Ollie Free 档", lambda r: name_of(r).startswith("⚠️ **`Ollie` 的 `Free` 档"),
     "⚠️ **停服日已过 `5` 天。 定价页 `41,791` 字节六期间值**，`50 messages … per month` 逐字仍在；"
     "**`Free` 档是否一并停服仍无官方口径。**", r41)

edit("鲸锐大赛", lambda r: name_of(r).startswith("🟢 **虎鲸文娱「鲸锐 AI 创作大赛」"),
     "🟢 **生效中（距截止 `11` 天）。 ⚠️（063 期新登记 · 媒体口径）** 总奖金池 `1000` 万元、`265` 个获奖名额、"
     "单项最高 `200` 万元。 **官方报名页本期仍未核到**。**", r41)

edit("国家超算", lambda r: name_of(r).startswith("🟠 **`国家超算互联网` 夜间限时免费调用"),
     "🟠 **已过 `12` 天（官方逐字 `10月21日至10月30日`）。 本期页面 `132,924` 字节、四项关键词仍零命中 —— "
     "连续第 `15` 期未复核到活动页留痕。**", r41)

edit("Anthropic 使用政策", lambda r: name_of(r).startswith("🟢 **Anthropic 新版使用政策"),
     "🟢 **距生效 `1` 天（`11/12` 生效）。 ⚠️ 官方明确：普通反驳、表达不满、研究测试、暗黑题材创作都不在禁止范围；"
     "本期未取到官方页新增口径。**", r41)

edit("Kimi K3.1 Pro 发布", lambda r: name_of(r).startswith("🟢 **`Moonshot` `Kimi K3.1 Pro` 发布"),
     "🟢 **已兑现＋ `060` 期第四层销项。 本期补一条搜索口径更正**：仓库 `moonshotai/Kimi-K3.1-Pro` 建于 `11/2`、"
     "`license: other`、`gated: false`、`downloads 30,721` —— **她一直在，是本报连续 6 期用 `Highspeed` 搜空**。**", r41)

edit("Fable 5.2 优惠", lambda r: name_of(r).startswith("🟢 **Anthropic `Claude Fable 5.2`"),
     "🟢 **生效中（距第一个截止 `5` 天）。 （065 期）本期定价页对比表把 `Fable` × `Free` 写成逐字 `No`** —— "
     "与 `Pro` 的 `Usage credits`、`Max` / `Ultra` 的 `50% of weekly limits*` 同屏可见。 "
     "**064 期写的「`Fable` 在 Free 档命中 `0`」指的是卡片，本表补上表态。**", r41)

# ---------------------------------------------------------------- 4.2
edit("Xing4.0 免费档", lambda r: name_of(r).startswith("🟡 **中国电信 `Xing4.0-29B-A4B`"),
     "⚪ **已从 `OpenRouter` 目录下架（065 期观测）。 目录 `ID` 级 diff：`xingchen-agi/xing4.0-29b-a4b:free` 是本期唯一消失的零价条目，"
     "`:free` 由 `13` 减到 `12`、零价由 `16` 减到 `15`**。 厂商侧未发说明，本报告只报「目录里没有了」。", r42)

edit("OpenRouter 免费档", lambda r: name_of(r).startswith("🟢 **OpenRouter 免费档（**官方 API 目录口径"),
     "🟢 **生效中（动态目录）。 （065 期）全量 `465 → 469`（`+4`）、零价 `16 → 15`（`−1`）、`:free` `13 → 12`（`−1`）**；"
     "**6 进 2 出**：进 `google/gemini-4-carbon`（+`:batch`）、`baidu/ernie-5.5-flash-preview`、"
     "`baidu/ernie-light-dt-1.0-intl`、`kt/midm-k-3.0-pro`、`motif-technologies/motif-3`；"
     "出 `qwen/qwen-2.5-7b-instruct`、**`xingchen-agi/xing4.0-29b-a4b:free`**。 另 `10` 条调价，`glm-5.3-flash` 回落。", r42)

edit("OpenCode 清单", lambda r: name_of(r).startswith("🟡 **`OpenCode` 免费模型清单"),
     "🟡 **生效中（清单动态）。 （065 期）三套口径仍 `13/13/13`，成员一个没动**（`-free` 后缀 `13` 个 `ID`、页面 `91,324 → 91,792`）；"
     "`LongCat 2.5 Free` 仍标「限免两周」，厂商侧口径连续第 `2` 期为零。", r42)

edit("Token 羊毛", lambda r: name_of(r).startswith("🟡 **`AIHOT` 的「Token 羊毛」"),
     "🟡 **生效中（第三方聚合，非厂商一手）。 （065 期连续第 `3` 期实测）页头「今天还能领 ¥599」**（`535 → 599`）、"
     "**「卡册 54 张」**（`52 → 54`）、**核实标注正文口径 `112` 处**，其中 **`11/11` 当天 `94` 条**。 "
     "**本期首次读到它自己写的下架规则：`3` 天内核实不了就下架。**", r42)

edit("AMD", lambda r: name_of(r).startswith("⚠️ **`AMD` `Radeon Token Factory`"),
     "⚠️ **生效中（线索，额度仍未确认）。 （065 期第 `3` 期）官方页 `200` / `200,572` 字节、与 `…/tokenfactory` 同字节**，"
     "正文仍是 `Loading Radeon Cloud…`，`Free` / `免费` / `quota` / `USD` **各 `0` 命中**。 三份来源冲突未解。", r42)

edit("Ripple", lambda r: name_of(r).startswith("🟢 **`Ripple-65B Preview` 开放权重"),
     "🟢 **生效中。 （065 期）四个仓库 `downloads` 全部回升**：主仓 `5,835 → 6,480`（`+645`）、`NVFP4` `2,724 → 2,974`、"
     "`-DFlash2` `2,787 → 3,112`、`Base` `408 → 484`；`likes` 主仓 `458 → 490`；**`lastModified` 由 `11/06` 推进到 `11/10T09:31Z`**。 "
     "**064 期的「零增长」次日全部回升 —— 那是刷新节奏，不是热度**（避坑 283 的反向验证）。", r42)

edit("ERNIE", lambda r: name_of(r).startswith("🟢 **百度开源 `ERNIE-5.5-Flash-Base`"),
     "🟢 **生效中。 （065 期第 `5` 次复核）流通量双双回升**：`FP8` `downloads 1,699 → 2,111`（`+412`）、`likes 244 → 252`；"
     "`BF16` `618 → 755`（`+137`）、`likes 383 → 387`。 **许可 `LICENSE` 仍恰为 `25,619` 字节**、两仓 `lastModified` 仍停在 `11/05`。", r42)

edit("豆包工作订阅", lambda r: name_of(r).startswith("🟢 **豆包工作 30 天订阅"),
     "🟢 **生效中（022 期登记）。 第三方整理口径，以客户端订阅页为准。 （065 期）`doubao-work` `169,627 → 169,630`（`+3` 字节），"
     "`doubao.com/work` `57,784` 逐字节同值，四项关键词仍各 `0` 命中 —— **连续第 `21` 期无一手。**", r42)

edit("商汤 Token Plan", lambda r: name_of(r).startswith("🟢 **商汤 `日日新 SenseNova` Token Plan"),
     "🟢 **生效中。 （065 期）`20,820` 字节 —— 与 057 期起连续九期逐字节相同**，`公测期完全免费开放` / `限时放量` / `¥ 0` 各 `1` 次，"
     "**`截止` 仍 `0` 命中（连续第 `9` 期）**。", r42)

edit("小浣熊", lambda r: name_of(r).startswith("🟢 **商汤 `小浣熊`（Raccoon）免费版"),
     "🟢 **生效中。 （065 期）页面 `159,731 → 188,107` 字节，新增「双十一限时特惠 · 会员卡 低至 2 折」，会员月费由 `¥29.9` 标为 `¥11.11`"
     "（原价 `¥48.0`）**；`免费版` `2` / `¥ 0` `2` / `/永久` `2` 逐字仍在。 **页面未给活动截止时点。**", r42)

edit("商汤 6.8 Flash", lambda r: name_of(r).startswith("⚠️ **商汤 `SenseNova 6.8 Flash` 上线"),
     "⚠️ **生效中（口径）。 （065 期）`sensetime.com/cn/news` `113,853 → 111,705` 字节（新闻列表翻页，正文命中未变）**，"
     "`SenseNova 6.8` 命中 `2` 次仍在；**`限时` 与 `免费` 仍各 `0` 命中 —— 连续第 `9` 期只有媒体口径。**", r42)

edit("AXON", lambda r: name_of(r).startswith("🟢 **`AXON Developer Edition`"),
     "🟢 **生效中。 （065 期）`20,111` 字节 —— 与 058 期起连续八期逐字节相同**，`license` / `LICENSE` / `version` / `Apache` "
     "**各 `0` 命中 —— 连续第 `8` 期无许可证与版本号**，仍标 `Free forever`。", r42)

edit("Antigravity 免费档", lambda r: name_of(r).startswith("🟢 **`Google Antigravity` 个人免费档"),
     "🟢 **生效中（官方定价页逐字）。 （065 期）定价页 `142,604` 字节（064 期 `142,552`）**，`$0/month` / "
     "`Experience Antigravity without a subscription plan` / `Basic weekly rate limits *` 逐字全在。 "
     "**`/models` 由 `000` 变成 `404`（连续第 `4` 期空）。**", r42)

# ---------------------------------------------------------------- 本期补入行
NEW = [
    # A. Claude 工作台扩张：定价页新增两行，Free 列逐字 No（4.2 · 无截止日）
    "| 🟢 **`Anthropic` 把 `Claude` 扩成工作台：`Plugins` / `Sheets` / `Whiteboards` / `Interactive Connectors`"
    "（**`11/10` 起陆续上线 · `Claude Meetings` 官方称 coming soon**）** | "
    "**无结束日（产品能力，非活动）** | "
    "🟢 **生效中（065 期新登记 · 官方定价页一手）。 定价页 `1,325,494 → 1,344,061` 字节，对比表新增 `Claude Sheets (beta)` 与 "
    "`Claude Whiteboards (beta)` 两行，两行的 `Free` 列都是逐字 `No`（`Pro` / `Max` / `Ultra` 为 `Yes`）**；"
    "`Interactive Connectors` 在页内 `0` 命中 —— 只有媒体口径。**" + PTR,
    # B. 小浣熊双十一（4.2 · 无截止时点）
    "| 🟡 **商汤 `小浣熊`「双十一限时特惠」会员卡 `2` 折（**页面逐字 · 月费 `¥29.9 → ¥11.11`、原价 `¥48.0`**）** | "
    "**未公布（页面只写「双十一限时特惠」，未给截止时点；本报告不推断几点结束）** | "
    "🟡 **生效中（065 期新登记 · 官方页一手）。 页面 `159,731 → 188,107` 字节**，`免费版` / `¥ 0` / `/永久` 三处免费口径未变；"
    "**这是本期唯一一条「厂商自己把折扣数字写进价格页」的促销 —— 与 `AIHOT` 的第三方折算不是一回事。**" + PTR,
    # C. DeepSeek Harness（4.2 · 无截止日）
    "| 🟢 **`DeepSeek Harness` 面向全球开放测试并同步开源（**「一切皆插件」· `Cordis` 架构 · 桌面端 `macOS` / `Windows`**）** | "
    "**无结束日（预览版开放测试，官方未给期限）** | "
    "🟢 **生效中（065 期新登记 · 官方页一手）。 `deepseek.com/harness` `206,789` 字节逐字「面向全球开放测试并同步开源」，"
    "`GitHub` 与「社区插件」入口都在**；**⚠️ 媒体称「官方开始给插件作者发 `Token`」，但该页 `Token` / `免费` / `额度` 各 `0` 命中 —— "
    "补贴部分只算媒体口径，不进表。**" + PTR,
]

r42.extend(NEW)
for n in NEW:
    assert n.rstrip().endswith("|"), ("新增行末尾缺 `|`", n[-30:])

# ---------------------------------------------------------------- 断言
for bucket, nm in ((r41, "4.1"), (r42, "4.2")):
    cells = Counter(len(r.strip().strip("|").split("|")) for r in bucket)
    print(nm, "字段数分布：", cells)
    assert cells == Counter({3: len(bucket)}), ("字段数异常（单元格里混进了竖线？）", nm, cells)

for n in NEW:
    assert ("本期" in n) or ("065 期" in n), ("新增行缺本期标记", n[:40])
    stat = n.strip().strip("|").split("|")[2]
    for bad in ("已结束", "未开始"):
        assert bad not in stat, ("状态列出现会被字面误读的词", bad)

# ---------------------------------------------------------------- 写回
out_lines = []
mode = None
for line in md.split("\n"):
    if line.startswith("### 4.1 限时动作"):
        mode = "41"
        out_lines.append(line)
        continue
    if line.startswith("### 4.2 常驻权益本期变更"):
        mode = "42"
        out_lines.append(line)
        continue
    if line.startswith("### ④ 本期第四章脚注"):
        mode = None
        out_lines.append(line)
        continue
    if mode == "41" and line.startswith("| ") and not line.startswith("| 活动 |") and not line.startswith("| --- |"):
        if not getattr(set_status, "_done41", False):
            out_lines.extend(r41)
            set_status._done41 = True
        continue
    if mode == "42" and line.startswith("| ") and not line.startswith("| 活动 |") and not line.startswith("| --- |"):
        if not getattr(set_status, "_done42", False):
            out_lines.extend(r42)
            set_status._done42 = True
        continue
    out_lines.append(line)

new_md = "\n".join(out_lines)
io.open(MD, "w", encoding="utf-8", newline="\n").write(new_md)

# 落盘复读（052 期纪律）
disk = io.open(MD, encoding="utf-8").read()
d41 = rows_of(disk, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
d42 = rows_of(disk, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
assert len(d41) == len(r41), ("落盘 4.1 行数", len(d41))
assert len(d42) == len(r42), ("落盘 4.2 行数", len(d42))
for n in NEW:
    assert n in disk, ("新增行未进落盘文件", n[:40])
for phrase in ("今天还能领 ¥599", "卡册 54 张", "`465 → 469`", "`16 → 15`", "`13 → 12`",
               "`Claude Sheets (beta)`", "`Claude Whiteboards (beta)`", "5,835 → 6,480",
               "1,699 → 2,111", "双十一限时特惠", "`206,789`", "`Highspeed` 搜空"):
    assert phrase in disk, ("落盘缺短语", phrase)
print("改写行：%d 条 -> %s" % (len(EDITED), "、".join(EDITED)))
print("written:", MD, len(disk.encode("utf-8")), "bytes | 4.1=%d 4.2=%d" % (len(d41), len(d42)))
