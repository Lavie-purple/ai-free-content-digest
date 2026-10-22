# -*- coding: utf-8 -*-
"""从 043 期 md 提取第四章截止表 -> 基准日 2026-10-22 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table044.md（纯表格块，供 044 期正文嵌入）。

沿用 043 期范式（027 期定做法、028 期定型），本期为第二十次落地：
  1) 先断言行数（043 期 body = 223）
  2) 按行名子串套 REWRITE 字典（每键必须恰好命中 1 次）
  3) 正则重算每一行的「距今 N 天」（基准日 10/22）
  4) 未 REWRITE 的行做归属化（「本期」-> 「043 期」）
  5) 新行插在 ⚪ 存档块之前 -> 再断言总数
  6) 输出后由 inject044.py 注入正文占位符

⚠️ **043 期起脚注小表已改为列表形式，源表不再有「| 口径 | 分布」行** ——
   但本脚本仍保留该截断逻辑（存在即截断、不存在则跳过），避免将来脚注再改回表格时静默出错。
⚠️ **REWRITE 命中的行不再过 recompute**（含多日期的截止列会被取到错误日期）。
⚠️ **先留 before_snapshot 再覆盖**（042 期修掉的诊断失效缺陷本期继续生效）。
⚠️ **本期核心变化**：
   - **OpenAI 10/21 一口气发 7 条公告**（`openai.com/news/` 实访确认），其中两条带免费/补贴语义：
     `Patch the Planet`（`github.com/openai/php2shell-checker` 免费分享 + `$1 billion` 补贴 Daybreak + Codex for OSS 订阅）
     与 `OpenAI models are coming to Google Cloud`（Model Garden 走 Marketplace，可用 GCP commitments 抵扣，**无免费层**）；
   - **Anthropic `Claude Duet` 研究预览**（`claude.com/resources/articles/claude-duet`，10/21）——
     **含在 Pro/Max 套餐内、用同一份额度、美国 Pro/Max 候补名单、官方无免费额度**；
   - **`OpenRouter` 官方 API 目录重取**（468 模型 / 21 零价 / 18 带 `:free`），新增 `recursive/flint-v1.0:free`；
   - **`MiniMax` `M3.1 Flash` 开放权重仍停在第 ② 级**（`HF` `MiniMaxAI` 组织页本轮 21 个仓库，无任何 `M3.1`）；
   - **`vLLM` 开源 `Humming`**（Apache-2.0，量化推理 JIT GEMM 内核库）与 `openai/php2shell-checker`（Apache-2.0）；
   - **本期新增 6 行**。
"""
import re
from datetime import date

SRC = "AI免费内容与权益速递-第043期-2026-10-21.md"
OUT = ".workbuddy/tmp_table044.md"
BASE = date(2026, 10, 22)
PREV = 223

lines = open(SRC, encoding="utf-8").read().split("\n")
s = e = None
for i, l in enumerate(lines):
    if l.startswith("## 四、"):
        s = i
    if s is not None and l.startswith("## 五、"):
        e = i
        break
rows = [l for l in lines[s:e] if l.startswith("|")]
# 043 期起脚注改为列表形式，源表无「| 口径 | 分布」行；保留截断逻辑以防将来脚注改回表格
_foot = None
for _i, _l in enumerate(rows):
    if _l.startswith("| 口径 | 分布"):
        _foot = _i
        break
header, sep = rows[0], rows[1]
body = rows[2:_foot] if _foot is not None else rows[2:]
assert len(body) == PREV, (len(body), PREV)

NEW = [
    # ---- 新行 1：OpenAI Patch the Planet 的免费 PHP 检查 Codex skill ----
    "| 🟢 **`OpenAI` 免费分享 `PHP` 版本检查 Codex skill（`github.com/openai/php2shell-checker` · **Apache-2.0 · 官方措辞是「分享」不是「免费」**）** | "
    "无结束日（**开源代码，不设活动期**） | 🟢 **生效中（仓库 `createdAt` 2026-10-21 00:29 UTC、`pushedAt` 2026-10-21 18:05 UTC）**。"
    "**官方一手（`openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/`，10/21）逐字**："
    "「**We’re sharing a PHP version checker as a Codex skill** to help operators identify potentially vulnerable PHP versions and, "
    "alongside PHP’s and their providers’ guidance, determine which updates apply.」**"
    "**⚠️ 一条必须逐字读出来的口径差别**：**官方写的是 `We’re sharing`（分享），全页没有把这份权益表述为 `free` —— "
    "本报告因此不写「免费」而写「免费分享 / 开源可自取」**（避坑 191 同族：**厂商的动词就是口径**）。"
    "**一手 GitHub API 字段（`api.github.com/repos/openai/php2shell-checker`）**："
    "**`license: apache-2.0`**、`stargazers_count` `411`、`forks_count` `29`、`created_at` `2026-10-21T00:29:12Z`、"
    "`pushed_at` `2026-10-21T18:05:56Z`、`description` 为空。"
    "**⚠️ 三个数字都带口径**：**`411` stars 是读于 2026-10-22 的实时值，且该仓库发布不足 24 小时** —— "
    "**star 数在这种时点只说明「有多少人点了星」，不说明「有多少人在生产里用它」**（避坑 165：厂商/社区自报数字只作量级参考）。"
    "**⚠️ 同一个公告里另有两笔钱，都不是普通开发者能直接领的**："
    "**① `we’ve committed $1 billion in subsidized Daybreak access through Daybreak for Frontline Defenders, focused on organizations "
    "with limited security resources protecting essential services.`** —— **这是给「资源有限的机构」的定向补贴，不是个人开发者额度**；"
    "**② `Our investments include subscriptions for all maintainers through Codex for OSS and direct sponsorship of projects such as the "
    "Rust Foundation`** —— **「给所有维护者的订阅」是维护者身份权益，申请入口在 `trailofbits.com/patch-the-planet/#apply`，不是自助领取**（避坑 182）。"
    "**⚠️ 本条最容易写成「免费领 $10 亿」的错误**：**`$1 billion` 的对象是机构、是补贴后的 `Daybreak access`、且官方未公布任何截止日** —— "
    "**第四章本行的「截止」列写「无结束日」而不是任何日期** |",

    # ---- 新行 2：OpenAI × Google Cloud Model Garden（无免费层）----
    "| ⚠ **⚠️ `OpenAI` 前沿模型上架 `Google Cloud Model Garden`（10/21 · **无免费层**）** | "
    "**未公布（GA 无确切日期，官方只写「未来几周」）** | ⚠ **登记启动日未定（**尚未 GA，官方逐字 `General availability is planned in the coming weeks.`**）**。"
    "**官方一手（`openai.com/index/openai-models-google-cloud/`，日期 `October 21, 2026`）逐字**："
    "「**Google Cloud customers will be able to purchase OpenAI frontier models via model garden, transacted through the Google Cloud Marketplace.**」；"
    "「**Enterprises with Google Cloud spend commitments will be able to draw down their GCP commitments for these purchases.**」；"
    "「**General availability is planned in the coming weeks.**」"
    "**⚠️ 本条登记的三个字段（每个都直接关系到「免费与否」）**："
    "**① 购买路径 = `Model Garden` 选型 → 经 `Google Cloud Marketplace` 交易**（**不是**在 `OpenAI` 官网直接买 —— "
    "**即这条是「换渠道」，不是「降价」**）；**② 结算口径 = 可用既有 `GCP` 消费承诺额抵扣** —— "
    "**这是「同一笔钱换个花法」，不是新增预算，更不是免费额度**；**③ 公告全页没有 `free tier` / 免费额度 / 试用额度 / 价格优惠任何一项** —— "
    "**本报告据此写「无免费层」，不写「有额度」**（避坑 154：上游没给的不替它写）。"
    "**⚠️ 「未来几周」不是一个日期**：**本报告在第四章该行写「未公布」，不替厂商写一个具体日**（避坑 154 / 166）。"
    "**⚠️ 本条对本报告读者的直接含义**：**它是「多一个采购渠道」，不是「多一份免费额度」** —— "
    "**做选型时不要把它当免费档来规划**（避坑 41 第一层） |",

    # ---- 新行 3：Anthropic Claude Duet 研究预览（含在 Pro/Max，无免费额度）----
    "| 🟡 **`Anthropic` `Claude Duet` 研究预览（10/21 · **含在 `Pro`/`Max` 套餐内 · 官方无免费额度**）** | "
    "**未公布（研究预览无结束日；官方未给日期）** | 🟡 **生效中（**研究预览已开，**候补名单制** —— 官方逐字 `A research preview is available by waitlist today, starting with US Pro and Max subscribers.`**）**。"
    "**官方一手（`claude.com/resources/articles/claude-duet`，页面标注 `Date October 21, 2026`）逐字**："
    "「**Today, we’re opening a research preview of Claude Duet, a new app where Claude works as a proactive agent.**」；"
    "「**It’s available as a standalone app on iOS and Android, and on claude.ai.**」；"
    "「**For now, Claude Duet lives in its own app, separate from the main Claude app.**」；"
    "「**For this research preview, Claude Duet is included in Pro and Max plans and uses the same usage limits as the rest of Claude.**」；"
    "「**We’re starting today with Pro and Max users in the US.**」；"
    "「**We designed it around Claude Opus 5.5** and built it to be resourceful and to decide what needs you, what can wait, and when to check with you first.」"
    "**⚠️ 五条必须写清的口径**："
    "**① 「免费」这件事官方一个字都没提 —— 本条不是免费档，是「付费套餐里多一个功能」**（避坑 154）；"
    "**② 团队档 `Team`/`Enterprise` 公告未说明包含、也未说明排除 —— 本报告写「公告未说明」，不写「不支持」**（避坑 161：**未核到 ≠ 不存在**）；"
    "**③ 地区口径是「美国 `Pro`/`Max` 用户」** —— **「能免费用」与「能报名」在此不是一回事**（避坑 181）；"
    "**④ 额度共享且后台检查计入额度** —— 官方逐字「**Its background checks count toward those limits**」，"
    "「**Claude Duet checks your connected accounts every few hours, because checking nonstop would use up your plan’s limits much faster.**」"
    "—— **即「放着不管」也在扣额度**，这是与常规对话最不一样的一条；"
    "**⑤ 模型是 `Opus 5.5`（不是 `Opus 5`）**。"
    "**⚠️ 一条不能从公告推出的结论**：**「`Claude Duet` 是不是 `Pro`/`Max` 之外的人也能用」—— 公告写的是 `waitlist`，"
    "而 waitlist 本身不是「已有资格」的证明**（避坑 182：**「没有申请截止日」≠「可以慢慢来」**） |",

    # ---- 新行 4：OpenRouter 新增 flint-v1.0:free（官方 API 口径重取）----
    "| 🟢 **`OpenRouter` 新增免费档 `recursive/flint-v1.0:free`（10/21 22:46 UTC 上线 · **官方无截止日**）** | "
    "**未公布**（**官方 API 目录与模型页均无 `limited time` / `until` / 地区限制字段**） | "
    "🟢 **生效中（自 2026-10-21 22:46 UTC 起在官方 API 目录内）**。"
    "**官方一手（`openrouter.ai/api/v1/models`，本轮实跑全量 468 个模型）**："
    "**`recursive/flint-v1.0:free` 的 `created` = `1792622765`（= 2026-10-21 22:46 UTC）、`context_length` = `262144`、"
    "`pricing.prompt` = `0`、`pricing.completion` = `0`**。"
    "**权重一手（`huggingface.co/RecursiveSI/flint`，本轮经 API 实访）**："
    "**`license: apache-2.0`、`gated: false`、`createdAt` `2026-10-21T14:20:58Z`、`lastModified` `2026-10-21T14:24:03Z`、"
    "`downloads` `0`、tags 含 `license:apache-2.0`**。"
    "**⚠️ 三个必须写清的量**："
    "**① `downloads: 0` 不是「没有人在用」，而是「仓库创建不足一天，下载计数还没起来」** —— "
    "**读一个刚发布的仓库的下载数当成熟度指标是错的**（避坑 165）；"
    "**② 同一批还有 `int4` / `int4-gguf` / `nvfp4-gguf` 三个衍生仓库**（043 期已核），**即量化版本与主仓库同时在架**；"
    "**③ 这是本报告第一次把「`OpenRouter` 官方 API 目录」当作一手目录来用** —— "
    "**此前 040–043 期引用的 `freellm.net` 转录数字与官方目录并不一致，本期把两套口径并列、不取其一**（避坑 161）。"
    "**⚠️ 本行的「截止」列写「未公布」**：**官方 API 目录对免费档不带任何时间字段**（避坑 191：**不替厂商写截止日**） |",

    # ---- 新行 5：vLLM Humming 开源（框架开源，Apache-2.0）----
    "| 🟢 **`vLLM` 开源 `Humming`（量化推理 JIT GEMM 内核库 · **Apache-2.0 · 本报告登记为「框架开源」**）** | "
    "无结束日（**开源代码，不设活动期**） | 🟢 **生效中（`pushedAt` 2026-10-21 05:54 UTC）**。"
    "**官方一手（`api.github.com/repos/vllm-project/humming`）**：**`license: apache-2.0`**、"
    "`stargazers_count` `284`、`forks_count` `58`、`created_at` `2026-02-11T10:55:17Z`、`pushed_at` `2026-10-21T05:54:07Z`、"
    "`description` 逐字「`Humming is a high-performance, lightweight, and highly flexible JIT (Just-In-Time) compiled GEMM kernel library "
    "specifically designed for quantized inference.`」。"
    "**README 一手要点（`raw.githubusercontent.com/vllm-project/humming/main/README.md`）逐字**："
    "「**Supports inference for any weight type under 8-bit across FP16 / BF16 / FP8 / FP4 / INT8 / INT4 activations**」；"
    "「**supports all NVIDIA GPUs from SM75+ (Turing architecture) and beyond**」；"
    "「**Requires only PyTorch and NVCC**」；「**The package size is only 100+KB**」；"
    "「Supports both **Dense GEMM** and **MoE GEMM**」；安装 `pip install humming-kernels`。"
    "**⚠️ 三个必须写清的可用性字段（避坑 41 第二层「能跑吗」）**："
    "**① 硬件门槛 = `SM75+`（Turing 架构起）** —— **这意味着 `V100`(SM70) 及更早的卡不在支持范围内**，"
    "**而 `V100` 至今仍是推理部署的存量主力之一，这个门槛对读者是硬约束**；"
    "**② 依赖只有 `PyTorch` + `NVCC`、包体 `100+KB`** —— **即「没有额外运行时依赖」是它相对其他内核库最实在的优势**；"
    "**③ 它是内核库、不是完整推理框架** —— **能不能替代现有算子要靠自己的 `HummingLayer` 集成测试，本报告不代厂商承诺性能**（避坑 165）。"
    "**⚠️ 分类定位（避坑 41 / 043 期新立「框架开源」条目类型）**：**本行属于「框架开源」而非「模型权重开源」** —— "
    "**权重开源的判据是「能不能下载、许可是什么」；框架开源的判据是「能不能跑起来、依赖什么硬件、支持哪些平台」**，"
    "**本行的关键字段是 `SM75+` 这个硬件门槛**（避坑 189 的五层结构不适用于框架，只适用权重） |",

]

REWRITE = {}

# ---- ① 老混元：Q04 连续第 32 期 + 高危窗口第 22 天 ----
REWRITE["🔴 **腾讯老混元大模型平台停服**"] = (
    "| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必须迁移到 TokenHub**。**10/22 高危窗口第 22 天**"
    "（9/25 自设倒排日已过 **27 天**；Q04 **连续第 32 期**未见确切日期，厂商只给「9 月底」）。"
    "⚠️ **一条「9 月底停服」拖到 10 月中下旬仍无日期，处置维持「按已停服对待、只做迁移」**——迁移动作本身不要等；"
    "⚠️ **同一家厂商两条线，一条无日期一条有精确到日的倒排**（元器 11/9，见下表），"
    "**说明「无日期」不是这家厂商的常态，而是这条线的常态**（避坑 164）。"
    "**⚠️ （044 期）回扫结论**：本轮未检索到该平台的任何补充公告（停服公告、迁移截止日或延期说明）—— "
    "**「连续第 32 期未见确切日期」本身就是本轮结论**（避坑 180：**这是待办状态、不是事实判断**） |"
)

# ---- ② DeepSeek Search / Fetch：倒计时推进到 10 天 ----
REWRITE["`DeepSeek Search` / `Fetch` 两个 API 开放"] = (
    "| 🟡 **`DeepSeek Search` / `Fetch` 两个 API 开放（10/17 · 服务端调用免费到 11/1）** | "
    "**11/1 00:00（北京）起按请求计费** | 🟡 **生效中（免费窗口距今 10 天）**。"
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
    "**⚠️ 速率限制**：官方 `Rate Limits` 表逐字 —— **`Search` QPS 上限 `100`、`Fetch` QPS 上限 `25`**；"
    "**两者各自独立计、互不消耗对方配额**；**QPS 按账户级计算、与模型并发限制分开**；**`Fetch` 另受按域名的 QPS 限制**；**超限返回 HTTP 429**。"
    "**⚠️ 对内容生成最要紧的三个响应字段**：`rerank_score` **0–3、≥1.5 视为高质量**（唯一可程序化判定的质量档）；"
    "`summary` **600–800 字符、面向模型**（`snippet` 是 100–200 字符、面向 UI，两者不是同一字段的截断版）；"
    "`content` 为页面 Markdown 全文、`need_content=false` 时恒为空字符串、且 `count` 不影响单价。"
    "**⚠️ 一条不能靠重试解决的失败**：`404` 表示无法取到可用页面内容（不可用 / 被站点策略拦截 / 目标站报错 / "
    "不支持的内容类型 / 无可提取 Markdown）—— **索引里有 ≠ 抓得到**。"
    "**⚠️ （044 期）回扫**：`api-docs.deepseek.com/updates` 本轮未见新条目 —— **连续第 5 期无新条目**；"
    "**且 043 期 `DeepSeek` 全面开源 `DeepInfer` 与 `deepseek-recipe`（10/20）不改变本行任何计费字段** —— "
    "**开源框架 ≠ API 免费或降价**（避坑 154） |"
)

# ---- ③ WorkBuddy Intl 限免：倒计时推进到 9 天 ----
REWRITE["`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免"] = (
    "| 🟢 **`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免（10/31）** | **10/31** | 🟢 **生效中（距今 9 天）**。"
    "**官方原文两句（`WorkBuddy` 官方 X，10/17 18:29）**：「新的 `DeepSeek` 刚刚发布。`WorkBuddy Intl` 也已更新到最新版本，"
    "**并且在 10 月 31 日前免费**。来试试看吧。」⚠️ **四条登记纪律**："
    "**① 主体是 `WorkBuddy Intl`（国际版），不是国内版 —— 本工作区的产品线在国内站与国际站是两套口径，不可互相代入**；"
    "**② 官方原文没有写额度上限、没有写适用账号范围、没有写结束后的价格** —— "
    "**即这三条字段全部缺失，只能按「有限时免费、无从判断能用多少」来规划**（避坑 41 第一层）；"
    "**③ 限免的标的是「已更新到最新版本」这件事，而不是某个模型名 —— 即换新版本后是否仍免费，官方原文没有回答**（避坑 166）；"
    "**④ 本行是「工作区自有产品公告」，与厂商公告分开放，避免被当成厂商口径**（避坑 126）。"
    "**⚠️ （044 期）回扫**：本轮未见续期或提前收口的公告，按避坑 78「无信号即默认维持」处理。"
    "⚠️ **与本表另两行「`WorkBuddy` 国内版」条目是三个不同主体的三笔账**（教育公益版 / DeepSeek 故障补偿 / 国际版限免），"
    "**互不代入**（避坑 126） |"
)

# ---- ④ AutoClaw 国际版：连续第 4 次未被改回 + 今天仍在 500 万档 ----
REWRITE["智谱 `AutoClaw` 第三期每日登录送 Token"] = (
    "| 🟢 **智谱 `AutoClaw` 第三期每日登录送 Token（**国际站 `z.ai` · 10/19–10/25**）** | "
    "**10/25（活动期末日）** | 🟢 **生效中（活动期末日距今 3 天 · **⚠️ 每档当天 24:00（北京）即过期，见下**）**。"
    "**官方页实测（`autoclaw.z.ai/blog/news/M10W3/`，读于 2026-10-22，本轮连续第 4 次实访）**：`Event Period: Oct 19 – Oct 25 (UTC+8)`；"
    "**`Oct 19-20 (Monday–Tuesday)` 每天领 `3,000 credits (30M tokens)`；"
    "**`Oct 21–25 (Wednesday–Sunday)` 每天领 `500 credits (5M tokens)`**；**每档 `Expires at 24:00 (UTC+8) the same day`。**"
    "**换算**：`1 credit = 1 万 tokens`；**总量 85M = 30M×2 + 5M×5**。"
    "**⚠️ 本行是本报告第一次登记的条目类型「同 URL 内容被官方就地改写」**："
    "**同一个 URL、发布日期未变、活动期 Oct 19–25 未变，但正文规则与标题总量都变了** —— "
    "**10/16 发布版是 `Get 60M Tokens`（`Oct 19` 单日 3000 万、`Oct 20–25` 每天 500 万）；"
    "本轮连续第 4 次实访仍为 `Get 85M Tokens`（`Oct 19–20` 每天 3000 万、`Oct 21–25` 每天 500 万）—— 即未被改回**。"
    "**⚠️ （044 期）本轮另核到一处页面结构的细节（本期新记）**：**该 URL 现在会 `301` 跳到带尾斜杠的 `autoclaw.z.ai/blog/news/M10W3/`** —— "
    "**即「同一篇活动页」现在有两个 URL 形态，必须用跟随重定向后的那个去核，否则会拿到空页并误判为「活动已撤」**"
    "（**注意：`301` 跳转本身不代表活动改写**—— 判定改写要看正文规则表，本轮正文仍是 `85M` 与同一套分档）。"
    "**⚠️ （044 期）今天仍在 `Oct 21–25` 那一档内 —— 每天只能领 `500 credits (5M tokens)`**，"
    "**距活动结束（10/25）还有 3 天、距 `Oct 21–25` 档结束还有 3 天**。"
    "**⚠️ 042 期那篇按旧版写的错误转述今天是「档位对、总量错」的第 2 天** —— "
    "**即避坑 192 说的「错误会从全错滑向部分对」在本例已连续两天成立**；"
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

# ---- ⑤ AutoClaw 国内站 2 亿：已过可领窗口末日（10/21 截止，今天 10/22 已不可领）----
REWRITE["`AutoClaw` 桌面端 v2.1.0 一次性 2 亿 Tokens"] = (
    "| ⚪ **`AutoClaw` 桌面端 v2.1.0 一次性 2 亿 Tokens（国内站 `zhipuai.cn` · **可领窗口已关闭**）** | **10/21** | "
    "⚪ **已结束（**可领窗口 10/15–10/21 昨日收口；**今天 10/22 已不可再领那 2 亿**）**。"
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
    "**⚠️ （044 期）本行状态推进：可领窗口已于昨日（10/21）关闭** —— **今天 10/22 起再登录已领不到那 2 亿**；"
    "**但「领到手的有效期」（7 天）是另一个日期 —— 10/15–10/21 领的那几份仍可用到 10/22–10/28 左右**"
    "（避坑 142 第二层：**可领窗口末日 ≠ 领到手的有效期**）。"
    "**⚠️ 每日登录那一档（`10.15–10.25`）不受影响，仍在活动期内**，但**它的量级是每日 500/800 积分（= 500 万 / 800 万 tokens）**，"
    "**与一次性 2 亿不是同一量级**（避坑 163：免费的是哪一档、范围有多大，三问都要答） |"
)

# ---- ⑥ OpenRouter 免费档目录：本轮改用官方 API 重取，两套口径并列 ----
REWRITE["🟢 **OpenRouter 免费档（`502+` 模型｜上期重取于 2026-10-17）**"] = (
    "| 🟢 **OpenRouter 免费档（**本轮改用官方 API 目录重取**）** | 未公布（动态目录） | 🟢 生效中。"
    "**⚠️ （044 期）本轮第一次把「`OpenRouter` 官方 API 目录」当作一手目录来用**（`openrouter.ai/api/v1/models`，本轮实跑）："
    "**全量 `468` 个模型；其中 `pricing.prompt` 与 `pricing.completion` 同为 `0` 的零价模型 `21` 个；"
    "**带 `:free` 后缀的 `18` 个**。"
    "**⚠️ 「21 个零价」与「18 个带 `:free` 后缀」不是同一集合** —— **差额 3 个是 `google/lyria-3-pro-preview`、"
    "`google/lyria-3-clip-preview` 与 `openrouter/free`（一个路由器）** —— "
    "**即「零价」⊅「`:free` 后缀」，写清单时必须说清是哪一个口径**（避坑 161：**同类源之间也要标口径**）。"
    "**⚠️ 与 `freellm.net` 转录口径的差异（两说并列、不取其一）**：**`freellm.net` 的 `OpenRouter` 专页"
    "（正确路径 `/providers/openrouter`，本轮实访）仍写 `20` 个条目、`Last Updated 2026-10-21` —— "
    "**与官方 API 目录的 `21` 零价 / `18` 后缀两个数都不吻合**。"
    "**⚠️ 截至本期，`OpenRouter` 仍未发布任何限免公告页**（041–044 连续四期未核到）—— "
    "**故本行「截止」列写「未公布」，不替厂商写一个截止日**（避坑 191：**把 uptime 统计窗口读成限免期是凭空造出截止日**）。"
    "**⚠️ 额度口径仍是「三源三个数、都带来源」**：**① `freellm.net` `OpenRouter` 专页：主限流「`200 req/day`（free tier）」、"
    "免绑卡「`Not required`」、免手机号「`Not required`」、上下文区间 `66K – 1.0M`；"
    "**② `OpenRouter` 官方 `docs/faq` 逐字「`For free models, rate limits are determined by the credits that you have purchased. "
    "If you have purchased at least 10 credits, your free model rate limit will be 1000 requests per day. "
    "Otherwise, you will be rate limited to 50 free model API requests per day.`」；**③ `benchlm.ai`：与 ② 同口径**。"
    "**⚠️ ① 与 ② 在「日请求数」上直接冲突（200 vs 50），不可取中间值、不可只写一个**（避坑 161） |"
)

# ---- ⑦ OpenCode 安全事件处置状态：本期回扫，官方仍无完成时点 ----
REWRITE["`OpenCode` 安全事件处置状态"] = (
    "| 🟡 **`OpenCode` 安全事件处置状态（10/17 起 · 040 期头条，本期状态推进）** | 未公布（**官方明确「事件仍在处置中」、无修复完成时点**） | "
    "🟡 **生效中（仍在处置中，官方不给完成时点）**。"
    "**041–044 期已登记的口径全部维持**：**攻击面 = 一套「正在停用的旧系统」遭未授权访问**，"
    "**存放在用户工作区的第三方 AI 服务 API 密钥可能泄露（含 `OpenAI`、`Anthropic`）**；"
    "**官方明确「目前尚无法确认相关密钥是否遭到恶意使用，初步调查也未发现其他数据泄露的证据」**（阴性结果，非清白证明，避坑 138 同族）；"
    "**退款口径按主体分四家（避坑 184）**：`OpenAI` **承诺**退款、`OpenCode` 退款**正在进行 / 已启动补偿流程**、"
    "`Anthropic` 与 `Google` **封禁**密钥且**本轮未核到其退款承诺**；"
    "**「1.4%」的分母口径官方仍未给出**。"
    "**⚠️ （044 期）本轮补一条与本期头条的交叉观察**：`OpenAI` 同日（10/21）发布的 `Patch the Planet` 公告里，"
    "**逐字提到 `We’re also calibrating additional blocking classifiers for Daybreak to help reduce the potential for misuse. "
    "This involves difficult tradeoffs: safeguards intended to prevent abuse can also block legitimate security work.`** —— "
    "**即防守方被护栏挡住这件事，官方本人在同一周自己写成了「困难的权衡」**（避坑 185："
    "**安全护栏会按场景拒绝防守方，这类通道必须提前申请**）。"
    "**⚠️ 但本行不写「防护失效」也不写「防护有效」**（避坑 190）—— **官方这段是在讲「校准分类器的取舍」，不是在讲本次事件的成因**。"
    "**⚠️ 「1.4%」这一条至今没有任何官方给出分母** —— **本报告不代官方补分母、不做推算**（避坑 165） |"
)

# ---- ⑧ MiniMax M3.1 Flash 开放权重：第 ④ 级连续第 2 期未见（改写 043 期那一行，不新增行）----
REWRITE["⚠️ **`MiniMax` `M3.1 Flash` 开放权重"] = (
    "| ⚠️ **`MiniMax` `M3.1 Flash` 开放权重（10/19 宣布 · **第 ④ 级连续第 2 期未见**）** | "
    "**官方未公布**（**官方博客逐字只写 `will be released later.`；媒体口径的「10 月 23 日」只出自官方 X 与第三方** —— "
    "**非活动截止，是权重交付的传闻日**） | "
    "⚠️ **未到可下载状态**（**第 ① 级已到（API 可调）、第 ② 级已到（官方文档站标 `open-weight`）、第 ③ 级官方未给日期、"
    "第 ④ 级连续第 2 期未见（`HF` `MiniMaxAI` 组织页无任何 `M3.1` 仓库）**）。"
    "**⚠️ （044 期）本轮实跑 `HF` API（`hf-mirror.com/api/models?author=MiniMaxAI`，`limit=100`）**：**组织页共 `21` 个仓库** —— "
    "`MiniMax-Text-01`、`MiniMax-VL-01`、`SynLogic-32B`、`SynLogic-Mix-3-32B`、`SynLogic-7B`、`MiniMax-Text-01-hf`、"
    "`MiniMax-M1-40k`、`MiniMax-M1-80k`、`MiniMax-M1-80k-hf`、`MiniMax-M1-40k-hf`、`MiniMax-M2`、`VTP-Small-f16d64`、"
    "`VTP-Base-f16d64`、`VTP-Large-f16d64`、`MiniMax-M2.1`、`MiniMax-M2.5`、`MiniMax-M2.7`、`MiniMax-M3`、`MiniMax-M3-MXFP8`、"
    "`MiniMax-H3`、`MiniMax-Music3`，**其中不含任何 `M3.1` 或 `M3.1-Flash`**。"
    "**⚠️ 「连续 N 期未见」是待办状态、不是事实判断**（避坑 180）—— **本行写「连续第 2 期未见」，不写「不会发布」**。"
    "**⚠️ 一个本报告自己抓到的计数错误（本期纠错第 1 条）**：**043 期正文写「`20` 个仓库逐个核过」，但它自己列出的名单是 `21` 个** —— "
    "**即上一期是「手写计数与明细不同源」**（避坑：凡出现数字，要么全从表里算、要么全在正文里定义）；"
    "**本轮 API 实跑为 `21` 个，与 043 期正文列出的明细一致 —— 即错的是那个 `20`，不是仓库数变了**。"
    "**⚠️ 顺带核到的另一个量（本期重取）**：`MiniMax-H3` 的 `downloads` 由 043 期记的 `489 万` 升至 **`5,007,397`** —— "
    "**这是本报告第一次把 `H3` 的下载数写成一个精确值**（此前只写「489 万」，本轮起写精确值以便下期做同口径 diff）。"
    "**⚠️ 在第 ④ 级之前，一律按「只能用 API、不能下载」规划**（避坑 41 第四层 / 139） |"
)

# ---- 归属化：未 REWRITE 的行把「本期」改为「043 期」 ----
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
    out.append(l.replace("**本期", "**043 期").replace("（本期", "（043 期"))

rw = 0
for k, v in REWRITE.items():
    src_hits = sum(1 for l in body if k in l)
    assert src_hits == 1, ("键在源表中命中数不为 1", k, src_hits)
    out_hits = sum(1 for l in out if v in l)
    assert out_hits == 1, ("REWRITE 的值未出现在输出里 / 出现多次", k, out_hits)
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

bad = []
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
