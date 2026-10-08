# -*- coding: utf-8 -*-
"""027 期结构化台账更新：
  A. frozen_items.md —— 追加 027 首登条目 + 就地补写既有条目的 027 进展
  B. open_questions.md —— Q04/Q17 期数推进；Q18/Q19/Q20 升格为避坑 125；补 027 期现状行
全部带断言，不匹配就中止。
"""
import io, re, sys

WS = "."

# ---------------- A. frozen_items ----------------
FR = WS + "/.workbuddy/data/frozen_items.md"
txt = io.open(FR, encoding="utf-8").read()
lines = txt.split("\n")

NEW_ROWS = [
    ("Claude Haiku 5.5", "027", "额度",
     "**Anthropic 10/7 发布的 Haiku 线新档**（`claude-haiku-5-5`）：**1M 上下文 / 128K 最大输出**，"
     "Haiku 线首次支持 **effort 设置 + adaptive thinking**；**AA Intelligence Index 43**；官方称运行成本平均降约 75%；"
     "**≤100K 提示：输入 $0.10 / 输出 $0.50 / 缓存读 $0.01 / 缓存写 $0.125**（每百万 token），"
     "**>100K 提示整单按 $0.50 / $2.50 / $0.05 / $0.625**，**Batch 再半价**；已上 Claude API / Bedrock / Google Cloud / Microsoft Foundry。"
     "⚠️ **破坏性变更：手写 extended thinking（走 `budget_tokens`）在 5.5 上返回 400**，adaptive thinking 默认开启、"
     "**响应可能以 thinking block 开头**；**新分词器使同段文本 token 数略增**，"
     "故「便宜 90%」≠账单降 90%", "演进中"),
    ("Claude Max·Team 月度 API 额度", "027", "额度",
     "**Anthropic 10/7 起给订阅附赠的 Claude Platform API 配额**：**Max 5x $100/月、Max 20x $200/月，"
     "Team 每 Standard 席 $20 + 每 Premium 席 $100、公司池化上限 $500/月**；可跑 Claude API / Batches / Managed Agents / Agent SDK，适用任意模型。"
     "⚠️ **三把锁**：**只走一方 API / Console（Bedrock、Vertex、Foundry 三家都不行）、不覆盖交互式 Claude Code 会话、按月发放当月未用不结转**；"
     "**Pro 没有**；**需在计划内满 7 天**；**不提高订阅本身的应用内限额**（避坑 123）", "演进中"),
    ("Sonnet 5.5 缓存读取", "027", "额度",
     "**Anthropic 10/7 把 Sonnet 5.5 的缓存读取价从 $0.20 降到 $0.10（每百万 token）**，即基础输入价的 0.05×（原 0.1×）；"
     "**缓存写与其他价格未变**。官方称这让 Sonnet 5.5 在多数长任务上成本降约 20%。**「不改模型、只改价目表」的降本**", "稳定"),
    ("Intelligent UI", "027", "发布",
     "**OpenAI 10/7–10/8 随 GPT-6 全量推送的交互形态**：ChatGPT **可用可交互界面回答**（图表 / 按钮 / 表单 / 可运行小工具），**边生成边渲染**；"
     "官方称 **GPT-6 Instant 在联网问题上平均比 GPT-5.6 Instant 早 44% 开始回答**。"
     "⚠️ **44% 是「开始回答时间」不是「完成任务时间」、且为厂商自评**；⚠️ **Pro reasoning 选项仍走 GPT-6 Astra，不支持 Intelligent UI**（避坑 116 同源）；"
     "**Work 与 Codex 的模型不随本次调整**；**公告未说 Free 用户有多少用量额度**", "演进中"),
    ("GPT-6.1 Astra（搁置）", "027", "发布",
     "**原计划 10 月的 GPT-6.1 Astra 因内部安全测试顾虑被搁置，不进入 10/7–10/8 的 ChatGPT 全量推送**。"
     "**直接影响迁移动作**：**GPT-5.5 → 仍按 `gpt-5.6-sol`（Free/Go 用 `gpt-6-luna`）**，**不要自行改成 Astra 系**（见 Q17）", "稳定"),
    ("GPT-6 Luna Decisions", "027", "额度",
     "**OpenAI Decisions API 开放公开测试（10/7–10/8），OpenRouter 同日上线 `GPT-6 Luna Decisions`**："
     "**输入 $0.10/M、输出免费、1M 上下文**，官方称决策速度比走 Responses API 的 GPT-6 Luna 快达 10 倍。"
     "⚠️ **「输出免费」是因为它不再生成文本——不是聊天模型的替代品**（避坑 118/119 同源）", "演进中"),
    ("Unsloth 决策模型微调", "027", "工具",
     "**Unsloth 开源的「把 LLM 微调成决策模型」教程 + 仓库（10/7）**：把 **Qwen3.8 / Gemma 4** 等改造成输出选项概率的决策模型；"
     "**Qwen3.5 0.8B 在 3 个决策基准合计准确率 20.7% → 74.3%**；**只要 4GB 显存即可复现**。"
     "⚠️ **可不可以商用取决于底座许可证**。**意义：决策模型线在 3 天内完成「只能调云 API → 可下载权重 → 可自己造」三级跳**", "演进中"),
    ("pplx-embed-v2-late", "027", "开源",
     "**Perplexity 10/7–10/8 开源的 late-interaction 多向量嵌入权重**（Hugging Face）：**9B（索引多模态数据）+ 0.6B（端侧查询）共享同一嵌入空间**；"
     "官方称**免 OCR 即可检索 PDF 页面**；**MADQA 92.4% / BrowseComp+ 64%**（公司自报）。⚠️ **官方未在本轮说明中展开许可证与商用条款**", "演进中"),
    ("混元图像 3.0", "027", "开源",
     "**腾讯 9/28 发布并开源的图像模型（027 期补登，025/026 两期漏登）**：**80B MoE / 13B 激活**；**商用 API 定价 0.15 元/张**；"
     "**10/5 腾讯宣布其在 LMArena 图像盲测 26 款模型中排名第一**（用户双盲投票，非厂商自评）。"
     "⚠️ **当前仅开放文生图**，图生图与图像编辑「后续推出」；⚠️ **榜位流动性高、官方同时给名次区间与置信区间，不宜当长期定论**。"
     "**027 期起出图位由「Hy Image3.5 preview 限免」改用「商用 API 0.15 元/张 + 本地权重」两条腿**", "演进中"),
    ("Utopai X", "027", "生成",
     "**Utopai Studios 的视频模型**：**Artificial Analysis 文生视频（带音频）榜第二（1150 分）**，仅次于阿里 Wan 3.0；"
     "**底座是 MiniMax 开源 H3 + 后训练**。⚠️ **与第一名 7 分差落在重叠区间内，官方标注名次为区间 #1–3**；"
     "⚠️ **与母模型 H3 的 12 分差同样区间重叠 →「后训练胜过母模型」方向成立、统计上不可靠**（避坑 116 同源）", "演进中"),
    ("Google SynthID Detector", "027", "工具",
     "**Google 的 AI 内容水印检测器，10/7 起从「记者 / 研究者白名单」开放到全球所有人**：**免费**，"
     "**需在 Google / OpenAI / Apple 账号中选一个登录**，**每天约 10 次检查上限**；可查 **Google / OpenAI / NVIDIA / Kakao** 的水印（**Apple 即将接入**）；"
     "官方称已为 **1800 亿+ 图片视频**、**约 24 万年音频**加水印，Search / Gemini / Chrome 侧每天处理 100 万+ 次验证请求。"
     "⚠️ **查不出水印 ≠ 人类所作**；**每日 10 次上限是为了防止被拿去做「去水印」实验**", "演进中"),
    ("Ecosia 换用中国开源模型", "027", "政策",
     "**德国搜索引擎 Ecosia 经 Melious 把模型从 Mistral 切到 Qwen / GLM / Kimi（10/8，IT 之家报道）**：CEO Christian Kroll 称**成本减半、性能提升**，"
     "并称 Mistral「质量落后一年」且服务器过载。⚠️ **二手报道、未获公司或第二家独立媒体确认；「成本减半」为 CEO 口径、未独立验证**。"
     "**意义：开源权重 + 第三方托管正在长出一条绕开原厂 API 的分发通道**", "稳定"),
    ("智谱清言 双节积分返还", "027", "额度",
     "**智谱清言「双节消耗积分 100% 返还」（10/8–10/31 领取）**：**期间登录即自动发放**（chatglm.cn / App），"
     "**9/25–10/7 花掉的积分按 100% 返、单账号上限 15 万**，**返还积分到账后约 30 天有效**。"
     "⚠️ **过期未登不补**；⚠️ **与已收口的「登录积分翻 10 倍」是两条不同的线**（避坑 52 同源）。**是「假期活动返场」，不是新一轮加码**", "稳定"),
    ("上海张江算力券", "027", "政策",
     "**上海张江 AI 创新小镇算力 / 模型 / 语料券（第 3 季度受理）**：**申报至 10/12 17:00**；**仅限张江 AI 创新小镇区域内企业**；"
     "入口为 **浦易达平台 `pyd.pudong.gov.cn`**；**算力券 / 模型券 / 语料券三类可申报**。"
     "**本报告表内第 5 条地方算力券**（青浦 / 湖北 / 珠海 / 上海张江 + 龙湖区政府词元券）", "稳定"),
    ("ZCode 月度安全审计报告", "027", "政策",
     "**ZCode 风波后的承诺交付物（027 期列为追踪项）**：ZCode 承诺**每月发布安全审计报告 + 设立漏洞奖励机制**；"
     "**截至 2026-10-08 未见首份月报**。**「承诺的交付物是否按月出现」是判断要不要长期留在该平台的信号**", "演进中"),
    ("codingplan.link", "027", "信源",
     "**「AI Coding Plan 订阅档横向对照」第一现场**（http://codingplan.link/）：把 **Tencent Cloud TokenHub / Volcengine Ark / 小米 MiMo / 白云智算** 等订阅的"
     "**档位 / 每 5 小时限额 / 周月上限 / 首月促销价 / 支持模型清单**并列，并标注「入门 / 推荐 / 最值」。"
     "**补的是本报告长期缺的字段：把「订阅额度」换算成「每 5 小时多少次请求」**（027 期首次命中，已入 T4）", "稳定"),
    ("creditforstartups.com", "027", "信源",
     "**「厂商面向创业公司 / 开发者生态的权益计划」对照源**（https://creditforstartups.com/）：逐条给出 **Anthropic / OpenAI / Google 等创业计划的额度上限、门槛、有效期、"
     "是否需要 VC、能不能用在云市场**，并把 **「是 API credit 不是现金」「6 个月过期」「不适用 Bedrock / Vertex」** 这类边界写在同一页。"
     "**027 期用它补全了 Claude Startup Stack 的 6 项限制（含地域排除）**；与 026 期的 CNBC 互补（CNBC 是消息第一落点，本站在条款对照）。已入 T4", "稳定"),
]

# 就地补写既有条目（key -> 追加片段）
UPD = {
    "Liquid d1": " **027 期重大反转**：**Liquid AI 已于 10/7 开源 `d1-3B`（文本 + 图像，Decision Index 0.2.1 = 48.57，10B 以下第一、与 "
                 "Decider 35B-A3B 的 47.11 持平；4090 8ms / AGX Orin 26ms / Orin Nano 50ms）与 `d1-omni-600M`（文本 + 图或音频，实验性）**，"
                 "Hugging Face 可下、**llama.cpp 原生支持（含 NVFP4）**。**上一条「API-only、无权重」自 10/7 起不成立**（避坑 124）；"
                 "⚠️ **模型卡许可是 LFM 1.0 条款，不是 Apache**。",
    "腾讯云 TokenHub": " **027 期**：**国际站两条促销**——**Promotion 1（至 10/30 12:00 北京）** GLM-5.3-Flash 17/55/4、GLM-5.2 99/310/19、Kimi K3 352/1758/36（credits/百万 token）；"
                       "**Promotion 2（至 10/8 12:00 北京）** Hy4 preview 66/196/4，**已于 10/8 12:00 收口**。"
                       "⚠️ **国际站 TokenHub 与国内 WorkBuddy 的「Hy3 限免 + Hy4 preview 夜间限免至 10/31」是两套体系，必须显式拆开写**。",
    "阶跃星辰 Step 5 Preview": " **027 期口径重要变更**：**官方已关闭新增领取通道**——**已领用户剩余权益以账户内为准，官方不再按「最高 75 天」口径新拉人**，"
                               "**上条路径自 027 期起不可执行**。⚠️ **替代体验：Step 5 Preview 已接入北京 AGI Bar，店内未来一周对所有用户免费体验**（单一信源、线下为主）。"
                               "**权重仍定档 10/15 开放**。",
    "Anthropic Claude Startup Stack": " **027 期口径补全（官方程序页 + 条款原文）**：① **$45,000 全部由第三方伙伴公司提供**（ElevenLabs / ClickHouse / Hex / Granola / Gamma / Firecrawl / Augment 等），"
                                      "**Anthropic 明确写「不是由 Anthropic 提供」**；② **$1,000 credit 一次性、6 个月过期、仅限一方 Claude API（不含 Bedrock / Vertex / Foundry）**；"
                                      "③ **免费 Team 年费只对「新加入 Team 的组织」生效**；④ **官方条款的不可用地区名单含中国**（另有 Belarus / Cuba / Iran / Myanmar / North Korea / "
                                      "Russia / Sudan / Syria / Crimea 等）——**这一条让「$45,000」对中国主体等于零**；⑤ **有伙伴 VC 背书的另可经投资人领最多 $100,000 API credit**；"
                                      "⑥ **Anthropic 自算「直接包」价值最高约 $7,000**（5 Premium 席 × $100/席/月 × 12 月 + $1,000）。**厂商自付 ≠ 伙伴 offer**（避坑 122）。",
    "Qwen-Image-2.1": " **027 期**：其配属的 **PE-T2I 提示词重写模型权重已可在 Hugging Face 单独下载**（**Qwen3.5-VL 9B 微调**，把任意语言的简短图像请求改写成详细英文提示词并推荐宽高比、输出 JSON）；"
                      "⚠️ **同为 Qwen Research License，仅研究/评估，商用须单独申请**。**同时澄清：Qwen-Image-2.0 / 3.0 至今只有 API、无权重**，而 2.1 有权重但非商用许可（避坑 124）。",
    "硅基流动": " **027 期行为样本**：**小模型永久免费已取消**（现免费仅 embedding / 语音 / OCR / 翻译 / Kolors；**新用户注册送约 16 元无门槛代金券，长期**）。"
                "**本报告自 001 期起引用的「9B 以下永久免费」口径就此作废**——**长期免费档会被单方面收缩，且不一定发公告**（与避坑 107 同源）。",
}

def append_to_row(key, extra):
    for i, ln in enumerate(lines):
        c = ln.split("|")
        if len(c) >= 7 and c[1].strip() == key:
            assert extra.strip() not in c[4], "已追加过: " + key
            c[4] = c[4].rstrip() + extra
            lines[i] = "|".join(c)
            return True
    raise AssertionError("未找到既有条目行: " + key)

for k, v in UPD.items():
    append_to_row(k, v)
    print("  ~ 补写", k)

# 追加 027 首登行（插在文件末尾）
if lines[-1].strip() != "":
    lines.append("")
for r in NEW_ROWS:
    lines.append("| %s | %s | %s | %s | %s |" % r)
    print("  + 新增", r[0])

io.open(FR, "w", encoding="utf-8").write("\n".join(lines))

# ---------------- B. open_questions ----------------
OQ = WS + "/.workbuddy/data/open_questions.md"
oq = io.open(OQ, encoding="utf-8").read()
ol = oq.split("\n")

# B1 插入 027 期现状行（放在 026 期现状行之后）
anchor = "> **026 期现状**：共 **20 条**"
idx = [i for i, l in enumerate(ol) if l.startswith(anchor)]
assert len(idx) == 1, idx
NEW_NOTE = ("> **027 期现状**：共 **20 条**（**本期无新增待澄清项**）。**Q04 第 15 期**（厂商口径仍是「2026 年 9 月底」，"
            "**本期为其第 7 个高危日**，10/8 仍无确切停服日）；**Q17 第 7 期**（**本期新增一条相关事实但议题未结**："
            "**GPT-6.1 Astra 因内部安全测试被搁置、不进入本次 ChatGPT 全量推送**——**迁移目标仍按 `gpt-5.6-sol` / `gpt-6-luna` 执行**，"
            "Codex 官方 models 页的迁移目标是否更新仍未核到）；**Q18 / Q19 / Q20 三条同源自本期起「已升格为避坑 125」**"
            "（**执行的是 025 期定下、026 期因窗口 65 分钟顺延的动作**；本期一次撞见三个「聚合层重发旧闻」新样本，具备升格实证）；"
            "其余 15 条状态不变。")
ol.insert(idx[0] + 1, NEW_NOTE)

txt2 = "\n".join(ol)

# B2 Q04 期数：第 7 期 -> 第 15 期（只改 Q04 那一行）
def patch_q(qid, old, new):
    global txt2
    ls = txt2.split("\n")
    hit = [i for i, l in enumerate(ls) if l.startswith("| " + qid + " |")]
    assert len(hit) == 1, (qid, len(hit))
    assert old in ls[hit[0]], (qid, old)
    ls[hit[0]] = ls[hit[0]].replace(old, new, 1)
    txt2 = "\n".join(ls)
    print("  ~ ", qid, old, "->", new)

patch_q("Q04", "**未澄清**（第 7 期，**避坑 24 已覆盖**）", "**未澄清**（第 15 期，**避坑 24 已覆盖**）")
patch_q("Q04", "**025 期维持（第 13 期）**：10/6 仍无具体日期，9/25 自设倒排日已过 11 天，厂商口径仍是「9 月底」",
        "**025 期维持（第 13 期）**：10/6 仍无具体日期，9/25 自设倒排日已过 11 天，厂商口径仍是「9 月底」。"
        "**027 期维持（第 15 期）**：10/8 仍只有「2026 年 9 月底」，**9/25 自设倒排日已过 13 天，本期为第 7 个高危日**——"
        "**本条已从「运维提醒」变为「长期悬案」，但迁移动作本身不要等**")
patch_q("Q17", "**未澄清**（第 5 期）", "**未澄清**（第 7 期）")
patch_q("Q17", "**025 期现状**：仍未取得新证据（本期未回核官方页，随延后）。",
        "**027 期现状**：仍未取得新证据，但**新增一条相关事实**——**GPT-6.1 Astra 因内部安全测试被搁置、不进入 10/7–10/8 的 ChatGPT 全量推送**，"
        "**故迁移目标仍按 `gpt-5.6-sol` / `gpt-6-luna` 执行，不要自行改成 Astra 系**。")

for q, extra in [("Q18", "**027 期处置**：**已升格为避坑 125**（026 期顺延的动作本期执行），与 Q19 / Q20 合并；本条不再单独挂账。"),
                 ("Q19", "**027 期处置**：**已升格为避坑 125**（与 Q18 / Q20 合并）；本条不再单独挂账。"),
                 ("Q20", "**027 期处置**：**已升格为避坑 125**（与 Q18 / Q19 合并）；本条不再单独挂账。")]:
    patch_q(q, "**未澄清**（第 2 期）" if q != "Q20" else "**未澄清**（第 1 期）",
            ("**✅ 已升格为避坑 125**" if q != "Q20" else "**✅ 已升格为避坑 125**"))
    # 追加说明到「下一步」列尾
    ls = txt2.split("\n")
    hit = [i for i, l in enumerate(ls) if l.startswith("| " + q + " |")]
    ls[hit[0]] = ls[hit[0]].rstrip().rstrip("|").rstrip() + " " + extra + " |"
    txt2 = "\n".join(ls)
    print("  ~ ", q, "标记升格")

io.open(OQ, "w", encoding="utf-8").write(txt2)
print("OK  台账已更新")
