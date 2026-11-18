# -*- coding: utf-8 -*-
"""072 期：把 11 条 R1 超长的状态列压回 200 字以内。

纪律（052/054）：
  · 键按「活动名唯一子串」定位，命中必须恰好 1 行；
  · 改完**回读落盘文件**再断言，不信任内存变量；
  · 被裁掉的论证**一字不删**，原文进 tmp_072_slim.json，由 appendix072.py 落进附录。
"""
import io
import json
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第072期-2026-11-18.md"
OUT = WS + ".workbuddy/tmp_072_slim.json"
DRY = "--apply" not in sys.argv

A = " [附录 072](details.html) |"

REWRITE = [
    ("腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
     "🟠 **距截止 `11` 天。 限免只限 `WorkBuddy` 内的 `Hy4 flash`**；`TokenHub` 是**限时 `5` 折**。 "
     "**参数改为官方口径**：`220.25B` / 激活 `11.3B` + `0.43B`（媒体 `224B` / `12B` 不再作主口径）。 "
     "**权重已挂 `HF` 三仓** —— 限免到期后能用的是权重，不是本行额度。" + A),

    ("MiniMax `H3-Image` `4K` 生图限时",
     "🔴 **官方写的截止时刻（`11/18 00:00` 北京）已过 `18` 小时，折扣与徽标一个没撤。 `0.4522 → 0.2261` 仍在**，"
     "`6` 处「限时5折」全在（标准版 `3` 行 + 极速版 `3` 行）。 页 `311,607`（`+316`）。 **是延期还是忘撤，页面上读不出来** —— 不猜。" + A),

    ("`Runware` 分发层 `MiniMax H3-Image`",
     "⚪ **已过 `1` 天（`11/17` 到期 · 本期已按期下架、已收口）。 数组仍在（`endsAt: \"2026-11-17\"`）、卡片徽标 `2 → 0`、价目没动** —— "
     "「账本 vs 货架」第 `12` 次实证。 **`4K` 类促销只挂徽标、不动价目**（官方帮助文案），**只有徽标能判下架**（避坑 312）。" + A),

    ("`Google Antigravity` 免费档三个第三方模型",
     "⚠️ **今日（`11/18`）为到期日，但本期两次抓取都读不到结果。 `/pricing` `000`（第 `2` 期）、首页 `200` 但是 `JS` 壳**（四个关键词全 `0` 命中）。 "
     "**不写「已移除」、也不写「仍在」—— 两个都没证据**；只保留 `11/17` 的 `178,404` 字节快照。" + A),

    ("OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **`470 → 478`（`+8`，全部 `GPT-6.2` 家族，可逐条点名）；`:free` `14`（第 `5` 天）；零价 `17`；`?max_price=0` `16`。 "
     "新增 `4` 条标准 + `4` 条 `:batch`（北京 `11/18 01:59–02:00`），**标价与官方一分不差**。 `Ling 3.2` `endpoints` **空 `6` 天**。" + A),

    ("`OpenCode` 免费模型清单",
     "🟡 **`Free models` 段现 `12` 条**（段落逐条；同口径正则只得 `11`，`Big Pickle` 无 `-free` 后缀 → **口径不同不可相减**）。 "
     "**弃用表本期首读**：`GLM-5.3-Flash Free` 今日弃用、`MiniMax M3.1 Flash Free` `11/17`。 **「滚动池」的解释被推翻**（纠错②）。 页 `+4,235`。" + A),

    ("`Google Antigravity` 个人免费档",
     "⚠️ **`$0/month`（`11/17` 快照，`178,404` 字节）。 本期 `/pricing` `000`（第 `2` 期）、首页 `200` 但是 `JS` 壳**（`217,290` 字节、可见文本 `0` 行）。 "
     "**「字节 + `md5` 双同」对这个壳无效** —— 那 `5` 期同值证的是壳没改（纠错④）。 **免费档含哪些模型：本期无一手证据。**" + A),

    ("腾讯混元 `Hy4 flash` 开放权重",
     "🟢 **（072 期补入）三仓同分钟建仓**：`Hy4-flash` / `-FP8` / `-base`（`11/17 03:44:46Z` 起），`gated: false`、`200` 个文件；`likes 136`、`GitHub 44` stars。 "
     "**`Apache 2.0` 派生 + `§10`**：对外 `MaaS` 且年收入 > `US$50M` 或 `MAU` > `1` 亿须另签，**内部用豁免**（避坑 309）。" + A),

    ("美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **已公开（069 期补登）。 `downloads 1,850 → 2,173`（`+323`）/ `likes 356`（`+3`）；`lastModified` 仍 `11/10 07:28Z`；`?author=meituan-longcat` 仍 `32` 仓**。 "
     "四个时间点分开写：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`、媒体稿 `11/15 10:06Z`、**一手页无发布日期**。" + A),

    ("MIT 韩松团队 `PEAR`",
     "🟢 **已公开（069 期补登）。 `stars 574 → 654`（`+80`）、`forks 42`、`issues 5`；`pushed_at` `11/18 10:07:10Z`**（隔一天再推）。 `Apache-2.0`；`LIBERO 74.4%`；**未见第三方复现**。" + A),

    ("OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
     "🟡 **（072 期补入）`publicationDate` `2026-11-17T17:45Z` ＝ 北京 `11/18 01:45`。 官方逐字 `available to all Plus, Pro, Enterprise, and Edu users`** —— "
     "**`Free` 一次都没出现**；`/api/pricing` 未列 `gpt-6.2` → **只能说「发布页没写免费档」**。" + A),
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
print("落盘复核：11 条全部命中新文本；状态列 > 200 字 = 0")
