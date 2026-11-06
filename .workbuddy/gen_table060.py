# -*- coding: utf-8 -*-
"""060 期：从 059 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-11-06
-> 行级改写 -> 补入本期新增行。输出 .workbuddy/tmp_table060.md。

沿用 055–059 的纪律：
  ① 输入直接取上期 md 的现行文本（不取上期的 tmp_table）。
  ② 写出行必须真的进落盘文件 —— 写出后复读断言。
  ③ 断言用逐字短语，不用裸数字。
  ④ 全表字段数分布断言 Counter({3: N})。
  ⑤ 新增行必须带「本期」或「060 期」标记。
  ⑥ 状态列用 set_status() 整体改写（059 期：slim 只留第一句边界，append_note 会被裁掉）。
  ⑦ 新增/改写行的状态列不许出现 classify() 会字面误读的词（避坑 239）。
"""
import io
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第059期-2026-11-05.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table060.md"

PREV_41 = 55
PREV_LED = 163


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
assert len(rows_41) == PREV_41, ("059 期 4.1 行数", len(rows_41))
assert len(rows_led) == PREV_LED, ("总账行数", len(rows_led))
body = rows_41 + rows_led
print("输入行数：4.1 = %d，总账 = %d，合计 = %d" % (len(rows_41), len(rows_led), len(body)))

NOTES = []


def set_status(row, status):
    """整体改写状态列（不是追加）—— 059 期纪律：slim 只保留第一句边界。"""
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


# ① OpenRouter 免费档：三档 454/16/12 全同值，成员换 4 个
def _or(r):
    assert "`454/16/12`" in r, ("旧计数未找到", r[:80])
    return set_status(r,
        "🟢 **生效中（动态目录）。 ⚠️（060 期）全量 `454 → 454`、零价 `16 → 16`、`:free` `12 → 12` —— "
        "**三个数全同值、成员却换了 `4` 个**：消失 `minimax/minimax-01` / `m2` / `m2-her` / `m2.1`（全付费），"
        "进目录 `google/gemini-omni-1.1-flash`（`11/5 04:54`）、`gemini-omni-1.2-flash`（`11/6 01:16`）、"
        "`inclusionai/ling-3.0-tiny`（`8/7` 旧模型首次进目录）、`openrouter/auto-code`（`11/5 21:12`、"
        "`pricing` 为 `\"-1\"/\"-1\"` 动态计价、**不是零价**）；**零价 `16` 条与 `:free` `12` 条逐条 `ID` 完全不变**。**")


edit("OpenRouter 免费档", lambda r: r.startswith("| 🟢 **OpenRouter 免费档（**官方 API 目录口径"), _or)


# ② crouton-alpha：第 4 天仍在 + 两个 inkling:free 没有回归
def _cr(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（060 期）上架第 `4` 天仍在**：`created 1793669930` 未变、`pricing` 仍 `0/0`、"
        "`1,048,576` 上下文、`llms.txt` `4,021` 字节与上期同值；`opencode.ai/docs/zen` 的 "
        "`crouton-alpha-free` 也还在（免费清单 `11` 项同值）—— **两站存活期本期没有分叉**；"
        "**两个 `inkling:free` 没有回归**（两个 `/llms.txt` 仍 `404`、`inkling:free` 的 `/endpoints` 仍 "
        "`200` 但 `endpoints: []`）—— **「下架可逆」第一次观测的答案是「没有」**。**")


edit("crouton", lambda r: r.startswith("| 🟢 **`OpenRouter` 免费隐身模型 `stealth/crouton-alpha`"), _cr)


# ③ OpenCode 免费清单 11 项同值
def _oc(r):
    return set_status(r,
        "🟡 **生效中（清单动态）。 ⚠️（060 期）`11` 项同值**：`crouton-alpha-free` 命中 `1`、"
        "`Crouton Alpha Free` `4` 次；页面 `58,736 → 58,718` 字节（`−18`），带 `-free` 后缀的 `ID` 共 `11` 个、"
        "逐条与 059 期一致；`LongCat 2.5 Preview Free` 仍 `0` 命中。**")


edit("OpenCode 清单", lambda r: r.startswith("| 🟡 **`OpenCode` 免费模型清单 10 → 11 项"), _oc)


# ④ Kimi K3.1 Pro 发布：许可全文销项（第四层能商用成立）
def _kimi(r):
    return set_status(r,
        "🟢 **已兑现（059 期权重公开）＋ 060 期第四层销项。 ⚠️（060 期）`LICENSE` `3,077` 字节逐字 "
        "`Permission is hereby granted, free of charge … sublicense, and/or sell copies` —— **能商用成立**；"
        "附两个门槛：`MaaS` 且关联方连续 `12` 个月营收 > `US$20 million` 须与 `Moonshot AI` 另签、"
        "商业产品 > `1` 亿 `MAU` 或月营收 > `US$20 million` 须显著展示 `Kimi K3.1-Pro`；"
        "内部使用与官方产品／认证推理伙伴豁免。**059 期把「未判定」写成了「需要更多证据」，其实只差一次 `raw` 请求**。**")


edit("Kimi 发布", lambda r: r.startswith("| 🟢 **`Moonshot` `Kimi K3.1 Pro` 发布"), _kimi)


# ⑤ Kimi 访问条件：Highspeed 权重 0 条
def _kimi_acc(r):
    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（060 期）`hf-mirror.com/api/models?search=Kimi-K3.1-Highspeed` 返回 `[]`"
        "（`2` 字节）—— **官方名下 `Highspeed` 版权重 `0` 条**（059 期强制动作②后半销项）；"
        "文档页本期 `474,557` 字节、`</html>` 收尾完整（**不是截断**），承诺句命中 `2` 次（059 期 `3` 次）、"
        "**句子仍在**；**本报告不判定官方是否改了文案**。**")


edit("Kimi 访问条件", lambda r: r.startswith("| ⚠️ **`Moonshot` `Kimi K3.1 Pro` 的访问条件"), _kimi_acc)


# ⑥ Antigravity：逐字节相同，本期没有重演截断
def _ag(r):
    return set_status(r,
        "🟡 **生效中（申请制）。 ⚠️（060 期）定价页 `137,595` 字节 —— 与 059 期逐字节相同，`</html>` 收尾完整**，"
        "**本期没有重演 059 期那次 `12,408` 字节的截断**（避坑 263）；`/models` 连续第 `9` 期 `404`；"
        "`Basic weekly rate limits` 的具体数字连续第 `4` 期未追。**")


edit("Antigravity 免费档", lambda r: r.startswith("| 🟡 **`Google Antigravity` 科研 / 安全 6 个月免费档"), _ag)


# ⑦ Runware 促销数组 18 条逐条同值，仍在售 7 -> 6
def _rw(r):
    return set_status(r,
        "🟢 **生效中（距结束 `2` 天）。 ⚠️（060 期）官方促销数组 `18` 条 —— 与 059 期逐条同值**"
        "（消失 `0`、进数组 `0`、`endsAt` 变化 `0`）；**但 `11/5` 的 `pruna-p-video-2-pro-avatar` 跨过基准日，"
        "仍在售 `7 → 6` 条**（`11/8`、`11/10` ×2、`11/15`、`11/19`、`11/30`），已过但仍在数组里 `12` 条 —— "
        "**数组一个字节的语义都没变、已过期数却 `+1`**（053 期「先归因基准日」最干净的样本）。**")


edit("Runware upscale", lambda r: r.startswith("| 🟢 **`Runware` 分发层 `pruna-p-video-upscale` 促销 `50% OFF`"), _rw)


# ⑧ Ollie 关停：今天就是生效日
def _ollie1(r):
    return set_status(r,
        "⚠️ **生效中（关停日当天 · `T+0`）。 ⚠️（060 期）今天就是告别信逐字写明的 `Nov 6, 2026` 生效日**；"
        "告别信 `39,747` 字节（**回到 058 期同值**，059 期那次 `35,662` 是构建产物变体、不是页面改小 —— 见第五章纠错①），"
        "`Ollie is sunsetting on Nov 6, 2026` / `effective Nov 6, 2026` / `billing will be canceled and you will receive a refund` "
        "三处逐字全在；**页面仍完整在线**。**")


edit("Ollie 关停", lambda r: r.startswith("| ⚠️ **`Ollie`（隐私向 AI 助手）宣布关停"), _ollie1)


def _ollie2(r):
    return set_status(r,
        "⚠️ **生效中（关停日当天 · `T+0`）。 ⚠️（060 期）定价页 `41,791` 字节 —— 与 058 / 059 两期逐字节相同**，"
        "`Free` `¥0` / `50 messages … per month` / `6 free additional messages … every day` 三处逐字仍在；"
        "首页 `Free to get started. No app, no login` 仍在；**官方三页没有任何一句逐字写「`Free` 档停服」或「免费额度保留」**"
        " —— **本报告只记页面与文案状态，不判定服务是否可用**（避坑 243，连续第 `3` 期同结论、本期起不再逐期追问）。**")


edit("Ollie Free 档", lambda r: r.startswith("| ⚠️ **`Ollie` 的 `Free` 档"), _ollie2)


# ⑨ 商汤 6.8 Flash：零命中归档件已落盘
def _sn68(r):
    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（060 期）`sensetime.com/cn/news` 本期 `115,245` 字节（`+400`），"
        "`SenseNova 6.8 Flash 正式版发布` 条目仍在、`6.8 Flash` 命中 `2` 次；**该页 `限时` 与 `免费` 仍各 `0` 命中**，"
        "`token-plan` `20,820` 字节逐字节同 —— **「限时免费」仍只有媒体口径**（连续第 `4` 期）。"
        "**本期已按避坑 260 把该页落盘 `tmp_060_s/sensetime_news.html`**。**")


edit("商汤 6.8 Flash", lambda r: r.startswith("| ⚠️ **商汤 `SenseNova 6.8 Flash` 上线"), _sn68)


# ⑩ 商汤 Token Plan：四期逐字节相同
def _sn(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（060 期）`20,820` 字节 —— 与 057 / 058 / 059 三期逐字节相同**，"
        "`公测期完全免费开放`／`限时放量`／`6.8 Flash Lite`／`U1 Fast` 各 `1` 次，**仍无截止日**。**")


edit("商汤 Token Plan", lambda r: r.startswith("| 🟢 **商汤 `日日新 SenseNova` Token Plan 公测免费档"), _sn)


# ⑪ 小浣熊：+1,413 字节而免费档一行未动
def _xxh(r):
    return set_status(r,
        "🟢 **生效中。 ⚠️（060 期）`158,318 → 159,731` 字节（`+1,413`）而免费档一行未动**："
        "`免费版` `2` / `¥ 0` `2` / `/永久` `2` / `300` `7` / `积分/日` `3` 逐字全在 —— "
        "**又一次「字节变了、口径没变」**（与 058 期 `+10,918` 同形态，避坑 259）。**")


edit("小浣熊免费版", lambda r: r.startswith("| 🟢 **商汤 `小浣熊`（Raccoon）免费版"), _xxh)


# ---------------- 本期补入行 ----------------
NEW = [
    "| 🟢 **百度开源 `ERNIE-5.5-Flash-Base`（**060 期首次登记 · `FP8` 与 `BF16` 双仓库 · `280B` 总参 / `14B` 激活 · `33.5T` tokens · `43` 层 · `128K` 训练上下文 / `1M` 推理上下文 · **未经中训练与后训练的 `Base` 权重**）** | "
    "**无结束日（`license:other` 自定义许可，无活动期）** | "
    "🟢 生效中。**一手**：`hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base`（`200` / `8,307` 字节）与 "
    "`-BF16`（`200` / `8,168` 字节）—— `private:false`、`gated:false`、`siblings 139` 个（含 `128` 个 `safetensors`）、"
    "`createdAt 2026-10-21` 而 `lastModified 2026-11-05`（**相差 `15` 天**，避坑 265）；"
    "官方博客 `ernie.baidu.com/release/ernie-5-5-flash-base/`（`48,571` 字节）。"
    "**四层开放**：能用 —— **不直接成立**（`Base` 权重，不是对话模型）／能下载 ✔／能跑 ✔（`vLLM` + `SGLang` + `Megatron-Bridge`）／"
    "**能商用 —— 有条件成立（`25,619` 字节 `LICENSE` 全文）**：非商用免费、商用 ≤ `US$50M` 免费但须 `Powered by ERNIE` 署名 ＋ "
    "一次性通知、> `US$50M` 须书面授权；**`Territory` 逐字排除欧盟／英国／韩国**；`Exhibit A` `20` 条禁用、"
    "`Last revised: November 6, 2026`（**主协议 `11/5`、附件次日就改**）。 |",
]

for n in NEW:
    body.append(n)

# ---------------- 断言 ----------------
cells = Counter(len(r.strip().strip("|").split("|")) for r in body)
print("字段数分布：", cells)
assert cells == Counter({3: len(body)}), ("字段数异常（单元格里混进了竖线？）", cells)

for r in NEW:
    assert ("本期" in r) or ("060 期" in r), ("新增行缺本期标记", r[:40])

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
assert "`454 → 454`" in disk, "OpenRouter 三档同值未改写"
assert "minimax/minimax-01" in disk, "MiniMax 消失清单未落盘"
assert '`"-1"/"-1"`' in disk, "动态计价哨兵值未落盘"
assert "ERNIE-5.5-Flash-Base" in disk, "百度新增行未落盘"
assert "Territory" in disk, "地域排除未落盘"
assert "3,077` 字节" in disk, "Kimi 许可销项未落盘"
assert "Highspeed" in disk, "Highspeed 零命中未落盘"
assert "39,747" in disk, "Ollie 关停日未落盘"
assert "58,718" in disk, "OpenCode 未落盘"
assert "115,245" in disk, "商汤未落盘"
assert "159,731" in disk, "小浣熊未落盘"
assert "已兑现（059 期权重公开）" in disk, "Kimi 状态未改写"
print("改写行：%d 条 -> %s" % (len(NOTES), "、".join(NOTES)))
print("written:", OUT, len(disk.encode("utf-8")), "bytes")
