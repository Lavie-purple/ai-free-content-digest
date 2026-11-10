# -*- coding: utf-8 -*-
"""064 期：从 063 期 md 的现行 4.1 表体 + 《常驻权益总账》全量表体
-> 基准日 2026-11-10 -> 行级改写 -> 补入本期新增行。输出 .workbuddy/tmp_table064.md。

纪律（055–063 沿用，本期一条不改）：
  ① 输入取上期 md 的**现行文本**（不取上期的 tmp_table）。
  ② 写出后**复读落盘文件**再断言。
  ③ 断言用**逐字短语**，不用裸数字。
  ④ 全表字段数分布断言 Counter({3: N})。
  ⑤ 新增行必须带「本期」或「064 期」标记。
  ⑥ 状态列用 set_status() **整体改写**，不用 append_note 追加（059 期）。
  ⑦ 单元格里不许出现 `|`（守门断言＝字段数分布）。
"""
import io
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第063期-2026-11-09.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table064.md"

PREV_41 = 56
PREV_LED = 169          # 063 期 split_ledger 重建后的总账条数
PTR = " [附录 064](details.html) |"


def rows_of(text, start, end=None):
    i = text.index(start)
    j = text.index(end) if end else len(text)
    seg = text[i:j]
    return [l for l in seg.split("\n")
            if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]


md = io.open(SRC_MD, encoding="utf-8").read().replace("\r\n", "\n")
led = io.open(SRC_LED, encoding="utf-8").read().replace("\r\n", "\n")

rows_41 = rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
rows_led = rows_of(led, "## 一、全量表")
assert len(rows_41) == PREV_41, ("063 期 4.1 行数", len(rows_41))
assert len(rows_led) == PREV_LED, ("总账行数", len(rows_led))
body = rows_41 + rows_led
print("输入行数：4.1 = %d，总账 = %d，合计 = %d" % (len(rows_41), len(rows_led), len(body)))

NOTES = []


def set_status(row, status):
    cells = row.strip().rstrip("|").split("|")
    assert len(cells) == 4, ("字段数异常", len(cells))
    st = " %s%s" % (status, PTR) if PTR.strip() else " %s |" % status
    return "|%s|%s|%s" % (cells[1], cells[2], st)


def find_one(pred, tag):
    hits = [k for k, r in enumerate(body) if pred(r)]
    assert len(hits) == 1, ("命中数不是 1", tag, len(hits))
    return hits[0]


def edit(tag, pred, status):
    k = find_one(pred, tag)
    old = body[k]
    new = set_status(old, status)
    assert new != old, ("改写未生效", tag)
    body[k] = new
    NOTES.append(tag)


def name_of(r):
    return r.strip().strip("|").split("|")[0].strip()


# ---------------------------------------------------------------- 4.1 天数推进
edit("腾讯老混元", lambda r: name_of(r).startswith("🔴 **腾讯老混元大模型平台停服**"),
     "🔴 **必办（已过 `41` 天，Q04 连续第 `38` 期未决 · 高危窗口第 `29` 天）。 厂商仍只给「9 月底」这一模糊口径，"
     "未给确切停服日。 迁移目标 `TokenHub` 的两个入口本期均未给出新的迁移截止。**")

edit("Claude Code credit", lambda r: name_of(r).startswith("🟢 **Claude Code 云会话 credit"),
     "🟢 **已过 `5` 天（`11/5` 到期，官方未给延长口径）。 本报告只记日期，不推断 `credit` 是否仍可领。**")

edit("Runware upscale", lambda r: name_of(r).startswith("🟢 **`Runware` 分发层 `pruna-p-video-upscale`"),
     "🟢 **已过 `2` 天（`11/8` 到期）。 官方促销数组本期**仍原样保留**该条：`endsAt: \"2026-11-08\"`、"
     "描述逐字 `50% off all generations until November 8, 2026`。 全数组 `19 → 19` 条、新增 `0`、消失 `0`、"
     "`endsAt` 变化 `0`；**按 `11/10` 基准，仍在售 `6` 条**（`11/10` ×2、`11/15`、`11/19`、`11/30`、`12/31`），"
     "**已过期但仍在数组里 `13` 条**。 「数组里还在 ≠ 在售」第四次实证。**")

edit("MiniMax M3/M2", lambda r: name_of(r).startswith("🟢 **MiniMax 开放平台 M3 / M2 免费试用**"),
     "🟢 **已过 `3` 天（`11/7` 到期，官方未给延长口径）。 该条仍留在 4.1 —— 归档规则是「过期 >7 天且已收口」，"
     "本期只过 `3` 天。**")

edit("火山 Coding Plan", lambda r: name_of(r).startswith("🟢 **火山 Coding Plan 2.5 折**"),
     "🟢 **已过 `2` 天（`11/8` 到期，官方未给延长口径）。 `Pro` 首购 `49.9` 元为**首月价**，续费按原价。**")

edit("火山方舟 Agent Plan", lambda r: name_of(r).startswith("🟢 **火山方舟 Agent Plan 个人版"),
     "🟢 **已过 `2` 天（`11/8` 到期）。 「数据调用次数」不是「模型 token」—— 两类额度不能相加。**")

edit("腾讯元器", lambda r: name_of(r).startswith("🔴 **腾讯智能体平台「元器」停止服务"),
     "🔴 **停服日已过 `1` 天（`11/9` 为官方停服日）。 四个日期必须继续分开排**：`10/29` 已停止新建、"
     "**`11/9` 停止服务（已过 1 天）**、`2027-01-09` 数据导出截止。 **本报告只报日期，不报「已停 / 未停」** —— "
     "没有逐字口径说几点停、也没说导出通道是否仍开。**")

edit("AutoClaw 国际站 M11W1", lambda r: name_of(r).startswith("🟢 **智谱 `AutoClaw` 国际站 `M11W1`"),
     "🟢 **已过 `2` 天（`11/8 23:59` 到期）。 国际站博客页 `32,938` 字节逐字节同值**，`M11W1` 仍 `0` 命中、"
     "`40M` 仍 `1` 次 —— **活动结束后页面也不留痕。**")

edit("AutoClaw 国内站 M11W1", lambda r: name_of(r).startswith("🟢 **智谱 `AutoClaw` 国内站 `M11W1`"),
     "🟢 **已过 `2` 天（`11/8 23:59` 到期）。 国内站博客页 `70,257` 字节逐字节同值**，`M11W1` 仍 `0` 命中、"
     "`50M` 仍 `4` 次 —— **活动结束后页面也不留痕。**")

edit("Ollie 关停", lambda r: name_of(r).startswith("⚠️ **`Ollie`（隐私向 AI 助手）宣布关停"),
     "⚠️ **停服日已过 `4` 天（`11/6` 起）。 告别信三页本期仍逐字节同值在线**（`39,747` / `41,791` / `107,182`）；"
     "**页面在线不等于服务在线** —— 官方无逐字口径，本报告不判定服务是否已停。**")

edit("Ollie Free 档", lambda r: name_of(r).startswith("⚠️ **`Ollie` 的 `Free` 档"),
     "⚠️ **停服日已过 `4` 天。 定价页 `41,791` 字节五期间值**，`50 messages … per month` / "
     "`6 free additional messages … every day` 逐字仍在；**`Free` 档是否一并停服仍无官方口径。**")

edit("鲸锐大赛", lambda r: name_of(r).startswith("🟢 **虎鲸文娱「鲸锐 AI 创作大赛」"),
     "🟢 **生效中（距截止 `12` 天）。 ⚠️（063 期新登记 · 媒体口径）** 奖金与名额逐字：总奖金池 `1000` 万元、"
     "`265` 个获奖名额、单项最高 `200` 万元。 **官方报名页本期仍未核到**，报名入口与细则以官方为准。**")

edit("国家超算", lambda r: name_of(r).startswith("🟠 **`国家超算互联网` 夜间限时免费调用"),
     "🟠 **已过 `11` 天（官方逐字 `10月21日至10月30日`）。 本期页面 `132,924` 字节、四项关键词仍零命中 —— "
     "连续第 `14` 期未复核到活动页留痕。**")

# ---------------------------------------------------------------- 4.2 常驻
edit("OpenRouter 免费档", lambda r: name_of(r).startswith("🟢 **OpenRouter 免费档（**官方 API 目录口径"),
     "🟢 **生效中（动态目录）。 （064 期）全量 `461 → 465`（`+4`）、零价 `16 → 16`（`0`）、`:free` `12 → 13`（`+1`）** —— "
     "**6 进 2 出**：进 `anthropic/claude-fable-5.2`（+`:batch`）、`meta/muse-ember`、`nex-agi/nex-n2.6`、"
     "`qwen/qwen3.8-max-0902:batch`、**`thinkingmachines/inkling-2-small:free`**；出 `minimax/minimax-m1`、"
     "**`stealth/crouton-alpha`**。 另 `12` 条付费条目调价：`z-ai/glm-5.3-flash` 输入 `×4.5`、输出 `×6.0`；"
     "`~anthropic/claude-fable-latest` 反向降（输入 `$10 → $8`/M，与官方公告一致）。**")

edit("OpenCode 清单", lambda r: name_of(r).startswith("🟡 **`OpenCode` 免费模型清单 10 → 11 项"),
     "🟡 **生效中（清单动态）。 （064 期）三套口径从 `12/12/13` 变成 `13/13/13`（`-free` 后缀 / 上游 `:free` / "
     "输入输出都 `Free`），**退一进二**：出 `crouton-alpha-free`，进 `longcat-2.5-free` 与 "
     "`minimax-m3.1-flash-free`**；页面 `97,064 → 91,324`（`−5,740`）。 **`LongCat 2.5 Free` 页面标注"
     "「自 11 月 9 日起限免两周」，但厂商官方站 `免费` / `限免` / `额度` 各 `0` 命中 —— 限免只有分发层在说。**")

edit("crouton", lambda r: name_of(r).startswith("🟢 **`OpenRouter` 免费隐身模型 `stealth/crouton-alpha`"),
     "⚪ **已下架（第 `8` 天收摊）。 三条线同时消失**：`OpenRouter` 目录里该 `ID` 已不在（`REM` 之一）、"
     "`stealth/crouton-alpha/llms.txt` 由 `4,021` 字节变为 `404` / `10` 字节 `Not Found`、"
     "`opencode.ai/docs/zen` 的 `crouton` 命中 `1 → 0`。 **隐身期结束**，官方未发说明。**")

edit("Ripple", lambda r: name_of(r).startswith("🟢 **`Ripple-65B Preview` 开放权重"),
     "🟢 **生效中。 （064 期）四个仓库 `downloads` 全部**零增长**（主仓 `5,835` 同值、`-NVFP4` `2,724`、"
     "`-DFlash2` `2,787`、`Base-Preview` `408`），`likes` 主仓 `423 → 458`（`+35`）；"
     "`lastModified` 仍 `2026-11-06T19:26:32Z`（四天没动）。 **单日 `downloads` 不动 ≠ 没人下载** —— 见避坑 283。**")

edit("ERNIE", lambda r: name_of(r).startswith("🟢 **百度开源 `ERNIE-5.5-Flash-Base`"),
     "🟢 **生效中。 （064 期第 `4` 次复核）许可 `LICENSE` 仍恰为 `25,619` 字节**、两仓 `lastModified` 仍停在 "
     "`2026-11-05T06:33Z` / `06:37Z`（五天没动）；流通量：`FP8` `downloads 1,699`（同值）、`likes 235 → 244`，"
     "`BF16` `downloads 618`（同值）、`likes 383`（同值）。 **两仓 `downloads` 首次双双零增长。**")

edit("豆包工作订阅", lambda r: name_of(r).startswith("🟢 **豆包工作 30 天订阅"),
     "🟢 **生效中（022 期登记）。 第三方整理口径，以客户端订阅页为准。 （064 期）`volcengine.com/product/doubao-work` "
     "`169,627` 字节与上期同值但 `md5` 不同（差 `idc` / `logId` / `master.version 8099 → 8100` 三个服务端构签字段）；"
     "`doubao.com/work` `57,784` 逐字节同值；四项关键词仍各 `0` 命中 —— **订阅活动连续第 `20` 期无一手。**")

edit("豆包额度规则", lambda r: name_of(r).startswith("🟢 **豆包工作个人版取消 `5` 小时额度限制"),
     "🟢 **生效中。 （064 期）仍只有媒体口径，官方无补稿**：两个官方页四项关键词各 `0` 命中，**距首发已 `4` 天**。 "
     "改的是「一周内怎么花」，不是「能花多少」。**")

edit("商汤 Token Plan", lambda r: name_of(r).startswith("🟢 **商汤 `日日新 SenseNova` Token Plan"),
     "🟢 **生效中。 （064 期）`20,820` 字节 —— 与 057–062 六期加 063 期逐字节相同**，`公测期完全免费开放` / "
     "`限时放量` / `¥ 0` 各 `1` 次，**`截止` 仍 `0` 命中**、仍无截止日（连续第 `8` 期）。**")

edit("小浣熊", lambda r: name_of(r).startswith("🟢 **商汤 `小浣熊`（Raccoon）免费版"),
     "🟢 **生效中。 （064 期）`159,731` 字节与 057–062 六期加 063 期逐字节相同**：`免费版` `2` / `¥ 0` `2` / "
     "`/永久` `2` / `300` `7` 逐字全在。**")

edit("商汤 6.8 Flash", lambda r: name_of(r).startswith("⚠️ **商汤 `SenseNova 6.8 Flash` 上线"),
     "⚠️ **生效中（口径）。 （064 期）`sensetime.com/cn/news` `113,853` 字节 —— 与 061–063 三期逐字节相同**，"
     "`SenseNova 6.8` 命中 `2` 次仍在；**`限时` 与 `免费` 仍各 `0` 命中** —— 「限时免费」仍只有媒体口径（连续第 `8` 期）。**")

edit("AXON", lambda r: name_of(r).startswith("🟢 **`AXON Developer Edition`"),
     "🟢 **生效中。 （064 期）`20,111` 字节 —— 与 058–063 六期逐字节相同**，`license` / `LICENSE` / `version` / "
     "`Apache` **各 `0` 命中 —— 连续第 `7` 期无许可证与版本号**，仍标 `Free forever`、无需账号。**")

edit("Token 羊毛", lambda r: name_of(r).startswith("🟡 **`AIHOT` 的「Token 羊毛」"),
     "🟡 **生效中（064 期新登记 · 第三方聚合，非厂商一手）。 （064 期连续第 `2` 期核实）页头「今天还能领 ¥201 → ¥535」、"
     "「卡册 51 → 52 张」**；**核实标注 `106 → 108` 处，日期分布整批翻页**（11/8 `78 → 8`、11/9 `24 → 84`、"
     "11/10 `0 → 12`）—— **这是它「按日复核」的自证，不是文案**。 ⚠️ 折算与不收范围见 063 期原文，本期未变。**")

edit("AMD", lambda r: name_of(r).startswith("⚠️ **`AMD` `Radeon Token Factory`"),
     "⚠️ **生效中（线索，额度仍未确认）。 （064 期）官方页 `developer.amd.com.cn/radeon/modelapis` 返回 `200` / "
     "`200,572` 字节，正文仍是 `Loading Radeon Cloud…` + `JavaScript is required`，`Free` / `免费` / `quota` / "
     "`Daily` / `USD` **各 `0` 命中** —— 三份来源 `$1` / `$10` / 「免费」的冲突本期仍未解，不取中位数、不取最好看的。**")

edit("OpenCode Inkling", lambda r: name_of(r).startswith("🟢 **`OpenCode` 的 `Inkling 2 Small Free`"),
     "🟢 **生效中。 （064 期）上游 `OpenRouter` 已上架 `thinkingmachines/inkling-2-small:free`（零价、`1M` 上下文、"
     "`17B` 激活 / `594B` 总参数、`11/9` 建条目）；`OpenCode` 侧 `inkling-2-small-free` 仍命中 `4` 次。 "
     "**`HF` 侧 `author=thinkingmachines` 仍 `6` 仓、无 `Inkling-2` —— 权重连续第 `4` 期未放。**")

edit("Antigravity 免费档", lambda r: name_of(r).startswith("🟢 **`Google Antigravity` 个人免费档"),
     "🟢 **生效中（官方定价页逐字）。 （064 期）定价页本期重新拿到：`200` / `142,552` 字节**（063 期是 `000`），"
     "`$0/month` / `Experience Antigravity without a subscription plan` / `Unlimited Tab completions` / "
     "`Unlimited Command requests` / `Basic weekly rate limits *` 逐字全在。 **官方就是不给数字**，本期不再追问。**")

edit("Kimi 访问条件", lambda r: name_of(r).startswith("⚠️ **`Moonshot` `Kimi K3.1 Pro` 的访问条件"),
     "⚠️ **生效中（口径）。 （064 期）`?search=Kimi-K3.1-Highspeed` 仍返回 `[]`（`2` 字节）—— 官方名下 `Highspeed` "
     "版权重连续第 `5` 期 `0` 条。**")

# ---------------------------------------------------------------- 本期补入行
NEW = [
    # A. Claude Fable 5.2 发布优惠（4.1 · 有确切截止日）
    "| 🟢 **Anthropic `Claude Fable 5.2` / `Mythos 5.2` 发布优惠（**`11/9` 发布 · `API` `$8` / `$40` 每百万 token · "
    "`fast mode` `$16` / `$80` · **发布优惠只给付费档，官方帮助中心逐字排除 `Free` 计划**）** | "
    "**`11/16 23:59 PT`（`Pro` / `Team` 标准席位含 `Fable` 一周）；`2027-03-08 23:59 PT`（`Max` / `Ultra` / 高级席位的 "
    "`1–3` 次 `Fable` 重置到期）** | "
    "🟢 **生效中（距第一个截止 `6` 天）。 （064 期新登记 · 官方帮助中心逐字）** 三档拆清：**`Pro` / `Team` 标准席位** "
    "`11/9–11/16 23:59 PT` 内含全部 `Fable` 模型、最多占每周额度 `50%`，另给 `1` 次重置；**`Max` / `Ultra` / 高级席位** "
    "按订阅时长给 `1–3` 次重置（<6 月 `1`、6–12 月 `2`、>12 月 `3`）；**`Free` 计划逐字「They aren't available on the "
    "Free plan」——说的是这两项发布优惠，不是模型本身。**" + PTR,
    # B. Inkling 2 Small 免费档上 OpenRouter（4.2 · 无截止日）
    "| 🟢 **`Thinking Machines` 的 `Inkling 2 Small` 免费档上架 `OpenRouter`（**`thinkingmachines/inkling-2-small:free` · "
    "零价 · `1M` 上下文 · `17B` 激活 / `594B` 总参数 · 多模态 `text+image`**）** | "
    "**无结束日（`:free` 条目，官方未给下架日）** | "
    "🟢 **生效中（064 期新登记 · 官方 `API` 目录一手）。 两条线要分开报**：**分发层到了** —— `OpenRouter` `461 → 465` "
    "里新增该条、`pricing` 输入输出均为 `0`；**权重层没到** —— `HF` `author=thinkingmachines` 仍 `6` 仓"
    "（`Inkling` / `Inkling-Small` / 两个 `NVFP4` / 两个 `tokenizer`），**无 `Inkling-2`，连续第 `4` 期**。 "
    "**用得上、拿不走。**" + PTR,
]

for n in NEW:
    n = n.rstrip()
    assert n.endswith("|"), ("新增行末尾缺 `|`", n[-30:])
    body.append(n)

# ---------------------------------------------------------------- 断言
cells = Counter(len(r.strip().strip("|").split("|")) for r in body)
print("字段数分布：", cells)
assert cells == Counter({3: len(body)}), ("字段数异常（单元格里混进了竖线？）", cells)

for r in NEW:
    assert ("本期" in r) or ("064 期" in r), ("新增行缺本期标记", r[:40])
    stat = r.strip().strip("|").split("|")[2]
    for bad in ("已结束", "未开始"):
        assert bad not in stat, ("状态列出现会被字面误读的词", bad, r[:40])

total = len(body)
assert total == PREV_41 + PREV_LED + len(NEW), total
print("表体总行数：%d = %d + %d + %d" % (total, PREV_41, PREV_LED, len(NEW)))

header = "| 活动 | 截止 | 状态 |\n| --- | --- | --- |\n"
io.open(OUT, "w", encoding="utf-8", newline="\n").write(header + "\n".join(body) + "\n")

# 落盘复读（052 期纪律）
disk = io.open(OUT, encoding="utf-8").read()
disk_rows = [l for l in disk.split("\n")
             if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(disk_rows) == total, ("落盘行数", len(disk_rows))
for n in NEW:
    assert n in disk, ("新增行未进落盘文件", n[:40])
for phrase in ("`461 → 465`", "`13/13/13`", "今天还能领 ¥201 → ¥535", "卡册 51 → 52",
               "106 → 108", "They aren't available on the", "`11/16 23:59 PT`",
               "`142,552`", "`200,572`", "第 `8` 天收摊", "`5835`" if False else "`5,835` 同值"):
    assert phrase in disk, ("落盘缺短语", phrase)
print("改写行：%d 条 -> %s" % (len(NOTES), "、".join(NOTES)))
print("written:", OUT, len(disk.encode("utf-8")), "bytes")
