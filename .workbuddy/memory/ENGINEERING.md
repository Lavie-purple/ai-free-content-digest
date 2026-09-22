# 工程基建详解 · AI 免费内容与权益速递

> 本文件是 `MEMORY.md` 的**明细附卷**，2026-09-18 从 MEMORY.md 整节迁出（只整合，内容未删）。
> MEMORY.md 只留约定与索引；改工具链/版式前先读本文件。

## 一、网页版编译器与校验器（2026-09-17 建立）

- 编译器：`.workbuddy/build_web.py`。**常驻保留，不要删**。
- 用法（006 期起**命令行优先**；2026-09-17 起**不传参自动取日期最新一期**）：
  ```bash
  python .workbuddy/build_web.py                                    # 自动取最新
  python .workbuddy/build_web.py "AI免费内容与权益速递-第006期-2026-09-17.md"   # 指定期
  ```
  issue 号、日期、主题行从 md 的 `#`/`>` 自动提取。
- 校验器：`.workbuddy/verify_web.py`，用法同上。**每次编译后必须跑，判定标准 `VERDICT: ALL GREEN`。**
  四项：① 表格列数/行数逐表比对；② 全文片段保真（去标点后 ≥12 字符的片段必须能在 html 里找到）；③ 标签闭合/占位符/外部引用应为 0；④ 第四章状态格每格只应有一个色标且不留裸 U+FE0F。
  **注意**：保真比对必须**排除标题行**——html 里章节号渲染成 `01/02…`，md 里是 `一/二…`，直接比会假报缺失。比对前统一"只保留中英文数字"再比，能绕开所有 markdown 标点/emoji 的对称性问题。
- 产物特征：单文件自包含（**0 外部引用**，约 98–113 KB）、离线可开、可直接打印 A4。
- 已实现能力（改脚本时别弄丢）：顶部导航 + 侧栏目录双高亮、全文检索（带命中计数与上下条跳转）、第四章按状态筛选（必办/今日换挡/生效中/口径存疑/已结束）、明暗主题（localStorage 记忆 + prefers-color-scheme 兜底）、阅读进度条、移动端目录抽屉、打印样式。
- **状态判定规则（006 期修订，别再改回去）**：**以状态格里最先出现的色标为准**。旧实现是 `⚠️` 无条件优先，会把"🟢 生效中……⚠️ 另有口径"这类行错判成"口径存疑"并从"生效中"筛选里漏掉。现在只有 `⚠️` 出现在任何颜色标之前才判 warn；`已结束` 文字仍强制 over。
  **同时必须摘干净色标**：`⚠️` 是 `U+26A0 + U+FE0F`，只 replace 基字符会在正文里留一个裸变体选择符（肉眼看不见、但确实渲染出来）。统一用 `ST_ANY_RE` 摘除。
- **设计规范**（详见 `~/.workbuddy/skills/frontend-design`）：暖纸质底 + 墨黑正文 + 单一信号色（赭红 **`#bf3327`**，旧文写的 `#B23A1E` 是错的）；标题字号用 `em` 相对单位，**不要用 `clamp(vw)`**；装饰性文字必须显式给 `opacity`/背景色，不能依赖 `z-index:-1`（会被 body 背景吞掉）。
- **字号令牌各归其位**：`--fs-sm:13.5px`（辅助）/ `--fs-tbl:14px`（表格正文）/ `--fs-mid:15px`（刊例说明）/ `--fs-base:17px`（正文）。表格与刊例说明用专名令牌，改一处不牵连全文。

## 二、工具链（`.workbuddy/`，除注明外均可**不传参自动取最新一期**）

| 脚本 | 作用 | 何时跑 |
| --- | --- | --- |
| `build_web.py [src] [out]` | md → 单文件网页版 | 出稿后 |
| `verify_web.py [src] [out]` | 六项自查，须 `ALL GREEN` | 编译后 |
| `probe_layout.py [src] [--widths 1440,560]` | UI 量测（列宽满足度/搜索可用宽/压字），需 Edge | 改版式后 |
| `audit_color.py [build_web.py]` | 配色审计（色距/WCAG/opacity 叠加） | 改配色后 |
| `extract_deadlines.py [src]` | 第四章截止表 → `data/deadlines.csv` | 出刊前 |
| `check_deadlines.py [--days N] [--today D]` | 到期巡检（`--today` 可复现任意基准日） | 出刊前 |
| `check_frozen.py [src]` | 防重复往期，有 🔴 高危则 **exit 1** | 出刊前 |
| `check_tables.py [src]` | **md 表格逐行数 `\|` 与分隔行比对** + 避坑编号跨期连续 | 出稿后 |
| `build_source_hits.py [--dry]` | 信源命中 → 回写台账 + CSV（幂等） | 出刊后 |
| `build_index.py` | 重建根目录 `INDEX.md` | **每期必跑**（出刊后） |
| `build_index_web.py` | 生成 GitHub Pages 根目录 `index.html` | **每期必跑**（出刊后） |
| `check_site_freshness.py` | 站点新鲜度守卫：`index.html` / `INDEX.md` 是否落后于最新一期，落后 **exit 1** | **推送 Pages 前必须为 0** |
| `probe_mobile.py [src] [--widths 320,360,375,414] [--out f]` | **窄视口** DOM 量测（iframe 模拟），两份产物共用 | 改移动端版式后 |
| `snap_mobile.py` | 375×812 手机截图（日报 8 张 + 首页 3 张），iframe 内滚动 + md5 去重 | 改移动端版式后 |
| `run_all.py [job...]` | 统一入口，Python 捕获 stdout 写 UTF-8 日志到 `_shot/_<job>.log`；**默认已含 build/probe/verify/index/indexmd/fresh** | 随时 |

### 站点发布：两个「每期必跑」项（2026-09-19 事故，008 期）

- **症状**：`https://lavie-purple.github.io/ai-free-content-digest/` 在 008 期出刊后仍显示「更新至 **第 007 期**」，最新一期大卡片是 9/18 那期。而 `INDEX.md` 里 008 是好的——**两个产物一个跟上了、一个没跟上**。
- **根因**：出刊只跑了 `build_index.py`，**漏跑 `build_index_web.py`**。`index.html` 的 mtime 停在 9/18 09:11，比 008 期的 md 早整一天。**不是脚本坏了，是触发条件写错了**——工具表原先写「改首页后」，可每新增一期都等于改了首页，这句措辞本身就在鼓励漏跑。
- **为什么靠肉眼发现不了**：`git status` 是干净的（旧 `index.html` 早已随 007 期提交），`git push` 也成功、无任何报错。**只有把线上页面抓回来比对期号才会暴露**。
- **现在怎么防**：① `build_index.py` 与 `build_index_web.py` 的触发条件统一改成「**每期必跑**」；② 新增 `check_site_freshness.py` 守卫，落后即 `exit 1`（已用反向证伪验证：把 `index.html` 换成 007 版，精确报出 3 项落后）；③ `run_all.py` 默认任务已含 index / indexmd / fresh。
- **推 Pages 的完整收口顺序**：`build_source_hits.py` → `build_index.py` → `build_index_web.py` → `check_site_freshness.py`（须 ALL GREEN）→ commit → push → **API 核 sha** → **抓一次线上页面确认期号**。
- **CDN 缓存别误判**：Pages 响应带 `Cache-Control: max-age=600`。构建完成前抓页面会拿到旧副本（`X-Cache: MISS` 但内容是旧的，因为构建还没跑完）。自查时带随机参数（`?t=<ts>`）绕过本地缓存，并记住 **push 到构建完成有约 1–2 分钟延迟**，别把"还没构建完"误读成"没推上去"。查构建状态用 `GET /repos/{owner}/{repo}/pages/builds/latest`。

## 三、移动端适配（2026-09-17 定稿）

- **Windows 上 `--window-size` 量不了窄视口**：Edge/Chrome 最小窗口宽约 **490px**，320/375/414 全被静默夹到 489px。`--force-device-scale-factor` 只改 `devicePixelRatio`。**唯一可行路径是用 iframe 模拟宽度**（媒体查询按 iframe 宽求值），子页 `postMessage` → 父页写 `document.title` → `--dump-dom` 抓回。这就是 `probe_mobile.py` 的存在理由。
- **三档表处理策略**：2 列 → 纵向堆叠卡片（`thead{display:none}`）；3 列及以上 → 横向滚动 + `td{position:sticky;left:0}` 首列吸附；**截止表（台账）→ 卡片**，因为最关键的一列（截止日期）正好落在横滑视口之外，横滑等于藏起最重要信息。
- **`.tbl{overflow:hidden}` 会静默废掉 `td` 的 sticky**：表格自己成了滚动容器，sticky 参照它而非外层滚动器。CSS 不报错、看截图才发现首列跟着滚走。手机端块里必须 `.tbl{overflow:visible;border-radius:0}`。**验证法**：`wrap.scrollLeft=120` 后重量 `td` 的 `left`，不变才算粘住。
- **搜索框窄屏改「图标 → 展开全宽条」**：常驻会被压到只剩 26px 可用文本。输入框字号 **必须 ≥16px**，否则 iOS Safari 自动放大整页。
- **台账卡片列宽用 `grid-template-columns:max-content minmax(0,1fr)`**，不能用 `1fr auto`——长状态文字会把日期列挤成逐字换行。
- **触控目标 ≥40px**；`viewport-fit=cover` + `env(safe-area-inset-*)`（不支持的浏览器整条丢弃该声明，自动回退，无需 `@supports`）。
- **头部高度别写魔法数字**：JS `syncMetrics()` 从活的 `offsetHeight` 写 `--tb-h`/`--chips-h`，load/resize/`fonts.ready` 三处调用。
- 中文孤字/拆字：`text-wrap:pretty` / `text-wrap:balance`，或直接插 **WORD JOINER `&#8288;`**。
- 判定线：`verify_web.py` 仍须 `ALL GREEN`；`probe_mobile.py` 在 320/360/375/414 四档**横向溢出必须为 0**、触控偏小为 0、首列 `[粘住]`。

## 四、UI 审查的量化口径（2026-09-17 建立）

- **看截图不可靠，一律量 DOM。** 无头浏览器把指标写进 `document.title`，再用 `--dump-dom` 抓回来。实测抓到过两个只看截图会漏的问题。
- **「首列过窄」判据**（`probe_layout.py` 已内置）：实宽 < 140px **+ 行高 > 130px** + 首列 ≥4 字真文字 **+ 满足度 < 90%**，四条同时成立。行高门槛别调低（94px 只是正常折 2~3 行，会误报）；最后一条是为了不把「已按内容撑满」的列也标红。需求宽度用「临时 `white-space:nowrap` 后量 `scrollWidth`」得到。
- **量「压字」必须量文字矩形**：`h1`/`.pubnote` 是块级元素占满整行，量 `getBoundingClientRect()` 会稳定误报（右侧留白也算重叠）。改用 `TreeWalker` 遍历文本节点 + `Range.getClientRects()` 取每行矩形再求交。`mh-num` 定稿后与四块文字的矩形交集为 0。
- **截图三条硬规矩**（`probe_layout.py` 里已内置第一条）：① 必须先关入场动画 —— 页面大量用 `animation:...both` 起始 `opacity:0`，无头下会冻结在 t=0，拍出来「标题+正文整块空白」；② 想看中段**不能用「删兄弟节点」** —— 删掉 `.rail` 后 `.drawerwrap` 会掉进第 1 栏（196px），页面被挤成窄缝（实测 PNG 只有 15KB）；正确做法是保留栅格、只把前置内容 `display:none`；③ 一图一个 `--user-data-dir`，截完 `md5sum` 验一遍（全同=抓拍失败），再删 profile（每个十几 MB）。
- **配色审计看三样**：语义色色距（阈值 40；**同族色不互检** —— `accent` 与 `accent-ink` 本就该相近，放进 `SEM` 只会稳定误报）、WCAG 对比度（小字要 4.5）、整行 opacity 叠加后的实际对比度（脚本从源码正则读 opacity，**别写死**）。

## 五、版式与配色定稿（C 档全量落地，2026-09-17）

**布局**
- **截止表**：`table-layout:fixed` + 编译期按表头文字给 `<th>` 打 `data-col="date|st|body"`，列宽 **76px / 190px / 余量**。根因记牢：状态列的 `white-space:nowrap` 把该列 min-content 撑到整句宽（实测 **779px**），把「活动」列榨到 126px 逐字换行。
- **`clamp()` 不能用在 `table-layout:fixed` 的列宽上**：浏览器当 `auto` 处理，两列直接平分（实测活动/状态各 420px）。列宽只用定值 + 媒体查询。
- **首列下限**：编译期按内容估宽（CJK 14px/字、ASCII 7.4px/字，剔除 emoji 与 `**`），落在 **92~210px** 才输出 `--w1`；表头 `#` 的序号列与超长说明列跳过。上限卡 210 是因为表6 模型名需 303px，强行撑满会让表格溢出容器 151px。
- **绝不给 `.tblwrap:not(.scrolly)` 加 `overflow-x:auto`**：一个轴设 auto 会逼另一个轴也变 auto，`.tblwrap` 就成了滚动容器，`thead` 的 sticky 从「吸视口」退化为「吸容器」= 表头不再吸顶。窄屏那条可接受（窄屏必须横滑）。
- **搜索框**：空态让 `.sc`（计数 + 上下条）不占位（`input:not(:placeholder-shown)` 才给 `padding-right`），并 `.search{flex:0 0 auto}` 防被压扁——改前 560px 下可用文本宽只剩 **26px**（占位符被截成一个「全」），改后 **120px**。
- **刊头水印**：`clamp(60px,9.8vw,138px)`，`top:clamp(74px,7.4vw,106px)`，≤600px 收起。

**配色**
- 亮色：`crit #8c1a10`（原 `#b23028`，与 `accent` 色距 13.4 → 61）、`soon #8f5e12`、`muted #5f584a`、`faint #736a5a`、`over #6e675c`。
- 暗色：`crit #ff3b30`（原与 `accent` **完全同值 `#ff6d55`**，色距 **0.0**）、`faint #8e8577`、`over #9c9387`。
- **弱化「已结束」行不要用整行 `opacity`**：`.55` 把对比度从 3.55 拉到 **1.87**（低于可读线）。改由 `--over` 状态色本身承担。
- 验证后亮色最接近的一对 `live` vs `plan` = 48.6，暗色 `accent` vs `crit` = 62.2，均 > 40 ✓。

**一致性**
- 摘要章节号三处统一为 `··`（原来目录 `··`、正文 `00`）。
- 暗色水印描边 alpha 降到 `.20`（原用 `--rule-2`，比亮色还抢眼）。
- 清掉从未生效的 `.tb-brand span{display:none}`（模板里没有对应 span）；品牌改 `.tbb-long`/`.tbb-short` 双标记，≤820px 切短名。

## 六、结构化台账（`.workbuddy/data/`）

- `deadlines.csv` —— 截止时间表，**每期从正文重建**（保证与正文一致）。状态分类**关键词优先于色标**：🟢 同时用于"生效中"和"未开始"，只认色标会误判。
- `frozen_items.md` —— 已固化条目库。关键词必须能唯一命中（专有名 + 版本号），泛词会大面积误报。
- `open_questions.md` —— 待澄清口径。**挂满 3 期的必须升级为正式避坑**（Q01 Qoder 已达阈值）。
- `source_hits.csv` —— 信源命中统计。**口径是"品牌被提及"，不等于"实际取料"**，同域名的源会得到相同数字。可用输出是"零命中 124 条"那批（T2 94% / T3 92% 从未被引用）；**不要拿高命中数对外声称覆盖量**。

### 台账两个静默陷阱（2026-09-18 实测，各中一次）

- **`check_frozen.py` 会误报"本期新增"**：写「**006 期新增。**」这类**标注往期**的话，若同一行后文出现某个已固化条目的关键词，那句"新增"就落进**关键词前 25 字符窗口**，被判 🔴 高危（007 期 `Union Alpha` 中招一次）。**改法：标注写成「006 期登记」**，或把关键词挪出窗口。
- **🆕 25 字符窗口的完整口径（009 期实测，一次出刊被它挡了 7 行）**：`cond_a = NEW_PAT in l[pos-25:pos]`，其中 `pos = 该行第一次出现关键词的位置`。**三个容易踩的形态**：
  1. **同一表格行跨越单元格**——`| 🆕 **做决策类…** | **TypeSafe AI Jev** |`：`🆕` 在第一个单元格，关键词在第二个单元格，**窗口照样命中**（`| **` 只有 4 字符）。**表格行不能靠"标记放别列"绕开。**
  2. **标题里的固定前缀**——`### 2. 🆕 可灵「看见微光」…`，即使改为 `🆕 快手公益 × 可灵`，`🆕` 距关键词仍只有 9 字符。**唯一稳的写法是把标记移到关键词之后 ≥25 字符处，或整行不用 `🆕`/`新增` 字样**（用「本期登记」「多了一个免费入口」等替代）。
  3. **`可灵` 这类"泛指品牌"关键词**（首见 003 期）：任何提到可灵的行都可能被扫到，**包括信源更新段的"新增本期命中（…、快手公益×可灵、…）"**。**写这段时把"新增"换成"补入 / 已补入"。**
  **规矩**：**给一个首见期较早的泛品牌关键词写 🆕 时，先数一数**；实在要标新，就**在写「本期登记」的同时把标记从中括号里删掉**——`❌ 引用` 与 `🔴 高危` 只差这一处措辞，重跑一次只要 2 秒。
- **状态色标错用会静默污染 `deadlines.csv` 分类**：分类是"关键词优先、色标兜底"，行内没有状态关键词时**按色标判**——🟠 被归为 `switch`（换挡日）。007 期把 7 条"生效中"误写成 🟠，全部被判成换挡日。**色标语义固定：🟢 生效中·未开始 / 🟠 换挡日 / 🔴 必办 / 🟡 一般 / ⚪ 已结束。**（009 期复核：把"今天启动"与"今天收口"两类边界日写成 🟠 是**正确**用法——`check_deadlines` 会把它们列在【B】14 天内到期的首条，符合预期。）
- **第四章状态列的文本会被 `extract_deadlines.py` 字面读入，不得残留旧状态词的原文（011 期实测）**：分类规则是"**关键词优先、色标兜底**"。011 期有一条「智谱 ZCode 夜间免费」需要**从"已结束"改回"生效中"**，状态格当场写成了 `🟢 生效中（状态反转：本行由"已结束"改回…）`——**结果那三个字被字面命中，整行又被归进【C】已结束**。**改法：叙述状态反转时不要复述旧状态词，写"本行由终止状态改回生效中"。** **同源风险**：`check_frozen.py` 的 25 字符窗口、`check_deadlines.py` 的关键词优先，本质都是"**按文本原义读**"的守卫——**凡是要被守卫读的格子，别在里面写会被误读的历史叙述。**
- **色标归一 + 复核脚本（011 期新加）**：状态格**第一个字符必须是颜色**（`cells[2][0]`）——有些行原本从状态文本里带来第二个 emoji（如 ⚪ 行里又出现 ⚪），导致取色取错。**先跑归一脚本把每格首色对齐本行行首标记，再跑计数脚本读 `cells[-1][0]` 复核**（011 期：🔴 4 / 🟠 11 / 🟡 15 / 🟢 34 / ⚪ 11 = 75，与 `check_deadlines` 的 A0+B25+C11+D21+E18=75 互证）。

## 七、两条边界（都是有意为之，别"顺手"改掉）

- **不做物理归档**（不把旧期挪进子目录）：自动化需跨期回读历史日报来避免重复，挪走会打断它。改用 `INDEX.md` 解决"找得到"，不牺牲"读得到"。
- **编号以「期号」为准**，不用「第 N 次触发」——两者会脱钩（003/004 漏登记时，"第 3 次触发"产出的其实是第 005 期）。

## 八、改脚本时的两条幂等纪律

- **回写表格要按表头记下的原表列数截断**再补列，不能用"值等于列名"剥列——否则第二次运行会把已写进的 `005`/`3` 当成数据留下，表越跑越宽。
- **不要假设所有表同构**：台账 T3 两张表只有 3 列（无「用途」列），强行补齐会撑坏表。
- 改完务必验幂等：连跑两次 `diff` 必须无输出。已验证：`build_source_hits.py` 连跑三次字节一致。

## 九、版本控制

- 本工作区已是 git 仓库，远端 **`Lavie-purple/ai-free-content-digest`**（**2026-09-17 已由 private 改为 public**，默认分支 main）。每期出刊 + 编译 + 校验后提交一次。
- 根目录有 `README.md`（仓库首页）。改仓库结构或工具链时**记得同步它**——它列了目录树与工具链表，容易和实际脱钩。
- **沙箱会丢弃 `.git/refs/remotes/` 的写入**，所以 `git status` 常年显示 `[gone]`——**这是假象，别据此判断没推上去**。核实远端只能调 GitHub API 比对 `repos/<owner>/<repo>/commits/main` 的 sha 与本地 `HEAD`（`git push` 的回显也不可信）。
- **推销路：凭据助手取不到凭据时 `git push` 会直接失败或挂死（011 期实测，必须记住）**。本机 `credential.helper=helper-selector`（来自 `PortableGit/versions/1.2.0/etc/gitconfig`），但它**返回空**；在 `GIT_TERMINAL_PROMPT=0` 下立刻报 `could not read Username for 'https://github.com': terminal prompts disabled`。换成 `-c credential.helper=manager` 更糟——**卡在 GCM 的交互回退上，沙箱内外都不返回，2 分多钟无输出**。**可用写法**（命令行一条搞定，令牌不落盘）：
  ```sh
  export GH_TOK="$(printf 'protocol=https\nhost=github.com\n\n' | git-credential-manager get 2>/dev/null | sed -n 's/^password=//p' | tr -d '\r\n')"
  git -c credential.helper= -c credential.helper='!f() { echo username=Lavie-purple; echo "password=$GH_TOK"; }; f' push origin main
  ```
  **三个要点**：① `-c credential.helper=`（**空值**）必须显式写上，先把 `helper-selector` 清空，否则它仍会被调用；② `git-credential-manager get` 本身是好用的（011 期返回 `gho_` 40 位令牌，`api.github.com/user` → 200），**只有通过 git 调用它才出问题**；③ 令牌只走环境变量、命令里写的是 `$GH_TOK` 字面量，**不进 ps 列表、不落盘**。另：`timeout` 在 Git Bash 里会解析到 `C:\Windows\System32\TIMEOUT.EXE`（报"无效语法"），**要用 `/usr/bin/timeout`**。
- **Pages 构建要等，抓一次会误判**：推送后 `repos/<o>/<r>/pages/builds/latest` 会先返回 `building`（011 期：`created 10:06:03Z` → `built`，同 commit `3f73edc`）。**在此之前带 `?t=<ts>` 抓首页，拿到的仍是上一期**（011 期首次抓取显示「更新至 第 010 期」，本地/线上体积 16879/16533 B 不一致即为此故）。**正确顺序：push → API 核 sha → 轮询 `pages/builds/latest` 到 `built` → 再抓线上页**（完成后体积与本地 `index.html` 逐字节一致）。
