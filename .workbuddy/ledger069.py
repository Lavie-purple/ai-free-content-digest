# -*- coding: utf-8 -*-
"""069 期：总账与 4.2 同步 + 补 2 条 + 表头更新。

纪律：
  ① 《总账》是状态快照，4.2 是本期变更 —— **同一行的两处文字必须逐字一致**（066 期立的）；
  ② 同步按 `extract_deadlines.key()`（前 40 个中英数字符）匹配，**不按整行**；
  ③ 新行必须带「069 期」标记，否则下期 `split_ledger` 会判成「常驻未变」；
  ④ 落盘后复读断言行数。
"""
import io
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第069期-2026-11-15.md"
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
        # 本期补登的新行本来就不在总账里 —— 下面 NEW 会补进去
        if "069 期" not in r:
            missing.append(c[0][:40])
        continue
    if led_lines[p] != r:
        led_lines[p] = r
        updated += 1

print("总账同步：改写 %d 行；4.2 在总账里找不到 %d 行 %s" % (updated, len(missing), missing))
assert not missing, missing

NEW = [
    "| 🟢 **美团 `LongCat-2.5` 以 `MIT` 公开权重（**`1.6T` 总参 / `48B` 激活 · `1M` 上下文 · 文本 + 图 + 视频 · `231` 个文件**）** "
    "| **无截止日（开放权重，官方未给回收 / 下线日）** "
    "| 🟢 **（069 期补登）`cardData.license = mit`、`gated: false`、两个仓各 `231` 个文件；`downloads 1,573` / `likes 267`。 "
    "`Terminal Bench v2.1` `88.4`（官方自测）；样例部署 `194` 张华为昇腾 `Atlas A2`、**无 `Nvidia` 指引**。 "
    "**四个时间点分开写**：建仓 `11/04 11:48Z`、最后变更 `11/10 07:28Z`（065 期窗口内）、媒体稿 `11/15 10:06Z`、**一手页无「发布日期」字段**。 "
    "[附录 069](details.html)  |",
    "| 🟢 **MIT 韩松团队 `PEAR` 开放权重 + 代码（**`Qwen3.8-27B` + 仿真 RL · `Apache-2.0` · `5090` 上 `220+` tok/s**）** "
    "| **无截止日（开放权重，官方未给回收 / 下线日）** "
    "| 🟢 **（069 期补登）`GitHub` `mit-han-lab/pear` 建仓 `11/13 17:43:06Z`、`pushed_at 17:43:22Z`（相隔 `16` 秒）、`stars 240`；"
    "`LICENSE` 原文 `11,544` 字节已读（Apache 2.0）。 `HF` 集合三条（`27.36B` / `-LIBERO_only` / `-NVFP4` `18.16B`）。 "
    "`LIBERO` 零样本 `1.6% → 74.4%`；真机 `YAM` `30` 次成功 `18` 次。 **时间点 `11/14 01:43` 北京，落在 068 期窗口内。** "
    "[附录 069](details.html)  |",
]

body = "\n".join(led_lines).rstrip("\n")
body = body + "\n" + "\n".join(NEW) + "\n"

# 表头与计数
body = body.replace("**最后全量复核**：2026-11-14（第 068 期）", "**最后全量复核**：2026-11-15（第 069 期）")
body = body.replace("**条目数**：179", "**条目数**：181")
body = body.replace("这 179 条里本期真正发生变化的只有 37 条", "这 181 条里本期真正发生变化的只有 39 条")
body = body.replace("## 一、全量表（179 条 · 按原文顺序）", "## 一、全量表（181 条 · 按原文顺序）")

if DRY:
    print("DRY RUN —— 未写盘；预计行数 %d" % len([l for l in body.split("\n") if l.startswith("| ")]))
    sys.exit(0)

io.open(LED, "w", encoding="utf-8", newline="\n").write(body)
disk = io.open(LED, encoding="utf-8").read()
rows = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows == 183, rows  # 181 条 + 表头 2 行
for p in ("PEAR", "LongCat-2.5", "第 069 期", "**条目数**：181", "全量表（181 条"):
    assert p in disk, p
print("ledger rows=%d | bytes=%d" % (rows, len(disk.encode())))
