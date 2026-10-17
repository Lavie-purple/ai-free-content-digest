# -*- coding: utf-8 -*-
"""从 037 期 md 提取第四章截止表 -> 基准日 2026-10-17 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table038.md（纯表格块，供 038 期正文嵌入）。

六步（027 期定做法、028 期定型；037 期第十一次落地，本期第十二次）：
  1) 先断言行数（037 期 body = 193）
  2) 按行名子串套 REWRITE 字典（每键必须恰好命中 1 次）
  3) 正则重算每一行的「距今 N 天」（基准日 10/17，较上期 10/16 全部 +1 天）
  4) 未 REWRITE 的行做归属化（「本期」-> 「037 期」）
  5) 新行插在 ⚪ 存档块（首行 "| ⚪ **DeepSeek 10/15"）之前 -> 再断言总数
  6) 输出后由 inject038.py 注入正文占位符

⚠️ **本期新纪律**：行名内嵌「本期重取于 YYYY-MM-DD」的行（OpenRouter 免费档）在行名 diff 里会显示成「改名」，
它不是新条目 —— **改写时必须连行名一起改，且要单独在脚注里说明「行名有变」不等于「新增行」**。
"""
import re
from datetime import date

SRC = "AI免费内容与权益速递-第037期-2026-10-16.md"
OUT = ".workbuddy/tmp_table038.md"
BASE = date(2026, 10, 17)
PREV = 193

lines = open(SRC, encoding="utf-8").read().split("\n")
s = e = None
for i, l in enumerate(lines):
    if l.startswith("## 四、限时活动与截止时间表"):
        s = i
    if s is not None and l.startswith("## 五、"):
        e = i
        break
rows = [l for l in lines[s:e] if l.startswith("|")]
header, sep, body = rows[0], rows[1], rows[2:]
assert len(body) == PREV, len(body)

REWRITE = {}

REWRITE["老混元大模型平台停服"] = (
    "| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必须迁移到 TokenHub**。"
    "**10/17 高危窗口第 17 天**（9/25 自设倒排日已过 **22 天**；Q04 **连续第 26 期**未见确切日期，厂商只给「9 月底」）。"
    "⚠️ **一条「9 月底停服」拖到 10 月中下旬仍无日期，处置维持「按已停服对待、只做迁移」**——迁移动作本身不要等；"
    "⚠️ **同一家厂商两条线，一条无日期一条有精确到日的倒排**（元器 11/9，见下表），**说明「无日期」不是这家厂商的常态，而是这条线的常态**（避坑 164） |"
)

# ---- 本期新行之一：Vercel AI Gateway 限免 Beam（两个 slug，收尾方式相反）----
# ⚠️ 截止列**不能写可被 extract_deadlines 解析的实日期** —— 「限时免费」没有确切结束日（036 期纪律），
#    故写「未公布（限免结束日未公布）」，它是 pending 而非已过期。

REWRITE["Vercel AI Gateway 免费档"] = (
    "| 🟢 **Vercel AI Gateway 免费档（2 模型）** | 未公布 | 🟢 生效中。⚠️ **零价模型也要求绑卡**（避坑 73 同源）。"
    "**（038 期）本行新增一条限免，且官方不公布结束日期**：**10/16 起 `reflection/beam` 与 `reflection/beam-free` 两个 slug 同时 $0** —— "
    "**`reflection/beam` 免费期结束后自动切到定价、slug 不变、无停服；`reflection/beam-free` 免费期结束即停止服务**。"
    "⚠️ **同一模型、同一渠道、同一天，两个 slug 的收尾方式完全相反** —— **选错 slug 的后果不是「多花钱」而是「服务没了」**（避坑 161）。"
    "⚠️ **限免条件写得很窄：「由 Reflection AI 提供服务时免费」，换 provider 就不在范围内**。"
    "⚠️ **免费期没有确切结束日期**：**Vercel changelog 与 Reflection 官方博客都没写** —— "
    "**这是本报告第一个「限时免费但完全没有截止日」的干净样本，与同表 Together AI 那条「限免至 10/18（有明确日期）」恰成两端**（避坑 154：**「限时」这个词本身不构成日期**） |"
)

REWRITE["OpenRouter 免费档"] = (
    "| 🟢 **OpenRouter 免费档（`502+` 模型｜本期重取于 2026-10-17）** | 未公布（动态目录） | 🟢 生效中。"
    "**⚠️ 额度口径本期起必须写成「三源三个数、都带来源」**："
    "**① `freellm.net` OpenRouter 专页（`Last Updated 2026-10-17`）：19 个 `:free` 模型在线、主限流写「200 req/day」、免绑卡「Not required」**；"
    "**② `OpenRouter` 官方（经 `freetokens.fyi` 转录，`Last checked Oct 16`）：50 次/日，账号累计充值满 $10 后 1,000 次/日、20 次/分；负余额返回 402 且免费模型同样受限**；"
    "**③ `benchlm.ai`（Data refreshed October 16, 2026）**：与 ② 同口径。"
    "⚠️ **①② 在「日请求数」上直接冲突（200 vs 50），不可取中间值、不可只写一个**（避坑 161）。"
    "**本期经 freellm.net OpenRouter 专页重取：19 个 `:free` 模型在线**（逐条含 Model ID / 开发者 / 上下文 / 可用性），"
    "**其中本期新增 `xingchen-agi/xing4.0-29b-a4b:free`（262K）** —— 见下表独立行。"
    "⚠️ **freellm.net 首页计数器（`511+` 模型 / `30` 提供方）与 OpenRouter 专页（`19` 个在线）不是同一口径，不可相减**（避坑 68）。"
    "⚠️ **该站首页 `Latest free LLM API model update` 与 OpenRouter 专页 `Last Updated` 不同步，引用必须点名是哪一页** |"
)

REWRITE["Together AI `Muse Spark Open` 限免（渠道级"] = (
    "| 🟡 **Together AI `Muse Spark Open` 限免** | **10/18** | 🟡 生效中（**距今 1 天**）。"
    "**限免到期后是否续期，本期回扫未见公告** —— 按避坑 78「无信号即默认收口」处理。"
    "**常规 serverless 价为 $1.25 输入 / $4.25 输出 / 缓存读 $0.15 每百万 token**（10/16 调成 $0 之前的口径）。"
    "⚠️ **同表另有一条同日限免（Vercel 的 `Beam`）却没有结束日** —— **两条限免的「到期可预期度」完全不同，不要合并成「本周有两个限免」**（避坑 154）。"
    "⚠️ **本条与 `Muse Spark Open` 权重开放是两笔账**：权重开放是永久事实、限免是活动窗口（避坑 148/150 同族） |"
)

REWRITE["上海青浦算力券补贴"] = (
    "| 🟢 **上海青浦算力券补贴** | 申报至 **10/23** | 🟢 生效中（**距今 6 天**）。⚠️ 企业向；来源为青浦区官方发布。"
    "⚠️ **第三方清单口径**：「**最高补 30%、封顶 1,500 万**」（什么值得买 10/16 清单复核，数字与前期一致）。"
    "⚠️ **（038 期）窗口提示**：**今天距截止 6 天，申报制地方券的实操节奏通常是「材料准备 3–5 天 + 平台审核」**，"
    "**若首次申报，本周内应完成材料准备**（这是本表唯一一条「距今 6 天且需要线下材料」的条目） |"
)

REWRITE["阶跃 `Step 5 Preview` × 腾讯 WorkBuddy 独家限免"] = (
    "| 🟢 **腾讯 `Step 5 Preview` × WorkBuddy 独家限免** | **10/25** | 🟢 生效中（**距今 8 天**）。"
    "**零积分限免 600B MoE、原生 1M 上下文**。"
    "⚠️ **（038 期）状态不变**：**10/16 首销当天未见该限免延长或提前收口的公告**；"
    "**它是本表里与「权重已开放」并存的那条渠道级限免 —— 权重 10/15 已按承诺兑现、这条限免 10/25 到期，两者不可混成一句**（避坑 148/150）。"
    "⚠️ **`STEPX Neo` 10/16 首销后的销量与「星辰船票」名额本期未见公告**，不进本表（无日期不占截止位） |"
)

REWRITE["智谱 AutoClaw「每日登录领 credits」第二期"] = (
    "| ⚪ **智谱 AutoClaw「每日登录领 credits」第二期** | **10/16（北京，活动期 10/12–10/16）** | ⚪ **已按原定日期收口（10/17 回扫未见延期或提前收口公告）**。"
    "**（037 期登记的档位表口径全部不变）**：**10/12 首日全体 10,000 Credits（1 亿 GLM-5.3-Flash Tokens）；10/13–10/16 每日全体 800 Credits（800 万 Tokens）**；"
    "**付费会员额外每日奖励按档位（AutoClaw 月度订阅 Lite/Base/Pro/Max = 500 / 5,000 / 7,000 / 8,000 Credits；`GLM Coding Plan` 个人版 Lite/Pro/Max = 5,000 / 7,000 / 8,000 Credits）**。"
    "⚠️ **（038 期）第三期是否接上：本期仍未见公告 —— 连续第 2 期未见**（037 期已记「本期未见公告」）。"
    "**按 032 期定的「疑似实质违约候选」判据：厂商承诺的交付物按期是否出现是可判定的，超过一个自然周期就换档** —— "
    "**注意这条不适用于本条（第二期本身按期兑现了），只适用于「第三期是否存在」这个待定问题**（Q 见待澄清库）。"
    "⚠️ **每日奖励当天午夜过期、当日领当日用；每账号每日限领一次；多重会员只取最高档、不可叠加**（避坑 52） |"
)

REWRITE["Reflection Beam 开放权重"] = (
    "| 🟢 **Reflection Beam 开放权重** | **10/16（权重交付日）** | 🟢 **已于 10/16 按 10/5 承诺兑现**。"
    "501B 总参 / 23B 激活、**1M 上下文**、**Apache 2.0**（模型卡明确不禁止蒸馏 / 用输出训练 / 微调或合并）。"
    "**⚠️ （038 期）纠错三条**："
    "**① 「10/16 发布」是错的 —— 10/5 已宣布是开放权重模型、只是权重未放，10/16 是权重交付日**（避坑 142 的第五个日期在本条上完整成立）；"
    "**② 基准不可混用 —— 官方口径 `Terminal-Bench 2.1` 80.1%，而独立的 Artificial Analysis 给 `Terminal-Bench 4.0` 只有 3.0%，`2.1` 与 `4.0` 是两个不同版本的同名基准，不可比大小**（避坑 144 同族，**本期最实用的一条防误读**）；"
    "**③ 「Apache 2.0」不等于「没有闸门」—— 闸门在权重之外：HF 侧未见 gated 申请表，但 Reflection 自家 API 的免费 beta 结束后价格至今未公布**（避坑 162）。"
    "**独立榜单（10/16 当日）**：**智能指数 30 分（美国开放权重第二、全部开放权重第十）、`AA-Cyber` 34%（其测过的美国开放权重第一）、`AutomationBench-AA` 48.5%；但 `AA-Omniscience` 幻觉率 47%（对比 `K2 Horizon` 26%），净值 1.5 仍领先**。"
    "**⚠️ 跑起来要什么**：**BF16 约 1 TB / NVFP4 约 280 GB、官方建议至少 4 张 B200** —— **不是「人人本地跑」的模型**（避坑 41 第三层）。"
    "**同日 `Mirror CLI` 一并开源（Python 产品层 + Rust agent core）** —— 「模型 + harness 一起开源」与 `Muse Spark Open` 只放权重形成形态差别 |"
)

# ---- 本期新行 ----
NEW = [
    "| 🟡 **商务部 AI 技术出口管制目录修订 · 出口前登记** | **征求意见 10/16–11/15（登记自 10/16 即启动）；目录正式实施之日未公布** | "
    "🟡 **登记义务已生效、管制范围尚未落地**。"
    "**商务部、科技部 2026 年第 48 号公告（10/16）**：拟将**大模型 / 智能体 / 算力集群 / 信息处理 23 项 AI 技术**"
    "（三领域共 40 项，其中拟禁止 14 项、拟限制 26 项）增列进《中国禁止出口限制出口技术目录》，"
    "**并同步对附件所列技术启动「出口前登记」，已经开始但尚未完成的出口也在范围内**。"
    "**⚠️ 距今 29 天**（征求意见截止）。"
    "**四条豁免（决定哪些开源模型还能正常出海）**：**① 已开源或已发论文进入公共领域的技术不纳入；"
    "② 人工智能类技术开源、境外自建自营算力中心、赴境外芯片流片、利用境外资源联合研发、参与国际标准制定 —— "
    "适用自动许可等便利措施（基本「即报即出」）；③ 用限制类大模型对外提供 API 调用 / APP 网页交互 / SaaS 应用 / "
    "本地端侧轻量化部署 —— 不属于大模型技术出口管理范围；④ 纳入限制类的技术若开展海外本地化部署属于技术出口管理范围，"
    "但部署在海外自有云等风险可控情形可适用自动许可**。"
    "**⚠️ 不得写成「AI 技术出口已被管制」** —— **生效日与实施日是两件事（避坑 154 同族）**；"
    "**Q27 登记三个未定项（实施日 / 23 项技术指标线 / 适用主体）** |",

    "| 🟢 **`OpenCode` 限免 `Reflection Beam`（1M 上下文）** | **未公布（免费结束日期未公布）** | 🟢 生效中。"
    "**10/16–10/17 `OpenCode` 官方 X 宣布把 `Beam` 与 `GLM-5.3-Flash` 一并免费**（501B/23B MoE、1M 上下文）。"
    "⚠️ **与同平台 `GLM-5.3-Flash` 免费档的四条限制必须分开写**（后者：仅平台内 / 上下文 200K 而非 1M / 拒 PDF / 速度慢且不稳定）—— "
    "**本条 `Beam` 免费档官方未给出对应限制清单，也未公布结束日期**。"
    "**⚠️ 时序细节**：`Beam` 在 `OpenCode` 上的代号正是 `stealth/cat-jam`，即开发者此前已在 `OpenCode` 里用过它 —— "
    "**「今天宣布免费」与「此前已是隐身免费条目」是两件事**（避坑 117 / 142）。"
    "⚠️ **是否计入套餐额度、是否改变限速，本期未核到** |",

    "| 🟡 **中国电信 `Xing4.0-29B-A4B` 上架 OpenRouter 免费档** | **未公布（限免结束日未公布）** | 🟡 生效中。"
    "**`xingchen-agi/xing4.0-29b-a4b:free`，262K 上下文**（`freellm.net` OpenRouter 专页 `Last Updated 2026-10-17` 实跑，逐条标注厂商为 XingChen / China Telecom）。"
    "⚠️ **与 008 期那条「`Xing4.0` 开放权重」是两件事**：权重自 2026-09-16 起就在 HF `XingChen-AGI` 组织页可下载（Apache-2.0），"
    "**本期变化的是「出现了免费可调入口」—— 「权重公开」与「免费可调用」之间隔了整整一个月**（避坑 142）。"
    "⚠️ **免费档额度按 `OpenRouter` 官方口径**：**50 次/日（累计充值满 $10 后 1,000 次/日）、20 次/分** —— "
    "⚠️ **`freellm.net` 该页写「200 req/day」，与官方冲突，两个口径都写、不取其一**（避坑 161）。"
    "**架构字段**：**29B 总参 / 每 token 约 4B 激活、40 层、64 路由专家选 4 + 1 常开共享专家、`MLA` 压缩 KV、`MTP` 内训、原生 256K 可扩 512K**；"
    "⚠️ **`mHC` 四路 hyper-connection 结构需框架自定义内核（SGLang 为其专门发 split-K 内核）**；"
    "⚠️ **基准全为厂商模型卡自报、无独立复现**（避坑 116） |",

    "| 🟡 **Perplexity 开源 `SPACE` 沙箱平台（Apache 2.0）** | **未公布（Apache 2.0 永久；托管版定价未公布）** | 🟡 生效中。"
    "**10/15–10/16 开源 `SPACE`（Sandboxed Platform for Agentic Code Execution）**，即 `Perplexity Computer` 每个任务背后的沙箱，"
    "**Rust、release 0.8.0、Apache 2.0、GitHub `perplexityai/SPACE`**。"
    "**机制**：**每个 agent 任务一个独立 Firecracker microVM；凭证注入与出网策略在 VM 边界之外执行 —— secrets 永不进入 guest VM**。"
    "⚠️ **运行门槛**：**Linux x86_64 + KVM + btrfs + Docker；⚠️ 不支持 macOS**；默认空闲 6 小时自动挂起。"
    "⚠️ **性能与安全数字全部是厂商自报**（避坑 116）：中位创建延迟 185→60 ms；**逃逸测试 9 个前沿模型、108 次尝试 0 成功**"
    "（⚠️ 另一处独立转述给「118 次尝试 0 成功」，**两个数并存、都写、都带来源**）"
    "⚠️ **但同一批测试里「修复前 54 次部分网络运行中 11 次绕过出网策略」—— 「VM 逃逸 0 次」与「出网策略曾被绕过」是两件事，不能只写前者**。"
    "**⚠️ 分发形态**：**CoreWeave / Akamai / Crusoe 三家承诺提供给其客户，而托管版定价至今未公布**（避坑 41 第一层）。"
    "**Q28 登记两个未定项（开源版与生产配置是否一致 / 有无第三方独立逃逸测试）** |",
]

# ---- 套 REWRITE：每键恰好命中 1 次 ----
rw = 0
out = []
for line in body:
    hit = None
    for k in REWRITE:
        if k in line:
            assert hit is None, ("一行命中两个 REWRITE 键", k, hit, line[:60])
            hit = k
    if hit:
        out.append(REWRITE[hit])
        rw += 1
    else:
        out.append(line)

# ---- 未 REWRITE 的行做归属化：本期 -> 037 期 ----
for i, l in enumerate(out):
    if l not in REWRITE.values():
        out[i] = l.replace("（037 期）", "（037 期）").replace("本期重取于 2026-10-16", "上期重取于 2026-10-16")
        out[i] = out[i].replace("037 期复核维持", "037 期复核维持，038 期未检出新变化")

# ---- 正则重算「距今 N 天」 ----
# ⚠️ **不能从旧天数 +1**：基准日推进一天时，旧天数与行内真实截止日期可能不是同一条
#    （036 期已记：`extract_deadlines` 不解析状态列里的倒计时文本，脚本守卫覆盖不到）。
# **正确做法：从行内「截止」列的日期重新算 delta**。
# ⚠️ **换挡日 / 非活动截止日期不能被解析**（036 期纪律：写 `10/14 00:30（北京）` 会被吞成截止日），
#    所以这里只认 `**10/23**`、`**10/25**` 这类带横线的完整日期，或 `M/D` 形式；带「北京」括注的一律跳过。
DATE_FULL = re.compile(r"\*\*(\d{4})-(\d{1,2})-(\d{1,2})\*\*")
DATE_MD = re.compile(r"\*\*(\d{1,2})/(\d{1,2})\*\*")

def recompute(l):
    if "距今" not in l:
        return l
    # 优先取「截止」列（第 2 列）里的日期
    cols = l.split("|")
    target = cols[2] if len(cols) > 3 else ""
    # 若截止列含「北京」等括注或「未公布」，则不动
    if "北京" in target or "未公布" in target or "以" in target:
        return l
    m = DATE_FULL.search(target)
    if m:
        d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    else:
        m2 = DATE_MD.search(target)
        if not m2:
            return l
        d = date(2026, int(m2.group(1)), int(m2.group(2)))
    delta = (d - BASE).days
    if "距今" not in l:
        return l
    return re.sub(r"\*\*距今 -?\d+ 天\*\*", "**距今 %d 天**" % delta, l)

out = [recompute(l) for l in out]

# ---- 插入新行：插在 ⚪ 存档块（首行以 "| ⚪ **DeepSeek 10/15" 开头）之前 ----
anchor_idx = None
for i, l in enumerate(out):
    if l.startswith("| ⚪ **DeepSeek 10/15"):
        anchor_idx = i
        break
assert anchor_idx is not None, "未找到 ⚪ 存档块锚点"
out = out[:anchor_idx] + NEW + out[anchor_idx:]

assert len(out) == PREV + len(NEW), (len(out), PREV + len(NEW))

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(header + "\n" + sep + "\n")
    f.write("\n".join(out) + "\n")

print("rows = %d（原 %d + 新增 %d）" % (len(out), PREV, len(NEW)))
print("rewrites = %d" % rw)
print("REWRITE 键数 = %d（每键已断言恰好命中 1 次）" % len(REWRITE))
print("新行名：")
for n in NEW:
    print("  " + n[2:n.index("|", 2)].strip())