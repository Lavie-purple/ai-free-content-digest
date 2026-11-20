# -*- coding: utf-8 -*-
"""074 期：在 073 期现行 4.1/4.2 表体上做「天数带符号重算 + 行级改写 + 补入 3 行」。

纪律（055–073 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 补入行必须带「074 期」标记；⑥ 状态列整体替换；
  ⑦ 单元格不许出现 `|`；⑧ 天数一律由基准日实算、断言带符号；
  ⑨ 状态列不写「未开始 / 已结束」；状态列里非本期期号引用 ≤ 1 处（lint R3）。
"""
import io
import re
import sys
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第074期-2026-11-20.md"
PTR = " [附录 074](details.html) |"
TODAY = date(2026, 11, 20)
DRY = "--apply" not in sys.argv

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")


def rows_of(text, start, end):
    i = text.index(start)
    j = text.index(end)
    return [l for l in text[i:j].split("\n")
            if l.startswith("|") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]


r41 = rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
r42 = rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("输入行数：4.1 = %d，4.2 = %d" % (len(r41), len(r42)))
assert len(r41) == 66, ("073 期 4.1 行数", len(r41))
assert len(r42) == 48, ("073 期 4.2 行数", len(r42))


def cells_of(r):
    return [c.strip() for c in r.strip().strip("|").split("|")]


def name_of(r):
    return cells_of(r)[0]


def days_of(deadline):
    m = re.search(r"(\d{1,2})\s*/\s*(\d{1,2})", deadline)
    if not m:
        m2 = re.search(r"(\d{1,2})\s*月\s*(\d{1,2})\s*日", deadline)
        if not m2:
            return None
        mo, d = int(m2.group(1)), int(m2.group(2))
    else:
        mo, d = int(m.group(1)), int(m.group(2))
    if not (1 <= mo <= 12 and 1 <= d <= 31):
        return None
    try:
        return (date(TODAY.year, mo, d) - TODAY).days
    except ValueError:
        return None


# ------------------------------------------------------------ ① 天数带符号重算
changed = 0
skipped = []
TOK = re.compile(r"(距截止|已过|距今|距承诺日)\s*`?(\d+)`?\s*天")


def fix_days(st, delta):
    if delta > 0:
        return TOK.sub(lambda m: "%s `%d` 天" % (m.group(1), delta), st)
    if delta == 0:
        return TOK.sub(lambda m: "今日（`11/20`）为截止日", st)
    return TOK.sub(lambda m: "已过 `%d` 天" % (-delta), st)


for bucket in (r41, r42):
    for k, row in enumerate(bucket):
        c = cells_of(row)
        if len(c) != 3:
            continue
        delta = days_of(c[1])
        if delta is None:
            skipped.append(name_of(row)[:26])
            continue
        new_st = fix_days(c[2], delta)
        new_dl = c[1]
        if delta < 0:
            new_dl = re.sub(r"已过\s*`?\d+`?\s*天", "已过 `%d` 天" % (-delta), new_dl)
            new_dl = re.sub(r"距截止\s*`?\d+`?\s*天", "已过 `%d` 天" % (-delta), new_dl)
        elif delta == 0:
            new_dl = re.sub(r"距截止\s*`?\d+`?\s*天", "今日为截止日", new_dl)
        if new_st != c[2] or new_dl != c[1]:
            bucket[k] = "|" + "|".join([c[0], new_dl, new_st]) + "|"
            changed += 1
print("天数改写行数 =", changed, "｜无日期可算 =", len(skipped))
print("无日期行：", skipped)


# ------------------------------------------------------------ ② 行级改写
EDITED = []


def edit(tag, prefix, status, bucket, deadline=None, name=None):
    hits = [k for k, r in enumerate(bucket) if prefix in name_of(r)]
    assert len(hits) == 1, ("命中数不是 1", tag, len(hits))
    c = cells_of(bucket[hits[0]])
    assert len(c) == 3, ("字段数异常", tag, len(c))
    assert "|" not in status, ("状态列里出现竖线", tag)
    dl = deadline if deadline is not None else c[1]
    assert "|" not in dl, ("截止列里出现竖线", tag)
    nm = name if name is not None else c[0]
    assert "|" not in nm, ("活动名列里出现竖线", tag)
    new = "|%s| %s | %s%s" % (nm, dl, status, PTR)
    assert new != bucket[hits[0]], ("改写未生效", tag)
    bucket[hits[0]] = new
    EDITED.append(tag)


# ---- 腾讯老混元：截止列不可解析，天数与期数手工推进
hits = [k for k, r in enumerate(r41) if "腾讯老混元" in name_of(r)]
assert len(hits) == 1
row = r41[hits[0]]
assert "已过 `50` 天" in row and "第 `46` 期" in row and "第 `37` 天" in row, row[:200]
row = row.replace("已过 `50` 天", "已过 `51` 天").replace("第 `46` 期", "第 `47` 期").replace("第 `37` 天", "第 `38` 天")
row = row.replace("`hunyuan.tencent.com` 本期 **`6,584` 字节**（上期记 `6,894`）—— **字节变了、仍是 `app-skeleton` 骨架屏**，六项关键词各 `0` 命中（第 `5` 期）。",
                  "`hunyuan.tencent.com` 本期 **`6,584` 字节**（与上期逐字节相同）—— **仍是 `app-skeleton` 骨架屏**，六项关键词各 `0` 命中（第 `6` 期）。")
row = row.replace(" [附录 073](details.html) |", PTR)
r41[hits[0]] = row
EDITED.append("腾讯老混元(手算)")

# ---- 4.1：Hy4 flash WorkBuddy 限免
edit("Hy4 flash 限免", "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
     "🟠 **距截止 `9` 天。 限免只限 `WorkBuddy` 内的 `Hy4 flash`**；其他模型与腾讯云 `TokenHub` 不在内（`TokenHub` 是**限时 `5` 折**）。 "
     "**参数取官方口径**：`220.25B` 实测 / 激活 `11.3B` + `0.43B`（媒体 `224B` / `12B` 不再作主口径）。 "
     "**权重已开放（三仓）**，48 小时读数见 `4.2` —— **限免到期后能用的是权重，不是本行额度**。", r41,
     name="🟠 **腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费（**`220.25B` 实测总参（含 `64B` Engram）/ 激活 `11.3B` + `0.43B` / `1M` 上下文 · 官方口径「`11/30` 前」**）**")

# ---- 4.1：MiniMax 4K —— 旧版收口（新版进 4.2）
edit("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
     "⚪ **旧版已过期（`11/18 00:00` 到期）；但同一促销已于本期换文案重挂，新版本见 `4.2`。 三个读数本期全部回涨**：`0.2261` / `0.2404` / `限时5折` 重新出现，页 `305,754 → 310,127`（`+4,373`）。 "
     "**所以本行只记「旧版过期」这一件事**，不代表该折扣已停 —— **判「活动结束」要连续两期不再出现**（避坑 317）。 "
     "旧文案的截止时刻逐字是「即日起至 2026 年 11 月 18 日 00:00」，**新文案里这句话整句不存在**（避坑 318）。", r41,
     deadline="**`11/18 00:00`（北京 · 旧版逐字「即日起至 2026 年 11 月 18 日 00:00」· 已过 `2` 天）**")

# ---- 4.1：Runware 4K 50%
edit("Runware 4K 50%", "`Runware` 分发层 `MiniMax H3-Image`",
     "🟠 **已过 `3` 天（`11/17` 到期）。 三个读数连续第 `3` 期不变：`h3-image` 命中 `18`、卡片徽标 `0`、价目一个数没变**"
     "（`0.2261` / `0.4522` 整页 `0` 命中）—— **「账本 vs 货架」第 `15` 次实证**。 "
     "**本期新增读数：数组在滚动** —— `2026-11-17` 从 `7` 处降到 `5` 处、`2026-11-19` 从 `1` 处升到 `5` 处；**「共 `22` 条」不是常量，别再按条数记账**（纠错③）。 "
     "价目不动是对的：官方帮助文案逐字「部分规格促销只挂徽标、不改价」→ **这类促销只有徽标能判下架**（避坑 312/315）。", r41,
     deadline="**`11/17`（官方促销数组 `endsAt: \"2026-11-17\"` 逐字 · 已过 `3` 天）**")

# ---- 4.1：Antigravity 三模型 —— 到期未执行（第 2 天）
edit("Antigravity 三模型", "`Google Antigravity` 免费档三个第三方模型 `11/18` 移除",
     "🔴 **到期第 `2` 天，页面仍未执行、措辞未改。 定价页 `183,218` 字节与上期完全相同、`md5` 变、去标签逐行 diff ＝ `0` 行**："
     "免费档 `Models included` 仍列四个 —— `Gemini 3.8 Flash` / `Claude Sonnet 4.6 (thinking)` / `Claude Opus 4.6 (thinking)` / `GPT-OSS-120b`；"
     "脚注 `4` 逐字仍是 `Will be removed on November 18, 2026.`。 **结论只到「页面口径」：三个模型仍可用，但官方自己写着要撤。** 免费档仍无配额数字。", r41,
     deadline="**`11/18`（官方脚注逐字 `Will be removed on November 18, 2026.` · 已过 `2` 天 · 本期核到未执行）**")

# ---- 4.1：ERNIE 5.5
edit("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `5` 天）。 官方发布页 `11月25日前开源` 逐字仍在**（本期 `54,010` 字节，与上期逐字节相同，第 `3` 期）。 "
     "**权重仍未放**：`?author=baidu` 仍 `39` 个仓库（连续第 `17` 天 `0` 变化）。 "
     "两个 `Base` 仓 `downloads` 继续涨（`5,075` / `1,920`）—— **`Base` ≠ `Preview`，别拿它当「已开源」的证据**。", r41)

# ---- 4.1：AutoClaw M11W3（本周）
edit("AutoClaw M11W3", "智谱 `AutoClaw` 国内站 `M11W3`",
     "🟠 **距截止 `2` 天。 官方博客 `M11W3` 逐字：`11 月 16 日至 11 月 22 日` 登录领 `100M` Tokens（`10,000` 积分）**，奖励 `11/22 23:59` 失效。 "
     "**下一期 `M11W4` 已于 `11/20` 挂出（`11/23`–`11/29`，仍 `100M`）** —— 两期首尾相接、**中间只隔 `1` 分钟**，本周领的额度本周日即作废。 "
     "额度锁在客户端内，导不出 `API`。", r41)

# ---- 4.2：OpenRouter 免费档
edit("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **全量 `480 → 477`（`−3`）；`:free` `12`（`14 → 12`，`−2`）；零价 `15`；`?max_price=0` `14`。 "
     "少的两个 `:free` 可逐条点名**：`cohere/north-mini-code:free`、`thinkingmachines/inkling-2-small:free`（两条 `/endpoints` 均返 `0` 路由）；"
     "**另少** `meta-llama/llama-3.2-1b-instruct`、`x-ai/grok-build-0.1`；**新增** `mistralai/pixtral-large-2502`（付费 `$2`/`$6`、`128K`、北京 `11/20 08:51`）。 "
     "`gpt-6.2` 仍 `8` 条、**仍无 `:free`**（第 `3` 天）。 `Ling 3.2 Flash` 的 `endpoints` **`0 → 1` 条（空窗结束）**。", r42,
     name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `477/15/12`**）**")

edit("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `12` 期：页头「今天还能领」`¥1737` 持平（第 `2` 期同值）、"
     "卡册 `60 → 62` 张（`+2`）** —— **面额与卡数第一次「不同向」**（上期是同降）。 "
     "**该合计是动态折算值、卡册是账户态**，只记读数、不推趋势。 页 `477,419 → 493,259`（`+15,840`）。", r42)

edit("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
     "🟢 **官方定价页逐字 `$0/month`（`183,218` 字节，与上期同字节、`md5` 变、可见文本 diff `0` 行）。 免费档四个模型**：`Gemini 3.8 Flash` + 三个第三方（`Sonnet 4.6` / `Opus 4.6` / `GPT-OSS-120b`）。 "
     "`Baseline agent quota refreshed weekly` **仍无数字**。 **该页连续 `3` 期可读、正文连续 `2` 期零变化**（避坑 320 实证）。", r42)

edit("ERNIE-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓库。 `FP8` `5,075`（`+432`）/ `360` 赞（`0`）；"
     "`BF16` `1,920`（`+206`）/ `394` 赞（`0`）**。 两仓 `lastModified` 仍停 `11/05` —— **仓库没变、下载在涨**，是滚动窗口重算。", r42)

edit("Inkling", "`thinkingmachines/Inkling-2-Small` 开放权重",
     "🟢 **`Apache-2.0` · `gated: false`。 `downloads 30,082 → 40,574`（`+10,492`）/ `likes 552 → 598`**；`lastModified` **`11/20 01:16Z`（本期窗口内）**。 "
     "**同一天它从 `OpenRouter` 免费区消失、但在 `OpenCode` 免费池里仍在** —— 两个目录两套账，**时间对得上，不写因果**（避坑 116）。", r42)

edit("OpenCode 免费清单", "`OpenCode` 免费模型清单",
     "🟡 **`Free models` 段仍 `12` 条**（段落逐条；`-free` 正则只得 `11`，`Big Pickle` 无后缀）。 **页 `102,667` 字节 / `md5 6105ecab` 与上期字节 + `md5` 双同** —— 这次「不变」是能证明的。 "
     "`GLM-5.3-Flash Free` **仍不在段内**、`Deprecated models` 表那行（`November 18, 2026`）**仍在** —— 两张表不同步第 `2` 期。 "
     "两条限制单独标：`LongCat 2.5 Free` **每日 `100` 次**；`Beam Free` 明确排除 `China (including Hong Kong and Macau)`。", r42,
     name="🟡 **`OpenCode` 免费模型清单（`Free models` 段 `12` 条 · 与上期字节 + `md5` 双同）**")

edit("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **已公开（069 期补登）。 `downloads 2,484 → 2,830`（`+346`）/ `likes 358 → 360`（`+2`）；`lastModified` 仍 `11/10 07:28Z`**。 "
     "四个时间点仍分开写：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`、媒体稿 `11/15 10:06Z`、**一手页无「发布日期」字段**。", r42)

edit("Hy4 开放权重", "腾讯混元 `Hy4 flash` 开放权重",
     "🟢 **（072 期补入）三仓均 `gated: false`。 第 `3` 天：`downloads 3,949`（主仓，`+3,790`）/ `1,219`（`FP8`，`+1,098`）/ `699`（`base`，`+570`）；`likes 483` / `22` / `24`**。 "
     "**第三方转档已能点名 `10` 个以上**（`GGUF` 七仓、`MLX` 两仓、`NVFP4` 一仓，另有微调仓）——`?search=Hy4` 结果 **`43 → 85` 条**。 "
     "**许可是 `Apache 2.0` 派生 + `§10`**：对外 `MaaS` 且过 `$50M` 营收或 `1` 亿 `MAU` 须另签；`§10.3` 内部使用豁免。", r42,
     name="🟢 **腾讯混元 `Hy4 flash` 开放权重（**`220.25B` 实测 · 激活 `11.3B` + `0.43B` · `1M` · `Tencent Hy License 1.0`**）**")

edit("GPT-6.2", "OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
     "🟡 **（072 期补入）发布页可用名单逐字 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 "
     "本期三读数：`OpenRouter` 仍 `8` 条、**仍无 `:free`**（第 `3` 天）；`chatgpt.com/pricing` 仍 `000`（第 `3` 期）→ **免费档是否含 `GPT-6.2` 仍无一手**；"
     "`openai.com/index/` `200` / `380,283` 字节，窗口内**无新免费档条目**。 **不写「免费用户可用/不可用」。**", r42,
     name="🟡 **OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布（**可用名单 `Plus` / `Pro` / `Enterprise` / `Edu` · **`Free` 不在名单里**）**")

edit("Ling 3.2", "`inclusionAI` `Ling 3.2 Flash`",
     "🟡 **生效中（068 期补入）。 本期变化：`/endpoints` 从 `[]` 变成 `1` 条路由（响应 `1,466` 字节）—— `7` 天空窗结束**。 "
     "**层数要重数**：目录有、路由有、权重仓仍 `404` —— **三层只开了两层**。 "
     "上期写的「有价无路由」当期成立、但那是过渡态；**本期只写读数，不写「已可用」**（纠错④）。", r42,
     name="🟡 **`inclusionAI` `Ling 3.2 Flash` 进入 `OpenRouter` 免费区（`:free` 零价 · `1,048,576` 上下文 · **路由本期接通 `1` 条**）**")


# ------------------------------------------------------------ ③ 补入新行
NEW41_A = ("| 🟠 **智谱 `AutoClaw` 国内站 `M11W4` 周福利：登录领 `100M` Tokens（**`10,000` 积分 · 每账号一次**）** "
           "| **`11/29 23:59`（北京时间 · 官方逐字「活动时间 11 月 23 日（周一）00:00—11 月 29 日（周日）23:59」· 距截止 `9` 天）** "
           "| 🟠 **（074 期补入）`11/23`–`11/29` 登录即领 `100M` Tokens，奖励 `11/29 23:59` 失效。 "
           "**与本周 `M11W3`（到 `11/22 23:59`）首尾相接、只隔 `1` 分钟** —— 本周领的额度本周日作废，下周一起要重新领。 "
           "`100M` 是**连续第 `2` 周**（`11/2`–`11/8`、`11/9`–`11/15` 两周均为 `50M`），**不写「一直是 1 亿」**。 "
           "额度锁在客户端内、导不出 `API`。 |")

idx = [k for k, r in enumerate(r41) if "智谱 `AutoClaw` 国内站 `M11W3`" in name_of(r)]
assert len(idx) == 1, idx
r41.insert(idx[0] + 1, NEW41_A)

NEW42_A = ("| 🟠 **`MiniMax H3-Image` `4K` 五折 · 第二版（**新文案无截止日 · 新增「宽 × 高 ≥ `1660` 万像素」门槛**）** "
           "| **无截止日（新版文案整句删掉日期：`2026-11-18` / `截止` / `结束` 各 `0` 命中）** "
           "| 🟠 **（074 期补入）横幅逐字「`4K 生图限时 5 折：MiniMax-H3-Image 和 MiniMax-H3-Image-Highspeed 最终交付图片的宽 × 高 ≥ 1660 万像素，即享整次请求费用 5 折。`」** "
           "六档折后价全部回位：`0.2261` / `0.2404` / `0.2605` / `0.4275` / `0.4499` / `0.5073`（原价 `0.4522`–`1.0146`）；`限时5折` `12` 处命中；页 `305,754 → 310,127`（`+4,373`）。 "
           "**门槛与 `4096 × 4096` ＝ `1677.7` 万像素刚好过线** —— 门槛卡的是「按 `4K` 计价但出图更小」的请求，不是 `4K` 本身。 "
           "**与 `4.1` 那一行是同一活动的两个版本，不合并、不继承截止日**（避坑 318）。 |")

NEW42_B = ("| 🟢 **`Kimi` 文件内容抽取 / 文件存储接口「限时免费」（**官方定价页逐字 · 无截止日 · 不含「文档内容当输入」的 token 费**）** "
           "| **无截止日（官方逐字「文件相关接口（文件内容抽取/文件存储）限时免费」，未给期限、未给额度上限、未给限流）** "
           "| 🟢 **（074 期补入）同一段还写着：抽出的文档内容作为 `Input` 传给模型时「也将按量计费」—— 免的是解析这一步，不是推理**。 "
           "同页下半段：`K2` 系列 `10/31` 已停新注册、**计划 `12` 月底下线全部 `K2` 系列模型**（相对期限、无确切日）→ 还挂 `kimi-k2.x` 的工作流要迁。 "
           "`Batch API` 仍为标准价 `60%`、缓存 `TTL` 默认 `5min`（与上期一致）。 |")

idx = [k for k, r in enumerate(r42) if "`inclusionAI` `Ling 3.2 Flash`" in name_of(r)]
assert len(idx) == 1, idx
r42.insert(idx[0], NEW42_A)
idx = [k for k, r in enumerate(r42) if "阿里 `Qwen4-Max` 发布" in name_of(r)]
assert len(idx) == 1, idx
r42.insert(idx[0], NEW42_B)


# ------------------------------------------------------------ ④ 指针重贴当期期号
def repoint(bucket):
    n = 0
    for k, r in enumerate(bucket):
        if "附录 073" in r:
            bucket[k] = r.replace("附录 073", "附录 074")
            n += 1
    return n


print("指针重贴：4.1", repoint(r41), "4.2", repoint(r42))
print("改写行：", len(EDITED), EDITED)
print("输出行数：4.1 = %d，4.2 = %d" % (len(r41), len(r42)))
if DRY:
    print("41 样本", r41[3][:300])
    print("42 样本", r42[6][:300])
    print("DRY RUN —— 未写盘")
    sys.exit(0)

# ------------------------------------------------------------ ⑤ 写回
i = md.index("### 4.1 限时动作")
k2 = md.index("### ④ 本期第四章脚注")
HEAD = "| 活动 | 截止 | 状态 |\n| --- | --- | --- |\n"
sec41 = HEAD + "\n".join(r41) + "\n\n"
sec42 = HEAD + "\n".join(r42) + "\n\n"

new_md = (md[:i]
          + "### 4.1 限时动作（有确切截止日 · %d 条）\n\n" % len(r41)
          + sec41
          + "### 4.2 常驻权益本期变更（无截止日 · 本期有变化 %d 条）\n\n" % len(r42)
          + sec42
          + md[k2:])
io.open(MD, "w", encoding="utf-8", newline="\n").write(new_md)

# ------------------------------------------------------------ ⑥ 复读落盘再断言
disk = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
d41 = rows_of(disk, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
d42 = rows_of(disk, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("落盘行数：4.1 = %d，4.2 = %d" % (len(d41), len(d42)))
assert len(d41) == 67, len(d41)
assert len(d42) == 50, len(d42)
assert "074 期补入" in disk
assert "已过 `51` 天" in disk
assert "第 `47` 期" in disk
assert "已过 `3` 天（`11/17` 到期）" in disk
assert "`477/15/12`" in disk
assert "附录 073" not in disk
assert "Will be removed on November 18, 2026." in disk
assert "1660" in disk
assert "文件相关接口（文件内容抽取/文件存储）限时免费" in disk

dist = Counter(len(cells_of(r)) for r in d41 + d42)
print("字段数分布：", dict(dist))
assert set(dist) == {3}, dist

bad = []
for r in d41 + d42:
    c = cells_of(r)
    delta = days_of(c[1])
    if delta is None:
        continue
    for m in re.finditer(r"(已过|距截止|距今|距承诺日)\s*`(\d+)`\s*天", c[2]):
        val = int(m.group(2))
        if m.group(1) == "已过":
            ok = (delta < 0 and val == -delta)
        elif m.group(1) == "距承诺日":
            ok = (val == delta)
        else:
            ok = (delta > 0 and val == delta) or (delta == 0 and val == 0)
        if not ok:
            bad.append((name_of(r)[:26], m.group(0), delta, c[1][:40]))
assert not bad, bad
print("天数复核（带符号）：全部一致")

conflict = []
for r in d41 + d42:
    c = cells_of(r)
    if "已过" in c[1] and re.search(r"距截止\s*`\d+`\s*天", c[2]):
        conflict.append(name_of(r)[:26])
assert not conflict, conflict
print("方向复核：0 行矛盾")

forbid = [r for r in d41 + d42 if ("未开始" in cells_of(r)[2] or "已结束" in cells_of(r)[2])]
assert not forbid, [name_of(r)[:30] for r in forbid]
print("禁词复核：状态列无「未开始 / 已结束」")

ISSUE_RE = re.compile(r"(?!074)(0\d{2})\s*期")
over = [(name_of(r)[:24], len(ISSUE_RE.findall(cells_of(r)[2]))) for r in d41 + d42
        if len(ISSUE_RE.findall(cells_of(r)[2])) >= 2]
assert not over, over
print("R3 预检：0 行超 1 处")
