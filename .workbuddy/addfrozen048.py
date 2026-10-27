# -*- coding: utf-8 -*-
"""048 期：把本期新增/改写条目登记进 frozen_items.md。
⚠️ **data/ 下是 CRLF** —— 必须用 newline="\\r\\n" 写回。
⚠️ **先写库、再跑 check_frozen**。
"""
F = ".workbuddy/data/frozen_items.md"

STATUS = {
 "OpenAI Signals v3.0 数据集发布（10/26 · 165 类工作活动 / 近 100 国 / 季度序列 / CC BY 4.0 · 047 期漏登补登）": "生效中",
 "Runware 的 Kling 4.0 模型页路径迁移（旧路径软 404 / 真实路径 /kling-4 / $0.133 归属 sync-3）": "演进中",
 "OpenRouter 目录层换血（463 同值但 +gpt-6.1-terra-pro / −granite-4.0-h-micro）": "演进中",
 "三个「页面上的日期 ≠ 条目日期」渲染陷阱（Anthropic 区块标题栏 / MiniMax dateModified / llm-stats dateModified）": "生效中",
}

NEW = [
 ("OpenAI Signals v3.0 数据集发布（10/26 · 165 类工作活动 / 近 100 国 / 季度序列 / CC BY 4.0 · 047 期漏登补登）", "048", "发布",
  "**本报告至今最干净的一条「免费内容」条目**：**一份可直接下载、许可写得很清楚的数据集**。"
  "**官方一手（`openai.com/index/chatgpt-expanding-world-of-work`，页面标注 `October 26, 2026`）逐字**："
  "`Today, we are releasing OpenAI Signals data that explores 165 work activities across nearly 100 countries, revealing how consumers use ChatGPT for work.`；"
  "`The data covers work-related messages on individual ChatGPT plans and does not include enterprise messages or Codex messages`（原文在此处截断为 `Cod`）。"
  "**官方一手（`openai.com/signals/data-download/`，读于 2026-10-27 10:2x，返回 200、338,939 字节）逐字**："
  "`Download CSV files of the data`；`Data dictionary`；"
  "`All Signals data is licensed for use under the Creative Commons CC BY 4.0 license, which allows you to use, share, and adapt the data but requires attribution or citation.`；"
  "另给第二个下载口 `Download data for the AI Jobs Transition Framework`，以及 BibTeX 引用格式"
  "（`@online{openaiecon2026signalsdata, …, title = {{OpenAI} Signals v3.0}, year = {2026}, organization = {OpenAI}, url = {https://openai.com/signals/data-download/}, urldate = {2026-10-26}, note = {Data download and methodology}}`"
  "—— **⚠️ 本报告在正文里把 `title` 字段按单层大括号书写（官方原文为 BibTeX 双层写法）：双层大括号与本项目模板占位符标记同形，会被 `verify_web.py` 判成「未替换的模板残留」——改措辞、不改守卫（045 期纪律）**）。"
  "**四层开放（避坑 41）**：① 能用 —— 免登录直接下载，未要求注册/订阅/填表（订阅提醒表单在页面下半部，与下载口分离）② 能下载 —— CSV + 数据字典 + AI Jobs Transition Framework 数据 "
  "③ 能跑 —— CSV 可直接用 Excel/R/Python 打开 ④ 能商用 —— `CC BY 4.0` 允许使用/分享/改编，**但须署名或引用**。"
  "**两个厂商自报的可核对数（避坑 116）**："
  "① `Across 74 countries observed in every quarter, the ten most common activities represented an average of 51.1% of each country's classified work messages in Q3 2026, down from 56.0% in Q1 2025`"
  "—— 74 国头部 10 类活动占比均值 `56.0% → 51.1%`（−4.9 个百分点）；"
  "② `about 43% of the employment-weighted task mix for mapped U.S. occupations falls into Other IWAs` —— 约 `43%` 的美国就业加权任务结构落在「Other IWAs」（搬运物料、操作车辆、维护健康或病历等），**因未达一致性门槛而未单独报出**。"
  "**⚠️ 期号与窗口归属**：官方发布日 `2026-10-26`（下载页 `urldate` 逐字）落在 **047 期窗口内**，"
  "**047 期正文与表格均未登记它**（经 `git show HEAD` 与全文检索逐行核过，047 期 md 中 `Signals` 命中 0 次）—— **故本期是「往期漏项补登」，不是「048 期新发布」**（避坑 44）。"),

 ("Runware 的 Kling 4.0 模型页路径迁移（旧路径软 404 / 真实路径 /kling-4 / $0.133 归属 sync-3）", "048", "事件",
  "**本期最有工程价值的一条分发层发现（三件事捆在一起）**："
  "**① 路径迁移**：`runware.ai/models/klingai`（047 期用的旧路径）本轮返回 **HTTP 404**，"
  "**而返回体仍是 845,983 字节的完整 SPA 页面**（`Kling 4.0` 4 处、`native audio` 47 处、`0.133` 1 处）—— **这是「软 404」：状态码说没有、正文说有**（048 期新立避坑 209）。"
  "**真实路径是 `runware.ai/kling-4`**（本轮 `200`、529,847 字节，两次抓取长度与关键字段完全一致），**该路径是从旧页返回体里的 `\"Kling 4.0-/kling-4\"` 找出来的**。"
  "**② `0.133/秒` 的归属被核到**：该页 JSON 逐字 `\"pricingRates\":[{\"amount\":0.133,\"unit\":\"durationSecond\"}]`，"
  "其同一条记录的 `coverImage` 指向 `sync-3.jpg`、`capabilities` 含 `io:audio-to-video`、`pricingExamples` 的两个配置是 `segmented-lip-sync` 与 `audio-driven` —— "
  "**它属于唇形同步模型 `sync-3`，不是 `Kling 4.0`**。"
  "**③ 因此 047 期的结论不变、理由要改**：047 期写「两页均未核到 `0.133` 与 `7 days`」；本期在正确路径 `/kling-4` 上 `0.133`、`7 days`、`15%` **各 0 处**，"
  "**故 `$0.133/秒` 与「15% × 7 天」仍不进价格位** —— **但理由从「页面上没有这个数」改成「这个数属于另一个模型」**：前者会诱导下期反复重抓，后者是已经抓到并确认了归属。"
  "**⚠️ 047 期记的 `native audio` 8 处 / `audio` 79 处取自已失效的旧路径**（047 期当时抓到的是该路径 176,419 字节的版本）；"
  "**在正确路径 `/kling-4` 上是 11 处 / 89 处**（047 期自己当时也抓到过 `/kling-4` 的 529,727 字节版本，计数同样是 11 / 89）—— "
  "**所以「8 → 11」是换 URL 的结果，不是内容增加**（048 期新立避坑 210：**同一模型在不同 URL 上的字段计数不可相减**）。"),

 ("OpenRouter 目录层换血（463 同值但 +gpt-6.1-terra-pro / −granite-4.0-h-micro）", "048", "额度",
  "**「总量同值 ≠ 没变化」的第一个正样本**：本轮 `openrouter.ai/api/v1/models`（读于 2026-10-27 10:1x）"
  "**全量 `463` / 零价 `20` / `:free` `17`** —— **与 047 期（463/20/17）三个数全部同值**。"
  "**但逐条 diff（046 期立的两层存档机制连续第二期生效）**：**新增 `openai/gpt-6.1-terra-pro`、消失 `ibm-granite/granite-4.0-h-micro`，`+1 −1 = 0` 与总数一致** ✔；"
  "**`:free` 17 条逐条 diff：无新增、无消失（连续第 3 期）**；**「零价 20」与「`:free` 17」仍差 3 个**（`google/lyria-3-pro-preview`、`google/lyria-3-clip-preview`、`openrouter/free` 路由器）—— 口径不变（避坑 161）。"
  "**新条目 `gpt-6.1-terra-pro` 的一手字段**：与 `gpt-6.1-terra` **完全同价**（`$1` 输入 / `$5` 输出 每 1M、缓存输入 `$0.05`、`ctx 1,050,000`）、**API 侧无 `:free` 档**、"
  "目录里也**没有** `gpt-6.1-terra-pro:batch`（`terra` 有）。"
  "**⚠️ 新立避坑 211：目录层的 `created` 是「加入目录的时间」，不是「厂商发布的时间」** —— "
  "`gpt-6.1-terra-pro` 的 `created` 是 `2026-10-26T18:15:56Z`（＝北京 10/27 02:15），**落在 047 期窗口内**，"
  "**即「047 期窗口内发布、048 期才在目录层挂出」**；**若把 `created` 当发布时刻，会把上期的发布算进本期窗口**。"
  "**⚠️ 消失的 `ibm-granite/granite-4.0-h-micro`：本轮该 ID 已不在全量目录中，但本报告不写「下线」「停服」「退役」** —— "
  "**目录层消失 ≠ 厂商撤下模型，官方 `IBM` 侧状态本轮未实访，如实记「未核到」**（避坑 154/161）。"
  "**同轮 `freellm.net` 六项计数器全部与 047 期同值**（`531+` / `300` / `31` / `449` / `243` / `Latest free LLM API model update: 2026-10-26`）—— "
  "**同值也要记账（避坑 029），但「同值」只说明这六个数没动**（避坑 207 同族）；"
  "**047 期记的 `Models Tracked` `−9` 本期维持 `300`、未回升，那 9 条仍定位不到**（`freellm` 不提供可存档的模型 ID 清单，不猜，避坑 44）。"
  "**`openrouter.ai/announcements` 本轮实访仍停在 `October 14, 2026`**（041–048 连续八期无新限免公告）。"),

 ("三个「页面上的日期 ≠ 条目日期」渲染陷阱（Anthropic 区块标题栏 / MiniMax dateModified / llm-stats dateModified）", "048", "事件",
  "**048 期新立避坑 208 的三个一手样本 —— 全在本轮实访的一手站上，且每个都差点导致一条不存在的头条**："
  "**① `anthropic.com/news` 首页顶部有「`Latest news` · `October 27, 2026`」的日期条** —— "
  "**但该页列表里的最新条目是 `Oct 26, 2026` 的 `S-1`（047 期已登记）**；那个日期条是**区块标题栏的渲染日期**，不是任何条目的日期；"
  "同页 `Introducing Claude Opus 5.5` 卡片的日期是 `Sep 22, 2026`（官方产品页 `anthropic.com/claude-opus-5-5` 页面自带同一日期）。"
  "**② `minimax.io/news` 与 `minimaxi.com/news` 的 JSON-LD 里有 `\"dateModified\":\"2026-10-27T01:16:23.752Z\"`** —— "
  "**那是页面渲染时刻**；**该页新闻列表本身是 JS 渲染，本轮只抓到导航栏、没抓到条目**。"
  "**③ `llm-stats.com` 的 JSON-LD 里也有 `\"dateModified\":\"2026-10-27T01:18:26.068Z\"`** —— 同样是渲染时刻。"
  "**三条纪律**：① 判定「窗口内有没有新东西」必须看**条目自己的日期/时间戳**，不看页面上的任何日期串；"
  "② **`dateModified` 永远不是发布日期**；③ 区块标题栏的日期只说明「这块内容是今天渲染的」。"
  "**⚠️ 本期为什么把它立成一条避坑**：**差点把 Anthropic 的「October 27, 2026」当成「Anthropic 今天发了公告」写进头条** —— "
  "**它离真值只有一步之遥，而那一步之遥会产出一条不存在的头条**（避坑 100 同族：**计数与明细必须同源，日期与日期也一样**）。"),
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
