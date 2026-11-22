# -*- coding: utf-8 -*-
"""第 076 期：quick_items.csv 增量（1 条新增）+ 4 条状态/说明更新。

纪律：
  - 新增条目无一来自「推断」：每条都能回到 076 期正文的表行或一手页逐字。
  - `OpenCode` 的 `Inkling 2 Small Free` **按弃用表置 `over`（11/19）** —— 上期还是 `live`。
  - `OpenRouter`：477/15/12 → **476/14/11**，四项同降 1。
"""
import csv
import datetime
import io
import shutil
import sys

SRC = ".workbuddy/data/quick_items.csv"
BASE = datetime.date(2026, 11, 22)
COLS = ["分组", "名称", "量", "截止日", "截止说明", "状态", "门槛"]

rows = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(rows) == 103, len(rows)

NEW = [
    {
        "分组": "api",
        "名称": "Thinking Machines Inkling 2 Mini API（OpenRouter）",
        "量": "2 provider：$0.075/$0.30 每百万 token（PrimeIntellect · fp4 · 1M ctx）｜$0.08/$0.35（Io Net · nvfp4 · 256K ctx）",
        "截止日": "",
        "截止说明": "无截止日（按量计费）；created 北京 2026-11-21 10:19；无 :free 变体、无免费额度",
        "状态": "live",
        "门槛": "discount 0（原价）；两个 provider 上下文与价格都不同；Tinker 侧是否有免费额度仍未取到一手",
    },
]

hit_or = [k for k, r in enumerate(rows) if r["名称"] == "OpenRouter 免费档"]
assert len(hit_or) == 1, hit_or
rows[hit_or[0]]["量"] = "全量 476 个模型中 14 个零价 / 11 个带 :free 后缀（2026-11-22 实读，四项同降 1）"
rows[hit_or[0]]["门槛"] = ("注册，看 :free 后缀；本期出 2 进 1：下架 dots-3-note-preview:free（真免费）与 meituan/longcat-2.0，"
                          "新增 thinkingmachines/inkling-2-mini（付费）；gpt-6.2 仍 8 条无 :free（第 5 天）")

hit_oc = [k for k, r in enumerate(rows) if r["名称"] == "OpenCode 免费模型清单"]
assert len(hit_oc) == 1, hit_oc
rows[hit_oc[0]]["量"] = "12 项（2026-11-22 实读，一进一出：进 Tidepool Alpha Free、出 Inkling 2 Small Free）"
rows[hit_oc[0]]["门槛"] = ("LongCat 2.5 Free 每日 100 次；Beam Free 明确排除中国大陆；弃用表 11/19 新增 3 行"
                         "（Inkling 2 Small Free / GLM 5.2 / GLM 5.1）")

hit_ink = [k for k, r in enumerate(rows) if r["名称"].startswith("OpenCode 的 Inkling 2 Small Free")]
assert len(hit_ink) == 1, hit_ink
rows[hit_ink[0]]["状态"] = "over"
rows[hit_ink[0]]["截止日"] = "2026-11-19"
rows[hit_ink[0]]["截止说明"] = "弃用表逐字 November 19, 2026（076 期核实：免费段已无此条）"

hit_w3 = [k for k, r in enumerate(rows) if r["名称"].startswith("智谱 AutoClaw 国内站 M11W3")]
assert len(hit_w3) == 1, hit_w3
rows[hit_w3[0]]["截止说明"] = "11/22 23:59 收口（11/16–11/22）；M11W4（11/23–11/29，仍 100M）11/23 00:00 接班，两期只隔 1 分钟"

for n in NEW:
    rows.append(n)

if "--apply" not in sys.argv:
    print("DRY RUN ｜ 预计行数", len(rows), "｜新增", [n["名称"] for n in NEW])
    raise SystemExit(0)

shutil.copy(SRC, SRC + ".bak076")
with io.open(SRC, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)

back = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(back) == 104, len(back)
assert any(r["名称"].startswith("Thinking Machines Inkling 2 Mini API") for r in back)
assert any("476" in r["量"] for r in back)
assert any("Tidepool" in r["量"] for r in back)
assert any(r["截止日"] == "2026-11-19" and r["状态"] == "over" for r in back)
print("quick items ok | rows =", len(back))
