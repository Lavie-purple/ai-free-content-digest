# -*- coding: utf-8 -*-
"""037 期台账更新：向 frozen_items.md 追加本期首登行与改写行；向 open_questions.md 更新 Q23/Q26。

纪律（035 期定）：**先写库、再跑 check_frozen** —— 它的「首登 / 未出现」判据字段就是本期才写入的内容。
data/ 下是 CRLF，用 newline="\\r\\n" 写回。
"""
import io, os

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(WS, ".workbuddy", "data")

# ---------------- frozen_items.md：本期首登 6 条 + 改写 4 条 ----------------
NEW = [
    # ===== 首登 =====
    "| Meta Muse Spark Open 开放权重 | 037 | 开源 | "
    "**Meta 于当地时间 2026-10-15（北京 10/15 傍晚至 10/16）发布 `Muse Spark Open` 权重，官方研究与开发者博客同日上线**（`research.meta.ai/blog/muse-spark-open`、`developer.meta.com` 开发者博客、HF `meta-models` 组织页、The New Stack（Frederic Lardinois，10/15 13:00）、VentureBeat、财联社 / 腾讯新闻 / 站长之家多源）。"
    "**官方标题即定调：「迄今能力最强的美国开放权重模型」（the most capable US open-weight model to date）**。"
    "**规格**：**原生多模态稀疏 MoE、总参 816B / 每 token 激活约 42B、上下文 1M token（1,048,576）、输入文本+图像+视频+音频 → 输出文本、每层 256 个专家每 token 路由 8 个、训练数据覆盖 100 多种语言**；**面向长程任务、复杂软件工程与多步推理**；"
    "**官方端侧实例：用 `Muse Code` 驱动 `Ice Cubes`（开源 Mastodon 客户端）的真实 iOS 改动（修 bug、加功能、完整构建），以及端到端驱动 DaVinci Resolve（逐帧审片、找高光、竖屏裁切）**。"
    "**权重四处可下**：**Hugging Face（`meta-models/Muse-Spark-Open-816B-A42B` 与 `-NVFP4`）、Amazon SageMaker AI、Google Cloud Model Garden、Microsoft Foundry Models**。"
    "⚠️ **下载闸门（本期最易被「开放权重」盖过去）**：**HF 上两个 Meta 仓库均为 gated 且人工审核 —— 访问表单要求「法定全名 + 出生日期 + 组织全称（含全部公司标识符）」、不得用缩写与特殊字符、提交后不可编辑，并警告不合规可能影响访问 HF 上其他模型；信息按 Meta 隐私政策（facebook.com 那套）收集、存储、处理与共享**；"
    "**同一段表单文案在 `Llama 4 Scout` / `Meta-SecAlign-8B` / `OMol25` 与 Meta 外的 `Tri-21B` 上也出现，但那些页面用 HF 默认勾选框、无自定义字段 —— 「要求出生日期」是本期第一次出现在 Meta 仓库上**。"
    "⚠️ **同一份权重的 ungated 镜像**：**Unsloth GGUF（21 档量化）、`ggml-org` GGUF（10/14 发布：`Q2_K` 304.080 GB / `Q4_K_S` 470.069 GB / `Q8_0` 871.648 GB / BF16 1,640.265 GB / mmproj 2.2–4.1 GB）、AMD Quark FP8 / MXFP4** —— **即「官方仓库要提交身份信息、镜像仓库一键下载」是同权重的两条路**（避坑 162）；⚠️ **`Q2_K` 是混合精度配方而非均匀 2-bit**（路由专家门与上投影 Q2_K、专家下投影 Q3_K、逐层潜投影与注意力输出门 Q8_0，用 Q8_0 构建的 imatrix 校准）。"
    "⚠️ **许可证 `Muse Model License`，不是 Apache-2.0**：**① 署名 —— 任何使用该模型或其衍生作品的产品或服务必须在界面 / 文档 / 网站 / 设置菜单中显著展示「Built with Muse Spark Open」；② 「衍生作品」定义极宽 —— 含任何用该软件或其任何输出 / 结果「训练、修改（含微调）、蒸馏或以其他方式改进」得到的模型（因此用 Muse 输出单独训练的小模型也算）；③ MaaS 收入闸门 —— 若把模型通过 API 或类似界面对外提供服务（Model as a Service）且你与关联方在任意连续 12 个月内总收入超 2,000 万美元，必须先通知 Meta 并另签书面协议（收入口径是「你与关联方的合计总收入」、不是「来自该模型的收入」；豁免内部使用、研究、MaaS 之外的商业活动、以及把模型作为自己产品组件且该产品本身不是 MaaS）；④ 使用政策是许可证的一部分（不面向 18 岁以下、禁军事用途与武器、禁运行关键基础设施（交通技术 / 重型机械）、禁蓄意规避安全措施、禁恶意软件与冒充）；Meta 声明不主张输出所有权**（避坑 158）。"
    "⚠️ **跑起来要什么**：**官方模型卡口径 NVFP4 约需 700 GB GPU 显存、BF16 约需 2 TB**；**BF16 仓库按 HF blobs 求和 1,644.366 GB / 65 分片（HF 帖称约 1.5 TB、Apple 称原生 BF16 需 >1.6 TB）、NVFP4 仓库 533.043 GB / 127 分片（Apple 称约 493 GB 且明确「加上中间计算所需内存装不进单机」）**；"
    "**Apple 路线为官方主推而非补充：M5 Ultra 集成 GPU 每台可用 512 GB 统一内存、两台机器即可容纳全量模型、芯片 1.2 TB/s 内存带宽、两台「表现得像一台拥有 TB 级统一内存的超级计算机」，官方称之为「同类首个能在桌面端跑起来的模型」**；**Hugging Face 实测 3-bit 版在 512 GB 的 M3 Ultra 上约需 344 GB 内存、约 21 tokens/s**；⚠️ **256 GB 及以下不可行，官方 Apple 方案用的是 NVFP4（4-bit 浮点）而不是 2-bit GGUF**。"
    "⚠️ **「最强」是限定词，不是排名**：**官方表内 `MCP-Atlas` 89.2 领先 `Qwen3.8-2.4T-A95B` 84.5 与 `Kimi K3` 82.3、`HLE-Diamond`（无工具）26.1 vs 22.2 / 16.4，但 `Terminal-Bench 2.1` 76.4 落后 `Kimi K3` 85.0 与 `GLM 5.3` 83.9、`DeepSWE 1.1` 60 vs 68，`Artificial Analysis` Intelligence Index 39（xhigh）落后 `GLM-5.3` 44 与 `Kimi K3` 45**；**对比对象为 Thinking Machines `Inkling` 与 NVIDIA `Nemotron 3 Ultra`，Meta 称跨项领先、常达 20 分以上**；⚠️ **基准全部为厂商自披露，官方称完整评测报告即将发布（`StrongREJECT v2` 为 0.5，越低越好；按其 `Meta Superintelligence Scaling Framework` 评估达到发布门槛）**（避坑 116 / 165）。"
    "**推理栈**：**SGLang（BF16 + NVFP4 + DFlash2 投机解码）/ vLLM（BF16 / NVFP4 / MXFP4，NVIDIA 与 AMD 双平台验证，DSpark 投机解码）/ TensorRT-LLM / Hugging Face Transformers / Apple MLX / llama.cpp / Unsloth**，在 NVIDIA / AMD / Intel / Apple 硅上验证；**训练侧 TorchTitan / SGLang + Miles / NVIDIA NeMo AutoModel / Hugging Face TRL**；**Helion GPU 内核在 SGLang 上带来 1.03–3.95× 内核级加速、AMD MI350 上 3% 端到端加速**。"
    "**托管**：**`Baseten`、`Fireworks AI`、`Groq`、`Modal`、`Nebius`、`OpenRouter`、`Together AI` 七家 day-one**；⚠️ **各宿主上下文上限不一致：Meta 部署文档写 GroqCloud 上限 131,072 token、Fireworks 为 1,048,576，且 Groq access requires approval for an organization**（避坑 159 同族）；**Together AI 常规价 $1.25 输入 / $4.25 输出 / $0.15 缓存**。"
    "⚠️ **与 `Muse Glimmer` 的对照（Q19 议题的延续）**：**`Muse Glimmer` 是 2026 年 8 月发布、Apache-2.0、30B（2B 视觉编码器 + 28B 文本解码器）、4-bit 量化后 <20 GB、131,072 上下文、可从 `Muse Spark` 蒸馏而来** —— **同一个模型家族的两个成员，发布日、参数量、上下文、许可证四项全不同**（避坑 142）；⚠️ **`Muse Spark 1.3` 是闭源模型、在 Meta Model API 上服务、`Artificial Analysis` 最高 effort 得分 48，与 `Muse Spark Open` 不是同一个模型**（两者均标价 $1.25 / $4.25）；"
    "⚠️ **本期把它登记为独立条目、与冻结库中 `Muse Glimmer` 的 Q19 行并列（不合并、不覆盖）** | 演进中 |",

    "| OpenCode GLM-5.3-Flash 免费档 | 037 | 额度 | "
    "**OpenCode 于 2026-10-16 在 X 宣布「GLM 5.3 Flash is now free in OpenCode」，模型 ID 为 `opencode/glm-5.3-flash-free`（OpenCode Zen 文档亦记 `glm-5.3-flash-free`）**（OpenCode 官方 X 帖、`Apidog` 博客（作者 Ashley Innocent，10/16 当日实测）、`freetokens.custats.info`（Last checked Oct 16, 2026））。"
    "**官方文档口径：「is free on OpenCode for a limited time」，并说明其 provider 遵循零留存策略、不用你的数据做模型训练**；**OpenCode Inference API 文档写明「付费模型需要 Authorization 头、免费聊天模型可不带」，形成账号可选的直连路径**。"
    "**四条限制（第三方当日实测）**：**① 只能在 OpenCode 内用、不是通用 API；② 上下文封顶 200K token，而非原生 1M；③ 拒绝 PDF 附件，尽管模型元数据里列出了 PDF；④ 回答慢且不稳定**。"
    "**正面结论**：**当日以全新安装、无登录、无 API Key 的方式实测成功调用**；**`Apidog` 另给实操细节：必须执行 `opencode models --refresh` 才能看到该模型，刷新后列出 11 个免费模型**。"
    "**四条对照必须一起写（避坑 163）**：**OpenCode `glm-5.3-flash-free` $0（限时）/ 200K 上下文 / 32K 最大输出 / 仅 OpenCode 内；OpenCode Zen `glm-5.3-flash`（付费）$0.15 输入 $0.50 输出 / 1M / 131K / 任何持 Zen key 的客户端；OpenCode Zen `glm-5.3`（非 Flash）$1.40 输入 $4.40 输出 / 1M / 131K；Z.ai 官方 API `glm-5.3-flash` $0.15 输入 $0.50 输出 / 缓存 $0.03 / 1M / 任何客户端**。"
    "⚠️ **「`GLM-5.3` 免费」是错误说法，免费的只是 Flash 档**。"
    "**模型本身（付费档口径）**：`GLM-5.3-Flash` 于 2026-08-26 发布，**320B 总参 / 18B 激活的 MoE、MIT 许可权重、原生图像输入**。"
    "**沿革（判断会不会收回去的唯一依据）**：**这是同一模型第二次被 OpenCode 免费 —— 8/20 起一个名为 `Ox Alpha` 的匿名模型出现在 OpenCode 与 OpenRouter 的免费列表里（1M 上下文），8/26 Z.ai 揭示它就是 `GLM-5.3-Flash`；这次改用本名 + 200K 窗口** —— **两次免费的窗口不同，不要当成同一轮活动**（避坑 117 同族）。"
    "⚠️ **与 10/15 的 `DeepSeek V4.1 Flash` 免费（同样 200K、仅平台内、不计套餐额度）是两笔账**（036 期登记）：**两天内同一平台把两个模型都免费了、两个的免费档上下文都是 200K —— ⚠️ 两例归纳不足以断言为规律，只记两例**（避坑 68）；**两款结束日均未公布**。"
    "⚠️ **`Apidog` 与 `freetokens` 在「是否需要账号」上口径略有差异**（前者称免登录免 key 实测成功、后者称直连路径账号可选但 Console 配置另需账单信息）—— **两个口径都写，不合并成「完全无需账号」**（避坑 161） | 演进中 |",

    "| 腾讯元器 11/9 停服 | 037 | 政策 | "
    "**腾讯智能体平台「元器」公告将于 2026 年 11 月 9 日停止服务**（南方都市报（南都 N 视频记者林文琪）、澎湃新闻、腾讯网（10/15 14:26，转南方都市报）、凤凰网多源）。"
    "**公告原文口径**：**妥善处理产品下架涉及的数据导出、替代产品及退费等事宜；停服生效后，所创建智能体将不再可用**。"
    "**四个日期必须分开写（本条的全部信息量）**：**① 10/29 起不再支持新建智能体、不再支持分发 API Key；② 11/9 平台停止全部服务（访问、数据读写、API 调用、后台控制台全部关闭）；③ 发布到公众号、微信客服等渠道的智能体也停止响应用户对话；④ 数据导出窗口开到 2027-01-09（导出智能体配置 / 工作流 / 对话记录）** —— ⚠️ **最后导出日比停服日晚两个月，是最容易漏掉的一个日期**（避坑 164）。"
    "**迁移方案**：**官方推荐迁往腾讯云智能体开发平台 `ADP`（2025 年 5 月上线，由腾讯云大模型知识引擎升级而来）** —— **官方称元器上的主要玩法均可延续，包括标准模式、Multi-Agent（多智能体协作）、单工作流三种应用模式，并支持更灵活的 `Claw` 模式**；**官方明确 `ADP` 更适合需要延续原有三种应用模式、使用工作流编排或自定义工具、以及希望在多个渠道同时对外提供服务的智能体**。"
    "**背景**：**元器发布于 2024 年 5 月**，在腾讯混元开启智能体生态的背景下上线，**定位一站式 AI 智能体创作与分发平台，支持用腾讯官方插件与知识库创建智能体并一键分发到 QQ、微信客服、腾讯云等渠道**。"
    "**定位差异（腾讯云副总裁、腾讯云智能负责人、腾讯优图实验室负责人吴运声此前受访口径）**：**元器偏 C 端、主要与「元宝」结合，面向个人用户或轻量开发者；`ADP` 面向 B 端企业级平台，强调系统性构建、数据接入、安全隔离、跨角色协作**。"
    "⚠️ **同期参照（同为腾讯自家产品线停服）**：**`QClaw` 已于 9/24 公告因业务发展调整，将于 2026 年 12 月 24 日 00:00 正式停止运营** —— ⚠️ **该条本期仅作背景参照，本报告未登记 `QClaw` 条目，下期应补**。"
    "⚠️ **量级判断**：**平台停服比任何额度到期都更该先排** —— **「优惠窗口结束」损失的是钱，「平台停服」损失的是存在本身**（避坑 164，与避坑 47「有预告的关停反而最容易拖」、避坑 78「无信号即默认收口」合并执行） | 演进中 |",

    "| Google AI Plus 11/13 失去 Pro 模型 | 037 | 额度 | "
    "**Google 已开始向 Gemini AI Plus 订阅者发送通知邮件，确认自 2026 年 11 月 13 日起调整模型访问权限**（CNMO 科技（10/15 10:22）、凤凰网科技、ITBear、网易（转 CNMO）、Android Central（作者 Sanuj Bhatia）多源）。"
    "**邮件内容**：**AI Plus 用户将无法在 Gemini 应用及 Google 搜索的 AI 模式中选择 Pro 模型，仅可使用 Flash-Lite 和 Flash 两款模型**。"
    "**四条边界**：**① 不是取消订阅而是降档可用 —— 此前使用 Pro 创建的对话不会被删除，但后续需切换至其他可用模型继续交流（即「历史可读、后续由较轻量引擎接管」）；② 继续用 Pro 只有两条路且月费涨约 4 倍 —— 升级到每月 19.99 美元的 Google AI Pro 或每月 99.99 美元的 AI Ultra，升级到 Pro 档的额外好处是使用额度从免费标准版的两倍提升至四倍；③ 免费档仍保留 —— 免费用户可继续使用 Flash-Lite，AI Plus 保留 Flash-Lite + Flash，其他订阅权益（Google Workspace 云存储、YouTube Premium 等）不受本次调整影响；④ `Gemini 4 Argon` 的归属一并确认 —— 该模型被纳入 AI Pro 和 AI Ultra，不再向 AI Plus 用户提供**。"
    "⚠️ **本期纠错要点（见五·1）**：**本条与「Google Gemini 免费档收缩（10/9 生效、针对个人未订阅账号）」不是同一件事 —— 10/9 针对「个人未订阅账号」（应用内只剩 Flash-Lite），11/13 针对「付费最低档 AI Plus」（失去 Pro、只剩 Flash-Lite + Flash）**。**两个日期、两个档位，勿合并**（避坑 142）。"
    "⚠️ **ITBear 的口径本身记录了这次日期差**：「Google 此前于 10 月更新 Gemini 支持文档，曾预计相关限制于 10/9 生效，此次邮件则明确了 11/13 这一新日期，但未说明调整原因」—— ⚠️ **当一个二级来源主动记录了日期不一致时，那不是它写错了，那是事实的一部分**。"
    "**Android Central 另给「AI Plus 随附 400GB 云存储」这一现有权益数字** | 演进中 |",

    "| 蚂蚁百灵 Ling-3.1-flash 开源 | 037 | 开源 | "
    "**蚂蚁集团百灵大模型于 10/15 宣布开源 `Ling-3.1-flash`，权重已在 Hugging Face 与 ModelScope 上线，采用 MIT 许可证**（AI 门户（caip.org.cn）、`chinaainews.org`、`writeble.com`、`tech360.tv`（转 Pandaily）、`allatra.media`、`toldrop.com`、OpenAI Hub、IT之家（9/30 首发报道）、智通财经（8/7 `Ling-3.0` 报道）、ToolNavs 转述百灵官方公众号、HF `inclusionAI/Ling-3.1-flash` 模型卡与 HF API 多源）。"
    "**规格**：**总参约 560B、每 token 激活约 25B、最高支持 1M 上下文**；**flash 系列首个达到五千亿参数级别的模型，总参数约为上一代的五倍**。"
    "**架构**：**混合线性 MoE：63 层 KDA（Kimi Delta Attention，线性注意力）+ 9 层门控 MLA，比例 7:1，另加 4 层稠密层**；**512 个路由专家 + 1 个共享专家，每 token 选 8 个**；**注意力 64 头、hidden size 4096、专家中间层 1280、稠密中间层 10240、词表 157,184**。"
    "⚠️ **量化与部署门槛（本期最有实用价值的一组）**：**路由专家采用 MXFP4 量化、稠密层保留 block-FP8，权重体积从约 534 GB 压缩至约 292 GB；Hopper GPU 环境下部署所需显卡由 8 卡降至 4 卡**；**另提供长上下文并行推理方案 PCP / DCP，并增强了 JSON Schema 支持（生产部署关键项）**；**Day-0 支持 SGLang（带投机解码专用镜像）与 vLLM，另附参考部署配置**；⚠️ **一份独立来源给出的推荐配置为 8 张 NVIDIA H200 或 4 张 GB300** —— **与「Hopper 由 8 卡降至 4 卡」不矛盾：前者是推荐配置、后者是 MXFP4 量化后的 Hopper 下限，两个都要写**。"
    "**权重状态**：**HF 仓库 `inclusionAI/Ling-3.1-flash` 创建于 10/13（11:16 UTC），10/15 正式宣布开源；`gated: false`（ungated）；文件为 FP8 量化，含 54 个分片 safetensors 加一个索引**。"
    "⚠️ **基准均为厂商自报（避坑 116）**：`GDPVal-AA V2.1` 办公任务 **ELO 1673**；`HealthBench Professional` **65.35**；**内部 Lua 原生编译器开发任务约 17 小时、独立测试通过率 97.8%**；**Artificial Analysis 智能指数 41、输出速度约每秒 210 token、混合调用价约每百万 token 0.19 美元**；**官方称在 `Claude Code` / `Kilo Code` / `Qwen Code` / `Hermes Agent` / `OpenClaw` 等 harness 中表现良好，无独立复现**。"
    "⚠️ **官方自陈局限**：**大量长文本一次性输入时可能失焦、一次性生成有适配边界；当前版本不具备原生视觉理解，需另配视觉模型**。"
    "**价格（限时 2.5 折，是价格不是免费）**：**OpenRouter 输入 $0.075 / 输出 $0.225 / 缓存读取 $0.015；Ling Studio 输入 ¥0.5 / 输出 ¥1.5 / 缓存读取 ¥0.1** —— ⚠️ **2.5 折的结束日本期未核到，按避坑 154 明确写「结束日未公布」、不预估**。"
    "⚠️ **它是服务器模型，不是「人人本地跑」的模型** —— **按量化后 292 GB 的权重体量，个人开发者不具备本地部署条件**（避坑 41 第三层）；**已接入蚂蚁集团内部桌面协作 Agent 客户端**。"
    "**沿革（本期最有价值的一条时间线，避坑 142 的完整样本）**：**9/30 `Ling-3.1-flash` 作为 API 模型首次出现在 Vercel AI Gateway，开放为期两周的免费体验（两个 ID：`inclusionai/ling-3.1-flash` 与 `inclusionai/ling-3.1-flash-free`），该试用窗口的上下文为 262K**；**当时官方表示：免费体验结束、转为付费服务后，计划开放 1M 上下文，并同步开源** —— ⚠️ **这个承诺已兑现：免费网关窗口与权重落地几乎同日（10/13），而 1M 上下文随权重一同开放** —— **这是一个「预告 → 兑现」的正样本，与 035–036 期 `Step 5 Preview` 的许可证挂账形成对照**（避坑 158：写「未公布」必须同时写「承诺日尚未到」）。"
    "**同系列参照**：`Ling-3.0-flash` 124B / 5.1B 激活（8 月开源，MXFP4 与 INT4 版可在单台 NVIDIA DGX Spark 上完成端到端推理）；`Ling-3.0-flash-Fin`、`Ling-3.0-flash-Sante`；`Ming-Image-0.1-Design`（012 期登记，MIT）；**另引入 `LingCode`（基于开源 coding agent `Pi` 扩展的 harness，面向数小时、含数百次工具轮次、需反复上下文压缩的长程编码任务，官方称未来考虑开源 —— ⚠️ 本期未开源）**。"
    "⚠️ **「价格约为 `Ling-3.0-flash` 的 3.6 倍」出自第三方分析推算**（理由是 3.1 每 token 激活 25B 而 3.0 只激活 5.1B），非厂商口径。"
    "⚠️ **同期对照（避坑 158）**：**本期同日 Meta 的 `Muse Spark Open` 用 `Muse Model License`（署名 + $20M MaaS 另签 + 使用政策），而本条是 MIT（零义务）** —— **「开源」这个词把两者写成同一件事，读者要做的合规动作完全相反** | 演进中 |",

    "| PilotDeck 2.0 开源 | 037 | 工具 | "
    "**清华 THUNLP、面壁智能（MiniCPM）、OpenBMB 与 AI9Stars 于 10/14–10/15 联合开源 Agent 工作台 `PilotDeck 2.0`**（腾讯研究院 AI 速递 20261016、波动智能 10 月 16 日早报、`theaiadventurer.com` 读码实测多源）。"
    "**官方定位**：**模型无关的「Agent 操作系统」，把自然语言指令转成成品任务，数据流可见、模型可选**。"
    "**四个 2.0 头条项**：**① Word / Excel / PowerPoint 文件可创建、编辑并校验，不只是起草；② 长任务可抗中断，官方称以 2,000 条交互消息做过压力测试；③ 一键桌面应用安装；④ `WorkBuddyBench` 得分**。"
    "⚠️ **四条「公告 vs 读码」对照（本条最典型的样本）**：**① 许可证 AGPL-3.0（copyleft，与 MIT 是两类完全不同的义务 —— AGPL 的触发点包含「通过网络提供服务」，是选型时最易踩的一条）；② 第三方读码确认 Office 三技能功能真实存在（`skills/docx` / `skills/spreadsheets` / `skills/pptx`，用 `python-docx` / `exceljs` / `jszip` + validate / render / compare / deliver 命令），但文件日期为 7/15、最后改动 8/24；③ 仓库没有 2.0 tag，最新 release 为桌面安装包 `v2026.10.13-r2`；④ 基准与 2,000 条消息压测均未独立复现**。"
    "**其余可核字段**：**仓库 `OpenBMB/PilotDeck`，AGPL-3.0，以 TypeScript 为主，约 4,050 Star**；**提供 macOS（arm64 / x64）、Windows（x64 / arm64）、Linux（deb / rpm，双架构）桌面安装包，macOS arm64 的 dmg 约 218 MB**；**另有需 Node.js ≥22.13 且 <23 的一行 shell 安装器与 `docker compose up -d --build` 路径**；**网站 `pilotdeck.openbmb.cn`**；**provider 目录含 12 家 provider、57 个模型**。"
    "**四个设计支柱**：**① 按项目隔离的「WorkSpace」（每个项目有自己的文件、记忆与技能，表格任务与播客任务不共享上下文）；② 可逐条查看与编辑的记忆；③ 智能路由（难调用强模型、易调用便宜模型）；④ 常驻模式（离开后继续工作）**。"
    "⚠️ **基准两个数并存（避坑 161）**：**腾讯研究院与波动智能口径为「换用 35B-A3B 轻量底座后 79.4 分居三者之首」、`theaiadventurer` 口径为「79.1，`WorkBuddy` 74.7、`Claude Code` 77.3」** —— **两个数都写、都带来源、不取中间值；⚠️ 注意口径差异所在：「79.4」是换底座后的数、「79.1」是该来源记录的默认配置数，两者不是同一配置**。"
    "**官方自报的路由数字（未复跑）**：**`Sonnet 4.6` 主 + `MiniMax-M2.7` 子 = 70.6 分 @ $3.15，对比 `Sonnet 4.6` 单用 69.1 分 @ $18.36**（OpenBMB 在七个任务上的自测，避坑 116 / 118）。"
    "⚠️ **与本报告工作区的关系必须写明**：**`WorkBuddyBench` 上被对比的一方就是本报告工作区的产品（74.7 分）** —— **本报告登记该数据但不做评价，只标注来源与未复现状态**。"
    "**另支持本地部署与飞书、微信等 IM 渠道，官方称智能路由使社媒任务费用降超 75%**；⚠️ **省的是模型成本，不是部署与运维成本**（避坑 118 同族） | 演进中 |",
]

REWRITE = {
    "Gemini 4 Argon": (
        "| Gemini 4 Argon | 037 | 改写 | "
        "**本期新增一条订阅档归属事实（属「往期条目本期有实质进展」的改写，不是纠错）**："
        "**`Gemini 4 Argon` 被明确纳入 Google AI Pro 与 AI Ultra 方案，不再向 AI Plus 用户提供** —— "
        "**这是本期「Google AI Plus 11/13 起失去 Pro 模型选择权」那条通知的一部分，两条要一起读**："
        "**AI Plus 在 11/13 起不仅失去手动选择 Pro 的能力，也一并失去 `Argon`**。"
        "⚠️ **036 期登记的口径不变**：`Gemini 4 Argon` 于 10/14 全球 GA，经付费版 `Gemini API` / `AI Studio` / `Antigravity` 与 Gemini 应用向 `AI Pro` / `AI Ultra` 订阅用户与付费 API 客户开放，"
        "**免费档与 $5 的 Plus 档仍拿不到**；**首发优惠价输入 $2 / 输出 $10 每百万 token（缓存输入按原价 5% 计）→ 11 月底恢复 $4 / $20**；**输出上限 100 万 token**；"
        "**10/15 新增 `Argon for Robotics`（`ERQA` 纯推理 87%，官方自披露）**；"
        "**基准全部为谷歌自披露**：`DeepSWE v1.1` 77.9% / `AutomationBench` 51.3% / `LVBench` 91.7% / `CWE-bench v1` 68% 并列第一，**AA Intelligence Index（High）52.6、最高推理档 53**。"
        "⚠️ **Q25（首发优惠价的恢复日与免费档开放时点）本期无新证据，维持挂账**：**官方只给「11 月底」这一相对口径，`OpenRouter` 模型页只给折扣幅度与发售日、无恢复日；"
        "**免费档开放时点仍只有 `Google AI Studio` 负责人 Logan Kilpatrick 的「正在开发其他版本的 Gemini 4」这一句**（避坑 154） | 演进中 |"
    ),
    "阶跃星辰 Step 5 Preview 开源权重": (
        "| 阶跃星辰 Step 5 Preview 开源权重 | 037 | 改写 | "
        "**本期新增一条对照事实（不改变本条定性）：同日 Meta 开放 `Muse Spark Open` 权重，但 HF 上是 gated 且访问表单要求「法定全名 + 出生日期 + 组织全称」** —— "
        "**两个 600B 级「开放权重」一个是 ungated、一个要提交身份信息，而本条的「三个仓库全部 ungated」正是它相对更好用的原因之一**（避坑 162）。"
        "⚠️ **036 期口径全部维持不变（037 期复核无变化）**：**10/15 按 9/20 承诺日期兑现；三个 HF 仓库（FP8 约 650 GB / BF16 约 1.2 TB / NVFP4 面向 Blackwell）+ ModelScope 同名镜像全部 ungated；"
        "**GitHub `stepfun-ai/Step-5-Preview` 只有 README、中英文协议、贡献者名单与图片，不含权重**；"
        "**规格：稀疏 MoE、总参约 600B（HF safetensors 合计 604.3B，取整说法）、每 token 激活约 27B、上下文与最大输出均约 100 万 token、输入文本 + 图像 / 输出文本；"
        "92 层 = 88 MoE + 4 稠密，352 路由专家选 8 + 1 共享，Sparse GQA**；"
        "**FP8 可跑 4×B300 或 8×H200 单节点，BF16 需 8×B300 或 16×H200**；**官方 Docker `vllm/vllm-openai:step-5-preview` 与 `lmsysorg/sglang:step-5-preview`**；"
        "**许可证 `StepFun Model License 1.0`（非 Apache），三条商业闸门：① 商业产品月活 >约 1 亿或月收入 >约 2,000 万美元须标注「Powered by StepFun AI」；② 硬件出厂内置（手机 / 汽车 / 眼镜 / 可穿戴 / 机器人 / 智能家居）须另签商业许可；③ 年收入 >约 2,000 万美元的 MaaS 须另签；内部自用豁免**（避坑 158）。"
        "⚠️ **与 `Muse Model License` 的门槛不可互相套用**：**后者是「MaaS 且合计总收入 >2,000 万」一条闸门，而本条是「月收入 >2,000 万 → 署名」与「年收入 >2,000 万 → 另签」两条不同闸门**。"
        "⚠️ **本条只是同期五条账之一**（权重 10/15 / 国内按量付费 API 缓存命中档 10/14 00:30 由 0.35 调到 0.70 元 / WorkBuddy 内 10/12–10/25 独家限免 / 各渠道免费周自 10/8 起算 / AGI Bar 店内线下免费），**勿并成一句**（避坑 148/150） | 演进中 |"
    ),
    "Claude Max·Team 月度 API 额度": (
        "| Anthropic Claude Max / Team 月度 API 额度 | 037 | 改写 | "
        "**本期新增一条官方确认（属「往期条目本期有实质进展」的改写，不是纠错）**："
        "**2026-10-15 Anthropic 正式确认，Claude Max 与 Team 计划订阅用户的月度 API 额度可直接用于 `Claude Agent SDK`、`claude -p` 命令、Claude API、Claude Managed Agents 以及所有使用相关技术的第三方应用** —— "
        "**业内称之为「BYOS」（自带订阅）模式**（钛媒体、站长之家、钛媒体《Edge AI Daily 早报（10 月 16 日）》）。"
        "⚠️ **变与不变必须分开写**：**额度数值完全不变（Max 5x $100/月、Max 20x $200/月、Team 每 Standard 席 $20 + 每 Premium 席 $100、公司池化上限 $500/月）；"
        "**变的是「适用范围由试点转为写入产品规则的长期安排」** —— **因此它属于「既有额度解锁更多出口」，不是「额度变多」**（避坑 54：**量纲没变就不要写成额度增加**）。"
        "**三条脉络（说明这条为何值得登记）**：**① 2026-04-04 Anthropic 以「第三方 agent 绕过 prompt cache 机制、token 消耗被倍数放大」为由封禁 `OpenClaw` / `OpenCode` 等路径；"
        "② 2026-05-13 恢复接入，但增设「不可滚存、用完不透支」的额度闸门（Pro $20 / Max 5x $100 / Max 20x $200 / Team 每席 $100 / Enterprise 每席 $200）；"
        "③ 2026-10-07 开发者生态团队成员 CJ Avilla 确认额度向 Max 与 Team 全面铺开（Team 池化上限 $500），10/15 最终由临时试点转为长期安排**。"
        "**036 期登记的边界全部不变**：**Pro 无；不覆盖交互式 Claude Code 会话；不可用于 Bedrock / Vertex / Foundry；需在计划内满 7 天才可领；不叠加订阅的应用内限额；当月未用即作废**（避坑 123）。"
        "⚠️ **「App Store 开放时刻」的类比属分析稿定性、非官方表述**（避坑 116） | 演进中 |"
    ),
    "智谱 AutoClaw 每日登录 credits": (
        "| 智谱 AutoClaw「每日登录领 credits」第二期 | 037 | 改写 | "
        "**本期回扫结论：已于 10/16 按原定日期收口（10/16 为活动最后一天，回扫未见延期或提前收口公告）**；"
        "**本期核到官方博客 Weekly Perks M10W2 的完整档位表（036 期未展开）**："
        "**10/12 首日全体可领 10,000 Credits（1 亿 GLM-5.3-Flash Tokens）；10/13–10/16 每日全体 800 Credits（800 万 Tokens）；"
        "付费会员额外每日奖励按档位 —— AutoClaw 月度订阅 Lite/Base/Pro/Max 分别 500 / 5,000 / 7,000 / 8,000 Credits；`GLM Coding Plan` 个人版 Lite/Pro/Max 分别 5,000 / 7,000 / 8,000 Credits**。"
        "**三条此前未写的边界（直接影响实操）**：**① 每日奖励当天午夜过期、当日领当日用；② 每账号每日限领一次；③ 账号持有多重会员时只取最高档、奖励不可叠加**（避坑 52）。"
        "⚠️ **036 期的口径纠正性质说明**：**不是「写错了」，而是「写得太粗」—— 「最多 1.32 亿」是把首日 1 亿与后四日 800 万混在一起的合计口径，读者无法从中推出「明天还能领多少」**；"
        "**本期第四章已按天展开并补上两套会员档位表**（见五·3）。"
        "⚠️ **与第一期是两条不同的账**（额度从「1,000 credits/天」变成「最多 1.32 亿 tokens/天」，量纲不同，避坑 117/140）。"
        "⚠️ **上一期记的「市面流传的充电礼 5000 万 / 300 万」「每周特权 1 亿 / 800 万」「普通用户合计 1.91 亿」「最高 4 亿」全部出自第三方情报站，以 App 内实际到账为准**；"
        "**「4 亿」是第三方按「非高峰半价 + 98% 缓存命中」推算的等效量，不是额度**（避坑 54）。"
        "⚠️ **下一轮强制动作：第三期是否接上**（本期未见公告） | 收口 |"
    ),
}

F = os.path.join(D, "frozen_items.md")
txt = io.open(F, encoding="utf-8").read()
lines = txt.rstrip("\n").split("\n")

# 改写：删掉旧行、插到文件末尾（按 036 期 fix036_ledger.py 的做法：改写行以新版本追加）
# ⚠️ 行名必须**精确相等**匹配，不能用子串 —— `Gemini 4 Argon` 与 `Gemini 4 Argon for Robotics`
#    是两行（036 期分两次登记），子串匹配会命中 2 行而触发断言。
for key, newline in REWRITE.items():
    hit = [i for i, l in enumerate(lines)
           if l.startswith("| ") and l.split("|")[1].strip() == key]
    assert len(hit) == 1, (key, len(hit), [lines[i].split("|")[1].strip() for i in hit])
    lines.pop(hit[0])

add = list(REWRITE.values()) + NEW
lines.extend(add)
io.open(F, "w", encoding="utf-8", newline="\r\n").write("\n".join(lines) + "\n")
print("frozen: rewrites %d + new %d = %d appended" % (len(REWRITE), len(NEW), len(add)))

# ---------------- open_questions.md：Q23 / Q26 补进展 ----------------
Q = os.path.join(D, "open_questions.md")
q = io.open(Q, encoding="utf-8").read()

Q23_OLD = "**下期回溯改为：腾讯云 / 腾讯开源官方页与 GitHub README 的「WorkBuddy」字样 + 官方新闻稿正文**。"
Q23_NEW = ("**037 期进展（维持，无新证据）**：**腾讯官方页与 GitHub README 仍无「WorkBuddy 开源版」表述 —— 产品身份一问仍未结，"
           "Q23 维持第 5 期**。⚠️ **本期新增一条同厂商对照事实（属背景、不结 Q）**：**腾讯智能体平台「元器」同期公告 11/9 停服、10/29 停止新建智能体与分发 API Key、"
           "数据导出窗口至 2027-01-09，迁移目标为腾讯云智能体开发平台 `ADP`** —— **说明同一家厂商在同一时间窗内，「开源并长期维护」与「关停并迁移」两条路线同时存在，"
           "因此不能从「某产品开源了」推断「腾讯的另一条产品线不会停」**。"
           "**下期回溯：腾讯云 / 腾讯开源官方页与 GitHub README 的「WorkBuddy」字样 + 官方新闻稿正文；另补 `QClaw` 条目（已公告 12/24 00:00 停运，本报告尚未登记）**。")
assert Q23_OLD in q
q = q.replace(Q23_OLD, Q23_NEW)

Q26_TAIL = "**取「免费档月度 API credits 有无与金额、Pro 月度 credits 金额、图像生成档位」三项的一手口径** |"
Q26_NEW = (Q26_TAIL[:-2] +
    " **037 期进展（维持，无新证据）**：**本期 `Mistral` 无任何新信息 —— 三方来源（一家价格比对站、一位第三方整理者、033 期起跟踪的 diff 站）仍互不一致，"
    "`mistral.ai` 官方定价页仍未逐项复核 → Q26 挂账第 2 期**（原「第一期」计法以首见 036 期为第 1 期）。"
    "⚠️ **本期同窗口内另有两处同类口径冲突，均按避坑 161 处置但不立 Q**："
    "**① `Apidog`（称免登录免 API Key 即可调用 OpenCode 免费档）与 `freetokens.custats.info`（称 Inference API 允许不带 Authorization 头、但 Console 配置另需账单信息）在「是否需要账号」上口径不同** —— "
    "**两口径都写、不合并成「完全无需账号」**；"
    "**② `PilotDeck 2.0` 的 `WorkBuddyBench` 得分两个数（腾讯研究院 / 波动智能 79.4、`theaiadventurer` 79.1）** —— "
    "**⚠️ 已核到两者并非矛盾而是配置不同（79.4 是换 35B-A3B 底座后的数、79.1 是该来源记录的默认配置数），故属「可当场判定」的同类差异，不需要长期挂账** —— "
    "**这与 Q26 的「三源对同一档位给出三个不同数字、无法当场判定谁对」不同构**（避坑 161 的两种适用场景）。"
    "**下期回溯：`mistral.ai/pricing` 官方定价页逐项对照（免费档 / Pro / Team 三档的 credits、Studio 模型测试、图像生成档位）+ 官方 changelog 或公告页；"
    "取「免费档月度 API credits 有无与金额、Pro 月度 credits 金额、图像生成档位」三项的一手口径** |")
assert Q26_TAIL in q
q = q.replace(Q26_TAIL, Q26_NEW)

io.open(Q, "w", encoding="utf-8", newline="\r\n").write(q)
print("open_questions: Q23 / Q26 updated")