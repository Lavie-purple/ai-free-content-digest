# -*- coding: utf-8 -*-
"""078 期：总账与 4.2 同步（本期补入 1 条：ERNIE-5.5-Flash-Preview 开放权重）。

纪律（066/068/071/072/074/075/076/077 沿用）：
  ① 《总账》是状态快照、4.2 是本期变更 —— 同一行两处文字必须逐字一致；
  ② 同步按 `key()`（前 40 个中英数字符）匹配，**不按整行**；
  ③ 行名里的计数（`474/15/12`）在 4.2 与总账必须同值；
  ④ 改名要在同步之前做，否则 `key()` 变了、匹配不上；
  ⑤ 断言要在写盘之前全部核过；
  ⑥ 本期补入 1 行 → 条目数 `195 → 196`，其余 `142 → 143`。
"""
import io
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第078期-2026-11-24.md"
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

# ---- ③ 先改总账里的行名（OpenRouter 计数）
led_lines = led.split("\n")
hit = [k for k, l in enumerate(led_lines) if "官方 API 目录口径" in l]
assert len(hit) == 1, hit
or_md = [l for l in r42_all if "官方 API 目录口径" in l]
assert len(or_md) == 1
or_name = cells(or_md[0])[0]
assert "474/15/12" in or_name, or_name
c = cells(led_lines[hit[0]])
assert len(c) == 3, c
assert "477/15/12" in c[0], c[0]
led_lines[hit[0]] = "| %s | %s | %s |" % (or_name, c[1], c[2])

# ---- ③-补 再改一行名：OpenCode 从「净减 1 条」变成「本期无进出」，key 也变了
h2 = [k for k, l in enumerate(led_lines) if "`OpenCode` 免费模型清单" in l]
assert len(h2) == 1, h2
oc_md = [l for l in r42_all if "`OpenCode` 免费模型清单" in l]
assert len(oc_md) == 1
oc_name = cells(oc_md[0])[0]
assert "本期无进出" in oc_name, oc_name
c2 = cells(led_lines[h2[0]])
assert len(c2) == 3, c2
led_lines[h2[0]] = "| %s | %s | %s |" % (oc_name, c2[1], c2[2])

# ---- ② 逐行同步（先同步已有行，再插入新行）
led_idx = {}
for k, l in enumerate(led_lines):
    if l.startswith("|"):
        cc = cells(l)
        if len(cc) >= 3:
            led_idx.setdefault(key(plain(EMOJI.sub("", cc[0]))), k)

updated, missing, new_rows = 0, [], []
for r in r42_all:
    cc = cells(r)
    k = key(plain(EMOJI.sub("", cc[0])))
    p = led_idx.get(k)
    if p is None:
        new_rows.append(r)
        continue
    r_norm = r if r.startswith("| ") else "| " + r[1:]
    if led_lines[p] != r_norm:
        led_lines[p] = r_norm
        updated += 1

print("总账同步：改写 %d 行；4.2 在总账里找不到 %d 行" % (updated, len(new_rows)))
assert len(new_rows) == 1, [x[:60] for x in new_rows]
assert "ERNIE-5.5-Flash-Preview" in new_rows[0]

# ---- 插入新行：紧跟 `ERNIE-5.5-Flash-Base` 那行（保持分组）
anchor = [k for k, l in enumerate(led_lines) if "百度开源 `ERNIE-5.5-Flash-Base`" in l]
assert len(anchor) == 1, anchor
new_norm = new_rows[0] if new_rows[0].startswith("| ") else "| " + new_rows[0][1:]
led_lines.insert(anchor[0] + 1, new_norm)

body = "\n".join(led_lines).rstrip("\n") + "\n"

# ---- 表头与统计句
assert "**最后全量复核**：2026-11-23（第 077 期）" in body
body = body.replace("**最后全量复核**：2026-11-23（第 077 期）",
                    "**最后全量复核**：2026-11-24（第 078 期）")
assert "**条目数**：195" in body
body = body.replace("**条目数**：195", "**条目数**：196")
assert "这 195 条里本期真正发生变化的只有 53 条，其余 142 条" in body
body = body.replace("这 195 条里本期真正发生变化的只有 53 条，其余 142 条",
                    "这 196 条里本期真正发生变化的只有 54 条，其余 143 条")
assert "## 一、全量表（195 条" in body
body = body.replace("## 一、全量表（195 条", "## 一、全量表（196 条")

rows_before = len([l for l in body.split("\n") if l.startswith("| ")])
assert rows_before == 198, rows_before
for p in ("第 078 期", "**条目数**：196", "`474/15/12`", "ERNIE-5.5-Flash-Preview", "441"):
    pass
assert "`474/15/12`" in body and "`477/15/12`" not in body
assert "ERNIE-5.5-Flash-Preview" in body

if DRY:
    print("DRY RUN —— 未写盘；表行数 %d" % rows_before)
    sys.exit(0)

io.open(LED, "w", encoding="utf-8", newline="\n").write(body)
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(LED, encoding="utf-8").read()
rows = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows == 198, rows
assert "`474/15/12`" in disk and "`477/15/12`" not in disk
print("ledger rows=%d | bytes=%d" % (rows, len(disk.encode())))
