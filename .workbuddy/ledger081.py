# -*- coding: utf-8 -*-
"""081 期：总账与 4.2 同步（无补入、无移出；改 3 处行名）。

纪律（066/068/071/072/074/075/076/077/078/079/080 沿用）：
  ① 《总账》是状态快照、4.2 是本期变更 —— 同一行两处文字必须逐字一致；
  ② 同步按 `key()`（前 40 个中英数字符）匹配，**不按整行**；
  ③ 行名里的计数（`477/14/11`、`6 个 provider`、`本期 +1`）在两处必须同值 —— **改名要先改总账，再同步**；
  ④ 条目数不变（196），4.2 条数不变（54）。
"""
import io
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第081期-2026-11-27.md"
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

led_lines = led.split("\n")

# ---- ③ 先改总账里的行名（三处）
RENAME = [("官方 API 目录口径", "OpenRouter 计数"),
          ("`Free models` 段", "OpenCode 条数"),
          ("个 provider", "inkling 价点数")]
for needle, tag in RENAME:
    hit = [k for k, l in enumerate(led_lines) if needle in l]
    assert len(hit) == 1, (tag, len(hit))
    or_md = [l for l in r42_all if needle in l]
    assert len(or_md) == 1, (tag, "md 命中", len(or_md))
    or_name = cells(or_md[0])[0]
    c = cells(led_lines[hit[0]])
    assert len(c) == 3, (tag, len(c))
    assert c[0] != or_name, (tag, "行名未变")
    led_lines[hit[0]] = "| %s | %s | %s |" % (or_name, c[1], c[2])
    print("改名：", tag, "→", or_name[:60])

# ---- ② 逐行同步
led_idx = {}
for p, line in enumerate(led_lines):
    if line.startswith("| ") and not line.startswith("| 活动 |") and not line.startswith("| --- |"):
        cc = cells(line)
        led_idx[key(plain(EMOJI.sub("", cc[0])))] = p

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
assert "**最后全量复核**：2026-11-26（第 080 期）" in body
body = body.replace("**最后全量复核**：2026-11-26（第 080 期）",
                    "**最后全量复核**：2026-11-27（第 081 期）")
assert "**条目数**：196" in body
assert "这 196 条里本期真正发生变化的只有 54 条，其余 142 条" in body

rows = len([l for l in body.split("\n") if l.startswith("| ")])
assert rows == 198, rows
assert "`477/14/11`" in body and "`474/14/11`" not in body
assert "`6` 个 provider" in body and "`7` 个 provider" not in body

if DRY:
    print("DRY RUN —— 未写盘；表行数 %d；同步 %d 行" % (rows, updated))
    sys.exit(0)

io.open(LED, "w", encoding="utf-8", newline="\n").write(body)

disk = io.open(LED, encoding="utf-8").read()
rows2 = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows2 == 198, rows2
assert "`477/14/11`" in disk and "`474/14/11`" not in disk
print("ledger rows=%d | bytes=%d | synced=%d" % (rows2, len(disk.encode()), updated))
