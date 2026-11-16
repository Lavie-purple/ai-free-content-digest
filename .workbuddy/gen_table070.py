# -*- coding: utf-8 -*-
"""070 期：在 069 期现行 4.1/4.2 表体上做「天数带符号重算 + 行级改写 + 补入 2+1 行」。

纪律（055–069 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 补入行必须带「070 期」标记；⑥ 状态列整体替换；
  ⑦ 单元格不许出现 `|`；⑧ 天数一律由基准日实算、**断言带符号**；
  ⑨ **070 期新立**：日粒度字段不做时区换算 —— `Runware` 的 `endsAt: 2026-11-17`
     与 `MiniMax` 的 `11/18 00:00` 北京**并排写、不判同源**（纠错①）。
"""
import io
import re
import sys
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第070期-2026-11-16.md"
PTR = " [附录 070](details.html) |"
TODAY = date(2026, 11, 16)
DRY = "--apply" not in sys.argv

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")


def rows_of(text, start, end):
    i = text.index(start)
    j = text.index(end)
    return [l for l in text[i:j].split("\n")
            if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]


r41 = rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
r42 = rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("输入行数：4.1 = %d，4.2 = %d" % (len(r41), len(r42)))
assert len(r41) == 61, ("069 期 4.1 行数", len(r41))
assert len(r42) == 39, ("069 期 4.2 行数", len(r42))


def name_of(r):
    return r.strip().strip("|").split("|")[0].strip()


def cells_of(r):
    return r.strip().strip("|").split("|")


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
TOK = re.compile(r"(距截止|已过|距今)\s*`?(\d+)`?\s*天")


def fix_status(st, delta):
    if delta > 0:
        return TOK.sub(lambda m: "%s `%d` 天" % ("距今" if m.group(1) == "距今" else "距截止", delta), st)
    if delta == 0:
        return TOK.sub(lambda m: "今日（`11/16`）为截止日" if m.group(1) != "距今" else "今日（`11/16`）", st)
    return TOK.sub(lambda m: "已过 `%d` 天" % (-delta), st)


for bucket in (r41, r42):
    for k, row in enumerate(bucket):
        c = cells_of(row)
        if len(c) != 3:
            continue
        delta = days_of(c[1])
        if delta is None:
            skipped.append(name_of(row)[:28])
            continue
        st = c[2]
        new = fix_status(st, delta)
        newdl = c[1]
        if delta < 0:
            newdl = re.sub(r"已过\s*`?\d+`?\s*天", "已过 `%d` 天" % (-delta), newdl)
        elif delta == 0:
            newdl = re.sub(r"（\s*已过\s*`?\d+`?\s*天\s*）", "（今日 `11/16` 到期）", newdl)
        if new != st or newdl != c[1]:
            c[2] = new
            c[1] = newdl
            bucket[k] = "|" + "|".join(c) + "|"
            changed += 1
print("天数改写行数 =", changed, "｜无日期可算 =", len(skipped), skipped)


# ------------------------------------------------------------ ② 行级改写
EDITED = []


def edit(tag, prefix, status, bucket, deadline=None):
    hits = [k for k, r in enumerate(bucket) if prefix in name_of(r)]
    assert len(hits) == 1, ("命中数不是 1", tag, len(hits))
    c = cells_of(bucket[hits[0]])
    assert len(c) == 3, ("字段数异常", tag, len(c))
    assert "|" not in status, ("状态列里出现竖线", tag)
    dl = deadline if deadline is not None else c[1]
    assert "|" not in dl, ("截止列里出现竖线", tag)
    new = "|%s| %s | %s%s" % (c[0], dl, status, PTR)
    assert new != bucket[hits[0]], ("改写未生效", tag)
    bucket[hits[0]] = new
    EDITED.append(tag)


# ---- 腾讯老混元：截止列不可解析，天数与期数手工推进（脚本不读）
hits = [k for k, r in enumerate(r41) if "腾讯老混元" in name_of(r)]
assert len(hits) == 1
row = r41[hits[0]]
assert "已过 `45` 天" in row and "第 `42` 期" in row and "第 `33` 天" in row, row[:200]
row = row.replace("已过 `45` 天", "已过 `47` 天").replace("第 `42` 期", "第 `43` 期").replace("第 `33` 天", "第 `34` 天")
row = row.replace("`6,893` 字节", "`6,894` 字节")
row = row.replace(" [附录 069](details.html) |", PTR)
r41[hits[0]] = row
EDITED.append("腾讯老混元(手算)")

# ---- 4.1 本期有事实的行
edit("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `9` 天）。 （066 期补入）官方发布页 `11月25日前开源` 逐字仍在**（本期 `54,010` 字节、可见文本 `131` 行）。 "
     "**权重仍未放**：`?author=baidu` 本期仍 `39` 个仓库（连续第 `13` 天 `0` 变化）、`ERNIE-5.5-Flash-Preview` 仓 `0` 命中；"
     "两个 `Base` 仓 `downloads` 本期冻结（`3,914` / `1,388`）、`likes` 仍在涨（`324` / `394`）。", r41)

edit("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时 `5` 折",
     "🟠 **生效中（距截止 `2` 天）。 （067 期补入）`4K` 单张 `0.4522 → 0.2261` 元；`1K` `0.1430` / `2K` `0.1531` **不打折**。 "
     "本期页面 `311,690` 字节 **且 `md5 3f0a6240` 与上期双同**（第 `2` 期）、可见文本逐行 `0` 差异 —— **这才是「真的没改」**（避坑 300）。 "
     "⚠️ 折的是按张单价、不是额度；要求 ≥ `1660` 万像素。", r41)

edit("Runware 30%", "`Runware` 分发层 `MiniMax H3 Max` 促销 `30% OFF`",
     "⚪ **已过 `1` 天（`11/15` 到期）。 （069 期补入）**本期卡片上的 `30% OFF` 徽标已卸下，而促销数组里 `endsAt: \"2026-11-15\"` 那条原样还在** —— "
     "**「数组是账本、卡片是货架」第 `1` 次双读实证**（避坑 303）。作用于 `minimax-h3-max` / `h3-max-turbo` 按次单价；折扣不是免费额度。",
     r41, deadline="**`11/15`（官方促销数组 `endsAt: \"2026-11-15\"`；已过 `1` 天）**")

edit("腾讯轻量云", "腾讯轻量云专家限量",
     "🟢 **已过 `3` 天（`11/13` 到期，官方未给延长口径）。", r41)

edit("48 号公告", "商务部 / 科技部 2026 年第 48 号公告",
     "🟡 **已过 `1` 天（`11/15` 征求意见截止，未见延长公告）**；登记实施日「未公布」（自公布之日起）。 "
     "本条只记日期，不对条款内容下判断。", r41,
     deadline="**`11/15`（征求意见截止 · 已过 `1` 天）；登记实施日「未公布」（自公告发布日起至目录正式修订实施日止）**")

edit("Gemini 4 Argon", "Google `Gemini 4 Argon`",
     "🟠 **距截止 `14` 天（官方口径「11 月底」：首发优惠价到期）。 本期未见官方改口径。", r41)

edit("Google AI Plus", "Google AI Plus 失去 Pro 模型选择权",
     "🟠 **已过 `3` 天（`11/13` 生效）。", r41)

edit("Fable 5.2", "Anthropic `Claude Fable 5.2` / `Mythos 5.2` 发布优惠",
     "🟢 **距截止 `1` 天（`11/16 23:59 PT` ＝ 北京 `11/17 15:59`）。 本期 `claude.com/pricing` 字节数 `1,344,079` **与上期完全相同**、"
     "`md5` 不同（`CSP nonce` 每请求都变 · 连续第 `5` 期）、可见文本逐行 `0` 差异；优惠口径未改。", r41,
     deadline="**`11/17 15:59`（北京 · 官方逐字 `11/16 23:59 PT`：`Pro` / `Team` 标准席位含 `Fable` 一周 · 距截止 `1` 天）；`2027-03-08 23:59 PT`（`Max` / `Ultra` / 高级席位的 `1–3` 次 `Fable` 重置到期）**")

edit("Runware upscale", "`Runware` 分发层 `pruna-p-video-upscale` 促销",
     "🟢 **已过 `8` 天（`11/8` 到期）。 促销数组本期 `endsAt` 仍 `20` 处、日期集合逐项相同；"
     "**「数组里还在 ≠ 在售」第 `9` 次实证**（`11/15` / `11/17` / `11/19` / `11/30` / `12/31` 五条仍未到期）。", r41)

# ---- 4.2 本期有事实的行
edit("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **全量 `470 → 468`（`−2`）；`:free` `14`（**第 `3` 天不变**）；零价 `17`；`?max_price=0` `16`。 "
     "**进 `1` 出 `3`**：进 `qwen/qwen4-max`（**付费**，`created 11/16 02:18:46Z`）；出 `qwen/qwen3-vl-30b-a3b-thinking` / "
     "`stepfun/step-3.5-flash` / `tencent/hunyuan-a13b-instruct` —— **换代，不是免费区缩水**。 "
     "`Ling 3.2 Flash` 的 `endpoints` **空 `3` 天**（`[]`）、`inclusionAI/Ling-3.2-flash` 仍 `404`。", r42)

edit("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `8` 期：页头「今天还能领」`¥2433 → ¥1760`（`−673`）、"
     "卡册 `62 → 60` 张、日戳 `11/16` `20` / `11/15` `22` / `11/14` `72` / `11/13` `2` / `11/9` `4` ＝ `120`。 "
     "**第一次「面额与卡数同降」**；`11/14` 的 `108` 掉到 `72`、`11/15` 的 `6` 涨到 `22` —— 日戳会被**重新盖章**到更晚日期。 五期形状全不同，只记读数。", r42)

edit("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
     "🟢 **官方定价页逐字 `$0/month`。 含 `Unlimited Tab` / `Unlimited Command` / **`Basic weekly rate limits`**；"
     "`free` / `Free` 整页各 `0` 命中；额度仍无具体数字。 **本期首页与 `/pricing` 的字节 + `md5` 与上期全同（第 `5` 期同值）**，横幅「`Gemini 4 Hydrogen and Orchestrator`」一字未动、**不写档位**。", r42)

edit("ERNIE-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓库。 `FP8` `3,914` 下载（**冻结**）/ `324` 赞（`+7`）；"
     "`BF16` `1,388`（`+231`）/ `394`（`+3`）—— **同一批里唯一在动的一个**。 `LICENSE` `25,619` 字节连续第 `11` 天不变；两仓 `lastModified` 仍停 `11/05`。", r42)

edit("Ripple", "`Ripple-65B Preview` 开放权重",
     "🟢 **`061` 期补登 · 仓库建于 `11/4`。 `downloads 10,675`（**冻结**）/ `likes 589`（`+5`）；`lastModified` 仍停 `11/10 09:31Z`。 "
     "**slug 是 `ricursiveAI/Ripple-65B-Preview`**（往期未留档，本期补记，供下期直接复抓）。", r42)

edit("Inkling", "`thinkingmachines/Inkling-2-Small` 开放权重",
     "🟢 **`Apache-2.0` · `gated: false`。 `downloads 7,329`（**冻结**、与上期同）/ `likes 363`（`+36`）；"
     "`MXFP8` 变体 `638`（`0`）/ `14`（`+1`）、`lastModified 11/15 05:56Z` 未再动。 **两日曲线 `12 → 1,064 → 7,329` 本期无法续算**（下载字段滞后 · 避坑 301）。", r42)

edit("OpenCode 免费清单", "`OpenCode` 免费模型清单",
     "🟡 **`-free` `id` `14 → 15`（同口径复扫）**：进 `hy4-flash-free`（逐字 `free on OpenCode for a limited time`、**零留存、不用于训练**、官方未给结束日）。 "
     "页面 `98,592` 字节（`+417`）、**可见文本 diff `10` 行全部落在这一个模型块**。 "
     "⚠️ 069 期正文写 `13` 条是手数口径，本期起统一用正则口径并给出完整清单。", r42)

edit("Praxis", "Runway `Praxis-1` 开放权重",
     "🟢 **（068 期补登）`Apache-2.0` · `27B` 混合专家扩散 Transformer。 本期 `HF` 单仓 `praxis-1-base` `155`（**冻结**）/ `10`；"
     "`GitHub` `stars 105 → 111`、`pushed_at` 仍停 `11/12 22:14Z`（**第 `5` 天未推**）。", r42)

edit("PEAR", "MIT 韩松团队 `PEAR`",
     "🟢 **已公开（069 期补登）。 `GitHub` `stars 240 → 442`（`+202`）、`forks 32`、**`pushed_at` 本期首次更新（`11/16 07:54:56Z`）** —— "
     "建仓后第一次推送，`created_at` 仍 `11/13 17:43:06Z`。 `LICENSE` 原文 `11,544` 字节已读（Apache 2.0）；`HF` 集合三条。 "
     "`LIBERO` 零样本 `1.6% → 74.4%`；真机 `YAM` `30` 试成 `18`；**不用遥操数据、不用真机数据**。", r42)

edit("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **已公开（069 期补登）。 `downloads 1,573`（**冻结**、与上期同）/ `likes 289`（`0`）；`lastModified` 仍 `11/10 07:28Z`；"
     "`?author=meituan-longcat` 仍 `32` 仓。 四个时间点仍分开写：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`、媒体稿 `11/15 10:06Z`、**一手页无「发布日期」字段**。", r42)


# ------------------------------------------------------------ ③ 补入新行
NEW41_1 = ("| 🟠 **腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费（**`224B` 总参（含 `64B` Engram）/ 激活 `12B` / `1M` 上下文 · 官方口径「`11/30` 前」**）** "
           "| **`11/29`（聚合层逐字「到 `11月29日`」；媒体逐字「`11月30日前`」——**两个日期并排写、不合并**）** "
           "| 🟠 **距截止 `13` 天。 （070 期补入）**限免只限 `WorkBuddy` 内的 `Hy4 flash`**：其他模型、腾讯云 `TokenHub` 接口**都不在**本次限免内（`TokenHub` 是**限时 `5` 折**、不是免费）。 "
           "同日在 `OpenCode Zen` 另有 `hy4-flash-free`（**零留存、不用于训练**）；`Hy4 flash` 本体「计划开源」、**无时间表**。 "
           "⚠️ `hunyuan.tencent.com` 是 `JS` 壳、`consult` 文档未更新 → **参数与价格本期只能引媒体**（如实标注）。 |")

idx = [k for k, r in enumerate(r41) if "百度 `ERNIE 5.5 Flash Preview` 发布" in name_of(r)]
assert len(idx) == 1, idx
r41.insert(idx[0], NEW41_1)

NEW41_2 = ("| 🟠 **`Runware` 分发层 `MiniMax H3-Image` / `-Highspeed` 促销 `50% OFF`（**逐字 `50% off images of at least 16,600,000 pixels until November 17, 2026`**）** "
           "| **`11/17`（官方促销数组 `endsAt: \"2026-11-17\"` 逐字 · 距截止 `1` 天）** "
           "| 🟠 **（070 期补入）只作用于 `4K`（≥ `1660` 万像素）图**，两个型号同价；**与 `MiniMax` 官方「`11/18 00:00` 北京」是两条不同的日期字段**（日粒度 vs 时刻，**不做时区换算** · 纠错①）。 "
           "`Runware` 侧比官方**早 `1` 天**结束，本报两个都写。 **折扣不是免费额度。** |")

idx = [k for k, r in enumerate(r41) if "`Runware` 分发层 `pruna-p-video-upscale` 促销" in name_of(r)]
assert len(idx) == 1, idx
r41.insert(idx[0] + 1, NEW41_2)

NEW42_1 = ("| 🟡 **阿里 `Qwen4-Max` 发布（**`2.4T` 主干 / 每 token 激活 `71B` + `328B` `N-Gram Embedding` · `1M` 上下文 · 原生视觉 · `$1.5` / `$4.5` 每百万 token**）** "
           "| **无截止日（付费旗舰；「小尺寸 `Qwen4` 将开源」是承诺、**无型号无日期**）** "
           "| 🟡 **（070 期补入）**付费**模型 —— 官方博客 `free` / `免费` **`0` 命中**，只写「可在 `QwenWork` / `Qoder` / `QwenStudio` 使用」，"
           "**本报只写「可体验」、不进免费清单**（避坑 304）。 真正能拿走的两件：`Qwen-Live-Delivery-Plugin` 官方逐字 `open-sourcing`（**仓库地址未给、未取 `spdx`**）、"
           "**「`Smaller models … are coming to open source`」（无型号 / 无日期 / 无许可证）**。 成本降幅两套口径：美元 `$4.43 → $1.67`（`−62%`）/ 人民币 `26.58 → 11.16` 元（`−58%`），**不合并**。 |")

idx2 = [k for k, r in enumerate(r42) if "美团 `LongCat-2.5` 以 `MIT`" in name_of(r)]
assert len(idx2) == 1, idx2
r42.insert(idx2[0], NEW42_1)


# ------------------------------------------------------------ ④ 指针重贴当期期号
def repoint(bucket):
    n = 0
    for k, r in enumerate(bucket):
        if "附录 069" in r:
            bucket[k] = r.replace("附录 069", "附录 070")
            n += 1
    return n


print("指针重贴：4.1", repoint(r41), "4.2", repoint(r42))
print("改写行：", len(EDITED), EDITED)
print("输出行数：4.1 = %d，4.2 = %d" % (len(r41), len(r42)))
if DRY:
    for tag, row in (("41 样本", r41[1]), ("42 样本", r42[5])):
        print(tag, row[:400])
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
assert len(d41) == 63, len(d41)
assert len(d42) == 40, len(d42)
assert "070 期补入" in disk
assert "`hy4-flash-free`" in disk
assert "已过 `47` 天" in disk
assert "第 `43` 期" in disk

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
