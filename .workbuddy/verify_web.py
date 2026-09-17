# -*- coding: utf-8 -*-
"""日报网页版（build_web.py 产物）的三项保真自查 + 结构自查。

用法： python verify_web.py <src.md> <out.html>
      不传参时自动取工作区里**日期最新**的一期（按文件名里的 YYYY-MM-DD 排序）。

检查项（每项都可复现，不靠目测）：
  1. 表格：md 与 html 的表数、每表列数、每表数据行数逐表比对
  2. 保真：md 的每个正文/单元格片段（去掉标点后 ≥12 字符）都能在 html 里找到
  3. 结构：标签闭合、占位符残留、外部资源引用（应为 0）
  4. 状态格：第四章状态列每格只应有一个色标、且不留裸变体选择符 U+FE0F
"""
import io, os, re, sys, html as H

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

if len(sys.argv) > 1:
    MD = sys.argv[1]
    HT = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(MD)[0] + ".html"
else:
    MD = pick_default()
    HT = os.path.splitext(MD)[0] + ".html"

print("src:", os.path.basename(MD))
md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
ht = io.open(HT, encoding="utf-8").read().replace("\r\n", "\n")

KEEP = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff]+")
key = lambda s: KEEP.sub("", s).lower()

def plain_html(t):
    return H.unescape(re.sub(r"<[^>]+>", "", t))

html_key = key(plain_html(ht))

# ---------- 1) 表格 ----------
def md_tables(text):
    blocks, cur = [], []
    for l in text.split("\n"):
        if l.strip().startswith("|"):
            cur.append(l)
        else:
            if cur: blocks.append(cur); cur = []
    if cur: blocks.append(cur)
    out = []
    for b in blocks:
        if len(b) < 2: continue
        nc = lambda s: len(s.strip().strip("|").split("|"))
        out.append((nc(b[0]), len(b) - 2))
    return out

def html_tables(text):
    out = []
    for m in re.finditer(r"<table[\s\S]*?</table>", text):
        blk = m.group(0)
        ncol = len(re.findall(r"<th[^>]*>", blk))
        trs = re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", blk)
        datas = [len(re.findall(r"<td[^>]*>", t)) for t in trs]
        datas = [d for d in datas if d > 0]
        out.append((ncol, len(datas), sorted(set(datas))))
    return out

mt, htl = md_tables(md), html_tables(ht)
ok = len(mt) == len(htl)
for i, (m, h) in enumerate(zip(mt, htl)):
    mc, mr = m; hc, hr, hcols = h
    good = (hcols == [mc] and hr == mr)
    ok = ok and good
    if not good:
        print("  [X] 表 %d: md(列=%d 行=%d) html(列=%d 行=%d %s)" % (i + 1, mc, mr, hc, hr, hcols))
print("1) 表格: md=%d html=%d 逐表列数/行数一致=%s" % (len(mt), len(htl), ok))

# ---------- 2) 保真 ----------
miss = []
for l in md.split("\n"):
    if l.lstrip().startswith("#"):
        continue          # 标题另做结构核对（html 的章节号是 01/02…，md 是一/二…）
    ls = l.strip()
    if not ls: continue
    parts = ls.strip("|").split("|") if ls.startswith("|") else [ls]
    for p in parts:
        k = key(p)
        if len(k) >= 12 and k not in html_key:
            miss.append((p.strip()[:70], k[:70]))
print("2) 保真: 缺失片段 %d" % len(miss))
for a, b in miss[:8]:
    print("   MISS:", a, "\n         key:", b)

# ---------- 3) 结构 ----------
bad = 0
for tag in ["div", "table", "thead", "tbody", "tr", "td", "th", "section", "span", "p", "ul", "ol",
            "li", "details", "summary", "button", "code", "strong", "nav", "main", "aside",
            "header", "footer", "h1", "h2", "h3", "h4", "a", "b", "i"]:
    o = len(re.findall(r"<%s[\s>]" % tag, ht)); c = len(re.findall(r"</%s>" % tag, ht))
    if o != c:
        bad += 1; print("  [X] <%s> open=%d close=%d" % (tag, o, c))
ph = 0
for pat in [r"\{\{", r"TODO", r"XXX", r">>>", r"None(?![a-zA-Z])", r"undefined"]:
    n = len(re.findall(pat, ht))
    if n: print("  [!] 占位符 %s = %d" % (pat, n)); ph += n
ext = len(re.findall(r"(?:src|href)\s*=\s*[\"']https?://", ht)) + len(re.findall(r"url\(\s*[\"']?https?://", ht))
print("3) 结构: 未闭合标签=%d 占位符=%d 外部引用=%d" % (bad, ph, ext))

# ---------- 4) 状态格 ----------
ST = "[\U0001F534\U0001F7E0\U0001F7E2\u26AA\u26A0]\uFE0F?"
sts = re.findall(r'<td data-col="st">([\s\S]*?)</td>', ht)
multi = sum(1 for s in sts if len(re.findall(ST, s)) > 1)
vs16 = sum(1 for s in sts if "\uFE0F" in s)
print("4) 状态格: 共 %d 格，多色标=%d，裸VS16=%d" % (len(sts), multi, vs16))

secs = len(re.findall(r"<section", ht)); h2 = len(re.findall(r"<h2", ht)); h3 = len(re.findall(r"<h3", ht))
md_h2 = len(re.findall(r"^##\s", md, re.M)); md_h3 = len(re.findall(r"^###\s", md, re.M))
print("   结构计数: section=%d h2=%d(md %d) h3=%d(md %d)" % (secs, h2, md_h2, h3, md_h3))

green = ok and not miss and bad == 0 and ph == 0 and ext == 0 and multi == 0 and vs16 == 0 and h2 == md_h2 and h3 == md_h3
print("VERDICT:", "ALL GREEN" if green else "NEEDS REVIEW")
