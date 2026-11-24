# -*- coding: utf-8 -*-
"""第 078 期：quick_items.csv 增量（1 条新增 ERNIE 开放权重）+ 4 条更新。

纪律：
  - 新增条目无一来自「推断」：每条都能回到 078 期正文的表行或一手页逐字。
  - ERNIE 5.5 Flash Preview 权重：`Apache-2.0`、`280B/14B`、三仓 `11/23 17:00`（北京）。
  - `OpenRouter`：477/15/12 → **474/15/12**（全量 −3，三项持平）。
"""
import csv
import datetime
import io
import shutil
import sys

SRC = ".workbuddy/data/quick_items.csv"
BASE = datetime.date(2026, 11, 24)
COLS = ["分组", "名称", "量", "截止日", "截止说明", "状态", "门槛"]

rows = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(rows) == 104, len(rows)

NEW = [
    {
        "分组": "oss",
        "名称": "百度 ERNIE 5.5 Flash Preview 开放权重",
        "量": "280B 总参 / 14B 激活 · 1M 上下文 · Apache-2.0 · 128 个分片（共 142 文件）",
        "截止日": "",
        "截止说明": "无结束日（Apache-2.0 开放权重）；三仓北京 2026-11-23 17:00 上线，比官方承诺的 11/25 早 2 天",
        "状态": "live",
        "门槛": "能下载 ≠ 能本地跑：BF16 约 560GB、FP8 约 280GB；社区 GGUF 尚未出（unsloth 名下 ?search=ernie 为 0）；OpenRouter 另有 :free API 可用",
    },
]

hit_or = [k for k, r in enumerate(rows) if r["名称"] == "OpenRouter 免费档"]
assert len(hit_or) == 1, hit_or
rows[hit_or[0]]["量"] = "全量 474 个模型中 15 个零价 / 12 个带 :free 后缀（2026-11-24 实读，全量 −3、三项持平）"
rows[hit_or[0]]["门槛"] = ("注册，看 :free 后缀；本期出 3 进 0：kimi-k2 / kimi-k2-thinking / mimo-v2.5-pro 全部为付费模型；"
                          "dots-3-note-preview:free 仍在目录（裸冒号 404、%3A 200）；带冒号的 id 要用 %3A 请求")

hit_ink = [k for k, r in enumerate(rows) if r["名称"].startswith("Thinking Machines Inkling 2 Mini API")]
assert len(hit_ink) == 1, hit_ink
rows[hit_ink[0]]["量"] = ("4 个价点：$0.0375/$0.15、$0.075/$0.30、$0.15/$0.60（PrimeIntellect · fp4 · 1M ctx）｜"
                         "$0.12/$0.50（Io Net · nvfp4 · 256K ctx）")
rows[hit_ink[0]]["门槛"] = ("最便宜档与最贵档差 4.0 倍；本期顶档由 $0.12/$0.50 涨到 $0.15/$0.60（输入 +25.0%、输出 +20.0%）；"
                            "Io Net 未涨 → 由最贵变第二贵；无 :free 变体、无免费额度")

hit_ag = [k for k, r in enumerate(rows) if r["名称"].startswith("Google Antigravity 免费档三个第三方模型")]
assert len(hit_ag) == 1, hit_ag
rows[hit_ag[0]]["截止说明"] = ("官方脚注原为 November 30, 2026；078 期首页已 0 处、pricing 页 000（30 秒超时）—— 本期无法核实，"
                             "日期照留、不下「已取消」结论")

hit_w4 = [k for k, r in enumerate(rows) if r["名称"].startswith("智谱 AutoClaw 国内站 M11W4")]
assert len(hit_w4) == 1, hit_w4
rows[hit_w4[0]]["门槛"] = ("登录客户端即领，每账号一次；与 M11W3（到 11/22 23:59）只隔 1 分钟、不重叠；"
                         "额度锁在客户端、导不出 API；M11W5 连续第 3 期 404")

for n in NEW:
    rows.append(n)

if "--apply" not in sys.argv:
    print("DRY RUN ｜ 预计行数", len(rows), "｜新增", [n["名称"] for n in NEW])
    raise SystemExit(0)

shutil.copy(SRC, SRC + ".bak078")
with io.open(SRC, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)

back = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
assert len(back) == 105, len(back)
assert any(r["名称"].startswith("百度 ERNIE 5.5 Flash Preview 开放权重") for r in back)
assert any("474" in r["量"] for r in back)
assert any("$0.15/$0.60" in r["量"] for r in back)
print("quick items ok | rows =", len(back))
