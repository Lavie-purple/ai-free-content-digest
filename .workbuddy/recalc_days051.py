# -*- coding: utf-8 -*-
"""051 期专用的「距今 N 天」重算器。

**纪律（048/049/050 期反复踩过）**：断言是「天数 == 截止日 − 基准日」，
**不是「推进一天就 −1」** —— 每一行都独立算，不做批量减一。

做法：
  1) 从每一行的**截止列**（第 2 列）里解析出第一个可解析的日期（月/日 或 年-月-日）。
  2) 用 `截止日 − 基准日` 算出真值。
  3) 把状态列里所有「距今 N 天」改成真值。
  4) 若截止列不可解析（长期档 / 无结束日），则该行的「距今」若存在则**报错退出**
     —— 因为「不可解析的截止日」不该带一个「距今」数字。
"""
import io
import re
import sys
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
TABLE = WS + ".workbuddy/tmp_table051.md"
BASE = date(2026, 10, 29)

# 月日 -> 截止日（含年份）。只在明确列出的行里用，避免把正文里的历史日期误判成截止日。
MD_RE = re.compile(r'(?<![0-9])(\d{1,2})\s*/\s*(\d{1,2})(?![0-9])')
YMD_RE = re.compile(r'(?<![0-9])(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日')
ISO_RE = re.compile(r'(?<![0-9])(20\d{2})-(\d{2})-(\d{2})(?![0-9])')
JI_ZH = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7,
         "八": 8, "九": 9, "十": 10, "十一": 11, "十二": 12}
CN_MD_RE = re.compile(r'(?<![0-9])(\d{1,2})\s*月\s*(\d{1,2})\s*日')

DAYS_RE = re.compile(r'距今\s*([0-9]+)\s*天')


def parse_deadline(col):
    """从截止列里解析出一个 (月, 日) 或 (年, 月, 日)。解析不出来返回 None。"""
    # 1) 明确的 YYYY-MM-DD
    m = ISO_RE.search(col)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    # 2) YYYY 年 M 月 D 日
    m = YMD_RE.search(col)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    # 3) M/D
    m = MD_RE.search(col)
    if m:
        mo, dy = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12 and 1 <= dy <= 31:
            return (mo, dy)
    # 4) M 月 D 日
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
    # 若算出来已过去超过 300 天，说明应是上一年
    if (BASE - d).days > 300:
        try:
            d = date(y - 1, mo, dy)
        except ValueError:
            return None
    return d


def main():
    lines = io.open(TABLE, encoding="utf-8").read().split("\n")
    out = []
    changed = []
    problems = []
    for l in lines:
        if not (l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")):
            out.append(l)
            continue
        cols = l.split("|")
        # cols[0]='' cols[1]=活动 cols[2]=截止 cols[3]=状态
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
            # 截止日已过：不该写「距今 N 天」的正数。保留原样并在报告里点名。
            problems.append(("截止日已过（真值为负）", cols[1].strip()[:60], col_dead.strip()[:60], ms))
            out.append(l)
            continue
        old = ms[0]
        if old != str(truth):
            col_stat2 = DAYS_RE.sub("距今 %d 天" % truth, col_stat)
            cols[3] = col_stat2
            l2 = "|".join(cols)
            changed.append((cols[1].strip()[:52], col_dead.strip()[:26], old, truth))
            out.append(l2)
        else:
            out.append(l)
    io.open(TABLE, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("重算行数:", len(changed))
    for name, dl, o, t in changed:
        print("   %-52s | 截止 %-26s | %s -> %s" % (name, dl, o, t))
    if problems:
        print("\n⚠️ 需人工确认 %d 行：" % len(problems))
        for p in problems:
            print("   ", p)
        sys.exit(1)
    print("\n全部「距今 N 天」均满足「天数 == 截止日 − 基准日」✔")


if __name__ == "__main__":
    main()
