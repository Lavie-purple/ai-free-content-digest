# -*- coding: utf-8 -*-
"""045 期：把本期新增/改写条目登记进 frozen_items.md。
⚠️ **data/ 下是 CRLF** —— 必须用 newline="\\r\\n" 写回。
⚠️ **先写库、再跑 check_frozen**。
"""
F = ".workbuddy/data/frozen_items.md"

STATUS = {
 "MiniMax M3.1 Flash 开放权重落地（HF 仓库 10/17 已建 · gated:false · minimax-community 许可三段 · 避坑 196/197）": "生效中",
 "OpenRouter minimax/minimax-m3.1-flash:free 免费档 10/22 结束（官方横幅逐字给出确切结束日 · :free 18→17）": "已终止",
 "OpenCode M3.1 Flash Free 同日下架（两页实访命中 0 · 官方无任何说明）": "已终止",
 "Anthropic 把 Agent Skills 开放标准捐赠给 Agentic AI Foundation（10/22 · 含名称/徽标/GitHub 组织/域名）": "生效中",
 "Anthropic 生命科学 guest investigators 公开招募（10/22 · at no cost to them · 约 14 天窗口）": "生效中",
 "Anthropic × Theorem：Claude 对 123 个 OSS-Fuzz 库完成汇编级形式化证明（10/22 · 第三方转录）": "生效中",
 "国办发〔2026〕29 号就业友好型意见（10/16 印发 · 10/23 公布 · 无个人免费额度入口）": "生效中",
 "智谱 AutoClaw 国内站 M10W4 一周福利 1 亿 Tokens（10/26–11/1 · 较 M10W3 的 2 亿降档）": "演进中",
 "freellm.net 计数器重取 520+/520/304/30/438/244（OpenRouter 专页首次与官方 API 逐条一致）": "演进中",
 "OpenAI Decisions API 正式可用 GA（10/22 · $0.10/$0.01 · 无免费层）": "生效中",
 "zcode.ai 域名已易主/停放（体育博彩页 · 登记项失效 · 避坑 198「消失」形态样本）": "已终止",
}

NEW = [
 ("MiniMax M3.1 Flash 开放权重落地（HF 仓库 10/17 已建 · gated:false · minimax-community 许可三段 · 避坑 196/197）", "045", "模型",
  "**045 期头条之一 —— 本报告自己连续两期判错的一处**：**043 / 044 两期都用 `hf-mirror.com/api/models?author=MiniMaxAI&limit=100`（默认排序）取组织页，得 `21` 个仓库、判定「权重未见」；本轮同一 URL 加 `&sort=createdAt&direction=-1` 返回 `22` 个仓库、`MiniMaxAI/MiniMax-M3.1-Flash` 居首（两种排序各实跑两次，结果可复现）**。"
  "**仓库一手字段（详情端点，读于 2026-10-23）**：`createdAt` `2026-10-17T06:37:50.000Z`、`lastModified` `2026-10-23T00:59:04.000Z`、`gated` `false`、`private` `false`、`license` `None`（API 字段为空）、`downloads` `357`（详情端点）/ `1,096`（列表端点，**两个端点同一次读取给出两个数，本报告两个都写**，避坑 161）、`likes` `2`、`siblings` `72` 个文件；`tags` 含 `transformers`、`safetensors`、`minimax_m3_vl`、`image-text-to-text`、`multimodal`、`moe`、`agent`、`coding`、`video`、`conversational`、`custom_code`、`arxiv:2606.13392`、**`license:other`**、`endpoints_compatible`、`8-bit`、`mxfp8`、`region:us`。"
  "**许可三个位置三个写法**：**① `HF` API 的 `license` 字段 = `None`；② README 逐字 `license: other` / `license_name: minimax-community` / `license_link: LICENSE`；③ `LICENSE` 正文（`raw/main/LICENSE`，3,363 字节）三段** —— "
  "**第①段非商用免费**（`Permission is hereby granted, free of charge … to deal in the Software for non-commercial purposes`）；"
  "**第②段商用两条义务**（`you shall prominently display “Built with MiniMax M3.1-Flash” on a related website, user interface, blogpost, about page or product documentation.`；且年收入超过 `20 million US dollars` 须向 `api@minimax.io` 发主题 `M3.1-Flash licensing - authorization request` 取得事先书面授权，否则只需一次性 notice）；"
  "**第③段 `Commercial Use` 定义极宽**（含(iii) `deployment or provision … that have been subjected to post-training, fine-tuning, instruction-tuning, or any other form of modification, for any commercial purpose`）；**附录另有 5 条禁止用途**（违法内容 / 军事目的 / 伤害未成年人 / 有意致害的虚假误导信息 / 歧视与仇恨言论）。"
  "**避坑 197 的三条结论**：**① 「权重可下载」（`gated: false`、72 个文件）≠ 「可商用」** —— 这是「非商用免费 + 商用须标注 + 年收入超 2,000 万美元须书面授权」的自定义许可，**不是开源许可**（与 031 期 `Nace AI Drex 1.5` 的 `Open RAIL-M` 变体同族，避坑 135/139）；"
  "**② 判许可必须读 `LICENSE` 正文，不能读 API 字段**（避坑 139 的加强版）；**③ `region:us` tag 的含义官方未解释，本报告不代官方解读**。"
  "**避坑 196（本期新立）**：**否证「某仓库不存在」只能用「直接取该仓库详情」这一种办法；用「列表里没有」否证，会把取数缺陷当成事实** —— 043/044 两期错在结论层而不只是计数层（避坑 100「计数与明细必须同源」的新反例，且反例出在本报告自己身上）。"
  "**生态侧（仅登记存在性）**：`HF` 检索 `M3.1` 命中 `30` 个仓库，10/23 当天批量出现第三方量化/移植版（`unsloth/MiniMax-M3.1-Flash` 04:17 UTC、`unsloth/…-GGUF` 04:20、`mlx-community/…-Text-4bit` 01:43 及三个 `-oQ*-mtp` 变体 03:00–03:02、`AMAImedia/…-NVFP4-GGUF` 05:13、`Mia-AiLab/…-EXL3-EAQ-v1-3.06bpw` 05:43、`vcruz305/…-EXL3-SAGE-2.15bpw` 03:43、`ArkhAngelLifeJiggy/…` 06:00），另有 `amd/…-Quark-MXFP4`（10/18）、`FlagRelease/…-W8A8-*` 系列（10/19，覆盖 `hygon`/`metax`/`ascend`/`mthreads`/`iluvatar`/`kunlunxin`/`tsingmicro`/`zhenwu`/`nvidia` 国产与商用卡）、`incoai/…-DFlash2`（10/19）、`RadixArk/Minimax-M3.1-Flash-Dflash2`（10/22）—— **这些第三方仓库的许可与可用性本报告一律不代判，它们的存在只能说明「权重确实已可下载」，不能说明「许可能商用」**。"),

 ("OpenRouter minimax/minimax-m3.1-flash:free 免费档 10/22 结束（官方横幅逐字给出确切结束日 · :free 18→17）", "045", "额度",
  "**045 期「收口」线的官方确证**：`openrouter.ai/minimax/minimax-m3.1-flash:free` 模型页顶部横幅逐字 `The free launch period ended Oct 22, 2026.`，**同页字段区仍写 `Price Free`、`Context` `1.0M`、`Released` `Oct 19, 2026`**（避坑 199：字段区与横幅/栏目标签可能矛盾，两个都必须读）。"
  "**官方 API 目录同步实跑（`openrouter.ai/api/v1/models`，读于 2026-10-23）**：**全量 `468` 个模型（与上期同值）/ 零价 `20` 个（上期 `21`）/ 带 `:free` 后缀 `17` 个（上期 `18`）** —— **差额精确定位为这一个模型**。"
  "**044 期「差额定位不到」的原因是上期没有留存 `:free` 全量清单；本期已把 17 条全量清单存档于 `.workbuddy/data/tmp_or_free_2026-10-23.txt`，下一期起可逐条 diff 并报出增减名**。"
  "**这是本报告跟踪 `OpenRouter` 免费档以来，官方第一次给出免费档的确切结束日** —— 但打破「无截止日」状态的不是公告页（`openrouter.ai/announcements` 本轮实访仍停 `October 14, 2026`），**是模型页上的一条横幅**。"
  "**聚合站口径本期反转**：**044 期记「聚合站的日期未核到故不采信」，本期官方横幅确认的结束日 `10/22` 与聚合站一致，但聚合站的「72 小时」与官方「10/19–10/22」仍不是一回事**（猜对的日期不等于猜对的口径）。"
  "**「零价 20」与「`:free` 后缀 17」仍不是同一集合**（差额为 `google/lyria-3-pro-preview`、`google/lyria-3-clip-preview` 与 `openrouter/free` 一个路由器），**写清单必须说清是哪一个口径**（避坑 161）。"),

 ("OpenCode M3.1 Flash Free 同日下架（两页实访命中 0 · 官方无任何说明）", "045", "工具",
  "**与 `OpenRouter` 同日收口、但零说明**：本轮实访两页（读于 2026-10-23）—— **① `opencode.ai/docs/go`（订阅页）模型列表现列 `M3.1` 与 `M3.1 Flash` 付费档、无 `M3.1 Flash Free`；② `opencode.ai/docs/zen`（按量付费页）`Free models` 段列 `DeepSeek V4.1 Flash Free`、`Exo Free`、`MiMo-V2.6-Flash Free`、`MiMo-V2.5-Flash Free`、`Nemotron 3.5 Lightning Free`、`Nemotron 3.5 Super VL Free`、`Big Pickle` 等，亦无 `M3.1 Flash Free`**；**全文检索 `M3.1 Flash Free` 命中 `0` 次**。"
  "**本行的收口判据是「两页同时不再出现该免费档字样」**；**`OpenCode` 两侧都没有发布任何关于本条下架的说明**（上游没给的不替它写，避坑 154）。"
  "**本报告不把 `OpenRouter` 的结束日套到 `OpenCode` 头上**（同类源之间也要标口径；未核到 ≠ 不存在，避坑 161）。"
  "**044 期在本行记的三条结论（`Unlimited` 是聚合平台口径等）随本条收口一并归档，本报告不重复往期已固化内容**。"),

 ("Anthropic 把 Agent Skills 开放标准捐赠给 Agentic AI Foundation（10/22 · 含名称/徽标/GitHub 组织/域名）", "045", "开源",
  "**官方一手（`anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation`，页面标注 `Published Oct 22, 2026` · `Category Product`）逐字**：`Today, we're donating Agent Skills, the open standard that gives AI agents specialized knowledge and workflows, to the Agentic AI Foundation (AAIF).`；`We are donating the Agent Skills name and logo, the GitHub organization, and the agentskills.io domain.`；`You can continue to use the standard or contribute to it without joining the AAIF.`。"
  "**治理结构（决定「中立」两个字的含金量）**：**`AAIF` 在 `Linux Foundation` 之下，`Anthropic` 与 `Block`、`OpenAI` 共同创立，`MCP` 此前已捐给它** —— 即这是同一个基金会的第二笔捐赠，不是新建一个壳；`Engineers from Anthropic, Google, OpenAI, and other companies will maintain the standard as individuals`，Lead Maintainers 为 `David Soria Parra` 与 `Mahesh Murag`。"
  "**规模数字全部带口径**：`More than 70 agent platforms, including ChatGPT, Cursor, GitHub Copilot, and VS Code, have integrated Agent Skills since we published the standard in December 2025.`；`So far, 1 million skills have been published and nearly 280 million installed.` —— **两个数都是官方自报，不是第三方实测**（避坑 165）。"
  "**⚠️ 「捐赠」不等于「开源许可变更」**：**公告全文没有写任何许可证条款**，规范正文在 `agentskills.io`（本轮实访可达，站上写 `Agent Skills are a lightweight, open format`）—— **本报告只写「标准与域名转入基金会」，不写「已改为某许可证」**（避坑 154）。"
  "**免费性判据**：标准本身可自由使用与贡献（`without joining the AAIF`）、无申请、无截止日 —— **这是避坑 193 三层次里的第①层「开源自取」**。"),

 ("Anthropic 生命科学 guest investigators 公开招募（10/22 · at no cost to them · 约 14 天窗口）", "045", "发布",
  "**官方一手（`anthropic.com/news/open-call-guest-investigators-life-sciences`，读于 2026-10-23）逐字**：`at no cost to them`、`8–12 weeks`（驻留时长）、`approximately 14 days`（申请审理时长）。"
  "**三条边界**：**① 官方不要数据、研究者保留数据权利**；**② 「免费」的客体是「参与研究的名额与工具」，不是 API 额度** —— **避坑 193 第③层「身份权益」的样本**；**③ 「约 14 天」不是截止日** —— 第四章该行截止列写「未公布」，不替厂商写一个日历日（避坑 154 / 166 / 187）。"
  "**下一轮强制动作**：申请窗口是否补出确切日历日、是否扩到 `US` 以外或非学术机构。"),

 ("Anthropic × Theorem：Claude 对 123 个 OSS-Fuzz 库完成汇编级形式化证明（10/22 · 第三方转录）", "045", "发布",
  "**045 期 `Anthropic` 三连发之三**。**⚠️ 本条的官方页 URL 与官方逐字引文本期未核到，全部字段来自第三方转录**（如实记，不当官方口径用）。"
  "**已登记的事实**：`Claude` 对 `123` 个 `OSS-Fuzz` 库完成汇编级形式化验证（`Coq` / `Lean` 证明），**证明子集公开**，`Theorem` 提供免费跑管线。"
  "**下一轮强制动作**：补官方页 URL 与逐字引文；`Theorem` 的免费跑管线是否给出申请入口与限制条件。"),

 ("国办发〔2026〕29 号就业友好型意见（10/16 印发 · 10/23 公布 · 无个人免费额度入口）", "045", "政策",
  "**《国务院办公厅关于适应人工智能技术发展助力构建就业友好型发展方式的意见》（国办发〔2026〕29 号）**，一手源 `gov.cn/zhengce/zhengceku/202610/content_7084108.htm`（全文已核），**署名日 `2026-10-16`、公布日 `2026-10-23`（两个日期都写）**。"
  "**三条边界**：**① 全文没有任何面向个人开发者的免费额度或补贴申领入口** —— 本报告不把它读成「发钱文件」；"
  "**② 这是「就业友好型」框架文件，不是技术管制文件**，**与同窗口的商务部 48 号公告是两条不同的线，不合并成一句**（避坑 134）；"
  "**③ 政府投资基金按市场化方式支持企业创新发展（国家创业投资引导基金、国家人工智能产业投资基金）—— 对象是企业，不是个人**。"
  "**第四章该行截止列写「无结束日（政策文件，非活动）」**。"),

 ("智谱 AutoClaw 国内站 M10W4 一周福利 1 亿 Tokens（10/26–11/1 · 较 M10W3 的 2 亿降档）", "045", "额度",
  "**官方一手（`autoclaw.zhipuai.cn/blog/news/M10W4/`，页面标注 `2026年10月23日` · 资讯）逐字**：`10 月 26 日（周一）00:00—11 月 1 日（周日）23:59（北京时间）`；`活动规则：登录 AutoClaw，即可领取 1 亿 Tokens（相当于 10,000 积分），每个账号限领一次。`；`奖励将在 11 月 1 日 23:59（北京时间）失效，越早领取，使用时间越充足哦。`"
  "**一次降档必须写全三样（避坑 198 本期新立）**：**① 上一档是多少 —— `M10W3` 国内站一次性档 2 亿 Tokens（20,000 积分，活动期 10.15–10.21，可领窗口已于 10/21 关闭）；② 这一档是多少 —— 1 亿 Tokens（10,000 积分，10/26–11/1）；③ 两档活动期是否相接 —— `M10W3` 到 10/21、`M10W4` 从 10/26 起，中间 10/22–10/25 四天没有一次性档，只有 10.15–10.25 的每日登录档（普通用户每日 500 积分 / 付费会员每日 800 积分）**。"
  "**本期未核到的一件事（如实记）**：**`M10W4` 公告只写了一次性 1 亿档，没有写 10.15–10.25 的每日登录档是否延续到 11/1 之后** —— 本报告不替官方续期，也不写「每日档已结束」（避坑 154 / 161：未核到 ≠ 不存在）。"
  "**国际站与国内站不是同一节奏**：本轮实访国际站 `autoclaw.z.ai/blog/news/M10W3/` 仍是 `Get 85M Tokens`、活动期 `Oct 19 – Oct 25 (UTC+8)`、`Oct 21–25` 每天 `500 credits (5M tokens)`（**连续第 5 次未被改回**）—— **国内站已发到 `M10W4`、国际站还停在 `M10W3`，两边不可互相推算**（避坑 163 多站点面）。"),

 ("freellm.net 计数器重取 520+/520/304/30/438/244（OpenRouter 专页首次与官方 API 逐条一致）", "045", "数据",
  "**045 期重取（六项全记账，读于 2026-10-23）**：**模型总数（Hero 句）`520+`（044 期 `510+`）/ `Models Tracked` `520`（`510`）/ `Free & Online` `304`（`301`）/ `Providers` `30`（同值）/ `No Credit Card` `438`（`425`）/ 经实时 API 验证 `244`（`241`）**；`Last update 2026-10-23 checked 2026-10-23`。"
  "**升 / 同值两种结果都写，不写趋势判断**（避坑 029）。"
  "**本期最大变化**：**`freellm.net/providers/openrouter` 专页 `Last Updated 2026-10-23`（044 期为 `2026-10-21`），列 `20` 个模型；本轮逐条比对，其 `20` 条与官方 API 的 `20` 个零价模型完全一致（含 3 个非 `:free` 后缀项）** —— **044 期「三个数都不吻合」的状态本期结束**。"
  "**⚠️ 但这是「转录站追上了」，不是「两个口径合并成一个」**（避坑 030：口径对齐不等于可以混用）—— 本报告继续把「官方 API 目录」与「转录站」当作两个源分别登记，不因为它们数值相同就只写一个。"
  "**专页其余字段（与 044 期同值，逐项记账）**：`Free Tier` `20 free models online`、`Base URL` `https://openrouter.ai/api/v1`、`OpenAI Compatible` `Yes`、`Phone Required` `No`、`Streaming` `Yes`、`Function Calling` `Yes`、`Vision` `Yes`、`Rate Limits Free Tier Primary Limit` `200 req/day (free tier)`、`Context Range` `66K – 1.0M`、`Credit Card` `Not required`、`Phone Verification` `Not required`；另有 `$10 lifetime top-up for 5× more rate limits` 与「`FreeLLM Score` `85/100`」（该站自评，本报告只登记存在性）。"
  "**额度口径仍是「三源三个数、都带来源」**：① `freellm.net` 的 `200 req/day`；② `OpenRouter` 官方 `docs/faq` 的「`50` 请求每日 / 购买满 `10 credits` 后 `1,000` 请求每日」；③ `benchlm.ai` 与 ② 同口径 —— **① 与 ② 在日请求数上直接冲突，不可取中间值、不可只写一个**（避坑 161）。"),

 ("OpenAI Decisions API 正式可用 GA（10/22 · $0.10/$0.01 · 无免费层）", "045", "发布",
  "**030 期登记条目 `Decisions API` 的 GA 里程碑**。**官方一手（`openai.com/index/decisions-api`，页面标注 `October 22, 2026`）逐字**：`Today, we're making the Decisions API generally available.`；`…helping applications get GPT‑6 Luna's intelligence on questions with bounded answers, helping applications … up to 10x faster than GPT‑6 Luna through the Responses API`；`Since public beta, we've added a native GPT‑Live integration, prompt …`；`400 questions per request, twice the previous limit.`；`We've also added capacity in several regions in Asia.`"
  "**定价（官方逐字）**：`Decisions API costs $0.10 per million input tokens` / `$0.01 per million cached input tokens`；`You only pay for input tokens: there are no output-token charges.` —— **「输出免费」是因为按选项返回概率、不生成文本，不是免费额度**（避坑 118/119 同源）。"
  "**全页没有任何 `free tier` / 试用额度 / 免费钟点** —— 第四章该行截止列写「未公布」。"
  "**`10x faster` 是厂商自报、对照系是「走 Responses API 的 `GPT‑6 Luna`**」（避坑 165）；**客户引语五个口径不取其中一个**（`Ramp` `4x faster and 30% cheaper`、`Sierra` `under 280 ms p95` 等，全部是厂商自报）。"
  "**与 030 期登记时的差别**：030 期是单一信源（第三方转述）且无定价，本期官方页已在手、定价三档齐全 —— **同一事件的「可断言字段」随一手源到位而增加，这是补登记不是重复登记**。"),

 ("zcode.ai 域名已易主/停放（体育博彩页 · 登记项失效 · 避坑 198「消失」形态样本）", "045", "事件",
  "**045 期「消失」线的唯一样本**：**本轮实访 `zcode.ai/` 返回 `1,043,615` 字节，但正文是体育博彩类停放页内容**（出现 `AI + Sports Betting = Winning Formula`、`sports betting revolution powered by artificial intelligence` 等字样，标题为 `AI PICKS The \"Next Big Thing\"?`）—— **即该域名已易主 / 停放，不再是本报告 026 期起跟踪的那个 `ZCode` 产品**。"
  "**处置**：**第四章 `ZCode / BigModel 新用户试用` 行状态列改为「登记项已失效（域名变更）」，不写「已结束」** —— 「活动到期」与「产品消失」是两件不同的事，混写会让读者以为厂商正常收口（避坑 198：降档 / 收口 / 消失三种形态必须分开写）。"
  "**连带待办变更**：**`ZCode 月报连续第 19 期未见` 这条待办从「等月报」改为「等域名 / 产品是否重新上线」**。"
  "**与 `智谱 ZCode 免费额度包`（⚪，10/7 截止）不是同一款产品，两行不合并**。"),
]

md = open(F, encoding="utf-8", newline="").read()
n0 = len([l for l in md.split("\n") if l.startswith("| ")])
lines = []
for name, issue, kind, body in NEW:
    assert "|" not in name, ("条目名含裸 | 会把 5 字段行切成更多字段", name)
    assert "|" not in body, ("条目正文含裸 | 会把 5 字段行切成更多字段", name)
    lines.append("| %s | %s | %s | %s | %s |" % (name, issue, kind, body, STATUS[name]))
add = "\n".join(lines)
md = md.rstrip("\n") + "\n" + add + "\n"
open(F, "w", encoding="utf-8", newline="\r\n").write(md)

n1 = len([l for l in open(F, encoding="utf-8", newline="").read().split("\n") if l.startswith("| ")])
print("frozen_items data rows: %d -> %d (+%d)" % (n0, n1, n1 - n0))

from collections import Counter
rows = [l for l in open(F, encoding="utf-8", newline="").read().split("\n") if l.startswith("| ") and "---" not in l]
print("field-count distribution:", Counter(len(l.split("|")) - 2 for l in rows))
