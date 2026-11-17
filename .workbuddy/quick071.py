# -*- coding: utf-8 -*-
"""第 071 期：quick_items.csv 增量（4 条）+ Runware 4K 补上官方截止日。

纪律：
  - 新增条目无一来自「推断」：每条都能回到 071 期正文的表行或一手页逐字。
  - 「今天到期 ≠ 已结束」：`Runware 4K 50% OFF` 的 `endsAt: "2026-11-17"` 今天 23:59 前仍在售，
    所以**不置 over**，只把 070 期写「未公布」的截止日补成官方逐字，等 072 期收口。
"""
import csv, io, datetime, shutil

SRC = ".workbuddy/data/quick_items.csv"
BASE = datetime.date(2026, 11, 17)
COLS = ["分组", "名称", "量", "截止日", "截止说明", "状态", "门槛"]

rows = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(rows) == 90, len(rows)

# 1) Runware 4K：070 期写「未公布（促销徽标，官网页未给结束日）」，本期在促销数组里读到 endsAt
hit = 0
for r in rows:
    if r["名称"].startswith("Runware 4K 图像生成"):
        assert r["状态"] == "live", r["状态"]
        assert r["截止日"] == "", r["截止日"]
        r["截止日"] = "2026-11-17"
        r["截止说明"] = ("11/17（促销数组 `endsAt: \"2026-11-17\"` ＋卡片 `title` 逐字"
                     "「until November 17, 2026」；**今天最后一天**）")
        r["量"] = "4K 档 50% OFF（数组 20 → 22 条，本条 `endsAt` 首次读到官方日期）"
        hit += 1
assert hit == 1, hit

NEW = [
    {"分组": "token",
     "名称": "智谱 AutoClaw 国内站 M11W3 每周福利（100M Tokens）",
     "量": "100M Tokens ＝ 10,000 积分（本周额度是上周同类活动的 2 倍）",
     "截止日": "2026-11-22",
     "截止说明": ("11/22 23:59（北京时间 · 官方逐字「活动时间 11 月 16 日（周一）00:00—"
              "11 月 22 日（周日）23:59」；奖励同日 23:59 失效）"),
     "状态": "live",
     "门槛": "登录即可领取、每账号限领一次；**只在 AutoClaw 内使用**，自接 Coding Plan 或其他 API 另计费"},
    {"分组": "api",
     "名称": "Google Antigravity 免费档三个第三方模型 11/18 移除",
     "量": "免费档 $0/month 不变；Claude Sonnet 4.6 / Claude Opus 4.6 / GPT-OSS-120b 三个模型下架",
     "截止日": "2026-11-18",
     "截止说明": ("11/18（角标 `title` 逐字 `Will be removed on November 18, 2026.`；"
              "**正文无此句、可见文本只是一个「4」**）"),
     "状态": "live",
     "门槛": ("免费档剩 Gemini 3.8 Flash；页 214,361 → 178,404 字节。"
              "查「免费档含哪些模型」必须同时读 `title` / `aria-label`，只抽可见文本读不到")},
    {"分组": "edu",
     "名称": "OpenAI ChatGPT for Academic Researchers 扩容至 20 万研究者",
     "量": "本轮 50,000 个名额、每名额带 2 名协作者（合计最多 150,000 人）；档位是 Plus",
     "截止日": "",
     "截止说明": "无截止日（名额制、先到先得；官方未给申请关闭日）—— 11/23 是开放申请日，不是截止日",
     "状态": "live",
     "门槛": ("**档位从 Pro 降到 Plus**（官方逐字 `most participants would have stayed within "
              "ChatGPT Plus usage limits`）；额度无数字、模型只写 `frontier models`；抽签改先到先得")},
    {"分组": "api",
     "名称": "腾讯 Hy4 flash 进入 OpenRouter 目录（付费 · 标价五折）",
     "量": "输入 $0.035 / 输出 $0.1405 每百万 token（≈ 官方人民币价五折）",
     "截止日": "",
     "截止说明": "无截止日（目录标价，未挂 `discount`、无 `:free` 变体）",
     "状态": "pending",
     "门槛": ("**付费条目**，进目录 ≠ 免费；`created` 换北京 11/16 22:18。"
              "按 7.1 折算正好是官方 0.5 元 / 2 元的一半 —— **汇率 7.1 是本报假设**")},
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
assert len(back) == 94, len(back)
assert all(b["分组"] in ("token", "api", "cloud", "subsidy", "edu", "oss", "over") for b in back)
stale = [b for b in back if b["截止日"] and b["状态"] != "over"
         and datetime.date.fromisoformat(b["截止日"]) < BASE]
assert not stale, [(b["名称"][:20], b["截止日"]) for b in stale]
assert any(b["分组"] == "edu" and "Academic" in b["名称"] for b in back), "edu 新增未落盘"
print("quick ok | 90 → %d 行 | 补截止日 1 条 | 新增 4 条 | 过期未收口 0" % len(back))
