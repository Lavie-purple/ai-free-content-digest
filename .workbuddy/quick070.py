# -*- coding: utf-8 -*-
"""第 070 期：quick_items.csv 增量 + 过期项收口。"""
import csv, io, datetime, shutil

SRC = ".workbuddy/data/quick_items.csv"
BASE = datetime.date(2026, 11, 16)
COLS = ["分组", "名称", "量", "截止日", "截止说明", "状态", "门槛"]

rows = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(rows) == 86, len(rows)

# 1) 过期收口：腾讯轻量云 专家限量（11/13 截止）
hit = 0
for r in rows:
    if r["名称"].startswith("腾讯轻量云 专家限量"):
        assert r["状态"] == "live", r["状态"]
        r["状态"] = "over"
        r["截止说明"] = "11/13 失效（已过 3 天）；本期无续期公告"
        hit += 1
assert hit == 1, hit

NEW = [
    {"分组": "api",
     "名称": "腾讯混元 Hy4 flash（WorkBuddy 内限免）",
     "量": "WorkBuddy 客户端内限免（原价 输入 0.5 元 / 输出 2 元 每百万 token）",
     "截止日": "2026-11-29",
     "截止说明": "11/29（聚合层）vs「11 月 30 日前」（媒体）两套口径并排写，表体取 11/29",
     "状态": "live",
     "门槛": "224B 总参（含 64B Engram）/ 激活 12B · 1M 上下文 · 缓存命中 0.02 元 · 只在 WorkBuddy 内免，API 直调仍按价目计费"},
    {"分组": "api",
     "名称": "OpenCode Zen hy4-flash-free",
     "量": "零价（`-free` 池第 15 个）",
     "截止日": "",
     "截止说明": "未公布（官方免费池，随池调整、不预告）",
     "状态": "live",
     "门槛": "`-free` 目录 14 → 15 · 页 98,175 → 98,592 字（+417）· diff 10 行全落在一个模型块；池内模型随时下架，不承诺长期"},
    {"分组": "api",
     "名称": "Runware 4K 图像生成 5 折",
     "量": "4K 档 50% OFF（新挂徽标）",
     "截止日": "",
     "截止说明": "未公布（促销徽标，官网页未给结束日）",
     "状态": "live",
     "门槛": "页 771,942 字字节与 md5 全同、内容真变 —— 只换了徽标（旧「30% OFF」卸下）；三项不变量相同不能证「没变」"},
    {"分组": "api",
     "名称": "阿里 Qwen4-Max（可体验，非免费额度）",
     "量": "付费 $1.5 / $4.5 每百万 token（1M 上下文 · 原生视觉）",
     "截止日": "",
     "截止说明": "无截止日（付费旗舰；「小尺寸 Qwen4 将开源」是承诺、无型号无日期）",
     "状态": "pending",
     "门槛": "官方博客 free / 免费 0 命中 —— 只写「可在 QwenWork / Qoder / QwenStudio 使用」，只算可体验、不进免费清单"},
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

back = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(back) == 90, len(back)
assert all(b["分组"] in ("token", "api", "cloud", "subsidy", "edu", "oss", "over") for b in back)
stale = [b for b in back if b["截止日"] and b["状态"] != "over"
         and datetime.date.fromisoformat(b["截止日"]) < BASE]
assert not stale, [b["名称"] for b in stale]
print("quick ok | %d → %d 行 | 过期未收口 0 | 新增 4 条" % (len(rows) - 4, len(back)))
