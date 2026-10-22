# -*- coding: utf-8 -*-
"""044 期：把本期新增/改写条目登记进 frozen_items.md。
⚠️ **data/ 下是 CRLF** —— 必须用 newline="\\r\\n" 写回。
⚠️ **先写库、再跑 check_frozen**。
"""
F = ".workbuddy/data/frozen_items.md"

STATUS = {
 "OpenAI Patch the Planet 公告全文：PHP 版本检查 Codex skill（Apache-2.0）+ $1B 定向补贴 + Codex for OSS 维护者订阅（避坑 193）": "生效中",
 "OpenAI 前沿模型上架 Google Cloud Model Garden（无免费层 · 换渠道不是降价 · 避坑 195）": "生效中",
 "Anthropic Claude Duet 研究预览（含在 Pro/Max 套餐内 · 官方无免费额度 · 候补名单制）": "生效中",
 "OpenRouter 新增免费档 recursive/flint-v1.0:free（10/21 22:46 UTC 上线 · 官方无截止日）": "生效中",
 "vLLM 开源 Humming（量化推理 JIT GEMM 内核库 · Apache-2.0 · SM75+ 硬件门槛 · 框架开源）": "生效中",
 "MiniMax M3.1 Flash 开放权重第 ④ 级连续第 2 期未见（HF MiniMaxAI 组织页 21 个仓库实跑）": "演进中",
 "freellm.net 计数器重取 510+/30/241/425（No Credit Card 口径由 425+ 变 425）": "演进中",
 "AutoClaw 国际站活动页 301 跳转（空页不等于活动已撤 · 避坑 194）": "演进中",
}

NEW = [
 ("OpenAI Patch the Planet 公告全文：PHP 版本检查 Codex skill（Apache-2.0）+ $1B 定向补贴 + Codex for OSS 维护者订阅（避坑 193）", "044", "发布",
  "**044 期头条 —— 同一篇公告里同时含三层「免费」，获取成本完全不同**：**① 开源自取（`github.com/openai/php2shell-checker`，`Apache-2.0`、"
  "`411` stars / `29` forks、created `2026-10-21T00:29:12Z`、pushed `2026-10-21T18:05:56Z`）；"
  "② 定向补贴（`$1 billion` subsidized `Daybreak access` through `Daybreak for Frontline Defenders`，**对象是「资源有限的机构、保护关键服务的组织」**，"
  "**官方未公布任何截止日**）；③ 身份权益（`subscriptions for all maintainers through Codex for OSS` + 直接赞助 `the Rust Foundation`，"
  "**申请入口在 `trailofbits.com/patch-the-planet/#apply`，不是自助领取**）。"
  "**⚠️ 官方动词是 `We’re sharing`，全页无 `free` 一词** —— **本报告在第四章写「免费分享 / 开源可自取」并注明官方措辞，不写「官方宣布免费」**。"
  "**⚠️ 官方同时写 `Maintainers remain in control of what patches are deployed and how disclosure is handled`** —— "
  "**即这是「协调披露 + 补贴工具」，不是「厂商替所有人打补丁」**。"
  "**⚠️ 官方自述的攻防细节**：`Calif` 用 `GPT-5.6 Sol` 发现一个关键漏洞、`Wiz` 独立发现并报告了两个漏洞。"
  "**⚠️ 官方自认护栏取舍**：`safeguards intended to prevent abuse can also block legitimate security work`（避坑 185）。"),

 ("OpenAI 前沿模型上架 Google Cloud Model Garden（无免费层 · 换渠道不是降价 · 避坑 195）", "044", "发布",
  "**044 期登记 —— 一条「看起来像新增额度、实为换渠道」的公告**：官方逐字 `Google Cloud customers will be able to purchase OpenAI frontier models "
  "via model garden, transacted through the Google Cloud Marketplace.`；`Enterprises with Google Cloud spend commitments will be able to draw down "
  "their GCP commitments for these purchases.`；`General availability is planned in the coming weeks.`"
  "**⚠️ 公告全页无 `free tier` / 免费额度 / 试用额度 / 价格优惠任何一项** —— **本报告据此写「无免费层」**（避坑 154：**上游没给的不替它写**）。"
  "**⚠️ 三个字段**：**① 购买路径 = `Model Garden` 选型 → 经 `Google Cloud Marketplace` 交易（不是在 `OpenAI` 官网直接买）；"
  "② 结算口径 = 可用既有 `GCP` 消费承诺额抵扣 —— 即「同一笔钱换个花法」，不是新增预算、更不是免费额度；"
  "③ 「未来几周」不是一个日期 —— 第四章该行截止列写「未公布」，不替厂商写一个具体日**（避坑 154 / 166 / 187）。"
  "**⚠️ 本报告第四章该行初稿误写 `⚪`（已收口）且连写两个色标，本期已改为 `⚠`（登记启动日未定）**（避坑 195 的自纠样本）。"),

 ("Anthropic Claude Duet 研究预览（含在 Pro/Max 套餐内 · 官方无免费额度 · 候补名单制）", "044", "发布",
  "**044 期登记 —— 本报告第一次用「三步法」判定一个新产品到底免不免费**：**① 找免费字样 → 全篇无 `free`；"
  "② 找权益归属 → `included in Pro and Max plans and uses the same usage limits as the rest of Claude`（**含在付费套餐内**）；"
  "③ 找额度口径 → 官方给的是 `usage limits`（与 Claude 其余功能同一套限额），**不是免费额度**。**结论：官方无免费额度**（避坑 195）。"
  "**其他逐字事实**：**独立应用（iOS / Android + claude.ai）**；`starting with Pro and Max users in the US`（**美国先行**）；"
  "`available by waitlist today`（**候补名单制**）；**基于 `Opus 5.5`**；`Its background checks count toward those limits`（**后台检查计入限额**）；"
  "`checks your connected accounts every few hours`。**⚠️ `Team`/`Enterprise` 公告未说明**。"),

 ("OpenRouter 新增免费档 recursive/flint-v1.0:free（10/21 22:46 UTC 上线 · 官方无截止日）", "044", "发布",
  "**044 期登记 —— 官方 API 目录实跑**：**`openrouter.ai/api/v1/models` 返回 468 个模型全量 / 21 个零价 / 18 个带 `:free` 后缀**"
  "（**差额 3 个为 `google/lyria-3-pro-preview`、`google/lyria-3-clip-preview`、`openrouter/free`（一个路由器）** —— "
  "**「零价」与「带 `:free` 后缀」是两个不同口径，写清单时必须说清是哪一个**，避坑 161）。"
  "**新增条目**：`recursive/flint-v1.0:free`，`created` = `1792622765`（**2026-10-21 22:46 UTC**），上下文 `262144`，prompt / completion 价均为 `0`。"
  "**⚠️ 官方 API 目录与模型页均无 `limited time` / `until` 字样** —— **第四章该行截止列写「未公布」，不替厂商写一个截止日**（避坑 191）。"
  "**⚠️ 同期 `HF` `RecursiveSI/flint`**：`Apache-2.0`、`gated: false`、createdAt `2026-10-21T14:20:58Z`、lastModified `14:24:03Z`、"
  "**`downloads` 0**、tags 含 `license:apache-2.0` 与 `region:us`、另有 `int4`/`int4-gguf`/`nvfp4-gguf` 三个衍生仓库。"),

 ("vLLM 开源 Humming（量化推理 JIT GEMM 内核库 · Apache-2.0 · SM75+ 硬件门槛 · 框架开源）", "044", "开源",
  "**044 期登记 —— 本报告第二个「框架开源」样本**：**`vllm-project/humming`**，`Apache-2.0`、`284` stars / `58` forks、"
  "created `2026-02-11`、pushed `2026-10-21 05:54 UTC`。**README 逐字**：`SM75+`、`Requires only PyTorch and NVCC`、"
  "`package size is only 100+KB`、`Supports both Dense GEMM and MoE GEMM`。**Support Matrix（关键字段）**："
  "`FP16`→SM75+、**`BF16`→SM80+**、`FP8`→SM89+、**`FP4`→SM120+**、`INT8`→SM75+、**`INT4`→SM80+**。"
  "**⚠️ 判据分工**：**权重开源看「能不能下载、许可是什么」；框架开源看「能不能跑起来、依赖什么硬件、支持哪些平台」** —— "
  "**避坑 189 的许可五层结构不适用于框架，只适用权重**。**⚠️ `SM75+` 是硬门槛**（`Turing` 架构起）—— **不写这一层，读者会以为「装上就能跑」**。"),

 ("MiniMax M3.1 Flash 开放权重第 ④ 级连续第 2 期未见（HF MiniMaxAI 组织页 21 个仓库实跑）", "044", "模型",
  "**044 期回扫 —— 四个状态仍停在第 ② 级**：**① API 可调 ✅ ② 官方文档站标 `open-weight` ✅ ③ 官方未给日期 ❌ ④ 权重未上 HF ❌**。"
  "**本轮实跑 `hf-mirror.com/api/models?author=MiniMaxAI&limit=100`：组织页共 `21` 个仓库**（逐条为 `MiniMax-Text-01`、`MiniMax-VL-01`、"
  "`SynLogic-32B`、`SynLogic-Mix-3-32B`、`SynLogic-7B`、`MiniMax-Text-01-hf`、`MiniMax-M1-40k`、`MiniMax-M1-80k`、"
  "`MiniMax-M1-80k-hf`、`MiniMax-M1-40k-hf`、`MiniMax-M2`、`VTP-Small-f16d64`、`VTP-Base-f16d64`、`VTP-Large-f16d64`、"
  "`MiniMax-M2.1`、`MiniMax-M2.5`、`MiniMax-M2.7`、`MiniMax-M3`、`MiniMax-M3-MXFP8`、`MiniMax-H3`、`MiniMax-Music3`），"
  "**其中不含任何 `M3.1` 或 `M3.1-Flash`**。"
  "**⚠️ 本期抓到 043 期自己的一处计数错误（见五·1）**：**043 期正文写「`20` 个仓库逐个核过」，但它自己列出的名单是 `21` 个** —— "
  "**即上一期「手写计数与明细不同源」**；**本轮 API 实跑为 `21` 个，与 043 期列出的明细一致 —— 错的是那个 `20`，不是仓库数变了**。"
  "**⚠️ 顺带把 `MiniMax-H3` 的下载数从「489 万」升级为精确值 `5,007,397`**（本报告第一次给精确值，以便下期做同口径 diff）。"
  "**⚠️ 「连续 N 期未见」是待办状态、不是事实判断**（避坑 180）—— **本行写「连续第 2 期未见」，不写「不会发布」**。"),

 ("freellm.net 计数器重取 510+/30/241/425（No Credit Card 口径由 425+ 变 425）", "044", "数据",
  "**044 期重取（本期首次把两个面板字段正式登记）**：`510+` 模型 / `30` 提供方 / `241` 经实时 API 验证 / **`No Credit Card 425`**"
  "（**上期写法为 `425+`，本期为 `425` —— 口径表述变化，两期不可相减**）/ **`Models Tracked 510`** / **`Free & Online 301`**（两项新登记）/"
  "`Last update 2026-10-21 checked 2026-10-21`。**⚠️ 「免绑卡数」本轮重新单列，与上期不可比**（030 期纪律：**口径变过就不相减**）。"
  "**⚠️ `freellm.net/providers/openrouter` 专页仍是 `20` 条**（`20 free models online` / `Supported Models 20 models` / `Total Models 20 listed` / "
  "title `20 Models`），`200 req/day (free tier)`、`Context Range 66K – 1.0M`、`Credit Card Not required`、"
  "**`Phone Verification Not required`（本期首次核到）**、`$10 lifetime top-up for 5× more rate limits`。"
  "**⚠️ 该站 `:free` 清单本期缺 `recursive/flint-v1.0:free`** —— **「转录源会滞后于官方目录」的具体样本**。"),

 ("AutoClaw 国际站活动页 301 跳转（空页不等于活动已撤 · 避坑 194）", "044", "工具",
  "**044 期登记的一条取料纪律样本**：`autoclaw.z.ai/blog/news/M10W3`（**无尾斜杠形态**）**返回 `301`、文件 0 字节** —— "
  "**若直接判「抓到空页」，极易误读成「活动已撤」**；**用 `curl -sL` 跟随重定向到 `autoclaw.z.ai/blog/news/M10W3/` 后正文正常**（`Get 85M Tokens`）。"
  "**⚠️ 判定活动是否还在必须看正文规则表，不是看抓到几字节**（避坑 194）。"
  "**⚠️ 本轮为该站活动页连续第 4 次实访仍是 `85M`（官方未改回旧版口径）** —— 详见本报告一·4 与五·2。"),
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
