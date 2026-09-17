# -*- coding: utf-8 -*-
"""截止时间巡检：读 .workbuddy/data/deadlines.csv，按基准日算出到期清单。

用法：
    python check_deadlines.py                    # 基准日=今天，窗口 14 天
    python check_deadlines.py --days 7           # 只看 7 天内
    python check_deadlines.py --today 2026-09-20 # 指定基准日（可复现）
    python check_deadlines.py --all              # 连"更远"的也列出来

前置：先跑 extract_deadlines.py 把最新一期刷进 CSV。

输出分四类，第一类最需要人管：
  A 已过期但状态仍非"已结束" —— 说明上期标错或活动已悄悄结束，必须复核
  B 窗口内到期 —— 按天数升序
  C 已结束 —— 只列名称，不占注意力
  D 无法解析日期 —— 应为 0，非 0 则说明日报里写了非标准日期写法
"""
import csv, datetime as dt, io, os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(WS, ".workbuddy", "data", "deadlines.csv")

LABEL = {"crit": "必办", "switch": "换挡日", "live": "生效中",
         "pending": "未开始", "over": "已结束", "unclear": "口径存疑", "other": "其他"}


def main():
    days, today, show_all = 14, None, False
    a = sys.argv[1:]
    i = 0
    while i < len(a):
        if a[i] == "--days":
            days = int(a[i + 1]); i += 2
        elif a[i] == "--today":
            today = dt.date.fromisoformat(a[i + 1]); i += 2
        elif a[i] == "--all":
            show_all = True; i += 1
        else:
            raise SystemExit("未知参数: " + a[i])
    if today is None:
        today = dt.date.today()
    if not os.path.exists(CSV_PATH):
        raise SystemExit("还没有 %s，先跑 extract_deadlines.py" % os.path.relpath(CSV_PATH, WS))

    rows = list(csv.DictReader(io.open(CSV_PATH, encoding="utf-8-sig", newline="")))
    if not rows:
        raise SystemExit("CSV 是空的")

    src = sorted(set(r["最后更新"] for r in rows))
    print("截止时间巡检 · 基准日 %s" % today.isoformat())
    print("数据源 %s（共 %d 条，来自第 %s 期）" % (os.path.relpath(CSV_PATH, WS), len(rows), "/".join(src)))

    expired, due, over, nodate, later = [], [], [], [], []
    for r in rows:
        d = r.get("截止日期", "").strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", d):
            nodate.append(r); continue
        delta = (dt.date.fromisoformat(d) - today).days
        if r["状态"] == "over":
            over.append((delta, r)); continue
        if delta < 0:
            expired.append((delta, r))
        elif delta <= days:
            due.append((delta, r))
        else:
            later.append((delta, r))

    def line(delta, r):
        when = "今天" if delta == 0 else ("T+%d" % delta if delta > 0 else "已过 %d 天" % -delta)
        return "  %-11s %-7s %s" % (r["截止日期"] + " (" + when + ")",
                                    LABEL.get(r["状态"], r["状态"]), r["活动"])

    # 按天数升序；天数相同时再按活动名——否则 sorted 会去比较 dict 而报错
    srt = lambda lst: sorted(lst, key=lambda x: (x[0], x[1]["活动"]))

    print()
    print("【A】已过期但状态仍非「已结束」：%d 条" % len(expired))
    if expired:
        print("     ^ 这些要么上期标错了，要么活动已悄悄收口——出刊前必须逐条复核")
        for delta, r in srt(expired):
            print(line(delta, r))
    else:
        print("     无（说明上期的状态标注是干净的）")

    print()
    print("【B】%d 天内到期：%d 条" % (days, len(due)))
    for delta, r in srt(due):
        print(line(delta, r))
    if not due:
        print("     窗口内无到期项")

    print()
    print("【C】已结束：%d 条" % len(over))
    for _, r in srt(over):
        print("     · " + r["活动"])
    if not over:
        print("     无")

    print()
    print("【D】日期无法解析：%d 条" % len(nodate))
    for r in nodate:
        print("     - %s | 原文「%s」" % (r["活动"][:36], r["截止原文"][:30]))
    if not nodate:
        print("     无")

    print()
    print("【E】窗口外（>%d 天）：%d 条" % (days, len(later)))
    if show_all:
        for delta, r in srt(later):
            print(line(delta, r))
    elif later:
        print("     " + "、".join(r["活动"][:24] for _, r in srt(later)))
        print("     （加 --all 可展开）")
    else:
        print("     无")

    print()
    tot = len(expired) + len(due) + len(over) + len(nodate) + len(later)
    print("对账：A%d + B%d + C%d + D%d + E%d = %d，CSV 共 %d 条 -> %s"
          % (len(expired), len(due), len(over), len(nodate), len(later), tot, len(rows),
             "一致" if tot == len(rows) else "不一致，需检查"))
    return 0 if tot == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
