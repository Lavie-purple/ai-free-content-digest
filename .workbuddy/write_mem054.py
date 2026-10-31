# -*- coding: utf-8 -*-
"""054 期：写盘三处记忆 —— 自动化 memory、当日日志、项目 MEMORY、工程附卷。"""
import io
import os

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MEM = WS + ".workbuddy/memory/"

# ---------------------------------------------------------------- 1) 自动化 memory
P1 = MEM + "automations/256c1349-ea4a-4721-9c5d-14067699f1f1/memory.md"

T1 = """

## 2026-10-31 第 054 期（隔日出刊 + OXR 官方免费 API 首现「免注册免 key ＋ 明写数字」）

- **状态**：成功。**窗口 = 053 期截止 10/30 09:30 → 本期截止 10/31 19:00（北京），约 33.5 小时**；美西/北京双向换算：起 北京 10/30 09:30 ＝ 美西 10/29 18:30 PT、止 北京 10/31 19:00 ＝ 美西 10/31 04:00 PT（**窗口跨越两个美西日**：美西 10/29 18:30 → 10/30 24:00 ＋ 10/31 00:00 → 04:00）。**本期是隔日出刊**（**两期不合并**）。
- **规模**：全量扫 **417** 个抓取件（另补抓 100 余个专项一手页）、解析出 **4,436** 条带时间戳条目、**窗口内 109 条** —— **逐条归因后只有 5 条产生免费内容条目**。

### 头条
- **⚠️ `OXR`（`SoMark` 团队）`1.3B` 开放权重文档解析模型 + 官方「免费 API」—— 本报告至今第一次读到「免注册、免 `API key`、且官方把免费额度写成具体数字」的免费 API**：一手 `github.com/SoMarkAI/OXR`（`README.md` `200`/`19,333` 字节、`LICENSE` `200`/`2,394`）、`huggingface.co/SoMarkAI/OXR-1.0`（`downloads 3,180`/`likes 132`/`gated false`）、**`docs.somark.ai` 的 `free-tier-rules.md`（`200`/`1,290` 字节 —— 本期最硬的一条一手证据）**、`docs.somark.ai` 的 `oxr/index.md`（`200`/`4,580`）、`docs.somark.ai/llms.txt`（`200`/`6,561`）。**官方逐字（规则表）**：`Up to 500 pages of free quota per day` ／ `Up to 2000 pages of free quota per month` ／ `Daily free quota resets at 00:00 each day` ／ `Monthly free quota resets at 00:00 on the 1st of each month`。**官方逐字（`Free API` 段）**：`OXR provides a free API so you can test parsing on your own documents without registering or requesting an API key.`、`The Free OXR API requires no authentication. Set api_key to any value, such as dummy.`。⚠️ **官方同时写了两条限制，逐字照录**：`We do not recommend using the Free OXR API in production.`、单文件 `10MB`/单请求 `20` 页。⚠️ **归期如实写**：`README.md` 的 `Free API` 段**最早见于提交 `0245ee0e`（`2026-10-19T10:11:58Z`）**（本报告实读逐 commit 的 README 内容确认）→ **落在 051 期窗口之前，本期按「首次登记的往期事件」写入**（避坑 229）。
- **⚠️ `AutoClaw` 万圣节双周档 `M11W1` —— 国际站 `80M`、国内站 `50M`，两个官方站点给了两个数、两个起始日**：一手 `autoclaw.z.ai/blog/news/M11W1/`（`200`/`42,467`，`datePublished 2026-10-30T08:17:44Z` ＝ 北京 10/30 16:17，**窗口内**）、`autoclaw.zhipuai.cn/blog/news/M11W1/`（`200`/`47,058`，`datePublished 2026-10-30T10:07:34Z` ＝ 北京 10/30 18:07，**窗口内**）。⚠️ **三个数都不一样**：上限 `80M` vs `50M`、起始日 `10/31` vs `11/2`、积分当量 `8,000` vs `5,000`；**到期日相同（`11/8`）**。
- **⚠️ `Moonshot` `K2` 系列 `10/31` 停新 —— 官方定价页逐字原文终于核到（被追 7 期的挂账项，本期销项）**：一手 `platform.moonshot.cn/docs/pricing/chat` 与 `platform.kimi.com/docs/pricing/chat`（各 `200`/`1,701`）。**官方逐字**：`K2 系列模型将于 2026 年 10 月 31 日起停止向新注册用户开放，已注册用户不受影响；我们计划在 12 月底下线所有 K2 系列模型。` ⚠️ **053 期记的是「四个候选文档页各命中 `0` 次」—— 本期在同一份 `kimi_pricing2.html` 上实读 `停止`/`下线`/`2026 年 10 月 31 日` 各命中 `1` 次**：即 053 期是「当期没读到那一段」、不是「官方没写」（新立避坑 243）。
- **⚠️ `Anthropic` 订阅档改版**：`Max 5x`→`Max`、`Max 20x`→`Ultra`，一手 `claude.com/pricing`（`200`/`1,323,504`）+ `support.claude.com/en/articles/11175166-...`（`200`/`254,392`）。**官方逐字**：`No 5-hour limit ‡ 10x Pro usage every week* $200 a month in API credits, up from $100 on Max † New`、脚注 `‡ No 5-hour limit for verified accounts.`；**与免费读者相关的只有 `Free` 档 —— 官方对照表两格都写 `Limited`**。
- **⚠️ `MiniMax` `H3` 的开源替代 `Open-H3-Regenerate-2K`**（`NVIDIA`+`MIT` 团队）—— 一手 `github.com/NVlabs/Sana` 的 **`sol-engine` 分支**（**不在 `main` 分支上 —— `commits?path=` 在默认分支返回 `0` 条、必须显式 `?sha=sol-engine`**），分支头提交 `781e8341`（`2026-10-30T07:01:24Z` ＝ 北京 10/30 15:01，**窗口内**）。官方逐字：`An open replacement for the closed H3-Regenerate-2K API`。⚠️ `HF` 实读 `downloads 0`；**权重许可是 `minimax-h3-community`、不是仓库的 `apache-2.0`**。

### 本期纠错 4 条
1. **⚠️ 053 期的「逐条零变化」口径本期被打破 —— `Runware` 促销数组里有一条的截止日被官方改了**：`heygen-video-1-0-launch-promo` 的 `endsAt` 从 `2026-10-31` 变成 `2026-11-30`、描述逐字从「`until October 31, 2026`」变成「`until November 30, 2026`」—— **官方把促销延长了 `30` 天**。**即「条数不变、过期数不变、单条内容可变」是第三种变化形态**（避坑 238 的新变体）。
2. **⚠️ 053 期的正文结论成立、但第四章表体与《常驻权益总账》没跟上（两条）**：`OpenRouter` 目录三个数（表体仍是 `464/19/16`）、`百度` `Unlimited OCR 2` 下载量（表体被 `slim` 裁掉了 `downloads`/`likes`）。**⚠️ 这是「表体层比正文层慢一拍」的第三种形态：不是数字写错、是数字被裁掉。**
3. **⚠️ 053 期记的「`K2` 系列 `10/31` 停新未核到」—— 本期在同一份文件上实读命中**（新立避坑 243）。
4. **⚠️ 053 期记的「`百度` `Unlimited OCR 2` 单期涨 `9,784`」被本期的实测改写了增速口径**：本期 `18,141` → `69,231`，**单期涨 `51,090`（涨 `281%）**，比 053 期那一跳还大 `5.2` 倍。

### 本期新增避坑（240–243）
240. **同一个活动在两个官方站点上可以给两个不同的数、两个不同的起始日、两个不同的积分当量** —— `AutoClaw` `M11W1`（国际 `80M`/`10/31`/`8,000 credits` vs 国内 `50M`/`11/2`/`5,000 积分`，到期日相同）。与避坑 41 同族但更强：**041 说的是「同一家厂商的多条产品线别混」，240 说的是「同一个活动在两个官方站点上就是两个活动，连起始日都不同」**。
241. **官方文档站如果有 `llms.txt` 索引，那份索引里的 `.md` 原文往往比网页正文更硬 —— 而且它常常是唯一给出「免费额度具体是多少」的地方** —— `docs.somark.ai/llms.txt` → `free-tier-rules.md` → 官方逐字 `500` 页/日 + `2,000` 页/月（**这些数字在 `oxr/index.md` 里一个字都没有**）。
242. **「开放权重 + `Apache-2.0` 底子」不等于「无附加条款」** —— `OXR` 的 `LICENSE` 三条附加条款：商用免单独许可有 `$2,000,000` 双阈值、对外在线服务须显著署名、禁止做竞品托管 API。
243. **「grep 零命中」只能证明「这次没搜到」，不能证明「官方没写」** —— 053 期搜「停新」而官方写「停止向新注册用户开放」，差一个词全盘落空。**判据：要下「官方没写」的结论，必须在同一份文件上用至少三组同义表述各搜一次。**

### 规模与对账
- 表体 **203** 行 ＝ 053 期 199 行 ＋ 本期新增 **6** 行 − 移出 **2** 行（`上海青浦算力券补贴`、`OpenAI` `o4-mini` API 停用，均为「过期 >7 天且已收口（⚪）」，原文逐行归档 `data/deadline_archive.md` 的「054 期」节）；`4.1` = **56** / `4.2` = **31**；**总账 147** 条；**速查页 71** 条。
- 色标 ⚪4/🔴4/🟢142/🟡22/🟠7/⚠5/空19 = 203；classify crit4/live158/over4/pending23/unclear8/switch6 = 203；**A7 + B26 + C2 + D159 + E9 = 203** ✔。
- ⚪ 与 over 本期**个数相同（4=4）且成员逐条一致** —— 写「本期恰好对上」。
- **「距今 N 天」由 `recalc_days054.py` 逐行独立重算**（14 行全部需改写、**无一行继承值与真值相同** —— 这本身就是「基准日真的推进了」的证据）；断言是「天数 == 截止日 − 基准日」。
- `lint_table.py --strict` **CLEAN**；`verify_web` **ALL GREEN**；`check_views` **ALL GREEN**（极速 71 / 总账 147）；`check_site_freshness` **ALL GREEN**；`check_frozen` **🔴 0**；`build_quick --check` 全覆盖。

### 本期实测的工程坑（全部已修）
- **① 「状态列里不能出现会被 `classify()` 字面误读的词」—— 本期又踩了一次，处置仍是「改措辞、不放宽守卫」**：初稿在 `国家超算互联网` 那行的尾注里写了「**不写「已结束」**」这句说明性的话，`classify()` 按字面文本判定 → **整行被误判成 `over` 桶**。**处置：把说明改成不带判定词的表述（「不写收口字样」）**。**053 期踩 `4` 次、本期踩 `1` 次**。
- **② 「markdown 表格单元格里不能出现竖线」**：本期新增的两行分别引用了 `claude.com/pricing` 的官方对照表与 `docs.somark.ai` 的官方规则表 —— **原文都含竖线，直接逐字贴进单元格会让该行字段数从 `3` 变成 `7` 与 `11`、整张表渲染错位**。**处置：把 `|` 转写成 `／` 分隔并保留「一行四格」「一行：」的原文结构说明**（`gen_table054.py` 的字段数分布断言 `Counter({3: 205})` 就是这条纪律的守门断言）。
- **③ 「表体层比正文层慢一拍」有第三种形态：不是数字写错，是数字被裁掉** —— `slim_table.py` 把 053 期那条 `百度` 行的 `downloads`/`likes` 裁掉了。**处置：把本期实读的流通量直接追加到该行的 tail 里**（流通量是避坑 029 的必记账项）。
- **④ `check_frozen` 的 🔴 高危本期触发 1 条，是措辞触发**：台账里 `REA`（`Reverse Engineer Anything`）这个关键词会**在 `README.md` 里被字面命中** —— 我那行的尾注以「不写成「本期新增」」结尾，落在 `NEW_PAT` 里 → 被判「声称新增」。**处置：改成「不写成「本期首条」」**。**这是 053 期立的那条纪律的第四种触发形态：关键词子串误命中**。
- **⑤ 台账计数改动必须按「行首标题」定位**：文件开头那段「历史沿革」长段落里**也含同名的分类名** —— 全局 `replace` 会改到历史叙述里的数字、而不是标题里的数字。**054 期第一次跑更新脚本就踩了，已改回并用行首定位重跑**。

### 发布
- **未核到 / 受阻**：`mistral.ai` 全站连续第 `14` 次 `000`；`platform.openai.com/docs/models` 连续第 `7` 期 `403`；`platform.reflection.ai` 连续第 `16` 期 `403`；`antigravity.google/models` 连续第 `3` 期 `404`；`next.opera.com/web-ai/` 连续第 `4` 期 `451`；`docs.unsloth.ai` 404（连续第 `3` 期）；`www.scnet.cn` 官方页六个关键词零命中（连续第 `2` 期）；`volcengine.com/product/doubao` 与 `/product/doubao-work` 均 `200` 但正文只有 `178` 字节 JS 壳（连续第 `8` 期）；`openrouter.ai/announcements/csam-screening` 与 `/blog/csam-screening` 均 `200` 但正文只有重定向壳；`deepmind.google/discover/blog/gemini-4-carbon/` 两种 slug 都 `404`（**但博客首页核到了条目**）。
- **下一轮强制动作（31 条，见 054 期第四章脚注③）**：最紧的八条 —— ① `豆包工作 30 天订阅`（A 档已过 `14` 天、连续第 `8` 期零命中）② `国家超算互联网` 官方页的「夜间免费」栏（连续第 `2` 期）③ `Mistral` 官方公告页原文（连续第 `14` 次 `000`）④ `Mistral` demo 免费预算的额度数字与日历日 ⑤ `AutoClaw` 国际站 `M10W4` 残留文案官方是否会改（**本期实访仍在、连续第 `2` 期**）⑥ `K2` 系列 `10/31` 停新**当日新用户能否注册**（**官方公告原文已核到，但「如期执行」需登录态实测 —— 两件事不合并**）⑦ `Kimi K3.1 Pro` 权重是否在 `11/4` 前放出 ⑧ `OXR` 免费 API 的**超额扣费**与**单请求上限**实测
"""

os.makedirs(os.path.dirname(P1), exist_ok=True)
# ⚠️ **追加，不是覆盖** —— 该文件是自动化任务的累计记忆（053 期时有 1,969 行），
#    覆盖写会把全部往期记忆抹掉（054 期第一次跑就踩了，已 `git checkout` 恢复）。
old_txt = io.open(P1, encoding="utf-8").read() if os.path.exists(P1) else ""
assert "第 054 期" not in old_txt, "本期内容已写过，不要重复追加"
io.open(P1, "a", encoding="utf-8", newline="\n").write(T1)
print("appended:", P1, "(+ %d 行)" % T1.count("\n"))

# ---------------------------------------------------------------- 2) 当日日志
P2 = MEM + "2026-10-31.md"
T2 = """# 2026-10-31（周六）· 第 054 期

## 出刊概况

- **期号**：第 054 期 · **隔日出刊**（053 期是 10/30 第一轮，本期是 10/31 第一轮）
- **窗口**：053 期截止 10/30 09:30 北京 → 本期截止 10/31 19:00 北京，约 **33.5 小时**
- **美西/北京双向换算**：起 北京 10/30 09:30 ＝ 美西 10/29 18:30 PT；止 北京 10/31 19:00 ＝ 美西 10/31 04:00 PT（**窗口跨越两个美西日**）
- **规模**：全量扫 **417** 个抓取件（另补抓 100 余个专项一手页）、解析出 **4,436** 条带时间戳条目、**窗口内 109 条** —— **逐条归因后只有 5 条产生免费内容条目**
- **发布**：commit → push → Pages `built` → **线上五页逐字节一致**

## 本期头条与硬条目

1. **`OXR`（`SoMark`）`1.3B` 开放权重文档解析模型 + 官方「免费 API」—— 本报告至今第一次读到「免注册、免 `API key`、且官方把免费额度写成具体数字」的免费 API**
   - 一手：`github.com/SoMarkAI/OXR`（`README.md` `200`/`19,333`、`LICENSE` `200`/`2,394`）、`HF` `SoMarkAI/OXR-1.0`（`downloads 3,180`/`likes 132`/`gated false`）、**`docs.somark.ai` 的 `free-tier-rules.md`（`200`/`1,290` —— 本期最硬的一条一手证据）**、`oxr/index.md`（`200`/`4,580`）、`llms.txt`（`200`/`6,561`）
   - 官方逐字（规则表）：`Up to 500 pages of free quota per day` ／ `Up to 2000 pages of free quota per month` ／ `Daily free quota resets at 00:00 each day` ／ `Monthly free quota resets at 00:00 on the 1st of each month`
   - 官方逐字（`Free API` 段）：`OXR provides a free API so you can test parsing on your own documents without registering or requesting an API key.` ／ `The Free OXR API requires no authentication. Set api_key to any value, such as dummy.`
   - ⚠️ 官方同时写了两条限制，逐字照录：`We do not recommend using the Free OXR API in production.`；单文件 `10MB` / 单请求 `20` 页
   - ⚠️ 许可证：`Apache-2.0` 底子 ＋ 三条附加条款（商用 `$2,000,000` 双阈值 / 对外在线服务须署名 / 禁止竞品托管 API）
   - ⚠️ **归期**：`Free API` 段最早见于提交 `0245ee0e`（`2026-10-19T10:11:58Z`）→ 落在 051 期窗口之前，**按「首次登记的往期事件」写入**
2. **`AutoClaw` 万圣节双周档 `M11W1` —— 国际站 `80M`、国内站 `50M`，连起始日都不同**
   - 一手：`autoclaw.z.ai/blog/news/M11W1/`（`200`/`42,467`，`datePublished 2026-10-30T08:17:44Z` ＝ 北京 10/30 16:17）、`autoclaw.zhipuai.cn/blog/news/M11W1/`（`200`/`47,058`，`datePublished 2026-10-30T10:07:34Z` ＝ 北京 10/30 18:07）
   - ⚠️ 上限 `80M` vs `50M`、起始日 `10/31` vs `11/2`、积分当量 `8,000` vs `5,000`；**到期日相同（`11/8`）**
3. **`Moonshot` `K2` 系列 `10/31` 停新 —— 官方定价页逐字终于核到（被追 7 期的挂账项，本期销项）**
   - 官方逐字：`K2 系列模型将于 2026 年 10 月 31 日起停止向新注册用户开放，已注册用户不受影响；我们计划在 12 月底下线所有 K2 系列模型。`
   - ⚠️ **053 期记「四个候选文档页各命中 0 次」，本期在同一份文件上实读 `停止`/`下线`/`2026 年 10 月 31 日` 各命中 `1` 次**
4. **`Anthropic` 订阅档改版** —— `Max 5x`→`Max`、`Max 20x`→`Ultra`；官方逐字 `No 5-hour limit ‡ 10x Pro usage every week* $200 a month in API credits, up from $100 on Max † New`、脚注 `‡ No 5-hour limit for verified accounts.`；**与免费读者相关的只有 `Free` 档 —— 官方对照表两格都写 `Limited`**
5. **`MiniMax` `H3` 的开源替代 `Open-H3-Regenerate-2K`**（`NVIDIA`+`MIT`）—— 一手 `NVlabs/Sana` 的 **`sol-engine` 分支**（**不在 `main` 上**），分支头提交 `781e8341`（`2026-10-30T07:01:24Z` ＝ 北京 10/30 15:01，窗口内）；官方逐字 `An open replacement for the closed H3-Regenerate-2K API`；⚠️ `HF` `downloads 0`、权重许可是 `minimax-h3-community`

## 规模与对账

- 表体 **203** 行 ＝ 053 期 199 ＋ 新增 **6** − 移出 **2**；`4.1` = **56** / `4.2` = **31**；总账 **147** 条；速查页 **71** 条
- 色标 ⚪4/🔴4/🟢142/🟡22/🟠7/⚠5/空19 = 203；classify crit4/live158/over4/pending23/unclear8/switch6 = 203；**A7 + B26 + C2 + D159 + E9 = 203** ✔
- ⚪ 与 over 本期**个数相同（4=4）且成员逐条一致**
- **「距今 N 天」由 `recalc_days054.py` 逐行独立重算**（14 行全部需改写、**无一行继承值与真值相同**）；断言是「天数 == 截止日 − 基准日」
- `lint_table.py --strict` **CLEAN**；`verify_web` **ALL GREEN**；`check_views` **ALL GREEN**；`check_site_freshness` **ALL GREEN**；`check_frozen` **🔴 0**

## 本期纠错 4 条

1. **053 期的「逐条零变化」口径本期被打破** —— `Runware` 的 `heygen-video-1-0-launch-promo` 截止日被官方从 `10/31` 延长到 `11/30`
2. **053 期的正文结论成立、但表体与总账没跟上（两条）** —— `OpenRouter` 目录三个数、`百度` `Unlimited OCR 2` 下载量（**后者是「被 slim 裁掉」而非「写错」**）
3. **053 期记的「`K2` 停新未核到」—— 本期在同一份文件上实读命中**
4. **053 期记的「`百度` 单期涨 `9,784`」被改写** —— 本期 `18,141` → `69,231`、单期涨 `51,090`（涨 `281%`）

## 本期新增避坑（240–243）

240 同一个活动在两个官方站点上可以给两个不同的数、两个不同的起始日、两个不同的积分当量；
241 官方文档站的 `llms.txt` 索引里的 `.md` 原文往往比网页正文更硬，且常常是唯一给出「免费额度具体是多少」的地方；
242 「开放权重 + `Apache-2.0` 底子」不等于「无附加条款」；
243 「grep 零命中」只能证明「这次没搜到」，不能证明「官方没写」。

## 本期实测的工程坑

- **① 状态列里不能出现会被 `classify()` 字面误读的词** —— 本期踩 `1` 次（`国家超算互联网` 行的尾注写了「不写「已结束」」→ 整行被误判成 `over`）；**处置仍是「改措辞、不放宽守卫」**
- **② markdown 表格单元格里不能出现竖线** —— 官方对照表/规则表的逐字引用必须把 `|` 转写成 `／`；**`gen_table054.py` 的字段数分布断言 `Counter({3: 205})` 是这条纪律的守门断言**
- **③ 「表体层比正文层慢一拍」有第三种形态：不是数字写错、是数字被 `slim` 裁掉**
- **④ `check_frozen` 的 🔴 高危本期触发 1 条，是措辞触发** —— 台账关键词 `REA` 会在 `README.md` 里被字面命中，而那行尾注以「不写成「本期新增」」结尾
- **⑤ 台账计数改动必须按「行首标题」定位** —— 文件开头的「历史沿革」长段落里也含同名的分类名，全局 `replace` 会改错地方

## 下一期强制动作（31 条）

最紧的八条：① `豆包工作 30 天订阅`（A 档已过 `14` 天、连续第 `8` 期零命中）② `国家超算互联网` 官方页的「夜间免费」栏（连续第 `2` 期）③ `Mistral` 官方公告页原文（连续第 `14` 次 `000`）④ `Mistral` demo 免费预算的额度数字与日历日 ⑤ `AutoClaw` 国际站 `M10W4` 残留文案官方是否会改（**本期实访仍在、连续第 `2` 期**）⑥ `K2` 系列 `10/31` 停新**当日新用户能否注册** ⑦ `Kimi K3.1 Pro` 权重是否在 `11/4` 前放出 ⑧ `OXR` 免费 API 的**超额扣费**与**单请求上限**实测
"""
io.open(P2, "w", encoding="utf-8", newline="\n").write(T2)
print("written:", P2)
