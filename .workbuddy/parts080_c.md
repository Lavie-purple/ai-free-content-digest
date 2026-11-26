## 八、本期信源体系更新

**本期按《AI 信息源分级清单 · T0–T4》重校了一遍路由，三处改动、一处升级、一处降级。**

| 动作 | 对象 | 原因 |
| --- | --- | --- |
| **新增必查位** | `hf-mirror.com/api/models?sort=trendingScore&limit=40` | **本期唯一的补登项（`Ternary-Bonsai`）只能从趋势榜捞到** —— 它挂在 `GGUF` 类目、名称里没有厂商名，官网 / `X` / 媒体三条线全不覆盖。**从本期起：趋势榜进「每期必跑」，用于捞「无厂商署名」的免费权重。** |
| **新增口径位** | `OpenRouter` 的 `:batch` 后缀 | 079 期已把它记成「SKU 迁移 ≠ 新增模型」，**但没有独立计数**；本期起**与 `:free` 分开统计**，且**不进免费池**（避坑 341）。 |
| **升级** | `aihot.news/free-tokens`（T4 聚合器） | 从「抽查」升为「**每期必查**」。理由：它是本报唯一能拿到「按官方价折算成人民币」的口径，**`¥847 / 61 张` 这两个数没有第二个来源**。⚠️ **升级的是频次，不是可信度** —— 它是聚合层，逐条必须回一手（本期 `MonkeyCode` 的规则变化就是从卡片原文读到的）。 |
| **降级** | `deepmind.google/discover/blog`、`ai.meta.com/blog`、`mistral.ai/news`、`x.ai/news` | 四家本期首轮全 `000`，**且都只请求了 `1` 次**。**降级为「可选」，本轮不写「站点异常」** —— 按纪律，一次取不到不等于关闭（第九章）。 |
| **登记待观察** | `docs.bigmodel.cn/cn/coding-plan/credit-campaign-rules` | 本期新增导航项，**活动生效日期 `2026-03-15`（旧活动补挂）**。**教训已写进流程：新增页面先读「生效日期」，再决定是否当新闻。** |

**一条流程修订（本期新增）：** 「厂商官网 + 官方 `X` + 中文媒体」这三条线，**只能覆盖「有署名、有发布会」的发布**；**本期 `Ternary-Bonsai` 与 `dots` 这两条，都是「无署名 / 无发布会」的类型**，前者靠趋势榜、后者靠 API 全集差集。**因此每期固定两个「无署名入口」：`HF` 趋势榜、`OpenRouter` 全量目录差集。** 缺任一个，就会漏掉一类发布。

**关于「一次取不到」的写法（沿用 076 期定的口径）：** 本轮四家官网 `000` **只记「本期未取到」**，不写「站点下线 / 政策变化」。**要写「关了」，至少要 `2` 次重试 + `1` 个替代入口同时失败** —— 本期 `antigravity` 首页与定价页就是「首轮 `000`、重试 `200`」，**差点被写成缺口**。

---

## 九、来源与核查说明

**一、本期一手端点（`200` 且有实质读数，共 `23` 个）**

| 端点 | 状态 / 字节 | 用途 |
| --- | --- | --- |
| `openrouter.ai/api/v1/models` | `200` / `921,576` | 全量 `474`、`:free` `11`、零价 `14`、`:batch` `96`、进出差集 |
| `openrouter.ai/api/v1/models?max_price=0` | `200` / `21,076` | `?max_price=0` 口径 `13` |
| `openrouter.ai/api/v1/models/thinkingmachines/inkling-2-mini/endpoints` | `200` / `8,385` | 七个价点与四档上下文 |
| `openrouter.ai/api/v1/models/dots-studio/dots-3-note-preview%3Afree/endpoints` | `200` / `482` | `endpoints: []`（第 `2` 期） |
| `openrouter.ai/api/v1/models/dots-studio/dots-3-note-preview:free` | `404` / `44` | 裸冒号不可用 |
| `hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Preview`（及 `-FP8` / `-BF16`） | `200` / `8,796`·`8,451`·`5,736` | 三仓次日下载与 `likes` |
| `hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base`（及 `-BF16`） | `200` / `19,279`·`—` | `5,938` / `2,308` |
| `hf-mirror.com/api/models/tencent/Hy4`（及 `-base` / `-flash` / `-flash-FP8` / `-flash-base`） | `200` / `33,758` 起 | 五仓 `+2,291` |
| `hf-mirror.com/api/models/thinkingmachines/Inkling-2-Mini`（及 `-Small`） | `200` / `9,762`·`10,907` | `+27,485` / `+11,142` |
| `hf-mirror.com/api/models/moonshotai/Kimi-K3.1-Pro` | `200` / `8,093` | `+4,786` |
| `hf-mirror.com/api/models/meituan-longcat/LongCat-2.5`（及 `-2.0`） | `200` / `37,633`·`22,308` | `+184` / **`−29`** |
| `hf-mirror.com/api/models/prism-ml/Ternary-Bonsai-2.5-27B-GGUF` | `200` / `8,747` | 补登项的许可、基座、下载 |
| `hf-mirror.com/api/models?sort=trendingScore&limit=40` | `200` / `21,155` | 补登入口 |
| `hf-mirror.com/api/models?author=baidu&limit=200` | `200` / `19,279` | `42` 仓、`0` 新增 |
| `runway.com/pricing` | `200` / `1,310,856` | `25% off` `21` 处、`expiresAt` `12/01` |
| `runware.ai/pricing` | `200` / `787,238` | 促销数组 `2` 条、`dehydratedAt` `11/26 01:06Z` |
| `platform.minimaxi.com/document/price` | `200` / `309,542` | 第二版第 `8` 天、正文 `0` 行变 |
| `opencode.ai/docs/zen` | `200` / `103,856` | 导航改版、免费段 `11` 条未变 |
| `aihot.news/free-tokens` | `200` / `513,309` | `¥847` / `61` 张 / 两处可归因卡片 |
| `freellm.net` | `200` / `170,810` | 四个计数 `+5` |
| `docs.bigmodel.cn/cn/coding-plan/overview` | `200` / `158,116` | `GLM-5.4` `14` 处、`免费` `0` 处、API 未开 |
| `docs.bigmodel.cn/cn/coding-plan/credit-campaign-rules` | `200` / `143,085` | 「拼好模」生效日 `2026-03-15` |
| `antigravity.google/pricing` | `200` / `188,088`（`3` 次请求 `200/200/000`） | 脚注 `13` 处、免费档 `5` 模型 |
| `autoclaw.zhipuai.cn/blog/news/M11W4/` | `200` / `48,257` | `11/23`–`11/29`、`100M` |
| `autoclaw.zhipuai.cn/blog/news/M11W5/` | `404` / `18,994` | 第 `5` 期未挂 |

**二、核查纪律与本期执行**

1. **「计数」与「明细」同源生成**：`474 / 11 / 14 / 13` 四数取自同一份 `921,576` 字节响应；`:batch` 的 `96` 条、`73 / 16 / 4 / 3` 分布，全部由该响应内的 `pricing.prompt` 现算，**未引用任何二手汇总**。
2. **不看单点、看两期**：`dots` 的三条读数、`Runware` 的 `2` 条、`MiniMax` 的「字节变正文不变」，**都要求连续两期同向**才写结论；`LongCat-2.0` 的 `−29` 只有一期，**本期只记「出现倒退」，不下结论**。
3. **口径变更显式声明**：`HF` 从「十三仓」改「十五仓」，**两个合计不相减**；`AIHOT` 的 `¥` 与「张」**不相加、不相减**；`Runway` 的 `11/30`（文案）与 `12/01`（配置）**并列不合并**。
4. **「取不到」与「已撤下」分开写**：本轮 `10` 个 `000`、`5` 个 `404`、`2` 个 `403`，**全部记「本期未取到」**；唯一按「已下线」结案的是 `dots-3-note-preview:free`，依据是**连续两期 `endpoints: []` + 目录 `0` 命中 + 裸冒号 `404`**，不是单次失败。
5. **时区**：本轮所有官网时间为**页面原文**，换算成北京时间时按 `PST`（`UTC−8`）处理；`HF` 的 `createdAt` 为 `UTC`，**换算示例：`2026-11-24 16:32Z` ＝ 北京 `11/25 00:32`**（`+8` 小时，不是 `+16`）。
6. **本报不做的事**：不预测价格、不替厂商解释动机、不把「聚合层转述」当一手（本期「拼好模」若只看导航标题，就会误报成新活动）。

**三、与往期的衔接**

- **本期对 079 期的纠错 `4` 条**（第五章）、**新增避坑 `341`–`344`**（第六章），**不修改 079 期原文**。
- **`4.1` / `4.2` 两张表**由脚本按基准日 `2026-11-26` 重算天数，**逐行 diff 与三态分布见第四章脚注 ④**。
- **本报告的数据时点为 `2026-11-26 09:00`（GMT+8）**，此后的发布不在本期覆盖范围；**早间出刊天然漏掉当天上午晚些时候的发布**，这一条从 001 期沿用至今。

---
