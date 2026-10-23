# -*- coding: utf-8 -*-
"""从 044 期 md 提取第四章截止表 -> 基准日 2026-10-23 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table045.md（纯表格块，供 045 期正文嵌入）。

沿用 044 期范式，本期为第二十一次落地：
  1) 先断言行数（044 期 body = 228）
  2) 按行名子串套 REWRITE 字典（每键必须恰好命中 1 次）
  3) 正则重算每一行的「距今 N 天」（基准日 10/23）
  4) 未 REWRITE 的行做归属化（「本期」-> 「044 期」）
  5) 新行插在 ⚪ 存档块之前 -> 再断言总数
  6) 输出后由 inject045.py 注入正文占位符

⚠️ **本期核心变化（五件）**：
   - **`MiniMax M3.1 Flash` 免费档 10/22 同日从 `OpenRouter` 与 `OpenCode` 双双收口**：
     `openrouter.ai/minimax/minimax-m3.1-flash:free` 页面出现官方横幅
     「**The free launch period ended Oct 22, 2026.**」（**OpenRouter 史上第一次给免费档确切结束日**）；
     `opencode.ai/docs/go` 的 `MiniMax M3.1 Flash Free (limited time)` 已改回 `MiniMax M3.1 Flash`，
     `docs/zen` 的 Free models 清单里 `M3.1 Flash Free` 计数为 `0`。
     官方 API 目录 `:free` 因此由 `18` 降为 `17`。
   - **`MiniMax M3.1 Flash` 权重早已在 `HF`**（`createdAt` 2026-10-17T06:37:50Z）——
     **043 / 044 两期判定「权重未见」是错的，错因是取数方法**（见避坑 196）；
     许可为 `minimax-community`（**非商用免费；商用须标注 `Built with MiniMax M3.1-Flash`；
     年收入 > 2,000 万美元须另行书面授权**）—— 不是开源许可（见避坑 197）。
   - **`Anthropic` 10/22 三连发**：捐赠 `Agent Skills` 开放标准给 `AAIF`（Linux Foundation 旗下）、
     生命科学 guest investigators 开放申请（`at no cost`，约 14 天窗口）、
     与 `Theorem` 的形式化验证成果（123 个 OSS-Fuzz 库 / 239 个入口点 / 约 1.8 亿行 Rocq；
     证明子集公开于 GitHub，`Theorem` 免费为其他开源项目跑同一管线）。
   - **智谱 `AutoClaw` 国内站 `M10W4` 已发布**：10/26–11/1 一次性 **1 亿** Tokens（10,000 积分），
     **较 `M10W3` 的 2 亿降档**（见避坑 198）。
   - **`OpenAI` `Decisions API` 10/22 GA**（030 期登记的公测期结束）。
"""
import re
from datetime import date

SRC = "AI免费内容与权益速递-第044期-2026-10-22.md"
OUT = ".workbuddy/tmp_table045.md"
BASE = date(2026, 10, 23)
PREV = 228

lines = open(SRC, encoding="utf-8").read().split("\n")
s = e = None
for i, l in enumerate(lines):
    if l.startswith("## 四、"):
        s = i
    if s is not None and l.startswith("## 五、"):
        e = i
        break
rows = [l for l in lines[s:e] if l.startswith("|")]
_foot = None
for _i, _l in enumerate(rows):
    if _l.startswith("| 口径 | 分布"):
        _foot = _i
        break
header, sep = rows[0], rows[1]
body = rows[2:_foot] if _foot is not None else rows[2:]
assert len(body) == PREV, (len(body), PREV)

NEW = [
    # ---- 新行 1：Anthropic 捐赠 Agent Skills 给 AAIF ----
    "| 🟢 **`Anthropic` 把 `Agent Skills` 开放标准捐赠给 `Agentic AI Foundation`（10/22 · **含名称/徽标/GitHub 组织/`agentskills.io` 域名**）** | "
    "无结束日（**开放标准，不设活动期**） | 🟢 **生效中（`anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation`，页面标注 `Published Oct 22, 2026` · `Category Product`）**。"
    "**官方一手逐字**：「**Today, we’re donating Agent Skills, the open standard that gives AI agents specialized knowledge and "
    "workflows, to the Agentic AI Foundation (AAIF).**」「**We’re committed to keeping Agent Skills open, community-driven, and "
    "vendor-neutral.**」「**We are donating the Agent Skills name and logo, the GitHub organization, and the agentskills.io domain.**」"
    "「**You can continue to use the standard or contribute to it without joining the AAIF.**」"
    "「**Engineers from Anthropic, Google, OpenAI, and other companies will maintain the standard as individuals, with David Soria "
    "Parra and Mahesh Murag as Lead Maintainers.**」"
    "**⚠️ 治理结构（决定「中立」这两个字的含金量）**：**`AAIF` 在 `Linux Foundation` 之下，`Anthropic` 与 `Block`、`OpenAI` 共同创立，"
    "`MCP` 此前已捐给它** —— **即这是同一个基金会的第二笔捐赠，不是新建一个壳**。"
    "**⚠️ 规模数字全部带口径**：**「超过 `70` 个智能体平台已集成」**（官方逐字 `More than 70 agent platforms, including ChatGPT, "
    "Cursor, GitHub Copilot, and VS Code, have integrated Agent Skills since we published the standard in December 2025.`）；"
    "**「已发布 `1` 百万个 skill、安装近 `280` 百万次」**（官方逐字 `So far, 1 million skills have been published and nearly 280 "
    "million installed.`）—— **这两个数都是官方自报，不是第三方实测**（避坑 165）。"
    "**⚠️ 「捐赠」不等于「开源许可变更」**：**公告全文没有写任何许可证条款**，"
    "**规范正文在 `agentskills.io`（本轮实访可达，站上写 `Agent Skills are a lightweight, open format`）** —— "
    "**本报告因此不写「已改为某许可证」，只写「标准与域名转入基金会」**（避坑 154）。"
    "**⚠️ 本条的免费性判据**：**标准本身可自由使用与贡献（官方逐字 `without joining the AAIF`），无申请、无截止日** —— "
    "**这是避坑 193 三层次里的第①层「开源自取」** |",

    # ---- 新行 2：Anthropic 生命科学 guest investigators ----
    "| 🟡 **`Anthropic` 生命科学 guest investigators 开放申请（10/22 · **官方逐字 `at no cost to them`**）** | "
    "**约 14 天（官方逐字 `Applications will be open for approximately 14 days`，自 10/22 起算 ≈ 11/5 前后；"
    "官方未给确切日历日）** | 🟡 **生效中（申请窗口开放中 · 审批类权益，不是领取类）**。"
    "**官方一手（`anthropic.com/news/open-call-guest-investigators-life-sciences`，`Published Oct 22, 2026` · `Category Announcements`）逐字**："
    "「**We’re looking for proposals from principal investigators and their research groups at academic institutions, nonprofits, or "
    "government labs who want to use Claude to investigate key questions in causal human biology, structural and computational "
    "molecular biology, medicinal chemistry, drug discovery, and clinical science.**」"
    "「**Over 8–12 weeks, guest investigators will work directly with Anthropic researchers on a problem of interest.**」"
    "「**Our team will run our models and harnesses at no cost to them.**」"
    "「**We’ll work together to publish these outputs and open-source the accompanying data and code.**」"
    "「**Guest investigators retain the rights to their data at every step during their project.**」"
    "「**Applications will be open for approximately 14 days, and we’ll strive to notify selected participants by email approximately "
    "14 days after applications close.**」"
    "**⚠️ 这是「免费」的第③层：身份权益 + 定向补贴**（避坑 193）—— **「`at no cost`」免的是算力与模型使用成本，"
    "不是一笔可以随便花的额度；拿到资格的是被选中的研究组，不是所有注册用户**。"
    "**⚠️ 三个不能省的限定**：**① 申请主体限「学术机构 / 非营利 / 政府实验室的 PI 及其研究组」；"
    "② 官方明写「不要给我们数据」（`We aren’t asking for guest investigators to give us their data`），"
    "且要求申请材料只含公开信息；③ 窗口是「约 14 天」不是确切日期** —— **本行「截止」列因此写「约 14 天」而不写 11/5**（避坑 154 / 166）。"
    "**⚠️ 与 `Claude Duet` 的对照**：**两者同在 10/21–10/22 发布、都带候补/申请制，但 `Duet` 官方一字未提免费，"
    "本条官方逐字写了 `at no cost`** —— **「官方有没有写」这件事本身就是口径**（避坑 195） |",

    # ---- 新行 3：Anthropic × Theorem 形式化验证 ----
    "| 🟢 **`Anthropic` × `Theorem`：`Claude` 对 `123` 个 `OSS-Fuzz` 库完成汇编级形式化证明（10/22 · **证明子集公开于 `GitHub`**）** | "
    "无结束日（**公开的是证明产物，不是活动**） | 🟢 **生效中（`Anthropic` `Frontier Red Team` 10/22 发布；"
    "本报告本轮未取到官方一手页，以下字段全部来自第三方转述并已逐条标注）**。"
    "**规模（第三方一致口径）**：**`239` 个入口点 / `123` 个 `OSS-Fuzz` 库 / 约 `1.8` 亿行 `Rocq` 证明；"
    "单条证明典型约 `60` 万行，对应二进制中位数约 `18,000` 条 `RISC-V` 指令。"
    "**⚠️ 本报告登记的免费性有三样，且三样的获取方式不同**（避坑 193 三层次同时出现在这一条里）："
    "**① 证明产物公开** —— **第三方逐字转述「`a subset of the proofs is public on GitHub for anyone to check`」、"
    "「`The proofs, specifications, and formal models from this project are available for independent verification`」**；"
    "**② `Theorem` 免费为其他开源项目跑同一管线** —— **第三方逐字「`Theorem is offering to run the same pipeline for other "
    "open-source projects`」「`free of charge`」** —— **这是厂商服务方的免费承诺，不是 `Anthropic` 的承诺**；"
    "**③ `Theorem` 发布了 `Claude` skill**（第三方逐字 `has published a Claude skill to help developers start verifying their own code`）。"
    "**⚠️ 覆盖范围的边界必须一起写（否则读者会把「证明了」读成「没问题了」）**："
    "**证明只覆盖「单线程、静态链接、`RISC-V` + `musl` + `Linux`、固定内存预算、输入 < `64 MB`」的二进制** —— "
    "**而生产环境主流是 `x86`/`ARM` + 动态链接 `glibc`，不在覆盖范围内**。"
    "**⚠️ 「形式化验证」不等于「无 bug」**：**官方/转述一致口径是「证明只说明程序满足所声明的规约，规约本身可能错」**；"
    "**且 `AddressSanitizer` 抓不到所有内存错误、每个库也并非所有入口点都被证明**。"
    "**⚠️ 取料状态（如实记）**：**本轮实访 `anthropic.com/research` 与 `/engineering` 均未在列表首屏取到该文**"
    "（`/research` 页内 `Theorem` 的 `7` 次命中全部指向 `Formalizing Fermat’s Last Theorem` 那篇数学文章，"
    "与本条不是同一件事）；**故本行不写任何「官方逐字」引文，只写第三方一致转述并标注**（避坑 44） |",

    # ---- 新行 4：AutoClaw 国内站 M10W4 ----
    "| 🟢 **智谱 `AutoClaw` 国内站 `M10W4` 一周福利：登录领 **1 亿** Tokens（10/26–11/1 · **较 `M10W3` 的 2 亿降档**）** | "
    "**10/26（周一）00:00 — 11/1（周日）23:59（北京时间）；奖励 11/1 23:59 失效** | "
    "🟢 **尚未开始（活动期 10/26 起，本行是「下一轮活动已公告」状态）**。"
    "**官方一手（`autoclaw.zhipuai.cn/blog/news/M10W4/`，页面标注 `2026年10月23日` · 资讯）逐字**："
    "「**10 月 26 日（周一）00:00—11 月 1 日（周日）23:59（北京时间）**」；"
    "「**活动规则：登录 AutoClaw，即可领取 1 亿 Tokens（相当于 10,000 积分），每个账号限领一次。**」；"
    "「**奖励将在 11 月 1 日 23:59（北京时间）失效，越早领取，使用时间越充足哦。**」"
    "**⚠️ 一条降档必须写全三样（避坑 198 本期新立）**：**① 上一档是多少 —— `M10W3` 国内站一次性档是 **2 亿** Tokens"
    "（`20,000` 积分，活动期 `10.15–10.21`，可领窗口已于 10/21 关闭）；② 这一档是多少 —— **1 亿** Tokens（`10,000` 积分）；"
    "③ 两档活动期是否相接 —— `M10W3` 一次性档 `10.15–10.21`、`M10W4` 一次性档 `10.26–11.1`，"
    "**中间 10/22–10/25 四天没有一次性档**，只有 `10.15–10.25` 的每日登录档（普通用户每日 `500` 积分 / 付费会员每日 `800` 积分）。"
    "**⚠️ 本期未核到的一件事（如实记）**：**`M10W4` 公告只写了一次性 1 亿档，没有写 `10.15–10.25` 的每日登录档"
    "是否延续到 11/1 之后** —— **本报告不替官方续期，也不写「每日档已结束」**（避坑 154 / 161：未核到 ≠ 不存在）。"
    "**⚠️ 国际站与国内站不是同一节奏**：**本轮实访国际站 `autoclaw.z.ai/blog/news/M10W3/` 仍是 `Get 85M Tokens`、"
    "活动期 `Oct 19 – Oct 25 (UTC+8)`、`Oct 21–25` 每天 `500 credits (5M tokens)`**（**连续第 5 次未被改回**）—— "
    "**即国内站已发到 `M10W4`，国际站还停在 `M10W3`，两边不可互相推算**（避坑 163 多站点面）。 |",

    # ---- 新行 5：国办发〔2026〕29号 ----
    "| 🟢 **国务院办公厅《关于适应人工智能技术发展助力构建就业友好型发展方式的意见》（国办发〔2026〕29 号 · **10/16 印发、10/23 公布**）** | "
    "无结束日（**政策文件，非活动**） | 🟢 **生效中（`gov.cn/zhengce/zhengceku/202610/content_7084108.htm`，"
    "文末署名 `国务院办公厅 2026年10月16日`、标注 `此件公开发布`；新华社 10/23 发电）**。"
    "**一手要点**：**总体要求提出「积极增强人工智能创造就业机会、赋能传统岗位、提升就业质量、激发创业活力的正面效应，"
    "有效减缓人工智能应用就业替代影响」**；**部署 6 个方面 18 项主要任务**。"
    "**⚠️ 本报告只登记其中与「免费/开放」直接相关的三条**（政策线不做全文摘录）："
    "**① `深入实施“人工智能+”行动`**；**② 「**以开源生态促进中小企业创新创业**」（第二方面第（二）项，"
    "官方同时写「保障中小微企业和个体工商户依法平等使用数据、算法等智能生产要素」）；"
    "③ 「**发挥好国家创业投资引导基金、国家人工智能产业投资基金等政府投资基金作用，按照市场化方式支持人工智能领域企业创新发展**」。"
    "**⚠️ 三条边界**：**① 本报告不把它读成「发钱文件」—— 全文没有任何面向个人开发者的免费额度或补贴申领入口**；"
    "② **印发日（10/16）与公布日（10/23）不是同一天**，本行两个日期都写；"
    "③ **这是「就业友好型」框架文件，不是技术管制文件**，**与同窗口的商务部 48 号公告是两条不同的线，不要合并成一句**（避坑 134） |",
]

REWRITE = {}

# ---- 1) 老混元 Q04：连续第 33 期 / 高危窗口第 23 天 ----
REWRITE["🔴 **腾讯老混元大模型平台停服**"] = (
    "| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必办（已过期，Q04 连续第 33 期未决 · 高危窗口第 23 天）**。"
    "**厂商仍只给「9 月底」这一模糊口径，未给确切停服日** —— **按避坑 47 与 164 的互补口径："
    "厂商不给确切日期时，本报告只做迁移提示、不替它排一个日**。"
    "**⚠️ （045 期）本轮实访 `cloud.tencent.com/document/product/1729` 返回的是压缩响应，正文未取到** —— "
    "**因此本期不更新该行的任何事实字段，只按基准日推进「连续第 33 期 / 第 23 天」两个由脚本重算的数**（避坑 180："
    "「连续 N 期」是待办状态、不是事实判断）。**迁移方向见 040 期起的既有结论，本报告不重复往期已固化内容。** |"
)

# ---- 2) OpenRouter 免费档：468/20/17 + freellm 520/304/30/438 ----
REWRITE["🟢 **OpenRouter 免费档（**本轮改用官方 API 目录重取**）**"] = (
    "| 🟢 **OpenRouter 免费档（**官方 API 目录口径 · `468/20/17`**）** | 未公布（动态目录） | "
    "🟢 生效中。**⚠️ （045 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-23）**："
    "**全量 `468` 个模型（与上期同值）；零价（`pricing.prompt` 与 `pricing.completion` 同为 `0`）`20` 个；"
    "带 `:free` 后缀 `17` 个**。"
    "**⚠️ 三个数都变了或没变，必须逐个说清**：**全量 `468` 与 044 期同值；零价 `21 → 20`；`:free` `18 → 17`** —— "
    "**即有一个带 `:free` 后缀的模型从官方目录里消失了**。"
    "**⚠️ 本期能定位到这个差额（044 期未能定位）**：**`minimax/minimax-m3.1-flash:free` 已不在目录中**，"
    "其模型页现在挂着官方横幅「**The free launch period ended Oct 22, 2026. MiniMax M3.1 Flash is now served at list price "
    "($0.15/M input, $0.60/M output, $0.015/M cached input).**」—— "
    "**这是本报告跟踪 `OpenRouter` 免费档以来，官方第一次给免费档一个确切结束日**（041–045 连续五期「无公告页」的状态首次被打破，"
    "但打破它的不是公告页，是模型页上的一条横幅）。"
    "**⚠️ 「零价 20」与「`:free` 后缀 17」仍不是同一集合**：**差额 3 个依旧是 `google/lyria-3-pro-preview`、"
    "`google/lyria-3-clip-preview` 与 `openrouter/free`（一个路由器）**（避坑 161）。"
    "**⚠️ 与 `freellm.net` 转录口径首次逐条一致**：**该站 `OpenRouter` 专页（`/providers/openrouter`）`Last Updated 2026-10-23`，"
    "列 `20` 个模型；本轮逐条比对，其 `20` 条与官方 API 的 `20` 个零价模型完全一致（含 3 个非 `:free` 后缀项）** —— "
    "**044 期「三个数都不吻合」的状态本期结束，但这是「转录站追上了」，不是「两个口径合并成一个」**（避坑 030："
    "口径对齐不等于可以混用）。"
    "**⚠️ 首页计数器（`freellm.net/`，读于 2026-10-23）逐项记账**：**`Models Tracked` `510 → 520`；"
    "`Free & Online` `301 → 304`；`Providers` `30 → 30`（同值）；`No Credit Card` `425 → 438`；"
    "Hero 句 `510+ → 520+`；「经实时 API 验证」`241 → 244`** —— "
    "**升/同值三种结果都写，不写趋势判断**（避坑 029）。"
    "**⚠️ 本行 17 个 `:free` 模型的全量清单已存档于 `.workbuddy/data/`**（`tmp_or_free_2026-10-23.txt`），"
    "**下一期起可逐条 diff —— 这是 044 期「差额定位不到」的直接修正**。"
    "**⚠️ 额度口径仍是「三源三个数、都带来源」**：**① `freellm.net` `OpenRouter` 专页 `200 req/day`、免绑卡、免手机号、"
    "上下文 `66K – 1.0M`；② `OpenRouter` 官方 `docs/faq` 的 `50 / 满 10 credits 后 1,000` 请求每日；"
    "③ `benchlm.ai` 与 ② 同口径** —— **① 与 ② 在日请求数上直接冲突，不可取中间值**（避坑 161）。"
    "**⚠️ `openrouter.ai/announcements` 本轮实访仍停在 `October 14, 2026`**（041–045 连续五期无新限免公告）。 |"
)

# ---- 3) 上海青浦算力券：申报截止日就是今天 ----
REWRITE["🟢 **上海青浦算力券补贴**"] = (
    "| 🔴 **上海青浦算力券补贴** | 申报至 **10/23** | 🔴 **申报截止日即本期基准日（10/23）—— 今日最后一天，过期不候**。"
    "**⚠️ 这是本报告「今天到期」类条目的标准处理**：**截止日是今天，状态列必须从「生效中」改为「今日截止」**，"
    "**不写「已结束」（今天还没过完）、也不写「生效中」（那会让读者以为还有明天）**。"
    "**⚠️ 本报告不代官方判断「是否可补报」** —— 官方页未写补报通道，本行不写（避坑 154）。"
    "**申报类权益 ≠ 领取类权益**（避坑 182）：**审批结果与到账时间官方均未公布，本行不写任何「到账日」。** |"
)

# ---- 4) o4-mini 停用：今天就是停用日 ----
REWRITE["🟢 **OpenAI `o4-mini` API 停用**"] = (
    "| ⚪ **OpenAI `o4-mini` API 停用** | **10/23** | ⚪ **已结束（停用日即本期基准日 10/23 · 044 期记为「距今 1 天」）**。"
    "**⚠️ 状态列由 🟢 改为 ⚪ 的判据只有一条：截止日 ≤ 基准日** —— "
    "**044 期该行写「距今 1 天」，本期重算为 `0`，按脚本口径归 `over` 档**（`check_deadlines.py --today 2026-10-23` 实跑）。"
    "**⚠️ 本报告不写「停用当天是否仍可调用」** —— **官方未给「当天几点截止」的钟点，本行不填**（避坑 154 / 166）。 |"
)

# ---- 5) Decisions API：公测 -> GA ----
REWRITE["🟢 **OpenAI Decisions API（system 1 决策接口）**"] = (
    "| 🟢 **OpenAI `Decisions API`（10/22 GA · **基于 `GPT‑6 Luna` · 无免费层**）** | 未公布 | "
    "🟢 **生效中（10/6 公测 → **10/22 正式 GA**，030 期补登、045 期状态推进）**。"
    "**官方一手（`openai.com/index/decisions-api`，页面标注 `October 22, 2026` · `Category Product`）逐字**："
    "「**Today, we’re making the Decisions API generally available.**」「**Built with GPT‑6 Luna, the Decisions API focuses "
    "Luna’s intelligence on questions with bounded answers, helping applications and agents make near real-time decisions from "
    "text, images, and structured inputs up to 10x faster than GPT‑6 Luna through the Responses API.**」"
    "「**Since public beta, we’ve added a native GPT‑Live integration, prompt caching for reused context, and inference residency "
    "in the US and EU.**」「**Developers can also pass native JSON inputs, include images in question instructions, and ask up to "
    "400 questions per request, twice the previous limit.**」「**We’ve also continued to improve latency, including additional "
    "capacity in several regions in Asia.**」"
    "**定价（官方逐字）**：「**Decisions API costs $0.10 per million input tokens. Cached input costs $0.01 per million tokens.**」"
    "「**You only pay for input tokens: there are no output-token charges.**」"
    "**⚠️ 三条必须写清的口径**：**① 「输出免费」是因为它不生成文本、只返回选项/分数** —— "
    "**这不是聊天模型的免费替代品**（避坑 118/119 同源）；"
    "② **全页没有任何 `free tier` / 试用额度 / 免费钟点** —— **本行不写「有免费额度」**（避坑 154）；"
    "③ **`10x faster` 是厂商自报、对照系是「走 Responses API 的 `GPT‑6 Luna`」，不是对照别的厂商**（避坑 116）。"
    "**⚠️ 客户引语里的数字同样是厂商自报**（官方页逐字）：`Box`「`~5x faster route selection`」、`Datadog`「`40x faster p95`」、"
    "`Ramp`「`4x faster and 30% cheaper`」、`Sierra`「`under 280 ms p95, about 3× faster and 90% lower cost per call`」—— "
    "**五家客户五个口径，本报告不取其中一个当结论**（避坑 116 / 165）。"
    "**⚠️ 与 030 期登记时的差别**：**030 期是「单一信源（The New Stack 转述）、官方模型卡未核到」；"
    "本期官方页已在手，且公测期新增的四项能力（`GPT‑Live` 集成 / 提示缓存 / 美欧推理驻留 / 单请求 400 题）均为官方逐字**。 |"
)

# ---- 6) 商务部 48 号：距 11/15 23 天 + 新增第三方转录的两项技术 ----
REWRITE["🟡 **商务部 AI 技术出口管制目录修订 · 出口前登记**"] = (
    "| 🟡 **商务部 / 科技部 2026 年第 48 号公告 · AI 领域 23 项技术增列 + 出口前登记** | "
    "**11/15（征求意见截止）；登记实施日「未公布」（自公告发布日起至目录正式修订实施日止）** | "
    "🟡 **生效中（义务已成立、通道未开的状态维持）**。**（045 期）距征求意见截止 **23 天**（基准日 10/23，由脚本重算）。"
    "**官方一手（`mofcom.gov.cn` 安全与管制局，`发文日期 2026年10月16日`，页面发布时间 `2026-10-16 16:00`）逐字**："
    "「**人工智能领域包括大模型、智能体、算力集群、信息处理相关 23 项技术；对已通过开源、发表学术论文等方式进入公共领域的技术，"
    "不纳入管理范围。**」「**自本公告发布之日起，至《中国禁止出口限制出口技术目录》正式修订并实施之日止，"
    "技术出口经营者在出口本公告附件所列技术前，应当在商务部业务系统统一平台技术贸易管理信息应用"
    "（https://ecomp.mofcom.gov.cn）登记。已经开始但尚未完成的出口，在登记范围内。**」"
    "**⚠️ 本期回扫结论（与 044 期相同，但多了一条交叉证据）**：**未见实施日公告、也未见任何一家厂商就「已启动登记」发出办理指引** —— "
    "**受影响主体仍处在「义务已成立、通道未开」的状态**（Q27 三项仍未定）。"
    "**⚠️ 本期新记一条与本报告 044 期头条直接相关的第三方口径（不采信为官方）**："
    "**附件技术范围（征求意见稿）以 `.wps` 附件形式发布，本报告未取到附件正文**；"
    "**第三方（百度百科词条转述附件）称「拟禁止出口 14 项」中含「**人工智能驱动的恶意代码生成与变异技术**」、"
    "「拟限制出口 26 项」中含「**人工智能辅助漏洞挖掘技术**」** —— "
    "**⚠️ 这两项若属实，与 `OpenAI` `Patch the Planet` / `PHP2Shell`（AI 协助发现 `PHP` 核心漏洞）是同一条线上的两端，"
    "但本报告只登记为「第三方转录、未经官方附件核实」，不写成官方口径**（避坑 44 / 116）。"
    "**⚠️ 不得写成「AI 技术出口已被管制」** —— **登记生效日与管制实施日是两件事**（避坑 167）。 |"
)

# ---- 7) DeepSeek Search/Fetch：倒计时 9 天 + 连续第 6 期无新条目 ----
REWRITE["`DeepSeek Search` / `Fetch` 两个 API 开放"] = (
    "| 🟡 **`DeepSeek Search` / `Fetch` 两个 API 开放（10/17 · 服务端调用免费到 11/1）** | "
    "**11/1 00:00（北京）起按请求计费** | 🟡 **生效中（免费窗口内 · 距今 9 天）**。"
    "**（045 期）回扫 `api-docs.deepseek.com/updates`（Change Log）实访**："
    "**最新条目仍是 `Date: 2026-10-17`（`Opening up the in-house search API` + `DeepSeek-V4.1-Flash-1017 Update`），"
    "其后无任何新条目** —— **即 `DeepSeek` 侧连续第 6 期无新发布**。"
    "**⚠️ 该页 10/17 条目里有一段与免费无关但影响成本判断的厂商自报**（官方逐字）："
    "「**While improving performance, we also reduced the model’s task runtime and output length, enabling users to complete tasks "
    "at lower cost and higher speed and achieving a new performance–cost Pareto optimum across multiple harnesses. We specifically "
    "optimized for DeepSeek Harness, Tencent CodeBuddy, WorkBuddy, and other platforms.**」—— "
    "**「更低成本」是厂商结论，且优化对象点名了具体平台，本报告不转写为普适结论**（避坑 116 / 165）。"
    "**⚠️ 「开源框架不改变 API 价格」这条既有结论本期不变**：**10/20 开源的 `DeepInfer` 与官方 API 计费是两本账**。 |"
)

# ---- 8) WorkBuddy Intl：9 天 ----
REWRITE["`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免"] = (
    "| 🟢 **`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免（10/31）** | **10/31** | "
    "🟢 **生效中（距今 9 天 · 工作区自有产品线）**。**（045 期）本轮未实访到该产品页的新变化，本行只按基准日推进天数** —— "
    "**「连续 N 期未变」不等于「已确认无变化」，本报告不写「已复核」**（避坑 030 / 180）。 |"
)

# ---- 9) AutoClaw 国际站：连续第 5 次未改回 + 距今 2 天 ----
REWRITE["智谱 `AutoClaw` 第三期每日登录送 Token"] = (
    "| 🟢 **智谱 `AutoClaw` 国际站 `M10W3` 每日登录送 Token（`z.ai` · 10/19–10/25 · **连续第 5 次未被改回**）** | "
    "**10/25（活动期末日）** | 🟢 **生效中（`Oct 21–25` 档内 · 距活动期结束 2 天）**。"
    "**（045 期）本轮实访 `autoclaw.z.ai/blog/news/M10W3/`（跟随 `301`，读于 2026-10-23）**："
    "**标题仍为 `Get 85M Tokens: Daily Login Event`；活动期 `Oct 19 – Oct 25 (UTC+8)`；"
    "`Oct 19-20 (Monday–Tuesday)` 每天 `3,000 credits (30M tokens)`；"
    "`Oct 21–25 (Wednesday–Sunday)` 每天 `500 credits (5M tokens)`；每档当天 24:00 (UTC+8) 过期** —— "
    "**与 044 期逐字一致，一字未改（连续第 5 次）**。"
    "**⚠️ 今天（10/23）仍在 `Oct 21–25` 那一档内，每天只能领 `500 credits (5M tokens)`；距 10/25 结束还有 2 天**。"
    "**⚠️ 041 期立的避坑 179 第一条实操（每次引用前现场打开）连续第 5 期成立** —— "
    "**「官方改写是一次性临时变动」这个猜测已连续第 5 次被证伪**。"
    "**⚠️ 取料纪律继续生效（避坑 194）**：**该 URL 旧形态（不带尾斜杠）会 `301`，不跟随重定向会拿到 `0` 字节空文件** —— "
    "**空页 ≠ 活动已撤，判定必须看正文规则表**。"
    "**⚠️ 国际站与国内站节奏不同（不可互相推算）**：**国内站 `M10W4`（10/26–11/1 一次性 1 亿）已于 10/23 发布，"
    "国际站仍停在 `M10W3`**（避坑 163 多站点面）。"
    "**⚠️ 「当天清零」型不可当存款**（避坑 117 同族）；**官方页未写各模型扣多少 credits，本报告不代官方换算**（避坑 41 第一层）。 |"
)

# ---- 10) AutoClaw 国内站 2 亿档：补 M10W4 与每日档现状 ----
REWRITE["`AutoClaw` 桌面端 v2.1.0 一次性 2 亿 Tokens"] = (
    "| ⚪ **`AutoClaw` 桌面端 v2.1.0 一次性 2 亿 Tokens（国内站 `zhipuai.cn` · **可领窗口已关闭**）** | "
    "**10/21（可领窗口截止）；奖励自领取成功起 7 天内有效** | "
    "⚪ **已结束（可领窗口 10/21 关闭 · 044 期已判，本期不变）**。"
    "**（045 期）本轮实访 `autoclaw.zhipuai.cn/blog/news/Weekly-Perks-M10W3/`（读于 2026-10-23）确认两档规则未变**："
    "**① `10.15–10.21` 任意一天登录领 2 亿 Tokens（20,000 积分），每账号限领一次，领取后 7 天有效；"
    "② `10.15–10.25` 每日登录，普通用户每日 `500` 积分、付费会员每日 `800` 积分（付费会员含连续包月订阅、"
    "`AutoClaw` 团购订阅及 `GLM Coding Plan` 个人套餐用户），每日限领一次**。"
    "**⚠️ 第②档今天（10/23）仍在窗口内，10/25 收口** —— **与第①档的「已结束」是两个日期，不要合并**（避坑 142 第二层："
    "「可领窗口」与「奖励有效期」是两件事）。"
    "**⚠️ 下一轮一次性档已公告且已降档**：**`M10W4` 为 10/26–11/1 一次性 **1 亿** Tokens（10,000 积分），"
    "**较本周的 2 亿少一半**（详见本表新增行；避坑 198）。"
    "**⚠️ 中间有四天空窗（10/22–10/25）没有一次性档**，**只有每日登录档** —— **官方未写每日档是否延续到 11/1 之后，"
    "本报告不替它续期**（避坑 154 / 161）。 |"
)

# ---- 11) MiniMax M3.1 Flash 发布行：补权重与定价 ----
REWRITE["🟢 **MiniMax `M3.1 Flash` 发布（10/19 · 国产 Flash 档输入压到 1 元/百万 tokens）**"] = (
    "| 🟢 **MiniMax `M3.1 Flash` 发布（10/19 · **权重已上 `HF` · 许可 `minimax-community`**）** | "
    "无结束日（**官方保留调价权；定价页未写任何免费额度或免费期**） | "
    "🟢 **生效中（官方博客 `minimax.io/blog/minimax-m31f`，页面标注 `2026-10-19`）**。"
    "**官方一手逐字**：「**Space Bunny 🐰, which processed more than 200 trillion tokens while operating anonymously, "
    "was an early version of MiniMax M3.1 Flash.**」「**As a next-generation Flash model, M3.1 Flash delivers a generational "
    "leap in agentic tasks, coding, Computer Use and cybersecurity, while making online inference nearly three times faster and "
    "reducing usage costs by 70%.**」"
    "**定价表（官方逐字）**：`MiniMax-M3.1-Flash` **输入 `$0.15` / 输出 `$0.60` / 缓存输入 `$0.015`（每 1M tokens）**。"
    "**基准（官方 README 逐字）**：`BankerToolBench` `76.2`、`DeepSWE v1.1` `73.7%`、`OSWorld V2` `61.7`、"
    "`Agents’ Last Exam` `29.6`、`CyberGym` `82.2`（README Highlights 段；`BabyVision (with tools)` `91.0`）。"
    "**⚠️ 上述基准全部是厂商自报，第三方复现未出**（避坑 116）；**`Artificial Analysis` 已于 10/19 独立评测该模型"
    "（其 Changelog 逐字 `New language model evaluation · 19 Oct — MiniMax-M3.1-Flash`），但本报告本轮未取到其指数分**。"
    "**⚠️ 规格（官方 README 逐字）**：**原生多模态 `MoE`；约 `428B` 总参 / 每 token 激活 `23B`；"
    "文本 + 图像 + 视频输入；上下文最高 `1M` tokens；`arXiv` 编号 `2606.13392`；"
    "`safetensors` + `mxfp8` 量化 + `custom_code`。**"
    "**⚠️ 官方博客对权重只写了一句**：「**M3.1 Flash is now available through the MiniMax API, M Plan, and MiniMax Code. "
    "Model weights will be released later.**」—— **「later」不是日期**；**权重实际落地情况见本表 `M3.1 Flash 开放权重` 那一行**。 |"
)

# ---- 12) OpenRouter 的 MiniMax free：10/22 收口（官方横幅第一次给确切结束日）----
REWRITE["🟢 **`OpenRouter` 的 `MiniMax M3.1 Flash (free)` 免费档（10/19 上线 · **官方模型页无任何截止日**）**"] = (
    "| ⚪ **`OpenRouter` 的 `MiniMax M3.1 Flash (free)` 免费档（10/19 上线 · **免费期已于 10/22 结束**）** | "
    "**10/22（官方横幅逐字 `The free launch period ended Oct 22, 2026.`）** | "
    "⚪ **已结束（本报告跟踪 `OpenRouter` 免费档以来，官方第一次给出确切结束日）**。"
    "**（045 期）本轮实访 `openrouter.ai/minimax/minimax-m3.1-flash:free`（读于 2026-10-23）**："
    "**页面顶部横幅逐字**：「**The free launch period ended Oct 22, 2026. MiniMax M3.1 Flash is now served at list price "
    "($0.15/M input, $0.60/M output, $0.015/M cached input).**」"
    "**⚠️ 一个必须写清的取料陷阱（本期新记，升格避坑 199）**：**同一个页面的字段区仍然写着 `Price` `Free`、"
    "`Context` `1.0M`、`Released` `Oct 19, 2026`，与横幅直接矛盾** —— "
    "**即「字段区写 Free、横幅写免费期已结束」同时出现在一页上。只读字段区会把它当成仍在免费；"
    "只读横幅会漏掉它曾经的规格。两个都必须读**。"
    "**⚠️ 官方 API 目录同步收口**：**`openrouter.ai/api/v1/models` 本轮实跑已不含 `minimax/minimax-m3.1-flash:free`，"
    "只剩付费档 `minimax/minimax-m3.1-flash`（`$0.15` / `$0.60` 每 1M）** —— "
    "**这就是 `OpenRouter` 官方目录 `:free` 由 `18` 降为 `17` 的那一个差额**（详见 `OpenRouter 免费档` 行）。"
    "**⚠️ 聚合站口径与一手源的关系本期反转**：**044 期记为「聚合站称免费 `72` 小时、约至 10/22 20:01，官方公告页未核到、"
    "故不采信」；本期官方横幅确认的结束日是 `10/22`（未给钟点）** —— "
    "**即聚合站的「日期」这次与官方一致，但「72 小时」与「20:01 钟点」仍无官方依据，本报告继续不采信这两项**（避坑 191："
    "猜对的日期不等于猜对的口径）。"
    "**⚠️ 该模型页另有两个既有字段本期仍成立**：`Not currently available through EU in-region routing.`；"
    "模型描述写 `It is an open-weight mixture-of-experts model with 23B active / 428B total parameters.`"
    "**⚠️ 「open-weight」这个词在 `OpenRouter` 页面上的含义与本报告第四章的许可口径不是一回事** —— "
    "**权重可下载 ≠ 可商用，见 `M3.1 Flash 开放权重` 行与避坑 197。** |"
)

# ---- 13) OpenCode 的 MiniMax free：同日收口 ----
REWRITE["🟢 **`OpenCode` 的 `MiniMax M3.1 Flash Free`（`limited time` · **两页均未给截止钟点**）**"] = (
    "| ⚪ **`OpenCode` 的 `MiniMax M3.1 Flash Free`（`limited time` · **已于 10/22 前后从两页下架**）** | "
    "**10/22（官方未给钟点；与 `OpenRouter` 同日收口，两边均未互相引用）** | "
    "⚪ **已结束（本轮两页实访，`M3.1 Flash Free` 字样计数为 `0`）**。"
    "**（045 期）本轮实访两页（读于 2026-10-23）**："
    "**① `opencode.ai/docs/go`（订阅页）** —— 模型列表里现在是 `MiniMax M3.1 Flash`（**无 `Free` 后缀、无 `(limited time)` 标注**），"
    "与 `MiniMax M3` 并列；"
    "**② `opencode.ai/docs/zen`（按量付费页）** —— `Free models` 说明段逐条列了 `GLM-5.3-Flash Free`、"
    "`DeepSeek V4.1 Flash Free`、`Exo Free`、`MiMo-V2.6-Flash Free`、`MiMo-V2.5 Free`、`Nemotron 3 Ultra Free`、"
    "`Nemotron 3.5 Lightning Free`、`Nemotron 3.5 Super VL Free`、`Big Pickle`、`Beam Free` —— "
    "**其中没有 `M3.1 Flash Free`（本轮全文检索 `M3.1 Flash Free` 命中 `0` 次）**。"
    "**⚠️ 本行的收口判据是「两页同时不再出现该免费档字样」，不是「官方公告」** —— "
    "**`OpenCode` 两侧都没有发布任何关于本条下架的说明**，**本报告因此不写「官方宣布结束」，只写「已从两页下架」**（避坑 154："
    "上游没给的不替它写）。"
    "**⚠️ 与 `OpenRouter` 的关系**：**两边同在 10/22 前后收口，但 `OpenRouter` 给了确切日期（`ended Oct 22, 2026`）、"
    "`OpenCode` 什么都没给** —— **本报告不把 `OpenRouter` 的日期借用到 `OpenCode` 这一行**（避坑 161："
    "同类源之间也要标口径；未核到 ≠ 不存在）。"
    "**⚠️ 044 期在本行记的三条结论（`Unlimited` 是聚合平台自估、留存口径落第一档、两页均未标 `limited regions`）"
    "随本条收口一并归档，本报告不重复往期已固化内容。** |"
)

# ---- 14) MiniMax M3.1 Flash 开放权重：本期最大的改写 ----
REWRITE["⚠️ **`MiniMax` `M3.1 Flash` 开放权重（10/19 宣布 · **第 ④ 级连续第 2 期未见**）**"] = (
    "| 🟢 **`MiniMax` `M3.1 Flash` 开放权重（**权重 10/17 就已在 `HF` · 043/044 两期判定「未见」是错的**）** | "
    "**无结束日（权重已公开，不是活动；但许可对商用有三条限制，见右列）** | "
    "🟢 **已开放权重（第 ④ 级已到）**。**⚠️ （045 期）这是本报告本期最大的一处自我纠错**："
    "**043 期与 044 期连续两期判定「权重未见」，根因是取数方法错误，不是厂商没发**（详见避坑 196）。"
    "**本轮一手实跑（`hf-mirror.com/api/models/MiniMaxAI/MiniMax-M3.1-Flash`，读于 2026-10-23）**："
    "`createdAt` **`2026-10-17T06:37:50.000Z`**、`lastModified` `2026-10-23T00:59:04.000Z`、"
    "`gated` **`false`**、`private` `false`、`license` **为空**（API 字段无值）、"
    "`downloads` `357`（详情端点）/ `1,096`（列表端点，**两个端点同一次读取给出两个数**，见下）、"
    "`likes` `2`、`siblings` `72` 个文件；"
    "`tags` 含 `transformers`、`safetensors`、`minimax_m3_vl`、`image-text-to-text`、`multimodal`、`moe`、`agent`、`coding`、"
    "`video`、`conversational`、`custom_code`、`arxiv:2606.13392`、**`license:other`**、`endpoints_compatible`、`8-bit`、"
    "`mxfp8`、`region:us`。"
    "**README 一手（`hf-mirror.com/MiniMaxAI/MiniMax-M3.1-Flash/raw/main/README.md`）逐字**："
    "`license: other`、`license_name: **minimax-community**`、`license_link: LICENSE`。"
    "**⚠️ `LICENSE` 正文一手（同路径 `raw/main/LICENSE`，3,363 字节）逐字三段**："
    "**① 非商用免费**：「**Permission is hereby granted, free of charge, to any person obtaining a copy of this software … "
    "to deal in the Software for non-commercial purposes**」；"
    "**② 商用两条义务**：「**you shall prominently display “Built with MiniMax M3.1-Flash” on a related website, user interface, "
    "blogpost, about page or product documentation.**」且「**you shall obtain a separate, prior written authorization from MiniMax "
    "by contacting api@minimax.io with the subject line “M3.1-Flash licensing - authorization request”, if such products and "
    "services generate more than 20 million US dollars (or equivalent in other currencies) in yearly revenue; otherwise, "
    "you only need to send a one-time notice to api@minimax.io with the subject “M3.1-Flash licensing — notice”.**」"
    "**③ `Commercial Use` 定义极宽**：「**…which includes, without limitation: (i) offering products or services to third parties "
    "for a fee, which utilize, incorporate, or rely on the Software or its derivatives, (ii) the commercial use of APIs provided "
    "by or for the Software or its derivatives … and (iii) the deployment or provision of the Software or its derivatives that "
    "have been subjected to post-training, fine-tuning, instruction-tuning, or any other form of modification, for any commercial "
    "purpose.**」**附录另有 5 条禁止用途（违法内容 / 军事目的 / 伤害未成年人 / 有意致害的虚假误导信息 / 歧视与仇恨言论）**。"
    "**⚠️ 避坑 197 的三条结论**：**① 「权重可下载」（`gated: false`、72 个文件）≠ 「可商用」** —— "
    "**这是一个「非商用免费 + 商用需标注 + 年收入超 2,000 万美元需书面授权」的自定义许可，不是开源许可**"
    "（**与 031 期 `Nace AI Drex 1.5` 的 `Open RAIL-M` 变体同族，避坑 135/139**）；"
    "**② `HF` API 的 `license` 字段为空而 `tags` 里有 `license:other`、README 里写 `license_name: minimax-community`** —— "
    "**三个位置三个写法，判许可必须读 `LICENSE` 正文，不能读 API 字段**（避坑 139 的加强版）；"
    "**③ 「`region:us`」这个 tag 的含义官方未解释，本报告不代官方解读**。"
    "**⚠️ 一条本报告自己抓到的口径不一致（如实记）**：**同一次读取中，列表端点给 `downloads = 1,096`、"
    "详情端点给 `downloads = 357`** —— **本报告两个数都写、不取其中一个**（避坑 161）；"
    "**对照：同期 `MiniMax-H3` 的列表与详情端点都给 `5,011,999`（044 期为 `5,007,397`，升 `4,602`）** —— "
    "**即「两个端点不一致」不是系统性的，只在这一个仓库上出现，最可能的解释是仓库刚公开、两侧缓存不同步，但本报告不断言**。"
    "**⚠️ 043/044 两期错在哪（避坑 196，本期新立）**：**两期都用 `hf-mirror.com/api/models?author=MiniMaxAI&limit=100` "
    "（默认排序）取组织页，得到 `21` 个仓库、其中无任何 `M3.1`**；"
    "**本轮同一 URL 加 `&sort=createdAt&direction=-1` 后返回 `22` 个仓库，`MiniMaxAI/MiniMax-M3.1-Flash` 排在第 1 位**。"
    "**同一 URL、同一 `limit=100`、只差排序参数，差一个仓库 —— 本轮两种排序各实跑两次，结果可复现**。"
    "**结论：否证「某仓库不存在」只能用「直接取该仓库详情」这一种办法；用「列表里没有」否证，会把取数缺陷当成事实**。"
    "**⚠️ 顺带纠正 044 期的一处推论**：**044 期写「`21` 个仓库里没有任何 `M3.1` 或 `M3.1-Flash`」—— "
    "这句话在它自己的取数口径内是对的，但作为「权重未见」的结论是错的**（避坑 100：计数与明细必须同源；"
    "本期进一步要求：**结论与取数方法也必须同源**）。"
    "**⚠️ 生态侧（第三方量化版，仅登记存在性）**：**本轮 `HF` 检索 `M3.1` 命中 `30` 个仓库，"
    "其中第三方量化/移植版在 10/23 当天批量出现**（`unsloth/MiniMax-M3.1-Flash` 04:17 UTC、"
    "`unsloth/MiniMax-M3.1-Flash-GGUF` 04:20 UTC、`mlx-community/MiniMax-M3.1-Flash-Text-4bit` 01:43 UTC、"
    "`mlx-community/…-oQ4e-mtp` / `-oQ3.5e-mtp` / `-oQ3e-mtp` 03:00–03:02 UTC、"
    "`AMAImedia/MiniMax-M3.1-Flash-NVFP4-GGUF` 05:13 UTC、`Mia-AiLab/…-EXL3-EAQ-v1-3.06bpw` 05:43 UTC、"
    "`vcruz305/…-EXL3-SAGE-2.15bpw` 03:43 UTC、`ArkhAngelLifeJiggy/MiniMax-M3.1-Flash` 06:00 UTC），"
    "**另有 `amd/…-Quark-MXFP4`（10/18）、`FlagRelease/…-W8A8-*` 系列（10/19，覆盖 `hygon`/`metax`/`ascend`/`mthreads`/"
    "`iluvatar`/`kunlunxin`/`tsingmicro`/`zhenwu`/`nvidia` 国产与商用卡）、`incoai/…-DFlash2`（10/19）、"
    "`RadixArk/Minimax-M3.1-Flash-Dflash2`（10/22）**。"
    "**⚠️ 这些第三方仓库的许可与可用性本报告一律不代判**（避坑 135/139）；**它们的存在只能说明「权重确实已可下载」，"
    "不能说明「许可能商用」**。 |"
)

# ---- 15) 腾讯元器：一行四个日期，脚本只解析得到第一个，必须逐行手算 ----
REWRITE["🔴 **腾讯智能体平台「元器」停止服务（040 期最高优先级运维项）**"] = (
    "| 🔴 **腾讯智能体平台「元器」停止服务（040 期最高优先级运维项）** | "
    "**11/9（停服）；10/29（停止新建）；2027 年 1 月 9 日（数据导出截止）** | "
    "🔴 **倒计时中，四个日期必须分开排（045 期逐行手算，不用脚本）**。"
    "**⚠️ 本行是「脚本解析不到状态列倒计时」的标准样本（`extract_deadlines` 不解析状态列，故本行不进 `deadlines.csv` 的重算集）**："
    "**截止列里有三个日期，而状态列里有三个独立的「距今」——脚本的 `DAYS_RE.sub` 会把三个数全部替换成截止列第一个日期算出的同一个值**。"
    "**因此本行在 045 期改为显式 `REWRITE`，四个日期按基准日 10/23 逐条手算**："
    "**① `10/29` 起不再支持新建智能体与分发 API Key（**距今 6 天**）；"
    "**② `11/9` 平台停止全部服务（**距今 17 天**）；"
    "**③ 数据导出窗口开到 `2027 年 1 月 9 日`（**距今 78 天** —— ⚠️ **比停服日晚两个月，这是最容易漏掉的一个日期**）；"
    "**④ 本报告自设的倒排基准日不变。**"
    "**⚠️ 与 044 期的 diff（逐条对得上才写）**：**044 期该行写 `11 / 22 / 83`（基准日 10/22），"
    "**而按 10/22 真值应为 `7 / 18 / 79`** —— **即这三个数在 044 期就已经与截止列脱钩，本期一并纠正**（避坑 027："
    "**继承字段必须重算，且「每行 −1」不等于重算通过**）。"
    "**⚠️ 官方公告口径不变**：**平台将于 2026-11-09 停止服务；停服生效后所创建智能体不再可用；"
    "平台访问、数据读写、API 调用、后台控制台全部关闭；发布到公众号、微信客服等渠道的智能体也停止响应用户对话。**"
    "**迁移方案**：**官方推荐迁往腾讯云智能体开发平台 `ADP`** —— **官方称元器上的主要玩法均可延续"
    "（标准模式 / Multi-Agent / 单工作流），并支持更灵活的 `Claw` 模式。"
    "**⚠️ 定位差异**：`元器` 偏 C 端、主要与「元宝」结合；**`ADP` 面向 B 端企业级平台**。"
    "**⚠️ 本行量级高于任何额度到期（避坑 164）**：**「优惠窗口结束」损失的是钱，「平台停服」损失的是存在本身。** |"
)

# ---- 16) ZCode / BigModel：域名已成停车站 ----
REWRITE["**ZCode / BigModel 新用户试用**"] = (    "| ⚪ **ZCode / BigModel 新用户试用** | 连接 BigModel 账号后起算，第 5 天到期 | "
    "⚪ **登记项已失效（域名变更，非活动截止）**。"
    "**（045 期）本轮实访 `zcode.ai/`**：**返回 `1,043,615` 字节，但正文是体育博彩类停放页内容**"
    "（页面标题与正文均与 AI 编程工具无关，出现 `AI + Sports Betting`、`sports betting revolution` 等字样）—— "
    "**即该域名已易主/停放，不再是本报告 026 期起跟踪的那个 `ZCode` 产品**。"
    "**⚠️ 本行的处置**：**状态列改为「登记项已失效（域名变更）」而不是「已结束」** —— "
    "**「活动到期」与「产品消失」是两件不同的事，混写会让读者以为厂商正常收口**（避坑 198 同族："
    "**降档/收口/消失三种形态必须分开写**）。"
    "**⚠️ `ZCode 月报连续第 19 期未见`这条待办本期有了新解释**：**不是厂商没发月报，是域名已经没有了** —— "
    "**本报告因此把这条待办从「等月报」改为「等域名/产品是否重新上线」，并不再每期重复记为「未见」**。"
    "**⚠️ 与 `智谱 ZCode 免费额度包`那一行（⚪，10/7 截止）的关系**：**两行是同一个产品的两个阶段，均随域名变更失效**。 |"
)

out = body[:]
rw = 0
for key, val in REWRITE.items():
    hit = [i for i, l in enumerate(out) if key in l]
    assert len(hit) == 1, ("REWRITE 键未恰好命中 1 行", key, len(hit))
    out[hit[0]] = val
    rw += 1

DAYS_RE = re.compile(r"\*\*距今 (\d+) 天\*\*")


def parse_cut(l):
    cells = l.split("|")
    if len(cells) < 3:
        return None
    cut = cells[2]
    import datetime as _dt
    for m in re.finditer(r"(20\d{2})-(\d{2})-(\d{2})", cut):
        try:
            return _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            continue
    for m in re.finditer(r"(?<!\d)(\d{1,2})/(\d{1,2})(?!\d)", cut):
        mo, da = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12 and 1 <= da <= 31:
            try:
                return _dt.date(2026, mo, da)
            except ValueError:
                continue
    return None


def recompute(l):
    if "距今" not in l:
        return l
    d = parse_cut(l)
    if d is None:
        return l
    return DAYS_RE.sub("**距今 %d 天**" % (d - BASE).days, l)


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

bad = []
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
