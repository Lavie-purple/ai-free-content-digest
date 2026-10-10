# -*- coding: utf-8 -*-
"""从 028 期 md 提取第四章截止表 -> 基准日推进到 2026-10-10 -> 应用行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table029.md（纯表格块，供 029 期正文嵌入）。"""
import re, sys, os

SRC = "AI免费内容与权益速递-第028期-2026-10-09.md"
OUT = ".workbuddy/tmp_table029.md"
BASE = "2026-10-10"

lines = open(SRC, encoding="utf-8").read().split("\n")
s = e = None
for i, l in enumerate(lines):
    if l.startswith("## 四、限时活动与截止时间表"):
        s = i
    if s is not None and l.startswith("## 五、"):
        e = i
        break
rows = [l for l in lines[s:e] if l.startswith("|")]
header, sep, body = rows[0], rows[1], rows[2:]
assert len(body) == 120, len(body)

REWRITE = {}

REWRITE["🔴 **腾讯老混元大模型平台停服**"] = (
    "| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必须迁移到 TokenHub**。"
    "**10/10 高危窗口第 9 天**（9/25 自设倒排日已过 **15 天**；Q04 连续第 17 期未见确切日期，厂商只给「9 月底」）。"
    "⚠️ **一条「9 月底停服」拖到 10 月中旬仍无日期，处置已改为「按已停服对待、只做迁移」**——迁移动作本身不要等 |"
)

REWRITE["🔴 **OpenAI GPT-5.5 下线"] = (
    "| 🔴 **OpenAI GPT-5.5 下线（ChatGPT / ChatGPT Work / Codex）** | **10/14** | 🔴 **最重要的运维节点，剩 4 天**。"
    "⚠️ **API 不受影响**——官方建议 Codex 用户迁移到 `gpt-5.6-sol`（Free/Go 用 `gpt-6-luna`），"
    "并同步更新已保存的模型设置、托管配置、自定义 Agent、定时任务与脚本。"
    "⚠️ **Q17（Codex 官方 models 页是否更新迁移目标）连续 9 期未核到**；"
    "⚠️ **本期补两条同族事实**：① **ChatGPT 聊天模式的选择器里 GPT-5.5 已标注「将于 10 月 14 日下线」**（网易订阅截图口径）；"
    "② **`o4-mini` 的 API 于 10/23 停用**（**下一个运维节点，已单独登记**）——**同一周里有两个下线日，别只记 10/14** |"
)

REWRITE["🟠 **Google Gemini 免费档收缩"] = (
    "| ⚪ **Google Gemini 免费档收缩（免费档仅剩 Flash-Lite）** | **10/9** | ⚪ **已于 10/9 生效、10/10 复核维持**——"
    "**个人未订阅账号在 Gemini 应用内只剩 Flash-Lite**，Flash 与 Pro 转入付费档；**AI Plus 保留 Flash-Lite + Flash、失去 Pro**"
    "（按邮件分批生效，**生效日不统一**）；**Deep Think 已下放 AI Pro / Ultra**。**免费档上下文 32K**（Plus 128K / Pro 与 Ultra 1M）；"
    "**每档模型可设 low / medium / high effort，effort 越高越吃额度**；额度按**算力消耗**计量、**每 5 小时刷新并另有周上限**。"
    "⚠️ **这是「永久性收缩」不是「活动到期」，所以留档口径是「已生效」而非「已结束」**——"
    "**10/8 之前 Google 主 limits 表与订阅页仍写着免费可用 Flash / Pro，只有模型表那一页是新的**（避坑 130 的第一个样本） |"
)

REWRITE["🟢 **Mistral Large 4 公开预览"] = (
    "| 🟢 **Mistral Large 4 公开预览（含 OpenRouter 五折）** | **权重月底（官方口径「十月底」；媒体口径 10/27）；五折限前两周** | "
    "🟢 生效中（025 期登记）。1T 总参 / 49B 激活、原生多模态；⚠️ **许可证仍未公布**（避坑 42）。"
    "⚠️ **本期补第三条第三方实测**：**Artificial Analysis 智能指数 38 分，被评「中美以外最强智能模型」**（Tom's Hardware 10/9）；"
    "此前 **Arena Agent Arena 净改进分 −6.6%、总排名第 43**。**\"中美以外最强\"是榜单口径，\"净改进分仍为负\"也是榜单口径——两句话都要写**（避坑 116）。"
    "⚠️ **本期另有一条被否掉的口径**：多篇低质聚合稿在 **10/9** 写成「**Mistral 已于 10/9 开源该模型权重**」，"
    "**与官方「预览 / 权重十月底」直接冲突** —— **按避坑 125/120 不作本期条目登记**（见第九章） |"
)

REWRITE["🟢 **腾讯混元 Hy4 preview 新用户窗口**"] = (
    "| 🟠 **腾讯混元 Hy4 preview 新用户窗口** | **10/10** | 🟠 **今天是首开窗口最后一天（23:59 截止）**——"
    "未使用用户首启后享 **14 天每日免费**；**已体验用户夜间 23:00–8:00 免费仍到 10/31**；**Hy3 限免同样到 10/31**。"
    "⚠️ **回扫结论：无延期公告、无提前收口**，按原窗口执行（避坑 47/78） |"
)

REWRITE["🟢 **WorkBuddy「企鹅教师助手」"] = (
    "| 🟠 **WorkBuddy「企鹅教师助手」Buddy 应用体验（50 Credits）** | **10/10** | 🟠 **今天最后一天**。"
    "⚠️ 回扫未见延期公告；**它是 WorkBuddy 成长计划里 13 个体验任务之一**，任务奖励与积分签到是两笔账（避坑 52 同族） |"
)

REWRITE["🟢 **OpenRouter 免费档（本期核对 20 模型）**"] = (
    "| 🟢 **OpenRouter 免费档（本期核对 19 模型）** | 未公布（动态目录） | 🟢 生效中。免费档 **200 req/day**；**$10 充值换 5× 速率**。"
    "⚠️ **本期由 20 → 19 个在线免费模型**（freellm.net 10/9 页面、OpenRouter 目录页同步）——"
    "**免费档的数量是「每天都可能变的目录」，不是「一个固定的额度」**（避坑 68：带核对日期读） |"
)

REWRITE["🟢 **阶跃星辰 Step 5 Preview（OpenRouter / OpenCode / Cline / Kilocode / Nous Research 免费一周）**"] = (
    "| 🟢 **阶跃星辰 Step 5 Preview（OpenRouter / OpenCode / Cline / Kilocode / Nous Research 免费一周）** | 未公布"
    "（公告未给结束日；**10/8 起算，约至 10/15**） | 🟢 生效中。**600B 总参 / 27B 激活 MoE、1M 上下文、文本 + 图像输入**；"
    "**OpenRouter 定价 $1.00/M 输入、$2.70/M 输出，缓存命中 $0.05/M（首发五折）**；**AA 实测每任务 $1.03**。"
    "⚠️ **免费窗口长度按渠道不同**（OpenCode 明确一周且声明零数据留存、Cline 未写期限，避坑 126）——"
    "**按 10/8 起算，本周内到期，到期前 24 小时回扫渠道公告**；⚠️ **权重 10/15 才发、许可证未公布**；"
    "⚠️ **AA 同时测出它产出 token 是 Sol 的 1.7 倍**（避坑 119 同族） |"
)

REWRITE["⚠️ **阶跃星辰 Step 5 Preview 新用户免费套餐**"] = (
    "| ⚠️ **阶跃星辰 Step 5 Preview 新用户免费套餐** | 未公布 | ⚠️ **口径变更（027 期）**：**官方已关闭新增领取通道**——"
    "已领用户的剩余权益以账户内为准。⚠️ **替代路径**：**Step 5 Preview 上线 OpenRouter 并在多渠道开放一周免费**（见下表）——"
    "**「官方通道关了」不等于「没地方免费用」** |"
)

# 追加的新行（插在 ⚪ 存档块末尾之前，即第一条 "| ⚪ **DeepSeek Harness" 之前）
NEW_ROWS = [
    "| 🟠 **火山方舟 Agent Plan 个人版 × 专业数据集 1000 次免费调用** | **11/8** | 🟠 生效中（距今 29 天）。"
    "**订阅 Agent Plan 个人版（Small / Medium / Large / Max 四档）并在控制台「配置 Harness」开启专业数据集，即得 1000 次免费调用**："
    "**企业工商 400 次 + 企业风险 400 次 + 宏观经济 200 次**；活动期 **10/8–11/8**；**资格按账号维度发放，新购 / 续费 / 升配共享同一资格**。"
    "⚠️ **它是「数据调用次数」不是「模型 token」——两类额度不能相加**（避坑 54 同源：计量单位不同就不能合并） |",

    "| 🟠 **智谱 AutoClaw「每日登录领 credits」活动** | **10/11 16:00 UTC（北京 10/12 00:00）** | 🟠 生效中（距今 1 天）。"
    "**活动期 10/4 16:00 UTC – 10/11 16:00 UTC**；**10/4–10/6 每天登录领 5,000 credits，10/6 起每天 1,000 credits**；"
    "**credits 每日 16:00 UTC 发放、24 小时后作废**；官方按 **GLM-5.3-Flash 费率折算为「100M+ tokens」**。"
    "⚠️ **「100M+ tokens」是折算描述、不是 token 数量本身**（避坑 54）；⚠️ **每日发放、隔夜作废，忘记领 = 当天额度归零**（避坑 33 的教科书样本） |",

    "| 🟢 **汕头「词元产业」实施细则（征求意见稿）** | **10/16（意见反馈截止）** | 🟢 生效中（距今 6 天）。"
    "**汕头华侨试验区 10/8 发布《促进词元产业创新发展若干措施实施细则（征求意见稿）》**，公开征求意见至 **10/16**，"
    "明确**算力券 / 词元券的资金申报、审核、兑付流程**；是对 9 月「词元十条」的落地细化。"
    "⚠️ **企业向、尚未开放申领**；⚠️ **这是本报告表内第 7 条地方券**（青浦 / 湖北 / 珠海 / 上海张江 / 龙湖区政府词元券 / 江苏 / 汕头）——"
    "**地方券聚合入口仍缺**（第 3 类清单缺口维持） |",

    "| 🟢 **Underdog AI Saluki 27B（2-bit 量化本地 agent 模型）** | 未公布 | 🟢 生效中（10/9–10/10，Hugging Face）。"
    "**把 Qwen3.8-27B 压成 2-bit、文件仅 7.89 GB，仅保留文字 I/O**；官方称**保留原版 96% 基准表现**，"
    "**工具选择与多工具并行调用甚至优于全尺寸 Qwen3.8-27B**（数学偏弱）；**Apache 2.0**、**标准 llama.cpp 格式、无需自定义编译**。"
    "⚠️ **「2-bit 不掉点」是厂商自报，第三方复现未出**；⚠️ **它是「量化版」不是「新模型」**——"
    "**同一模型名的「不同量化档」是三条独立产品线**（避坑 124 同族） |",

    "| 🟢 **Cloudflare Clef-omni（四模态开源决策模型）** | 未公布 | 🟢 生效中（10/9 深夜，Hugging Face / GitHub）。"
    "**文本 + 图像 + 音频 + 视频四模态「一口吞」，不做 ASR 转写、不手动抽帧**（MP3 / MP4 直接喂）；"
    "基于 **Qwen3-Omni-30B-A3B-Instruct** 定制；官方实测**纯文本中位 130 ms / 单图 150 ms / 21 秒 MP4 端到端 1.5 s**；"
    "**权重开源**。⚠️ **它是 023 期登记的 Clef（27B）/ Clef-flash（9B）之后的「omni 第三代」——三条线不要混算**；"
    "⚠️ **响应时间与准确率均为厂商自报**；⚠️ **「不吃输出 token」不等于「便宜」**——**多模态输入按块 / 按秒计费**（避坑 132） |",

    "| 🟢 **AutoTrust AI Lab JEV-27B-VL（多模态决策模型）** | 未公布 | 🟢 生效中（10/10，ModelScope）。"
    "**基于 Qwen3.8-27B 的多模态决策模型**，沿用 **System 1（单次前向完成 yes/no、2–256 选项、0–5 评分 + 校准概率）** 与 "
    "**System 2 推理**，把输入扩展到图像；官方称 **Jev Decision Index 0.3 视觉榜单第一**。"
    "⚠️ **与 Cloudflare Clef-omni 同日出现，但两者是「同一条线（决策模型）的两个方向」**："
    "**Clef-omni 走「模态广度」、JEV-27B-VL 走「榜单位次」**——**名字里的 JEV 指决策模型基准，不是 TypeSafe 的 Jev 本体**（避坑 124） |",

    "| 🟢 **Qwen-Image-2.1-Turbo（8 步 / 7B 开源权重）** | 未公布 | 🟢 生效中（10/9，Hugging Face / ModelScope）。"
    "**Qwen-Image-2.1 的加速 checkpoint**：**去噪步数 40 → 8**，**同架构 7B 视觉生成器 + Qwen3-VL 8B 文本编码器**；"
    "**2K 出图 + 多参考图编辑 + 原生 RGBA 透明**（继承 2.1 全部能力）；**托管 API 每图 ¥0.10、120 RPM**（Pro 档 ¥0.25 / 20 RPM）；"
    "**Diffusers 接入（`QwenImage21Pipeline`）**。⚠️ **许可证仍是 Qwen Research License（仅研究 / 评估，商用须单独申请）**；"
    "⚠️ **8 步采样计划已烘焙进权重，改 `num_inference_steps` 无效，只能传显式 `sigmas`**；⚠️ **只有基座分（Qwen-Image-Bench 60.28）、无 Turbo 专项分** |",

    "| 🟢 **Google EmbeddingGemma 2（补登 10/6）** | 未公布 | 🟢 生效中（**10/6 发布、本期补登**）。"
    "**740M 开源多模态嵌入模型（Apache 2.0 可商用）**：**文本 / 代码 / 图像 / 视频 / 音频映到同一 768 维空间**；"
    "**模块化加载**（纯文本 270M / 加视觉 440M / 加音频 570M / 全量 740M）；**8K 上下文（4× 前代）**；"
    "**Matryoshka 可截到 512/256/128 维、存储最高省 6×**；**量化后文本档约 191MB、全模态约 567MB（Pixel 11 Pro 实测）**；"
    "**MTEB Code 68.76 → 78.68（+9.92）**。⚠️ **「手机端可跑」是厂商标称 + 单机型实测**；⚠️ **它是「本报告图像 / 多模态线漏登链条」的第三条同源样本**（见避坑 131） |",

    "| 🟢 **B站 Index-Translate 多语言翻译模型家族** | 未公布 | 🟢 生效中（10/8，ModelScope）。"
    "**哔哩哔哩 Index LLM 团队开源**：文本模型覆盖 **150 种语言**，**2B / 9B / 35B-A3B（preview）三种规模**；"
    "官方强调**保留网络热梗与语境**、长文人物名一致性、视频配音。⚠️ **「能接住热梗」是官方示例口径**；"
    "⚠️ **与 B站既有的「觉醒漫剧计划 2.0」是两件事**（一个是模型开源、一个是创作激励） |",

    "| 🟢 **OpenAI `o4-mini` API 停用** | **10/23** | 🟢 未开始（距今 13 天）。"
    "**`o4-mini` 在 ChatGPT 侧已下线，API 将于 10/23 停用**；官方替代为 **`gpt-5.6-terra`** 或更便宜的模型。"
    "⚠️ **这是继 10/14 GPT-5.5 之后的「同一周第二个下线日」**——**10 月中旬有两批迁移要排**（避坑 77：官方定档 ≠ 节点冻结） |",

    "| 🟢 **HeyGen Voice（AA 语音合成榜首，促销五折）** | **10/31** | 🟢 生效中（距今 21 天）。"
    "**HeyGen Voice 首发即登 Artificial Analysis 受控语音 TTS 榜首（Elo 1,201）**；**10/31 前 API 五折、$15 / 百万字符**。"
    "⚠️ **榜首为单一榜单口径**（避坑 116）；⚠️ **本报告主体是文本 / 图像 / 视频线，语音类只作登记** |",

    "| 🟢 **OpenAI Free / Go 档图像生成广告测试** | 未公布 | 🟢 生效中（OpenAI 10/5 公告，10/9 复核仍在）。"
    "**OpenAI 在 Free 与 Go 档测试「在图像生成过程中」的视觉广告格式**；官方定价页 Free 档备注出现「此计划可能包含广告」。"
    "⚠️ **这是「免费档的付费方从订阅者变成广告主」的第一个大厂样本**——**免费档的代价从「额度少」变成「注意力被占用」**（避坑 133）；"
    "⚠️ **仍处测试期、格式与投放范围随时可变** |",
]

DATE_RE = re.compile(r"(\d{1,2})/(\d{1,2})")
out = [header, sep]
applied_rewrite = set()
for r in body:
    name = r.strip().strip("|").split("|")[0].strip()
    hit = None
    for k in REWRITE:
        if name.startswith(k):
            hit = k
            break
    if hit:
        out.append(REWRITE[hit])
        applied_rewrite.add(hit)
        continue
    cells = r.strip().strip("|").split("|")
    if len(cells) == 3 and "距今" in cells[2]:
        m = DATE_RE.search(cells[1])
        if m:
            from datetime import date
            mm, dd = int(m.group(1)), int(m.group(2))
            try:
                d = date(2026, mm, dd)
                delta = (d - date(2026, 10, 10)).days
                cells[2] = re.sub(r"距今\s*\d+\s*天", f"距今 {delta} 天", cells[2])
                r = "|" + "|".join(cells) + "|"
            except ValueError:
                pass
    out.append(r)

missing = set(REWRITE) - applied_rewrite
assert not missing, missing
idx = next(i for i, l in enumerate(out) if l.startswith("| ⚪ **DeepSeek Harness"))
out = out[:idx] + NEW_ROWS + out[idx:]
assert len(out) - 2 == 120 + len(NEW_ROWS), len(out) - 2
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("rows:", len(out) - 2, "rewrites:", len(applied_rewrite), "new:", len(NEW_ROWS))
