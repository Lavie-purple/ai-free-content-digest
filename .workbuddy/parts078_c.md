## 七、按任务选型速查（延续 077 期 · 本期更新 `10` 处）

| 你要做的事 | 现在最省钱的入口 | 本期变动 | 边界 |
| --- | --- | --- | --- |
| **白拿一笔能马上用的额度** | `AutoClaw` `M11W4`（**第 `2` 天**） | 页 `47,974` 与上期同字节；**`11/29 23:59` 收口，剩 `5` 天** | **锁在客户端内、导不出 `API`**；`M11W5` 连续第 `3` 期 `404`，别提前等 |
| **下载一个国产旗舰的权重** | **`ERNIE 5.5 Flash Preview`**（`Apache-2.0` · `280B` / `14B` 激活 · `1M`） | **`11/23 17:00` 上线 `3` 仓**（`39 → 42` 仓），比承诺早 `2` 天 | `128` 个分片，**`BF16` 约 `560GB` / `FP8` 约 `280GB`** —— 能下载≠能本地跑 |
| 用 `ERNIE 5.5` 的免费 API | `OpenRouter` `baidu/ernie-5.5-flash-preview:free` | `created` `11/10`、`1,024,000` ctx、`$0 / $0`，本期未动 | **`:free` 是 API 免费，不是权重开放** —— 两件事本月已解耦 |
| 在笔记本上跑一个能用的开源模型 | **`Inkling 2 Mini`**（`26.4B` / `3.4B` 激活 / `Apache-2.0`） | **`downloads` 本期 `0` 变化（整列冻结）**，`likes` `+296` | `~20GB` 是 `NVFP4` 权重内存；**`downloads` 别当趋势看**（避坑 334） |
| 调这个模型的 API（不想自己跑） | `OpenRouter` → `PrimeIntellect` **最低档 `$0.0375` / `$0.15`** | **顶档涨到 `$0.15 / $0.60`（`+25%`）**；**`Io Net` `$0.12 / $0.50` 反而变便宜了** | 最贵/最便宜由 `3.2` 倍拉到 **`4.0` 倍**；**默认走哪档查不到**，要主动选 |
| 拿免费 API key 试模型 | `OpenRouter` `:free` **`12` 条** | **三项（`:free`/零价/`max_price=0`）全未动**；全量 `−3` 全是付费 | **带冒号的 `id` 用 `%3A` 请求**，裸写会假 `404`（避坑 333） |
| 写代码 / 多步任务（云端免费） | `OpenCode` `Free models`（**`11` 条**） | **整页与上期逐字节相同**（`108,492` / `md5` 同） | 免费的是 `Jev 1.13`，不是 `1.14`；`Tidepool Alpha Free` 第 `3` 期在列、未转正 |
| 图像生成（`4K`，要便宜） | **`MiniMax H3-Image` `4K`** | **第二版第 `5` 天**；字节 `310,183` 三连同，`md5` 变 | 要过 `1660` 万像素门槛；**文案里仍无截止日** |
| 图像生成（走分发层） | `Runware` | **`11-23` 两条过期一天后仍在页面**（第三次实证） | **数组是台账、不是货架**：过期项不会自动删 |
| 中文旗舰 + 写代码（付费） | **`GLM-5.4` × `GLM Coding Plan`** | 官方逐字：**Coding Plan 全量开放、API 待安全评估**；`z.ai` 首页 `5.4` 仍 `0` | **订阅制、无免费档**（页内 `免费` `0` 命中）；`OpenRouter` `0` 条 |
| 浏览器内建 Agent（$0） | `Google Antigravity` 免费档（`$0/month`） | **`11/30` 剩 `6` 天**，但**首页 `November 30` 已 `0` 处**、`pricing` 页 `000` | **本期无法核实**三个第三方模型是否真被移除；免费档 `4` 模型不变 |
| 长文档 / 中文 | `Kimi K3.1 Pro`（`1M`、权重已开） | `likes` `+14`；**`OpenRouter` 的 `kimi-k2` / `kimi-k2-thinking` 已退目录** | `K2` 系列**`12` 月底全部下线**；还挂 `kimi-k2.x` 的工作流要迁 |
| 跑开源旗舰（大机器） | `Hy4`（`770B` / 激活 `49B` / `1M`） | **`downloads` 全零**（十三个仓同批冻结） | **`BF16` 约 `1.5TB`、`FP8` 约 `770GB`**；**不是「能本地跑」的量级** |
| 盘点「还有哪些羊毛」 | `AIHOT` Token 羊毛 | **`¥845`（`+¥24`）、卡册 `65` 张（`+4`）**，口径未再改 | 本期两数**可比**（上期是改版期）；合计无法按厂商拆 |

**本期更新 `10` 处**：① `AutoClaw` 改「第 `2` 天、剩 `5` 天」；② **新增「下载国产旗舰权重」一行（`ERNIE 5.5`）**；③ **新增「用 `ERNIE` 的免费 API」一行，把「权重」与「API」拆成两行**；④ `Inkling` 本地跑行改成「`downloads` 冻结」；⑤ 「调 API」行改成**顶档涨价 + `Io Net` 变便宜**；⑥ `OpenRouter` 行改成「全量 `−3` 全是付费」；⑦ `OpenCode` 行改成「逐字节同」；⑧ `MiniMax` 改「第 `5` 天」；⑨ `Runware` 改「过期一天仍在」；⑩ `GLM-5.4` / `Antigravity` / 「盘点羊毛」三行按本期口径重写。

---

## 八、本期信源体系更新

**一、你随任务给的 `T0`–`T4` 清单：与 077 期收到的版本比对，无新增项、无缺项。**

- 五个分层的自称条数与上期一致（`T0` 根节点（`97`）、`T1` 社区 `19`、`T2` Newsletter `18`、`T3` 媒体 `36`、`T4` 聚合器 `12`），**本期未逐条重数**。
- `https://aihot.news/` 本期首页 `200` / **`248,874`** 字节、`/free-tokens` `200` / **`529,918`** 字节（**上期 `499,261`，`+30,657`**）。
- 清单里的评测站（`LMArena` 三榜、`Artificial Analysis`、`llm-stats`、`LiveBench`、`SWE-bench`、`Terminal-bench`、`OSWorld`、`Epoch AI`、`Vals AI`、`Scale SEAL`、`OpenCompass`、`SuperCLUE`、`FlagEval`、`C-Eval`）**台账均已覆盖**；`lmarena.ai` 仍 `000`（**第 `11` 期**），**本期不引用任何第三方转述的名次**。

**二、本期新纳入固定抓取位的端点（`2` 个，本期首次跑）：**

| 端点 | 用途 | 本期结果 |
| --- | --- | --- |
| `hf-mirror.com/api/models?author=<org>&limit=200` | **「权重放没放」的唯一硬判据**（仓库数 + `createdAt`） | `baidu` **`39 → 42`**，三个新仓 `createdAt` 精确到秒 |
| `docs.bigmodel.cn/cn/guide/start/model-overview` | 官方对「API 何时开」的口径 | **`200` / `237,517`**，逐字「`API` 将在完成安全评估后开放」 |

**三、两条方法上的补充，本期新立：**

- **「列表页顶部的日期」是当天日期，不是文章日期。** `anthropic.com/news` 顶部 `Latest news / November 24, 2026`，紧接着第一条是 `Nov 9, 2026`。**与上期逐行 diff，唯一变化就是那行日期。** 所以「新闻页日期 = 今天」这个读法会凭空造出一条「今日发布」。**下期起，任何新闻列表页都只认条目旁的日期。**
- **「承诺有没有兑现」要看计数端点，不看发布页。** `ERNIE` 发布页连续 `7` 期逐字节相同（`54,010`），权重却在其中一期上线了。**发布页只用来读承诺文本，兑现与否只看 `?author=<org>` 的仓库数。**

**四、本期仍然拿不到的（不进「已覆盖」）**：`lmarena.ai`（第 `11` 期）、`artificialanalysis.ai`（第 `2` 期）、`chatgpt.com/pricing`（第 `7` 期，`301` 后 `0` 字节）、`antigravity.google/pricing`（**第 `1` 期超时，`30` 秒 `000`**）、`blog.google` / `ai.meta.com` / `mistral.ai` / `x.ai` 四家 `000`、`hunyuan.tencent.com` `JS` 骨架屏（`6,584` 字节，第 `10` 期）、`open.bigmodel.cn/pricing`（`JS` 壳）、`cursor.com/pricing` / `windsurf.com/pricing` / `perplexity.ai/pro` 三家定价页、`news.ycombinator.com` / `reddit.com/r/LocalLLaMA`（连续第 `2` 期 `000`）。

---

## 九、来源与核查说明

**一、本期实际取料（`97` 个专项端点 + `8` 次定向补抓；`200` `77` / `79.4%`）。** 逐条列关键端点与读数，未列出的按日志留档：

| 端点 | 码 | 字节 | 用途 |
| --- | --- | --- | --- |
| `hf-mirror.com/api/models?author=baidu&limit=200` | `200` | **`19,257`** | **`42` 仓**（`39 → 42`）；三个 `11/23 09:00Z` 新仓 |
| `…/api/models/baidu/ERNIE-5.5-Flash-Preview` | `200` | **`8,722`** | `Apache-2.0` / `299.6B` 张量 / `142` 文件 / `128` 分片 |
| `…/baidu/ERNIE-5.5-Flash-Preview/raw/main/LICENSE` | `200` | **`11,418`** | 逐字 `Apache License Version 2.0` |
| `…/baidu/ERNIE-5.5-Flash-Preview/raw/main/README.md` | `200` | — | `280B total / 14B active`、`1M-token context` |
| `openrouter.ai/api/v1/models` | `200` | **`919,922`** | **`474`** / `:free` `12` / 零价 `15`；差集 **出 `3` 进 `0`** |
| `…/models?max_price=0` | `200` | `22,317` | `14` 条（未动） |
| `…/models/dots-studio/dots-3-note-preview%3Afree/endpoints` | `200` | **`1,434`** | **`1` 条 `AtlasCloud` 路由、`$0/$0`、`512K`** |
| `…/models/dots-studio/dots-3-note-preview:free`（裸冒号） | **`404`** | `44` | **编码问题的现场证据** |
| `…/models/thinkingmachines/inkling-2-mini/endpoints` | `200` | **`5,086`** | `4` 条价点，**顶档涨到 `$0.15/$0.60`** |
| `…/models/inclusionai/ling-3.2-flash:free/endpoints` | `200` | `1,466` | **`1` 条** |
| `opencode.ai/docs/zen` | `200` | **`108,492`** | **与上期逐字节相同**（`md5` `7d206215` 双同），免费段 `11` |
| `claude.com/pricing` | `200` | **`1,448,601`** | 四档价格逐字未变；`Fable` 进 `Pro` 的「按量另付」 |
| `anthropic.com/news` | `200` | **`344,228`** | 顶部 `November 24` 是当天日期；条目 `Nov 9` |
| `docs.bigmodel.cn/cn/guide/start/model-overview` | `200` | **`237,517`** | 逐字「`API` 将在完成安全评估后开放」 |
| `docs.bigmodel.cn/cn/coding-plan/overview` | `200` | **`153,759`** | `GLM-5.4` `14` 处、`免费` `0` 处 |
| `openrouter.ai/api/v1/models?q=glm-5.4` | `200` | `49` | **`0` 条**（未落地） |
| `antigravity.google/` | `200` | **`217,127`** | `November 30` **`0` 处**；横幅换成 `Gemini 4 Neon`（`11/18` 文） |
| `antigravity.google/pricing` | **`000`** | `0` | **`30` 秒超时**，本期读不到 |
| `platform.minimaxi.com/document/price` | `200` | **`310,183`** | 第二版第 `5` 天；字节三连同 |
| `runware.ai/pricing` | `200` | **`786,595`** | `endsAt` `22` 条；`11-23` **仍 `2`** |
| `runway.com/pricing` | `200` | **`1,020,485`** | `25% off` `10` 处、`November 30` `5` 处、`Sign by 12/31` 在 |
| `aihot.news/free-tokens` | `200` | **`529,918`** | **`¥845` / 卡册 `65`**；规则文字未变 |
| `freellm.net` | `200` | `169,555` | **可见文本 `0` 行 diff**，`512+` 不变 |
| `autoclaw.zhipuai.cn/blog/news/M11W4` | `200` | `47,974` | `11/23–11/29`，与上期同字节 |
| `…/M11W5` | `404` | `18,994` | 连续第 `3` 期未挂 |
| `ernie.baidu.com/…/ernie-5-5-flash-preview` | `200` | `54,010` | 「`11月25日前开源`」逐字仍在（第 `7` 期同字节） |

**二、本期用到的对照口径（写清楚，便于复算）：**

- **`OpenRouter` 四项**：全量 = `data` 数组长度；`:free` = `id` 以 `:free` 结尾；零价 = `pricing.prompt` 与 `pricing.completion` 都为 `0`；`max_price=0` = 该查询返回的 `data` 长度。**带冒号的 `id` 一律 `%3A` 请求。**
- **`OpenCode` 免费条数**：沿用 073–077 期口径（页内 `-free` 结尾 `id` 的**出现次数**）。**本期该页 `md5` `7d206215` 与上期双同**，故条数必然与上期相同（**`11`**）；表内去重后实为 **`10` 行**（`jev-1.13-free` 计数含一次重复），**两种数法都写出来，避免下期对不上**。
- **`AIHOT` 卡册数**：页内 `◆` 标记数（与 076/077 同口径）；「今天还能领」取页头大字。
- **`HF` `downloads` / `likes`**：单仓 API 原值；**本期改口径 —— `downloads` 只做跨批次比对、不逐期**（避坑 334）。合计 `198,940` 仅用于说明「整列冻结」。
- **页面「变没变」**：一律先剔 `script`/`style`、按行切、`difflib` 逐行；**字节与 `md5` 只作附注**（避坑 335）。

**三、未核实 / 明确不写的：**

- **`Antigravity` 三个第三方模型 `11/30` 是否真被移除**：本期首页 `November 30` `0` 处、`pricing` 页 `000` → **只写「本期无法核实」，不写「活动取消」也不写「确认移除」**。
- **`ERNIE` 三仓为何在 077 期的 `19:09` 抓取里没出现**：两种可能（抓取早于 `17:00` / API 缓存），**本报不选**。
- **`PrimeIntellect` 顶档为何涨 `25%`**：无公告 → **只记价差，不猜原因**。
- **`AIHOT` 的 `+¥24` 涨在哪个厂商**：页面不提供逐卡人民币拆分 → **只写合计，不点名**（这条此前每期都被追问，本期明确写进「不写」清单）。
- **`GLM-5.4` 的架构与基准**（`Loop Transformer`、`28` 层循环等）：**只见聚合层转述** → **不进结论**。
- **`Tinker` 侧的免费额度**：登录后才可见 → **不写「可以白嫖」，也不写「没有」**（已挂 `4` 期）。
- **`LMArena` / `Artificial Analysis` 的任何名次**：第 `11` / `2` 期 `000` → **不引用第三方转述**。
- **`Runway` 企业版条款**：`runway.com/terms` 本期未重取（077 期 `404`）→ **维持「条款读不到」**。
