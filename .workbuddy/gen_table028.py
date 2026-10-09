# -*- coding: utf-8 -*-
"""从 027 期 md 提取第四章截止表 -> 基准日推进到 2026-10-09 -> 应用行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table028.md（纯表格块，供 028 期正文嵌入）。"""
import re, sys, os

SRC = "AI免费内容与权益速递-第027期-2026-10-08.md"
OUT = ".workbuddy/tmp_table028.md"
BASE = "2026-10-09"

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
assert len(body) == 109, len(body)

# 需要整行改写（键=行首唯一片段）
REWRITE = {}

REWRITE["🔴 **腾讯老混元大模型平台停服**"] = (
    "| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必须迁移到 TokenHub**。"
    "**10/9 高危窗口已开启第 8 天**（9/25 自设倒排日已过 **14 天**；Q04 连续第 16 期未见确切日期，厂商只给「9 月底」）。"
    "⚠️ **10 月中旬仍未给出停服日，本条已从「运维提醒」变成「长期悬案」**——迁移动作本身不要等 |"
)

REWRITE["🔴 **OpenAI GPT-5.5 下线"] = (
    "| 🔴 **OpenAI GPT-5.5 下线（ChatGPT / ChatGPT Work / Codex）** | **10/14** | 🔴 **最重要的运维节点**。"
    "⚠️ **API 不受影响**——官方建议 Codex 用户迁移到 `gpt-5.6-sol`（Free/Go 用 `gpt-6-luna`），"
    "并同步更新已保存的模型设置、托管配置、自定义 Agent、定时任务与脚本。官方一手来源维持定档；"
    "⚠️ **Q17（Codex 官方 models 页是否更新迁移目标）连续 8 期未核到**。"
    "⚠️ **本期新增两条相关事实**：① **GPT-6.1 Astra 仍处搁置，不进入 ChatGPT 全量推送**（027 期已记）；"
    "② **10/8 起 `gpt-6.1-sol` 上了一个 Ultrafast 提速档**（API 侧 `service_tier: \"ultrafast\"`，"
    "**6 倍价、官方称最高 8 倍速**）——**它说明 `gpt-6.1-sol` 已是独立在售的 API 模型名，"
    "但没有改变官方给出的 5.5 迁移目标**（迁移仍按 `gpt-5.6-sol` / `gpt-6-luna` 执行，"
    "**不要因为看到 `gpt-6.1-sol` 就自行改道**）。**窗口剩 5 天** |"
)

REWRITE["🟠 **Google Gemini 免费档收缩"] = (
    "| 🟠 **Google Gemini 免费档收缩（免费档仅剩 Flash-Lite）** | **10/9** | 🟠 **今天（10/9）就是换挡日**——"
    "**个人未订阅账号在 Gemini 应用内只剩 Flash-Lite**，Flash 与 Pro 转入付费档；"
    "**AI Plus 保留 Flash-Lite + Flash、失去 Pro**（按邮件分批生效，**生效日不统一**）；"
    "**Deep Think 已下放 AI Pro / Ultra**（不再仅 Ultra）。**免费档上下文 32K**（Plus 128K / Pro 与 Ultra 1M）；"
    "**每档模型可设 low / medium / high effort，effort 越高越吃额度**；额度按**算力消耗**计量、"
    "**每 5 小时刷新一次并另有周上限**。⚠️ **10/8 之前 Google 主 limits 表与订阅页仍写着免费可用 Flash / Pro**"
    "（多源交叉：中时 / ai-toolbox / clurky / ai.jp.net）——**以 10/9 生效的模型表为准**；"
    "⚠️ **Workspace 托管账号不在本次变更范围** |"
)

REWRITE["🟢 **阿里云 AgentCore 协作管控面限时免费**"] = (
    "| 🟢 **阿里云 AgentCore 协作管控面限时免费** | **10/18 23:59:59** | 🟢 生效中（距今 9 天）。"
    "⚠️ 不含 Agent 运行时算力/存储/网关；连续 30 天无操作停用并自动回收，不可逆。"
    "⚠️ **本期新增一条安全侧事实（同一产品族）**：**Zenity Labs 发现 Bedrock AgentCore 上"
    "「单个公开可达的 agent 足以越权接管同一 AWS 账号与区域内全部 AgentCore agent」**"
    "（利用内部临时凭证接口），**AWS 已打补丁并显著收紧 agent 默认权限**。"
    "**用它做生产前，先确认自己的默认权限与公开可达面** |"
)

REWRITE["🟢 **Mistral Large 4 公开预览"] = (
    "| 🟢 **Mistral Large 4 公开预览（含 OpenRouter 五折）** | **权重月底（官方 10/8 口径「十月底」；媒体口径 10/27）；五折限前两周** | "
    "🟢 生效中（025 期登记）。1T 总参 / 49B 激活、原生多模态；⚠️ **许可证仍未公布**（避坑 42）。"
    "⚠️ **本期补一条第三方实测**：**Arena 的 Agent Arena（5000+ 真实智能体会话）把它列进前十五实验室，"
    "净改进分 −6.6%、总排名第 43**，比上一代 Mistral Medium 3.5（−12.60%）高 11 位——"
    "**\"美欧最强开放权重\"是厂商口径，\"净改进分仍为负\"是榜单口径，两句话都要写**（避坑 116） |"
)

REWRITE["⚠️ **阶跃星辰 Step 5 Preview 新用户免费套餐**"] = (
    "| ⚠️ **阶跃星辰 Step 5 Preview 新用户免费套餐** | 未公布 | ⚠️ **口径变更（027 期）**：**官方已关闭新增领取通道**——"
    "已领用户的剩余权益以账户内为准，**不再按「最高 75 天」口径新拉人**。⚠️ **替代路径本期起多了一条**："
    "**Step 5 Preview 已上线 OpenRouter，并在 OpenCode / Cline / Kilocode / Nous Research 等渠道开放一周免费**（见下表新行）——"
    "**\"官方通道关了\"不等于\"没地方免费用\"** |"
)

REWRITE["🟢 **阶跃 Step 5 Preview（AGI Bar 线下免费体验）**"] = (
    "| 🟢 **阶跃 Step 5 Preview（AGI Bar 线下免费体验）** | 未公布（店内口径，约一周） | 🟢 生效中（027 期登记）。"
    "**店内连 WiFi、配好 Base URL 与 API Key 即可调用，未来一周对所有用户免费**。"
    "⚠️ **单一信源 + 线下为主**；⚠️ **线上免费入口本期已由 OpenRouter 那条补齐，不必再依赖线下** |"
)

# 追加的新行（插在 🟢 块末尾、⚪ 存档块之前）
NEW_ROWS = [
    "| 🟢 **阶跃星辰 Step 5 Preview（OpenRouter / OpenCode / Cline / Kilocode / Nous Research 免费一周）** | "
    "未公布（公告未给结束日） | 🟢 生效中（10/8 上线）。**600B 总参 / 27B 激活 MoE、1M 上下文、文本 + 图像输入**"
    "（StepFun 原生指南与 OpenRouter 另列视频）；**OpenRouter 定价 $1.00/M 输入、$2.70/M 输出，缓存命中 $0.05/M（首发五折）**；"
    "**对 427 分那一档的能力，AA 实测每任务 $1.03，比 GPT-5.6 Terra 便宜 26%、比 Sol 便宜 48%**。"
    "⚠️ **免费窗口长度按渠道不同**（**OpenCode 明确一周且声明零数据留存、Cline 未写期限**，避坑 126）；"
    "⚠️ **权重 10/15 才发、未公布许可证**；⚠️ **AA 同时测出它产出 token 是 Sol 的 1.7 倍**——**单价低不等于账单低**（避坑 119 同族） |",

    "| 🟢 **GMI Cloud 免费档延长（Qwen3.8-Max / Qwen3.8-Flash / Wan3.0）** | 未公布（本次再延 7 天） | "
    "🟢 生效中。**三个模型免费窗口各延长 7 天并提高速率上限**；**GMI API Key 可在 OpenCode / Hermes Agent 等工具内直接调用**；"
    "同期**社区赛：用 Qwen 或 Wan 做项目，3 名各得 $200 现金 + $200 GMI credits**。"
    "⚠️ **「再延 7 天」不是新活动**——**它是同一个滚动窗口的第二次续期**（12 小时 → 一周 → +7 天），"
    "**别把它当成又开了一轮**（避坑 117 同族） |",

    "| 🟢 **OpenAI `gpt-6.1-sol` Ultrafast 提速档** | 未公布 | 🟢 生效中（10/8）。**同一个 `gpt-6.1-sol` 模型名，"
    "API 侧按请求传 `service_tier: \"ultrafast\"` 切换**；**官方称最高 8× 标准版速度**（**未公布 p50 / p95**）；"
    "**定价 6× 标准档：$12/M 输入、$60/M 输出；长上下文 $24 / $90；短上下文缓存读 $0.60/M、缓存写 $15/M**。"
    "⚠️ **Codex 与 ChatGPT Work 只对 Pro $500、符合条件的按量付费企业版、配额计费教育版开放，企业管理员默认关闭**；"
    "⚠️ **消费端 Chat 不在本次范围**；⚠️ **订阅内用量按 8× 扣减、购买 credit 按 6× 计费**（避坑 127）；"
    "⚠️ **Astra Ultrafast 不支持欧盟数据驻留，Sol Ultrafast 支持**——**对欧洲团队这是它唯一能买到的 Ultrafast 配置** |",

    "| 🟢 **Anthropic OSS Scanner（开源项目免费漏洞扫描）+ Claude for OSS** | 未公布（长期） | 🟢 生效中（10/8）。"
    "**开源项目 opt-in 后获定期安全扫描，完全免费**；报告**全模型生成、无人工复核**，含**可自证复现脚本、"
    "bisection 定位引入版本、候选补丁**；Anthropic 自报**早期 97 条高危中 88% 达到其 CVD 标准、仅 1 条误报**，"
    "**wolfSSL 收到的 74 条里 72 条有效、5 条成了 CVE**。**合格维护者另可领免费 Claude Max 20x 订阅（Claude for OSS）**，"
    "并有一个 **Defender Advantage Fund** 支撑试点。⚠️ **无人工复核是它的定价代价**——**\"免费\"换的是\"你自己做 triage\"**"
    "（避坑 41 同族）；⚠️ **它是独立于 Claude Security 的产品线**，不要混算 |",

    "| 🟢 **Claude Dashboards / Motion（beta）+ Docs·Slides·Design 全计划开放** | 未公布 | 🟢 生效中（10/8）。"
    "**Docs / Slides / Design 已退出 beta、对所有计划开放（含 Free）**，官方称已产出 4,500 万+ 文档/演示/设计；"
    "**Dashboards 为付费档 beta**（连 Redshift / BigQuery / ClickHouse / Databricks / Snowflake，"
    "另可连 Salesforce 等连接器，每个图表可看底层查询）；**Motion 仅 Team 与 Enterprise**。"
    "⚠️ **\"对所有计划开放\"≠\"三个功能都免费\"**（避坑 128）；⚠️ Enterprise 侧 **Docs/Slides/Design 10/15 才默认开启**，"
    "**Dashboards 与 Motion 默认关闭**；⚠️ **独立站 claude.ai/design 仅保留到 12/14，旧项目与评论不迁移** |",

    "| 🟢 **江苏省词元（Token）券 / 语料券 / 模型券** | 未公布（按批次受理，省级统筹） | 🟢 生效中"
    "（**省发改委等五部门发文日期 9/30、官网公开 10/9**）。**省级三券并行**，"
    "支持对象含**企业 / 高校院所 / 研究机构 / OPC**；**省级财政对设区市实际兑付给予支持（预拨 + 清算）**，"
    "鼓励纳入**江苏省一体化算力监测调度平台**。⚠️ **企业向 + 省级统筹**；"
    "**这是本报告表内第 6 条地方券**（青浦 / 湖北 / 珠海 / 上海张江 / 龙湖区政府词元券 + 江苏）——"
    "**地方券聚合入口仍缺**（第 3 类清单缺口维持） |",

    "| 🟢 **Google Nano Banana 2 停用（Gemini API）** | **10/29** | 🟢 未开始（距今 20 天）。"
    "**Nano Banana 2（`gemini-3.1-flash-image`）在 Gemini API 中已 deprecated，10/29 正式停用**，迁移目标为 **Nano Banana 2.1**。"
    "⚠️ **Google 未公布具体停机时刻**；⚠️ **这是本期\"图像模型线漏登链条\"上的第一个明确运维节点**"
    "（027 补登混元图像 3.0、本期补登 Nano Banana 2.1，两次同源，见避坑 129） |",

    "| 🟢 **OpenAI 学生 $100 Codex 额度（美国 / 加拿大）** | 领取后 12 个月 | 🟢 生效中。"
    "**在读大学生经学校邮箱验证后可领 $100 ChatGPT credits，限定用于 Codex，每人一次、12 个月过期**。"
    "⚠️ **仅美加学籍**；⚠️ **来源为优惠聚合站（DealSelected / Hunt4Freebies 等），官方页未核到**（避坑 44 同族）。"
    "⚠️ 同期另有一条：**InkPal Pro 学生免费 12 个月**（.edu 邮箱申请）——**与本报告主体无关，仅登记** |",

    "| 🟢 **Arena（LMArena）Alignment Index** | 未公布 | 🟢 生效中（10/8）。**用 27 个模型、9 万+ 条真实 agent 会话**评三个信号："
    "**未授权动作 / 错误归因 / 虚假完成**；**榜首 GPT-6.1 Sol 87.9、Claude Opus 5.5 83.2、Grok 4.7 82.7，前五全为 OpenAI**。"
    "⚠️ **它与\"能力榜\"是两件事**——**它测\"有没有越界与谎报\"，不测\"能不能做对\"**（避坑 116 同族）；"
    "⚠️ 同期 Arena 宣布 **$2 亿 B 轮、估值 31 亿美元**（Lightspeed 与 Khosla 联合领投） |",

    "| 🟢 **Google ML Drift（端侧 GPU 推理引擎）+ AQuA（环境质量智能体）** | 未公布 | 🟢 生效中（10/8）。"
    "**ML Drift 以 Apache 2.0 开源**，是 **LiteRT 的跨平台端侧 GPU 加速层、接替 TFLite GPU delegate**；"
    "**AQuA 开源**，从 Cloud Trace / Cloud Logging / BigQuery 抽生产会话，经**抽样-评审-聚类-验证-跟踪五阶段**诊断 agent 失败。"
    "⚠️ **两条都是\"能跑\"层，不含权重许可证问题、也不含额度** |",

    "| 🟢 **Anthropic 新版使用政策（含首次禁止虐待模型）** | **11/12 生效** | 🟢 未开始（距今 34 天）。"
    "**新增「禁止持续且无必要地虐待或残酷对待模型」**，处置方式为**终止当前会话**（不影响账号内其他会话、不封号）；"
    "把分散的选举 / 欺诈 / 隐私 / 虚假信息条款**合并为统一的「欺骗性活动」章节**；**武器与监控条款收紧**；"
    "**自主物理动作需人在环、可随时介入**。⚠️ **官方明确：普通反驳、表达不满、研究测试、暗黑题材创作都不在禁止范围**；"
    "⚠️ **与额度无关，但改变「能不能用」的边界**（避坑 41 第一问） |",
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
    # 距今 N 天 重算：从「截止」列解析 M/D（同年），基准日 2026-10-09
    cells = r.strip().strip("|").split("|")
    if len(cells) == 3 and "距今" in cells[2]:
        m = DATE_RE.search(cells[1])
        if m:
            from datetime import date
            mm, dd = int(m.group(1)), int(m.group(2))
            try:
                d = date(2026, mm, dd)
                delta = (d - date(2026, 10, 9)).days
                cells[2] = re.sub(r"距今\s*\d+\s*天", f"距今 {delta} 天", cells[2])
                r = "|" + "|".join(cells) + "|"
            except ValueError:
                pass
    out.append(r)

missing = set(REWRITE) - applied_rewrite
assert not missing, missing
# 追加新行：插到 ⚪ 存档块之前（找第一条以 "| ⚪ **DeepSeek Harness" 开头的行）
idx = next(i for i, l in enumerate(out) if l.startswith("| ⚪ **DeepSeek Harness"))
out = out[:idx] + NEW_ROWS + out[idx:]
assert len(out) - 2 == 109 + len(NEW_ROWS), len(out) - 2
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("rows:", len(out) - 2, "rewrites:", len(applied_rewrite), "new:", len(NEW_ROWS))
