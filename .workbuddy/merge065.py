# -*- coding: utf-8 -*-
"""065 期：把 4.2 的「本期有变化」行同步进《常驻权益总账》，并裁掉 4.2 里本期没变化的行。

为什么单独写一个（不跑 split_ledger.py）：
  本期表体是**在上期已拆好的 4.1/4.2 上原地改写**的，不是「合并表 -> 注入 -> 拆分」那条老路。
  split_ledger 的输入约定是「第四章里最长的那一块」，本期有两块（4.1 / 4.2），
  直接跑只会处理 4.1 并把 4.2 全判成「常驻未变」（dry-run 实测：4.2 变更 0 行）。

两条纪律：
  ① 总账**只增不删**：已存在的行不覆盖，只在状态列末尾追加「065 期复核补记」，
     这样长论证一字不丢（052 期：被裁的长论证要有地方存）。
  ② 4.2 只留「本期有变化」的行 —— 判据是状态列含「065 期」或「本期」。
"""
import io
import re

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第065期-2026-11-11.md"
LED = WS + "常驻权益总账.md"
PTR = " [附录 065](details.html)"

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
led = io.open(LED, encoding="utf-8").read().replace("\r\n", "\n")

j = md.index("### 4.2 常驻权益本期变更")
k = md.index("### ④ 本期第四章脚注")
seg = md[j:k]
rows42 = [l for l in seg.split("\n")
          if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(rows42) == 52, len(rows42)

keep, drop = [], []
for r in rows42:
    st = r.split("|")[3]
    (keep if ("065 期" in st or "本期" in st) else drop).append(r)
print("4.2：保留 %d 行、移入总账（本期无变化）%d 行" % (len(keep), len(drop)))


def nm(r):
    c = r.strip().strip("|").split("|")[0]
    return re.sub(r"^[\W_]+", "", c)


def key(s):
    return re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", s)[:26]


led_rows = [l for l in led.split("\n")
            if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(led_rows) == 170, len(led_rows)
lmap = {key(nm(r)): i for i, r in enumerate(led_rows)}

replaced, appended = 0, 0
for r in keep:
    kk = key(nm(r))
    cells = r.strip().rstrip("|").split("|")
    status = cells[3].strip()
    assert status.endswith("|") is False
    status = status.replace(PTR, "").strip().rstrip("|").strip()
    if kk in lmap:
        i = lmap[kk]
        old = led_rows[i].rstrip()
        assert old.endswith("|"), old[-20:]
        cell = old[:-1].rstrip()  # 去掉行尾 `|`
        led_rows[i] = cell + " **〔065 期复核补记〕** " + status + " |"
        replaced += 1
    else:
        led_rows.append("|" + "|".join(cells[1:]) + " |")
        appended += 1

print("总账：替换/补记 %d 行、新增 %d 行、总 %d 行" % (replaced, appended, len(led_rows)))

# ---- 写总账 ----
head_end = led.index("## 一、全量表")
head = led[:head_end]
head = re.sub(r"\*\*最后全量复核\*\*：\d{4}-\d{2}-\d{2}（第 \d{3} 期）　\*\*条目数\*\*：\d+",
              "**最后全量复核**：2026-11-11（第 065 期）　**条目数**：%d" % len(led_rows), head)
head = re.sub(r"这 \d+ 条里本期真正发生变化的只有 \d+ 条，其余 \d+ 条",
              "这 %d 条里本期真正发生变化的只有 %d 条，其余 %d 条"
              % (len(led_rows), len(keep), len(led_rows) - len(keep)), head)
tail = led[led.index("## 二、"):] if "## 二、" in led else ""
new_led = head + "## 一、全量表（%d 条 · 按原文顺序）\n\n| 活动 | 截止 | 状态 |\n| --- | --- | --- |\n%s\n" % (
    len(led_rows), "\n".join(led_rows))
if tail:
    new_led += "\n" + tail.lstrip("\n")
io.open(LED, "w", encoding="utf-8", newline="\n").write(new_led)

# ---- 写日报 4.2 ----
new_seg = seg
lines = seg.split("\n")
out = []
done = False
for ln in lines:
    if ln.startswith("| ") and not ln.startswith("| 活动 |") and not ln.startswith("| --- |"):
        if not done:
            out.extend(keep)
            done = True
        continue
    out.append(ln)
new_seg = "\n".join(out)
new_seg = re.sub(r"> \*\*其余 \d+ 条常驻权益本期无变化\*\*", "> **其余 %d 条常驻权益本期无变化**" % len(drop), new_seg)
md2 = md[:j] + new_seg + md[k:]
io.open(MD, "w", encoding="utf-8", newline="\n").write(md2)

# ---- 复读断言 ----
d = io.open(MD, encoding="utf-8").read()
j2 = d.index("### 4.2"); k2 = d.index("### ④")
d42 = [l for l in d[j2:k2].split("\n")
       if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(d42) == len(keep), (len(d42), len(keep))
dl = io.open(LED, encoding="utf-8").read()
dlr = [l for l in dl.split("\n") if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(dlr) == len(led_rows)
assert "2026-11-11（第 065 期）" in dl
assert "〔065 期复核补记〕" in dl
assert "今天还能领 ¥599" in dl
print("OK | md 4.2 = %d 行 | 总账 = %d 行 | md %d 字节 / 总账 %d 字节"
      % (len(d42), len(dlr), len(d.encode()), len(dl.encode())))
