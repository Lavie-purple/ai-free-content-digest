# -*- coding: utf-8 -*-
"""055 期：把本期记忆追加到自动化累计记忆文件（append-only + 「本期内容已写过就断言退出」）。"""
import io

P = ("C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/.workbuddy/memory/"
     "automations/256c1349-ea4a-4721-9c5d-14067699f1f1/memory.md")

MARKER = "## 2026-11-01 第 055 期"

INS = """
## 2026-11-01 第 055 期（隔日出刊 + Anthropic 文本水印官方逐模型对照表 + 官方免费 Content Checker）

- **状态**：成功。**窗口 = 054 期截止 10/31 19:00 → 本期截止 11/1 13:30（北京），约 18.5 小时**；美西/北京双向换算：起 北京 10/31 19:00 ＝ 美西 10/31 04:00 PT、止 北京 11/1 13:30 ＝ 美西 10/31 22:30 PT（**窗口完全落在美西同一天内**；**换季不影响本窗口** —— 美国夏令时 `11/1` 02:00 PT 结束 ＝ 北京 `11/1` 17:00，晚于窗口截止）。**本期是隔日出刊**（054 期是 10/31 第一轮、窗口约 33.5 小时；**两期不合并**）。
- **规模**：全量扫 **320** 个抓取件（另补抓 90 余个专项一手页）、解析出 **3,105** 条带时间戳条目、**窗口内 48 条** —— **逐条归因后只有 4 条产生免费内容条目**。

### 头条
- **⚠️ `Anthropic` 文本水印与 `C2PA`：官方逐模型逐列对照表 —— 且官方给了一个完全免费的 `Content Checker`** —— 一手 `support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content`（`200`/`238,182` 字节、`dateModified 2026-10-28T18:53:26Z`）、`anthropic.com/news/claude-text-watermark`（`200`/`180,551` 字节）、`platform.claude.com/docs/llms-full.txt`（`200`/`49,296,328` 字节）、**`claude.com/check-content`（`200`/`394,825` 字节）**。**官方逐字**：`Watermarking will be applied at the model level, which means it will be present no matter which Claude product or surface the text comes from.` → **标记不分档位，`Free` 档同样带**；`Marks will apply to output from supported Claude models across Claude Platform (API), Claude, Claude Code, Claude Cowork, and Claude Tag, and wherever Claude is offered, worldwide.`；**对照表逐行实读 `16` 个模型 × `3` 列、`✅` 共 `34` 个 —— 其中 `7` 个模型只在第一方有文本水印、云厂商列与 `C2PA` 列均为空**（`Mythos 5`/`Opus 4.7`/`Opus 4.6`/`Opus 4.5`/`Sonnet 4.6`/`Sonnet 4.5`/`Haiku 4.5`）。**免费工具逐字**：`This tool runs in your browser. Your file never leaves your device.`、单文件 `100 MB`、`The tool does not check text.`。⚠️ **文本水印检测是私有预览**（`Watermark detection is currently in private preview`），**文件 `C2PA` 检测才是免费的**。⚠️ **归期**：官方支持页 `dateModified` ＝ 北京 `10/29 02:53`，落在 054 期窗口之前 → **按「首次登记的往期事件」写入**（避坑 229）。
- **⚠️ `Moonshot` `Kimi K3.1 Pro` 的访问条件官方逐字核到（被追 8 期的挂账项，本期销项）** —— 一手 `platform.moonshot.cn/docs/guide/kimi-k3-1-pro-quickstart` 与 `platform.kimi.com/...`（各 `200`/`736,950` 字节、`dateModified 2026-10-28T11:18:14.893Z`、**两站字节数完全一致** → 记一条不拆两口径）。**官方逐字**：`在开放平台完成充值（最低充值金额 10 元）后即可解锁调用。新用户注册认证赠送的 15 元代金券不可用于 Kimi K3.1 Pro。`；`完整模型权重将于 11 月 4 日前发布。`。⚠️ **权重仍未放出**：`HF` 官方 `moonshotai` 名下 `19` 个模型、最新仍是 `Kimi-K3`（`createdAt 2026-06-13T06:42:57.000Z`、`downloads 866,041`）；`search=Kimi-K3` 全站含 `K3.1` 的 `10` 条里**官方名下 `0` 条**。
- **⚠️ `OpenRouter` 目录 `Poolside` 的 `Laguna` 系列 `4` 条整批撤下（含 `2` 条 `:free`）—— 本报告至今第一次出现「免费档减少」** —— 全量 `456`→`452`、零价 `19`→`17`、`:free` `16`→`14`；**逐条 diff 新增 `0`、消失 `4`**（`poolside/laguna-s-2.1` / `...:free` / `poolside/laguna-xs-2.1` / `...:free`）。官方 `created` 时间戳 `1784652683`（＝`2026-07-21 16:51 UTC`）与 `1783002429`（＝`2026-07-02 14:27 UTC`）→ **不是本周新品、是整批撤下**。⚠️ `openrouter.ai/announcements` 实读 `poolside`/`laguna` **各命中 `0` 次** —— 官方无下架公告，本报告只记事实。
- **⚠️ `Ollie` 官方 CEO 告别信核到（挂账项㉛销项）—— 且官方定价页显示它确有一个 `Free` 档** —— 一手 `ollie.ai/farewell`（`200`/`39,747` 字节）逐字 `Ollie is sunsetting on Nov 6, 2026`、`effective Nov 6, 2026.`、署名 `Bill Lennon`；`ollie.ai/pricing`（`200`/`41,791` 字节）第一格逐字 `Free`/`$0`/`50 messages from Ollie per month`/`6 free additional messages from Ollie every day` —— **054 期记的「付费订阅制、非免费额度」被官方原文推翻**。

### 本期纠错 4 条
1. **⚠️ 054 期记「`Ollie` 是付费订阅制、非免费额度」被官方定价页推翻** —— 054 期只读了 `TechCrunch` 转述（`offered a subscription-based model`），据此在第四章写明「不是免费额度条目」；本期实访 `ollie.ai/pricing` 实读，第一格就是 `Free` 档。**要害问题**：只用 `Free` 档的用户，这个免费档 `11/6` 一并消失。**本期把它改写成「有 `Free` 档的限时条目」并在第三章单列一条。**
2. **⚠️ 054 期记「`Unsloth` 那组数在官网零命中」被本期在同一批归档文件上推翻** —— 实读 `tmp_054/unsloth_docs2.html`（`1,178,524` 字节）：`91.5` 命中 **15** 次、`89.9` **8** 次 —— **全是 `SVG` 路径坐标**（`d="M391.5 53.2c-4.5 1.7..."`）；**剥 `<svg>` 后 `5`/`5`，再剥 `<script>` 后 `0`/`0`** —— **结论（官网正文没有那组基准数）成立，但「零命中」这个表述在原文件口径上不成立**。本期改写成三档可核对计数（新立避坑 248）。
3. **⚠️ 053/054 两期「`OpenRouter` 三个数全部逐条零变化」被本期打破** —— 本期消失 `4` 条、全是 `Poolside` 的 `Laguna` 系列（含 `2` 个 `:free`）；**官方 `created` 是 7 月 —— 不是新品下架、是整批撤下**（新立避坑 247）。
4. **⚠️ 054 期记「`Runware` 那条促销 `endsAt` 被官方延长 `30` 天」被本期逐条 diff 推翻** —— 本期实读 `runware.ai/pricing`（`200`/`745,859` 字节，054 期同源文件 `747,303` 字节）逐条 diff：`14` 条全部同值、`0` 新增、`0` 消失、`0` 条 `endsAt` 改动 —— **那条 `endsAt` 回到 `2026-10-31`**。**⚠️ 两种解释本报告都不替官方选边**（① 054 期读到的是短暂中间状态；② 官方随后改回原值 —— 只记「本期实读的逐条结果」）。

### 本期新增避坑（244–248）
244 **官方对照表有两种形态，「档位 × 限额」与「模型 × 标记方式」不能互相替代** —— 后者才是免费读者真正要查的那张表（`✅` 在前者表示「有额度」、在后者表示「**输出带官方标记**」，对免费读者是负担）；
245 **「注册送 X 元代金券」必须逐字读官方有没有写排除条款** —— `Kimi K3.1 Pro` 逐字「`15` 元代金券不可用于 `Kimi K3.1 Pro`」；**「官方没写」不等于「没有排除」，只说明该页没提**；
246 **判断「是不是免费额度条目」不能只看付费页或媒体转述** —— 要看有没有独立的 `Free` 档，且若产品同时有关停公告，要问「`Free` 档会不会一起消失」（本期答案：会）；
247 **目录总数变化有第三种形态「同一家厂商的同一系列整批撤下（含 `:free` 变体）」，且官方可能不给任何公告** —— **零价档减少比总数减少更值得报告**，且**目录类数据每次都要报三档（全量/零价/`:free`）+ 零价档逐条 ID 名单存档**；
248 **在现代前端页面上 grep 一个数字，命中数会被 `SVG` 路径坐标与 `JS` 数据块放大** —— **「命中 `0` 次」与「命中 `15` 次」都可能是假信号**，必须分三档报告并抽查上下文。

### 规模与对账
- 表体 **208** 行 ＝ 054 期 203 ＋ 新增 **5** − 移出 **0**（`prune_table.py` 实跑移出 `0` 条）；`4.1` = **57** / `4.2` = **36**；**总账 151** 条；**速查页 71** 条。
- 色标 ⚪4/🔴5/🟢143/🟡22/🟠7/⚠8/空19 = 208；classify crit5/live160/over4/pending23/unclear10/switch6 = 208；**五条新增行归桶逐条对得上：`crit +1` ＋ `live +1` ＋ `unclear +3` = `+5`** ✔。
- ⚪ 与 over 本期**个数相同（4=4）且成员逐条一致** —— 写「本期恰好对上」。
- **「距今 N 天」由 `recalc_days055.py` 逐行独立重算**（10 行全部需改写、**无一行继承值与真值相同**）；断言是「天数 == 截止日 − 基准日」。
- `lint_table.py --strict` **CLEAN**；`verify_web` **ALL GREEN**；`check_tables` **ALL GREEN**（7 表）；`check_views` **ALL GREEN**（极速 71 / 总账 151）；`check_site_freshness` **ALL GREEN**；`check_frozen` **🔴 0**；`build_quick --check` 全覆盖。

### 本期实测的工程坑（全部已修，详见 `.workbuddy/memory/ENGINEERING.md` §十·32）
- **① 「截止日跨过基准日」的行，正确处置是「改写状态列」而不是「放宽重算器」** —— `recalc_days055.py` 对 `4` 条真值为负的行 `exit 1`（**这是对的**），但它们是「刚过期未收口」的待办、按 `KEEP-3` 必须留 → **在 `gen_table055.py` 里先改状态列为「截止日已过（…已过 1 天）」**，措辞不用收口字样（避坑 239，**本期踩 `0` 次**）。**连带效果：这 `4` 行不再带「距今 N 天」→ 重算器不再报错 → 本期改写 `10` 行（054 期 `14` 行），差额恰是这 `4` 行。**
- **② 「在现代前端页面上 grep 一个数字」必须分三档报告命中数** —— 新立避坑 248 的来源。
- **③ 脚本断言一律用「逐字短语」、不用「裸数字」** —— **本期实际踩到一次**：`CHECKS` 里大小写不同的 `heygen-video-1-0-launch-promo` 断言当场失败。
- **④ 表格单元格里不能出现竖线 —— 升级成「全表字段数分布断言」`Counter({3: 208})`** —— **本期初稿 `2` 条 `NEW` 行漏了行尾 ` |`，被这条断言当场抓住**。
- **⑤ 「分类统计」必须在 `slim` 之后取** —— **本期实测撞上**：`slim` 前 `OpenRouter` 那行含 `口径`+`冲突` → `unclear`；`slim` 后 `冲突` 被裁掉 → `live` —— **同一份表体取数时机不同就差 `1`**。**处置：脚注里的分布数字一律在 `slim` 两轮跑完、`extract` 重跑之后取，取完再注入脚注、然后重跑 `extract` 复核未漂移。**
- **⑥ 三条「事实被推翻」的改写都要落到表体里**（`Ollie` 免费档 / `Runware` `endsAt` / `Unsloth` 零命中口径）—— **正文改了、表体没跟上，就是避坑 239 说的「表体层比正文层慢一拍」。**

### 发布
- **未核到 / 受阻**：`mistral.ai` 全站连续第 `15` 次 `000`；`platform.openai.com/docs/models` 连续第 `8` 期 `403`；`platform.reflection.ai` 连续第 `17` 期 `403`；`next.opera.com/web-ai/` 与 `blogs.opera.com/webai/` 均 `451`（连续第 `5` 期）；`antigravity.google/models` 与 `/pricing` 均 `000`；`docs.unsloth.ai/baselines/unsloth-benchmarks` `404`；`openrouter.ai/blog/how-much-does-claude-code-cost` `404`（另一篇仍是 `1,496` 字节重定向壳）；`www.scnet.cn` 官方页关键词零命中（连续第 `3` 期）；`volcengine.com/product/doubao-work` 正文 `178` 字节 `JS` 壳（连续第 `9` 期）；`techdirt.com` `403`；`ollie.ai/letter-from-the-ceo` `404`（**真身是 `/farewell`**）；`cloudy.chat`（`hnrss` 窗口内唯一「Free AI」条目）超时不可达 → **不登记**。
- **下一轮强制动作（33 条，见 055 期第四章脚注③）**：最紧的八条 —— ① `豆包工作 30 天订阅`（A 档已过 `15` 天、连续第 `9` 期零命中）② `国家超算互联网` 官方页的「夜间免费」栏（连续第 `3` 期）③ `Mistral` 官方公告页原文（连续第 `15` 次 `000`）④ `Mistral` demo 免费预算的额度数字与日历日 ⑤ `AutoClaw` 国际站 `M10W4` 残留文案（连续第 `3` 期未改）⑥ `K2` 系列 `10/31` 停新当日新用户能否注册（需登录态实测）⑦ `Kimi K3.1 Pro` 权重是否在 `11/4` 前放出 ⑧ `Ollie` `Free` 档与关停日 `11/6` 的关系（**免费档会一并消失**）
"""

s = io.open(P, encoding="utf-8").read()
assert MARKER not in s, "本期内容已写过 —— 断言退出，不重复追加"
s = s.rstrip("\n") + "\n" + INS
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("ok, memory.md 行数", s.count("\n") + 1)
