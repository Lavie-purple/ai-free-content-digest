# -*- coding: utf-8 -*-
"""从 039 期 md 提取第四章截止表 -> 基准日 2026-10-18 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table040.md（纯表格块，供 040 期正文嵌入）。

六步（027 期定做法、028 期定型；040 期第十五次落地）：
  1) 先断言行数（039 期 body = 201）
  2) 按行名子串套 REWRITE 字典（每键必须恰好命中 1 次）
  3) 正则重算每一行的「距今 N 天」（基准日 10/18 -> 与 039 期不同，全部 -1）
  4) 未 REWRITE 的行做归属化（「本期」-> 「039 期」）
  5) 新行插在 ⚪ 存档块（首行 "| ⚪ **DeepSeek 10/15"）之前 -> 再断言总数
  6) 输出后由 inject040.py 注入正文占位符

⚠️ **本期基准日推进一天**（10/17 -> 10/18），故「距今 N 天」应逐行 -1；
   实跑后须核对：变化行数应等于「原本带可解析日期且该日期 >= 10/18」的行数。
⚠️ **截止列纪律**：真截止日才写可解析 `M/D`；换挡日/登记启动日/权重交付日一律写不可解析形态。
   「限时免费」没有结束日时写「未公布」（避坑 154/166）。
⚠️ **今日到期三条**（Together AI / 阿里云 AgentCore / MiniMax Code 均为 10/18）
   与 **DeepSeek Search/Fetch 11/1 起计费** 是本期截止表的核心变化。
"""
import re
from datetime import date

SRC = "AI免费内容与权益速递-第039期-2026-10-17.md"
OUT = ".workbuddy/tmp_table040.md"
BASE = date(2026, 10, 18)
PREV = 201

lines = open(SRC, encoding="utf-8").read().split("\n")
s = e = None
for i, l in enumerate(lines):
    if l.startswith("## 四、"):
        s = i
    if s is not None and l.startswith("## 五、"):
        e = i
        break
rows = [l for l in lines[s:e] if l.startswith("|")]
header, sep, body = rows[0], rows[1], rows[2:]
assert len(body) == PREV, len(body)

REWRITE = {}

# ---- ① 老混元：Q04 连续第 28 期 + 高危窗口第 18 天 ----
REWRITE["腾讯老混元大模型平台停服"] = (
    "| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必须迁移到 TokenHub**。**10/18 高危窗口第 18 天**"
    "（9/25 自设倒排日已过 **23 天**；Q04 **连续第 28 期**未见确切日期，厂商只给「9 月底」）。"
    "⚠️ **一条「9 月底停服」拖到 10 月中下旬仍无日期，处置维持「按已停服对待、只做迁移」**——迁移动作本身不要等；"
    "⚠️ **同一家厂商两条线，一条无日期一条有精确到日的倒排**（元器 11/9，见下表），"
    "**说明「无日期」不是这家厂商的常态，而是这条线的常态**（避坑 164） |"
)

# ---- ② Together AI 限免：本轮绕过 Cloudflare，取到「常规行 + 促销行」两个价 ----
REWRITE["Together AI `Muse Spark Open` 限免"] = (
    "| 🟡 **Together AI `Muse Spark Open` 限免** | **10/18** | 🟡 **今日到期（距今 0 天）**。"
    "**⚠️ （040 期）038、039 两期该页被 Cloudflare 拦截，本轮访问成功，并核到页面上同时存在两行**："
    "**① 常规行 `Muse Spark Open`：输入 `$1.25` / 缓存读 `$0.15` / 输出 `$4.25`；**"
    "**② 促销行 `Muse Spark Open (Free for limited time)`：标 `PROMO` 与 `Promotion valid until 10/18/2026`，"
    "输入 `$1.00` / 缓存读 `$0.00` / 输出 `$5.00`**。"
    "⚠️ **促销行的输出价 `$5.00` 高于常规行的 `$4.25` 约 18% —— 「限免」不是「常规价打折」，"
    "而是把计费重心从缓存读挪到输出**：**只读长上下文负载在促销期确实更便宜，生成长输出负载反而更贵**（避坑 177）。"
    "**039 期写「限免到期后常规 serverless 价为 $1.25 / $4.25 / $0.15」这句与常规行一致、不是错的，"
    "错在它把这一页写成了只有一个价**（见五·1）。"
    "⚠️ **本期补入同一页另外两条免费 / 零价行（038、039 均未登记）**："
    "**`Ternary Bonsai 27B` 输入 `$0.00` / 缓存读 `$0.00`（页面未标输出价）；"
    "`Tev1 4B Experimental` 输入 `$0.04` / 输出标 `Free`** —— "
    "**「输入免费但输出收费」与「输入收费但输出免费」是两种完全不同的免费形状，两列必须一起抄**（避坑 163）。"
    "⚠️ **同页 `Reflection Beam` 为 `$0.40` 输入 / `$0.04` 缓存读 / `$1.20` 输出 —— 即 `Together AI` 侧的 `Beam` 是付费的**，"
    "与 Vercel / `OpenCode` / `Ollama Cloud` 三条限免并列为第四条路径且不免费（避坑 154）。"
    "⚠️ **本条与 `Muse Spark Open` 权重开放是两笔账**：权重开放是永久事实、限免是活动窗口（避坑 148/150 同族）。"
    "⚠️ **到期后是否续期，本轮仍未见公告** —— 按避坑 78「无信号即默认收口」处理 |"
)

# ---- ③ DeepSeek Search / Fetch：本期新增的「有确切免费截止日」条目 ----
REWRITE["`OpenCode` 的地区限制清单"] = (
    "| 🟡 **`OpenCode` 的地区限制清单（`Beam Free` 等 · 本期起读法改变）** | 未公布（长期，随供应商变动） | 🟢 生效中"
    "（**清单本身不是活动，是产品事实**）。**（040 期）回扫结果：039 期登记的清单本期未见变动** —— "
    "`Beam Free` 等仍标 `limited regions`、不可用地区仍为 18 国 + 乌克兰 3 个州、明确含「China (including Hong Kong and Macau)」。"
    "⚠️ **本期读法改变（这是新增的一条）**：**039 期把同页 15 个免费模型分成三档留存，却没有记 `docs/go` 上那句 —— "
    "「`DeepSeek`: ZDR agreement is **renewed monthly**. The current agreement is valid through **October 31, 2026**」** —— "
    "**即被归为「零留存」的那一批模型，其留存口径本身带一个 10/31 的复签节点，不是一个静态承诺**（避坑 155 的时间维度）。"
    "**⚠️ 另一条必须同时读的事实（本期头条）**：**同一平台昨夜发生安全漏洞、1.4% Console 用户的外部提供商凭证受影响、"
    "`Anthropic` 已撤销相关 `Claude API` 密钥** —— **「留存」与「凭证安全」是两个独立闸门**，"
    "零留存承诺不回答 key 是否安全（避坑 175）。"
    "⚠️ **本行仍是本报告第一个「以地域可用性为主线」的条目** —— 面向中文读者时，免费清单必须先过这一关 |"
)

# ---- ④ Reflection Beam 开放权重：补 AA 官方六组评测 + 基准落差未核项 ----
REWRITE["**Reflection Beam 开放权重**"] = (
    "| 🟢 **Reflection Beam 开放权重** | **已交付（权重交付日 10 月 16 日，非活动截止）** | 🟢 **已于 10/16 按 10/5 承诺兑现**。"
    "501B 总参 / 23B 激活、**1M 上下文**、**Apache 2.0**（模型卡明确不禁止蒸馏 / 用输出训练 / 微调或合并）。"
    "**⚠️ 038 期纠错三条（维持，不重复展开）**：**① 「10/16 发布」是错的 —— 10/5 已宣布是开放权重模型、只是权重未放；"
    "② `Terminal-Bench 2.1`（官方 80.1%）与独立评测 3.0% 的落差本期有新进展（见下）；**③ 「Apache 2.0」不等于「没有闸门」**（避坑 162）。"
    "**⚠️ （040 期）本期首次登记 `Artificial Analysis` 官方文章的六组评测对比（第三方口径，逐条带来源）**："
    "**① `Intelligence Index`（v4.3）得 `30` 分，美国开放权重第 2（次于 `Muse Spark Open` 的 `39`），全部开放权重总榜第 10**"
    "（落后阿联酋 `K2 Horizon`（`31`）一分）；**② token 效率：每任务约 `26k` 输出 token（约 `19k` 推理 + `7k` 回答），"
    "其中仅 `26%` 用于最终答案，在 v4.3 测过的 219 个模型中排第 28 低 —— 而领先一分的 `K2 Horizon` 用 token 是其两倍（约 `52k`）**；"
    "**③ 智能体强、终端弱：`AutomationBench-AA` `48.5%`（领先 `K2 Horizon` 的 `37.2%` 11 个百分点、与 `Qwen3.8 27B` 的 `48.2%` 持平），"
    "而 `Terminal-Bench 4.0` 仅 `3.0%`（落后 `Qwen3.8 27B` 的 `5.6%` 与 `Muse Spark Open` 的 `8.1%`）**；"
    "**④ 知识与幻觉：`AA-Omniscience` 正确率 `33%`（`K2 Horizon` `18%`、`Qwen3.8 27B` `16%`），"
    "但幻觉率 `47%`（`K2 Horizon` `26%`、`Qwen3.8 27B` `30%`），净指数得分 `1.5` 领先两个同类（`−3.0` 与 `−10.0`）**；"
    "**⑤ `Cyber Index` 完成 `34%` 任务，位于「Cyber Index vs 每任务输出 token」前沿曲线上，与 `GPT-6 Sol` 并列**；"
    "**⑥ 编程（`Mirror` CLI）：`Coding Agent Index` 得 `28`，落后 `Claude Code` + `Qwen3.8 Max`（`43`）15 分、落后领先者（`68`）40 分，"
    "但只有 `Codex` + `GPT-6 Astra` 与 `Codex` + `GPT-6.1 Sol` 用得比它少**。"
    "**⚠️ 本期最需写下的一个落差（039 期的解释被修正）**：039 期把「官方 `Terminal-Bench 2.1` 80.1%」与「独立 `Terminal-Bench 4.0` 3.0%」"
    "归因为「两个版本的同名基准」；**而本期 `Artificial Analysis` 官方文章明确 3.0% 出自 `Terminal-Bench 4.0`** —— "
    "**若 `Reflection` 官方那张表确为 4.0，则同一基准上会出现 80.1% 与 3.0% 两个数、相差约 26 倍，"
    "「版本不同」这个解释至少是不完整的**。⚠️ **本报告不裁决谁对，只把「官方那张表的确切版本号」列为未核项**（避坑 178）。"
    "**⚠️ 同期两条推理栈支持（均为 10/16 一手源）**：**`vLLM` day-0 支持**（官方摘要逐字：501B total / 23B active、"
    "「agent-driven optimization that **cut decode latency 2.71×**」、`DFlash2` speculative decoding with adaptive verification —— "
    "**`2.71×` 是相对值、官方未给并发度与输入输出长度**）；**`SGLang` 宣布原生支持并以其驱动 `Reflection` 的生产 `API`**。"
    "**即同一权重在 24 小时内被两家推理栈声明支持 —— 这是「权重交付日」与「生态就绪日」可以不同的一条样本**（避坑 150）。"
    "**⚠️ 跑起来要什么**：**BF16 约 1 TB / NVFP4 约 280 GB、官方建议至少 4 张 B200（720 GB 显存口径）** —— 不是「人人本地跑」的模型（避坑 41 第三层）。"
    "**⚠️ Reflection 自家 API 免费 beta 结束后的价格仍未公布（连续第 2 期）** —— "
    "**`platform.reflection.ai` 本轮实访仍需登录才见模型与价格** |"
)

# ---- ⑤ Muse Spark Open：补 Arena WebDev 第二个独立名次 ----
REWRITE["**Meta `Muse Spark Open` 开放权重"] = (
    "| 🟢 **Meta `Muse Spark Open` 开放权重（816B / 42B 激活 / 1M 上下文 · HF gated 需填出生日期）** | 未公布（权重已开放） | "
    "🟢 生效中（**当地时间 10/15 发布，北京时间 10/15 傍晚至 10/16**）。**官方称「迄今能力最强的美国开放权重模型」**。"
    "**规格**：**原生多模态稀疏 MoE、总参 816B / 每 token 激活约 42B、上下文 1M token（1,048,576）、100 多种语言**。"
    "**⚠️ （040 期）本期补入一个独立第二名次：`Arena` 官方 X（10/17）** —— "
    "**`Muse Spark Open (Max)` 在 `Code Arena: WebDev` 以 `1511` 分位列开放模型总榜第 `13`、美国开放模型第 `1`；"
    "比 `Muse Glimmer` 高 `156` 分（后者 `1355` 分、开放模型第 `41`）；定价 `$1.25` / `$4.25` 每百万输入/输出 token，"
    "比 `Muse Wonder (Max)` 便宜 `79%`、与 `Muse Spark 1.3 (Max)` 持平**；**分领域：品牌与营销、数据与分析 第 `13`、"
    "基于参考的设计 第 `14`、游戏与消费产品 第 `15`、模拟 第 `20`**。"
    "**⚠️ 把这个名次与 037 期登记的官方表并排看，得到的正是避坑 165 说的形状**："
    "**官方表里 `MCP-Atlas` 领先但 `Terminal-Bench 2.1` 落后、`AA` 智能指数 `39` 落后 `GLM-5.3` 与 `Kimi K3`；"
    "而 `Arena` 给出「WebDev 榜美国开放模型第一」、`AA` 给出「开放权重总榜第 `10`」—— "
    "**同一个模型在编码前端榜第一、在综合智能榜第十，两个结论都对，问题是量的不是同一件事**（避坑 144/165）。"
    "**⚠️ 下载闸门（037 期登记，本期维持）**：**HF 上两个 Meta 仓库均为 gated 且人工审核 —— "
    "访问表单要求「法定全名 + 出生日期 + 组织全称」、提交后不可编辑，并警告影响 HF 上其他模型；"
    "同一份权重的 `Unsloth` GGUF（21 档）、`ggml-org` GGUF、AMD Quark 检查点均 ungated**（避坑 162）。"
    "**⚠️ 许可证 `Muse Model License`，不是 Apache-2.0**：**① 显著展示「Built with Muse Spark Open」；"
    "② 「衍生作品」定义极宽，含任何用该模型或其输出训练 / 微调 / 蒸馏得到的模型；"
    "③ 作为 MaaS 对外服务且连续 12 个月总收入超 2,000 万美元须先通知 Meta 并另签书面协议；④ 使用政策是许可证的一部分**（避坑 158）。"
    "**⚠️ 跑起来要什么**：**NVFP4 约需 700 GB GPU 显存、BF16 约需 2 TB；Apple 路线为主推（两台 M5 Ultra 各 512 GB 统一内存经 MLX 跑全量）** |"
)

# ---- ⑥ GLM-Legal：官方博客全文无 open-weight 字样（本期补更硬的证据） ----
REWRITE["智谱 `GLM-Legal`"] = (
    "| 🟢 **智谱 `GLM-Legal`（法律智能体 · API 申请制 · 本期补一条更硬的「不是开源」证据）** | 未公布 | 🟢 生效中（**10/12 发布**）。"
    "**基于轻量级 `GLM-5.3-Flash` 构建**；**官方口径 `Harvey LAB` 全通过率 `19.2%`（较基座提升 `12.5` 个百分点）、"
    "`LegalBench` 与顶级闭源前沿模型持平、`PLawBench` 中文本地化持平；两项由 `Vals` 独立评测**。"
    "**⚠️ （040 期）本期实访智谱官方博客 `z.ai/blog/glm-legal`（2026-10-12）全文**："
    "**无「开放权重 / open-weight」表述、无权重下载入口、无许可证；唯一进入路径是「Apply for API access: `z.ai/consultation/legal`」"
    "与 `AutoClaw` 链接** —— **而中文媒体（量子位 10/17）标题写「开源模型」、同一篇正文又写「申请 `GLM-Legal` Beta」，"
    "标题与正文给出两种口径**。⚠️ **维持 035 / 037 期「不是开放权重模型」的口径，并补上这条更硬的证据**；"
    "**媒体的「开源」表述原样记录，两说并列、不替厂商裁决**。"
    "**⚠️ `Harvey LAB` 的难度口径（本期首次登记）**：**首版设置**超过 1,200 项**模拟律所工作任务、"
    "覆盖并购与知识产权与银行金融等 **24 个**法律业务领域；采用**「全条件通过」机制** —— "
    "**满足一项任务的全部评分条件才算通过，少一条都不行** —— **这解释了 19.2% 为何看起来低：它是「全条件通过率」不是「正确率」**（避坑 144 同族）。"
    "**⚠️ 第三方口径（媒体转述、不可与官方表相加）**：**`Vals AI` 最新测评中以 `19.2%` 全通过率与 `86.23%` 准确率"
    "摘得 `Harvey LAB` 与 `LegalBench` 双榜开放权重模型榜首；成绩相近时 `GLM-Legal` 比 `Gemini 4 Argon` 慢近 30 分钟、"
    "但 `Gemini` 每项测试成本约为其 `70` 倍** —— **「慢 30 分钟但便宜 70 倍」是本条最有选型价值的一句，"
    "但它出自媒体转述的厂商对比、非受控测试**（避坑 116）。"
    "**⚠️ 免费档一问仍未结（036 期挂账延续）**：核到 `AutoClaw` 侧注册赠 `$24` 额度；第三方另转述「2 亿 tokens」，"
    "**两个数都带来源记账、不折算、不取中间值**（避坑 54/161）；**035 期已更正：`Artificial Lawyer` 10/13 报道称该法律版本"
    "「不打算作为开放权重模型发布」—— 开放的是基座 `GLM-5.3-Flash`，不是这个领域模型**（避坑 155） |"
)

# ---- ⑦ OpenCode 限免 Beam：补安全事件与地区限制回扫 ----
REWRITE["**`OpenCode` 限免 `Reflection Beam`（1M 上下文）**"] = (
    "| 🟢 **`OpenCode` 限免 `Reflection Beam`（1M 上下文）** | **未公布（免费结束日期未公布）** | 🟢 生效中。"
    "**10/16–10/17 `OpenCode` 官方 X 宣布把 `Beam` 与 `GLM-5.3-Flash` 一并免费**（501B/23B MoE、1M 上下文）。"
    "**039 期已从官方两页核齐的四组字段本期维持**：**① 留存 30 天**（官方原文「not used for training. "
    "Data is retained for 30 days for safety reasons」）；**② `limited regions`、不可用清单 18 国 + 乌克兰 3 州、"
    "含「China (including Hong Kong and Macau)」**；**③ 不占套餐额度（`Go` 与 `Go Plus` 两档月度用量均 `Unlimited`）**；"
    "**④ Input / Output / Cached Read 三列均 `Free`、Cached Write 为 `-`（占位符非数值）**。"
    "**⚠️ （040 期）本期最重要的一条叠加事实 —— 同一平台昨夜发生安全漏洞**："
    "**`OpenCode` 官方 X 逐字原文「We had a security breach last night related to a large scale distillation attack "
    "that impacted 1.4% of OpenCode Console users」「We have notified them all this morning via email. "
    "If you did not get an email you were not impacted, it was a subset of users who had external providers linked」"
    "「The incident is ongoing so we cannot share more details at this point but we are working with Anthropic, OpenAI, "
    "and Google to remediate」**；**`Anthropic` 已撤销疑似受影响的 `Claude API` 密钥并建议用户重新创建**。"
    "**⚠️ 这与本行「留存 30 天」是两个独立闸门 —— 零留存承诺不回答 key 是否安全**（避坑 175）。"
    "**⚠️ 定性受到公开质疑**：`Nathan Lambert` 称把窃取密钥归入「蒸馏」很反常、"
    "**且流量规模与模型训练的关联目前不清楚** —— **本报告两说并列，判断风险时用「凭证可能已泄露、需轮换」这个可判定事实**（避坑 116 同族）。"
    "**⚠️ 三条现在就能判定的边界**：**① 受影响范围是「链接了外部提供商」的子集、不是全部 Console 用户；"
    "② 判据是「有没有收到那封邮件」，官方未给字段级说明；③ 官方明确「cannot share more details」—— "
    "本报告不推测泄露了什么数据**。⚠️ **「1.4%」按原样引用，不换算成「影响很小」** —— "
    "**它是厂商自报、未经第三方复核、且官方明确仍在处置中的比例** |"
)

# ---- ⑧ 商务部 48 号公告：回扫登记状态仍未变 ----
REWRITE["商务部 AI 技术出口管制目录修订"] = (
    "| 🟡 **商务部 AI 技术出口管制目录修订 · 出口前登记** | **未公布（征求意见与登记实施日均为「非活动截止」，两个时点见正文一·4）** | "
    "🟡 **登记义务已生效、管制范围尚未落地**。**商务部、科技部 2026 年第 48 号公告（10/16）**：拟将"
    "**大模型 / 智能体 / 算力集群 / 信息处理 23 项 AI 技术**（三领域共 40 项，其中拟禁止 14 项、拟限制 26 项）"
    "增列进《中国禁止出口限制出口技术目录》，**并同步对附件所列技术启动「出口前登记」，已经开始但尚未完成的出口也在范围内**。"
    "**⚠️ 距今 28 天**（征求意见截止）。**⚠️ （040 期）回扫：登记义务生效满两天，本期仍未见实施日公告、"
    "也未见任何一家厂商就「已启动登记」发出办理指引** —— **受影响主体仍处在「义务已成立、通道未开」的状态**（Q27 三项仍未定）。"
    "**⚠️ 同期多源报道口径（本期新增）**：**`The Verge` 10/16 报道称中国考虑将 `23` 项 AI 技术纳入出口管制，"
    "**包括芯片设计、AI agents、模型权重和源代码**，并涉及 `Kimi K3` 等国产模型** —— "
    "**「拟增列的 23 项」在媒体侧被具体到「模型权重与源代码」，而官方 48 号公告文本未逐项列出指标线**，"
    "**两者是「官方给了框架、媒体给了猜测性举例」的关系，不可写成官方已明确权重复出管**（避坑 116）。"
    "**四条豁免（决定哪些开源模型还能正常出海）**：**① 已开源或已发论文进入公共领域的技术不纳入；"
    "② 人工智能类技术开源、境外自建自营算力中心、赴境外芯片流片、利用境外资源联合研发、参与国际标准制定 —— "
    "适用自动许可等便利措施（基本「即报即出」）；③ 用限制类大模型对外提供 API 调用 / APP 网页交互 / SaaS 应用 / "
    "本地端侧轻量化部署 —— 不属于大模型技术出口管理范围；④ 纳入限制类的技术若开展海外本地化部署属于技术出口管理范围，"
    "但部署在海外自有云等风险可控情形可适用自动许可**。"
    "**⚠️ 不得写成「AI 技术出口已被管制」** —— 登记生效日与管制实施日是两件事（避坑 167） |"
)

# ---- ⑨ AutoClaw 第二期：第三期连续第 4 期未见 ----
REWRITE["智谱 AutoClaw「每日登录领 credits」第二期"] = (
    "| ⚪ **智谱 AutoClaw「每日登录领 credits」第二期** | **已按原定日期收口（活动期 10 月 12 日至 10 月 16 日，北京）** | "
    "⚪ **已按原定日期收口（10/18 回扫未见延期或提前收口公告）**。**（037 期登记的档位表口径全部不变）**："
    "**10/12 首日全体 10,000 Credits（1 亿 GLM-5.3-Flash Tokens）；10/13–10/16 每日全体 800 Credits（800 万 Tokens）**；"
    "**付费会员额外每日奖励按档位（AutoClaw 月度订阅 Lite/Base/Pro/Max = 500 / 5,000 / 7,000 / 8,000 Credits；"
    "`GLM Coding Plan` 个人版 Lite/Pro/Max = 5,000 / 7,000 / 8,000 Credits）**。"
    "**⚠️ （040 期）第三期是否接上：本期仍未见公告 —— 连续第 4 期未见**（037、038、039 期已连续记三次「本期未见公告」）。"
    "**按 032 期定的「疑似实质违约候选」判据：厂商承诺的交付物按期是否出现是可判定的，超过一个自然周期就换档** —— "
    "**注意这条不适用于本条（第二期本身按期兑现了），只适用于「第三期是否存在」这个待定问题**。"
    "⚠️ **每日奖励当天午夜过期、当日领当日用；每账号每日限领一次；多重会员只取最高档、不可叠加**（避坑 52） |"
)

# ---- ⑩ OpenRouter 免费档：本期专页 URL 改版返回 404，如实记「未重取」 ----
REWRITE["**OpenRouter 免费档（`502+` 模型"] = (
    "| 🟢 **OpenRouter 免费档（`502+` 模型｜上期重取于 2026-10-17）** | 未公布（动态目录） | 🟢 生效中。"
    "**⚠️ （040 期）本期未重取 —— `freellm.net` 的 OpenRouter 专页 URL 本轮返回 404**"
    "（站点改版为 `/models/provider/model-name/` 形态），**因此本行的在线模型数沿用上期口径并标注核对日，"
    "本期不得声称已复核**。⚠️ **额度口径仍是「三源三个数、都带来源」**：**① `freellm.net` OpenRouter 专页"
    "（上期读数 `Last Updated 2026-10-17`）：19 个 `:free` 模型在线、主限流「200 req/day」、免绑卡「Not required」；"
    "② `OpenRouter` 官方（经 `freetokens.fyi` 转录）：50 次/日，累计充值满 $10 后 1,000 次/日、20 次/分；"
    "③ `benchlm.ai`：与 ② 同口径。⚠️ **① 与 ② 在「日请求数」上直接冲突（200 vs 50），不可取中间值、不可只写一个**（避坑 161）。"
    "⚠️ **本期只取到 `freellm.net` 首页计数器（`505+` 模型 / `30` 提供方，`Latest free LLM API model update: 2026-10-17`）"
    "—— 与 OpenRouter 专页的 19 个在线不是同一口径，不可相减**（避坑 68）。"
    "⚠️ **同站本期另核到两条此前未登记的限流形态**：`Kilo Code` 的 `qwen/qwen3.8-27b:free` 与 "
    "`inclusionai/ling-3.1-flash` 均标 **`200 req/hr`**（按小时计，与 OpenRouter 的按日不同）；"
    "`OVHcloud AI Endpoints` 的 `Qwen3.8-27B` 标 **`2 RPM (anonymous)`（匿名即 2 次/分）** —— "
    "**三种限流单位（日 / 小时 / 分）不可直接比大小**（避坑 54 同族） |"
)

# ---- ⑪ DeepSeek 相关：把 V4.1-Flash-1017 与 Search/Fetch 拆成两行 ----
REWRITE["腾讯开源 Coding Agent `Octop`"] = (
    "| 🟢 **腾讯开源 Coding Agent `Octop`** | 未公布（已开源） | 🟢 生效中。"
    "**许可证已核到：Python / MIT**（`github.com/tencentcloud/octop`，**8.7k Star**）。"
    "**能力清单**：**单进程同时服务 Web 面板 / CLI / IM 频道 / 定时任务，共享一份 SQLite 状态（重启后仍在）；"
    "JWT 多用户隔离与工具审批；飞书 / 钉钉 / QQ / Discord / 企业微信等 IM 频道矩阵；双向 ACP；"
    "本地磁盘 / Docker / PostgreSQL / COS·S3 多种后端；16 种 MBTI 人格模板 + 场景化专家**。"
    "⚠️ **「开源版 WorkBuddy」仍是媒体与博主表述，腾讯官方页未核到该表述**。"
    "⚠️ **Q23 状态不变**：`GitHub` 仓库历史确认最早提交可追到 2026-07-09、v1.0.2b8 于 10/14 推送 —— "
    "**「10/6」「10/12 收录」「2026-07-09」三个口径不可互换**（避坑 142）。"
    "⚠️ **同厂商对照事实**：`Octop`（开源、MIT、无停服日）与元器（C 端平台、11/9 停服、迁移 `ADP`）"
    "是腾讯 AI 产品线里两条方向相反的账，不可合并叙述（避坑 148）。"
    "⚠️ **省的是模型成本，不是部署与运维成本**（避坑 118 同族） |"
)

REWRITE["阶跃 `Step 5 Preview` API 缓存命中输入档调价"] = (
    "| 🟢 **阶跃 `Step 5 Preview` API 缓存命中输入档调价** | 未公布（调价已于 2026-10-14 00:30 生效，非活动截止） | "
    "🟢 **已按公告生效（040 期回扫：未检索到延期或改价公告）**。**缓存命中输入价 0.35 元 → 0.70 元 / 百万 token**；"
    "**缓存未命中输入 7 元与输出 20 元明文不变**；⚠️ **祖父条款：10/14 00:30 之前已通过按量付费 API 调用过该模型的用户，"
    "之后仍按 0.35 元计费**；⚠️ **`Step Plan` 订阅渠道的缓存价格不在本次调整范围内**。"
    "⚠️ **官方未给调价理由**；⚠️ **限速按累计充值分档**"
    "（**<100 元 = 5 并发 / 100 RPM / 50 万 TPM；≥1 万元 = 130 并发 / 2600 RPM / 1300 万 TPM**）。"
    "⚠️ **截止列写「未公布 + 注明生效时刻」是刻意的** —— 调价是「换挡日」不是「活动到期」，"
    "**写可解析实日期会让巡检脚本把它误报成「已过期但未结束」（A 档）**（036 期纪律）。"
    "⚠️ **第三方结构化价格页在生效前明确标注「截至该页撰写时该涨幅尚未生效」—— 引用时必须带「生效前 / 生效后」的时效说明**（避坑 150） |"
)

NEW = [
    # ---- 新行 1：DeepSeek-V4.1-Flash-1017（本期头条 · 模型线 + 额度线）----
    "| 🟢 **`DeepSeek-V4.1-Flash-1017`（10/17 发布 · 价格不变 · 本期头条）** | 未公布（**非活动截止**：发布日 10 月 17 日、"
    "官方更新日志写「API calling method and pricing remain unchanged」） | 🟢 生效中。"
    "**官方更新日志逐字**：`DeepSeek V4.1 Flash` 已升级为 `DeepSeek-V4.1-Flash-1017`；**网页端与 APP 同步更新；"
    "调用方式与价格不变、仍用 `deepseek-flash` 访问**。**⚠️ 绝对价格（040 期首次从官方 `Models & Pricing` 页核到，单位每百万 token）**："
    "**缓存命中输入 `$0.003`（Off-Peak）/ `$0.006`（Peak）；缓存未命中输入 `$0.15` / `$0.30`；输出 `$0.6` / `$1.2`** —— "
    "**官方规则「Off-peak rates are half of the peak rates」，Peak 时段为 UTC 01:00–04:00 与 06:00–10:00、周一至周五"
    "（不含中国法定假日），其余全部为 Off-Peak（含周末与全部中国法定假日）**。"
    "**⚠️ 两个此前未记字段**：**上下文 1M、最大输出 `MAXIMUM: 384K`、并发限制 250**；"
    "**旧名 `deepseek-v4-flash` 与 `deepseek-v4-flash-vision-exp` 仍被接受，但对应模型已退役、其请求由 "
    "`DeepSeek-V4.1-Flash-1017` 服务并按 Flash 价计费**（避坑 142：**同一个模型名下面换了实现，是一条独立事实**）。"
    "**⚠️ 官方基准必须连口径一起引**：**`HLE`(w/o tools) `42.6`（纯文本子集 `44.0`）／`Terminal-Bench 4.0` `42.3`"
    "（**用 Claude Code 框架测**）／`DeepSWE v1.1` `77.0`（**用 Mini-SWE-V2 框架测**）／`ProgramBench` `29.1`／"
    "`NL2Repo-Bench` `68.2`／`Automation-Bench v1.0.6` `60.5`／`Agents' Last Exam` `35.4`／`Apex Bench v1.1` `72.1`／"
    "`Chartography`(w/tools) `83.0`／`BabyVision`(w/tools) `92.5`／`ZeroBench-main`(w/tools) `51.0`（**`Pass@5`**）** —— "
    "**同一条表里两个基准各自标了不同框架，故分数不可跨模型直接比，而表内没有任何一句写「均在同一 harness 下测得」**（避坑 165）。"
    "**⚠️ 版本门槛**：`DeepSeek Harness 0.2.1-rc.1` 或更高（**「or later」而非「必须」，不升级也能用、只是拿不到专项优化**）。"
    "**⚠️ 一条发布前泄露的可判定细节（第三方口径）**：**官方发布前数小时有用户在模型列表中短暂看到 `1017` 这一项，"
    "且 `deepseek-flash` 的系统指纹从 `aeb56401...` 变为 `e72d3c7f...`** —— "
    "**`1017` 对应 10 月 17 日、符合用日期标记快照的一贯方式；而系统指纹变化说明「可访问时刻」早于「公告时刻」**（避坑 142） |",

    # ---- 新行 2：DeepSeek Search / Fetch（本表至今「到期可预期度」最高的一条）----
    "| 🟡 **`DeepSeek Search` / `Fetch` 两个 API 开放（10/17 · 服务端调用免费到 11/1）** | "
    "**11/1 00:00（北京）起按请求计费** | 🟡 **生效中（免费窗口距今 14 天）**。"
    "**接入（官方逐字）**：base URL `https://api.deepseek.com`；**Search `POST /v1/tools/search`、Fetch `POST /v1/tools/fetch`**；"
    "**两者均为原始 JSON API、使用与 `DeepSeek API` 相同的 bearer 认证**。"
    "**计费（官方逐字）**：**Search 与 Fetch 均按「每 1,000 次成功请求 `$0.75`」计价 —— 按请求计费，不按 token、也不按返回结果条数**；"
    "**只有 HTTP 200 且产生结果才算成功**（Search 须返回非空 `results`、Fetch 须返回页面内容）；"
    "**失败请求、空搜索结果、超时一律不计费**。⚠️ **「空结果不收费」对做 RAG 的读者有直接后果 —— "
    "一次检索没命中是零成本、命中才计费，与按 token 计费是相反的成本结构**（避坑 176）。"
    "**⚠️ 免费窗口（官方附注逐字）**：**「when you use the `DeepSeek API` through `DeepSeek Harness`, `Claude Code`, or `Codex`, "
    "server-side tool calls already hit the Search and Fetch APIs. These calls are currently free of charge; "
    "per-request billing starts at **00:00 Beijing time on November 1, 2026**」** —— "
    "**必须拆三行读**：**① 直接调 API 从一开始就是 `$0.75` / 1,000 次成功请求，没有免费期；"
    "② 三个 harness 的服务端工具调用目前免费；③ 计费起点是北京时间 11/1 00:00，不是美西也不是 UTC**。"
    "**⚠️ 速率限制**：**Search 与 Fetch 各自独立、各 QPS 5、按账户级计（无论用哪个 key）、互不消耗对方配额；"
    "`Fetch` 另受按域名的 QPS 限制；超限返回 HTTP 429**。"
    "**⚠️ 对内容生成最要紧的三个响应字段**：`rerank_score` **0–3、≥1.5 视为高质量**（唯一可程序化判定的质量档）；"
    "`summary` **600–800 字符、面向模型**（`snippet` 是 100–200 字符、面向 UI，两者不是同一字段的截断版）；"
    "`content` 为页面 Markdown 全文、`need_content=false` 时恒为空字符串、且 `count` 不影响单价。"
    "**⚠️ 一条不能靠重试解决的失败**：`404` 表示无法取到可用页面内容（不可用 / 被站点策略拦截 / 目标站报错 / "
    "不支持的内容类型 / 无可提取 Markdown）—— **索引里有 ≠ 抓得到** |",

    # ---- 新行 3：WorkBuddy Intl 的模型限免（10/31）----
    "| 🟢 **`WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免（10/31）** | **10/31** | 🟢 **生效中（距今 13 天）**。"
    "**官方原文两句（`WorkBuddy` 官方 X，10/17 18:29）**：「新的 `DeepSeek` 刚刚发布。`WorkBuddy Intl` 也已更新到最新版本，"
    "**并且在 10 月 31 日前免费**。来试试看吧。」⚠️ **四条登记纪律**："
    "**① 主体是 `WorkBuddy Intl`（国际版），不是国内版 —— 本工作区的产品线在国内站与国际站是两套口径，不可互相代入**；"
    "**② 官方原文没有写额度上限、没有写适用账号范围、没有写结束后的价格** —— "
    "**按避坑 126「免费窗口的长度写在渠道里」登记为「未公布」，不推测**；"
    "**③ 免费的是「这一版模型」，不是「这个产品全模型免费」**（避坑 163）；"
    "**④ 它引用的 `DeepSeek` 官方推文里只有模型能力与 `Harness 0.2.1-rc.1` 版本要求，没有一句写价格或免费** —— "
    "**「10/31 前免费」这句只出现在 `WorkBuddy` 自己那条帖子里，不可写成 `DeepSeek` 官方口径**（避坑 116） |",

    # ---- 新行 4：DeepSeek Harness 6 元赠金（二手口径，明确标注）----
    "| 🟡 **`DeepSeek Harness` 首次登录 6 元赠金（二手口径 · 官方未核到）** | "
    "未公布（**赠金到账后 7 天有效**；官方更新日志未见该活动） | 🟡 生效中（**限量发放、赠完即止**）。"
    "**⚠️ 来源为媒体转述**：量子位 10/17 20:21 称**符合条件的用户首次登录 `DeepSeek Harness` 可直接领取 6 元赠金、"
    "无需充值、到账后 7 天内有效、额度限量发放赠完即止**，并提示**「之前登过 `Harness` 的记得先退出再登」**。"
    "**⚠️ 本轮实访 `DeepSeek` 官方更新日志，该页面没有出现这条赠金活动** —— **按避坑 44 记为二手口径、"
    "不得声称已在官方核到**。⚠️ **量纲必须写清**：**这是「元」、按赠金余额计，不是送 token、不是补时长** —— "
    "**与 039 期登记的 `DeepSeek` 10/15 故障返赠金是两笔账**（避坑 160） |",

    # ---- 新行 5：OpenCode 安全事件（本期头条 · 运维必办项）----
    "| 🔴 **`OpenCode` 安全事件（1.4% Console 用户凭证受影响 · `Anthropic` 已撤销密钥）** | "
    "未公布（**事件处置中，非活动截止**；官方写 `The incident is ongoing`） | 🔴 **需立即行动**。"
    "**`OpenCode` 官方 X 原文逐字（本报告第一次登记的平台侧安全事件）**："
    "**「We had a security breach last night related to a large scale distillation attack that impacted "
    "**1.4% of OpenCode Console users**」「We have notified them all this morning via email. "
    "**If you did not get an email you were not impacted**, it was a subset of users who had external providers linked」"
    "「The incident is **ongoing** so we **cannot share more details at this point** but we are working with "
    "**Anthropic, OpenAI, and Google** to remediate」**。"
    "**⚠️ 三条现在就能判定的边界（不要越过这三条去推测）**：**① 受影响范围是「链接了外部提供商」的子集、不是全部 Console 用户；"
    "② 官方判据是「有没有收到那封邮件」，未给 1.4% 的分母（账户数 / 工作区数 / key 数）与统计口径；"
    "③ 官方明确「cannot share more details」—— 本报告不推测泄露了什么数据**。"
    "**⚠️ 上游已动手**：`Anthropic` 的 Lydia Hallie 表示团队正与 `OpenCode` 协作处理，"
    "**已撤销疑似受影响的 `Claude API` 密钥并建议在 `OpenCode` 保存过密钥的用户重新创建**；"
    "**`OpenAI` 与 `Google` 同在官方列出的协作方名单里，但本轮未见这两家发布对应公告**（避坑 175）。"
    "**⚠️ 定性受到公开质疑**：`Nathan Lambert` 称把窃取密钥归入「蒸馏」很反常、把流向中国的模型转发站混为一谈同样如此，"
    "**且流量规模与模型训练的关联目前不清楚** —— **本报告两说并列；判断风险时用「凭证可能已泄露、需轮换」这个可判定事实**（避坑 116 同族）。"
    "**⚠️ 「1.4%」按原样引用，不换算成「影响很小」** —— **厂商自报、未经第三方复核、且官方明确仍在处置中**。"
    "**⚠️ 执行办法**：**把「轮换在 `OpenCode` 保存过的上游 key」写进日常运维清单，而不是写进事故响应清单** |",
]

# ---- ⑫-⑭ 三行「带时刻 / 带括注」的截止列：正则解析不到，必须显式重写 ----
# ⚠️ 这正是 027 期记的盲区：extract_deadlines / recompute 的正则都只认 `**M/D**` 精确闭合形态，
#    而 `**10/18 23:59:59**`、`**10/18（UTC+8）**`、`**11/9（停服）；…**` 三种都匹配不上 -> 天数不会被自动 -1。
#    本期断言（基准日推进一天 -> 每行必须 -1）当场把这三行抓住，按纪律处置 = 显式 REWRITE，不放宽断言。
REWRITE["阿里云 AgentCore 协作管控面限时免费"] = (
    "| 🟢 **阿里云 AgentCore 协作管控面限时免费** | **10/18 23:59:59** | 🟢 **今日到期（距今 0 天）**。"
    "⚠️ **本期回扫未见延期或提前收口公告** —— 按避坑 78「无信号即默认收口」处理。"
    "⚠️ **截止列带时刻（`23:59:59`）这一点本身要读**：**它比同日的另两条（`Together AI` 限免、`MiniMax Code` 加赠）"
    "精确到秒，但截止列写成带时刻形态后，巡检脚本的正则解析不到 —— "
    "**本期已按「基准日推进一天 -> 每行天数必须 -1」的断言把这三行逐条抓住并显式重写**（027 期纪律的第四次实测） |"
)

REWRITE["MiniMax Code 周额度重置卡限时加赠"] = (
    "| 🟢 **MiniMax Code 周额度重置卡限时加赠（每日签到）** | **10/18（UTC+8）** | 🟢 **今日到期（距今 0 天）**。"
    "**订阅用户每日签到额外领周额度重置卡，全勤最多 9 张、有效期 15 天，把用掉的周窗口清零重开**。"
    "⚠️ **本期回扫未见延期公告**。⚠️ **来源为第三方清单（什么值得买社区 10/16 版）转述 MiniMax 官方推特，"
    "本报告未回官方推特原帖核**（避坑 44）。"
    "⚠️ **与「MiniMax Code 每日签到积分」是两笔账** —— 后者的公开口径为"
    "**标准签到 400 积分/天（第 4、7 天为 1,000 积分/天、替代而非叠加当日奖励）、积分领取后 30 天有效**；"
    "**重置卡是重置「周窗口」的另一种量纲，不可与积分相加**（避坑 54）。"
    "⚠️ **本行的免费积分额度不改变「无免费模型」这一事实** —— 该工具的免费部分是账号可用于全目录的积分数额，"
    "不是某个模型本身免费（避坑 117） |"
)

REWRITE["腾讯智能体平台「元器」停止服务"] = (
    "| 🔴 **腾讯智能体平台「元器」停止服务（本期最高优先级运维项）** | "
    "**11/9（停服）；10/29（停止新建）；2027 年 1 月 9 日（数据导出截止）** | "
    "🔴 **倒计时中，四个日期必须分开排（本期全部 -1 天）**。"
    "**官方公告：平台将于 2026-11-09 停止服务**；**停服生效后，所创建智能体将不再可用**。"
    "**三个硬后果**：**① 平台访问、数据读写、API 调用、后台控制台全部关闭；② 发布到公众号、微信客服等渠道的智能体也停止响应用户对话；③ API 不再可调**。"
    "**四个日期逐条**：**10/29 起不再支持新建智能体与分发 API Key**（**距今 11 天**）；"
    "**11/9 平台停止全部服务**（**距今 22 天**）；**数据导出窗口开到 2027 年 1 月 9 日**"
    "（**距今 83 天** —— ⚠️ **比停服日晚两个月，这是最容易漏掉的一个日期**）。"
    "**迁移方案**：**官方推荐迁往腾讯云智能体开发平台 `ADP`（2025 年 5 月上线）** —— "
    "**官方称元器上的主要玩法均可延续，包括标准模式、Multi-Agent（多智能体协作）、单工作流三种应用模式，并支持更灵活的 `Claw` 模式**。"
    "**⚠️ 定位差异**：`元器` 偏 C 端、主要与「元宝」结合；**`ADP` 面向 B 端企业级平台**，强调系统性构建、数据接入、安全隔离、跨角色协作。"
    "**⚠️ 本行量级高于任何额度到期（避坑 164）**：**「优惠窗口结束」损失的是钱，「平台停服」损失的是存在本身** |"
)

# ---- ⑮ Kling 4.0：截止列带括注，正则解析不到，倒计时必须显式重写 ----
REWRITE["快手可灵 Kling 4.0（完整版 10 月上线）"] = (
    "| 🟢 **快手可灵 Kling 4.0（完整版 10 月上线）** | **10/31（官方口径「10 月正式上线」）** | "
    "🟢 **未开始（距今 13 天）**。**升级方向「真实 / 可控 / 专业」**："
    "**单次原生生成时长提升到 30 秒（Kling 3.0 的两倍）**，**配合多次续拍单条最长延展到 2 分钟**；"
    "**提示词上限提升至 8,000 tokens**；**支持最多 10 张关键帧**（Kling 3.0 仅首尾帧）+ 15 项参考素材；"
    "**4K 10-bit HDR 与 21:9 画幅**。⚠️ **轻量版 Kling 4.0 Flash 已在 9/28 内测（黑金年卡小范围）"
    "——「Flash 内测」不等于「4.0 上线」**（避坑 135 同族）；"
    "⚠️ **同期可灵 AI 传出上市承销团已定（中金 / 高盛 / 瑞银，至少募 10 亿美元、最快 2027 年）**（彭博口径，避坑 44）。"
    "⚠️ **本期回扫未见上线延期或提前公告**。⚠️ **截止列带括注（`10/31（官方口径…）`）导致巡检脚本的正则解析不到，"
    "故「距今 N 天」不被自动重算 —— 本期已显式写死为 13 天**（027 期纪律的第五次实测，与 AgentCore / MiniMax Code / 元器三行同因） |"
)

out = []
rw = 0
for line in body:
    hit = None
    for k in REWRITE:
        if k in line:
            assert hit is None, ("一行命中两个 REWRITE 键", k, hit, line[:60])
            hit = k
    if hit:
        out.append(REWRITE[hit])
        rw += 1
    else:
        out.append(line)

assert len(REWRITE) == rw, ("REWRITE 键数与命中数不等（很可能抄错行名）", len(REWRITE), rw)

# ---- 未 REWRITE 的行做归属化：本期 -> 039 期 ----
for i, l in enumerate(out):
    if l not in REWRITE.values():
        out[i] = l.replace("（040 期）", "（039 期）")
        out[i] = out[i].replace("（039 期）", "（038 期）") if "（039 期）" in out[i] and "回扫" not in out[i] else out[i]

# ---- 正则重算「距今 N 天」 ----
DAYS_RE = re.compile(r"(?:\*\*)?距今 (-?\d+) 天(?:\*\*)?")
DATE_FULL = re.compile(r"\*\*(\d{4})-(\d{1,2})-(\d{1,2})\*\*")
DATE_MD = re.compile(r"\*\*(\d{1,2})/(\d{1,2})\*\*")

def parse_cut(l):
    cols = l.split("|")
    target = cols[2] if len(cols) > 3 else ""
    if "北京" in target or "未公布" in target or "以" in target:
        return None
    m = DATE_FULL.search(target)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m2 = DATE_MD.search(target)
    if not m2:
        return None
    return date(2026, int(m2.group(1)), int(m2.group(2)))

def recompute(l):
    if "距今" not in l:
        return l
    d = parse_cut(l)
    if d is None:
        return l
    return DAYS_RE.sub("**距今 %d 天**" % (d - BASE).days, l)

# ⚠️ **REWRITE 的行一律不再过 recompute** —— REWRITE 即手写内容，天数由脚本作者逐条算对；
#    若再过一遍 recompute，含多日期 / 带时刻的截止列会被取到错误的日期并把整行覆盖掉（元器行即此例）。
prev_days = {id(l): DAYS_RE.search(l).group(1) for l in out if DAYS_RE.search(l)}
out = [recompute(l) if l not in REWRITE.values() else l for l in out]

# ⚠️ **040 期修正的断言口径**：基准日推进一天，正确期望不是「每行 -1」，而是「每行等于（其截止日 − 基准日）」。
#    实跑证明 039 期本身就有几行倒计时已带错（继承误差，逐期滚雪球），故断言改为「结果必须等于按截止列算出的真值」，
#    并把 before→after 的真实差异逐行打印出来供人工复核（**继承字段必须重算，但重算结果要与旧值对账**）。
diff = []
bad = []
for l in out:
    m = DAYS_RE.search(l)
    if not m:
        continue
    if l in REWRITE.values():
        continue
    d = parse_cut(l)
    if d is None:
        continue
    truth = (d - BASE).days
    if int(m.group(1)) != truth:
        bad.append((m.group(1), truth, l.split("|")[1][:40]))
print("recomputed rows with 距今:", len([l for l in out if DAYS_RE.search(l)]))
print("before -> after diff (行名 / 旧值 -> 新值):")
for l in out:
    m = DAYS_RE.search(l)
    if not m or l in REWRITE.values():
        continue
    d = parse_cut(l)
    if d is None:
        continue
    truth = (d - BASE).days
    if int(m.group(1)) != truth:
        diff.append((l.split("|")[1][:46].strip(), m.group(1), truth))
for name, a, b in diff:
    print("   %-46s %s -> %s" % (name, a, b))
assert not bad, ("重算结果不等于按截止列算出的真值", bad)

# ---- 插入新行：插在 ⚪ 存档块之前 ----
anchor_idx = None
for i, l in enumerate(out):
    if l.startswith("| ⚪ **DeepSeek 10/15"):
        anchor_idx = i
        break
assert anchor_idx is not None, "未找到 ⚪ 存档块锚点"
out = out[:anchor_idx] + NEW + out[anchor_idx:]

assert len(out) == PREV + len(NEW), (len(out), PREV + len(NEW))

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(header + "\n" + sep + "\n")
    f.write("\n".join(out) + "\n")

print("rows: %d (%d + %d new) / rewrites: %d" % (len(out), PREV, len(NEW), rw))