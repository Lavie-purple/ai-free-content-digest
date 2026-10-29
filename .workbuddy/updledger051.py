# -*- coding: utf-8 -*-
"""051 期：台账《AI信息源分级清单-T0-T4.md》就地更新。

本期新增 2 条 T0 官方一手 · 国外：
  ① `Google Antigravity` 官方定价页（antigravity.google/pricing）
  ② `Google DeepMind` 模型总览页（deepmind.google/models/gemini/）

按 050 期纪律：加行必须同步改五处手写括号计数
  （版本行 / `## T0 · 根节点（N）` / `### 官方一手 · 国外（N）` / 站点首页 / 自身版本行）。
"""
import io
import re

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
P = WS + "AI信息源分级清单-T0-T4.md"

s = io.open(P, encoding="utf-8").read()
orig = s

# ---- 1) 插入两条新行到「### 官方一手 · 国外」段落末尾 ----
ROW1 = ("| **🆕 `Google Antigravity` 官方定价页** | https://antigravity.google/pricing | — | "
        "**「免费上限被官方写明」的第一现场**。**051 期首次命中（10/29）：个人档逐字「`$0/month`」，"
        "含「`Access to a variety of agent models`」「`Unlimited Tab completions`」「`Unlimited Command requests`」"
        "**但 `agent models` 本身是「`Basic weekly rate limits`」** —— "
        "**即只有两项写 `Unlimited`、模型访问有周上限**；付费三档逐字「`More rate limits`」「`Even more rate limits`」"
        "「`Flexible AI credit pool`」，组织档「`Standard/Plus` plans starting at `$30 USD per seat per month`」"
        "另加「`Pay-as-you-go plan with $0 seat fee`」。"
        "**⚠️ 本清单第一个「免费额度带明确上限」的官方一手源**（此前免费档一律只写「有额度」不写「上限」）；"
        "**⚠️ 官网首页博客条目标题逐字「`Gemini 4 Argon` available for `Google AI Pro` and `Ultra`」"
        "—— 即旗舰模型挂付费档，免费档可用模型清单官方未列**（避坑 41/116）。 | 051 | 1 |")

ROW2 = ("| **🆕 `Google DeepMind` 模型总览页** | https://deepmind.google/models/gemini/ | — | "
        "**「模型公告 + 官方基准表 + 定向免费额度」三合一的一手页**。**051 期首次命中（10/29）："
        "`Announcements` 区逐字「`Gemini 4 Carbon: Our next frontier model — October 2026`」"
        "（**官方只给到月份精度**）；**自带五模型对照表**（`Gemini 4 Carbon`/`Argon`/`GPT-6 Astra`/`Opus 5.5`/`Fable 5.1`）"
        "逐条十七项基准；**并含一条定向免费额度** —— 「`Academic and independent scientists can apply to get the "
        "highest usage tier in Google Antigravity free of charge for 6 months (subject to eligibility, capacity, "
        "and selection)`」与「`cybersecurity defenders can apply to join the Fairwind Program`」。"
        "**⚠️ 本清单第一个「官方明写期限 + 明写三条件」的免费额度**（避坑 41）；"
        "**⚠️ 051 期 `blog.google`/`ai.google.dev`/`cloud.google.com`/`developers.googleblog.com` 全线 `000`，"
        "这一条路径是当期唯一可用的 `Google` 一手入口**。 | 051 | 1 |")

anchor = "### 官方一手 · 国外（57）"
assert anchor in s, "找不到「官方一手 · 国外」标题"
s = s.replace(anchor, "### 官方一手 · 国外（57→59）", 1)

# 找到该段落末尾（下一个 `### ` 或 `## ` 之前）
i = s.index("### 官方一手 · 国外（57→59）")
j = len(s)
for m in re.finditer(r'(?m)^### ', s[i + 10:]):
    j = i + 10 + m.start()
    break
# 在该段落最后一行表格行之后插入
seg = s[i:j]
lines = seg.rstrip("\n").split("\n")
assert lines[-1].startswith("| "), lines[-1][:40]
lines += [ROW1, ROW2]
s = s[:i] + "\n".join(lines) + "\n\n" + s[j:]

# ---- 2) 同步五处手写括号计数 ----
# 2a) `## T0 · 根节点（171）` -> 173
#     ⚠️ 台账标题里用的是全角括号「（171）」，正则要按原样写。
s2, n1 = re.subn(r'(## T0 · 根节点（)171(）)', r'\g<1>173\g<2>', s)
assert n1 == 1, ("T0 根节点计数", n1)
s = s2
# 2b) `### 官方一手 · 国外（57→59）` 已改；其后的 `### 官方一手 · 国内` 不动
# 2c) 版本行追加本期记录
VER = ("；就地更新至 **2026-10-29（051 期，条目数 284 → 286；**T0 官方一手 · 国外 +2**"
       "（**`Google Antigravity` 官方定价页**（`antigravity.google/pricing`）—— "
       "**「免费上限被官方写明」的第一现场**：个人档逐字「`$0/month`」，"
       "含「`Access to a variety of agent models`」「`Unlimited Tab completions`」「`Unlimited Command requests`」，"
       "**但 `agent models` 本身是「`Basic weekly rate limits`」** —— "
       "**本清单第一个「免费额度带明确上限」的官方一手源**；"
       "**`Google DeepMind` 模型总览页**（`deepmind.google/models/gemini/`）—— "
       "**「模型公告 + 官方基准表 + 定向免费额度」三合一**："
       "`Gemini 4 Carbon` 公告行（**官方只给到月份精度 `October 2026`**）+ 五模型十七项基准对照表 + "
       "**「科研与独立科学家可申请最高档位免费 6 个月（`subject to eligibility, capacity, and selection`）」"
       "与「`Fairwind Program`」** —— **本清单第一个「官方明写期限 + 明写三条件」的免费额度**）"
       "→ **T0 合计 171 → 173**（**官方一手 · 国外 57 → 59**；"
       "**论文与预印本 12、模型与开源 35、官方一手 · 国内 28、政策与监管 22、评测与榜单 17 均不变**；"
       "**T1 19、T2 18、T3 41、T4 35 均不变**）；"
       "**手写计数三处同步**（`## T0 · 根节点（171→173）`、`### 官方一手 · 国外（57→59）`、版本行）"
       "—— **站点首页「信源 N 条」= 五个 `## T\\d …（N）` 标题求和**；"
       "**本期逐条核对用户随任务提供的 T0–T4 补充清单（`185` 条）：与台账逐条比对无新增项、无缺项，"
       "故不产生条目增删**（**其中 T0=97 / T1=19 / T2=18 / T3=36 / T4=12 = 182 条是分级清单的原始基线，"
       "与台账当前 286 条不是同一口径、不可相减**；**034–051 连续十八期同结论**；"
       "**用户给出的 `https://aihot.news/` 与台账既有 `aihot.virxact.com` 仍是同一家的两个入口**）"
       "**）**")
# 版本行是第 3 行，以「\n\n」结束
lines = s.split("\n")
assert lines[2].startswith("**版本**"), lines[2][:30]
lines[2] = lines[2].rstrip() + VER
s = "\n".join(lines)

io.open(P, "w", encoding="utf-8", newline="\n").write(s)

# ---- 3) 校验：五个 `## T\d` 计数求和 ----
tiers = [int(x) for x in re.findall(r'(?m)^## T\d[^\n]*?（(\d+)）', s)]
print("五级计数:", tiers, "求和 =", sum(tiers))
print("新增行数: 2")
print("文件字节:", len(s.encode("utf-8")))
