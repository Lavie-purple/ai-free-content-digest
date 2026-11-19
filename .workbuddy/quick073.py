# -*- coding: utf-8 -*-
"""第 073 期：quick_items.csv 增量（3 条）+ MiniMax 4K 收口 + Antigravity 去日期化。

纪律：
  - 新增条目无一来自「推断」：每条都能回到 073 期正文的表行或一手页逐字。
  - `MiniMax` 4K：本期核到已撤净（价目回位、徽标清零）→ **置 over**。
  - `Antigravity` 三模型：**到期未执行**、官方未给新日期 → **截止日清空**，
    说明里写清「官方写 11/18 移除、至今未执行」；不置 over（模型仍可用）。
"""
import csv, io, datetime, shutil

SRC = ".workbuddy/data/quick_items.csv"
BASE = datetime.date(2026, 11, 19)
COLS = ["分组", "名称", "量", "截止日", "截止说明", "状态", "门槛"]

rows = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(rows) == 97, len(rows)

# 1) MiniMax 4K：已撤净 → 收口
hit = 0
for r in rows:
    if r["名称"].startswith("MiniMax H3-Image 4K 五折"):
        r["量"] = "4K 文生图 0.4522 元/张（原价）· 编辑 0.4809 / 0.5211；**五折已撤**"
        r["截止说明"] = ("11/18 00:00 到期；**本期核到已撤净**：`0.2261` / `0.2404` / `限时5折` 整页 0 命中，"
                     "`6` 处徽标清零，页 311,607 → 305,754 字节")
        r["状态"] = "over"
        r["门槛"] = ("按原价预算，**不要沿用上期折后价**。要求最终交付图片宽 × 高 ≥ 1660 万像素。"
                  "撤回落在 11/18 18:10–11/19 16:55 之间（截止后 18–41 小时），非「改日期续期」")
        hit += 1
assert hit == 1, hit

# 2) Antigravity：到期未执行 → 清空截止日
hit = 0
for r in rows:
    if r["名称"].startswith("Google Antigravity 免费档三个第三方模型"):
        r["截止日"] = ""
        r["截止说明"] = ("官方脚注逐字 `Will be removed on November 18, 2026.`，**到期日已过 1 天、三个模型仍在**"
                     "（`Sonnet 4.6` / `Opus 4.6` / `GPT-OSS-120b`），官方未给新日期")
        r["状态"] = "live"
        r["门槛"] = ("定价页本期恢复 200（183,218 字节 / 可见文本 12,481 字符）；免费档仍 4 个模型、`$0/month`、"
                  "配额无数值。**当「随时可能没」用，不当「承诺保留」**（避坑 313）")
        hit += 1
assert hit == 1, hit

NEW = [
    {"分组": "api",
     "名称": "DeepSeek 服务端搜索 / 抓取不计费",
     "量": "调用模型时触发的 `web tools` / `web_search` 不再单独计费（原 $0.75 / 千次归零）",
     "截止日": "",
     "截止说明": "11/18 12:00（北京）起生效；结果并入上下文按 token 计",
     "状态": "live",
     "门槛": ("**单独调 `Search` / `Fetch` API 仍 $0.75 / 千次**（同页表未变）。"
              "免的是「模型自己搜」，不是「你去搜」；读进去的正文仍按 token 收")},
    {"分组": "oss",
     "名称": "范式 Phai-A1-35B-1M 开放权重",
     "量": "35.1B 全 BF16 / 1M 上下文 / Apache-2.0 / 28 个文件",
     "截止日": "",
     "截止说明": "无截止日（权重永久开放）；建仓 11/12，公开日 11/19",
     "状态": "live",
     "门槛": ("**「单张 3090」需 4bit 量化**：BF16 权重 70.2 GB vs 显存 24 GB（避坑 316）。"
              "底座 `Qwen3.6-35B-A3B`；`Phai-M1`（视频）仓未检索到，记预告")},
    {"分组": "oss",
     "名称": "MatOS 材料科研智能体（开源）",
     "量": "3,135 数据集 / 386 技能 / 104 工作流 / 51 角色 / 48 款计算软件",
     "截止日": "",
     "截止说明": "无截止日（arXiv + GitHub 双开源）",
     "状态": "live",
     "门槛": ("基准均在同底座前提下：ResearchClawBench +33.6%、材料任务 +80.8%；DuoCompNet MAE 低 13.6%。"
              "**开源 ≠ 免费算力**，要自己的模型与机器")},
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

# 回读断言（053/054）
back = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(back) == 100, len(back)
assert all(b["分组"] in ("token", "api", "cloud", "subsidy", "edu", "oss", "over") for b in back)
stale = [b for b in back if b["截止日"] and b["状态"] != "over"
         and datetime.date.fromisoformat(b["截止日"]) < BASE]
assert not stale, [(b["名称"][:20], b["截止日"]) for b in stale]
assert any("Phai-A1" in b["名称"] for b in back), "Phai 未落盘"
assert any(b["名称"].startswith("MiniMax H3-Image 4K") and b["状态"] == "over" for b in back), "MiniMax 未收口"
print("quick ok | 97 → %d 行 | 收口 1 条 | 去日期 1 条 | 新增 3 条 | 过期未收口 0" % len(back))
