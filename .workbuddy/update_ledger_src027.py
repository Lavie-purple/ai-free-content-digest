# -*- coding: utf-8 -*-
"""027 期信源台账更新：
  1) 版本行 / 复核汇总行 追加 027 增量
  2) T4 标题计数 20 → 22
  3) T4 表尾新增 2 行（codingplan.link / creditforstartups.com）
  4) 就地更新：阶跃星辰、AIHOT（行内追加 027 注记）、freellm.net 计数器
"""
import io

P = "AI信息源分级清单-T0-T4.md"
ls = io.open(P, encoding="utf-8").read().split("\n")
N0 = len(ls)


def line_of(prefix, exact=False):
    hit = [i for i, l in enumerate(ls)
           if (l == prefix if exact else l.startswith(prefix))]
    assert len(hit) == 1, (prefix[:40], len(hit))
    return hit[0]


def cell1(prefix, want_cell, extra):
    """找到以 prefix 开头的行，取其第 want_cell 个 | 分隔单元（0 基，含首空），追加 extra"""
    i = line_of(prefix)
    c = ls[i].split("|")
    assert len(c) >= 7, (prefix[:30], len(c))
    assert extra[:20] not in c[want_cell], "已追加过"
    c[want_cell] = c[want_cell].rstrip() + extra
    ls[i] = "|".join(c)
    return i


# ---- 1. 版本行 ----
i = line_of("**版本**：v1 · 2026-09-15 建立")
assert ls[i].rstrip().endswith("**")
ls[i] = ls[i].rstrip() + ("；就地更新至 **2026-10-08（027 期，条目数 213 → 215；"
                          "新增 **codingplan.link**（T4，「AI Coding Plan 订阅档横向对照」第一现场，"
                          "把订阅额度换算成「每 5 小时多少次请求」）/ **creditforstartups.com**"
                          "（T4，厂商「面向创业公司 / 开发者生态的权益计划」对照源）；"
                          "**AIHOT 边界升级为第二十三次逐期计数确认**，操作禁令**第六次落地**——"
                          "本期首次记录「该源在同一天内也会把旧闻当新条目收录」；"
                          "**本期就地更新 2 行**：freellm.net、阶跃星辰）**")
print("  ~ 版本行追加")

# ---- 2. 复核汇总行 ----
i = line_of("T0 内部分类复核（025 期）")
ls[i] = ls[i].rstrip() + (" **027 期新增两条**：**T4 +2**（**codingplan.link**，订阅档横向对照；"
                          "**creditforstartups.com**，厂商创业权益计划对照源）→ **213 → 215**"
                          "（**T0 合计仍 118、T1 19、T2 18、T3 38 不变**）。"
                          "**027 期就地更新两行**：**freellm.net**（计数器 489 → **508 模型 / 30 提供方 / 更新至 2026-10-7**）、"
                          "**AIHOT（aihot.news）**（第二十三次逐期计数确认 + 操作禁令第六次落地）。")
print("  ~ 复核汇总行追加")

# ---- 3. T4 标题计数 ----
i = line_of("## T4 · 聚合器与工具（20）", exact=True)
ls[i] = ls[i].replace("（20）", "（22）")
print("  ~ T4 标题 20 -> 22")

# ---- 4. T4 表尾新增两行 ----
i = line_of("| 🆕 ClawLabsAI/free-ai-models")
NEW = [
    "| **🆕 codingplan.link** | http://codingplan.link/ | — | **「AI Coding Plan 订阅档横向对照」第一现场**（027 期首次命中）。"
    "把 **Tencent Cloud TokenHub / Volcengine Ark / 小米 MiMo / 白云智算** 等订阅的 **档位 / 每 5 小时限额 / 周月上限 / 首月促销价 / 支持模型清单** 并列，"
    "并标注「入门 / 推荐 / 最值」。**它补的是本报告长期缺的一个字段：把「订阅额度」换算成「每 5 小时多少次请求」**"
    "（与 022 期缺口「Agent Harness / 模型托管平台官方页」互补：那一类答「谁能跑什么」，这一类答「花了钱能跑多少」）。"
    "**027 期用它核对了 TokenHub Coding Plan 的 ¥7.9 首月与火山方舟 ¥8.91 首月两档**。⚠️ **第三方对照站，档位与价格须回厂商页复核** | 027 | 0 |",
    "| **🆕 creditforstartups.com** | https://creditforstartups.com/ | — | **「厂商面向创业公司 / 开发者生态的权益计划」对照源**（027 期首次命中）——"
    "**正是 026 期新增的第 9 类清单缺口所要的那一条**。逐条给出 **Anthropic / OpenAI / Google 等创业计划的额度上限、门槛、有效期、是否需要 VC、能不能用在云市场**，"
    "并把 **「是 API credit 不是现金」「6 个月过期」「不适用 Bedrock / Vertex」** 这类边界写在同一页。"
    "**027 期用它补全了 Claude Startup Stack 的 6 项限制（含「不可用地区名单含中国」）**。"
    "**与 026 期的 CNBC 互补：CNBC 是「消息第一落点」，本站在「条款对照」** | 027 | 0 |",
]
for r in NEW:
    ls.insert(i + 1, r)
    i += 1
print("  + T4 新增 2 行")

# ---- 5. 就地更新：阶跃星辰 / AIHOT / freellm.net ----
cell1("| 阶跃星辰 |", 4,
      "；**027 期状态变更**：**Step Plan 已关闭新增领取通道**——「注册 99 元套餐 + 首登 15 天 + 首调 15 天 + "
      "邀请最多 45 天 = 最高 75 天」这条路径**已不可执行**（已领用户剩余权益以账户内为准）；"
      "**替代体验：Step 5 Preview 已接入北京 AGI Bar，店内一周对所有用户免费**（单一信源、线下为主）；**权重仍定档 10/15 开放**")

cell1("| AI-HOT（168 信源分级）", 4,
      " **⚠️ 027 期第二十三次逐期计数确认（操作禁令第六次落地）**：10/8 全天 21 条、最后一条 18:24，"
      "**其中与「免费额度 / 领取 / 权益活动」直接相关的为 0 条**——本期全部免费额度与权益增量"
      "（Max/Team 额度、智谱清言返还、上海张江算力券、TokenHub 促销）**没有一条来自这一层**；"
      "**但本期它确实带出了第一章两条主干（Anthropic Haiku 5.5 / Sonnet 5.5 缓存降价、OpenAI GPT-6 全量 + Intelligent UI + Decisions API）"
      "与第二章的 3 条（Liquid `d1` 开源、`pplx-embed-v2-late`、Unsloth 决策微调）**——边界第五次以定论形式复用。"
      "**⚠️ 027 期新增一条实质结论**：**该源在同一天内也会把旧闻当新条目收录**——本期「旧闻澄清 3 条」"
      "（Qwen-Image-Layered / 混元 Hy3 开源 / Qwen3）中有 2 条的传播路径经过同类聚合层。"
      "**对出刊纪律的含义：这条源可以用作「今天有什么」的入口，但不能用作「这是今天发生的」的证据**"
      "——**「是不是今天发生」必须回官方页或条目原文发布时间戳**（避坑 125 的操作定义）")

i = line_of("| **免费额度垂直追踪站**")
old = "freellm.net（484+ 免费模型、228 条实时验证）"
assert old in ls[i], "freellm 计数器串未找到"
ls[i] = ls[i].replace(old, "freellm.net（**027 期计数器：508 模型 / 30 提供方 / 更新至 2026-10-7**）", 1)
print("  ~ freellm.net 计数器更新")

io.open(P, "w", encoding="utf-8").write("\n".join(ls))
print("OK  台账行数 %d -> %d" % (N0, len(ls)))
