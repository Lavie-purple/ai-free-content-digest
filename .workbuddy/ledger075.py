# -*- coding: utf-8 -*-
"""075 期：总账与 4.2 同步 + 补 2 条 + 表头更新。

纪律（066/068/071/072/074 沿用）：
  ① 《总账》是状态快照、4.2 是本期变更 —— 同一行两处文字必须逐字一致；
  ② 同步按 `key()`（前 40 个中英数字符）匹配，**不按整行**；
  ③ 新行必须带「075 期」标记；
  ④ 落盘后复读断言行数；
  ⑤ 行名里的计数（`477/15/12`）在 4.2 与总账必须同值（本期未变，只断言）；
  ⑥ 改行名要在同步之前做，否则 `key()` 变了、匹配不上；
  ⑦ 断言要在写盘之前全部核过（074 期坑：断言写在写盘之后 → 失败但文件已写）。
"""
import io
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第075期-2026-11-21.md"
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

# ---- ⑤ 行名里的计数必须两侧同值（本期未变）
assert md.count("`477/15/12`") == 1, md.count("`477/15/12`")
assert led.count("`477/15/12`") == 1, led.count("`477/15/12`")

# ---- OpenCode 行改名：整格取 md 里那一行的活动名（把「第 3 期」写进名字）
i = md.index("### 4.2 常驻权益本期变更")
j = md.index("### ④ 本期第四章脚注")
r42_all = [l for l in md[i:j].split("\n")
           if l.startswith("|") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
oc_rows = [l for l in r42_all if "`OpenCode` 免费模型清单" in l]
assert len(oc_rows) == 1, len(oc_rows)
oc_name = cells(oc_rows[0])[0]
assert "双同第 `3` 期" in oc_name, oc_name

led_lines0 = led.split("\n")
hit = [k for k, l in enumerate(led_lines0) if "`OpenCode` 免费模型清单" in l]
assert len(hit) == 1, hit
c = cells(led_lines0[hit[0]])
assert len(c) == 3, c
led_lines0[hit[0]] = "| %s | %s | %s |" % (oc_name, c[1], c[2])
led = "\n".join(led_lines0)

led_lines = led.split("\n")
r42 = r42_all
print("4.2 行数：", len(r42))
assert len(r42) == 52, len(r42)

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
        if "075 期" not in r:
            missing.append(c[0][:44])
        continue
    r_norm = r if r.startswith("| ") else "| " + r[1:]
    if led_lines[p] != r_norm:
        led_lines[p] = r_norm
        updated += 1

print("总账同步：改写 %d 行；4.2 在总账里找不到 %d 行 %s" % (updated, len(missing), missing))
assert not missing, missing

NEW = []
for r in r42:
    if "075 期" in r and key(plain(EMOJI.sub("", cells(r)[0]))) not in led_idx:
        NEW.append(r if r.startswith("| ") else "| " + r[1:])
print("新增行：", len(NEW))
assert len(NEW) == 2, len(NEW)

body = "\n".join(led_lines).rstrip("\n")
body = body + "\n" + "\n".join(NEW) + "\n"

# ---- 表头与统计句（192 → 194 条 / 变化 50 → 52 条 / 未变 142 → 142 条）
assert "**最后全量复核**：2026-11-20（第 074 期）" in body
body = body.replace("**最后全量复核**：2026-11-20（第 074 期）", "**最后全量复核**：2026-11-21（第 075 期）")
assert "**条目数**：192" in body
body = body.replace("**条目数**：192", "**条目数**：194")
assert "这 192 条里本期真正发生变化的只有 50 条，其余 142 条" in body
body = body.replace("这 192 条里本期真正发生变化的只有 50 条，其余 142 条",
                    "这 194 条里本期真正发生变化的只有 52 条，其余 142 条")
assert "## 一、全量表（192 条 · 按原文顺序）" in body
body = body.replace("## 一、全量表（192 条 · 按原文顺序）", "## 一、全量表（194 条 · 按原文顺序）")

# ---- ⑥ 写盘前把断言全过一遍（074 期坑）
rows_before = len([l for l in body.split("\n") if l.startswith("| ")])
assert rows_before == 196, rows_before  # 194 条 + 表头 2 行
for p in ("第 075 期", "**条目数**：194", "全量表（194 条", "`477/15/12`",
          "Inkling-2-Mini", "`770B`"):
    assert p in body, p
assert "这 194 条里本期真正发生变化的只有 52 条" in body

if DRY:
    print("DRY RUN —— 未写盘；预计表行数 %d" % rows_before)
    sys.exit(0)

io.open(LED, "w", encoding="utf-8", newline="\n").write(body)
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(LED, encoding="utf-8").read()
rows = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows == 196, rows
for p in ("第 075 期", "**条目数**：194", "全量表（194 条", "`477/15/12`", "Inkling-2-Mini"):
    assert p in disk, p
print("ledger rows=%d | bytes=%d" % (rows, len(disk.encode())))
