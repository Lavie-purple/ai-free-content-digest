# -*- coding: utf-8 -*-
"""第 074 期：quick_items.csv 增量（1 条新增）+ 4 条状态更新。

纪律：
  - 新增条目无一来自「推断」：每条都能回到 074 期正文的表行或一手页逐字。
  - `MiniMax` 4K：新版重新上架且无截止日 → **回置 live、清空截止日**，
    说明里写「旧版 11/18 过期、新版无截止日 + 1660 万像素门槛」。
  - `OpenRouter`：`:free` 14 → 12（点名两条）。
  - `Antigravity` 三模型：**第 2 天仍未执行**，截止日仍空。
  - `Ling 3.2`：endpoints 0 → 1，`pending` → `live`。
"""
import csv
import datetime
import io
import shutil

SRC = ".workbuddy/data/quick_items.csv"
BASE = datetime.date(2026, 11, 20)
COLS = ["分组", "名称", "量", "截止日", "截止说明", "状态", "门槛"]

rows = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(rows) == 100, len(rows)

NEW = {
    "分组": "token",
    "名称": "智谱 AutoClaw 国内站 M11W4 每周福利（100M Tokens）",
    "量": "100M Tokens ＝ 10,000 积分（第 2 周维持 100M）",
    "截止日": "2026-11-29",
    "截止说明": "11/29 23:59（北京时间）失效；领取窗口 11/23 00:00 起（官方逐字「活动时间 11 月 23 日（周一）00:00—11 月 29 日（周日）23:59」）",
    "状态": "live",
    "门槛": "登录客户端即领，每账号一次；与 M11W3（到 11/22 23:59）只隔 1 分钟、不重叠；额度锁在客户端、导不出 API",
}

hit_oc = [k for k, r in enumerate(rows) if r["名称"].startswith("OpenRouter 免费档")]
assert len(hit_oc) == 1, hit_oc
rows[hit_oc[0]]["量"] = "全量 477 个模型中 15 个零价 / 12 个带 :free 后缀（2026-11-20 实读）"
rows[hit_oc[0]]["门槛"] = ("注册，看 :free 后缀；本期 2 出 0 进（cohere/north-mini-code、thinkingmachines/inkling-2-small 消失；"
                          "新增 pixtral-large-2502 为付费）；Ling 3.2 路由已接通 1 条")

hit_ag = [k for k, r in enumerate(rows) if r["名称"].startswith("Google Antigravity 免费档三个第三方模型")]
assert len(hit_ag) == 1, hit_ag
rows[hit_ag[0]]["截止说明"] = ("官方脚注逐字 `Will be removed on November 18, 2026.` —— 到期第 2 天仍未执行、措辞未改"
                          "（183,218 字节与上期同、可见文本 diff 0 行）")
rows[hit_ag[0]]["门槛"] = "免费档四个模型全在：Gemini 3.8 Flash + Sonnet 4.6 / Opus 4.6 / GPT-OSS-120b；当「随时可能没」用"

hit_mm = [k for k, r in enumerate(rows) if r["名称"].startswith("MiniMax H3-Image 4K 五折（官方页）")]
assert len(hit_mm) == 1, hit_mm
rows[hit_mm[0]]["量"] = "4K 五折回挂：0.2261 / 0.2404 / 0.2605 / 0.4275 / 0.4499 / 0.5073 元/张（原价 0.4522–1.0146）"
rows[hit_mm[0]]["截止日"] = ""
rows[hit_mm[0]]["截止说明"] = "无截止日（新版文案删掉日期：2026-11-18 / 截止 / 结束 各 0 命中）；旧版 11/18 00:00 已过期"
rows[hit_mm[0]]["状态"] = "live"
rows[hit_mm[0]]["门槛"] = "最终交付图片宽 × 高 ≥ 1660 万像素（4096² = 1677.7 万，刚好过线）；与旧版是同一活动两个版本"

hit_ling = [k for k, r in enumerate(rows) if r["名称"].startswith("inclusionAI Ling 3.2 Flash")]
assert len(hit_ling) == 1, hit_ling
rows[hit_ling[0]]["状态"] = "live"
rows[hit_ling[0]]["门槛"] = "注册；endpoints 已从 [] 变为 1 条路由（第 8 天接通）；权重仓仍 404"

rows.append(NEW)

if "--apply" not in __import__("sys").argv:
    print("DRY RUN ｜ 预计行数", len(rows), "｜最后一行", NEW["名称"])
    raise SystemExit(0)

shutil.copy(SRC, SRC + ".bak074")
with io.open(SRC, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)

back = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(back) == 101, len(back)
assert any(r["名称"] == NEW["名称"] for r in back)
assert any("1660" in r["门槛"] for r in back)
assert any("477" in r["量"] for r in back)
assert sum(1 for r in back if r["状态"] == "live") >= 60
print("quick items ok | rows =", len(back))
