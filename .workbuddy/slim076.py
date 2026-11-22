# -*- coding: utf-8 -*-
"""076 期：把 1 条 R1 超长的状态列压回 200 字以内。

纪律（052/054/074/075）：
  · 键按「活动名唯一子串」定位，命中必须恰好 1 行；
  · 改完**回读落盘文件**再断言，不信任内存变量；
  · 被裁掉的论证**一字不删**，原文进 tmp_076_slim.json，由 appendix076.py 落进附录。
"""
import io
import json
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第076期-2026-11-22.md"
OUT = WS + ".workbuddy/tmp_076_slim.json"
DRY = "--apply" not in sys.argv

A = " [附录 076](details.html) |"

REWRITE = [
    ("`thinkingmachines/inkling-2-mini` 进入 `OpenRouter`",
     "🟡 **（076 期新增观测位）`created` 北京 `11/21 10:19`。 `PrimeIntellect`：`fp4` / `1M` ctx / `$0.075` 输入、`$0.30` 输出（每百万 token）；"
     "`Io Net`：`nvfp4` / `256K` ctx / `$0.08` / `$0.35`。 均 `discount: 0`。 "
     "**「免费 API 入口」答案：收费、无免费档**；`Tinker` 额度仍未取到一手。" + A),
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
