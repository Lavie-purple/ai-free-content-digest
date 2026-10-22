# -*- coding: utf-8 -*-
"""044 期：把本期新增的待澄清口径登记进 open_questions.md（追加，不删行）。
⚠️ data/ 下是 CRLF —— 写回用 newline="\\r\\n"。
"""
F = ".workbuddy/data/open_questions.md"

NEW = [
 ("Q32",
  "**`MiniMax M3.1 Flash` 权重到底何时真的上传（官方四个状态停在第 ② 级，本期连续第 2 期未见）**",
  "**① 官方博客（`minimax.io/blog/minimax-m31f`，10/19 发布）**：逐字只写 `Model weights will be released later.` —— **全篇无任何日期**；"
  "**② 官方文档站**已在模型表里标 `open-weight`（**强度高于博客**，但仍无日期）；"
  "**③ 官方 X 与第三方（`The Decoder` / `SiliconANGLE` / `HuggingNews` / `RITS`）**：口径为「10 月 23 日」，"
  "其中 `RITS` 逐字 `The reported October 23 date is a plan, not a checkpoint.`；"
  "**④ 本期（044）实跑 `HF` `MiniMaxAI` 组织页：21 个仓库逐个核过，无任何 `M3.1` / `M3.1-Flash`** —— **第 ④ 级仍未到**。",
  "044",
  "挂账中",
  "**回扫节点：10/23 之后**。**处置：在第 ④ 级之前一律按「只能用 API、不能下载」规划**（避坑 41 第四层 / 139）。"
  "**⚠️ 写「官方确认 10 月 23 日开放权重」是失实的** —— 第三方给的日期只能写成「第三方口径」。"),
 ("Q33",
  "**`OpenRouter` 官方 API 目录的 468 / 21 / 18 与第三方转录站的 20 条为什么三个数各不相同**",
  "**① `openrouter.ai/api/v1/models`（官方 API，本期首次用作判据）**：**468 个模型全量 / 21 个零价 / 18 个带 `:free` 后缀**；"
  "**差额 3 个为 `google/lyria-3-pro-preview`、`google/lyria-3-clip-preview`、`openrouter/free`（一个路由器）** —— "
  "**「零价」与「带 `:free` 后缀」本就是两个口径**（避坑 161）；"
  "**② `freellm.net/providers/openrouter`（第三方转录）**：**`20` 条**（`20 free models online` / `Supported Models 20 models` / "
  "`Total Models 20 listed`），**且本期该站清单缺 `recursive/flint-v1.0:free`**（官方目录 10/21 22:46 UTC 已上线）；"
  "**③ 043 期正文写的 `502+` 模型**：**已非现行口径**，且其来源为第三方转录，与官方 API 口径**不可相减**。",
  "044",
  "挂账中",
  "**处置：一律以官方 API 目录为准，第三方站的数字只作旁证**；**引用时必须写清是「零价」还是「带 `:free`」**。"
  "**⚠️ 这是「转录源会滞后于官方目录」的第一个量化样本**（滞后 ≥ 1 个新模型）。"),
 ("Q34",
  "**`freellm.net` 的免费模型限速到底是 50 次/日、200 次/日，还是充 $10 后 1000 次/日**",
  "**① `OpenRouter` 官方 `docs/faq` 逐字**：`For free models, rate limits are determined by the credits that you have purchased. "
  "If you have purchased at least 10 credits, your free model rate limit will be 1000 requests per day. Otherwise, you will be rate limited to "
  "50 free model API requests per day.` —— **50 / 1000 两档**；"
  "**② `freellm.net/providers/openrouter` 逐字**：`200 req/day (free tier)` —— **与官方差 4 倍**；"
  "**③ 官方 `docs/faq` 未说明该 200 是从哪个口径换算来的**。",
  "044",
  "挂账中",
  "**本期为该口径冲突的第 6 次记账**（036–044 期连续挂账）。**处置：两说并列，不取其一、不取中间值**（避坑 161）。"
  "**回扫方向：官方 `docs/faq` 是否补上「200」这一档的来源**。"),
 ("Q35",
  "**`Anthropic` `Claude Duet` 的两个未定项（`Team`/`Enterprise` 是否可用 / `US` 以外地区何时开放）**",
  "**① 官方资源页（`claude.com/resources/articles/claude-duet`，日期 `October 21, 2026`）逐字**：`starting with Pro and Max users in the US`、"
  "`available by waitlist today`；**② 全篇只提 `Pro` 与 `Max`，`Team`/`Enterprise` 未被提及**；"
  "**③ 官方未给 `US` 以外地区的开放时点**（避坑 187：**条件里没有日期就不算日期**）。",
  "044",
  "挂账中",
  "**回扫节点：下一次 `Anthropic` 资源页更新或产品更新日志**。"
  "**⚠️ 结论已定的部分不要再反复解释：官方无免费额度**（含在 `Pro`/`Max` 套餐内、用同一套 `usage limits`）—— "
  "**本条只挂「地区与档位」这一个未定项**。"),
 ("Q36",
  "**`OpenAI` × `Google Cloud Model Garden` 的 GA 具体日期（官方只写「未来几周」）**",
  "**① 官方公告（`openai.com/index/openai-models-google-cloud/`，日期 `October 21, 2026`）逐字**：`General availability is planned in the coming weeks.`"
  " —— **「未来几周」不是一个日期**（避坑 187）；**② 官方未给任何可解析的时点**。",
  "044",
  "挂账中",
  "**处置：第四章该行截止列写「未公布」，不替厂商写一个具体日**（避坑 154 / 166）。"
  "**回扫节点：10 月底前若仍未给日期，则该行从「登记启动日未定」降为「已收口（未 GA 落地）」**。"),
]

md = open(F, encoding="utf-8", newline="").read()
n0 = len([l for l in md.split("\n") if l.startswith("| Q")])
lines = []
for qid, topic, conflict, issue, st, nxt in NEW:
    for f in (topic, conflict, nxt):
        assert "|" not in f, (qid, "字段含裸 | 会把 6 字段行切成更多字段")
    lines.append("| %s | %s | %s | %s | %s | %s |" % (qid, topic, conflict, issue, st, nxt))
md = md.rstrip("\n") + "\n" + "\n".join(lines) + "\n"
open(F, "w", encoding="utf-8", newline="\r\n").write(md)

n1 = len([l for l in open(F, encoding="utf-8", newline="").read().split("\n") if l.startswith("| Q")])
print("open_questions rows: %d -> %d (+%d)" % (n0, n1, n1 - n0))

from collections import Counter
rows = [l for l in open(F, encoding="utf-8", newline="").read().split("\n") if l.startswith("| Q")]
print("field-count distribution:", Counter(len(l.split("|")) - 2 for l in rows))
