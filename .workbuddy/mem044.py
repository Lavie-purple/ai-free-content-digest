# -*- coding: utf-8 -*-
"""044 期：更新 MEMORY.md（追加 044 期索引）与 ENGINEERING.md（追加 §十·23 实测样本）。"""
import io

MEM = ".workbuddy/memory/MEMORY.md"
ENG = ".workbuddy/memory/ENGINEERING.md"

MEM_BLOCK = """
**044 期（2026-10-22）**
- **避坑 193**：**「免费」至少三层** —— **开源自取 / 定向补贴 / 身份权益**；**三者获取成本完全不同，不可统称**（本期样本：`OpenAI` `Patch the Planet` 一篇公告里三层并存，官方逐字 `We’re sharing` / `$1 billion` 面向机构 / `Codex for OSS` 面向维护者需申请，**全页无 `free` 一词**）。
- **避坑 194**：**官方页面改 URL（加尾斜杠）时「抓到空页」极易被误读成「活动已撤」** → **判定活动是否还在必须看正文规则表**（本期样本：`autoclaw.z.ai/blog/news/M10W3` 返回 `301`、0 字节，`curl -sL` 跟随后正文正常）。
- **避坑 195**：**判断新产品「免费与否」有两条路** —— **「官方说免费」与「官方没说免费」**；**后者必须走完三步**（① 找免费字样 → ② 找权益归属 → ③ 找额度口径），**三步都无 = 官方无免费额度**（本期样本：`Anthropic` `Claude Duet`）。
- **044 期一条工程纪律**：**「同一实体的状态推进」是改写（REWRITE），不是新增行** —— 本期初稿把 `MiniMax M3.1 Flash` 开放权重另起一行（043 期已有该行），**已改为改写**，表体由 229 回到 228（**新增 5 / 改写 8**）。
- **044 期一条取料纪律**：**公告的真实 slug 必须从列表页 HTML 里「标题之后的最近一个 href」取** —— `openai.com/index/patch-the-planet/` 抓到的是 6 月旧文，真实 slug 是 `/index/coordinated-disclosure-of-critical-vulnerabilities/`。
- **044 期一条脚本纪律**：**脚注从「小表」改成「列表」后，按固定标记定位分节的取表逻辑会失效** → **改成「存在即截断、不存在则不截断」的条件式**（与 043 期同一根因的两副面孔）。
"""

ENG_BLOCK = """
### §十·23 · 044 期（2026-10-22）五条实测样本

**背景**：044 期窗口 10/21 12:00 → 10/22 12:00（24.0 小时整日整段，不适用短窗口纪律）。头条是
「同一天里 `OpenAI` 一口气发了 7 条公告，而其中真正带免费/补贴语义的只有一条」。

**① 避坑 193 实测样本 —— 同一篇公告里三层「免费」并存（`OpenAI` `Patch the Planet`，2026-10-21）**
- **① 开源自取**：`github.com/openai/php2shell-checker` —— 官方逐字 `We’re sharing a PHP version checker as a Codex skill`；
  仓库实测 `Apache-2.0`、411 stars / 29 forks、created `2026-10-21T00:29:12Z`、pushed `2026-10-21T18:05:56Z`、description 空。
- **② 定向补贴**：官方逐字 `we’ve committed $1 billion in subsidized Daybreak access through Daybreak for Frontline Defenders,
  focused on organizations with limited security resources protecting essential services` —— **对象是机构，不是个人开发者；官方未给任何截止日**。
- **③ 身份权益**：官方逐字 `Our investments include subscriptions for all maintainers through Codex for OSS and direct sponsorship of
  projects such as the Rust Foundation` —— **入口在 `trailofbits.com/patch-the-planet/#apply`，不是自助领取**。
- **⚠️ 全页无 `free` 一词**，也无 `ChatGPT Pro` / `Codex Security` / `API credits` / `LiteLLM` / `Daybreak Blue`。
- **⚠️ 官方同时写 `Maintainers remain in control of what patches are deployed and how disclosure is handled`** ——
  **即这是「协调披露 + 补贴工具」，不是「厂商替所有人打补丁」**。
- **⚠️ 官方自认护栏取舍**：`safeguards intended to prevent abuse can also block legitimate security work`（与避坑 185 互为印证）。

**② 避坑 194 实测样本 —— 301 跳转被误读成「活动已撤」（`AutoClaw` 国际站）**
- `autoclaw.z.ai/blog/news/M10W3`（**无尾斜杠形态**）返回 **`301`、文件 0 字节**；
  `curl -sL` 跟随后 `autoclaw.z.ai/blog/news/M10W3/` 正文正常（`Get 85M Tokens`）。
- **判据**：**「抓到几字节」不是「活动还在不在」的判据；正文规则表才是**（避坑 179「现场打开」的取料侧延伸）。
- **本期该站活动页连续第 4 次实访仍是 `85M`**（官方未改回旧版口径）。

**③ 避坑 195 实测样本 —— 「官方没说免费」的三步法（`Anthropic` `Claude Duet`，2026-10-21）**
- **① 找免费字样 → 全篇无 `free`**；**② 找权益归属 → `included in Pro and Max plans and uses the same usage limits as the rest of Claude`**（含在付费套餐内）；
  **③ 找额度口径 → 官方给的是 `usage limits`（与 Claude 其余功能同一套限额），不是免费额度** → **结论：官方无免费额度**。
- 其余逐字：`starting with Pro and Max users in the US`、`available by waitlist today`、基于 `Opus 5.5`、
  `Its background checks count toward those limits`、`checks your connected accounts every few hours`；**`Team`/`Enterprise` 未说明**。

**④ 避坑 191 的第三个反例 —— `OpenRouter` 改用官方 API 目录**
- `openrouter.ai/api/v1/models` 实跑：**468 全量 / 21 零价 / 18 带 `:free`**；差额 3 个为
  `google/lyria-3-pro-preview`、`google/lyria-3-clip-preview`、`openrouter/free`（路由器）。
- 新增 `recursive/flint-v1.0:free`（created `1792622765` = 2026-10-21 22:46 UTC、ctx 262144、prompt/completion 均 0）；
  同期 `HF` `RecursiveSI/flint`：`apache-2.0` + `gated: false` + `downloads: 0` + `region:us` 标签。
- **官方 API 目录与模型页均无 `limited time` / `until`** → 第四章写「未公布」。
- **⚠️ 与第三方转录站三数都不同**：`freellm.net/providers/openrouter` 写 `20` 条、043 期正文写 `502+` 模型 ——
  **官方 API / 第三方转录 / 旧期正文三个口径互不相等，一律以官方 API 为准**。

**⑤ 工程侧：本期三处自纠**
- **「同一实体的状态推进」应为改写而非新增行**：初稿把 `MiniMax M3.1 Flash` 开放权重另起一行（043 期已有该行），
  **改为 REWRITE 后表体由 229 回到 228（新增 5 / 改写 8）** —— **判据：同一行名 + 同一实体 + 只是状态推进 → 改写**。
- **脚注从「小表」改成「列表」后，按固定标记定位分节的取表逻辑失效** —— `gen_table044.py` 首次运行报 `IndexError`；
  **修法：把「找到 `| 口径 | 分布 |` 则截断」改成条件式（找到即截断，找不到则不截断）**（与 043 期同一根因的两副面孔）。
- **回注脚本不能按 `\n\n---` 定位表尾** —— 本期 `reinject044.py` 用它定位，**把已写入的脚注一起覆盖掉了**；
  **修法：按「连续的以 `|` 开头的行块」末尾定位**。
- **色标笔误自纠**：`OpenAI` × `Google Cloud Model Garden` 初稿写 `⚪ **⚪⚪ ...`（连写两个色标，且 `⚪` 语义错 ——
  该条是「尚未 GA、启动日未公布」不是「已收口」）→ **本期改为 `⚠`（登记启动日未定），与脚本 `classify()` 的 `unclear` 结论一致**。
"""

m = io.open(MEM, encoding="utf-8", newline="").read()
assert "044 期（2026-10-22）" not in m
anchor = "\n## 出刊流水线（顺序固定）"
assert m.count(anchor) == 1
m = m.replace(anchor, MEM_BLOCK + anchor)
io.open(MEM, "w", encoding="utf-8", newline="\n").write(m)
print("MEMORY.md updated,", len(m.encode("utf-8")), "bytes")

e = io.open(ENG, encoding="utf-8", newline="").read()
assert "§十·23" not in e
e = e.rstrip("\n") + "\n" + ENG_BLOCK
io.open(ENG, "w", encoding="utf-8", newline="\n").write(e)
print("ENGINEERING.md updated,", len(e.encode("utf-8")), "bytes")
