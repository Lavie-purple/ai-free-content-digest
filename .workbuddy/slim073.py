# -*- coding: utf-8 -*-
"""073 期：把 13 条 R1 超长的状态列压回 200 字以内，并消掉 Phai 行的第 2 个避坑编号。

纪律（052/054）：
  · 键按「活动名唯一子串」定位，命中必须恰好 1 行；
  · 改完**回读落盘文件**再断言，不信任内存变量；
  · 被裁掉的论证**一字不删**，原文进 tmp_073_slim.json，由 appendix073.py 落进附录。
"""
import io
import json
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第073期-2026-11-19.md"
OUT = WS + ".workbuddy/tmp_073_slim.json"
DRY = "--apply" not in sys.argv

A = " [附录 073](details.html) |"

REWRITE = [
    ("腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
     "🟠 **距截止 `10` 天。 只限 `WorkBuddy` 内的 `Hy4 flash`**；`TokenHub` 是**限时 `5` 折**。 "
     "参数取官方口径 `220.25B` / 激活 `11.3B` + `0.43B`。 **权重已挂 `HF` 三仓** —— 到期后能用的是权重。" + A),

    ("腾讯混元 `Hy4` / `Hy4 flash` 官方 `Reddit` `AMA`",
     "🔴 **（073 期补入）官方 `X` 公布：`11/20` `8–10 AM PT` 在 `r/LocalLLaMA` 办 `AMA`，研发团队解读 `Hy4` / `Hy4 flash`**；"
     "帖中 `224B` / 激活 `12B` 是媒体口径（官方卡 `220.25B` / `11.3B` + `0.43B`）。 **问 `§10` 商用条款的唯一公开窗口。**" + A),

    ("MiniMax `H3-Image` `4K` 生图限时",
     "⚪ **已收口（`11/18 00:00` 到期；本期核到已撤净）。 `0.2261` / `0.2404` / `限时5折` 三串整页 `0` 命中；"
     "`4K` 价目回到 `0.4522` / `0.4809` / `0.5211`**。 撤回落在 `11/18 18:10`–`11/19 16:55` 之间（截止后 `18`–`41` 小时），**文案整段摘掉、非改日期续期**。" + A),

    ("`Runware` 分发层 `MiniMax H3-Image`",
     "🟠 **已过 `2` 天（`11/17` 到期）。 三条读数连续第 `2` 期不变：数组仍留（`endsAt: \"2026-11-17\"`）、徽标 `0`、价目没动** —— 第 `13` 次实证。 "
     "**`4K` 类促销只挂徽标、不动价目，只有徽标能判下架**（避坑 315）。 数组 `22` 条里今天另有一条到期（`pruna-p-video-2-pro-replace`）。" + A),

    ("`Google Antigravity` 免费档三个第三方模型",
     "🔴 **到期日已过 `1` 天，页面未执行、措辞未改。 定价页恢复 `200`（`183,218` 字节 / 可见文本 `12,481` 字符）、免费档仍列四个**："
     "`Gemini 3.8 Flash` + `Sonnet 4.6` / `Opus 4.6` / `GPT-OSS-120b`；脚注 `4` 仍是 `Will be removed on November 18, 2026.` **当「随时可能没」用。**" + A),

    ("OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **`478 → 480`（`+2` 可点名）；`:free` `14`（第 `6` 天）；零价 `17`；`?max_price=0` `16`。 新增 `google/gemini-4-neon` 与 `:batch`**（北京 `11/18 21:02`、`$3`/`$15`）。 "
     "`gpt-6.2` 仍 `8` 条、无 `:free`；`Ling 3.2` `endpoints` **空第 `7` 天**。" + A),

    ("`OpenCode` 免费模型清单",
     "🟡 **`Free models` 段仍 `12` 条**（正则只得 `11`，`Big Pickle` 无后缀）。 **`GLM-5.3-Flash Free` 不在段内、弃用表那行仍在 —— 两张表不同步**（纠错②）。 "
     "`Hy4 flash Free` 仍在（第 `7` 天）。 页 `+352`。" + A),

    ("`Google Antigravity` 个人免费档",
     "🟢 **官方逐字 `$0/month`（本期 `183,218` 字节，第 `3` 期恢复）。 免费档四个模型**：`Gemini 3.8 Flash` + `Sonnet 4.6` / `Opus 4.6` / `GPT-OSS-120b`。 "
     "**`Baseline agent quota refreshed weekly` 仍无数字。**" + A),

    ("腾讯混元 `Hy4 flash` 开放权重",
     "🟢 **（072 期补入）24 小时：`downloads` `0 → 159` / `121` / `129`；`likes` `136 → 269`**。 **第三方转档 `4` 个**："
     "`AngelSlim` `GGUF`、`TensorFold` `MLX` 两仓、`Avifenesh` `NVFP4`。 **`Apache 2.0` + `§10`**：对外 `MaaS` 且过 `$50M` / `1` 亿 `MAU` 须另签。" + A),

    ("范式（`Phai`）`Phai-A1-35B-1M` 开放权重",
     "🟢 **（073 期补入）`createdAt 11-12T08:10:51Z`（比公开日早 `7` 天）、`35,107,181,936` 全 `BF16`、`apache-2.0`、`28` 文件、`gated: false`、`downloads 9`**。 "
     "**「单卡 `3090`」须量化：`BF16` `70.2 GB` vs `24 GB` 显存**（避坑 316）。 `Phai-M1` 仓未检索到，记预告。" + A),

    ("`MatOS` 材料科研智能体开源",
     "🟢 **（073 期补入）`arXiv` + `GitHub` 双开源**（`量子位` `11/19` 一手）。 基准均在同底座前提下：`ResearchClawBench` `+33.6%`、材料任务 `+80.8%`；`DuoCompNet` `MAE` 低 `13.6%`。 **开源 ≠ 免费算力。**" + A),

    ("OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
     "🟡 **（072 期补入）可用名单 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 本期补核：`/api/pricing` 的 `2` 处 `gpt-6.2` 全是推广链接、非价格行；`chatgpt.com/pricing` 仍 `000`** → "
     "**免费档是否含 `GPT-6.2` 仍无一手，不写「可用/不可用」。**" + A),

    ("`DeepSeek` 服务端搜索 / 网页抓取不再单独计费",
     "🟢 **（073 期补入）官方逐字 `Starting 12:00 on November 18, 2026 … server-side search and web fetch … are no longer billed`**；结果并入上下文按 token 计。 "
     "⚠️ **单独调 `Search` / `Fetch` API 仍 `$0.75` / 千次**（同页表未变）。 **免的是「模型自己搜」。**" + A),
]

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")


def cells(r):
    return [c.strip() for c in r.strip().strip("|").split("|")]


def ns(s):
    return len("".join(re.sub(r"\[[^\]]*\]\([^)]*\)", "", s).split()))


lines = md.split("\n")
saved = []
for pref, new in REWRITE:
    hits = [k for k, l in enumerate(lines) if l.startswith("|") and l.count("|") >= 3 and pref in cells(l)[0]]
    assert len(hits) == 1, ("命中数不是 1", pref, len(hits))
    k = hits[0]
    c = cells(lines[k])
    assert len(c) == 3, (pref, len(c))
    before, after = ns(c[2]), ns(new)
    assert after <= 200, ("压完仍超长", pref, after)
    assert after < before, ("没有变短", pref, before, after)
    saved.append({"name": c[0], "old": c[2], "new": new, "before": before, "after": after})
    lines[k] = "|%s| %s | %s" % (c[0], c[1], new)

print("压缩条数 =", len(saved))
for it in saved:
    print("  %3d → %3d  %s" % (it["before"], it["after"], it["name"][:34]))

if DRY:
    print("DRY RUN —— 未写盘")
    sys.exit(0)

io.open(OUT, "w", encoding="utf-8").write(json.dumps(saved, ensure_ascii=False, indent=1))
io.open(MD, "w", encoding="utf-8", newline="\n").write("\n".join(lines))

# 回读落盘文件再断言
disk = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
bad = [it["name"][:24] for it in saved if it["new"] not in disk]
assert not bad, bad
over = []
for l in disk.split("\n"):
    if l.startswith("|") and l.count("|") >= 3 and not l.startswith("| 活动 |") and not l.startswith("| --- |"):
        c = cells(l)
        if len(c) == 3 and ns(c[2]) > 200:
            over.append((ns(c[2]), c[0][:30]))
assert not over, over
print("落盘复核：%d 条全部命中新文本；状态列 > 200 字 = 0" % len(saved))
