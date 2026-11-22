# -*- coding: utf-8 -*-
"""076 期：在 075 期现行 4.1/4.2 表体上做「天数带符号重算 + 行级改写 + 补入 1 行」。

纪律（055–075 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 补入行必须带「076 期」标记；⑥ 状态列整体替换；
  ⑦ 单元格不许出现 `|`；⑧ 天数一律由基准日实算、断言带符号；
  ⑨ 状态列不写「未开始 / 已结束」；状态列里非本期期号引用 ≤ 1 处（lint R3）；
  ⑩ 本期新增：4.2 补入 `inkling-2-mini` 的 API 入口（无截止日 → D 桶）。
"""
import io
import re
import sys
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第076期-2026-11-22.md"
PTR = " [附录 076](details.html) |"
TODAY = date(2026, 11, 22)
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
assert len(r41) == 67, ("075 期 4.1 行数", len(r41))
assert len(r42) == 52, ("075 期 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "今日（`11/22`）为截止日", st)
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


# ---- 腾讯老混元：截止列不可解析，天数与期数手工推进（09-30 起算 = 已过 53 天）
hits = [k for k, r in enumerate(r41) if "腾讯老混元" in name_of(r)]
assert len(hits) == 1
row = r41[hits[0]]
assert "已过 `52` 天" in row and "第 `48` 期" in row and "第 `39` 天" in row, row[:200]
row = row.replace("已过 `52` 天", "已过 `53` 天").replace("第 `48` 期", "第 `49` 期").replace("第 `39` 天", "第 `40` 天")
row = row.replace("六项关键词各 `0` 命中（第 `7` 期）", "六项关键词各 `0` 命中（第 `8` 期）")
row = row.replace("`md5` `0f922791`", "`md5` `0f922791`")
row = row.replace("本期 **`6,584` 字节**（与上期逐字节相同）", "本期 **`6,584` 字节 / `md5` 与上期双同**")
row = row.replace(" [附录 075](details.html) |", PTR)
r41[hits[0]] = row
EDITED.append("腾讯老混元(手算)")

# ---- 4.1：Hy4 flash WorkBuddy 限免
edit("Hy4 flash 限免", "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
     "🟠 **距截止 `7` 天。 限免只限 `WorkBuddy` 内的 `Hy4 flash`**；`TokenHub` 是**限时 `5` 折**。 "
     "三仓 `downloads` 本期同批上跳（`5,588` / `1,535` / `826`）—— **到期后能用的是权重，不是本行额度**。",
     r41, name="🟠 **腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费（**`220.25B` 实测总参（含 `64B` Engram）/ 激活 `11.3B` + `0.43B` / `1M` 上下文 · 官方口径「`11/30` 前」**）**")

# ---- 4.1：Hy4 AMA（已收口 1 天）
edit("Hy4 AMA", "腾讯混元 `Hy4` / `Hy4 flash` 官方 `Reddit` `AMA`",
     "⚪ **已收口（`11/21 02:00` 收口，已过 `1` 天）。 官方 `X` 公布 `11/20` `8–10 AM PT` ＝ 北京 `11/21 00:00–02:00`**，在 `r/LocalLLaMA` 由研发团队答问。 "
     "**`reddit.com` 两个入口本期仍 `000`，本报未抄录问答内容** —— 只记「按计划开过」。",
     r41, deadline="**北京 `11/21` 00:00–02:00（`11/20` `8–10 AM PT` 换算 · 已过 `1` 天）**")

# ---- 4.1：ERNIE 5.5
edit("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `3` 天）。 官方发布页 `11月25日前开源` 逐字仍在**（`54,010` 字节，第 `5` 期逐字节相同）。 "
     "**权重仍未放**：`?author=baidu` 仍 `39` 仓（第 `19` 天 `0` 变化）。 **本季最后一个「官方给了日期」的开源承诺。**",
     r41)

# ---- 4.1：MiniMax 4K —— 旧版收口（新版在 4.2）
edit("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
     "⚪ **旧版已过期（`11/18 00:00` 到期）；现行版本是第二版（无截止日、`1660` 万像素门槛），见 `4.2`。 本行只记「旧版过期」。** "
     "第二版第 `3` 天仍原样在架（页 `310,183`，`+21`），**不代表该折扣已停**（避坑 317）。 旧文案的截止句整句不存在，**截止日不跨版本**。", r41,
     deadline="**`11/18 00:00`（北京 · 旧版逐字「即日起至 2026 年 11 月 18 日 00:00」· 已过 `4` 天）**")

# ---- 4.1：Runway Kling 4.0
edit("Runway Kling", "Runway 平台 `Kling 4.0`",
     "🟠 **生效中（距截止 `8` 天）。 （068 期补入）只在 `Standard` / `Pro` 两个付费档下列出，免费档（`125` 一次性 credits）下没有这一条**；"
     "与 `Runware` 那条 `Kling 4.0 15% OFF`（`10/29` 已过期）是两个分发商的两场促销，不可合并。 **折扣不是免费。**",
     r41, deadline="**`11/30`（官方逐字 `until November 30`，未写时区 · 距截止 `8` 天）**")

# ---- 4.1：Runway 企业版
edit("Runway 企业版", "Runway 企业版",
     "🟠 **生效中（距截止 `39` 天）。 （068 期补入）三个要件缺两个：`up to`（上限不是保底）、条件（`terms` 页本期仍 `404`）**。 "
     "只登记横幅与日期，不写「几个月 / 什么条件」。 免费档另有 `125` 一次性 credits（`$0/月`、限「a selection of models」）。",
     r41, deadline="**`12/31`（官方逐字 `Sign by 12/31`；条款页 `runway.com/terms` 本期 `404` · 距截止 `39` 天）**")

# ---- 4.1：Runware 4K 50%
edit("Runware 4K 50%", "`Runware` 分发层 `MiniMax H3-Image`",
     "⚪ **已收口（`11/17` 到期、已过 `5` 天）。 `h3-image` `18`、徽标 `0`、价目不动（`0.2261` / `0.4522` 全页 `0` 命中）** —— "
     "第 `17` 次实证，**本期起按「已成稳定行为」记、不再单列次数**。 数组 `22` 条、日期分布一整期未动。",
     r41, deadline="**`11/17`（官方促销数组 `endsAt: \"2026-11-17\"` 逐字 · 已过 `5` 天）**")

# ---- 4.1：Runware H3 Max 30%
edit("Runware H3 Max", "`Runware` 分发层 `MiniMax H3 Max`",
     "⚪ **已过 `7` 天（`11/15` 到期）。 数组里 `endsAt: \"2026-11-15\"` 仍在、卡片徽标卸下后未挂回** —— 「数组是账本、卡片是货架」。 "
     "本期数组 `22` 条、分布与上期逐项相同（`11-17` `1`、`11-19` `1`、`11-23` `2`）。",
     r41, deadline="**`11/15`（官方促销数组 `endsAt: \"2026-11-15\"`；已过 `7` 天）**")

# ---- 4.1：AutoClaw M11W3（今天收口）
edit("AutoClaw M11W3", "智谱 `AutoClaw` 国内站 `M11W3`",
     "🔴 **今天 `23:59` 收口。 官方逐字 `11 月 16 日至 11 月 22 日` 登录领 `100M`（`10,000` 积分），奖励同日 `23:59` 失效**。 "
     "`M11W4` 明天 `00:00` 接班（仍 `100M`），**两期只隔 `1` 分钟**；`M11W5` 仍 `404`。 **锁客户端、导不出 `API`。**",
     r41, deadline="**`11/22 23:59`（北京时间 · 官方逐字「活动时间 11 月 16 日（周一）00:00—11 月 22 日（周日）23:59」· 今日为截止日）**")

# ---- 4.1：AutoClaw M11W4
edit("AutoClaw M11W4", "智谱 `AutoClaw` 国内站 `M11W4`",
     "🟠 **距截止 `7` 天。 `11/23`–`11/29` 登录领 `100M`（`10,000` 积分），`11/29 23:59` 失效**。 与 `M11W3`（今晚 `23:59` 收口）**只隔 `1` 分钟**。 "
     "`100M` 连续第 `2` 周（前两周 `50M`）。 锁客户端、导不出 `API`。",
     r41, deadline="**`11/29 23:59`（北京时间 · 官方逐字「活动时间 11 月 23 日（周一）00:00—11 月 29 日（周日）23:59」· 距截止 `7` 天）**")

# ---- 4.1：Antigravity 三模型
edit("Antigravity 三模型", "`Google Antigravity` 免费档三个第三方模型",
     "🟠 **距截止 `8` 天（改期后第 `2` 天）。 脚注 `8` 处全为 `November 30, 2026`、`November 18` 一处不剩** —— 075 期判的「改期」在第二天仍成立。 "
     "免费档仍四模型；付费档另列 `Gemini 4` 四款与 `Sonnet 5.5` / `Opus 5.5`，**免费档一个都没有**。",
     r41, deadline="**`11/30`（官方脚注逐字 `Will be removed on November 30, 2026.` · 距截止 `8` 天）**",
     name="🟠 **`Google Antigravity` 免费档三个第三方模型 `11/30` 移除（`Claude Sonnet 4.6` / `Claude Opus 4.6` / `GPT-OSS-120B`）**")

# ---- 4.2：OpenRouter 免费档
edit("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **四项同降 `1`：全量 `477 → 476`、`:free` `12 → 11`、零价 `15 → 14`、`max_price=0` `14 → 13`。 出 `2` 进 `1`**："
     "下架 `dots-3-note-preview:free`（真免费）与 `meituan/longcat-2.0`（付费），新增 `inkling-2-mini`（付费）。 "
     "`gpt-6.2` 仍 `8` 条、**无 `:free`（第 `5` 天）**。",
     r42, name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `476/14/11`**）**")

# ---- 4.2：OpenCode
edit("OpenCode 免费清单", "`OpenCode` 免费模型清单",
     "🟡 **段内仍 `12` 条，但一进一出：进 `Tidepool Alpha Free`、出 `Inkling 2 Small Free`**。 弃用表新增 `3` 行 `11/19`"
     "（`Inkling 2 Small Free` / `GLM 5.2` / `GLM 5.1`）—— **撤项有日期可查**。 页 `109,169`（`+6,502`）。 "
     "`LongCat 2.5 Free` 每日 `100` 次；`Beam Free` 排除中国大陆。",
     r42, name="🟡 **`OpenCode` 免费模型清单（`Free models` 段 `12` 条 · 本期一进一出）**")

edit("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `14` 期：「今天还能领」`¥1804 → ¥1829`（`+25`）、"
     "卡册 `62 → 64` 张**。 两期连涨（`+67`、`+25`）；新卡偏小额（平均 `12.5` 元 vs 存量 `29` 元）。 页 `517,051` 字节。",
     r42)

edit("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
     "🟢 **逐字 `$0/month`（`182,905` 字节 / `md5 ed4bbe91`）。 免费档四模型**（`3.8 Flash` + 三个第三方）。 "
     "**改期后第 `2` 天：脚注 `8` 处全为 `11/30`、`November 18` 归零**。 `Baseline agent quota refreshed weekly` **仍无数字（第 `7` 期）**。",
     r42)

edit("ERNIE-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓。 本期 `downloads` 同批上跳**（`5,237` / `1,995`）；`likes` `346`（`−14`）/ `394`（`0`）。 "
     "两仓 `lastModified` 仍停 `11/05` —— **仓库没变，数字是批次刷新**（避坑 327）。",
     r42)

edit("Inkling 2 Mini 开放权重", "`thinkingmachines/Inkling-2-Mini` 开放权重",
     "🟢 **（075 期补入）`downloads` `136 → 7,944`、`likes` `705 → 3,256`（含批次刷新，不当趋势）**。 `HF` 趋势榜第 `1`；"
     "`unsloth` `GGUF` 已 `238,152` 次下载。 `~20GB` 为 `NVFP4` 权重、实测机 `48GB`。 **API 已上 `OpenRouter` 收费、无免费档**（见本表新增行）。",
     r42)

edit("Inkling 2 Small", "`thinkingmachines/Inkling-2-Small` 开放权重",
     "🟢 **`Apache-2.0`。 `downloads` `40,574 → 45,356`、`likes` `654 → 636`（`−18`）**；`lastModified` `11/20 14:09Z`。 "
     "**`OpenCode` 把它的 `Free` 变体按弃用表下架（`11/19`）** —— 权重还在，免费入口少了一个。",
     r42)

edit("Hy4 flash 开放权重", "腾讯混元 `Hy4 flash` 开放权重",
     "🟢 **（072 期补入）三仓 `gated: false`。 本期 `downloads` 同批上跳**（`5,588` / `1,535` / `826`）；`likes` `551` / `25` / `25`。 "
     "`?search=Hy4` 返回 `100`（**触 `limit` 上限，`≥100`**）。 许可 `Apache 2.0` 派生 + `§10`：对外 `MaaS` 过 `$50M` 或 `1` 亿 `MAU` 须另签。",
     r42, name="🟢 **腾讯混元 `Hy4 flash` 开放权重（**`220.25B` 实测 · 激活 `11.3B` + `0.43B` · `1M` · `Tencent Hy License 1.0`**）**")

edit("Hy4 770B", "腾讯混元 `Hy4`（旗舰 · 非 `flash`）开放权重",
     "🟢 **（075 期补登）三仓 `downloads` `228 → 1,992`（`974` / `536` / `482`）、`likes` `177` / `16` / `9`** —— 与上次解冻同型：停更一天后次日同批补算。 "
     "**`BF16` 约 `1.5TB`、`FP8` 约 `770GB` —— 开放≠可本地跑**；量化走 `AngelSlim/Hy4-GGUF`。",
     r42)

edit("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **已公开（069 期补登）。 `downloads` `2,830 → 2,949`、`likes` `361 → 278`（`−83`，统计动作，不指认原因）**。 "
     "四个时间点仍分开写：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`、媒体稿 `11/15`、**一手页无发布日期字段**。",
     r42)

edit("GPT-6.2", "OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
     "🟡 **（072 期补入）名单 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 `OpenRouter` 仍 `8` 条、**无 `:free`（第 `5` 天）**；"
     "`chatgpt.com/pricing` 第 `5` 期读不到正文；`openai.com/news` 最新条目仍是 `11/18`。 **不写「免费可用/不可用」。**",
     r42, name="🟡 **OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布（**可用名单 `Plus` / `Pro` / `Enterprise` / `Edu` · **`Free` 不在名单里**）**")

edit("Ling 3.2", "Ling 3.2 Flash` 进入 `OpenRouter`",
     "🟡 **生效中（068 期补入）。 本期两套 `id` 同形：`:free` `1` 条路由（`1,466` 字节）、基名 `0` 条（`462` 字节）** —— 连续第 `2` 期。 "
     "**三层只开两层：目录有、`:free` 路由有、权重仓仍 `404`。**",
     r42, name="🟡 **`inclusionAI` `Ling 3.2 Flash` 进入 `OpenRouter` 免费区（`:free` 零价 · `1,048,576` 上下文 · **`:free` 路由 `1` 条 / 基名 `0` 条**）**")

edit("MiniMax 第二版", "`MiniMax H3-Image` `4K` 五折 · 第二版",
     "🟠 **第二版第 `3` 天仍在架（页 `310,162 → 310,183`，`+21`）。 六档折后价全在**（`0.2261`–`0.5073`），`2026-11-18` / `截止` / `结束` 各 `0` 命中。 "
     "门槛：宽 × 高 ≥ `1660` 万像素（`4096²` 过线 `1.06%`）。 **文案里没有任何日期 —— 不替它排日。**",
     r42)


# ------------------------------------------------------------ ③ 补入新行
NEW42_INKLING_API = ("| 🟡 **`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`（**`2` 个 provider · 按量计费 · **无 `:free` 变体**）** "
                     "| **无截止日（按量计费；官方未承诺免费额度）** "
                     "| 🟡 **（076 期新增观测位）`created` 北京 `11/21 10:19`。 `PrimeIntellect` `fp4` / `1,048,576` ctx / `$0.075` 输入、`$0.30` 输出（每百万 token）；"
                     "`Io Net` `nvfp4` / `262,144` ctx / `$0.08` / `$0.35`。 `discount: 0`（原价）。 "
                     "**075 期问的「免费 API 入口」答案：收费、无免费档**；`Tinker` 侧额度仍未取到一手。 |")

idx = [k for k, r in enumerate(r42) if "`thinkingmachines/Inkling-2-Mini` 开放权重" in name_of(r)]
assert len(idx) == 1, idx
r42.insert(idx[0] + 1, NEW42_INKLING_API)


# ------------------------------------------------------------ ④ 指针重贴当期期号
def repoint(bucket):
    n = 0
    for k, r in enumerate(bucket):
        if "附录 075" in r:
            bucket[k] = r.replace("附录 075", "附录 076")
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
assert len(d42) == 53, len(d42)
assert "076 期新增观测位" in disk
assert "已过 `53` 天" in disk
assert "第 `49` 期" in disk
assert "`476/14/11`" in disk
assert "Tidepool Alpha Free" in disk
assert "附录 075" not in disk

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

ISSUE_RE = re.compile(r"(?!076)(0\d{2})\s*期")
over = [(name_of(r)[:24], len(ISSUE_RE.findall(cells_of(r)[2]))) for r in d41 + d42
        if len(ISSUE_RE.findall(cells_of(r)[2])) >= 2]
assert not over, over
print("R3 预检：0 行超 1 处")
