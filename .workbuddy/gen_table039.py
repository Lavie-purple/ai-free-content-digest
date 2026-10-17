# -*- coding: utf-8 -*-
"""从 038 期 md 提取第四章截止表 -> 基准日 2026-10-17（同日第二轮，天数不变）-> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table039.md（纯表格块，供 039 期正文嵌入）。

六步（027 期定做法、028 期定型；039 期第十四次落地）：
  1) 先断言行数（038 期 body = 197）
  2) 按行名子串套 REWRITE 字典（每键必须恰好命中 1 次）
  3) 正则重算每一行的「距今 N 天」（基准日仍是 10/17 -> 同日第二轮，delta 全部不变）
  4) 未 REWRITE 的行做归属化（「本期」-> 「038 期」）
  5) 新行插在 ⚪ 存档块（首行 "| ⚪ **DeepSeek 10/15"）之前 -> 再断言总数
  6) 输出后由 inject039.py 注入正文占位符

⚠️ **本期是同日第二轮**：基准日与 038 期同为 2026-10-17，故「距今 N 天」**不应变化**；
   若实跑发现任何一行天数变了，说明该行的截止日本身变了，必须逐条看过 —— 这是本期新增的一道断言。
⚠️ **截止列纪律**：真截止日才写可解析 `M/D`；换挡日/登记启动日/权重交付日一律写不可解析形态。
   「限时免费」没有结束日时写「未公布」（避坑 154/166）。
"""
import re
from datetime import date

SRC = "AI免费内容与权益速递-第038期-2026-10-17.md"
OUT = ".workbuddy/tmp_table039.md"
BASE = date(2026, 10, 17)
PREV = 197

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

# ---- 本期核心：把 038 期「未核到」的四组字段一次补齐（全部来自 OpenCode 官方两页一手源）----
REWRITE["`OpenCode` 限免 `Reflection Beam`"] = (
    "| 🟢 **`OpenCode` 限免 `Reflection Beam`（1M 上下文）** | **未公布（免费结束日期未公布）** | 🟢 生效中。"
    "**10/16–10/17 `OpenCode` 官方 X 宣布把 `Beam` 与 `GLM-5.3-Flash` 一并免费**（501B/23B MoE、1M 上下文）。"
    "**⚠️ （039 期）038 期留下的「四条限制未核到 / 是否计入套餐额度未核到」两组问题，本期已从 `opencode.ai` 官方两页一手核齐，逐条抄**："
    "**① 数据留存：`Beam Free` 不是零留存 —— 官方原文「Prompts and other inputs are not used for training. "
    "Data is retained for 30 days for safety reasons」**；"
    "**② 地区限制：`Beam Free` 被官方标注 `limited regions`，不可用地区含「China (including Hong Kong and Macau)」"
    "—— 全表 18 国 + 乌克兰 3 个州（安哥拉、白俄罗斯、柬埔寨、中国、刚果民主共和国、赤道几内亚、伊朗、伊拉克、老挝、利比亚、"
    "尼日利亚、朝鲜、俄罗斯、叙利亚、土库曼斯坦、乌兹别克斯坦、委内瑞拉，及乌克兰的克里米亚、顿涅茨克、卢甘斯克）**；"
    "**③ 套餐额度：`Beam Free` 在 `Go`（$10/月）与 `Go Plus`（$40/月）两档的月度用量均写 `Unlimited`，"
    "且 5 小时 / 周 / 月三个请求估算列全为 `Unlimited`** —— **即它不占用套餐额度**（这回答了 038 期的第 ⑧ 项强制动作）；"
    "**④ token 价格：Input / Output / Cached Read 三列均为 `Free`、Cached Write 为 `-`（该表所有免费行同款占位符，非数值）**。"
    "**⚠️ 三个必须分开读的点**：**「不用你的数据训练」≠「不留存」**（038 期把同平台 `GLM-5.3-Flash` 的「零留存」口径"
    "外推到本条，是错的）；**地区限制挂在「提供方」而非「权重」上 —— `Beam` 权重是 Apache 2.0、无地域闸门，"
    "受封锁地区的团队仍可下载自部署，用不了的是这个免费端点**（避坑 171）；"
    "**托管地只有美国与欧盟（OpenCode 自述），叠加 30 天留存与 18 国封锁，是一条可当场核对的合规形状**。"
    "**⚠️ 与同平台 `GLM-5.3-Flash` 免费档的四条限制仍必须分开写**（后者：仅平台内 / 上下文 200K 而非 1M / 拒 PDF / 速度慢且不稳定）"
    "**⚠️ 时序细节**：`Beam` 在 `OpenCode` 上的代号正是 `stealth/cat-jam`，开发者此前已用过它 —— "
    "**「今天宣布免费」与「此前已是隐身免费条目」是两件事**（避坑 117 / 142） |"
)

# ---- 第二条纠错：Zen 页与 Go 页对同两个模型给出「免费 / 收费」两个答案 ----
REWRITE["OpenCode `GLM-5.3-Flash` 免费档"] = (
    "| 🟢 **OpenCode `GLM-5.3-Flash` 免费档（200K 上下文 · 仅平台内）** | 未公布（官方口径 limited time） | 🟢 生效中。"
    "**免费模型 ID `glm-5.3-flash-free`（OpenCode 侧 `opencode/glm-5.3-flash-free`）**。"
    "**四条限制（第三方当日实测）**：**① 只能在 OpenCode 内用，不是通用 API；② 上下文封顶 200K token，而非原生 1M；"
    "③ 拒绝 PDF 附件，尽管模型元数据列出了 PDF；④ 回答慢且不稳定**。"
    "**正面结论**：**当日以全新安装、无登录、无 API Key 实测成功调用**；"
    "**官方 Inference API 文档写明「付费模型需要 Authorization 头、免费聊天模型可不带」，形成账号可选的直连路径**。"
    "**⚠️ （039 期）核到一处「同一平台两个官方页面给出两个答案」，039 期首次登记，两说并列**："
    "**① 按量付费页（`opencode.ai/docs/zen`，即 Console）把 `GLM-5.3-Flash Free` 列为 Input/Output/Cached Read 全 `Free`、"
    "标注 `free on OpenCode for a limited time`、且称其 provider 遵循零留存；**"
    "② 订阅页（`opencode.ai/docs/go`）上只有 `GLM-5.3-Flash`（无 Free 后缀），Input $0.15 / Output $0.50 / Cached Read $0.03、"
    "**月度用量写 `$60`、无 `limited time` 标签**，并给出每 5 小时 6,320 次的请求估算**。"
    "**⚠️ 本报告不取其一、不合并成一句**（避坑 172）；**可核的差异是「按量付费口径免费」与「订阅口径有月度上限」两套账**，"
    "**而 038 期只写了「OpenCode 免费了」、没有写清是哪一套口径**。"
    "**⚠️ 免费的是 Flash 档，不是 `GLM-5.3`** —— **四条对照必须一起写**（避坑 163）："
    "**OpenCode `glm-5.3-flash-free` $0 / 200K / 32K / 仅 OpenCode 内；OpenCode Zen `glm-5.3-flash` $0.15 输入 $0.50 输出 / 1M / 131K / "
    "任何持 Zen key 的客户端；OpenCode Zen `glm-5.3`（非 Flash）$1.40 输入 $4.40 输出；Z.ai 官方 API `glm-5.3-flash` $0.15 / $0.50 / 缓存 $0.03 / 1M**。"
    "**⚠️ 这是同一模型第二次被 OpenCode 免费** —— 8/20 起匿名模型 `Ox Alpha` 出现在 OpenCode 与 OpenRouter 免费列表（1M 上下文），"
    "8/26 Z.ai 揭示它就是 `GLM-5.3-Flash`；本次改用本名 + 200K 窗口 —— **两次免费的窗口不同，不要当成同一轮活动**（避坑 117 同族）。"
    "**⚠️ 与 10/15 的 `DeepSeek V4.1 Flash` 免费（同样 200K）是两笔账**（036 期登记）—— **两款结束日均未公布** |"
)

# ---- 第三条：DeepSeek V4.1 Flash 同样存在两页口径冲突，且本次核到峰谷定价 ----
REWRITE["OpenCode `DeepSeek V4.1 Flash` 免费档"] = (
    "| 🟢 **OpenCode `DeepSeek V4.1 Flash` 免费档（200K 上下文档）** | 未公布（免费档结束日未公布） | 🟢 生效中。"
    "**10/15 宣布**。**免费版实测支持 200K 上下文窗口，而该模型原生为 1M**；"
    "**免费开放后，该模型在 OpenCode 平台内的调用不再计入套餐额度消耗**。"
    "**沿革（「Operation Cheepseek」）**：**9 月 OpenCode 曾把该模型在 OpenCode Go 套餐中的使用额度从 $15 临时提到 $60，"
    "10/12 又调到 $80，（036 期）直接全免** —— **三次方向一致，但每一次都是「临时额度」口径，不是「永久免费」口径**。"
    "**⚠️ （039 期）与上一条同族的一处两页冲突**：**按量付费页列 `DeepSeek V4.1 Flash Free` 为全 `Free` + `limited time`；"
    "订阅页只有 `DeepSeek V4.1 Flash`，且分成 Off-Peak（$0.15 输入 / $0.60 输出 / 缓存读 $0.003）与 "
    "Peak（$0.30 / $1.20 / $0.006）两行、月度用量写 `$80`、无 `limited time` 标签**。"
    "**⚠️ 峰谷时段官方有明确口径**：**Peak 为周一至周五 UTC 01:00–04:00 与 06:00–10:00，其余时段（含周末）均为 Off-Peak** —— "
    "**这是本表里唯一一条「同模型同时存在两个价格」且切换时刻可查的条目**（避坑 172 同族）。"
    "⚠️ **这不代表 DeepSeek 官方 API 变免费** —— **`V4.1 Flash` 在 DeepSeek 官方平台没有免费 API 层级，仍为预充值按量付费**。"
    "⚠️ **社区 TPS 反馈（非受控测试）**：**ollama 云最高约 490 tok/s 但不稳定、午间可降至五六十；OpenCode Go 套餐内有用户反映掉到 100 以下；"
    "上下文 >100K 后 <100、到 200K 时约 50**。"
    "⚠️ **模型本身事实**：**2026-09-10 发布，原生多模态 MoE、主干 552B + 196B `Engram` 条件记忆参数、40 层语言主干"
    "（前 20 因果编码器 / 后 20 解码器）、Prefill 计算量接近减半**（避坑 159） |"
)

# ---- 第四条：Together AI 限免 10/18 到期（本期基准日仍是 10/17，故仍为 T+1）----
# ⚠️ 行名逐字抄自 038 期表（037/038 期纪律：从正文抄行名几乎一定抄错，抄错由下方断言兜住）
REWRITE["Together AI `Muse Spark Open` 限免"] = (
    "| 🟡 **Together AI `Muse Spark Open` 限免** | **10/18** | 🟡 生效中（**距今 1 天**）。"
    "**限免到期后是否续期，本期回扫未见公告** —— 按避坑 78「无信号即默认收口」处理。"
    "**常规 serverless 价为 $1.25 输入 / $4.25 输出 / 缓存读 $0.15 每百万 token**（10/16 调成 $0 之前的口径）。"
    "**⚠️ （039 期）官方定价页本轮回访被 Cloudflare 拦截、未取到新的价格表** —— "
    "**按 037 期纪律记「核对受阻」而不是「已复核」**，上一行的价格仍是 038 期沿用的口径、**两期不可声称已重新核过**。"
    "⚠️ **同表另有一条同日限免（Vercel 的 `Beam`）却没有结束日** —— **两条限免的「到期可预期度」完全不同，"
    "不要合并成「本周有两个限免」**（避坑 154）。"
    "⚠️ **本条与 `Muse Spark Open` 权重开放是两笔账**：权重开放是永久事实、限免是活动窗口（避坑 148/150 同族） |"
)

# ---- 第五条：Vercel 限免补上「与 Ollama 的对照」----
REWRITE["Vercel AI Gateway 免费档"] = (
    "| 🟢 **Vercel AI Gateway 免费档（2 模型）** | 未公布 | 🟢 生效中。⚠️ **零价模型也要求绑卡**（避坑 73 同源）。"
    "**（038 期登记）本行新增一条限免，且官方不公布结束日期**：**10/16 起 `reflection/beam` 与 `reflection/beam-free` 两个 slug 同时 $0** —— "
    "**`reflection/beam` 免费期结束后自动切到定价、slug 不变、无停服；`reflection/beam-free` 免费期结束即停止服务**。"
    "⚠️ **同一模型、同一渠道、同一天，两个 slug 的收尾方式完全相反** —— **选错 slug 的后果不是「多花钱」而是「服务没了」**（避坑 161）。"
    "⚠️ **限免条件写得很窄：「由 Reflection AI 提供服务时免费」，换 provider 就不在范围内**。"
    "**⚠️ （039 期）补一条横向对照：`Beam` 同期在 `Ollama Cloud` 也限免（见下表独立行）—— "
    "**三条限免渠道（Vercel / OpenCode / Ollama）全部不公布结束日期，而 Together AI 那条限免至 10/18 有明确日期**，"
    "**四者恰成「到期可预期度」的两端**（避坑 166）。"
    "⚠️ **免费期没有确切结束日期**：**Vercel changelog 与 Reflection 官方博客都没写** |"
)


# ---- 第七条：老混元 Q04 天数推进（同日第二天）----
REWRITE["老混元大模型平台停服"] = (
    "| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必须迁移到 TokenHub**。"
    "**10/17 高危窗口第 17 天**（9/25 自设倒排日已过 **22 天**；Q04 **连续第 27 期**未见确切日期，厂商只给「9 月底」）。"
    "⚠️ **一条「9 月底停服」拖到 10 月中下旬仍无日期，处置维持「按已停服对待、只做迁移」**——迁移动作本身不要等；"
    "⚠️ **同一家厂商两条线，一条无日期一条有精确到日的倒排**（元器 11/9，见下表），"
    "**说明「无日期」不是这家厂商的常态，而是这条线的常态**（避坑 164） |"
)

# ---- 第八条：AutoClaw 第三期仍无公告（连续第 3 期）----
REWRITE["智谱 AutoClaw「每日登录领 credits」第二期"] = (
    "| ⚪ **智谱 AutoClaw「每日登录领 credits」第二期** | **已按原定日期收口（活动期 10 月 12 日至 10 月 16 日，北京）** | ⚪ **已按原定日期收口（10/17 回扫未见延期或提前收口公告）**。"
    "**（037 期登记的档位表口径全部不变）**：**10/12 首日全体 10,000 Credits（1 亿 GLM-5.3-Flash Tokens）；10/13–10/16 每日全体 800 Credits（800 万 Tokens）**；"
    "**付费会员额外每日奖励按档位（AutoClaw 月度订阅 Lite/Base/Pro/Max = 500 / 5,000 / 7,000 / 8,000 Credits；"
    "`GLM Coding Plan` 个人版 Lite/Pro/Max = 5,000 / 7,000 / 8,000 Credits）**。"
    "**⚠️ （039 期）第三期是否接上：本期仍未见公告 —— 连续第 3 期未见**（037、038 期已连续记两次「本期未见公告」）。"
    "**按 032 期定的「疑似实质违约候选」判据：厂商承诺的交付物按期是否出现是可判定的，超过一个自然周期就换档** —— "
    "**注意这条不适用于本条（第二期本身按期兑现了），只适用于「第三期是否存在」这个待定问题**（见待定问题库）。"
    "⚠️ **每日奖励当天午夜过期、当日领当日用；每账号每日限领一次；多重会员只取最高档、不可叠加**（避坑 52） |"
)

# ---- 第九条：Reflection 自家 API 免费 beta 的价格仍未公布（回扫结果）----
REWRITE["Reflection Beam 开放权重"] = (
    "| 🟢 **Reflection Beam 开放权重** | **已交付（权重交付日 10 月 16 日，非活动截止）** | 🟢 **已于 10/16 按 10/5 承诺兑现**。"
    "501B 总参 / 23B 激活、**1M 上下文**、**Apache 2.0**（模型卡明确不禁止蒸馏 / 用输出训练 / 微调或合并）。"
    "**⚠️ 038 期纠错三条（本期维持，不重复展开）**："
    "**① 「10/16 发布」是错的 —— 10/5 已宣布是开放权重模型、只是权重未放，10/16 是权重交付日**（避坑 142）；"
    "**② `Terminal-Bench 2.1`（官方 80.1%）与 `Terminal-Bench 4.0`（独立 3.0%）是两个版本的同名基准，不可比大小**（避坑 144 同族）；"
    "**③ 「Apache 2.0」不等于「没有闸门」**（避坑 162）。"
    "**⚠️ （039 期）回扫结果：Reflection 自家 API 免费 beta 结束后的价格仍然未公布** —— "
    "**`platform.reflection.ai` 本轮实访需登录才见模型与价格，未取到公开价目表**；"
    "**独立侧唯一可读的第三方价格是 `Artificial Analysis` 记录的跨托管商中位价 $0.70 输入 / $2.10 输出每百万 token**，"
    "**这不是 Reflection 的报价、也不能推知免费期结束后的定价**（避坑 116 同族）。"
    "**⚠️ 跑起来要什么**：**BF16 约 1 TB / NVFP4 约 280 GB、官方建议至少 4 张 B200（720 GB 显存口径）** —— 不是「人人本地跑」的模型（避坑 41 第三层）。"
    "**同日 `Mirror CLI` 一并开源（Python 产品层 + Rust agent core）**，且官方称 Beam 与该 harness 共同训练 |"
)

# ---- 第十条：商务部 48 号公告登记仍在进行（登记启动日已过一天）----
REWRITE["商务部 AI 技术出口管制目录修订"] = (
    "| 🟡 **商务部 AI 技术出口管制目录修订 · 出口前登记** | **未公布（征求意见与登记实施日均为「非活动截止」，两个时点见正文一·4）** | "
    "🟡 **登记义务已生效、管制范围尚未落地**。"
    "**商务部、科技部 2026 年第 48 号公告（10/16）**：拟将**大模型 / 智能体 / 算力集群 / 信息处理 23 项 AI 技术**"
    "（三领域共 40 项，其中拟禁止 14 项、拟限制 26 项）增列进《中国禁止出口限制出口技术目录》，"
    "**并同步对附件所列技术启动「出口前登记」，已经开始但尚未完成的出口也在范围内**。"
    "**⚠️ 距今 29 天**（征求意见截止）。"
    "**⚠️ （039 期）回扫：登记义务生效满一天，本期未见实施日公告、也未见任何一家厂商就「已启动登记」发出办理指引** —— "
    "**这意味着受影响主体目前处在「义务已成立、通道未开」的状态**（Q27 三项仍未定）。"
    "**四条豁免（决定哪些开源模型还能正常出海）**：**① 已开源或已发论文进入公共领域的技术不纳入；"
    "② 人工智能类技术开源、境外自建自营算力中心、赴境外芯片流片、利用境外资源联合研发、参与国际标准制定 —— "
    "适用自动许可等便利措施（基本「即报即出」）；③ 用限制类大模型对外提供 API 调用 / APP 网页交互 / SaaS 应用 / "
    "本地端侧轻量化部署 —— 不属于大模型技术出口管理范围；④ 纳入限制类的技术若开展海外本地化部署属于技术出口管理范围，"
    "但部署在海外自有云等风险可控情形可适用自动许可**。"
    "**⚠️ 不得写成「AI 技术出口已被管制」** —— **登记生效日与管制实施日是两件事**（避坑 167）；"
    "**Q27 登记三个未定项（实施日 / 23 项技术指标线 / 适用主体）** |"
)

# ---- 第十一条：Xing4.0 免费档本轮重取（流通量字段不得沿用）----
REWRITE["中国电信 `Xing4.0-29B-A4B` 上架 OpenRouter 免费档"] = (
    "| 🟡 **中国电信 `Xing4.0-29B-A4B` 上架 OpenRouter 免费档** | **未公布（限免结束日未公布）** | 🟡 生效中。"
    "**`xingchen-agi/xing4.0-29b-a4b:free`，262K 上下文**（`freellm.net` OpenRouter 专页 `Last Updated 2026-10-17` 实跑，逐条标注厂商为 XingChen / China Telecom）。"
    "**⚠️ （039 期）本轮重取同一页面，`:free` 清单逐条比对结果与 038 期一致（19 个在线、本模型仍在列、上下文仍为 262K）—— "
    "按 029 期定「重取三结果记账」，本期为同值，且不得据此写趋势**。"
    "⚠️ **与 008 期那条「`Xing4.0` 开放权重」是两件事**：权重自 2026-09-16 起就在 HF `XingChen-AGI` 组织页可下载（Apache-2.0），"
    "**本期变化的是「出现了免费可调入口」—— 「权重公开」与「免费可调用」之间隔了整整一个月**（避坑 142）。"
    "⚠️ **免费档额度按 `OpenRouter` 官方口径**：**50 次/日（累计充值满 $10 后 1,000 次/日）、20 次/分** —— "
    "⚠️ **`freellm.net` 该页写「200 req/day」，与官方冲突，两个口径都写、不取其一**（避坑 161）。"
    "**架构字段**：**29B 总参 / 每 token 约 4B 激活、40 层、64 路由专家选 4 + 1 常开共享专家、`MLA` 压缩 KV、`MTP` 内训、原生 256K 可扩 512K**；"
    "⚠️ **`mHC` 四路 hyper-connection 结构需框架自定义内核（SGLang 为其专门发 split-K 内核）**；"
    "⚠️ **基准全为厂商模型卡自报、无独立复现**（避坑 116） |"
)

# ---- 本期新行 ----
NEW = [
    "| 🟡 **`Ollama Cloud` 限免 `Reflection Beam`（1M 上下文 · 全量零留存）** | **未公布（限免结束日期未公布）** | 🟡 生效中。"
    "**`Ollama` 官方博客（10/16，署名 Ollama）原文**：「Reflection's first open-weight model Beam is generally available as of this morning, "
    "and we're day-zero partners rolling it out on Ollama for free (for a limited time only!)」"
    "**—— 即「首发合作方（day-zero partner）」身份与限免是同一句话给出的**。"
    "**⚠️ 本条最干净的一个字段是留存**：**「In collaboration with Reflection, Ollama's Beam endpoint runs with full zero data retention (ZDR)」"
    "—— 全量零数据保留，与 `OpenCode` 那条 30 天留存形成同周内两种口径**（避坑 171 同族）。"
    "**接入方式（官方给的四条命令，逐条抄）**：`ollama run beam:cloud`；"
    "`ollama launch claude --model beam:cloud`；`ollama launch codex --model beam:cloud`；`ollama launch opencode --model beam:cloud`"
    "**—— 即它同时给出了三家编码 agent 的接入口**。"
    "**规格（官方博客复述）**：**稀疏 MoE、约 501B 总参 / 每 token 激活约 23B、1M 上下文、文本进文本出、Apache 2.0**。"
    "**⚠️ 三处必须分开读的限制**：**① 限免没有结束日期（原文只写 `for a limited time only`）**；"
    "**② 模型托管在美国**（另一来源明确写 `hosted in the US`）—— **「零留存」回答的是「留不留」，不回答「存哪里」**；"
    "**③ `Ollama` 这条限免在 038 期已被核到但未被登记**（038 期正文只把它列为 `Beam` 的 40+ 生态伙伴之一、并写「本期只核到 Vercel 一家给出了免费口径」）"
    "**—— 本期更正为「Vercel 与 Ollama 两家」**（避坑 173）。"
    "⚠️ **与权重自部署是两笔账**：`ollama run` 走的是 Ollama Cloud 端点、不下载权重（避坑 148） |",

    "| 🟡 **`OpenCode` 的地区限制清单（`Beam Free` 等，本期首次成条登记）** | 未公布（长期，随供应商变动） | 🟢 生效中（**清单本身不是活动，是产品事实**）。"
    "**（039 期）本期把「地区限制」从单条备注升格为本表一条独立事实**，因为它第一次同时满足三个条件："
    "**① 官方成文列出可读清单 ② 它决定「中国大陆读者能不能用」 ③ 它与许可证、留存、托管地是四个独立的闸门**。"
    "**OpenCode 官方订阅页标注 `limited regions` 的模型至少两个：`Beam Free` 与 `Muse Spark 1.3 Contributor`（另有 `Muse Spark 1.2 Contributor` 同标）**；"
    "**`Beam Free` 的不可用清单为 18 国 + 乌克兰 3 个州，明确含「China (including Hong Kong and Macau)」**。"
    "**⚠️ 三条必须一起读的限制纪律**："
    "**① 地区限制挂在「免费端点的提供方」上，不挂在权重上 —— `Beam` 权重 Apache 2.0、无地域闸门，受限地区团队仍可下载自部署**（避坑 171）；"
    "**② 「零留存 / 不训练」与「能不能用」是两个独立维度 —— 本周三条 `Beam` 限免里，Vercel 未公布留存、OpenCode 30 天、Ollama 全量 ZDR，"
    "而能不能用又各自另有一套规则**；"
    "**③ 封锁清单会变，本行须标注核对日，不写「永久不可用」**（避坑 78 同族）。"
    "**⚠️ 本行是本报告第一个「以地域可用性为主线」的条目 —— 面向中文读者时，免费清单必须先过这一关** |",
    
    "| 🟡 **OpenCode 三个免费模型的留存口径分三档（本期首次成条登记）** | 未公布（随免费期结束而变） | 🟢 生效中（**这是产品事实的横向对照，不是活动**）。"
    "**（039 期）038 期把「留存」当单条备注处理，本期升格为独立一条**，理由是：**同页 15 个免费模型的留存口径至少分三档，"
    "把它们混成一句「OpenCode 免费模型」会让读者做出错误的合规判断**（避坑 171）。"
    "**逐档抄官方原文**：**① 零留存 + 不训练（最干净的一档）**：`GLM-5.3-Flash Free`、`DeepSeek V4.1 Flash Free`、"
    "`LongCat 2.5 Preview Free`、`Space Bunny Free` —— 官方称其 provider 遵循 zero-retention policy 且不使用数据训练；"
    "**② 不训练但留存 30 天**：`Beam Free`、`LL Alpha Free` —— 官方原文「not used for training. Data is retained for 30 days for safety reasons」；"
    "**③ 免费期数据可能被用于改进模型**：`Big Pickle`、`Exo Free`、`MiMo-V2.6-Flash Free`、`MiMo-V2.5 Free` —— 官方写「may be used to improve the model」；"
    "**④ 另有一档更硬的警告**：`Muse Spark 1.3 Contributor Free` 的免费价是**换取「允许用你的 prompts 与 completions 训练未来 Meta 模型」的许可**；"
    "**⑤ `Nemotron` 三个免费端点带试用警告**：官方原文「Trial use only — do not submit personal or confidential data」。"
    "**⚠️ 为什么这在编码 agent 里更要紧**：**「提问」不敏感，"
    "而一个编码 agent 送出的是它读过的文件、生成的 diff 与自认为相关的上下文动辄几十万 token —— "
    "「零留存」与「30 天」的区别在这里是「源码要不要在第三方留 30 天」的区别**（避坑 145 同族）。"
    "⚠️ **本表三档不可互相代入**：**038 期把同平台 `GLM-5.3-Flash` 的零留存口径外推到 `Beam`，本期已更正** |",
    "| 🟢 **`Ollama Cloud` 接入 `Beam` 的四条官方命令（长期可用）** | 未公布（命令长期有效） | 🟢 生效中。"
    "**（039 期）随 `Ollama` 限免一并登记**，因为**它是本报告至今唯一一组「官方直接给出的跨工具接入口」**。"
    "**四条命令（`Ollama` 官方博客逐字抄）**：`ollama run beam:cloud`；"
    "`ollama launch claude --model beam:cloud`；`ollama launch codex --model beam:cloud`；`ollama launch opencode --model beam:cloud`。"
    "**⚠️ 读法**：`ollama run` 走 Ollama Cloud 端点、**不下载权重**；`ollama launch` 则是把该端点注册给 Claude Code / Codex / OpenCode 三个编码 agent 用。"
    "⚠️ **它与「权重自部署」是两笔账（避坑 148）** —— 前者省的是部署、后者省的是钱与数据主权，两者不可互相替代。"
    "⚠️ **同时它也是本表第一条把「免费限免」与「接入方式」分开登记的样本**：限免有结束日、命令没有 |",
]

# ---- 套 REWRITE：每键恰好命中 1 次 ----
rw = 0
out = []
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

# ⚠️ **037/038 期纪律：REWRITE 键数必须等于实际 rewrites 数** —— 两个未命中的键就是抄错的行名
assert len(REWRITE) == rw, ("REWRITE 键数与命中数不等（很可能抄错行名）", len(REWRITE), rw)

# ---- 未 REWRITE 的行做归属化：本期 -> 038 期 ----
for i, l in enumerate(out):
    if l not in REWRITE.values():
        out[i] = l.replace("（039 期）", "（038 期）")
        out[i] = out[i].replace("本期重取于 2026-10-17", "上期重取于 2026-10-17")
        out[i] = out[i].replace("038 期复核维持", "038 期复核维持，039 期未检出新变化")

# ---- 正则重算「距今 N 天」 ----
# ⚠️ 不能从旧天数 +1：基准日推进时旧天数与行内真实截止日期可能不是同一条。
# ⚠️ 换挡日 / 非活动截止日期不能被解析（036 期纪律），故只认带横线的完整日期或 `**M/D**`；带括注的一律跳过。
DATE_FULL = re.compile(r"\*\*(\d{4})-(\d{1,2})-(\d{1,2})\*\*")
DATE_MD = re.compile(r"\*\*(\d{1,2})/(\d{1,2})\*\*")

def recompute(l):
    if "距今" not in l:
        return l
    cols = l.split("|")
    target = cols[2] if len(cols) > 3 else ""
    if "北京" in target or "未公布" in target or "以" in target:
        return l
    m = DATE_FULL.search(target)
    if m:
        d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    else:
        m2 = DATE_MD.search(target)
        if not m2:
            return l
        d = date(2026, int(m2.group(1)), int(m2.group(2)))
    delta = (d - BASE).days
    return re.sub(r"\*\*距今 -?\d+ 天\*\*", "**距今 %d 天**" % delta, l)

before = [re.search(r"\*\*距今 (-?\d+) 天\*\*", l).group(1) for l in out if "距今" in l and re.search(r"\*\*距今 (-?\d+) 天\*\*", l)]
out = [recompute(l) for l in out]
after = [re.search(r"\*\*距今 (-?\d+) 天\*\*", l).group(1) for l in out if "距今" in l and re.search(r"\*\*距今 (-?\d+) 天\*\*", l)]

# ⚠️ **本期新增断言**：同日第二轮 -> 基准日未变 -> 所有「距今 N 天」必须逐一不变
changed = [(i, a, b) for i, (a, b) in enumerate(zip(before, after)) if a != b]
assert not changed, ("同日第二轮基准日未变，但有行的天数变了，需逐条复核", changed)

# ---- 插入新行：插在 ⚪ 存档块（首行以 "| ⚪ **DeepSeek 10/15" 开头）之前 ----
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

print("rows = %d（原 %d + 新增 %d）" % (len(out), PREV, len(NEW)))
print("rewrites = %d" % rw)
print("REWRITE 键数 = %d（已断言 == rewrites）" % len(REWRITE))
print("同日第二轮断言：距今天数变化行数 = %d（应为 0）" % len(changed))
print("新行名：")
for n in NEW:
    print("  " + n[2:n.index("|", 2)].strip())
