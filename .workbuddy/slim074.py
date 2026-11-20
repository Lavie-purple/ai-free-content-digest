# -*- coding: utf-8 -*-
"""074 期：把 11 条 R1 超长的状态列压回 200 字以内，并消掉 MiniMax 4K 行的第 2 个避坑编号。

纪律（052/054）：
  · 键按「活动名唯一子串」定位，命中必须恰好 1 行；
  · 改完**回读落盘文件**再断言，不信任内存变量；
  · 被裁掉的论证**一字不删**，原文进 tmp_074_slim.json，由 appendix074.py 落进附录。
"""
import io
import json
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第074期-2026-11-20.md"
OUT = WS + ".workbuddy/tmp_074_slim.json"
DRY = "--apply" not in sys.argv

A = " [附录 074](details.html) |"

REWRITE = [
    ("腾讯混元 `Hy4 flash` · `WorkBuddy` 限时免费",
     "🟠 **距截止 `9` 天。 只限 `WorkBuddy` 内的 `Hy4 flash`**；`TokenHub` 是**限时 `5` 折**。 "
     "参数官方口径 `220.25B` / 激活 `11.3B` + `0.43B`。 **权重已开放三仓**，到期后能用的是权重。" + A),

    ("MiniMax `H3-Image` `4K` 生图限时",
     "⚪ **旧版已过期（`11/18 00:00`）；同一促销已换文案重挂，新版本见 `4.2`。 本期 `0.2261` / `限时5折` 全部回涨、页 `305,754 → 310,127`（`+4,373`）。 "
     "本行只记「旧版过期」，**判结束要连续两期不再出现**（避坑 317）。" + A),

    ("`Runware` 分发层 `MiniMax H3-Image`",
     "🟠 **已过 `3` 天（`11/17` 到期）。 `h3-image` `18`、徽标 `0`、价目不动 —— 第 `15` 次实证。 "
     "新增读数：数组在滚动（`2026-11-17` `7→5`、`2026-11-19` `1→5`），**「共 `22` 条」不是常量**。 这类促销只有徽标能判下架。" + A),

    ("智谱 `AutoClaw` 国内站 `M11W4`",
     "🟠 **（074 期补入）`11/23`–`11/29` 登录领 `100M`（`10,000` 积分），`11/29 23:59` 失效。 "
     "与 `M11W3`（到 `11/22 23:59`）**只隔 `1` 分钟**，本周额度本周日作废。 `100M` 连续第 `2` 周（前两周 `50M`）。 锁客户端、导不出 `API`。" + A),

    ("`Google Antigravity` 免费档三个第三方模型",
     "🔴 **到期第 `2` 天，未执行、措辞未改。 `183,218` 字节与上期同、`md5` 变、逐行 diff `0` 行**：免费档仍四个（`3.8 Flash` + `Sonnet 4.6` / `Opus 4.6` / `GPT-OSS-120b`），"
     "脚注 `4` 仍 `Will be removed on November 18, 2026.`" + A),

    ("OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **`480 → 477`；`:free` `12`（`−2`，点名 `cohere/north-mini-code`、`thinkingmachines/inkling-2-small`）；零价 `15`；`max_price=0` `14`。 "
     "另少 `llama-3.2-1b`、`grok-build-0.1`，新增 `pixtral-large-2502`（付费）。 `Ling 3.2` 路由 `0 → 1`。**" + A),

    ("`OpenCode` 免费模型清单",
     "🟡 **`Free models` 段仍 `12` 条；页 `102,667` / `md5 6105ecab` 与上期双同**（这次「不变」能证明）。 "
     "`GLM-5.3-Flash Free` 不在段内、弃用表仍留行（第 `2` 期）。 `LongCat` 每日 `100` 次；`Beam` 排除中国大陆。" + A),

    ("`Google Antigravity` 个人免费档",
     "🟢 **逐字 `$0/month`；`183,218` 字节与上期同、可见文本 diff `0` 行。 免费档四个模型**（`3.8 Flash` + 三个第三方）。 "
     "`Baseline agent quota refreshed weekly` 仍无数字。" + A),

    ("腾讯混元 `Hy4 flash` 开放权重",
     "🟢 **（072 期补入）第 `3` 天：`dl 3,949` / `1,219` / `699`，`likes 483` / `22` / `24`。 "
     "第三方转档 `10` 个以上（`?search=Hy4` `43 → 85` 条）。 许可 `Apache 2.0` 派生 + `§10`**：对外 `MaaS` 过 `$50M` / `1` 亿 `MAU` 须另签。" + A),

    ("OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
     "🟡 **（072 期补入）名单 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 本期三读数：`OpenRouter` 仍 `8` 条无 `:free`；"
     "`chatgpt.com/pricing` 仍 `000`；`openai.com/index/` 窗口内无新免费条目。 不写「免费可用/不可用」。**" + A),

    ("`MiniMax H3-Image` `4K` 五折 · 第二版",
     "🟠 **（074 期补入）逐字「最终交付图片的宽 × 高 ≥ `1660` 万像素，即享整次请求费用 `5` 折」。 "
     "六档折后价回位（`0.2261`–`0.5073`）、`限时5折` `12` 处、页 `+4,373`。 `4096²` ＝ `1677.7` 万，刚好过线。 与 `4.1` 是同一活动两版，不合并。**" + A),
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
