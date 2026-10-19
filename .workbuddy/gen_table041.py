# -*- coding: utf-8 -*-
"""从 040 期 md 提取第四章截止表 -> 基准日 2026-10-19 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table041.md（纯表格块，供 041 期正文嵌入）。

六步（027 期定做法、028 期定型；041 期第十六次落地）：
  1) 先断言行数（040 期 body = 206）
  2) 按行名子串套 REWRITE 字典（每键必须恰好命中 1 次）
  3) 正则重算每一行的「距今 N 天」（基准日 10/19 -> 与 040 期不同，全部按真值重算）
  4) 未 REWRITE 的行做归属化（「本期」-> 「040 期」）
  5) 新行插在 ⚪ 存档块（首行 "| ⚪ **DeepSeek 10/15"）之前 -> 再断言总数
  6) 输出后由 inject041.py 注入正文占位符

⚠️ **040 期立的两条脚本纪律本期继续生效**：
   ① 断言口径是「每行天数 == 其截止日 − 基准日」，**不是「−1」**（继承误差逐期滚雪球）；
   ② **REWRITE 命中的行不再过 recompute**（否则含多日期的截止列会被取到错误日期并覆盖整行）。
⚠️ **截止列纪律**：真截止日才写可解析 `M/D`；换挡日/登记启动日/权重交付日一律写不可解析形态。
   「限时免费」没有结束日时写「未公布」（避坑 154/166）。
⚠️ **本期核心变化**：Together AI 促销行已于 10/18 到期并从页面撤下（040 期遗留动作③兑现）；
   DeepSeek Search/Fetch 免费窗口进入倒计时第 13 天；WorkBuddy Intl 限免剩 12 天；
   **本期新增 6 行**，其中 2 行是 040 期全漏登的补登（Bolt Builders Week 免费周末 / OpenAI Rosalind 学术计划）。
"""
import re
from datetime import date

SRC = "AI免费内容与权益速递-第040期-2026-10-18.md"
OUT = ".workbuddy/tmp_table041.md"
BASE = date(2026, 10, 19)
PREV = 206

lines = open(SRC, encoding="utf-8").read().split("\n")
s = e = None
for i, l in enumerate(lines):
    if l.startswith("## 四、"):
        s = i
    if s is not None and l.startswith("## 五、"):
        e = i
        break
rows = [l for l in lines[s:e] if l.startswith("|")]
header, sep, body = rows[0], rows[1], rows[2:]
assert len(body) == PREV, len(body)

REWRITE = {}

# ---- ① 老混元：Q04 连续第 29 期 + 高危窗口第 19 天 ----
REWRITE["腾讯老混元大模型平台停服"] = (
    "| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必须迁移到 TokenHub**。**10/19 高危窗口第 19 天**"
    "（9/25 自设倒排日已过 **24 天**；Q04 **连续第 29 期**未见确切日期，厂商只给「9 月底」）。"
    "⚠️ **一条「9 月底停服」拖到 10 月中下旬仍无日期，处置维持「按已停服对待、只做迁移」**——迁移动作本身不要等；"
    "⚠️ **同一家厂商两条线，一条无日期一条有精确到日的倒排**（元器 11/9，见下表），"
    "**说明「无日期」不是这家厂商的常态，而是这条线的常态**（避坑 164） |"
)

# ---- ② Together AI：促销行已撤下（040 期遗留动作③兑现）----
REWRITE["Together AI `Muse Spark Open` 限免"] = (
    "| ⚪ **Together AI `Muse Spark Open` 限免（促销行已撤下）** | **10/18** | ⚪ **已收口（**本轮 10/19 实访确认促销行已从页面撤下**）**。"
    "**040 期记的「促销行标 `PROMO`、`Promotion valid until 10/18/2026`、价格 `$1.00 / $0.00 / $5.00`」在 10/19 的页面上已不存在** —— "
    "`Muse Spark Open` **只剩常规行：输入 `$1.25` / 缓存读 `$0.15` / 输出 `$4.25`**，页面上无 `PROMO` 标记、无 `until` 字样。"
    "⚠️ **本期新立的一条读法（040 期的记录没错、错在没说清收尾方式）**："
    "**官方给的 `Promotion valid until` 这个字段，语义是「有效期至」，而实测行为是「到期即从页面移除」** —— "
    "**即官方给的截止日 ≠ 截止后还能在页面上看到它**（避坑 177 补一层）。"
    "⚠️ **040 期新立的那条避坑（促销行的输出 `$5.00` 比常规行 `$4.25` 贵约 18%）所描述的状态本期已结束**，"
    "**但纪律继续有效 —— 下一次任何促销行出现时仍要两读**。"
    "⚠️ **本行记的是「促销窗口的收口」，不是「`Muse Spark Open` 下线」** —— 该模型在 `Together AI` 仍按常规价可调用（避坑 154）。"
    "⚠️ **到期后是否续期，本轮未见公告** —— 按避坑 78「无信号即默认收口」处理 |"
)

# ---- ③ DeepSeek Search / Fetch：免费窗口倒计时推进 + UTC 口径差两说并列 ----
REWRITE["`DeepSeek Search` / `Fetch` 两个 API 开放"] = (
    "| 🟡 **`DeepSeek Search` / `Fetch` 两个 API 开放（10/17 · 服务端调用免费到 11/1）** | "
    "**11/1 00:00（北京）起按请求计费** | 🟡 **生效中（免费窗口距今 13 天）**。"
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
    "**⚠️ （041 期）截止时点存在两个口径，本期两说并列、不取中间值**："
    "**官方文档写「北京时间 2026 年 11 月 1 日 00:00」；而 `The Decoder` 的报道写「until November 1, 2026 "
    "(or **October 31, 2026 at 4:00 PM UTC** per The Decoder)」—— 两个时点相差 8 小时**"
    "（北京 11/1 00:00 = UTC 10/31 16:00）。⚠️ **本报告以官方文档为准，同时保留媒体口径并标明来源**（避坑 161）。"
    "⚠️ **速率限制**：**Search 与 Fetch 各自独立、各 QPS 5、按账户级计（无论用哪个 key）、互不消耗对方配额；"
    "`Fetch` 另受按域名的 QPS 限制；超限返回 HTTP 429**。"
    "**⚠️ 对内容生成最要紧的三个响应字段**：`rerank_score` **0–3、≥1.5 视为高质量**（唯一可程序化判定的质量档）；"
    "`summary` **600–800 字符、面向模型**（`snippet` 是 100–200 字符、面向 UI，两者不是同一字段的截断版）；"
    "`content` 为页面 Markdown 全文、`need_content=false` 时恒为空字符串、且 `count` 不影响单价。"
    "**⚠️ 一条不能靠重试解决的失败**：`404` 表示无法取到可用页面内容（不可用 / 被站点策略拦截 / 目标站报错 / "
    "不支持的内容类型 / 无可提取 Markdown）—— **索引里有 ≠ 抓得到**。**⚠️ （041 期）回扫**：`api-docs.deepseek.com/updates` "
    "**本轮实访确认 10/18 与 10/19 均无新条目**，最新仍是 10/17 的两条 |"
)

# ---- ④ WorkBuddy Intl 限免：倒计时推进到 12 天 ----
REWRITE["`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免"] = (
    "| 🟢 **`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免（10/31）** | **10/31** | 🟢 **生效中（距今 12 天）**。"
    "**官方原文两句（`WorkBuddy` 官方 X，10/17 18:29）**：「新的 `DeepSeek` 刚刚发布。`WorkBuddy Intl` 也已更新到最新版本，"
    "**并且在 10 月 31 日前免费**。来试试看吧。」⚠️ **四条登记纪律**："
    "**① 主体是 `WorkBuddy Intl`（国际版），不是国内版 —— 本工作区的产品线在国内站与国际站是两套口径，不可互相代入**；"
    "**② 官方原文没有写额度上限、没有写适用账号范围、没有写结束后的价格** —— "
    "**即这三条字段全部缺失，只能按「有限时免费、无从判断能用多少」来规划**（避坑 41 第一层）；"
    "**③ 限免的标的是「已更新到最新版本」这件事，而不是某个模型名 —— 即换新版本后是否仍免费，官方原文没有回答**（避坑 166）；"
    "**④ 本行是「工作区自有产品公告」，与厂商公告分开放，避免被当成厂商口径**（避坑 126）。"
    "**⚠️ （041 期）回扫**：本轮未见续期或提前收口的公告，按避坑 78「无信号即默认维持」处理 |"
)

# ---- ⑤ OpenCode 地区限制清单：本轮实访只有 beam-free 一行带限制 ----
REWRITE["**`OpenCode` 的地区限制清单"] = (
    "| 🟡 **`OpenCode` 的地区限制清单（`Beam Free` 等 · 本期起读法改变）** | 未公布（长期，随供应商变动） | 🟢 生效中"
    "（**清单本身不是活动，是产品事实**）。**（041 期）回扫结果：`docs/zen` 本轮实访 13 条 `Free` 条目，"
    "其中**只有 `beam-free` 一条带地区限制**，不可用地区仍为 18 国 + 乌克兰 3 个地区、明确含「China (including Hong Kong and Macau)」。"
    "⚠️ **本期新立的一条纪律（避坑 181）**：**同页其余 12 条免费条目在页面上没有地区限制标注 —— "
    "「页面没写」不等于「没有限制」，必须逐行读、不可按整页推断**。**即读者看到同一页 12 条没有限制、"
    "不能推断第 13 条也没有 —— 而事实正相反**。"
    "⚠️ **041 期本轮实访的三条结构性事实（比「增减几条」更有用）**："
    "**① 免费档的留存口径在同一页上分四档** —— 零留存 + 不训练（`glm-5.3-flash-free` / `deepseek-v4.1-flash-free` / "
    "`space-bunny-free` / `longcat-2.5-preview-free`）、不训练但因安全原因保留 30 天（`beam-free`）、"
    "收集的数据可能用于改进模型（`ll-alpha-free` / `exo-free` / `mimo-v2.6-flash-free` / `mimo-v2.5-free`）、"
    "`NVIDIA` 免费试用端点且数据记录用于安全与改进产品（`nemotron-3-ultra-free` / `nemotron-3.5-lightning-free` / "
    "`nemotron-3.5-super-vl-free`）—— **同平台的免费模型之间留存口径不可互推**（避坑 171/172 同族）。"
    "**② 该页不提供免费档的上下文长度，也不提供任何限速（`RPM` / `TPM` / 并发 / 每日次数）** —— "
    "**凡引用本页的免费条目，都不能同时给出「1M 上下文」或「每天 N 次」这类数字，除非另有一手源**。"
    "**③ 13 条免费条目逐条为**：`big-pickle`（stealth model）、`glm-5.3-flash-free`、`deepseek-v4.1-flash-free`、"
    "`space-bunny-free`、`beam-free`、`ll-alpha-free`、`longcat-2.5-preview-free`、`exo-free`、"
    "`mimo-v2.6-flash-free`、`mimo-v2.5-free`、`nemotron-3-ultra-free`、`nemotron-3.5-lightning-free`、"
    "`nemotron-3.5-super-vl-free`。"
    "**⚠️ 039 / 040 两期记的是 15 条、但那两期正文未逐条列出，故本期无法逐条 diff 出哪两条新增、哪两条下架** —— "
    "**本期只按实访登记全部 13 条 slug，下期起可逐条 diff**（避坑 100 同族：**计数与明细必须同源**）。"
    "**⚠️ 另一条独立事实（040 期登记，本期维持）**：**`docs/go` 上「`DeepSeek`: ZDR agreement is **renewed monthly**. "
    "The current agreement is valid through **October 31, 2026**」—— 被归为「零留存」的那一批模型，"
    "其留存口径本身带一个 10/31 的复签节点，不是一个静态承诺**。"
    "**⚠️ 平台侧的安全事件（040 期头条，本期状态推进，见三章）**："
    "**攻击面已定位为「正在停用流程中的一套旧系统」，且官方明确「正在与相关 AI 服务商讨论异常费用的退款问题，"
    "但尚未作出退款承诺」** —— **「零留存」与「凭证安全」仍是两个独立闸门**（避坑 175） |"
)

NEW = [
    # ---- 新行 1：AutoClaw 第三期（本轮头条 · 同 URL 内容被改写）----
    "| 🟢 **智谱 `AutoClaw` 第三期每日登录送 Token（10/19–10/25 · **本轮头条**）** | "
    "**10/25（活动期末日）** | 🟢 **生效中（活动期末日距今 6 天 · **⚠️ 每档当天 24:00（北京）即过期，见下**）**。"
    "**官方页实测（`autoclaw.z.ai/blog/news/M10W3`，读于 2026-10-19）**：`Event Period: Oct 19 – Oct 25 (UTC+8)`；"
    "**`Oct 19-20 (Monday–Tuesday)` 每天领 `3,000 credits (30M tokens)`；"
    "**`Oct 21–25 (Wednesday–Sunday)` 每天领 `500 credits (5M tokens)`；**每档 `Expires at 24:00 (UTC+8) the same day`。"
    "**换算**：`1 credit = 1 万 tokens`；**总量 85M = 30M×2 + 5M×5**。"
    "**⚠️ 本行是本报告第一次登记的条目类型「同 URL 内容被官方就地改写」**："
    "**同一个 URL、发布日期未变、活动期 Oct 19–25 未变，但正文规则与标题总量都变了** —— "
    "**10/16 发布版是 `Get 60M Tokens`（`Oct 19` 单日 3000 万、`Oct 20–25` 每天 500 万）；"
    "本轮实访是 `Get 85M Tokens`（`Oct 19–20` 每天 3000 万、`Oct 21–25` 每天 500 万）**。"
    "**而中文媒体 10/18 20:00 的截图转述仍写「只在 10/19 当天有效」「后天 3000 万那一档也已经过去了」"
    "—— 与本轮实访的官方版本直接冲突**（避坑 179）。"
    "**⚠️ 为什么难发现**：**新旧两版各自自洽** —— `30M + 5M×6 = 60M` 与 `30M×2 + 5M×5 = 85M` 都对得上自己的规则表，"
    "**验算能排除「笔误」，排除不了「过期」**。"
    "**⚠️ 领取资格（官方页口径）**：**登录即领、不分新老用户、无邀请奖励；官方页只列一档**。"
    "⚠️ **中文媒体广泛转述的「付费会员另有额外每日奖励（按会员档位解锁）」在本期这一档的官方页上没有** —— "
    "**但上一档（`Weekly-Perks-M10W2`，活动期 10/12–10/16，132M Tokens）确实有**（官方页逐字："
    "「Paid members can also unlock an additional daily reward based on their active membership tier」）—— "
    "**即同一句话从「真」变成「没有」而不改活动期，这是最容易当成漏写的地方**（避坑 179）。"
    "**⚠️ 与上一档是无缝接档、但不可比大小**：**上一档 132M、这一档 85M，且 10/17–10/18 两天无活动**"
    "（避坑 140 第一层：**「无缝续期」≠「同一活动」，额度量纲变了不可直接比**）。"
    "**⚠️ 「当天清零」型不可当存款**：**领了当天 24:00（北京）就过期、错过不补** —— "
    "**与 9/28、9/30 两期「开放平台新用户礼包、领了能放一阵」不是同一件事**（避坑 117 同族）；"
    "**官方页未写各模型扣多少 credits，本报告不代官方换算**（避坑 41 第一层）。"
    "**⚠️ 另有一档并存的一次性活动**：`AutoClaw` 桌面端 v2.1.0 版本福利为 **10/15–10/21 之间任意一天登录领 2 亿 Tokens**"
    "（`20000` 积分）、**每账号限领一次、领到手只有 7 天有效期**（⚠️ **一手页本轮未核到，为中文媒体口径**）—— "
    "**它与本行是两套不同活动、不可合并**：**前者一次性大额 + 7 天有效、后者每天小额 + 当天清零** |",

    # ---- 新行 2：Bolt Builders Week 免费周末（040 期全漏登 · 补登 · 窗口内到期）----
    "| ⚪ **`Bolt` Builders Week 免费周末（10/17–10/18 PT · **040 期全漏登，本期补登**）** | "
    "**10/18 23:59 PT（＝北京 10/19 14:59）** | ⚪ **已收口（**本轮出刊时点 10/19 18:00（北京）已过期**）**。"
    "**官方 X 原文（`@boltdotnew`，经中文聚合站逐字转述）**：「**Bolt is free for EVERYONE for an ENTIRE weekend.** "
    "And you could win $10K! Introducing the Builders Week challenge. **Build all weekend Oct 17 + 18. "
    "Turn your idea into a product, and submit by Oct 20.**」"
    "**⚠️ 六条必须一起读的事实**："
    "**① 时间窗按美西日历写、对北京读者跨了一整天**：**10/17 00:00 PT 起 → 10/18 23:59 PT 止 = 北京 10/17 15:00 → 10/19 14:59**"
    "（避坑 142 第三层：**厂商按自己的时区写截止日**）。"
    "**② 免费的是模型不是全站**：`GLM 5.3 Flash` 在模型选择器里对所有 `Bolt` 账号免费、**不需换套餐、不需兑换码**；"
    "⚠️ **它走 `Bolt Forge`（只用开放权重模型的 agent），不是 `Standard` / `Max` 两个自带 agent**。"
    "**③ 额度以六小时分块发放、不结转**：**块在你打开 `Bolt` 时开始、结束后你的下次访问开启新块**；"
    "**未用完的免费额度不结转到下一块**；**付费档每块的额度是免费档的 5 倍**；"
    "⚠️ **`Bolt` 未公布每块具体多少 token**（避坑 41 第一层）。"
    "**48 小时的周末最多只装得下 8 个六小时块，且必须每块一结束就立刻开始下一块（含过夜）—— 任何离开都会把后面的块整体后移**。"
    "**④ 正常档位是另一笔账**：`Bolt.new` 免费档平时是**每天 300,000 tokens、每月上限 100 万**，"
    "**免费周末的 `GLM 5.3 Flash` 用量不从这个额度里扣**（避坑 117 同族：**活动额度与基础额度是两笔**）。"
    "**⑤ 同期竞赛是另一条时间线**：**投稿截止 10/20 23:59 PT = 北京 10/21 14:59**；"
    "**奖金 `$10,000` / `$5,000` / `$2,500`，合计 `$17,500`**，**一等奖另含与 `Bolt` CEO `Eric Simons` 的一对一辅导**；"
    "**评审四项等权**（`Bolt` 使用度 / 想法 / 实现与设计 / 潜在影响）；**免费档即可参赛、付费档不加分**。"
    "**⑥ ⚠️ 竞赛的地区排除名单明确含中国大陆**：**规则排除在美国或当地法律禁止参与的地区，"
    "包括巴西、**中国**、克里米亚、顿涅茨克与卢甘斯克地区、古巴、伊朗、朝鲜、魁北克、俄罗斯、叙利亚** —— "
    "**即「免费周末可参与」与「竞赛可获奖」是两个地域资格**（避坑 161/181）。"
    "**⚠️ 一条本报告此前从未写过的数据条款（二手口径，⚠️ 未在 `Bolt` 官方页取到一手表述）**："
    "**`Bolt Forge` 的条款写明，提示词、代码与项目文件的去标识化版本会用于训练开放权重模型，EEA / 英国 / 瑞士的会话除外**；"
    "⚠️ **且 `Bolt` 账号设置里的「Model training」开关默认开启（EU / 英国 / 瑞士以外），覆盖 2026-10-07 起创建的内容，"
    "但该开关管不到 `Forge`** —— **「关掉了训练开关」并不等于 `Forge` 会话不被训练**（避坑 162 同族：**闸门要逐个产品查**）。"
    "**⚠️ 本行取料面极窄（避坑 143）**：`bolt.new` 站内页面本轮实访未取到 Builders Week 内容页"
    "（`/blog/builders-week` 返回产品首页、`support.bolt.new/Builders-Week` 返回 404），"
    "**官方 X 只给了三句核心信息，其余细则均来自第三方规则整理站** |",

    # ---- 新行 3：OpenAI Rosalind 学术计划（040 期全漏登 · 补登 · 有免费期限无申请截止）----
    "| 🟢 **`OpenAI` `Rosalind Academic Plan`（**040 期全漏登，本期补登** · **无申请截止日，故本行不进截止倒计时**）** | "
    "未公布（**免费额度期限最长 12 个月，但官方页无申请截止日** —— 两者不可互推，见下） | "
    "🟢 **生效中（公告日 10/15；审批制、无名额上限说明）**。"
    "**官方公告逐字字段**："
    "**① 面向谁**：「academic labs at **U.S. universities**」（**不是面向学生个人**）；"
    "**② 给什么**：「**Up to 30 Business Standard seats at `$0 per user per month` for up to `12 months`**」；"
    "**③ 怎么拿**：「PIs and lab leads at universities **without an OpenAI Enterprise agreement** can apply on behalf of their labs "
    "through our trusted access process」；**已有 Enterprise 协议的学校必须走学校自己的 Enterprise 渠道**；"
    "**④ 审批查什么**：机构合法性、PI 身份与专业背景、机构任命与授权、实验室的机构隶属与预期用途、"
    "**并要求指定机构安全联系人**；"
    "**⑤ 数据**：「Research data shared through the Rosalind Academic Plan is **not used to train our models by default**」；"
    "**⑥ API**：「**API access is not included at this time.**」；"
    "**⑦ 其他模型**：「Access to all commercially available frontier OpenAI models, **subject to plan usage limits**」。"
    "**⚠️ 四条读法（本期新增避坑 182）**："
    "**① 「免费最长 12 个月」是额度期限、不是申请期限** —— **官方页既没写申请截止日，也没写名额上限或「先到先得」，"
    "所以不能据此判断「现在申请还赶得上」**；**「没有申请截止日」≠「可以慢慢来」**（避坑 142 第二层：**每个日期都要问它是哪一种**）。"
    "**② 「席位可用」不等于「能调 API」** —— 官方逐字排除 API，**对做研究流水线的人是硬闸门：拿不到 API 就只能人工用界面**。"
    "**③ 申请主体是实验室负责人、不是学生** —— 学生能否用**取决于其所在实验室是否获批、以及获批负责人是否把席位给到该学生**"
    "（30 个 named members 的分配权在实验室负责人手里）。"
    "**④ 审批含「指定机构安全联系人」这一条** —— **这是前置条件而不是事后追责**，"
    "**即实验室要先在机构内安排一个人承担该角色，才可能提交**（避坑 41 第二层：能否跑起来）。"
    "**⚠️ 不可与 `Anthropic` 10/18 公告里的那句混为一谈**：**后者写「discounts on Claude for nonprofits and scientific institutions」"
    "但未给折扣幅度、是否完全免费、适用地区、申请条件与有效期 —— 字段全空，不可用**（避坑 161） |",

    # ---- 新行 4：AutoClaw 桌面端 v2.1.0 的一次性 2 亿额度 ----
    "| 🟡 **`AutoClaw` 桌面端 v2.1.0 一次性 2 亿 Tokens（10/21 截止 · ⚠️ **一手页本轮未核到**）** | "
    "**10/21** | 🟡 **生效中（距今 2 天）**。"
    "**口径（中文媒体转述版本公告，⚠️ 未在 `autoclaw.z.ai/blog/news` 列表页核到该条一手页）**："
    "**10/15–10/21 之间任意一天登录 `AutoClaw` 桌面端即可领 2 亿 Tokens（`20000` 积分）**；"
    "**每账号限领一次**；⚠️ **领到手只有 7 天有效期，过期作废、不补**。"
    "**⚠️ 与本表 `AutoClaw` 第三期每日登录那条是两套不同活动、不可合并**："
    "**本行是一次性大额 + 7 天有效、每日登录那档是每天小额 + 当天清零** —— "
    "**「一次性领 2 亿然后 7 天烧完」与「每天领 500 万连领 7 天」是两种完全不同的用法**，"
    "前者适合这几天正好有大活要跑的人（避坑 140 第一层：**同厂商不同活动不可比大小**）。"
    "**⚠️ 「可领窗口的末日」（10/21）与「领到手的有效期」（7 天）是两个日期** —— "
    "**10/21 之后不能再领，但 10/15 领的那份仍可用到 10/22 左右**（避坑 142 第二层）。"
    "**⚠️ 入口是桌面端（`autoclaw.zhipuai.cn`，Windows / Mac），与网页版 `autoclaw.z.ai` 不是同一个入口**；"
    "**国际版 `z.ai` 是另一套规则，别看混**（避坑 163：先确认免费的是哪一档、范围有多大） |",

    # ---- 新行 5：OpenCode 安全事件的处置状态（040 期头条的后续状态行）----
    "| 🟡 **`OpenCode` 安全事件处置状态（10/17 起 · 040 期头条，本期状态推进）** | 未公布（**官方明确「事件仍在处置中」，无修复完成时点**） | "
    "🟡 **进行中（**本轮从「定性」推进到「费用」，但**官方未承诺退款**）**。"
    "**官方通知邮件的三段口径（本轮由中文媒体转述邮件原文）**："
    "**① 攻击面（本轮新拿到）**：「OpenCode 发现一套**正在停用的旧系统**遭到未经授权访问，"
    "保存在用户工作区中的第三方 AI 服务 API 密钥**可能泄露**，包括 `OpenAI`、`Anthropic` 等服务商的密钥」；"
    "**② 范围与判据**：已通过电子邮件通知所有受影响用户，**未收到通知邮件的用户不在影响范围内**；"
    "**③ 费用与退款（本轮新拿到）**：「**目前尚无法确认相关密钥是否遭到恶意使用，初步调查也未发现其他数据泄露的证据**」；"
    "「**正在与相关 AI 服务商讨论异常费用的退款问题，但尚未作出退款承诺**」。"
    "**⚠️ 三个具体金额（全部是受影响用户自述，不是官方统计，必须标注口径）**："
    "**`Anthropic` 账户 400 美元非授权扣费**；**谷歌相关服务约 200 欧元意外费用、对应项目因滥用行为遭暂停**；"
    "**另一名用户在收到 `OpenCode` 通知的同时收到 `Anthropic` 异常使用预警、显示当月 20 美元 API 额度已耗尽**（避坑 116）。"
    "**⚠️ 「正在谈退款」与「会退」是两件事** —— 官方用词是 `discussing`，**本报告不写成「预计可退」**。"
    "**⚠️ 「未发现其他数据泄露的证据」是阴性结果、不是清白证明** —— **它只覆盖官方已检查的范围**（避坑 138 同族）。"
    "**⚠️ 攻击面已定位为「退役路径」，这改变了风险判读方向**：**平台主链路的密钥处理未必有问题，"
    "出问题的是退役流程** —— **对应的处置动作从「立刻轮换全部上游 key」收窄为「确认哪些工作区在旧系统上、"
    "以及退役清单是否清干净」**（避坑 175 的补充面）。"
    "**⚠️ 官方建议的动作本轮第一次成文可抄**：**通过服务商管理后台吊销并重新颁发密钥、更新使用这些密钥的应用、检查近期调用记录**；"
    "⚠️ **社区侧另有一条操作细节值得抄**：「**切勿点击泄露邮件中的链接**」—— "
    "**事故邮件是钓鱼的高发场景，这是「厂商公告」这一信源类型第一次带出反面操作提醒**。"
    "**⚠️ 责任主体本轮第一次拿到中文侧确认**：`OpenCode` 开发商为 **Anomaly Innovations（前身为 `SST`）** —— "
    "**「免费端点由谁提供」与「留存协议由谁签」决定出事时找谁**（避坑 175 补第三个字段：闸门的责任主体是谁）。"
    "**⚠️ 「正在处理中」这一状态没有截止日，因此本行不进任何倒计时**（避坑 166） |",

    # ---- 新行 6：德国法院对 Google AI Overview 的责任裁定（政策线 · 无截止日）----
    "| 🟡 **德国法院裁定 `Google` 须为 `AI Overview` 内容负责（10/18 报道 · 政策线）** | "
    "未公布（**已以和解结案、无后续时间表**） | 🟡 **已裁定但已和解（**不是终局判例**）**。"
    "**事实（`The Decoder` 10/18 19:49 逐字转述）**：「**慕尼黑地区法院 I 五月底裁定 `Google` 的 AI 搜索摘要"
    "属于公司自己的陈述而非中立转述，`Google` 须为错误内容担责**；`Google` 公开宣布上诉后"
    "**实际以和解结案，未获上级法院裁决**。」"
    "**⚠️ 引用时必须写三段、缺一段就变成一个不存在的判例**：**① 有一审裁定 ② 被告上诉 ③ 以和解结案、未获上级法院裁决** —— "
    "**只写 ① 是把和解说成败诉，只写 ③ 是把裁定说成无效**（避坑 116 同族）。"
    "**⚠️ 对本报告读者的间接意义**：「AI 摘要是不是中立转述」这一区分，"
    "会影响「能不能把 AI 生成的摘要当转述来源引用」—— **本报告在三章对 `Gemma 4 31B` 等两行列头未对齐的处理，"
    "正是同一类问题的最低限度版本（不核到就不判断）**。"
    "**⚠️ 归类**：本条登记为政策线事件，**无截止日故不进任何倒计时**，**也不改变任何厂商的免费额度** |",
]

# ---- 归属化：未 REWRITE 的行把「本期」改为「040 期」 ----
# ⚠️ **041 期实测抓到的一个脚本缺陷（此前 040 期脚本也有，040 期侥幸没暴露）**：
#    「断言命中数 == 1」并不等于「替换已生效」—— 断言只查 `k in l`，
#    若漏掉 `out = [REWRITE[...] ...]` 这一步替换，断言照样通过、输出照样是旧行。
#    **即：断言只能证明「键命中了目标行」，不能证明「值被写回去了」。**
#    本期新增一条自检：**替换后必须断言「REWRITE 的每个值都出现在 out 里」**。
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
    out.append(l.replace("**本期", "**040 期").replace("（本期", "（040 期"))

rw = 0
for k, v in REWRITE.items():
    hits = sum(1 for l in out if k in l)
    assert hits == 1, (k, hits)
    assert v in out, ("REWRITE 的值未出现在输出里 —— 替换步骤缺失", k)
    rw += 1

DAYS_RE = re.compile(r"(?:\*\*)?距今 (-?\d+) 天(?:\*\*)?")
DATE_FULL = re.compile(r"\*\*(\d{4})-(\d{1,2})-(\d{1,2})\*\*")
DATE_MD = re.compile(r"\*\*(\d{1,2})/(\d{1,2})\*\*")

def parse_cut(l):
    cols = l.split("|")
    target = cols[2] if len(cols) > 3 else ""
    if "北京" in target or "未公布" in target or "以" in target:
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

# ⚠️ **REWRITE 的行一律不再过 recompute**（040 期立，本期维持）
diff = []
bad = []
out = [recompute(l) if l not in REWRITE.values() else l for l in out]

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
print("before -> after diff (行名 / 旧值 -> 新值):")
for l in out:
    m = DAYS_RE.search(l)
    if not m or l in REWRITE.values():
        continue
    d = parse_cut(l)
    if d is None:
        continue
    truth = (d - BASE).days
    if int(m.group(1)) != truth:
        diff.append((l.split("|")[1][:46].strip(), m.group(1), truth))
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

# ⚠️ **字段数守卫（040 期 §十·15 第 5 条）**：正文里的裸 `|` 会把行切成更多字段
from collections import Counter
print("field-count distribution:", Counter(len(l.split("|")) - 2 for l in out))

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(header + "\n" + sep + "\n")
    f.write("\n".join(out) + "\n")

print("rows: %d (%d + %d new) / rewrites: %d" % (len(out), PREV, len(NEW), rw))
