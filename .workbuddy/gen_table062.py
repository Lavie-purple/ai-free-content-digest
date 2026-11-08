# -*- coding: utf-8 -*-
"""062 期：从 061 期 md 的现行 4.1 表体 + 《常驻权益总账》全量表体
-> 基准日 2026-11-08 -> 行级改写 -> 补入本期新增行。输出 .workbuddy/tmp_table062.md。

沿用 055–061 的纪律：
  ① 输入直接取上期 md 的现行文本（不取上期的 tmp_table）。
  ② 写出后复读落盘文件再断言。
  ③ 断言用逐字短语，不用裸数字。
  ④ 全表字段数分布断言 Counter({3: N})（单元格里不许混进竖线）。
  ⑤ 新增行必须带「本期」或「062 期」标记。
  ⑥ 状态列用 set_status() 整体改写（slim 只留第一句边界）。
  ⑦ 状态列不许出现 classify() 会字面误读的词。
  ⑧ 活动名列**一个字不动**（改名会让下一期 split_ledger 的键匹配断掉）。
"""
import io
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第061期-2026-11-07.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table062.md"

PREV_41 = 55
PREV_LED = 166


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
assert len(rows_41) == PREV_41, ("061 期 4.1 行数", len(rows_41))
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


# ① OpenRouter 免费档：461 / 16 / 12，成员全未换、消失的是 Inception 整族
def _or(r):
    assert "`454/16/12`" in r, ("旧计数未找到", r[:80])
    assert "本期" not in r or True
    new = set_status(r,
        "🟢 **生效中（动态目录）。 ⚠️（062 期）全量 `460 → 461`（`+1`）、零价 `16 → 16`、`:free` `12 → 12` —— "
        "**两个免费计数一个没动，免费区成员本期一个都没换**；**进 `4` 条全是 `:batch`**（`deepseek-v4.1-flash-1017` / "
        "`morph-v3-fast` / `morph-v3-large` / `glm-5.2`），**出 `3` 条是 `Inception` 整族**（`mercury-2` / `2.5` / `3`，"
        "`461` 条里 `inception` 关键字 `0` 命中）。**⚠️ 净值 `+1` 掩盖了两个方向。**")
    # 活动名列只改括号里的三个计数，语义与键名不动
    assert new.count("`454/16/12`") == 1, "活动名里的旧计数没找到"
    return new.replace("`454/16/12`", "`461/16/12`")


edit("OpenRouter 免费档", lambda r: r.startswith("| 🟢 **OpenRouter 免费档（**官方 API 目录口径"), _or)


# ② OpenCode 免费清单：三套口径 12/12/13，退 Pulse 进 Inkling
def _oc(r):
    return set_status(r,
        "🟡 **生效中（清单动态）。 ⚠️（062 期）三套口径全部同值、成员各换 `1` 个**：`-free` 后缀 `12 → 12`、"
        "价格表三列全 `Free` 的 `12 → 12`、「输入与输出都 `Free`」的 `13 → 13`；**出** `Pulse Alpha Free`"
        "（弃用表逐字 `November 6, 2026`）、**进** `Inkling 2 Small Free`。**页面 `54,653 → 99,283` 字节（`+44,630`）"
        "涨的是条款与地区限制，不是模型数。**")


edit("OpenCode 清单", lambda r: r.startswith("| 🟡 **`OpenCode` 免费模型清单 10 → 11 项"), _oc)


# ③ crouton 第 6 天
def _cr(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（062 期）上架第 `6` 天仍在**：`llms.txt` `4,021` 字节与 059–061 三期逐字节相同，"
        "`opencode.ai/docs/zen` 里 `crouton-alpha-free` 命中 `1` 次；**同页本期多了一句定性** "
        "`Crouton Alpha Free is a stealth model`，且**留存 `30` 天、不用于训练**。**两个 `inkling:free`（第一代）仍不回归。**")


edit("crouton", lambda r: r.startswith("| 🟢 **`OpenRouter` 免费隐身模型 `stealth/crouton-alpha`"), _cr)


# ④ Ripple：downloads 5,087 / likes 382 / 四个仓库
def _rp(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（062 期）两天 `downloads 2,013 → 5,087`（`+152.6%`）、`likes 333 → 382`**，"
        "`lastModified` 仍 `2026-11-06T19:26:32Z`（仓库文件一个没动）、`siblings` 仍 `31`。**061 期问的两个变体都在**："
        "`ricursiveAI` 名下 `4` 个仓库（`-NVFP4` `2,481` dl / `-DFlash2` `2,507` dl / `Base-Preview` `340` dl）。"
        "**⚠️ `downloads` 是近 `30` 天滚动窗口，不是累计。**")


edit("Ripple", lambda r: r.startswith("| 🟢 **`Ripple-65B Preview` 开放权重（**061 期补登"), _rp)


# ⑤ ERNIE 第 2 次复核
def _ernie(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（062 期第 `2` 次复核）许可 `LICENSE` 仍恰为 `25,619` 字节（逐字节同）、两个仓库 "
        "`lastModified` 仍停在 `2026-11-05T06:33Z` / `06:37Z`**；流通量：`FP8` `downloads 526 → 1,400`、`likes 211 → 225`，"
        "`BF16` `downloads 241 → 503`、`likes 39 → 384`（**两个同类仓库 `likes` 增速差 `24` 倍，本报告不解释成因**）。")


edit("ERNIE 复核", lambda r: r.startswith("| 🟢 **百度开源 `ERNIE-5.5-Flash-Base`"), _ernie)


# ⑥ 豆包工作 30 天订阅：官方两页仍零命中（第 18 期）
def _db(r):
    return set_status(r,
        "🟢 **生效中（022 期登记）。 ⚠️ 第三方整理口径，以客户端订阅页为准。 ⚠️（062 期）官方两页字节都变了、"
        "四项关键词仍全零**：`volcengine.com/product/doubao-work` `169,559 → 169,627`、`doubao.com/work` "
        "`57,171 → 57,887`，`5小时` / `周额度` / `额度` / `免费` **各 `0` 命中** —— **订阅活动本身连续第 `18` 期无一手。**")


edit("豆包工作订阅", lambda r: r.startswith("| 🟢 **豆包工作 30 天订阅（新一轮）**"), _db)


# ⑦ 豆包工作个人版取消 5 小时限制：媒体口径无补稿
def _dbq(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（062 期）仍只有媒体口径，官方无补稿**：两个官方页四项关键词各 `0` 命中，"
        "**距首发已 `2` 天**。**改的是「一周内怎么花」，不是「能花多少」** —— 读者可自查客户端「设置-订阅与额度管理」。**")


edit("豆包额度规则", lambda r: r.startswith("| 🟢 **豆包工作个人版取消 `5` 小时额度限制"), _dbq)


# ⑧ 商汤 Token Plan：第 6 期逐字节同
def _sn(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（062 期）`20,820` 字节 —— 与 057–061 五期逐字节相同**，`公测期完全免费开放` / `限时放量` / "
        "`¥ 0` 各 `1` 次，**`截止` 仍 `0` 命中**、仍无截止日。**")


edit("商汤 Token Plan", lambda r: r.startswith("| 🟢 **商汤 `日日新 SenseNova` Token Plan 公测免费档"), _sn)


# ⑨ 小浣熊：159,731 第 6 期同值
def _xxh(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（062 期）`159,731` 字节与 057–061 五期逐字节相同**：`免费版` `2` / `¥ 0` `2` / `/永久` `2` / "
        "`300` `7` 逐字全在。**")


edit("小浣熊免费版", lambda r: r.startswith("| 🟢 **商汤 `小浣熊`（Raccoon）免费版"), _xxh)


# ⑩ 商汤 6.8 Flash：news 页同值而关键词仍零命中（第 6 期）
def _sn68(r):
    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（062 期）`sensetime.com/cn/news` `113,853` 字节 —— 与 061 期逐字节相同**，"
        "`SenseNova 6.8` 命中 `2` 次仍在；**`限时` 与 `免费` 仍各 `0` 命中** —— **「限时免费」仍只有媒体口径（连续第 `6` 期），"
        "官方页面连字节都没变。**")


edit("商汤 6.8 Flash", lambda r: r.startswith("| ⚠️ **商汤 `SenseNova 6.8 Flash` 上线"), _sn68)


# ⑪ AXON：20,111 第 5 期、无许可证
def _axon(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（062 期）`20,111` 字节 —— 与 058–061 四期逐字节相同**，`license` / `LICENSE` / `version` / "
        "`Apache` **各 `0` 命中 —— 连续第 `5` 期无许可证与版本号**，仍标 `Free forever`、无需账号。**")


edit("AXON", lambda r: r.startswith("| 🟢 **`AXON Developer Edition`"), _axon)


# ⑫ Kimi Highspeed 连续第 3 期零命中
def _kimi(r):
    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（062 期）`?search=Kimi-K3.1-Highspeed` 仍返回 `[]`（`2` 字节）—— "
        "**官方名下 `Highspeed` 版权重连续第 `3` 期 `0` 条**。**官方名下无此仓库，不写「还没放出」。**")


edit("Kimi 访问条件", lambda r: r.startswith("| ⚠️ **`Moonshot` `Kimi K3.1 Pro` 的访问条件"), _kimi)


# ⑬⑭ 两条 Ollie：截止日已过 2 天（055 期纪律：跨过基准日 -> 改写为「已过 N 天」）
def _ollie1(r):
    return set_status(r,
        "⚠️ **关停日已过 `2` 天。 ⚠️（062 期）告别信三页仍逐字节同值在线**（`39,747` / `41,791` / `107,182`）；"
        "**页面在线不等于服务在线** —— 官方无逐字口径，本报告不判定服务是否已停。**")


edit("Ollie 关停", lambda r: r.startswith("| ⚠️ **`Ollie`（隐私向 AI 助手）宣布关停"), _ollie1)


def _ollie2(r):
    return set_status(r,
        "⚠️ **关停日已过 `2` 天。 ⚠️（062 期）定价页 `41,791` 字节三期间值**，`50 messages … per month` / "
        "`6 free additional messages … every day` 逐字仍在；**`Free` 档是否一并停服仍无官方口径。**")


edit("Ollie Free 档", lambda r: r.startswith("| ⚠️ **`Ollie` 的 `Free` 档"), _ollie2)


# ---------------- 本期补入行 ----------------
NEW = [
    "| 🟢 **`OpenCode` 的 `Inkling 2 Small Free`（**062 期新登记 · `Thinking Machines` 第二代模型 · 权重**未放**、"
    "但**分发层免费** · 价格表三列 `Free` · **会留存数据且可能用于训练** · **十个地区不可用**）** | "
    "**无结束日（官方逐字 `free on OpenCode for a limited time`，未给具体日期）** | "
    "🟢 **生效中。 ⚠️（062 期）一手**：`opencode.ai/docs/zen`（`200` / `99,283` 字节）价格表逐字 `Inkling 2 Small Free` / "
    "`Free` / `Free` / `Free` / `-`（输入 / 输出 / 缓存读）；条款逐字 `free on OpenCode for a limited time. Its provider "
    "retains your data and may use it for model training`；**不可用地区十个**（欧盟、冰岛、列支敦士登、挪威、古巴、伊朗、"
    "朝鲜、俄罗斯、乌克兰、委内瑞拉）。**⚠️ 同一模型三处「拿不到权重」同时成立**：`hf-mirror.com/api/models?author="
    "thinkingmachines`（`2,668` 字节）`6` 个仓库**无 `Inkling-2-Small`**；`OpenRouter` `461` 条**无第二代**；官方 "
    "`Tinker` 页（`602,272` 字节）**`free` / `credit` 各 `0` 命中**、`serverless` 按 tokens 计费。**「用得上、拿不走、还要交数据」"
    "—— 不写成「开源了」。** |",
]

for n in NEW:
    body.append(n)

# ---------------- 断言 ----------------
cells = Counter(len(r.strip().strip("|").split("|")) for r in body)
print("字段数分布：", cells)
assert cells == Counter({3: len(body)}), ("字段数异常（单元格里混进了竖线？）", cells)

for r in NEW:
    assert ("本期" in r) or ("062 期" in r), ("新增行缺本期标记", r[:40])

for r in NEW:
    stat = r.strip().strip("|").split("|")[2]
    for bad in ("已结束", "未开始", "已收口"):
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
assert "`461/16/12`" in disk, "OpenRouter 活动名计数未改写"
assert "`460 → 461`" in disk, "OpenRouter 全量计数未改写"
assert "Inception" in disk, "Inception 整族消失未落盘"
assert "`+44,630`" in disk, "OpenCode 字节差未落盘"
assert "downloads 2,013 → 5,087" in disk, "Ripple downloads 未落盘"
assert "`25,619`" in disk, "ERNIE 许可字节未落盘"
assert "`4,021`" in disk, "crouton 未落盘"
assert "`20,820`" in disk, "商汤 token-plan 未落盘"
assert "`159,731`" in disk, "小浣熊未落盘"
assert "`113,853`" in disk, "商汤 news 未落盘"
assert "`20,111`" in disk, "AXON 未落盘"
assert "Inkling 2 Small Free" in disk, "Inkling 免费档未落盘"
assert "关停日已过 `2` 天" in disk, "Ollie 天数未改写"
print("改写行：%d 条 -> %s" % (len(NOTES), "、".join(NOTES)))
print("written:", OUT, len(disk.encode("utf-8")), "bytes")
