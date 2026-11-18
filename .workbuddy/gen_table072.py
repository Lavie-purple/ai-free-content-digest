# -*- coding: utf-8 -*-
"""072 期：在 071 期现行 4.1/4.2 表体上做「天数带符号重算 + 行级改写 + 补入 2 行」。

纪律（055–071 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 补入行必须带「072 期」标记；⑥ 状态列整体替换；
  ⑦ 单元格不许出现 `|`；⑧ 天数一律由基准日实算、**断言带符号**；
  ⑨ 状态列不写「未开始 / 已结束」（会污染 classify()）。
  ⑩ 截止列里既可能有「已过 N 天」也可能有「距截止 N 天」，两个方向都要改（071 只改了前者）。
"""
import io
import re
import sys
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第072期-2026-11-18.md"
PTR = " [附录 072](details.html) |"
TODAY = date(2026, 11, 18)
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
assert len(r41) == 65, ("071 期 4.1 行数", len(r41))
assert len(r42) == 42, ("071 期 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "今日（`11/18`）为截止日", st)
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
assert "已过 `48` 天" in row and "第 `44` 期" in row and "第 `35` 天" in row, row[:200]
row = row.replace("已过 `48` 天", "已过 `49` 天").replace("第 `44` 期", "第 `45` 期").replace("第 `35` 天", "第 `36` 天")
row = row.replace("（第 `2` 期「字节 + `md5`」双同）", "（第 `3` 期「字节 + `md5`」双同）")
row = row.replace(" [附录 071](details.html) |", PTR)
r41[hits[0]] = row
EDITED.append("腾讯老混元(手算)")

# ---- 4.1：Hy4 flash WorkBuddy 限免（参数口径更正 + 权重已开放）
edit("Hy4 flash 限免", "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
     "🟠 **距截止 `11` 天。 （070 期补入）限免只限 `WorkBuddy` 内的 `Hy4 flash`**；其他模型与腾讯云 `TokenHub` 不在内（`TokenHub` 是**限时 `5` 折**）。 "
     "**本期同时补正参数口径**：官方模型卡为 `220B`（含 `64B` Engram）、`safetensors` 实测 `220.25B`、激活 `11.3B` 文本 + `0.43B` 视觉"
     "（070/071 沿用的「`224B` / 激活 `12B`」是媒体口径，本期起不再作主口径）。 "
     "**权重已于 `11/17 11:44`（北京）挂上 `HF` 三仓**（详见 4.2 新增行）—— **限免到期后能用的是权重，不是本行额度**。", r41,
     name="🟠 **腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费（**`220.25B` 实测总参（含 `64B` Engram）/ 激活 `11.3B` + `0.43B` / `1M` 上下文 · 官方口径「`11/30` 前」**）**")

edit("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
     "🔴 **官方写的截止时刻（`11/18 00:00` 北京）已过 `18` 小时，页面上折扣与徽标一个没撤。 （067 期补入）**"
     "`4K` 单张 `0.4522 → 0.2261` 元**仍在**（`6` 处「限时5折」徽标全在：标准版 `3` 行 + 极速版 `3` 行）；`1K` / `2K` **不打折**。 "
     "页 `311,291 → 311,607`（`+316`）；元信息 `dateModified` `2026-11-18T07:17:21Z`（北京 `15:17`）**页面今天动过、折扣没动**（可能是全站构建戳，不作续期证据）。 "
     "**是「悄悄延期」还是「忘了撤」，页面上读不出来** —— 本期不猜。 ⚠️ 折的是按张单价、非额度；要求 ≥ `1660` 万像素。", r41)

edit("Runware 4K 50%", "`Runware` 分发层 `MiniMax H3-Image`",
     "🟠 **已过 `1` 天（`11/17` 到期，本期已按期下架）。 （070 期补入）三条读数：数组仍在（`endsAt: \"2026-11-17\"`、`appliesTo: \"4K images\"`）、"
     "卡片徽标 `2 → 0`、价目一个数没变**（`0.2261` / `0.4522` 整页 `0` 命中）—— **「账本 vs 货架」第 `12` 次实证**。 "
     "**价目不动是对的**：官方帮助文案逐字「`A sale that covers only some generations, such as 4K images, shows a badge … and leaves prices unchanged.`」"
     "→ **这类促销只有徽标能判下架**（避坑 312）。 与 `MiniMax` 官方页（截止 `11/18 00:00`、未撤）**两个口径分岔，两个都写、不换算**。", r41,
     deadline="**`11/17`（官方促销数组 `endsAt: \"2026-11-17\"` 逐字 · 已过 `1` 天）**")

edit("Antigravity 三模型", "`Google Antigravity` 免费档三个第三方模型 `11/18` 移除",
     "⚠️ **今日（`11/18`）为到期日，但本期两次抓取都读不到结果。 （071 期新增观测位）`/pricing` `000`（第 `2` 期）、首页 `200` 但是 `JS` 壳**"
     "（去标签后可见文本 `0` 行，`Gemini 3.8 Flash` / `Sonnet 4.6` / `Opus 4.6` / `Will be removed` **四串全 `0` 命中**）。 "
     "**不写「已移除」、也不写「仍在」—— 两个都没证据**；在页面恢复前，本条只保留 071 期取回的 `178,404` 字节快照（截至 `11/17`）。", r41,
     deadline="**`11/18`（官方角标 `title` 逐字 `Will be removed on November 18, 2026.` · 今日为到期日 · 本期未核到）**")

edit("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `7` 天）。 （066 期补入）官方发布页 `11月25日前开源` 逐字仍在**（本期 `54,010` 字节，与上期逐字节相同）。 "
     "**权重仍未放**：`?author=baidu` 仍 `39` 个仓库（连续第 `15` 天 `0` 变化）。 "
     "两个 `Base` 仓 `downloads` 继续涨（`4,410` / `1,621`）、`likes` `357` / `394`。", r41)

# ---- 4.2：本期有事实的行
edit("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **全量 `470 → 478`（`+8`，全部是 `GPT-6.2` 家族，可逐条点名）；`:free` `14`（**第 `5` 天不变**）；零价 `17`；`?max_price=0` `16`。 "
     "新增 `8` 条：`gpt-6.2-astra` / `-astra-pro` / `-sol` / `-sol-pro` 四条 + 各自 `:batch` 四条（`created` 北京 `11/18 01:59–02:00`）。 "
     "**标价与官方一分不差**（`astra` `$8`/`$40`、`sol` `$2`/`$10`，`batch` 再半价），上下文一律 `1,050,000`（聚合层取整，官方卡是 `1M`）。 "
     "`Ling 3.2 Flash` 的 `endpoints` **仍空（第 `6` 天）**；`hy4-flash` 仍无 `:free` 变体。", r42,
     name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `478/17/14`**）**")

edit("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `10` 期：页头「今天还能领」`¥1758 → ¥1738`（`−20`）、"
     "卡册 `61` 张**（与上期持平）。 **「面额落、卡数不动」是第七种形状**；`71` 期是「面额微降、卡数微增」、本期是**只落面额**。 "
     "**该合计是动态值，不是「羊毛总量」** —— 只记读数、不推规律。", r42)

edit("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
     "⚠️ **官方定价页逐字 `$0/month`（071 期快照，`178,404` 字节）。 本期 `/pricing` `000`（第 `2` 期）、首页 `200` 但是 `JS` 壳**"
     "（`217,290` 字节、可见文本 `0` 行、四个模型名与 `Will be removed` 全 `0` 命中）。 "
     "**「连续 `N` 期字节 + `md5` 双同」对这个壳无效** —— 070 期之前那 `5` 期同值证的是「壳没改」，不是「免费档没改」（纠错④）。 "
     "**免费档现在含哪些模型：本期无一手证据，不出结论。**", r42)

edit("ERNIE-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓库。 `FP8` `4,410`（`+265`）/ `357` 赞（`+2`）；"
     "`BF16` `1,621`（`+140`）/ `394` 赞（`0`）**。 两仓 `lastModified` 仍停 `11/05` —— **仓库没变、下载在涨**，是滚动窗口重算。 "
     "`LICENSE` `25,619` 字节连续第 `13` 天不变。", r42)

edit("Inkling", "`thinkingmachines/Inkling-2-Small` 开放权重",
     "⚠️ **`Apache-2.0` · `gated: false`。 本期 `downloads` 未取到（`429` 限流）** —— **不写涨跌、不拿别仓补位**。"
     "上期读数 `16,918`（`+9,589`）保留作为历史值。 **`downloads` 是近 `30` 天滚动窗口**，跨期不可相减（避坑 249/301）。", r42)

edit("OpenCode 免费清单", "`OpenCode` 免费模型清单 10 → 11",
     "🟡 **`Free models` 段现 `12` 条**（段落逐条；同口径 `-free` 正则只得 `11`，因 `Big Pickle` 无 `-free` 后缀 —— **三个数口径不同，不可相减**）。 "
     "**同页 `Deprecated models` 表本期第一次读**：`GLM-5.3-Flash Free` `November 18, 2026`（今天）、`MiniMax M3.1 Flash Free` / `Gemini 3.1 Pro` / `Gemini 3 Flash` 均 `11/17`。 "
     "**071 期「滚动池有进有出」的解释被这张表推翻** —— 是按表弃用（纠错②）。 `hy4-flash-free` **仍在**。 页 `98,080 → 102,315`（`+4,235`）。", r42,
     name="🟡 **`OpenCode` 免费模型清单（`Free models` 段 `12` 条 · `GLM-5.3-Flash Free` 今日弃用）**")

edit("Praxis", "Runway `Praxis-1` 开放权重",
     "🟢 **（068 期补登）`Apache-2.0` · `27B` 混合专家扩散 Transformer。 本期 `GitHub` `stars 115 → 117`（`+2`）、`forks 6`、`open_issues 10`；"
     "`pushed_at` `11/17 15:52:01Z`、`updated_at` `11/18 06:46:32Z`**（有活动，非停推）。 `HF` 单仓仍未取到。", r42)

edit("PEAR", "MIT 韩松团队 `PEAR`",
     "🟢 **已公开（069 期补登）。 `GitHub` `stars 574 → 654`（`+80`）、`forks 36 → 42`、`open_issues 5`；"
     "`pushed_at` 更新为 `11/18 10:07:10Z`**（上期 `11/16 07:54:56Z`，隔一天再推）。 `LICENSE` 原文 `11,544` 字节已读（`Apache-2.0`）；"
     "`LIBERO` `1.6% → 74.4%`；**仍未见到第三方复现 `74.4%`**。", r42)

edit("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **已公开（069 期补登）。 `downloads 1,850 → 2,173`（`+323`）/ `likes 353 → 356`（`+3`）；`lastModified` 仍 `11/10 07:28Z`；"
     "`?author=meituan-longcat` 仍 `32` 仓**。 四个时间点仍分开写：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`、媒体稿 `11/15 10:06Z`、**一手页无「发布日期」字段**。", r42)


# ------------------------------------------------------------ ③ 补入新行（4.2 两条）
NEW42_A = ("| 🟢 **腾讯混元 `Hy4 flash` 开放权重（**`220.25B` 实测 · 激活 `11.3B` + `0.43B` · `1M` · `Tencent Hy License 1.0`**）** "
           "| **无截止日（权重永久开放；许可证 `§10` 有商用门槛，不是时间门槛）** "
           "| 🟢 **（072 期补入）三仓同分钟建仓**：`tencent/Hy4-flash`（`11/17 03:44:46Z`）/ `-FP8` / `-base`，均 `gated: false`、`200` / `200` / `191` 个文件；"
           "`HF` `downloads 0`、`likes 136`；`GitHub` `44` stars。 **许可是 `Apache 2.0` 派生 + `§10`**：对外做 `MaaS` 且（全球年毛收入 > `US$50M` 或产品 `MAU` > `1` 亿）须另签；"
           "**`§10.3` 纯内部使用豁免**。 **开放四层：能下载 / 能跑 / 能改 都是「是」，能商用是「有条件」**（避坑 309）。 |")

idx2 = [k for k, r in enumerate(r42) if "阿里 `Qwen4-Max` 发布" in name_of(r)]
assert len(idx2) == 1, idx2
r42.insert(idx2[0], NEW42_A)

NEW42_B = ("| 🟡 **OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布（**可用名单 `Plus` / `Pro` / `Enterprise` / `Edu` · **`Free` 不在名单里**）** "
           "| **无截止日（模型发布；无免费档配额可算）** "
           "| 🟡 **（072 期补入）`publicationDate` `2026-11-17T17:45:00Z`（北京 `11/18 01:45`）。 官方逐字 `available to all Plus, Pro, Enterprise, and Edu users`**"
           "—— **`Free` 一次都没出现**；`chatgpt.com/pricing` 本期 `000`、`openai.com/api/pricing` **也未列 `gpt-6.2`** → **只能说「发布页名单里没有免费档」**。 "
           "API 价：`Astra` `$8`/`$0.40`/`$40`、`Sol` `$2`/`$0.10`/`$10`（每百万 token）；`Pro 200` **首次**拿到 `Ultrafast`（从 `Sol` 开始）。 "
           "`OpenRouter` 同日 `8` 条，**标价与官方一分不差**（不是「折扣写进标价」）。 |")

idx2 = [k for k, r in enumerate(r42) if "`inclusionAI` `Ling 3.2 Flash`" in name_of(r)]
assert len(idx2) == 1, idx2
r42.insert(idx2[0], NEW42_B)


# ------------------------------------------------------------ ④ 指针重贴当期期号
def repoint(bucket):
    n = 0
    for k, r in enumerate(bucket):
        if "附录 071" in r:
            bucket[k] = r.replace("附录 071", "附录 072")
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
assert len(d41) == 65, len(d41)
assert len(d42) == 44, len(d42)
assert "072 期补入" in disk
assert "Tencent Hy License 1.0" in disk
assert "已过 `49` 天" in disk
assert "第 `45` 期" in disk
assert "已过 `1` 天（`11/17` 到期" in disk
assert "`478/17/14`" in disk
assert "附录 071" not in disk

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
            bad.append((name_of(r)[:26], m.group(0), delta))
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
