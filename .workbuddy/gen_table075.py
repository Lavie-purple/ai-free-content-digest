# -*- coding: utf-8 -*-
"""075 期：在 074 期现行 4.1/4.2 表体上做「天数带符号重算 + 行级改写 + 补入 2 行」。

纪律（055–074 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 补入行必须带「075 期」标记；⑥ 状态列整体替换；
  ⑦ 单元格不许出现 `|`；⑧ 天数一律由基准日实算、断言带符号；
  ⑨ 状态列不写「未开始 / 已结束」；状态列里非本期期号引用 ≤ 1 处（lint R3）；
  ⑩ 本期新增：Antigravity 行的截止日从 `11/18` 改到 `11/30`（官方改期，不是未执行）。
"""
import io
import re
import sys
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第075期-2026-11-21.md"
PTR = " [附录 075](details.html) |"
TODAY = date(2026, 11, 21)
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
assert len(r41) == 67, ("074 期 4.1 行数", len(r41))
assert len(r42) == 50, ("074 期 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "今日（`11/21`）为截止日", st)
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


# ---- 腾讯老混元：截止列不可解析，天数与期数手工推进（09-30 起算 = 已过 52 天）
hits = [k for k, r in enumerate(r41) if "腾讯老混元" in name_of(r)]
assert len(hits) == 1
row = r41[hits[0]]
assert "已过 `51` 天" in row and "第 `47` 期" in row and "第 `38` 天" in row, row[:200]
row = row.replace("已过 `51` 天", "已过 `52` 天").replace("第 `47` 期", "第 `48` 期").replace("第 `38` 天", "第 `39` 天")
row = row.replace("六项关键词各 `0` 命中（第 `6` 期）", "六项关键词各 `0` 命中（第 `7` 期）")
row = row.replace(" [附录 074](details.html) |", PTR)
r41[hits[0]] = row
EDITED.append("腾讯老混元(手算)")

# ---- 4.1：Hy4 flash WorkBuddy 限免
edit("Hy4 flash 限免", "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
     "🟠 **距截止 `8` 天。 限免只限 `WorkBuddy` 内的 `Hy4 flash`**；`TokenHub` 是**限时 `5` 折**。 "
     "**权重已开放三仓，本期 `downloads` 三仓全部未刷新**（`3,949` / `1,219` / `699`）、`likes` 仍在动 —— **到期后能用的是权重，不是本行额度**。",
     r41, name="🟠 **腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费（**`220.25B` 实测总参（含 `64B` Engram）/ 激活 `11.3B` + `0.43B` / `1M` 上下文 · 官方口径「`11/30` 前」**）**")

# ---- 4.1：Hy4 AMA（已于 11/21 02:00 收口）
edit("Hy4 AMA", "腾讯混元 `Hy4` / `Hy4 flash` 官方 `Reddit` `AMA`",
     "⚪ **已收口（活动已于 `11/21 02:00` 收口）。 官方 `X` 公布的是 `11/20` `8–10 AM PT` ＝ 北京 `11/21` 00:00–02:00**，在 `r/LocalLLaMA` 由研发团队答问。 "
     "**本报未抄录问答内容**：`reddit.com` 两个入口本期均 `000`，无一手可核 —— **只记「按计划开过」，不转述任何「团队说了什么」。** ",
     r41, deadline="**北京 `11/21` 00:00–02:00（`11/20` `8–10 AM PT` 换算 · 已收口）**")

# ---- 4.1：ERNIE 5.5
edit("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `4` 天）。 官方发布页 `11月25日前开源` 逐字仍在**（本期 `54,010` 字节，与上期逐字节相同，第 `4` 期）。 "
     "**权重仍未放**：`?author=baidu` 仍 `39` 个仓库（连续第 `18` 天 `0` 变化）。 "
     "**本季最后一个「官方给了日期」的开源承诺，剩 `4` 天。**",
     r41)

# ---- 4.1：MiniMax 4K —— 旧版收口（新版在 4.2）
edit("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
     "⚪ **旧版已过期（`11/18 00:00` 到期）；同一促销的现行版本是第二版（无截止日、`1660` 万像素门槛），见 `4.2`。 本期本行只记「旧版过期」这一件事** —— "
     "第二版本期仍原样在架（页 `310,127 → 310,162`，`+35`），**不代表该折扣已停**（避坑 317）。 "
     "旧文案的截止时刻逐字是「即日起至 2026 年 11 月 18 日 00:00」，**现行文案里这句话整句不存在**（避坑 318）。", r41,
     deadline="**`11/18 00:00`（北京 · 旧版逐字「即日起至 2026 年 11 月 18 日 00:00」· 已过 `3` 天）**")

# ---- 4.1：Runware 4K 50%
edit("Runware 4K 50%", "`Runware` 分发层 `MiniMax H3-Image`",
     "🟠 **已过 `4` 天（`11/17` 到期）。 三个读数连续第 `4` 期不变：`h3-image` 命中 `18`、卡片徽标 `0`、价目一个数没变**"
     "（`0.2261` / `0.4522` 整页 `0` 命中）—— **「账本 vs 货架」第 `16` 次实证**。 "
     "**本期新增读数：数组日期整排换过** —— `11-17` 从 `5` 处降到 `1` 处、`11-19` 从 `5` 处降到 `1` 处，**总条数恒为 `22`**；**「共几条」不是台账字段，`endsAt` 在滚动**。",
     r41, deadline="**`11/17`（官方促销数组 `endsAt: \"2026-11-17\"` 逐字 · 已过 `4` 天）**")

# ---- 4.1：Antigravity 三模型 —— 官方把日期改到 11/30
edit("Antigravity 三模型", "`Google Antigravity` 免费档三个第三方模型",
     "🟠 **距截止 `9` 天（官方改期，不是「未执行」）。 073/074 两期写的「到期第 N 天仍未执行」本期更正：页面把脚注 `4` 从 `November 18` 改成 `November 30`**"
     "（全页 `November 18` **`0` 命中**、`Will be removed` `8` 处）。 付费档另列 `Gemini 4 Neon` / `4 Carbon` / `4 Argon` / `4 Hydrogen` / `Orchestrator` 与 `Claude Sonnet 5.5` / `Opus 5.5` —— **免费档一个都没有**。",
     r41, deadline="**`11/30`（官方脚注逐字 `Will be removed on November 30, 2026.` · 距截止 `9` 天）**",
     name="🟠 **`Google Antigravity` 免费档三个第三方模型 `11/30` 移除（`Claude Sonnet 4.6` / `Claude Opus 4.6` / `GPT-OSS-120B`）**")

# ---- 4.1：AutoClaw M11W3（本周）
edit("AutoClaw M11W3", "智谱 `AutoClaw` 国内站 `M11W3`",
     "🟠 **距截止 `1` 天。 官方博客 `M11W3` 逐字：`11 月 16 日至 11 月 22 日` 登录领 `100M` Tokens（`10,000` 积分）**，奖励 `11/22 23:59` 失效。 "
     "**下一期 `M11W4` 已挂出（`11/23`–`11/29`，仍 `100M`）** —— 两期首尾相接、**中间只隔 `1` 分钟**，本周领的额度本周日即作废。 "
     "`M11W5` 本期 `404`（未发布）。 额度锁在客户端内，导不出 `API`。",
     r41, deadline="**`11/22 23:59`（北京时间 · 官方逐字「活动时间 11 月 16 日（周一）00:00—11 月 22 日（周日）23:59」；奖励同日 `23:59` 失效 · 距截止 `1` 天）**")

# ---- 4.1：AutoClaw M11W4
edit("AutoClaw M11W4", "智谱 `AutoClaw` 国内站 `M11W4`",
     "🟠 **距截止 `8` 天。 `11/23`–`11/29` 登录领 `100M`（`10,000` 积分），`11/29 23:59` 失效。 与 `M11W3`（到 `11/22 23:59`）**只隔 `1` 分钟**，本周额度本周日作废。 "
     "`100M` 连续第 `2` 周（前两周 `50M`）。 锁客户端、导不出 `API`。",
     r41, deadline="**`11/29 23:59`（北京时间 · 官方逐字「活动时间 11 月 23 日（周一）00:00—11 月 29 日（周日）23:59」· 距截止 `8` 天）**")

# ---- 4.2：OpenRouter 免费档
edit("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **四个口径本期全部持平：全量 `477`、`:free` `12`、零价 `15`、`?max_price=0` `14`（第 `2` 天同值）。 窗口内只新增 `1` 条**：`radixark/daisyrose-27b`（北京 `11/21 08:49`，付费 `$0.15` / `$1.875`），**无 `:free`**。 "
     "`gpt-6.2` 仍 `8` 条、**仍无 `:free`**（第 `4` 天）。 **`Ling 3.2 Flash` 口径更正：`:free` 变体 `1` 条路由（`1,466` 字节）、基名 `0` 条（`462` 字节）** —— 只查基名会误判成「路由断了」。",
     r42, name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `477/15/12`**）**")

edit("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `13` 期：页头「今天还能领」`¥1737 → ¥1804`（`+67`，前四期一路小跌后首次回升）、"
     "卡册 `62` 张持平（第 `2` 期同值）**。 **该合计是当日动态折算值、卡册是账户态**，只记读数、不推趋势。 页 `486,754` 字节。",
     r42)

edit("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
     "🟢 **官方定价页逐字 `$0/month`（`181,393` 字节，`md5 7738ba05`）。 免费档仍是四个模型**：`Gemini 3.8 Flash` + 三个第三方（`Sonnet 4.6` / `Opus 4.6` / `GPT-OSS-120B`）。 "
     "**本期唯一实质变化：三个第三方的移除日从 `11/18` 改到 `11/30`** —— **是改期，不是未执行**。 `Baseline agent quota refreshed weekly` **仍无数字（第 `6` 期）**。",
     r42)

edit("ERNIE-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓库。 本期两仓 `downloads` 均未刷新**（`5,075` / `1,920`，与上期同值）；`likes` `360`（`0`）/ `394`（`0`）。 "
     "两仓 `lastModified` 仍停 `11/05` —— **仓库没变，`downloads` 本批次也没刷新**（避坑 324）。",
     r42)

edit("Inkling 2 Small", "`thinkingmachines/Inkling-2-Small` 开放权重",
     "🟢 **`Apache-2.0` · `gated: false`。 `downloads` `40,574` 本期未刷新（与上期同值）/ `likes 598 → 654`（`+56`）**；`lastModified` **`11/20 14:09Z`（本期窗口内）**。 "
     "**同日它的「小兄弟」`Inkling 2 Mini` 发布**（见本表下方新增行）—— **两个仓、两个规格，别混**。",
     r42)

edit("OpenCode 免费清单", "`OpenCode` 免费模型清单",
     "🟡 **`Free models` 段仍 `12` 条**（段落逐条；`-free` 正则全页 `14` 处，**含导航，口径不同**）。 **页 `102,667` 字节 / `md5 6105ecab` 与上期字节 + `md5` 双同（第 `3` 期）**。 "
     "`GLM-5.3-Flash Free` **仍不在段内**、`Deprecated models` 表那行**仍在** —— 两张表不同步第 `3` 期。 "
     "两条限制单独标：`LongCat 2.5 Free` **每日 `100` 次**；`Beam Free` 明确排除 `China (including Hong Kong and Macau)`。",
     r42, name="🟡 **`OpenCode` 免费模型清单（`Free models` 段 `12` 条 · 与上期字节 + `md5` 双同第 `3` 期）**")

edit("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **已公开（069 期补登）。 `downloads` `2,830` 本期未刷新（与上期同值）/ `likes 360 → 361`；`lastModified` 仍 `11/10 07:28Z`**。 "
     "四个时间点仍分开写：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`、媒体稿 `11/15 10:06Z`、**一手页无「发布日期」字段**。",
     r42)

edit("Hy4 开放权重", "腾讯混元 `Hy4 flash` 开放权重",
     "🟢 **（072 期补入）三仓均 `gated: false`。 第 `4` 天：`downloads` 三仓全部未刷新**（`3,949` / `1,219` / `699`，与上期同值）；`likes 483 → 550` / `22 → 23` / `24`（`0`）。 "
     "**第三方转档仍能点名 `10` 个以上；`?search=Hy4` 本期返回 `100` 条（已触 `limit` 上限，`≥100`，不再当精确数）**。 "
     "**许可是 `Apache 2.0` 派生 + `§10`**：对外 `MaaS` 且过 `$50M` 营收或 `1` 亿 `MAU` 须另签；`§10.3` 内部使用豁免。",
     r42, name="🟢 **腾讯混元 `Hy4 flash` 开放权重（**`220.25B` 实测 · 激活 `11.3B` + `0.43B` · `1M` · `Tencent Hy License 1.0`**）**")

edit("GPT-6.2", "OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
     "🟡 **（072 期补入）发布页可用名单逐字 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 "
     "本期三读数：`OpenRouter` 仍 `8` 条、**仍无 `:free`**（第 `4` 天）；`chatgpt.com/pricing` 仍读不到正文（第 `4` 期，`301` 后 `0` 字节）→ **免费档是否含 `GPT-6.2` 仍无一手**；"
     "`openai.com/index/` `200` / `404,884` 字节，窗口内**无新免费档条目**（唯一新条目是 `MedChemBench` 研究基准，`11/20`）。 **不写「免费用户可用/不可用」。**",
     r42, name="🟡 **OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布（**可用名单 `Plus` / `Pro` / `Enterprise` / `Edu` · **`Free` 不在名单里**）**")

edit("Ling 3.2", "Ling 3.2 Flash` 进入 `OpenRouter`",
     "🟡 **生效中（068 期补入）。 本期口径更正：`/endpoints` 有两套 `id` —— `:free` 变体 `1` 条路由（`1,466` 字节）、基名 `0` 条（`462` 字节）**。 "
     "**上期写的「接通 `1` 条」读的是 `:free`，主语该是 SKU 不是模型**（纠错②）。 "
     "**层数不变：目录有、`:free` 路由有、权重仓仍 `404` —— 三层只开了两层**。",
     r42, name="🟡 **`inclusionAI` `Ling 3.2 Flash` 进入 `OpenRouter` 免费区（`:free` 零价 · `1,048,576` 上下文 · **`:free` 路由 `1` 条 / 基名 `0` 条**）**")


# ------------------------------------------------------------ ③ 补入新行
NEW42_INKLING = ("| 🟢 **`thinkingmachines/Inkling-2-Mini` 开放权重（**`26.4B` 总参 / `3.4B` 激活 / 每 token 权重激活 `5.4B`（循环层跑 `3` 次）· `~20GB` · **`Apache-2.0`**）** "
                 "| **无截止日（权重永久开放；`Apache-2.0` 无附加商用条款）** "
                 "| 🟢 **（075 期补入）官方逐字 `small enough to run on your laptop`；权重多为原生 `NVFP4`、末 `4` 层 `MXFP8`，官方实测机 `MacBook Pro (M5 Pro, 48GB)` 飞行模式跑通**。 "
                 "`DeepSWE v1.1` `48.2%` / `Vals Index v2.2` `46.5%`（**厂商自评：`<100B` 开放权重第一，未经第三方复现**）。 "
                 "`HF` 建仓 `11/17 00:26Z`、权重最后变更 `11/20 22:55Z`、公告北京 `11/21 04:28` —— **三个时间点不合并**（避坑 311）。 "
                 "发布 `6` 小时 `?search=Inkling-2-Mini` 已 `31` 仓（`GGUF` / `MLX` / `NVFP4` / 去审查）。 **`~20GB` 是权重内存，不是「`24GB` 显卡够用」**（避坑 321）。 |")

NEW42_HY4 = ("| 🟢 **腾讯混元 `Hy4`（旗舰 · 非 `flash`）开放权重（**`770B` 总参 / 激活 `49B` + 视觉 `1.23B` · `1M` · `78` 层 · `256` 路由专家取 `top-8` ＋ `1` 共享 · `Tencent Hy License`**）** "
             "| **无截止日（权重永久开放；`license: other` → `Tencent Hy License`，须读 `LICENSE` 原文）** "
             "| 🟢 **（075 期补登）三仓权重在 `11/20 03:05:49Z`–`03:05:54Z`（北京 `11:05`）同批落盘** —— 该时刻在上一期窗口内、距其截止还有 `9` 小时，**上一期未登，本期补**（纠错①）。 "
             "`downloads`：`Hy4` `89` / `Hy4-FP8` `71` / `Hy4-base` `68`（合计 `228`）；`likes` `127` / `11` / `8`。 "
             "**`770B` 全 `BF16` 约 `1.5TB`、`FP8` 约 `770GB` —— 「开放权重」不等于「可本地部署」**；想跑走官方挂的 `AngelSlim/Hy4-GGUF`。 "
             "内置 `DFly2` `3.3B` 投机解码、`Gated DSA` ＋ `IndexCache`、`iHC` 四条残差流。 |")

idx = [k for k, r in enumerate(r42) if "`thinkingmachines/Inkling-2-Small`" in name_of(r)]
assert len(idx) == 1, idx
r42.insert(idx[0], NEW42_INKLING)

idx = [k for k, r in enumerate(r42) if "腾讯混元 `Hy4 flash` 开放权重" in name_of(r)]
assert len(idx) == 1, idx
r42.insert(idx[0] + 1, NEW42_HY4)


# ------------------------------------------------------------ ④ 指针重贴当期期号
def repoint(bucket):
    n = 0
    for k, r in enumerate(bucket):
        if "附录 074" in r:
            bucket[k] = r.replace("附录 074", "附录 075")
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
assert len(d42) == 52, len(d42)
assert "075 期补入" in disk and "075 期补登" in disk
assert "已过 `52` 天" in disk
assert "第 `48` 期" in disk
assert "已过 `4` 天（`11/17` 到期）" in disk
assert "Will be removed on November 30, 2026." in disk
assert "`477/15/12`" in disk
assert "附录 074" not in disk

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

ISSUE_RE = re.compile(r"(?!075)(0\d{2})\s*期")
over = [(name_of(r)[:24], len(ISSUE_RE.findall(cells_of(r)[2]))) for r in d41 + d42
        if len(ISSUE_RE.findall(cells_of(r)[2])) >= 2]
assert not over, over
print("R3 预检：0 行超 1 处")
