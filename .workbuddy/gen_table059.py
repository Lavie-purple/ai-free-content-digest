# -*- coding: utf-8 -*-
"""059 期：从 058 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-11-05
-> 行级改写 -> 追加本期新增行。输出 .workbuddy/tmp_table059.md。

沿用 055–058 的纪律：
  ① 输入直接取上期 md 的现行文本（不取上期的 tmp_table）。
  ② 写出行必须真的进落盘文件 —— 写出后复读断言。
  ③ 断言用逐字短语，不用裸数字。
  ④ 全表字段数分布断言 Counter({3: N})。
  ⑤ 新增行必须带「本期」或「059 期」标记。
  ⑥ 新增/改写行的状态列不许出现 classify() 会字面误读的词（避坑 239）。
"""
import io
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第058期-2026-11-04.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table059.md"

PREV_41 = 55
PREV_LED = 162


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
assert len(rows_41) == PREV_41, ("058 期 4.1 行数", len(rows_41))
assert len(rows_led) == PREV_LED, ("总账行数", len(rows_led))
body = rows_41 + rows_led
print("输入行数：4.1 = %d，总账 = %d，合计 = %d" % (len(rows_41), len(rows_led), len(body)))

NOTES = []


def append_note(row, note):
    r = row.rstrip()
    assert r.endswith("|"), r[-20:]
    base = r[:-1].rstrip()
    return base + " " + note + " |"


def set_status(row, status):
    """整体改写状态列（不是追加）。

    ⚠️ 059 期踩到的坑：slim_table.py 只保留「第一句边界」，追加在尾部的注
       会在瘦身时被裁掉（054 期纪律③的第三种形态）。所以本期改成直接改写状态列，
       让当期事实成为「第一句边界」。
    """
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


# ① OpenRouter 免费档：455/18/14 -> 454/16/12（两个 :free 整批摘下）
def _or(r):
    assert "`455/18/14`" in r, ("旧计数未找到", r[:80])
    r = r.replace("`455/18/14`", "`454/16/12`")
    return set_status(r,
        "🟢 **生效中（动态目录）。 ⚠️（059 期）全量 `455 → 454`、零价 `18 → 16`、`:free` `14 → 12`；"
        "**两个 `:free` 档整批摘下**（`thinkingmachines/inkling:free` 与 `inkling-small:free`），"
        "**付费版原价原上下文一字未动**；新增 `ricursiveai/ripple-65b-preview`（付费 · 北京 `11/5 03:03`）；"
        "**`announcements` 全文 `inkling` 命中 `0` 次**。**")


edit("OpenRouter 免费档", lambda r: r.startswith("| 🟢 **OpenRouter 免费档（**官方 API 目录口径"), _or)


# ② crouton-alpha：第 3 天仍在 + OpenCode 出现 crouton-alpha-free
def _cr(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（059 期）上架第 `3` 天仍在**：`created 1793669930` 未变、`pricing` 仍 `0/0`、"
        "`1,048,576` 上下文、`llms.txt` `4,021` 字节逐字节相同；**并且多了第二个入口** —— "
        "`opencode.ai/docs/zen` 新增 `Crouton Alpha Free`（id `crouton-alpha-free`），清单 `10 → 11`，"
        "**同一隐身模型第一次带 `-free` 后缀出现在别家目录**。**")


edit("crouton", lambda r: r.startswith("| 🟢 **`OpenRouter` 免费隐身模型 `stealth/crouton-alpha`"), _cr)


# ③ OpenCode 免费清单 10 -> 11（新增 crouton-alpha-free）
def _oc(r):
    return set_status(r,
        "🟡 **生效中（清单动态）。 ⚠️（059 期）`10 → 11`：新增 `crouton-alpha-free`（行名 `Crouton Alpha Free`）；"
        "`LongCat 2.5 Preview Free` 仍 `0` 命中；页面 `57,838 → 58,736` 字节（`+898`）。**")


edit("OpenCode 清单", lambda r: r.startswith("| 🟡 **`OpenCode` 免费模型清单 10 → 11 项"), _oc)


# ④ Kimi K3.1 Pro 发布：权重已公开（改写状态列，不是贴一句注）
def _kimi(r):
    old = "🟢 **已发布可用、权重未落地（第 ④ 级未到）。"
    assert old in r, "058 期状态原文未找到"
    r = r.replace(old, "🟢 **已兑现（059 期实核：权重已公开）。")
    cells = r.strip().strip("|").split("|")
    assert "｜" not in cells[1] and "|" not in cells[1]
    assert "已兑现" in r
    return set_status(r,
        "🟢 **已兑现（059 期实核：权重已公开）。 ⚠️ `HF` 官方 `moonshotai/Kimi-K3.1-Pro`：`112` 个文件、"
        "`96` 个 `safetensors` 分片、`gated:false`、`private:false`、`license: other`（`kimi-k3.1-pro`）、"
        "仓库卡一手 `2.8T` 总参 / `104B` 激活 / `93` 层** —— **第 ④ 级「能下载」已到，"
        "「能商用」仍要看自定义许可条款（未逐条读）**。⚠️ **官方文档页那句承诺仍逐字未改**（`740,462` 字节、命中 `3` 次）。**")


edit("Kimi 发布", lambda r: r.startswith("| 🟢 **`Moonshot` `Kimi K3.1 Pro` 发布（10/23 晚–10/24"), _kimi)


# ⑤ Kimi 访问条件：充值门槛现在只约束 API
def _kimi_acc(r):
    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（059 期）权重已公开，「充值 `10` 元解锁」现在只约束 API / 在线体验，"
        "不约束下载与自托管** —— 仓库 `gated:false`、`private:false`，无需申请即可拉取。**")


edit("Kimi 访问条件", lambda r: r.startswith("| ⚠️ **`Moonshot` `Kimi K3.1 Pro` 的访问条件"), _kimi_acc)


# ⑥ Antigravity：字节数与上期相同 + 首次抓取被截断的实证
def _ag(r):
    return set_status(r,
        "🟡 **生效中（申请制）。 ⚠️（059 期）定价页 `137,595` 字节 —— 与上期逐字节相同**，"
        "`Generally Available` / `$0/month` / `Basic weekly rate limits` 命中数仍是 `1`/`1`/`1`；"
        "**本期首抓的 `12,408` 字节是传输被截断**（文件断在 `CSS` 中间），不是页面变小（避坑 263）；"
        "`/models` 连续第 `7` 期 `404`。**")


edit("Antigravity 免费档", lambda r: r.startswith("| 🟡 **`Google Antigravity` 科研 / 安全 6 个月免费档"), _ag)


# ⑦ Runware 促销数组 14 -> 18
def _rw(r):
    return set_status(r,
        "🟢 **生效中（距结束 `3` 天）。 ⚠️（059 期）官方促销数组 `14 → 18`**（新增 `4`、消失 `0`）："
        "`klingai-video-4-0-flash` / `krea-3`（`11/10`）、`minimax-h3-max-november`（`11/15`）、"
        "`pruna-p-video-2-pro-replace`（`11/19`）；**`pruna-p-video-2-pro-avatar` 的 `endsAt` 就是今天（`11/5`）**。**")


edit("Runware upscale", lambda r: r.startswith("| 🟢 **`Runware` 分发层 `pruna-p-video-upscale` 促销 `50% OFF`"), _rw)


# ⑧ Ollie 两行：只剩 1 天
def _ollie1(r):
    return set_status(r,
        "⚠️ **生效中（关停倒计时 · 距今 `1` 天）。 ⚠️（059 期）告别信 `35,662` 字节（上期 `39,747`，`−4,085`）"
        "而 `sunsetting` `5` / `Nov 6` `7` / `effective` `2` 逐字未变** —— **又一次「字节变了、口径没变」**。**")


edit("Ollie 关停", lambda r: r.startswith("| ⚠️ **`Ollie`（隐私向 AI 助手）宣布关停"), _ollie1)


def _ollie2(r):
    return set_status(r,
        "⚠️ **生效中（距今 `1` 天）。 ⚠️（059 期）定价页 `41,791` 字节 —— 与上期逐字节相同**，"
        "`Free` `9` / `$0` `6` / `50 messages` `6` / `6 free additional` `3` 逐字同值；"
        "**⚠️ `Free` 档是否一并停服，公告里仍没有逐字写**。**")


edit("Ollie Free 档", lambda r: r.startswith("| ⚠️ **`Ollie` 的 `Free` 档"), _ollie2)


# ⑨ 商汤 6.8 Flash：官方发布条目现在读得到
def _sn68(r):
    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（059 期）`sensetime.com/cn/news` 读到 `2026/11/03` 的「`SenseNova 6.8 Flash` 正式版发布」条目**"
        "（上期记「无条目」）；**但该页 `限时` 与 `免费` 各 `0` 命中**，`token-plan` `20,820` 字节逐字节同、`截止` `0` 命中"
        " —— **「限时免费」仍只是媒体口径**；**上期未归档该页，无法判定后上架还是漏读**（避坑 260）。**")


edit("商汤 6.8 Flash", lambda r: r.startswith("| ⚠️ **商汤 `SenseNova 6.8 Flash` 上线"), _sn68)


# ⑩ 商汤 Token Plan：三期逐字节相同
def _sn(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（059 期）`20,820` 字节 —— 与 057 / 058 两期逐字节相同**，"
        "`公测期完全免费开放`／`限时放量`／`6.8 Flash Lite`／`U1 Fast` 各 `1` 次，**仍无截止日**。**")


edit("商汤 Token Plan", lambda r: r.startswith("| 🟢 **商汤 `日日新 SenseNova` Token Plan 公测免费档"), _sn)


# ⑪ 小浣熊：逐字节相同
def _xxh(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（059 期）`158,318` 字节 —— 与上期逐字节相同**；`免费版` `7` / `积分/日` `6` 仍在，"
        "`6.8` / `Flash` / `Lite` 仍各 `0` 命中。**")


edit("小浣熊免费版", lambda r: r.startswith("| 🟢 **商汤 `小浣熊`（Raccoon）免费版"), _xxh)


# ---------------- 本期新增行 ----------------
NEW = [
    "| 🟢 **`Vercel Labs` `fx`（`vercel-labs/fx` · `Unix like coding agent` · `Zig` 写 · `Apache-2.0` · "
    "**059 期首次登记的往期项目：仓库创建于 `2026-08-11`，本期由 `InfoQ` `11/5 02:00` 的报道带出**）** | "
    "**无结束日（`Apache-2.0` 开源代码，无活动期）** | "
    "🟢 生效中。**一手**：`api.github.com/repos/vercel-labs/fx`（`200`）—— `license: Apache-2.0`、`language: Zig`、"
    "`stargazers_count: 3753`、`created_at 2026-08-11T08:57:04Z`、`pushed_at 2026-11-05T04:41:53Z`、`homepage: https://fx.sh`。"
    "**四层开放**：能用 ✔／能下载 ✔／能跑 ✔（`Zig` 工具链）／**能商用 ✔（`Apache-2.0` 明写）**"
    " —— **本报告登记的开源编码 agent 里少见的「四层全过」**。⚠️ **不是本期新品**：仓库建于 8 月，本期只是首次登记（避坑 229）。 |",
]

for n in NEW:
    body.append(n)

# ---------------- 断言 ----------------
cells = Counter(len([c for c in r.strip().strip("|").split("|")]) for r in body)
print("字段数分布：", cells)
assert cells == Counter({3: len(body)}), ("字段数异常（单元格里混进了竖线？）", cells)

for r in NEW:
    assert ("本期" in r) or ("059 期" in r), ("新增行缺本期标记", r[:40])

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
assert "`454/16/12`" in disk and "`455/18/14`" not in disk, "OpenRouter 三档计数未改写"
assert "inkling-small:free" in disk, "inkling 两条未落盘"
assert "crouton-alpha-free" in disk, "OpenCode crouton 未落盘"
assert "已兑现（059 期实核：权重已公开）" in disk, "Kimi 状态未改写"
assert "权重未落地" not in disk, "Kimi 旧状态仍在"
assert "kimi-k3.1-pro" in disk, "许可名未落盘"
assert "12,408" in disk, "截断实证未落盘"
assert "pruna-p-video-2-pro-replace" in disk, "Runware 新增条目未落盘"
print("改写行：%d 条 -> %s" % (len(NOTES), "、".join(NOTES)))
print("written:", OUT, len(disk.encode("utf-8")), "bytes")
