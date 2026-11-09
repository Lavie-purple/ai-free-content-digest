# -*- coding: utf-8 -*-
"""063 期：从 062 期 md 的现行 4.1 表体 + 《常驻权益总账》全量表体
-> 基准日 2026-11-09 -> 行级改写 -> 补入本期新增行。输出 .workbuddy/tmp_table063.md。

沿用 055–062 的纪律：
  ① 输入直接取上期 md 的现行文本（不取上期的 tmp_table）。
  ② 写出后复读落盘文件再断言。
  ③ 断言用逐字短语，不用裸数字。
  ④ 全表字段数分布断言 Counter({3: N})。
  ⑤ 新增行必须带「本期」或「063 期」标记。
  ⑥ 状态列用 set_status() 整体改写。
"""
import io
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第062期-2026-11-08.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table063.md"

PREV_41 = 55
# ⚠️ 063 期实跑时《常驻权益总账》还是 062 期重建后的 **167** 条；
#    本期 `split_ledger.py` 跑完把总账重建成 169 条（+2 条新登记）。
#    **因此本脚本现在重跑会在这一行断言失败 —— 那是预期行为，不是回归。**
#    实跑的输入快照留在 `.workbuddy/tmp_table063.md`（225 行）。
PREV_LED = 167


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
assert len(rows_41) == PREV_41, ("062 期 4.1 行数", len(rows_41))
assert len(rows_led) == PREV_LED, ("总账行数", len(rows_led))
body = rows_41 + rows_led
print("输入行数：4.1 = %d，总账 = %d，合计 = %d" % (len(rows_41), len(rows_led), len(body)))

NOTES = []


def set_status(row, status):
    cells = row.strip().rstrip("|").split("|")
    assert len(cells) == 4, ("字段数异常", len(cells))
    return "|%s|%s| %s |" % (cells[1], cells[2], status)


def find_one(pred, tag):
    hits = [k for k, r in enumerate(body) if pred(r)]
    assert len(hits) == 1, (tag, len(hits))
    return hits[0]


def edit(tag, pred, fn):
    k = find_one(pred, tag)
    old = body[k]
    new = fn(old)
    assert new != old, ("改写未生效", tag)
    body[k] = new
    NOTES.append(tag)


# ① OpenRouter：461→461，成员零变动，12 条付费条目调价
def _or(r):
    assert "`461/16/12`" in r, ("旧计数未找到", r[:80])
    return set_status(r,
        "🟢 **生效中（动态目录）。 ⚠️（063 期）全量 `461 → 461`（`0`）、零价 `16 → 16`、`:free` `12 → 12` —— "
        "**三个计数与成员本期一个都没动**（`ADD 0` / `REM 0`）；**但 `12` 条付费条目调价**："
        "`openai/gpt-oss-120b` 输入 `$0.000000019 → $0.00000015`（**`×7.9`**）、输出 `×8.5`；"
        "`deepseek/deepseek-v4-pro` 输入 `×3.4`、输出 `×3.4`；`meta-llama/llama-3.1-8b-instruct` 反向腰斩（`×0.4`）。"
        "**⚠️ 免费区看不见这些变化，两条账要分开报。**")


edit("OpenRouter 免费档", lambda r: r.startswith("| 🟢 **OpenRouter 免费档（**官方 API 目录口径"), _or)


# ② OpenCode：三套口径 12/12/13 成员全同，页面 −2,219 全是导航
def _oc(r):
    return set_status(r,
        "🟡 **生效中（清单动态）。 ⚠️（063 期）三套口径全部同值、成员一个没换**：`-free` 后缀 `12`、"
        "价格表三列全 `Free` 的 `12`、「输入与输出都 `Free`」的 `13`；**页面 `99,283 → 97,064`（`−2,219`）**，"
        "逐段 diff 后差异**全在侧栏导航**（编号列表被换成 `How it works` 折叠），模型表一行没动。"
        "**⚠️ 字节变少不等于条目变少。**")


edit("OpenCode 清单", lambda r: r.startswith("| 🟡 **`OpenCode` 免费模型清单 10 → 11 项"), _oc)


# ③ crouton 第 7 天
def _cr(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（063 期）上架第 `7` 天仍在**：`llms.txt` `4,021` 字节与 059–062 四期逐字节相同；"
        "`opencode.ai/docs/zen` 里 `crouton-alpha-free` 命中 `1` 次，留存 `30` 天、不用于训练的口径未变。"
        "**两个 `inkling:free`（第一代）仍不回归。**")


edit("crouton", lambda r: r.startswith("| 🟢 **`OpenRouter` 免费隐身模型 `stealth/crouton-alpha`"), _cr)


# ④ Ripple：downloads 5,835 / likes 423
def _rp(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（063 期）`downloads 5,087 → 5,835`（`+748` / `+14.7%`）、`likes 382 → 423`（`+41`）**；"
        "`lastModified` 仍 `2026-11-06T19:26:32Z`（仓库文件三天没动）。**四个仓库增速分化**：主仓 `5,835`、"
        "`-NVFP4` `2,724`、`-DFlash2` `2,787`、`Base-Preview` `408`。**⚠️ `downloads` 是近 `30` 天滚动窗口，不是累计。**")


edit("Ripple", lambda r: r.startswith("| 🟢 **`Ripple-65B Preview` 开放权重（**061 期补登"), _rp)


# ⑤ ERNIE 第 3 次复核
def _ernie(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（063 期第 `3` 次复核）许可 `LICENSE` 仍恰为 `25,619` 字节（逐字节同）、两个仓库 "
        "`lastModified` 仍停在 `2026-11-05T06:33Z` / `06:37Z`（四天没动）**；流通量：`FP8` `downloads 1,400 → 1,699`、"
        "`likes 225 → 235`，`BF16` `downloads 503 → 618`、`likes 384 → 383`（**`likes` 首次回落 `1`，本报告不解释成因**）。")


edit("ERNIE 复核", lambda r: r.startswith("| 🟢 **百度开源 `ERNIE-5.5-Flash-Base`"), _ernie)


# ⑥ 豆包工作 30 天订阅：第 19 期
def _db(r):
    return set_status(r,
        "🟢 **生效中（022 期登记）。 ⚠️ 第三方整理口径，以客户端订阅页为准。 ⚠️（063 期）`volcengine.com/product/doubao-work` "
        "`169,627` 字节与上期同值但 `md5` 不同（`doubao.com/work` `57,887 → 57,784`），`5小时` / `周额度` / `额度` / `免费` "
        "**仍各 `0` 命中** —— **订阅活动连续第 `19` 期无一手。**")


edit("豆包工作订阅", lambda r: r.startswith("| 🟢 **豆包工作 30 天订阅（新一轮）**"), _db)


# ⑦ 豆包额度规则：媒体口径第 3 天
def _dbq(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（063 期）仍只有媒体口径，官方无补稿**：两个官方页四项关键词各 `0` 命中，**距首发已 `3` 天**。"
        "**改的是「一周内怎么花」，不是「能花多少」。**")


edit("豆包额度规则", lambda r: r.startswith("| 🟢 **豆包工作个人版取消 `5` 小时额度限制"), _dbq)


# ⑧ 商汤 Token Plan 第 7 期同值
def _sn(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（063 期）`20,820` 字节 —— 与 057–062 六期逐字节相同**，`公测期完全免费开放` / `限时放量` / "
        "`¥ 0` 各 `1` 次，**`截止` 仍 `0` 命中**、仍无截止日。")


edit("商汤 Token Plan", lambda r: r.startswith("| 🟢 **商汤 `日日新 SenseNova` Token Plan 公测免费档"), _sn)


# ⑨ 小浣熊第 7 期同值
def _xxh(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（063 期）`159,731` 字节与 057–062 六期逐字节相同**：`免费版` `2` / `¥ 0` `2` / `/永久` `2` / "
        "`300` `7` 逐字全在。")


edit("小浣熊免费版", lambda r: r.startswith("| 🟢 **商汤 `小浣熊`（Raccoon）免费版"), _xxh)


# ⑩ 商汤 6.8 Flash 第 7 期
def _sn68(r):
    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（063 期）`sensetime.com/cn/news` `113,853` 字节 —— 与 061–062 两期逐字节相同**，"
        "`SenseNova 6.8` 命中 `2` 次仍在；**`限时` 与 `免费` 仍各 `0` 命中** —— **「限时免费」仍只有媒体口径（连续第 `7` 期）。**")


edit("商汤 6.8 Flash", lambda r: r.startswith("| ⚠️ **商汤 `SenseNova 6.8 Flash` 上线"), _sn68)


# ⑪ AXON 第 6 期
def _axon(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（063 期）`20,111` 字节 —— 与 058–062 五期逐字节相同**，`license` / `LICENSE` / `version` / "
        "`Apache` **各 `0` 命中 —— 连续第 `6` 期无许可证与版本号**，仍标 `Free forever`、无需账号。")


edit("AXON", lambda r: r.startswith("| 🟢 **`AXON Developer Edition`"), _axon)


# ⑫ Kimi Highspeed 第 4 期空
def _kimi(r):
    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（063 期）`?search=Kimi-K3.1-Highspeed` 仍返回 `[]`（`2` 字节）—— "
        "**官方名下 `Highspeed` 版权重连续第 `4` 期 `0` 条**。**官方名下无此仓库，不写「还没放出」。**")


edit("Kimi 访问条件", lambda r: r.startswith("| ⚠️ **`Moonshot` `Kimi K3.1 Pro` 的访问条件"), _kimi)


# ⑬⑭ Ollie 两条：关停日已过 3 天
def _ollie1(r):
    return set_status(r,
        "⚠️ **关停日已过 `3` 天。 ⚠️（063 期）告别信三页仍逐字节同值在线**（`39,747` / `41,791` / `107,182`）；"
        "**页面在线不等于服务在线** —— 官方无逐字口径，本报告不判定服务是否已停。")


edit("Ollie 关停", lambda r: r.startswith("| ⚠️ **`Ollie`（隐私向 AI 助手）宣布关停"), _ollie1)


def _ollie2(r):
    return set_status(r,
        "⚠️ **关停日已过 `3` 天。 ⚠️（063 期）定价页 `41,791` 字节四期间值**，`50 messages … per month` / "
        "`6 free additional messages … every day` 逐字仍在；**`Free` 档是否一并停服仍无官方口径。**")


edit("Ollie Free 档", lambda r: r.startswith("| ⚠️ **`Ollie` 的 `Free` 档"), _ollie2)


# ⑮ Runware pruna-upscale：11/8 到期，数组未动
def _rw(r):
    return set_status(r,
        "🟢 **截止日已过 `1` 天（`11/8` 到期）。 ⚠️（063 期）到期次日，官方促销数组**仍原样保留**该条："
        "`endsAt: \"2026-11-08\"`、描述逐字 `50% off all generations until November 8, 2026` —— **字面过去时，条目还在**。"
        "全数组 `19 → 19` 条、新增 `0`、消失 `0`、`endsAt` 变化 `0`；**按 `11/9` 基准，仍在售 `6` 条**"
        "（`11/10` ×2、`11/15`、`11/19`、`11/30`、`12/31`），已过期但仍在数组里 `13` 条。**「数组里还在 ≠ 在售」第三次实证。**")


edit("Runware upscale", lambda r: r.startswith("| 🟢 **`Runware` 分发层 `pruna-p-video-upscale`"), _rw)


# ⑯⑰ 火山两条：11/8 到期
def _volc1(r):
    return set_status(r,
        "🟢 **已过 `1` 天（`11/8` 到期，官方未给延长口径）。 ⚠️（063 期）** `Pro` 首购 `49.9` 元为**首月价**，"
        "续费按原价；到期后活动页未更新。")


edit("火山 Coding Plan", lambda r: r.startswith("| 🟢 **火山 Coding Plan 2.5 折**"), _volc1)


def _volc2(r):
    return set_status(r,
        "🟢 **已过 `1` 天（`11/8` 到期）。 ⚠️（063 期）** 「数据调用次数」不是「模型 token」——两类额度不能相加"
        "（避坑 54 同源：计量单位不同就不能合并）。")


edit("火山方舟 Agent Plan", lambda r: r.startswith("| 🟢 **火山方舟 Agent Plan 个人版"), _volc2)


# ⑱ MiniMax M3/M2：11/7 到期，已过 2 天
def _mm(r):
    return set_status(r,
        "🟢 **已过 `2` 天（`11/7` 到期，官方未给延长口径 · 061 期是 `T+0`、062 期是 `T+1`）。 ⚠️（063 期）"
        "**该条仍留在 4.1，未移入归档** —— 归档规则是「过期 >7 天且已收口」，本期只过 `2` 天。")


edit("MiniMax 试用", lambda r: r.startswith("| 🟢 **MiniMax 开放平台 M3 / M2 免费试用**"), _mm)


# ⑲⑳ AutoClaw M11W1 两条：11/8 23:59 到期
def _ac1(r):
    return set_status(r,
        "🟢 **已过 `1` 天（`11/8 23:59` 到期）。 ⚠️（063 期）国际站博客页本期 `32,938` 字节逐字节同值**，"
        "`M11W1` 仍 `0` 命中、`40M` 仍 `1` 次 —— **活动结束后页面也不留痕。**")


edit("AutoClaw 国际站 M11W1", lambda r: r.startswith("| 🟢 **智谱 `AutoClaw` 国际站 `M11W1` 万圣节档"), _ac1)


def _ac2(r):
    return set_status(r,
        "🟢 **已过 `1` 天（`11/8 23:59` 到期）。 ⚠️（063 期）国内站博客页本期 `70,257` 字节逐字节同值**，"
        "`M11W1` 仍 `0` 命中、`50M` 仍 `4` 次 —— **活动结束后页面也不留痕。**")


edit("AutoClaw 国内站 M11W1", lambda r: r.startswith("| 🟢 **智谱 `AutoClaw` 国内站 `M11W1` 万圣节档"), _ac2)


# ㉑ 腾讯元器：今天停服
def _yq(r):
    return set_status(r,
        "🔴 **今天是停服日（`11/9`）。 ⚠️（063 期）四个日期必须继续分开排**：`10/29` 已停止新建、**`11/9` 停止服务（今天）**、"
        "`2027-01-09` 数据导出截止；官方公告口径本期未变。**⚠️ 本报告只报日期，不报「已停/未停」——没有逐字口径说几点停。**")


edit("腾讯元器", lambda r: r.startswith("| 🔴 **腾讯智能体平台「元器」停止服务"), _yq)


# ㉒ 腾讯老混元：高危窗口天数
def _hy(r):
    return set_status(r,
        "🔴 **必办（已过 `40` 天，Q04 连续第 `37` 期未决 · 高危窗口第 `28` 天）。 厂商仍只给「9 月底」这一模糊口径，"
        "未给确切停服日；** 迁移目标 `TokenHub` 的两个入口本期均未给出新的迁移截止。")


edit("腾讯老混元", lambda r: r.startswith("| 🔴 **腾讯老混元大模型平台停服**"), _hy)


# ---------------- 本期补入行 ----------------
NEW = [
    # A. 鲸锐 AI 创作大赛（4.1）
    "| 🟢 **虎鲸文娱「鲸锐 AI 创作大赛」（**国内首个总奖金池 `1,000` 万元的 AI 视频创作大赛 · `265` 个获奖名额 · "
    "单项最高 `200` 万元 · 不限工具与题材 · 个人与团队均可**）** | "
    "**11/22（作品征集截止；媒体一手 `量子位` `2026-11-09 10:19` 逐字「作品征集将在 11 月 22 日截止」）** | "
    "🟢 **生效中（距截止 `13` 天）。 ⚠️（063 期新登记 · 媒体口径）** 奖金与名额逐字：总奖金池 `1000` 万元、`265` 个获奖名额、"
    "单项最高 `200` 万元；赛事由虎鲸文娱集团主办，评审团首席专家唐季礼；`9` 月已启动，同期配套「虎鲸 AI 人才计划」。"
    "**⚠️ 官方报名页本期未核到（只有媒体稿与活动现场信息），报名入口与细则以官方为准。**",
    # B. Token 羊毛（4.2）
    "| 🟡 **`AIHOT` 的「Token 羊毛」免费额度聚合页（**第三方聚合层 · 逐条标核实日 · 按官方价折成人民币 · "
    "自带 `Agent` 接入与开源仓库**）** | "
    "**无结束日（聚合页，自身不设活动截止；每条按厂商截止日自动下架）** | "
    "🟡 **生效中（063 期新登记 · 第三方聚合，非厂商一手）。 ⚠️ 本期实读 `aihot.news/free-tokens`（`200` / `423,498` 字节）**："
    "页面自报 **「今天还能领 ¥201」「我的卡册 51 张」「下次刷新 还有 05:47」**；**`109` 处「核实」标注，其中 `24` 处为「11月9日核实」、"
    "`78` 处为「11月8日核实」**。**口径逐字（这是它最值得引的一条）**：「『今天还能领』只算在厂商官方页面或官方客户端里核实过的；"
    "只见社区消息的标『待官方确认』，不算进总数，**3 天内核实不了就下架**。只给在读学生的、到期会自动扣费的也不算进总数」；"
    "**不收的逐字**：「返利和邀请链接、**API 中转站（`OpenRouter` 这类模型厂商官方接入的平台不算）**、二手积分、接码多开……"
    "这里只放厂商自己的页面」。**⚠️ 折算口径**：限时加赠不折、无适用单价不折、产品内专用 `Token` 不折、按次与长期免费不折，"
    "`Token` 按「缓存命中 : 输入 : 输出 = `7 : 2 : 1`」折算。**⚠️ 本报告只把它当「发现通道」，不当一手证据** —— "
    "卡片里的额度仍需回厂商页核对（本期抽核 `AMD Token Factory` 见第三章第 `5` 节）。",
    # C. AMD Token Factory（4.2）
    "| ⚠️ **`AMD` `Radeon Token Factory` 公共免费模型 `API`（**`developer.amd.com.cn` · `OpenAI` / `Anthropic` 双兼容 · "
    "免绑卡 · 每日重置**）** | "
    "**未公布（官方只写「每日重置」，未给日历日；免费模型标 `Free` / `限时`）** | "
    "⚠️ **生效中（063 期新登记 · 额度口径三份来源互相矛盾，本期不写具体数字）。 ⚠️ 三份口径**：① 聚合页 `Token 羊毛` 标「免费」；"
    "② `Dify` 官方插件市场页（`amdtokenfactory`，作者留 `@amd.com` 邮箱）逐字 **`Daily free quota 1 USD/day, reset daily`**、"
    "`Request rate 20 requests/minute`；③ 多篇中文教程写 **「每日约 `$10` 等值」**。**差 `10` 倍，谁对不判定。**"
    "**⚠️ 官方页本期未取到逐字额度**：`developer.amd.com.cn/radeon/modelapis` 返回 `200` / `196,967` 字节，"
    "但正文是 `Loading Radeon Cloud…` + `JavaScript is required`，服务端 `HTML` 里 `Free` / `免费` / `quota` **各 `0` 命中**。"
    "**模型清单（第三方逐字）**：`DeepSeek-V4.1-Flash`（`1M`）、`GLM-5.3-Flash`（`256K`）、`Qwen3.8-Flash-Next`、`Qwen3.8-27B`、"
    "`Gemma-4-31B-IT`、`MiMo-V2.6-Flash`、`MiniCPM5-1B`。**⚠️ 按本报告规则：官方页读不到额度数字的，不登记为「已确认额度」，只登记为线索。**",
]

for n in NEW:
    n = n.rstrip() + " |"
    body.append(n)

# ---------------- 断言 ----------------
cells = Counter(len(r.strip().strip("|").split("|")) for r in body)
print("字段数分布：", cells)
assert cells == Counter({3: len(body)}), ("字段数异常（单元格里混进了竖线？）", cells)

for r in NEW:
    assert ("本期" in r) or ("063 期" in r), ("新增行缺本期标记", r[:40])

for r in NEW:
    stat = r.strip().strip("|").split("|")[2]
    for bad in ("已结束", "未开始", "已收口"):
        assert bad not in stat, ("状态列出现会被字面误读的词", bad, r[:40])

total = len(body)
assert total == PREV_41 + len(rows_42) + len(rows_led) + len(NEW), total
print("表体总行数：%d = %d + %d + %d + %d" % (total, PREV_41, len(rows_42), len(rows_led), len(NEW)))

header = "| 活动 | 截止 | 状态 |\n| --- | --- | --- |\n"
io.open(OUT, "w", encoding="utf-8", newline="\n").write(header + "\n".join(body) + "\n")

# 落盘复读（052 期纪律）
disk = io.open(OUT, encoding="utf-8").read()
disk_rows = [l for l in disk.split("\n")
             if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(disk_rows) == total, ("落盘行数", len(disk_rows))
for n in NEW:
    assert n in disk, ("新增行未进落盘文件", n[:40])
for phrase in ("`461 → 461`", "`×7.9`", "`−2,219`", "downloads 5,087 → 5,835", "`25,619`",
               "`169,627`", "`20,820`", "`159,731`", "`113,853`", "`20,111`", "`4,021`",
               "关停日已过 `3` 天", "11/22（作品征集截止", "今天还能领 ¥201", "Daily free quota 1 USD/day"):
    assert phrase in disk, ("落盘缺短语", phrase)
print("改写行：%d 条 -> %s" % (len(NOTES), "、".join(NOTES)))
print("written:", OUT, len(disk.encode("utf-8")), "bytes")
