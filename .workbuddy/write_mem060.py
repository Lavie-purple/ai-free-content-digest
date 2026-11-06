# -*- coding: utf-8 -*-
"""060 期执行记忆落盘：自动化记忆 append-only + 当日工作日志新建。

纪律：
  · 自动化记忆只能追加，不能重写/覆盖（054 期）。
  · memory/ 目录 LF；data/ 目录 CRLF —— 两种行尾不许混。
  · 写出后回读断言关键逐字短语（053 期：断言是必要条件，不是充分条件）。
"""
import io
import os

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
AUTO = WS + ".workbuddy/memory/automations/256c1349-ea4a-4721-9c5d-14067699f1f1/memory.md"
LOG = WS + ".workbuddy/memory/2026-11-06.md"

AUTO_TEXT = r"""

---

## 第 060 期 · 2026-11-06（窗口 北京 11/5 12:35 → 11/6 13:46，约 25.2h）

### 窗口与抓取
- **窗口**：北京 `2026-11-05 12:35 → 2026-11-06 13:46`（`25.2h`）；UTC `11/5 04:35 → 11/6 05:46`；美西 `11/4 20:35 PT → 11/5 21:46 PT`（跨美西两个日历日）。**隔日出刊，用「窗口 = 上期截止 → 本期截止」句式，不用同日双刊句式。**
- **主抓取 `fetch060.sh`**：复用 059 期 `284` 源清单（`tmp_060_list.txt`），`xargs -P 16`；**落盘 284 / 200 191 / 000 57（`20.1%）`**。`000` 时 `curl` 不建文件 → 显式写空占位（058 期纪律）。
- **专用核验 `fetch060_special.sh`**：059 期 20 条强制动作的对象（Ollie 三页、OpenRouter 目录/announcements、两个 `inkling:free`、`crouton`、OpenCode zen、Kimi LICENSE、Highspeed 搜索、Runware、Antigravity、商汤、scnet、freellm 等）。
- **百度专项 `fetch060_baidu.sh`**：`ernie.baidu.com/release/ernie-5-5-flash-base/`、`hf-mirror.com` 两个仓库 API + `raw/main/LICENSE` + README、`api.github.com/repos/baidu/vLLM-ERNIE`、`?search=Hy4`。
- **窗口解析 `tmp_060_window.py`**：`280` 个抓取件 / `3,135` 条带时间戳条目 / **窗口内 `118` 条**。正文按实算改为「`1` 条免费主线 ＋ `1` 条口径澄清 ＋ `114` 条不产生免费条目」（**计数与明细同源**）。

### 头条（本期主线：两份自定义许可同一天读全）
1. **百度 `11/5` 开源 `ERNIE-5.5-Flash-Base`** —— `280B` 总参 / `14B` 激活 / `33.5T` tokens / `43` 层 / `128K` 训练、`1M` 推理上下文 / `FP8` 与 `BF16` 双仓库各 `128` 个 `safetensors` 分片 / 未经中训练与后训练的 `Base` 权重。**`LICENSE` 全文 `25,619` 字节**：`ERNIE 5.5 Flash Base Model License Agreement v1.0`、`Release date: November 5, 2026`；**分三档有条件商用**（非商用免费／商用且年相关营收 ≤ `US$50M` 免费但须 `Powered by ERNIE` 署名 ＋ 一次性通知／> `US$50M` 须事先书面授权）；**`Territory` 逐字排除欧盟、英国、韩国**；`Exhibit A` `Last revised: November 6, 2026`。**`license:other` ≠ 法律意义的「开源」，本报告只写「开放权重 ＋ 自定义许可条件」。**
2. **`Kimi K3.1 Pro` 第四层「能商用」销项（059 期挂账一整期）** —— 一次 `hf-mirror.com/moonshotai/Kimi-K3.1-Pro/raw/main/LICENSE`（`200` / `3,077` 字节）就读到逐字 `Permission is hereby granted, free of charge … to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies`；**能商用成立，但挂两个门槛**：`MaaS` 且关联方连续 `12` 个月营收 > `US$20M` 须另签；商业产品 > `100 million MAU` 或月营收 > `US$20M` 须显著展示 `Kimi K3.1-Pro`；内部使用、官方产品／认证推理伙伴豁免。
3. **`OpenRouter` 三档计数 `454/16/12` 全同值、成员却换 `4` 个** —— `ID` 级 diff：出 `minimax/minimax-01`、`minimax-m2`、`minimax-m2-her`、`minimax-m2.1`（**MiniMax 四个付费模型整批下架**）；进 `google/gemini-omni-1.1-flash`、`1.2-flash`、`inclusionai/ling-3.0-tiny`、`openrouter/auto-code`。**报「同值」前必须先跑 ID 级 diff。**
4. **`Ollie` 今天（`11/6`）是告别信逐字写明的 `sunsetting` 生效日** —— `39,747` 字节逐字 `Ollie is sunsetting on Nov 6, 2026`、`effective Nov 6, 2026`、`billing will be canceled and you will receive a refund`；定价页 `41,791` 与 059 期逐字节相同，`Free ¥0` / `50 messages … per month` / `6 free additional messages … every day` 三处逐字仍在。**关停日当天页面与文案仍完整在线 —— 本报告不据此判定「服务仍开」或「已停」，只记页面状态。**
5. **两个 059 期强制动作同日销项**：`stealth/crouton-alpha` 第 `4` 天仍在（`created 1793669930`、`pricing 0/0`、`1,048,576` 上下文、`llms.txt 4,021` 同值），`OpenCode zen` 的 `crouton-alpha-free` 也还在（清单 `11` 项）；**两个 `inkling:free` 没有回归**（两个 `/llms.txt` 仍 `404`/`10` 字节，`/endpoints` `200` 但 `"endpoints": []`）—— **「下架可逆」第一次观测的答案是「没有」**。

### 059 期强制动作逐条答案
① `Ollie` `11/6` 关停**已实核**（生效日当天三页仍在线）；`Free` 档是否一并停服**官方仍无逐字口径，连续第 3 期无答案** ② `Kimi` 商用**已销项**（`LICENSE`）；`Highspeed` 版权重 **`?search=Kimi-K3.1-Highspeed` 返回 `[]`（`2` 字节，已归档）→ 官方名下 `0` 条** ③ 两个 `inkling:free` **没有回归** ④ `crouton-alpha` 第 `4` 天仍在、两站存活期未分叉 ⑤ `Runware` 促销数组本期 `18` 条（`endsAt` 命中 `18`）⑥ `tencent/hy4` 腾讯自有平台免费档连续第 `3` 期未复核 ⑦ `AXON` 许可证连续第 `3` 期未放出（`20,111` 逐字节同）⑧ 商汤 `6.8 Flash` 官方「限时免费」截止日第 `4` 期仍只有媒体口径 ⑨ `freellm.net` **已按约定改口径：正文直接写「该站已停止维护该字段」**（连续第 `9` 期停在 `2026-10-27`），不再逐期写「与上期同值」⑩ `Antigravity` `/docs/plans` 连续第 `4` 期未追 ⑪ `/models` 连续第 `9` 期 `404` ⑫ 老混元 `Q04` 连续第 `39` 期未决 ⑬ 豆包工作连续第 `16` 期未复核 ⑭ 国家超算互联网连续第 `10` 期 ⑮ `Mistral` 连续第 `21` 次 `000` ⑯ `platform.reflection.ai` 连续第 `23` 期 `403` ⑰ `platform.openai.com/docs/models` 连续第 `14` 期 `403` ⑱ `next.opera.com/web-ai/` 连续第 `11` 期 `451` ⑲ `docs.somark.ai/free-tier-rules.md` 连续第 `6` 期 `404` ⑳ **零命中页面全部入档**（`tmp_060_s/` 八件，出刊前逐个 `ls` 过）。

### 目录与同值记账
- **`freellm.net`** `535/296/31/454`、`171,340` 字节四期同值；**仍只作背景，不用于交叉验证 `OpenRouter`**。
- **`Antigravity` 定价页 `137,595` 同值**（本期 `ag_pricing.html`）；`/models` `404`。
- **两个 `AI-HOT` 入口**：`aihot.html` 与 `aihot_virxact.html` **各 `222,441` 字节且 `cmp` 逐字节相同** —— 用户本轮点名的 `https://aihot.news/` 与 `aihot.virxact.com`（`168` 信源分级）是同一份 `JS` SPA 的两个入口。**284 清单里共 `5` 个 `aihot*` 条目，路由去重按内容不按 URL 字面，否则「`200` 源数」虚增 `4`**（已写进正文第八章）。
- **商汤**：`sensetime_news.html` `限时`/`免费` 各 `0`；`token-plan` `20,820` 四期逐字节同；`xiaohuanxiong` 定价 `+1,413` 字节但 `¥0 / 永久 / 300 积分/日` 一字未改。
- **`AXON`** `20,111` 逐字节同，仍无许可证与版本号。

### 本期纠错 2 条（对 059 期）
1. **059 期把 `Kimi` 第四层写成「未判定」，其实是「没去读」** —— 证据只差一次 `raw/main/LICENSE` 请求（避坑 268）。**「读不到」要写 `HTTP` 状态与路径，「没去读」要当场补做；「需要更多证据」这种措辞一律不用。**
2. **059 期 `Ollie` 告别信的字节数差异被写成了方向性判断** —— 本期关停日当天实测三页仍完整在线、三处关键逐字未变。**本期起凡写「页面字节 `A → B`」，若关键逐字未变，只写「两次读到的字节数分别是 `A`/`B`，关键逐字未变」，不写方向、不写成因**（避坑 259 收紧版）。**纠的是表述，不是事实** —— 059 期关于关停日与 `Free` 档的结论本期全部成立。

### 本期新增避坑 264–269
264 **四层开放的第四层要拆成三到四问**（允不允许商用／到什么规模要另签／在哪些地区有效／附件修订日）—— 「有 `LICENSE` 文件」与「读过 `LICENSE` 条款」是两件事；
265 **`createdAt` 与发布日可以差 `15` 天** —— 百度两仓库 `createdAt` 都是 `2026-10-21`，`lastModified` 是 `11/05T06:33Z`/`06:37Z`，许可 `Release date: November 5, 2026`；**有 `lastModified` 且吻合发布日时它更接近公开时刻，但仍不写「精确放出时刻」**；
266 **「三档计数全同值」不等于目录没变** ＋ 同名不同版本（`tencent/Hy4-preview` 是 `8/27` 的 `Apache-2.0` 旧权重，与本周正式发布的付费 `tencent/hy4` 不是一件事）；
267 **`pricing` 里的 `"-1"` 不是价格** —— `openrouter/auto-code` 的 `prompt`/`completion` 逐字都是 `"-1"`（动态路由哨兵）；**零价必须严格相等 `str(v) in ("0","0.0")`，用 `float(price) <= 0` 会让零价 `16 → 17`**；
268 **「未判定」必须写清是「读不到」还是「没去读」**（第五章纠错顺带立条，不计入四条速查）；
269 **继承行的「本期」必须随期号重贴**（脚注 ⑤① 新立，见下）。

### 规模与对账
- 表体 **219** 行 ＝ 059 期 `218` ＋ 补入 `1`（`百度 ERNIE-5.5-Flash-Base`）− 移出 `0`；`gen_table060.py` 字段数分布 `Counter({3: 219})`；`prune_table.py` 移出 `0`（归档区最后一段仍是 `056 期`）。
- `split_ledger.py`：**`4.1` = `55` / `4.2` = `43` / 常驻未变 `121` / 总账全量 `164`**；极速视图 `76` 条（同值）、基准日 `2026-11-06`。
- 色标 ⚪2/🔴5/🟢150/🟡22/🟠7/⚠14/空19 = 219；`classify()` crit5/live167/over2/pending23/unclear16/switch6 = 219。**与 059 期逐桶对账：色标 🟢 `149→150`、`live 166→167`，各 `+1` 正是本期新增的 ERNIE 行；其余桶全部同值。**
- `check_deadlines` **A23 + B13 + C0 + D176 + E7 = 219**：**`A +2`（`Anthropic` 生命科学 guest investigators、`Claude Code` 云会话 credit 两条 `11/5` 跨过基准日）与 `B −2` 是同一件事的两面**；`D +1` 正是 ERNIE 新增行；`E 7` 连续两期同值同成员。
- **⚪ 与 `C` 的差额 `2` 逐条归因（不是拿常数相减）**：① `ZCode / BigModel 新用户试用`（相对期限 `连接 BigModel 账号后起算，第 5 天到期` → 落 `D`）② `智谱 AutoClaw「每日登录领 credits」第二期`（日期藏在叙述句里 → 落 `D`）。**056–060 五期连续同一对。**
- **4.2 的 `42 → 43` 是「进 `1` 条、出 `0` 条」**（`tmp_060_42diff.py` 实跑，4.1 为 `55→55`、进出皆 `0`）—— **但「出 0」不等于「没有条目该毕业」，见工程坑①。**

### 本期实测的工程坑（详见 060 期第四章脚注 ⑤）
- **① ⚠️ 继承行里的「本期」会过期，但 `split_ledger.py` 的 `CHANGE_RE = re.compile(r"(本期|060\s*期)")` 只看字面** —— `Vercel Labs fx` 是 059 期原文照搬，行内残留 3 处 059 期的「本期」（活动名「本期由 InfoQ … 带出」、状态列「不是本期新品」／「本期只是首次登记」），**结果被判成「本期有变化」，没有按 059 期 `AXON` 的先例毕业进总账**。**这就是 4.2「出 `0` 条」的全部原因**。**⚠️ 处置：不在已固化产物上重跑 `split_ledger.py`** —— 它重建 `intro` 会丢 049 期瘦身导语、`post` 会带出重复的 `pointer` 段，**修补动作本身会制造两处新错**；改为脚注点名 ＋ 列为 `061` 期强制动作①（**新立避坑 269**）。**与 059 期「桶是筛子，不是结论」同族：这次是「正则也是筛子」。**
- **② `createdAt` 不许写进截止列** —— 060 期新增行截止列写 `无结束日（license:other 自定义许可，无活动期）`；**若误用 `createdAt 10/21`，`D` 桶少 `1`、`A` 桶凭空多一条「已过 16 天」，头条「开源日」被提前半个月**。
- **③ 零价严格相等** —— `tmp_060_diff.py` 的 `zero()` 用 `str(v) in ("0","0.0")`；`gen_table060.py` 对哨兵值有逐字断言，**第一次写成 `` `"-1"` `` 断言失败，回读落盘文本才发现真值是 `` `"-1"/"-1"` ``** —— **断言本身也要拿落盘文本核对**（053 期「回读再断言」的第二次实证）。
- **④ 零命中连归档件一起留** —— 本期八件全部 `ls` 过：`hf_search_highspeed.json`（`2` B `[]`）、`inkling_free_llms.txt` 与 `inklingsmall_free_llms.txt`（各 `10` B `Not Found`）、`inkling_free_endpoints.json`（`525` B `"endpoints": []`）、`sensetime_news.html`（`115,245` B）、`scnet.html`（`132,924` B）、`xai_news.html` 与 `mistral_news.html`（`0` B 空占位）。
- **⑤ `slim` 只留状态列第一句** —— 060 期 `12` 条改写**全部**用 `set_status()` 整体改写，**没有一条**用 `append_note()`；两轮 `slim` 收敛后才取分类统计。**059 期纪律⑥第一次在下一期完整复用且 `0` 处返工。**
- **⑥ 附录当期段指针标签停在上期** —— `patch060_pointers.py` 把 `## 第 060 期` 段内 **`50` 处** `[附录 059]` 重贴为 `[附录 060]`、历史段 **`55` 处**未回改；正文 **`98` 处** `〔附录 060〕` 链接化；**计数都从落盘文件实算，脚本对「命中 0 条」显式断言失败**（避坑 257）。
- **⑦ `foot060.py` 的脚注数字先实跑再写入** —— 脚本从 `check_deadlines.py --today 2026-11-06` 输出与 `deadlines.csv` 实算三态桶／双口径，**断言等于脚注里要写的每个数字才允许落盘**，写出后回读落盘文件逐字断言 8 个短语。**脚注注入后重跑 `extract_deadlines.py`，CSV 仍 `219` 条**（脚注没污染表体解析）。

### 守卫（全绿）
- `lint_table --strict` **CLEAN（98 行 / R1–R4 全 0）**；`verify_web` **ALL GREEN（14 表逐表列数行数一致／缺失片段 0／98 状态格多色标 0）**；`check_tables` **ALL GREEN（14 表异常 0）**；`check_frozen` **🔴 0**（引用 `28`）；`build_site.sh` **两守卫 ALL GREEN**（五页同构、`index.html == quick.html` 同字节、极速基准日 = `2026-11-06`、`archive.html` 收录 `60` 期）；`chk_eol` memory/ 全 LF、data/ 全 CRLF。
- 产物：`AI免费内容与权益速递-第060期-2026-11-06.md`（正文十节）／`.html` `226,095` B；`index.html` = `quick.html` `43,013` B；`archive.html` `42,051` B；`standing.html` `341,795` B；`details.html` `2,226,039` B。
- `build_quick.py --check` 报 `16` 条相似度提示（另按规则跳过 `12` 条）：**人工逐条认定无本期新增漏登** —— 商汤小浣熊／Token Plan 已在 CSV（假阳性，名称措辞不同），`OXR`／`AXON`／`Claude Content Checker` 是往期既有缺口，**本期唯一免费主线 ERNIE 是开源权重、按极速页规则「发布／开源不进本页」**，故 `quick_items.csv` 本期不需因新内容刷新。**⚠️ 该 CSV 是手工维护、时间戳仍是上期，下期若新增可领额度必须同步。**

### 发布与台账
- **未核到 / 受阻**：`Mistral` 连续第 `21` 次 `000`；`platform.reflection.ai` 连续第 `23` 期 `403`；`platform.openai.com/docs/models` 连续第 `14` 期 `403`；`next.opera.com/web-ai/` 连续第 `11` 期 `451`；`antigravity.google/models` 连续第 `9` 期 `404`；`docs.somark.ai/free-tier-rules.md` 连续第 `6` 期 `404`；`x.ai/news` 本期 `000`。
- **`AI信息源分级清单-T0-T4.md` 本期未改动** —— 逐条核对用户随任务提供的 `T0–T4` 补充清单（T0 `97`／T1 `19`／T2 `18`／T3 `36`／T4 `12` = `182` 条原始基线）无新增项、无缺项；**版本行只记有条目增删的期次**，且 `182` 条基线与台账当前条目数不是同一口径、不可相减。**台账是内部件，不对外展示。**
- **下一轮强制动作（`061` 期出刊前必须逐条过，共 16 条，见 060 期脚注③）**；**最紧的五条**：① `Vercel Labs fx` 归类修正（3 处 059 期「本期」重贴为期号，预期 4.2 出 `1` 条毕业）—— **本期新立、优先级最高** ② `Ollie` 关停后续：核三页是否已下线、`Free` 档是否一并停服（连续第 `3` 期无逐字答案） ③ 两个 `inkling:free` 是否回归（**别把「端点数组为空」写成「模型已下架」**） ④ `crouton-alpha` 第 `5` 天 ＋ `OpenCode` 那份是否先消失 ⑤ `ERNIE` 首次复核（`Exhibit A` 修订日／`Territory` 排除清单／两仓库 `lastModified`）。
"""

LOG_TEXT = r"""# 2026-11-06 工作日志

## 完成：《AI 免费内容与权益速递》第 060 期出刊（全流水线）

- **窗口**：北京 `11/5 12:35 → 11/6 13:46`（`25.2h`）。主抓 `284` 源（落盘 `284` / `200` `191` / `000` `57`）＋ 专用核验 ＋ 百度 ERNIE 专项，共三层实抓。窗口内 `118/3,135` 条。
- **头条**：百度 `11/5` 开源 `ERNIE-5.5-Flash-Base`（`280B/14B` 激活、`FP8`+`BF16` 双仓库、`LICENSE` 分三档有条件商用、`Territory` 排除欧盟/英国/韩国）；`Kimi K3.1 Pro` 第四层「能商用」销项（`3,077` 字节 `LICENSE`）；`OpenRouter` 三档 `454/16/12` 全同值但 `ID` diff 换 `4` 个；`Ollie` `11/6` 关停生效日当天；`crouton-alpha` 第 `4` 天仍在、两个 `inkling:free` 未回归。
- **新增避坑 `264–269`**（正文 4 条 + 纠错 1 条 + 脚注 ⑤① 1 条）。

## 技术决策

1. **`Vercel Labs fx` 归类缺陷不就地重跑脚本** —— `split_ledger.py` 的 `CHANGE_RE` 只看「本期／当期期号」字面，继承行残留 3 处 059 期「本期」导致该行没毕业。**重跑该脚本会丢瘦身导语并重复 pointer 段**（修补动作制造两处新错），故按 059 期先例「不改脚本、在脚注点名」，并列入 `061` 期强制动作①（新立避坑 269）。
2. **脚注数字先实跑再写入** —— 新建 `.workbuddy/foot060.py`：从 `check_deadlines.py` 输出 + `deadlines.csv` 实算三态桶与双口径，断言等于将写入的每个数字才允许落盘；写出后回读文件逐字断言 8 个短语。注入后重跑 `extract_deadlines.py` 确认 CSV 仍 `219` 条。
3. **用户补充的两个 `AI-HOT` 入口给出逐字节实证** —— `aihot.html` 与 `aihot_virxact.html` 各 `222,441` 字节、`cmp` 相同，是同一份 JS SPA 的两个入口；写进第八章，并明确「路由去重按内容不按 URL 字面」（284 清单里 5 个 `aihot*` 条目不得各计一次抓取）。
4. **极速数据源未改动** —— `build_quick.py --check` 的 16 条提示经人工逐条认定为假阳性／往期既有缺口，本期唯一免费主线是开源权重（按规则不进极速页），故 `quick_items.csv` 不需因本期内容刷新；`check_site_freshness` 确认基准日 = `2026-11-06`。
5. **台账未改动** —— `AI信息源分级清单-T0-T4.md` 版本行只记有条目增删的期次；本期核对用户补充的 T0–T4 清单无增删。

## 关键文件

- 新建：`.workbuddy/foot060.py`（脚注生成 + 实算断言）、`.workbuddy/write_mem060.py`（记忆落盘）。
- 主交付：`AI免费内容与权益速递-第060期-2026-11-06.md` + 同名 `.html`（`226,095` B）。
- 站点五页重建：`index.html` == `quick.html`（`43,013` B）、`archive.html`（收录 60 期）、`standing.html`、`details.html`。
- 第四章脚注四段 + ⑤ 工程纪律 6 条；表体 `219` 行（`4.1 55` / `4.2 43` / 常驻未变 `121` / 总账 `164`）。

## 守卫结果（全绿）

`lint_table --strict` CLEAN · `verify_web` ALL GREEN · `check_tables` ALL GREEN · `check_frozen` 🔴 0 · `check_deadlines` `A23+B13+C0+D176+E7=219` · `build_site.sh` 两守卫 ALL GREEN · `chk_eol` 行尾合规 · 首页与极速同字节 · 占位符 `0`。
"""

# --- 自动化记忆：append-only ---
before = os.path.getsize(AUTO)
with io.open(AUTO, "a", encoding="utf-8", newline="\n") as f:
    f.write(AUTO_TEXT.lstrip("\n"))
after = os.path.getsize(AUTO)
assert after > before, "自动化记忆没有增长"
disk = io.open(AUTO, encoding="utf-8").read()
for p in [
    "## 第 060 期 · 2026-11-06",
    "新立避坑 269",
    "A23 + B13 + C0 + D176 + E7 = 219",
    "aihot.html` 与 `aihot_virxact.html",
    "下一轮强制动作（`061` 期",
]:
    assert p in disk, ("自动化记忆缺逐字短语", p)
assert disk.count("## 第 060 期 · 2026-11-06") == 1
print("自动化记忆追加:", before, "->", after, "bytes")

# --- 当日工作日志：新建 ---
assert not os.path.exists(LOG), "当日日志已存在，应改为追加而不是覆盖"
with io.open(LOG, "w", encoding="utf-8", newline="\n") as f:
    f.write(LOG_TEXT)
d2 = io.open(LOG, encoding="utf-8").read()
for p in ["# 2026-11-06 工作日志", "foot060.py", "ALL GREEN", "避坑 `264–269`"]:
    assert p in d2, ("日志缺逐字短语", p)
print("当日日志新建:", os.path.getsize(LOG), "bytes")
print("回读断言全部通过 ✔")
