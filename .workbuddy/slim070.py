# -*- coding: utf-8 -*-
"""070 期：把 7 条 R1 超长的状态列压回 200 字以内（两轮收敛）。

纪律（052/054）：
  · 键按「活动名唯一子串 + 旧状态前缀」双条件定位，命中必须恰好 1 行；
  · 改完**回读落盘文件**再断言，不信任内存变量；
  · 被裁掉的论证**一字不删**，原文进 tmp_070_slim.json，由 appendix070.py 落进附录。
"""
import io
import json
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第070期-2026-11-16.md"
OUT = WS + ".workbuddy/tmp_070_slim.json"

A = " [附录 070](details.html)"


def plain(s):
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s).strip()


# (活动名唯一子串, 旧状态前缀, 新状态)
REWRITE = [
    ("OpenRouter 免费档",
     "🟢 **全量 `470 → 468`",
     "🟢 **全量 `470 → 468`；`:free` `14`（第 `3` 天不变）、零价 `17`、`max_price=0` `16`。 "
     "进 `1` 出 `3`：进 `qwen/qwen4-max`（**付费**）；出 `qwen3-vl-30b` / `step-3.5-flash` / `hunyuan-a13b` 三条同族旧款 —— "
     "**换代，不是免费区缩水**。 `Ling 3.2` 空 `3` 天、权重仓仍 `404`。" + A + "**"),

    ("阿里 `Qwen4-Max` 发布",
     "🟡 **（070 期补入）**付费**模型",
     "🟡 **（070 期补入）**付费**模型：官方博客 `free` / `免费` `0` 命中，只写「可在 `QwenWork` / `Qoder` / `QwenStudio` 使用」—— "
     "**只写「可体验」、不进免费清单**（避坑 304）。 能拿走：`Live-Delivery` 插件已开源（**地址未给**）、「小尺寸 `Qwen4` 将开源」（**无型号无日期**）。 "
     "降本 `−62%`（美元）/ `−58%`（人民币）两套口径，**不合并**。" + A + "**"),

    ("腾讯混元 `Hy4 flash`",
     "🟠 **距截止 `13` 天。 （070 期补入）",
     "🟠 **距截止 `13` 天。 （070 期补入）限免只限 `WorkBuddy` 内的 `Hy4 flash`**；其他模型与腾讯云 `TokenHub` 不在内"
     "（`TokenHub` 是**限时 `5` 折**）。 同日 `OpenCode Zen` 另有 `hy4-flash-free`（**零留存**）。 "
     "⚠️ 官网是 `JS` 壳，**参数与价格只能引媒体**。" + A + "**"),

    ("MIT 韩松团队 `PEAR`",
     "🟢 **已公开（069 期补登）",
     "🟢 **已公开（069 期补登）。 `stars 240 → 442`、`forks 32`、**`pushed_at` 首次更新（`11/16 07:54:56Z`）**；"
     "`LICENSE` 原文 `11,544` 字节已读（Apache 2.0）。 `LIBERO` `1.6% → 74.4%`；真机 `YAM` `30` 试成 `18`；**不用遥操、不用真机数据**。" + A + "**"),

    ("`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日",
     "🟡 **第三方聚合层 · 逐条标核实日。 第 `8` 期：`¥2433 → ¥1760`（`−673`）、卡册 `60` 张、"
     "日戳 `11/16` `20` / `11/15` `22` / `11/14` `72` / `11/13` `2` / `11/9` `4` ＝ `120`。 "
     "**首次「面额与卡数同降」**；`11/14` 由 `108` 掉到 `72`、`11/15` 由 `6` 涨到 `22` —— 日戳会被**重新盖章**。" + A + "**"),

    ("百度 `ERNIE 5.5 Flash Preview` 发布",
     "🟢 **生效中（距承诺日 `9` 天）",
     "🟢 **生效中（距承诺日 `9` 天）。 （066 期补入）发布页 `11月25日前开源` 逐字仍在**；"
     "**权重仍未放**：`?author=baidu` 仍 `39` 仓，两仓 `downloads` 冻结、`likes` 仍涨（`324` / `394`）。" + A + "**"),

    ("`Google Antigravity` 个人免费档",
     "🟢 **官方定价页逐字 `$0/month`",
     "🟢 **官方定价页逐字 `$0/month`。 含 `Unlimited Tab` / `Unlimited Command` / **`Basic weekly rate limits`**；"
     "`free` 整页 `0` 命中；额度无数字。 **字节 + `md5` 与上期全同（第 `5` 期同值）**，不写档位。" + A + "**"),
]

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


rows = md.split("\n")
items = []
for tag, old_prefix, new in REWRITE:
    hits = [k for k, l in enumerate(rows) if l.startswith("| ") and tag in l and old_prefix in l]
    assert len(hits) == 1, ("命中数不是 1", tag, len(hits))
    c = cells(rows[hits[0]])
    assert len(c) == 3, ("字段数异常", tag, len(c))
    assert "|" not in new, ("新状态列里出现竖线", tag)
    old_status = c[2]
    rows[hits[0]] = "|%s|%s| %s" % (c[0], c[1], new)
    items.append({"name": c[0], "old": old_status, "new": new,
                  "before": len(plain(old_status)), "after": len(plain(new))})
    print("%-34s %3d → %3d 字" % (tag, items[-1]["before"], items[-1]["after"]))
    assert items[-1]["after"] <= 195, ("压完仍超 195", tag, items[-1]["after"])

assert len(items) == 7, len(items)
io.open(MD, "w", encoding="utf-8", newline="\n").write("\n".join(rows))
io.open(OUT, "w", encoding="utf-8").write(json.dumps(items, ensure_ascii=False, indent=1))

# ---- 回读落盘再断言（052 期纪律）
disk = io.open(MD, encoding="utf-8").read()
for it in items:
    assert it["new"].rstrip()[:60] in disk, it["name"]
    assert it["old"] not in disk, ("旧状态列仍在盘上", it["name"])
print("slim ok |", len(items), "条 | json", OUT)
