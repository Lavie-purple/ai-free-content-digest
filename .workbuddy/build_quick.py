#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成《免费速查》单页 —— 只回答四件事：给什么 / 多少 / 到什么时候 / 门槛。

设计原则（048 期起 · 用户 2026-10-27 提「主网页太臃肿，能不能只答重点」）：
  1. 只收「能拿到免费东西」的条目。发布 / 开源 / 申报 / 停服不进本页 —— 那些是新闻，
     不是「我现在能领什么」。边界写在页面顶部，读者不会以为漏了。
  2. 一条一行，四个字段写死，**不写沿革、不写避坑编号、不写期号**。要追证去完整版。
  3. 分区按「还剩几天」而不是按章节：先答「快没了」，再答「长期在那儿」。

数据源：.workbuddy/data/quick_items.csv（手工维护，一条一条核过原文）
用法：
  python build_quick.py                    # 基准日取最新一期 md 的日期
  python build_quick.py --today 2026-10-27
  python build_quick.py --check            # 只体检：找出截止表里有、速查表里漏的额度类条目
"""

import csv
import datetime as dt
import io
import os
import re
import sys
from string import Template

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(WS, ".workbuddy", "data", "quick_items.csv")
DEADLINES = os.path.join(WS, ".workbuddy", "data", "deadlines.csv")
OUT = os.path.join(WS, "quick.html")

GROUPS = [
    ("token", "Token 与积分", "登录或注册就能领的额度"),
    ("api", "模型 API 免费档", "能直接调用的免费模型与免费额度"),
    ("cloud", "云资源与工具", "服务器、部署额度、工具授权"),
    ("subsidy", "算力券与地方补贴", "企业向，多数要申报"),
    ("edu", "学生与教育", "在校师生专属"),
    ("oss", "开源与长期权益", "没有截止日、长期有效"),
]
GROUP_NAME = dict((k, n) for k, n, _ in GROUPS)
GROUP_NAME["over"] = "已结束"


# ---------------------------------------------------------------- 数据

def base_date(argv):
    for i, a in enumerate(argv):
        if a == "--today" and i + 1 < len(argv):
            return dt.date.fromisoformat(argv[i + 1])
    best = None
    for fn in os.listdir(WS):
        m = re.match(r"^AI免费内容与权益速递-第\d+期-(\d{4}-\d{2}-\d{2})\.md$", fn)
        if m:
            d = dt.date.fromisoformat(m.group(1))
            if best is None or d > best:
                best = d
    return best or dt.date.today()


def load():
    if not os.path.exists(SRC):
        raise SystemExit("找不到 %s" % SRC)
    rows = list(csv.DictReader(io.open(SRC, encoding="utf-8-sig")))
    for r in rows:
        r["days"] = None
        if r["截止日"]:
            try:
                r["days"] = (dt.date.fromisoformat(r["截止日"]) - BASE).days
            except ValueError:
                raise SystemExit("截止日写错了：%s / %s" % (r["名称"], r["截止日"]))
    return rows


def bucket(r):
    """把一行归到 倒计时 / 长期 / 已结束 三个区。"""
    if r["状态"] == "over":
        return "over"
    if r["days"] is not None:
        return "ticking"
    return "standing"


def when_text(r):
    """右列「到什么时候」的展示文本。"""
    if r["状态"] == "over":
        return r["截止说明"] or "已结束"
    if r["days"] is not None:
        d = r["days"]
        if d < 0:
            return "%s（已过 %d 天）" % (r["截止说明"], -d)
        if d == 0:
            return "%s（就是今天）" % r["截止说明"]
        return "%s（还有 %d 天）" % (r["截止说明"], d)
    return r["截止说明"] or "未公布"


def when_short(r):
    """移动端用的短版：只留「日期 · 天数」，长说明在窄屏会占三行。"""
    if r["状态"] == "over":
        return (r["截止说明"] or "已结束").split("（")[0][:12]
    if r["days"] is not None:
        d = r["days"]
        if d < 0:
            return "已过 %d 天" % -d
        if d == 0:
            return "今天截止"
        return "还有 %d 天" % d
    txt = r["截止说明"] or "未公布"
    return txt.split("（")[0][:12]


def tone(r):
    """色标：crit / soon / live / plan / over。"""
    if r["状态"] == "over":
        return "over"
    if r["days"] is not None:
        d = r["days"]
        if d <= 0:
            return "crit"
        if d <= 7:
            return "soon"
        return "live"
    if r["状态"] in ("unclear", "pending"):
        return "plan"
    return "live"


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


# ---------------------------------------------------------------- 渲染

def render_rows(rows, show_group=False):
    out = []
    for r in rows:
        t = tone(r)
        tag = ('<span class="tag">%s</span>' % esc(GROUP_NAME.get(r["分组"], r["分组"]))
               if show_group else "")
        out.append(
            '<tr data-t="%s">'
            '<td class="c-name"><span class="nm">%s</span>%s'
            '<span class="need">%s</span></td>'
            '<td class="c-qty">%s</td>'
            '<td class="c-when"><span class="dot"></span>'
            '<span class="w-l">%s</span><span class="w-s">%s</span></td>'
            "</tr>" % (t, esc(r["名称"]), tag, esc(r["门槛"]), esc(r["量"]),
                       esc(when_text(r)), esc(when_short(r)))
        )
    return "\n".join(out)


def table(head, rows, show_group=False):
    return (
        '<table class="qt"><thead><tr><th>给什么</th><th>能拿多少</th>'
        "<th>到什么时候</th></tr></thead><tbody>\n%s\n</tbody></table>" % render_rows(rows, show_group)
    )


def build(rows):
    ticking = sorted([r for r in rows if bucket(r) == "ticking"],
                     key=lambda r: (r["days"], r["名称"]))
    standing = [r for r in rows if bucket(r) == "standing"]
    over = sorted([r for r in rows if bucket(r) == "over"],
                  key=lambda r: (r["days"] if r["days"] is not None else 9999))

    n_live = len([r for r in rows if bucket(r) != "over"])
    n_week = len([r for r in ticking if r["days"] is not None and 0 <= r["days"] <= 7])
    n_over = len(over)

    # 长期区按分组切
    blocks = []
    for key, gname, gdesc in GROUPS:
        g = [r for r in standing if r["分组"] == key]
        if not g:
            continue
        blocks.append(
            '<h3 class="gh">%s<span class="gd">%s</span><span class="gc">%d 条</span></h3>\n%s'
            % (esc(gname), esc(gdesc), len(g), table(None, g))
        )

    over_block = ""
    if over:
        over_block = (
            '<details class="fold"><summary>已结束的 %d 条<span class="fd">留着做对照，'
            "点开看看哪些是刚关掉的</span></summary>\n%s\n</details>"
            % (n_over, table(None, over, show_group=True))
        )

    return Template(TEMPLATE).substitute({
        "date": BASE.strftime("%Y-%m-%d"),
        "n_live": n_live,
        "n_week": n_week,
        "n_over": n_over,
        "n_tick": len(ticking),
        "ticking": table(None, ticking, show_group=True) if ticking else '<p class="empty">当前没有带确切截止日的条目。</p>',
        "standing": "\n".join(blocks) if blocks else '<p class="empty">当前没有长期条目。</p>',
        "over": over_block,
        "n_all": len(rows),
    })


# ---------------------------------------------------------------- 体检

FREE_RE = re.compile(r"免费|试用|额度|积分|Tokens|token|赠送|白嫖|学生|新人|福利|礼包|抵扣|返还|补贴|券|免费层|free|Free")

# 故意不收的：不是「能白拿」，或者本身就不是一条额度。
# 这里必须显式写出来 —— 否则体检每期都会把这批当「漏登」刷屏，久了就没人看体检输出了。
SKIP_RE = re.compile(
    r"无免费层|无免费额度|促销价|免费档改版|留存口径|地区限制|广告测试"
    r"|停服|下线|停止服务|申报指南|清单$|政策实施细则"
)


def _grams(s):
    """2-gram 集合，用来算相似度。中文按字切，比整串包含稳得多。"""
    s = re.sub(r"[\s·（）()、，,。:：/—\-+“”\"'！!？?]", "", s)
    s = re.sub(r"\d+", "", s)
    return set(s[i:i + 2] for i in range(len(s) - 1))


def check(rows):
    """找出「截止表里算额度类、但速查表没写」的条目 —— 防止新增条目静默漏掉。

    判定用 2-gram 相似度而不是子串包含：同一条目在两张表里的写法几乎从不一样
    （「智谱清言「双节消耗积分 100% 返还」」vs「智谱清言 双节积分 100% 返还」），
    子串匹配会把 20 条已覆盖的条目报成漏登。
    """
    if not os.path.exists(DEADLINES):
        print("没有 deadlines.csv，跳过体检")
        return 0
    dl = list(csv.DictReader(io.open(DEADLINES, encoding="utf-8-sig")))
    have = [_grams(r["名称"]) for r in rows]

    miss, skipped = [], 0
    for r in dl:
        a = r["活动"]
        if not FREE_RE.search(a):
            continue
        if SKIP_RE.search(a):
            skipped += 1
            continue
        g = _grams(a)
        if not g:
            continue
        best = max((len(g & h) / float(len(g | h)) for h in have), default=0.0)
        if best >= 0.26:
            continue
        miss.append((best, r))

    if not miss:
        print("体检：额度类条目全部已覆盖（%d 条；另有 %d 条按规则不收）" % (len(rows), skipped))
        return 0
    print("体检：截止表里有 %d 条额度类条目没进速查表 ——" % len(miss))
    for best, r in sorted(miss):
        print("  [%s] %.2f  %s" % (r["状态"], best, r["活动"][:84]))
    print("\n（另按规则跳过 %d 条：无免费层 / 促销价 / 改版公告 / 指南类）" % skipped)
    return 1


# ---------------------------------------------------------------- 模板

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>免费速查 · AI 免费内容与权益速递</title>
<meta name="description" content="AI 免费额度速查：给什么、能拿多少、到什么时候结束，一条一行。">
<style>
:root{
  --bg:#faf8f4; --surface:#ffffff; --surface-2:#f4f1ea; --rule:#e2ddd1; --rule-2:#cfc8b8;
  --ink:#1b1913; --ink-2:#3a362d; --muted:#5f584a; --faint:#736a5a;
  --accent:#bf3327; --accent-ink:#a02a20; --accent-soft:rgba(191,51,39,.09);
  --crit:#8c1a10; --soon:#8f5e12; --live:#3b6a4d; --plan:#38587a; --over:#6e675c;
  --shadow:0 1px 2px rgba(27,25,19,.06),0 8px 24px -16px rgba(27,25,19,.18);
  --fs: "PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC",sans-serif;
  --fm:ui-monospace,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#14120e; --surface:#1b1813; --surface-2:#221e17; --rule:#332d24; --rule-2:#463e31;
    --ink:#ece7dc; --ink-2:#cec8ba; --muted:#9d9486; --faint:#8e8577;
    --accent:#ff6d55; --accent-ink:#ff8b76; --accent-soft:rgba(255,109,85,.13);
    --crit:#ff3b30; --soon:#e0a24a; --live:#6fbe8e; --plan:#82a9d6; --over:#9c9387;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px -16px rgba(0,0,0,.6);
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:var(--fs); font-size:15px; line-height:1.65;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:860px; margin:0 auto; padding:0 20px 72px}

/* ---------- 页头 ---------- */
header{padding:36px 0 0}
.kicker{
  font-family:var(--fm); font-size:11.5px; letter-spacing:.16em; text-transform:uppercase;
  color:var(--accent-ink); font-weight:600;
}
h1{
  font-size:30px; line-height:1.2; margin:8px 0 0; letter-spacing:-.02em; font-weight:800;
}
.lede{
  margin:10px 0 0; color:var(--ink-2); font-size:15px; max-width:56ch;
}
.lede b{color:var(--ink); font-weight:700}
hr.rule{border:0; border-top:2px solid var(--ink); margin:22px 0 0}

/* ---------- 数字条 ---------- */
.stats{
  display:flex; gap:0; margin:0 0 4px; border-bottom:1px solid var(--rule);
}
.stat{flex:1; padding:16px 0 14px; border-right:1px solid var(--rule)}
.stat:last-child{border-right:0}
.stat b{
  display:block; font-family:var(--fm); font-size:28px; line-height:1; font-weight:700;
}
.stat.live b{color:var(--live)} .stat.soon b{color:var(--soon)} .stat.over b{color:var(--over)}
.stat span{display:block; margin-top:5px; font-size:12.5px; color:var(--muted)}

/* ---------- 边界说明 ---------- */
.boundary{
  margin:18px 0 0; padding:11px 14px; background:var(--surface-2);
  border-left:2px solid var(--rule-2); font-size:13px; color:var(--muted); line-height:1.7;
}
.boundary b{color:var(--ink-2); font-weight:600}
.legend{
  margin:10px 0 0; font-size:12.5px; color:var(--faint); line-height:1.75;
}
.legend b{color:var(--muted); font-weight:600}

/* ---------- 分区 ---------- */
h2{
  font-size:13px; font-family:var(--fm); letter-spacing:.1em; text-transform:uppercase;
  color:var(--accent-ink); font-weight:700; margin:38px 0 0; padding-bottom:7px;
  border-bottom:1px solid var(--rule);
}
h2 .cnt{color:var(--faint); font-weight:500; letter-spacing:0; text-transform:none; margin-left:8px}
h2 .sub{display:block; font-family:var(--fs); font-size:13px; letter-spacing:0; text-transform:none;
  color:var(--muted); font-weight:400; margin-top:4px}
h3.gh{
  font-size:14.5px; margin:26px 0 8px; font-weight:700; display:flex; align-items:baseline; gap:9px;
  flex-wrap:wrap;
}
h3.gh .gd{font-size:12.5px; color:var(--muted); font-weight:400}
h3.gh .gc{
  font-family:var(--fm); font-size:11px; color:var(--faint); margin-left:auto;
}

/* ---------- 表 ---------- */
table.qt{
  width:100%; table-layout:fixed; border-collapse:collapse; margin:0; font-size:14px;
}
table.qt td,table.qt th{overflow-wrap:anywhere; word-break:break-word}
table.qt th{
  text-align:left; font-size:11px; font-family:var(--fm); letter-spacing:.08em;
  color:var(--faint); font-weight:500; padding:7px 10px 7px 0; border-bottom:1px solid var(--rule);
  text-transform:uppercase; white-space:nowrap;
}
table.qt th:nth-child(2){width:31%} table.qt th:nth-child(3){width:28%}
table.qt td{
  padding:8px 10px 8px 0; border-bottom:1px solid var(--rule); vertical-align:top;
}
table.qt tr:last-child td{border-bottom:0}
.nm{color:var(--ink); font-weight:600; display:inline; line-height:1.45}
.tag{
  display:inline-block; font-size:10.5px; font-family:var(--fm); color:var(--faint);
  border:1px solid var(--rule); padding:0 5px; border-radius:2px; margin-left:7px;
  vertical-align:1px; white-space:nowrap;
}
.need{display:block; font-size:11.5px; color:var(--faint); line-height:1.45; margin-top:3px}
.c-qty{color:var(--ink); font-weight:700; font-size:13.5px; line-height:1.55;
  font-variant-numeric:tabular-nums}
.c-when{font-size:12.5px; color:var(--ink-2); line-height:1.55}
.w-s{display:none}
.dot{
  display:inline-block; width:6px; height:6px; border-radius:50%; margin-right:6px;
  vertical-align:1px; background:var(--live);
}
tr[data-t="crit"] .dot{background:var(--crit)} tr[data-t="soon"] .dot{background:var(--soon)}
tr[data-t="plan"] .dot{background:var(--plan)} tr[data-t="over"] .dot{background:var(--over)}
tr[data-t="crit"] .c-when{color:var(--crit); font-weight:600}
tr[data-t="soon"] .c-when{color:var(--soon); font-weight:600}
tr[data-t="over"] .nm,tr[data-t="over"] .c-qty{color:var(--over); font-weight:500}
tr[data-t="over"] .c-when{color:var(--over)}

/* ---------- 折叠 ---------- */
details.fold{margin:36px 0 0; border-top:1px solid var(--rule); padding-top:18px}
details.fold summary{
  cursor:pointer; font-size:13px; color:var(--muted); list-style:none; padding:2px 0;
}
details.fold summary::-webkit-details-marker{display:none}
details.fold summary::before{content:"▸ "; color:var(--faint)}
details.fold[open] summary::before{content:"▾ "}
details.fold summary .fd{margin-left:10px; color:var(--faint); font-size:12.5px}
details.fold summary:hover{color:var(--ink)}
details.fold table{margin-top:12px}

.empty{color:var(--muted); font-size:13.5px; padding:14px 0}

/* ---------- 页脚 ---------- */
footer{
  margin:52px 0 0; padding-top:18px; border-top:2px solid var(--ink);
  font-size:12.5px; color:var(--faint); line-height:1.85;
}
footer a{color:var(--accent-ink); text-decoration:none; border-bottom:1px solid var(--accent-soft)}
footer a:hover{border-bottom-color:var(--accent)}
footer p{margin:0 0 6px}
footer b{color:var(--muted); font-weight:600}
.back{
  display:inline-block; margin-top:2px; font-family:var(--fm); font-size:12px;
  color:var(--accent-ink);
}

@media (max-width:640px){
  body{font-size:14px}
  h1{font-size:24px}
  .wrap{padding:0 15px 56px}
  .stat b{font-size:23px}
  /* 窄屏不再挤三列：一行一条，名称与短日期同行、额度单独一行 */
  table.qt{display:block}
  table.qt thead{display:none}
  table.qt tbody{display:block}
  table.qt tr{
    display:grid; grid-template-columns:1fr auto;
    grid-template-areas:"name when" "qty qty" "need need";
    column-gap:12px; row-gap:1px; padding:10px 0;
    border-bottom:1px solid var(--rule);
  }
  table.qt tr:last-child{border-bottom:0}
  table.qt td{display:block; border:0; padding:0 !important}
  /* display:contents 让 td 透明，名称 / 额度 / 门槛 三行按阅读顺序排 */
  .c-name{display:contents !important}
  .nm{grid-area:name}
  .need{grid-area:need}
  .c-when{grid-area:when; text-align:right; padding-top:2px !important}
  .c-qty{grid-area:qty; margin-top:3px}
  .w-l{display:none} .w-s{display:inline}
  .c-when{font-size:11.5px; white-space:nowrap}
  .c-qty{font-size:12.5px}
  .nm{font-size:13px}
  .need{font-size:11px; margin-top:2px}
  .tag{display:none}
}
@media print{
  body{background:#fff; color:#000}
  .wrap{max-width:none; padding:0}
  details.fold{display:block} details.fold summary{display:none}
  table.qt tr{break-inside:avoid}
  a{color:#000; text-decoration:none}
}
</style>
</head>
<body>
<div class="wrap">

<header>
  <div class="kicker">免费速查 · Free Tier Index</div>
  <h1>AI 免费额度，一条一行</h1>
  <p class="lede">只回答四个问题：<b>给什么</b>、<b>能拿多少</b>、<b>到什么时候结束</b>、<b>要什么门槛</b>。不写沿革、不写期号、不写论证过程。</p>
  <hr class="rule">
</header>

<div class="stats">
  <div class="stat live"><b>${n_live}</b><span>现在能拿</span></div>
  <div class="stat soon"><b>${n_week}</b><span>其中 7 天内截止</span></div>
  <div class="stat over"><b>${n_over}</b><span>已结束</span></div>
</div>

<div class="boundary">
  <b>本页不收什么：</b>模型发布、开源公告、申报通知、停服迁移这类「新闻」不在本页 —— 它们不是「我现在能领什么」。
  需要看这些，或者要查某条的依据、口径、历史变更，去<a href="index.html">完整版日报</a>。
  每一条的原文与核对时点都留在那里，本页只做「能不能白拿」的判断。
</div>

<p class="legend">
  <b>右列怎么读：</b>写<b>具体日期</b>的是限时活动，过期就没了；写<b>「长期 / 每日重置 / 按月」</b>的是常驻，
  额度可能调整、但不会到期；写<b>「领后 N 天」</b>的是领到手才开始算 —— 早领早用，放着不算数。
</p>

<h2>正在倒计时 <span class="cnt">${n_tick} 条 · 按剩余天数排</span>
  <span class="sub">有确切截止日的，先看这一区。橙点 7 天内到期，红点今天或已过。</span>
</h2>
${ticking}

<h2>长期有效 / 未公布截止日 <span class="cnt">按类型分组</span>
  <span class="sub">这些不会「过两天就没了」，但额度随时可能调整 —— 拿之前扫一眼右边的说明。</span>
</h2>
${standing}

${over}

<footer>
  <p><b>怎么读这本速查：</b>「能拿多少」一律写官方口径的数字，没写的写「见官方页」或「未公布」，不做估算、不把估算写成确定值。
     同一家的两笔额度分开列（例如 AutoClaw 的周福利与升级礼），不能相加 —— 计量单位或领取条件不同的额度互换没有意义。</p>
  <p><b>数字会变。</b>本页基准日 <b>${date}</b>，共 ${n_all} 条。厂商随时可能降档、提前收口或不公布结束日；
     看到「未公布」的，按「随时会关」处理，别拿它排长期计划。</p>
  <p><b>要追证：</b>每一条的原始出处、核对时点、口径变更与避坑记录，都在完整版日报里。
     <a href="index.html">完整版与历史各期 &#8594;</a></p>
  <p class="back">AI 免费内容与权益速递 · 免费速查</p>
</footer>

</div>
</body>
</html>
"""


# ---------------------------------------------------------------- 入口

def main():
    global BASE
    argv = sys.argv[1:]
    BASE = base_date(argv)
    rows = load()

    if "--check" in argv:
        raise SystemExit(check(rows))

    # 每条都必须在分组表里，否则页面上会凭空少一块
    unknown = sorted(set(r["分组"] for r in rows) - set(GROUP_NAME))
    if unknown:
        raise SystemExit("分组没登记：%s（在 GROUPS 里补一行）" % unknown)

    html = build(rows)

    # 占位符必须全被替换（${name} 形式，漏一个页面上就会露出字面量）
    left = re.findall(r"\$\{[a-z_]+\}", html)
    if left:
        raise SystemExit("还有占位符没填：%s" % set(left))

    io.open(OUT, "w", encoding="utf-8", newline="\n").write(html)
    print("quick.html 已生成：%d 条 / %d B / 基准日 %s"
          % (len(rows), len(html.encode("utf-8")), BASE))


if __name__ == "__main__":
    main()
