# -*- coding: utf-8 -*-
"""032 期台账更新。

纪律：
  1) 断言式替换 rep(old, new, cnt=1)
  2) 改章节标题手写计数必须与表体行数同源
  3) 行插入用行首定位，插入后重新断言总行数

032 期增量：229 → 235
  T0 模型与开源     23 → 26  (vLLM-SR / AMI / 小思框架)
  T0 官方一手·国外  34 → 35  (Odyssey)
  T4 聚合器与工具   25 → 27  (OrcaRouter / Inferse)
  T0 根节点        128 → 132
  其余：论文 12 / 官方一手·国内 24 / 政策 18 / 评测 17 / T1 19 / T2 18 / T3 39 不变
"""
import io, sys

LEDGER = "AI信息源分级清单-T0-T4.md"

def rep(s, old, new, cnt=1):
    got = s.count(old)
    assert got == cnt, f"anchor count expect={cnt} got={got}\n---\n{old[:200]}"
    return s.replace(old, new)


s = io.open(LEDGER, encoding="utf-8").read()

# ---------- 1 版本行追加 032 期 ----------
old_ver = "；**本期新增第 13 类清单缺口**「许可证变更追踪位」**）**"
new_ver = (
    old_ver +
    "；就地更新至 **2026-10-12（032 期，条目数 229 → 235；"
    "新增 **vLLM Semantic Router（vLLM-SR）**（`Decision 3.0` 六档 Apache-2.0，"
    "**「开放权重决策模型的批发式发布」+「先传权重、公告只发在 X」第一个样本**）"
    "/**AMI（Advanced Machine Intelligence）**（`H-JEPA` 分层世界模型，代码 + 预训练权重公开）"
    "/**小思框架**（`Moti-1` 摩谛，**把层内自注意力整个换掉**的 RCA 跨层波前注意力）——三条均入 **T0 模型与开源**；"
    "**Odyssey**（`Odyssey-3`，14B 生成式世界模型 + 免费公开研究预览）入 **T0 官方一手 · 国外**；"
    "**OrcaRouter**（**唯一把「权重已交付、发布说明未发」写清楚的源**）/**Inferse**（**免费模型目录的第二个独立口径**）入 **T4**；"
    "**AIHOT 边界升级为第二十八次逐期计数确认**，操作禁令**第十一次落地**，"
    "**新增第三条读数口径「首页头条区按热度排序、可跨日堆积、不含日期，不能当当日条目读」**；"
    "**本期就地更新 2 行**：freellm.net（**逐期记账以来第二次「重取后与上期同值」——维持 500+ 模型 / 30 提供方 / 免绑卡 417+ / 已实测 234 / "
    "该站 `Last Updated` 2026-10-11**）、AIHOT（**第二十八次逐期计数确认 + 操作禁令第十一次落地**）；"
    "**本期新增第 14 类清单缺口**「发布方式追踪位」**）**"
)
s = rep(s, old_ver, new_ver, 1)

# ---------- 2 T0 内部分类复核汇总行追加 032 期 ----------
old_review = ("**031 期另逐条核对用户随任务提供的 T0–T4 补充清单**：**与台账一致、无新增项、无缺项**，**故不产生条目增删**。")
new_review = (
    old_review +
    "**032 期新增六条**：**T0 模型与开源 +3**（**vLLM Semantic Router（vLLM-SR）**，`Decision 3.0` 六档 Apache-2.0，"
    "**「开放权重决策模型」的批发式发布第一现场，也是「先传权重、公告只发在 X」的第一个样本**；"
    "**AMI（Advanced Machine Intelligence）**，`H-JEPA` 分层世界模型，**LeCun 的创业公司**；"
    "**小思框架**，`Moti-1` 摩谛，**用 RCA 跨层波前注意力整个换掉层内自注意力**）、"
    "**T0 官方一手 · 国外 +1**（**Odyssey**，`Odyssey-3` 14B 生成式世界模型 + 免费公开研究预览）、"
    "**T4 +2**（**OrcaRouter**，**唯一把「权重已交付、发布说明未发」写清楚的源**；"
    "**Inferse**，**免费模型目录的第二个独立口径**，本期与 freellm.net 对同一批 OpenRouter 免费模型给出 22 vs 19）"
    "→ **229 → 235**，其中 **T0 合计 128 → 132**（**模型与开源 23 → 26、官方一手 · 国外 34 → 35**；"
    "**论文与预印本 12、官方一手 · 国内 24、政策与监管 18、评测与榜单 17 均不变**）、**T4 25 → 27**"
    "（**T1 19、T2 18、T3 39 不变**）；**手写计数四处同步**（`## T0 · 根节点（128→132）`、`### 模型与开源（23→26）`、"
    "`### 官方一手 · 国外（34→35）`、`## T4 · 聚合器与工具（25→27）`）——**站点首页「信源 N 条」= 五个 `## T\\d …（N）` 标题求和，"
    "只加行不改数会导致首页显示旧数字**。**032 期就地更新两行**：**freellm.net**（**维持 500+ 模型 / 30 提供方 / 「免绑卡」417+ / "
    "已实测 234 / 该站 `Last Updated` 2026-10-11** —— **逐期记账以来第二次「重取后与上期同值」，故不得据此写「继续回落」或「继续回升」**）、"
    "**AIHOT（aihot.news）**（**第二十八次逐期计数确认 + 操作禁令第十一次落地**，并**新增第三条读数口径「首页头条区按热度排序、可跨日堆积、不含日期」**）。"
    "**032 期另逐条核对用户随任务提供的 T0–T4 补充清单**：**结论与 030 / 031 期一致 —— 与台账逐条比对无新增项、无缺项，故不产生条目增删**"
    "（其中用户给出的 `https://aihot.news/` 与台账既有 `aihot.virxact.com` **为同一家的两个入口**）。"
)
s = rep(s, old_review, new_review, 1)

# ---------- 3 四处手写计数 ----------
s = rep(s, "## T0 · 根节点（128）", "## T0 · 根节点（132）", 1)
s = rep(s, "### 模型与开源（23）", "### 模型与开源（26）", 1)
s = rep(s, "### 官方一手 · 国外（34）", "### 官方一手 · 国外（35）", 1)
s = rep(s, "## T4 · 聚合器与工具（25）", "## T4 · 聚合器与工具（27）", 1)

# ---------- 4 清单缺口表的计数注（补记第 14 类） ----------
old_gap_note = "合并计入）。**注：本表只保留 8 条基础行，第 9 类起的增量按本注 + 版本行维护**。）"
new_gap_note = (
    "合并计入）；**032 期新增第 14 类**（「**发布方式追踪位**」—— **本清单第一次为「过程字段」设追踪位**，"
    "**对每个「开放权重」条目固定记录「发布方式 + 公告源 + 公告时点」三列**，与 031 期的「许可证 + 核对日」并列；"
    "**本期两个样本**：`Decision 3.0` = 先权重后 X、`Intern-Decision-4B` = 完全无公告）。"
    "**注：本表只保留 8 条基础行，第 9 类起的增量按本注 + 版本行维护**。）"
)
s = rep(s, old_gap_note, new_gap_note, 1)

# ---------- 5 插入新信源行 ----------
lines = s.split("\n")

def find_line(prefix, frm=0):
    for i in range(frm, len(lines)):
        if lines[i].startswith(prefix):
            return i
    raise AssertionError("line not found: " + prefix[:60])

# T0 模型与开源：在 Speridlabs 行之后插入 3 行
i_sp = find_line("| **🆕 Speridlabs**")
assert "Iris-3B" in lines[i_sp], lines[i_sp][:80]
NEW_MODELS = [
    "| **🆕 vLLM Semantic Router（vLLM-SR）** | https://huggingface.co/vllm-sr · vLLM 官方 X | — | "
    "**「开放权重决策模型」的批发式发布第一现场，也是「先传权重、公告只发在 X」的第一个样本**。**032 期首次命中**——**`Decision 3.0`**："
    "**六个检查点全部 Apache-2.0，10/10 09:38 → 23:49 UTC 上传完毕**；**在 vLLM 的 route 层按 query 类型路由到不同决策头**，"
    "**六档分别对应不同成本 / 延迟档**；**每份仓库都带自定义建模代码与独立读出头**（**等于一个可直接自托管的 decision server**）。"
    "⚠️ **公告只发了 vLLM 官方 X 的一条转推**（官网 blog 索引停在 10/10、GitHub releases 停在 9/27 的 v0.4.0）—— "
    "**「权重已交付」与「有发布说明」是两件事**（避坑 143）。补入 **T0 模型与开源** —— **与 024 期 StartLux / 029 期 AutoTrust / 030 期 HAL-X AI "
    "同属「决策模型线」，本条为「批发 + 无公告」形态的第一个样本**（避坑 134 两维表的「售卖形态」列 × 032 期新增的「发布方式」列） | 032 | 4 |",

    "| **🆕 AMI（Advanced Machine Intelligence）** | https://ami.ai · 论文与开源仓库 | — | "
    "**「分层联合嵌入预测架构（H-JEPA）」世界模型的第一现场**。**032 期首次命中（10/11）**——**`H-JEPA`**："
    "**AMI 联合纽约大学、巴黎 INRIA 与布朗大学**；**多层 JEPA 堆叠、各层在自身表征空间预测不同时间跨度状态**；"
    "**高层出粗略计划、把预测的中间状态当子目标交低层细化**；**沿用 SIGReg 避免表征坍塌**；"
    "**Visual AntMaze 三层成功率 73%、单层 18%；Push-T 上两层最好、三 / 四层反降**；**代码与预训练权重同步公开**（**LeCun 的创业公司，3 月融资 10.3 亿美元**）。"
    "⚠️ **它不生成像素、只预测嵌入**，**与同一天发布的 `Odyssey-3`（生成可交互环境）是两条路线、不可比大小**（避坑 144）。"
    "补入 **T0 模型与开源** | 032 | 3 |",

    "| **🆕 小思框架** | https://modelscope.cn/models/ericsjq/Moti-1-7B | — | "
    "**「把层内自注意力整个换掉」这一路线的第一现场**。**032 期首次命中（10/11）**——**`Moti-1`（摩谛）**："
    "**7B 因果语言模型**；**保留 `Qwen2.5-7B-Instruct` 的 FFN / Embedding / LayerNorm，把层内自注意力换成 RCA 跨层波前注意力（约 822M）**；"
    "**64-token 分块、按「块 0 全部层 → 块 1 全部层」推进**；**原 q/k/v/o 权重作 RCA 分支初始权重**；"
    "**6 领域均分 43.2（原版 38.1）、前端代码最高 +24.7**；**RTX 3090 30 tok/s**；**权重 18.57 GB、推理显存峰值约 18.6 GB**。"
    "⚠️ **RCA 分支需 fp32**（bf16 会落进 cuDNN 劣化路径，单层 63 ms vs 3.7 ms）。补入 **T0 模型与开源** —— "
    "**「注意力机制层」这条线此前只覆盖架构论文，未覆盖「个人 / 小团队改完并开源权重」** | 032 | 3 |",
]
lines[i_sp + 1:i_sp + 1] = NEW_MODELS

# T0 官方一手 · 国外：在 Prime Intellect 行之后插入 1 行
i_pi = find_line("| **🆕 Prime Intellect**")
assert "Prime Agent" in lines[i_pi], lines[i_pi][:80]
NEW_EN = [
    "| **🆕 Odyssey** | https://odyssey.systems | — | "
    "**「生成式世界模型 + 免费公开研究预览」的第一现场**。**032 期首次命中（10/11 07:50 UTC）**——**`Odyssey-3`**："
    "**14B 参数生成式世界模型**（**模型 9/15 首次亮相**）；**自回归扩散 transformer，基于前一帧 + 用户最近动作逐帧生成**；"
    "**底座 832×480、Pro 1280×720**；**免费 demo 跑在 `Odyssey-3 Flash`**；"
    "**`Physics-IQ Verified` 视频到视频 66.1（单次运行 + 八选一；榜单要求四次并报标准差；去掉择选法四次平均 63.37）**；"
    "**`WorldMark` 第一人称风格化 77.2 / 第三人称真实 79.0 / 第三人称风格化 76.3 三项第一、第一人称真实 80.6 第三**；"
    "**创始人 Oliver Cameron 与 Jeff Hawke**；**与瑞士机器人公司 Flexion 合作人形**；**API 需申请**。"
    "⚠️ **权重未开放、且榜单两组数据都由 Odyssey 自己提交**（避坑 144）。补入 **T0 官方一手 · 国外** —— "
    "**「世界模型」自 031 期与「具身智能」合并设扫描位后的第一个国外样本** | 032 | 3 |",
]
lines[i_pi + 1:i_pi + 1] = NEW_EN

# T4：在 Talorys 行之后插入 2 行
i_tal = find_line("| **🆕 Talorys**")
assert "Cloudflare 免费层" in lines[i_tal], lines[i_tal][:80]
NEW_T4 = [
    "| **🆕 OrcaRouter** | https://orcarouter.ai（blog） | — | "
    "**「决策模型逐条拆解 + 权重 vs SKU 对照」的第一现场**。**032 期首次命中（10/11）**——"
    "**它是本报告看到的唯一一家把「权重已交付、发布说明未发」写清楚的源**（**官网 blog 索引停在 10/10、GitHub releases 停在 9/27 的 v0.4.0、"
    "公告只有 vLLM 官方 X 的一条转推**），并**逐项列出 `Decision 3.0` 六个检查点的参数量、底座与上传时间**；"
    "**同源另给出「`Decision 3.0` 权重 vs `Microsoft-Decision-1` SKU」对照**（**两边都没有 Brier / ECE**）。"
    "⚠️ **侧栏列的 `OrcaCyber Zero 1.5` / `OrcaVerify Text 1.0` 本期未核到官方发布稿，只作观察项**（避坑 44）。补入 **T4 聚合器与工具** | 032 | 3 |",

    "| **🆕 Inferse** | https://inferse.com/best/free-models | — | "
    "**免费模型目录的第二个独立口径**（**按上下文排序、逐条标注读自哪一页**）。**032 期首次命中（10/11）**——"
    "**本期它与 freellm.net 对同一批 OpenRouter `:free` 模型给出 22 vs 19 两个数字**（**口径差异在「是否把 `openrouter/free` 这个路由条目与 "
    "Google `Lyria` 两条预览各算一条」上**）。补入 **T4 聚合器与工具** —— **「同类源之间也要标口径」的第二个样本**"
    "（前例：freellm.net 与 freetokens.custats.info 的互补记账） | 032 | 3 |",
]
lines[i_tal + 1:i_tal + 1] = NEW_T4

s = "\n".join(lines)

# ---------- 6 freellm.net（缺口表内）就地更新 ----------
old_flm = ('**031 期同日重取（同一天第二轮）：500+ 模型 / 30 提供方 / 「免绑卡」417+ / '
           '更新至 2026-10-11 / 已实测 234** —— **重取后回落**，'
           '**是逐期记账以来第一次「先同值、后下降」**（**与 028 期「首次反向下降」同族：本报告只记数字、不推断原因**）')
new_flm = (old_flm +
           '；**032 期重取（10/12）：维持 500+ 模型 / 30 提供方 / 「免绑卡」417+ / 已实测 234 / '
           '该站 `Last Updated` 2026-10-11** —— **逐期记账以来第二次「重取后与上期同值」**'
           '（**第三次「重取后与上期同值」记为 030 期**；**照例只记数字、不据此写趋势**）')
s = rep(s, old_flm, new_flm, 1)

# ---------- 7 AIHOT 行就地更新 ----------
old_hot = "（避坑 140）。 | 031 | 237 |"
new_hot = (
    "（避坑 140）。 ⚠️ **032 期第二十八次逐期计数确认（操作禁令第十一次落地）**："
    "**该源 10/12 尚无条目**（凌晨时段）；**10/11 全天仍只有 1 条**（06:24 MarkTechPost「OpenAI 智能体逃逸 ExploitGym 并入侵 Hugging Face 基础设施」），"
    "**与 031 期记录一致、本期窗口内无新增**；**本期全部额度增量没有一条是它先报的** —— **边界第十一次以定论形式复用**；"
    "**本期新增第三条读数口径（重要）**：**它的「首页头条区」是按热度排序、可跨日堆积、且不含日期的，不能当「当日新闻」读** —— "
    "**本期头条区五条里 `Gemini 4 Argon` 那条只帮助确认「Argon 的发布已进入聚合层」，但必须回点原文才能定窗口归属**。"
    "**三条口径合起来**：① 强项在「当日技术 / 安全事件」、弱项在「当日商业权益」；② 时间戳为当地（GMT+8）、需逐条对时；"
    "③ **头条区按热度排序、不含日期**。 | 032 | 238 |"
)
s = rep(s, old_hot, new_hot, 1)

io.open(LEDGER, "w", encoding="utf-8").write(s)

# ---------- 8 复核 ----------
chk = io.open(LEDGER, encoding="utf-8").read().split("\n")
def cnt(a, b):
    n = 0
    for l in chk[a:b]:
        if l.startswith("|") and not l.startswith("| ---") and not l.startswith("| 信源"):
            n += 1
    return n

def idx(prefix):
    for i, l in enumerate(chk):
        if l.startswith(prefix):
            return i
    raise AssertionError(prefix)

top = idx("## T0 · 根节点")
t1 = idx("## T1 · 社区与社交")
t2 = idx("## T2 · Newsletter")
t3 = idx("## T3 · 媒体")
t4 = idx("## T4 · 聚合器与工具")
gap = idx("## 清单缺口")

n_t0 = cnt(top, t1)
n_t1 = cnt(t1, t2)
n_t2 = cnt(t2, t3)
n_t3 = cnt(t3, t4)
n_t4 = cnt(t4, gap)
print("表体行数：T0=%d T1=%d T2=%d T3=%d T4=%d" % (n_t0, n_t1, n_t2, n_t3, n_t4))
print("全表 =", n_t0 + n_t1 + n_t2 + n_t3 + n_t4)

def sub(prefix):
    i = idx(prefix)
    j = i + 1
    while j < len(chk) and not chk[j].startswith("###") and not chk[j].startswith("##"):
        j += 1
    return cnt(i, j)

print("  论文与预印本 =", sub("### 论文与预印本"))
print("  模型与开源 =", sub("### 模型与开源"))
print("  官方一手·国外 =", sub("### 官方一手 · 国外"))
print("  官方一手·国内 =", sub("### 官方一手 · 国内"))
print("  政策与监管 =", sub("### 政策与监管"))
print("  评测与榜单 =", sub("### 评测与榜单"))
print("  T3 国外 =", sub("### 国外"))
print("  T3 国内 =", sub("### 国内"))

assert sub("### 模型与开源") == 26, sub("### 模型与开源")
assert sub("### 官方一手 · 国外") == 35
assert sub("### 官方一手 · 国内") == 24
assert n_t0 == 132, n_t0
assert n_t1 == 19 and n_t2 == 18 and n_t3 == 39 and n_t4 == 27
assert n_t0 + n_t1 + n_t2 + n_t3 + n_t4 == 235
print("[OK] 台账更新完成：229 → 235，手写计数与表体行数同源 ✓")
