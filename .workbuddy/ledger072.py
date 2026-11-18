# -*- coding: utf-8 -*-
"""072 期：总账与 4.2 同步 + 补 2 条 + 表头更新。

纪律（066/068/071 沿用）：
  ① 《总账》是状态快照、4.2 是本期变更 —— 同一行两处文字必须逐字一致；
  ② 同步按 `key()`（前 40 个中英数字符）匹配，**不按整行**；
  ③ 新行必须带「072 期」标记；
  ④ 落盘后复读断言行数；
  ⑤ 行名里的计数（`470/17/14`）必须在 4.2 与总账**同时**改名；
  ⑥ 072 期新增：两行改了行名（`OpenRouter` 的计数、`OpenCode` 的口径），
     **改名要在同步之前做**，否则 `key()` 变了、匹配不上。
"""
import io
import re
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第072期-2026-11-18.md"
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
# gen_table072 已把 4.2 的行名改成 478；此处只补「还没改」的情况
if "`470/17/14`" in md:
    assert md.count("`470/17/14`") == 1, md.count("`470/17/14`")
    md = md.replace("`470/17/14`", "`478/17/14`")
assert md.count("`478/17/14`") == 1, md.count("`478/17/14`")
assert led.count("`470/17/14`") == 1, led.count("`470/17/14`")
led = led.replace("`470/17/14`", "`478/17/14`")

# ---- ⑥ OpenCode 行改名（口径从「`-free` id」改为「段落逐条」）
# 直接取 md 里那一行的「活动名」单元格，整格替换，避免手抄引号位置出错
i = md.index("### 4.2 常驻权益本期变更")
j = md.index("### ④ 本期第四章脚注")
r42_all = [l for l in md[i:j].split("\n")
           if l.startswith("|") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
oc_rows = [l for l in r42_all if "`OpenCode` 免费模型清单" in l]
assert len(oc_rows) == 1, len(oc_rows)
oc_name = cells(oc_rows[0])[0]
assert "Free models" in oc_name, oc_name

led_lines0 = led.split("\n")
hit = [k for k, l in enumerate(led_lines0) if "`OpenCode` 免费模型清单 10 → 11 项" in l]
assert len(hit) == 1, hit
c = cells(led_lines0[hit[0]])
assert len(c) == 3, c
led_lines0[hit[0]] = "| %s | %s | %s |" % (oc_name, c[1], c[2])
led = "\n".join(led_lines0)

led_lines = led.split("\n")

i = md.index("### 4.2 常驻权益本期变更")
j = md.index("### ④ 本期第四章脚注")
r42 = [l for l in md[i:j].split("\n")
       if l.startswith("|") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
print("4.2 行数：", len(r42))
assert len(r42) == 44

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
        if "072 期" not in r:
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
    if "072 期" in r and key(plain(EMOJI.sub("", cells(r)[0]))) not in led_idx:
        NEW.append(r if r.startswith("| ") else "| " + r[1:])
print("新增行：", len(NEW))
assert len(NEW) == 2, len(NEW)

body = "\n".join(led_lines).rstrip("\n")
body = body + "\n" + "\n".join(NEW) + "\n"

body = body.replace("**最后全量复核**：2026-11-17（第 071 期）", "**最后全量复核**：2026-11-18（第 072 期）")
body = body.replace("**条目数**：184", "**条目数**：186")
body = body.replace("这 184 条里本期真正发生变化的只有 42 条，其余 142 条",
                    "这 186 条里本期真正发生变化的只有 44 条，其余 142 条")
body = body.replace("## 一、全量表（184 条 · 按原文顺序）", "## 一、全量表（186 条 · 按原文顺序）")

if DRY:
    print("DRY RUN —— 未写盘；预计表行数 %d" % len([l for l in body.split("\n") if l.startswith("| ")]))
    sys.exit(0)

io.open(LED, "w", encoding="utf-8", newline="\n").write(body)
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(LED, encoding="utf-8").read()
rows = len([l for l in disk.split("\n") if l.startswith("| ")])
assert rows == 188, rows  # 186 条 + 表头 2 行
for p in ("第 072 期", "**条目数**：186", "全量表（186 条", "`478/17/14`", "Tencent Hy License 1.0", "GPT-6.2 Astra"):
    assert p in disk, p
assert "这 186 条里本期真正发生变化的只有 44 条" in disk
print("ledger rows=%d | bytes=%d" % (rows, len(disk.encode())))
