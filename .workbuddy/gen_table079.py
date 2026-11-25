# -*- coding: utf-8 -*-
"""079 期：在 078 期现行 4.1/4.2 表体上做「天数带符号重算 + 行级改写 + 归档 2 行」。

纪律（055–078 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 状态列整体替换；⑥ 单元格不许出现 `|`；
  ⑦ 天数一律由基准日实算、断言带符号；⑧ 状态列不写「未开始 / 已结束」；
  ⑨ 本期归档 2 行（Runware 4K 50% / H3 Max，均 ⚪ 且过期 >7 天）→ 4.1 67 → 65；
  ⑩ 4.2 的 OpenRouter 行名带计数，改名必须在重建 CSV 之前。
"""
import io
import re
import sys
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第079期-2026-11-25.md"
ARCH = WS + ".workbuddy/data/deadline_archive.md"
PTR = " [附录 079](details.html) |"
TODAY = date(2026, 11, 25)
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
assert len(r41) == 67, ("078 期 4.1 行数", len(r41))
assert len(r42) == 54, ("078 期 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "今日（`11/25`）为截止日", st)
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
    EDITED.append(tag)


def sub_row(tag, prefix, pairs, bucket=None):
    b = bucket if bucket is not None else r41
    k = find(b, prefix, tag)
    row = b[k]
    for old, new in pairs:
        assert old in row, ("逐字短语未命中", tag, old[:60])
        row = row.replace(old, new)
    assert "附录 078" not in row
    b[k] = row
    EDITED.append(tag)


# ---- 4.1：腾讯老混元（截止列不可解析，手工推进：09-30 → 已过 56 天）
k = find(r41, "腾讯老混元", "腾讯老混元")
row = r41[k]
assert "已过 `55` 天" in row and "第 `51` 期" in row and "第 `42` 天" in row, row[:200]
row = (row.replace("已过 `55` 天", "已过 `56` 天")
          .replace("第 `51` 期", "第 `52` 期")
          .replace("第 `42` 天", "第 `43` 天"))
row = row.replace("六项关键词各 `0` 命中（第 `10` 期）", "六项关键词各 `0` 命中（第 `11` 期）")
row = row.replace("`6,584` 字节 / `md5` 与上期双同（第 `10` 期）", "`6,584` 字节 / `md5` 与上期双同（第 `11` 期）")
r41[k] = row
EDITED.append("腾讯老混元(手算)")

# ---- 4.1：Hy4 flash WorkBuddy 限免（downloads 解冻）
set_row("Hy4 flash 限免", "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
        "🟠 **距截止 `4` 天。 限免只限 `WorkBuddy` 内的 `Hy4 flash`**；`TokenHub` 是**限时 `5` 折**。 "
        "三仓 `downloads` 本期**解冻**（`9,167` / `2,239` / `1,168`，合计 `+1,918`）—— **到期后能用的是权重，不是本行额度**。",
        r41, deadline="**`11/29`（聚合层逐字「到 `11月29日`」；媒体逐字「`11月30日前`」——**两个日期并排写、不合并**）**")

# ---- 4.1：Hy4 AMA（已收口）
set_row("Hy4 AMA", "腾讯混元 `Hy4` / `Hy4 flash` 官方 `Reddit` `AMA`",
        "⚪ **已收口（`11/21 02:00` 收口，已过 `4` 天）。 官方 `X` 公布 `11/20` `8–10 AM PT` ＝ 北京 `11/21 00:00–02:00`**，在 `r/LocalLLaMA` 由研发团队答问。 "
        "**`reddit.com` 三个入口连续四期 `000`，本报未抄录问答内容** —— 只记「按计划开过」。",
        r41, deadline="**北京 `11/21` 00:00–02:00（`11/20` `8–10 AM PT` 换算 · 已过 `4` 天）**")

# ---- 4.1：ERNIE 5.5 —— 承诺兑现 + 首日读数
set_row("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
        "⚪ **已兑现（`11/23 17:00` 上线三仓，已过 `2` 天；承诺日 `11/25` 本期到点）。 首日读数：三仓合计 `117` 次下载 / `314` `likes`（`75` / `15` / `27`）；`?author=baidu` 仍 `42` 仓、`0` 新增**。 "
        "077 期「权重仍未放」属漏抓（比其截稿早 `2` 小时）—— 权重行见 `4.2`。", r41)

# ---- 4.1：MiniMax 4K 旧版（新版在 4.2）
set_row("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
        "⚪ **旧版已过期（`11/18 00:00` 到期）；现行版本是第二版（无截止日、`1660` 万像素门槛），见 `4.2`。 本行只记「旧版过期」。** "
        "第二版第 `6` 天**字节 `310,179`**（`md5` 变、字节 `−4`），**不代表该折扣已停**。 旧文案的截止句整句不存在，**截止日不跨版本**。",
        r41, deadline="**`11/18 00:00`（北京 · 旧版逐字「即日起至 2026 年 11 月 18 日 00:00」· 已过 `7` 天）**")

# ---- 4.1：Runway Kling 4.0（本期不可比）
set_row("Runway Kling", "Runway 平台 `Kling 4.0`",
        "🟠 **距截止 `5` 天。 （068 期补入）只在 `Standard` / `Pro` 两个付费档下列出，免费档（`125` 一次性 credits）下没有这一条**；"
        "与 `Runware` 那条 `Kling 4.0` 促销是两个分发商的两场活动，不可合并。 **折扣不是免费。** "
        "**本期页面 `25% off` `0` 命中，但可见文本 `375` → `24` 行、价格表不在 `HTML` 里 —— 形态不同、不可比，只记读数**（二章第 `2` 条）。",
        r41, deadline="**`11/30`（官方逐字 `until November 30`，未写时区 · 距截止 `5` 天）**")

# ---- 4.1：Runway 企业版
set_row("Runway 企业版", "Runway 企业版",
        "🟠 **生效中（距截止 `36` 天）。 （068 期补入）三个要件缺两个：`up to`（上限不是保底）、条件（`terms` 页本期未取，077 期 `404`）**。 "
        "页 `658,189` 字节（`−35.5%`），**可见文本 `375` → `24` 行（价格表整块不在 `HTML`）** —— **本期唯一能说「确实没变」的是企业版横幅仍 `2` 处**。",
        r41, deadline="**`12/31`（官方逐字 `Sign by 12/31`；条款页 `runway.com/terms` 本轮未取 · 距截止 `36` 天）**")

# ---- 4.1：AutoClaw M11W3（已收口）
set_row("AutoClaw M11W3", "智谱 `AutoClaw` 国内站 `M11W3`",
        "⚪ **已收口（`11/22 23:59` 收口，已过 `3` 天）。 官方逐字 `11 月 16 日至 11 月 22 日` 登录领 `100M`（`10,000` 积分），奖励同日 `23:59` 失效**。 "
        "`M11W4` 已在 `11/23 00:00` 接班（仍 `100M`）；`M11W5` 连续第 `4` 期 `404`。 **锁客户端、导不出 `API`。**",
        r41, deadline="**`11/22 23:59`（北京时间 · 官方逐字「活动时间 11 月 16 日（周一）00:00—11 月 22 日（周日）23:59」· 已过 `3` 天）**")

# ---- 4.1：AutoClaw M11W4
set_row("AutoClaw M11W4", "智谱 `AutoClaw` 国内站 `M11W4`",
        "🟠 **距截止 `4` 天。 `11/23`–`11/29` 登录领 `100M`（`10,000` 积分），`11/29 23:59` 失效**。 页 `47,974` **连续两期逐字节相同**。 "
        "`100M` 连续第 `3` 周（前两周 `50M`）。 锁客户端、导不出 `API`；**`M11W5` 第 `4` 期仍 `404`，周档到点才挂、别提前等**。",
        r41, deadline="**`11/29 23:59`（北京时间 · 官方逐字「活动时间 11 月 23 日（周一）00:00—11 月 29 日（周日）23:59」· 距截止 `4` 天）**")

# ---- 4.1：Antigravity 三模型（本期核实到）
set_row("Antigravity 三模型", "`Google Antigravity` 免费档三个第三方模型",
        "🟠 **距截止 `5` 天。 本期核实到：`pricing` 页 `200` / `188,088` 字节，脚注逐字 `Will be removed on November 30, 2026.` 共 `13` 处（`12` 个 `title` + `1` 条可见脚注）。 "
        "免费档 `$0/month` 列 `5` 个模型，其中 `3` 个挂该脚注** —— **`11/30` 后第一方模型剩 `2`–`3` 个**（`Gemini 3.8 Flash` 两种写法并存、归属存疑）。 "
        "该页**间歇可达**（`4` 次请求 `2` 次 `200`、`2` 次 `000`）。",
        r41, deadline="**`11/30`（官方脚注逐字 `Will be removed on November 30, 2026.` · 距截止 `5` 天）**",
        name="🟠 **`Google Antigravity` 免费档三个第三方模型 `11/30` 移除（`Claude Sonnet 4.6` / `Claude Opus 4.6` / `GPT-OSS-120B`）**")

# ---- 4.2：OpenRouter 免费档（改名 474/15/12 → 472/14/11）
set_row("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
        "🟢 **四项同降：全量 `474 → 472`（`−2`）、`:free` `12 → 11`、零价 `15 → 14`、`max_price=0` `14 → 13`**。 "
        "出 `5` 进 `3`；**唯一退出的免费条目是 `dots-3-note-preview:free`** —— 目录 `0` 命中、`%3A` 端点 `200` 但 **`endpoints: []`**。 "
        "新进三条全付费（`upstage` 两条 `11/24 23:18Z`、小米 `mimo-v2.6-flash-mopd`）。 `gpt-6.2` 仍 `8` 条、无 `:free`（第 `8` 天）。",
        r42, name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `472/14/11`**）**")

# ---- 4.2：OpenCode（静态期结束）
set_row("OpenCode 免费清单", "`OpenCode` 免费模型清单",
        "🟡 **`+335` 字节（`108,492 → 108,827`）、`md5` 变 —— 078 期「整页完全静止」只维持一期。 免费段 `11` 条（去重 `10`）一个未变**；"
        "新增 `Kimi K3.1 Pro` **付费**行（`$2.00` / `$10.00` / 缓存读 `$0.20`）；`embeddings` 说明改成「**免费档不含、`Go` 含一部分**」。",
        r42)

# ---- 4.2：Token 羊毛（第 17 期）
set_row("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
        "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `17` 期：`¥845` 持平、卡册 `65` 张持平**"
        "（构成换了 `3` 处：某卡 `400 → 500` 积分、进 `千问办公` / `Dots`、出 `ADP`）。 "
        "**本期统计规则文字未变 → 两数可比**；**合计口径对「谁在羊毛里」不敏感**，页面不提供逐卡拆分，**不点名涨幅来源**。",
        r42)

# ---- 4.2：Antigravity 个人免费档
set_row("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
        "🟢 **逐字 `$0/month`（首页页 `219,391` 字节、`pricing` 页本期 `200` / `188,088`）。 免费档列 `5` 个模型，其中 `3` 个挂 `11/30` 移除脚注（脚注 `13` 处）**。 "
        "`Baseline agent quota refreshed weekly` **仍无数字（第 `10` 期）**。 首页 `November 30` 仍 `0` 处 —— **免费档模型数只认定价页**（避坑 340）。",
        r42)

# ---- 4.2：ERNIE-5.5-Flash-Base（downloads 解冻）
set_row("ERNIE-5.5-Flash-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
        "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓。 本期 `downloads` 两仓解冻**（`5,532 → 5,715`、`2,120 → 2,225`）；`likes` `+3` / `0`。 "
        "**十三个仓同窗齐涨 → 批次补齐窗，不是单仓热度**（避坑 334）。",
        r42)

# ---- 4.2：Inkling 2 Mini
set_row("Inkling 2 Mini", "`thinkingmachines/Inkling-2-Mini` 开放权重",
        "🟢 **（075 期补入）`downloads` `41,888 → 69,042`（`+27,154`）、`likes` `5,526 → 5,817`（`+291`）**。 `HF` 趋势榜仍第 `1`；"
        "`unsloth` `GGUF` 已 `1,913,407` 次下载（**比原仓高 `27.7` 倍**）。 `~20GB` 为 `NVFP4` 权重、实测机 `48GB`。 **API 见本表价格行**。",
        r42)

# ---- 4.2：inkling-2-mini 的 API 入口（价点 4 → 5）
set_row("inkling API", "`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`",
        "🟡 **（076 期新增观测位）价点 `4 → 5`：`DeepInfra` 进场 `$0.075 / $0.30`（与 `PrimeIntellect` 中档同价）**；"
        "顶档 `PrimeIntellect` `$0.15 / $0.60` 本期稳住；`Io Net` `$0.12 / $0.50`（上下文仅 `262,144`）。 "
        "最贵/最便宜仍 `4.0` 倍；无 `:free`（第 `8` 天）。",
        r42)

# ---- 4.2：Inkling 2 Small
set_row("Inkling 2 Small", "`thinkingmachines/Inkling-2-Small` 开放权重",
        "🟢 **`Apache-2.0`。 `downloads` `55,885 → 67,132`（`+11,247`）、`likes` `1,447 → 1,475`（`+28`）**；`lastModified` `11/20 14:09Z`。 "
        "**`OpenCode` 把它的 `Free` 变体按弃用表下架（`11/19`）** —— 权重还在，免费入口已不在。",
        r42)

# ---- 4.2：Hy4 flash 权重
set_row("Hy4 flash 权重", "腾讯混元 `Hy4 flash` 开放权重",
        "🟢 **（072 期补入）三仓 `gated: false`。 本期 `downloads` 三仓解冻**（`7,696 → 9,167`、`1,949 → 2,239`、`1,011 → 1,168`）；`likes` `+29` / `+1` / `0`。 "
        "许可 `Apache 2.0` 派生 + `§10`：对外 `MaaS` 过 `$50M` 或 `1` 亿 `MAU` 须另签。",
        r42)

# ---- 4.2：Hy4（770B）
set_row("Hy4 770B", "腾讯混元 `Hy4`（旗舰 · 非 `flash`）开放权重",
        "🟢 **（075 期补登）三仓 `downloads` `2,384` / `970` / `873`（合计 `4,227`，本期 `+899`）、`likes` `+19` / `+1` / `0`**。 "
        "**`BF16` 约 `1.5TB`、`FP8` 约 `770GB` —— 开放≠可本地跑**；量化走 `AngelSlim/Hy4-GGUF`。",
        r42)

# ---- 4.2：LongCat-2.5
set_row("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT` 公开权重",
        "🟢 **已公开（069 期补登）。 `downloads` `3,303 → 3,538`（`+235`）、`likes` `283 → 284`（`+1`）**。 "
        "**`OpenCode` 的免费入口已撤**（`longcat-2.5-free` 不在 `Free models` 段），**权重不受影响**。 四个时间点分开写：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`、媒体稿 `11/15`、一手页无发布日期。",
        r42)

# ---- 4.2：GPT-6.2（第 8 天）
set_row("GPT-6.2", "OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
        "🟡 **（072 期补入）名单 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 `OpenRouter` 仍 `8` 条、**无 `:free`（第 `8` 天）**；"
        "`chatgpt.com/pricing` 第 `8` 期读不到正文**。 **不写「免费可用/不可用」。**",
        r42)

# ---- 4.2：Ling 3.2
set_row("Ling 3.2", "`inclusionAI` `Ling 3.2 Flash` 进入 `OpenRouter` 免费区",
        "🟡 **生效中（068 期补入）。 `:free` 路由本期未单独重取（078 期为 `1` 条 / `1,466` 字节；基名 `0` 条）**。 "
        "**三层只开两层：目录有、`:free` 路由有、权重仓仍 `404`。**",
        r42)

# ---- 4.2：MiniMax 4K 第二版（第 6 天）
set_row("MiniMax 4K 第二版", "`MiniMax H3-Image` `4K` 五折 · 第二版",
        "🟠 **第二版第 `6` 天仍在架（页 `310,179`，字节 `−4`、`md5` 变 —— 构建副本抖动）。 六档折后价全在**（`0.2261`–`0.5073`），`2026-11-18` / `截止` / `结束` 各 `0` 命中。 "
        "门槛：宽 × 高 ≥ `1660` 万像素。 **文案里没有任何日期 —— 不替它排日。**",
        r42)

# ---- 4.2：ERNIE-5.5-Flash-Preview 开放权重（首日读数）
set_row("ERNIE Preview 权重", "百度 `ERNIE-5.5-Flash-Preview` 开放权重",
        "🟢 **已开放权重（四层全通 · 078 期补登）。 首日读数：三仓 `downloads` `75` / `15` / `27`（合计 `117`）、`likes` `262` / `29` / `23`（合计 `314`）**；"
        "`?author=baidu` 仍 `42` 仓、`0` 新增。 `Apache-2.0`、`128` 分片、`142` 文件。 "
        "**`likes : downloads = 2.7 : 1`** —— 点收藏的多、下得动的少。 `BF16` 约 `560GB` / `FP8` 约 `280GB`，**能下载 ≠ 能本地跑**。",
        r42)

# ------------------------------------------------------------ ③ 归档 2 行（⚪ 且过期 >7 天）
ARCH_ROWS = []
for pref, tag in (("`Runware` 分发层 `MiniMax H3-Image`", "Runware 4K 50%"),
                  ("`Runware` 分发层 `MiniMax H3 Max`", "Runware H3 Max")):
    k = find(r41, pref, tag)
    c = cells_of(r41[k])
    assert c[2].startswith("⚪"), ("不是收口态，不能归档", tag, c[2][:20])
    d = days_of(c[1])
    assert d is not None and d < -7, ("未超过 7 天宽限", tag, d)
    ARCH_ROWS.append(r41.pop(k))
    EDITED.append(tag + "(归档)")
print("归档行数 =", len(ARCH_ROWS), "｜改写标记 =", len(EDITED))
assert len(r41) == 65

# ------------------------------------------------------------ ④ 写回（原地替换两个表块）
NL = chr(10)
old_41 = NL.join(rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更"))
old_42 = NL.join(rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注"))
assert md.count(old_41) == 1 and md.count(old_42) == 1
new_md = md.replace(old_41, NL.join(r41), 1).replace(old_42, NL.join(r42), 1)

# 标题与统计句：4.1 67 → 65
assert "### 4.1 限时动作（有确切截止日 · 67 条）" in new_md
new_md = new_md.replace("### 4.1 限时动作（有确切截止日 · 67 条）",
                        "### 4.1 限时动作（有确切截止日 · 65 条）")
# 4.2 的「本期改写 / 补入 / 沿用」三个数（改写 = EDITED 里非归档的条数）
n_edit = len([e for e in EDITED if not e.endswith("(归档)")])
n_carry = 54 - n_edit
assert "本期改写 `0` 条、补入 `0` 条、其余 `54` 条沿用上期读数" in new_md
new_md = new_md.replace("本期改写 `0` 条、补入 `0` 条、其余 `54` 条沿用上期读数",
                        "本期改写 `%d` 条、补入 `0` 条、其余 `%d` 条沿用上期读数" % (n_edit, n_carry))

assert new_md != md
if DRY:
    print("DRY RUN —— 未写盘；改写 %d 行、归档 %d 行；4.1 = %d" % (n_edit, len(ARCH_ROWS), len(r41)))
    print("EDITED:", EDITED)
    sys.exit(0)

io.open(MD, "w", encoding="utf-8", newline=NL).write(new_md)

# ---- 归档文件追加
arch = io.open(ARCH, encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")
block = ["", "## 079 期（归档日 2026-11-25 · 移出 2 条）", "",
         "| 活动 | 截止 | 状态 |", "| --- | --- | --- |"] + ARCH_ROWS + [""]
io.open(ARCH, "w", encoding="utf-8", newline=NL).write(arch + "\n".join(block))

# ------------------------------------------------------------ ⑤ 落盘复核
back = io.open(MD, encoding="utf-8").read()
rb = rows_of(back, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
rb2 = rows_of(back, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("落盘复核：4.1 = %d，4.2 = %d，字节 = %d" % (len(rb), len(rb2), len(back.encode("utf-8"))))
assert len(rb) == 65 and len(rb2) == 54
assert "本期有变化 54 条" in back
assert "`472/14/11`" in back and "`474/15/12`" not in back
assert "`endpoints: []`" in back
assert back.count("附录 079") > 80, back.count("附录 079")
assert "附录 078" not in back
assert "本期改写 `%d` 条" % n_edit in back
for tag, phrase in (("Hy4 flash 限免", "`4` 天"), ("M11W4", "`4` 天"), ("Antigravity 三模型", "`13` 处")):
    assert phrase in back, (tag, phrase)
ab = io.open(ARCH, encoding="utf-8").read()
assert "## 079 期（归档日 2026-11-25 · 移出 2 条）" in ab
assert "H3 Max" in ab and "MiniMax H3-Image" in ab
print("OK 归档行数 =", len(ARCH_ROWS), "｜改写 =", n_edit, "｜沿用 =", n_carry)
