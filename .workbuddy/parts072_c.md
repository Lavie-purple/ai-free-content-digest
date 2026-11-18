---

## 八、本期信源体系更新

**新增可复用抓法三条**：

1. **「闷声挂仓」比公告早一天，抓法是按作者端点拉全量再按 `createdAt` 排。**
   `hf-mirror.com/api/models?author=tencent&limit=100`（本期 `45,368` 字节、`100` 条）→ 按 `createdAt` 倒排，**第一条就是当天的新仓**；再用 `?search=Hy4&limit=50`（`33` 条，含第三方 `GGUF` / `MLX` / `FP8` 转档）交叉确认「生态有没有跟上」。**本期这条路比聚合层的官方帖早 `25` 小时**。**从此对「国产大厂开权重」这类条目，先拉作者端点、再看公告** —— 与 059 期「免费条目靠目录 diff、不靠标题」同一条思路。
2. **许可证必须走 `raw` 端点，而且要和模型卡一起读。**
   `/<repo>/raw/main/LICENSE`（本期 `13,942` 字节）+ `/<repo>/raw/main/README.md`（`20,098` 字节）**两个文件分工不同**：**模型卡给参数表与架构，许可证给商用边界**。`api/models` 的 `cardData.license` 只会给你一个 `other` —— **`other` 是「不是标准协议」的意思，不是「没有约束」**。
3. **`OpenCode` 的弃用表在同一页，抓法是从 `Free models` 往下滚到 `Deprecated models`。**
   清单回答「现在有谁」、弃用表回答「谁哪天走」。**本期第一次读它，直接解释了上一期那条「净减 `1`」**。**从此这一条固定两段式抓取**（清单 + 弃用表），不再只数 `-free` `id`。

**信源质量记账（本期新增三条、恶化一条）**：

- **`lmarena.ai` 连续 `5` 期 `000`**（`068`–`072`）：**本报已连续五期无法引用 `LMArena` 任何榜单数字**。本期榜单侧改用 `Artificial Analysis`（`1,198,902` 字节、`GPT-6.2` 相关 `162` 处）与 `llm-stats`（`2,135,094` 字节）—— **但这两家与 `LMArena` 的口径不同，不可互相替代**。
- **`antigravity.google/pricing` 连续 `2` 期 `000`，且首页退化为 `JS` 壳**：这一条从「偶发」升级为「缺口」。**在恢复之前，本报不出任何「`Antigravity` 免费档含哪些模型」的现在时表述** —— 只引用 071 期已取回的 `178,404` 字节快照，并标注「截至 `11/17`」。
- **`openai.com/api/pricing` 不跟随发布更新**：`GPT-6.2` 发布当天，该页 `gpt-6.2-astra` / `gpt-6.2-sol` **各 `0` 命中**，`gpt-6-astra` 仍 `4` 处。**价格只能从发布页正文取** —— 这是「定价页滞后于发布页」的第 `1` 次记录，**以后不要用定价页反推「有没有新模型」**。
- **`qwen.ai/blog` 连续 `2` 期 `JS` 壳**（本期去标签后可见文本 **`1` 行**）。`DeepSeek` 动态页最新仍是 **`2026 年 9 月 10 日`**（`V4.1 Flash`）—— **两家国内一线本期都没有新发布，这本身是一条事实**，写在这里，不占头条。

---

## 九、来源与核查说明

**本期一手来源（按引用顺序，均标注取回字节数）**：

| 来源 | 用途 | 状态 |
| --- | --- | --- |
| `hf-mirror.com/api/models/tencent/Hy4-flash` | `createdAt` / `downloads` / `likes` / `safetensors.total` / 文件数 | `200` / `29,165` B |
| `hf-mirror.com/api/models/tencent/Hy4-flash-FP8` `-base` | 三仓同分钟建仓、各自 `likes` | `200` / `72,699` + `23,156` B |
| `hf-mirror.com/tencent/Hy4-flash/raw/main/README.md` | 参数表、架构、`vLLM` / `SGLang` 段 | `200` / `20,098` B |
| `hf-mirror.com/tencent/Hy4-flash/raw/main/LICENSE` | **`§10` 两个门槛 + `§10.3` 豁免** | `200` / `13,942` B |
| `hf-mirror.com/api/models?author=tencent` / `?search=Hy4` / `?author=Tencent-Hunyuan` | 作者全量、第三方转档、同名组织 | `200` / `45,368` + `13,745` + `8,589` B |
| `api.github.com/repos/Tencent-Hunyuan/Hy4-flash` | `44` stars / `created_at` / `pushed_at` | `200` / `7,176` B |
| `openai.com/index/introducing-gpt-6-2-astra-sol` | 可用名单、`Ultrafast`、API 价 | `200` / `828,587` B |
| `openai.com/news/` | `publicationDate` `2026-11-17T17:45:00Z` | `200` / `360,550` B |
| `openai.com/api/pricing/` | 反证：`gpt-6.2` 未列 | `200` / `783,662` B（`0` 命中） |
| `openrouter.ai/api/v1/models` + `?max_price=0` + `Ling` 端点 | `478/17/14/16`、`8` 条 `GPT-6.2`、`Ling` 空端点 | `200` ×3 |
| `platform.minimaxi.com/document/price` | `4K` 五折价目、`6` 处徽标、截止时刻原文 | `200` / `311,607` B |
| `runware.ai/pricing` | 促销数组 `22` 条、`4K` 徽标 `2 → 0`、`4K` 只挂徽标的帮助文案 | `200` / `782,116` B |
| `opencode.ai/docs/zen` | `Free models` `12` 条 + `Deprecated models` 表 | `200` / `102,315` B |
| `aihot.news/free-tokens` | `Token 羊毛` 第 `10` 期（`¥1738` / `61` 张） | `200` / `481,474` B |
| `aihot.news/` | 当日 `33` 条：`Hy4 flash` 官方帖、`Gemini 4 Hydrogen`、`AI Studio` 全栈 `Android`、`OpenClaw` 登录 | `200` / `244,565` B |
| `hf-mirror.com/api/models/*`（`Kimi` / `LongCat` / `ERNIE` ×2） | `downloads` / `likes` / `lastModified` | `200` ×4（`Inkling` `429`） |
| `api.github.com/repos/mit-han-lab/pear` / `runwayml/praxis-1-oss` | `654` / `117` stars、`pushed_at` | `200` ×2 |
| `freellm.net` | `170,931` B、`md5 6b1d95eb` | `200` |
| `autoclaw.zhipuai.cn/blog/news/M11W3/` | `100M Tokens` 活动到 `11/22`（与 071 同一条） | `200` / `47,578` B |
| `antigravity.google/` / `/pricing` | **首页 `200` 但是 `JS` 壳；定价页 `000`** | `200` / `217,290` B；`000` |
| `artificialanalysis.ai` / `llm-stats.com` | `GPT-6.2` 已入榜（AA 逐字 `#2`） | `200` / `1,198,902` + `2,135,094` B |

**口径声明（本期新增四条）**：

1. **`Hy4 flash` 的参数一律写两套**：**`220.25B`（`safetensors` 实测，本报采用）+ 媒体 `224B`**；**激活写 `11.3B + 0.43B`（模型卡），并注明媒体写作 `12B`**。**不合并成一个数。**
2. **`OpenCode` 的池子数本期改口径**：从「`-free` `id` 正则」改为「`Free models` 段落逐条」。**`12`（本期段落）/ `11`（本期正则）/ `14`（071 期正则）三个数不可相减**，正文已标。
3. **`1M` 上下文两个写法**：厂商模型卡写 `1M`（`1,048,576`）、`OpenRouter` 写 `1,050,000`。**本报写「`1M`（`1,048,576`）」，并注明聚合层取整到 `1,050,000`。**
4. **`Runware` 的促销「数组 / 徽标 / 价目」三处分开记**：**数组是账本**（只追加不清扫）、**徽标是货架**（`4K` 类唯一可靠信号）、**价目对 `4K` 类本来就不动**。**三者不一致是常态，不是异常。**

**本期未核到的项（如实列出，不补位）**：

- **`Antigravity` 的 `11/18` 三条模型是否已移除** —— 定价页 `000`（第 `2` 期）、首页 `JS` 壳、四个关键词 `0` 命中。**本期不出结论。**
- **`GPT-6.2` 在免费档的可用性** —— `chatgpt.com/pricing` `000`、`openai.com/api/pricing` 未更新。**只能说「发布页的可用名单里没有 `Free`」。**
- **`Hy4 flash` 的 `ModelScope` 页** —— `200` 但是 `JS` 壳（去标签后可见文本 `1` 行），**下载量与点赞数没取到**。
- **`Inkling-2-Small` 的 `downloads`** —— `429` 限流，本期**不写涨跌**。
- **`Gemini 4 Hydrogen` 进 `Search`、`AI Studio` 全栈 `Android`** —— 只有聚合层转述，**`Google` 两个官方博客本期 `000`**，**这两条只写「有什么」，不写额度与限制**。
- **`AutoClaw` `M11W4`** —— 页面 `404`（下周才开），**额度是否延续 `100M` 未知**。
