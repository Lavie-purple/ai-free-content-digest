# -*- coding: utf-8 -*-
"""第 075 期：quick_items.csv 增量（2 条新增）+ 4 条状态/说明更新。

纪律：
  - 新增条目无一来自「推断」：每条都能回到 075 期正文的表行或一手页逐字。
  - `Antigravity` 三模型：**官方把移除日从 11/18 改到 11/30** → 名字与截止日一起改。
  - `Ling 3.2`：口径更正为「`:free` 1 条路由 / 基名 0 条」。
  - `OpenRouter`：477/15/12 四口径持平。
"""
import csv
import datetime
import io
import shutil
import sys

SRC = ".workbuddy/data/quick_items.csv"
BASE = datetime.date(2026, 11, 21)
COLS = ["分组", "名称", "量", "截止日", "截止说明", "状态", "门槛"]

rows = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(rows) == 101, len(rows)

NEW = [
    {
        "分组": "oss",
        "名称": "Thinking Machines Inkling 2 Mini 开放权重",
        "量": "26.4B 总参 / 3.4B 激活（循环层跑 3 次）· 权重约 20GB",
        "截止日": "",
        "截止说明": "无截止日（Apache-2.0，权重永久开放）；公告 2026-11-20 PT ＝ 北京 11/21 04:28",
        "状态": "live",
        "门槛": "权重约 20GB（多为原生 NVFP4、末 4 层 MXFP8），官方实测机 MacBook Pro M5 Pro 48GB；32GB 机器能否跑满上下文官方未给数；HF 建仓 11/17、权重变更 11/20、公告 11/21",
    },
    {
        "分组": "oss",
        "名称": "腾讯混元 Hy4（770B）开放权重",
        "量": "770B 总参 / 激活 49B + 视觉 1.23B · 1M 上下文 · 78 层",
        "截止日": "",
        "截止说明": "无截止日（权重永久开放；Tencent Hy License，须读 LICENSE 原文）",
        "状态": "live",
        "门槛": "三仓权重 11/20 03:05Z（北京 11:05）同批落盘；BF16 约 1.5TB、FP8 约 770GB —— 开放≠可本地跑；想跑走 AngelSlim/Hy4-GGUF",
    },
]

hit_ag = [k for k, r in enumerate(rows) if r["名称"].startswith("Google Antigravity 免费档三个第三方模型")]
assert len(hit_ag) == 1, hit_ag
rows[hit_ag[0]]["名称"] = "Google Antigravity 免费档三个第三方模型 11/30 移除"
rows[hit_ag[0]]["截止日"] = "2026-11-30"
rows[hit_ag[0]]["截止说明"] = ("官方脚注由 `Will be removed on November 18, 2026.` 改为 `November 30, 2026.`"
                          "（全页 November 18 归零）；073/074 写的「到期未执行」应更正为「改期」")
rows[hit_ag[0]]["门槛"] = "免费档四个模型全在：Gemini 3.8 Flash + Sonnet 4.6 / Opus 4.6 / GPT-OSS-120B；Gemini 4 全家只在付费档"

hit_or = [k for k, r in enumerate(rows) if r["名称"].startswith("OpenRouter 免费档")]
assert len(hit_or) == 1, hit_or
rows[hit_or[0]]["量"] = "全量 477 个模型中 15 个零价 / 12 个带 :free 后缀（2026-11-21 实读，与上期持平）"
rows[hit_or[0]]["门槛"] = ("注册，看 :free 后缀；本期 0 出 1 进（新增 radixark/daisyrose-27b 为付费）；"
                          "gpt-6.2 仍 8 条无 :free（第 4 天）")

hit_ling = [k for k, r in enumerate(rows) if r["名称"].startswith("inclusionAI Ling 3.2 Flash")]
assert len(hit_ling) == 1, hit_ling
rows[hit_ling[0]]["门槛"] = ("注册；`:free` 变体 1 条路由（1,466 字节），基名 0 条（462 字节）—— 只查基名会误判「路由断了」；"
                          "权重仓仍 404")

hit_w3 = [k for k, r in enumerate(rows) if r["名称"].startswith("智谱 AutoClaw 国内站 M11W3")]
assert len(hit_w3) == 1, hit_w3
rows[hit_w3[0]]["截止说明"] = "11/22 23:59 失效（11/16 起）；下一期 M11W4（11/23–11/29，仍 100M）已挂出，两期只隔 1 分钟"

for n in NEW:
    rows.append(n)

if "--apply" not in sys.argv:
    print("DRY RUN ｜ 预计行数", len(rows), "｜新增", [n["名称"] for n in NEW])
    raise SystemExit(0)

shutil.copy(SRC, SRC + ".bak075")
with io.open(SRC, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)

back = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(back) == 103, len(back)
assert any(r["名称"].startswith("Thinking Machines Inkling 2 Mini") for r in back)
assert any("770B" in r["量"] for r in back)
assert any("2026-11-30" == r["截止日"] for r in back)
assert any("1,466" in r["门槛"] for r in back)
assert sum(1 for r in back if r["状态"] == "live") >= 60
print("quick items ok | rows =", len(back))
