# -*- coding: utf-8 -*-
"""077 期：总账与 4.2 同步（本期无新增条目）。

纪律（066/068/071/072/074/075/076 沿用）：
  ① 《总账》是状态快照、4.2 是本期变更 —— 同一行两处文字必须逐字一致；
  ② 同步按 `key()`（前 40 个中英数字符）匹配，**不按整行**；
  ③ 行名里的计数（`477/15/12`）在 4.2 与总账必须同值；
  ④ 改名要在同步之前做，否则 `key()` 变了、匹配不上；
  ⑤ 断言要在写盘之前全部核过；
  ⑥ 本期无补入行 → 条目数 `195` 不变。
"""
import io
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第077期-2026-11-23.md"
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

# ---- 行名里的计数必须两侧同值（本期 476/14/11 → 477/15/12）
assert md.count("`477/15/12`") == 1, md.count("`477/15/12`")
assert led.count("`476/14/11`") == 1, led.count("`476/14/11`")

i = md.index("### 4.2 常驻权益本期变更")
j = md.index("### ④ 本期第四章脚注")
r42_all = [l for l in md[i:j].split("\n")
           if l.startswith("|") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
print("4.2 行数：", len(r42_all))
assert len(r42_all) == 53, len(r42_all)

# ---- ③ 先改总账里的两处行名（OpenRouter 计数、OpenCode 说明）
led_lines = led.split("\n")
hit = [k for k, l in enumerate(led_lines) if "官方 API 目录口径" in l]
assert len(hit) == 1, hit
or_md = [l for l in r42_all if "官方 API 目录口径" in l]
assert len(or_md) == 1
or_name = cells(or_md[0])[0]
assert "477/15/12" in or_name, or_name
c = cells(led_lines[hit[0]])
assert len(c) == 3, c
led_lines[hit[0]] = "| %s | %s | %s |" % (or_name, c[1], c[2])

h2 = [k for k, l in enumerate(led_lines) if "`OpenCode` 免费模型清单" in l]
assert len(h2) == 1, h2
oc_md = [l for l in r42_all if '`OpenCode` 免费模型清单' in l]
assert len(oc_md) == 1
oc_name = cells(oc_md[0])[0]
assert "净减 `1` 条" in oc_name, oc_name
c2 = cells(led_lines[h2[0]])
assert len(c2) == 3, c2
led_lines[h2[0]] = "| %s | %s | %s |" % (oc_name, c2[1], c2[2])

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
        missing.append(cc[0][:44])
        continue
    r_norm = r if r.startswith("| ") else "| " + r[1:]
    if led_lines[p] != r_norm:
        led_lines[p] = r_norm
        updated += 1

print("总账同步：改写 %d 行；4.2 在总账里找不到 %d 行 %s" % (updated, len(missing), missing))
assert not missing, missing

body = "\n".join(led_lines).rstrip("\n") + "\n"

# ---- 表头与统计句（条目数不变，只推日期）
assert "**最后全量复核**：2026-11-22（第 076 期）" in body
body = body.replace("**最后全量复核**：2026-11-22（第 076 期）",
                    "**最后全量复核**：2026-11-23（第 077 期）")
for p in ("**条目数**：195", "这 195 条里本期真正发生变化的只有 53 条，其余 142 条",
          "## 一、全量表（195 条 · 按原文顺序）"):
    assert p in body, p

rows_before = len([l for l in body.split("\n") if l.startswith("| ")])
assert rows_before == 197, rows_before
for p in ("第 077 期", "**条目数**：195", "`477/15/12`", "净减 `1` 条", "$0.0375"):
    assert p in body, p

if DRY:
    print("DRY RUN —— 未写盘；表行数 %d" % rows_before)
    sys.exit(0)

io.open(LED, "w", encoding="utf-8", newline="\n").write(body)
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(LED, encoding="utf-8").read()
rows = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows == 197, rows
assert "`477/15/12`" in disk and "`476/14/11`" not in disk
print("ledger rows=%d | bytes=%d" % (rows, len(disk.encode())))
