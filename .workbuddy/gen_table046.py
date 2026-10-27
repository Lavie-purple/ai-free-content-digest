# -*- coding: utf-8 -*-
"""从 045 期 md 提取第四章截止表 -> 基准日 2026-10-25 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table046.md（纯表格块，供 046 期正文嵌入）。

沿用 045 期范式，本期为第二十二次落地：
  1) 先断言行数（045 期 body = 233）
  2) 按行名子串套 REWRITE 字典（每键必须恰好命中 1 次）
  3) 正则重算每一行的「距今 N 天」（基准日 10/25）
  4) 新行插在 ⚪ 存档块之前 -> 再断言总数
  5) 输出后由 inject046.py 注入正文占位符

⚠️ **本期核心变化（六件）**：
   - **`Kimi K3.1 Pro` 发布（窗口内头条）**：官方英文技术博客（`kimi.com/blog/kimi-k3-1`）
     逐字 `our most capable 3T-class open-weight model to date, with a 1-million-token context window`、
     `The full model weights will be released by Nov 4.`；`OpenRouter` 目录已上架
     （`$2.00/$10.00/$0.20` 每 1M、`ctx 1,048,576`、`created` 2026-10-23T17:56:28Z）。
   - **`Kimi` 同日公告 `K2` 系列停新与下线**：定价页 callout 逐字「2026 年 10 月 31 日起停止向新注册用户开放……
     计划在 12 月底下线所有 K2 系列模型」。
   - **`fal` 的 `Kling 4.0` 四个端点可商用调用**：`status: public`、`licenseType: commercial`，
     `$0.157/$0.235` 每秒（720p/1080p）；`publishedAt` 2026-10-21（**属 044 期窗口，045 期因 `fal.ai`
     未进信源清单而漏登，本期补登**）；官网首页已可体验。
   - **`OpenRouter` 免费清单 `468/20/17` → `467/20/17`**：`:free` 17 条逐条 diff 无增减
     （045 期存档清单可直接比对）；全量 −1 且**无法定位消失的是哪一个**（045 期只存档了 `:free` 清单）。
   - **智谱 `AutoClaw` 国际站首次跟进 `M10W4`**（`Weekly Perk: 40M Tokens`，10/23 发布），
     **且页面正文 40M 与结尾句 100 million 自相矛盾**；国内站 `M10W4`（1 亿）明日 10/26 开启。
   - **`OpenCode` 免费清单 10 → 11 →（窗口外复读）10**：`LongCat 2.5 Preview Free` 上架又下架。
"""
import re
from datetime import date

SRC = "AI免费内容与权益速递-第045期-2026-10-23.md"
OUT = ".workbuddy/tmp_table046.md"
BASE = date(2026, 10, 25)
PREV = 233

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
    # ---- 新行 1：Kimi K3.1 Pro 发布 ----
    "| 🟢 **`Moonshot` `Kimi K3.1 Pro` 发布（10/23 晚–10/24 · **3T 级开放权重旗舰 · 权重定于 11/4 前**）** | "
    "**11/4 前（官方逐字 `The full model weights will be released by Nov 4.` —— 是「by」不是「on」，未给确切日）** | "
    "🟢 **已发布可用、权重未落地（第 ④ 级未到）**。"
    "**官方一手（`kimi.com/blog/kimi-k3-1`，研究博客索引标注 `Kimi K3.1 Pro 2026-10-24`）逐字**："
    "「**We’re introducing Kimi K3.1 Pro, the first model in our new K3.1 series and our most capable "
    "3T-class open-weight model to date, with a 1-million-token context window.**」"
    "「**We are also releasing Kimi K3.1 Pro Highspeed, which delivers 2-3× the speed of K3.1 Pro.**」"
    "「**Kimi K3.1 Pro and Kimi K3.1 Pro Highspeed are available today on Kimi.ai, Kimi Work, Kimi Code, "
    "and the Kimi API. The full model weights will be released by Nov 4.**」"
    "**官方基准（全部厂商自报，避坑 116）**：`Terminal-Bench 4.0` **`65.7%`**（`GPT-6 Astra` `58.2%`、"
    "`Claude Opus 5.5` `66.4%`）；`Kimi Code Bench 3.0 Long-horizon` **`61.2%`**（`K3` `55.95%`）；"
    "`BenchCAD` **`92.7%`**（`Opus 5.5` `96.2%`、`GPT-6 Astra` `95.9%`）；`OfficeQA Pro v2` `64.4`；"
    "`Financial Modeling` 较 `K3` **+7.2 分**、`Financial Research` **+11.6 分**、`Business Operation` 约 **4.2×**；"
    "`Kimi Hallu Bench Hard` 单项事实陈述错误率 `23.4%` → **`8.3%`**、「含至少一处事实错误的回答比例」为前代的 **`42.4%`**；"
    "`xdev-bench-hard` 未做风险削减的 checkpoint `90.5%` → 正式版 **`81.0%`**。"
    "**⚠️ 中英文页面对同一指标给出四个不同数字（本期新立避坑 201 的直接样本）**："
    "**英文技术博客 vs 中文文档（`platform.kimi.com/docs/guide/kimi-k3-1-pro-quickstart.md`）** —— "
    "幻觉率 `8.3%` vs `6.85%`（前值 `23.4%` vs `23.35%`）；含错回答比例 `42.4%` vs `46.4%`；"
    "财务建模 `+7.2 分` vs `+14%`；金融研究 `+11.6 分` vs `+20%`。"
    "**⚠️ 参数口径两个数**：**官方英文博客与中文文档都写「3T 级 / 3 万亿级」**，"
    "**而聚合站转引的官方社媒帖写「2.8T 总参数 / 104B 激活」** —— **「级」是约数、社媒数未经本报告一手核实，两个都写、不合并**（避坑 161）。"
    "**⚠️ 价格与解锁门槛（中文文档一手逐字）**：「**在开放平台完成充值（最低充值金额 10 元）后即可解锁调用。"
    "新用户注册认证赠送的 15 元代金券不可用于 Kimi K3.1 Pro。**」FAQ 亦逐字「**不可以。**」"
    "**⚠️ 文件接口限时免费**（定价页逐字）：「**文件相关接口（文件内容抽取/文件存储）限时免费**」—— "
    "**官方未给结束日，本行不替它排一个日**（避坑 154/166）。"
    "**⚠️ `OpenRouter` 侧一手（读于 2026-10-25）**：`moonshotai/kimi-k3.1-pro`，"
    "上下文 `1,048,576`，定价 **`$2.00` / `$10.00` / 缓存读 `$0.20`** 每 1M，`created` `2026-10-23T17:56:28Z`"
    "（＝北京 10/24 01:56，**落在本窗口内**）；模型页挂 `Artificial Analysis` 基准（`Intelligence Index` `55.1`、"
    "`HLE` `52.5%`、`AA-LCR` `86.3%`、`GDPval-AA` `67.3%`、`CritPt` `24.6%`、`SciCode` `60.8%`、"
    "`Terminal-Bench 4.0` `67.2%` —— **与厂商自报的 `65.7%` 不同口径，两个都写**）。"
    "**⚠️ 权重现状（`HF` 一手实跑）**：`hf-mirror.com/api/models?author=moonshotai&limit=100` 返回 **`19` 个仓库、"
    "无任何 `K3.1`**（10/24、10/25 两轮一致；直接取 `moonshotai/Kimi-K3.1-Pro` 详情返回 `401`）—— "
    "**与官方「11/4 前发布」的表述一致，不是矛盾**（避坑 196 同族：**列表里没有 ≠ 不存在，但详情端点取不到时本报告只写「未落地」**）。"
    "**⚠️ 企业版口径**（官方逐字）：「**Kimi Enterprise administrators can enable K3.1 Pro for their organization; "
    "access is off by default at launch.**」**⚠️ 官方未写任何免费额度、免费期或试用钟点**（避坑 154）。 |",

    # ---- 新行 2：Kimi K2 系列停新与下线 ----
    "| 🔴 **`Moonshot` `K2` 系列模型停新注册与计划下线（公告见于 `Kimi` 定价页 · **10/31 停新 / 12 月底计划下线**）** | "
    "**10/31（停止向新注册用户开放）；12 月底（计划下线，官方未给确切日）** | "
    "🔴 **生效中（义务性变更，不是活动）**。**官方一手（`platform.kimi.com/docs/pricing/chat` 页面 callout，"
    "10/24 与 10/25 06:24 两轮实访均在）逐字**：「**尊敬的 Kimi 用户，K2 系列模型将于 2026 年 10 月 31 日起停止向新注册用户开放，"
    "已注册用户不受影响；我们计划在 12 月底下线所有 K2 系列模型，请提前做好迁移准备。**」"
    "**⚠️ 三条必须拆开的口径**：**① 「停止向新注册用户开放」≠「下线」** —— **两个日期、两类影响面，"
    "已注册用户在前一个日期不受影响、在后一个日期才受影响**；**② 「计划在 12 月底」是计划口径，不是确切日** —— "
    "**本行截止列因此写「12 月底（计划）」而不写 `12/31`**（避坑 154/166）；"
    "**③ 「下线」的官方含义未定义**（停 API？停权重下载？停客户端内调用？）—— **本报告不代官方定义**。"
    "**⚠️ 受影响范围（一手列表）**：`K2` 系列在 `HF` `moonshotai` 组织下现有 `Kimi-K2`、`Kimi-K2-Instruct`、"
    "`Kimi-K2-Instruct-0905`、`Kimi-K2-Base`、`Kimi-K2-Thinking`、`Kimi-K2.5`、`Kimi-K2.6`、`Kimi-K2.7-Code` "
    "**共 8 个权重仓库**（10/25 实跑 `19` 个仓库中逐条点出）—— **但公告说的是「K2 系列模型」，"
    "未逐一列名，本报告不把 8 个仓库当作官方清单**（避坑 154）。"
    "**⚠️ 迁移指向（公告内链）**：官方给的「迁移准备」链接指向 `Kimi K3.1 Pro` 快速开始文档。"
    "**⚠️ 与 `K3.1 Pro` 新发布的关系**：**两者同在 10/23–10/24 出现，但一个是新产品、一个是旧产品退场** —— "
    "**不可合并成一句「Kimi 换代」**（避坑 134）。 |",

    # ---- 新行 3：Claude Duet 安全、隐私与安全 ----
    "| 🟢 **`Anthropic` 发布 `Claude Duet Safety, Privacy, and Security`（10/23 · **研究预览的安全设计全文**）** | "
    "**未公布（文章，非活动）** | "
    "🟢 **生效中（`claude.com/resources/articles/claude-duet-safety-privacy-and-security`，页面标注 `Published Oct 23, 2026`）**。"
    "**官方一手逐字（节选与本报告相关的）**：「**Claude Duet never sees your passwords, browser cookies, sign-in tokens, "
    "or other credentials.**」「**A separate, automated check runs alongside each action, built on the auto mode classifier "
    "from Claude Code and extended for Claude Duet. … The check runs outside the model doing the work so instructions "
    "hidden in a page cannot affect the outcome.**」「**For purchases, Claude Duet pays with a one-time card from a wallet "
    "like Link from Stripe, limited to that merchant and amount. … Your real card number isn’t shared with Claude Duet "
    "or the merchant.**」"
    "**敏感信息两级（官方逐字分类名）**：**`Never share`**（登录凭证、完整卡号与银行账号、政府 ID 号码）与 "
    "**`Needs consent to share`**（健康、财务等 —— **「You own request counts as consent」**）。"
    "**审批与边界（官方逐字）**：付款、发消息、删除前出审批卡，**「shows you the action, the destination, and the content, "
    "including every recipient」**；**有些动作即使批准也禁止**（交易证券、账户间转账、访问他人账号）；"
    "**付款/转账/删单/建账号不适用「别再问我」**。"
    "**浏览器隔离（官方逐字）**：「**runs in its own dedicated virtual machine in the cloud, separate from the model**」；"
    "智能体只能通过**固定命令集**驱动浏览器；**「requests that its web browser sends include a distinct User-Agent header, "
    "and we publish the public IP addresses it browses from」**；**上线前联系了若干大型网站并给予阻止 `Claude Duet` 访问的选项，"
    "「some chose to」**。"
    "**测试与赏金（官方逐字）**： Safeguards 团队三变体评测（无害版 / 注入指令版 / 诱导越权版）+ 影子流量；"
    "外部渗透测试公司测过一轮、云浏览器与登录表单的跟进测试「is running now」；"
    "**「in scope of Anthropic’s public bug bounty program」**（`HackerOne`）。"
    "**⚠️ 本条的免费性判据（与 044 期登记的 `Claude Duet` 行一致，本期不改变）**："
    "**官方一字未提免费** —— **研究预览含在 `Pro`/`Max` 套餐内、候补名单制、起始于美国 `Pro`/`Max` 用户**"
    "（官方逐字 `A research preview is available by waitlist today, starting with US Pro and Max subscribers.`）。"
    "**⚠️ 本篇是「安全设计说明」，不是「额度说明」** —— **全文没有任何免费额度、试用期或钟点**（避坑 154）。 |",

    # ---- 新行 4：AutoClaw 国际站 M10W4 ----
    "| 🟢 **智谱 `AutoClaw` 国际站 `M10W4` `Weekly Perk`：登录领 **40M** Tokens（10/26–11/1 · **国际站首次跟进周档**）** | "
    "**10/26（周一）00:00 — 11/1（周日）23:59（UTC+8）；奖励 11/1 23:59 失效** | "
    "🟢 **尚未开始（活动期 10/26 起 · 距开始 1 天）**。"
    "**官方一手（`autoclaw.z.ai/blog/news/M10W4/`，`By AutoClaw Team Oct 23 2026`）逐字**："
    "「**From October 26 to November 1, log in to AutoClaw and get 40 million Tokens.**」"
    "「**Event period: October 26 (Mon) 00:00 – November 1 (Sun) 23:59 (UTC+8)**」"
    "「**Log in to AutoClaw during the event to claim 40 million Tokens (worth 4,000 credits) — one claim per account. "
    "The reward expires on November 1 at 23:59 (UTC+8), so the earlier you claim it, the more time you’ll have to use it.**」"
    "**⚠️ 同一页自相矛盾（本期新立避坑 202 的直接样本）**：**结尾句逐字「Remember to log in to AutoClaw on October 26 — "
    "100 million Tokens are waiting for you!」** —— **正文全程 40 million、结尾句 100 million，差 2.5 倍**。"
    "**⚠️ 本报告的处置**：**按正文规则表（40 million / 4,000 credits）登记，结尾句原样引录、不取中间值、不择其一**（避坑 199 同族）。"
    "**⚠️ 一个不断言的猜测**：**100 million 与国内站 `M10W4` 的 1 亿 Tokens 数值相同**，"
    "**疑为两站共用文案时未改数，但本报告没有证据，不写成结论**（避坑 44）。"
    "**⚠️ 国内站同题页面无此矛盾**（`autoclaw.zhipuai.cn/blog/news/M10W4/` 结尾句为「1 亿 Tokens 等你领取！」，与正文一致）。"
    "**⚠️ 与国内站 `M10W4` 的关系**：**两站活动期相同（10/26–11/1）但额度不同（国内站 1 亿 = 100M / 国际站 40M）** —— "
    "**「同期同题不同额」必须分开写，不可互相推算**（避坑 163 多站点面）。"
    "**⚠️ 一条降档必须写全三样（避坑 198 的第三次实测）**：**国际站上一档（`M10W3` 每日登录）10/19–10/25 合计上限 85M；"
    "本档（`M10W4` 一次性）40M；两档活动期相接（10/25 结束、10/26 开始），中间无空窗** —— "
    "**与国内站「2 亿 → 1 亿、中间四天无一次性档」是两种不同的档型，不可对比出「国际站降得少」**（避坑 198：口径不同不相减）。 |",

    # ---- 新行 5：OpenCode 免费清单变动 ----
    "| 🟡 **`OpenCode` 免费模型清单 10 → 11 项（`LongCat 2.5 Preview Free` 上架 · **窗口外复读已下架**）** | "
    "**未公布（`limited time` 均无结束日）** | "
    "🟡 **生效中（清单动态变动，逐条以两页实读为准）**。"
    "**（046 期）两轮实读 `opencode.ai/docs/zen` 的 `Free models` 段**："
    "**① 10/24 09:05（窗口内）实读 11 项**：`GLM-5.3-Flash Free`、`DeepSeek V4.1 Flash Free`、"
    "`MiMo-V2.6-Flash Free`、`Nemotron 3 Ultra Free`、`Nemotron 3.5 Lightning Free`、`Nemotron 3.5 Super VL Free`、"
    "`Big Pickle`、`Beam Free`、`Flint 40B Free`、**`LongCat 2.5 Preview Free`（新）**、**`Jev 1.13 Free`（新）**；"
    "**② 10/25 20:17（窗口外复读，属 047 期窗口）实读 10 项**：**`LongCat 2.5 Preview Free` 已不在清单中**，其余同上。"
    "**⚠️ 与 045 期（10/23 实读 10 项）的逐条 diff**：**新增 3 条**（`Flint 40B Free`、`LongCat 2.5 Preview Free`、`Jev 1.13 Free`）、"
    "**减少 2 条**（`Exo Free`、`MiMo-V2.5 Free`）—— **净 +1，两轮之间又是 10 → 11 → 10**。"
    "**⚠️ `LongCat 2.5 Preview Free` 的留存口径（官方逐字）**：「**Its provider follows a zero-retention policy and "
    "does not use your data for model training.**」；**`Flint 40B Free` 的口径相反**："
    "「**During its free period, collected data may be used to improve the model. Data is retained for 30 days.**」"
    "**⚠️ `Go` 订阅页同步变动**：10/24 实读有 `LongCat 2.5 Preview Free (limited time)` 与 `Beam Free (limited time, limited regions)` 两行；"
    "10/25 20:17 复读**只剩 `Beam Free` 一行** —— **与 `zen` 页同向，两页合起来才构成「已下架」的结论**（避坑 199：单读一页会漏）。"
    "**⚠️ 下架本身没有任何官方说明**：**`OpenCode` 两侧均未发布关于 `LongCat` 上/下架的公告，"
    "本报告因此不写「官方宣布上架/下架」，只写「两页出现/不再出现」**（避坑 154）。"
    "**⚠️ `Beam Free` 地区清单本轮仍在**（`Angola, Belarus, Cambodia, China (including Hong Kong and Macau), Cuba, …` 等 20 个条目，"
    "含中国港澳台地区按官方原文照录）—— **与 045 期一致，本期不变**。"
    "**⚠️ `Gemini 4 Argon` 五折（官方逐字 `The 50% discount applies through November 30, 2026.`）本轮仍在 `Go` 页**。 |",
]

REWRITE = {}

# ---- 1) 老混元 Q04：连续第 34 期 / 高危窗口第 25 天 ----
REWRITE["🔴 **腾讯老混元大模型平台停服**"] = (
    "| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必办（已过期，Q04 连续第 34 期未决 · 高危窗口第 25 天）**。"
    "**厂商仍只给「9 月底」这一模糊口径，未给确切停服日** —— **按避坑 47 与 164 的互补口径："
    "厂商不给确切日期时，本报告只做迁移提示、不替它排一个日**。"
    "**⚠️ （046 期）本轮未实访 `cloud.tencent.com/document/product/1729`（045 期该页返回压缩响应、正文未取到，本期未再试）** —— "
    "**因此本期不更新该行的任何事实字段，只按基准日推进「连续第 34 期 / 第 25 天」两个由脚本重算的数**（避坑 180："
    "「连续 N 期」是待办状态、不是事实判断；**且「本期未实访」要如实写，不写「已复核」**）。"
    "**迁移方向见 040 期起的既有结论，本报告不重复往期已固化内容。** |"
)

# ---- 2) OpenRouter 免费档：467/20/17 + freellm 530/309/31/448/243 ----
REWRITE["🟢 **OpenRouter 免费档（**官方 API 目录口径"] = (
    "| 🟢 **OpenRouter 免费档（**官方 API 目录口径 · `467/20/17`**）** | 未公布（动态目录） | "
    "🟢 生效中。**⚠️ （046 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-25 06:24 与 20:17 两次，结果一致）**："
    "**全量 `467` 个模型；零价（`pricing.prompt` 与 `pricing.completion` 同为 `0`）`20` 个；带 `:free` 后缀 `17` 个**。"
    "**⚠️ 三个数的变动必须逐个说清**：**全量 `468 → 467`（−1）；零价 `20 → 20`（同值）；`:free` `17 → 17`（同值）**。"
    "**⚠️ 本期能对 `:free` 做逐条 diff（045 期立的存档机制本期第一次生效）**："
    "**045 期存档于 `.workbuddy/data/tmp_or_free_2026-10-23.txt` 的 17 条，与本期重取的 17 条逐条比对，无新增、无消失**"
    "（本期存档为 `.workbuddy/data/tmp_or_free_2026-10-25.txt`）。"
    "**⚠️ 但「全量 −1」这一个差额本期定位不到**：**045 期只存档了 `:free` 清单，没有存档全量目录 ID** —— "
    "**即付费档里有一个模型从官方目录消失了，本报告无法说出是哪一个**（避坑 44 同族：**没留档的账，下一期就查不动**）。"
    "**本期已补档**：**全量 467 个 ID 存档于 `.workbuddy/data/tmp_or_all_2026-10-25.txt`，下一期起全量 diff 可做**。"
    "**⚠️ 「零价 20」与「`:free` 后缀 17」仍不是同一集合**：**差额 3 个依旧是 `google/lyria-3-pro-preview`、"
    "`google/lyria-3-clip-preview` 与 `openrouter/free`（一个路由器）**（避坑 161）。"
    "**⚠️ 与 `freellm.net` 转录口径连续第二期逐条一致**：**该站 `OpenRouter` 专页（`/providers/openrouter`）`Last Updated 2026-10-25`，"
    "声称 `Free Tier 20 free models online`；本轮按可见表格逐条核，其 20 行 = 官方 20 个零价模型（17 个 `:free` + 2 个 `lyria` + "
    "`openrouter/free`「Free Models Router」）**。"
    "**⚠️ 但转录站页面里还藏着第二份清单（本期新抓到的取料陷阱）**：**同一 HTML 的 `data-provider-import-data` 属性里"
    "内嵌了一份 `44` 个 `:free` 的一键配置导入清单，其中 27 个不在官方目录中**"
    "（如 `minimax/minimax-m2.5:free`、`qwen/qwen3.8-27b:free`、`tencent/hy3:free`、`inclusionai/ling-3.0-flash:free` 等，"
    "且个别行的 `id` 与 `name` 不一致，如 `minimax/minimax-m2.5` 的 name 写 `minimax-m2.5:free`）—— "
    "**即「页面声称 20 条」与「页面内嵌 44 条」同时为真，读转录站必须读可见表格、不能抓 HTML 里所有 `:free` 串**（避坑 199 同族）。"
    "**⚠️ 首页计数器（`freellm.net/`，读于 2026-10-25 06:24）逐项记账**：**`Models Tracked` `520 → 530`；"
    "`Free & Online` `304 → 309`；`Providers` `30 → 31`；`No Credit Card` `438 → 448`；"
    "Hero 句 `520+ → 530+`；「经实时 API 验证」`244 → 243`** —— "
    "**五升一降，三种结果都写，不写趋势判断**（避坑 029）。"
    "**⚠️ 「Providers 30 → 31」多出来的那一条无法断言是谁**：**045 期的首页快照未留存，本报告只记「计数 +1，"
    "且本轮提供商条上可见 `Gonka Broker`（有专页，`Last Updated 2026-10-25`，`4 free models online`，"
    "限速 `~1M tokens/month (shared, varies by model)`，上下文 `8K – 400K`，免绑卡免手机号）」** —— "
    "**不断言「Gonka Broker 就是新增的那一个」**（避坑 154）。"
    "**⚠️ 复读稳定性（06:24 与 20:17 两次）**：**六项计数器完全相同，只有 `Latest free LLM API model update` 一行"
    "从 `2026-10-24 checked 2026-10-24` 推进到 `2026-10-25 checked 2026-10-25`**。"
    "**⚠️ 额度口径仍是「三源三个数、都带来源」**：**① `freellm.net` `OpenRouter` 专页 `200 req/day`、免绑卡、免手机号、"
    "上下文 `66K – 1.0M`；② `OpenRouter` 官方 `docs/faq` 的 `50 / 满 10 credits 后 1,000` 请求每日；"
    "③ `benchlm.ai` 与 ② 同口径** —— **① 与 ② 在日请求数上直接冲突，不可取中间值**（避坑 161）。"
    "**⚠️ `openrouter.ai/announcements` 本轮实访仍停在 `October 14, 2026`**（041–046 连续六期无新限免公告）。 |"
)

# ---- 3) 上海青浦算力券：045 期「今日截止」→ 046 期已过期 ----
REWRITE["🔴 **上海青浦算力券补贴**"] = (
    "| ⚪ **上海青浦算力券补贴** | 申报至 **10/23** | ⚪ **已过期（申报截止 10/23，本期基准日 10/25 已过 2 天）**。"
    "**⚠️ 状态迁移路径必须写清**：**045 期该行是「🔴 今日截止（截止日即基准日 10/23）」**，"
    "**本期按「截止日 < 基准日」改 ⚪** —— **这是「今天到期」类条目的标准两步处理，不跳过「今日截止」直接写「已结束」**（避坑 198 同族）。"
    "**⚠️ 本报告不代官方判断「是否可补报」** —— 官方页未写补报通道，本行不写（避坑 154）。"
    "**申报类权益 ≠ 领取类权益**（避坑 182）：**审批结果与到账时间官方均未公布，本行不写任何「到账日」。** |"
)

# ---- 4) 阿里云 AgentCore：状态列「今日到期（距今 0 天）」是 040 期旧文本，本期显式改 ⚪ ----
REWRITE["🟢 **阿里云 AgentCore 协作管控面限时免费**"] = (
    "| ⚪ **阿里云 AgentCore 协作管控面限时免费** | **10/18 23:59:59** | "
    "⚪ **已结束（截止 10/18 23:59:59，本期基准日 10/25 已过 7 天）**。"
    "**⚠️ 本期新抓到一类继承误差（本报告自己身上第四例，避坑 027 的第四次实测）**："
    "**该行的状态列从 040 期起就写着「今日到期（距今 0 天）」，而截止日是 10/18** —— "
    "**即「今日到期」这四个字在 040 期之后从未随基准日推进，一路留到了 045 期**。"
    "**⚠️ 根因**：**「距今」写在粗体标记内部（`**今日到期（距今 0 天）**`），巡检脚本的 `DAYS_RE` 模式是 "
    "`\\*\\*距今 (\\d+) 天\\*\\*`，匹配不到这种内嵌形态，于是这行从不被重算**。"
    "**⚠️ 同类行本期一并显式改写**：**`佛山 2026 年度网络微短剧扶持申报`（状态列留「距今 -2 天」负值，"
    "因为正则同样匹配不到负号）与 `MiniMax Code 周额度重置卡`（同为「今日到期（距今 0 天）」旧文本）** —— "
    "**三条都是 10 月 18–20 截止，本期统一按基准日 10/25 判「已结束」**。"
    "**⚠️ 纪律修正**：**今后「今日到期」类状态只允许在「截止日 == 当期基准日」的那一期出现**，"
    "**下一期必须改为「已结束（距今 −N 天）」或 ⚪；脚本管不到的内嵌形态，由每期的显式 `REWRITE` 兜底**。 |"
)

# ---- 5) 佛山微短剧扶持：负值「距今 -2 天」的显式纠正 ----
REWRITE["🟢 **佛山 2026 年度网络微短剧扶持申报**"] = (
    "| ⚪ **佛山 2026 年度网络微短剧扶持申报** | **10/20** | "
    "⚪ **已结束（申报截止 10/20，本期基准日 10/25 已过 5 天）**。"
    "**⚠️ 本期纠正一处负值天数**：**045 期该行状态列写「生效中（**距今 -2 天**）」** —— "
    "**负的天数不该出现在正式刊里，它是 044 期脚本重算时正则匹配不到负号、把 044 期的错误值原样继承下来的结果**。"
    "**⚠️ 事实字段不变**：AI 微短剧首次入列；主体不限佛山本地；\"佛山扶持通\"线上填报。"
    "**⚠️ 本报告未核到延期或补报公告** —— **不写「可补报」，也不写「已彻底关闭」**（避坑 154/161：未核到 ≠ 不存在）。 |"
)

# ---- 6) MiniMax Code 周额度重置卡：同 AgentCore 病因 ----
REWRITE["🟢 **MiniMax Code 周额度重置卡限时加赠（每日签到）**"] = (
    "| ⚪ **MiniMax Code 周额度重置卡限时加赠（每日签到）** | **10/18（UTC+8）** | "
    "⚪ **已结束（截止 10/18 UTC+8，本期基准日 10/25 已过 7 天）**。"
    "**⚠️ 与 `阿里云 AgentCore` 同一病因**：**状态列「今日到期（距今 0 天）」是 040 期旧文本，"
    "「距今」内嵌在粗体里、脚本正则匹配不到，从 040 期留到 045 期** —— **本期按 `AgentCore` 行的同一处置显式改写**。"
    "**⚠️ 既有结论不变**：订阅用户每日签到额外领周额度重置卡，全勤最多 9 张、有效期 15 天；"
    "**来源为第三方清单（什么值得买社区 10/16 版）转述 `MiniMax` 官方推特，本报告未回官方推特原帖核**（避坑 44）；"
    "**与「MiniMax Code 每日签到积分」是两笔账，量纲不同不可相加**（避坑 54）；"
    "**该工具的免费部分是账号积分额度，不是某个模型本身免费**（避坑 117）。 |"
)

# ---- 7) WorkBuddy 国内版 DeepSeek 故障补偿：10/22 24:00 截止 → 已结束 ----
REWRITE["🟡 **腾讯 `WorkBuddy` 国内版 `DeepSeek` 故障补偿"] = (
    "| ⚪ **腾讯 `WorkBuddy` 国内版 `DeepSeek` 故障补偿 `500` 积分（10/22 24:00 截止 · **工作区自有产品**）** | "
    "**10/22 24:00** | ⚪ **已结束（领取截止 10/22 24:00，本期基准日 10/25 已过 3 天）**。"
    "**⚠️ 本期纠正一处与截止列脱钩的状态文本**：**045 期该行状态列写「生效中（距今 2 天）」**，"
    "**而按 045 期基准日 10/23 与截止列 10/22 的真值应为 `-1`，「2 天」在任何一期基准日下都对不上** —— "
    "**本报告不断言这个「2」从何而来，只按截止列与本期基准日重判**（避坑 027/180）。"
    "**⚠️ 既有口径不变（工作区自有产品，按避坑 126 与厂商条目分开放）**："
    "**① 必须手动领取，不会自动到账**（官网头像 → 个人主页 → 用量管理 → 点击领取）；"
    "**② 领到后 1 个月有效；③ 另一笔自动到账的账（10/8–14 消耗返还）7 个工作日内到账、不用领** —— "
    "**两笔账不可互推**（避坑 117 同族）。 |"
)

# ---- 8) Step 5 Preview × WorkBuddy：截止日即本期基准日 → 今日截止 ----
REWRITE["🟢 **腾讯 `Step 5 Preview` × WorkBuddy 独家限免**"] = (
    "| 🟢 **腾讯 `Step 5 Preview` × WorkBuddy 独家限免** | **10/25** | "
    "🟢 **今日截止（截止日即本期基准日 10/25 —— 今天最后一天，过期不候）**。"
    "**⚠️ 这是本报告「今天到期」类条目的标准处理**：**截止日是今天，状态列必须写「今日截止」**，"
    "**不写「已结束」（今天还没过完）、也不写「生效中」（那会让读者以为还有明天）**（与 045 期青浦算力券同一处置）。"
    "**⚠️ 零积分限免 600B MoE、原生 1M 上下文**（038 期登记口径不变）；"
    "**权重 10/15 已按承诺兑现、这条限免 10/25 到期，两者不可混成一句**（避坑 148/150）。"
    "**⚠️ （046 期）本轮未实访该产品页，本行只按截止列推进状态** —— "
    "**「未实访」如实写，不写「已复核」**（避坑 030/180）。 |"
)

# ---- 9) AutoClaw 国际站 M10W3：今天是活动期末日 + 连续第 6 次未被改回 ----
REWRITE["智谱 `AutoClaw` 国际站 `M10W3` 每日登录送 Token"] = (
    "| 🟢 **智谱 `AutoClaw` 国际站 `M10W3` 每日登录送 Token（`z.ai` · 10/19–10/25 · **连续第 6 次未被改回**）** | "
    "**10/25（活动期末日）** | 🟢 **今日截止（活动期最后一天 · `Oct 21–25` 档内）**。"
    "**（046 期）本轮实访 `autoclaw.z.ai/blog/news/M10W3/`（跟随 `301`，读于 2026-10-25）**："
    "**标题仍为 `Get 85M Tokens: Daily Login Event`；活动期 `Oct 19 – Oct 25 (UTC+8)`；"
    "`Oct 19-20 (Monday–Tuesday)` 每天 `3,000 credits (30M tokens)`；"
    "`Oct 21–25 (Wednesday–Sunday)` 每天 `500 credits (5M tokens)`；每档当天 24:00 (UTC+8) 过期** —— "
    "**与 044、045 两期逐字一致，一字未改（连续第 6 次）**。"
    "**⚠️ 今天（10/25）仍在 `Oct 21–25` 那一档内，每天只能领 `500 credits (5M tokens)`，且当天 24:00 (UTC+8) 清零**；"
    "**距活动期结束还有不到一天**。"
    "**⚠️ 041 期立的避坑 179 第一条实操（每次引用前现场打开）连续第 6 期成立** —— "
    "**「官方改写是一次性临时变动」这个猜测已连续第 6 次被证伪**。"
    "**⚠️ 取料纪律继续生效（避坑 194）**：**该 URL 旧形态（不带尾斜杠）会 `301`，不跟随重定向会拿到 `0` 字节空文件** —— "
    "**空页 ≠ 活动已撤，判定必须看正文规则表**。"
    "**⚠️ 活动页本身没改，但站内已发下一轮**：**该页 `Related Posts` 里已出现 `Weekly Perk : 40M Tokens Login to claim`"
    "（`M10W4`，10/23 发布，见本表新增行）** —— **「旧活动页未改」与「新活动已发布」同时为真**（避坑 199 同族：两个都必须读）。"
    "**⚠️ 国际站与国内站节奏不同（不可互相推算）**：**国内站 `M10W4` 为 10/26–11/1 一次性 1 亿 Tokens，"
    "国际站 `M10W4` 为同期 40M，同期同题不同额**（避坑 163 多站点面）。"
    "**⚠️ 「当天清零」型不可当存款**（避坑 117 同族）；**官方页未写各模型扣多少 credits，本报告不代官方换算**（避坑 41 第一层）。 |"
)

# ---- 10) AutoClaw 国内站 M10W4：明日开始 + 每日登录档今日收口 ----
REWRITE["智谱 `AutoClaw` 国内站 `M10W4` 一周福利"] = (
    "| 🟢 **智谱 `AutoClaw` 国内站 `M10W4` 一周福利：登录领 **1 亿** Tokens（10/26–11/1 · **明日开启 · 较 `M10W3` 的 2 亿降档**）** | "
    "**10/26（周一）00:00 — 11/1（周日）23:59（北京时间）；奖励 11/1 23:59 失效** | "
    "🟢 **尚未开始（活动期 10/26 起，本行是「下一轮活动已公告」状态 · 距开始 1 天）**。"
    "**官方一手（`autoclaw.zhipuai.cn/blog/news/M10W4/`，页面标注 `2026年10月23日` · 资讯）逐字**："
    "「**10 月 26 日（周一）00:00—11 月 1 日（周日）23:59（北京时间）**」；"
    "「**活动规则：登录 AutoClaw，即可领取 1 亿 Tokens（相当于 10,000 积分），每个账号限领一次。**」；"
    "「**奖励将在 11 月 1 日 23:59（北京时间）失效，越早领取，使用时间越充足哦。**」"
    "**⚠️ 一条降档必须写全三样（避坑 198）**：**① 上一档是多少 —— `M10W3` 国内站一次性档是 **2 亿** Tokens"
    "（`20,000` 积分，活动期 `10.15–10.21`，可领窗口已于 10/21 关闭）；② 这一档是多少 —— **1 亿** Tokens（`10,000` 积分）；"
    "③ 两档活动期是否相接 —— `M10W3` 一次性档 `10.15–10.21`、`M10W4` 一次性档 `10.26–11.1`，"
    "**中间 10/22–10/25 四天没有一次性档**，只有 `10.15–10.25` 的每日登录档。"
    "**⚠️ （046 期）每日登录档今天（10/25）收口**：**`M10W3` 页实读（读于 2026-10-25）确认"
    "「10.15–10.25 每日登录，普通用户每日 500 积分、付费会员每日 800 积分」规则未变** —— "
    "**即今日是该每日档的最后一天，明日（10/26）起进入 `M10W4` 一次性档**。"
    "**⚠️ 本期仍未核到的一件事（如实记）**：**`M10W4` 公告只写了一次性 1 亿档，没有写 `10.15–10.25` 的每日登录档"
    "是否延续到 11/1 之后** —— **本报告不替官方续期，也不写「每日档已结束」**（避坑 154 / 161：未核到 ≠ 不存在）。"
    "**⚠️ 国际站同日跟进但额度不同**：**国际站 `M10W4` 为 `Weekly Perk: 40M Tokens`（10/26–11/1，见本表新增行），"
    "与国内站 1 亿同期同题不同额，两边不可互相推算**（避坑 163）。 |"
)

# ---- 11) 腾讯元器：一行四个日期，脚本只解析得到第一个，必须逐行手算 ----
REWRITE["🔴 **腾讯智能体平台「元器」停止服务（040 期最高优先级运维项）**"] = (
    "| 🔴 **腾讯智能体平台「元器」停止服务（040 期最高优先级运维项）** | "
    "**11/9（停服）；10/29（停止新建）；2027 年 1 月 9 日（数据导出截止）** | "
    "🔴 **倒计时中，四个日期必须分开排（046 期逐行手算，不用脚本）**。"
    "**⚠️ 本行是「脚本解析不到状态列倒计时」的标准样本（`extract_deadlines` 不解析状态列，故本行不进 `deadlines.csv` 的重算集）**："
    "**截止列里有三个日期，而状态列里有三个独立的「距今」——脚本的 `DAYS_RE.sub` 会把三个数全部替换成截止列第一个日期算出的同一个值**。"
    "**因此本行在 046 期继续显式 `REWRITE`，四个日期按基准日 10/25 逐条手算**："
    "**① `10/29` 起不再支持新建智能体与分发 API Key（**距今 4 天**）；"
    "**② `11/9` 平台停止全部服务（**距今 15 天**）；"
    "**③ 数据导出窗口开到 `2027 年 1 月 9 日`（**距今 76 天** —— ⚠️ **比停服日晚两个月，这是最容易漏掉的一个日期**）；"
    "**④ 本报告自设的倒排基准日不变。**"
    "**⚠️ 与 045 期的 diff（逐条对得上才写）**：**045 期该行写 `6 / 17 / 78`（基准日 10/23），"
    "**本期按基准日 10/25 推进为 `4 / 15 / 76`，两期相差 2 天，逐条对得上** ✔"
    "（**注意：045 期纠正过的 044 期 `11 / 22 / 83` 是「每行 −1」式继承错误，本期不是** —— "
    "**本期的三个数全部由「截止日 − 基准日」现算**）。"
    "**⚠️ （046 期）本轮实访元器官网未取到停服横幅**：**页面为 JS 渲染外壳，静态 HTML 只有标题"
    "「腾讯元器 - AI 智能体创建与分发平台」** —— **官方公告口径沿用既有记录，不写「官网已撤公告」，也不写「公告仍在」**（避坑 154/161：未核到 ≠ 不存在）。"
    "**⚠️ 官方公告口径不变**：**平台将于 2026-11-09 停止服务；停服生效后所创建智能体不再可用；"
    "平台访问、数据读写、API 调用、后台控制台全部关闭；发布到公众号、微信客服等渠道的智能体也停止响应用户对话。**"
    "**迁移方案**：**官方推荐迁往腾讯云智能体开发平台 `ADP`** —— **官方称元器上的主要玩法均可延续"
    "（标准模式 / Multi-Agent / 单工作流），并支持更灵活的 `Claw` 模式。"
    "**⚠️ 定位差异**：`元器` 偏 C 端、主要与「元宝」结合；**`ADP` 面向 B 端企业级平台**。"
    "**⚠️ 本行量级高于任何额度到期（避坑 164）**：**「优惠窗口结束」损失的是钱，「平台停服」损失的是存在本身。** |"
)

# ---- 12) 快手可灵 Kling 4.0：未开始 → 已上线（fal 四端点 + 官网可体验 + 补登 10/21 上架）----
REWRITE["🟢 **快手可灵 Kling 4.0（完整版 10 月上线）**"] = (
    "| 🟢 **快手可灵 Kling 4.0（**已在 `fal` 全量上线 · 官网可体验 · 权重/开源口径未见**）** | "
    "**未公布（已上线，非活动；官方未给任何活动期或结束日）** | "
    "🟢 **已上线（生效中 · 045 期记为「未开始（距今 13 天）」，本期状态推进）**。"
    "**⚠️ （046 期）这是本期最大的一处跨期补登**：**`fal` 上四个 `Kling 4.0` 端点的 `publishedAt` 是 "
    "`2026-10-21T15:09–15:22Z`（＝北京 10/21 23:09–23:22，属 044 期窗口）**，"
    "**而本报告 045 期（10/23）仍写「未开始」—— 漏登原因是 `fal.ai` 当时不在本报告的信源清单里**"
    "（本期已在第八章把 `fal.ai` 补进台账）。**端点 `date`（创建）更早，为 `2026-10-16T15:18–15:21Z`**。"
    "**⚠️ 四个端点与定价（`fal.ai/api/models?keywords=kling` 一手实跑，读于 2026-10-25）**："
    "`kling/v4/text-to-video`、`kling/v4/image-to-video`、`kling/v4/reference-to-video`、`kling/v4/video-to-video/edit`；"
    "**四个端点 `status` 均为 `public`、`deprecated` `false`、`removed` `false`、`licenseType` `commercial`、"
    "`hostingType` `proxy`、`landingPageSlug` `kling-4`**。"
    "**定价（页面 `pricingInfoOverride` 一手逐字）**："
    "**① 文生视频 / 图生视频 / 参考生视频（无视频参考）**：「**Video costs $0.157 per second at 720p and "
    "$0.235 per second at 1080p.**」；"
    "**② 参考生视频带视频参考或视频元素、以及视频编辑端点**：「**$0.094 per second at 720p and $0.141 per second "
    "at 1080p, billed on the input plus output length (minimum 2× the output).**」"
    "**规格（端点描述一手逐字）**：「**durations from 3 to 30 seconds**」「**720p or 1080p**」「**per-shot prompts**」"
    "（模型页另有 `Multi Prompt` / `Duration` / `Resolution` / `Aspect Ratio 16:9` 参数）。"
    "**⚠️ 官方站点同步可体验**：**`klingai.com` 首页（读于 2026-10-25 06:24）首屏为「**Kling 4.0 全新升级**」+「立即体验」**。"
    "**⚠️ `fal` 侧没有为 `Kling 4.0` 发博客文**（`fal.ai/blog` 最新两篇是 10/20 `EAGLE-4 Technical Deepdive` 与 "
    "10/19 `Introducing FLUX 3 Max by fal`）；**站点「Video Models」导航仍列 `Kling 3.0`、没有 4.0** —— "
    "**「端点已上线」与「站点导航未更新」同时为真**（避坑 199 同族）。"
    "**⚠️ 聚合站时间点（转引，未核到一手）**：**`aihot.news` 10/23 23:25 条转引 `fal` 官方社媒称「Kling 4.0 正式向公众开放，"
    "所有客户均可通过 API 访问……最长 30 秒带音频的原生视频生成、最多 15 个图像/视频/元素参考、最多 10 个关键帧」** —— "
    "**「带音频」这一点在本报告实访的四个端点描述里没有对应字段，本报告只登记为聚合站转引、不写成官方规格**（避坑 44）。"
    "**⚠️ 045 期记的三条升级方向不变**（单次 30 秒 / 8,000 tokens 提示词 / 10 张关键帧 / 4K 10-bit HDR / 21:9）—— "
    "**但「4K」在 `fal` 上不成立：`fal` 的 `Kling 4.0` 端点最高 1080p，4K 只在 `fal-ai/kling-video/v3/4k/*`（3.0 代）端点上**。"
    "**⚠️ 图像线未动**：**`fal` 的 Kling 图像端点仍为 `kling-image/v3/*` 与 `kling-image/o3/*`（`Kling Image 3.0` / `Kling Omni 3`），"
    "官网首页同主打 `Kling Image 3.0` 原生 4K** —— **视频 4.0 与图像 3.0 是两条线，不可合并成「可灵 4.0」**（避坑 134）。"
    "**⚠️ 一个 API 字段级陷阱（本期新立避坑 203 的直接样本）**：**同一 URL `fal.ai/api/models?keywords=kling` 会返回两种响应变体"
    "（本轮实跑：`58,512` 字节与 `60,270` 字节两种，同样 40 项、同样定价），只有一种在 `discovery` 子对象里带 "
    "`reviewedAt`；且该字段出现时，全部 40 个 Kling 模型的值完全相同（`2026-10-23T13:31:45.929Z`）** —— "
    "**即它是目录级批量时间戳，不是逐模型的审核/上架时间；把它读成「Kling 4.0 于 10/23 21:31 获批」会错**。 |"
)

# ---- 13) MiniMax M3.1 Flash 开放权重：downloads 两轮重取，端点裂口关闭又出现 likes 裂口 ----
REWRITE["**`MiniMax` `M3.1 Flash` 开放权重"] = (
    "| 🟢 **`MiniMax` `M3.1 Flash` 开放权重（**权重 10/17 就已在 `HF` · 043/044 两期判定「未见」是错的**）** | "
    "**无结束日（权重已公开，不是活动；但许可对商用有三条限制，见右列）** | "
    "🟢 **已开放权重（第 ④ 级已到）**。"
    "**（046 期）`HF` 仓库字段两轮重取**："
    "**① 10/24 09:05–09:15**（列表端点连读 4 次 + 详情端点 1 次，全在窗口内）**：`downloads` **`1,096`**（**五个读取全部同值**）、"
    "`likes` **`200`**（列表端点 4 次）/ **`259`**（详情端点 1 次）；"
    "**② 10/25 06:24**（列表端点，仍在窗口内）**：`downloads` **`5,789`**、`likes` **`283`**。"
    "`createdAt` **`2026-10-17T06:37:50.000Z`**（不变）、`lastModified` `2026-10-23T03:37:20.000Z`"
    "（**045 期为 `2026-10-23T00:59:04.000Z`，同一天内又改了一次**）、`gated` **`false`**、`private` `false`。"
    "**⚠️ 045 期「详情 `357` / 列表 `1,096`」的端点裂口本期关闭**：**10/24 五个读取全部给 `1,096`** —— "
    "**本报告因此不把 045 期「缓存不同步」的猜测写成结论，只记「两期各读到什么」**（避坑 116 同族：不断因）。"
    "**⚠️ 但 `likes` 出现了新的端点裂口**：**同日列表端点 `200` vs 详情端点 `259`（差 `59`）** —— "
    "**「一个字段的裂口关闭、另一个字段的裂口打开」，两个数都写、不取其中一个**（避坑 161）。"
    "**⚠️ 流通量重取记账（升/降/同值都记）**：**`downloads` `1,096` → `5,789`（升 `4,693`，约 5.3 倍，发生在 10/24 09:15 → 10/25 06:24 的 21 小时内）**；"
    "**`likes` `200` → `283`（升 `83`）**。**⚠️ 045 期 `likes` 记为 `2`，与本期两个端点都差两个数量级 —— 045 期那个 `2` 疑为取数时点过早，本期按实际读值记账、不回改 045 期**。"
    "**⚠️ 对照组继续记账**：**同期 `MiniMax-H3` 详情端点 `downloads` `4,967,030`（10/24）→ **列表端点** `5,099,332`（10/25，**升 `132,302`**）**、"
    "`lastModified` `2026-08-13T01:46:29.000Z`（不变）；**045 期记为 `5,011,999`，本期两个读值都高于它**。"
    "**⚠️ 许可与四层结论不变（045 期已固化，本期不重复）**：**`minimax-community` = 非商用免费 + 商用须标注 "
    "`Built with MiniMax M3.1-Flash` + 年收入超 2,000 万美元须书面授权；判许可必须读 `LICENSE` 正文，"
    "不读 API 字段（为空）也不读 tag（`license:other`）**（避坑 197）。"
    "**⚠️ `MiniMax` 官方新闻页（`minimaxi.com/news`，读于 2026-10-25）导航仍只有 `MiniMax M3.1 Flash` · `NEW` 与 `MiniMax M3` 两条** —— "
    "**官方侧连续第 2 期无新发布**（045 期同）。 |"
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

# 负值守卫：正式刊正文里不允许出现「距今 -N 天」作为现行值
# （REWRITE/NEW 行里引用历史错误文本的负值不算 —— 那是纠错引文，不是现行字段）
neg = [l.split("|")[1][:40] for l in out
       if "距今 -" in l and l not in REWRITE.values() and l not in NEW]
assert not neg, ("出现负值天数", neg)

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
