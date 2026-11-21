# -*- coding: utf-8 -*-
"""075 期：把 10 条 R1 超长的状态列压回 200 字以内，并消掉 2 行的多避坑编号（R2）。

纪律（052/054/074）：
  · 键按「活动名唯一子串」定位，命中必须恰好 1 行；
  · 改完**回读落盘文件**再断言，不信任内存变量；
  · 被裁掉的论证**一字不删**，原文进 tmp_075_slim.json，由 appendix075.py 落进附录。
"""
import io
import json
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第075期-2026-11-21.md"
OUT = WS + ".workbuddy/tmp_075_slim.json"
DRY = "--apply" not in sys.argv

A = " [附录 075](details.html) |"

REWRITE = [
    ("`Runware` 分发层 `MiniMax H3-Image`",
     "⚪ **已收口（`11/17` 到期、已过 `4` 天）。 `h3-image` `18`、徽标 `0`、价目不动 —— 第 `16` 次实证。 "
     "新增：数组日期整排换过（`11-17` `5→1`、`11-19` `5→1`），**总条数恒为 `22`**、`endsAt` 在滚动。 这类促销只有徽标能判下架。" + A),

    ("智谱 `AutoClaw` 国内站 `M11W3`",
     "🟠 **距截止 `1` 天。 博客逐字 `11 月 16 日至 11 月 22 日` 登录领 `100M`（`10,000` 积分），`11/22 23:59` 失效。 "
     "`M11W4` 已挂出（`11/23`–`11/29`，仍 `100M`），**两期只隔 `1` 分钟**、本周额度周日作废。 `M11W5` 本期 `404`。 锁客户端、导不出 `API`。" + A),

    ("`Google Antigravity` 免费档三个第三方模型",
     "🟠 **距截止 `9` 天（官方改期，不是「未执行」）。 073/074 写的「到期第 N 天未执行」本期更正：脚注 `4` 从 `November 18` 改成 `November 30`**"
     "（全页 `November 18` `0` 命中）。 付费档另列 `Gemini 4` 四款 + `Sonnet 5.5` / `Opus 5.5`，**免费档一个都没有**。" + A),

    ("OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **四口径全部持平：全量 `477`、`:free` `12`、零价 `15`、`max_price=0` `14`（第 `2` 天）。 窗口内只新增 `1` 条**："
     "`radixark/daisyrose-27b`（`11/21 08:49`，付费）。 `gpt-6.2` 仍 `8` 条无 `:free`（第 `4` 天）。 **`Ling` 口径：`:free` `1` 条路由、基名 `0` 条**。" + A),

    ("`OpenCode` 免费模型清单",
     "🟡 **`Free models` 段仍 `12` 条；页 `102,667` / `md5 6105ecab` 与上期字节 + `md5` 双同（第 `3` 期）**。 "
     "`GLM-5.3-Flash Free` 不在段内、弃用表仍留行（不同步第 `3` 期）。 `LongCat` 每日 `100` 次；`Beam` 排除中国大陆。" + A),

    ("`Google Antigravity` 个人免费档",
     "🟢 **逐字 `$0/month`（`181,393` 字节 / `md5 7738ba05`）。 免费档四个模型**（`3.8 Flash` + 三个第三方）。 "
     "**唯一实质变化：三个第三方的移除日 `11/18 → 11/30`** —— 是改期、不是未执行。 `Baseline agent quota` 仍无数字（第 `6` 期）。" + A),

    ("`thinkingmachines/Inkling-2-Mini` 开放权重",
     "🟢 **（075 期补入）官方逐字 `small enough to run on your laptop`；`~20GB` 为原生 `NVFP4` 权重，实测机 `MacBook Pro M5 Pro 48GB` 飞行模式跑通**。 "
     "`DeepSWE v1.1` `48.2%` / `Vals Index v2.2` `46.5%`（**厂商自评**）。 建仓 `11/17`、权重变更 `11/20`、公告 `11/21` —— **三个时间点不合并**。" + A),

    ("腾讯混元 `Hy4 flash` 开放权重",
     "🟢 **（072 期补入）`downloads` 三仓本批次全未刷新**（`3,949` / `1,219` / `699`）；`likes 550` / `23` / `24`。 "
     "第三方转档 `10` 个以上；`?search=Hy4` 返回 `100`（**触 `limit` 上限，`≥100`**）。 许可 `Apache 2.0` 派生 + `§10`：对外 `MaaS` 过 `$50M` 或 `1` 亿 `MAU` 须另签。" + A),

    ("腾讯混元 `Hy4`（旗舰 · 非 `flash`）开放权重",
     "🟢 **（075 期补登）三仓权重 `11/20 03:05:49Z`–`03:05:54Z`（北京 `11:05`）同批落盘**，落在上一期窗口内、**未登**。 "
     "`downloads` `89` / `71` / `68`（合计 `228`）、`likes` `127` / `11` / `8`。 **`BF16` 约 `1.5TB`、`FP8` 约 `770GB` —— 开放≠可本地跑**；量化走 `AngelSlim` `GGUF`。" + A),

    ("OpenAI `GPT-6.2 Astra` / `GPT-6.2 Sol` 发布",
     "🟡 **（072 期补入）名单 `Plus` / `Pro` / `Enterprise` / `Edu`，`Free` 不在其中。 本期读数：`OpenRouter` 仍 `8` 条无 `:free`（第 `4` 天）；"
     "`chatgpt.com/pricing` 第 `4` 期读不到正文；`openai.com/index/` 窗口内无新免费条目。 不写「免费可用/不可用」。**" + A),

    # R2：两处避坑 → 只留一处
    ("MiniMax `H3-Image` `4K` 生图限时",
     "⚪ **旧版已过期（`11/18 00:00` 到期）；现行版本是第二版（无截止日、`1660` 万像素门槛），见 `4.2`。 本行只记「旧版过期」。 "
     "第二版本期仍原样在架（页 `310,127 → 310,162`，`+35`），**不代表该折扣已停**（避坑 317）。 旧文案的截止句整句不存在，**截止日不跨版本**。" + A),
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
