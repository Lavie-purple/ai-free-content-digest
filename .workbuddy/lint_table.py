# -*- coding: utf-8 -*-
"""截止表的行内体检：盯着「一行越写越长」，不盯着「行数变多」。

为什么需要它（047 期修订）：
    40→47 期的行均字数连续八期单调上升（336 → 513），但每期都被「行数没涨」骗过去。
    prune 删得掉死行，删不掉活行里的历史沉积 —— 于是必须有个卡口管「一行写多长」。

四条判据（都只看单行，不看总数）：
  R1 单行字数 > --max（默认 200）：一行顶一篇小作文，读者扫不了
  R2 单行避坑编号 ≥ 2 处：避坑是审计索引，不是表格该承担的内容
  R3 单行非本期期号引用 ≥ 2 处：写「（029 期）改过口径」是沿革，应进 changelog
  R4 截止列无确切日期却出现在 4.1（限时表）：口径错位

用法：
    python lint_table.py <md>                 # 报告模式，永远 exit 0
    python lint_table.py <md> --strict        # 卡口模式，有超限就 exit 1
    python lint_table.py <md> --max 260       # 放宽阈值
"""
import io, os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAY_RE = re.compile(r"^\s*\**\s*(未公布|无结束日|无截止|未定|动态|持续|不适用|按量|随套餐|名额有限|ongoing|视|依)")
PIT_RE = re.compile(r"避坑\s*\d+")


def pick_default():
    cands = []
    for fn in os.listdir(WS):
        m = re.match(r"^(AI免费内容与权益速递.*?(\d{4})-(\d{2})-(\d{2}))\.md$", fn)
        if m:
            cands.append((m.group(2) + m.group(3) + m.group(4), fn))
    cands.sort()
    return os.path.join(WS, cands[-1][1]) if cands else None


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def blocks(lines):
    res, cur = [], []
    for idx, ln in enumerate(lines):
        if ln.strip().startswith("|"):
            cur.append(idx)
        else:
            if cur:
                res.append((cur[0], cur[-1] + 1)); cur = []
    if cur:
        res.append((cur[0], cur[-1] + 1))
    return res


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    maxc = 200
    for a in sys.argv[1:]:
        if a.startswith("--max"):
            maxc = int(a.split("=")[1]) if "=" in a else maxc
    src = args[0] if args else pick_default()
    if not src:
        raise SystemExit("没找到日报 md")

    md = io.open(src, encoding="utf-8").read().replace("\r\n", "\n")
    mm = re.search(r"第\s*(\d{3})\s*期", os.path.basename(src))
    issue = mm.group(1) if mm else "???"
    ISSUE_RE = re.compile(r"(?<!%s)(0\d{2})\s*期" % issue)

    lines = md.split("\n")
    # 标记每行归属的小节
    sec_of, cur_sec = {}, ""
    for idx, ln in enumerate(lines):
        if ln.startswith("#"):
            cur_sec = ln.strip("# ").strip()
        sec_of[idx] = cur_sec

    hits = {"R1": [], "R2": [], "R3": [], "R4": []}
    total_rows = 0
    for b0, b1 in blocks(lines):
        head = cells(lines[b0])
        if len(head) != 3 or head[0] != "活动":
            continue
        for idx in range(b0 + 2, b1):
            ln = lines[idx].strip()
            if not ln or re.match(r"^\|[\s:\-\|]+\|$", ln):
                continue
            c = cells(ln)
            if len(c) < 3:
                continue
            total_rows += 1
            n = len("".join(ln.split()))
            name = c[0][:48]
            sec = sec_of.get(idx, "")
            if n > maxc:
                hits["R1"].append((n, name, sec))
            if len(PIT_RE.findall(ln)) >= 2:
                hits["R2"].append((len(PIT_RE.findall(ln)), name, sec))
            if len(ISSUE_RE.findall(ln)) >= 2:
                hits["R3"].append((len(ISSUE_RE.findall(ln)), name, sec))
            d = c[1].replace("**", "").strip()
            if "4.1" in sec and STAY_RE.match(d):
                hits["R4"].append((0, name, sec))

    print("src   : %s" % os.path.basename(src))
    print("表体行: %d（阈值 %d 字/行）" % (total_rows, maxc))
    print()
    labels = {
        "R1": "单行超长（> %d 字）" % maxc,
        "R2": "单行避坑编号 ≥ 2 处",
        "R3": "单行非本期期号引用 ≥ 2 处",
        "R4": "无确切截止日却排在 4.1 限时表",
    }
    for k in ("R1", "R2", "R3", "R4"):
        v = sorted(hits[k], reverse=True)
        print("%s %-26s : %d 条" % (k, labels[k], len(v)))
        for row in v[:6]:
            if k == "R1":
                print("     %5d 字  %s" % (row[0], row[1]))
            elif k in ("R2", "R3"):
                print("     %5d 处  %s" % (row[0], row[1]))
            else:
                print("               %s" % row[1])
        if len(v) > 6:
            print("     …… 另 %d 条" % (len(v) - 6))
        print()

    bad = sum(len(hits[k]) for k in ("R2", "R3", "R4")) + len(hits["R1"])
    if strict and bad:
        print("STRICT: %d 处超限 -> exit 1" % bad)
        return 1
    print("VERDICT: %s（%d 处待改）" % ("CLEAN" if not bad else "REPORT ONLY", bad))
    return 0


if __name__ == "__main__":
    sys.exit(main())
