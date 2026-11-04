# -*- coding: utf-8 -*-
"""058 期专用的「距今 N 天」重算器（直接作用于日报 md 里的第四章表体）。

**纪律（048/049/050/051 期反复踩过）**：断言是「天数 == 截止日 − 基准日」，
**不是「推进一天就 −1」** —— 每一行都独立算，不做批量减一。

⚠️ **055 期是隔日出刊、基准日是 2026-11-01** —— **本期基准日推进到 2026-11-02**
   本脚本照样逐行独立解析截止列、算真值、逐行比对继承值、**并把「重算值与继承值逐行相同」作为一条可核对的结论输出**。

⚠️ **056 期新立的一条工程纪律（避坑 252）**：本脚本只重算**状态列**的「距今 N 天」，
   **截止列里的「距结束 N 天」与状态列里的「已过 N 天」从来没人重算过** ——
   实测这些数字**自 049 期写入起就冻结着**（`距结束 11 天` / `距结束 5 天` / `距结束 8 天` / `距开卖 0 天`），
   **而基准日一直在推进**。
   **本期处置：① `gen_table056.py` 里把这几处逐条改写成 11/2 的真值；**
   **② 本脚本在跑完后加一道「全表天数 token 复核」—— 把表体里每一个天数 token 都解析出来、**
   **对照截止列独立重算一遍，任何一个对不上就 `exit 1`**（这样下期不会再漏）。

做法（与 051–055 期同一套判据）：
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
MD = WS + "AI免费内容与权益速递-第058期-2026-11-04.md"
BASE = date(2026, 11, 4)

MD_RE = re.compile(r'(?<![0-9])(\d{1,2})\s*/\s*(\d{1,2})(?![0-9])')
YMD_RE = re.compile(r'(?<![0-9])(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日')
ISO_RE = re.compile(r'(?<![0-9])(20\d{2})-(\d{2})-(\d{2})(?![0-9])')
CN_MD_RE = re.compile(r'(?<![0-9])(\d{1,2})\s*月\s*(\d{1,2})\s*日')
DAYS_RE = re.compile(r'距今\s*`?([0-9]+)`?\s*天')
# ⚠️ **056 期新立**：全表复核用的 token 模式 —— 「距今 / 距结束 / 距开卖 / 已过」
TOKEN_RE = re.compile(r'(距今|距结束|距开卖)\s*`?(\d+)`?\s*天|已(?:早于|过)本期基准日\s*`?(\d+)`?\s*天|已过\s*`?(\d+)`?\s*天')


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

    # 只在第四章区间内改。
    # ⚠️ 054 期新立、055 期沿用：**结束标记不能写死 "*本期完.*"** —— 那要等脚注注入之后才存在。
    s = md.index("## 四、限时活动与截止时间表")
    nxt = md.find("\n## ", s + 10)
    e = nxt if nxt > 0 else len(md)
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

    # ============================================================
    # ⚠️ **056 期新立（避坑 252）**：全表「天数 token」复核
    # ------------------------------------------------------------
    # 背景：`recalc_days` 只重算**状态列**的「距今 N 天」，
    # **截止列里的「距结束 N 天」与状态列里的「已过 N 天」从来没人重算过** ——
    # 实测它们自 049 期写入起就冻结着，而基准日一直在推进。
    # 本期由 `gen_table056.py` 逐条改正；**这里加一道独立复核**，
    # 任何一行对不上就 `exit 1` —— **这样下期不会再漏**。
    #
    # 复核口径：
    #   「距今 N 天」  → 真值 = 截止日 − 基准日（正数）
    #   「距结束 N 天」→ 真值 = 截止日 − 基准日（正数；取截止列里的**最后一个**日期）
    #   「距开卖 N 天」→ 真值 = 截止日 − 基准日（正数）
    #   「已过 N 天」  → 真值 = 基准日 − 截止日（正数）
    # ============================================================
    md2 = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
    lines2 = md2.split("\n")
    bad = []
    checked = 0
    for l in lines2:
        if not (l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")):
            continue
        cols = l.split("|")
        if len(cols) < 5:
            continue
        col_dead, col_stat = cols[2], cols[3]
        name = cols[1].strip()[:52]

        # ⚠️ **056 期新立的一条复核口径**：**「引用式」的天数不算**。
        #    本期多处纠错尾注里要**原样引用往期的错误值**（那是证据链），
        #    而那些引用一律写在 `「」` 里 —— **所以复核时必须跳过 `「」` 内的 token**，
        #    否则「引用一个旧值」会被误判成「表体里还留着旧值」。
        #    **判据：`「」` 内是引用、`「」` 外是本行当前生效的口径。**
        def strip_quoted(text):
            out, depth = [], 0
            for ch in text:
                if ch == "「":
                    depth += 1
                    out.append(" ")
                elif ch == "」":
                    depth = max(0, depth - 1)
                    out.append(" ")
                else:
                    out.append(" " if depth > 0 else ch)
            return "".join(out)

        live_dead = strip_quoted(col_dead)
        live_stat = strip_quoted(col_stat)
        for cm in TOKEN_RE.finditer(live_dead + " " + live_stat):
            kind = cm.group(1)
            val = cm.group(2) or cm.group(3) or cm.group(4)
            if kind is None:
                # 「已过 N 天」/「已早于本期基准日 N 天」→ 真值 = 基准日 − 截止日
                ms = MD_RE.findall(live_dead)
                if not ms:
                    continue
                mo, dy = int(ms[-1][0]), int(ms[-1][1])
                if not (1 <= mo <= 12 and 1 <= dy <= 31):
                    continue
                try:
                    d = date(BASE.year, mo, dy)
                except ValueError:
                    continue
                truth = (BASE - d).days
                if truth < 0:
                    # 与 `to_date` 同口径：相差超过 300 天才回退到上一年
                    try:
                        truth = (BASE - date(BASE.year - 1, mo, dy)).days
                    except ValueError:
                        continue
            else:
                # 「距今 / 距结束 / 距开卖」→ 真值 = 截止日 − 基准日
                # ⚠️ 「距结束」取截止列里的**最后一个**日期（区间活动取收官日）。
                ms = MD_RE.findall(live_dead)
                if not ms:
                    continue
                mo, dy = int(ms[-1][0]), int(ms[-1][1])
                if not (1 <= mo <= 12 and 1 <= dy <= 31):
                    continue
                try:
                    d = date(BASE.year, mo, dy)
                except ValueError:
                    continue
                truth = (d - BASE).days
                if truth < 0 and (BASE - d).days > 300:
                    # 与 `to_date` 同口径：相差超过 300 天才回退到上一年
                    try:
                        d = date(BASE.year - 1, mo, dy)
                    except ValueError:
                        continue
                    truth = (d - BASE).days
            checked += 1
            if int(val) != truth:
                bad.append((name, cm.group(0), truth, live_dead.strip()[:40]))
    print("\n全表天数 token 独立复核：共核对 %d 处（已跳过 `「」` 内的引用式表述）" % checked)
    if bad:
        print("⚠️ 有 %d 处对不上：" % len(bad))
        for name, tok, truth, dl in bad:
            print("   %-52s | %-22s | 真值 %d | 截止 %s" % (name, tok, truth, dl))
        sys.exit(1)
    print("全部 %d 处天数 token 均满足「天数 == 截止日 − 基准日」✔（避坑 252 的独立复核）" % checked)


if __name__ == "__main__":
    main()
