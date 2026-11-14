# AI 免费内容与权益速递 · 第 068 期

**2026-11-14（周六）· 本期是「模型先进免费列表、再谈能不能用」的一期** —— `inclusionAI` 的 **`Ling 3.2 Flash`** 在本期窗口内进了 `OpenRouter` 免费区：`:free` 后缀、零价、`1,048,576` 上下文、文本 + 图片双模态、单次最多 `200` 张图 —— **看上去是这一天最值得写的一条**。但本报按三层逐个查过去，得到的是一条反过来的结论：**它在列表里（第一层过了）、`/models/<slug>/endpoints` 返回空数组（第二层没过）、它自己在 `hugging_face_id` 里写的 `inclusionAI/Ling-3.2-flash` 在 `HF` 上是 `404`（第三层没过）**。**「免费区 `+1`」是列表计数，「能用」是另外两件事。** 同一天真正能拿走的开源权重来自另一条线：Runway 把 **`Praxis-1`**（`27B` 混合专家扩散 Transformer、`Apache-2.0`、权重 + 推理 + 微调代码）放了出来，`NVIDIA RoboLab-120` 上 `46.2%` 领先同类 —— **但这条本报 066、067 两期都漏了，本期按「补登」收录，并把三个时间点分开写。**

**主题：AI 免费内容发布 · 免费内容（生成/分发）· 免费额度**

> 扫描截止 **2026-11-14 18:00（GMT+8）**，**窗口 = 上一期（067）扫描截止 11/13 18:00 → 本期截止**，整 **24.0 小时**。
> ⚠️ **本期的性质：隔日出刊、窗口 `24.0` 小时**（067 期 `29.1` 小时、066 期 `22.9` 小时）。**窗口起点 ＝ 上期截止点，各期内容各自独立成立、不合并、不互相覆盖。**
> ⚠️ **窗口换算**：**起于北京 `11/13 18:00` ＝ 美西 `11/13 02:00 PT`；止于北京 `11/14 18:00` ＝ 美西 `11/14 02:00 PT`**（冬令时 `PST`，`UTC−8`，北京快 `16` 小时）。**整段窗口覆盖美西 `11/13`（周五）一个完整工作日，加周六凌晨两小时** —— 周五是本周最后一个工作日，`OpenAI` 在美西当晚发了 `ChatGPT Wallet`、`Runway` 的 `Praxis-1` 报道在周六上午铺开；**同期最大的新闻（英伟达换帅）不在本报范围内，本期只在「不进清单」一节里提一句为什么不计入。**
> ⚠️ **本期的实抓规模**：**主清单 `285` 行 / 唯一文件名 `285` 个 / 实际落盘 `285` 个**（另专项核验 `56` 件）；`200` 共 **`198`**（`69.5%`）、`000` 共 **`53`**（`18.6%`），另 `403` `12` / `404` `8` / `412` `2` / `429` `2` / `503` `1` / `400` `1` / `422` `1` / `401` `1` / `521` `1` / `405` `1` / `502` `1` / `302` `1` / `301` / `451` 各 `1`；**解析出 `3,177` 条带时间戳条目、落在窗口内 `85` 条**（`hnrss 20`、`infoq 11`、`decoder 10`、`lesswrong 10`、`techcrunch 8`、`aws_ml 7`、`verge 5`、`leiphone 3`、`wired 3`、`simon 2`）。
> ⚠️ **本期新增一个信源**：**`aihot.news`（168 信源分级的聚合器 + 「Token 羊毛」免费额度台账）本期正式并入 T4 聚合器层**（用户本轮提供）。它的「Token 羊毛」页本报已连记 `6` 期，本期起同时作为「多站点交叉核对」的一个观察点，**但它只作交叉，不作一手**。
> 与 001–067 期的关系：**只做增量与纠错，不重复已固化内容**。**本期纠错 3 条（第五章）**、**新增避坑 3 条：294–296**。


---

## 摘要（3 秒版）

- **本期头条（免费区 `+1`，但三层的门只开了一层）**：`inclusionAI` **`Ling 3.2 Flash`** 进了 `OpenRouter` 免费区 —— `:free`、`0` 价、`1,048,576` 上下文、文本 + 图片、`max_completion_tokens 262,144`、单次最多 `200` 张图、混合推理（`reasoning.mandatory: false`、`default_enabled: true`）。**`created` 时间戳 `1794591958` ＝ `11/13 17:45 UTC` ＝ 北京 `11/14 01:45`，落在本期窗口内。** 但：**① `/models/inclusionai/ling-3.2-flash-20261113/endpoints` 返回 `"endpoints":[]`**（空数组）；**② 它自己声明的 `hugging_face_id` 是 `inclusionAI/Ling-3.2-flash`，`hf-mirror` 单仓端点 `404`**；**③ 全量 `471` 条里只有这一条 `ling-3.2`，没有对应的付费档**。**「登记了」与「开门了」之间，本期差着两层。**
- **本期头条之二（真正能拿走的那条，是本报漏了两期的）**：Runway **`Praxis-1`** 开放权重 + 源码，**`Apache-2.0`，明写允许商用**。`27B` 混合专家扩散 Transformer，预测视频与动作；`NVIDIA RoboLab-120` `46.2%`（`FLUX 3 Action` `42.9%`、`Cosmos3 Nano` `36.8%`、`π0.5` `28.0%`，`1,200` 回合）；微调到从未见过的 `RT-1` 机体后在 `SimplerEnv` 上 `80.0%`（原版 `RT-1` `52.4%`）。**⚠️ 三个时间点没有一个落在本期窗口内**：官方页 `datePublished 2026-11-11T15:00:00Z`、`HF` 集合 `lastUpdated 11/12 20:22 UTC`、`GitHub pushed_at 11/12 22:14 UTC` —— **本期按「补登」写，不写「今天发布」。**
- **本期第三条（第 `3` 期卡住的那个站点通了）**：`antigravity.google` 首页本期 `200` / **`214,361`** 字节、`/pricing` `200` / **`140,014`** 字节（前两期全组 `000`）。定价页逐字：**「Generally Available / For Individuals / `$0/month` / Experience Antigravity without a subscription plan」**，含「Access to a variety of agent models / Unlimited Tab completions / Unlimited Command requests / **Basic weekly rate limits**」。**⚠️ 全页 `free` `0` 命中**，「免费」这件事只用 `$0/month` 表达；顶部横幅写「**Gemini 4 Hydrogen and Orchestrator now in Google Antigravity**」——**产品里有，但页面不写它在哪一档**。
- **本期第四条（不进的比进的更值得记）**：`ChatGPT Wallet`（`11/13`，`377,842` 字节）逐字「initially available through **dots** for **ChatGPT Pro subscribers in the US**」，**整页 `free` `0` 命中**、`Plus` `0` 命中 —— **付费档 + 单一国家，免费用户拿不到**；`Claude Meetings` 在 `claude.com/pricing`（`1,344,079` 字节）里**连续第 `4` 期 `0` 命中**；Runway 的 `Kling 4.0 25% off` 是**折扣**不是免费，且 `11/30` 到期。
- **本期第五条（`Token 羊毛` 第 `6` 期：页头第一次破千）**：页头「今天还能领」**`¥598 → ¥1599`（`+1001`）**、卡册 **`57 → 59` 张**、核实日戳 **`11/14` `108` 条 / `11/13` `2` 条 / `11/9` `4` / `11/8` `4` ＝ `118`**。**`¥1001` 这个数字与卡册里那条 `¥1001`（`Zed`）同值，但本报不据此断言因果**（只有两个观测点，065 期已立此界）。

---

## 一、AI 免费内容发布（分发入口线）

### 1. ⚡ `Ling 3.2 Flash` 进 `OpenRouter` 免费区：**列表开了、端点空着、权重 `404` —— 三层门只开了一层**

**一手**：`openrouter.ai/api/v1/models`（`200` / **`851,712`** 字节，067 期同端点 `851,7xx`）与单模型端点 `/api/v1/models/inclusionai/ling-3.2-flash-20261113/endpoints`（`200` / **`462`** 字节）。逐字四段：

> 「**Ling 3.2 Flash is a hybrid reasoning model from inclusionAI that accepts text and image input, with a 1M-token context window and up to 200 images per request.**」
> `"id": "inclusionai/ling-3.2-flash:free"`、`"canonical_slug": "inclusionai/ling-3.2-flash-20261113"`、`"created": 1794591958`
> `"hugging_face_id": "inclusionAI/Ling-3.2-flash"`、`"modality": "text+image->text"`、`"context_length": 1048576`
> `"endpoints": []`

**⚠️ 第一层过了：列表里有它、价是 `0`、两个价格字段都是 `0`。** 本期全量 **`472 → 471`（`−1`）**、`:free` **`14 → 14`**、零价 **`17 → 17`**、`?max_price=0` **`16 → 16`** —— **免费区「进 `1` 出 `1`」，总数反而少 `1`**。进的是 `inclusionai/ling-3.2-flash:free`；出的是 `liquid/lfm-2.5-2.6b` 与它的 `:free` 两条（同一家族的 `lfm-3-1.7b` / `:free` 还在）。**「免费区 `+1`」与「总模型数 `−1`」同时成立**，两个数不能互相替代。

**⚠️ 第二层没过：端点是空数组。** 单模型端点返回的 `endpoints` 是 `[]` —— **不是 `404`、不是 `403`、是 `200` 加一个空数组**。**这条与 067 期的 `particle-1:free`、`Inkling-2-Small` 都不同**：那两个是「有端点、能调」，本期这个是「有 `ID`、没端点」。**本报不写「可以免费用 `Ling 3.2 Flash`」**，只能写「它出现在免费列表里」。

**⚠️ 第三层没过：它自己指的权重仓在 `HF` 上是 `404`。** `hugging_face_id` 逐字 `inclusionAI/Ling-3.2-flash`，而 `hf-mirror.com/api/models/inclusionAI/Ling-3.2-flash` 返回 **`404` / `32` 字节**；同厂在 `?author=inclusionAI` 下能列出 **`100` 个仓库**（`42,754` 字节），**里面没有 `Ling-3.2` 系列的任何一条**（有 `Ling-3.0-flash` / `Ling-3.1-flash` / `Ling-3.1-flash-1019`）。**「模型卡上写了 `hugging_face_id`」与「那个仓库存在」是两件事** —— `OpenRouter` 的字段是**预留位**，不是承诺。

**⚠️ 第四条边界：没有付费档，所以不是「换档」，也不是「并排多开」。** 全量 `471` 条里 `ling-3.2` 只有 `:free` 这一条（`ling-3.1-flash` 是另一代、带价 `0.000000045` / `0.000000135`）。067 期立的两种形态（289：换档 / 并排多开）都不适用 —— **这是第三种形态：只登免费档、付费档还没建**。**免费档先于付费档出现，本报第一次见**；它意味着「免费」在这里是**冷启动期的占位**，不是长期权益。

**⚠️ 本报不做的推断**：不推断 `Ling 3.2` 何时开端点、不推断权重是否会在 `11/25` 前和 `ERNIE` 一起放出来（那是两家的两件事，`?author=baidu` 本期仍 `39` 个仓库、`ERNIE 5.5 Flash Preview` 权重仍未上）、不推断它与 `Ling 3.1 Flash` 的能力差。

---

### 2. ⚡ Runway `Praxis-1` 开放权重：**`Apache-2.0`、`27B` 混合专家、`RoboLab-120` 第一 —— 但这是本报漏了两期的一条**

**一手**：`runway.com/news/company-news/praxis-1-is-now-available`（`200` / **`653,601`** 字节）、`runway.com/research/praxis-1-video-pretraining-to-robot-control`（`200` / **`1,101,471`** 字节，gzip 传输后解压）、`api.github.com/repos/runwayml/praxis-1-oss`、`hf-mirror.com/api/collections/runwayml/praxis-1`（`10,186` 字节）。官方逐字四段：

> 「Praxis-1, our state-of-the-art world action model, is now available to everyone with **open weights under the Apache 2.0 license**.」
> 「Praxis-1 is a **27B-parameter mixture-of-experts diffusion transformer** that predicts video and actions together.」
> 「On RoboLab-120, Praxis-1 reaches **46.2%** success across 1,200 episodes, compared with **42.9%** for FLUX 3 Action, **36.8%** for Cosmos3 Nano and **28.0%** for π0.5.」
> 「**Everything you need to run and adapt it on your own hardware is released under Apache 2.0, including for commercial use.**」

**⚠️ 时间点必须三个分开写，且三个都不在本期窗口内**：

| 观测点 | 实读 | 折北京时间 | 落在哪一期窗口 |
| --- | --- | --- | --- |
| 官方页 `datePublished` | **`2026-11-11T15:00:00Z`** | `11/11 23:00` | **066 期窗口内**（`11/11 14:00 → 11/12 12:55`） |
| `HF` 集合 `lastUpdated` | **`2026-11-12T20:22:56Z`** | `11/13 04:22` | **067 期窗口内**（`11/12 12:55 → 11/13 18:00`） |
| `GitHub` `pushed_at` | **`2026-11-12T22:14:40Z`** | `11/13 06:14` | **067 期窗口内** |
| 媒体首报（`The Decoder`） | `2026-11-14T09:45:45Z` | `11/14 17:45` | **本期窗口内**（仅媒体稿） |

**⚠️ 所以本期按「补登」收录，不写「今天发布」。** 本报 066、067 两期都漏了它 —— 漏因写在第五章纠错②：**主抓清单里只有 `runwayml.com/news` 首页，而那是 `757,046` 字节的 `JS` 壳（正文文本只有导航）**，`Praxis-1` 的正文在 `company-news` 二级页里。**「首页抓到了」不等于「这个站的新发布抓到了」** —— 本期起 `runway.com/news/company-news` 单列一条。

**⚠️ 「开源」四层，逐层实读**：

| 层 | 实读 | 依据 |
| --- | --- | --- |
| **能下载** | `HF` 集合 `11` 个条目：`praxis-1-base` / `-droid` / `-yam` / `-so101` 四组，各带 `-lerobot` 与 `-nvfp4` 变体，另 `praxis-1-eval` 数据集 | `hf-mirror.com/api/collections/runwayml/praxis-1` |
| **能跑** | 标准版需 **`80 GB` 显存**；压缩版按官方估算可放进 **`RTX 5090`（`32 GB`）**，但 `GitHub` 文档注明**峰值显存未实测**；官方称支持 `H100` / `B200` / `RTX PRO 6000` / `Jetson Thor` | 官方博客 + `GitHub` `README`（`80,830` 字节） |
| **能商用** | **`Apache-2.0`**（`GitHub` `license.spdx_id` 逐字），官方明写「including for commercial use」；权重、推理代码、微调代码（全量 + `LoRA`）同一许可 | `api.github.com` + 官方博客 |
| **哪里都能用** | **未发现地域排除** —— 与 067 期 `MiniMax-H3-Image` 的 `LICENSE` 第 `I.5` 条（排除欧盟 / 英国 / 韩国 / 美国）形成对照 | 见下条说明 |

**⚠️ 第四层这次是「干净」的，但要写清「怎么知道的」。** 067 期的纪律是「`license: other` 一律读 `LICENSE` 原文」。本期 `Praxis-1` 的许可是 `Apache-2.0` **标准短标识**（`GitHub` 直接给出 `spdx_id`，不返回 `other`）—— **标准许可证没有「排除地域」这一段可写**，所以本报的结论是「按其声明的 `Apache-2.0` 无地域限制」，**而不是「本报逐字读完了它的附加条款」**（它没有附加条款）。**「没有读到排除」与「读完了确认没有排除」在标准许可证上是同一件事，在 `other` 上不是。**

**⚠️ 一个必须同时写的反向信号**：`GitHub` `stargazers_count` **`103`**、仓库 `created_at` **`10/26`**（不是今天建的）、`pushed_at 11/12`。**「权重公开」与「社区已经用起来」之间还有距离**（与 067 期 `Inkling-2-Small` 的 `downloads 12` / `likes 166` 同型）。**评测也是官方自测**：官方逐字「We ran all the tests ourselves」，媒体报道里也写了「results haven't been independently verified yet」。

---

### 3. ⚠️ `Antigravity` 第 `3` 期通了：**`$0/month` 免费档还在，「`Basic weekly rate limits`」首次给出「有上限」这个形容词**

**一手**：`antigravity.google/`（`200` / **`214,361`** 字节）、`antigravity.google/pricing`（`200` / **`140,014`** 字节）；`/models` 本期 `404`。066、067 两期这一组全是 `000`，本期**首页与定价页都能打开**。

**⚠️ 逐字四段**：

> 「Generally Available / **For Individuals** / **`$0/month`** / **Experience Antigravity without a subscription plan**」
> 「Plan includes: Access to a **variety of agent models** · Unlimited Tab completions · Unlimited Command requests · **Basic weekly rate limits**」
> 「**New — Gemini 4 Hydrogen and Orchestrator now in Google Antigravity**」（页面顶部横幅，链到发布帖）
> 「For subscription options … Standard/Plus plans starting at **$30 USD per seat per month** … Pay-as-you-go plan with **$0 seat fee**」

**⚠️ 第一件：免费档确实还在，但整页不写「免费」这个词。** `free` / `Free` 在 `214,361` 字节里**各 `0` 命中**；`$0` 共 `2` 处 —— 一处是 `$0/month`（个人档），另一处是 `$0 seat fee`（企业按量付费的席位费）。**「免费」在这张页面上是一个价格符号，不是一个词** —— 只搜 `free` 会得出「没有免费档」的错误结论。

**⚠️ 第二件：额度第一次有了「有」的表述，但仍然没有数字。** `Basic weekly rate limits`（带脚注星号）是本报第一次在这张页面上读到**关于额度上限的形容词**；`quota` / `requests per day` 一类词**各 `0` 命中**，脚注正文也没有给出周限额的具体数值。**「有上限」与「上限是多少」是两件事**（与 067 期 `Gemini 4 Hydrogen` 的「能用到、点不到」同源）。

**⚠️ 第三件：`Hydrogen` 进了这个产品，但页面不写它在哪一档。** 横幅只说「now in Google Antigravity」；付费档的卖点是「higher access to our latest Gemini models」「More rate limits」。**所以本报本期把 067 期那句话改写了**：067 期写「`Antigravity` 里它只给付费 `AI Pro` / `Ultra`」（依据是 `blog.google` 的发布帖），本期 `Antigravity` 自己的页面说它**已经进了产品**，两句话并不冲突 —— **「发布当天只给付费档」与「后来进了产品、档位未写」可以同时为真**。**本报不写「免费档现在能用 Hydrogen」**，因为没有一手依据。

---

### 4. ⚠️ 三条「当天有发布、但不进免费清单」的边界案例

| 发布 | 一手实读 | 为什么不进免费清单 |
| --- | --- | --- |
| **`ChatGPT Wallet`**（`11/13`，`openai.com/index/introducing-chatgpt-wallet/`，**`377,842`** 字节） | 逐字「ChatGPT Wallet will initially be available through **dots** for **ChatGPT Pro subscribers in the US**」；整页 `free` `0`、`Free` `0`、`Plus` `0`；`Pro` `40` 命中 | **付费档 + 单一国家**。`Pro` 是订阅档，不是免费档；连 `Plus` 都不在里面。**「上线」与「免费用户能用」之间隔着两档** |
| **`Claude Meetings`**（`11/12` 起 beta） | `claude.com/pricing` **`1,344,079`** 字节（067 期 `1,344,061`，`+18`），`Meetings` **`0` 命中**；可见文本与上期**逐行 `0` 差异** | **连续第 `4` 期「上线 ≠ 进定价表」**。`+18` 字节全部来自构建指纹（见第三章第 `5` 条），**没有一个字讲 `Meetings`** |
| **Runway `Kling 4.0 25% off`** | `runway.com/pricing`（**`952,380`** 字节）逐字「**25% off Kling 4.0 generations until November 30**」，在 `Standard` 与 `Pro` 两个付费档下面 | **折扣 ≠ 免费**，且只对第三方模型 `Kling 4.0` 生效；免费档（`125` 一次性 credits）下面**没有**这一条 |

**⚠️ 再记一条不算进来的**：本期窗口内全球最大的新闻是**英伟达换帅**（`Jensen Huang` 离任，`hnrss` / `techcrunch` / `verge` / `wired` 共 `10` 余条）。**它不是「AI 免费内容发布」，本报不收录**；它对本报告的唯一影响是**周五美西的厂商发布节奏被打断**（`OpenAI` 当天只发了 `Wallet` 一篇产品稿，`Anthropic` 全站无新发布）。**「今天没什么可写」有时是因为别的大事占满了版面** —— 这一句写在这里，是为了让读者知道本报的「窗口内 `85` 条」里有多少是与本报无关的。
