# -*- coding: utf-8 -*-
"""071 期：总账与 4.2 同步 + 补 2 条 + 表头更新。

纪律：
  ① 《总账》是状态快照，4.2 是本期变更 —— **同一行的两处文字必须逐字一致**（066 期立的）；
  ② 同步按 `key()`（前 40 个中英数字符）匹配，**不按整行**；
  ③ 新行必须带「071 期」标记，否则下期 `split_ledger` 会判成「常驻未变」；
  ④ 落盘后复读断言行数；
  ⑤ **行名里的计数（`468/17/14`）必须同时在 4.2 与总账改名**（068 期踩过多算一行的坑）。
"""
import io
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第071期-2026-11-17.md"
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
# 071 期：gen_table071 已把 4.2 的行名改成 470；此处只补「还没改」的情况
if md.count("`468/17/14`"):
    assert md.count("`468/17/14`") == 1, md.count("`468/17/14`")
    md = md.replace("`468/17/14`", "`470/17/14`")
assert md.count("`470/17/14`") == 1, md.count("`470/17/14`")
assert led.count("`468/17/14`") == 1, led.count("`468/17/14`")
led = led.replace("`468/17/14`", "`470/17/14`")

led_lines = led.split("\n")

i = md.index("### 4.2 常驻权益本期变更")
j = md.index("### ④ 本期第四章脚注")
r42 = [l for l in md[i:j].split("\n")
       if l.startswith("|") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
print("4.2 行数：", len(r42))
assert len(r42) == 42

led_idx = {}
for k, l in enumerate(led_lines):
    if l.startswith("|"):
        c = cells(l)
        if len(c) >= 3:
            led_idx.setdefault(key(plain(EMOJI.sub("", c[0]))), k)

updated, missing = 0, []
for r in r42:
    c = cells(r)
    k = key(plain(EMOJI.sub("", c[0])))
    p = led_idx.get(k)
    if p is None:
        if "071 期" not in r:
            missing.append(c[0][:40])
        continue
    r_norm = r if r.startswith("| ") else "| " + r[1:]
    if led_lines[p] != r_norm:
        led_lines[p] = r_norm
        updated += 1

print("总账同步：改写 %d 行；4.2 在总账里找不到 %d 行 %s" % (updated, len(missing), missing))
assert not missing, missing

NEW = [
    "| 🟡 **OpenAI `ChatGPT for Academic Researchers` 扩容至最多 `20` 万研究者（**本轮 `50,000` 个名额 · 每名额带 `2` 名协作者**）** "
    "| **无截止日（名额制：`11/23` 开放申请、先到先得；官方未给申请关闭日）** "
    "| 🟡 **（071 期补入）名额 `3` 个数不可互换**：`20` 万＝项目总目标、`5` 万＝本轮新增、`15` 万＝本轮可覆盖人数（`5` 万 × `3`）。 "
    "**档位从 `Pro` 降到 `Plus`**（官方逐字「`most participants would have stayed within ChatGPT Plus usage limits`」）；**可用模型只写「`frontier models`」、额度无数字**。 "
    "试点 `20,000` 人 / `33` 国（7 月起）；**由抽签改为先到先得**。 默认不用于训练（`by default`，留口子）。 [附录 071](details.html) |",
    "| 🟡 **腾讯 `Hy4 flash` 进入 `OpenRouter` 目录（**`tencent/hy4-flash` · 标价 ≈ 官方人民币价五折 · **付费**）** "
    "| **无截止日（目录标价，未挂 `discount`、无 `:free` 变体）** "
    "| 🟡 **（071 期补入）`created` 换北京 `11/16 22:18`**（晚于 070 期截止 `17:50`）。 标价：输入 `$0.035` / 输出 `$0.1405`（每百万 token）；"
    "**按 `7.1` 折算，正好是官方 `0.5` 元 / `2` 元的一半** → **`TokenHub` 的 `5` 折被写进标价**，不是促销字段（避坑 307）。 **汇率 `7.1` 是本报假设**，官方未给换算口径。 [附录 071](details.html) |",
]

body = "\n".join(led_lines).rstrip("\n")
body = body + "\n" + "\n".join(NEW) + "\n"

body = body.replace("**最后全量复核**：2026-11-16（第 070 期）", "**最后全量复核**：2026-11-17（第 071 期）")
body = body.replace("**条目数**：182", "**条目数**：184")
body = body.replace("这 182 条里本期真正发生变化的只有 40 条，其余 142 条", "这 184 条里本期真正发生变化的只有 42 条，其余 142 条")
body = body.replace("## 一、全量表（182 条 · 按原文顺序）", "## 一、全量表（184 条 · 按原文顺序）")

if DRY:
    print("DRY RUN —— 未写盘；预计行数 %d" % len([l for l in body.split("\n") if l.startswith("| ")]))
    sys.exit(0)

io.open(LED, "w", encoding="utf-8", newline="\n").write(body)
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(LED, encoding="utf-8").read()
rows = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows == 186, rows  # 184 条 + 表头 2 行
for p in ("ChatGPT for Academic Researchers", "第 071 期", "**条目数**：184", "全量表（184 条", "`470/17/14`", "tencent/hy4-flash"):
    assert p in disk, p
print("ledger rows=%d | bytes=%d" % (rows, len(disk.encode())))
