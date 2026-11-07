# -*- coding: utf-8 -*-
"""061 期：从 060 期 md 的现行 4.1 表体 + 《常驻权益总账》全量表体
-> 基准日 2026-11-07 -> 行级改写 -> 补入本期新增行。输出 .workbuddy/tmp_table061.md。

沿用 055–060 的纪律：
  ① 输入直接取上期 md 的现行文本（不取上期的 tmp_table）。
  ② 写出后复读落盘文件再断言。
  ③ 断言用逐字短语，不用裸数字。
  ④ 全表字段数分布断言 Counter({3: N})。
  ⑤ 新增行必须带「本期」或「061 期」标记。
  ⑥ 状态列用 set_status() 整体改写（slim 只留第一句边界）。
  ⑦ 状态列不许出现 classify() 会字面误读的词。
  ⑧ （061 新增）060 期强制动作①：Vercel Labs fx 行内 3 处 059 期的「本期」重贴为「059 期」，
     让 split_ledger 的 CHANGE_RE 不再命中 —— 这是「过期措辞钩住分类正则」的销项动作。
"""
import io
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第060期-2026-11-06.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table061.md"

PREV_41 = 55
PREV_LED = 164


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
assert len(rows_41) == PREV_41, ("060 期 4.1 行数", len(rows_41))
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


# ① OpenRouter 免费档：460 / 零价 16 / :free 12，成员各换 1 个（换人在免费档）
def _or(r):
    assert "`454/16/12`" in r, ("旧计数未找到", r[:80])
    return set_status(r,
        "🟢 **生效中（动态目录）。 ⚠️（061 期）全量 `454 → 460`（`+6`）、零价 `16 → 16`、`:free` `12 → 12` —— "
        "**两个免费计数一个没动，成员各换 `1` 个**：**出** `nvidia/nemotron-3.5-content-safety:free`（`4B` 多模态护栏、"
        "`128,000` 上下文；它已从目录 `460` 条里消失，但 `/endpoints` 仍 `200` 且 `\"endpoints\": []`）；"
        "**进** `liquid/lfm-3-1.7b:free`（`$0`、`262,144` 上下文、`fp8`、`provider: Liquid`、`created` 北京 `11/7 07:57`）"
        "＋ 同款付费版 ＋ `5` 条旧模型的 `:batch` `SKU`。**⚠️ 官方描述逐字 `Prompts and outputs may be retained and used...`**。**")


edit("OpenRouter 免费档", lambda r: r.startswith("| 🟢 **OpenRouter 免费档（**官方 API 目录口径"), _or)


# ② crouton-alpha：第 5 天仍在 + 两个 inkling:free 连续第 2 期无回归
def _cr(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（061 期）上架第 `5` 天仍在**：`llms.txt` `4,021` 字节与 059 / 060 两期同值，"
        "`opencode.ai/docs/zen` 里 `crouton-alpha-free` 命中 `1` 次 —— **两站存活期第 `5` 天仍同步**；"
        "**两个 `inkling:free` 连续第 `2` 期没有回归**（两个 `/llms.txt` 仍 `404` / `10` 字节，两个 `/endpoints` 仍 "
        "`200` 但 `\"endpoints\": []`）。**⚠️ 「端点数组为空」不能反推「已下架」—— 本期 `nemotron-3.5-content-safety:free` "
        "已从目录消失、端点同为 `200` 且空，两种状态共用一个返回值。**")


edit("crouton", lambda r: r.startswith("| 🟢 **`OpenRouter` 免费隐身模型 `stealth/crouton-alpha`"), _cr)


# ③ OpenCode 免费清单 11 -> 12（新增 iceman-free）
def _oc(r):
    return set_status(r,
        "🟡 **生效中（清单动态）。 ⚠️（061 期）`11 → 12` 项，新增 `iceman-free`**：页面逐字 `Iceman Free` / "
        "`iceman-free`、端点 `opencode.ai/inference/openai/v1/chat/completions`；**页面未给厂商名、参数量、上下文或"
        "「隐身/预览」标注**，`OpenRouter` 目录 `460` 条里 `iceman` `0` 命中 —— **只在 `OpenCode` 这一侧出现**。"
        "其余 `11` 项逐条同值；页面 `58,718 → 54,653` 字节（`−4,065`）**而清单 `+1`** —— "
        "**字节变少不等于条目变少**。**")


edit("OpenCode 清单", lambda r: r.startswith("| 🟡 **`OpenCode` 免费模型清单 10 → 11 项"), _oc)


# ④ 060 期强制动作①：Vercel Labs fx 的 3 处过期「本期」重贴为「059 期」
def _fx(r):
    assert r.count("本期") == 3, ("fx 行「本期」计数异常", r.count("本期"))
    return r.replace("本期", "059 期")


edit("fx 归类修正", lambda r: r.startswith("| 🟢 **`Vercel Labs` `fx`"), _fx)


# ⑤ Kimi 访问条件：Highspeed 连续第 2 期零命中
def _kimi2(r):
    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（061 期）`?search=Kimi-K3.1-Highspeed` 仍返回 `[]`（`2` 字节）—— "
        "**官方名下 `Highspeed` 版权重连续第 `2` 期 `0` 条**；`LICENSE` `3,077` 字节与 060 期逐字节相同。"
        "**官方名下无此仓库，不写「还没放出」。**")


edit("Kimi 访问条件", lambda r: r.startswith("| ⚠️ **`Moonshot` `Kimi K3.1 Pro` 的访问条件"), _kimi2)


# ⑥ 商汤 Token Plan：五期逐字节相同
def _sn(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（061 期）`20,820` 字节 —— 与 057 / 058 / 059 / 060 四期逐字节相同**，"
        "`公测期完全免费开放`／`限时放量`／`6.8 Flash Lite`／`U1 Fast`／`¥ 0` 各 `1` 次，**仍无截止日**。**")


edit("商汤 Token Plan", lambda r: r.startswith("| 🟢 **商汤 `日日新 SenseNova` Token Plan 公测免费档"), _sn)


# ⑦ 小浣熊：159,731 逐字节相同
def _xxh(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（061 期）`159,731` 字节与 060 期逐字节相同**：`免费版` `2` / `¥ 0` `2` / `/永久` `2` / "
        "`300` `7` 逐字全在。**")


edit("小浣熊免费版", lambda r: r.startswith("| 🟢 **商汤 `小浣熊`（Raccoon）免费版"), _xxh)


# ⑧ 商汤 6.8 Flash：news 页 -1,392 字节而关键词仍零命中
def _sn68(r):
    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（061 期）`sensetime.com/cn/news` `115,245 → 113,853` 字节（`−1,392`），"
        "`SenseNova 6.8` 命中 `2` 次仍在；**该页 `限时` 与 `免费` 仍各 `0` 命中**，`token-plan` `20,820` 字节逐字节同 —— "
        "**「限时免费」仍只有媒体口径**（连续第 `5` 期）。**")


edit("商汤 6.8 Flash", lambda r: r.startswith("| ⚠️ **商汤 `SenseNova 6.8 Flash` 上线"), _sn68)


# ⑨ 百度 ERNIE 首次复核
def _ernie(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（061 期首次复核）许可与仓库三处关键字段全部未变**：`LICENSE` 恰为 `25,619` 字节（与 060 期逐字节同）、"
        "`Release date: November 5, 2026` 与 `Exhibit A` 的 `Last revised: November 6, 2026` 均未动、"
        "`Territory` 仍逐字排除欧盟／英国／韩国；两个仓库 `lastModified` 仍停在 `2026-11-05T06:33Z` / `06:37Z`、"
        "`siblings` 各 `139`。**流通量变了、条款没变**：`FP8` 仓库 `downloads 13 → 526`、`likes 191 → 211`，"
        "`BF16` 仓库 `downloads 11 → 241`、`likes 39 → 39`（**按避坑 249，`downloads` 是近 `30` 天滚动窗口，不是累计量**）。")


edit("ERNIE 复核", lambda r: r.startswith("| 🟢 **百度开源 `ERNIE-5.5-Flash-Base`"), _ernie)


# ⑩ 豆包工作 30 天订阅：拿到规则变化（媒体口径），官方页仍零命中
def _db(r):
    return set_status(r,
        "🟢 **生效中（022 期登记）。 ⚠️ 第三方整理口径，以客户端订阅页为准。 ⚠️（061 期）本轮拿到的是「额度规则变化」"
        "而非本行的订阅活动**：`11/6` 起个人版取消 `5` 小时短周期额度限制（媒体逐字），**周额度不变**；"
        "`volcengine.com/product/doubao-work` `169,559` 字节与 `doubao.com/work` `57,171` 字节，`5小时` / `周额度` / "
        "`额度` / `免费` **各 `0` 命中** —— **订阅活动本身仍未拿到一手**。")


edit("豆包工作订阅", lambda r: r.startswith("| 🟢 **豆包工作 30 天订阅（新一轮）**"), _db)


# ---------------- 本期补入行 ----------------
NEW = [
    "| 🟢 **豆包工作个人版取消 `5` 小时额度限制（**061 期新登记 · **限额窗口规则变化，不是额度变多** · `11/6` 起 · "
    "**媒体口径，官方两页零命中**）** | **无结束日（产品规则，非活动期）** | "
    "🟢 **生效中。 ⚠️（061 期）逐字「个人用户不再受到 `5` 小时短周期额度限制，可以在周额度范围内，根据实际工作节奏灵活安排使用时间。"
    "**周额度及其他使用规则仍以对应套餐为准**」** —— **改的是「一周内怎么花」，不是「能花多少」**。"
    "**首发**：雷峰网 `11/6 16:29`（`200` / `48,312` 字节），新京报 / 澎湃 / 每日经济新闻同稿，**全部「记者获悉」**；"
    "**官方页**：`volcengine.com/product/doubao-work`（`200` / `169,559` 字节）与 `doubao.com/work`（`200` / `57,171` 字节），"
    "`5小时` / `周额度` / `额度` / `免费` **各 `0` 命中**。**读者可自查**：客户端「设置-订阅与额度管理」。** |",

    "| 🟢 **`Ripple-65B Preview` 开放权重（**061 期补登 · 仓库建于 `11/4`，058–060 三期均未登记** · `65B` 稠密 · `12` 万亿 tokens · "
    "`1M` 上下文 · **`Apache-2.0` 全文 `11,357` 字节** · `TerminalBench 2.1` `80.52`）** | "
    "**无结束日（`Apache-2.0` 开源权重，无活动期）** | "
    "🟢 **生效中。 ⚠️（061 期）一手**：`hf-mirror.com/api/models/ricursiveAI/Ripple-65B-Preview`（`200` / `5,386` 字节）—— "
    "`createdAt 2026-11-04T02:41Z`、`lastModified 2026-11-06T19:26Z`、`downloads 2,013`、`likes 333`、`siblings 31` 个、"
    "`license:apache-2.0`；`LICENSE` 为 `Apache License Version 2.0` 全文（`11,357` 字节，标准许可、无附加条款）；"
    "模型卡逐字 `65B parameter dense Transformer model pretrained on 12 trillion tokens with support for up to 1Mi "
    "(1,048,576 tokens) of context`、`80.52 on TerminalBench 2.1`；官方页自述训练成本 `US$32M`。"
    "**四层开放全过**：能用（指令微调版 `BF16` ＋ `NVFP4`）／能下载（`31` 个 `siblings`）／能跑（官方称可跑 `DGX Spark`）／"
    "**能商用（`Apache-2.0`，无地域与营收门槛）**。**⚠️ `OpenRouter` 上同款为付费档**（`ricursiveai/ripple-65b-preview`、"
    "`$0.2` / `$0.6` 每百万 tokens、`1,048,576` 上下文，`created` 北京 `11/5 03:03`）—— **权重免费不等于端点免费**。** |",
]

for n in NEW:
    body.append(n)

# ---------------- 断言 ----------------
cells = Counter(len(r.strip().strip("|").split("|")) for r in body)
print("字段数分布：", cells)
assert cells == Counter({3: len(body)}), ("字段数异常（单元格里混进了竖线？）", cells)

for r in NEW:
    assert ("本期" in r) or ("061 期" in r), ("新增行缺本期标记", r[:40])

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
assert "`454 → 460`" in disk, "OpenRouter 计数未改写"
assert "liquid/lfm-3-1.7b:free" in disk, "新免费档未落盘"
assert "nemotron-3.5-content-safety:free" in disk, "消失条目未落盘"
assert "iceman-free" in disk, "OpenCode 新增未落盘"
assert "Ripple-65B" in disk, "Ripple 补登未落盘"
assert "豆包工作个人版取消" in disk, "豆包额度行未落盘"
assert "11,357" in disk, "Ripple 许可字节未落盘"
assert "526" in disk, "ERNIE downloads 未落盘"
assert "113,853" in disk, "商汤 news 字节未落盘"
assert "159,731" in disk, "小浣熊未落盘"
assert "4,021" in disk, "crouton 未落盘"
# ⑤ fx 行不再含「本期」
fxrows = [r for r in disk_rows if r.startswith("| 🟢 **`Vercel Labs` `fx`")]
assert len(fxrows) == 1, ("fx 行数", len(fxrows))
assert "本期" not in fxrows[0], "fx 行仍含过期「本期」"
assert "059 期只是首次登记" in fxrows[0], "fx 行未重贴期号"
print("改写行：%d 条 -> %s" % (len(NOTES), "、".join(NOTES)))
print("written:", OUT, len(disk.encode("utf-8")), "bytes")
