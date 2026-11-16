# -*- coding: utf-8 -*-
"""070 期：总账与 4.2 同步 + 补 1 条 + 表头更新。

纪律：
  ① 《总账》是状态快照，4.2 是本期变更 —— **同一行的两处文字必须逐字一致**（066 期立的）；
  ② 同步按 `extract_deadlines.key()`（前 40 个中英数字符）匹配，**不按整行**；
  ③ 新行必须带「070 期」标记，否则下期 `split_ledger` 会判成「常驻未变」；
  ④ 落盘后复读断言行数；
  ⑤ **070 期新增**：行名里的计数（`468/17/14`）必须**同时在 4.2 与总账**改名 ——
     只改一处会让下期 CSV 多算一行（068 期踩过）。
"""
import io
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第070期-2026-11-16.md"
LED = WS + "常驻权益总账.md"
DRY = "--apply" not in sys.argv

KEEP = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff]+")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF]\uFE0F?")


def key(s):
    return KEEP.sub("", s).lower()[:40]


def plain(s):
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return s.strip()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
led = io.open(LED, encoding="utf-8").read().replace("\r\n", "\n")

# ---- ⑤ 行名里的计数同步改名（两处必须一起改）
assert md.count("`471/17/14`") == 1, md.count("`471/17/14`")
md = md.replace("`471/17/14`", "`468/17/14`")
assert led.count("`471/17/14`") == 1, led.count("`471/17/14`")
led = led.replace("`471/17/14`", "`468/17/14`")

led_lines = led.split("\n")

i = md.index("### 4.2 常驻权益本期变更")
j = md.index("### ④ 本期第四章脚注")
r42 = [l for l in md[i:j].split("\n")
       if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
print("4.2 行数：", len(r42))

led_idx = {}
for k, l in enumerate(led_lines):
    if l.startswith("| "):
        c = cells(l)
        if len(c) >= 3:
            led_idx.setdefault(key(plain(EMOJI.sub("", c[0]))), k)

updated, missing = 0, []
for r in r42:
    c = cells(r)
    k = key(plain(EMOJI.sub("", c[0])))
    p = led_idx.get(k)
    if p is None:
        if "070 期" not in r:
            missing.append(c[0][:40])
        continue
    if led_lines[p] != r:
        led_lines[p] = r
        updated += 1

print("总账同步：改写 %d 行；4.2 在总账里找不到 %d 行 %s" % (updated, len(missing), missing))
assert not missing, missing

NEW = [
    "| 🟡 **阿里 `Qwen4-Max` 发布（**`2.4T` 主干 / 每 token 激活 `71B` + `328B` `N-Gram Embedding` · `1M` 上下文 · 原生视觉 · `$1.5` / `$4.5` 每百万 token**）** "
    "| **无截止日（付费旗舰；「小尺寸 `Qwen4` 将开源」是承诺、**无型号无日期**）** "
    "| 🟡 **（070 期补入）**付费**模型 —— 官方博客 `free` / `免费` **`0` 命中**，只写「可在 `QwenWork` / `Qoder` / `QwenStudio` 使用」，"
    "**本报只写「可体验」、不进免费清单**（避坑 304）。 能拿走的两件：`Qwen-Live-Delivery-Plugin` 官方逐字 `open-sourcing`（**仓库地址未给、未取 `spdx`**）、"
    "**「`Smaller models … are coming to open source`」**。 成本降幅两套口径：美元 `$4.43 → $1.67`（`−62%`）/ 人民币 `26.58 → 11.16` 元（`−58%`），**不合并**。 "
    "[附录 070](details.html)  |",
]

body = "\n".join(led_lines).rstrip("\n")
body = body + "\n" + "\n".join(NEW) + "\n"

body = body.replace("**最后全量复核**：2026-11-15（第 069 期）", "**最后全量复核**：2026-11-16（第 070 期）")
body = body.replace("**条目数**：181", "**条目数**：182")
body = body.replace("这 181 条里本期真正发生变化的只有 39 条", "这 182 条里本期真正发生变化的只有 40 条")
body = body.replace("## 一、全量表（181 条 · 按原文顺序）", "## 一、全量表（182 条 · 按原文顺序）")

if DRY:
    print("DRY RUN —— 未写盘；预计行数 %d" % len([l for l in body.split("\n") if l.startswith("| ")]))
    sys.exit(0)

io.open(LED, "w", encoding="utf-8", newline="\n").write(body)
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(LED, encoding="utf-8").read()
rows = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows == 184, rows  # 182 条 + 表头 2 行
for p in ("Qwen4-Max", "第 070 期", "**条目数**：182", "全量表（182 条", "`468/17/14`"):
    assert p in disk, p
print("ledger rows=%d | bytes=%d" % (rows, len(disk.encode())))
