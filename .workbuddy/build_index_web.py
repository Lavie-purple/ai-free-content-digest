# -*- coding: utf-8 -*-
"""生成 GitHub Pages 站点首页 index.html（根路径 / 的入口页）。

为什么需要它：
    GitHub Pages 访问根路径时只认 index.html / index.md。日报文件名带中文
    （AI免费内容与权益速递-第006期-2026-09-17.html），根路径下没有 index.html
    就会返回 404 —— 页面提示原话是「For root URLs you must provide an
    index.html file」。

这个脚本产出的是**索引页而非跳转页**：只把最新一期做成一张大卡片，
其余各期排成列表。理由是读者到站点首页通常想看「最新那期」，
但也可能想翻旧期，跳转页会把后一种需求直接丢掉。

用法：
    python .workbuddy/build_index_web.py
"""
import html as H
import io
import os
import re
import urllib.parse

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(WS, "index.html")
DEF = "AI免费内容与权益速递-"

ACCENT = "#bf3327"


def tables_in(text):
    n, prev = 0, False
    for ln in text.split("\n"):
        cur = ln.strip().startswith("|")
        if cur and not prev:
            n += 1
        prev = cur
    return n


def pit_range(text):
    m = re.search(r"(?ms)^##+[^\n]*避坑[^\n]*\n(.*?)(?=^## |\Z)", text)
    if not m:
        return "—"
    nums = [int(x) for x in re.findall(r"(?m)^\s*(?:\*\*)?(\d{1,2})[\.、)]", m.group(1))]
    return "%d–%d" % (min(nums), max(nums)) if nums else "—"


def theme_of(text):
    m = re.search(r"(?m)^\*\*\d{4}-\d{2}-\d{2}（[^）]*）·\s*(.+?)\*\*\s*$", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"(?m)^\*\*主题[：:]\s*(.+?)\*\*\s*$", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"(?m)^\*\*(.+?)\*\*\s*$", text.lstrip("\n").split("\n", 1)[-1])
    return m.group(1).strip() if m else "—"


def abstract_of(text, n=4):
    """从「摘要（3 秒版）」里取前 n 条要点，去掉 markdown 标记。"""
    m = re.search(r"(?ms)^##+[^\n]*摘要[^\n]*\n(.*?)(?=^## |\Z)", text)
    if not m:
        return []
    out = []
    for ln in m.group(1).split("\n"):
        t = ln.strip()
        if not re.match(r"^[-*]\s+", t):
            continue
        t = re.sub(r"^[-*]\s+", "", t)
        t = re.sub(r"\*\*", "", t)
        t = re.sub(r"`([^`]*)`", r"\1", t)
        t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
        t = re.sub(r"^\s*[0-9]+[\.、)]\s*", "", t)
        if t:
            out.append(t)
        if len(out) >= n:
            break
    return out


def url_of(fn):
    """中文文件名 → 可点击 URL（RFC 3986 百分号编码）。"""
    return urllib.parse.quote(fn)


def main():
    files = sorted(fn for fn in os.listdir(WS)
                   if re.match(r"^" + re.escape(DEF) + r".*\.md$", fn))
    if not files:
        raise SystemExit("工作区里没找到日报 md")

    issues = []
    tot_md = 0
    for idx, fn in enumerate(files, 1):
        txt = io.open(os.path.join(WS, fn), encoding="utf-8").read()
        m = re.search(r"第\s*(\d{3})\s*期", fn)
        no = m.group(1) if m else "%03d" % idx
        d = re.search(r"(\d{4}-\d{2}-\d{2})", fn)
        size = os.path.getsize(os.path.join(WS, fn))
        tot_md += size
        hp = os.path.splitext(fn)[0] + ".html"
        has_html = os.path.exists(os.path.join(WS, hp))
        issues.append({
            "no": no, "date": d.group(1) if d else "—", "theme": theme_of(txt),
            "size": size, "tables": tables_in(txt), "pit": pit_range(txt),
            "md": fn, "html": hp if has_html else None,
            "abstract": abstract_of(txt),
        })

    issues.reverse()          # 新的在前
    latest = issues[0]
    rest = issues[1:]
    total_words = sum(len(re.sub(r"\s", "", io.open(os.path.join(WS, i["md"]), encoding="utf-8").read()))
                      for i in issues)

    # 台账/信源统计
    led = os.path.join(WS, "AI信息源分级清单-T0-T4.md")
    tiers, src_total = [], 0
    if os.path.exists(led):
        lt = io.open(led, encoding="utf-8").read()
        tiers = [int(x) for x in re.findall(r"(?m)^## T\d[^\n]*?（(\d+)）", lt)]
        src_total = sum(tiers)

    def esc(t):
        return H.escape(t, quote=True)

    # ---------------------------------------------------------------- 大卡片
    def big_card(it):
        btns = []
        if it["html"]:
            btns.append('<a class="btn primary" href="%s">读网页版 →</a>' % esc(url_of(it["html"])))
        btns.append('<a class="btn" href="%s">看 Markdown</a>' % esc(url_of(it["md"])))
        ab = ""
        if it["abstract"]:
            li = "".join("<li>%s</li>" % esc(x) for x in it["abstract"])
            ab = '<ul class="abs">%s</ul>' % li
        return """<article class="card big">
  <div class="tagline"><span class="dot"></span>最新一期</div>
  <div class="metaline"><b>第 %s 期</b><span class="sep">·</span>%s<span class="sep">·</span>%s 字<span class="sep">·</span>%d 张表</div>
  <h2><a href="%s">%s</a></h2>
  %s
  <div class="acts">%s</div>
</article>""" % (
            esc(it["no"]), esc(it["date"]), format(it["size"], ","), it["tables"],
            esc(url_of(it["html"] or it["md"])), esc(it["theme"]), ab, "".join(btns))

    # ---------------------------------------------------------------- 小行
    def row(it):
        link = it["html"] or it["md"]
        kind = "网页版" if it["html"] else "Markdown"
        return """<li class="row">
  <a href="%s">
    <span class="no">%s</span>
    <span class="d">%s</span>
    <span class="th">%s</span>
    <span class="pit">避坑 %s</span>
    <span class="kind">%s</span>
  </a>
</li>""" % (esc(url_of(link)), esc(it["no"]), esc(it["date"][5:]), esc(it["theme"]),
            esc(it["pit"]), kind)

    from datetime import date
    issue_range = "%s ~ %s" % (issues[-1]["date"], issues[0]["date"])
    today = date.today().isoformat()

    DOC = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 免费内容与权益速递 · 总目录</title>
<meta name="description" content="每天筛出 AI 免费额度、免费内容与分发入口的新变化，只做增量与纠错。已出 __CNT__ 期。">
<meta property="og:title" content="AI 免费内容与权益速递">
<meta property="og:description" content="每天筛出 AI 免费额度、免费内容与分发入口的新变化，只做增量与纠错。">
<meta property="og:type" content="website">
<style>
:root{
  --bg:#f2eee5; --surface:#fbf9f3; --surface-2:#f6f2e8;
  --ink:#1b1913; --ink-2:#3a362d; --muted:#5f584a; --faint:#736a5a;
  --rule:rgba(27,25,19,.16); --rule-2:rgba(27,25,19,.34); --rule-strong:rgba(27,25,19,.62);
  --accent:__ACCENT__; --accent-ink:#a02a20; --accent-soft:rgba(191,51,39,.10);
  --fd:Georgia,"Times New Roman","Source Han Serif SC","Songti SC","SimSun",serif;
  --fu:-apple-system,"Segoe UI","Microsoft YaHei","PingFang SC","Hiragino Sans GB",sans-serif;
  --fm:"Cascadia Mono",Consolas,"JetBrains Mono",Menlo,monospace;
  --shadow:0 1px 2px rgba(40,32,20,.10),0 8px 28px rgba(40,32,20,.07);
  --ease:cubic-bezier(.16,1,.3,1);
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#131210; --surface:#1c1a16; --surface-2:#232019;
    --ink:#ece7dc; --ink-2:#cec8ba; --muted:#9d9486; --faint:#8e8577;
    --rule:rgba(236,231,220,.15); --rule-2:rgba(236,231,220,.3); --rule-strong:rgba(236,231,220,.55);
    --accent:#ff6d55; --accent-ink:#ff8b76; --accent-soft:rgba(255,109,85,.14);
    --shadow:0 1px 2px rgba(0,0,0,.5),0 10px 30px rgba(0,0,0,.42);
  }
}
*,*::before,*::after{box-sizing:border-box}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:var(--fu); line-height:1.85; -webkit-text-size-adjust:100%;
}
body::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:radial-gradient(70rem 42rem at 8% -12%, var(--accent-soft), transparent 62%);
}
.wrap{position:relative; z-index:2; max-width:880px; margin:0 auto; padding:56px 24px 88px}
a{color:inherit}
header.top{border-bottom:3px solid var(--ink); padding-bottom:18px; margin-bottom:8px}
.kicker{
  font-family:var(--fm); font-size:12px; letter-spacing:.16em; text-transform:uppercase;
  color:var(--muted); display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap;
  padding-bottom:10px;
}
.kicker em{font-style:normal; color:var(--accent-ink)}
h1{
  font-size:clamp(30px,5.2vw,46px); line-height:1.14; margin:0 0 12px;
  font-weight:800; letter-spacing:-.01em;
}
.lede{
  font-family:var(--fd); font-size:17px; line-height:1.9; color:var(--ink-2);
  margin:0 0 18px; max-width:60ch;
}
.lede strong{color:var(--ink); font-weight:700}
.stats{
  display:flex; gap:22px; flex-wrap:wrap; font-family:var(--fm); font-size:12.5px;
  color:var(--muted); padding-top:4px;
}
.stats b{color:var(--ink); font-weight:700; font-size:15px; margin-right:4px}
section{margin-top:44px}
.slabel{
  font-family:var(--fm); font-size:11px; letter-spacing:.18em; text-transform:uppercase;
  color:var(--faint); padding-bottom:8px; margin-bottom:16px; border-bottom:1px solid var(--rule);
}
.card{
  background:var(--surface); border:1px solid var(--rule); border-radius:0 10px 10px 0;
  border-left:3px solid var(--accent); box-shadow:var(--shadow); padding:24px 26px;
}
.card .tagline{
  font-family:var(--fm); font-size:11px; letter-spacing:.16em; text-transform:uppercase;
  color:var(--accent-ink); display:flex; align-items:center; gap:7px; margin-bottom:10px;
}
.card .dot{width:7px;height:7px;border-radius:99px;background:var(--accent);display:inline-block}
.metaline{font-family:var(--fm); font-size:12.5px; color:var(--muted); margin-bottom:8px}
.metaline b{color:var(--ink)}
.metaline .sep{margin:0 8px; color:var(--faint)}
.card h2{
  font-size:clamp(22px,3.4vw,30px); line-height:1.3; margin:0 0 14px; font-weight:800;
}
.card h2 a{text-decoration:none; border-bottom:2px solid transparent; transition:border-color .18s}
.card h2 a:hover{border-bottom-color:var(--accent)}
ul.abs{list-style:none; margin:0 0 20px; padding:0; display:grid; gap:9px}
ul.abs li{
  position:relative; padding-left:19px; font-family:var(--fd); font-size:15.5px;
  line-height:1.85; color:var(--ink-2);
}
ul.abs li::before{
  content:""; position:absolute; left:2px; top:.8em; width:7px; height:1.5px; background:var(--accent);
}
.acts{display:flex; gap:10px; flex-wrap:wrap}
.btn{
  display:inline-block; padding:9px 18px; border-radius:99px; font-size:14px; font-weight:600;
  border:1px solid var(--rule-2); text-decoration:none; transition:all .18s var(--ease);
}
.btn:hover{border-color:var(--accent); color:var(--accent-ink); transform:translateY(-1px)}
.btn.primary{background:var(--ink); border-color:var(--ink); color:var(--bg)}
.btn.primary:hover{background:var(--accent); border-color:var(--accent); color:#fff}
ul.list{list-style:none; margin:0; padding:0; border-top:1px solid var(--rule)}
ul.list li.row{border-bottom:1px solid var(--rule)}
ul.list li.row a{
  display:grid;
  grid-template-columns:52px 68px minmax(0,1fr) auto auto;
  gap:14px; align-items:baseline; padding:13px 10px 13px 12px; text-decoration:none;
  border-left:3px solid transparent; transition:background .16s,border-color .16s;
}
ul.list li.row a:hover{background:var(--surface-2); border-left-color:var(--accent)}
.no{font-family:var(--fm); font-weight:700; color:var(--accent-ink); font-size:14px}
.d{font-family:var(--fm); font-size:12.5px; color:var(--faint)}
.th{font-size:14.5px; color:var(--ink-2); overflow-wrap:break-word}
.pit{font-family:var(--fm); font-size:11.5px; color:var(--faint); white-space:nowrap}
.kind{
  font-family:var(--fm); font-size:10.5px; letter-spacing:.06em; color:var(--muted);
  border:1px solid var(--rule); border-radius:3px; padding:1px 6px; white-space:nowrap;
}
footer{
  margin-top:56px; padding-top:20px; border-top:2px solid var(--ink);
  font-size:13.5px; color:var(--muted); line-height:1.9;
}
footer a{color:var(--accent-ink); text-decoration:none; border-bottom:1px solid var(--rule-2)}
footer a:hover{border-bottom-color:var(--accent)}
footer .fr{
  font-family:var(--fm); font-size:11px; letter-spacing:.12em; text-transform:uppercase;
  display:flex; justify-content:space-between; gap:14px; flex-wrap:wrap;
  padding-bottom:10px; margin-bottom:14px; border-bottom:1px solid var(--rule); color:var(--faint);
}
.warn{
  margin:26px 0 0; padding:14px 18px; border-left:3px solid var(--rule-strong);
  background:var(--surface-2); border-radius:0 8px 8px 0;
  font-size:13.5px; color:var(--muted); line-height:1.85;
}
@media (max-width:720px){
  .wrap{padding:36px 16px 64px}
  ul.list li.row a{grid-template-columns:52px minmax(0,1fr); gap:6px 12px}
  .d{order:2}
  .th{grid-column:2; font-size:14px}
  .pit,.kind{display:none}
  .card{padding:20px 18px}
  .stats{gap:16px}
}
@media (max-width:420px){
  .wrap{padding:26px 12px 52px}
  h1{font-size:clamp(24px,7.4vw,32px)}
  .lede{font-size:15.5px}
  .card{padding:18px 15px}
  ul.abs li{font-size:15px; padding-left:17px}
  ul.list li.row a{padding:11px 6px 11px 10px; grid-template-columns:46px minmax(0,1fr)}
  .no{font-size:13px}
  .btn{padding:8px 15px; font-size:13.5px}
}
@media print{
  body::before{display:none}
  .wrap{max-width:none; padding:0}
  .card,ul.list li.row a{box-shadow:none}
  .btn{display:none}
}
</style>
</head>
<body>
<div class="wrap">

<header class="top">
  <div class="kicker">
    <span>AI 免费内容与权益速递</span>
    <span>更新至 <em>第 __LATEST__ 期</em></span>
  </div>
  <h1>每天，哪些 AI 能力可以免费用</h1>
  <p class="lede">
    把散落在官方公告、模型卡、平台招募页和社区帖里的<strong>免费额度、免费内容与分发入口</strong>
    逐条核实，写清口径、标好截止日期。<strong>只做增量与纠错</strong>，不重复往期已固化的内容。
  </p>
  <div class="stats">
    <span><b>__CNT__</b>期</span>
    <span><b>__WORDS__</b>字</span>
    <span><b>__TABLES__</b>张表</span>
    <span><b>__SRC__</b>条信源</span>
  </div>
</header>

<section>
  <div class="slabel">最新一期</div>
  __BIG__
</section>

<section>
  <div class="slabel">全部 __CNT__ 期 · 新的在前</div>
  <ul class="list">
__ROWS__
  </ul>
</section>

<div class="warn">
  <strong>说明</strong>：这是一份人工核实过的情报整理，<strong>不构成投资、法律或商业决策建议</strong>。
  厂商条款与额度随时会变，请以官方页面为最终依据。<br>
  其中「免费」区分三种不同口径：<strong>零价格</strong> / <strong>限时试用</strong> / <strong>不限量但留存数据</strong>，
  报告里会在需要处写明条款分叉点。
</div>

<footer>
  <div class="fr"><span>AI 免费内容与权益速递</span><span>__RANGE__</span></div>
  <p>本页由 <code>.workbuddy/build_index_web.py</code> 自动生成，请勿手工编辑。</p>
  <p>仓库：<a href="https://github.com/Lavie-purple/ai-free-content-digest">Lavie-purple/ai-free-content-digest</a></p>
</footer>

</div>
</body>
</html>
"""

    doc = (DOC
           .replace("__ACCENT__", ACCENT)
           .replace("__CNT__", str(len(issues)))
           .replace("__LATEST__", latest["no"])
           .replace("__WORDS__", format(total_words, ","))
           .replace("__TABLES__", str(sum(i["tables"] for i in issues)))
           .replace("__SRC__", str(src_total) if src_total else "—")
           .replace("__RANGE__", issue_range)
           .replace("__BIG__", big_card(latest))
           .replace("__ROWS__", "\n".join(row(i) for i in rest))
           .replace("__TODAY__", today))

    io.open(OUT, "w", encoding="utf-8", newline="\n").write(doc)
    print("站点首页 -> index.html  %d bytes" % os.path.getsize(OUT))
    print("  共 %d 期（%s）· 合计 %d 字 · %d 张表 · 信源 %d 条"
          % (len(issues), issue_range, total_words,
             sum(i["tables"] for i in issues), src_total))
    print("  最新一期：第 %s 期 %s  %s" % (latest["no"], latest["date"], latest["theme"]))
    print("  旧期列表：%d 条" % len(rest))
    print("  网页版可用：%d / %d" % (sum(1 for i in issues if i["html"]), len(issues)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
