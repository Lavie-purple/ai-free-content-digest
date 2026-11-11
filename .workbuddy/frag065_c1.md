## 一、AI 免费内容发布（分发入口线）

### 1. ⚡ `Claude` 扩成工作台：**定价页当天新增的两行，`Free` 列全是 `No`**

**一手**：`claude.com/pricing`（`200` / **`1,344,061`** 字节，064 期 `1,325,494`，**`+18,567`**）。**媒体一手（窗口内两条）**：`The Decoder` `11/11 03:48`「Anthropic turns Claude into a full workspace with Plugins, spreadsheets, whiteboards, and soon Meeting notes」；`TechCrunch` `11/11 01:30`「Anthropic launches Claude Meetings to turn workplace discussions into plans and tasks」。

**⚠️ 「新增了什么」媒体写了，但「谁能用」只有定价页写了。** 把两期的对比表逐行对齐，本期多出来的就是这两行：

| 能力（定价页对比表原文行） | `Free` | `Pro` | `Max` | `Ultra` |
| --- | --- | --- | --- | --- |
| `Claude Design` | `Yes` | `Yes` | `Yes` | `Yes` |
| `Claude Docs` | `Yes` | `Yes` | `Yes` | `Yes` |
| `Claude Slides` | `Yes` | `Yes` | `Yes` | `Yes` |
| `Claude Motion (beta)` | `No` | `No` | `No` | `No` |
| **`Claude Sheets (beta)`（本期新增，标 `New`）** | **`No`** | `Yes` | `Yes` | `Yes` |
| **`Claude Whiteboards (beta)`（本期新增，标 `New`）** | **`No`** | `Yes` | `Yes` | `Yes` |
| `Claude Data` | `No` | `Yes` | `Yes` | `Yes` |
| `Fable` | **`No`** | `Usage credits` | `50% of weekly limits*` | `50% of weekly limits*` |
| `Usage credits` | `No` | `Yes` | `Yes` | `Yes` |

**⚠️ 这张表里最值钱的一行不是新增的两行，是上面三行老能力的对照**：`Design` / `Docs` / `Slides` **四个档全给 `Yes`**，而**三个带 `(beta)` 的新能力（`Motion` / `Sheets` / `Whiteboards`）在 `Free` 列一个 `Yes` 都没有**，其中 `Motion` 连 `Pro` 都是 `No`。**同一类能力、同一张表、同一天 —— 老的对免费开放，新的对免费关闭。** 这不是「免费额度变少」，是**新能力从上线那一刻起就不进免费档**。

**⚠️ 三条必须钉住的边界**：

1. **`Free` 列写 `No` ≠ 「Free 档看不到这个功能入口」** —— 定价页只承诺「套餐包含什么」，**入口是否可见、试用是否可点，定价表不回答**。本报告只报表格里的字，不推断界面。
2. **`Interactive Connectors` 在页内 `0` 命中** —— 媒体列的四个东西里，**三个能在定价页找到对应行（`Sheets` / `Whiteboards` / 既有 `Connectors`），`Interactive Connectors` 找不到**。**同一篇报道里的四个名词，证据强度不同。**
3. **`Claude Meetings` 是 `coming soon`，不是「已上线」** —— `The Decoder` 逐字 `is coming soon`，`TechCrunch` 标题写 `launches`。**两家标题一个说「即将」一个说「发布」，本期采信官方口径的「即将」。**

**⚠️ 「免费」这件事在本期出现的次数**：公告体系（工作台扩张）里 **`Free` 只在定价表出现，正文一句没有**；`Claude` 的免费档仍然是 `$0` / `Free for everyone` / `Limited usage every 5 hours and every week`，**与 064 期逐字相同**。**这一轮扩张没有给免费档加任何一项能力。**

### 2. ⚡ `OpenRouter` 免费区第一次净减：**`:free` `13 → 12`，掉的是一条本报长期登记的零价条目**

**一手**：`openrouter.ai/api/v1/models`（`200` / **`842,553`** 字节，064 期 `836,217`），与 064 期归档做 `ID` 级 diff；另用 `?max_price=0` 端点做第二口径交叉验证（`15 → 14`）。

| 项 | 064 期 | 本期 | 变化 |
| --- | --- | --- | --- |
| 全量 | `465` | **`469`** | **`+4`** |
| 零价（`prompt` 与 `completion` 严格等于 `"0"`） | `16` | **`15`** | **`−1`** |
| `:free` 后缀 | `13` | **`12`** | **`−1`** |
| `?max_price=0` 端点（第二口径） | `15` | **`14`** | **`−1`** |
| 新增 `ID` | `6` | **`6`** | — |
| 消失 `ID` | `2` | **`2`** | — |
| `pricing` 变化 | `12` | **`10`** | — |

**新增 6 条**：`google/gemini-4-carbon`、`google/gemini-4-carbon:batch`、`baidu/ernie-5.5-flash-preview`、`baidu/ernie-light-dt-1.0-intl`、`kt/midm-k-3.0-pro`、`motif-technologies/motif-3`。
**消失 2 条**：`qwen/qwen-2.5-7b-instruct`、**`xingchen-agi/xing4.0-29b-a4b:free`**。

**⚠️ 这条为什么值得单列**：`xingchen-agi/xing4.0-29b-a4b:free` 不是一条陌生条目 —— 它在本报 `4.2` 里挂着「中国电信 `Xing4.0-29B-A4B` 上架 OpenRouter 免费档」，备注还写着「免费档额度按官方口径 `50` 次/日」。**这一条本期从表体改成了 `⚪ 已从 OpenRouter 目录下架`**。**三个口径同时指同一件事**：全量口径（`465 → 469` 里少了它）、零价口径（`16 → 15`）、`:free` 口径（`13 → 12`）——**三条线同向，才能写「下架」**（只凭一条线只配写「没搜到」，避坑 277）。

**⚠️ 厂商侧本期没有说明**：`xingchen-agi` 是聚合器上的厂商账号，**官方没有发下架公告，也没有说「限时结束」**。本报告只报「目录里没有了」，不推断是转付费、限时到期还是撤档。

**⚠️ 同时 `10` 条调价，方向对半**：`z-ai/glm-5.3-flash` 输入 `$0.15 → $0.0399` / 输出 `$0.50 → $0.0784`（**回落**，见第五章纠错②）；`~z-ai/glm-flash-latest` 微涨（`0.0335 → 0.0399`）；`mancer/weaver`、`undi95/remm-slerp-l2-13b`、`z-ai/glm-5.1`、`z-ai/glm-5.2:batch`、`deepseek/deepseek-v4-flash` 下调；`z-ai/glm-5.2`、`~moonshotai/kimi-latest` 上调。**免费区那 `12` 条一条没动**（它们本来就是 `0`）。

### 3. ⚡ `DeepSeek Harness` 全球开放测试并开源：**「免费」写在官方页，「发 Token」只写在媒体里**

**一手**：`deepseek.com/harness`（`200` / **`206,789`** 字节）。官方逐字：**「面向全球开放测试并同步开源，以可自由组合的插件，拓展 Agent 能力」**；页面结构给到 `下载桌面端（macOS Apple 芯片 / Windows 64 位）`、`GitHub`、`开发者文档`、`社区插件`、`Cordis 论文` 五个入口，并标 `预览版`。架构口径逐字 **「基于 `Cordis` 的「一切皆插件」架构构建」**。

**媒体一手（窗口内）**：`InfoQ` `11/11 00:20`「DeepSeek Harness 日活154万，官方开始给插件作者发Token：Agent 生态要靠开发者了」。

**⚠️ 两件事必须拆开**：

| 说法 | 来源 | 本期能不能核 |
| --- | --- | --- |
| 「面向全球开放测试并同步开源」 | **官方页逐字** | **能**（`206,789` 字节页内直读） |
| 「日活 `154` 万」 | 媒体 | **不能**（官方页 `154` 命中 `0`） |
| 「官方开始给插件作者发 `Token`」 | 媒体 | **不能**（官方页 `Token` / `token` / 免费 / 额度 / 激励 **各 `0` 命中**） |

**⚠️ 所以本期只登记「产品免费开放测试 + 开源」这一层**，「发 `Token`」按本报规则**只算媒体口径、不进表** —— **补贴是「免费额度」里最容易被中转稿夸大的那一类**（过去三期里出现过两次同类：媒体写「免费开放」，官方原文是「对所有用户开放」）。**等官方页出现额度说明再登记。**

**⚠️ 附带一条**：`Cordis`（插件架构）与「社区插件」两个入口都在页面上，**说明它的「开源」不只是模型权重，还包括插件层** —— 这一点比 `Token` 补贴更持久：**补贴会停，架构不会。**

### 4. ⚡ `Kimi K3.1` 的权重一直在：**本报把一个不存在的型号名当了 6 期检索词**

**一手**：`hf-mirror.com/api/models?author=moonshotai`（`200`）逐仓实读；`hf-mirror.com/api/models?search=Kimi-K3.1-Highspeed`（`200` / **`2` 字节 `[]`**）。

| 检索方式 | 结果 |
| --- | --- |
| `?search=Kimi-K3.1-Highspeed`（本报 060–064 期用法） | **`[]`（`2` 字节）**，连续第 `6` 期为空 |
| `?author=moonshotai`（本期改法） | **`moonshotai/Kimi-K3.1-Pro`** —— `createdAt 2026-11-02T04:13:51Z`、`gated: false`、`license: other`、`downloads 30,721`、`likes 1,878`、`pipeline_tag: image-text-to-text`、权重为 `mxfp4-pack-quantized`（`compressed-tensors`） |

**⚠️ 结论不是「官方补放了权重」，是「本报的检索词一直指错」**：`K3.1` 家族在 `HF` 上只有 `Pro`，**没有 `Highspeed` 这个型号**。连续 6 期把 `search=` 的空数组当成「官方没放」，等同于把「我没找到」写成「它不存在」（避坑 285）。

**⚠️ 同时这也把 064 期强制动作⑫ 结掉了**：不再追问「`Highspeed` 何时上架」，改记 **`Kimi-K3.1-Pro` 权重自 `11/2` 起可下载、`gated: false`（无需申请）**。`license: other` 意味着**商用条款要逐条读仓库许可，本文不代读**。

**⚠️ 交叉验证**：`AWS` 官方博客 `11/11 09:07` 发布 **`Introducing Kimi K3.1 Pro on Amazon Bedrock`**，正文提到可用 `OpenAI` 兼容的 `Chat Completions` / `Responses` / `Converse` 三个接口、并「在 `OpenCode` 里当编码助手用」。**同一周里，权重在 `HF`、托管在 `Bedrock`、客户端在 `OpenCode` —— 三层都到位。**

### 5. ⚠️ 两条「进目录但不进免费区」的边界案例

**① `Google Gemini 4 Carbon`**：`OpenRouter` 新增 `google/gemini-4-carbon` 与 `:batch` 两条，**`Artificial Analysis` 页面同日出现 `Gemini 4 Carbon (high)` / `(medium)` 两档**，但 `isOpenWeights: false`、`openSourceCategorization: proprietary`。**没有任何零价 `SKU`** —— **能用到，但要付费；权重没有。**

**② `Meta Muse Ember`**：`search=Muse-Ember` 仍返回 **`[]`（`2` 字节）**、`author=meta-llama` 全量 `70` 仓里 `Muse` **命中 `0`**、`ai.meta.com/blog/` 本期仍 **`000` / `0` 字节**。**连续第 `2` 期「目录有、权重无、官网不可达」**。窗口内媒体另报它「上了 `Apple Watch` 与 `Android Wear OS`」（`TechCrunch` `11/10 23:29`）—— **进的是终端，不是权重**。

**⚠️ 这两条都不进第四章、也不进极速页**：本报收的是「免费能拿到的东西」，**它们是「新模型但只有付费档」**，登记在这里是为了让读者知道「为什么它不在免费清单里」。

---

