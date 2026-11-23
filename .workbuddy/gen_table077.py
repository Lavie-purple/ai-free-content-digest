# -*- coding: utf-8 -*-
"""077 期：在 076 期现行 4.1/4.2 表体上做「天数带符号重算 + 行级改写」。

纪律（055–076 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言 ≤ 4；⑤ 状态列整体替换；⑥ 单元格不许出现 `|`；
  ⑦ 天数一律由基准日实算、断言带符号；⑧ 状态列不写「未开始 / 已结束」；
  ⑨ 本期无补入行（无新常驻权益）；⑩ 4.2 的 OpenRouter / OpenCode 行名带计数，改名必须在重建 CSV 之前。
"""
import io
import re
import sys
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第077期-2026-11-23.md"
PTR = " [附录 077](details.html) |"
TODAY = date(2026, 11, 23)
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
assert len(r41) == 67, ("076 期 4.1 行数", len(r41))
assert len(r42) == 53, ("076 期 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "今日（`11/23`）为截止日", st)
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
print("无日期行：", skipped[:8])


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


# ---- 腾讯老混元：截止列不可解析，天数与期数手工推进（09-30 起算 = 已过 54 天）
hits = [k for k, r in enumerate(r41) if "腾讯老混元" in name_of(r)]
assert len(hits) == 1
row = r41[hits[0]]
assert "已过 `53` 天" in row and "第 `49` 期" in row and "第 `40` 天" in row, row[:200]
row = row.replace("已过 `53` 天", "已过 `54` 天").replace("第 `49` 期", "第 `50` 期").replace("第 `40` 天", "第 `41` 天")
row = row.replace("六项关键词各 `0` 命中（第 `8` 期）", "六项关键词各 `0` 命中（第 `9` 期）")
row = row.replace("`6,584` 字节 / `md5` 与上期双同", "`6,584` 字节 / `md5` 与上期双同（第 `9` 期）")
row = row.replace(" [附录 076](details.html) |", PTR)
r41[hits[0]] = row
EDITED.append("腾讯老混元(手算)")

# ---- 4.1：Hy4 flash WorkBuddy 限免
edit("Hy4 flash 限免", "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
     "🟠 **距截止 `6` 天。 限免只限 `WorkBuddy` 内的 `Hy4 flash`**；`TokenHub` 是**限时 `5` 折**。 "
     "三仓 `downloads` 本期同批上跳（`7,696` / `1,949` / `1,011`）—— **到期后能用的是权重，不是本行额度**。",
     r41, name="🟠 **腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费（**`220.25B` 实测总参（含 `64B` Engram）/ 激活 `11.3B` + `0.43B` / `1M` 上下文 · 官方口径「`11/30` 前」**）**")

# ---- 4.1：Hy4 AMA（已收口）
edit("Hy4 AMA", "腾讯混元 `Hy4` / `Hy4 flash` 官方 `Reddit` `AMA`",
     "⚪ **已收口（`11/21 02:00` 收口，已过 `2` 天）。 官方 `X` 公布 `11/20` `8–10 AM PT` ＝ 北京 `11/21 00:00–02:00`**，在 `r/LocalLLaMA` 由研发团队答问。 "
     "**`reddit.com` 两个入口连续两期 `000`，本报未抄录问答内容** —— 只记「按计划开过」。",
     r41, deadline="**北京 `11/21` 00:00–02:00（`11/20` `8–10 AM PT` 换算 · 已过 `2` 天）**")

# ---- 4.1：ERNIE 5.5
edit("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `2` 天）。 本期是最后窗口 —— 官方发布页 `11月25日前开源` 逐字仍在**（`54,010` 字节，第 `6` 期逐字节相同）。 "
     "**权重仍未放**：`?author=baidu` 仍 `39` 仓（第 `20` 天 `0` 变化）。 **`078` 期给判定：放权重或承认延期。**",
     r41)

# ---- 4.1：MiniMax 4K —— 旧版收口（新版在 4.2）
edit("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
     "⚪ **旧版已过期（`11/18 00:00` 到期）；现行版本是第二版（无截止日、`1660` 万像素门槛），见 `4.2`。 本行只记「旧版过期」。** "
     "第二版第 `4` 天**逐字节同**（页 `310,183`），**不代表该折扣已停**（避坑 317）。 旧文案的截止句整句不存在，**截止日不跨版本**。", r41,
     deadline="**`11/18 00:00`（北京 · 旧版逐字「即日起至 2026 年 11 月 18 日 00:00」· 已过 `5` 天）**")

# ---- 4.1：Runway Kling 4.0
edit("Runway Kling", "Runway 平台 `Kling 4.0`",
     "🟠 **生效中（距截止 `7` 天）。 （068 期补入）只在 `Standard` / `Pro` 两个付费档下列出，免费档（`125` 一次性 credits）下没有这一条**；"
     "与 `Runware` 那条 `Kling 4.0 15% OFF`（`10/29` 已过期）是两个分发商的两场促销，不可合并。 **折扣不是免费。**",
     r41, deadline="**`11/30`（官方逐字 `until November 30`，未写时区 · 距截止 `7` 天）**")

# ---- 4.1：Runway 企业版
edit("Runway 企业版", "Runway 企业版",
     "🟠 **生效中（距截止 `38` 天）。 （068 期补入）三个要件缺两个：`up to`（上限不是保底）、条件（`terms` 页本期仍 `404`）**。 "
     "只登记横幅与日期，不写「几个月 / 什么条件」。 页 `907,130` 字节（`−29.3%`，每句重复次数 `4 → 2`，文案全在）。",
     r41, deadline="**`12/31`（官方逐字 `Sign by 12/31`；条款页 `runway.com/terms` 本期 `404` · 距截止 `38` 天）**")

# ---- 4.1：Runware 4K 50%
edit("Runware 4K 50%", "`Runware` 分发层 `MiniMax H3-Image`",
     "⚪ **已收口（`11/17` 到期、已过 `6` 天）。 `h3-image` `18`、徽标 `0`、价目不动（`0.2261` / `0.4522` 全页仍在）** —— "
     "**076 期起按「已成稳定行为」记、不再单列次数**。 数组日期分布第三次逐项相同；`11-23` 两条到期当天仍在页面。",
     r41, deadline="**`11/17`（官方促销数组 `endsAt: \"2026-11-17\"` 逐字 · 已过 `6` 天）**")

# ---- 4.1：Runware H3 Max 30%
edit("Runware H3 Max", "`Runware` 分发层 `MiniMax H3 Max`",
     "⚪ **已过 `8` 天（`11/15` 到期）。 数组里 `endsAt: \"2026-11-15\"` 仍在、卡片徽标卸下后未挂回** —— 「数组是账本、卡片是货架」。 "
     "本期数组分布与上期逐项相同（`11-17` `1`、`11-19` `1`、`11-23` `2`）。",
     r41, deadline="**`11/15`（官方促销数组 `endsAt: \"2026-11-15\"`；已过 `8` 天）**")

# ---- 4.1：AutoClaw M11W3（已收口）
edit("AutoClaw M11W3", "智谱 `AutoClaw` 国内站 `M11W3`",
     "⚪ **已收口（`11/22 23:59` 收口，已过 `1` 天）。 官方逐字 `11 月 16 日至 11 月 22 日` 登录领 `100M`（`10,000` 积分），奖励同日 `23:59` 失效**。 "
     "`M11W4` 已在 `11/23 00:00` 接班（仍 `100M`），**无缝衔接**；`M11W5` 连续第 `2` 期 `404`。 **锁客户端、导不出 `API`。**",
     r41, deadline="**`11/22 23:59`（北京时间 · 官方逐字「活动时间 11 月 16 日（周一）00:00—11 月 22 日（周日）23:59」· 已过 `1` 天）**")

# ---- 4.1：AutoClaw M11W4
edit("AutoClaw M11W4", "智谱 `AutoClaw` 国内站 `M11W4`",
     "🟠 **距截止 `6` 天。 `11/23`–`11/29` 登录领 `100M`（`10,000` 积分），`11/29 23:59` 失效**。 `11/23 00:00` 已接班，页 `47,974` 与上期同字节。 "
     "`100M` 连续第 `2` 周（前两周 `50M`）。 锁客户端、导不出 `API`。",
     r41, deadline="**`11/29 23:59`（北京时间 · 官方逐字「活动时间 11 月 23 日（周一）00:00—11 月 29 日（周日）23:59」· 距截止 `6` 天）**")

# ---- 4.1：Antigravity 三模型
edit("Antigravity 三模型", "`Google Antigravity` 免费档三个第三方模型",
     "🟠 **距截止 `7` 天（改期后第 `3` 天）。 脚注 `8` 处全为 `November 30, 2026`、`November 18` 一处不剩**；页面字节与上期同（`182,905`）、**可见文本 `diff` `0` 行**、`md5` 变（构建标识）。 "
     "免费档仍四模型；付费档另列 `Gemini 4` 四款与 `Sonnet 5.5` / `Opus 5.5`，**免费档一个都没有**。",
     r41, deadline="**`11/30`（官方脚注逐字 `Will be removed on November 30, 2026.` · 距截止 `7` 天）**",
     name="🟠 **`Google Antigravity` 免费档三个第三方模型 `11/30` 移除（`Claude Sonnet 4.6` / `Claude Opus 4.6` / `GPT-OSS-120B`）**")

# ---- 4.2：OpenRouter 免费档（改名 + 状态整体替换，必须在重建 CSV 之前）
edit("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **四项全部回补：全量 `476 → 477`、`:free` `11 → 12`、零价 `14 → 15`、`max_price=0` `13 → 14`。 差集只进 `1` 出 `0`**："
     "`dots-3-note-preview:free` 回归（`created` 仍 `2026-08-14`，**不是新上架**）。 "
     "`gpt-6.2` 仍 `8` 条、**无 `:free`（第 `6` 天）**。",
     r42, name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `477/15/12`**）**")

# ---- 4.2：OpenCode
edit("OpenCode 免费清单", "`OpenCode` 免费模型清单",
     "🟡 **段内 `12 → 11`：出 `LongCat 2.5 Free`、无新增**。 同日上架 `Jev 1.14`（**付费 `$0.042`**），`jev-1.13-free` 仍在。 "
     "弃用表**换行**：清走 `5` 行旧记录、新增 `LongCat-2.0 / November 22, 2026`（**行名与撤下的 `2.5` 不同，不写因果**）。 页 `108,492`（`−677`）。",
     r42, name="🟡 **`OpenCode` 免费模型清单（`Free models` 段 `11` 条 · 本期净减 `1` 条）**")

# ---- 4.2：Token 羊毛
edit("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `15` 期：口径改版 —— 「今天还能领」`¥821`（上期 `¥1,829`），"
     "卡册 `64 → 61` 张（出 `7` 进 `4`）**。 **规则新增两条排除（仅限学生 / 到期自动扣费）＋ 到期自动下架 + 规则不明暂停展示 → 两期数字不可相减。** 页 `499,261` 字节。",
     r42)

# ---- 4.2：Antigravity 个人免费档
edit("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
     "🟢 **逐字 `$0/month`（`182,905` 字节 / `md5 e5f53049`）。 免费档四模型**（`3.8 Flash` + 三个第三方）。 "
     "**改期后第 `3` 天：脚注 `8` 处全为 `11/30`、`November 18` 归零、可见文本与上期 `diff` `0` 行**。 `Baseline agent quota refreshed weekly` **仍无数字（第 `8` 期）**。",
     r42)

# ---- 4.2：ERNIE-Base
edit("ERNIE-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓。 本期 `downloads` 继续上跳**（`5,532` / `2,120`）；`likes` `347`（`+1`）/ `394`（`0`）。 "
     "两仓 `lastModified` 仍停 `11/05` —— **仓库没变，数字是批次刷新**（避坑 327）。",
     r42)

# ---- 4.2：Inkling 2 Mini 开放权重
edit("Inkling 2 Mini 开放权重", "`thinkingmachines/Inkling-2-Mini` 开放权重",
     "🟢 **（075 期补入）`downloads` `7,944 → 41,888`、`likes` `3,256 → 5,230`（含批次刷新，不当趋势）**。 `HF` 趋势榜第 `1`；"
     "`unsloth` `GGUF` 已 `805,993` 次下载（**比原仓高 `19` 倍**）。 `~20GB` 为 `NVFP4` 权重、实测机 `48GB`。 **API 见本表价格行**。",
     r42)

# ---- 4.2：inkling-2-mini 的 API 入口（价点 2 → 4）
edit("Inkling API 定价", "`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`",
     "🟡 **（076 期新增观测位）价点 `2 → 4`：`PrimeIntellect` 三档 `$0.0375/$0.15`、`$0.075/$0.30`、`$0.12/$0.50`（同 `id` / 同 `fp4` / 同报 `1M`）；"
     "`Io Net` 由 `$0.08/$0.35` 涨到 `$0.12/$0.50`（输入 `+50.0%`、输出 `+42.9%`）**。 **同模型最贵档是最便宜档的 `3.2` 倍**；无 `:free`。",
     r42, name="🟡 **`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`（**`2` 个 provider / `4` 个价点 · 按量计费 · **无 `:free` 变体**）**")

# ---- 4.2：Inkling 2 Small
edit("Inkling 2 Small", "`thinkingmachines/Inkling-2-Small` 开放权重",
     "🟢 **`Apache-2.0`。 `downloads` `45,356 → 55,885`、`likes` `636 → 1,420`（`+784`）**；`lastModified` `11/20 14:09Z`。 "
     "**`OpenCode` 把它的 `Free` 变体按弃用表下架（`11/19`）** —— 权重还在，免费入口已不在。",
     r42)

# ---- 4.2：Hy4 flash 开放权重
edit("Hy4 flash 开放权重", "腾讯混元 `Hy4 flash` 开放权重",
     "🟢 **（072 期补入）三仓 `gated: false`。 本期 `downloads` 同批上跳**（`7,696` / `1,949` / `1,011`）；`likes` `632` / `27` / `26`。 "
     "`?search=Hy4` 返回 `100`（**触 `limit` 上限，`≥100`**）。 许可 `Apache 2.0` 派生 + `§10`：对外 `MaaS` 过 `$50M` 或 `1` 亿 `MAU` 须另签。",
     r42, name="🟢 **腾讯混元 `Hy4 flash` 开放权重（**`220.25B` 实测 · 激活 `11.3B` + `0.43B` · `1M` · `Tencent Hy License 1.0`**）**")

# ---- 4.2：Hy4 770B
edit("Hy4 770B", "腾讯混元 `Hy4`（旗舰 · 非 `flash`）开放权重",
     "🟢 **（075 期补登）三仓 `downloads` `1,815` / `787` / `726`（合计 `3,328`）、`likes` `266` / `16` / `11`** —— 第三次全仓同向上跳。 "
     "**`BF16` 约 `1.5TB`、`FP8` 约 `770GB` —— 开放≠可本地跑**；量化走 `AngelSlim/Hy4-GGUF`。",
     r42)

# ---- 4.2：LongCat-2.5
edit("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **已公开（069 期补登）。 `downloads` `2,949 → 3,303`、`likes` `278 → 284`**。 **`OpenCode` 的免费入口本期撤下**（`longcat-2.5-free` 从 `Free models` 段消失），"
     "**权重不受影响**。 四个时间点仍分开写：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`、媒体稿 `11/15`、**一手页无发布日期字段**。",
     r42)

# ---- 4.2：GPT-6.2
edit("GPT-6.2", "OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
     "🟡 **（072 期补入）名单 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 `OpenRouter` 仍 `8` 条、**无 `:free`（第 `6` 天）**；"
     "`chatgpt.com/pricing` 第 `6` 期读不到正文；`openai.com/news` 最新条目仍是 `11/18`。 **不写「免费可用/不可用」。**",
     r42, name="🟡 **OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布（**可用名单 `Plus` / `Pro` / `Enterprise` / `Edu` · **`Free` 不在名单里**）**")

# ---- 4.2：Ling 3.2
edit("Ling 3.2", "Ling 3.2 Flash` 进入 `OpenRouter`",
     "🟡 **生效中（068 期补入）。 本期两套 `id` 同形：`:free` `1` 条路由（`1,480` 字节）、基名 `0` 条（`462` 字节）** —— 连续第 `3` 期。 "
     "**三层只开两层：目录有、`:free` 路由有、权重仓仍 `404`。**",
     r42, name="🟡 **`inclusionAI` `Ling 3.2 Flash` 进入 `OpenRouter` 免费区（`:free` 零价 · `1,048,576` 上下文 · **`:free` 路由 `1` 条 / 基名 `0` 条**）**")

# ---- 4.2：MiniMax 第二版
edit("MiniMax 第二版", "`MiniMax H3-Image` `4K` 五折 · 第二版",
     "🟠 **第二版第 `4` 天仍在架（页 `310,183`，与上期逐字节相同）。 六档折后价全在**（`0.2261`–`0.5073`），`2026-11-18` / `截止` / `结束` 各 `0` 命中。 "
     "门槛：宽 × 高 ≥ `1660` 万像素。 **文案里没有任何日期 —— 不替它排日。**",
     r42)


# ------------------------------------------------------------ ③ 指针重贴当期期号
def repoint(bucket):
    n = 0
    for k, r in enumerate(bucket):
        if "附录 076" in r:
            bucket[k] = r.replace("附录 076", "附录 077")
            n += 1
    return n


print("指针重贴：4.1", repoint(r41), "4.2", repoint(r42))
print("改写行：", len(EDITED), EDITED)
print("输出行数：4.1 = %d，4.2 = %d" % (len(r41), len(r42)))

if DRY:
    print("41 样本", r41[1][:300])
    print("42 样本", r42[6][:300])
    print("DRY RUN —— 未写盘")
    sys.exit(0)

# ------------------------------------------------------------ ④ 写回（原地替换两个表块，其余一字不动）
NL = chr(10)
old_41 = NL.join(rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更"))
old_42 = NL.join(rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注"))
assert md.count(old_41) == 1 and md.count(old_42) == 1
new_md = md.replace(old_41, NL.join(r41), 1).replace(old_42, NL.join(r42), 1)
assert new_md != md
io.open(MD, "w", encoding="utf-8", newline=NL).write(new_md)

back = io.open(MD, encoding="utf-8").read()
assert "477/15/12" in back and "`108,492`" in back
assert back.count("附录 077") > 60, back.count("附录 077")
assert "附录 076" not in back
assert "其余 `142` 条常驻权益本期无变化" in back
rb = rows_of(back, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
rb2 = rows_of(back, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("落盘复核：4.1 = %d，4.2 = %d，字节 = %d" % (len(rb), len(rb2), len(back.encode("utf-8"))))
assert len(rb) == 67 and len(rb2) == 53
print("OK")
