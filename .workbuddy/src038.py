# -*- coding: utf-8 -*-
"""038 期台账（信源分级清单）更新：新增 3 条信源行 + 同步 5 处手写计数 + 版本行补登。

本期三条新信源（**先搜重后落节**，037 期「加行前必须先搜这一行是不是已经有了」的同族纪律）：

1. **T0 政策与监管 +1** —— **商务部 / 科技部（技术进出口管制公告 + 商务部业务系统统一平台）**
   本期头条政策线一手现场：公告 2026 年第 48 号把 23 项 AI 技术拟增列进出口管制目录，
   **并同步启动「出口前登记」**。这是本清单第一次拿到「征求意见窗口 + 登记启动日」两个日期的
   政策原文，也是第一次拿到「哪些情形不属于技术出口」这条**豁免边界**的一手表述。
   ⚠️ 搜重结论：台账政策与监管节**只有工信部一家部委**，商务部此前以「地方政府门户」形式出现过，
   但**不是这一行** → 属真新增。

2. **T0 官方一手 · 国外 +1** —— **Vercel（AI Gateway changelog + 定价页）**
   本期 `Beam` 限免的两个 slug（`reflection/beam` / `reflection/beam-free`）**收尾方式不同**，
   且**官方不公布限免结束日期** —— 「渠道级限免」这一形态的一手现场。
   ⚠️ 搜重结论：台账里 `Vercel` 只出现 2 次，均在正文说明中（T4 缺口语料段），
   **表格里没有这一行** → 属真新增。

3. **T4 +1** —— **AICoder（aicoder.com，含 RSS + 模型定价库）**
   本期**唯一在窗口内提供逐条带时间戳、且把「免费但无截止日期」显式标出来的聚合源**。
   ⚠️ 搜重结论：`aicoder` 在台账中 0 命中 → 属真新增。
   它同时是「发布方式追踪位」（032 期立的第 14 类缺口）的一个新样本：
   **条目把原始出处写成 `Source: 厂商官方 X 账号` 一行，而不是给公告 URL**。

计数同步（**T0 内部分类复核那一行的括注是历史基线标签，不要改名，只在行尾追加**）：
  T0 根节点 147 → 150；政策与监管 21 → 22；官方一手·国外 39 → 40；T4 31 → 32
  顶层求和 256 → 259
"""
import io, os, re

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(WS, "AI信息源分级清单-T0-T4.md")
BAK = os.path.join(WS, ".workbuddy", "tmp_src_bak038.md")


def audit(txt, label):
    sec_re = re.compile(r"^(#{2,3}) (.+?)（(\d+)）\s*$")
    cur = cur_decl = None
    cur_n = 0
    rep, tops = [], []

    def flush():
        if cur:
            rep.append((cur, cur_decl, cur_n))

    for l in txt.split("\n"):
        m = sec_re.match(l)
        if m:
            flush()
            cur, cur_decl, cur_n = m.group(2).strip(), int(m.group(3)), 0
            if l.startswith("## "):
                tops.append((m.group(2).strip().split()[0], cur_decl))
            continue
        if l.startswith("| ") and not l.startswith("| 信源 ") and "---" not in l:
            if cur:
                cur_n += 1
    flush()
    if label:
        print("\n=== %s ===" % label)
        for name, d, c in rep:
            if c == 0:
                tag = "n/a（顶层，本身不带数据行）"
            elif name.startswith("T4"):
                tag = "n/a（含表外补登行，括号口径≠表内行数）"
            else:
                tag = "OK" if d == c else "<<< MISMATCH"
            print("  %-28s 括号 %3d / 实际 %3d  %s" % (name[:28], d, c, tag))
    return dict((n, (d, c)) for n, d, c in rep), dict(tops)


base_rep, base_tops = audit(io.open(BAK, encoding="utf-8").read(), None)
txt = io.open(F, encoding="utf-8").read()

# ---- 0) 搜重：三行在插入前必须都不存在（037 期纪律：加行前先搜这一行是不是已经有了）----
for probe in ["商务部安全与管制局", "Vercel AI Gateway changelog", "AICoder"]:
    assert txt.count(probe) == 0, ("疑似重复登记", probe, txt.count(probe))
print("搜重：三条候选信源在台账中均 0 命中 → 均可登记")


def insert_after(anchor, row):
    global txt
    assert txt.count(anchor) == 1, ("anchor not unique", anchor[:70], txt.count(anchor))
    idx = txt.index(anchor)
    end = txt.index("\n", idx) + 1
    txt = txt[:end] + row + "\n" + txt[end:]


# ---- 1) T0 政策与监管：+1 行（6 列：信源 | 地址 | RSS | 对本报告的用途 | 上次命中 | 命中次数）----
POLICY_ANCHOR = "| 工业和信息化部 | https://www.miit.gov.cn | — | 产业政策 | 028 | 1 |"
assert txt.count(POLICY_ANCHOR) == 1
insert_after(POLICY_ANCHOR,
    "| **🆕 商务部 / 科技部（技术进出口管制公告 + 商务部业务系统统一平台）** | https://www.mofcom.gov.cn · "
    "https://ecomp.mofcom.gov.cn | — | "
    "**「出口前登记」这一形态的第一现场**。**038 期首次命中**——**商务部、科技部 2026 年第 48 号公告**"
    "（10/16）拟将**大模型 / 智能体 / 算力集群 / 信息处理 23 项 AI 技术**增列进《中国禁止出口限制出口技术目录》"
    "（三领域共 40 项，其中拟禁止 14 项、拟限制 26 项），**并同步对附件所列技术启动「出口前登记」**"
    "（登记即日起至目录正式实施之日止，已开始未完成的出口也在范围内）。"
    "**两个日期要分开记**：**征求意见 10/16–11/15**，**登记自 10/16 即启动**；"
    "**四条豁免是本条最该抄下来的部分**——① 已开源或已发论文进入公共领域的技术**不纳入**；"
    "② 人工智能类技术开源、境外自建自营算力中心、赴境外芯片流片、利用境外资源联合研发、参与国际标准制定"
    "**适用自动许可等便利措施**（基本「即报即出」）；③ 用限制类大模型对外提供 **API 调用 / APP 网页交互 / "
    "SaaS 应用 / 本地端侧轻量化部署，不属于**大模型技术出口管理范围；④ **海外本地化部署属于**技术出口管理范围，"
    "但部署在海外自有云等风险可控情形可适用自动许可。"
    "⚠️ **这是「免费内容 / 权益」报告里第一条会影响开源模型跨境可用性的政策变量** | **038** | 1 |"
    " |")

# ---- 2) T0 官方一手 · 国外：+1 行（Vercel）----
INTL_ANCHOR = "| Cohere Blog | https://cohere.com/blog | ✅ | 配额调整 | 037 | 18 |"
if txt.count(INTL_ANCHOR) != 1:
    # 退化路径：取该小节内第一行数据行作为锚
    m = re.search(r"(### 官方一手 · 国外（39）\n\n\| 信源 \|[^\n]*\n\| --- \|[^\n]*\n)", txt)
    assert m, "官方一手·国外 小节表头未找到"
    anchor = txt[m.end():txt.index("\n", m.end())]
    assert txt.count(anchor) == 1
    insert_after(anchor,
        "| **🆕 Vercel（AI Gateway changelog + 定价页）** | https://vercel.com/changelog · "
        "https://vercel.com/ai-gateway | — | "
        "**「渠道级限免」的一手现场**。**038 期首次命中（10/16）**——**`Reflection Beam` 在 AI Gateway 上同时给了两个 slug**："
        "**`reflection/beam`**（免费期内 $0，**免费期结束后自动切到定价、slug 不变、无停服**）与 "
        "**`reflection/beam-free`**（现在 $0，**免费期结束即停止服务**）。"
        "⚠️ **同一模型、同一个渠道、同一天，两个 slug 的收尾方式完全相反** —— "
        "**且官方 changelog 与 Reflection 官方博客都没有给出限免的确切结束日期**（这是本期「限免无截止日」的第一个样本）；"
        "另该页明确写出 **AI Gateway 不加价、不收平台费（含 BYOK 请求）** | **038** | 1 |"
        " |")
    print("Vercel 行：走退化锚点插入")
else:
    insert_after(INTL_ANCHOR,
        "| **🆕 Vercel（AI Gateway changelog + 定价页）** | https://vercel.com/changelog · "
        "https://vercel.com/ai-gateway | — | "
        "**「渠道级限免」的一手现场**。**038 期首次命中（10/16）**——**`Reflection Beam` 在 AI Gateway 上同时给了两个 slug**："
        "**`reflection/beam`**（免费期内 $0，**免费期结束后自动切到定价、slug 不变、无停服**）与 "
        "**`reflection/beam-free`**（现在 $0，**免费期结束即停止服务**）。"
        "⚠️ **同一模型、同一个渠道、同一天，两个 slug 的收尾方式完全相反** —— "
        "**且官方 changelog 与 Reflection 官方博客都没有给出限免的确切结束日期**（这是本期「限免无截止日」的第一个样本）；"
        "另该页明确写出 **AI Gateway 不加价、不收平台费（含 BYOK 请求）** | **038** | 1 |"
        " |")
    print("Vercel 行：走正常锚点插入")

# ---- 3) T4：+1 行（AICoder）----
T4_ANCHOR = "| **🆕 AI Agent Store** | 见其模型卡片与价格页 | — |"
assert txt.count(T4_ANCHOR) == 1
insert_after(T4_ANCHOR,
    "| **🆕 AICoder（aicoder.com）** | https://aicoder.com · https://aicoder.com/rss.xml | ✅ | "
    "**「逐条带 GMT 时间戳的发布流」+「免费但无截止日期」显式标注位**。**038 期首次命中**——"
    "它把当日发布按 `Sat, 17 Oct 2026 00:0X:XX GMT` 精确到分钟排序（**做窗口接缝判定时可直接用**），"
    "并在每条末尾写 `Source: 厂商官方 X 账号` 一行；**其价格目录把「免费」与「限免但未给结束日期」分成两栏**，"
    "本期实测两条 `OpenCode` 免费条目都落在「免费但未提供截止日期」栏。"
    "⚠️ **它是「发布方式追踪位」（032 期第 14 类缺口）的新样本**：**条目给的是 X 账号而不是公告 URL**，"
    "必须回一手页复核；另其独立评测数字（`SWE-bench Verified 81.6%` 等）与 Artificial Analysis 口径**不可混用** | **038** | 1 |"
    " |")

# ---- 4) 同步 5 处手写计数 ----
# ⚠️ **首版这里把 `## T0 · 根节点` 写成了 147 → 150（+3），而实际只往 T0 插了 2 行** ——
# **顶层求和因此变成 +4，与「有意图的插入数」不符，当场被逐节核对抓住。**
# **T0 根节点必须等于它六个子节的求和**：12 + 33（+0）+ 40（+1）+ 25 + 22（+1）+ 17 = **149**。
# 这正是 036 期写的「改完要做一次逐节行数自检」的同族纪律，**而 `audit()` 把 `c == 0` 的顶层标 n/a 不判错，
# 顶层只能靠「求和 vs 插入数」这一条断言兜住** —— 所以顶层断言必须单独写、不能只靠逐节核对。
COUNT_FIX = [
    ("## T0 · 根节点（147）", "## T0 · 根节点（149）"),
    ("### 官方一手 · 国外（39）", "### 官方一手 · 国外（40）"),
    ("### 政策与监管（21）", "### 政策与监管（22）"),
    ("## T4 · 聚合器与工具（31）", "## T4 · 聚合器与工具（32）"),
]
for old, new in COUNT_FIX:
    n = txt.count(old)
    assert n == 1, ("count-anchor not unique", old, n)
    txt = txt.replace(old, new)

# ---- 5) 版本行（第 3 行）追加 038 期登记 ----
lines = txt.split("\n")
assert lines[2].startswith("**版本**"), lines[2][:40]
lines[2] = (lines[2][:-2] + "；就地更新至 **2026-10-17（038 期，条目数 256 → 259；"
    "**T0 政策与监管 +1**（**商务部 / 科技部（技术进出口管制公告 + 商务部业务系统统一平台）** —— "
    "**「出口前登记」这一形态的第一现场**：公告 2026 年第 48 号拟将 **23 项 AI 技术**（大模型 / 智能体 / "
    "算力集群 / 信息处理）增列进《中国禁止出口限制出口技术目录》，**并自 10/16 起对附件所列技术启动出口前登记**，"
    "征求意见到 **11/15**；**四条豁免边界首次拿到一手表述**，其中「用限制类大模型对外提供 API / APP / SaaS / "
    "端侧轻量部署**不属于**技术出口管理范围」是本报告最该抄下来的一句 —— **这是「免费内容 / 权益」报告里"
    "第一条会影响开源模型跨境可用性的政策变量**）/ "
    "**T0 官方一手 · 国外 +1**（**Vercel（AI Gateway changelog + 定价页）** —— 「渠道级限免」的一手现场："
    "**同一模型同一天两个 slug、收尾方式完全相反**，且**官方不公布限免结束日期**）/ "
    "**T4 +1**（**AICoder（aicoder.com）** —— 「逐条带 GMT 时间戳的发布流」+ **把「免费但无截止日期」"
    "显式标成一栏**，是本期做窗口接缝判定最省事的一个源；⚠️ 它给的是 X 账号不是公告 URL，**属「发布方式追踪位」新样本**）"
    "→ **256 → 259**，其中 **T0 合计 147 → 149**（**政策与监管 21 → 22、官方一手 · 国外 39 → 40**；"
    "**论文与预印本 12、模型与开源 33、官方一手 · 国内 25、评测与榜单 17 均不变**）、**T4 31 → 32**"
    "（**T1 19、T2 18、T3 41 均不变**）；**手写计数五处同步**（`## T0 · 根节点（147→149）`、"
    "`### 官方一手 · 国外（39→40）`、`### 政策与监管（21→22）`、`## T4 · 聚合器与工具（31→32）`，"
    "以及版本行本身）—— **站点首页「信源 N 条」= 五个 `## T\\d …（N）` 标题求和**；"
    "**AIHOT 边界第三十四次确认**（本期为 12:00 截止的午间刊，**当日条目尚未进入其归档节奏**，按 029 期纪律"
    "**不写具体条数**）；**本期就地更新 1 行**：**freellm.net**（**OpenRouter 专页重取：19 个 `:free` 模型在线 / "
    "`Last Updated` 推进到 2026-10-17** —— ⚠️ **但首页计数器仍是 511+ 模型 / 30 提供方，与 037 期同值，"
    "且该站 OpenRouter 专页与首页的日���本不同步，引用必须点名是哪一页**）；"
    "**038 期另逐条核对用户随任务提供的 T0–T4 补充清单**：**与台账逐条比对无新增项、无缺项，"
    "故不产生条目增删**（**其中 T0=97 / T1=19 / T2=18 / T3=36 / T4=12 = 182 条是分级清单的原始基线，"
    "与台账当前 259 条不是同一口径、不可相减**）。**）**）")

txt = "\n".join(lines)
io.open(F, "w", encoding="utf-8", newline="\r\n").write(txt)

# ---- 6) 逐节核对：括号数 == 实际行数，且相对基线的增量 == 有意图的插入数 ----
new_rep, new_tops = audit(txt, "038 期台账逐节核对")
top_sum = sum(new_tops.values())
base_sum = sum(base_tops.values())
print("\n顶层求和 = %d（基线 %d，增量 %+d）" % (top_sum, base_sum, top_sum - base_sum))

# ⚠️ **顶层断言必须单独写**：`audit()` 把 `c == 0` 的顶层标题标 n/a 不判错，
# 所以「顶层求和是否等于基线 + 有意图的插入数」这一条只能靠这里兜住（本期首版就是在这里被抓住的）。
INSERTED = 3  # 政策与监管 1 + 官方一手·国外 1 + T4 1
assert top_sum - base_sum == INSERTED, ("顶层求和与插入数不符", top_sum - base_sum, INSERTED)
assert new_tops["T0"] == sum(v[0] for k, v in new_rep.items()
                             if k in ("论文与预印本", "模型与开源", "官方一手 · 国外",
                                      "官方一手 · 国内", "政策与监管", "评测与榜单")), \
    ("T0 根节点数不等于其六个子节求和", new_tops["T0"])
print("顶层求和断言：ALL GREEN（增量 == 有意图的插入数 %d）" % INSERTED)
print("T0 根节点 %d == 六子节求和 ✅" % new_tops["T0"])

EXPECT = {"政策与监管": 1, "官方一手 · 国外": 1}
bad = []
for name, (d, c) in new_rep.items():
    if c == 0 or name.startswith("T4"):
        continue
    bd, bc = base_rep[name]
    want = EXPECT.get(name, 0)
    if d != c or (d - bd) != want or (c - bc) != want:
        bad.append((name, (bd, bc), (d, c), "want +%d" % want))
if bad:
    for b in bad:
        print("  MISMATCH", b)
    raise SystemExit("逐节核对不过")
print("逐节增量核对：ALL GREEN（政策与监管 +1、官方一手·国外 +1，其余不变）")
print("顶层：", new_tops, "求和 =", sum(new_tops.values()))

# T4 用「表内行数增量」单独核
print("T4 括号 31 -> 32；表内行数增量应为 +1（T4 含表外补登行，括号口径 ≠ 表内行数）")