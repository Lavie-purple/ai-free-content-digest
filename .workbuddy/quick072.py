# -*- coding: utf-8 -*-
"""第 072 期：quick_items.csv 增量（3 条）+ Runware 4K 收口。

纪律：
  - 新增条目无一来自「推断」：每条都能回到 072 期正文的表行或一手页逐字。
  - 「今天到期 ≠ 已结束」：`MiniMax` 官方页的 4K 五折，截止时刻过了 18 小时仍在挂 →
    **状态保持 live，但在截止说明里写清「已过截止时刻、页面未撤」**，不置 over。
  - 「分发层已下架」：`Runware` 的 4K 促销徽标 2 → 0 → **置 over**（收口）。
"""
import csv, io, datetime, shutil

SRC = ".workbuddy/data/quick_items.csv"
BASE = datetime.date(2026, 11, 18)
COLS = ["分组", "名称", "量", "截止日", "截止说明", "状态", "门槛"]

rows = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(rows) == 94, len(rows)

# 1) Runware 4K：徽标 2 → 0，收口
hit = 0
for r in rows:
    if r["名称"].startswith("Runware 4K 图像生成"):
        assert r["状态"] == "live", r["状态"]
        r["截止日"] = "2026-11-17"
        r["截止说明"] = ("11/17（促销数组 `endsAt: \"2026-11-17\"` 仍在册、卡片 `title` **2 → 0**、"
                     "价目一个数没动；**本期已按期下架**）")
        r["量"] = "4K 档 50% OFF（数组 22 条不变；徽标清零 = 货架下架）"
        r["状态"] = "over"
        r["门槛"] = ("`4K` 类促销只挂徽标、不动价目（官方帮助文案原话）；**判下架只能看徽标**。"
                  "与 `MiniMax` 官方页（截止 11/18 00:00、未撤）**两个口径分岔**")
        hit += 1
assert hit == 1, hit

NEW = [
    {"分组": "oss",
     "名称": "腾讯混元 Hy4 flash 开放权重",
     "量": "220.25B 实测总参（含 64B Engram）/ 激活 11.3B + 0.43B / 1M 上下文 / 三仓 600 个文件",
     "截止日": "",
     "截止说明": "无截止日（权重永久开放；许可有商用门槛，不是时间门槛）",
     "状态": "live",
     "门槛": ("`Tencent Hy License 1.0` ＝ `Apache 2.0` 派生 + `§10`：对外做 `MaaS` 且"
              "（全球年毛收入 > US$50M 或产品 MAU > 1 亿）须另签；**纯内部使用豁免**。"
              "三仓 `gated: false`；`safetensors` 实测 220.25B ≠ 媒体 224B")},
    {"分组": "api",
     "名称": "OpenAI GPT-6.2 Astra / Sol 发布",
     "量": "Astra $8 / $0.40 缓存 / $40；Sol $2 / $0.10 / $10（每百万 token）",
     "截止日": "",
     "截止说明": "无截止日（模型发布；可用名单 `Plus` / `Pro` / `Enterprise` / `Edu`）",
     "状态": "pending",
     "门槛": ("**发布名单里没有 `Free`**（官方逐字 `available to all Plus, Pro, Enterprise, and Edu users`）。"
              "`chatgpt.com/pricing` 本期 000、`/api/pricing` 未列 `gpt-6.2` → 只能说「发布页没写免费档」。"
              "`Pro 200` 首次拿到 `Ultrafast`（从 Sol 开始）")},
    {"分组": "api",
     "名称": "MiniMax H3-Image 4K 五折（官方页）",
     "量": "4K 单张 0.4522 → 0.2261 元；6 处「限时5折」徽标（标准版 3 + 极速版 3）",
     "截止日": "2026-11-18",
     "截止说明": ("11/18 00:00（官方逐字「即日起至 2026 年 11 月 18 日 00:00（北京时间，结束时刻不含）」）"
              "—— **已过 18 小时，页面折扣与徽标一个没撤**"),
     "状态": "live",
     "门槛": ("要求最终交付图片宽 × 高 ≥ 1660 万像素；`1K` / `2K` 不打折。"
              "**是「悄悄延期」还是「忘了撤」，页面上读不出来** —— 用之前按原价预期")},
]
have = set(r["名称"] for r in rows)
for n in NEW:
    assert n["名称"] not in have, n["名称"]

rows.extend(NEW)

shutil.copyfile(SRC, SRC + ".bak")
buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=COLS, lineterminator="\n")
w.writeheader()
for r in rows:
    w.writerow({k: r.get(k, "") for k in COLS})
io.open(SRC, "w", encoding="utf-8", newline="").write(buf.getvalue())

# 回读断言（053/054：断言是必要条件，落盘后必须回读）
back = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(back) == 97, len(back)
assert all(b["分组"] in ("token", "api", "cloud", "subsidy", "edu", "oss", "over") for b in back)
stale = [b for b in back if b["截止日"] and b["状态"] != "over"
         and datetime.date.fromisoformat(b["截止日"]) < BASE]
assert not stale, [(b["名称"][:20], b["截止日"]) for b in stale]
assert any("Hy4 flash 开放权重" in b["名称"] for b in back), "oss 新增未落盘"
assert any(b["名称"].startswith("Runware 4K") and b["状态"] == "over" for b in back), "Runware 未收口"
print("quick ok | 94 → %d 行 | 收口 1 条 | 新增 3 条 | 过期未收口 0" % len(back))
