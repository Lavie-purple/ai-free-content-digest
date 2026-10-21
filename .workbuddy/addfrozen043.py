# -*- coding: utf-8 -*-
"""043 期：把本期新增/改写条目登记进 frozen_items.md。
⚠️ **data/ 下是 CRLF** —— 必须用 newline="\\r\\n" 写回，否则 git diff --stat 会显示成整文件重写（033 期事故）。
⚠️ **先写库、再跑 check_frozen** —— 它的「首登 / 未出现」判据字段就是本期才写入的内容。
"""
F = ".workbuddy/data/frozen_items.md"

STATUS = {
    "MiniMax M3.1 Flash 开放权重的四个状态（本期停在第 ② 级 · 避坑 188）": "演进中",
    "MiniMax-H3 的真实许可：自定义社区许可 + 地域排除美/欧/英/韩 + $20M 营收门槛（避坑 189）": "演进中",
    "MiniCPM-V 4.7 开源（Apache-2.0 · 无下载闸门 · 本报告至今最宽松的一档）": "生效中",
    "DeepSeek 全面开源内部推理框架 DeepInfer + deepseek-recipe（框架开源 · 本报告首次登记该类型）": "生效中",
    "OpenRouter / OpenCode 侧 M3.1 Flash 免费档：一手源核验 + 聚合站三条口径全部未核到（避坑 191）": "演进中",
    "Anthropic 反蒸馏公告全文与 OpenCode 事件的时间线对读（防护声明的分母/范围/有效期 · 避坑 190）": "演进中",
    "Anthropic 护栏拦截的请求自 9/24 起恢复计费（失败 ≠ 不计费）": "生效中",
    "freellm.net 计数器重取 510+/30/241（三项首次记到下降），且 :free 清单从 19 变 20（路径亦更正）": "演进中",
    "OpenRouter 侧 M3.1 Flash 免费档的实测性能与 AA 基准（第三方托管实测口径）": "演进中",
    "美国土安全部对 DeepSeek 的联邦采购排除与移除令（Federal Register 全文已核）": "生效中",
}

NEW = [
    ("MiniMax M3.1 Flash 开放权重的四个状态（本期停在第 ② 级 · 避坑 188）", "043", "模型",
     "**043 期头条 —— 本报告第一次把「开放权重」拆成四个可分别核验的状态**：**"
     "① 宣布了模型（官方 API 可调）② 官方承诺会开权重（官方文字出现 `open-weight` 或 `weights will be released`）"
     "③ 给了具体日期（官方正文出现可解析日期）④ 权重真的在 `Hugging Face` 上（组织页存在对应仓库）**。"
     "**本例取值：① ✅ 已上线（`platform.minimax.io` / `.cn`）② ✅ 官方 API 文档站（`platform.minimax.io/docs/guides/text-generation`）"
     "已在模型表里标「`An ultra-efficient` **`open-weight`** `model for everyday work`」、上下文 `1,000,000`；"
     "官方博客（`minimax.io/blog/minimax-m31f`，发布日 2026-10-19）逐字「`M3.1 Flash is now available through the MiniMax API, "
     "M Plan, and MiniMax Code.` **`Model weights will be released later.`**」③ ⚠️ 官方博客与文档站**均无任何日期** —— "
     "**「10 月 23 日」只出自 `MiniMax` 官方 X 与第三方（`The Decoder` / `SiliconANGLE` / `HuggingNews` / `RITS`），"
     "`RITS` 逐字「`The reported October 23 date is a plan, not a checkpoint.`」④ ❌ 本轮实访 `HF` `MiniMaxAI` 组织页，"
     "**20 个仓库逐个核过（`MiniMax-H3`、`MiniMax-Music3`、`MiniMax-M3`、`MiniMax-M3-MXFP8`、`MiniMax-M2`/`M2.1`/`M2.5`/`M2.7`、"
     "`VTP-Small`/`Base`/`Large`、`Text-01`、`Text-01-hf`、`VL-01`、`M1-40k`/`M1-80k`/`M1-40k-hf`/`M1-80k-hf`、"
     "`SynLogic-32B`/`Mix-3-32B`/`7B`），无任何 `M3.1` 仓库，`gated` 均为 `false`**。"
     "**⚠️ 参数量与许可证官方均未给，本报告不代为确认**（`428B`/`23B` 只见于第三方，且 `RITS` 注明是借 `M3` 的 model card）（避坑 116）。"
     "**⚠️ 在第 ④ 级之前，一律按「只能用 API、不能下载」规划**（避坑 41 第四层 / 139）。"
     "**⚠️ 三条纪律**：**① 「官方文档站标 open-weight」与「官方博客说 later」是同一家厂商给出的强度不同的承诺，"
     "引用时要说清是哪一处**（避坑 143 同族的新形态）；**② 官方博客与文档站的承诺强度不一致时，以较弱者为准做规划**；"
     "**③ 第三方给的日期只能写成「第三方口径」** —— **写「`MiniMax` 官方确认 10 月 23 日开放权重」是失实的**。"
     "**⚠️ 与本表 `MiniMax-H3` 那条并读可得一个更硬的结论**：`H3` 的许可 8/2 就已发布、`HF` 上已下载 489 万次、`gated: false` —— "
     "**即同一家的另一个模型早已走完 ③④，本期的 `M3.1 Flash` 还停在 ②**。"),

    ("MiniMax-H3 的真实许可：自定义社区许可 + 地域排除美/欧/英/韩 + $20M 营收门槛（避坑 189）", "043", "口径",
     "**043 期核实 —— 本报告至今最完整的一份许可读数，也是「开放权重 ≠ 可随意使用」的最强样本**："
     "**`Hugging Face` 的 `MiniMaxAI/MiniMax-H3` 仓库字段逐字**：`gated: false`、`downloads: 4890714`、"
     "**`license: other`**、**`license_name: minimax-h3-community-license-agreement`**、`license_link: LICENSE`、"
     "`createdAt: 2026-07-28`、`lastModified: 2026-08-13`。"
     "**许可原文（`LICENSE`，许可日 `2026-08-02`，标题「`MiniMax H3 COMMUNITY LICENSE AGREEMENT`）关键条款**："
     "**① 地域排除（最易漏）**：「`Applicable Territory` means worldwide, **excluding the Excluded Territories**」；"
     "「`Excluded Territories` means the **European Union, the United Kingdom, the Republic of Korea and the "
     "United States of America**」；原文另写「should any person in such Excluded Territories be interested in deploying "
     "our models, you are welcome to **contact us about obtaining a license**」—— "
     "**即在中国大陆之外的四个主要市场按许可条款不授予使用授权**；"
     "**② 商业门槛**（官方授权申请表 `platform.minimax.io/h3-license` 逐字）："
     "「**Does the commercial products and services offered by the applicant generate annual revenue in excess of "
     "US$20,000,000?**」，国家选项含「**South Korea / United States / United Kingdom / European Union** / other」，"
     "并有「We will **indemnify and hold harmless** MiniMax」条款 —— **年营收超 2,000 万美元需事先书面授权**；"
     "**③ 署名义务**（二手转述，许可原文页面本机不可达、未逐字核到）："
     "使用 `H3 Works` 的商业产品需在界面**显著标注「MiniMax H3」**（许可 IV.2）；"
     "**④ 反蒸馏**（许可原文逐字）：「`Model Derivatives` means… any other machine learning model created by transferring "
     "the patterns of the weights, parameters, operational patterns, or Outputs of MiniMax H3… **including by distillation "
     "methods**, methods using intermediate data representations, or methods based on training using synthetic-data Outputs`」；"
     "**⑤ 授权主体**：「`We`, `Us` or `MiniMax` means **Nanonoble Pte. Ltd.**」（新加坡实体）；"
     "**⑥ 开源范围**：开放权重仅 `H3-Base`（FL2VA / Ref2VA，BF16）；`H3-Context-IR` 仅托管、`H3-Regeneration-2K` 未开源。"
     "**⚠️ 043 期新立避坑 189（开放权重的许可是五层）**：**① 下载闸门 ② 许可类型 ③ 地域范围 ④ 商业门槛 ⑤ 衍生义务** —— "
     "**本例把 ③④⑤ 三层同时演示了一遍，而这三层恰好是「下载闸门 + 许可类型」这两个常见问法覆盖不到的**（037 期避坑 162 的扩展）。"
     "**⚠️ 必须同时给反例**：**同期 `MiniCPM-V 4.7` 是 `Apache-2.0` + `gated: false` + 无地域排除** —— "
     "**否则读者容易把「某家的模型有地域排除」误推成「这类的模型都有」**（避坑 163 的多站点面同样适用于同一家的不同模型）。"
     "**⚠️ 归类**：本条是**许可口径**、不是免费额度活动，**但它直接决定「能不能下载后商用」**（避坑 41 第四层）。"),

    ("MiniCPM-V 4.7 开源（Apache-2.0 · 无下载闸门 · 本报告至今最宽松的一档）", "043", "模型",
     "**043 期新登记 —— 与 `MiniMax-H3` 构成本报告第一组「许可档位完全相反」的对照样本**："
     "**`OpenBMB` 的 `MiniCPM-V 4.7`（端侧多模态模型集合，覆盖 35B-A3B 与 1B 两种规模）**。"
     "**本轮实访 `HF` API 一手字段**：**`openbmb/MiniCPM-V-4.7-35B-A3B`** 与 **`openbmb/MiniCPM-V-4.7-1B`** 两个仓库 —— "
     "**`gated: false`、`disabled: false`、`private: false`（即无下载闸门、无需点同意、无人工审核）**、"
     "**`license: apache-2.0`（可商用、可修改、可再分发，仅需保留版权与 NOTICE）**；"
     "**实际参数量 `35,212,875,824`（35.2B）与 `1,554,476,272`（1.55B）**（`safetensors` 统计）、存储 `70.6 GB` / `3.30 GB`、"
     "**下载量 `95,240` 与 `46,506`**、`createdAt` 2026-10-07 / 2026-10-06、`lastModified` 2026-10-19 12:52、"
     "`pipeline_tag` `image-text-to-text`、likes `1079` / `399`、权重分片 16 个 / 单个。"
     "**⚠️ 量化格式（一手仓库名 + tags 全清单，共 13 个衍生仓库，全部 `license:apache-2.0`）**：**GGUF**"
     "（`-35B-A3B-gguf` / `-1B-gguf` / `-35B-A3B-DSpark-gguf` / `-1B-DSpark-gguf`）、**GPTQ**、**AWQ**、**int4**、**FP8**、"
     "另有 `-DSpark` 推测解码草稿模型。"
     "**⚠️ 一个容易踩的判读点**：**`FP8` 那个仓库的 tags 是 `quantized` + `compressed-tensors`，并没有独立的 `fp8` 标签** —— "
     "**「FP8」只出现在仓库名里**。"
     "**⚠️ 两条不能替它确认的字段**：**① 上下文长度 —— `HF` API 与 config 均未给出，第三方说法冲突（`256K` vs 约 `976K`），"
     "本报告两说并列、不取中间值**（避坑 161）；**② 仓库名用点号不是下划线** —— **搜 `MiniCPM-V-4_7` 会 404**。"
     "**⚠️ 归类**：本条是**开放权重发布**、不是免费额度活动，**但「能下载吗（闸门）」与「能商用吗（许可）」两个字段都已核到**"
     "（避坑 41 第二层 / 第四层 / 避坑 162）。"),

    ("DeepSeek 全面开源内部推理框架 DeepInfer + deepseek-recipe（框架开源 · 本报告首次登记该类型）", "043", "发布",
     "**043 期发布线头条 —— 本报告第一次登记「框架开源」这个条目类型（此前登记过的开源条目全是「模型权重」）**："
     "**`DeepSeek` 于 10/20 宣布全面开源内部推理框架 `DeepInfer`，并同步开源生产级 Token 编解码组件 `deepseek-recipe`**。"
     "**⚠️ 取料面（如实记）**：**官方为微信公众号，本轮网页端未取到；以下字段据中新经纬、澎湃、中国基金报、证券时报、腾讯新闻"
     "五家转述的同一段原文**（避坑 116 / 143）。"
     "**① 官方逐字**：「`基于 DeepInfer，已实现 DeepSeek V4.1 Flash 高吞吐、低延迟的大规模推理服务`」；"
     "`deepseek-recipe`「与 `DeepSeek` 官方 API 处理逻辑完整对齐，确保社区获得与官方部署一致的 API 体验」；"
     "能力含「**分布式推理、推测解码、SWA Bounded Replay、结构化输出**」，「可在**英伟达与华为昇腾平台**上运行」；"
     "**② 官方给的量化数字**：「**单一集群的服务吞吐是 155 万亿 Tokens/天，整体收入是每卡每小时 38 美金（按谷价）**」。"
     "**⚠️ 本报告自算（只做算术、不做判断）**：单卡 24 小时满负荷 = `38 × 24 = 912` 美元/天 ≈ 人民币 `6,090.48` 元/天；"
     "30 天 ≈ 人民币 `18.27` 万元/卡/月。"
     "**⚠️ 这两个数对读者是双向的**：**① 正向 —— 它把「自建推理 vs 调 API」第一次量化了，但「自建一定更省」这个结论本报告不下**"
     "（**未算电费、折旧、机房、人力、故障率，也未算峰值容量与闲时浪费**，避坑 165：厂商自报的经营数字只作量级参考）；"
     "**② 反向 —— 它同时把厂商的成本结构公开了**。"
     "**⚠️ 腾讯新闻那篇转述里有一句推论**（「大规模云厂商部署非原生 `DeepSeek` 的调用成本甚至存在低于官方原生的可能性」）—— "
     "**本报告明确标注为转述方推论、不是官方口径，也不写成结论**（避坑 116）。"
     "**⚠️ 一条最容易当成「免费」但不是的区分**：本条开源的是**代码**，**不改变 `DeepSeek` 官方 API 的任何计费** —— "
     "本报告 040 期登记的 `Search`/`Fetch`「11/1 00:00（北京）起按请求计费」与 `V4.1-Flash-1017` 的谷/峰价全部维持**（避坑 154）。"
     "**⚠️ 本条的类别定位**：**权重开源的判据是「能不能下载、许可是什么」；框架开源的判据是「能不能跑起来、依赖什么硬件、支持哪些平台」** —— "
     "**本条的关键字段是「英伟达 + 华为昇腾双平台」**（避坑 41 第二层：能否跑起来）。"),

    ("OpenRouter / OpenCode 侧 M3.1 Flash 免费档：一手源核验 + 聚合站三条口径全部未核到（避坑 191）", "043", "额度",
     "**043 期免费额度线最重要的一条 —— 聚合站说了什么与官方一手源写了什么，第一次正面冲突**："
     "**① `OpenRouter` 侧**（`openrouter.ai/minimax/minimax-m3.1-flash:free`，本轮实访）逐字字段："
     "「`Modalities` `Price` **Free** `Context` **1.0M** `Released` **Oct 19, 2026**」；"
     "Providers 表「`MiniMax` — 输入 **Free**、输出 **Free**、`1.66s`、`75 tps`、`100.00%`」；模型描述末尾「**Open weights are planned.**」；"
     "**页面上不存在 `limited time` / `until` / `expires` / `promotional` / `region` / `not available in` / `credit card` / "
     "`top up` / `minimum purchase` 任何一项**。"
     "**⚠️ 而聚合站称「`OpenRouter` 于北京时间 10/19 20:01 宣布免费 72 小时、约至 10/22 20:01、之后价格 $0.15/$0.60/$0.015」—— "
     "本轮实访 `openrouter.ai/announcements`（该 URL 实为 Blog 列表页）最新一篇为 `October 14, 2026`，"
     "按猜测 slug 实访 `openrouter.ai/blog/announcements/minimax-m3-1-flash-free` 返回 `404 —— Page Not Found`**，"
     "**即「官方公告」这一处本轮不存在，故 72 小时与截止钟点本报告不采信为官方口径**。"
     "**⚠️ 本期抓到一个极高危误读点**：**该模型页上确实出现「`3 days`」三个字，但它不是免费期** —— "
     "原文是「`Uptime is the percentage of the past 3 days that at least one provider was responding to requests.`」"
     "与「`Availability over the last 3 days — Oct 17, 9 PM - Oct 20, 9 PM`」，**即 uptime 统计窗口**；"
     "**把 uptime 窗口读成「限免 3 天」是凭空造出一个截止日**（避坑 116 同族的新形态：**误读可以发生在「读到哪个字段」这一步**）。"
     "**② `OpenCode` 侧**（两页逐字分列，不合并）：**`docs/go`（订阅页）** —— 「`MiniMax M3.1 Flash Free (limited time)`」、"
     "「`Free` `Free` `Free` — **`Unlimited`**　`limited time`」、表下「**Free for a limited time.**」、"
     "Model ID `minimax-m3.1-flash-free`、Endpoint `https://opencode.ai/inference/go/openai/v1/chat/completions`、"
     "请求量估算「**Unlimited** ×3 档」（per 5 hours / week / month）、Go `$10/month`、Go Plus `$40/month`；"
     "**`docs/zen`（按量付费页）** —— 「`MiniMax M3.1 Flash Free`」、价格「`Free` `Free` `Free` `Free`」、"
     "「**Its provider follows a zero-retention policy and does not use your data for model training.**」、"
     "Endpoint `https://opencode.ai/inference/openai/v1/chat/completions`、同页唯一的 `MiniMax` 付费档是 `MiniMax M3 $0.30 / $1.20 / $0.06`"
     "（**没有 `M3.1 Flash` 的付费档**）。**两页均只标 `limited time`、全页无 `3 days` / `72 hours` / 任何钟点** —— "
     "**聚合站那条「免费 3 天 / 10/19 20:17 公告」在一手源未核到**。"
     "**⚠️ 039 期记的「`docs/zen` 与 `docs/go` 两页对同模型给出相反答案」本轮未复现** —— "
     "**但这只是本轮观察、不是冲突已消解**（避坑 180）；**两页仍有一处结构性差异：endpoint 不同、计费体系不同、"
     "只有 `docs/go` 给「Unlimited」的请求量估算**。"
     "**⚠️ 地区限制**：**两页均未对本条标 `limited regions`**，而同页 `Beam Free` 标了且含中国大陆 —— "
     "**即「别的条目有」≠「这条也有」，但「页面没写」仍不等于「没有限制」**（避坑 181 及其反向）。"
     "**⚠️ 一条本报告第一次记的免费档形态**：「`Unlimited`」是**聚合平台自己给的估算**，不是上游厂商承诺（避坑 116）。"),

    ("Anthropic 反蒸馏公告全文与 OpenCode 事件的时间线对读（防护声明的分母/范围/有效期 · 避坑 190）", "043", "口径",
     "**043 期新登记 —— 本报告第一次把「厂商的防护公告」与「另一平台的安全事件」放在一起对读，而对读结果与直觉相反**："
     "**`Anthropic` 一手（`anthropic.com/research/distillation-defenses`，发布日期 `Oct 12, 2026`，分类 `Safeguards`）逐字**："
     "**① 降幅**：「**Early evidence suggests that these methods have reduced the amount of data harvested by distillers by "
     "around 90 to 99%.**」—— ⚠️ **页面摘要的措辞更弱**（「`reduced the rate of distillation by more than 90%`」），"
     "**`90–99%` 说的是「被采集的数据量」、摘要说的是「蒸馏发生率」，两者不是同一个量**（避坑 161）；"
     "**② 措施三条**：「`Controlling where reasoning can go.`」（`preserved thinking`；"
     "「prevents new API accounts (those created **on or after August 31, 2026**) from editing Claude's prior context」）、"
     "「`Blocking and patching extraction attempts.`」（「a two-stage classifier system`，「**false positive rate of less than 0.1%**」）、"
     "「`Making repeated attempts difficult.`」（「stricter usage limits… we ban the associated accounts」）；"
     "**③ 适用模型**：「currently, **Claude Sonnet 5.5, Claude Opus 5 and 5.5, and Claude Fable 5 and 5.1**」；"
     "**④ 官方自述的边界**：「**We don't yet know how long these gains will last.**」「We expect that **attackers will find ways "
     "around these safeguards**」；**⑤ 计费恢复**：「**since September 24, we have resumed charging for requests that are blocked "
     "by our safeguards before Claude responds**, in the specific areas (including distillation) where they have a <0.1% false "
     "positive rate」；**⑥ 具名案例**：点名 `Zhipu`（`GLM-5.3` 蒸馏美模型 cyber 能力，"
     "「after finding that our cyber safeguards degraded its attacks, it **switched to an older Claude model** and another lab's model」）"
     "与 `Moonshot`（`Kimi` 请求被秘密转发至 `Claude`）。"
     "**⚠️ 与 `OpenCode` 事件（040–042 期已登记）的对读结论只有三条，本报告不越线**：**① 时间线 —— 公告在攻击"
     "（10/16–17 夜）之前约 4–5 天；② 防护面不重合 —— `Anthropic` 的分类器跑在它自己家的 API 模型上，"
     "而 `OpenCode` 事件里泄露的是存放在 `OpenCode Console` 的第三方 API 密钥，双方原文都没说这两个防护面是否重合；"
     "③ 归因本身有第三方质疑 —— `TechCrunch` 明确记录「`Some skeptics called the framing an overstretch, arguing that the incident "
     "was a straightforward breach whose use for distillation remains unproven`」，且 `OpenCode`「`didn't specify how the distillation "
     "attack occurred`」—— 即「这是蒸馏攻击」是 `OpenCode` 的定性、不是已证实的事实**（避坑 116 / 132）。"
     "**⚠️ 043 期新立避坑 190**：**读到「防护降低了 X%」时问三句 —— ① X 的分母是什么 ② 防护覆盖哪一段链路 "
     "③ 官方有没有写有效期；三句都能从原文抄到就照抄，抄不到就写「未公布」**。"
     "**⚠️ 本行不写「防护失效」也不写「防护有效」**（避坑 190）。"),

    ("Anthropic 护栏拦截的请求自 9/24 起恢复计费（失败 ≠ 不计费）", "043", "额度",
     "**043 期新登记 —— 一条被多数转述漏掉的官方计费变化（它就夹在 10/12 那篇反蒸馏公告里）**："
     "**`Anthropic` 10/12 公告原文逐字**：「Additionally, **since September 24, we have resumed charging for requests that are "
     "blocked by our safeguards before Claude responds**, in the specific areas (including distillation) where they have a "
     "<0.1% false positive rate.」"
     "**⚠️ 这意味着被安全护栏拦下的请求、在指定范围内（误报率 <0.1% 的那些场景，含蒸馏）自 9/24 起恢复计费** —— "
     "**即「请求失败」不再等于「不计费」**。"
     "**⚠️ 这与 040 期登记的 `DeepSeek Search`/`Fetch`「失败/空结果/超时一律不计费」恰好是相反的成本结构**"
     "（避坑 176：**按请求计费与按 token 计费是相反的成本结构 —— 这里再多一类：按「是否被拦截」计费**）。"
     "**⚠️ 范围纪律**：**只覆盖官方明说的那些场景（误报率 <0.1% 的区域，含蒸馏），其余场景本报告不作断言**（避坑 41 第一层）。"
     "**⚠️ 对读者的动作**：**做 `Anthropic` API 成本估算时，被护栏拦下的请求要按「计费」计，不要按「免费」计**。"),

    ("freellm.net 计数器重取 510+/30/241（三项首次记到下降），且 :free 清单从 19 变 20（路径亦更正）", "043", "口径",
     "**`freellm.net` 本轮重取（043 期登记，按 029 期纪律三种结果都记账）**："
     "**`510+` 模型 / `30` 提供方 / `241` 经实时 API 验证 / 更新至 2026-10-21（checked 2026-10-21）**。"
     "**与 042 期（`512+ / 30 / 243`）对照：模型数 ↓、提供方数 同值、实测数 ↓**（**本期是该站计数器首次下降** —— "
     "039→042 一路为 `500+→505+→512+`）。**与 041 期（`505+ / 30 / 237`）、040 期（`500+ / 30 / 233`）对照同上**。"
     "**本报告只记事实、不写趋势判断**（避坑 161）—— **两期之间发生了什么（是否有模型下线、是否有目录改版）本轮未核到，故不解释**。"
     "**⚠️ 「免绑卡数」本轮该站首页重新单列**（原文「`Browse` **`425+`** `models that never ask for a card`」）—— "
     "**042 期该字段未单列，故本期该字段与上期不可比**（030 期纪律：**口径变过就不相减**）。"
     "**⚠️ 同站内部两处口径不一（新发现）**：首页写 `510+`，而目录页 `freellm.net/models/` 写「`Directory of Free LLM APIs: "
     "Compare` **`302+`** `Models`」—— **本报告两处并列、不做调和**（避坑 161）。"
     "**⚠️ 其 `OpenRouter` 专页的 URL 本期更正** —— **042 期记的 `freellm.net/openrouter` 不存在，正确路径是 "
     "`freellm.net/providers/openrouter`**（页面 title 即含 `20 Models`）。"
     "**⚠️ 该页 `:free` 清单本期为 `20` 条**（页面四处一致：「`20 free models online`」「`Supported Models` `20 models`」"
     "「`Total Models` `20 listed`」与 title），**与 038、041、042 三期的 `19` 不同，即连续三次同值后本期首次变化**；"
     "**且 042 期说「该站首次给出全部 19 个 `:free` 模型的 slug」在措辞上不准确 —— 那 19 条里有 2 条不带 `:free` 后缀"
     "（`google/lyria-3-pro-preview`、`google/lyria-3-clip-preview`）、还有 1 条是路由器 `openrouter/free`（`Free Models Router`，200K）**，"
     "**即真正带 `:free` 后缀的是 17 条**（避坑 100：**计数与明细必须同源**）。"
     "**本期新增 1 条**：`minimax/minimax-m3.1-flash:free`（1.0M）；`Last Updated` **`2026-10-21`**；"
     "模型详情页另写「`Free listing since` `Oct 19, 2026`」「`Released` `Oct 19, 2026`」；上下文区间「`66K – 1.0M`」；"
     "全部 20 条站上状态均为 `Online`；分类计数「`Chat 20 models`　`Reasoning 8 models`　`Coding 1 model`　`Vision 1 model`」。"
     "**⚠️ free tier 限速的三种写法（本期为该口径冲突的第 5 次记账）**：该站写「`The free tier (marked :free) offers` "
     "**`200 requests/day — or 1,000/day with a $10 lifetime top-up`**」、命中后是「**`429`** rate limit error」、日重置在「**`midnight UTC`**」；"
     "**`OpenRouter` 官方 FAQ（`openrouter.ai/docs/faq`）写 `50` 次/日、买满 `10` credits 后 `1,000` 次/日**；"
     "**而该站自己的第三处写法是「`$10 lifetime top-up for` **`5×`** `more rate limits`」—— 若基数为 200 则 5× = 1000（自洽），"
     "若基数为 50 则 5× = 250（与官方 1000 不自洽）**。**三说并列、不取中间值**（避坑 161）。"),

    ("OpenRouter 侧 M3.1 Flash 免费档的实测性能与 AA 基准（第三方托管实测口径）", "043", "口径",
     "**043 期新登记 —— 本报告第一次登记 OpenRouter 免费档的实测面板数字（`OpenRouter` 自己观测到的第三方托管实例数据，"
     "不是厂商自报）**：**`openrouter.ai/minimax/minimax-m3.1-flash:free` 本轮实访**："
     "**延迟**：`P50` **`1.66s`**（P50, best provider）、`P75 2.11s` / `P90 3.65s` / `P95 5.52s` / `P99 13.04s`；"
     "**吞吐**：`P50` **`75 tok/s`**（P50, best across providers）、`Avg 88 tok/s` / `P75 63` / `P90 41` / `P95 30` / `P99 15`；"
     "**端到端延迟**：`E2E P50 Avg 7.87s` / `P99 Avg 156.50s`；"
     "**工具调用错误率**：`MiniMax` **`Avg 4.30 %`**；**缓存命中率**：`MiniMax` **`Avg 90.49 %`**；"
     "**可用性（3d）**：`Uptime` **`99.99%`**、`Availability` **`99.79%`**，近 24 小时 `99.78%`。"
     "**⚠️ 这组数字与「厂商自报 200+ TPS / P50 170+ TPS」不是一回事**（避坑 165 / 178）—— "
     "**厂商口径是峰值、第三方托管实测是分位，两者测的不是同一件事；本报告两说并列、不判定谁对**。"
     "**⚠️ 对读者最有用的一条**：「`Tool call error rate` **`Avg 4.30 %`**」—— **即做 agent 编排时，每 25 次工具调用约有 1 次会失败**，"
     "**这个量级在官方资料里完全看不到**。"
     "**⚠️ 同一页转录的 `Artificial Analysis` 基准（第三方口径）**：`Intelligence Index` **`42.7`**（`#21 of 351`）、"
     "`HLE` `48.0%`（`#13 of 337`）、`AA-LCR` `79.7%`（`#47 of 285`）、`GDPval-AA` `47.9%`（`#30 of 158`）、"
     "`CritPt` `22.3%`（`#20 of 282`）、`SciCode` `53.4%`（`#35 of 129`）、`Terminal-Bench 4.0` **`25.8%`**（`#22 of 124`）、"
     "`AA-Omniscience Accuracy` `56.2%`（`#9 of 280`）、**`AA-Omniscience Non-Hallucination Rate` `7.2%`（`#256 of 280`）**。"
     "**⚠️ 最后一项必须单独看** —— **`7.2%` 的非幻觉率意味着它在不确定时几乎不拒答**（`The Decoder` 侧表述为「`93 percent` 幻觉率」），"
     "**即「`Intelligence Index` 排第 21」与「非幻觉率排第 256」是两个方向相反的事实**（避坑 165）。"
     "**⚠️ 处置**：**这些数字全部是第三方口径、且 `AA` 的抓取时点与厂商自报不同 —— 本报告只登记、不把任何排名写进第四章行内**（避坑 116）。"),

    ("美国土安全部对 DeepSeek 的联邦采购排除与移除令（Federal Register 全文已核）", "043", "事件",
     "**043 期政策线唯一一条可判定的新事件，一手源（`Federal Register` 全文）已核到**："
     "**`Federal Register` 第 91 卷第 201 期（2026-10-20 星期二），`govinfo.gov` 全文**："
     "**标题**「`Notice of Order Regarding Exclusion and Removal of DeepSeek Products From Federal Civilian Executive Branch "
     "Information Technology Systems and Procurements`」；**案号** `Docket No. DHS-2026-0628`、`FR Doc No. 2026-21447`、"
     "「`[FR Doc. 2026-21447 Filed 10-19-26; 8:45 am]`」；"
     "**法律依据**「Pursuant to the authority granted by the **Federal Acquisition Supply Chain Security Act of 2018**, "
     "41 U.S.C. 1321-1328, and implementing regulations at 41 CFR 201-1」；"
     "**命令两条（逐字结构）**：**① 「exclusion of information technology products and services developed by Hangzhou DeepSeek "
     "Artificial Intelligence Co., Ltd (DeepSeek), to include affiliated entities as defined in 48 CFR 2.101, from federal "
     "civilian agency procurements」；② 「removal of all DeepSeek and DeepSeek-affiliate products, and **third-party products and "
     "services developed using DeepSeek implementations**, from civilian agency information technology」**；"
     "**落地渠道**「The Federal Acquisition Security Council Recommendation」；签署人 `James H. Percival II, General Counsel`；"
     "附件见 `regulations.gov` 的 `DHS Docket Number DHS-2026-0628`；联系入口 `FASCSA Order Implementation Team, CISA Cybersecurity "
     "Division, fascsa.orders@cisa.dhs.gov`。"
     "**⚠️ 命令第二条里那句最容易被读漏的话**：「**and third-party products and services developed using DeepSeek implementations**」"
     "—— **即受令移除的不只是 `DeepSeek` 自家产品，还包括「用了 `DeepSeek` 实现做出来的第三方产品与服务」**（避坑 41 第三层）。"
     "**⚠️ 中文侧两方声音，本报告两说并列、不取其一（避坑 132）**：**① 商务部（10/20 晚，央视新闻 / 北京日报客户端）** —— "
     "「中方对此**强烈不满、坚决反对**」，定性为「**典型的泛化国家安全概念、滥用行政手段打压中国企业的行为，"
     "实质上是将科技经贸问题政治化、工具化**」，敦促美方「**立即纠正错误做法……撤销有关歧视性限制措施**」，"
     "并写明「将密切关注事态进展，对于任何实质性损害中方利益的行为，将采取一切必要措施」；"
     "**② 中国日报社论（10/20，标题「`US crackdown on tech counterproductive`」）** —— "
     "「Washington aims to slow down China's AI advances to maintain its competitive standing」，"
     "并提到同日美国国务院依据《Protecting American Intellectual Property Act of 2022》对五家中国实体实施制裁、"
     "以及中美上月就建立「中美 AI 对话」达成共识、下一次交流定在 11 月。"
     "**⚠️ 一条独立的第三方事实（`TechCrunch` 报道口径）**：中美已就「中美 AI 对话」与「AI 事件双边通报渠道」达成共识 —— "
     "**本报告记为「双方公开口径一致的事实」，不作为对错判断的依据**。"
     "**⚠️ 对读者最实际的两条影响（只写后果、不作判断）**：**① 采购面 —— 被排除出联邦民事机构采购、"
     "且要求从既有 IT 系统中移除（与「被禁售」是两种不同后果：一份是不能再卖，一份是已装的也要拆）；"
     "② 第三方面 —— 用了 `DeepSeek` 实现做的第三方产品也在移除范围内，即「我没直接用 `DeepSeek`」不构成豁免**。"
     "**⚠️ 一条如实记的未核项**：**命令全文未给出移除的完成期限**（避坑 142：**每个日期都要问它是哪一种；没有日期就是没有日期**）。"),
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
# ⚠️ data/ 下是 CRLF
open(F, "w", encoding="utf-8", newline="\r\n").write(md)

n1 = len([l for l in open(F, encoding="utf-8", newline="").read().split("\n") if l.startswith("| ")])
print("frozen_items data rows: %d -> %d (+%d)" % (n0, n1, n1 - n0))

from collections import Counter
rows = [l for l in open(F, encoding="utf-8", newline="").read().split("\n") if l.startswith("| ") and "---" not in l]
print("field-count distribution:", Counter(len(l.split("|")) - 2 for l in rows))
