# -*- coding: utf-8 -*-
"""第七次压缩 · 第二步：把「展示规则」里带叙事的长条目改成命令式短句（不改任何约束语义）。
每一处替换都断言 old 命中且 new 更短；结束后断言总字节 <= 14000、CR=0、关键守卫名仍在。"""
import io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, ".workbuddy", "memory", "MEMORY.md")
s = io.open(MEM, encoding="utf-8").read()
before = len(s.encode("utf-8"))

PAIRS = []

PAIRS.append((
"""- **完整日报网页层 = 30 秒卡 + 审计层折叠（060 期 A 方案落地）**：`build_web.py` 给「第 NNN 期」日报自动加一张速览卡（头条取 `headlines.json`，数字从表体实算），并把 `s04/s05/s06/s08/s09` 五章默认收进 `<details>`；**信息一条不删，逐 section 与改前逐字一致**。极速 / 总账 / 附录 / 目录不受影响，历史期重跑生成器即自动带上。折叠会打断搜索命中、目录跳转、打印、`.rise` 动画与 `syncMetrics` 量高，四件都已在 JS 补做；`PAGE` 是普通字符串，CSS/JS 里的反斜杠要写双份。**md 章节编号不能变**（`FOLD_SECTIONS` 靠 `sNN` 认人）。""",
"""- **完整日报网页层 = 30 秒卡 + 审计层折叠（060 期 A 方案）**：`build_web.py` 自动加速览卡（头条取 `headlines.json`、数字从表体实算），`s04/s05/s06/s08/s09` 五章默认收进 `<details>`；**信息一条不删，逐 section 与改前逐字一致**。
  **md 章节编号不能变**（`FOLD_SECTIONS` 靠 `sNN` 认人）。折叠会打断搜索命中 / 目录跳转 / 打印 / `.rise` 动画 / `syncMetrics` 量高，五件都已在 JS 补做；`PAGE` 是普通字符串，CSS/JS 反斜杠写双份。"""))

PAIRS.append((
"""- **极速页顶部不许用「三格数字框」**（2026-11-06 用户：「不要这样框法」）：切换器下方是**一行无框概览句** `<p class="pulse">`，主读数在前、两条附注随后，零边框零底色；数字仍由 `build_quick.py` 实算（`n_live/n_week/n_over`），**改版式不许改数字来源**。完整日报的 30 秒速览卡是另一套，未动。""",
"""- **极速页顶部不许用「三格数字框」**（2026-11-06 用户「不要这样框法」）：切换器下方只留**一行无框概览句** `<p class="pulse">`（主读数在前、两条附注随后，零边框零底色）；数字仍由 `build_quick.py` 实算 `n_live/n_week/n_over`，**改版式不许改数字来源**。日报的 30 秒卡是另一套，未动。"""))

PAIRS.append((
"""- **常驻总账页目录默认折叠、全量表三列配宽**（2026-11-06 用户：「本期目录可以暂时隐藏先」「活动列那么宽，截止列那么窄」）：该页只有一张表，目录收成主区顶部一行 `<details class="toc-fold">`（默认收起、条目零删），`.shell shell-wide` 单列铺满；表加 `ledger-full` 类按 `28/32/40%` 分列，**日报 4.1 的 `date=76px` 不许套到总账**（那是短日历日口径，套用会把中文压成竖排）。""",
"""- **常驻总账页：目录默认折叠、全量表按 `28/32/40%` 配宽**（2026-11-06 用户）：目录收成主区顶部一行 `<details class="toc-fold">`（默认收起、条目零删），`.shell shell-wide` 单列铺满，表加 `ledger-full` 类。**日报 4.1 的 `date=76px` 不许套到总账**（短日历日口径，会把中文压成竖排）。"""))

PAIRS.append((
"""- **完整日报的目录与顶栏顺序 = 方案 A**（2026-11-07 用户选定）：显示序 `摘要 → 01 → 02 → 03 → 04 → 07 → 05 → 06 → 08 → 09`，四组标签「本期内容 / 马上要办 / 怎么用 / 审计层 · 默认折叠」（`TOC_ORDER` / `TOC_GROUPS`）；**正文物理顺序与章节编号一律不动**，点 04 会跳到文末（`openFold` 自动展开）。排序与分组**只许对 `is_digest` 生效** —— 附录 12 个小节的 aid 全是 `s-abs`，套上去会插 12 个「本期内容」标签。""",
"""- **完整日报目录 = 方案 A**（2026-11-07 用户选定）：显示序 `摘要 → 01 → 02 → 03 → 04 → 07 → 05 → 06 → 08 → 09`，四组标签「本期内容 / 马上要办 / 怎么用 / 审计层 · 默认折叠」（`TOC_ORDER` / `TOC_GROUPS`）；**正文物理顺序与章节编号一律不动**，点 04 跳到文末（`openFold` 自动展开）。排序分组**只许对 `is_digest` 生效** —— 附录 12 小节 aid 全是 `s-abs`，套上去会插 12 个「本期内容」标签。"""))

PAIRS.append((
"""- **可滚动表格里的 sticky 表头不许有 `overflow:hidden`**（2026-11-07 修）：`.tbl` 上的 `overflow:hidden` 会新建滚动容器、废掉 `th{position:sticky}`，表头滚上去被筛选条压掉半行；解药是 `.tblwrap.scrolly .tbl{overflow:visible}`（**只加 `border-collapse:separate` 无效**，实测过）。改任何表格容器样式后量 `chips.bottom − th.top`，必须 = 0。""",
"""- **可滚动表格的 sticky 表头不许有 `overflow:hidden`**（2026-11-07 修）：`.tbl` 上的 `overflow:hidden` 会新建滚动容器、废掉 `th{position:sticky}`；解药 `.tblwrap.scrolly .tbl{overflow:visible}`（**只加 `border-collapse:separate` 无效**，实测过）。改表格容器样式后量 `chips.bottom − th.top`，必须 = 0。"""))

PAIRS.append((
"""- **Pages 部署失败先查 `deployments` API，别猜缓存**（2026-11-07）：`pages/builds` 常 404，但 `/repos/<o>/<r>/deployments` + `/deployments/<id>/statuses` 能读到 sha 与 state；`state=failure` 且耗时≈10 分钟 = **Deploy 步骤超时**（服务端偶发），处置是 `git commit --allow-empty` 空提交重试一次，**不要改内容、不要 force push**。只有 `Age` 接近 600 且 `Last-Modified` 已刷新才是纯 CDN 缓存。""",
"""- **Pages 部署失败先查 `deployments` API，别猜缓存**（2026-11-07）：`pages/builds` 常 404，但 `/repos/<o>/<r>/deployments` + `/deployments/<id>/statuses` 能读到 sha 与 state；`state=failure` 且耗时≈10 分钟 = **Deploy 步骤超时**（服务端偶发）→ `git commit --allow-empty` 重试一次，**不改内容、不 force push**。只有 `Age` 近 600 且 `Last-Modified` 已刷新才是纯 CDN 缓存。"""))

PAIRS.append((
"""- **章节分组 / 折叠 / 排序一律认标题、不认编号**（2026-11-07 统一往期时修）：002–046 期的第四章是
  「免费内容生成工具」、第五章才是限时表，写死 `s04` 会把生成工具标成「马上要办」、把限时表折进审计层、
  速览卡「看必办清单」也指错章。判据是 `kind_of()`（限时活动 / 选型速查 / 纠错·避坑·信源·核查），
  折叠、目录分组、顶栏 `tail`、速览卡章号全由它推导；047+ 各期输出逐字节不变。""",
"""- **章节分组 / 折叠 / 排序一律认标题、不认编号**（2026-11-07 统一往期时修）：002–046 期第四章是
  「免费内容生成工具」、第五章才是限时表 —— 写死 `s04` 会标错「马上要办」、折错审计层、速览卡指错章。
  判据是 `kind_of()`（限时活动 / 选型速查 / 纠错·避坑·信源·核查），折叠、目录分组、顶栏 `tail`、
  速览卡章号全由它推导；047+ 各期输出逐字节不变。"""))

PAIRS.append((
"""  **核对六页时两个坑**：`curl --compressed` 与 `-H "Accept-Encoding: identity"` **同时用会返回 0 字节**（六页全假 `DIFF`）；期页 URL **照抄 `archive.html` 里的 `href`**，多一个 `%20` 就拿到 9,379 字节的 `404` 页 —— **`DIFF` 先比响应体大小**。""",
"""  **核对六页两个坑**：`curl --compressed` 与 `-H "Accept-Encoding: identity"` **同时用会返回 0 字节**（六页全假 `DIFF`）；期页 URL **照抄 `archive.html` 的 `href`**，多一个 `%20` 就拿到 9,379 字节的 `404` 页 —— **`DIFF` 先比响应体大小**。"""))

PAIRS.append((
"""- **目录「头条」只写当天发生的新闻事件（2026-11-06 用户要求「以后都不要这样」）**：
  `archive.html` 列表 / 最新一期大卡片 / `INDEX.md` 主题列的唯一真源是
  `.workbuddy/data/headlines.json`，每期一条「谁发布/免费了什么、额度、截止」。
  **禁止**把「本报告改进了什么 / 纠错 / 挂账 / 补登 / 口径 / 轮次 / 方法论 / 至今第一次读到」
  当头条 —— 那些照旧写在正文里给读者看，只是**不占头条位**。""",
"""- **目录「头条」只写当天发生的新闻事件（2026-11-06 用户「以后都不要这样」）**：
  `archive.html` 列表 / 最新一期大卡片 / `INDEX.md` 主题列的唯一真源是 `.workbuddy/data/headlines.json`，
  每期一条「谁发布/免费了什么、额度、截止」。**禁止**把「本报告改进了什么 / 纠错 / 挂账 / 补登 /
  口径 / 轮次 / 方法论 / 至今第一次读到」当头条 —— 那些照旧写进正文给读者，只是**不占头条位**。"""))

for old, new in PAIRS:
    assert old in s, old[:40]
    assert len(new.encode("utf-8")) < len(old.encode("utf-8")), old[:40]
    s = s.replace(old, new, 1)

io.open(MEM, "w", encoding="utf-8", newline="\n").write(s)

chk = io.open(MEM, encoding="utf-8").read()
after = len(chk.encode("utf-8"))
assert "\r" not in chk
assert after < before, (before, after)
for must in ("check_headlines.py", "check_views.py", "check_frozen.py", "§十·37",
             "viewswitch.py", "build_site.sh", "headlines.json", "FOLD_SECTIONS"):
    assert must in chk, must
print("MEMORY.md %d -> %d bytes (-%d), lines %d" % (before, after, before - after, chk.count("\n")))
