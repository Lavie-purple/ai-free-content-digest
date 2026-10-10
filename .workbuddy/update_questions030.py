# -*- coding: utf-8 -*-
"""030 期 open_questions 更新：新增 030 现状行 + Q04/Q17 期数推进（断言式）。"""
import io

P = ".workbuddy/data/open_questions.md"
s = io.open(P, encoding="utf-8").read()
orig = s
n = 0


def rep(old, new, cnt=1, tag=""):
    global s, n
    got = s.count(old)
    assert got == cnt, "REP FAIL[%s] expect=%d got=%d :: %r" % (tag, cnt, got, old[:80])
    s = s.replace(old, new)
    n += 1
    print("  ok  %-30s x%d" % (tag, cnt))


# ---- 1. 在 029 现状行之后插入 030 现状行
ANCHOR = "未达「口径冲突」的登记门槛**（Q16 同源判据）。"
assert s.count(ANCHOR) == 1, "anchor 029 line not unique"

LINE030 = (
    "\n> **030 期现状**：共 **20 条**（**本期无新增待澄清项**）。**Q04 第 18 期**（厂商口径仍是「2026 年 9 月底」，"
    "**本期为其第 10 个高危日**；9/25 自设倒排日已过 **16 天**——**处置维持「按已停服对待、只做迁移，不再等厂商日期」**，"
    "🔴 高危窗口**刻意保持开启**但不重复升级）；**Q17 第 10 期**（**本期新增一条相关事实但不结案**：**030 期把 10/14 与 10/23 两个"
    "下线日并置在摘要的最高优先级里**，**并再次确认「迁移目标按模型逐个给、不存在一张统一迁移表」**——Codex 侧 `gpt-5.6-sol`、"
    "`o4-mini` 侧 `gpt-5.6-terra`；**官方 Codex models 页是否更新仍未核到**，**迁移动作继续按 `gpt-5.6-sol` / `gpt-6-luna` 执行**）；"
    "**Q18 / Q19 / Q20 已于 027 期合并升格为避坑 125**，不再单独挂账；其余 15 条状态不变。"
    "**⚠️ 本期未新增 Q 条**：三个候选（① OpenRouter 目录页改版为**按类型分栏**后，「免费模型 N 个」这一口径**已从源头消失**，"
    "与 Q14 同族；② **UnoRouter 目录页正文与列表计数不一致（56–58）**，但**属「同一个站点自己的两处数字」、尚无第二家独立口径**；"
    "③ **Vidu Q4 首发优惠 0.09 元/秒的标准价官方未公布**，与 Q15 同族）**均已在正文标存疑并写进第四章，"
    "但都属「一手口径本来就只给到这个精度」或「只有单一来源」，未达「口径冲突」的登记门槛**（Q16 同源判据）。"
)
s = s.replace(ANCHOR, ANCHOR + LINE030)
n += 1
print("  ok  %-30s x1" % "插入 030 现状行")

# ---- 2. Q04 期数推进
rep(
    "**未澄清**（第 16 期，**避坑 24 已覆盖**）",
    "**未澄清**（第 18 期，**避坑 24 已覆盖**）",
    1, "Q04 表头 16->18期",
)
rep(
    "**处置不变——不再等厂商日期，只做迁移**；🔴 高危窗口保持开启 |",
    "**处置不变——不再等厂商日期，只做迁移**；🔴 高危窗口保持开启。"
    "**030 期维持（第 18 期）**：10/11 厂商口径仍只有「2026 年 9 月底」，**9/25 自设倒排日已过 16 天、本期为第 10 个高危日**；"
    "**处置维持——按已停服对待、只做迁移**；🔴 高危窗口**刻意保持开启** |",
    1, "Q04 第17->18期",
)

# ---- 3. Q17 期数推进
rep("**未澄清**（第 9 期） |", "**未澄清**（第 10 期） |", 1, "Q17 第9->10期")
rep(
    "**下期回溯**：developers.openai.com/codex/models + help.openai.com changelog |",
    "**下期回溯**：developers.openai.com/codex/models + help.openai.com changelog。**030 期现状（第 10 期）**："
    "**本期新增一条相关事实但不结案** —— **030 期把 10/14（GPT-5.5）与 10/23（`o4-mini`）两个下线日并置为摘要里的最高优先级运维项**，"
    "**并再次确认「迁移目标按模型逐个给」**（Codex 侧 `gpt-5.6-sol` / Free·Go 用 `gpt-6-luna`，`o4-mini` 侧 `gpt-5.6-terra`）；"
    "**官方 Codex models 页是否更新仍未核到**，**迁移动作继续按 `gpt-5.6-sol` / `gpt-6-luna` 执行**。"
    "**下期回溯**：developers.openai.com/codex/models + help.openai.com changelog |",
    1, "Q17 追加030",
)

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("\n[完成] edits=%d  lines=%d -> %d" % (n, len(orig.split("\n")), len(s.split("\n"))))
