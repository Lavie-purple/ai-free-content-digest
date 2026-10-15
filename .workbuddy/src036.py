# -*- coding: utf-8 -*-
"""036 期信源台账回写：新增 3 条信源 + 同步五处手写计数。
注意：本文件用 Write 工具写成，避免 bash 双引号内的反引号被命令替换吃掉内容。"""
import io

P = "AI信息源分级清单-T0-T4.md"
# 该文件是 LF 行尾：必须用 newline="" 读写，否则 Windows 文本模式会把整文件改成 CRLF，
# git diff --stat 会显示成整文件重写（033 期事故 1446/1351 行 vs 真实 95 行的同型）。
with io.open(P, encoding="utf-8", newline="") as f:
    t = f.read()
assert "\r\n" not in t, "源文件不是 LF 行尾，先查清再改"

REPS = [
    ("## T0 · 根节点（143）", "## T0 · 根节点（144）"),
    ("### 官方一手 · 国外（36）", "### 官方一手 · 国外（37）"),
    ("### 政策与监管（20）", "### 政策与监管（21）"),
    ("## T3 · 媒体（39）", "## T3 · 媒体（40）"),
]
for a, b in REPS:
    assert t.count(a) == 1, (a, t.count(a))
    t = t.replace(a, b)

FIGMA = (
    "| **🆕 Figma 官方 release notes + pricing FAQ** | https://www.figma.com/whats-new/ · https://www.figma.com/pricing-faq/ | — | "
    "**「限时免费 → 转 AI credits」这一形态的第一现场，也是本清单第一个「把免费边界写到『同一条提示词里两件事只免一件』粒度」的信源**。"
    "**036 期首次命中（10/15 发版说明）**——Config India 2026 一批：**`Code Layers` 转入全计划 open beta，创建与编辑 code layer 在付费计划上免费至 2026-11-04**；"
    "**`Figma Make` 原生 scaffold `Payload` 后端（CMS / 数据库 / 媒体 / API / 认证 / 管理面板），托管 beta 免费、官方承诺「先公布定价与打包方式再生效」**；"
    "**`Figma Specs` 付费计划 open beta，不用 AI 创建 / 编辑免费、用 agent 则耗 credits**。"
    "⚠️ **它同时是「先免费后定价」的标准样本**（避坑 126）；⚠️ **Figma 的 agent 已于 10/6 转 GA 并自此消耗 credits** —— "
    "**「某功能免费」≠「用该功能的流程免费」** | 036 | 1 |"
)

AG = (
    "| **🆕 美国各州总检察长办公室通稿（NH / IL / CO 等 40 州 + DC）** | https://www.doj.nh.gov/ · https://www.illinoisattorneygeneral.gov/ · https://coag.gov/ | — | "
    "**「州级监管如何进入联邦破产程序」的第一现场，也是本清单第一个「从监管方一手文件（而非媒体转述）拿到 AI 平台破产口径」的信源**。"
    "**036 期首次命中（10/14）**——**40 州 bipartisan 联盟就 `Character.AI` 破产提交 notice of interest**："
    "**要求任何资产出售落实儿童与消费者数据保护，并明确指出该平台对未成年人的限制「非强制、不完整、可能被未来买家绕过或推翻」**；"
    "**通稿同时给出全部 40 州 + DC 名单、威尔明顿首次听证会细节（法官 Brendan Shannon、代表各州的律师 Abigail Ryan）与纽约州总检察长詹乐霞（Letitia James）的声明原文**。"
    "⚠️ **它把 035 期避坑 157 的「三句话」推进为「四句话」**（**新增第四句：「已做出的儿童安全承诺」本身也可能随出售失效**） | 036 | 1 |"
)

CB = (
    "| **🆕 博客园（`vibecodinghuanzhe` 等深读稿）** | https://www.cnblogs.com/ | — | 036 | 1 |"
)

# 1) T0 · 官方一手 · 国外：插在该节最后一行之后、下一个 ### 之前
anchor = "### 官方一手 · 国外（37）"
i = t.index(anchor)
j = t.index("\n### ", i + 10)
t = t[:j] + "\n" + FIGMA + t[j:]

# 2) T0 · 政策与监管：插在该节最后一行之后、下一个 ## 之前
anchor2 = "### 政策与监管（21）"
i = t.index(anchor2)
j = t.index("\n## ", i + 10)
t = t[:j] + "\n" + AG + t[j:]

# 3) T3 · 国内：插在该节最后一行之后、下一个 --- 之前
anchor3 = "## T3 · 媒体（40）"
i = t.index(anchor3)
k = t.index("\n---", i)
t = t[:k] + "\n" + CB + t[k:]

with io.open(P, "w", encoding="utf-8", newline="") as f:
    f.write(t)
assert "\r\n" not in io.open(P, encoding="utf-8", newline="").read()
print("ledger updated (LF preserved)")
