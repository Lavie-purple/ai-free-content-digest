# AI 免费内容与权益速递 · 第 067 期

**2026-11-13（周五）· 本期是「前沿档模型第一次对免费用户开门，但只开一条缝」的一期** —— 谷歌 `11/12` 发布 **`Gemini 4 Hydrogen`**，官方博客逐字写得很清楚：「**In the Gemini app, free users will get access to Gemini 4 Hydrogen via auto model selection when it's the appropriate model for the prompt**」。**免费用户能用到它，但点不到它** —— 应用里的模型下拉里没有这一项，只能等系统判断「这个提示词该用它」。同一天它出现在 `OpenRouter`（`$1.50` / `$7.50`、`1,048,576` 上下文、五种输入模态）和 `OpenCode Zen`（同样 `$1.50` / `$7.50`，**全站只有它不打折**）。**三条一手口径给出同一个价格，这是本报第一次见到「三层价完全一致」** —— 上一期文心那条正好相反，三层价三层来源、只有一层是一手。**另一条是「开源」二字背后的第四条脚注**：MiniMax `H3-Image` 权重确实开放，但它的社区许可第 `5` 条把**欧盟、英国、韩国、美国**整个划成 `Excluded Territories` —— **「开源」与「哪里都能用」是两件事，而这一条写在 `LICENSE` 里、不在模型卡首页。**

**主题：AI 免费内容发布 · 免费内容（生成/分发）· 免费额度**

> 扫描截止 **2026-11-13 18:00（GMT+8）**，**窗口 = 上一期（066）扫描截止 11/12 12:55 → 本期截止**，约 **29.1 小时**。
> ⚠️ **本期的性质：隔日出刊、窗口 `29.1` 小时**（066 期 `22.9` 小时、065 期 `25.8` 小时）。**窗口起点 ＝ 上期截止点，各期内容各自独立成立、不合并、不互相覆盖。**
> ⚠️ **窗口换算**：**起于北京 `11/12 12:55` ＝ 美西 `11/11 20:55 PT`；止于北京 `11/13 18:00` ＝ 美西 `11/13 02:00 PT`**（冬令时 `PST`，`UTC−8`，北京快 `16` 小时）。**整段窗口覆盖美西 `11/12`（周四）一个完整工作日，再加周五凌晨两小时** —— 066 期撞上 `Veterans Day`、大厂集体静默，**本期正好是假日后第一个工作日，「积压 + 当天」一起放出来**：谷歌一天里发了 `Gemini 4 Hydrogen` 与 `Gemini 4 Hydrogen for Search` 两篇、`World Labs` 发了 `Atlas`、`MiniMax` 的 `H3-Image` 媒体稿铺开、`Anthropic` 的 `Claude Meetings` 进了 beta。
> ⚠️ **本期的实抓规模**：**清单 `285` 行 / 唯一文件名 `285` 个 / 实际落盘 `285` 个**；`200` 共 **`195`**（`68.4%`）、`000` 共 **`51`**（`17.9%`），另 `403` `12` / `404` `8` / `500` `3` / `503` `2` / `429` `2` / `412` `2` / `405` `2`，其余 `202`–`521` 各 `1`；**解析出 `3,293` 条带时间戳条目、落在窗口内 `146` 条**（`hnrss 20`、`leiphone 20`、`techcrunch 19`、`aws_ml 11`、`infoq 11`、`lesswrong 10`、`verge 10`、`wired 10`、`qbitai 8`、`decoder 7`）。
> 与 001–066 期的关系：**只做增量与纠错，不重复已固化内容**。**本期纠错 3 条（第五章）**、**新增避坑 3 条：291–293**。


---

## 摘要（3 秒版）

- **本期头条（前沿档第一次对免费用户开门，但门上没有把手）**：谷歌 `11/12` 发布 **`Gemini 4 Hydrogen`**（`blog.google` 一手，`417,537` 字节，页面日期逐字 `Nov 12, 2026`）。定价 **`$1.50` / `$7.50` 每百万 token，整个 `1M` 上下文一口价**；`Artificial Analysis` 智能指数默认 `high` 档 `51`（超过 `Argon` 的 `50`）、`xhigh` 档 `54`。**免费用户的口径只有一句官方逐字**：「**In the Gemini app, free users will get access to Gemini 4 Hydrogen via auto model selection when it's the appropriate model for the prompt.**」—— **能用到、不能点名要**；`Google Search` 侧对全部用户开放。**`Antigravity` 里它只给付费的 `AI Pro` / `Ultra`** —— 与上一期「`Antigravity` 个人免费档」那条并排看，是免费档在同一天里被划走了一块。
- **本期头条之二（「开源」的第四条脚注：地域）**：MiniMax `H3-Image` 权重在 `HF` 上（`306,718` 次下载、`933` 赞、`gated: false`），但许可第 `5` 条把 **`Excluded Territories` 定义为「欧盟、英国、韩国、美国」**，且**年化营收超 `$1M` 或对外提供 `Hosted Service` 需另签**、**商业产品界面须显著展示 `MiniMax-H3-Image`**。**「开源」「能下载」「能商用」「哪里都能用」是四件事**，本报按四层分开写。
- **本期第三条（有确切截止日的那条：`11/18 00:00` 北京）**：MiniMax 官方定价页逐字 **「4K 生图限时 5 折：即日起至 2026 年 11 月 18 日 00:00（北京时间，结束时刻不含），`MiniMax-H3-Image` 和 `MiniMax-H3-Image-Highspeed` 最终交付图片的宽 × 高 ≥ 1660 万像素，即享整次请求费用 5 折」**。`4K` 单张 **`0.4522 → 0.2261` 元**；媒体标题里的「一张两毛」就是这一格，**但它是折后价、且必须 ≥ 1660 万像素** —— 两个条件缺一不可。
- **本期第四条（挂了 `6` 期的账，本期在 `HF` 上看到了）**：`thinkingmachines/Inkling-2-Small` 出现在公开仓库列表里 —— `apache-2.0`、`gated: false`、`36` 个文件、`24` 个 `safetensors` 分片、`downloads 12` / `likes 166`。**建仓 `11/04`、`lastModified` `11/13 03:42 UTC`、本期才进 `?author=` 列表** —— 三件事分开写（059 期纪律：`createdAt` 不是公开时间）。
- **本期第五条（免费区 `+1`，但付费档这次没消失）**：`OpenRouter` 全量 **`467 → 472`（`+5`）**、零价 **`16 → 17`**、`:free` **`13 → 14`**、`?max_price=0` **`15 → 16`**。进 `google/gemini-4-hydrogen`（含 `:batch`）、`moonshotai/kimi-k3.1-pro:batch`、`thinkingmachines/inkling-2-small`、`particle-ai/particle-1:free`；**消失 `0` 条**。**`particle-1:free` 与付费的 `particle-1` 并排存在、`created` 相同** —— 这是避坑 289 的**第二种形态**：不是「换档」，是「并排多开一个免费 `SKU`」。

---

## 一、AI 免费内容发布（分发入口线）

### 1. ⚡ `Gemini 4 Hydrogen`：**免费用户「能用到、点不到」—— 三层价第一次完全一致，免费路径只有一条半**

**一手**：`blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/`（`200` / **`417,537`** 字节，页面日期逐字 `Nov 12, 2026`）。作者 `Koray Kavukcuoglu`（`SVP, Google DeepMind and Chief AI Architect`）。官方逐字四段：

> 「Gemini 4 Hydrogen is priced flat across its entire 1 million-token context window at **`$1.50` per million input tokens and `$7.50` per million output tokens**.」
> 「Hydrogen surpasses Argon on the Artificial Analysis Intelligence Index at its default high thinking level (**`51` vs. `50`**, and reaching **`54`** at its highest xhigh thinking setting)」
> 「**For everyone:** Start using it in the Gemini app model drop down and in Google Search for all users」
> 「**In the Gemini app, free users will get access to Gemini 4 Hydrogen via auto model selection when it's the appropriate model for the prompt.**」

**⚠️ 第一条边界：免费路径是「自动选模」，不是「免费档位」。** 官方两句话必须并排读：一句说「`For everyone` … in the Gemini app **model drop down**」，另一句紧接着说「free users will get access … **via auto model selection**」。**合起来的意思是：下拉框里有它，但免费用户不自己去点，而是由系统在「提示词适合」时替他们选。** 本报**不写「免费用户可以在下拉里选 Hydrogen」** —— 官方没有这么写，媒体转述成「免费用户也能用」时把这层机制删掉了。

**⚠️ 第二条边界：没有额度、没有次数、没有开关。** 整篇 `417,537` 字节里，`free tier` / `quota` / `requests per day` / `rate limit` 一类表述**一个都没有**；「免费」只以 `free users` 这一处的身份出现在 `auto model selection` 那句里。**所以本条不能进「免费额度」栏，只能进「免费入口」栏** —— 「能碰到」与「能算清楚给你多少」是两个层次。

**⚠️ 第三条边界：`Antigravity` 里它只给付费。** 官方逐字「**if you're a paid Google AI Pro or Ultra subscriber, you can try it in Google Antigravity**」。**这与 066 期 4.2 里那条「`Google Antigravity` 个人免费档（官方定价页逐字 `$0/month`）」并排看，是同一天里被划走的一块**：`Antigravity` 的免费档还在，但**新模型不在免费档里**。**「产品有免费档」与「新模型进免费档」是两件事**（与 066 期 `Claude Meetings` 那条同源：能力上线 ≠ 免费档有了）。

**⚠️ 第四条边界：三层价这次完全一致 —— 值得单独记一句。** 同一模型在三个一手口径上读到的价：

| 口径 | 一手程度 | 输入 / 输出（每百万 token） | 上下文 |
| --- | --- | --- | --- |
| `blog.google` 发布页 | **官方逐字** | `$1.50` / `$7.50`（「priced flat across its entire 1 million-token context window」） | `1M` |
| `OpenRouter` 目录 `JSON` | **一手（`JSON`）** | `0.0000015` / `0.0000075`，即 `$1.50` / `$7.50` | `1,048,576` |
| `OpenCode Zen` 价格表 | **一手（`HTML`）** | `$1.50` / `$7.50` | — |

**三层同值，本期没有口径差可写** —— 这与上一期文心那条正好相反（那里是「媒体价 / 聚合器零价 / 权重未开」三层三层来源）。**所以本期不给「哪个价可信」的结论，只记「三方一致」这个事实**：一致不等于正确，但一致意味着**没有哪个渠道在私自加价或补贴**。

**⚠️ 第五条边界：`OpenCode Zen` 全站都在五折，只有它按标价。** 同一张价格表里，`Gemini 4 Carbon (50% off)` `$4.00 / $20.00`（划线价 `$2.00 / $10.00`）、`Gemini 4 Argon (50% off)` 同理、`Gemini 3.8 Flash (50% off)` `$1.50 / $7.50`（划线 `$0.75 / $3.75`）—— **唯独 `Gemini 4 Hydrogen` 写的是 `$1.50 / $7.50`，没有 `(50% off)` 后缀、也没有划线价**。**「新模型不打折」不是「新模型贵」**：它按标价就已经是 `3.8 Flash` 折后同价，**等于用旧模型折后价买新一代**。

**⚠️ 第六条边界：`Gemini 4 Carbon` 那条挂账本期结掉，但它不是免费项。** 066 期第一章第 5 条写「`Gemini 4 Carbon` 全面开放落在窗口外 `10` 分钟」，本期它落在窗口内 `10` 分钟处（`InfoQ` `11/12 05:05 UTC` ＝ 北京 `13:05`）。**本期读到的口径是：`Carbon` 与 `Argon` 是「前沿模型」，Hydrogen 才是「让所有人用上 Gemini 4」的那一个**（官方逐字「With Hydrogen, we're also bringing Gemini 4 to everyone」）。**所以 `Carbon` 那条不进免费清单、也不进第四章** —— 它是付费前沿档，本期只做「挂账结项」。

### 2. ⚡ `OpenRouter`：**全量 `+5`、免费区 `+1`、消失 `0` —— 免费档这次是「并排多开」，不是「换档」**

**一手**：`openrouter.ai/api/v1/models`（`200` / **`852,454`** 字节，066 期 `842,603`，`+9,851`），与 066 期归档做 `ID` 级 diff；另用 `?max_price=0` 端点做第二口径（`23,496` 字节）。

| 项 | 066 期 | 本期 | 变化 |
| --- | --- | --- | --- |
| 全量 | `467` | **`472`** | **`+5`** |
| 零价（`prompt` 与 `completion` 严格等于 `"0"`） | `16` | **`17`** | **`+1`** |
| `:free` 后缀 | `13` | **`14`** | **`+1`** |
| `?max_price=0` 端点（第二口径） | `15` | **`16`** | **`+1`** |
| 新增 `ID` | `2` | **`5`** | — |
| 消失 `ID` | `4` | **`0`** | — |

**新增 `5` 条**：`google/gemini-4-hydrogen`（`$1.50` / `$7.50`，`1,048,576` 上下文，输入模态 `audio` / `file` / `image` / `text` / `video`）、`google/gemini-4-hydrogen:batch`、`moonshotai/kimi-k3.1-pro:batch`（`$0.70` / `$6.00`）、`thinkingmachines/inkling-2-small`（**付费档**，`$0.30` / `$1.00`）、`particle-ai/particle-1:free`（零价）。
**消失 `0` 条** —— 这是本报自 060 期开始做 `ID` 级 diff 以来**第一次出现「只进不出」**。

**⚠️ `particle-ai/particle-1:free` 是避坑 289 的第二种形态。** 上一期那条是「付费 `ID` 消失、`:free` 同刻出现」（`created` 相同 ＝ 换档）。**本期这条相反**：`particle-ai/particle-1`（`$0.05` / `$0.50`）**还在**，同刻多出一条 `particle-ai/particle-1:free`，**两条 `created` 都是 `1793207893`**。**同一个模型、同一个建仓时刻、两个 `SKU` 并存** —— 所以：

- **不能写「免费区多了一个模型」**（模型没变）；
- **也不能写「付费档转成了免费档」**（付费档还在）；
- **只能写「同一模型并排多开了一个零价 `SKU`」**。

**⚠️ `thinkingmachines/inkling-2-small` 进目录是「付费档补位」，不是「新模型」。** 它的 `:free` 条目从 063 期起就在零价名单里，本期多出来的是**付费版**（`$0.30` / `$1.00`、`1,048,576` 上下文、`hugging_face_id: thinkingmachines/Inkling-2-Small`）。**`created` 是 `2026-11-09T22:04:07Z`** —— 早于本期窗口，**是聚合器目录延迟上架，不是今天发布**（与 059 期「`createdAt` 不是公开时间」同源）。**它同时是一个信号**：`hugging_face_id` 指向的仓库本期真的能打开了（见第三章第 6 条）。

### 3. ⚡ `Claude Meetings` 上线：**`beta` 只给 `Team` / `Enterprise` —— 免费档没有，定价页连续第 `3` 期 `0` 命中**

**一手**：`anthropic.com/news`（`200` / `343,872` 字节，页面上 `Meetings` **`0` 命中**）+ `claude.com/pricing`（`200` / **`1,344,061`** 字节，`Claude Meetings` **`0` 命中**）；**媒体一手**：`The Decoder` `11/13 04:26 UTC`（＝北京 `12:26`，窗口内）。

**⚠️ 三件事分开写，别混成一句「Claude 能开会了」**：

1. **能力已上线** —— `The Decoder` 逐字「Anthropic has launched Claude Meetings, a feature that puts Claude into video calls as a visible participant」，会上能答题、生成文档与白板、记录要点与待办。
2. **范围是 `beta`、只 `Team` / `Enterprise`** —— 逐字「The feature is in beta for **Team and Enterprise plans**, with **Google Meet as the only supported platform** so far」，且「Organizations running HIPAA or customer-managed encryption configurations can't use Meetings yet」。**免费档（`Free`）不在名单里。**
3. **定价页连续第 `3` 期 `0` 命中** —— `1,344,061` 字节里 `Claude Meetings` 与 `Meetings` **各 `0`**。**066 期说它「上线后没有变成第三行」，本期它真上线了，仍然没有变成第三行。**

**⚠️ 所以 066 期强制动作①的答案是「两件事都发生了」**：`Meetings` 上线了（能力层面），**定价页里仍然没有它**（目录层面）。**「能力上线」与「能力进价格表」是两个动作，中间隔着 `beta` 名单** —— 这一条本报已经连写三期，本期第一次拿到完整的「上线了但没进表」样本。

**⚠️ 附带一条：定价页字节第三次完全相同。** `1,344,061` 字节，`md5` `db8d1bc2 → 7deaeede`。**连续三期同字节、三期不同 `md5`** —— 本报不对这三期的差异做归因（066 期已立此界：字节差 = 条款差只在当次成立）。

### 4. ⚠️ 三条「当天有发布、但不进免费清单」的边界案例

**① `World Labs` 的 `Atlas`（`11/12`）**：官方博客逐字「**Atlas: Releasing our next generation world model** — Generate and reconstruct worlds and bring creations into your own workflows with our tools and developer APIs」。**全页 `free` `0` 命中、`weights` `0` 命中、`open` 只在导航里出现** —— **它是产品 + 开发者 `API`，不是免费额度、也不是开放权重**。媒体转述里的「开放」指的是「开放使用」，**不是「开放权重」**，两者差着一个下载动作。

**② `Edge0` 开源 `145B` 端侧模型（媒体口径）**：`hf-mirror` 上 `?author=edge0` 返回 **`[]`（`2` 字节）**、`?search=edge0` 返回 `502`。**本期核不到对应仓库，所以不写「已开源」** —— 只登记「有这条媒体口径、一手未核到」。**「搜不到」不等于「不存在」**（065 期避坑 285 的反面用法：那次是「没换检索键」，这次是「换了键也没有」，两种情况都要写明用了哪个键）。

**③ `NVIDIA` 管理层更替（`11/12`，窗口内、全窗口最大的一条新闻）**：`Wired` / `The Verge` / `TechCrunch` 十余条，`11/12 21:58 UTC` 起铺开。**它不进本报任何一章** —— 本报只收「免费能拿到的东西」，**人事变动既不产生额度、也不改变任何一家的免费政策**。登记在此只为说明：**本期窗口内新闻量最大的那条，恰好是与「免费」无关的那条。**

**⚠️ 这三条都不进第四章、也不进极速页。** 登记在这里是为了让读者知道「为什么它不在免费清单里」——**「当天最大的新闻」与「当天最该记的免费项」经常不是同一条**。

---
