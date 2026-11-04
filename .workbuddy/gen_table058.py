# -*- coding: utf-8 -*-
"""058 期：从 057 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-11-04
-> 行级改写 -> 追加本期新增行。输出 .workbuddy/tmp_table058.md（纯表格块）。

沿用 055–057 的纪律：
  ① 输入直接取上期 md 的现行文本（不取上期的 tmp_table）。
  ② 写出行必须真的进落盘文件 —— 写出后复读断言。
  ③ 断言用逐字短语，不用裸数字（避坑 248）。
  ④ 字段数分布断言 Counter({3: N})（避坑 242 的表格版）。
  ⑤ 新增行必须带「本期」或「058 期」标记，否则会被 split_ledger 当「无变化」移进总账（054 期踩过）。
  ⑥ 新增：改写后的行里不许出现「已结束 / 未开始」这类会被 classify() 字面误读的词（避坑 239）。
"""
import io
import re
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第057期-2026-11-03.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table058.md"

PREV_41 = 55
PREV_LED = 160


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
assert len(rows_41) == PREV_41, ("057 期 4.1 行数", len(rows_41))
assert len(rows_led) == PREV_LED, ("总账行数", len(rows_led))
body = rows_41 + rows_led
print("输入行数：4.1 = %d，总账 = %d，合计 = %d" % (len(rows_41), len(rows_led), len(body)))

# ---------------- 行级改写 ----------------
NOTES = []


def append_note(row, note):
    r = row.rstrip()
    assert r.endswith("|"), r[-20:]
    base = r[:-1].rstrip()
    return base + " " + note + " |"


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


# ① OpenRouter：451/17/14 -> 455/18/14（+4：crouton-alpha / hy4 / grok 两条 batch；零价 +1）
def _or(r):
    assert "`451/17/14`" in r, ("旧计数未找到", r[:80])
    r = r.replace("`451/17/14`", "`455/18/14`")
    return append_note(r,
        "**⚠️（058 期）官方目录重取：全量 `451 → 455`（新增 `4`、消失 `0`）、零价 `17 → 18`、`:free` `14` 同值**；"
        "**新增四条** `stealth/crouton-alpha`（**零价** · 北京 `11/3 09:38`）／`tencent/hy4`（付费 · 北京 `11/4 12:20`）／"
        "`x-ai/grok-4.6:batch` 与 `x-ai/grok-4.7:batch`（**`created` 都在 9 月，是 `:batch` 变体首次进目录、不是新品**）；"
        "**`:free` 的 `14` 条逐条 ID 完全不变** —— **零价档变了、`:free` 档没变，两者不是同一口径**。")


edit("OpenRouter 免费档", lambda r: r.startswith("| 🟢 **OpenRouter 免费档（**官方 API 目录口径"), _or)


# ② Kimi K3.1 Pro 发布（4.1）：到期日当天，权重仍未放出
def _kimi_rel(r):
    return append_note(r,
        "**⚠️（058 期）承诺到期日当天实核：`HF` 官方 `moonshotai` 名下仍 `19` 个模型、含 `K3.1` 的 `0` 条；"
        "`GitHub` `MoonshotAI` `42` 个仓库无 `K3.1` 仓库、`Kimi-K3` 仓库 `releases` 为 `0` 条** —— "
        "**官方文档页那句承诺逐字未改（命中 `3` 次）、也没有任何延期说明；今天 `T+0`。**")


edit("Kimi 发布", lambda r: r.startswith("| 🟢 **`Moonshot` `Kimi K3.1 Pro` 发布（10/23 晚–10/24"), _kimi_rel)


# ③ Kimi K3.1 Pro 访问条件（4.2）
def _kimi_acc(r):
    return append_note(r,
        "**⚠️（058 期）`HF` 全站搜索 `Kimi-K3.1` 只有 `1` 条结果，且是第三方仓库 "
        "`audnai/penclaw-Kimi-K3.1-pro-unrestricted`（`createdAt 2026-10-23T21:38:11Z`、`downloads 0`、`likes 123`）"
        " —— **不是官方权重，本报告不把它记成「已放出」**；官方名下仍 `0` 条。**")


edit("Kimi 访问条件", lambda r: r.startswith("| ⚠️ **`Moonshot` `Kimi K3.1 Pro` 的访问条件"), _kimi_acc)


# ④ Antigravity 6 个月免费档：+200 字节、三处逐字同值（并纠正「没有任何数字」）
def _ag(r):
    return append_note(r,
        "**⚠️（058 期）定价页 `137,395 → 137,595` 字节（`+200`），三处关键逐字命中数完全相同"
        "（`Generally Available` `1`／`$0/month` `1`／`Basic weekly rate limits` `1`）—— "
        "**价格写明、额度没写**（`$0/month` 就是一个数字，057 期「没有任何数字」的表述本期更正）；"
        "`/models` 连续第 `6` 期 `404`。**")


edit("Antigravity 免费档", lambda r: r.startswith("| 🟡 **`Google Antigravity` 科研 / 安全 6 个月免费档"), _ag)


# ⑤ Runware pruna-p-video-edit：11/3 已跨过基准日（T-1），改写状态列（不放宽重算器）
def _pruna(r):
    new = r.replace("距结束 `0` 天**）**", "已过 `1` 天**）**")
    new = new.replace("🟢 **生效中（本期新核到一手 · 距结束 `0` 天）。",
                      "🟢 **截止日已过（官方 `endsAt 2026-11-03`，本期基准日 `11/4`，已过 `1` 天）。")
    assert "距结束 `0` 天" not in new, "距结束 0 天未替换干净"
    return append_note(new,
        "**⚠️（058 期）官方数组里仍在、`endsAt` 逐字仍是 `2026-11-03`** —— "
        "**「数组里还在」不等于「活动还在售」**（避坑 230 第四次实证）。")


edit("Runware p-video-edit", lambda r: r.startswith("| 🟢 **`Runware` 分发层 `pruna-p-video-edit` 促销 `25% OFF`"), _pruna)


# ⑥ Ollie 关停 + Free 档 + 信息分散实证：距 11/6 剩 2 天
def _ollie1(r):
    return append_note(r,
        "**⚠️（058 期）`farewell` 与定价页两页与上期逐字节相同（`39,747` / `41,791`），"
        "`Ollie is sunsetting on Nov 6, 2026` 逐字未改 —— 距今 `2` 天。**")


edit("Ollie 关停", lambda r: r.startswith("| ⚠️ **`Ollie`（隐私向 AI 助手）宣布关停"), _ollie1)


def _ollie2(r):
    return append_note(r,
        "**⚠️（058 期）定价页 `Free` / `$0` / `50 messages from Ollie per month` / "
        "`6 free additional messages from Ollie every day` 逐字同值 —— 距今 `2` 天。**")


edit("Ollie Free 档", lambda r: r.startswith("| ⚠️ **`Ollie` 的 `Free` 档"), _ollie2)


def _ollie3(r):
    # 057 期在这行留了「关停距今 `3` 天」；本行截止列是「无活动期」，不带天数
    # （normalize 只处理能解析出日期的行，所以这处必须在这里改）
    assert "关停距今 `3` 天" in r, "057 期遗留天数未找到"
    r = r.replace("关停距今 `3` 天。", "关停日仍是 `11/6`（倒计天数记在同节另外两行）。")
    return append_note(r,
        "**⚠️（058 期）首页仍未出现关停字样（两期同结论）** —— **本行截止列是「无活动期」的口径记录行，"
        "故不写天数**（`11/6` 的倒计时记在同节另外两行）。")


edit("Ollie 信息分散", lambda r: r.startswith("| ⚠️ **一条「信息分散在子页」的实证：`Ollie`"), _ollie3)


# ⑦ 小浣熊：页面 +10,918 字节、免费档未动；并记「短语被 DOM 切碎」这条实证
def _xxh(r):
    return append_note(r,
        "**⚠️（058 期）`xiaohuanxiong.com/pricing` `147,400 → 158,318` 字节（`+10,918`）：新增的全是付费档对比内容"
        "（`¥29.9 /月起` 的 `500 积分/日` ＋ `额外 10000 积分/月`；`¥1599 起/年/人` 的 `1000 积分/日/人`），"
        "**免费档一行未动**；**整页 `grep` `每日 0 点重置` 命中 `0` 次 → 剥标签拼接后原文完好**"
        "（源码里被切成 `每日` ＋ `<b>0</b>` ＋ `点重置` 三段，避坑 258）。")


edit("小浣熊免费版", lambda r: r.startswith("| 🟢 **商汤 `小浣熊`（Raccoon）免费版"), _xxh)


# ⑧ 商汤 Token Plan：逐字节相同
def _sn(r):
    return append_note(r,
        "**⚠️（058 期）`www.sensenova.cn/token-plan` `200` / `20,820` 字节 —— 与 057 期逐字节相同**，"
        "`公测期完全免费开放`／`限时放量`／`6.8 Flash Lite`／`U1 Fast` 各命中 `1` 次，**仍无截止日**。")


edit("商汤 Token Plan", lambda r: r.startswith("| 🟢 **商汤 `日日新 SenseNova` Token Plan 公测免费档"), _sn)


# ---------------- 本期新增行 ----------------
NEW = [
    # 1) OpenRouter 免费隐身模型
    "| 🟢 **`OpenRouter` 免费隐身模型 `stealth/crouton-alpha`（**058 期新登记 · `$0` · `1,048,576` 上下文 · "
    "**无公告、无厂商页、只有一家 provider `Stealth`**）** | **未公布（官方页无 `limited time`、无 `trial`、无截止日）** | "
    "🟢 生效中。**官方逐字**：模型页 meta `Crouton Alpha is a lightweight model built for scalable coding, agentic, "
    "and multimodal workflows. This model is free to use. 1,048,576 token context window.`；"
    "`llms.txt` 定价段 `- Stealth: Free`、`Pay-as-you-go with no markup on the provider's price.`；"
    "目录字段 `\"pricing\":{\"prompt\":\"0\",\"completion\":\"0\"}`、`\"created\":1793669930`（＝北京 `11/3 09:38`）。"
    "**⚠️ 三条边界**：① **没有 `:free` 后缀、页面上没有任何「每日 N 次」的额度说明 —— 本报告不替它编一个额度**；"
    "② **`announcements` 全文 `crouton` 命中 `0` 次**，这条上架官方一句话没说；③ **「谁做的」官方也没回答**"
    "（`creator` meta 逐字 `stealth`）。 |",

    # 2) AXON Developer Edition
    "| 🟢 **`AXON Developer Edition`（**058 期新登记 · 本地 AI 协处理器 · `Rust` 写 · **免费但不开源**）** | "
    "**无结束日（官方逐字 `Free forever` 区块与 `No trial, no paywall, no subscription`；未给任何活动期）** | "
    "🟢 生效中。**官方逐字**：`AXON is a local AI co-processor that runs on your own machine.`、"
    "`Windows 10/11 · Free · No account required`、`Developer Edition is the full build. No trial, no paywall, "
    "no subscription.`、`AXON is not an AI model. It has no large language model, no cloud dependency, "
    "no inference subscription.`。**四层开放**：能用 ✔／能下载 ✔／能跑 ✔（**仅 Windows**，`macOS` 与 `Linux` 各 `0` 命中）／"
    "**能商用 ✘ —— 全页 `open source`、`license`、`MIT`、`Apache` 各命中 `0` 次，许可证一个字都没写**"
    "（**没有许可证既不等于禁止商用、也不等于允许商用，本报告不替它选边**）。 |",
]

for n in NEW:
    body.append(n)

# ---------------- 断言 ----------------
cells = Counter(len([c for c in r.strip().strip("|").split("|")]) for r in body)
print("字段数分布：", cells)
assert cells == Counter({3: len(body)}), ("字段数异常（单元格里混进了竖线？）", cells)

for r in NEW:
    assert ("本期" in r) or ("058 期" in r), ("新增行缺本期标记", r[:40])

# 避坑 239：改写/新增行的状态列不许出现会被 classify() 字面误读的词
for r in NEW:
    stat = r.strip().strip("|").split("|")[2]
    for bad in ("已结束", "未开始", "已收口"):
        assert bad not in stat, ("状态列出现会被字面误读的词", bad, r[:40])

total = len(body)
assert total == PREV_41 + PREV_LED + len(NEW), total
print("表体总行数：%d = %d + %d + %d" % (total, PREV_41, PREV_LED, len(NEW)))

header = "| 活动 | 截止 | 状态 |\n| --- | --- | --- |\n"
io.open(OUT, "w", encoding="utf-8", newline="\n").write(header + "\n".join(body) + "\n")

# 落盘复读（052 期纪律：断言必须校验落盘文件，不是内存对象）
disk = io.open(OUT, encoding="utf-8").read()
disk_rows = [l for l in disk.split("\n")
             if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(disk_rows) == total, ("落盘行数", len(disk_rows))
for n in NEW:
    assert n in disk, ("新增行未进落盘文件", n[:40])
assert "`455/18/14`" in disk and "`451/17/14`" not in disk, "OpenRouter 三档计数未改写"
assert "已过 `1` 天**）**" in disk or "已过 `1` 天" in disk, "pruna 状态未改写"
assert "距结束 `0` 天" not in disk, "仍有「距结束 0 天」"
assert "audnai/penclaw" in disk, "Kimi 第三方仓库事实未落盘"
print("改写行：%d 条 -> %s" % (len(NOTES), "、".join(NOTES)))
print("written:", OUT, len(disk.encode("utf-8")), "bytes")
