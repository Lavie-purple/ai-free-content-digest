# -*- coding: utf-8 -*-
"""从 042 期 md 提取第四章截止表 -> 基准日 2026-10-21 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table043.md（纯表格块，供 043 期正文嵌入）。

六步（027 期定做法、028 期定型；043 期第十八次落地）：
  1) 先断言行数（042 期 body = 218）
  2) 按行名子串套 REWRITE 字典（每键必须恰好命中 1 次）
  3) 正则重算每一行的「距今 N 天」（基准日 10/21）
  4) 未 REWRITE 的行做归属化（「本期」-> 「042 期」）
  5) 新行插在 ⚪ 存档块（首行 "| ⚪ **DeepSeek 10/15"）之前 -> 再断言总数
  6) 输出后由 inject043.py 注入正文占位符

⚠️ 042 期立的两条脚本纪律本期继续生效：
   ① 断言口径是「每行天数 == 其截止日 − 基准日」，**不是「−1」**（继承误差逐期滚雪球）；
   ② **REWRITE 命中的行不再过 recompute**（否则含多日期的截止列会被取到错误日期并覆盖整行）。
⚠️ 041 期抓到并已修的缺陷本期继续生效：`assert hits == 1` 只能证明「键命中了目标行」，
   不能证明「值被写回去了」-> 替换循环是「逐行找键、命中即换」，且额外断言 `v in out`。
⚠️ 042 期修掉的诊断失效缺陷本期继续生效：**先留 before_snapshot，再覆盖**，否则「逐行 diff」恒为空。
⚠️ **截止列纪律**：真截止日才写可解析 `M/D`；换挡日/登记启动日/权重交付日一律写不可解析形态。
   「限时免费」没有结束日时写「未公布」（避坑 154/166）。
⚠️ **本期核心变化**：
   - **MiniMax M3.1 Flash 的开放权重 = 四个状态**（宣布 → 承诺 → 给日期 → 上传仓库），本期核到停在第 ② 级；
   - **MiniMax-H3 的真实许可已核**（自定义社区许可 + 地域排除美/欧/英/韩 + $20M 营收门槛）；
   - **OpenRouter / OpenCode 侧 M3.1 Flash 免费档的两页一手核验**（均无官方截止日）；
   - **DHS 对 DeepSeek 的联邦采购排除与移除令**（Federal Register 全文已核）。
   - **本期新增 5 行**。
"""
import re
from datetime import date

SRC = "AI免费内容与权益速递-第042期-2026-10-20.md"
OUT = ".workbuddy/tmp_table043.md"
BASE = date(2026, 10, 21)
PREV = 218

lines = open(SRC, encoding="utf-8").read().split("\n")
s = e = None
for i, l in enumerate(lines):
    if l.startswith("## 四、"):
        s = i
    if s is not None and l.startswith("## 五、"):
        e = i
        break
rows = [l for l in lines[s:e] if l.startswith("|")]
# ⚠️ **043 期修正**：第四章脚注里有一张「口径 | 分布」小表，它同样以 "|" 开头，
#    若不排除会被当成表体行 —— 042 期生成的 218 行里含 4 行脚注行，本期必须同样剔除。
_foot = None
for _i, _l in enumerate(rows):
    if _l.startswith("| 口径 | 分布"):
        _foot = _i
        break
assert _foot is not None, "未找到第四章脚注的口径小表起点"
header, sep, body = rows[0], rows[1], rows[2:_foot]
assert len(body) == PREV, (len(body), PREV)

NEW = [
    # ---- 新行 1：DeepSeek 全面开源内部推理框架 DeepInfer（发布线 · 本报告第一次登记「框架开源」）----
    "| 🟢 **`DeepSeek` 全面开源内部推理框架 `DeepInfer` + `deepseek-recipe`（10/20 · **本报告第一次登记「框架开源」这个条目类型**）** | "
    "无结束日（**开源代码，不改变官方 API 计费**） | 🟢 **生效中（10/20 官方公众号已发布；回扫节点为后续版本迭代）**。"
    "**官方一手（公众号 `DeepSeek`，10/20 16:54 北京；本轮经中新经纬、澎湃、中国基金报、证券时报、腾讯新闻五家转述核到同一段原文）**："
    "**开源了什么** —— 内部推理框架 `DeepInfer` 全面开源，**并同步开源生产级 Token 编解码组件 `deepseek-recipe`**，"
    "后者「与 `DeepSeek` 官方 API 处理逻辑完整对齐，确保社区获得与官方部署一致的 API 体验」；"
    "**能力（官方逐字）**：「集成高性能算子和深度优化的推理引擎，支持**分布式推理、推测解码、SWA Bounded Replay、结构化输出**等能力，"
    "可在**英伟达与华为昇腾平台**上运行」；**官方给的量化数字**：「单一集群的服务吞吐是 `155 万亿 Tokens/天`，"
    "整体收入是每卡每小时 `38` 美金（按谷价）」。"
    "**⚠️ 本报告自算的两个数（只做算术、不做判断）**：单卡 24 小时满负荷 = `38 × 24 = 912` 美元/天 ≈ 人民币 `6,090.48` 元/天；"
    "30 天 ≈ 人民币 `18.27` 万元/卡/月。**⚠️ 这两个数对读者是双向的**："
    "**① 正向 —— 它把「自建推理 vs 调 API」第一次量化了，但「自建一定更省」这个结论本报告不下** "
    "（**未算电费、折旧、机房、人力、故障率，也未算峰值容量与闲时浪费**，避坑 165：厂商自报的经营数字只作量级参考）；"
    "**② 反向 —— 它同时把厂商的成本结构公开了**。"
    "**⚠️ 腾讯新闻那篇转述里有一句推论（「大规模云厂商部署非原生 `DeepSeek` 的调用成本甚至存在低于官方原生的可能性」）—— "
    "本报告明确标注为转述方推论、不是官方口径，也不写成结论**（避坑 116）。"
    "**⚠️ 一条最容易当成「免费」但不是的区分**：本条开源的是**代码**，**不改变 `DeepSeek` 官方 API 的任何计费** —— "
    "本表 `DeepSeek Search`/`Fetch` 的「11/1 00:00（北京）起按请求计费」与 `V4.1-Flash-1017` 的谷/峰价全部维持**（避坑 154）。"
    "**⚠️ 本条的类别定位（本期新记）**：**本报告至此登记过的开源条目全是「模型权重」；本条是第一次登记「框架」** —— "
    "**二者的可用性判据完全不同：权重开源的判据是「能不能下载、许可是什么」；框架开源的判据是「能不能跑起来、依赖什么硬件、支持哪些平台」**。"
    "**本条的关键字段是「英伟达 + 华为昇腾双平台」**（避坑 41 第二层：能否跑起来） |",

    # ---- 新行 2：OpenRouter 侧 M3.1 Flash 免费档（无官方截止日）----
    "| 🟢 **`OpenRouter` 的 `MiniMax M3.1 Flash (free)` 免费档（10/19 上线 · **官方模型页无任何截止日**）** | "
    "**未公布**（**官方模型页只给 `Price: Free`，无 `limited time` / `until` / `expires` / 地区限制 / 充值要求**） | "
    "🟢 **生效中（自 10/19 上线至今仍在 `Free` 状态；官方未给结束时点）**。"
    "**官方一手（`openrouter.ai/minimax/minimax-m3.1-flash:free`，本轮实访）逐字字段**：「`Modalities` `Price` **Free** `Context` **1.0M** "
    "`Released` **Oct 19, 2026**」；Providers 表「`MiniMax` — 输入 **Free**、输出 **Free**、`1.66s`、`75 tps`、`100.00%`」；"
    "模型描述末尾「**Open weights are planned.**」。"
    "**⚠️ 聚合站口径与一手源冲突**：聚合站称「`OpenRouter` 于北京时间 `10/19 20:01` 宣布免费 `72` 小时、约至 `10/22 20:01`、"
    "之后价格为 `$0.15 / $0.60 / $0.015`」—— **本轮实访 `openrouter.ai/announcements`（该 URL 实为 Blog 列表页）最新一篇为 "
    "`October 14, 2026`，按猜测 slug 实访 `openrouter.ai/blog/announcements/minimax-m3-1-flash-free` 返回 `404 —— Page Not Found`**，"
    "**即「官方公告」这一处本轮不存在，故 72 小时与截止钟点本报告不采信为官方口径**（避坑 191）。"
    "**⚠️ 本期抓到一个极高危误读点**：**该模型页上确实出现「`3 days`」三个字，但它不是免费期** —— "
    "原文是「`Uptime is the percentage of the past 3 days that at least one provider was responding to requests.`」"
    "与「`Availability over the last 3 days — Oct 17, 9 PM - Oct 20, 9 PM`」，**即 uptime 统计窗口**。"
    "**把 uptime 窗口读成「限免 3 天」是凭空造出一个截止日**（避坑 116 同族的新形态）。"
    "**⚠️ 同一站的免费档限速官方口径（本轮首次核到）**：`openrouter.ai/docs/faq` 逐字「`For free models, rate limits are determined by "
    "the credits that you have purchased. If you have purchased at least 10 credits, your free model rate limit will be 1000 requests per day. "
    "Otherwise, you will be rate limited to 50 free model API requests per day.`」—— **与 `freellm.net` 的 `200 req/day` 口径冲突，两说并列**（避坑 161）。"
    "**⚠️ 本轮实测面板（`OpenRouter` 自己观测的第三方托管实例，非厂商自报）**：`P50` 延迟 `1.66s`、`P50` 吞吐 `75 tok/s`、"
    "**工具调用错误率 `Avg 4.30 %`**、缓存命中率 `Avg 90.49 %`、`Uptime(3d)` `99.99%`、`Availability(3d)` `99.79%`；"
    "**⚠️ 其中「工具调用错误率 4.30%」是官方资料里完全看不到、而对做 agent 编排最要紧的一个量级** |",

    # ---- 新行 3：OpenCode 侧 M3.1 Flash Free（limited time 无钟点）----
    "| 🟢 **`OpenCode` 的 `MiniMax M3.1 Flash Free`（`limited time` · **两页均未给截止钟点**）** | "
    "**未公布**（**两页均只标 `limited time`，全页无 `3 days` / `72 hours` / 任何钟点**） | "
    "🟢 **生效中（免费档当前仍在架；结束时点官方未给）**。"
    "**本轮实访两页，逐字分列（不合并）**：**`opencode.ai/docs/go`（订阅页）** —— 模型行「`MiniMax M3.1 Flash Free (limited time)`」、"
    "价格行「`Free` `Free` `Free` — **`Unlimited`**　`limited time`」、表下说明「`MiniMax M3.1 Flash Free:` **Free for a limited time.**」、"
    "Model ID `minimax-m3.1-flash-free`、Endpoint `https://opencode.ai/inference/go/openai/v1/chat/completions`、"
    "请求量估算行「**Unlimited** `Unlimited` `Unlimited`」（per 5 hours / week / month）、同页 Go `$10/month` 与 Go Plus `$40/month`；"
    "**`opencode.ai/docs/zen`（按量付费页）** —— 模型行「`MiniMax M3.1 Flash Free`」、价格行「`Free` `Free` `Free` `Free`」"
    "（Input / Output / Cached Read / Cached Write）、"
    "「**`MiniMax M3.1 Flash Free` is free on OpenCode for a limited time. Its provider follows a **zero-retention policy** and "
    "**does not use your data for model training**.**」、Endpoint `https://opencode.ai/inference/openai/v1/chat/completions`、"
    "同页唯一的 `MiniMax` 付费档是 `MiniMax M3 $0.30 / $1.20 / $0.06`（**没有 `M3.1 Flash` 的付费档**）。"
    "**⚠️ 三条可断言的结论**：**① 截止钟点官方未给 —— 聚合站那条「免费 3 天 / 10/19 20:17 公告」在一手源未核到**（避坑 191）；"
    "**② 留存口径落第一档（零留存 + 不训练），且该页未对 `MiniMax` 标 30 天留存**（040 期记的 30 天档是 `Beam Free` / `LL Alpha Free` / "
    "`OpenAI APIs` / `Anthropic APIs`，不是 `MiniMax`）（避坑 173）；"
    "**③ 两页均未对本条标 `limited regions` —— 同页 `Beam Free` 标了且含中国大陆，即「别的条目有」≠「这条也有」，"
    "但「页面没写」仍不等于「没有限制」**（避坑 181 及其反向）。"
    "**⚠️ 039 期记的「`docs/zen` 与 `docs/go` 两页对同模型给出相反答案」本轮未复现** —— **但这只是本轮观察、不是冲突已消解**（避坑 180）；"
    "**两页仍有一处结构性差异：endpoint 不同、计费体系不同、只有 `docs/go` 给「Unlimited」的请求量估算**。"
    "**⚠️ 一条本报告第一次记的免费档形态**：「`Unlimited`」是**聚合平台自己给的估算**，不是上游厂商承诺（避坑 116） |",

    # ---- 新行 4：MiniMax M3.1 Flash 开放权重（四个状态，本期停在第 ② 级）----
    "| ⚠️ **`MiniMax` `M3.1 Flash` 开放权重（10/19 宣布 · **本期核到「四个状态」停在第 ② 级**）** | "
    "**官方未公布**（**官方博客逐字只写 `will be released later.`；媒体口径的「10 月 23 日」只出自官方 X 与第三方，"
    "官方博客与文档站均无此日期** —— **非活动截止，是权重交付的传闻日**） | "
    "⚠️ **未到可下载状态**（**第 ① 级已到（API 可调）、第 ② 级已到（官方文档站标 `open-weight`）、第 ③ 级官方未给日期、第 ④ 级未到（HF 上无仓库）**）。"
    "**⚠️ 043 期新立避坑 188 的四状态判据（逐级核、缺哪级写哪级）**：**① 宣布了模型（官方 API 可调）② 官方承诺会开权重"
    "（官方文字出现 `open-weight` 或 `weights will be released`）③ 给了具体日期（官方正文出现可解析日期）④ 权重真的在 `HF` 上（组织页存在对应仓库）**。"
    "**本例取值：① ✅ 已上线（`platform.minimax.io` / `.cn`）② ✅ 文档站已在模型表标 `open-weight`、博客已说 `later` "
    "③ ⚠️ 仅官方 X 与第三方（`RITS` 逐字「`The reported October 23 date is a plan, not a checkpoint.`」）④ ❌ `HF` `MiniMaxAI` 组织页无任何 `M3.1` 仓库**。"
    "**⚠️ 本轮实访 `HF` `MiniMaxAI` 组织页**：20 个仓库逐个核过（`MiniMax-H3`、`MiniMax-Music3`、`MiniMax-M3`、`MiniMax-M3-MXFP8`、"
    "`MiniMax-M2`/`M2.1`/`M2.5`/`M2.7`、`VTP-Small`/`Base`/`Large`、`Text-01`、`Text-01-hf`、`VL-01`、`M1-40k`/`M1-80k`/`M1-40k-hf`/`M1-80k-hf`、"
    "`SynLogic-32B`/`Mix-3-32B`/`7B`），**`gated` 均为 `false`；即「权重未上传」这一条，一手的 `HF` 组织页是空的**。"
    "**⚠️ 在第 ④ 级之前，一律按「只能用 API、不能下载」规划**（避坑 41 第四层 / 139）。"
    "**⚠️ 参数量与许可证官方均未给，本报告不代为确认**（`428B`/`23B` 只见于第三方，且 `RITS` 注明是借 `M3` 的 model card）（避坑 116） |",

    # ---- 新行 5：MiniCPM-V 4.7 端侧多模态开源（Apache-2.0 · 最宽松一档）----
    "| 🟢 **`MiniCPM-V 4.7` 端侧多模态开源（`OpenBMB` · **Apache-2.0 + 无下载闸门 = 本报告至今最宽松的一档**）** | "
    "无结束日（**开放权重，无活动期**） | 🟢 **生效中（HF 仓库 `lastModified` 2026-10-19 12:52）**。"
    "**本轮实访 `HF` API 一手字段**：**`openbmb/MiniCPM-V-4.7-35B-A3B`** 与 **`openbmb/MiniCPM-V-4.7-1B`** 两个仓库 —— "
    "**`gated: false`、`disabled: false`、`private: false`（即无下载闸门、无需点同意、无人工审核）**、"
    "**`license: apache-2.0`（可商用、可修改、可再分发，仅需保留版权与 NOTICE）**；"
    "**实际参数量 `35,212,875,824`（35.2B）与 `1,554,476,272`（1.55B）**（`safetensors` 统计）、存储 `70.6 GB` / `3.30 GB`、"
    "**下载量 `95,240` 与 `46,506`**、`createdAt` 2026-10-07 / 2026-10-06、`lastModified` 2026-10-19 12:52、"
    "`pipeline_tag` `image-text-to-text`。"
    "**⚠️ 量化格式（一手仓库名 + tags 全清单，共 13 个衍生仓库，全部 Apache-2.0）**：**GGUF**（`-35B-A3B-gguf` / `-1B-gguf` / "
    "`-35B-A3B-DSpark-gguf` / `-1B-DSpark-gguf`）、**GPTQ**、**AWQ**、**int4**、**FP8**、另有 `-DSpark` 推测解码草稿模型。"
    "**⚠️ 一个容易踩的判读点**：**`FP8` 那个仓库的 tags 是 `quantized` + `compressed-tensors`，并没有独立的 `fp8` 标签 —— "
    "「FP8」只出现在仓库名里**。"
    "**⚠️ 两条不能替它确认的字段**：**① 上下文长度 —— `HF` API 与 config 均未给出，第三方说法冲突（`256K` vs 约 `976K`），"
    "本报告两说并列、不取中间值**（避坑 161）；**② 仓库名用点号不是下划线**（`MiniCPM-V-4.7-35B-A3B`）—— "
    "**搜 `MiniCPM-V-4_7` 会 404**。"
    "**⚠️ 本行与同表 `MiniMax-H3` 那条必须一起读**：**同一周被媒体推荐的两个国产模型，许可档位完全相反 —— "
    "本条是 Apache-2.0 且无地域排除，`MiniMax-H3` 是自定义社区许可且把美/欧/英/韩排除在外** —— "
    "**本报告因此新立避坑 189（许可的五层：下载闸门 / 许可类型 / 地域范围 / 商业门槛 / 衍生义务）** |",
]

REWRITE = {}

# ---- ① 老混元：Q04 连续第 31 期 + 高危窗口第 21 天 ----
REWRITE["🔴 **腾讯老混元大模型平台停服**"] = (
    "| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必须迁移到 TokenHub**。**10/21 高危窗口第 21 天**"
    "（9/25 自设倒排日已过 **26 天**；Q04 **连续第 31 期**未见确切日期，厂商只给「9 月底」）。"
    "⚠️ **一条「9 月底停服」拖到 10 月中下旬仍无日期，处置维持「按已停服对待、只做迁移」**——迁移动作本身不要等；"
    "⚠️ **同一家厂商两条线，一条无日期一条有精确到日的倒排**（元器 11/9，见下表），"
    "**说明「无日期」不是这家厂商的常态，而是这条线的常态**（避坑 164） |"
)

# ---- ② DeepSeek Search / Fetch：倒计时推进到 11 天 + DeepInfer 开源不影响计费 ----
REWRITE["`DeepSeek Search` / `Fetch` 两个 API 开放"] = (
    "| 🟡 **`DeepSeek Search` / `Fetch` 两个 API 开放（10/17 · 服务端调用免费到 11/1）** | "
    "**11/1 00:00（北京）起按请求计费** | 🟡 **生效中（免费窗口距今 11 天）**。"
    "**接入（官方逐字）**：base URL `https://api.deepseek.com`；**Search `POST /v1/tools/search`、Fetch `POST /v1/tools/fetch`**；"
    "**两者均为原始 JSON API、使用与 `DeepSeek API` 相同的 bearer 认证**。"
    "**计费（官方逐字）**：**Search 与 Fetch 均按「每 1,000 次成功请求 `$0.75`」计价 —— 按请求计费，不按 token、也不按返回结果条数**；"
    "**只有 HTTP 200 且产生结果才算成功**（Search 须返回非空 `results`、Fetch 须返回页面内容）；"
    "**失败请求、空搜索结果、超时一律不计费**。⚠️ **「空结果不收费」对做 RAG 的读者有直接后果 —— "
    "一次检索没命中是零成本、命中才计费，与按 token 计费是相反的成本结构**（避坑 176）。"
    "**⚠️ 免费窗口（官方附注逐字）**：**「when you use the `DeepSeek API` through `DeepSeek Harness`, `Claude Code`, or `Codex`, "
    "server-side tool calls already hit the Search and Fetch APIs. These calls are currently free of charge; "
    "per-request billing starts at **00:00 Beijing time on November 1, 2026**」** —— "
    "**必须拆三行读**：**① 直接调 API 从一开始就是 `$0.75` / 1,000 次成功请求，没有免费期；"
    "② 三个 harness 的服务端工具调用目前免费；③ 计费起点是北京时间 11/1 00:00，不是美西也不是 UTC**。"
    "**⚠️ 截止时点存在两个口径，两说并列、不取中间值**：**官方文档写「北京时间 2026 年 11 月 1 日 00:00」；"
    "而 `The Decoder` 的报道写「until November 1, 2026 (or **October 31, 2026 at 4:00 PM UTC** per The Decoder)」"
    "—— 两个时点相差 8 小时（北京 11/1 00:00 = UTC 10/31 16:00）。⚠️ **本报告以官方文档为准，同时保留媒体口径并标明来源**（避坑 161）。"
    "**⚠️ 速率限制（042 期已纠错，本期维持）**：官方 `Rate Limits` 表逐字 —— "
    "**`Search` QPS 上限 `100`、`Fetch` QPS 上限 `25`**；**两者各自独立计、互不消耗对方配额**；"
    "**QPS 按账户级计算、与模型并发限制分开**；**`Fetch` 另受按域名的 QPS 限制**；**超限返回 HTTP 429**。"
    "**⚠️ 对内容生成最要紧的三个响应字段**：`rerank_score` **0–3、≥1.5 视为高质量**（唯一可程序化判定的质量档）；"
    "`summary` **600–800 字符、面向模型**（`snippet` 是 100–200 字符、面向 UI，两者不是同一字段的截断版）；"
    "`content` 为页面 Markdown 全文、`need_content=false` 时恒为空字符串、且 `count` 不影响单价。"
    "**⚠️ 一条不能靠重试解决的失败**：`404` 表示无法取到可用页面内容（不可用 / 被站点策略拦截 / 目标站报错 / "
    "不支持的内容类型 / 无可提取 Markdown）—— **索引里有 ≠ 抓得到**。"
    "**⚠️ （043 期）回扫**：`api-docs.deepseek.com/updates` **本轮实访确认 10/21 无新条目** —— "
    "**连续第 4 期无新条目**；**且 043 期 `DeepSeek` 全面开源 `DeepInfer` 与 `deepseek-recipe`（10/20）不改变本行任何计费字段** —— "
    "**开源框架 ≠ API 免费或降价**（避坑 154） |"
)

# ---- ③ WorkBuddy Intl 限免：倒计时推进到 10 天 ----
REWRITE["`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免"] = (
    "| 🟢 **`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免（10/31）** | **10/31** | 🟢 **生效中（距今 10 天）**。"
    "**官方原文两句（`WorkBuddy` 官方 X，10/17 18:29）**：「新的 `DeepSeek` 刚刚发布。`WorkBuddy Intl` 也已更新到最新版本，"
    "**并且在 10 月 31 日前免费**。来试试看吧。」⚠️ **四条登记纪律**："
    "**① 主体是 `WorkBuddy Intl`（国际版），不是国内版 —— 本工作区的产品线在国内站与国际站是两套口径，不可互相代入**；"
    "**② 官方原文没有写额度上限、没有写适用账号范围、没有写结束后的价格** —— "
    "**即这三条字段全部缺失，只能按「有限时免费、无从判断能用多少」来规划**（避坑 41 第一层）；"
    "**③ 限免的标的是「已更新到最新版本」这件事，而不是某个模型名 —— 即换新版本后是否仍免费，官方原文没有回答**（避坑 166）；"
    "**④ 本行是「工作区自有产品公告」，与厂商公告分开放，避免被当成厂商口径**（避坑 126）。"
    "**⚠️ （043 期）回扫**：本轮未见续期或提前收口的公告，按避坑 78「无信号即默认维持」处理。"
    "⚠️ **与本表另两行「`WorkBuddy` 国内版」条目是三个不同主体的三笔账**（教育公益版 / DeepSeek 故障补偿 / 国际版限免），"
    "**互不代入**（避坑 126） |"
)

# ---- ④ AutoClaw 国际版：连续第 3 次未被改回 + 今天跨过档位分界 ----
REWRITE["智谱 `AutoClaw` 第三期每日登录送 Token"] = (
    "| 🟢 **智谱 `AutoClaw` 第三期每日登录送 Token（**国际站 `z.ai` · 10/19–10/25**）** | "
    "**10/25（活动期末日）** | 🟢 **生效中（活动期末日距今 4 天 · **⚠️ 每档当天 24:00（北京）即过期，见下**）**。"
    "**官方页实测（`autoclaw.z.ai/blog/news/M10W3`，读于 2026-10-21，本轮连续第 3 次实访）**：`Event Period: Oct 19 – Oct 25 (UTC+8)`；"
    "**`Oct 19-20 (Monday–Tuesday)` 每天领 `3,000 credits (30M tokens)`；"
    "**`Oct 21–25 (Wednesday–Sunday)` 每天领 `500 credits (5M tokens)`**；**每档 `Expires at 24:00 (UTC+8) the same day`。**"
    "**换算**：`1 credit = 1 万 tokens`；**总量 85M = 30M×2 + 5M×5**。"
    "**⚠️ 本行是本报告第一次登记的条目类型「同 URL 内容被官方就地改写」**："
    "**同一个 URL、发布日期未变、活动期 Oct 19–25 未变，但正文规则与标题总量都变了** —— "
    "**10/16 发布版是 `Get 60M Tokens`（`Oct 19` 单日 3000 万、`Oct 20–25` 每天 500 万）；"
    "本轮连续第 3 次实访仍为 `Get 85M Tokens`（`Oct 19–20` 每天 3000 万、`Oct 21–25` 每天 500 万）—— 即未被改回**。"
    "**⚠️ （043 期）今天正好跨过档位分界 —— 042 期那个「少领 2,500 万」的结论今天自动失效**："
    "**今天（10/21）是 `Oct 21–25` 那一档的第一天，即从今天起每天只能领 `500 credits (5M tokens)`，"
    "而昨天（10/20）仍可领 `3,000 credits (30M)`** —— **即 3000 万档已在 10/20 24:00（北京）过期**。"
    "**⚠️ 但那篇按旧版写的稿子并没有因此变对 —— 它从「全错」变成了「部分对」**："
    "**042 期核到的那篇 10/20 发布的聚合稿写「`Get 60M Tokens`」「今天（10/20）起至 10/25 每天登录领 500 credits」"
    "「整期七天合计 6000 万 tokens」—— 其中「档位」那一项从今天起恰好是对的（今天确实是 500 档），"
    "而「总量」那一项仍然错（现行表是 85M，不是 60M）**。"
    "**⚠️ 这正是 043 期新立避坑 192 的样本**：**错误的转述会随时间从「全错」滑向「部分对」—— 部分对比全错更难识破**，"
    "**读者若发现「有一项对了」就整体采信，恰恰会错在总量那一项**（避坑 192）。"
    "**⚠️ 为什么难发现**：**新旧两版各自自洽** —— `30M + 5M×6 = 60M` 与 `30M×2 + 5M×5 = 85M` 都对得上自己的规则表，"
    "**验算能排除「笔误」，排除不了「过期」**（避坑 179）。"
    "**⚠️ 领取资格（国际站官方页口径）**：**登录即领、不分新老用户、无邀请奖励；官方页只列一档**。"
    "⚠️ **中文媒体广泛转述的「付费会员另有额外每日奖励」在国际站这一档的官方页上没有** —— "
    "**但国内站那一档有（每日 800 积分），见下两行 —— 即「会员加赠没有」这句话只对国际站成立**（避坑 163 的多站点面）。"
    "**⚠️ 「当天清零」型不可当存款**：**领了当天 24:00（北京）就过期、错过不补** —— "
    "**与 9/28、9/30 两期「开放平台新用户礼包、领了能放一阵」不是同一件事**（避坑 117 同族）；"
    "**官方页未写各模型扣多少 credits，本报告不代官方换算**（避坑 41 第一层）。"
    "**⚠️ 与上一档是无缝接档、但不可比大小**：**上一档（`Weekly-Perks-M10W2`，10/12–10/16）132M、这一档 85M，"
    "且 10/17–10/18 两天无活动**（避坑 140 第一层：**「无缝续期」≠「同一活动」，额度量纲变了不可直接比**）。"
    "**⚠️ 官方页未写各档对应的可用模型范围**，本报告不代官方换算 |"
)

# ---- ⑤ AutoClaw 国内站 2 亿：今天是最后一天（10/21 截止） ----
REWRITE["`AutoClaw` 桌面端 v2.1.0 一次性 2 亿 Tokens"] = (
    "| 🟡 **`AutoClaw` 桌面端 v2.1.0 一次性 2 亿 Tokens（国内站 `zhipuai.cn` · **本期已核到一手页**）** | **10/21** | "
    "🟡 **生效中（**今天 10/21 就是「可领窗口的末日」** · 距今 0 天）**。"
    "**一手页（`autoclaw.zhipuai.cn/blog/news/Weekly-Perks-M10W3/`，发布日 2026-10-14，本轮逐字核到）**："
    "**官方把两档活动写在同一张表里**：**① 一次性大额（`10.15–10.21 周四至下周三`）**：「活动期间任意一天登录 AutoClaw，"
    "即可领取 2 亿 Tokens（20,000 积分）」、**「每个账号限领一次。领取成功后 7 天内有效，逾期自动失效」**；"
    "**② 每日登录（`10.15–10.25 周四至下周日`）**：「活动期间每日登录 AutoClaw，**普通用户每日可领取 500 积分，"
    "付费会员每日可领取 800 积分**」、「每日限领一次」，**付费会员包括连续包月订阅、AutoClaw 团购订阅及 GLM Coding Plan 个人套餐用户**。"
    "**③ 有效期总则（官方逐字）**：「**所有活动积分自领取成功起 7 天内有效，请及时使用**。」"
    "**⚠️ 国内站与国际站是两套完全不同的活动，五点都不一样**：**① 总量：国内「2 亿一次性 + 每日 500/800 积分」，"
    "国际「85M 每日、总量 85M」；② 有效期：国内「领到起 7 天」，国际「当天 24:00（北京）清零」—— 这两条决定了同一笔额度能不能跨日用**；"
    "**③ 付费会员：国内每日 800 积分（比普通用户多 60%），国际官方页没有会员加赠档；④ 一次性大额：国内有 2 亿档，国际没有；"
    "⑤ 入口：国内站 `autoclaw.zhipuai.cn`、国际站 `autoclaw.z.ai`，两边各自发活动、规则不一样**（避坑 163 的多站点面）。"
    "**⚠️ （043 期）今天是最关键的一天**：**今天 10/21 是「可领窗口的末日」—— 过了今天就不能再领那 2 亿**；"
    "**而「领到手的有效期」（7 天）是另一个日期 —— 10/15–10/20 领的那几份仍可用到 10/21–10/27 左右**"
    "（避坑 142 第二层：**可领窗口末日 ≠ 领到手的有效期**）。"
    "**⚠️ 每日登录那一档（`10.15–10.25`）不受影响，仍在活动期内**，但**它的量级是每日 500/800 积分（= 500 万 / 800 万 tokens）**，"
    "**与一次性 2 亿不是同一量级**（避坑 163：免费的是哪一档、范围有多大，三问都要答） |"
)

# ---- ⑥ OpenCode 地区限制清单：本期未复现两页冲突 ----
REWRITE["`OpenCode` 的地区限制清单"] = (
    "| 🟡 **`OpenCode` 的地区限制清单（`Beam Free` 等 · 本期起读法改变）** | 未公布（**官方页未给完成期限**） | "
    "🟡 **生效中（仍在限制中，官方未给解除时点）**。"
    "**本轮实访 `opencode.ai/docs/go` 与 `opencode.ai/docs/zen` 两页逐条维持 042 期结论**："
    "**`Beam Free` 仍标 `limited regions`、不可用清单为 18 国 + 乌克兰 3 个州，逐字含「`China (including Hong Kong and Macau)``」**；"
    "**同页另两个模型同标 `limited regions`：`Muse Spark 1.3 Contributor`、`Muse Spark 1.2 Contributor`**。"
    "**⚠️ 地区限制挂在免费端点的提供方、不挂在权重上 —— `Beam` 权重 Apache 2.0、HF 无 gated，受限地区仍可下载自部署**（避坑 171）。"
    "**⚠️ （043 期）本轮核到「同页不同条目的限制不可互推」这一层**：**`MiniMax M3.1 Flash Free` 在两页均**未**标 "
    "`limited regions` —— 而同页的 `Beam Free` 标了。**即「别的条目有」≠「这条也有」**（避坑 181 的反向）。"
    "⚠️ **但「页面没写」仍然不等于「没有限制」** —— **本报告只写「官方页未标注」，不写「该模型在中国大陆可用」** |"
)

# ---- ⑦ OpenCode 留存分档：本期新增 M3.1 Flash 落第一档 ----
REWRITE["**OpenCode 三个免费模型的留存口径分三档（040 期首次成条登记）**"] = (
    "| 🟡 **`OpenCode` 三个免费模型的留存口径分三档（040 期首次成条登记）** | 未公布（**留存协议按月续签**） | "
    "🟡 **生效中（协议按月续签，续签节点不固定公示）**。"
    "**`OpenCode` 同页 15 个免费模型的留存口径至少分三档**：**① 零留存+不训练**（`GLM-5.3-Flash Free`/`DeepSeek V4.1 Flash Free`/"
    "`LongCat 2.5 Preview Free`/`Space Bunny Free`）；**② 不训练但留存 30 天**（`Beam Free`、`LL Alpha Free`）；"
    "**③ 免费期数据可能用于改进模型**（`Big Pickle`/`Exo Free`/`MiMo-V2.6-Flash Free`/`MiMo-V2.5 Free`）。"
    "**另有 `Muse Spark 1.3 Contributor Free` 以训练许可换免费价、`Nemotron` 三个端点带「Trial use only — do not submit personal or confidential data」硬警告**。"
    "**⚠️ 038 期把同平台 `GLM-5.3-Flash` 的零留存口径外推到了 `Beam`（实际 30 天）**（避坑 173）。"
    "**⚠️ （043 期）本轮新增一条落到第一档的模型**：**`MiniMax M3.1 Flash Free`** —— "
    "**`opencode.ai/docs/zen` 逐字「`MiniMax M3.1 Flash Free` is free on OpenCode for a limited time. "
    "Its provider follows a **zero-retention policy** and **does not use your data for model training**.`」**；"
    "**且该页未对 `MiniMax` 标 30 天留存**（040 期记的 30 天档是 `Beam Free` / `LL Alpha Free` / `OpenAI APIs` / `Anthropic APIs`，"
    "**不是 `MiniMax`**）。**即 043 期读到的第一档模型是 5 个，比 042 期多一个**。"
    "**⚠️ 但同一行还挂着「`limited time`」而**全页无任何天数或截止钟点** —— "
    "**「零留存」是可以说清的，「免费到什么时候」是说不清的**（避坑 191） |"
)

# ---- ⑧ OpenCode 安全事件处置状态：本期补 Anthropic 10/12 公告的时间线对读 ----
REWRITE["`OpenCode` 安全事件处置状态"] = (
    "| 🟡 **`OpenCode` 安全事件处置状态（10/17 起 · 040 期头条，本期状态推进）** | 未公布（**官方明确「事件仍在处置中」、无修复完成时点**） | "
    "🟡 **生效中（仍在处置中，官方不给完成时点）**。"
    "**041–042 期已登记的口径全部维持**：**攻击面 = 一套「正在停用的旧系统」遭未授权访问**，"
    "**存放在用户工作区的第三方 AI 服务 API 密钥可能泄露（含 `OpenAI`、`Anthropic`）**；"
    "**官方明确「目前尚无法确认相关密钥是否遭到恶意使用，初步调查也未发现其他数据泄露的证据」**（阴性结果，非清白证明，避坑 138 同族）；"
    "**退款口径按主体分四家（避坑 184）**：`OpenAI` **承诺**退款、`OpenCode` 退款**正在进行 / 已启动补偿流程**、"
    "`Anthropic` 与 `Google` **封禁**密钥且**本轮未核到其退款承诺**；"
    "**「1.4%」的分母口径官方仍未给出**。"
    "**⚠️ （043 期）本轮补一条时间线对读的结果（两说并列、不裁决）**："
    "**`Anthropic` 于 10/12 发布反蒸馏公告（`anthropic.com/research/distillation-defenses`），逐字「`Early evidence suggests that these methods "
    "have reduced the amount of data harvested by distillers by around 90 to 99%.`」** —— "
    "**① 公告在攻击（10/16–17 夜）之前约 4–5 天；② 其分类器覆盖的是 `Anthropic` 自家 API 的五个模型"
    "（`Sonnet 5.5`/`Opus 5` 与 `5.5`/`Fable 5` 与 `5.1`），而本事件泄露的是存放在 `OpenCode Console` 的**第三方**密钥 —— "
    "**双方原文都没说这两个防护面是否重合；③ 官方自己写「`We don't yet know how long these gains will last.`」**。"
    "**⚠️ 另记一条归因本身的第三方质疑**：`TechCrunch` 明确记录「`Some skeptics called the framing an overstretch, arguing that the incident "
    "was a straightforward breach whose use for distillation remains unproven`」，且 `OpenCode`「`didn't specify how the distillation attack occurred`」"
    "—— **即「这是蒸馏攻击」是 `OpenCode` 的定性，不是已证实的事实**（避坑 116 / 132）。"
    "**⚠️ 本行不写「防护失效」也不写「防护有效」**（避坑 190） |"
)

# ---- 归属化：未 REWRITE 的行把「本期」改为「042 期」 ----
out = []
for l in body:
    new = None
    for k, v in REWRITE.items():
        if k in l:
            new = v
            break
    if new is not None:
        out.append(new)
        continue
    out.append(l.replace("**本期", "**042 期").replace("（本期", "（042 期"))

rw = 0
for k, v in REWRITE.items():
    # ⚠️ **042 期修正**：hits 必须在 **源表 body** 上数，值必须在 **out** 里出现 —— 两件事分开断言。
    src_hits = sum(1 for l in body if k in l)
    assert src_hits == 1, ("键在源表中命中数不为 1", k, src_hits)
    out_hits = sum(1 for l in out if v in l)
    assert out_hits == 1, ("REWRITE 的值未出现在输出里 / 出现多次 —— 替换步骤缺失或键重叠", k, out_hits)
    rw += 1

DAYS_RE = re.compile(r"(?:\*\*)?距今 (-?\d+) 天(?:\*\*)?")
DATE_FULL = re.compile(r"\*\*(\d{4})-(\d{1,2})-(\d{1,2})\*\*")
DATE_MD = re.compile(r"\*\*(\d{1,2})/(\d{1,2})\*\*")

def parse_cut(l):
    cols = l.split("|")
    target = cols[2] if len(cols) > 3 else ""
    if "北京" in target or "未公布" in target or "以" in target or "无结束日" in target:
        return None
    m = DATE_FULL.search(target)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m2 = DATE_MD.search(target)
    if not m2:
        return None
    return date(2026, int(m2.group(1)), int(m2.group(2)))

def recompute(l):
    if "距今" not in l:
        return l
    d = parse_cut(l)
    if d is None:
        return l
    return DAYS_RE.sub("**距今 %d 天**" % (d - BASE).days, l)

# ⚠️ **REWRITE 的行一律不再过 recompute**
bad = []
# ⚠️ **先留 before 快照**（042 期修掉的诊断失效缺陷本期继续生效）
before_snapshot = list(out)
out = [recompute(l) if l not in REWRITE.values() else l for l in out]

diff = []
for before, after in zip(before_snapshot, out):
    m = DAYS_RE.search(before)
    if not m or before in REWRITE.values():
        continue
    d = parse_cut(before)
    if d is None:
        continue
    truth = (d - BASE).days
    if int(m.group(1)) != truth:
        diff.append((after.split("|")[1][:46].strip(), m.group(1), truth))

for l in out:
    m = DAYS_RE.search(l)
    if not m or l in REWRITE.values():
        continue
    d = parse_cut(l)
    if d is None:
        continue
    truth = (d - BASE).days
    if int(m.group(1)) != truth:
        bad.append((m.group(1), truth, l.split("|")[1][:40]))

print("recomputed rows with 距今:", len([l for l in out if DAYS_RE.search(l)]))
print("before -> after diff (行名 / 旧值 -> 真值), 共 %d 行:" % len(diff))
for name, a, b in diff:
    print("   %-46s %s -> %s" % (name, a, b))
assert not bad, ("重算结果不等于按截止列算出的真值", bad)

# ---- 插入新行：插在 ⚪ 存档块之前 ----
anchor_idx = None
for i, l in enumerate(out):
    if l.startswith("| ⚪ **DeepSeek 10/15"):
        anchor_idx = i
        break
assert anchor_idx is not None, "未找到 ⚪ 存档块锚点"
out = out[:anchor_idx] + NEW + out[anchor_idx:]

assert len(out) == PREV + len(NEW), (len(out), PREV + len(NEW))

from collections import Counter
print("field-count distribution:", Counter(len(l.split("|")) - 2 for l in out))

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(header + "\n" + sep + "\n")
    f.write("\n".join(out) + "\n")

print("rows: %d (%d + %d new) / rewrites: %d" % (len(out), PREV, len(NEW), rw))
