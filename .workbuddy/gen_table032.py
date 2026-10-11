# -*- coding: utf-8 -*-
"""从 031 期 md 提取第四章截止表 -> 基准日 2026-10-12 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table032.md（纯表格块，供 032 期正文嵌入）。

五步（027 期定做法、028 期定型，029 / 030 / 031 期第二~四次落地，本期第五次）：
  1) 先断言行数（031 期 body = 153）
  2) 按行名前缀套 REWRITE 字典
  3) 正则重算每一行的「距今 N 天」（新基准日 10/12）
  4) 未 REWRITE 的行做「本期 -> （031 期）」归属化，避免继承字段被读成当期
  5) 新行插在 ⚪ 存档块之前 -> 再断言总数
"""
import re
from datetime import date

SRC = "AI免费内容与权益速递-第031期-2026-10-11.md"
OUT = ".workbuddy/tmp_table032.md"
BASE = date(2026, 10, 12)
PREV = 153

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
assert len(body) == PREV, len(body)

REWRITE = {}

REWRITE["🔴 **腾讯老混元大模型平台停服**"] = (
    "| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必须迁移到 TokenHub**。"
    "**10/12 高危窗口第 12 天**（9/25 自设倒排日已过 **17 天**；Q04 **连续第 20 期**未见确切日期，厂商只给「9 月底」）。"
    "⚠️ **一条「9 月底停服」拖到 10 月中旬仍无日期，处置已改为「按已停服对待、只做迁移」**——迁移动作本身不要等 |"
)

REWRITE["🔴 **OpenAI GPT-5.5 下线"] = (
    "| 🔴 **OpenAI GPT-5.5 下线（ChatGPT / ChatGPT Work / Codex）** | **10/14** | 🔴 **最重要的运维节点，剩 2 天**。"
    "⚠️ **API 不受影响**——官方建议 Codex 用户迁移到 `gpt-5.6-sol`（Free/Go 用 `gpt-6-luna`），"
    "并同步更新已保存的模型设置、托管配置、自定义 Agent、定时任务与脚本。"
    "⚠️ **Q17（Codex 官方 models 页是否更新迁移目标）连续 12 期未核到**；"
    "⚠️ **同一周还有第二个下线日**：**`o4-mini` 的 API 于 10/23 停用**（已单独登记）——**10 月中旬有两批迁移要排，别只记 10/14** |"
)

REWRITE["🟢 **OpenRouter 免费档"] = (
    "| 🟢 **OpenRouter 免费档（19 模型｜本期重取于 2026-10-12）** | 未公布（动态目录） | 🟢 生效中。免费档 **200 req/day**；**$10 充值换 5× 速率**。"
    "**本期经 freellm.net 的 OpenRouter 专页重取：19 个免费模型**（该站自己的 `Last Updated` 仍写 2026-10-11；避坑 68：带核对日期读）——"
    "**与 030 / 031 期数值相同，为连续第 3 期 19**。⚠️ **OpenRouter 自家目录页仍按类型分栏、不给「免费模型 N 个」这一个数**（Text / Image / Video / Speech / **Decisions** / Embeddings / Rerank / Audio），"
    "**故本行口径锚仍固定在 freellm.net 专页**。⚠️ **本期仍在清单里的 `poolside/laguna-s-2.1:free` / `laguna-xs-2.1:free` / `dots-studio/dots-3-note-preview:free` 等，是 016 期（9/25–9/26）就登记过的上架项，不是新发布**（避坑 125） |"
)

REWRITE["🟢 **珠海算力券**"] = (
    "| 🟢 **珠海算力券** | 申报至 **10/14 18:00** | 🟢 生效中（距今 2 天）。⚠️ 企业向，每年最高 200 万；"
    "**兑现截止时刻为 10/14 18:00**（030 期只写「10/14」，031 期补上时刻，本期维持） |"
)

REWRITE["🟢 **阶跃星辰 Step 5 权重开放**"] = (
    "| 🟢 **阶跃星辰 Step 5 权重开放** | **10/15** | 🟢 未开始（距今 3 天）。⚠️ 在此之前它只有 API 一条路；"
    "**600B 稀疏 MoE / 27B 激活 / 1M 上下文**。**031 期已补入官方口径**：**确认 10/15 正式开源、开源后可在自有算力上免费部署自跑**。"
    "⚠️ **「OpenRouter Trending 登顶」是渠道榜位口径、与权重是否开放无关**；⚠️ **许可证仍未公布**（避坑 42/135/142：**「将开源」三个字在 10/15 之前不成立**） |"
)

REWRITE["🟠 **上海张江 AI 创新小镇算力 / 模型 / 语料券"] = (
    "| 🔴 **上海张江 AI 创新小镇算力 / 模型 / 语料券（第 3 季度受理）** | **10/12 17:00** | 🔴 **今天收口（距今不足 12 小时）**。"
    "⚠️ **企业向 + 区域限定**（仅限张江 AI 创新小镇区域内企业）；**算力券 / 模型券 / 语料券三类可申报**；"
    "入口为**浦易达平台 `pyd.pudong.gov.cn`**。⚠️ **这是本报告表内截止时刻最近的一条** |"
)

REWRITE["⚪ **智谱 AutoClaw「每日登录领 credits」第一期**"] = (
    "| ⚪ **智谱 AutoClaw「每日登录领 credits」第一期** | **10/11 16:00 UTC（北京 10/12 00:00）** | ⚪ **已收口（本期回扫：无延期公告）**。"
    "**活动期 10/4 16:00 UTC – 10/11 16:00 UTC**；**10/4–10/6 每天登录领 5,000 credits，10/6 起每天 1,000 credits**；"
    "**credits 每日 16:00 UTC 发放、24 小时后作废**；官方按 **GLM-5.3-Flash 费率折算为「100M+ tokens」**。"
    "⚠️ **「100M+ tokens」是折算描述、不是 token 数量本身**（避坑 54）；⚠️ **每日发放、隔夜作废**（避坑 33 的教科书样本）。"
    "⚠️ **原一期最后一笔（10/11 16:00 UTC 发放）需在 10/12 16:00 UTC 前用掉** —— **「活动收口」不等于「已领的用完了」**（避坑 140） |"
)

REWRITE["🟠 **智谱 AutoClaw「每日登录领 credits」第二期**"] = (
    "| 🟢 **智谱 AutoClaw「每日登录领 credits」第二期** | **10/16（北京，活动期 10/12–10/16）** | 🟢 **生效中（本期回扫：10/12 已按预告开跑）**。"
    "**每日登录可领最多 1.32 亿 GLM-5.3-Flash Tokens**（按 GLM-5.3-Flash 费率折算）；**付费会员按会员等级额外解锁一份每日奖励**；"
    "**credits 每日发放、当天过期**。⚠️ **与第一期是两条不同的账**：**额度从「1,000 credits/天」变成「最多 1.32 亿 tokens/天」，量纲不同**（避坑 54），"
    "**且新增了付费会员加成** —— **窗口衔接不等于「同一活动延期」**（避坑 117/140）；⚠️ 出处为 **AutoClaw 官方活动页**，"
    "**官方未公布新一期的单日额度明细（1.32 亿是「最多」而非「每天」）** |"
)

# ---- 追加的新行（插在 ⚪ 存档块（首行 "| ⚪ **DeepSeek Harness"）之前）----
NEW_ROWS = [
    "| 🟢 **vLLM-SR `Decision 3.0`（六档 Apache-2.0 开放权重决策模型）** | 未公布（权重已上 HF `vllm-sr`） | 🟢 生效中（**10/10 09:38 → 23:49 UTC 六个检查点全部上传，10/11 vLLM 官方 X 转推**）。"
    "**`d3` 26.09B（0.46B 视觉编码器，`Qwen/Qwen3.8-27B`）/ `d3-flash` 8.39B（Qwen3.5-9B）/ `d3-mini` 4.54B（Qwen3.5-4B）/ `d3-nano` 2.21B（Qwen3.5-2B）/ `d3-lite` 0.85B / `d3-edge` 0.59B**；**全部 Apache-2.0**。"
    "**一次请求 = state（文本 / JSON，可带图像与视频）+ 一组命名问题 → 带类型的概率分布**；**三类问题 Choice / Noul / Score，每问一次前向、无解码循环**。"
    "**`Jev Decision Index 0.3.1` 上 d3 64.7 居首**（公开集 65.5 / 同技能 62.8 / 新领域 56.6；Perplexity Decider v1.1 62.8、Fastino GLiDE 60.2、Jev 60.1、Torchcast 59.9、Decision 2.0 55.9）。"
    "⚠️ **卡片自己注明：d3 行是内部评测，对手行是 10 月 10 日读的实时榜数据**；⚠️ **延迟（单请求 / 单块 MI325X）：文本 19.1 ms、图像 149.4 ms、10 秒视频 407.6 ms**；"
    "⚠️ **无 Brier / ECE**（避坑 141）；⚠️ **`max_length` 在随附配置里是 `null`，上下文上限要自测**；⚠️ **官网 blog 与 GitHub releases 至今没跟上，公告只发在 X**（避坑 143） |",

    "| 🟢 **AMI `H-JEPA`（分层世界模型 · 代码 + 权重开源）** | 未公布（代码与预训练权重已公开） | 🟢 生效中（**10/11**）。"
    "**AMI 联合纽约大学、巴黎 INRIA 与布朗大学**；**多层 JEPA 逐层堆叠，各层在自身表征空间预测不同时间跨度的状态**；"
    "**高层先出粗略计划、把预测的中间状态当子目标交给低层，低层接力细化成动作**；**沿用 SIGReg 避免表征坍塌**。"
    "**Visual AntMaze 仿真迷宫：三层成功率 73%、单层仅 18%**；**Push-T 上两层最好，加到三、四层成绩反降**。"
    "⚠️ **许可证本期未核到**（避坑 41）；⚠️ **AMI 官网尚无面向公众的产品入口**；⚠️ **它与 `Odyssey-3` 虽同日、都叫「世界模型」，但一条不生成像素，不可比大小**（避坑 144） |",

    "| 🟢 **Odyssey `Odyssey-3`（14B 世界模型 · 免费公开研究预览）** | 未公布（**研究预览期免费**；API 需申请） | 🟢 生效中（**10/11 07:50 UTC 起公开预览**；模型 9/15 首次亮相）。"
    "**14B 生成式世界模型**：**文字提示 → 实时生成可交互环境**，可第一 / 第三人称走动、触发事件、看模型实时反应；"
    "**自回归扩散 transformer，基于前一帧与用户最近动作逐帧生成**；**底座 832×480、Pro 1280×720**；**免费 demo 跑在 `Odyssey-3 Flash`**。"
    "⚠️ **`Physics-IQ Verified` 视频到视频 66.1 是「单次运行 + 八选一挑最好」**，**榜单规则要求四次并报标准差**，**去掉择选法后四次平均 63.37** —— **两组数都由 Odyssey 自己提交**（避坑 144）；"
    "⚠️ **`WorldMark` 四项拿三项第一**（第一人称风格化 77.2 / 第三人称真实 79.0 / 第三人称风格化 76.3），**第一人称真实 80.6 第三**；⚠️ **权重未开放** |",

    "| 🟢 **小思框架 `Moti-1`（摩谛 · 换掉层内自注意力的 7B 模型）** | 未公布（已开源） | 🟢 生效中（**10/11**，魔搭模型卡 + 作者技术稿）。"
    "**保留 `Qwen2.5-7B-Instruct` 的 FFN / Embedding / LayerNorm，把层内自注意力整体换成自研 RCA（跨层波前注意力，约 822M）**；"
    "**序列切 64-token 块，按「块 0 全部层 → 块 1 全部层」推进，浅层可直读深层成品 KV**；**原 q/k/v/o 权重作 RCA 分支初始权重**。"
    "**6 领域对照均分 43.2（原版 38.1，+5.1），前端代码方向最高领先 +24.7**；**RTX 3090 实测 30 tok/s**；**`trust_remote_code=True` 两行加载**。"
    "⚠️ **权重 18.57 GB、推理显存峰值约 18.6 GB；RCA 分支必须以 fp32 运行**（**存成 bf16 会落进 cuDNN 劣化路径，单层 63 ms vs 3.7 ms**）；"
    "⚠️ **单一来源、无第三方复现**（避坑 44） |",

    "| 🟠 **Google `Gemini 4 Argon`（前沿模型 · 分级访问）** | 未公布（**首发价 $2 / $10 每百万 token，缓存输入 $0.10；恢复价 $4 / $20**） | 🟠 **部分开放中**。"
    "**单次最多 100 万输出 token**（上一代 6.4 万；GPT-6 Astra / `gpt-6.1-sol` / Fable 5.1 / Opus 5.5 目前均 12.8 万）。"
    "**访问顺序：Fairwind 计划内网络安全防御者 + Google 内部团队（卸掉网络护栏的版本）→ 付费 API 客户与 Google AI Ultra → 普通消费者**，"
    "**三批均未公布日期**。⚠️ **先完成四个方向的安全强化**（滥调 / 提示注入 / 失准 / 沙箱）；⚠️ **Fairwind 为面向政府与可信伙伴的有限访问计划，全球 650+ 参与方**；"
    "⚠️ **「能查到模型名」不等于「能用上」**（避坑 142）—— **027 期的 Google limits 页已写「Argon 仅 Ultra」，但发布后四期都没登记**；"
    "⚠️ **编码项互有胜负**（FrontierSWE v2 55.0% 落后 Astra 65.5%、Terminal-Bench 4.0 57.4% 落后 Opus 5.5 66.4%） |",
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
            mm, dd = int(m.group(1)), int(m.group(2))
            try:
                d = date(2026, mm, dd)
                delta = (d - BASE).days
                cells[2] = re.sub(r"距今\s*-?\d+\s*天", f"距今 {delta} 天", cells[2])
                r = "|" + "|".join(cells) + "|"
            except ValueError:
                pass
    # 继承行归属化：未被本期改写的行里的「本期」指写入该行的那一期（031 期）
    r = r.replace("（本期", "（031 期").replace("本期", "（031 期）")
    out.append(r)

missing = set(REWRITE) - applied_rewrite
assert not missing, missing
idx = next(i for i, l in enumerate(out) if l.startswith("| ⚪ **DeepSeek Harness"))
out = out[:idx] + NEW_ROWS + out[idx:]
assert len(out) - 2 == PREV + len(NEW_ROWS), len(out) - 2

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("rows:", len(out) - 2, "rewrites:", len(applied_rewrite), "new:", len(NEW_ROWS))
