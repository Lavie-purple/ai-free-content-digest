# -*- coding: utf-8 -*-
"""从日报第四章「限时活动与截止时间表」抽取结构化数据 → .workbuddy/data/deadlines.csv

用法：
    python extract_deadlines.py              # 自动取日期最新一期
    python extract_deadlines.py <src.md>

设计要点：
  - 每次都按最新一期**重建** CSV，保证与日报正文一致，不做手工维护
  - 「首次出现」期号从旧 CSV 继承（按活动名归一化后匹配），重建不会丢历史
  - 保留「截止原文」「状态原文」，任何数字都能回溯到原句，不产生二手数字
  - CSV 用 utf-8-sig 写出，Windows Excel 直接双击不乱码
"""
import calendar, csv, io, os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(WS, ".workbuddy", "data")
CSV_PATH = os.path.join(DATA_DIR, "deadlines.csv")
COLS = ["截止日期", "状态", "紧急度", "活动", "截止原文", "状态原文", "最后更新", "首次出现"]

KEEP = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff]+")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF]\uFE0F?")


def key(s):
    return KEEP.sub("", s).lower()[:40]


def plain(s):
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return s.strip()


def pick_default():
    cands = []
    for fn in os.listdir(WS):
        m = re.match(r"^(AI免费内容与权益速递.*?(\d{4})-(\d{2})-(\d{2}))\.md$", fn)
        if m:
            cands.append((m.group(2) + m.group(3) + m.group(4), fn, int(m.group(3))))
    if not cands:
        raise SystemExit("工作区里没找到日报 md")
    cands.sort()
    return os.path.join(WS, cands[-1][1]), cands[-1][2]


def norm_date(raw, year, month):
    """把「9/20」「9/17–9/20」「2026 年 9 月底」归一为 YYYY-MM-DD；解析不了返回 ''。"""
    t = raw.replace("**", "")
    if "月底" in t:
        m = re.search(r"(\d{1,2})\s*月", t) or re.search(r"(\d{1,2})/", t)
        if m:
            mm = int(m.group(1))
            yy = year + (1 if mm < month - 6 else 0)
            return "%04d-%02d-%02d" % (yy, mm, calendar.monthrange(yy, mm)[1])
    ms = re.findall(r"(\d{1,2})/(\d{1,2})", t)
    if ms:
        mm, dd = int(ms[-1][0]), int(ms[-1][1])   # 区间取最后一个日期为截止
        yy = year + (1 if mm < month - 6 else 0)
        try:
            return "%04d-%02d-%02d" % (yy, mm, dd)
        except ValueError:
            return ""
    return ""


def classify(status_text):
    """状态类别。

    判定顺序：**关键词优先于色标**。日报里 🟢 同时用于「生效中」和
    「未开始」（例：'🟢 未开始，35 家市级大创园现场'），只认色标会误判，
    所以先看文字再回落到色标。
    """
    t = status_text.strip()
    if "已结束" in t:
        return "over"
    if "未开始" in t:
        return "pending"
    if "口径" in t and ("冲突" in t or "存疑" in t or "澄清" in t):
        return "unclear"
    if "今天换挡" in t:
        return "switch"
    for mark, name in [("\U0001F534", "crit"), ("\U0001F7E0", "switch"),
                       ("\U0001F7E1", "pending"), ("\U0001F7E2", "live"),
                       ("\u26AA", "over"), ("\u26A0", "unclear")]:
        if t.startswith(mark):
            return name
    if "生效中" in t:
        return "live"
    return "other"


def main():
    if len(sys.argv) > 1:
        src = sys.argv[1]
        m = re.search(r"(\d{4})-(\d{2})", os.path.basename(src))
        year, month = (int(m.group(1)), int(m.group(2))) if m else (2026, 9)
    else:
        src, month = pick_default()
        year = 2026
    issue = os.path.basename(src)
    mm = re.search(r"第\s*(\d{3})\s*期", issue)
    issue_no = mm.group(1) if mm else "???"

    md = io.open(src, encoding="utf-8").read().replace("\r\n", "\n")

    # 定位第四章，并取其后第一个表格
    sec = re.search(r"(?m)^##\s*四、[^\n]*\n([\s\S]*?)(?=^##\s|\Z)", md)
    if not sec:
        raise SystemExit("没找到第四章「限时活动与截止时间表」")
    rows = []
    for ln in sec.group(1).split("\n"):
        if ln.strip().startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            rows.append(cells)
    if len(rows) < 3:
        raise SystemExit("第四章表格只有 %d 行，不像数据表" % len(rows))
    header, data = rows[0], rows[2:]
    if len(header) != 3:
        print("!! 表头列数=%d（预期 3），仍按前三列解析" % len(header))

    # 继承历史「首次出现」
    first_seen = {}
    if os.path.exists(CSV_PATH):
        with io.open(CSV_PATH, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                first_seen[key(r.get("活动", ""))] = r.get("首次出现", "")

    out, no_date = [], []
    for c in data:
        c = (c + ["", "", ""])[:3]
        act_raw, due_raw, st_raw = c
        act = plain(EMOJI.sub("", act_raw)).strip()
        if not act:
            continue
        due = norm_date(due_raw, year, month)
        if not due:
            no_date.append((act, plain(due_raw)))
        ind = EMOJI.findall(act_raw)
        out.append({
            "截止日期": due,
            "状态": classify(st_raw),
            "紧急度": ind[0].strip("\uFE0F") if ind else "",
            "活动": act,
            "截止原文": plain(due_raw),
            "状态原文": plain(st_raw),
            "最后更新": issue_no,
            "首次出现": first_seen.get(key(act), issue_no),
        })

    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    with io.open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in sorted(out, key=lambda x: (x["截止日期"] or "9999", x["活动"])):
            w.writerow(r)

    from collections import Counter
    print("src      :", issue)
    print("写入     : %s" % os.path.relpath(CSV_PATH, WS))
    print("数据行   : %d（第四章表体 %d 行）" % (len(out), len(data)))
    print("状态分布 :", dict(Counter(r["状态"] for r in out)))
    print("已解析日期: %d / %d" % (len(out) - len(no_date), len(out)))
    if no_date:
        print("未能解析日期的 %d 条（需人工确认）:" % len(no_date))
        for a, d in no_date:
            print("   -", a[:40], "|", d[:40])
    span = [r["截止日期"] for r in out if r["截止日期"]]
    if span:
        print("日期区间 : %s ~ %s" % (min(span), max(span)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
