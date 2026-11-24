# -*- coding: utf-8 -*-
"""078 期：在 077 期现行 4.1/4.2 表体上做「天数带符号重算 + 行级改写 + 补入 1 行」。

纪律（055–077 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 状态列整体替换；⑥ 单元格不许出现 `|`；
  ⑦ 天数一律由基准日实算、断言带符号；⑧ 状态列不写「未开始 / 已结束」；
  ⑨ 本期补入 1 行（ERNIE-5.5-Flash-Preview 开放权重）→ 4.2 53 → 54；
  ⑩ 4.2 的 OpenRouter 行名带计数，改名必须在重建 CSV 之前。
"""
import io
import re
import sys
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第078期-2026-11-24.md"
PTR = " [附录 078](details.html) |"
TODAY = date(2026, 11, 24)
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
assert len(r41) == 67, ("077 期 4.1 行数", len(r41))
assert len(r42) == 53, ("077 期 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "今日（`11/24`）为截止日", st)
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


# ---- 腾讯老混元：截止列不可解析，天数与期数手工推进（09-30 起算 = 已过 55 天）
hits = [k for k, r in enumerate(r41) if "腾讯老混元" in name_of(r)]
assert len(hits) == 1
row = r41[hits[0]]
assert "已过 `54` 天" in row and "第 `50` 期" in row and "第 `41` 天" in row, row[:200]
row = (row.replace("已过 `54` 天", "已过 `55` 天")
          .replace("第 `50` 期", "第 `51` 期")
          .replace("第 `41` 天", "第 `42` 天"))
row = row.replace("六项关键词各 `0` 命中（第 `9` 期）", "六项关键词各 `0` 命中（第 `10` 期）")
row = row.replace("`6,584` 字节 / `md5` 与上期双同（第 `9` 期）", "`6,584` 字节 / `md5` 与上期双同（第 `10` 期）")
row = row.replace(" [附录 077](details.html) |", PTR)
r41[hits[0]] = row
EDITED.append("腾讯老混元(手算)")

# ---- 4.1：Hy4 flash WorkBuddy 限免
edit("Hy4 flash 限免", "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
     "🟠 **距截止 `5` 天。 限免只限 `WorkBuddy` 内的 `Hy4 flash`**；`TokenHub` 是**限时 `5` 折**。 "
     "三仓 `downloads` 本期整列冻结（`7,696` / `1,949` / `1,011`）—— **到期后能用的是权重，不是本行额度**。",
     r41, name="🟠 **腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费（**`220.25B` 实测总参（含 `64B` Engram）/ 激活 `11.3B` + `0.43B` / `1M` 上下文 · 官方口径「`11/30` 前」**）**")

# ---- 4.1：Hy4 AMA（已收口）
edit("Hy4 AMA", "腾讯混元 `Hy4` / `Hy4 flash` 官方 `Reddit` `AMA`",
     "⚪ **已收口（`11/21 02:00` 收口，已过 `3` 天）。 官方 `X` 公布 `11/20` `8–10 AM PT` ＝ 北京 `11/21 00:00–02:00`**，在 `r/LocalLLaMA` 由研发团队答问。 "
     "**`reddit.com` 三个入口连续三期 `000`，本报未抄录问答内容** —— 只记「按计划开过」。",
     r41, deadline="**北京 `11/21` 00:00–02:00（`11/20` `8–10 AM PT` 换算 · 已过 `3` 天）**")

# ---- 4.1：ERNIE 5.5 —— 承诺兑现
edit("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
     "⚪ **已兑现（`11/23 17:00` 上线三仓，已过 `1` 天）。 `?author=baidu` `39 → 42`；`Apache-2.0`、`280B` 总参 / `14B` 激活、`128` 分片。 "
     "077 期「权重仍未放」属漏抓**（比其截稿早 `2` 小时）—— 权重行见 `4.2`。",
     r41)

# ---- 4.1：MiniMax 4K —— 旧版收口（新版在 4.2）
edit("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
     "⚪ **旧版已过期（`11/18 00:00` 到期）；现行版本是第二版（无截止日、`1660` 万像素门槛），见 `4.2`。 本行只记「旧版过期」。** "
     "第二版第 `5` 天**字节第 `3` 期同值**（`310,183`），**不代表该折扣已停**。 旧文案的截止句整句不存在，**截止日不跨版本**。", r41,
     deadline="**`11/18 00:00`（北京 · 旧版逐字「即日起至 2026 年 11 月 18 日 00:00」· 已过 `6` 天）**")

# ---- 4.1：Runway Kling 4.0
edit("Runway Kling", "Runway 平台 `Kling 4.0`",
     "🟠 **生效中（距截止 `6` 天）。 （068 期补入）只在 `Standard` / `Pro` 两个付费档下列出，免费档（`125` 一次性 credits）下没有这一条**；"
     "与 `Runware` 那条 `Kling 4.0` 促销是两个分发商的两场活动，不可合并。 **折扣不是免费。** 可见文本本期只改 `<title>`。",
     r41, deadline="**`11/30`（官方逐字 `until November 30`，未写时区 · 距截止 `6` 天）**")

# ---- 4.1：Runway 企业版
edit("Runway 企业版", "Runway 企业版",
     "🟠 **生效中（距截止 `37` 天）。 （068 期补入）三个要件缺两个：`up to`（上限不是保底）、条件（`terms` 页本期未取，077 期 `404`）**。 "
     "页 `1,020,485` 字节（`+12.5%`），**可见文本仅 `<title>` 一处变化** —— 字节涨跌不作证据。",
     r41, deadline="**`12/31`（官方逐字 `Sign by 12/31`；条款页 `runway.com/terms` 本轮未取 · 距截止 `37` 天）**")

# ---- 4.1：Runware 4K 50%
edit("Runware 4K 50%", "`Runware` 分发层 `MiniMax H3-Image`",
     "⚪ **已收口（`11/17` 到期、已过 `7` 天）。 `h3-image` `18`、`4K` `40`、价目不动（`0.2261` / `0.4522` 全页仍在）** —— "
     "**076 期起按「已成稳定行为」记、不再单列次数**。 `endsAt` 数组 `22` 条与上期逐项相同；`11-23` 两条**过期一天仍在页面**。",
     r41, deadline="**`11/17`（官方促销数组 `endsAt: 2026-11-17` 逐字 · 已过 `7` 天）**")

# ---- 4.1：Runware H3 Max 30%
edit("Runware H3 Max", "`Runware` 分发层 `MiniMax H3 Max`",
     "⚪ **已过 `9` 天（`11/15` 到期）。 数组里 `endsAt: 2026-11-15` 仍在、卡片徽标卸下后未挂回** —— 「数组是账本、卡片是货架」。 "
     "本期 `endsAt` 全量 `22` 条，与上期逐项相同。",
     r41, deadline="**`11/15`（官方促销数组 `endsAt: 2026-11-15`；已过 `9` 天）**")

# ---- 4.1：AutoClaw M11W3（已收口）
edit("AutoClaw M11W3", "智谱 `AutoClaw` 国内站 `M11W3`",
     "⚪ **已收口（`11/22 23:59` 收口，已过 `2` 天）。 官方逐字 `11 月 16 日至 11 月 22 日` 登录领 `100M`（`10,000` 积分），奖励同日 `23:59` 失效**。 "
     "`M11W4` 已在 `11/23 00:00` 接班（仍 `100M`）；`M11W5` 连续第 `3` 期 `404`。 **锁客户端、导不出 `API`。**",
     r41, deadline="**`11/22 23:59`（北京时间 · 官方逐字「活动时间 11 月 16 日（周一）00:00—11 月 22 日（周日）23:59」· 已过 `2` 天）**")

# ---- 4.1：AutoClaw M11W4
edit("AutoClaw M11W4", "智谱 `AutoClaw` 国内站 `M11W4`",
     "🟠 **距截止 `5` 天。 `11/23`–`11/29` 登录领 `100M`（`10,000` 积分），`11/29 23:59` 失效**。 页 `47,974` 与上期同字节。 "
     "`100M` 连续第 `2` 周（前两周 `50M`）。 锁客户端、导不出 `API`。",
     r41, deadline="**`11/29 23:59`（北京时间 · 官方逐字「活动时间 11 月 23 日（周一）00:00—11 月 29 日（周日）23:59」· 距截止 `5` 天）**")

# ---- 4.1：Antigravity 三模型（本期无法核实）
edit("Antigravity 三模型", "`Google Antigravity` 免费档三个第三方模型",
     "🟠 **距截止 `6` 天，但本期无法核实：首页 `November 30` 已 `0` 处、横幅换成 `11/18` 的 `Gemini 4 Neon` 公告、`pricing` 页 `000`（`30` 秒超时）。** "
     "只保留 `11/17` 起连读 `3` 期的官方脚注文字，**不写「已取消」也不写「确认移除」**。",
     r41, deadline="**`11/30`（官方脚注逐字 `Will be removed on November 30, 2026.` · 距截止 `6` 天）**",
     name="🟠 **`Google Antigravity` 免费档三个第三方模型 `11/30` 移除（`Claude Sonnet 4.6` / `Claude Opus 4.6` / `GPT-OSS-120B`）**")

# ---- 4.2：OpenRouter 免费档（改名 + 状态整体替换，必须在重建 CSV 之前）
edit("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **全量 `477 → 474`（`−3`），`:free` / 零价 / `max_price=0` 三项全未动；退出的三条全是付费**（`kimi-k2` / `kimi-k2-thinking` / `mimo-v2.5-pro`）。 "
     "`dots-3-note-preview:free` 仍在目录（裸冒号 `404`、`%3A` `200`）。 `gpt-6.2` 仍 `8` 条、无 `:free`（第 `7` 天）。",
     r42, name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `474/15/12`**）**")

# ---- 4.2：OpenCode
edit("OpenCode 免费清单", "`OpenCode` 免费模型清单",
     "🟡 **整页与上期逐字节相同（`108,492` / `md5 7d206215` 双同）** —— 免费段 `11` 条、弃用表、`Jev 1.14` 定价一字未变。 "
     "**这是本报跟踪以来第一次「整页完全静止」。**",
     r42, name="🟡 **`OpenCode` 免费模型清单（`Free models` 段 `11` 条 · 本期无进出）**")

# ---- 4.2：Token 羊毛
edit("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `16` 期：`¥821 → ¥845`（`+¥24`）、卡册 `61 → 65` 张**（进 `MonkeyCode` / 海绵音乐 / `EKHOS AI`；`Cloudflare` 由 `50次` 改 `1次`）。 "
     "**本期统计规则文字未变 → 两数可比**；页面不提供逐卡拆分，**不点名涨幅来源**。",
     r42)

# ---- 4.2：Antigravity 个人免费档
edit("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
     "🟢 **逐字 `$0/month`（页 `217,127` 字节）。 免费档 `4` 模型不变**。 但**首页 `November 30` 已 `0` 处**、横幅换 `Gemini 4 Neon`（`11/18` 公告）、`pricing` 页本期 `000`。 "
     "`Baseline agent quota refreshed weekly` **仍无数字（第 `9` 期）**。",
     r42)

# ---- 4.2：ERNIE-Base
edit("ERNIE-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓。 本期 `downloads` 两仓均 `0` 变化**（`5,532` / `2,120`）；`likes` `+3` / `+1`。 "
     "**十三个仓同批冻结 → 批次快照，不是热度**（避坑 334）。",
     r42)

# ---- 4.2：Inkling 2 Mini 开放权重
edit("Inkling 2 Mini 开放权重", "`thinkingmachines/Inkling-2-Mini` 开放权重",
     "🟢 **（075 期补入）`downloads` `41,888` 本期 `0` 变化、`likes` `5,230 → 5,526`（`+296`）**。 `HF` 趋势榜仍第 `1`；"
     "`unsloth` `GGUF` 已 `805,993` 次下载（**比原仓高 `19` 倍**）。 `~20GB` 为 `NVFP4` 权重、实测机 `48GB`。 **API 见本表价格行**。",
     r42)

# ---- 4.2：inkling-2-mini 的 API 入口（顶档换人）
edit("Inkling API 定价", "`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`",
     "🟡 **（076 期新增观测位）价点仍 `4`，但顶档换人：`PrimeIntellect` `$0.12/$0.50 → $0.15/$0.60`（输入 `+25.0%`、输出 `+20.0%`）**；"
     "`Io Net` 仍 `$0.12/$0.50`，**由最贵变第二贵**。 最贵/最便宜 `4.0` 倍；无 `:free`（第 `7` 天）。",
     r42, name="🟡 **`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`（**`2` 个 provider / `4` 个价点 · 按量计费 · **无 `:free` 变体**）**")

# ---- 4.2：Inkling 2 Small
edit("Inkling 2 Small", "`thinkingmachines/Inkling-2-Small` 开放权重",
     "🟢 **`Apache-2.0`。 `downloads` `55,885`（本期 `0` 变化）、`likes` `1,420 → 1,447`（`+27`）**；`lastModified` `11/20 14:09Z`。 "
     "**`OpenCode` 把它的 `Free` 变体按弃用表下架（`11/19`）** —— 权重还在，免费入口已不在。",
     r42)

# ---- 4.2：Hy4 flash 开放权重
edit("Hy4 flash 开放权重", "腾讯混元 `Hy4 flash` 开放权重",
     "🟢 **（072 期补入）三仓 `gated: false`。 本期 `downloads` 三仓均 `0` 变化**（`7,696` / `1,949` / `1,011`）；`likes` `+22` / `+1` / `−1`。 "
     "许可 `Apache 2.0` 派生 + `§10`：对外 `MaaS` 过 `$50M` 或 `1` 亿 `MAU` 须另签。",
     r42, name="🟢 **腾讯混元 `Hy4 flash` 开放权重（**`220.25B` 实测 · 激活 `11.3B` + `0.43B` · `1M` · `Tencent Hy License 1.0`**）**")

# ---- 4.2：Hy4 770B
edit("Hy4 770B", "腾讯混元 `Hy4`（旗舰 · 非 `flash`）开放权重",
     "🟢 **（075 期补登）三仓 `downloads` `1,815` / `787` / `726`（合计 `3,328`，本期 `0` 变化）、`likes` `+20` / `+2` / `+1`**。 "
     "**`BF16` 约 `1.5TB`、`FP8` 约 `770GB` —— 开放≠可本地跑**；量化走 `AngelSlim/Hy4-GGUF`。",
     r42)

# ---- 4.2：LongCat-2.5
edit("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **已公开（069 期补登）。 `downloads` `3,303`（本期 `0` 变化）、`likes` `284 → 283`（`−1`）**。 **`OpenCode` 的免费入口已撤**（`longcat-2.5-free` 不在 `Free models` 段），"
     "**权重不受影响**。 四个时间点分开写：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`、媒体稿 `11/15`、一手页无发布日期。",
     r42)

# ---- 4.2：GPT-6.2
edit("GPT-6.2", "OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
     "🟡 **（072 期补入）名单 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 `OpenRouter` 仍 `8` 条、**无 `:free`（第 `7` 天）**；"
     "`chatgpt.com/pricing` 第 `7` 期读不到正文。 **不写「免费可用/不可用」。**",
     r42, name="🟡 **OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布（**可用名单 `Plus` / `Pro` / `Enterprise` / `Edu` · **`Free` 不在名单里**）**")

# ---- 4.2：Ling 3.2
edit("Ling 3.2", "Ling 3.2 Flash` 进入 `OpenRouter`",
     "🟡 **生效中（068 期补入）。 本期 `:free` 路由 `1` 条（`1,466` 字节）；基名本期未重取（上期 `0` 条 / `462` 字节）**。 "
     "**三层只开两层：目录有、`:free` 路由有、权重仓仍 `404`。**",
     r42, name="🟡 **`inclusionAI` `Ling 3.2 Flash` 进入 `OpenRouter` 免费区（`:free` 零价 · `1,048,576` 上下文 · **`:free` 路由 `1` 条**）**")

# ---- 4.2：MiniMax 第二版
edit("MiniMax 第二版", "`MiniMax H3-Image` `4K` 五折 · 第二版",
     "🟠 **第二版第 `5` 天仍在架（页 `310,183`，第 `3` 期同值；`md5` 变）。 六档折后价全在**（`0.2261`–`0.5073`），`2026-11-18` / `截止` / `结束` 各 `0` 命中。 "
     "门槛：宽 × 高 ≥ `1660` 万像素。 **文案里没有任何日期 —— 不替它排日。**",
     r42)

# ------------------------------------------------------------ ③ 补入 1 行（4.2）
NEW_NAME = ("🟢 **百度 `ERNIE-5.5-Flash-Preview` 开放权重（**`Apache-2.0` · `280B` 总参 / `14B` 激活 · `1M` 上下文 · 本期补登**）**")
NEW_DL = "**无结束日（`Apache-2.0` 开放权重；建仓 `11/23 09:00:29Z` ＝ 北京 `17:00`）**"
NEW_ST = ("🟢 **已开放权重（四层全通 · 本期补登）。 `11/23 17:00`（北京）上线三仓（主仓 / `FP8` / `BF16`），`?author=baidu` `39 → 42` 仓；"
          "总参张量 `299.6B`、`128` 个分片、`142` 个文件。 `LICENSE` 逐字 `Apache License Version 2.0` —— 无商用门槛。 "
          "`BF16` 约 `560GB` / `FP8` 约 `280GB`，**能下载 ≠ 能本地跑**。")
assert "|" not in NEW_NAME + NEW_DL + NEW_ST
NEW_ROW = "|%s| %s | %s%s" % (NEW_NAME, NEW_DL, NEW_ST, PTR)

anchor = [k for k, r in enumerate(r42) if "百度开源 `ERNIE-5.5-Flash-Base`" in name_of(r)]
assert len(anchor) == 1, anchor
r42.insert(anchor[0] + 1, NEW_ROW)
EDITED.append("补入 ERNIE-5.5-Flash-Preview")


# ------------------------------------------------------------ ④ 指针重贴当期期号
def repoint(bucket):
    n = 0
    for k, r in enumerate(bucket):
        if "附录 077" in r:
            bucket[k] = r.replace("附录 077", "附录 078")
            n += 1
    return n


print("指针重贴：4.1", repoint(r41), "4.2", repoint(r42))
print("改写行：", len(EDITED), EDITED)
print("输出行数：4.1 = %d，4.2 = %d" % (len(r41), len(r42)))
assert all(len(cells_of(r)) == 3 for r in r41 + r42)

if DRY:
    print("41 样本", r41[3][:300])
    print("42 新行", NEW_ROW[:300])
    print("DRY RUN —— 未写盘")
    sys.exit(0)

# ------------------------------------------------------------ ⑤ 写回（原地替换两个表块，其余一字不动）
NL = chr(10)
old_41 = NL.join(rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更"))
old_42 = NL.join(rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注"))
assert md.count(old_41) == 1 and md.count(old_42) == 1
new_md = md.replace(old_41, NL.join(r41), 1).replace(old_42, NL.join(r42), 1)

# 标题与统计句：67 / 53 → 54，142 → 143，195 → 196
assert "### 4.2 常驻权益本期变更（无截止日 · 本期有变化 53 条）" in new_md
new_md = new_md.replace("### 4.2 常驻权益本期变更（无截止日 · 本期有变化 53 条）",
                        "### 4.2 常驻权益本期变更（无截止日 · 本期有变化 54 条）")
assert new_md.count("**其余 `142` 条常驻权益本期无变化，未逐条重印**") == 2, new_md.count("**其余 `142` 条")
new_md = new_md.replace("**其余 `142` 条常驻权益本期无变化，未逐条重印**",
                        "**其余 `143` 条常驻权益本期无变化，未逐条重印**")
assert new_md.count("（`195` 条）") == 2
new_md = new_md.replace("（`195` 条）", "（`196` 条）")
assert "**`4.2` 收录 `53` 条" in new_md
new_md = new_md.replace("**`4.2` 收录 `53` 条", "**`4.2` 收录 `54` 条")

assert new_md != md
io.open(MD, "w", encoding="utf-8", newline=NL).write(new_md)

back = io.open(MD, encoding="utf-8").read()
assert "474/15/12" in back and "`108,492`" in back
assert back.count("附录 078") > 60, back.count("附录 078")
assert "附录 077" not in back
assert "其余 `143` 条常驻权益本期无变化" in back
assert "本期有变化 54 条" in back
rb = rows_of(back, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
rb2 = rows_of(back, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("落盘复核：4.1 = %d，4.2 = %d，字节 = %d" % (len(rb), len(rb2), len(back.encode("utf-8"))))
assert len(rb) == 67 and len(rb2) == 54
print("OK")
