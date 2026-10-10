# -*- coding: utf-8 -*-
"""030 期台账更新（断言式替换）：AI信息源分级清单-T0-T4.md

纪律（028 期起固定）：
  - 每处编辑先断言行数/命中数，再替换；不符立即 exit 1。
  - 手写计数四处同步：T0 根节点 / 模型与开源 / 官方一手·国内 / T4（+ 汇总行）。
  - 站点首页「信源 N 条」= 五个 `## T\\d …（N）` 标题数字求和 → 只加行不改数会显示旧数字。
  - 本期新增 3 条：HAL-X AI（T0 模型与开源）/ 生数科技·Vidu（T0 官方一手·国内）/ UnoRouter（T4）
"""
import io, re, sys

P = "AI信息源分级清单-T0-T4.md"
s = io.open(P, encoding="utf-8").read()
orig = s
n_edits = 0


def rep(old, new, cnt=1, tag=""):
    global s, n_edits
    got = s.count(old)
    assert got == cnt, "REP FAIL[%s] expect=%d got=%d :: %r" % (tag, cnt, got, old[:90])
    s = s.replace(old, new)
    n_edits += 1
    print("  ok  %-32s x%d" % (tag, cnt))


# ---------------------------------------------------------------- 1. 手写计数
rep("## T0 · 根节点（121）", "## T0 · 根节点（123）", 1, "T0 根节点 121->123")
rep("### 模型与开源（18）", "### 模型与开源（19）", 1, "模型与开源 18->19")
rep("### 官方一手 · 国内（22）", "### 官方一手 · 国内（23）", 1, "官方一手国内 22->23")
rep("## T4 · 聚合器与工具（23）", "## T4 · 聚合器与工具（24）", 1, "T4 23->24")

# ---------------------------------------------------- 2. 模型与开源 +1 行（尾插）
ANCHOR_MS = "本层第一条国内决策模型信源）** 形成国内双样本 | 029 | 43 |"
assert s.count(ANCHOR_MS) == 1, "anchor 模型与开源 tail not unique"

ROW_HALX = (
    '| **🆕 HAL-X AI** '
    '| https://api.hal-x.ai/docs/thx-01 · https://huggingface.co/doofz/THX-01 '
    '| — '
    '| **「决策模型同时做到『权重 Apache 2.0 + 接口免密钥 + 单次前向』」的第一现场**（030 期首次命中）——'
    '**`THX-01`**：**322M 参数、非自回归、单次前向返回带校准概率的结构化答案**（choice / yes-no / score / number / excerpt / citations）；'
    '**18 种后训练语言**；**Apache 2.0（权重 + 源码 + 训练脚本）**、`pip install thx01`；'
    '**托管 API 免密钥 / 免注册 / 免付费**（官方称有速率限制）。'
    '补入 **T0 模型与开源**——补的是本报告「**能不能白用**」这一层长期缺的字段；'
    '与 024 期 StartLux、029 期 AutoTrust 同属「决策模型线」开源样本，**本条为「接口侧」**（避坑 134 两维表中的「售卖形态」一列） '
    '| 030 | 1 |'
)
s = s.replace(ANCHOR_MS, ANCHOR_MS + "\n" + ROW_HALX)
n_edits += 1
print("  ok  %-32s x1" % "插入 模型与开源 +1 行")

# --------------------------------------- 3. 官方一手·国内 +1 行（尾插）
ANCHOR_CN = "非原版准确率 | 029 | 61 |"
assert s.count(ANCHOR_CN) == 1, "anchor 官方一手国内 tail not unique"

ROW_VIDU = (
    '| **🆕 生数科技（Shengshu / Vidu）** '
    '| https://www.vidu.cn/（以官方发布为准） '
    '| — '
    '| **「视频线『每秒单价』这一列的第一个样本」**（030 期首次命中，10/10）——'
    '**`Vidu Q4 Preview`** 把**首发 0.09 元/秒**写进发布物，**使本报告第一次能在视频线做「每抽成本」量级比较**'
    '（避坑 137 的来源；同期 `Kling 4.0` 以官方口径同台，快手可灵为已跟踪信源）。'
    '补入 **T0 官方一手 · 国内**——**视频线自 029 期避坑 131 定编独立扫描位后，首次有信源落位** '
    '| 030 | 1 |'
)
s = s.replace(ANCHOR_CN, ANCHOR_CN + "\n" + ROW_VIDU)
n_edits += 1
print("  ok  %-32s x1" % "插入 官方一手国内 +1 行")

# ------------------------------------------------------------ 4. T4 +1 行（尾插）
ANCHOR_T4 = "同样不能当事实源**（避坑 125/129）。 | 028 | 11 |"
assert s.count(ANCHOR_T4) == 1, "anchor T4 tail not unique"

ROW_UNO = (
    '| **🆕 UnoRouter（api.unorouter.com）** '
    '| https://api.unorouter.com/v1 · https://www.llmperks.com/unorouter '
    '| — '
    '| **「一个 Key 路由到 `:free` 模型 + 免绑卡 + 共享容量」的第二个独立样本**（030 期首次命中）——'
    '与 OpenRouter 免费档形成对照：**同样是「免费目录」，但 OpenRouter 给 200 req/day 的确定性限额，UnoRouter 只给「共享容量」**'
    '（**记账时两类必须分开**）。**「免费额度垂直追踪站」的第五个样本**'
    '（前四：freellm.net 数据目录、magpie 客户端登录态、llmperks 单网关逐日核对、OpenRouter 免费档）；'
    '`56–58 模型 / 免绑卡` 的核对出自 llmperks。补入 **T4 聚合器与工具** '
    '| 030 | 1 |'
)
s = s.replace(ANCHOR_T4, ANCHOR_T4 + "\n" + ROW_UNO)
n_edits += 1
print("  ok  %-32s x1" % "插入 T4 +1 行")

# ------------------------------------------------------------ 5. 汇总行追加 030
SUMMARY_TAIL = "并**第二次实证「时间戳需做时区换算」**）。"
assert s.count(SUMMARY_TAIL) == 1, "anchor summary tail not unique"
ADD_SUMMARY = (
    "**030 期新增三条**：**T0 模型与开源 +1**（**HAL-X AI**，`THX-01` ——「权重 Apache 2.0 + 接口免密钥 + 单次前向」的第一现场）、"
    "**T0 官方一手 · 国内 +1**（**生数科技 / Vidu**，`Vidu Q4 Preview` 把「首发 0.09 元/秒」写进发布物，视频线首个「每秒单价」样本）、"
    "**T4 +1**（**UnoRouter**，「一个 Key 路由到 `:free` 模型 + 免绑卡 + 共享容量」的第二个独立样本）"
    "→ **220 → 223**（**模型与开源 18 → 19、官方一手·国内 22 → 23、T4 23 → 24**；**T1 19、T2 18、T3 39 不变**）。"
    "**030 期就地更新两行**：**freellm.net**（计数器 **维持 507+ 模型 / 30 提供方 / 免绑卡 424+ / 更新至 2026-10-10** —— "
    "**逐期记账以来第一次「重取后与上期同值」**，故**正文不得据此写「继续回升」**）、**AIHOT（aihot.news）**"
    "（**第二十六次逐期计数确认 + 操作禁令第九次落地**，并**第三次记录「该源 10/11 尚无条目」**）。"
    "**030 期另逐条核对用户随任务提供的 T0–T4 补充清单**：与台账**一致、无新增项、无缺项**，**故不产生条目增删**"
    "（其中用户给出的 `https://aihot.news/` 与台账既有 `aihot.virxact.com` **为同一家的两个入口**）。"
)
s = s.replace(SUMMARY_TAIL, SUMMARY_TAIL + ADD_SUMMARY)
n_edits += 1
print("  ok  %-32s x1" % "汇总行追加 030")

# ----------------------------------------------------------- 6. 版本行追加 030
VER_TAIL = "、AIHOT（**时间戳时区口径第二次实证**）**）**"
assert s.count(VER_TAIL) == 1, "anchor version tail not unique"
ADD_VER = (
    "；就地更新至 **2026-10-11（030 期，条目数 220 → 223；新增 **HAL-X AI**（`THX-01`，**权重 Apache 2.0 + 免密钥托管 API + 单次前向返回校准概率**）入 **T0 模型与开源**；"
    "**生数科技 / Vidu**（`Vidu Q4 Preview`，**首发 0.09 元/秒**，**视频线首个「每秒单价」样本**）入 **T0 官方一手 · 国内**；"
    "**UnoRouter**（**一个 Key 路由到 `:free` 模型 + 免绑卡 + 共享容量**）入 **T4**；"
    "**AIHOT 边界升级为第二十六次逐期计数确认**，操作禁令**第九次落地**；"
    "**本期就地更新 2 行**：freellm.net（**逐期记账以来第一次「重取后与上期同值」——维持 507+ 模型 / 30 提供方 / 免绑卡 424+ / 更新至 2026-10-10**）、"
    "AIHOT（**第三次记录「该源 10/11 尚无条目」**）；**本期逐条核对用户随任务提供的 T0–T4 补充清单，与台账一致、无增删**）**"
)
s = s.replace(VER_TAIL, VER_TAIL + ADD_VER)
n_edits += 1
print("  ok  %-32s x1" % "版本行追加 030")

# ------------------------------------------------------- 7. 就地更新 freellm.net 行
FRE_TAIL = "**「降了又升」说明该计数器是流通量口径、不是存量口径**）"
assert s.count(FRE_TAIL) == 1, "anchor freellm tail not unique"
FRE_NEW = (
    "**「降了又升」说明该计数器是流通量口径、不是存量口径**；"
    "**030 期计数器重取：维持 507+ 模型 / 30 提供方 / 更新至 2026-10-10（「免绑卡」424+）**——"
    "**这是逐期记账以来第一次「重取后与上期同值」**（**故不得据此写「继续回升」，029 期曾因沿用旧值误写趋势**））"
)
s = s.replace(FRE_TAIL, FRE_NEW)
n_edits += 1
print("  ok  %-32s x1" % "就地更新 freellm.net")

# ------------------------------------------------------------ 8. 就地更新 AIHOT 行
AIHOT_TAIL = "不做换算会把它误记成「10/10 美国白天发布」**。 | 029 | 215 |"
assert s.count(AIHOT_TAIL) == 1, "anchor AIHOT tail not unique"
AIHOT_NEW = (
    "不做换算会把它误记成「10/10 美国白天发布」**。"
    " ⚠️ **030 期第二十六次逐期计数确认（操作禁令第九次落地）**：**10/10 共 15 条，其中 2 条落在本期窗口内**"
    "（**OpenAI 700+ 数学手稿 21:06**、**MIT 教育副院长谈 Navier-Stokes 反例 22:18**）；**10/11 尚无可读条目**"
    "（**第三次记录「该源 10/11 尚无条目」**——该源更新滞后于本期 06:10 截止）。**本期全部额度增量**"
    "（THX-01 免费 API、Mercury Decide、Vidu 首发价、TeamAI 开源、AutoClaw 倒计时）**没有一条是它先报的**；"
    "**THX-01 / Mercury Decide / UnoRouter / Vidu 四条事实全部出自官方文档与垂直目录站，该源 0 命中**"
    "——**边界第八次以定论形式复用**。 | 030 | 216 |"
)
s = s.replace(AIHOT_TAIL, AIHOT_NEW)
n_edits += 1
print("  ok  %-32s x1" % "就地更新 AIHOT")

# --------------------------------------------------------------- 9. 收尾断言
assert s != orig, "nothing changed"
io.open(P, "w", encoding="utf-8", newline="\n").write(s)

nums = re.findall(r"^## T\d[^\n（]*（(\d+)）", s, flags=re.M)
print("\n[标题计数] %s -> 合计 %d" % (nums, sum(int(x) for x in nums)))
assert sum(int(x) for x in nums) == 223, "标题计数合计 != 223"
assert len(nums) == 5, "标题数 != 5"

# 内部小节复核：T0 六个子节求和应 = 123
sub = re.findall(r"^### [^（\n]+（(\d+)）", s, flags=re.M)
t0 = sub[:6]
print("[T0 子节] %s -> 合计 %d" % (t0, sum(int(x) for x in t0)))
assert sum(int(x) for x in t0) == 123, "T0 子节合计 != 123"

print("[完成] edits=%d  bytes %d -> %d" % (n_edits, len(orig.encode('utf-8')), len(s.encode('utf-8'))))
