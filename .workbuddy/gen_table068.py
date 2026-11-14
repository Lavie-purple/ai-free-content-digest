# -*- coding: utf-8 -*-
"""068 期：在 067 期现行 4.1/4.2 表体上做「天数实算 + 行级改写 + 补入 2+2 行」。

纪律（055–067 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 补入行必须带「068 期」标记；⑥ 状态列整体替换；
  ⑦ 单元格不许出现 `|`；⑧ 天数一律由基准日实算。
"""
import io
import re
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第068期-2026-11-14.md"
PTR = " [附录 068](details.html) |"
TODAY = date(2026, 11, 14)

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")


def rows_of(text, start, end):
    i = text.index(start)
    j = text.index(end)
    return [l for l in text[i:j].split("\n")
            if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]


r41 = rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
r42 = rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
print("输入行数：4.1 = %d，4.2 = %d" % (len(r41), len(r42)))
assert len(r41) == 58, ("067 期 4.1 行数", len(r41))
assert len(r42) == 35, ("067 期 4.2 行数", len(r42))


def name_of(r):
    return r.strip().strip("|").split("|")[0].strip()


def cells_of(r):
    return r.strip().strip("|").split("|")


def days_of(deadline):
    m = re.search(r"(\d{1,2})/(\d{1,2})", deadline)
    if not m:
        return None
    mo, d = int(m.group(1)), int(m.group(2))
    return (date(2026, mo, d) - TODAY).days


# ------------------------------------------------------------ ① 天数一律实算
changed = 0
skipped = []
for bucket in (r41, r42):
    for k, row in enumerate(bucket):
        if len(cells_of(row)) != 3:
            continue
        c = cells_of(row)
        delta = days_of(c[1])
        if delta is None:
            skipped.append(name_of(row)[:28])
            continue
        st = c[2]
        new = st
        if delta > 0:
            new = re.sub(r"已过 `\d+` 天", "已过 `%d` 天" % delta, new)
            new = re.sub(r"距截止 `\d+` 天", "距截止 `%d` 天" % delta, new)
            new = re.sub(r"距承诺日 `\d+` 天", "距承诺日 `%d` 天" % delta, new)
        elif delta == 0:
            new = re.sub(r"已过 `\d+` 天", "今日（`11/14`）为截止日", new)
            new = re.sub(r"距截止 `\d+` 天", "今日（`11/14`）为截止日", new)
            new = re.sub(r"距承诺日 `\d+` 天", "今日（`11/14`）为承诺日", new)
        else:
            # 尚未到期：把「已过」改回「距截止」
            new = re.sub(r"已过 \d+ 天", "距截止 `%d` 天" % (-delta), new)
            new = re.sub(r"已过 `\d+` 天", "距截止 `%d` 天" % (-delta), new)
            new = re.sub(r"距截止 `\d+` 天", "距截止 `%d` 天" % (-delta), new)
            new = re.sub(r"距承诺日 `\d+` 天", "距承诺日 `%d` 天" % (-delta), new)
        if new != st:
            c[2] = new
            bucket[k] = "|" + "|".join(c) + "|"
            changed += 1
print("天数改写行数 =", changed, "｜无日期可算 =", len(skipped))


# ------------------------------------------------------------ ② 行级改写
EDITED = []


def edit(tag, prefix, status, bucket):
    hits = [k for k, r in enumerate(bucket) if prefix in name_of(r)]
    assert len(hits) == 1, ("命中数不是 1", tag, len(hits))
    c = cells_of(bucket[hits[0]])
    assert len(c) == 3, ("字段数异常", tag, len(c))
    assert "|" not in status, ("状态列里出现竖线", tag)
    new = "|%s|%s| %s%s" % (c[0], c[1], status, PTR)
    assert new != bucket[hits[0]], ("改写未生效", tag)
    bucket[hits[0]] = new
    EDITED.append(tag)


# 4.1 里本期有事实的行
edit("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `11` 天）。 （066 期补入）官方发布页 `限时` / `免费` 各 `0` 命中**；"
     "`11月25日前开源` 逐字仍在（本期 `1` 命中）。 **权重仍未放**：`?author=baidu` 本期仍 `39` 个仓库（`0` 变化）、"
     "`ERNIE-5.5-Flash-Preview` 仓 `0` 命中；`OpenRouter` 的 `:free` 条目仍在（本条未撤）。", r41)

edit("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时 `5` 折",
     "🟠 **生效中（距截止 `4` 天）。 （067 期补入）标准版 `4K` 单张 `0.4522 → 0.2261` 元、极速版 `0.8550 → 0.4275`；"
     "`1K` `0.1430` 与 `2K` `0.1531` **不打折**。 本期页面 `331,542 → 311,690` 字节（`−19,852`），"
     "但**可见文本 `111,720` 字逐字相同** —— 只动了构建指纹。 `Runware` 同名促销 `endsAt 2026-11-17`（`UTC`）＝北京 `11/18 00:00`。**"
     " ⚠️ 折的是按张单价、不是额度；要求 ≥ `1660` 万像素。", r41)

edit("Antigravity 6mo", "`Google Antigravity` 科研 / 安全 6 个月免费档",
     "🟡 **以申请通过为准（相对日期：官方逐字 `free of charge for 6 months`，未给统一截止日）。 "
     "⚠️ 本期 `antigravity.google` 恢复可达（首页 `200` / `214,361` 字节、`/pricing` `200` / `140,014` 字节），"
     "个人档 `$0/month` 仍在、含 `Basic weekly rate limits`；**`free` 整页 `0` 命中**（免费只用 `$0` 表达）。", r41)

edit("腾讯轻量云", "腾讯轻量云专家限量",
     "🟢 **已过 `1` 天（`11/13` 到期，官方未给延长口径）。 067 期记为「今日为截止日」，本期按实算改为「已过 `1` 天」。", r41)

edit("48 号公告", "商务部 / 科技部 2026 年第 48 号公告",
     "🟡 **距截止 `1` 天（`11/15` 征求意见截止）；登记实施日「未公布」（自公布之日起）。 "
     "本条只记日期，不对条款内容下判断。", r41)

edit("Gemini 4 Argon", "Google `Gemini 4 Argon`",
     "🟠 **距截止 `16` 天（官方口径「11 月底」：首发优惠价到期）。 本期未见官方改口径。", r41)

edit("Google AI Plus", "Google AI Plus 失去 Pro 模型选择权",
     "🟠 **已过 `1` 天（`11/13` 生效，067 期写「今日为截止日」，本期按实算改为「已过 `1` 天」）。", r41)

edit("Fable 5.2", "Anthropic `Claude Fable 5.2` / `Mythos 5.2` 发布优惠",
     "🟢 **距截止 `2` 天（`11/16 23:59 PT`）。 本期 `claude.com/pricing` `+18` 字节、可见文本逐行 `0` 差异，优惠口径未改。", r41)

# 4.2 里本期有事实的行
edit("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **全量 `472 → 471`（`−1`）；`:free` `14 → 14`；零价 `17 → 17`；`?max_price=0` `16 → 16`。 "
     "进 `inclusionai/ling-3.2-flash:free`（`created 11/13 17:45 UTC`，`1,048,576` 上下文、文+图、**`endpoints` 为空数组**）；"
     "出 `liquid/lfm-2.5-2.6b` 与它的 `:free` 两条。**进 `1` 出 `2`，总数 `−1`。**", r42)

edit("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `6` 期：页头「今天还能领」`¥598 → ¥1599`（`+1001`）、"
     "卡册 `57 → 59` 张、核实日戳 `11/14` `108` / `11/13` `2` / `11/9` `4` / `11/8` `4` ＝ `118`。 "
     "**`11/13` 的 `12` 条次日定格到 `2`**（进行值第 `3` 次实证）。 本报只记数字，不解释 `+1001` 的成因。", r42)

edit("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
     "🟢 **官方定价页逐字 `$0/month`（本期首次真正读到）。 含 `Unlimited Tab` / `Unlimited Command` / **`Basic weekly rate limits`**；"
     "`free` / `Free` 整页各 `0` 命中（免费只用 `$0` 表达）；额度仍无具体数字。 顶部横幅写 `Gemini 4 Hydrogen and Orchestrator now in Google Antigravity`，"
     "**不写档位**。 本条是本报至今唯一一条「免费上限有形容词、没有数」的样本。", r42)

edit("ERNIE-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓库。 本期 `FP8` `3,372` 下载 / `308` 赞（`+409` / `+9`）、"
     "`BF16` `1,157` / `391`（`+136` / `+1`）；`LICENSE` `25,619` 字节连续第 `9` 天不变；两个仓库 `lastModified` 仍停 `11/05`。", r42)

edit("Ripple", "`Ripple-65B Preview` 开放权重",
     "🟢 **`061` 期补登 · 仓库建于 `11/4`。 本期 `downloads 8,500` / `likes 582`（`+833` / `+38`）；`lastModified` 未动。", r42)

edit("Inkling", "`thinkingmachines/Inkling-2-Small` 开放权重",
     "🟢 **`Apache-2.0` · `gated: false` · `36` 个文件。 本期 `downloads 12 → 1,064`（**`86` 倍**）/ `likes 166 → 280`；"
     "`lastModified 11/13 21:12 UTC`（北京 `11/14 05:12`，落在本期窗口内）。`MXFP8` 变体 `13 → 221` / `7 → 12`。 "
     "**`likes`/`downloads` 比从 `13.8` 掉到 `0.26`** —— 从「没人拉」变成「拉的人比点赞的多 `4` 倍」。", r42)

edit("OpenCode 免费清单", "`OpenCode` 免费模型清单",
     "🟡 **免费清单 `10 → 11` 项（`LongCat 2.5 Preview Free` 上架 · 窗口外补记）**。 本期 `opencode.ai/docs/zen` "
     "`98,175` 字节 / `md5 2a3bb097` 与上期**逐字节相同**，免费 `ID` 仍 `13` 条 —— **第 `5` 期冻结**。", r42)


# ------------------------------------------------------------ ③ 补入新行
NEW41_1 = ("| 🟠 **Runway 企业版「最多 `2` 个月用量免费」（**官方横幅逐字 `Enterprises get up to 2 months of usage free. Sign by 12/31.`**）** "
           "| **`12/31`（官方逐字 `Sign by 12/31`；条款页 `runway.com/terms` 本期 `404`）** "
           "| 🟠 **生效中（距截止 `47` 天）。 （068 期补入）⚠️ 三个要件缺两个：`up to`（上限不是保底）、条件（`See terms` 指向的条款页本期 `404` / `364,328` 字节）。 "
           "**本报只登记横幅与日期，不写「几个月」「什么条件」。** 免费档另有 `125` **一次性** credits（`$0/月`、`Free forever`、限「a selection of models」）。 "
           "|")

NEW41_2 = ("| 🟠 **Runway 平台 `Kling 4.0` 生成 `25% off`（**官方 `pricing` 页逐字 `25% off Kling 4.0 generations until November 30`**）** "
           "| **`11/30`（官方逐字 `until November 30`，未写时区）** "
           "| 🟠 **生效中（距截止 `16` 天）。 （068 期补入）⚠️ 只在 `Standard` / `Pro` 两个**付费档**下列出，免费档（`125` 一次性 credits）下没有这一条；"
           "与 4.1 里 `Runware` 那条 `Kling 4.0 15% OFF`（`10/29` 已过期）是**两个不同分发商的两场促销**，不可合并。 **折扣不是免费。** "
           "|")

idx = [k for k, r in enumerate(r41) if "MiniMax `H3-Image` `4K` 生图限时" in name_of(r)]
assert len(idx) == 1, idx
r41.insert(idx[0] + 1, NEW41_2)
r41.insert(idx[0] + 2, NEW41_1)

NEW42_1 = ("| 🟡 **`inclusionAI` `Ling 3.2 Flash` 进入 `OpenRouter` 免费区（**`:free` 零价 · `1,048,576` 上下文 · 文本 + 图片 · 单次最多 `200` 张图**）** "
           "| **无截止日（进入免费列表，官方未给上下线时间）** "
           "| 🟡 **（068 期补入）三层只开一层**：① 列表有（`created 1794591958` ＝ `11/13 17:45 UTC`）；"
           "② `/api/v1/models/inclusionai/ling-3.2-flash-20261113/endpoints` 返回 **`\"endpoints\":[]`**；"
           "③ 它自己写的 `hugging_face_id` `inclusionAI/Ling-3.2-flash` 在 `hf-mirror` 是 **`404`**。 "
           "**全量 `471` 条里 `ling-3.2` 只有 `:free` 一条，没有付费档** —— 是「只登免费档」的第三种形态。 **本报不写「可以免费用」。** "
           "|")

NEW42_2 = ("| 🟢 **Runway `Praxis-1` 开放权重（**`Apache-2.0` · `27B` 混合专家扩散 Transformer · 权重 + 推理 + 微调代码**）** "
           "| **无截止日（开放权重，官方未给回收 / 下线日）** "
           "| 🟢 **（068 期补登）`RoboLab-120` `46.2%`（`FLUX 3 Action` `42.9%` / `Cosmos3 Nano` `36.8%` / `π0.5` `28.0%`，`1,200` 回合，**官方自测**）；"
           "`SimplerEnv`（`RT-1` 机体微调后）`80.0%`，原版 `RT-1` `52.4%`。 `HF` 集合 `11` 条（`base`/`droid`/`yam`/`so101` × `lerobot`/`nvfp4` + `eval` 数据集）；"
           "`GitHub` `runwayml/praxis-1-oss` `license.spdx_id = Apache-2.0`、`pushed_at 11/12 22:14 UTC`、`stars 103`。 "
           "**⚠️ 三个时间点（官方页 `11/11 15:00Z` / `HF` 集合 `11/12 20:22Z` / `GitHub` `11/12 22:14Z`）都不在本期窗口内 —— 066、067 两期漏报，本期按「补登」收录。** "
           "标准版 `80 GB` 显存，压缩版官方估算可上 `RTX 5090`（峰值未实测）。 |")

idx2 = [k for k, r in enumerate(r42) if "`thinkingmachines/Inkling-2-Small` 开放权重" in name_of(r)]
assert len(idx2) == 1, idx2
r42.insert(idx2[0] + 1, NEW42_2)
r42.insert(idx2[0] + 2, NEW42_1)


# ------------------------------------------------------------ ④ 指针重贴当期期号
def repoint(bucket):
    n = 0
    for k, r in enumerate(bucket):
        if "附录 067" in r:
            bucket[k] = r.replace("附录 067", "附录 068")
            n += 1
    return n


print("指针重贴：4.1", repoint(r41), "4.2", repoint(r42))


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
assert len(d41) == 60, len(d41)
assert len(d42) == 37, len(d42)
assert "068 期补入" in disk
assert "`endpoints` 为空数组" in disk or '"endpoints":[]' in disk
assert "86` 倍" in disk
assert "111,720" in disk

dist = Counter(len(cells_of(r)) for r in d41 + d42)
print("字段数分布：", dict(dist))
assert set(dist) == {3}, dist

# 天数复核：每个带日期的行，状态列里的数字必须等于实算
bad = []
for r in d41 + d42:
    c = cells_of(r)
    delta = days_of(c[1])
    if delta is None:
        continue
    for m in re.finditer(r"(已过|距截止|距承诺日) `(\d+)` 天", c[2]):
        if int(m.group(2)) != abs(delta):
            bad.append((name_of(r)[:26], m.group(0), delta))
assert not bad, bad
print("天数复核：全部一致")
print("改写 %d 行 + 补入 4 行" % len(EDITED))
print("bytes", len(disk.encode("utf-8")))
