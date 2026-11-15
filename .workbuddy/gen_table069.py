# -*- coding: utf-8 -*-
"""069 期：在 068 期现行 4.1/4.2 表体上做「天数带符号重算 + 行级改写 + 补入 1+2 行」。

纪律（055–068 沿用 + 069 新增）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 补入行必须带「069 期」标记；⑥ 状态列整体替换；
  ⑦ 单元格不许出现 `|`；⑧ 天数一律由基准日实算；
  ⑨ **069 期新立（纠错①）**：`delta < 0` 必须写「已过 N 天」、`delta > 0` 写「距截止 N 天」，
     **断言带符号比对** —— 068 期用 `abs(delta)` 让「过期」写成了「距截止」而断言照样通过。
"""
import io
import re
import sys
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第069期-2026-11-15.md"
PTR = " [附录 069](details.html) |"
TODAY = date(2026, 11, 15)
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
assert len(r41) == 60, ("068 期 4.1 行数", len(r41))
assert len(r42) == 37, ("068 期 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "今日（`11/15`）为截止日" if m.group(1) != "距今" else "今日（`11/15`）", st)
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
        # 截止列里冻结的「已过 N 天」也按新基准日重算
        newdl = c[1]
        if delta < 0:
            newdl = re.sub(r"已过\s*`?\d+`?\s*天", "已过 `%d` 天" % (-delta), newdl)
        elif delta == 0:
            newdl = re.sub(r"（\s*已过\s*`?\d+`?\s*天\s*）", "（今日 `11/15` 到期）", newdl)
        if new != st or newdl != c[1]:
            c[2] = new
            c[1] = newdl
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


# 4.1 本期有事实的行
edit("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `10` 天）。 （066 期补入）官方发布页 `限时` / `免费` 各 `0` 命中**；"
     "`11月25日前开源` 逐字仍在。 **权重仍未放**：`?author=baidu` 本期仍 `39` 个仓库（`0` 变化）、"
     "`ERNIE-5.5-Flash-Preview` 仓 `0` 命中；`OpenRouter` 的 `:free` 条目仍在（本条未撤）。", r41)

edit("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时 `5` 折",
     "🟠 **生效中（距截止 `3` 天）。 （067 期补入）`4K` 单张 `0.4522 → 0.2261` 元；`1K` `0.1430` / `2K` `0.1531` **不打折**。 "
     "本期页面 `311,690` 字节**与上期完全相同**、`md5 9be85044 → 3f0a6240`（不同）、**可见文本逐行 `0` 差异** —— "
     "`511` 个字节位全落在构建产物哈希上。 **`md5` 不同 ≠ 内容变了**（避坑 300）。 ⚠️ 折的是按张单价、不是额度；要求 ≥ `1660` 万像素。", r41)

edit("Antigravity 6mo", "`Google Antigravity` 科研 / 安全 6 个月免费档",
     "🟡 **以申请通过为准（相对日期：官方逐字 `free of charge for 6 months`，未给统一截止日）。 "
     "⚠️ 本期 `antigravity.google` 首页与 `/pricing` **`md5` 与上期逐字节相同**（`214,361` / `ad05c63b`、`140,014` / `0bcaffdb`，第 `4` 期同值），"
     "个人档 `$0/month` 仍在、含 `Basic weekly rate limits`；**`free` 整页 `0` 命中**。", r41)

edit("腾讯轻量云", "腾讯轻量云专家限量",
     "🟢 **已过 `2` 天（`11/13` 到期，官方未给延长口径）。", r41)

edit("48 号公告", "商务部 / 科技部 2026 年第 48 号公告",
     "🟡 **今日（`11/15`）为征求意见截止日**；登记实施日「未公布」（自公布之日起）。 "
     "本条只记日期，不对条款内容下判断。", r41)

edit("Gemini 4 Argon", "Google `Gemini 4 Argon`",
     "🟠 **距截止 `15` 天（官方口径「11 月底」：首发优惠价到期）。 本期未见官方改口径。", r41)

edit("Google AI Plus", "Google AI Plus 失去 Pro 模型选择权",
     "🟠 **已过 `2` 天（`11/13` 生效，067 期写「今日为截止日」，按实算改为「已过 `2` 天」）。", r41)

edit("Fable 5.2", "Anthropic `Claude Fable 5.2` / `Mythos 5.2` 发布优惠",
     "🟢 **距截止 `1` 天（`11/16 23:59 PT`）。 本期 `claude.com/pricing` 字节数 `1,344,079` **与上期完全相同**、"
     "`md5` 不同（`CSP nonce` 每次请求都变）、可见文本逐行 `0` 差异；优惠口径未改。", r41)

edit("Runware pruna-video-upscale", "`Runware` 分发层 `pruna-p-video-upscale` 促销",
     "🟢 **已过 `7` 天（`11/8` 到期）。 促销数组本期 `endsAt` 仍 `20` 处、日期集合逐项相同；"
     "**「数组里还在 ≠ 在售」第 `8` 次实证**（`11/15` / `11/17` / `11/19` / `11/30` 四条仍未到期）。", r41)

# 4.2 本期有事实的行
edit("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **全量 `471 → 470`（`−1`）；`:free` `14 → 14`；零价 `17 → 17`；`?max_price=0` `16 → 16`。 "
     "**进 `0` 出 `1`**：出的是 `z-ai/glm-5.2:batch` —— **一个 `:batch` 变体，`glm-5.2` 本体仍在、价未变**。 "
     "`Ling 3.2 Flash` 的 `endpoints` **第 `2` 天仍为 `[]`**、`inclusionAI/Ling-3.2-flash` **仍 `404`**。", r42)

edit("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `7` 期：页头「今天还能领」`¥1599 → ¥2433`（`+834`）、"
     "卡册 `59 → 62` 张、日戳 `11/14` `108` / `11/15` `6` / `11/13` `2` / `11/9` `4` / `11/8` `4` ＝ `124`。 "
     "**`11/14` 的 `108` 次日一个没动**（前三次分别是 `4→80`、`12→2`、`108`）—— 四次形状全不同，本报只记读数、不推规律。", r42)

edit("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
     "🟢 **官方定价页逐字 `$0/month`。 含 `Unlimited Tab` / `Unlimited Command` / **`Basic weekly rate limits`**；"
     "`free` / `Free` 整页各 `0` 命中（免费只用 `$0` 表达）；额度仍无具体数字。 "
     "本期整页 `md5` **与上期逐字节相同** —— 第 `4` 期同值，横幅「`Gemini 4 Hydrogen and Orchestrator now in Google Antigravity`」一字未动、**不写档位**。", r42)

edit("ERNIE-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓库。 本期 `FP8` `3,914` 下载 / `317` 赞（`+542` / `+9`）、"
     "`BF16` `1,388` / `392`（`+231` / `+1`）；`LICENSE` `25,619` 字节连续第 `10` 天不变；两个仓库 `lastModified` 仍停 `11/05`。", r42)

edit("Ripple", "`Ripple-65B Preview` 开放权重",
     "🟢 **`061` 期补登 · 仓库建于 `11/4`。 本期 `downloads 10,675` / `likes 584`（`+2,175` / `+2`）；`lastModified` 未动（`11/10`）。", r42)

edit("Inkling", "`thinkingmachines/Inkling-2-Small` 开放权重",
     "🟢 **`Apache-2.0` · `gated: false` · `36` 个文件。 本期 `downloads 1,064 → 7,329`（`6.3` 倍）/ `likes 280 → 327`；"
     "`MXFP8` 变体 `221 → 638` / `12 → 13`，`lastModified 11/15 05:56 UTC`（北京 `13:56`，落在本期窗口内）。 "
     "**两日曲线 `12 → 1,064 → 7,329`**：增速从 `86` 倍降到 `6.3` 倍，方向不变。", r42)

edit("OpenCode 免费清单", "`OpenCode` 免费模型清单",
     "🟡 **免费清单 `13` 条 `-free` ID 不变（含 `longcat-2.5-free`）**。 本期 `opencode.ai/docs/zen` "
     "`98,175` 字节 / `md5 2a3bb097` 与上期**逐字节相同** —— **第 `6` 期冻结**。", r42)

edit("Praxis", "Runway `Praxis-1` 开放权重",
     "🟢 **（068 期补登）`Apache-2.0` · `27B` 混合专家扩散 Transformer · 权重 + 推理 + 微调代码。 "
     "本期 `HF` 单仓 `praxis-1-base` `155` 下载 / `10` 赞；`GitHub` `stars 103 → 105`、`pushed_at` 仍停 `11/12 22:14 UTC`。 "
     "**「权重公开」与「社区用起来」之间仍有距离**（与 `PEAR` 同型）。", r42)


# ------------------------------------------------------------ ③ 补入新行
NEW41_1 = ("| 🔴 **`Runware` 分发层 `MiniMax H3 Max` 促销 `30% OFF`（**官方 `pricing` 页促销数组逐字 `30% off all generations until November 15, 2026`**）** "
           "| **`11/15`（官方促销数组 `endsAt: \"2026-11-15\"` 逐字）—— **今日为截止日**）** "
           "| 🔴 **今日（`11/15`）为截止日。 （069 期补入）作用于 `minimax-h3-max` / `h3-max-turbo` 的**按次单价**；"
           "挂在 `Runware`（分发商）页面上，**与 `MiniMax` 官方定价页是两套价格体系**。 **折扣不是免费额度。** |")

idx = [k for k, r in enumerate(r41) if "`Runware` 分发层 `pruna-p-video-upscale`" in name_of(r)]
assert len(idx) == 1, idx
r41.insert(idx[0] + 1, NEW41_1)

NEW42_1 = ("| 🟢 **美团 `LongCat-2.5` 以 `MIT` 公开权重（**`1.6T` 总参 / `48B` 激活 · `1M` 上下文 · 文本 + 图 + 视频 · `231` 个文件**）** "
           "| **无截止日（开放权重，官方未给回收 / 下线日）** "
           "| 🟢 **（069 期补登）`cardData.license = mit`、`gated: false`、两个仓各 `231` 个文件；`downloads 1,573` / `likes 267`（`W4A4` 仓 `487` / `3`）。 "
           "`Terminal Bench v2.1` `88.4` / `v4.0` `38.5` / `DeepSWE` `64.6`（**官方自测**）；样例部署 `194` 张华为昇腾 `Atlas A2`、**无 `Nvidia` 指引**。 "
           "**四个时间点分开写**：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`（065 期窗口内）、媒体稿 `11/15 10:06Z`、**一手页无「发布日期」字段** —— 本报只写「已公开」。 |")

NEW42_2 = ("| 🟢 **MIT 韩松团队 `PEAR` 开放权重 + 代码（**`Qwen3.8-27B` + 仿真 RL · `Apache-2.0` · `5090` 上 `220+` tok/s**）** "
           "| **无截止日（开放权重，官方未给回收 / 下线日）** "
           "| 🟢 **（069 期补登）`GitHub` `mit-han-lab/pear` 建仓 `11/13 17:43:06Z`、`pushed_at 17:43:22Z`（相隔 `16` 秒）、`stars 240`、`spdx_id Apache-2.0`；"
           "`LICENSE` 原文 `11,544` 字节已读（Apache 2.0）。 `HF` 集合三条：`Qwen3.8-27B-PEAR`（`27.36B`）/ `-LIBERO_only` / `-NVFP4`（`18.16B`）。 "
           "`LIBERO` 零样本 `1.6% → 74.4%`；真机 `YAM` `30` 次成功 `18` 次（训练前 `0`）；**不用遥操数据、不用真机数据**。 **时间点 `11/14 01:43` 北京，落在 068 期窗口内。** |")

idx2 = [k for k, r in enumerate(r42) if "`thinkingmachines/Inkling-2-Small` 开放权重" in name_of(r)]
assert len(idx2) == 1, idx2
r42.insert(idx2[0] + 1, NEW42_2)
r42.insert(idx2[0] + 1, NEW42_1)


# ------------------------------------------------------------ ④ 指针重贴当期期号
def repoint(bucket):
    n = 0
    for k, r in enumerate(bucket):
        if "附录 068" in r:
            bucket[k] = r.replace("附录 068", "附录 069")
            n += 1
    return n


print("指针重贴：4.1", repoint(r41), "4.2", repoint(r42))

print("改写行：", len(EDITED), EDITED)
print("输出行数：4.1 = %d，4.2 = %d" % (len(r41), len(r42)))
if DRY:
    for tag, prefix in (("41 样本", r41[1]), ("42 样本", r42[3])):
        print(tag, prefix[:400])
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
assert len(d41) == 61, len(d41)
assert len(d42) == 39, len(d42)
assert "069 期补入" in disk and "069 期补登" in disk
assert "`z-ai/glm-5.2:batch`" in disk
assert "`11/14` 的 `108` 次日一个没动" in disk

dist = Counter(len(cells_of(r)) for r in d41 + d42)
print("字段数分布：", dict(dist))
assert set(dist) == {3}, dist

# 天数复核：带符号比对（069 期纠错①）
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

# 方向复核：截止列说过期、状态列不许说「距截止」
conflict = []
for r in d41 + d42:
    c = cells_of(r)
    if "已过" in c[1] and re.search(r"距截止\s*`\d+`\s*天", c[2]):
        conflict.append(name_of(r)[:26])
assert not conflict, conflict
print("方向复核：0 行矛盾")
