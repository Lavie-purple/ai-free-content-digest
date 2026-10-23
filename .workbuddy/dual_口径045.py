# -*- coding: utf-8 -*-
"""045 期：双口径三态 + 差值名单，从 deadlines.csv 实跑。"""
import csv, io, os
from collections import Counter

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(WS, ".workbuddy", "data", "deadlines.csv")

rows = list(csv.DictReader(io.open(CSV, encoding="utf-8-sig")))
print("csv rows:", len(rows))

col = Counter((r["紧急度"] or "空").strip() for r in rows)
sta = Counter((r["状态"] or "空").strip() for r in rows)
print("色标口径:", dict(col), "sum", sum(col.values()))
print("classify():", dict(sta), "sum", sum(sta.values()))

diff = [r for r in rows if r["紧急度"].strip() in ("🟠", "🟢") and r["状态"].strip() == "pending"]
print("差值(色标 🟠/🟢 且 pending):", len(diff))
for r in diff:
    print("   - %s | 截止 %s | 紧急度 %s | 状态 %s | 截止原文 %s"
          % (r["活动"], r["截止日期"], r["紧急度"], r["状态"], r["截止原文"]))

# 与 044 期差值名单比对（044: Nano Banana 2 停用 / Anthropic 新版使用政策 / o4-mini / Kling 4.0 / Cloudflare 收购 Deno）
prev = {"Google Nano Banana 2", "Anthropic 新版使用政策", "OpenAI o4-mini", "快手可灵 Kling 4.0", "Cloudflare"}
now_names = [r["活动"] for r in diff]
for r in diff:
    hit = any(p in r["活动"] for p in prev)
    print("   与044同名: %s -> %s" % (r["活动"], "是" if hit else "否（新进出）"))
