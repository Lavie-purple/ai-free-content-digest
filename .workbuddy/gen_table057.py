# -*- coding: utf-8 -*-
"""057 期：从 056 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-11-03
-> 行级改写 -> 追加本期新增行。输出 .workbuddy/tmp_table057.md（纯表格块）。

沿用 055/056 的纪律：
  ① 输入直接取上期 md 的现行文本（不取上期的 tmp_table）。
  ② 写出行必须真的进落盘文件 —— 写出后复读断言。
  ③ 断言用逐字短语，不用裸数字（避坑 248）。
  ④ 字段数分布断言 Counter({3: N})（避坑 242 的表格版）。
  ⑤ 新增行必须带「本期」或「057 期」标记，否则会被 split_ledger 当「无变化」移进总账（054 期踩过）。
"""
import io
import re
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第056期-2026-11-02.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table057.md"

PREV_41 = 55
PREV_LED = 157


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
assert len(rows_41) == PREV_41, ("056 期 4.1 行数", len(rows_41))
assert len(rows_led) == PREV_LED, ("总账行数", len(rows_led))
body = rows_41 + rows_led
print("输入行数：4.1 = %d，总账 = %d，合计 = %d" % (len(rows_41), len(rows_led), len(body)))

# ---------------- 行级改写 ----------------
NOTES = []          # (标记, 说明)


def append_note(row, note):
    r = row.rstrip()
    assert r.endswith("|"), r[-20:]
    body = r[:-1].rstrip()
    return body + " " + note + " |"


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


# ① OpenRouter：452 -> 451（全量 −1：+1 付费新增、−2 旧模型撤下），零价/`:free` 逐条不变
def _or(r):
    r = r.replace("`452/17/14`", "`451/17/14`")
    return append_note(r,
        "**⚠️（057 期）官方目录重取：全量 `452 → 451`、零价 `17` 同值、`:free` `14` 同值**；"
        "**逐条 diff 新增 `1` 条 `z-ai/glm-5.3-flashx-legal`（付费档）、消失 `2` 条 "
        "`nousresearch/hermes-3-llama-3.1-405b` 与 `…-70b`** —— **`+1 −2 = −1`，与总数差逐条对得上**；"
        "**零价档与 `:free` 档的逐条 ID 名单与上期完全一致**。")


edit("OpenRouter 免费档", lambda r: r.startswith("| 🟢 **OpenRouter 免费档（**官方 API 目录口径"), _or)

# ② 百度 Unlimited OCR 2：流通量复读（近 30 天窗口口径）
def _ocr(r):
    return append_note(r,
        "**⚠️（057 期）流通量复读（近 `30` 天窗口口径）：`downloads 109,519 → 147,588`、"
        "`likes 520 → 550`** —— **按避坑 249 只写窗口值，不写「累计涨了 X%」**。")


edit("百度 Unlimited OCR 2", lambda r: r.startswith("| 🟢 **`百度` 开源 `文心 Unlimited OCR 2`"), _ocr)

# ③ 商汤 Token Plan：免费档首次点名到具体型号
def _sn(r):
    return append_note(r,
        "**⚠️（057 期）免费档点名的模型首次细化到具体型号**：一手 `www.sensenova.cn/token-plan`"
        "（`200` / `20,820` 字节）逐字 `公测期完全免费开放，付费档位即将上线`、`Free · 公测`、`限时放量`、"
        "`¥ 0 /月`、`SenseNova 6.8 Flash Lite`、`SenseNova U1 Fast`、`最多 20 个 API Key`；"
        "**全文 `12 月` / `12月` 各命中 `0` 次 —— 官方没写任何截止日**。")


edit("商汤 Token Plan", lambda r: r.startswith("| 🟢 **商汤 `日日新 SenseNova` Token Plan 公测免费档"), _sn)

# ④ 豆包工作 30 天订阅：连续第 11 期零命中
def _db(r):
    return append_note(r,
        "**⚠️（057 期）`volcengine.com/product/doubao-work` `200` / `169,633` 字节，正文提取后仍 `178` 字节 "
        "`JS` 壳，`免费`/`额度`/`赠送`/`试用`/`30 天`/`订阅` 各命中 `0` 次 —— 连续第 `11` 期零命中。**")


edit("豆包工作", lambda r: r.startswith("| 🟢 **豆包工作 30 天订阅（新一轮）**"), _db)

# ⑤ Kimi K3.1 Pro：11/4 前放出权重 —— 本期仍未放出
def _kimi(r):
    return append_note(r,
        "**⚠️（057 期）`HF` 官方 `moonshotai` 名下仍 `19` 个模型，最新仍是 `Kimi-K3`"
        "（`createdAt 2026-06-13T06:42:57Z`），含 `K3.1` 的官方条目 `0` 条** —— "
        "**官方承诺的 `11/4` 前只剩 `1` 天，本期仍未放出。**")


edit("Kimi K3.1 Pro 门槛", lambda r: r.startswith("| ⚠️ **`Moonshot` `Kimi K3.1 Pro` 的访问条件"), _kimi)

# ⑥ 国家超算互联网：连续第 5 期零命中
def _sc(r):
    return append_note(r,
        "**⚠️（057 期）`www.scnet.cn` 首页 `200` / `132,762` 字节，`夜间`/`21:00`/`09:00`/`每晚`/`限时` "
        "仍各命中 `0` 次 —— 连续第 `5` 期。**")


edit("国家超算互联网", lambda r: r.startswith("| 🟠 **`国家超算互联网` 夜间限时免费调用"), _sc)

# ⑦ Ollie「信息分散在子页」实证行：距关停天数
def _ollie(r):
    return append_note(r,
        "**⚠️（057 期）三页复读：`farewell` 仍逐字 `Ollie is sunsetting on Nov 6, 2026`、"
        "定价页 `Free` / `$0` / `6 free additional messages from Ollie every day` 同值** —— "
        "**关停距今 `3` 天。**")


edit("Ollie 信息分散", lambda r: r.startswith("| ⚠️ **一条「信息分散在子页」的实证：`Ollie`"), _ollie)

# ---------------- 本期新增行 ----------------
NEW = [
    # 1) 商汤小浣熊免费版（产品侧）
    "| 🟢 **商汤 `小浣熊`（Raccoon）免费版：`¥0 / 永久` ＋ `300` 积分/日（**057 期新登记 · 产品侧免费档，"
    "与 API 侧 `Token Plan` 是两笔账**）** | **未公布（官方写「永久」，无活动截止日）** | "
    "🟢 生效中。**官方一手 `xiaohuanxiong.com/pricing`（`200` / `147,400` 字节）逐字**：`免费版`、`¥ 0`、`/永久`、"
    "`300`、`积分/日`、`每日 0 点重置 · 不累计 · 仅限标准模型`；权益逐条 `AI 对话 · 标准模型`、"
    "`PPT 标准模式 · 全部模板任选`、`文件上传 5 个/对话 · 80 MB`、`存储空间 500 MB`、`社群答疑支持`；"
    "另一处逐字 `一次对话 ≈ 1~5 积分`。**⚠️ 三条边界**：① **产品站 `6.8` / `Flash` / `Lite` / `限时` / `12 月` "
    "各命中 `0` 次** —— **媒体说的「`6.8 Flash` 限时免费」在产品定价页与首页都读不到**；"
    "② `仅限标准模型` 是逐字限制，**不是全部模型**；③ 「永久」是官方对该档位的描述，**不等于该档位的内容永不缩水**。 |",

    # 2) SenseNova-Skills 开源技能库
    "| 🟢 **商汤 `SenseNova-Skills` 开源技能库（`MIT` 许可 · **057 期新登记**）** | "
    "**无结束日（`MIT` 许可，与模型额度无关）** | 🟢 生效中。**一手 `api.github.com/repos/OpenSenseNova/SenseNova-Skills`**："
    "`stargazers_count 6009`、`forks_count 432`、`license.spdx_id MIT`、`created_at 2026-04-14T06:21:51Z`、"
    "`pushed_at 2026-11-02T10:54:08Z`（＝北京 `11/2 18:54`）。**`README.md` 逐字**：`The skills cover image generation & "
    "visualization, slide-deck (PPT) generation, Excel data analysis, deep research, code-driven video creation, "
    "HTML experiences, team collaboration, and proactive project tracking`。**四层开放**：能用 ✔／能下载 ✔／能跑 ✔"
    "（`SKILL.md` 约定，兼容 `OpenClaw` / `hermes-agent`）／**能商用 ✔（`MIT`）**。 |",

    # 3) SenseNova 6.8 Flash（媒体说限免，官方无截止日）
    "| ⚠️ **商汤 `SenseNova 6.8 Flash` 上线（**057 期补入 · 媒体称「限时免费」，官方两页均无截止日**）** | "
    "**未公布（媒体稿无截止日；产品站 `12 月` 零命中）** | ⚠️ **生效中（口径存疑）**。**媒体稿**（量子位 "
    "`2026-11-02 21:36` 北京，`pubDate` 落在本期窗口内）逐字：`商汤科技刚刚发布的多模态智能体模型日日新 "
    "SenseNova 6.8 Flash`、`主打的就是委派智能`、`它现在可以是限时免费的哦`。**⚠️ 官方侧实读**："
    "`sensenova.cn/token-plan` 只点名 `SenseNova 6.8 Flash Lite`（**是 `Lite`**）与 `SenseNova U1 Fast`，"
    "写 `限时放量` 但**无截止日**；`xiaohuanxiong.com/pricing` 与 `/work` 对 `6.8` / `Flash` / `限时` **各命中 `0` 次**；"
    "`sensetime.com/cn/news` 列表**无 6.8 Flash 发布条目**。**⚠️ 故本行只写「可体验」与「官方无截止日」，不写「限免至某日」。** |",
]

for n in NEW:
    body.append(n)

# ---------------- 断言 ----------------
cells = Counter(len([c for c in r.strip().strip("|").split("|")]) for r in body)
print("字段数分布：", cells)
assert cells == Counter({3: len(body)}), ("字段数异常（单元格里混进了竖线？）", cells)

for r in NEW:
    assert ("本期" in r) or ("057 期" in r), ("新增行缺本期标记", r[:40])

total = len(body)
assert total == PREV_41 + PREV_LED + len(NEW), total
print("表体总行数：%d = %d + %d + %d" % (total, PREV_41, PREV_LED, len(NEW)))

header = "| 活动 | 截止 | 状态 |\n| --- | --- | --- |\n"
io.open(OUT, "w", encoding="utf-8", newline="\n").write(header + "\n".join(body) + "\n")

# 落盘复读
disk = io.open(OUT, encoding="utf-8").read()
disk_rows = [l for l in disk.split("\n") if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(disk_rows) == total, ("落盘行数", len(disk_rows))
for n in NEW:
    assert n in disk, ("新增行未进落盘文件", n[:40])
assert "`451/17/14`" in disk and "`452/17/14`" not in disk, "OpenRouter 三档计数未改写"
assert "147,588" in disk and "6009" in disk, "流通量/仓库数未进落盘文件"
print("改写行：%d 条 -> %s" % (len(NOTES), "、".join(NOTES)))
print("written:", OUT, len(disk.encode("utf-8")), "bytes")
