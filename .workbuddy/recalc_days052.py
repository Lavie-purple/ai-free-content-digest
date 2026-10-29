# -*- coding: utf-8 -*-
"""052 期专用的「距今 N 天」重算器（直接作用于日报 md 里的第四章表体）。

**纪律（048/049/050/051 期反复踩过）**：断言是「天数 == 截止日 − 基准日」，
**不是「推进一天就 −1」** —— 每一行都独立算，不做批量减一。

⚠️ **052 期是同日增补轮，基准日仍是 2026-10-29** —— **「基准日没变」不是跳过重算的理由**：
   本脚本照样逐行独立解析截止列、算真值、逐行比对继承值，**并把「重算值与继承值逐行相同」作为一条可核对的结论输出**。

做法（与 051 期同一套判据）：
  1) 从每一行的**截止列**（第 2 列）里解析出第一个可解析的日期（月/日 或 年-月-日）。
  2) 用 `截止日 − 基准日` 算出真值。
  3) 把状态列里所有「距今 N 天」改成真值。
  4) 若截止列不可解析（长期档 / 无结束日），则该行的「距今」若存在则**报错退出**。
"""
import io
import re
import sys
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第052期-2026-10-29.md"
BASE = date(2026, 10, 29)

MD_RE = re.compile(r'(?<![0-9])(\d{1,2})\s*/\s*(\d{1,2})(?![0-9])')
YMD_RE = re.compile(r'(?<![0-9])(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日')
ISO_RE = re.compile(r'(?<![0-9])(20\d{2})-(\d{2})-(\d{2})(?![0-9])')
CN_MD_RE = re.compile(r'(?<![0-9])(\d{1,2})\s*月\s*(\d{1,2})\s*日')
DAYS_RE = re.compile(r'距今\s*([0-9]+)\s*天')


def parse_deadline(col):
    m = ISO_RE.search(col)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = YMD_RE.search(col)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = MD_RE.search(col)
    if m:
        mo, dy = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12 and 1 <= dy <= 31:
            return (mo, dy)
    m = CN_MD_RE.search(col)
    if m:
        mo, dy = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12 and 1 <= dy <= 31:
            return (mo, dy)
    return None


def to_date(v):
    if isinstance(v, date):
        return v
    mo, dy = v
    y = BASE.year
    try:
        d = date(y, mo, dy)
    except ValueError:
        return None
    if (BASE - d).days > 300:
        try:
            d = date(y - 1, mo, dy)
        except ValueError:
            return None
    return d


def main():
    md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
    lines = md.split("\n")

    # 只在第四章区间内改
    s = md.index("## 四、限时活动与截止时间表")
    e = md.index("*本期完。*")
    head_lines = md[:s].count("\n")
    tail_lines = md[e:].count("\n")
    body = lines[head_lines:len(lines) - tail_lines]

    out = []
    changed = []
    same = []
    problems = []
    for l in body:
        if not (l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")):
            out.append(l)
            continue
        cols = l.split("|")
        if len(cols) < 5:
            out.append(l)
            continue
        col_dead, col_stat = cols[2], cols[3]
        ms = DAYS_RE.findall(col_stat)
        if not ms:
            out.append(l)
            continue
        dl = parse_deadline(col_dead)
        if dl is None:
            problems.append(("截止不可解析却带距今", cols[1].strip()[:60], col_dead.strip()[:60], ms))
            out.append(l)
            continue
        d = to_date(dl)
        if d is None:
            problems.append(("日期非法", cols[1].strip()[:60], col_dead.strip()[:60], ms))
            out.append(l)
            continue
        truth = (d - BASE).days
        if truth < 0:
            problems.append(("截止日已过（真值为负）", cols[1].strip()[:60], col_dead.strip()[:60], ms))
            out.append(l)
            continue
        old = ms[0]
        if old != str(truth):
            cols[3] = DAYS_RE.sub("距今 %d 天" % truth, col_stat)
            changed.append((cols[1].strip()[:52], col_dead.strip()[:26], old, truth))
            out.append("|".join(cols))
        else:
            same.append((cols[1].strip()[:52], col_dead.strip()[:26], old))
            out.append(l)

    new_md = "\n".join(lines[:head_lines] + out + lines[len(lines) - tail_lines:])
    io.open(MD, "w", encoding="utf-8", newline="\n").write(new_md)

    print("逐行独立重算：共 %d 行带「距今 N 天」" % (len(changed) + len(same)))
    print("  继承值 == 重算值（逐行相同）：%d 行" % len(same))
    for name, dl, o in same:
        print("     %-52s | 截止 %-26s | 距今 %s 天" % (name, dl, o))
    print("  需要修正：%d 行" % len(changed))
    for name, dl, o, t in changed:
        print("     %-52s | 截止 %-26s | %s -> %s" % (name, dl, o, t))
    if problems:
        print("\n⚠️ 需人工确认 %d 行：" % len(problems))
        for p in problems:
            print("   ", p)
        sys.exit(1)
    print("\n全部「距今 N 天」均满足「天数 == 截止日 − 基准日」✔")


if __name__ == "__main__":
    main()
