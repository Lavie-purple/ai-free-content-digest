# -*- coding: utf-8 -*-
"""045 期 md 第八章与台账实况对齐：
- 「新增 4 条信源」→「新增 2 条 + 再次取用 2 条」
- 表格加「登记状态」列，两条既有源标回首登期
- 补「差点重复登记」自纠段（避坑 44 同族）
- 计数行改为 52→54 / 166→168 / 模型与开源 35 不变
"""
import io, os, sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(WS, "AI免费内容与权益速递-第045期-2026-10-23.md")

with io.open(MD, encoding="utf-8") as f:
    text = f.read()

OLD_HEAD = "**本期新增 4 条信源（均为本轮实际取料的一手源）**："
NEW_HEAD = "**本期新增 2 条信源、再次取用 2 条既有信源（四条均为本轮实际取料的一手源）**："
assert text.count(OLD_HEAD) == 1
text = text.replace(OLD_HEAD, NEW_HEAD)

# 表头：加「登记状态」列
OLD_TH = "| 信源 | 分级 | 首次取用 | 为什么进清单 |"
NEW_TH = "| 信源 | 分级 | 登记状态 | 为什么进清单 / 本轮新用途 |"
assert text.count(OLD_TH) == 1
text = text.replace(OLD_TH, NEW_TH)

# 两行新源：首次取用 045 → 🆕 045 期新增
OLD_RSS = "| **`OpenAI News RSS`**（`openai.com/news/rss.xml`） | T0 · 官方一手 · 国外 | **045** |"
NEW_RSS = "| **`OpenAI News RSS`**（`openai.com/news/rss.xml`） | T0 · 官方一手 · 国外 | **🆕 045 期新增** |"
assert text.count(OLD_RSS) == 1
text = text.replace(OLD_RSS, NEW_RSS)

OLD_HF = ("| **`HF` 仓库详情端点 + 原始文件端点**（`hf-mirror.com/api/models/<org>/<repo>`、"
          "`…/raw/main/README.md`、`…/raw/main/LICENSE`） | T0 · 官方一手 · 国外 | **045** |")
NEW_HF = ("| **`HF` API 仓库详情端点 + 原始文件端点**（`hf-mirror.com/api/models/<org>/<repo>`、"
          "`…/raw/main/README.md`、`…/raw/main/LICENSE`） | T0 · 官方一手 · 国外 | **🆕 045 期新增** |")
assert text.count(OLD_HF) == 1, "HF row not found"
text = text.replace(OLD_HF, NEW_HF)

# MiniMax 官方博客：043 期已登记，本期再次取用
OLD_MM = ("| **`MiniMax` 官方博客**（`minimax.io/blog/minimax-m31f`） | T0 · 官方一手 · 国外 | **045** |")
NEW_MM = ("| **`MiniMax` 官方博客**（`minimax.io/blog/minimax-m31f`） | T0 · 官方一手 · 国外 | "
          "**043 期已登记 · 本期再次取用** |")
assert text.count(OLD_MM) == 1
text = text.replace(OLD_MM, NEW_MM)

# OpenCode 文档两页：039 期已登记，本期首次被用作收口判据源
OLD_OC = ("| **`OpenCode` 文档两页**（`opencode.ai/docs/go`、`opencode.ai/docs/zen`） | "
          "T0 · 官方一手 · 国外 | **045** |")
NEW_OC = ("| **`OpenCode` 文档两页**（`opencode.ai/docs/go`、`opencode.ai/docs/zen`） | "
          "T0 · 官方一手 · 国外 | **039 期已登记 · 本期首次被用作收口判据源** |")
assert text.count(OLD_OC) == 1
text = text.replace(OLD_OC, NEW_OC)

# 在「本期一条既有源的口径变化」段前插入自纠段
ANCHOR = "**本期一条既有源的口径变化（重要）**"
SELF_FIX = (
    "**本期一次台账自纠（避坑 44 同族：「再次命中 ≠ 新增信源」）**：本报告初稿曾把上表四条全部写成"
    "「本期新增 4 条信源」，经 `git show HEAD` 调各期台账逐行核对，确认 **`MiniMax` 官方博客是 043 期**"
    "（发布日 2026-10-19）**已登记**（commit `2b289f4`）、**`OpenCode` 文档两页是 039 期已登记**"
    "（commit `6b3ddba`）—— 本期只是再次取用，不产生条目增删；台账已按「新增 2 条」改正"
    "（`### 官方一手 · 国外` 52 → 54、`## T0 · 根节点` 166 → 168，`### 模型与开源` 35 不动）。"
    "**「本期用过」与「本期新增」是两个集合，动手改计数前必须逐行核台账，不能凭本期印象下笔**。\n\n"
)
assert text.count(ANCHOR) == 1
text = text.replace(ANCHOR, SELF_FIX + ANCHOR)

# 计数行重写
OLD_CNT_START = "**计数（手写五处已同步）**：**`### 模型与开源` 35 → 36**"
assert text.count(OLD_CNT_START) == 1
i = text.index(OLD_CNT_START)
j = text.index("\n", i)
NEW_CNT = (
    "**计数（手写括号计数已同步）**：**`### 官方一手 · 国外` 52 → 54**（补 `OpenAI News RSS`、"
    "`HF` API 详情端点 + `raw` 端点）、**`## T0 · 根节点` 166 → 168**、**`### 模型与开源` 35 不变**、"
    "**论文与预印本 / 官方一手 · 国内 / 政策与监管 / 评测与榜单 / T1 / T2 / T3 / T4 本期均未动**。"
    "⚠️ **站点首页「信源 N 条」= 五个 `## T\\d …（N）` 标题求和，台账现为 279 = 168 + 19 + 18 + 41 + 33"
    "（已实跑核对）**；⚠️ **T4 一节本期无条目增删** —— `freellm.net` 已在台账内，"
    "**本期只是重取计数器与专页，不产生条目增删**。"
)
text = text[:i] + NEW_CNT + text[j:]

with io.open(MD, "w", encoding="utf-8", newline="") as f:
    f.write(text)
print("OK: 第八章已对齐台账实况")
