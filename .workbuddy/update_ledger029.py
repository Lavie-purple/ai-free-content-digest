# -*- coding: utf-8 -*-
"""029 期台账更新（断言式替换）：AI信息源分级清单-T0-T4.md

纪律（028 期起固定）：
  - 每处编辑先断言命中数，再替换；命中数不符立即 exit 1。
  - 手写计数四处同步：T0 根节点 / 模型与开源 / 官方一手·国外 + T0 内部分类复核 汇总行。
  - 站点首页「信源 N 条」= 五个 `## T\\d …（N）` 标题数字求和 → 只加行不改数会显示旧数字。
"""
import io, sys

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
    print("  ok  %-28s x%d" % (tag, cnt))


# ---------------------------------------------------------------- 1. 手写计数
rep("## T0 · 根节点（118）", "## T0 · 根节点（121）", 1, "T0 根节点 118->121")
rep("### 模型与开源（16）", "### 模型与开源（18）", 1, "模型与开源 16->18")
rep("### 官方一手 · 国外（33）", "### 官方一手 · 国外（34）", 1, "官方一手国外 33->34")

# ---------------------------------------------------- 2. 模型与开源 +2 行（尾插）
ANCHOR_MS = (
    '未覆盖"广告资助"形态 | 028 | 29 |'
)
assert s.count(ANCHOR_MS) == 1, "anchor 模型与开源 tail not unique"

ROW_UNDERDOG = (
    '| **🆕 Underdog AI（ConwayResearch）** '
    '| https://underdog.ai/ · https://huggingface.co/ConwayResearch '
    '| — '
    '| **「把大模型压到 8GB 以内、且是 llama.cpp 标准格式」的第一现场**。029 期首次命中——**`Saluki 27B`**：'
    '**2-bit 量化、权重 7.89 GB、Apache 2.0、llama.cpp 可直接加载**，官方称**工具调用优于同尺寸全精度**。'
    '⚠️ **同一模型在 AIHOT 记作「Conway Research」、在厂商页记作「Underdog」——名字多处不一致，认仓库 ID 不认站名**（避坑 124）。'
    '补入 **T0 模型与开源**——此前「能不能跑」这一层没有专门的权重信源 '
    '| 029 | 1 |'
)
ROW_AUTOTRUST = (
    '| **🆕 AutoTrust AI Lab** '
    '| https://modelscope.cn/models · https://community.modelscope.cn/ '
    '| — '
    '| **「多模态决策模型」的第一条国内样本**。029 期首次命中（10/10，ModelScope 发布）——**`JEV-27B-VL`** '
    '把决策模型从纯文本扩到**图像输入**（决策模型线此前只有 `d1` 带视觉）。'
    '补入 **T0 模型与开源**，与 024 期登记的 **StartLux（决策模型五档，本层第一条国内决策模型信源）** 形成国内双样本 '
    '| 029 | 1 |'
)
s = s.replace(ANCHOR_MS, ANCHOR_MS + "\n" + ROW_UNDERDOG + "\n" + ROW_AUTOTRUST)
n_edits += 1
print("  ok  %-28s x1" % "插入 模型与开源 +2 行")

# ------------------------------------------- 3. 官方一手·国外 +1 行（尾插，表格最后一行之后）
ANCHOR_FG = '本层此前缺"harness 与模型之间的连接层" | 028 | 60 |'
assert s.count(ANCHOR_FG) == 1, "anchor 官方一手国外 tail not unique"

ROW_PRIME = (
    '| **🆕 Prime Intellect** '
    '| https://www.primeintellect.ai/ · https://github.com/PrimeIntellect-ai '
    '| — '
    '| **「用多智能体重写自身代码」的第一现场**。029 期首次命中——**`Prime Agent` 用 Rust 从零重写**：'
    '**2000+ 智能体自主完成端到端迁移、上线以来下载超 30 万次、处理超 8 万亿 token**。'
    '补入 **T0 官方一手 · 国外**——补的是本报告长期缺的「**自我改写型 agent harness**」这一类（与避坑 131「模型线各自独立扫」同源） '
    '| 029 | 1 |'
)
s = s.replace(ANCHOR_FG, ANCHOR_FG + "\n" + ROW_PRIME)
n_edits += 1
print("  ok  %-28s x1" % "插入 官方一手国外 +1 行")

# ------------------------------------------------------------ 4. 汇总行追加 029
SUMMARY_TAIL = "**本清单「评测与榜单」一节目前只列站、不列指标**。"
assert s.count(SUMMARY_TAIL) == 1, "anchor summary tail not unique"
ADD_SUMMARY = (
    "**029 期新增三条**：**T0 模型与开源 +2**（**Underdog AI**，「把大模型压到 8GB 以内的 llama.cpp 权重」`Saluki 27B`；"
    "**AutoTrust AI Lab**，`JEV-27B-VL` 多模态决策模型）、**T0 官方一手 · 国外 +1**（**Prime Intellect**，`Prime Agent` 自我改写型 harness）"
    "→ **217 → 220**（**T1 19、T2 18、T3 39、T4 23 不变**）。**029 期就地更新两行**：**freellm.net**"
    "（计数器 **499+ → 507+ 模型 / 30 提供方 / 更新至 2026-10-10**，「免绑卡」**416+ → 424+**，**在 028 期反向下降后回升**）、"
    "**AIHOT（aihot.news）**（**第二十五次逐期计数确认 + 操作禁令第八次落地**，并**第二次实证「时间戳需做时区换算」**）。"
)
s = s.replace(SUMMARY_TAIL, SUMMARY_TAIL + ADD_SUMMARY)
n_edits += 1
print("  ok  %-28s x1" % "汇总行追加 029")

# ----------------------------------------------------------- 5. 版本行追加 029
VER_TAIL = "**本期就地更新 2 行**：freellm.net、阶跃星辰）**"
assert s.count(VER_TAIL) == 1, "anchor version tail not unique"
ADD_VER = (
    "；就地更新至 **2026-10-10（029 期，条目数 217 → 220；新增 **Underdog AI**（把大模型压到 8GB 以内、llama.cpp 标准格式的权重，`Saluki 27B`）/ "
    "**AutoTrust AI Lab**（`JEV-27B-VL`，多模态决策模型的国内首样本）——两者均入 **T0 模型与开源**；**Prime Intellect**（`Prime Agent` 用 Rust 重写、2000+ 智能体自主迁移）入 **T0 官方一手 · 国外**；"
    "**AIHOT 边界升级为第二十五次逐期计数确认**，操作禁令**第八次落地**；**本期就地更新 2 行**：freellm.net（**计数器反向下降后回升 499+ → 507+ 模型 / 30 提供方 / 「免绑卡」416+ → 424+ / 更新至 2026-10-10**）、"
    "AIHOT（**时间戳时区口径第二次实证**）**）**"
)
s = s.replace(VER_TAIL, VER_TAIL + ADD_VER)
n_edits += 1
print("  ok  %-28s x1" % "版本行追加 029")

# ------------------------------------------------------- 6. 就地更新 freellm.net 行
FRE_TAIL = "**这是逐期记账以来第一次「下架多过新增」，说明「计数器下降」本身也是有效信号**）"
assert s.count(FRE_TAIL) == 1, "anchor freellm tail not unique"
FRE_NEW = (
    "**这是逐期记账以来第一次「下架多过新增」，说明「计数器下降」本身也是有效信号**；"
    "**029 期计数器回升：507+ 模型 / 30 提供方 / 更新至 2026-10-10（「免绑卡」424+、其中 240 条经实时 API 复核）**——"
    "**「降了又升」说明该计数器是流通量口径、不是存量口径**）"
)
s = s.replace(FRE_TAIL, FRE_NEW)
n_edits += 1
print("  ok  %-28s x1" % "就地更新 freellm.net")

# ------------------------------------------------------------ 7. 就地更新 AIHOT 行
AIHOT_TAIL = "必须回原文页时间戳**。 | 028 | 209 |"
assert s.count(AIHOT_TAIL) == 1, "anchor AIHOT tail not unique"
AIHOT_NEW = (
    "必须回原文页时间戳**。"
    " ⚠️ **029 期第二十五次逐期计数确认（操作禁令第八次落地）**：10/10 至 13:33 共 **13 条**、最后一条 13:33，"
    "**「免费额度 / 领取 / 权益活动」类仍接近 0 条**——本期全部额度与权益增量（火山方舟专业数据集、AutoClaw 登录活动、汕头词元券、OpenRouter 免费档 19）"
    "**没有一条是它先报的**；**但它带出了本期安全线的全部主干（Anthropic 越界三条、OpenAI 失准报告、Redwood 蒸馏论文、Epoch AI `InnovationEval`）**"
    "——**边界第七次以定论形式复用**。**⚠️ 029 期第二次实证时区口径**：10/10 的 Anthropic 条目（**03:38–06:16**）"
    "**对应美西 10/9 中午到下午**，**正是 028 期挂账「美西 10/9 工作日白天」的那一段**——**不做换算会把它误记成「10/10 美国白天发布」**。 | 029 | 210 |"
)
s = s.replace(AIHOT_TAIL, AIHOT_NEW)
n_edits += 1
print("  ok  %-28s x1" % "就地更新 AIHOT")

# --------------------------------------------------------------- 8. 收尾断言
assert s != orig, "nothing changed"
io.open(P, "w", encoding="utf-8", newline="\n").write(s)

# 五个标题数字求和 = 220
import re
nums = re.findall(r"^## T\d[^\n（]*（(\d+)）", s, flags=re.M)
print("\n[标题计数] %s -> 合计 %d" % (nums, sum(int(x) for x in nums)))
assert sum(int(x) for x in nums) == 220, "标题计数合计 != 220"
assert len(nums) == 5, "标题数 != 5"

print("[完成] edits=%d  bytes %d -> %d" % (n_edits, len(orig.encode('utf-8')), len(s.encode('utf-8'))))
