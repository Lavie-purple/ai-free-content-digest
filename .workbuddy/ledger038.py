# -*- coding: utf-8 -*-
"""038 期冻结库与待澄清库更新。

库内改动分三档记账（035 期定）：**首登（追加新行）/ 补登（报道时点落上期窗口、本期才登记）/ 改写（往期条目本期有实质进展）**。
⚠️ **`check_frozen` 的「首登 N」只算首登、不含改写** —— 两者必须分开计数。
⚠️ **顺序必须是「先写库、再跑守卫」**：它的首登判据字段就是本期才写入的内容。
⚠️ **`data/` 下是 CRLF** —— 写回必须 `newline="\\r\\n"`，否则 `git diff --stat` 会显示成整文件重写。

本期记账：**首登 8 条 + 改写 3 条**（无补登 —— 窗口内 7 条硬条目全部落在线后，无一条落在 037 期窗口）。
"""
import io, os, shutil

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
FROZEN = os.path.join(D, "frozen_items.md")
OQ = os.path.join(D, "open_questions.md")

# ---------- 备份（就地，CRLF 保持） ----------
shutil.copyfile(FROZEN, os.path.join(D, ".frozen_bak038.md"))
shutil.copyfile(OQ, os.path.join(D, ".open_questions_bak038.md"))

# ---------- 改写行（往期条目本期有实质进展） ----------
REWRITE = {
    "| Meta Muse Spark Open 开放权重 | 037 |": (
        "⚠️ **038 期新增一条独立复现事实（不改变本条定性）**：**Artificial Analysis 已给 `Muse Spark Open` "
        "记 39 分并在同表里把 `Beam`（30）列为「美国开放权重第二」、`Nemotron 3.5 Super VL`（26）第三** —— "
        "**即 037 期记的「AA 39 分落后 GLM-5.3 44 与 Kimi K3 45」这条，本期被独立榜单正式确认**，"
        "且「美国开放权重第一」这个位置在同一周内被三款模型先后占据（037 期登记的 Meta → 038 期登记的 "
        "`Beam` → 同期 `Nemotron 3.5 Super VL`）。**这条印证了 037 期的避坑 165："
        "「最强」是一周就会过期的话术，写下来时必须带核对日**（避坑 142 第五个日期）。"
        "**037 期其余口径全部维持不变**"
    ),
    "| 阶跃星辰 Step 5 Preview 开源权重 | 037 |": (
        "⚠️ **038 期新增一条合规对照事实（不改变本条定性）**：**同一天（10/16）`Reflection Beam` 以 "
        "**Apache 2.0** 放出 501B 权重，官方明确「不禁止蒸馏、不禁止用输出训练、不禁止微调与合并」** —— "
        "**与本条的 `StepFun Model License 1.0`（三条商业闸门）、037 期登记的 `Muse Model License`、"
        "同日的 `Ling-3.1-flash`（MIT）构成同一周内四种并存的许可证形态**。"
        "**「开源」这四个字在本周的四条样本里对应四种完全不同的合规动作**（避坑 158 / 162）。"
        "**036–037 期其余口径全部维持不变**"
    ),
    # ⚠️ **行名从正文抄一定会抄错**（037 期纪律）：正文写「012 期那条 `Xing4.0`」，
    # 而库里真实行名是 `| Xing4.0-29B-A4B | 008 |` —— **首登期是 008（信源另有一条 012 期的行）**。
    "| Xing4.0-29B-A4B | 008 |": (
        "⚠️ **038 期新增一条「权重早已在、可用性才是本期变化」的对照事实**：**`Xing4.0-29B-A4B` 的 "
        "Apache-2.0 权重自 2026-09-16 起就在 HF `XingChen-AGI` 组织页可下载，而多篇 10/17 稿把它当新模型发布** —— "
        "**第三个来源（`orcarouter`）明确纠正了这一点**。**本期真正变化的是「可调用」而非「可下载」**："
        "**10/15–10/16 出现带 262,144 token 上下文窗口的商业上架、13 日量化构建跟上、SGLang 支持 PR 从 draft "
        "转可合并、vLLM 已带该架构**；⚠️ **同时 `OpenRouter` 上已出现 `xingchen-agi/xing4.0-29b-a4b:free` "
        "免费档（262K）** —— **即「权重公开」与「免费可调」之间可以隔一个月**（避坑 142）。"
        "⚠️ **`orcarouter` 另给一组值得抄的架构字段：40 层、hidden 3,584、64 路由专家选 4 + 1 常开共享专家、"
        "`MLA` 压缩 KV、`MTP` 多 token 预测内训、256K 原生可扩到 512K**；"
        "**其自陈一个真实部署门槛：SGLang 为该模型的四路 hyper-connection 结构专门发了 split-K 内核**。"
        "**008 期登记的其余口径不变**"
    ),
}

# ---------- 首登行（本期新增，报道时点落在线后） ----------
NEW_ROWS = [
    (
        "Reflection AI Beam 开放权重",
        "038",
        "开源",
        "**Reflection AI 于 2026-10-16 13:01 UTC（北京 10/16 21:01）正式开放其首个开放权重模型 `Beam` 的权重**，"
        "**恰落在 037 期扫描截止（10/16 21:00）之后 1 分钟 —— 本期窗口接缝最紧的一条**"
        "（官方博客 `reflection.ai/blog/beam-is-available`、HF `reflection` 组织页、Vercel changelog、"
        "`artificialanalysis.ai/articles/reflection-beam`、`linkloot.io`、`artificialwatch.com`、"
        "`myaiguide.co` 日报、`aicoder.com` 多源）。"
        "**⚠️ 先纠正一条广泛流传的错误**：**`Beam` 不是「10/16 发布的新模型」—— 10/5 就已宣布是开放权重模型，"
        "只是当时权重未放；10/16 是权重交付日**（避坑 142 的第五个日期在本条上完整成立："
        "**公告日 10/5 ≠ 权重上传日 10/16**）。"
        "**规格**：**稀疏 MoE、总参 501.3B（501B）/ 每 token 激活 23.4B（23B）、52 层（3 稠密 + 49 MoE）、"
        "256 专家 top-8、文本进文本出、上下文 1M token、最大输出 128K token、知识截止 2026-06-30**。"
        "**权重格式**：**BF16 / FP8 / NVFP4 三档 + 一个投机解码 drafter 模型（2B）**；"
        "⚠️ **BF16 权重约 1 TB、NVFP4 约 280 GB、官方建议至少 4 张 B200**（避坑 41 第三层："
        "**它不是「人人本地跑」的模型**）。"
        "**⚠️ 许可证是本条最干净的一条：Apache 2.0，且模型卡明确「不禁止蒸馏、不禁止用其输出训练、"
        "不禁止微调或合并」** —— **与 037 期登记的 `Muse Spark Open`（`Muse Model License`，署名 + $20M MaaS 另签）"
        "和同日的 `Ling-3.1-flash`（MIT）形成三方对照**（避坑 158 / 162）。"
        "⚠️ **但「Apache 2.0」不等于「没有闸门」—— 闸门在权重之外**："
        "**HF 侧为普通公开仓库（未见 gated 申请表，与 `Muse Spark Open` 的「要填出生日期」不同）**，"
        "**但 Reflection 自家 API 是免费公开 beta、免费期结束后的价格至今未公布**。"
        "**⚠️ 独立榜单（Artificial Analysis，10/16 发布当日）给出的四个数必须一起读**："
        "**智能指数 30 分（美国开放权重第二、全部开放权重第十）；`AA-Cyber` 指数 34%（其测过的美国开放权重第一）；"
        "`AutomationBench-AA` 48.5%；而 `Terminal-Bench 4.0` 仅 3.0%**（落后 `Qwen3.8 27B` 5.6% 与 "
        "`Muse Spark Open` 8.1%）—— ⚠️ **同表内 `AA-Omniscience` 答对 33% 领先同侪，但幻觉率 47% "
        "（对比 `K2 Horizon` 26%、`Qwen3.8 27B` 30%），净值 1.5 仍领先（−3.0 / −10.0）**；"
        "**token 效率是它真正的卖点：约 26k 输出 token / 指数题（约 19k 推理 + 约 7k 答案），"
        "而 `K2 Horizon` 用约 52k；但只有 26% 的输出用于最终答案，是 219 款受测模型里第 28 低**（避坑 165）。"
        "⚠️ **厂商自报与独立实测不一致，必须两套都写**：**官方 BF16 口径 `SWE-bench Verified` 81.6%、"
        "`Terminal-Bench 2.1` 80.1%、`GPQA Diamond` 90.6%、`AIME 2026` 97.7%、`HLE` 36.0%（无工具）/ 51.1%（有工具）；"
        "**而独立的 `Terminal-Bench 4.0` 只有 3.0% —— `2.1` 与 `4.0` 是两个不同版本的同名基准，不可比大小**"
        "（避坑 144 同族，**这是本期最实用的一条防误读**）。"
        "**⚠️ 训练规模是本条另一个「数字很大但要读清楚」的样本**：**RL 全程约 13 亿个 sandbox，"
        "峰值 883,006 vCPU（占可分配 83%）横跨 GCP 与 AWS 23 个集群；官方称在 1 万张 GB300 上跑出 1 亿+ 次 rollout**。"
        "**生态**：**40+ 伙伴**，含 AWS / Google Cloud / Microsoft Foundry / Oracle / Cloudflare / CoreWeave / "
        "Databricks / Fireworks / Baseten / Modal / Nebius / Nscale / Together AI / OpenRouter / Vercel / "
        "NVIDIA NIMs / Ollama / LM Studio / OpenCode；**本地与主权部署由 Dell 与 HPE 交付**；"
        "**推理栈 day-0：Transformers / vLLM（Inferact）/ SGLang（RadixArk）/ Unsloth / Axolotl / "
        "TokenSpeed（LightSeek Foundation）/ Dynamo（NVIDIA）**；"
        "**训练侧合作 NVIDIA（NeMo RL、AutoModel、Megatron）、RadixArk（Miles）、HF TRL、Anyscale SkyRL、Axolotl**，"
        "并承诺向 **Hugging Face `OpenEnv`** 贡献开放环境标准。"
        "**⚠️ 同日开源的还有它自己的 harness `Mirror CLI`**（**Python 产品层 + Rust agent core**，"
        "支持可恢复会话、独立 worktree 里的并行 agent、工具调用需批准）—— "
        "**「模型 + harness 一起开源」是本条与 037 期 `Muse Spark Open`（只放权重）的形态差别**。"
        "**⚠️ 隐身期两个代号要记**（避坑 117 同族）：**`stealth/cat-jam`（OpenCode）与 "
        "`stealth/missingno`（Nous Portal）** —— **`missingno` 这个代号此前属于 `Nous Research` 的另一款模型，"
        "同名不同物，读到这两个代号时必须连发布方一起读**。"
        "**⚠️ 第三方记录的两处「当时还没有」**：**ArtificialWatch 10/16 13:58 UTC 记「OpenRouter 目录当时还没有 "
        "Beam 的 id」** —— **这与本期重取到的 `OpenRouter` `:free` 列表不含 Beam 并不矛盾："
        "免费档与付费上架是两件事（避坑 148）**"
    ),
    (
        "Vercel AI Gateway 限免 Beam（双 slug）",
        "038",
        "额度",
        "**Vercel 于 10/16 在 AI Gateway 上架 `Reflection Beam` 并限免，官方 changelog 给出两个 slug、"
        "收尾方式完全相反（Vercel changelog `Reflection AI's Beam now available on AI Gateway for free`，"
        "作者 Jerilyn Zheng / Kevin Dawkins / Walter Korman / Zachary Chen，16 Oct 2026）**："
        "**① `reflection/beam` —— 免费期内 $0 / $0，限免结束后该 slug 自动切到定价、slug 不变、无停服**；"
        "**② `reflection/beam-free` —— 现在 $0 / $0，限免结束即停止服务**。"
        "**⚠️ 本条的全部信息量就是这一条对照**：**同一模型、同一个渠道、同一天，两个 slug 一个「无缝转正」"
        "一个「到期即死」** —— **选错 slug 的后果不是「多花钱」而是「服务没了」**。"
        "**⚠️ 免费期没有确切结束日期**：**Vercel changelog 与 Reflection 官方博客都没写，"
        "第三方（`linkloot.io`）明确写「两家都没公布，把它当开放式、依赖前盯 changelog」** —— "
        "**这是本报告第一个「限免无截止日」的干净样本，与 037 期登记的 Together AI 限免至 10/18（"
        "有明确日期）恰好构成两端**（避坑 154：**「限时」这个词本身不构成日期**）。"
        "**同页另两条可抄的口径**：**AI Gateway 不加价、不收推理平台费（**含 BYOK 请求**）**；"
        "**接入方式为标准模型名或 `-free` 后缀，均走 AI SDK / Chat Completions，"
        "`npx vercel ai-gateway setup` 可把 `reflection/beam` 或 `reflection/beam-free` 接进 "
        "Claude Code / Codex / Cursor**。⚠️ **限免条件写得很窄：「由 Reflection AI 提供服务时免费」** —— "
        "**换 provider 就不在限免范围内**（避坑 161：**同价不同范围**）。"
        "⚠️ **另一处独立口径差异**：**`huggingnews` 引 NVIDIA 官方 X 称「Ollama 也限时免费提供该模型」，"
        "而 Vercel changelog 的平台清单里 `Ollama` 是以托管方身份出现、不带免费口径** —— "
        "**「同一模型在多个渠道同时限免」这期只核到 Vercel 一家给出了免费口径，Ollama 侧本期未核到**"
        "（避坑 161 / 161 同族）"
    ),
    (
        "OpenCode 把 Reflection Beam 也免费",
        "038",
        "额度",
        "**OpenCode 于 10/16–10/17 在 X 宣布把 `Reflection Beam` 与 `GLM-5.3-Flash` 一并免费"
        "（`aicoder.com` 收 OpenCode 官方 X 帖）**：**Beam 为 501B/23B MoE、上下文 1M token、"
        "官方口径 `Terminal-Bench 2.1` 80.1%**。"
        "**⚠️ 037 期登记的「OpenCode 只免了 `GLM-5.3-Flash`」在本期被扩为两个模型** —— "
        "**这是同一平台、同一天、第二次扩免免模型的样本（037 期刚记过「两天内同一平台把两个模型都免费了」）**，"
        "**至此三天内三次**（10/15 `DeepSeek V4.1 Flash` / 10/16 `GLM-5.3-Flash` / 10/16–17 `Beam`）—— "
        "⚠️ **本报告仍只记三例，不据此断言为规律**（避坑 68：**两例不足归纳、三例也只是提示**）。"
        "**⚠️ 与 `GLM-5.3-Flash` 免费档的四条限制必须分开写**（037 期已记：**仅平台内 / 上下文 200K "
        "而非 1M / 拒 PDF / 速度慢且不稳定**）：**本条 Beam 免费档官方未给出对应限制清单，"
        "也未公布免费结束日期** —— **两者同为「限时免费」，可核字段却差一整组**（避坑 154 / 163）。"
        "⚠️ **传播数字与产品事实要分开**：**该条附「X 上超 192 万浏览、1.75 万点赞」是宣传数据，不是产品指标**"
        "（避坑 116）。⚠️ **一个值得记的时序细节**：**`Beam` 在 OpenCode 上的代号正是 `stealth/cat-jam`，"
        "即开发者此前已在 OpenCode 里用过它 —— 「今天宣布免费」与「此前已是隐身免费条目」是两件事**"
        "（避坑 117 / 142）。⚠️ **`OpenCode` 是否把 `Beam` 计入套餐额度、是否会改变限速，本期未核到**"
    ),
    (
        "商务部 / 科技部 AI 技术出口管制目录修订",
        "038",
        "政策",
        "**商务部、科技部于 2026-10-16 发布 2026 年第 48 号公告，就修订《中国禁止出口限制出口技术目录》"
        "公开征求意见，并同步对相关技术实施出口前登记管理**"
        "（`mofcom.gov.cn` 公告与答记者问原文、商务部安全与管制局、证券时报电子报 10/17、"
        "中国经济网、央广网、中证网、中新网、Global Times 多源；**本期头条政策线**）。"
        "**范围（三领域共 40 项）**：**人工智能 23 项（大模型、智能体、算力集群、信息处理）、"
        "生物医药 5 项（细胞与基因治疗、小核酸药、病原微生物）、光伏 12 项（多晶硅、硅片、电池制造）**；"
        "**其中拟禁止出口 14 项、拟限制出口 26 项**。"
        "**⚠️ 两个日期必须分开记**：**征求意见 10/16–11/15**（意见反馈邮箱 `jinxianmulu@mofcom.gov.cn`、"
        "传真 010-65197565、信函北京市东长安街 2 号商务部安全与管制局）；"
        "**出口前登记自 10/16 公告发布之日起即启动，直到目录正式修订并实施之日止 —— "
        "已经开始但尚未完成的出口也在登记范围内**。"
        "**⚠️ 四类需登记的出口情形**：**① 向境外转让技术所有权（如知识产权转让）；② 境内技术授权境外使用"
        "（如知识产权授权使用）；③ 境内技术的所有权人或实际控制人变更为境外主体；④ 商务部以通知等形式"
        "明确要求登记的其他情形**。"
        "**⚠️ 本条对本报告最要紧的是四条豁免（全部抄下，这四条决定「哪些开源模型还能正常出海」）：**"
        "**① 已通过开源、发表学术论文等方式进入公共领域的技术，不纳入出口管理范围**；"
        "**② 人工智能类技术开源、中国企业在境外自建自营算力中心、赴境外开展芯片流片制造、利用境外资源"
        "开展联合研发、参与国际标准制定 —— 适用自动许可等便利措施，基本实现「即报即出」**；"
        "**③ 利用限制类大模型对外提供 API 调用、APP / 网页交互、SaaS 应用、本地端侧轻量化部署 —— "
        "不属于大模型技术出口管理范围**；**④ 纳入限制类的技术若开展海外本地化部署，属于技术出口管理范围；"
        "但部署在海外自有云等风险相对可控的情形下，可适用自动许可等便利措施**。"
        "**⚠️ 一条不能漏的时间线判断**：**今天是征求意见期 + 登记已启动 —— "
        "「目录正式修订并实施之日」未给日期，所以本条目前是「登记义务已生效、管制范围尚未落地」的状态**，"
        "**不得写成「AI 技术出口已被管制」**（避坑 154 同族：**生效日与截止日是两件事**）。"
        "**⚠️ 央广网专家解读里有一句是本报告要引的**：**「此次管控的焦点是底层技术，不是产品和服务」**、"
        "**「目录管理的对象是技术出口，不是简单意义上的服务出海或产品销售」**。"
        "**⚠️ 央广网另提到一条与本报告直接相关的动机表述**：**「信息对抗、网络攻防类技术参照 "
        "`Claude Mythos` 暴露的安全风险，从严管控」** —— **即官方解读把某具体闭源模型列为参照，"
        "这类表述在中文报道里极易被简化成「某模型被点名」，引用时必须原文照录**。"
        "**背景口径**：**中方称此次修订「不针对任何特定国家、地区或实体」，"
        "并将依据《对外贸易法》第二十条与科技部共同调整，商务部、科技部将依法对《目录》管理范围实施动态调整、"
        "及时将不先进或落后技术移出**；**另称支持全球南方国家加强人工智能能力建设，"
        "对世界人工智能合作组织成员间的能力建设国际合作、技术共享和规则共建所需的技术出口提供更多便利**"
    ),
    (
        "Perplexity 开源 SPACE 沙箱",
        "038",
        "工具",
        "**Perplexity 于 10/15–10/16 开源 `SPACE`（Sandboxed Platform for Agentic Code Execution），"
        "即 `Perplexity Computer` 每个任务背后的沙箱平台，Rust 编写、release 0.8.0、Apache 2.0、"
        "在 GitHub `perplexityai/SPACE`**"
        "（`perplexity.ai/hub/blog` 官方博客、Semafor（Reed Albergotti，10/15）、"
        "`github.com/perplexityai/SPACE`、MarkTechPost（10/17）、TSNMedia、webainews、"
        "`interestana`、`aidailypost`、mezha 多源）。"
        "**⚠️ 本条与「免费内容」线的连接点**：**它开源的不是模型而是「让 agent 能安全跑代码」的那一层**，"
        "**而这一层此前是纯付费采购项** —— **Perplexity 自己是在 7 月从一家商业沙箱供应商切换到自研的**。"
        "**机制**：**每个 agent 任务分配一个独立的 Firecracker microVM（自带 guest kernel）；"
        "凭证注入与出网策略在 VM 边界之外执行 —— secrets 永不进入 guest VM，"
        "凭证在网络层注入并带分层作用域、限速与审计日志**。"
        "**⚠️ 性能与安全数字全部是厂商自报（避坑 116）**：**中位创建延迟从 185 ms 降到 60 ms、"
        "p90 从 447 ms 降到 89 ms（官方称比原商业供应商快 3–5 倍）；每日处理「数百万次沙箱创建」、"
        "Computer 全部会话 100% 跑在 SPACE 上**；**逃逸测试：9 个前沿模型、108 次尝试、0 次成功逃逸**"
        "（⚠️ **另一处独立转述给出「118 次尝试 0 成功」，两个数并存、都写、都带来源，不取其一**）；"
        "⚠️ **但同一批测试里「修复前 54 次部分网络运行中有 11 次绕过出网策略」—— "
        "「VM 逃逸 0 次」与「出网策略曾被绕过 11 次」是两件事，不能只写前者**（避坑 132 同族）。"
        "**运行门槛（选型必读）**：**Linux x86_64 宿主机 + KVM（`/dev/kvm`）+ btrfs + Docker，"
        "本地 Kind（Kubernetes）或直连模式；⚠️ 不支持 macOS**；HTTP API + server-sent events；"
        "四态生命周期 running / paused / suspended / deleted，**默认空闲 6 小时自动挂起**，"
        "K8s 部署用 warm pools、单节点用 base snapshot 加速创建。"
        "**⚠️ 分发形态值得记**：**CoreWeave、Akamai、Crusoe 三家承诺把 SPACE 提供给其客户**"
        "（Akamai 已在其云上测试并上线、CoreWeave 已发布 CKS 评估部署指南、Crusoe 正在纳入其托管 AI 服务）—— "
        "**即「多数企业会消费托管版、不会自己运维 Firecracker 集群」**，"
        "**而托管版的定价至今未公布**（避坑 41 第一层：**能下载 ≠ 你会运营**）。"
        "⚠️ **本期未核到**：**开源版与 Computer 生产配置在默认网络 / 凭证策略上是否一致**（厂商博客未明说），"
        "**以及第三方对这个开源构建的独立逃逸测试结果** —— **两项均登记为待澄清**"
    ),
    (
        "Liquid AI d1-ultra 决策模型",
        "038",
        "发布",
        "**Liquid AI 于 10/16（周二）发布多模态决策模型 `d1-ultra`，官方称在 Artificial Analysis "
        "Decision Index v1.0 得 65 分、排名第一**（Liquid 官方、MarkTechPost（10/16）、"
        "`theblockbeats.info`（BlockBeats，10/17）、`syncai.news`、`aidailypost`、`interestana` 多源）。"
        "**机制**：**读文本、图像或两者，对每个问题返回各候选答案的概率，一次前向、输出 token 恒为 0**；"
        "**三种题型 Noul（是/否，返回 0–1 概率）/ Choice（集合内单选 + 各标签概率）/ "
        "Score（有序评分表上的概率加权位置）**。"
        "**⚠️ 榜首与它的反差必须一起写（这是本期最有信息量的一组对照）**："
        "**`AA-Omniscience` 500 道知识题只答对约 32%，低于上一代 `d1` 的 41%** —— "
        "**但「答不对时选择『不知道』的比例从 2% 提高到 85%**；"
        "⚠️ **Artificial Analysis 给「知识正确率」与「避免错误作答」各 12.5% 权重，"
        "其余成绩来自复杂推理、工具调用判断与安全分类** —— "
        "**即这个榜首是「知道自己不知道」换来的，不是「知道得更多」**（避坑 165 同族的新形态："
        "**同一个榜首可以由完全不同的能力构成**）。"
        "**⚠️ 对照口径（10/13 AA 发榜时的排序）**：**Jev 1.13 第一 58 分、`GLiDE` 与 `Microsoft-Decision-1` "
        "各 54 分**；本期变为 `d1-ultra` 65 分、`Jev 1.14` 57 分 —— "
        "**`Jev` 的版本号从 1.13 变成 1.14、分数从 58 变成 57，两次不可直接比**（避坑 141：**双分数必须记取的是哪个分**）。"
        "**定价**：**Liquid API 每百万输入 token $0.042（为 `d1` 的 2.1 倍），输出不收费**；"
        "**图像按 32×32 像素块折算 1.5 token/块 → 1024×1024 图像计 1,536 token**；"
        "⚠️ **同一张图回答多个问题会重复计费（每个问题都作为独立 prompt 计费，含全部图像）** —— "
        "**这是「按输入计费」这一形态里最容易被忽略的一条计费规则**（避坑 154 同族）。"
        "**容量限制**：**单请求最多 8 张图、10,000 个图像块、JSON 体不超过 4.5 MB**；上下文 32,768 token；"
        "**支持 44 种语言**。**⚠️ 开放程度**：**参数量与上下文均未披露、仅托管 API（Liquid API 已上线，"
        "Vercel AI Gateway 与 OpenRouter「即将支持」）—— ⚠️ 官方称它建立在「比 `d1` 更大的开放权重底座」上，"
        "**但底座是哪一个、权重能否下载，官方都没说**（避坑 41 / 162：**「基于开放权重底座」≠「权重开放」**）。"
        "⚠️ **厂商自报**：Liquid 自陈 112 项评测中八类任务全部领先 `Jev 1.14`，"
        "以及「自己测试中校准误差最低」—— **均为厂商口径、无独立复现**（避坑 116）"
    ),
    (
        "中国电信 Xing4.0 进 OpenRouter 免费档",
        "038",
        "额度",
        "**`OpenRouter` 的 `:free` 列表本期新增 `xingchen-agi/xing4.0-29b-a4b:free`（262K 上下文），"
        "厂商标注为 XingChen / China Telecom**（`freellm.net` OpenRouter 专页 `Last Updated 2026-10-17` 实跑，"
        "该页逐条给出 Model ID / 开发者 / 上下文 / 可用性 / 用途标签；`myaiguide.co` 10/16 日报同源印证"
        "「free on OpenRouter with a 262K context window」）。"
        "**⚠️ 本条必须与 012 期那条 `Xing4.0` 开放权重行区分开**：**权重自 2026-09-16 起就在 HF "
        "`XingChen-AGI` 组织页可下载（Apache-2.0），本期变化的是「出现了免费可调入口」** —— "
        "**「权重公开」与「免费可调用」之间隔了整整一个月**（避坑 142）。"
        "**⚠️ 官方可得字段（供选型对照）**：**29B 总参 / 每 token 约 4B 激活的稀疏 MoE、"
        "40 层、hidden 3,584、64 路由专家选 4 + 1 常开共享专家、`MLA` 压缩 KV 注意力、"
        "`MTP` 多 token 预测内训、原生 256K 可扩到 512K**；"
        "**Apache-2.0、bfloat16 safetensors / FP8 / w8a8 / GGUF 四种构建**；"
        "**⚠️ 一个真实的部署门槛：`mHC`（manifold-constrained hyper-connection）四路 hyper-connection "
        "结构需要框架自定义内核，SGLang 为其专门发了 split-K 内核**。"
        "⚠️ **基准全是厂商模型卡自报、无独立复现**：`SWE-bench Verified` 75.00（210K 上下文、"
        "SWE-agent harness）、`Terminal-Bench 2.1` 57.50（terminus-2、64K、24 小时超时、三次平均）、"
        "`SWE-bench Multilingual` 66.00、`Claw-Eval` 76.55（避坑 116）。"
        "**⚠️ 一条值得记的沿革（避坑 117 同族）**：**泄露期流传过 `XingChen4` → `Xing4_0` 的改名，"
        "且该模型的早期代号就是 `stealth/cat-jam` 与 `stealth/missingno` 的对照物之一 —— "
        "**代号不能当身份**。⚠️ **`OpenRouter` 免费档的额度口径要按原站读**："
        "**50 次/日（累计充值满 $10 后 1,000 次/日）、20 次/分；负余额返回 402 且免费模型同样受限**"
        "（避坑 155 **本期特别提醒**：`freellm.net` 该页写的是「200 req/day」，"
        "**与 `OpenRouter` 官方与 `freetokens.fyi` 记的「50 次/日（充值后 1,000）」不一致** —— "
        "**三个来源三个数，两个口径都要写、都带来源、不取中间值**）"
    ),
    (
        "Replit 宣称不再与 Anthropic 合作",
        "038",
        "发布",
        "**Replit 联合创始人兼 CEO Amjad Masad 于 10/16 在 TechCrunch Disrupt 台上称 Replit 已不再与 Anthropic 合作，"
        "理由是成本、合作与性能**（TechCrunch 报道，记者 Lucas Ropek；`el-fondo.com`、`lumienai.com`、"
        "`aidailypost`、`explainx.ai`、`chainmind.com.ng` 多源转述；`myaiguide.co` 日报同源）。"
        "**⚠️ 本条的全部信息量在「口径互斥」，不在「合作结束」—— 它是本报告第一个"
        "「企业高管台上表态 vs 公司自有文档」直接冲突的样本**：**"
        "**Masad 称 Replit 内部与公开基准显示 OpenAI 的 `Sol` 与 `Astra` 在「从零构建 vibe-coded 应用」上更好，"
        "并说「I think ChatGPT is better now」**；"
        "**但 TechCrunch 同时报道「一位知情人士称该合作仍在进行」**，"
        "**且有公开文档佐证：Replit 9 月底的博客把 `Claude Fable 5` 与 `Claude Fable 5.1` 列为 "
        "`Replit Agent` 生产环境在用的模型，同期一名 Replit 产品员工在 X 上推广 `Opus 5.5`**；"
        "**TechCrunch 已回访 Replit 要求澄清，截至本期未见澄清声明**。"
        "**⚠️ 因此本条的登记口径是「有一方这样说过、另一方这样说过、尚无第三方裁定」，"
        "不对「合作是否已终止」下结论**（避坑 132：**互斥口径必须并列，不取其一**）。"
        "**旁证（同场给出的经营数字，与本报告主线关系较弱但可记）**："
        "**企业合同占总收入从 2025 年约 2% 升至 2026 年约 15%、B2B 已超总收入 50%**。"
        "**背景**：Replit 于 2026 年 8 月 18 日发布《Replit Introduces Free Mode to Expand What is Possible "
        "with AI》并宣布与 OpenAI 合作（副标题即「With OpenAI, Replit now helps you accomplish even more, "
        "every day」），8 月 26 日又发布《Intelligent Model Routing on Replit》"
        "—— ⚠️ **三个月内先接 OpenAI、再由 CEO 台上宣布弃 Anthropic，而 Replit 自己的产品形态是"
        "「按任务自动选最优模型」，所以「用谁的模型」本来就不是一个稳定承诺**（避坑 117 同族）。"
        "**⚠️ 对本报告读者的实际含义**：**「平台与某模型厂商的合作」与「平台当前给你什么模型」是两个问题**，"
        "**选型时应按后者核、按前者盯**（避坑 68 的变体）"
    ),
]

frozen = io.open(FROZEN, encoding="utf-8", newline="").read()
n_before = len([l for l in frozen.split("\n") if l.startswith("| ") and "---" not in l and not l.startswith("| 关键词")])

# ---- 改写：逐条断言唯一命中 + 行尾必须是「| 演进中 |」 ----
rw = 0
for key, extra in REWRITE.items():
    assert frozen.count(key) == 1, ("改写锚点不唯一", key, frozen.count(key))
    i = frozen.index(key)
    end = frozen.index("\n", i)
    line = frozen[i:end]
    assert line.rstrip().endswith("| 演进中 |"), ("改写行尾不是「演进中」", key, line[-40:])
    frozen = frozen[:i] + line + extra + frozen[end:]
    rw += 1
    print("改写：%s" % key.strip("| "))

# ---- 首登：追加在文件末尾 ----
for name, issue, cat, body in NEW_ROWS:
    row = "| %s | %s | %s | %s | 演进中 |" % (name, issue, cat, body)
    frozen = frozen.rstrip("\n") + "\n" + row
    print("首登：%s" % name)

io.open(FROZEN, "w", encoding="utf-8", newline="\r\n").write(frozen)

frozen2 = io.open(FROZEN, encoding="utf-8", newline="").read()
n_after = len([l for l in frozen2.split("\n") if l.startswith("| ") and "---" not in l and not l.startswith("| 关键词")])
crlf = frozen2.count("\r\n")
print("\nfrozen_items：%d -> %d（首登 +%d / 改写 %d）；CRLF 行数 = %d，应等于总行数 %d（末行无换行，故少 1 属正常） -> %s"
      % (n_before, n_after, n_after - n_before, rw, crlf,
         len(frozen2.rstrip("\n").split("\n")),
         "OK" if crlf == len(frozen2.rstrip("\n").split("\n")) else "EOL MIXED"))

# ================= open_questions =================
oq = io.open(OQ, encoding="utf-8", newline="").read()
oq_lines = oq.split("\n")

# Q26（Mistral 三源互斥）补 038 期进展
# ⚠️ 该库的行尾是 `… |`（竖线前无空格），与 frozen_items 的 `| 演进中 |` 不同 —— 两库行尾格式不一样，别混用
n_q26 = 0
for i, l in enumerate(oq_lines):
    if l.startswith("| Q26 "):
        assert l.rstrip().endswith("|"), ("Q26 行尾不是竖线", repr(l[-20:]))
        oq_lines[i] = l.rstrip() + "**⚠️ 038 期进展：本期未再核到第四个来源，Q26 挂账第 3 期；" \
            "同域另有一条新的互斥样本 —— `freellm.net` 记 OpenRouter 免费档「200 req/day」、" \
            "而 `OpenRouter` 官方与 `freetokens.fyi` 记「50 次/日（累计充值满 $10 后 1,000 次/日）」，" \
            "**两个口径都要带来源读、不可取中间值（避坑 161）** |"
        n_q26 += 1
        break
assert n_q26 == 1, ("Q26 行未唯一命中", n_q26)
print("open_questions：Q26 补 038 期进展")

oq = "\n".join(oq_lines)

# 新增 Q27 / Q28（**格式必须与既有行一致：`| QNN | 标题 | 内容 |`，行尾竖线前无空格**）
NEW_OQ = [
    "| Q27 | **商务部 48 号公告的三个未定项（目录生效日 / 23 项技术指标线 / 适用主体）** | "
    "**商务部 / 科技部 2026 年第 48 号公告（AI 技术出口管制目录修订）的三个未定项**："
    "**① 目录「正式修订并实施之日」未定 —— 在此之前只有「出口前登记」义务生效、管制范围尚未落地，"
    "本期不得写成「AI 技术出口已被管制」；② 23 项 AI 技术的具体指标（哪些算「算力集群」、"
    "FLOPs / 参数量的门槛线）只在附件里，商务部正文未列 —— "
    "**第三方报道提到「10^26 FLOPs 或 2 万亿参数」这一门槛，但该数字未在商务部 / 央广网 / 中新网的正文里核到，"
    "属未确认口径**；③ 「技术出口经营者」是否覆盖开源项目的个人贡献者、以模型权重本体对外发布算不算"
    "「转让技术所有权」，公告未给出示例。"
    "**为什么挂账**：这三条每一条都会改变「某个开源模型还能不能正常给海外用户用」的判断，"
    "而目前只能确定「公开领域的技术不纳入」这一条豁免。**回扫节点：征求意见截止 11/15 之后，"
    "以及正式修订公告发布当日** |",
    "| Q28 | **Perplexity 开源 `SPACE` 的两个未定项（开源版与生产配置是否一致 / 有无第三方独立逃逸测试）** | "
    "**Perplexity 开源 `SPACE` 的两个未定项**："
    "**① 开源版与 `Perplexity Computer` 生产配置在默认网络出口策略与凭证策略上是否一致 —— 官方博客未明说**；"
    "**② 是否有第三方对这个开源构建做独立逃逸测试 —— 目前「108 次尝试 0 成功」与「118 次尝试 0 成功」"
    "两个数并存，且都出自厂商口径**。"
    "**为什么挂账**：**「逃逸 0 次」与「出网策略曾被绕过 11 次」是同一批测试里的两件事**，"
    "只引用前者会给出错误的安全感（避坑 132 同族）。"
    "另附一条同族待澄清：`CoreWeave` / `Akamai` / `Crusoe` 三家托管版 SPACE 的定价至今未公布，"
    "即「多数企业会消费托管版、不会自建」，而托管版价格是空的（避坑 41 第一层）。"
    "**回扫节点：三家发布正式 GA SKU 或定价页时** |",
]
oq = oq.rstrip("\n") + "\n" + "\n".join(NEW_OQ)
io.open(OQ, "w", encoding="utf-8", newline="\r\n").write(oq)

oq2 = io.open(OQ, encoding="utf-8", newline="").read()
nq = len([l for l in oq2.split("\n") if l.startswith("| Q")])
crlf2 = oq2.count("\r\n")
print("open_questions：现有 Q 条数 = %d；CRLF 行数 = %d -> %s"
      % (nq, crlf2, "OK" if crlf2 == len(oq2.rstrip("\n").split("\n")) else "EOL MIXED"))