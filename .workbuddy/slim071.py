# -*- coding: utf-8 -*-
"""071 期：把 16 条 R1 超长的状态列压回 200 字以内。

纪律（052/054）：
  · 键按「活动名唯一子串」定位，命中必须恰好 1 行；
  · 改完**回读落盘文件**再断言，不信任内存变量；
  · 被裁掉的论证**一字不删**，原文进 tmp_071_slim.json，由 appendix071.py 落进附录。
"""
import io
import json
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第071期-2026-11-17.md"
OUT = WS + ".workbuddy/tmp_071_slim.json"
DRY = "--apply" not in sys.argv

A = " [附录 071](details.html)"

REWRITE = [
    ("Google Antigravity` 个人免费档",
     "🟢 **官方定价页逐字 `$0/month`",
     "🟢 **`$0/month`。 免费档首次列 4 个模型**：`Gemini 3.8 Flash` / `Claude Sonnet 4.6` / `Claude Opus 4.6` / `GPT-OSS-120b`，**后 3 个 `11/18` 移除**。 "
     "旧三串措辞**整页 0 命中**，改 `Baseline agent quota refreshed weekly`。 页 `−35,957` 字节。" + A),

    ("MIT 韩松团队 `PEAR`",
     "🟢 **已公开（069 期补登）",
     "🟢 **已公开（069 期补登）。 `stars 442 → 574`、`forks 36`；`pushed_at` 仍 `11/16 07:54:56Z`**。 "
     "**那次推送查清了**：`d604856a` 是「`README` 论文链接改指 `arXiv`」—— **改文档、不是改代码**。 `Apache-2.0`；`LIBERO 74.4%`；**未见第三方复现**。" + A),

    ("智谱 `AutoClaw` 国内站 `M11W3`",
     "🟠 **距截止 `5` 天。 （071 期补入）",
     "🟠 **距截止 `5` 天。 （071 期补入）官方逐字「登录即可领取 `100M Tokens`（相当于 `10,000` 积分），每账号限领一次」**；`100M` ＝ 「`1` 亿」。 "
     "**只在 `AutoClaw` 内用**，自接 API 另计费；内置 `GLM-5.3` / `GLM-5-Turbo` / `GLM-5V-Turbo`。 **周变量**：`50M → 50M → 100M`，**不可跨周相减**。" + A),

    ("`Google Antigravity` 免费档三个第三方模型",
     "🟠 **距截止 `1` 天。 （071 期新增观测位）",
     "🟠 **距截止 `1` 天。 （071 期新增观测位）三个模型名后的 `<a title>` 逐字「Will be removed on November 18, 2026.」，可见文本只有一个 `4`**（避坑 305）。 "
     "移除后免费档只剩 `Gemini 3.8 Flash`。 **降档三样只有「模型」有日期，上下文与额度两期都无数字。**" + A),

    ("OpenAI `ChatGPT for Academic Researchers`",
     "🟡 **（071 期补入）名额 `3` 个数不可互换",
     "🟡 **（071 期补入）`3` 个数不可互换**：`20` 万＝项目总目标、`5` 万＝本轮新增、`15` 万＝本轮可覆盖人数。 "
     "**档位从 `Pro` 降到 `Plus`**（官方逐字 `most participants would have stayed within ChatGPT Plus usage limits`）；**额度无数字、模型只写 `frontier models`**。 **抽签改先到先得**。" + A),

    ("阿里 `Qwen4-Max` 发布",
     "🟡 **（070 期补入）**付费**模型",
     "🟡 **（070 期补入）**付费**模型 —— 官方博客 `free` / `免费` `0` 命中**。 "
     "**本期两条**：① `?author=Qwen` 无 `Qwen4` 仓 → 「小尺寸将开源」仍无落地；② `OpenRouter` 端点价 `$1.425` / `$4.275` ＝ 官方价 `0.95` 倍且 `discount: 0` → **两套报价并排、不合并**。" + A),

    ("OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **全量 `468 → 470`",
     "🟢 **全量 `468 → 470`（`+2`）；`:free` `14`（**第 `4` 天**）；零价 `17`；`?max_price=0` `16`。 "
     "**只能指名 `1` 条**：`tencent/hy4-flash`（北京 `11/16 22:18`）；另一条是「重上架」，`created` 旧、**无名册留白**。 `Ling 3.2` `endpoints` **空 `4` 天**（`404` 已变 `200`）。" + A),

    ("MiniMax `H3-Image` `4K` 生图限时",
     "🟠 **距截止 `1` 天（`11/18 00:00` 北京时间",
     "🟠 **距截止 `1` 天（`11/18 00:00` 北京，实剩约 `6` 小时）。 `4K` 单张 `0.4522 → 0.2261` 元**仍在；`1K` / `2K` **不打折**。 "
     "页 `311,291`（`−399`），**价格与门槛句未变**；**无同源快照、本期不做逐行 diff**（留白）。 ⚠️ 折的是按张单价、非额度。" + A),

    ("`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日",
     "🟡 **第三方聚合层 · 逐条标核实日。 第 `9` 期：`¥1760 → ¥1758`（`−2`）、卡册 `60 → 61`、日戳 `122`**（`11/17` `2` / `11/16` `28` / `11/15` `18` / `11/14` `70` / `11/13` `2` / `11/9` `2`）。 "
     "**「面额微降、卡数微增」是第六种形状**；只记读数、不推规律。" + A),

    ("Anthropic `Claude Fable 5.2`",
     "🟠 **今日已到期（`11/17 15:59` 北京",
     "🟠 **今日已到期（`11/17 15:59` 北京 · 官方逐字 `11/16 23:59 PT`）。** 定价页 `1,344,780` 字节（`+701`）、`md5` 仍随 `CSP nonce` 变；"
     "**本期未见「`Fable` 一周」促销字样**（`November` 仅 `1` 处、属企业版说明）—— **未逐字比对该段，不作因果判断**。" + A),

    ("`Runware` 分发层 `MiniMax H3-Image`",
     "🟠 **今日到期（`11/17`",
     "🟠 **今日到期（`11/17` · 数组 `endsAt: \"2026-11-17\"`）。 三条同验：数组在、徽标在（两型号各一）、官方价目 `0.2261` 在** —— **「三方一致」首次干净样本**。 "
     "只作用于 `4K`（≥ `1660` 万像素）；`MiniMax` 侧是 `11/18 00:00` 北京（**时刻**），**两个都写、不换算**。" + A),

    ("`OpenCode` 免费模型清单",
     "🟡 **`-free` `id` `15 → 14`",
     "🟡 **`-free` `id` `15 → 14`（同口径正则）**：撤 `minimax-m3.1-flash-free`（页内 `m3.1` **`0` 命中**）、`hy4-flash-free` **仍在**。 "
     "页 `−512` 字节 —— **删块只掉几百字节、`diff` 里没有一行像删除**，**撤项靠 `id` 清单不靠字节**（避坑 308）。" + A),

    ("美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **已公开（069 期补登）。 `downloads 1,573",
     "🟢 **已公开（069 期补登）。 `downloads 1,573 → 1,850`（`+277`）/ `likes 353`（`+64`）；`lastModified` 仍 `11/10 07:28Z`；`?author=meituan-longcat` 仍 `32` 仓**。 "
     "四个时间点分开写：建仓 `11/04`、最后变更 `11/10`、媒体稿 `11/15`、**一手页无发布日期字段**。" + A),

    ("`thinkingmachines/Inkling-2-Small`",
     "🟢 **`Apache-2.0` · `gated: false`",
     "🟢 **`Apache-2.0` · `gated: false`。 `downloads 7,329 → 16,918`（**`+9,589`**）/ `likes 429`（`+66`）；`lastModified 11/15 05:54Z` 未动**。 "
     "**`downloads` 是近 `30` 天滚动窗口、且中间停更快照至少 `3` 天 → 只记「窗口涨了」**（避坑 301）。" + A),

    ("百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `8` 天）",
     "🟢 **生效中（距承诺日 `8` 天）。 `11月25日前开源` 逐字仍在**（页 `54,010` 字节，与上期逐字节相同）。 **权重仍未放**：`?author=baidu` 仍 `39` 仓（第 `14` 天 `0` 变化）；"
     "两 `Base` 仓 `downloads` **解冻**（`4,145` / `1,481`）、`likes` `355` / `394`。" + A),

    ("`Runware` 分发层 `MiniMax H3 Max` 促销 `30% OFF`",
     "⚪ **已过 `2` 天（`11/15` 到期）",
     "⚪ **已过 `2` 天（`11/15` 到期）。 数组里那条 `endsAt: \"2026-11-15\"` 仍在，卡片徽标卸下后未挂回** —— **「数组是账本、卡片是货架」第 `2` 次双读**。 "
     "本期数组 `22` 条、**其中 `13` 条早于今日** —— 「数组里有」≠「在售」。" + A),
]

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
rows = md.split("\n")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def count(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return len(re.sub(r"\s", "", s))


archive, done = [], []
for tag, old_prefix, new in REWRITE:
    hits = [k for k, l in enumerate(rows)
            if l.startswith("|") and tag in l and l.split("|")[3].strip().startswith(old_prefix)]
    assert len(hits) == 1, ("命中数不是 1", tag, len(hits))
    c = cells(rows[hits[0]])
    assert len(c) == 3, ("字段数异常", tag, len(c))
    assert "|" not in new, ("状态列里出现竖线", tag)
    archive.append({"name": c[0], "old": c[2], "new": new, "before": count(c[2]), "after": count(new)})
    rows[hits[0]] = "|%s| %s | %s" % (c[0], c[1], new)
    done.append(tag)

print("改写 %d 行" % len(done))
over = [(a["before"], a["after"], a["name"][:30]) for a in archive if a["after"] > 200]
print("压后仍 >200：", over)
assert not over, over

if DRY:
    print("DRY RUN —— 未写盘")
    sys.exit(0)

io.open(MD, "w", encoding="utf-8", newline="\n").write("\n".join(rows))
io.open(OUT, "w", encoding="utf-8").write(json.dumps(archive, ensure_ascii=False, indent=1))

disk = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
back = [l for l in disk.split("\n") if l.startswith("|") and not l.startswith("| 活动") and not l.startswith("| ---")]
for l in back:
    c = cells(l)
    if len(c) == 3 and count(c[2]) > 200:
        raise AssertionError(("落盘后仍超长", c[0][:30], count(c[2])))
assert len(json.load(open(OUT, encoding="utf-8"))) == len(REWRITE)
print("slim ok | 回读 %d 行全部 ≤ 200 | 归档 %d 条" % (len(back), len(archive)))
