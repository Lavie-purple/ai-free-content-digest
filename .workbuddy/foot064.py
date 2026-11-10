# -*- coding: utf-8 -*-
"""064 期第四章脚注：A / B 明细**直接由 `check_deadlines.py --all` 输出解析生成**（不手抄）。

纪律：
  · 计数与明细同源；断言条数与桶头一致。
  · 分布数字先实跑、断言等于要写的数字，才允许写入。
  · 写出后回读落盘文件再逐字断言（052 期）。
"""
import csv
import io
import re
import subprocess
import sys
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第064期-2026-11-10.md"
CSV = WS + ".workbuddy/data/deadlines.csv"

out = subprocess.check_output(
    [sys.executable, WS + ".workbuddy/check_deadlines.py", "--today", "2026-11-10", "--all"],
    stderr=subprocess.STDOUT,
).decode("utf-8", "replace").replace(chr(13), "")
buckets = {k: int(v) for k, v in re.findall(r"【([A-E])】[^：\n]*：(\d+)\s*条", out)}
print("实跑三态桶:", buckets)
assert buckets == {"A": 31, "B": 7, "C": 0, "D": 182, "E": 7}, buckets
assert "CSV 共 227 条 -> 一致" in out, "对账行没命中（命中 0 条不是通过）"

rows = list(csv.DictReader(io.open(CSV, encoding="utf-8-sig")))
color = Counter(r["紧急度"] for r in rows)
cls = Counter(r["状态"] for r in rows)
print("实算色标:", dict(color))
print("实算状态:", dict(cls))
assert len(rows) == 227
assert color == Counter({"🟢": 156, "🟡": 23, "": 19, "⚠": 15, "🟠": 7, "🔴": 5, "⚪": 2}), color
assert cls == Counter({"live": 172, "pending": 24, "unclear": 17, "switch": 6, "crit": 5, "over": 3}), cls
assert sum(color.values()) == sum(cls.values()) == 227

white = [r for r in rows if r["紧急度"] == "⚪"]
print("⚪ 条数:", len(white), [w["活动"][:24] for w in white])
assert len(white) == 2

# ---- 从 check 输出解析 A / B 明细 ----
LINE = re.compile(r"^\s{2}(\d{4}-\d{2}-\d{2})\s+\(([^)]*)\)\s+(\S+)\s+(.+)$", re.M)
seg = out.split("【A】")[1]
segA = seg.split("【B】")[0]
segB = seg.split("【B】")[1].split("【C】")[0]
A = LINE.findall(segA)
B = LINE.findall(segB)
assert len(A) == 31, ("A 明细条数", len(A))
assert len(B) == 7, ("B 明细条数", len(B))


def short(name, n=44):
    return name if len(name) <= n else name[:n] + "…"


a_lines = []
for d, note, lvl, name in A:
    days = re.search(r"已过 (\d+) 天", note)
    a_lines.append("`%s`（已过 %s 天）%s" % (d[5:], days.group(1) if days else "?", short(name, 46)))
a_text = "　".join(a_lines)

b_lines = []
for d, note, lvl, name in B:
    b_lines.append("`%s`（%s）%s" % (d[5:], note, short(name, 52)))
b_text = "\n".join("  " + x for x in b_lines)

FOOT = """
### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-10` 实跑；CSV 共 `227` 条 —— 取自日报表体与《常驻权益总账》两处合并，所以「`227` 条」与「本章可见 `106` 行」不是矛盾）**：

- **【A】已过期但状态仍非收口态：`31` 条 —— 与 063 期同为 `31` 条，但「同为 31」是两件事相抵的结果，不是「什么都没发生」**：**063 期那 `31` 条全部还在**（相隔 `1` 天，每条天数 `+1`）；**本期没有新条目落进 A** —— `11/9` 与 `11/10` 两天**没有任何一条表内条目到期**（`腾讯元器` 的 `10/29` 早就把它带进 A 了）。**所以 `A` 的「不变」是「零进零出」，不是「复核后无变化」。**
  %s

- **【B】14 天内到期：`7` 条 —— 较 063 期的 `6` 条多 `1` 条**，新增的是本期登记的 **`Anthropic Claude Fable 5.2` 发布优惠（`11/16 23:59 PT`）**；其余 `6` 条全部是 063 期原班（`11/12` 政策、`11/13`×2、`11/15`、`11/18`、`11/22`），天数各 `+1`。
%s

- **【C】已结束：`0` 条。连续第 `2` 期为空**（062 期也是 `0`）—— **不是因为没东西结束，而是本报告的「已结束」只给有逐字收口口径的条目**，其余一律留在 A 里等人工核。

- **【D】日期无法解析：`182` 条（较 063 期 `181` 条多 `1` 条）** —— 新增的那条是本期登记的 `Inkling 2 Small` 免费档（`无结束日`）。**D ≠ 失效**：这是「长期档 / 无结束日 / 政策文件」的集合，`4.2` 与总账里的常驻权益全在这一桶。

- **【E】窗口外（>14 天）：`7` 条，与 063 期同数同成员**（`11/28` 天猫、`11/30`×2、`12/9`、`12/31`×3）。**对账：`A31 + B7 + C0 + D182 + E7 = 227`，CSV `227` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自 `slim_table` 之后重跑的 `deadlines.csv`，不是改表前的老数据）**：

| 口径 | 分布 | 合计 |
| --- | --- | --- |
| 色标（活动名列行首） | ⚪`2` / 🔴`5` / 🟢`156` / 🟡`23` / 🟠`7` / ⚠`15` / 空`19` | **`227`** |
| `classify()`（状态列语义） | `crit 5` / `live 172` / `switch 6` / `pending 24` / `unclear 17` / `over 3` | **`227`** |

**⚠️ 两侧数字必须分开报，不能互相替代**：色标是**人写给人看的优先级标记**，`classify()` 是**脚本按关键词判的状态**。本期两者在 `over` 上差 `1`（色标 ⚪`2` vs `classify over 3`）—— **差的是有一条 `⚪ 已下架`（`crouton`）被 `classify()` 判成了 `over`**。**这不是 bug，是两套口径的边界**：`⚪` 在白名单里等于「已收口」，而状态列写「已下架」时 `classify()` 归 `over`。**逐条归因，不做「差额是常数」的假设。**

**③ 逐行 diff（本期改写 `29` 行状态列 + 补入 `2` 行 + 修正 `26` 处天数 token）**：

- **改写 `29` 行**（`set_status()` 整体改写，字段数守恒 `Counter({3: 227})`）：`腾讯老混元`（`41` 天 / Q04 第 `38` 期 / 高危第 `29` 天）、`Claude Code credit`、`Runware upscale`、`MiniMax M3/M2`、`火山 Coding Plan`、`火山方舟 Agent Plan`、`腾讯元器`、`AutoClaw` 两条、`Ollie` 两条、`鲸锐大赛`、`国家超算`、`OpenRouter 免费档`、`OpenCode 清单`、`crouton`、`Ripple`、`ERNIE`、`豆包工作订阅`、`豆包额度规则`、`商汤 Token Plan`、`小浣熊`、`商汤 6.8 Flash`、`AXON`、`Token 羊毛`、`AMD`、`OpenCode Inkling`、`Antigravity 免费档`、`Kimi 访问条件`。
- **补入 `2` 行**：`Claude Fable 5.2` 发布优惠（4.1，有确切截止日）；`Inkling 2 Small` 免费档（4.2，无结束日）。**两条都带 `064 期` 标记**（否则会被 `split_ledger` 移进总账，054 期纪律）。
- **修正 `26` 处天数 token**：本期第一次做到「`已过 N 天` 也逐行重算」—— `056` 期立的避坑 `252` 说这些数字会冻结，本期实测 **`26` 处全部停在 `11/9` 的口径上**，逐行按「基准日 − 截止日」改真值后，`recalc_days064.py` 的独立复核 **`38` 处 token 全部通过**。
- **一处口径改写（不是算术修正）**：`天猫「AI 空间站」` 的截止列原写「距开卖 `19` 天」，而它 `10/20` 就开卖了 —— **「距开卖」这个说法本身失效**，本期改成「已开卖」（**去掉数字，不编新数字**）。**⚠️ 这类「措辞随时间失真」的字段，比数字算错更难被发现**：数字算错会被复核脚本抓住，措辞失真不会。

**④ `065` 期强制动作（`14` 条，出刊前逐条过）**：

① `Fable 5.2` 那「一周包含」在 **`11/16 23:59 PT`** 到期后，`Pro` 档是否真的回落到 `paid with usage credits`；**`Free` 档是否出现 `Fable`**（本期 `0` 命中，第 `2` 期）② `Inkling 2 Small` 权重是否终于上 `HF`（`author=thinkingmachines` `6 → 7`？第 `5` 期）+ `:free` 条目会不会随 062 期那句「limited time」一起撤 ③ `crouton` 是否以正式名回归（第 `2` 期）+ `iceman-free` 是否同步下架 ④ `LongCat 2.5 Free` 的**终点日**（`11/22` 还是 `11/23`）＋ 厂商侧是否终于开口径（本期 `longcat.chat` 四项关键词各 `0`）⑤ `Token 羊毛` 能否连续第 `3` 期（`¥535` 是否再跳 + 是否出现「11月11日核实」）⑥ `OpenRouter` 免费区是否再变（`:free` `13` 条成员逐条比）+ `465` 是否回落 ⑦ `AMD` 正式额度（第 `3` 期，官方页仍是 `Loading` 壳）⑧ 商汤 `6.8 Flash` 截止日（第 `9` 期）⑨ `Ollie` 三页（停服第 `5` 天，仍 `md5` 全同？）⑩ `Antigravity` 定价页能否**连续两期**拿到（本期 `200` / `142,552`）+ `models` 页（连续第 `3` 期空）⑪ 豆包工作四项关键词（第 `21` 期）⑫ `Kimi K3.1-Highspeed`（第 `6` 期空）+ `tencent/Hy4`（第 `5` 期 `404`）⑬ 老混元 `Q04`（第 `39` 期未决）、国家超算（第 `15` 期）⑭ 受阻项：`Mistral`（第 `28` 次 `000`）、`x.ai/news`（第 `8` 期 `000`）、`platform.reflection.ai`（第 `29` 期 `403`）、`platform.openai.com/docs/models`（第 `21` 期 `403`）、`next.opera.com/web-ai/`（第 `17` 期 `451`）、`docs.somark.ai/free-tier-rules.md`（第 `12` 期 `404`）、`ai.meta.com/blog/`（第 `2` 期 `000`）。
""" % (a_text, b_text)

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
anchor = "\n---\n\n*本期完。*\n"
assert md.count(anchor) == 1, md.count(anchor)
md = md.replace(anchor, FOOT.rstrip("\n") + "\n" + anchor, 1)
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(MD, encoding="utf-8").read()
for phrase in ("### ④ 本期第四章脚注", "`A31 + B7 + C0 + D182 + E7 = 227`",
               "`crit 5` / `live 172`", "本期改写 `29` 行状态列",
               "本期第一次做到「`已过 N 天` 也逐行重算」", "第 `39` 期未决"):
    assert phrase in disk, ("落盘缺短语", phrase)
assert disk.count("### ④ 本期第四章脚注") == 1
print("脚注已写入；A=%d 条明细、B=%d 条明细均来自实跑输出" % (len(A), len(B)))
print("bytes:", len(disk.encode()))
