# -*- coding: utf-8 -*-
"""071 期：在 070 期现行 4.1/4.2 表体上做「天数带符号重算 + 行级改写 + 补入 2+2 行」。

纪律（055–070 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 补入行必须带「071 期」标记；⑥ 状态列整体替换；
  ⑦ 单元格不许出现 `|`；⑧ 天数一律由基准日实算、**断言带符号**；
  ⑨ 状态列不写「未开始 / 已结束」（会污染 classify()）。
"""
import io
import re
import sys
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第071期-2026-11-17.md"
PTR = " [附录 071](details.html) |"
TODAY = date(2026, 11, 17)
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
assert len(r41) == 63, ("070 期 4.1 行数", len(r41))
assert len(r42) == 40, ("070 期 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "%s `%d` 天" % (m.group(1) if m.group(1) != "距今" else "距今", delta), st)
    if delta == 0:
        return TOK.sub(lambda m: "今日（`11/17`）为截止日", st)
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
        elif delta == 0:
            new_dl = re.sub(r"今日\s*`11/16`\s*到期", "今日 `11/17` 到期", new_dl)
        if new_st != c[2] or new_dl != c[1]:
            bucket[k] = "|" + "|".join([c[0], new_dl, new_st]) + "|"
            changed += 1
print("天数改写行数 =", changed, "｜无日期可算 =", len(skipped), skipped)


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
assert "已过 `47` 天" in row and "第 `43` 期" in row and "第 `34` 天" in row, row[:200]
row = row.replace("已过 `47` 天", "已过 `48` 天").replace("第 `43` 期", "第 `44` 期").replace("第 `34` 天", "第 `35` 天")
row = row.replace("`6,894` 字节", "`6,894` 字节（第 `2` 期「字节 + `md5`」双同）")
row = row.replace(" [附录 070](details.html) |", PTR)
r41[hits[0]] = row
EDITED.append("腾讯老混元(手算)")

# ---- 4.1 本期有事实的行
edit("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
     "🟠 **距截止 `1` 天（`11/18 00:00` 北京时间，实剩约 `6` 小时）。 （067 期补入）`4K` 单张 `0.4522 → 0.2261` 元**仍在（各 `2` 处）；"
     "`1K` `0.1430` / `2K` `0.1531` **不打折**。 本期页面 `311,291` 字节（上期 `311,690`，**`−399`**），"
     "**价格与门槛句均未变** —— 但 070 期抓取件已清理，**无同源快照、本期不做逐行 diff**（如实留白）。 "
     "⚠️ 折的是按张单价、不是额度；要求 ≥ `1660` 万像素。", r41)

edit("Runware 4K 50%", "`Runware` 分发层 `MiniMax H3-Image`",
     "🟠 **今日到期（`11/17` · 官方促销数组 `endsAt: \"2026-11-17\"`）。 （070 期补入）三条同验：数组在、卡片徽标在（两型号各一处）、官方价目 `0.2261` 在** —— "
     "**「三方一致」的第一次干净样本**。 只作用于 `4K`（≥ `1660` 万像素）图；`MiniMax` 侧截止是 `11/18 00:00` 北京（**时刻**），"
     "`Runware` 侧是 `11/17`（**日粒度**）—— **两个都写、不换算**。 **折扣不是免费额度。**", r41)

edit("Runware 30%", "`Runware` 分发层 `MiniMax H3 Max` 促销 `30% OFF`",
     "⚪ **已过 `2` 天（`11/15` 到期）。 （069 期补入）数组里 `minimax-h3-max-november-promo` **仍在**（`endsAt: \"2026-11-15\"`），卡片徽标自 070 期卸下后**未挂回** —— "
     "**「数组是账本、卡片是货架」连续第 `2` 次双读**（避坑 303）。 本期数组 `20 → 22` 条，**其中 `13` 条早于今日** —— "
     "「数组里还有」在任何时点都不等于「在售」。", r41)

edit("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `8` 天）。 （066 期补入）官方发布页 `11月25日前开源` 逐字仍在**（本期 `54,010` 字节，与上期逐字节相同）。 "
     "**权重仍未放**：`?author=baidu` 本期仍 `39` 个仓库（连续第 `14` 天 `0` 变化）。 "
     "两个 `Base` 仓 `downloads` **本期解冻**（`3,914 → 4,145` / `1,388 → 1,481`）、`likes` `355` / `394`。", r41)

edit("48 号公告", "商务部 / 科技部 2026 年第 48 号公告",
     "🟡 **已过 `2` 天（`11/15` 征求意见截止，未见延长公告）**；登记实施日「未公布」（自公布之日起）。 "
     "本条只记日期，不对条款内容下判断。", r41,
     deadline="**`11/15`（征求意见截止 · 已过 `2` 天）；登记实施日「未公布」（自公告发布日起至目录正式修订实施日止）**")

edit("Gemini 4 Argon", "Google `Gemini 4 Argon`",
     "🟠 **距截止 `13` 天（官方口径「11 月底」：首发优惠价到期）。 本期未见官方改口径。", r41)

edit("Google AI Plus", "Google AI Plus 失去 Pro 模型选择权",
     "🟠 **已过 `4` 天（`11/13` 生效）。", r41)

edit("Fable 5.2", "Anthropic `Claude Fable 5.2`",
     "🟠 **今日已到期（`11/17 15:59` 北京 · 官方逐字 `11/16 23:59 PT`）。** 本期 `claude.com/pricing` 字节 `1,344,780`（上期 `1,344,079`，**`+701`**）、"
     "`md5` 仍随 `CSP nonce` 变；**定价页本期未见「`Fable` 一周」促销字样**（`November` 仅 `1` 处，是 `Enterprise` 的 `11/20` 默认开启说明）。 "
     "⚠️ 两期之间未逐字对比该段，**不作「促销已撤」的因果判断**。", r41,
     deadline="**`11/17 15:59`（北京 · 官方逐字 `11/16 23:59 PT`：`Pro` / `Team` 标准席位含 `Fable` 一周 · **今日已到期**）；`2027-03-08 23:59 PT`（`Max` / `Ultra` / 高级席位的 `1–3` 次 `Fable` 重置到期）**")

edit("Runware upscale", "`Runware` 分发层 `pruna-p-video-upscale` 促销",
     "🟢 **已过 `9` 天（`11/8` 到期）。 促销数组本期 `22` 条、日期集合逐项相同；"
     "**「数组里还在 ≠ 在售」第 `10` 次实证**（`11/15` / `11/17` / `11/19` / `11/23` ×2 / `11/30` / `12/31` 未到期）。", r41)

# ---- 4.2 本期有事实的行
edit("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **全量 `468 → 470`（`+2`）；`:free` `14`（**第 `4` 天不变**）；零价 `17`；`?max_price=0` `16`。 "
     "**增量只能指名 `1` 条**：`tencent/hy4-flash`（`created` 北京 `11/16 22:18`）；另一条为「下架后重上架」，`created` 是旧的、**目录无逐日快照，指名不了、本期留白**。 "
     "`Ling 3.2 Flash` 的 `endpoints` **空 `4` 天**（`404` 已变 `200`：模型页有了、端点仍 `[]`）。", r42,
     name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `470/17/14`**）**")

edit("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `9` 期：页头「今天还能领」`¥1760 → ¥1758`（`−2`）、"
     "卡册 `60 → 61` 张、日戳合计 `122`（`11/17` `2` / `11/16` `28` / `11/15` `18` / `11/14` `70` / `11/13` `2` / `11/9` `2`）。 "
     "**「面额微降、卡数微增」是第六种形状**；`11/16` 那 `28` 次里含 `Hy4` 卡的 `11月16日核实`（**聚合层核实日未刷新**）。 只记读数、不推规律。", r42)

edit("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
     "🟢 **官方定价页逐字 `$0/month`。 免费档第一次列出模型清单**：`Gemini 3.8 Flash` / `Claude Sonnet 4.6（thinking）` / `Claude Opus 4.6（thinking）` / `GPT-OSS-120b`；"
     "**后三个角标 `title` 逐字 `Will be removed on November 18, 2026.`**（单列一行见 4.1）。 "
     "`Unlimited Tab` / `Unlimited Command` / `Basic weekly rate limits` **三串整页 `0` 命中**，改为 `Baseline agent quota refreshed weekly`（**仍无数字**）；"
     "页 `214,361 → 178,404` 字节。 企业侧新增席位制（`$30/seat/月`）。 ⚠️ 首页本期 `000`，**「双同」观测中断**。", r42)

edit("ERNIE-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓库。 `FP8` `4,145`（`+231`）/ `355` 赞（`+31`）；"
     "`BF16` `1,481`（`+93`）/ `394` 赞（`0`）** —— 两仓 `downloads` 本期**同时解冻**（上期五个仓逐字不动）。 "
     "`LICENSE` `25,619` 字节连续第 `12` 天不变；两仓 `lastModified` 仍停 `11/05`。", r42)

edit("Inkling", "`thinkingmachines/Inkling-2-Small` 开放权重",
     "🟢 **`Apache-2.0` · `gated: false`。 `downloads 7,329 → 16,918`（**`+9,589`，一天翻倍多**）/ `likes 363 → 429`（`+66`）；"
     "`MXFP8` 变体另计；`lastModified 11/15 05:54Z` 未再动。 **`downloads` 是「近 `30` 天滚动窗口」、且中间停更快照至少 `3` 天 → 只记「窗口涨了」，不记「今天涨了多少」**（避坑 301）。", r42)

edit("OpenCode 免费清单", "`OpenCode` 免费模型清单 10 → 11",
     "🟡 **`-free` `id` `15 → 14`（同口径正则复扫）**：撤 `minimax-m3.1-flash-free`（页内 `m3.1` **`0` 命中**）、`hy4-flash-free` **仍在**。 "
     "页面 `98,592 → 98,080`（**`−512`**），**删块只掉几百字节、`diff` 里没有一行像「删除」** —— **撤项靠 `id` 清单、不靠字节数**（避坑 308）。 "
     "⚠️ 070 期「只进不出」的隐含假设本期推翻。", r42)

edit("Praxis", "Runway `Praxis-1` 开放权重",
     "🟢 **（068 期补登）`Apache-2.0` · `27B` 混合专家扩散 Transformer。 本期 `GitHub` `stars 105 → 111 → 115`（`+4`）、"
     "**`pushed_at` 更新为 `11/16 19:07:26Z`**（上期停 `11/12 22:14Z`，停推 `4` 天后首次推送）。 `HF` 单仓 `praxis-1-base` 本期未取到。", r42)

edit("PEAR", "MIT 韩松团队 `PEAR`",
     "🟢 **已公开（069 期补登）。 `GitHub` `stars 442 → 574`（`+132`）、`forks 32 → 36`、`open_issues 3`；"
     "`pushed_at` 仍 `11/16 07:54:56Z`、`updated_at 11/17 09:40:50Z`**。 **那一次推送查清了：commit `d604856a`「`[docs] fix: the README's Paper link points to the paper on arXiv (#3)`」—— 改的是文档链接，不是代码**（观测点 `#12` 的答案）。 "
     "`LICENSE` 原文 `11,544` 字节已读（`Apache-2.0`）；`LIBERO` `1.6% → 74.4%`；真机 `YAM` `30` 试成 `18`；**未见到第三方复现 `74.4%`**。", r42)

edit("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **已公开（069 期补登）。 `downloads 1,573 → 1,850`（`+277`）/ `likes 289 → 353`（`+64`）；`lastModified` 仍 `11/10 07:28Z`；"
     "`?author=meituan-longcat` 仍 `32` 仓。 四个时间点仍分开写：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`、媒体稿 `11/15 10:06Z`、**一手页无「发布日期」字段**。", r42)

edit("Qwen4-Max", "阿里 `Qwen4-Max` 发布",
     "🟡 **（070 期补入）**付费**模型 —— 官方博客 `free` / `免费` `0` 命中**，只写「可在 `QwenWork` / `Qoder` / `QwenStudio` 使用」。 "
     "**本期补两条**：① `?author=Qwen` 无 `Qwen4` 仓（`200` 条上限内 `0` 命中）→ **「小尺寸将开源」仍无落地**；"
     "② `OpenRouter` 端点价 `$1.425` / `$4.275` / 缓存 `$0.07125` ＝ 官方价的 `0.95` 倍，且 `discount: 0` → **两套报价并排写、不合并**（纠错④）。", r42)


# ------------------------------------------------------------ ③ 补入新行
NEW41_A = ("| 🟠 **智谱 `AutoClaw` 国内站 `M11W3` 每周福利：登录领 **`100M`** Tokens（**本周额度是上周同类活动的 `2` 倍**）** "
           "| **`11/22 23:59`（北京时间 · 官方逐字「活动时间 11 月 16 日（周一）00:00—11 月 22 日（周日）23:59」；奖励同日 `23:59` 失效 · 距截止 `5` 天）** "
           "| 🟠 **距截止 `5` 天。 （071 期补入）官方逐字「登录 AutoClaw，即可领取 `100M Tokens`（相当于 `10,000` 积分），每个账号限领一次」**；`100M` ＝ 中文常说的「`1` 亿」。 "
           "**只在 `AutoClaw` 内使用**，自接 `Coding Plan` 或模型 API 另行计费；内置 `GLM-5.3` / `GLM-5-Turbo` / `GLM-5V-Turbo` / `Auto`。 "
           "**额度是周变量**：`M11W1` `50M` → 双十一档 `50M` → 本周 `100M`，**不可跨周相减**（避坑 306）。 同站 `2.2.0` 升级礼 `5,000` 积分（约 `5,000` 万 tokens、发放后 `7` 天有效）**门槛不同、不进本行**。 |")

idx = [k for k, r in enumerate(r41) if "智谱 `AutoClaw` 国内站 `M10W4`" in name_of(r)]
assert len(idx) == 1, idx
r41.insert(idx[0], NEW41_A)

NEW41_B = ("| 🟠 **`Google Antigravity` 免费档三个第三方模型 `11/18` 移除（`Claude Sonnet 4.6` / `Claude Opus 4.6` / `GPT-OSS-120b`）** "
           "| **`11/18`（官方角标 `title` 逐字 `Will be removed on November 18, 2026.` · 正文无此句 · 距截止 `1` 天）** "
           "| 🟠 **距截止 `1` 天。 （071 期新增观测位）三个模型名后的 `<a title>` 逐字「Will be removed on November 18, 2026.」，可见文本只有一个 `4`**（避坑 305）。 "
           "移除后免费档只剩 `Gemini 3.8 Flash`。 同日整页 `214,361 → 178,404` 字节（`−35,957`）；070 期引过的 `Unlimited Tab` / `Unlimited Command` / `Basic weekly rate limits` **三串整页 `0` 命中**，"
           "改为 `Baseline agent quota refreshed weekly`（**仍无数字**）。 **降档三样只有「模型」有日期，上下文与额度两期都无数字。** |")

idx = [k for k, r in enumerate(r41) if "`Google Antigravity` 科研 / 安全 6 个月免费档" in name_of(r)]
assert len(idx) == 1, idx
r41.insert(idx[0], NEW41_B)

NEW42_A = ("| 🟡 **OpenAI `ChatGPT for Academic Researchers` 扩容至最多 `20` 万研究者（**本轮 `50,000` 个名额 · 每名额带 `2` 名协作者**）** "
           "| **无截止日（名额制：`11/23` 开放申请、先到先得；官方未给申请关闭日）** "
           "| 🟡 **（071 期补入）名额 `3` 个数不可互换**：`20` 万＝项目总目标、`5` 万＝本轮新增、`15` 万＝本轮可覆盖人数（`5` 万 × `3`）。 "
           "**档位从 `Pro` 降到 `Plus`**（官方逐字「`most participants would have stayed within ChatGPT Plus usage limits`」）；**可用模型只写「`frontier models`」、额度无数字**。 "
           "试点 `20,000` 人 / `33` 国（7 月起）；**由抽签改为先到先得**。 默认不用于训练（`by default`，留口子）。 |")

idx2 = [k for k, r in enumerate(r42) if "阿里 `Qwen4-Max` 发布" in name_of(r)]
assert len(idx2) == 1, idx2
r42.insert(idx2[0], NEW42_A)

NEW42_B = ("| 🟡 **腾讯 `Hy4 flash` 进入 `OpenRouter` 目录（**`tencent/hy4-flash` · 标价 ≈ 官方人民币价五折 · **付费**）** "
           "| **无截止日（目录标价，未挂 `discount`、无 `:free` 变体）** "
           "| 🟡 **（071 期补入）`created` 换北京 `11/16 22:18`**（晚于 070 期截止 `17:50`）。 标价：输入 `$0.035` / 输出 `$0.1405`（每百万 token）；"
           "**按 `7.1` 折算，正好是官方 `0.5` 元 / `2` 元的一半** → **`TokenHub` 的 `5` 折被写进标价**，不是促销字段（避坑 307）。 **汇率 `7.1` 是本报假设**，官方未给换算口径。 |")

idx2 = [k for k, r in enumerate(r42) if "`inclusionAI` `Ling 3.2 Flash`" in name_of(r)]
assert len(idx2) == 1, idx2
r42.insert(idx2[0], NEW42_B)


# ------------------------------------------------------------ ④ 指针重贴当期期号
def repoint(bucket):
    n = 0
    for k, r in enumerate(bucket):
        if "附录 070" in r:
            bucket[k] = r.replace("附录 070", "附录 071")
            n += 1
    return n


print("指针重贴：4.1", repoint(r41), "4.2", repoint(r42))
print("改写行：", len(EDITED), EDITED)
print("输出行数：4.1 = %d，4.2 = %d" % (len(r41), len(r42)))
if DRY:
    print("41 样本", r41[1][:300])
    print("42 样本", r42[2][:300])
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
assert len(d42) == 42, len(d42)
assert "071 期补入" in disk
assert "M11W3" in disk
assert "Will be removed on November 18, 2026" in disk
assert "已过 `48` 天" in disk
assert "第 `44` 期" in disk

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
