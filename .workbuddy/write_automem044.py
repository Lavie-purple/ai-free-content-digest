# -*- coding: utf-8 -*-
"""044 期：写当日日志 + 追加自动化记忆。"""
import io
import os

DAY = ".workbuddy/memory/2026-10-22.md"
AUTO = ".workbuddy/memory/automations/256c1349-ea4a-4721-9c5d-14067699f1f1/memory.md"

LOG = """
## 044 期（2026-10-22）· AI 免费内容与权益速递

**窗口**：10/21 12:00 → 10/22 12:00（24.0 小时整日整段，不适用短窗口纪律）。

**头条**：「同一天里 `OpenAI` 一口气发了 7 条公告，而其中真正带免费/补贴语义的只有一条」。

**本期实访的一手源**：`openai.com/news/`（10/21 公告 7 条逐条核对标题/分类/日期）、
`openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/`（`Patch the Planet` 全文逐字）、
`github.com/openai/php2shell-checker`（GitHub API）、`openai.com/index/openai-models-google-cloud/`（`Model Garden` 全文逐字）、
`claude.com/resources/articles/claude-duet`、`openrouter.ai/api/v1/models`（官方 API 目录）、
`hf-mirror.com/api/models/RecursiveSI/flint`、`hf-mirror.com/api/models?author=MiniMaxAI&limit=100`、
`github.com/vllm-project/humming`（GitHub API + README + Support Matrix）、
`autoclaw.z.ai/blog/news/M10W3/`（活动规则全文）、`autoclaw.zhipuai.cn`（国内站）、
`freellm.net` 首页与 `/providers/openrouter` 专页、`openrouter.ai/docs/faq`、`anthropic.com/news`。

**本期新立三条避坑（193–195）**：
- **193**「免费」至少三层 —— 开源自取 / 定向补贴 / 身份权益，获取成本完全不同，不可统称。
- **194** 官方页面改 URL（加尾斜杠）时「抓到空页」极易被误读成「活动已撤」；判定必须看正文规则表。
- **195** 判断新产品「免费与否」有两条路；「官方没说免费」这一路必须走完三步（免费字样 → 权益归属 → 额度口径）。

**本期三条纠错**：
1. 043 期正文写「`20` 个仓库逐个核过」，但它自己列出的名单是 `21` 个 —— **上一期「手写计数与明细不同源」**（本报告自己身上）。
2. 043 期第四章 `OpenRouter` 的「`502+` 模型」已非现行口径，且其来源为第三方转录，与本期官方 API 口径不可相减。
3. `freellm.net` 的 `No Credit Card` 由 `425+` 变为 `425`（口径表述变化，不可相减），并新增两个从未登记的面板字段
   （`Models Tracked 510`、`Free & Online 301`）。

**数据规模**：第四章表体 **228 行**（223 + 5 新增 / 8 改写，字段数全 3）；
`deadlines.csv` 228 条；`A5 + B21 + C52 + D137 + E13 = 228` 对账一致；
固化库 **434 条**（+8 首登）；待澄清口径 **35 条**（+5，Q32–Q36）；台账 **277 条**（+5，一手源 5 条）。

**工程侧三处自纠**：
- `MiniMax M3.1 Flash` 开放权重初稿另起一行（043 期已有该行）→ **改为 REWRITE**，表体 229 → 228。
- `gen_table044.py` 首次运行报 `IndexError` —— 脚注已从「小表」改成「列表」，按固定标记定位分节失效 → 改条件式。
- `reinject044.py` 按 `\n\n---` 定位表尾，**把已写入的脚注一起覆盖** → 改为按「连续的 `|` 行块末尾」定位。
- 色标笔误：`OpenAI` × `Model Garden` 初稿 `⚪ **⚪⚪` → 改 `⚠`（登记启动日未定）。

**守卫全绿**：`check_frozen`（高危 0）/ `extract_deadlines` + `check_deadlines`（对账一致）/ `check_tables`（10 表 ALL GREEN）/
`build_web` + `verify_web`（**VERDICT: ALL GREEN**，228 状态格多色标 0、裸 VS16 0）/ `build_source_hits` /
`build_index` + `build_index_web`（首页 44 期 / 2,435,081 字 / 649 张表 / 277 条信源）/ `check_site_freshness`（ALL GREEN）/
`audit_src036`（逐节括号数 = 实际行数 ALL GREEN）。

**明确未核到 / 受阻**：`mistral.ai/news` **第 4 次抓取失败**（`http=000`）→ 本期该处不写当日条目；
`huggingface.co` 主站网络层仍不可达（改用 `hf-mirror.com` API）；
`anthropic.com/news` 10/21 条目**标题未在列表页渲染**（仅确认存在）→ 记为未核到；
商务部 48 号公告回扫未见实施日公告与厂商办理指引，「义务已成立、通道未开」维持（距征求意见截止 11/15 剩 24 天）。

**用户补充的 T0–T4 清单逐条比对**：与台账逐条比对**无新增项、无缺项，不产生条目增删**（034–044 期连续十一期同结论）。
"""

AUTO_BLOCK = """
---

## 044 期（2026-10-22）· AI 免费内容与权益速递

**头条**：「同一天里 `OpenAI` 一口气发了 7 条公告，而其中真正带免费/补贴语义的只有一条」。
**窗口**：10/21 12:00 → 10/22 12:00（24.0 小时整日整段）。

**本期新增避坑 193–195**：
- **193**「免费」至少三层 —— **开源自取 / 定向补贴 / 身份权益**，三者获取成本完全不同，不可统称
  （本期样本：`OpenAI` `Patch the Planet` 一篇里三层并存，官方逐字 `We’re sharing` / `$1 billion`（面向资源有限的机构）/
  `Codex for OSS`（维护者需申请），**全页无 `free` 一词**）。
- **194** 官方页面改 URL（加尾斜杠）时「抓到空页」极易被误读成「活动已撤」→ **判定必须看正文规则表**
  （本期样本：`autoclaw.z.ai/blog/news/M10W3` 返回 301、0 字节，`curl -sL` 跟随后正文正常）。
- **195** 判断新产品「免费与否」有两条路；**「官方没说免费」这一路必须走完三步**（免费字样 → 权益归属 → 额度口径），
  三步都无 = 官方无免费额度（本期样本：`Anthropic` `Claude Duet`）。

**本期三条纠错**：① 043 期正文写「`20` 个仓库逐个核过」但自己列了 `21` 个（**本报告自己身上**）；
② 043 期 `OpenRouter`「`502+` 模型」已非现行口径（第三方转录源，与官方 API 口径不可相减）；
③ `freellm.net` `No Credit Card` 由 `425+` 变 `425`（口径表述变化，不可相减），并新增两个从未登记的面板字段。

**一手核查（全部实访）**：`openai.com/news/`（10/21 的 7 条逐条核对）、`openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/`
（`Patch the Planet` 全文）、`github.com/openai/php2shell-checker`（`Apache-2.0`、411 stars、created 10/21 00:29 UTC）、
`openai.com/index/openai-models-google-cloud/`（**全页无 free tier**）、`claude.com/resources/articles/claude-duet`、
`openrouter.ai/api/v1/models`（**468 / 21 / 18**）、`HF` `RecursiveSI/flint`（`apache-2.0` + `gated: false` + `downloads: 0`）、
`HF` `MiniMaxAI`（**21 个仓库，无 M3.1**；`MiniMax-H3` downloads 精确值 `5,007,397`）、
`github.com/vllm-project/humming`（`Apache-2.0`、284 stars、**`SM75+`**）、`autoclaw.z.ai` 国际站（**连续第 4 次仍是 85M**）、
`autoclaw.zhipuai.cn` 国内站（2 亿档可领窗口昨日已关闭）、`freellm.net`（`510+/30/241/425`）、
`openrouter.ai/docs/faq`（50 vs freellm 200 差 4 倍，**第 6 次记账**）。

**规模**：表体 **228 行**（223 + 5 / 改写 8）、`A5+B21+C52+D137+E13 = 228` 对账一致、固化库 **434 条**（+8）、
待澄清 **35 条**（+5）、台账 **277 条**（+5，模型与开源 33→35、官方一手·国外 49→52、T0 161→166）。

**工程侧三处自纠**：`M3.1 Flash` 行改写而非新增（229→228）；`gen_table044.py` 因脚注改列表而报 `IndexError` → 改条件式截断；
`reinject044.py` 按 `\n\n---` 定位表尾把脚注覆盖 → 改按 `|` 行块末尾定位。

**守卫全绿**：`check_frozen` 高危 0 / `check_deadlines` 对账一致 / `check_tables` 10 表 ALL GREEN /
`verify_web` **VERDICT: ALL GREEN**（228 状态格、多色标 0、裸 VS16 0）/ `audit_src036` 逐节括号数 = 实际行数 ALL GREEN /
`check_site_freshness` ALL GREEN。

**未核到 / 受阻**：`mistral.ai/news` **第 4 次抓取失败**；`huggingface.co` 主站不可达（改 `hf-mirror.com`）；
`anthropic.com/news` 10/21 标题未渲染；商务部 48 号公告「通道未开」维持（距 11/15 剩 24 天）。

**用户 T0–T4 清单逐条比对**：无新增项、无缺项、不产生条目增删（034–044 连续十一期同结论）。

**下一轮强制动作**：① `M3.1 Flash` 权重是否上传（回扫 10/23 之后）② `OpenRouter` 是否为 `recursive/flint-v1.0:free` 补公告页
③ `Model Garden` 的 GA 是否给确切日期 ④ `Claude Duet` 是否扩 `Team`/`Enterprise` 与非美区 ⑤ `AutoClaw` 国际站第 5 轮改写（10/25 后）
⑥ A 档三条（豆包工作 / MiniMax Code / 阿里云 AgentCore）是否收口 ⑦ `freellm.net` 计数器与 `:free` 清单逐条 diff
⑧ `platform.reflection.ai` 定价（连续第 6 期）⑨ `mistral.ai/news` 抓取恢复 ⑩ 老混元 Q04 连续第 33 期
⑪ 商务部登记「通道未开」（11/15 后）⑫ ZCode 月报连续第 19 期未见 ⑬ `anthropic.com/news` 标题渲染恢复
⑭ 044 期新登记的 `AutoClaw` 国内站每日登录档（10/25 收口）。
"""


def append(path, block, must_not):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    exists = os.path.exists(path)
    s = io.open(path, encoding="utf-8", newline="").read() if exists else ""
    assert must_not not in s, (path, "already present")
    s = s.rstrip("\n") + "\n" + block
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    print(path, "->", len(s.encode("utf-8")), "bytes")


append(DAY, LOG, "## 044 期（2026-10-22）· AI 免费内容与权益速递")
append(AUTO, AUTO_BLOCK, "## 044 期（2026-10-22）· AI 免费内容与权益速递")
