# -*- coding: utf-8 -*-
"""079 期：总账与 4.2 同步（无补入、无移出；改 1 处行名）。

纪律（066/068/071/072/074/075/076/077/078 沿用）：
  ① 《总账》是状态快照、4.2 是本期变更 —— 同一行两处文字必须逐字一致；
  ② 同步按 `key()`（前 40 个中英数字符）匹配，**不按整行**；
  ③ 行名里的计数（`472/14/11`）在 4.2 与总账必须同值 —— **改名要先改总账，再同步**；
  ④ 条目数不变（196），4.2 条数不变（54），只有「本期改写 N 条」变化。
"""
import io
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第079期-2026-11-25.md"
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

i = md.index("### 4.2 常驻权益本期变更")
j = md.index("### ④ 本期第四章脚注")
r42_all = [l for l in md[i:j].split("\n")
           if l.startswith("|") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
print("4.2 行数：", len(r42_all))
assert len(r42_all) == 54, len(r42_all)

# ---- ③ 先改总账里的行名（OpenRouter 计数 474/15/12 → 472/14/11）
led_lines = led.split("\n")
hit = [k for k, l in enumerate(led_lines) if "官方 API 目录口径" in l]
assert len(hit) == 1, hit
or_md = [l for l in r42_all if "官方 API 目录口径" in l]
assert len(or_md) == 1
or_name = cells(or_md[0])[0]
assert "472/14/11" in or_name, or_name
c = cells(led_lines[hit[0]])
assert len(c) == 3, c
assert "474/15/12" in c[0], c[0]
led_lines[hit[0]] = "| %s | %s | %s |" % (or_name, c[1], c[2])

# ---- ② 逐行同步
led_idx = {}
for k, l in enumerate(led_lines):
    if l.startswith("|"):
        cc = cells(l)
        if len(cc) >= 3:
            led_idx.setdefault(key(plain(EMOJI.sub("", cc[0]))), k)

updated, missing = 0, []
for r in r42_all:
    cc = cells(r)
    k = key(plain(EMOJI.sub("", cc[0])))
    p = led_idx.get(k)
    if p is None:
        missing.append(cc[0][:50])
        continue
    r_norm = r if r.startswith("| ") else "| " + r[1:]
    if led_lines[p] != r_norm:
        led_lines[p] = r_norm
        updated += 1

print("总账同步：改写 %d 行；4.2 在总账里找不到 %d 行" % (updated, len(missing)))
assert not missing, missing

body = "\n".join(led_lines).rstrip("\n") + "\n"

# ---- 表头与统计句
assert "**最后全量复核**：2026-11-24（第 078 期）" in body
body = body.replace("**最后全量复核**：2026-11-24（第 078 期）",
                    "**最后全量复核**：2026-11-25（第 079 期）")
assert "**条目数**：196" in body
assert "这 196 条里本期真正发生变化的只有 54 条，其余 143 条" in body
body = body.replace("这 196 条里本期真正发生变化的只有 54 条，其余 143 条",
                    "这 196 条里本期真正发生变化的只有 54 条，其余 142 条")

rows = len([l for l in body.split("\n") if l.startswith("| ")])
assert rows == 198, rows
assert "`472/14/11`" in body and "`474/15/12`" not in body

if DRY:
    print("DRY RUN —— 未写盘；表行数 %d；同步 %d 行" % (rows, updated))
    sys.exit(0)

io.open(LED, "w", encoding="utf-8", newline="\n").write(body)

disk = io.open(LED, encoding="utf-8").read()
rows2 = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows2 == 198, rows2
assert "`472/14/11`" in disk and "`474/15/12`" not in disk
print("ledger rows=%d | bytes=%d | synced=%d" % (rows2, len(disk.encode()), updated))
