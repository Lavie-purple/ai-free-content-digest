# -*- coding: utf-8 -*-
"""信源命中统计：给台账 182 条信源算「上次命中 / 产出条数」，并回写台账 + 导出 CSV。

用法：
    python build_source_hits.py            # 计算 + 回写台账 + 导出 CSV
    python build_source_hits.py --dry      # 只算不写，先看结果

匹配规则（写死在这里，保证可复现）：
    对每条信源取若干**别名**，再拿别名去各期日报正文里做子串匹配。
    两边都先归一化：只保留 0-9a-z 和汉字，其余全去掉。
    于是「Hugging Face」（正文）与 huggingface（域名根）能对上。
    别名来源：
      a) 信源全名归一化，长度 ≥4
      b) 名字里第一个括号/全角括号之前的部分归一化，长度 ≥2
         （用于「微博（AI 官方账号+话题）」→ 微博 这类中文源）
      c) 域名去 www./api./docs./blog. 后取第一段，长度 ≥4
    别名短于上述阈值的一律丢弃，避免「x」「ai」这种泛词造成大面积误报。

**口径要说清，否则这列数字会被误读：**
    统计的是「该信源的名字或域名根，在各期日报**正文**里出现的情况」，
    即**品牌/来源被提及**，不等于「这一期真的从它取过料」。
    已知两个失真来源，使用时要记住：
      1. 同域名的多个源会得到相同数字（OpenAI News 与 OpenAI Research 都是 openai.com）；
      2. 域名根过短会误报（Google Alerts 的根是 google，会吃下正文里所有 Google）。
    因此**真正可用的输出是「零命中的那批」**——名字和域名在 001–006 正文里
    一次都没出现过，这批人值得重新评估；而"高命中"那批不要拿来当覆盖量对外声称。
    想要精确的"实际取料"记录，只能逐期人工登记，本脚本不替代它。
"""
import csv, io, os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(WS, "AI信息源分级清单-T0-T4.md")
CSV_OUT = os.path.join(WS, ".workbuddy", "data", "source_hits.csv")
COL_A, COL_B = "上次命中", "命中次数"
SRC_HEAD = ("信源", "地址")

STOP = {"ai", "api", "rss", "llm", "http", "https", "www", "com", "org", "net", "cn"}


def norm(s):
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", s.lower())


def is_cjk(s):
    return bool(s) and all("\u4e00" <= c <= "\u9fff" for c in s)


def aliases(name, url):
    out = set()
    n = norm(name)
    if len(n) >= 4:
        out.add(n)
    head = re.split(r"[（(]", name)[0]
    h = norm(head)
    if len(h) >= 2 and (is_cjk(h) or len(h) >= 4):
        out.add(h)
    m = re.match(r"https?://([^/]+)", url)
    if m:
        host = re.sub(r"^(www\.|api\.|docs\.|blog\.|s\.|m\.)", "", m.group(1).lower())
        root = host.split(".")[0]
        if len(root) >= 4 and root not in STOP:
            out.add(root)
    return {a for a in out if a and a not in STOP}


def split_row(ln):
    return [c.strip() for c in ln.strip().strip("|").split("|")]


def parse_sources(text):
    """返回 [(行号, 表序号, 名称, 地址)]，只认表头含「信源」「地址」的表。"""
    lines = text.split("\n")
    rows, tno, in_tbl = [], 0, False
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s.startswith("|"):
            in_tbl = False
            continue
        cells = split_row(s)
        if not in_tbl and len(cells) >= 2 and cells[0] == SRC_HEAD[0] and cells[1] == SRC_HEAD[1]:
            in_tbl, tno = True, tno + 1
            continue
        if in_tbl:
            if set("".join(cells)) <= set("-: "):      # 分隔行
                continue
            if len(cells) >= 2 and cells[1].startswith("http"):
                rows.append((i, tno, cells[0], cells[1]))
    return rows


def main():
    dry = "--dry" in sys.argv
    led = io.open(LEDGER, encoding="utf-8").read().replace("\r\n", "\n")
    rows = parse_sources(led)

    # 按文件名排序即为期次顺序（001 期文件名里没有「第 001 期」字样，故按位置兜底编号）
    files = sorted(fn for fn in os.listdir(WS) if re.match(r"^AI免费内容与权益速递.*\.md$", fn))
    issues = []
    for idx, fn in enumerate(files, 1):
        m = re.search(r"第\s*(\d{3})\s*期", fn)
        no = m.group(1) if m else "%03d" % idx
        txt = io.open(os.path.join(WS, fn), encoding="utf-8").read()
        issues.append((no, fn, norm(txt)))

    print("信源台账 : %d 条（%d 张表）" % (len(rows), len(set(r[1] for r in rows))))
    print("扫描期次 : %s" % "、".join("第%s期" % n for n, _, _ in issues))

    hits = {}
    for _, _, name, url in rows:
        al = aliases(name, url)
        got = []
        for no, fn, body in issues:
            c = sum(len(re.findall(re.escape(a), body)) for a in al)
            if c > 0:
                got.append((no, c))
        hits[name] = (got, al)

    nz = [k for k, (g, _) in hits.items() if g]
    print()
    print("有命中 : %d 条" % len(nz))
    print("零命中 : %d 条  <- 这批是「扫描时间可疑」的候选" % (len(rows) - len(nz)))
    print()
    top = sorted(nz, key=lambda k: -sum(c for _, c in hits[k][0]))[:12]
    print("产出最高的 12 条：")
    for k in top:
        g, _ = hits[k]
        print("   %-34s 命中 %d 期 / 共 %d 次  (%s)"
              % (k[:34], len(g), sum(c for _, c in g), ",".join(n for n, _ in g)))

    if dry:
        print()
        print("--dry：未写任何文件")
        return 0

    # ---- 写 CSV ----
    if not os.path.isdir(os.path.dirname(CSV_OUT)):
        os.makedirs(os.path.dirname(CSV_OUT))
    with io.open(CSV_OUT, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["信源", "地址", "命中期数", "命中次数", "上次命中", "命中期号明细", "匹配别名"])
        for _, _, name, url in rows:
            g, al = hits[name]
            w.writerow([name, url, len(g), sum(c for _, c in g),
                        g[-1][0] if g else "", "/".join(n for n, _ in g), " ".join(sorted(al))])
    print()
    print("CSV -> %s" % os.path.relpath(CSV_OUT, WS))

    # ---- 回写台账（幂等：先剥掉旧的这两列，再补） ----
    lines = led.split("\n")
    tmap = {}
    for i, tno, name, url in rows:
        g, _ = hits[name]
        tmap[i] = (g[-1][0] if g else "—", str(sum(c for _, c in g)) if g else "0")

    out, cur_hdr, cur_nbase, touched, skipped = [], None, 0, 0, 0
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s.startswith("|"):
            out.append(ln)
            cur_hdr = None
            continue
        cells = split_row(s)
        if cur_hdr is None and len(cells) >= 2 and cells[0] == SRC_HEAD[0] and cells[1] == SRC_HEAD[1]:
            # 幂等做法：记下**原表列数**，数据行一律只取前 n 列再补两列。
            # 不能靠「值等于列名」来剥列——第二次运行时数据行里已经写进去的
            # 005 / 3 这类值不匹配列名，剥不掉，表会每跑一次宽两列。
            # 同时保留原始列数：T3 的两张表只有 3 列（无「用途」列）。
            base = [c for c in cells if c not in (COL_A, COL_B)] or cells
            cur_nbase = len(base)
            cur_hdr = base + [COL_A, COL_B]
            out.append("| " + " | ".join(cur_hdr) + " |")
            continue
        if cur_hdr is None:
            out.append(ln)
            continue
        if set("".join(cells)) <= set("-: "):
            out.append("| " + " | ".join(["---"] * len(cur_hdr)) + " |")
            continue
        vals = tmap.get(i)
        if vals is None:
            out.append(ln); skipped += 1; continue
        out.append("| " + " | ".join(cells[:cur_nbase] + [vals[0], vals[1]]) + " |")
        touched += 1

    io.open(LEDGER, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("台账 -> 回写 %d 行，跳过 %d 行（非信源行）" % (touched, skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
