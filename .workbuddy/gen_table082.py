# -*- coding: utf-8 -*-
"""082 期：在 081 期现行 4.1/4.2 表体上做「天数重算 + 行级改写」。

纪律（055–081 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 状态列整体替换；⑥ 单元格不许出现 `|`；
  ⑦ 天数一律由基准日实算（断言带符号）；⑧ 状态列不写「未开始 / 已结束」；
  ⑨ 本期无归档、无补入（4.1 仍 65、4.2 仍 54），只改读数；
  ⑩ 4.2 的 OpenRouter 行名带计数（477/14/11 → 475/13/10）、OpenCode 行名带条数。
"""
import io
import re
import sys
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第082期-2026-11-28.md"
PTR = " [附录 082](details.html) |"
TODAY = date(2026, 11, 28)
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
assert len(r41) == 65, ("输入 4.1 行数", len(r41))
assert len(r42) == 54, ("输入 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "今日（`11/28`）为截止日", st)
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


# ---- 4.1：腾讯老混元（截止列不可解析，手算 09-30 → 已过 59 天）
k = find(r41, "腾讯老混元", "腾讯老混元")
r41[k] = ("| 🔴 **腾讯老混元大模型平台停服** | **2026 年 9 月底** | 🔴 **必办（已过 `59` 天，Q04 连续第 `55` 期未决 · 高危窗口第 `46` 天）。 "
          "厂商仍只给「9 月底」这一模糊口径，未给确切停服日。 `hunyuan.tencent.com` 本期 **`6,318` 字节（`0` 变化）**，仍是 `app-skeleton` 骨架屏，六项关键词各 `0` 命中（第 `14` 期）**；"
          "迁移目标 `TokenHub` 的两个入口本期均未给出新的迁移截止。**" + PTR)
EDITED.append(("腾讯老混元(手算)", "4.1"))

# ---- 4.1：Hy4 flash WorkBuddy 限免（downloads 解冻）
set_row("Hy4 flash 限免", "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
        "🟠 **距截止 `1` 天。 限免只限 `WorkBuddy` 内的 `Hy4 flash`**；`TokenHub` 是**限时 `5` 折**。 "
        "三仓 `downloads` 本期 `12,933` / `2,933` / `1,469`（**合计 `+3,104` —— 整列解冻**），`likes` `+32` / `+2` / `0`。 "
        "**到期后能用的是权重，不是本行额度**。",
        r41)

# ---- 4.1：ERNIE 5.5（第四天读数）
set_row("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
        "⚪ **已兑现（`11/23 17:00` 上线三仓，已过 `3` 天）。 三仓 `downloads` `2,609` / `792` / `825`（**`+1,416` / `+418` / `+437`，解冻后补涨），`likes` `394` / `30` / `25`**。 "
        "`?author=baidu` 仍 `42` 仓、`0` 新增；社区首个 `GGUF` 仍在（`11/25 13:35Z`，下载 `0`）。 **判热度改用 `likes`（避坑 345）。**",
        r41, deadline="**`11/25` 前（官方逐字 `权重将于11月25日前开源` —— 是「前」不是「当天」；媒体统一写成 `11月25日` · 已过 `3` 天）**")

# ---- 4.1：MiniMax 4K 旧版
set_row("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
        "⚪ **旧版已过期（`11/18 00:00` 到期）；现行版本是第二版（无截止日、`1660` 万像素门槛），见 `4.2`。 本行只记「旧版过期」。** "
        "第二版第 `10` 天**字节 `309,394`（`0` 变化）**，六档折后价与标题一字未变，**不代表该折扣已停**。 截止日不跨版本。",
        r41, deadline="**`11/18 00:00`（北京 · 旧版逐字「即日起至 2026 年 11 月 18 日 00:00」· 已过 `10` 天）**")

# ---- 4.1：Runway Kling 4.0
set_row("Runway Kling", "Runway 平台 `Kling 4.0`",
        "🟠 **距截止 `2` 天。 （068 期补入）只在 `Standard` / `Pro` 两个付费档下列出，免费档（`125` 一次性 credits）下没有这一条**；"
        "与 `Runware` 那条 `Kling 4.0` 促销是两个分发商的两场活动，不可合并。 **折扣不是免费。** "
        "**本期载荷 `1,069,415` 字节（`−243,518`）、`25% off` `15` 处、`expiresAt` 归零（上期 `2` 处）** —— 促销仍在架，配置字段整段消失（五章第 `3` 条）。",
        r41, deadline="**`11/30`（官方逐字 `Kling 4.0 generations until November 30`；配置层 `expiresAt` 本期未下发 —— 只按文案记 · 距截止 `2` 天）**")

# ---- 4.1：Runway 企业版
set_row("Runway 企业版", "Runway 企业版",
        "🟠 **生效中（距截止 `33` 天）。 （068 期补入）三个要件缺两个：`up to`（上限不是保底）、条件（`terms` 页 077 期 `404`）**。 "
        "页 `1,069,415` 字节（`−243,518`），企业版横幅仍在 —— **字节与行数的抖动不等于条目变化**（避坑 342）。",
        r41, deadline="**`12/31`（官方逐字 `Sign by 12/31`；条款页 `runway.com/terms` 本轮未取 · 距截止 `33` 天）**")

# ---- 4.1：AutoClaw M11W3（已收口）
set_row("AutoClaw M11W3", "智谱 `AutoClaw` 国内站 `M11W3`",
        "⚪ **已收口（`11/22 23:59` 收口，已过 `6` 天）。 官方逐字 `11 月 16 日至 11 月 22 日` 登录领 `100M`（`10,000` 积分），奖励同日 `23:59` 失效**。 "
        "`M11W4` 已接班（仍 `100M`）；`M11W5` 连续第 `7` 期 `404`。 **锁客户端、导不出 `API`。**",
        r41, deadline="**`11/22 23:59`（北京时间 · 官方逐字「活动时间 11 月 16 日（周一）00:00— 11 月 22 日（周日）23:59」· 已过 `6` 天）**")

# ---- 4.1：AutoClaw M11W4
set_row("AutoClaw M11W4", "智谱 `AutoClaw` 国内站 `M11W4`",
        "🟠 **距截止 `1` 天。 `11/23`–`11/29` 登录领 `100M`（`10,000` 积分），`11/29 23:59` 失效**。 页 `48,257` 字节 —— **连续 `3` 期完全同字节，`md5` 也未变**，周档页发完即冻结。 "
        "**`M11W5` 第 `7` 期仍 `404`，周档到点才挂。**",
        r41, deadline="**`11/29 23:59`（北京时间 · 官方逐字「活动时间 11 月 23 日（周一）00:00— 11 月 29 日（周日）23:59」· 距截止 `1` 天）**")

# ---- 4.1：Antigravity（免费档 4 个挂脚注）
set_row("Antigravity 三模型", "`Google Antigravity` 免费档三个第三方模型",
        "🟠 **距截止 `2` 天。 本期 `pricing` 页 `200` / `188,088` 字节（与 079–081 连续 `4` 期完全同字节），脚注逐字 `Will be removed on November 30, 2026.` 共 `13` 处**。 "
        "免费档 `$0/month` 列 `5` 个模型，其中 **`4` 个**挂该脚注（含第一方 `Gemini 3.8 Flash`）** —— **`11/30` 后只剩 `Gemini 4 Hydrogen` `1` 个**。 "
        "⚠️ **行名沿用 080 期的「三个第三方模型」，实际是 `4` 个 —— 见第五章第 `1` 条。**",
        r41, deadline="**`11/30`（官方脚注逐字 `Will be removed on November 30, 2026.` · 距截止 `2` 天）**")

# ---- 4.2：OpenRouter 免费档（改名 477/14/11 → 475/13/10）
set_row("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
        "🟢 **全量 `477 → 475`（进 `1` / 出 `3`）、免费三项 `11 / 14 / 13` → `10 / 13 / 12`（同向 `−1`）**。 "
        "唯一进项是 `inclusionai/ling-3.2-flash:free` **摘掉 `:free` 后缀**后的本体，同档案改按 `$0.30 / $0.90` 收费；真下架只有 `qwen/qwen3-235b-a22b-thinking-2507` 一条。 "
        "`:batch` `96 → 95`、那 `4` 条贵价第 `3` 期一分未改。 `gpt-6.2` 仍 `8` 条、无 `:free`（第 `11` 天）。",
        r42, name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `475/13/10`**）**")

# ---- 4.2：OpenCode 免费清单
set_row("OpenCode 免费清单", "`OpenCode` 免费模型清单",
        "🟡 **`104,585 → 110,635`（本期 `+6,050` 字节）、免费段 `11` 个唯一 `id`（`-free` 严格匹配）** —— **与上期集合比对差集为空**。 "
        "新增的全是付费行（`SystemOne` 系列等），**免费段一字未动**；价格表变动与免费条目无关。 **字节变化只是哨子**（避坑 343 / 351）。",
        r42, name="🟡 **`OpenCode` 免费模型清单（`Free models` 段 `11` 条 · 与上期相同）**")

# ---- 4.2：Token 羊毛（第 20 期）
set_row("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
        "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `20` 期：`¥784`（`−61`）、卡册 `67` 张（`+2`）** —— **第一次「钱掉、卡涨」**（前四期是 `845/65 → 847/61 → 845/65` 来回摆）。 "
        "**金额与张数各自独立，不能互校**；`JSON-LD` 只暴露首页一批，其余不逐条归因。",
        r42)

# ---- 4.2：Antigravity 个人免费档
set_row("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
        "🟢 **逐字 `$0/month`（`pricing` 页本期 `200` / `188,088`，连续 `4` 期同字节）。 免费档列 `5` 个模型，其中 `4` 个挂 `11/30` 移除脚注（脚注 `13` 处）** —— **撤完只剩 `1` 个**。 "
        "`Baseline agent quota refreshed weekly` **仍无数字（第 `13` 期）**。 **免费档模型数只认定价页**（避坑 340）。",
        r42)

# ---- 4.2：ERNIE-5.5-Flash-Base
set_row("ERNIE-5.5-Flash-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
        "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓。 本期 `downloads` 两仓 `6,417` / `2,506`（**`+479` / `+198`，整列解冻**）、`likes` `355` / `395`（`+2` / `0`）**。 "
        "**解冻后补涨，不写「需求爆发」**（避坑 349）。",
        r42)

# ---- 4.2：Inkling 2 Mini（开放权重）
set_row("Inkling 2 Mini", "`thinkingmachines/Inkling-2-Mini` 开放权重",
        "🟢 **`155,741` 下载（`+59,214`，本期最大增量）、`likes` `6,256 → 6,514`（`+258`）**。 "
        "**趋势榜仍第 `1`** —— 解冻后补涨，与 `likes` 同向。",
        r42)

# ---- 4.2：inkling-2-mini 的 API 入口（价点 6）
set_row("inkling-2-mini API", "`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`",
        "🟡 **（076 期新增观测位）价点 `6`、provider `6` —— 与上期逐项相同（`Relace` 未回归，第 `2` 期）**；"
        "地板价仍 `Darkbloom` `$0.02625 / $0.105`，顶档 `PrimeIntellect` `$0.15 / $0.60`；**最贵/最便宜 `5.71×` 未变**。 "
        "**价点是瞬时快照，不作趋势**（避坑 346）；无 `:free`（第 `11` 天）。",
        r42, name="🟡 **`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`（**`6` 个 provider / `6` 个价点 · 按量计费 · **无 `:free` 变体**）**")

# ---- 4.2：Inkling 2 Small
set_row("Inkling 2 Small", "`thinkingmachines/Inkling-2-Small` 开放权重",
        "🟢 **`100,356` 下载（`+22,082`）、`likes` `1,528 → 1,568`（`+40`）**。 **同门 `Mini` 的增量是它的 `2.7` 倍，小模型的热度仍集中在小尺寸那一档。**",
        r42)

# ---- 4.2：Hy4 flash（权重）
set_row("Hy4 flash 权重", "腾讯混元 `Hy4 flash` 开放权重",
        "🟢 **（072 期补入）三仓 `gated: false`。 本期 `downloads` 三仓 `12,933` / `2,933` / `1,469`（**合计 `+3,104`，整列解冻**）、`likes` `+32` / `+2` / `0`**。 "
        "许可 `Apache 2.0` 派生 + `§10`：对外 `MaaS` 过 `$50M` 或 `1` 亿 `MAU` 须另签。",
        r42)

# ---- 4.2：Hy4（770B）
set_row("Hy4 770B", "腾讯混元 `Hy4`（旗舰 · 非 `flash`）开放权重",
        "🟢 **（075 期补登）三仓 `downloads` `4,106` / `1,222` / `1,470`（合计 `6,798`，本期 `+2,034`）、`likes` `+1` / `0` / `+7`**。 "
        "**`BF16` 约 `1.5TB`、`FP8` 约 `770GB` —— 开放≠可本地跑**；量化走 `AngelSlim/Hy4-GGUF`。",
        r42)

# ---- 4.2：LongCat-2.5
set_row("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT` 公开权重",
        "🟢 **已公开（069 期补登）。 `downloads` `4,032`（`+310`）、`likes` `286`（`+1`）**。 "
        "**同门 `LongCat-2.0` 本期 `2,645`（`−19`）—— 连续第 `2` 次倒退**，同一批刷新里只有它往回走（五章第 `1` 条 / 避坑 349）。",
        r42)

# ---- 4.2：GPT-6.2
set_row("GPT-6.2", "OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
        "🟡 **（072 期补入）名单 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 `OpenRouter` 仍 `8` 条、**无 `:free`（第 `11` 天）**；"
        "`chatgpt.com/pricing` 第 `12` 期读不到正文（`301` 后 `0` 字节）**。 **`11/26` 计费修复后额度消耗加快（`Astra` `40%` / `Sol` `25%`），补偿为一次 `banked reset`（第三章第 `7` 条）。**",
        r42)

# ---- 4.2：MiniMax 4K 第二版（第 10 天）
set_row("MiniMax 4K 第二版", "`MiniMax H3-Image` `4K` 五折 · 第二版",
        "🟠 **第二版第 `10` 天仍在架（页 `309,394`，与上期完全同字节，六档折后价与标题一字未变）。 六档折后价全在**（`0.2261`–`0.5073`），`2026-11-18` / `截止` / `结束` 各 `0` 命中。 "
        "**文案里没有任何日期 —— 不替它排日。**",
        r42)

# ---- 4.2：Ling 3.2 Flash（本期退出免费区 · 色标 🟡 → 🟠）
set_row("Ling 3.2 Flash", "`inclusionAI` `Ling 3.2 Flash` 进入 `OpenRouter` 免费区",
        "🟠 **本期退出免费区（`082` 期起）：`:free` 后缀被摘掉，同一档案改按 `$0.30 / $0.90` 每百万 token 收费（缓存读 `$0.06`）**。 "
        "`created` 仍是 `2026-11-13 17:45Z`（北京 `11/14 01:45`）—— **不是新模型，是免费变体被收回**；权重仓 `inclusionAI/Ling-3.2-air`（`MIT`、`2,403` 下载 / `309` 赞）。 "
        "**这是 079–081 三期「免费池不动」之后第一次下降的唯一原因。**",
        r42, name="🟠 **`inclusionAI` `Ling 3.2 Flash` 退出 `OpenRouter` 免费区（**`:free` 摘除 · 改按 `$0.30 / $0.90` 计费 · 权重仓 `Ling-3.2-air` `MIT`**）**")

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
assert "`475/13/10`" in back and "`477/14/11`" not in back
assert "`6` 个 provider" in back and "`7` 个 provider" not in back
assert "本期改写 `%d` 条" % n_edit in back
for tag, phrase in (("Hy4 flash 限免", "`1` 天"), ("M11W4", "`1` 天"),
                    ("Antigravity 三模型", "`4` 个**"), ("Token 羊毛", "`67` 张")):
    assert phrase in back, (tag, phrase)
print("OK 改写 =", n_edit, "｜沿用 =", n_carry)
