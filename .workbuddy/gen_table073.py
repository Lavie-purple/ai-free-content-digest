# -*- coding: utf-8 -*-
"""073 期：在 072 期现行 4.1/4.2 表体上做「天数带符号重算 + 行级改写 + 补入 5 行」。

纪律（055–072 沿用）：
  ① 输入取本期 md 的现行文本；② 写出后复读落盘再断言；③ 断言用逐字短语；
  ④ 全表字段数分布断言；⑤ 补入行必须带「073 期」标记；⑥ 状态列整体替换；
  ⑦ 单元格不许出现 `|`；⑧ 天数一律由基准日实算、断言带符号；
  ⑨ 状态列不写「未开始 / 已结束」；状态列里非本期期号引用 ≤ 1 处（lint R3）。
"""
import io
import re
import sys
from collections import Counter
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第073期-2026-11-19.md"
PTR = " [附录 073](details.html) |"
TODAY = date(2026, 11, 19)
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
assert len(r41) == 65, ("072 期 4.1 行数", len(r41))
assert len(r42) == 44, ("072 期 4.2 行数", len(r42))


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
        return TOK.sub(lambda m: "今日（`11/19`）为截止日", st)
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
assert "已过 `49` 天" in row and "第 `45` 期" in row and "第 `36` 天" in row, row[:200]
row = row.replace("已过 `49` 天", "已过 `50` 天").replace("第 `45` 期", "第 `46` 期").replace("第 `36` 天", "第 `37` 天")
row = row.replace("`hunyuan.tencent.com` 本期仍是 `6,894` 字节（第 `3` 期「字节 + `md5`」双同）的 `app-skeleton` 骨架屏，六项关键词各 `0` 命中。",
                  "`hunyuan.tencent.com` 本期 **`6,584` 字节**（上期记 `6,894`）—— **字节变了、仍是 `app-skeleton` 骨架屏**，六项关键词各 `0` 命中（第 `5` 期）。")
row = row.replace(" [附录 072](details.html) |", PTR)
r41[hits[0]] = row
EDITED.append("腾讯老混元(手算)")

# ---- 4.1：Hy4 flash WorkBuddy 限免
edit("Hy4 flash 限免", "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
     "🟠 **距截止 `10` 天。 限免只限 `WorkBuddy` 内的 `Hy4 flash`**；其他模型与腾讯云 `TokenHub` 不在内（`TokenHub` 是**限时 `5` 折**）。 "
     "**参数取官方口径**：`220.25B` 实测 / 激活 `11.3B` + `0.43B`（媒体 `224B` / `12B` 不再作主口径）。 "
     "**权重已于 `11/17 11:44`（北京）挂上 `HF` 三仓，24 小时读数见 4.2** —— **限免到期后能用的是权重，不是本行额度**。 "
     "同日配套：`WorkBuddy` **日活超 `1,000` 万、日均 Token 超 `100` 万亿**（腾讯 Q3 财报口径）。", r41,
     name="🟠 **腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费（**`220.25B` 实测总参（含 `64B` Engram）/ 激活 `11.3B` + `0.43B` / `1M` 上下文 · 官方口径「`11/30` 前」**）**")

# ---- 4.1：MiniMax 4K —— 已撤（收口）
edit("MiniMax 4K", "MiniMax `H3-Image` `4K` 生图限时",
     "⚪ **已结束（`11/18 00:00` 到期；本期核到已撤净）。 三个读数同时归零：`0.2261` 整页 `0` 命中、`0.2404` `0` 命中、`限时5折` `0` 命中；"
     "`4K` 价目回到 `0.4522`（文生图）/ `0.4809`（编辑 `1` 张）/ `0.5211`（编辑 `3` 张）；页 `311,607 → 305,754`（`−5,853`）。 "
     "**撤回时刻只能给区间：`11/18 18:10`（上期仍挂牌）→ `11/19 16:55`（已撤），即截止后 `18`–`41` 小时** —— 不写「约 40 小时」。 "
     "**促销文案整段摘掉、不是改日期续期**（页内 `即日起至` `0` 命中）。", r41,
     deadline="**`11/18 00:00`（北京 · 官方逐字「即日起至 2026 年 11 月 18 日 00:00」· 已过 `1` 天）**")

# ---- 4.1：Runware 4K 50%
edit("Runware 4K 50%", "`Runware` 分发层 `MiniMax H3-Image`",
     "🟠 **已过 `2` 天（`11/17` 到期）。 三条读数连续第 `2` 期不变：数组仍在（`endsAt: \"2026-11-17\"`）、卡片徽标 `0`、价目一个数没变**"
     "（`0.2261` / `0.4522` 整页 `0` 命中）—— **「账本 vs 货架」第 `13` 次实证**。 "
     "**价目不动是对的**：官方帮助文案逐字「`A sale that covers only some generations, such as 4K images, shows a badge … and leaves prices unchanged.`」"
     "→ **这类促销只有徽标能判下架**（避坑 312/315）。 数组 `22` 条里今天另有一条到期（`pruna-p-video-2-pro-replace`，`endsAt: \"2026-11-19\"`）。", r41,
     deadline="**`11/17`（官方促销数组 `endsAt: \"2026-11-17\"` 逐字 · 已过 `2` 天）**")

# ---- 4.1：Antigravity 三模型 —— 到期未执行
edit("Antigravity 三模型", "`Google Antigravity` 免费档三个第三方模型 `11/18` 移除",
     "🔴 **到期日已过 `1` 天，页面没有执行、措辞也没改。 定价页本期恢复 `200`（`183,218` 字节 / 可见文本 `12,481` 字符）："
     "免费档 `Models included` 仍列四个** —— `Gemini 3.8 Flash` / `Claude Sonnet 4.6 (thinking)` / `Claude Opus 4.6 (thinking)` / `GPT-OSS-120b`；"
     "脚注 `4` 逐字仍是 `Will be removed on November 18, 2026.`（全页该日期仅 `1` 处、未改新日期）。 "
     "**结论只到「页面口径」：三个模型仍可用，但官方自己写着要撤 —— 当「随时可能没」用，不当「承诺保留」。** 免费档仍无配额数字。", r41,
     deadline="**`11/18`（官方脚注逐字 `Will be removed on November 18, 2026.` · 已过 `1` 天 · 本期核到未执行）**")

# ---- 4.1：ERNIE 5.5
edit("ERNIE 5.5", "百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `6` 天）。 官方发布页 `11月25日前开源` 逐字仍在**（本期 `54,010` 字节，与上期逐字节相同，第 `2` 期）。 "
     "**权重仍未放**：`?author=baidu` 仍 `39` 个仓库（连续第 `16` 天 `0` 变化）。 "
     "两个 `Base` 仓 `downloads` 继续涨（`4,643` / `1,714`）、`likes` `360` / `394`。", r41)

# ---- 4.2：本期有事实的行
edit("OpenRouter 免费档", "OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **全量 `478 → 480`（`+2`，可逐条点名）；`:free` `14`（**第 `6` 天不变**）；零价 `17`；`?max_price=0` `16`。 "
     "新增 `2` 条：`google/gemini-4-neon` 与 `:batch`（`created` 北京 `11/18 21:02`，`$3`/`$15` 与 `$1.5`/`$7.5`、`1,048,576` 上下文）；**除这两条无第三条**。 "
     "`gpt-6.2` 家族仍 `8` 条、**仍无 `:free` 变体**（连续 `2` 天）。 `Ling 3.2 Flash` 的 `endpoints` **仍空（第 `7` 天）**。", r42,
     name="🟢 **OpenRouter 免费档（**官方 API 目录口径 · `480/17/14`**）**")

edit("Token 羊毛", "`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折成人民币。 第 `11` 期：页头「今天还能领」`¥1738 → ¥1737`（`−1`）、"
     "卡册 `61 → 60` 张** —— **第一次「面额与卡数同降」**（前 `10` 期从未同向）。 "
     "**该合计是动态折算值、卡册是账户态**，只记读数、不推行业趋势。 页 `477,419` 字节。", r42)

edit("Antigravity 个人免费档", "`Google Antigravity` 个人免费档",
     "🟢 **官方定价页逐字 `$0/month`（本期 `183,218` 字节，第 `3` 期恢复可读）。 免费档 `Models included` 四个**：`Gemini 3.8 Flash` + 三个第三方（`Sonnet 4.6` / `Opus 4.6` / `GPT-OSS-120b`）。 "
     "`Baseline agent quota refreshed weekly` **仍无数字**（脚注只说按方案与任务复杂度浮动）。 "
     "**072 期「首页 `JS` 壳 → 站点抓不到」的推论本期被推翻**（避坑 314）。", r42)

edit("ERNIE-Base", "百度开源 `ERNIE-5.5-Flash-Base`",
     "🟢 **`060` 期首次登记 · `FP8` 与 `BF16` 双仓库。 `FP8` `4,643`（`+233`）/ `360` 赞（`+3`）；"
     "`BF16` `1,714`（`+93`）/ `394` 赞（`0`）**。 两仓 `lastModified` 仍停 `11/05` —— **仓库没变、下载在涨**，是滚动窗口重算。", r42)

edit("Inkling", "`thinkingmachines/Inkling-2-Small` 开放权重",
     "🟢 **`Apache-2.0` · `gated: false`。 上期 `429` 限流解除，本期取到 `downloads 30,082` / `likes 552`**；`lastModified` `11/17 18:39Z`。 "
     "**不写环比**：上期无值，拿更早的 `16,918` 相减会把 `2` 天记成 `1` 天；且 `downloads` 是近 `30` 天滚动窗口（避坑 249/301）。", r42)

edit("OpenCode 免费清单", "`OpenCode` 免费模型清单",
     "🟡 **`Free models` 段仍 `12` 条**（段落逐条；`-free` 正则只得 `11`，`Big Pickle` 无后缀）。 "
     "**`GLM-5.3-Flash Free` 不在段内**，但 `Deprecated models` 表里那行（`November 18, 2026`）仍在 —— **两张表不同步**（纠错②）。 "
     "`Hy4 flash Free` **仍在**（第 `7` 天）。 页 `102,315 → 102,667`（`+352`）。", r42,
     name="🟡 **`OpenCode` 免费模型清单（`Free models` 段 `12` 条 · 弃用表留行、清单已摘）**")

edit("LongCat-2.5", "美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **已公开（069 期补登）。 `downloads 2,173 → 2,484`（`+311`）/ `likes 356 → 358`（`+2`）；`lastModified` 仍 `11/10 07:28Z`**。 "
     "四个时间点仍分开写：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`、媒体稿 `11/15 10:06Z`、**一手页无「发布日期」字段**。", r42)

edit("Hy4 开放权重", "腾讯混元 `Hy4 flash` 开放权重",
     "🟢 **（072 期补入）三仓均 `gated: false`。 开放后 `24` 小时：`downloads` `0 → 159`（主仓）/ `121`（`FP8`）/ `129`（`base`）；`likes` `136 → 269` / `8 → 20` / `9 → 21`**。 "
     "**第三方转档已出 `4` 个**：`AngelSlim/Hy4-flash-GGUF`（`744` 下载 / `37` 赞）、`TensorFold` 的 `MLX-4bit` / `8bit` 两仓、`Avifenesh` 的 `NVFP4` 一仓（后三个 `0` 下载）。 "
     "**许可是 `Apache 2.0` 派生 + `§10`**：对外做 `MaaS` 且过 `$50M` 营收或 `1` 亿 `MAU` 须另签；`§10.3` 内部使用豁免。", r42,
     name="🟢 **腾讯混元 `Hy4 flash` 开放权重（**`220.25B` 实测 · 激活 `11.3B` + `0.43B` · `1M` · `Tencent Hy License 1.0`**）**")

edit("GPT-6.2", "OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
     "🟡 **（072 期补入）发布页可用名单逐字 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 "
     "本期补核两处：`openai.com/api/pricing` `200`（`795,662` 字节）但 `gpt-6.2` 的 `2` 处命中全是推广链接（`chatgpt.com/?surface=work&model=gpt-6.2-astra-wm`）、`gpt-6.2-sol` `0` 命中 → **未进价格表**；"
     "`chatgpt.com/pricing` 仍 `000`（第 `2` 期）→ **免费档是否含 `GPT-6.2` 仍无一手**。**不写「免费用户可用/不可用」。**", r42,
     name="🟡 **OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布（**可用名单 `Plus` / `Pro` / `Enterprise` / `Edu` · **`Free` 不在名单里**）**")

# ------------------------------------------------------------ ③ 补入新行
NEW41_A = ("| 🔴 **腾讯混元 `Hy4` / `Hy4 flash` 官方 `Reddit` `AMA`（`r/LocalLLaMA` · 研发团队现场答问）** "
           "| **`11/20 08:00–10:00 PT` ＝ 北京 `11/21 00:00–02:00`（距截止 `1` 天）** "
           "| 🔴 **（073 期补入）官方在 `X` 公布：本周五 `11/20` `8–10 AM PT` 在 `r/LocalLLaMA` 办 `AMA`，研发团队与 `@ShunyuYao12` 解读 `Hy4` 与 `Hy4 flash`**；"
           "作者帖同时写明 `Hy4 flash` 已开放权重（含 `-FP8` / `-Base`、`224B` 参数 / 激活 `12B` / `1M` 上下文 —— **这是媒体口径，官方卡是 `220.25B` / 激活 `11.3B` + `0.43B`**）。 "
           "**要问「`§10` 商用条款怎么算」的，这是唯一一次公开问答窗口。** |")

idx = [k for k, r in enumerate(r41) if "腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费" in name_of(r)]
assert len(idx) == 1, idx
r41.insert(idx[0] + 1, NEW41_A)

NEW42_A = ("| 🟢 **`DeepSeek` 服务端搜索 / 网页抓取不再单独计费（**调用模型时触发的那一层免费**）** "
           "| **无截止日（计费规则变更 · `11/18 12:00` 北京起生效）** "
           "| 🟢 **（073 期补入）官方定价页逐字 `Starting 12:00 on November 18, 2026 (Beijing Time, UTC+8), the server-side search and web fetch tool calls triggered when calling the model are no longer billed`**；"
           "结果并入上下文、按 token 计。 ⚠️ **单独调 `Search` / `Fetch` API 仍 `$0.75` / 千次**（同页表格未变）；`TTS` / `ASR` 仍限时五折（`$0.45→0.225` / `$0.116→0.058`）。 "
           "**免的是「模型自己搜」，不是「你去搜」。** |")

NEW42_B = ("| ⚠️ **`DeepSeek` 应用 / 网页端限额（**`7` 天不活跃长对话不再续接 · 单次输入约 `4` 万字 · 日额度封顶**）** "
           "| **无截止日（限额生效日未公布 · 官方未给恢复时间表）** "
           "| ⚠️ **（073 期补入）`IT之家` `2026/11/16 11:44` 转述用户反馈：平台提示「算力不足，不再支持超过 7 天不活跃的长对话」，单次输入上限缩至 `4` 万字左右、每日额度有上限。 "
           "**官方三处（官网 / 状态页 / `API Docs`）本期均无对应公告** —— 只到「媒体转述」这一级，不写「官方宣布」。 "
           "同日另一侧在放宽：服务端搜索/抓取已不计费 —— **一收一放，两条都写。** |")

NEW42_C = ("| 🟢 **范式（`Phai`）`Phai-A1-35B-1M` 开放权重（**`35.1B` 全 `BF16` · `1M` · `Apache-2.0` · 底座 `Qwen3.6-35B-A3B`**）** "
           "| **无截止日（权重永久开放）** "
           "| 🟢 **（073 期补入）`HF` 仓 `PhaiModelLab/Phai-A1-35B-1M`：`createdAt 2026-11-12T08:10:51Z`、`lastModified 11-14T08:43:23Z`、`safetensors.total 35,107,181,936`、`28` 文件、`gated: false`、`downloads 9` / `likes 3`**。 "
           "**公开日比建仓日晚 `7` 天**（避坑 311 第三次实证）。 **「单卡 `3090`」需量化**：`BF16` 权重 `70.2 GB` vs 显存 `24 GB`（避坑 316）。 "
           "`Phai-M1`（视频 · `15` 秒 `720P` 约 `3` 分钟）**`HF` 未检索到仓库**，官方口径「近期上架」—— 记预告，不记已开放。 |")

NEW42_D = ("| 🟢 **`MatOS` 材料科研智能体开源（**中关村两院 · `3,135` 数据集 / `386` 技能 / `104` 工作流 / `51` 角色 / `48` 款软件**）** "
           "| **无截止日（开源）** "
           "| 🟢 **（073 期补入）`arXiv` 技术报告 + `GitHub` 代码双开源（`量子位` `2026/11/19` 一手）。** "
           "基准均在「同底座模型」前提下：`ResearchClawBench` 平均 `+33.6%`、材料任务 `+80.8%`；`MatTools` 完整问题成功率高于 `Codex CLI` / `Claude Code`；自研 `DuoCompNet` 的 `MAE` 比次优低 `13.6%`。 "
           "**开源 ≠ 免费算力**：系统与资产库可自部署，跑起来仍要自己的模型与机器。 |")

idx = [k for k, r in enumerate(r42) if "`inclusionAI` `Ling 3.2 Flash`" in name_of(r)]
assert len(idx) == 1, idx
r42.insert(idx[0], NEW42_A)
idx = [k for k, r in enumerate(r42) if "`inclusionAI` `Ling 3.2 Flash`" in name_of(r)]
assert len(idx) == 1, idx
r42.insert(idx[0], NEW42_B)
idx = [k for k, r in enumerate(r42) if "阿里 `Qwen4-Max` 发布" in name_of(r)]
assert len(idx) == 1, idx
r42.insert(idx[0], NEW42_C)
idx = [k for k, r in enumerate(r42) if "阿里 `Qwen4-Max` 发布" in name_of(r)]
assert len(idx) == 1, idx
r42.insert(idx[0], NEW42_D)


# ------------------------------------------------------------ ④ 指针重贴当期期号
def repoint(bucket):
    n = 0
    for k, r in enumerate(bucket):
        if "附录 072" in r:
            bucket[k] = r.replace("附录 072", "附录 073")
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
assert len(d41) == 66, len(d41)
assert len(d42) == 48, len(d42)
assert "073 期补入" in disk
assert "已过 `50` 天" in disk
assert "第 `46` 期" in disk
assert "已过 `2` 天（`11/17` 到期）" in disk
assert "`480/17/14`" in disk
assert "附录 072" not in disk
assert "Will be removed on November 18, 2026." in disk
assert "no longer billed" in disk

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

# 状态列里的非本期期号引用 ≤ 1 处（lint R3）
ISSUE_RE = re.compile(r"(?!073)(0\d{2})\s*期")
over = [(name_of(r)[:24], len(ISSUE_RE.findall(cells_of(r)[2]))) for r in d41 + d42
        if len(ISSUE_RE.findall(cells_of(r)[2])) >= 2]
assert not over, over
print("R3 预检：0 行超 1 处")
