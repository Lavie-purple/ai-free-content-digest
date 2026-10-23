# -*- coding: utf-8 -*-
"""045 期台账修正：把 045 期真正新增的 2 条信源补进 ledger，并同步计数。

背景（定稿前核对抓到，避坑 44 同族）：
  045 md 初稿声称「本期新增 4 条信源」，核对台账发现
    - `MiniMax` 官方博客  早在 043 期已登记（line 148）
    - `OpenCode` 官方文档 早在 039 期已登记（line 97）
  真正首次取用的只有 2 条：`OpenAI News RSS`、`HF` API 详情端点 + raw 端点。
  本脚本按「计数与明细必须同源」补行 + 改标题 + 追加版本行。
⚠️ 台账是 LF；写回用 newline="\\n"。
"""
import io

F = "AI信息源分级清单-T0-T4.md"
lines = io.open(F, encoding="utf-8").read().split("\n")

# ---------- 0) 前置断言（0-indexed） ----------
assert lines[150].startswith("| **🆕 `Anthropic` 官方资源页（`Claude Duet`）**"), lines[150][:60]
assert lines[151] == "### 官方一手 · 国内（28）", lines[151][:40]
assert lines[29] == "## T0 · 根节点（166）", lines[29]
assert lines[92] == "### 官方一手 · 国外（52）", lines[92]
assert lines[96].startswith("| **🆕 OpenCode 官方文档"), lines[96][:60]
assert lines[60].startswith("| OpenRouter Models |"), lines[60][:40]
assert lines[3].startswith("；就地更新至 **2026-10-22（044 期"), lines[3][:40]

# ---------- 1) 两条新行（插在 官方一手·国外 节末） ----------
NEW_ROWS = [
 "| **🆕 `OpenAI News RSS`**（`openai.com/news/rss.xml`） | https://openai.com/news/rss.xml | ✅（**它本身就是 RSS**） | "
 "⚠️ **045 期新增 —— 本报告第一次把 `OpenAI` 的 RSS 当作公告列表的一手源**："
 "**`openai.com/news/` 列表页是 JS 渲染、直接抓只得约 9.7KB 空壳，而 RSS 给全量 `1,316` 条的标题 / 摘要 / 分类 / `pubDate` / `link`**"
 "（**正文仍需逐条抓 `/index/<slug>`，且必须带完整浏览器 UA，否则只得 9.7KB**）。"
 "**045 期 `Decisions API` GA、`Uber` 铺开、`NASK` 合作三条都是从它读到的**（避坑 194 同族：**取料路径本身要记进条目**） | — | 0 |",

 "| **🆕 `HF` API 仓库详情端点 + 原始文件端点**（`hf-mirror.com/api/models/<org>/<repo>`、`…/raw/main/README.md`、`…/raw/main/LICENSE`） | https://hf-mirror.com/api/models | — | "
 "⚠️ **045 期新增 —— 避坑 196 / 197 的直接来源**："
 "**组织页列表端点会漏仓库**（默认排序下 `?author=MiniMaxAI&limit=100` 只返 `21` 个、漏掉 10/17 就已建的 `MiniMaxAI/MiniMax-M3.1-Flash`；同一 URL 加 `&sort=createdAt&direction=-1` 才返 `22` 个），**详情端点不会**；"
 "**且 `README.md` 与 `LICENSE` 的 `raw` 路径是判许可的唯一可靠位置**（API 的 `license` 字段为空、`tags` 写 `license:other`、README 写 `license_name: minimax-community`，三个位置三个写法）。"
 "**⚠️ 本报告因 `huggingface.co` 主站网络层不可达，一律经 `hf-mirror.com` 读取 —— 该镜像域名此前不在台账内，本期随本行首次登记** | — | 0 |",
]

# ---------- 2) 既有行追加 045 期新用途 ----------
def append_use(idx, add):
    cells = lines[idx].strip().strip("|").split("|")
    assert len(cells) == 6, (idx, len(cells))
    cells[3] = cells[3].rstrip() + add
    lines[idx] = "| " + " | ".join(c.strip() for c in cells) + " |"

append_use(96,
 "；**⚠️ 045 期第二次关键取用（新用途：免费档收口判据源）**："
 "`docs/go` 模型列表去掉 `M3.1 Flash Free` 的 `Free` 后缀（现列 `M3.1` 与 `M3.1 Flash` 付费档）、"
 "`docs/zen` 的 `Free models` 段全文检索 `M3.1 Flash Free` 命中 `0` 次 —— **两页同时不再出现该字样，才构成「已于 10/22 前后下架」的结论**"
 "（避坑 199：单读一页会漏）；**`OpenCode` 官方未就此下架发任何说明，本报告不把 `OpenRouter` 的结束日套到它头上**。")

append_use(60,
 "；**⚠️ 045 期新增取料位：模型页顶部横幅** —— `openrouter.ai/minimax/minimax-m3.1-flash:free` 页面横幅逐字 `The free launch period ended Oct 22, 2026.`"
 "（**同页字段区仍写 `Price Free`、`Context 1.0M`、`Released Oct 19, 2026`，避坑 199**），"
 "**这是 041 期起「`OpenRouter` 无任何限免公告页」这条连续五期结论的第一次被打破，但打破它的不是公告页而是模型页**；"
 "本报告从本期起把「模型页横幅」列为与公告页同级的取料位。")

# ---------- 3) 标题两处 ----------
lines[92] = "### 官方一手 · 国外（54）"
lines[29] = "## T0 · 根节点（168）"

# ---------- 4) 版本行追加 045 条目 ----------
lines[3] = lines[3] + (
 "；就地更新至 **2026-10-23（045 期，条目数 277 → 279；"
 "**T0 官方一手 · 国外 +2**（**`OpenAI News RSS`** —— 公告列表的一手源，`openai.com/news/` 列表页 JS 渲染只返约 9.7KB 空壳、RSS 给全量 `1,316` 条元数据；"
 "**`HF` API 仓库详情端点 + 原始文件端点** —— 避坑 196/197 的直接来源，组织页列表端点会漏仓库、详情端点不会，且 `README.md` / `LICENSE` 的 `raw` 路径是判许可唯一可靠位置）"
 "→ **T0 合计 166 → 168**（**论文与预印本 12、模型与开源 35、官方一手 · 国内 28、政策与监管 22、评测与榜单 17 均不变**）、"
 "**T1 19、T2 18、T3 41、T4 33 均不变**）→ **全表 277 → 279 条**；"
 "**手写计数两处同步**（`### 官方一手 · 国外（52→54）`、`## T0 · 根节点（166→168）`）"
 "—— **站点首页「信源 N 条」= 五个 `## T\\d …（N）` 标题求和，只加行不改数会导致首页显示旧数字**；"
 "**本期就地更新 2 行**："
 "**`OpenCode` 官方文档两页**（**追加 045 期新用途：第一次被用作「免费档下架」的判据源** —— `docs/go` 去掉 `Free` 后缀、`docs/zen` 命中 `0` 次，两页合起来才构成收口结论，避坑 199）、"
 "**`OpenRouter Models`**（**追加 045 期新取料位：模型页顶部横幅可公布免费档结束日** —— `minimax/minimax-m3.1-flash:free` 逐字 `The free launch period ended Oct 22, 2026.`，与公告页同级；"
 "这是 041 期起「`OpenRouter` 无任何限免公告页」连续五期结论的第一次被打破，但打破它的不是公告页而是模型页）；"
 "**⚠️ 本期一处「差点重复登记」被定稿前核对当场抓住（避坑 44 同族）**："
 "**045 期初稿把 `MiniMax` 官方博客（043 期已登记）与 `OpenCode` 官方文档两页（039 期已登记）列成本期新增信源，核对台账时发现两行均已在库** —— "
 "**已改为「再次取用」并只给 `OpenCode` 追加新用途，不产生重复行**（「加行」之前必须先核「这一行是不是已经有了」）；"
 "**045 期另逐条核对用户随任务提供的 T0–T4 补充清单**："
 "**与台账逐条比对无新增项、无缺项，故不产生条目增删**"
 "（**其中 T0=97 / T1=19 / T2=18 / T3=36 / T4=12 = 182 条是分级清单的原始基线，与台账当前 279 条不是同一口径、不可相减**；"
 "**`https://aihot.news/` 与台账既有 `aihot.virxact.com` 仍为同一家的两个入口，033 期已核、本期结论不变**）**"
)

out = lines[:151] + NEW_ROWS + lines[151:]
io.open(F, "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("ledger updated: +2 rows, headers 52->54 / 166->168, version line appended")
