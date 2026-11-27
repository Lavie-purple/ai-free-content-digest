# -*- coding: utf-8 -*-
"""081 期：在 080 期现行 4.1/4.2 表体上做「天数重算 + 行级改写」。

纪律（055–080 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 状态列整体替换；⑥ 单元格不许出现 `|`；
  ⑦ 天数一律由基准日实算（断言带符号）；⑧ 状态列不写「未开始 / 已结束」；
  ⑨ 本期无归档、无补入（4.1 仍 65、4.2 仍 54），只改读数；
  ⑩ 4.2 的 OpenRouter 行名带计数（474/14/11 → 477/14/11）、inkling 行名带 provider 数
     （7 → 6），两处改名都必须在《总账》里先改、再按 `key()` 同步。
"""
import io
import re
import sys
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第081期-2026-11-27.md"
PTR = " [附录 081](details.html) |"
TODAY = date(2026, 11, 27)
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
assert len(r41) == 65, ("080 期 4.1 行数", len(r41))
assert len(r42) == 54, ("080 期 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "今日（`11/27`）为截止日", st)
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

# ------------------------------------------------------------ ② 行级改写
EDITED = []


def find(bucket, prefix, tag):
    hits = [k for k, r in enumerate(bucket) if prefix in name_of(r)]
    assert len(hits) == 1, ("命中数不是 1", tag, len(hits))
    return hits[0]


def set_row(tag, prefix, status=None, bucket=None, deadline=None, name=None):
    b = bucket if bucket is not None else r41
    k = find(b, prefix, tag)
    c = cells_of(b[k])
    assert len(c) == 3, ("字段数异常", tag, len(c))
    st = status if status is not None else c[2]
    dl = deadline if deadline is not None else c[1]
    nm = name if name is not None else c[0]
    for v, lab in ((st, "状态"), (dl, "截止"), (nm, "活动名")):
        assert "|" not in v, ("单元格里出现竖线", tag, lab)
    new = "|%s| %s | %s%s" % (nm, dl, st, PTR)
    assert new != b[k], ("改写未生效", tag)
    b[k] = new
    EDITED.append((tag, "4.2" if b is r42 else "4.1"))


# ---- 4.1：腾讯老混元（截止列不可解析，手算 09-30 → 已过 58 天）
k = find(r41, "腾讯老混元", "腾讯老混元")
r41[k] = ("| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必办（已过 `58` 天，Q04 连续第 `54` 期未决 · 高危窗口第 `45` 天）。 "
          "厂商仍只给「9 月底」这一模糊口径，未给确切停服日。 `hunyuan.tencent.com` 本期 **`6,318` 字节（`−266`）**，仍是 `app-skeleton` 骨架屏，六项关键词各 `0` 命中（第 `13` 期）**；"
          "迁移目标 `TokenHub` 的两个入口本期均未给出新的迁移截止。**" + PTR)
EDITED.append(("腾讯老混元(手算)", "4.1"))

# ---- 4.1：Hy4 flash WorkBuddy 限免（downloads 全冻结）
set_row("Hy4 flash 限免", "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
        "🟠 **距截止 `2` 天。 限免只限 `WorkBuddy` 内的 `Hy4 flash`**；`TokenHub` 是**限时 `5` 折**。 "
        "三仓 `downloads` 本期 `10,479` / `2,472` / `1,280`（**合计 `0` 变化 —— 整列批次快照冻结**），`likes` `+36` / `0` / `0`。 "
        "**到期后能用的是权重，不是本行额度**。",
        r41)

# ---- 4.1：ERNIE 5.5（第三天读数）
set_row("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
        "⚪ **已兑现（`11/23 17:00` 上线三仓，已过 `4` 天）。 三仓 `downloads` 仍 `1,955`（**整列冻结**），`likes` `360 → 405`（`+45`）**。 "
        "`?author=baidu` 仍 `42` 仓、`0` 新增；社区首个 `GGUF` 仍在（`11/25 13:35Z`，下载 `0`）。 **判热度改用 `likes`（避坑 345）。**",
        r41, deadline="**`11/25` 前（官方逐字 `权重将于11月25日前开源` —— 是「前」不是「当天」；媒体统一写成 `11月25日` · 已过 `2` 天）**")

# ---- 4.1：MiniMax 4K 旧版
set_row("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
        "⚪ **旧版已过期（`11/18 00:00` 到期）；现行版本是第二版（无截止日、`1660` 万像素门槛），见 `4.2`。 本行只记「旧版过期」。** "
        "第二版第 `9` 天**字节 `309,394`（`−148`）**，六档折后价与标题一字未变，**不代表该折扣已停**。 截止日不跨版本。",
        r41, deadline="**`11/18 00:00`（北京 · 旧版逐字「即日起至 2026 年 11 月 18 日 00:00」· 已过 `9` 天）**")

# ---- 4.1：Runway Kling 4.0
set_row("Runway Kling", "Runway 平台 `Kling 4.0`",
        "🟠 **距截止 `3` 天。 （068 期补入）只在 `Standard` / `Pro` 两个付费档下列出，免费档（`125` 一次性 credits）下没有这一条**；"
        "与 `Runware` 那条 `Kling 4.0` 促销是两个分发商的两场活动，不可合并。 **折扣不是免费。** "
        "**本期载荷 `1,312,933` 字节、`25% off` `21` 处（第 `3` 期不变）、`expiresAt: 2026-12-01T05:00:00Z`** —— 按配置换算，实际截止是北京 `12/1 13:00`。",
        r41, deadline="**`11/30`（官方逐字 `until November 30`；配置层 `expiresAt 2026-12-01T05:00:00Z` ＝ 北京 `12/1 13:00` —— 两个时点并排写 · 距截止 `3` 天）**")

# ---- 4.1：Runway 企业版
set_row("Runway 企业版", "Runway 企业版",
        "🟠 **生效中（距截止 `34` 天）。 （068 期补入）三个要件缺两个：`up to`（上限不是保底）、条件（`terms` 页 077 期 `404`）**。 "
        "页 `1,312,933` 字节（`+2,077`）、可见文本 `379` 行（`+5`），企业版横幅仍在 —— **字节与行数的抖动不等于条目变化**（避坑 342）。",
        r41, deadline="**`12/31`（官方逐字 `Sign by 12/31`；条款页 `runway.com/terms` 本轮未取 · 距截止 `34` 天）**")

# ---- 4.1：AutoClaw M11W3（已收口）
set_row("AutoClaw M11W3", "智谱 `AutoClaw` 国内站 `M11W3`",
        "⚪ **已收口（`11/22 23:59` 收口，已过 `5` 天）。 官方逐字 `11 月 16 日至 11 月 22 日` 登录领 `100M`（`10,000` 积分），奖励同日 `23:59` 失效**。 "
        "`M11W4` 已接班（仍 `100M`）；`M11W5` 连续第 `6` 期 `404`。 **锁客户端、导不出 `API`。**",
        r41, deadline="**`11/22 23:59`（北京时间 · 官方逐字「活动时间 11 月 16 日（周一）00:00—11 月 22 日（周日）23:59」· 已过 `5` 天）**")

# ---- 4.1：AutoClaw M11W4
set_row("AutoClaw M11W4", "智谱 `AutoClaw` 国内站 `M11W4`",
        "🟠 **距截止 `2` 天。 `11/23`–`11/29` 登录领 `100M`（`10,000` 积分），`11/29 23:59` 失效**。 页 `48,257` 字节 —— **与上期完全同字节，`md5` 也未变**，周档页发完即冻结。 "
        "**`M11W5` 第 `6` 期仍 `404`，周档到点才挂。**",
        r41, deadline="**`11/29 23:59`（北京时间 · 官方逐字「活动时间 11 月 23 日（周一）00:00—11 月 29 日（周日）23:59」· 距截止 `2` 天）**")

# ---- 4.1：Antigravity（免费档 4 个挂脚注）
set_row("Antigravity 三模型", "`Google Antigravity` 免费档三个第三方模型",
        "🟠 **距截止 `3` 天。 本期 `pricing` 页 `200` / `188,088` 字节（与 079、080 完全同字节），脚注逐字 `Will be removed on November 30, 2026.` 共 `13` 处**。 "
        "免费档 `$0/month` 列 `5` 个模型，其中 **`4` 个**挂该脚注（含第一方 `Gemini 3.8 Flash`）** —— **`11/30` 后只剩 `Gemini 4 Hydrogen` `1` 个**。 "
        "⚠️ **行名沿用 080 期的「三个第三方模型」，实际是 `4` 个 —— 见第五章第 `1` 条。**",
        r41, deadline="**`11/30`（官方脚注逐字 `Will be removed on November 30, 2026.` · 距截止 `3` 天）**")

# ---- 4.2：OpenRouter 免费档（改名 474/14/11 → 477/14/11）
set_row("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
        "🟢 **全量 `474 → 477`（进 `3` / 出 `0`）、免费三项 `11 / 14 / 13` 全未动（第 `3` 期）**。 "
        "三条新进里 `2` 条是 `2025` 年的 `Kimi K2` 回架（`created` `2025-07-11` / `2025-09-04`），唯一新条目 `inclusionai/lingsante-3.1-air-vl` 的权重仓建于 `11/19`。 "
        "`:batch` 仍 `96` 条、那 `4` 条贵价一分未改。 `gpt-6.2` 仍 `8` 条、无 `:free`（第 `10` 天）。",
        r42, name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `477/14/11`**）**")

# ---- 4.2：OpenCode 免费清单
set_row("OpenCode 免费清单", "`OpenCode` 免费模型清单",
        "🟡 **`108,827 → 104,585`（两期累计 `−4,242`）、本期 `+729` 字节 / 可见行 `1,646`（`+14`）**。 "
        "免费段 `11` 个唯一 `id`（`-free` 严格匹配），**与 079 比唯一新增 `seaglass-alpha-free`**；价格表一行未变。 **字节变化只是哨子**（避坑 343）。",
        r42, name="🟡 **`OpenCode` 免费模型清单（`Free models` 段 `11` 条 · 本期 `+1`）**")

# ---- 4.2：Token 羊毛（第 19 期）
set_row("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
        "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `19` 期：`¥845`（`−2`）、卡册 `65` 张（`+4`）** —— **一对数原样退回 079 期的组合**（080 的 `¥847 / 61` 只维持一期）。 "
        "**金额与张数各自独立，不能互校**；`JSON-LD` 只暴露首页一批，其余不逐条归因。",
        r42)

# ---- 4.2：Antigravity 个人免费档
set_row("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
        "🟢 **逐字 `$0/month`（`pricing` 页本期 `200` / `188,088`，与 079、080 同字节）。 免费档列 `5` 个模型，其中 `4` 个挂 `11/30` 移除脚注（脚注 `13` 处）** —— **撤完只剩 `1` 个**。 "
        "`Baseline agent quota refreshed weekly` **仍无数字（第 `12` 期）**。 **免费档模型数只认定价页**（避坑 340）。",
        r42)

# ---- 4.2：ERNIE-5.5-Flash-Base
set_row("ERNIE-5.5-Flash-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
        "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓。 本期 `downloads` 两仓仍是 `5,938` / `2,308`（`0` 变化）、`likes` `353` / `395`（`0` / `0`）**。 "
        "**整列冻结期 → 这一格本期没有新信息，不写「齐涨」**（避坑 345）。",
        r42)

# ---- 4.2：Inkling 2 Mini（开放权重）
set_row("Inkling 2 Mini", "`thinkingmachines/Inkling-2-Mini` 开放权重",
        "🟢 **`96,527` 下载（`0` 变化，整列冻结）、`likes` `6,040 → 6,256`（`+216`，十五仓里最大增量）**。 "
        "**趋势榜仍第 `1`** —— 热度没降，只是 `downloads` 不刷新（避坑 345）。",
        r42)

# ---- 4.2：inkling-2-mini 的 API 入口（价点 7 → 6）
set_row("inkling-2-mini API", "`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`",
        "🟡 **（076 期新增观测位）价点 `7 → 6`：`Relace`（`$0.075 / $0.30`、ctx `131,072`）本期消失，其余六家一字未改**；"
        "地板价仍 `Darkbloom` `$0.02625 / $0.105`，顶档 `PrimeIntellect` `$0.15 / $0.60`；**最贵/最便宜 `5.71×` 未变**。 "
        "**价点是瞬时快照，不作趋势**（避坑 346）；无 `:free`（第 `10` 天）。",
        r42, name="🟡 **`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`（**`6` 个 provider / `6` 个价点 · 按量计费 · **无 `:free` 变体**）**")

# ---- 4.2：Inkling 2 Small
set_row("Inkling 2 Small", "`thinkingmachines/Inkling-2-Small` 开放权重",
        "🟢 **`78,274` 下载（`0` 变化）、`likes` `1,501 → 1,528`（`+27`）**。 **同门 `Mini` 的增量是它的 `8` 倍，小模型的热度仍集中在小尺寸那一档。**",
        r42)

# ---- 4.2：Hy4 flash（权重）
set_row("Hy4 flash 权重", "腾讯混元 `Hy4 flash` 开放权重",
        "🟢 **（072 期补入）三仓 `gated: false`。 本期 `downloads` 三仓仍是 `10,479` / `2,472` / `1,280`（`0` 变化，整列冻结）、`likes` `+36` / `0` / `0`**。 "
        "许可 `Apache 2.0` 派生 + `§10`：对外 `MaaS` 过 `$50M` 或 `1` 亿 `MAU` 须另签。",
        r42)

# ---- 4.2：Hy4（770B）
set_row("Hy4 770B", "腾讯混元 `Hy4`（旗舰 · 非 `flash`）开放权重",
        "🟢 **（075 期补登）三仓 `downloads` `2,898` / `993` / `873`（合计 `4,764`，本期 `0` 变化）、`likes` `+31` / `0` / `0`**。 "
        "**`BF16` 约 `1.5TB`、`FP8` 约 `770GB` —— 开放≠可本地跑**；量化走 `AngelSlim/Hy4-GGUF`。",
        r42)

# ---- 4.2：LongCat-2.5
set_row("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT` 公开权重",
        "🟢 **已公开（069 期补登）。 `downloads` `3,722`（`0` 变化）、`likes` `285`（`0`）**。 "
        "**同门 `LongCat-2.0` 本期 `2,664`（`0` 变化）** —— 080 期把它上一期的 `−29` 记成「滚动窗口」，**本期整列冻结后修正为「批次重算」**（第五章第 `2` 条 / 避坑 345）。",
        r42)

# ---- 4.2：GPT-6.2
set_row("GPT-6.2", "OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
        "🟡 **（072 期补入）名单 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 `OpenRouter` 仍 `8` 条、**无 `:free`（第 `10` 天）**；"
        "`chatgpt.com/pricing` 第 `11` 期读不到正文（`301` 后 `0` 字节）**。 **不写「免费可用/不可用」。**",
        r42)

# ---- 4.2：MiniMax 4K 第二版（第 9 天）
set_row("MiniMax 4K 第二版", "`MiniMax H3-Image` `4K` 五折 · 第二版",
        "🟠 **第二版第 `9` 天仍在架（页 `309,394`，字节 `−148`，六档折后价与标题一字未变）。 六档折后价全在**（`0.2261`–`0.5073`），`2026-11-18` / `截止` / `结束` 各 `0` 命中。 "
        "**文案里没有任何日期 —— 不替它排日。**",
        r42)

# ------------------------------------------------------------ ③ 写回（原地替换两个表块）
assert len(r41) == 65
NL = chr(10)
old_41 = NL.join(rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更"))
old_42 = NL.join(rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注"))
assert md.count(old_41) == 1 and md.count(old_42) == 1
new_md = md.replace(old_41, NL.join(r41), 1).replace(old_42, NL.join(r42), 1)

n_edit = len([e for e in EDITED if e[1] == "4.2"])
n_carry = 54 - n_edit
assert "本期改写 `13` 条、补入 `0` 条、其余 `41` 条沿用上期读数" in new_md, "4.2 统计句未找到"
new_md = new_md.replace("本期改写 `13` 条、补入 `0` 条、其余 `41` 条沿用上期读数",
                        "本期改写 `%d` 条、补入 `0` 条、其余 `%d` 条沿用上期读数" % (n_edit, n_carry))

assert new_md != md
if DRY:
    print("DRY RUN —— 未写盘；改写 4.2 %d 行 / 4.1 %d 行；4.1 = %d"
          % (n_edit, len(EDITED) - n_edit, len(r41)))
    print("EDITED:", EDITED)
    sys.exit(0)

io.open(MD, "w", encoding="utf-8", newline=NL).write(new_md)

# ------------------------------------------------------------ ④ 落盘复核
back = io.open(MD, encoding="utf-8").read()
rb = rows_of(back, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
rb2 = rows_of(back, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("落盘复核：4.1 = %d，4.2 = %d，字节 = %d" % (len(rb), len(rb2), len(back.encode("utf-8"))))
assert len(rb) == 65 and len(rb2) == 54
assert "`477/14/11`" in back and "`474/14/11`" not in back
assert "`6` 个 provider" in back and "`7` 个 provider" not in back
assert "`endpoints: []`" in back
assert "本期改写 `%d` 条" % n_edit in back
for tag, phrase in (("Hy4 flash 限免", "`2` 天"), ("M11W4", "`2` 天"),
                    ("Antigravity 三模型", "`4` 个**"), ("Token 羊毛", "`65` 张")):
    assert phrase in back, (tag, phrase)
print("OK 改写 =", n_edit, "｜沿用 =", n_carry)
