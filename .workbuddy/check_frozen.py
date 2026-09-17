# -*- coding: utf-8 -*-
"""已固化条目库交叉检查：防止把往期写过的内容当"本期新增"再写一次。

用法：
    python check_frozen.py                 # 扫工作区日期最新一期
    python check_frozen.py <src.md>
    python check_frozen.py <src.md> -v     # 展开全部命中行

为什么不能只做"关键词命中"：
    日报第四章「截止时间表」和第五章「纠错清单」**本来就会**反复提到往期条目，
    那是正当引用。真正的错误是**行文里声称"本期新增/🆕"，但该条目早已固化**。
    所以这里按「命中行里有没有新增表述」分成两级：
      🔴 高危 —— 命中行是"新增"表述，且该条目首见期早于本期  → 必须改
      ⚪ 引用 —— 命中行不是"新增"表述  → 通常正常，仅在 -v 时展开

退出码：有 🔴 高危则返回 1，便于挂进出刊流程做卡点。
"""
import io, os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(WS, ".workbuddy", "data", "frozen_items.md")

NEW_PAT = re.compile(r"(新增|🆕|首次纳入|全新上架|首次出现)")


def pick_default():
    cands = []
    for fn in os.listdir(WS):
        m = re.match(r"^(AI免费内容与权益速递.*?(\d{4}-\d{2}-\d{2}))\.md$", fn)
        if m:
            cands.append((m.group(2), fn))
    if not cands:
        raise SystemExit("工作区里没找到日报 md")
    cands.sort()
    return os.path.join(WS, cands[-1][1])


def load_lib():
    out = []
    for ln in io.open(LIB, encoding="utf-8").read().split("\n"):
        s = ln.strip()
        if not s.startswith("|"):
            continue
        c = [x.strip() for x in s.strip("|").split("|")]
        if len(c) < 5 or c[0] in ("关键词",) or set(c[0]) <= set("-: "):
            continue
        out.append({"kw": c[0], "seen": c[1], "cat": c[2], "sum": c[3], "st": c[4]})
    return out


def issue_no(text, name):
    for src in (name, text):
        m = re.search(r"第\s*(\d{3})\s*期", src)
        if m:
            return m.group(1)
    return "???"


def main():
    args = [a for a in sys.argv[1:] if a != "-v"]
    verbose = "-v" in sys.argv
    src = args[0] if args else pick_default()
    md = io.open(src, encoding="utf-8").read().replace("\r\n", "\n")
    no = issue_no(md, os.path.basename(src))
    lib = load_lib()

    print("已固化条目库交叉检查")
    print("目标期次 : 第 %s 期（%s）" % (no, os.path.basename(src)))
    print("库内条目 : %d 条" % len(lib))

    high, ref, fresh, absent = [], [], [], []
    for it in lib:
        first = it["seen"]
        if first == no:
            fresh.append(it); continue
        hits = [(i + 1, ln.strip()) for i, ln in enumerate(md.split("\n")) if it["kw"] in ln]
        if not hits:
            absent.append(it); continue
        bad = []
        for n, l in hits:
            pos = l.find(it["kw"])
            # 条件 A：标记紧邻关键词之前（如「🆕 **Union Alpha**」）
            cond_a = bool(NEW_PAT.search(l[max(0, pos - 25):pos]))
            # 条件 B：整行以「← 本期新增」收尾，且关键词是本行首列（表格里
            #         这个后缀标注的是行主体，不是同行其他列的内容）
            cells = l.strip().strip("|").split("|")
            cond_b = bool(NEW_PAT.search(l[-16:])) and it["kw"] in (cells[0] if cells else "")
            if cond_a or cond_b:
                bad.append((n, l))
        if bad:
            high.append((it, bad))
        else:
            ref.append((it, hits))

    print()
    print("【🔴 高危】%d 条 —— 行文声称「新增」，但条目首见期更早，属重复往期" % len(high))
    for it, bad in high:
        print("   %s  (首见 第%s期, 状态 %s)" % (it["kw"], it["seen"], it["st"]))
        for n, l in bad[:2]:
            print("      行%d: %s" % (n, l[:110]))
    if not high:
        print("     无 —— 本期没有把往期内容当新增")

    print()
    print("【⚪ 引用】%d 条 —— 命中的行不是「新增」表述（通常是第四章截止表或纠错章引用，正常）" % len(ref))
    if verbose:
        for it, hits in ref:
            print("   %s (首见 第%s期) x%d 行" % (it["kw"], it["seen"], len(hits)))
    else:
        print("     " + "、".join(it["kw"] for it, _ in ref) if ref else "     无")

    print()
    print("【○ 本期首次登记】%d 条" % len(fresh))
    if fresh:
        print("     " + "、".join(it["kw"] for it in fresh))

    print()
    print("【— 本期未出现】%d 条（正常，说明当期没写到）" % len(absent))
    print()
    print("对账：高危%d + 引用%d + 首登%d + 未出现%d = %d，库内 %d 条 -> %s"
          % (len(high), len(ref), len(fresh), len(absent),
             len(high) + len(ref) + len(fresh) + len(absent), len(lib),
             "一致" if len(high) + len(ref) + len(fresh) + len(absent) == len(lib) else "不一致"))
    return 1 if high else 0


if __name__ == "__main__":
    sys.exit(main())
