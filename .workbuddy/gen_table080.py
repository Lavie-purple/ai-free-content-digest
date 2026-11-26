# -*- coding: utf-8 -*-
"""080 期：在 079 期现行 4.1/4.2 表体上做「天数重算 + 行级改写」。

纪律（055–079 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 状态列整体替换；⑥ 单元格不许出现 `|`；
  ⑦ 天数一律由基准日实算（断言带符号）；⑧ 状态列不写「未开始 / 已结束」；
  ⑨ **本期无归档、无补入**（4.1 仍 65、4.2 仍 54），只改读数；
  ⑩ 4.2 的 OpenRouter 行名带计数（472/14/11 → 474/14/11），改名必须在重建 CSV 之前。
"""
import io
import re
import sys
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第080期-2026-11-26.md"
PTR = " [附录 080](details.html) |"
TODAY = date(2026, 11, 26)
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
assert len(r41) == 65, ("079 期 4.1 行数", len(r41))
assert len(r42) == 54, ("079 期 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "今日（`11/26`）为截止日", st)
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


def sub_row(tag, prefix, pairs, bucket=None):
    b = bucket if bucket is not None else r41
    k = find(b, prefix, tag)
    row = b[k]
    for old, new in pairs:
        assert old in row, ("逐字短语未命中", tag, old[:60])
        row = row.replace(old, new)
    assert "附录 079" not in row
    b[k] = row
    EDITED.append((tag, "4.2" if b is r42 else "4.1"))


# ---- 4.1：腾讯老混元（截止列不可解析，手算 09-30 → 已过 57 天）
k = find(r41, "腾讯老混元", "腾讯老混元")
row = r41[k]
assert "已过 `56` 天" in row and "第 `52` 期" in row and "第 `43` 天" in row, row[:200]
row = (row.replace("已过 `56` 天", "已过 `57` 天")
          .replace("第 `52` 期", "第 `53` 期")
          .replace("第 `43` 天", "第 `44` 天")
          .replace("（第 `11` 期）", "（第 `12` 期）"))
r41[k] = row
EDITED.append(("腾讯老混元(手算)", "4.1"))

# ---- 4.1：Hy4 flash WorkBuddy 限免（三仓解冻读数）
set_row("Hy4 flash 限免", "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
        "🟠 **距截止 `3` 天。 限免只限 `WorkBuddy` 内的 `Hy4 flash`**；`TokenHub` 是**限时 `5` 折**。 "
        "三仓 `downloads` 本期 `10,479` / `2,472` / `1,280`（合计 `+1,057`）—— **到期后能用的是权重，不是本行额度**。",
        r41, deadline="**`11/29`（聚合层逐字「到 `11月29日`」；媒体逐字「`11月30日前`」——**两个日期并排写、不合并**）**")

# ---- 4.1：ERNIE 5.5（次日读数）
set_row("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
        "⚪ **已兑现（`11/23 17:00` 上线三仓，已过 `3` 天）。 次日读数：三仓合计 `1,955` 次下载 / `360` `likes`（`1,193` / `374` / `388`）；首日（`117`）的 `16.7` 倍**。 "
        "`?author=baidu` 仍 `42` 仓、`0` 新增；社区首个 `GGUF` 已现（`11/25 13:35Z`，下载 `0`）。",
        r41)

# ---- 4.1：MiniMax 4K 旧版
set_row("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
        "⚪ **旧版已过期（`11/18 00:00` 到期）；现行版本是第二版（无截止日、`1660` 万像素门槛），见 `4.2`。 本行只记「旧版过期」。** "
        "第二版第 `8` 天**字节 `309,542`**（`md5` 变、字节 `−637`、正文 `0` 行变），**不代表该折扣已停**。 截止日不跨版本。",
        r41, deadline="**`11/18 00:00`（北京 · 旧版逐字「即日起至 2026 年 11 月 18 日 00:00」· 已过 `8` 天）**")

# ---- 4.1：Runway Kling 4.0（本期确定读数）
set_row("Runway Kling", "Runway 平台 `Kling 4.0`",
        "🟠 **距截止 `4` 天。 （068 期补入）只在 `Standard` / `Pro` 两个付费档下列出，免费档（`125` 一次性 credits）下没有这一条**；"
        "与 `Runware` 那条 `Kling 4.0` 促销是两个分发商的两场活动，不可合并。 **折扣不是免费。** "
        "**本期载荷 `1,310,856` 字节、`25% off` `21` 处、内嵌 `expiresAt: 2026-12-01` —— 促销仍在架**（二章第 `1` 条）。",
        r41, deadline="**`11/30`（官方逐字 `until November 30`，未写时区 · 距截止 `4` 天）**")

# ---- 4.1：Runway 企业版
set_row("Runway 企业版", "Runway 企业版",
        "🟠 **生效中（距截止 `35` 天）。 （068 期补入）三个要件缺两个：`up to`（上限不是保底）、条件（`terms` 页 077 期 `404`）**。 "
        "页 `1,310,856` 字节（`+99.2%`）、可见文本 `374` 行（价格表整块回来），企业版横幅仍在 —— **同一 URL 两次抓取是两份载荷**（避坑 342）。",
        r41, deadline="**`12/31`（官方逐字 `Sign by 12/31`；条款页 `runway.com/terms` 本轮未取 · 距截止 `35` 天）**")

# ---- 4.1：AutoClaw M11W3（已收口）
set_row("AutoClaw M11W3", "智谱 `AutoClaw` 国内站 `M11W3`",
        "⚪ **已收口（`11/22 23:59` 收口，已过 `4` 天）。 官方逐字 `11 月 16 日至 11 月 22 日` 登录领 `100M`（`10,000` 积分），奖励同日 `23:59` 失效**。 "
        "`M11W4` 已接班（仍 `100M`）；`M11W5` 连续第 `5` 期 `404`。 **锁客户端、导不出 `API`。**",
        r41, deadline="**`11/22 23:59`（北京时间 · 官方逐字「活动时间 11 月 16 日（周一）00:00—11 月 22 日（周日）23:59」· 已过 `4` 天）**")

# ---- 4.1：AutoClaw M11W4
set_row("AutoClaw M11W4", "智谱 `AutoClaw` 国内站 `M11W4`",
        "🟠 **距截止 `3` 天。 `11/23`–`11/29` 登录领 `100M`（`10,000` 积分），`11/29 23:59` 失效**。 页 `48,257` 字节（`+283`）、**正文 `0` 行变** —— "
        "`md5` 变的是页尾博客列表（新文 `11/25` 顶掉旧文 `11/02`，避坑 343）。 **`M11W5` 第 `5` 期仍 `404`，周档到点才挂。**",
        r41, deadline="**`11/29 23:59`（北京时间 · 官方逐字「活动时间 11 月 23 日（周一）00:00—11 月 29 日（周日）23:59」· 距截止 `3` 天）**")

# ---- 4.1：Antigravity 三模型
set_row("Antigravity 三模型", "`Google Antigravity` 免费档三个第三方模型",
        "🟠 **距截止 `4` 天。 本期 `pricing` 页 `200` / `188,088` 字节（与上期完全同字节），脚注逐字 `Will be removed on November 30, 2026.` 共 `13` 处**。 "
        "免费档 `$0/month` 列 `5` 个模型，其中 `3` 个挂该脚注** —— **`11/30` 后第一方模型剩 `2`–`3` 个**。 该页**间歇可达**（`3` 次请求 `200 / 200 / 000`）。",
        r41, deadline="**`11/30`（官方脚注逐字 `Will be removed on November 30, 2026.` · 距截止 `4` 天）**",
        name="🟠 **`Google Antigravity` 免费档三个第三方模型 `11/30` 移除（`Claude Sonnet 4.6` / `Claude Opus 4.6` / `GPT-OSS-120B`）**")

# ---- 4.2：OpenRouter 免费档（改名 472/14/11 → 474/14/11）
set_row("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
        "🟢 **全量 `472 → 474`（`+5` 进 / `3` 出）、免费三项 `11 / 14 / 13` 全未动（第 `2` 期）**。 "
        "新进 `5` 条里 `4` 条是 `:batch` 副本、唯一新模型 `tngtech/deepseek-r1t2-chimera` 是老仓新上架。 "
        "`dots` 第 `2` 期空路由、按 `T+2` 结案下线。 `gpt-6.2` 仍 `8` 条、无 `:free`（第 `9` 天）。",
        r42, name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `474/14/11`**）**")

# ---- 4.2：OpenCode（导航改版）
set_row("OpenCode 免费清单", "`OpenCode` 免费模型清单",
        "🟡 **`−4,971` 字节（`108,827 → 103,856`）、`md5` 变 —— 逐行 `diff` 全是导航改版**（四入口并成六项）＋页尾新增 `Usage export`。 "
        "**免费段 `11` 条（去重 `10`）与价格表一行未变**。 **字节变化只是哨子、不是证据**（避坑 344 之外，见第五章第 `2` 条）。",
        r42)

# ---- 4.2：Token 羊毛（第 18 期）
set_row("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
        "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `18` 期：`¥847`（`+2`）、卡册 `61` 张（`−4`）**"
        "（两处可归因：`MonkeyCode` 签到改新人礼 `≈¥0.5 → ≈¥25`、`Rime` 汇率 `≈¥333 → ≈¥334`）。 "
        "**金额与张数反向 → 不是口径稳定，是巧合**；`JSON-LD` 只暴露首页 `32` 张，其余不逐条归因。",
        r42)

# ---- 4.2：Antigravity 个人免费档
set_row("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
        "🟢 **逐字 `$0/month`（`pricing` 页本期 `200` / `188,088`，与上期同字节）。 免费档列 `5` 个模型，其中 `3` 个挂 `11/30` 移除脚注（脚注 `13` 处）**。 "
        "`Baseline agent quota refreshed weekly` **仍无数字（第 `11` 期）**。 **免费档模型数只认定价页**（避坑 340）。",
        r42)

# ---- 4.2：ERNIE-5.5-Flash-Base
set_row("ERNIE-5.5-Flash-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
        "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓。 本期 `downloads` 两仓**（`5,715 → 5,938`、`2,225 → 2,308`，合计 `+306`）；`likes` `0` / `0`。 "
        "**十五个仓同窗齐涨 → 批次补齐窗，不是单仓热度**（避坑 334）。",
        r42)

# ---- 4.2：Inkling 2 Mini
set_row("Inkling 2 Mini", "`thinkingmachines/Inkling-2-Mini` 开放权重",
        "🟢 **（075 期补入）`downloads` `69,042 → 96,527`（`+27,485`）、`likes` `5,817 → 6,040`（`+223`）**。 `HF` 趋势榜仍第 `1`；"
        "`unsloth` `GGUF` 已 `2,445,633` 次下载（**比原仓高 `25.3` 倍**）。 `~20GB` 为 `NVFP4` 权重、实测机 `48GB`。 **API 见本表价格行**。",
        r42)

# ---- 4.2：inkling 的 API 入口（价点 5 → 7）
set_row("inkling API", "`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`",
        "🟡 **（076 期新增观测位）价点 `5 → 7`：`Darkbloom` 进场 `$0.02625 / $0.105`（地板价）、`Relace` 进场 `$0.075 / $0.30`（ctx 仅 `131,072`）**；"
        "顶档 `PrimeIntellect` `$0.15 / $0.60`。 **地板价 `−30.0%`、最贵/最便宜 `4.0 → 5.7` 倍**；无 `:free`（第 `9` 天）。",
        r42, name="🟡 **`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`（**`7` 个 provider / `7` 个价点 · 按量计费 · **无 `:free` 变体**）**")

# ---- 4.2：Inkling 2 Small
set_row("Inkling 2 Small", "`thinkingmachines/Inkling-2-Small` 开放权重",
        "🟢 **`Apache-2.0`。 `downloads` `67,132 → 78,274`（`+11,142`）、`likes` `1,475 → 1,501`（`+26`）**；`lastModified` `11/20 14:09Z`。 "
        "**`OpenCode` 把它的 `Free` 变体按弃用表下架（`11/19`）** —— 权重还在，免费入口已不在。",
        r42)

# ---- 4.2：Hy4 flash 权重
set_row("Hy4 flash 权重", "腾讯混元 `Hy4 flash` 开放权重",
        "🟢 **（072 期补入）三仓 `gated: false`。 本期 `downloads`**（`9,167 → 10,479`、`2,239 → 2,472`、`1,168 → 1,280`，合计 `+1,657`）；`likes` `+29` / `0` / `0`。 "
        "许可 `Apache 2.0` 派生 + `§10`：对外 `MaaS` 过 `$50M` 或 `1` 亿 `MAU` 须另签。",
        r42)

# ---- 4.2：Hy4（770B）
set_row("Hy4 770B", "腾讯混元 `Hy4`（旗舰 · 非 `flash`）开放权重",
        "🟢 **（075 期补登）三仓 `downloads` `2,898` / `993` / `873`（合计 `4,764`，本期 `+537`）、`likes` `+30` / `0` / `0`**。 "
        "**`BF16` 约 `1.5TB`、`FP8` 约 `770GB` —— 开放≠可本地跑**；量化走 `AngelSlim/Hy4-GGUF`。",
        r42)

# ---- 4.2：LongCat-2.5
set_row("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT` 公开权重",
        "🟢 **已公开（069 期补登）。 `downloads` `3,538 → 3,722`（`+184`）、`likes` `+1`**。 **同门 `LongCat-2.0` 本期 `2,693 → 2,664`（`−29`）—— `downloads` 会倒退，是滚动窗口不是累计值**（避坑 249 第二次实证）。",
        r42)

# ---- 4.2：GPT-6.2
set_row("GPT-6.2", "OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
        "🟡 **（072 期补入）名单 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 `OpenRouter` 仍 `8` 条、**无 `:free`（第 `9` 天）**；"
        "`chatgpt.com/pricing` 第 `10` 期读不到正文（`301` 后 `0` 字节）**。 **不写「免费可用/不可用」。**",
        r42)

# ---- 4.2：MiniMax 4K 第二版（第 8 天）
set_row("MiniMax 4K 第二版", "`MiniMax H3-Image` `4K` 五折 · 第二版",
        "🟠 **第二版第 `8` 天仍在架（页 `309,542`，字节 `−637`、`md5` 变、**正文 `0` 行变** —— 构建副本抖动）。 六档折后价全在**（`0.2261`–`0.5073`），`2026-11-18` / `截止` / `结束` 各 `0` 命中。 "
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
assert "本期改写 `25` 条、补入 `0` 条、其余 `29` 条沿用上期读数" in new_md, "4.2 统计句未找到"
new_md = new_md.replace("本期改写 `25` 条、补入 `0` 条、其余 `29` 条沿用上期读数",
                        "本期改写 `%d` 条、补入 `0` 条、其余 `%d` 条沿用上期读数" % (n_edit, n_carry))

assert new_md != md
if DRY:
    print("DRY RUN —— 未写盘；改写 %d 行；4.1 = %d" % (n_edit, len(r41)))
    print("EDITED:", EDITED)
    sys.exit(0)

io.open(MD, "w", encoding="utf-8", newline=NL).write(new_md)

# ------------------------------------------------------------ ④ 落盘复核
back = io.open(MD, encoding="utf-8").read()
rb = rows_of(back, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
rb2 = rows_of(back, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("落盘复核：4.1 = %d，4.2 = %d，字节 = %d" % (len(rb), len(rb2), len(back.encode("utf-8"))))
assert len(rb) == 65 and len(rb2) == 54
assert "`474/14/11`" in back and "`472/14/11`" not in back
assert "`endpoints: []`" in back
assert "本期改写 `%d` 条" % n_edit in back
for tag, phrase in (("Hy4 flash 限免", "`3` 天"), ("M11W4", "`3` 天"),
                    ("Antigravity 三模型", "`13` 处"), ("Token 羊毛", "`61` 张")):
    assert phrase in back, (tag, phrase)
print("OK 改写 =", n_edit, "｜沿用 =", n_carry)
