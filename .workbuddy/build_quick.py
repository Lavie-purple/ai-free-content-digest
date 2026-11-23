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

产物（2026-11-02 起）：
  · quick.html —— 极速视图本体
  · index.html —— **与 quick.html 逐字节相同**。站点根路径直接落到极速视图，
                  不再经过「总目录」中转页；往期总目录移到 archive.html
                  （由 build_index_web.py 生成），页脚「历史各期索引」指向它。
"""

import csv
import datetime as dt
import io
import os
import re
import sys
from string import Template

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import datebadge
import themeswitch
import viewswitch
SRC = os.path.join(WS, ".workbuddy", "data", "quick_items.csv")
DEADLINES = os.path.join(WS, ".workbuddy", "data", "deadlines.csv")
OUT = os.path.join(WS, "quick.html")
# 2026-11-02 起（用户要求「以后每天运行都把极速视图作为首页」）：
# 站点根路径 `index.html` **就是极速视图本身**，与 quick.html **逐字节相同**。
# 同一份字符串写两次，不做任何替换 —— 两份文件一旦分叉，就等于「首页」和
# 「极速视图」两个名字指向两种内容，读者点进来看到的东西随时可能不一样。
# 分叉由 check_views.py 用 `bytes 相等` 断言守住（不是靠记忆）。
OUT_HOME = os.path.join(WS, "index.html")

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

    # 三档视图切换器：放在刊头之后、统计之前，与日报页 / 总账页同一位置同一外观
    n_ledge = None
    _lp = os.path.join(WS, "常驻权益总账.md")
    if os.path.exists(_lp):
        _lt = io.open(_lp, encoding="utf-8").read()
        n_ledge = max(sum(1 for _l in _lt.split("\n")
                          if _l.strip().startswith("|")
                          and not re.match(r"^\|\s*-", _l.strip())) - 1, 0)
    full_href = viewswitch.latest_issue_html(WS) or "index.html"
    vs_html = viewswitch.render("quick", n_quick=len(rows), n_ledger=n_ledge,
                                full_href=full_href, ws=WS)

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
        # 页头日期条：读者第一眼要看到的「这是哪一天」。
        # 日期取 BASE（最新一期 md 的日期）—— 与页脚「本页基准日」同源，
        # 两处不一致就说明 CSV 与日报没对齐，属于出刊事故而不是显示问题。
        "datebar": datebadge.render(
            BASE.strftime("%Y-%m-%d"),
            note="%d 条在册" % len(rows)),
        "db_css": datebadge.CSS,
        "n_live": n_live,
        "n_week": n_week,
        "n_over": n_over,
        "n_tick": len(ticking),
        "ticking": table(None, ticking, show_group=True) if ticking else '<p class="empty">当前没有带确切截止日的条目。</p>',
        "standing": "\n".join(blocks) if blocks else '<p class="empty">当前没有长期条目。</p>',
        "over": over_block,
        "n_all": len(rows),
        "viewswitch": vs_html,
        "full_href": full_href,
        "vs_css": viewswitch.CSS,
        # 皮肤切换（2026-11-23）：三个占位符 + 一段暗色变量。
        # 暗色值沿用本页原有那套（没有跟日报统一 —— 两页底色本来就差一点，
        # 强行拉齐会改变既有观感；要统一的是「按钮行为」，不是色号）。
        "ts_head": themeswitch.HEAD_JS,
        "ts_css": themeswitch.CSS,
        "ts_btn": themeswitch.button(),
        # 页脚那枚不写 id（同页重复 id 不合法）；JS 按 .themebtn 类同时绑两枚。
        "ts_btn_foot": themeswitch.button(bid=None),
        "ts_js": themeswitch.JS,
        "ts_dark": themeswitch.dark_block(
            "--bg:#14120e; --surface:#1b1813; --surface-2:#221e17; --rule:#332d24; --rule-2:#463e31;"
            " --ink:#ece7dc; --ink-2:#cec8ba; --muted:#9d9486; --faint:#8e8577;"
            " --accent:#ff6d55; --accent-ink:#ff8b76; --accent-soft:rgba(255,109,85,.13);"
            " --crit:#ff3b30; --soon:#e0a24a; --live:#6fbe8e; --plan:#82a9d6; --over:#9c9387;"
            " --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px -16px rgba(0,0,0,.6)"
        ),
    })


# ---------------------------------------------------------------- 体检

FREE_RE = re.compile(r"免费|试用|额度|积分|Tokens|token|赠送|白嫖|学生|新人|福利|礼包|抵扣|返还|补贴|券|免费层|free|Free")

# 故意不收的：不是「能白拿」，或者本身就不是一条额度。
# 这里必须显式写出来 —— 否则体检每期都会把这批当「漏登」刷屏，久了就没人看体检输出了。
SKIP_RE = re.compile(
    r"无免费层|无免费额度|促销价|免费档改版|留存口径|地区限制|广告测试"
    r"|停服|下线|停止服务|申报指南|清单$|政策实施细则"
    # 050 期新增：免费端点已标 Deprecated / 弃用的 —— 不是「现在能白拿」的额度
    # （`NVIDIA` 官方 `nemotron-3-super-120b-a12b` 的 `Free Endpoint` 标 `Deprecated`，
    #   但 `Partner Endpoint` 与权重仍 `Available` —— 入口在、不免费）
    r"|Deprecated|弃用"
    # 053 期新增：**付费档**的额度变动 —— 读者拿不到任何免费东西。
    # （`OpenAI` 本期把 `Pro 100` / `Pro 500` / `Pro 200` 三档付费档的用量上限翻倍，
    #   但 `Plus` 档不变 —— 那一行是本期唯一与免费读者有关的事实，仍然不是「一条免费额度」，
    #   不该进速查页的「我现在能领什么」清单。）
    r"|付费档"
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
<meta name="color-scheme" content="light dark">
${ts_head}
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
${ts_dark}
*{box-sizing:border-box}
/* hidden 属性必须压过作者样式：
   `h3.gh` 写了 display:flex，浏览器默认的 `[hidden]{display:none}` 会被它盖掉，
   于是筛选时表藏了、标题还杵在那儿（2026-11-23 实测：h3.hidden === true 却仍然可见）。
   加 !important 是因为窄屏那段还把 `table.qt tr` 改成了 display:grid。 */
[hidden]{display:none !important}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:var(--fs); font-size:15px; line-height:1.65;
  -webkit-font-smoothing:antialiased;
}
/* 2026-11-23：原来钉死 860px。1920 屏上实测左 512 / 右 512 全空，正文只占 45%，
   而同一刊的完整日报与常驻总账都是 1240px —— 三视图并排截图时本页窄一大截。
   统一到 1240：宽屏不再白扔一半地方，与另外两页的版心右边界也对得上。 */
.wrap{max-width:1240px; margin:0 auto; padding:0 20px 72px}

/* ---------- 页头 ---------- */
header{padding:36px 0 0}
.kicker{
  font-family:var(--fm); font-size:11.5px; letter-spacing:.16em; text-transform:uppercase;
  color:var(--accent-ink); font-weight:600;
  /* 2026-11-23：右侧原来只有一枚「往期总目录」，现在加上皮肤切换按钮。
     改 flex 是为了让两者一起贴右、且窄屏能整块换行（原来 .arc 是 float，按钮没处放）。 */
  display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap;
}
.kicker .kick-tools{display:flex; align-items:center; gap:10px; margin-left:auto}
/* 首页（= 本页）不再是总目录，往期入口缩到页头右上角一行小字：
   不占首屏、但也不必翻到页脚才找得到。 */
.kicker .arc{
  letter-spacing:0; text-transform:none; font-weight:500;
  color:var(--muted); text-decoration:none; border-bottom:1px solid var(--rule);
}
.kicker .arc:hover{color:var(--accent-ink); border-bottom-color:var(--accent)}
h1{
  font-size:30px; line-height:1.2; margin:8px 0 0; letter-spacing:-.02em; font-weight:800;
}
.lede{
  /* 2026-11-06：原来 max-width:56ch 把导语挤成左侧一窄条，
     右边空一大块，与下面的表格不同宽 —— 去掉限制，与正文同宽。 */
  margin:10px 0 0; color:var(--ink-2); font-size:15px;
}
.lede b{color:var(--ink); font-weight:700}
hr.rule{border:0; border-top:2px solid var(--ink); margin:22px 0 0}

/* ---------- 概览句 ----------
   2026-11-06 改版：旧版是三等分数字格，每个数字独占一格、上下有横线、
   格间有竖线，看起来像被框住的 KPI 面板（用户：「不要这样框法」）。
   改成一行摘要句：主读数在前、两条附注随后，数字跟着文字走；
   不画任何框线、不加底色，与 archive.html 的统计行同族（内联数字），
   但用字号分出主次，三个数字仍各自保留状态色。 */
.pulse{
  display:flex; flex-wrap:wrap; align-items:baseline; gap:2px 0;
  margin:20px 0 0; padding:0; line-height:1.6;
}
.pulse-lead{
  font-size:14px; font-weight:600; color:var(--ink-2); white-space:nowrap;
}
.pulse-lead b{
  font-family:var(--fm); font-size:29px; line-height:1; font-weight:700;
  color:var(--live); margin-right:5px; vertical-align:-2px;
  font-variant-numeric:tabular-nums;
}
.pulse-rest{font-size:13px; color:var(--muted)}
.pulse-rest b{
  font-family:var(--fm); font-size:15px; font-weight:700;
  font-variant-numeric:tabular-nums;
}
.pulse-rest b.hot{color:var(--soon)}
.pulse-rest b.done{color:var(--over)}

/* 2026-11-06：首屏原有一块「本页不收什么」的口径说明（带背景与左边框），
   用户明确说「这段其实不用显示给用户看」—— 从首屏移除，内容不删，
   整合进页脚「要追证」一段；这里不再保留 .boundary 样式。 */
.legend{
  margin:20px 0 0; font-size:12.5px; color:var(--faint); line-height:1.75;
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
  /* 页脚这枚皮肤按钮是「滚到表尾也能切」的兜底（页头那枚会滚出视野）。
     改 flex 是为了让按钮与刊名同基线；文字那半不加弹性，按钮紧跟着不飘到右边。 */
  display:flex; align-items:center; gap:12px; flex-wrap:wrap;
  margin-top:2px; font-family:var(--fm); font-size:12px;
  color:var(--accent-ink);
}

@media (max-width:640px){
  body{font-size:14px}
  h1{font-size:24px}
  .wrap{padding:0 15px 56px}
  .pulse-lead b{font-size:25px}
  .pulse-rest{font-size:12.5px}
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
  /* 筛选条在窄屏：chip 占第一行（可换行），计数跟右，检索框整行垫底 */
  .tools{gap:8px; margin-top:18px}
  .chips{order:1; gap:5px}
  .chips-label{display:none}
  .chip{font-size:12px; padding:6px 9px}
  .tools-count{order:2}
  .qsearch{order:3; flex:1 1 100%; max-width:none}
  .qtop{right:12px; bottom:14px; width:42px; height:42px}
}
@media print{
  body{background:#fff; color:#000}
  .wrap{max-width:none; padding:0}
  details.fold{display:block} details.fold summary{display:none}
  table.qt tr{break-inside:avoid}
  a{color:#000; text-decoration:none}
  .tools,.qtop,.qempty{display:none !important}
  mark.hl{background:none; color:inherit}
}
/* ---------- 筛选条 + 检索 + 回顶（2026-11-23） ----------
   起因：极速页 8 张表 112 行，缺了日报 / 总账都有的「按状态筛」与「全文检索」，
   想只看 7 天内到期的条目只能肉眼扫；滚到底想回顶也只能手划。
   这里的三件是本页专属实现（日报那套绑在顶栏抽屉与单张 .tbl.ledger 上，
   直接搬过来会把「只筛一张表」的假设带进来 —— 本页要筛的是全部 8 张）。
   计数一律从表体实算（JS 里 counts），不写死数字。 */
.tools{
  display:flex; flex-wrap:wrap; align-items:center; gap:10px 12px;
  margin:22px 0 0; padding-top:14px; border-top:1px solid var(--rule);
}
.chips{display:flex; flex-wrap:wrap; align-items:center; gap:6px; flex:1 1 auto; order:1}
.chips-label{
  font-family:var(--fm); font-size:10.5px; letter-spacing:.12em; text-transform:uppercase;
  color:var(--faint); margin-right:2px;
}
.chip{
  display:inline-flex; align-items:center; gap:5px;
  font-family:var(--fs); font-size:12.5px; line-height:1;
  padding:6px 10px; border:1px solid var(--rule-2); border-radius:999px;
  background:transparent; color:var(--ink-2); cursor:pointer;
  transition:color .15s,border-color .15s,background .15s;
}
.chip b{font-family:var(--fm); font-size:10.5px; color:var(--faint); font-weight:600}
/* chip 上的小圆点与表格右列的 .dot 同色同尺寸 —— 两处色标必须能对上，
   否则读者筛了「7 天内」，表里那列点却是另一种颜色，等于没说 */
.chip .cd{width:7px; height:7px; border-radius:50%; display:inline-block; flex:0 0 auto; background:var(--live)}
.chip[data-f="crit"] .cd{background:var(--crit)}
.chip[data-f="soon"] .cd{background:var(--soon)}
.chip[data-f="plan"] .cd{background:var(--plan)}
.chip[data-f="over"] .cd{background:var(--over)}
.chip:hover{border-color:var(--accent); color:var(--accent-ink)}
.chip.on{background:var(--ink); border-color:var(--ink); color:var(--bg)}
.chip.on b{color:var(--bg); opacity:.7}
.chip:focus-visible{outline:2px solid var(--accent); outline-offset:2px}

/* 检索框整行垫底（flex-basis 100% 强制换行）：chip 行撑满、计数留在同行右端，
   检索框换到第二行占左半 —— 否则 860px 容器里三样抢一行，计数会被挤成孤零零一行。 */
.qsearch{display:flex; align-items:center; gap:8px; flex:1 1 100%; max-width:360px; order:3}
.qsearch input{
  flex:1 1 auto; min-width:0;
  font-family:var(--fs); font-size:12.5px; color:var(--ink);
  background:var(--surface); border:1px solid var(--rule-2); border-radius:999px;
  padding:6px 11px; outline:none;
}
.qsearch input:focus{border-color:var(--accent)}
.qsearch input::placeholder{color:var(--faint)}
.qnav{display:flex; align-items:center; gap:3px; font-family:var(--fm); font-size:10.5px; color:var(--faint);
  font-variant-numeric:tabular-nums; white-space:nowrap}
.qnav button{
  width:21px; height:21px; padding:0; font-size:10px; line-height:1;
  background:transparent; border:1px solid var(--rule); border-radius:3px;
  color:var(--muted); cursor:pointer;
}
.qnav button:hover{color:var(--accent-ink); border-color:var(--accent)}
.tools-count{
  /* order 必须在检索框之前：DOM 里它是最后一个，若按原序排，
     `flex-basis:100%` 的检索框会先占掉第二行，计数就被一起拖下去。 */
  order:2; margin-left:auto; font-family:var(--fm); font-size:11px; color:var(--faint);
  font-variant-numeric:tabular-nums; white-space:nowrap;
}
mark.hl{background:rgba(255,196,0,.35); color:inherit; padding:0 1px; border-radius:2px}
mark.hl.cur{background:var(--accent); color:#fff}
.qempty{display:none; margin:16px 0 0; font-size:13.5px; color:var(--muted)}
.qempty.show{display:block}

/* 回到顶部：表格长到 112 行，滚到底部想回顶不该靠手划 */
.qtop{
  position:fixed; right:18px; bottom:20px; z-index:30;
  width:40px; height:40px; padding:0;
  display:none; align-items:center; justify-content:center;
  font-size:14px; line-height:1;
  background:var(--surface); color:var(--muted);
  border:1px solid var(--rule-2); border-radius:50%;
  box-shadow:var(--shadow); cursor:pointer;
  transition:color .15s,border-color .15s;
}
.qtop.show{display:inline-flex}
.qtop:hover{color:var(--accent-ink); border-color:var(--accent)}
.qtop:focus-visible{outline:2px solid var(--accent); outline-offset:2px}

/* ---------- 宽屏（≥1080） ----------
   版心由 860 放宽到 1240 之后，三列表若仍按 41/31/28 分，
   「到什么时候」会空出 330 多像素只放一行短日期，行看着左重右轻。
   宽屏按 44/32/24 重分：名称列放得下「名称 + 标签 + 门槛小字」，
   日期列收到 24% 刚好容下「12/20（27 天）」。
   检索框同步由 360 放到 440 —— 1240 宽的版心里 360 像根短棍。
   注意：这段必须在「筛选条」那批规则之后（.qsearch 基础值写在 593 行），
   否则同特异性下会被基础值盖回去。 */
@media (min-width:1080px){
  /* 字号要跟着版心上调：15px / 14px 是给 860 宽定的，
     同样的字号放到 1240 里，一眼看上去就是「行很稀、字很小」。 */
  body{font-size:16px}
  h1{font-size:34px}
  .lede{font-size:15.5px}
  table.qt{font-size:15px}
  .nm{font-size:15px}
  .c-qty{font-size:14px}
  .c-when{font-size:13px}
  .need{font-size:12px}
  .chip{font-size:12.5px}
  /* 检索框基础值是 flex:1 1 100%（窄屏要它独占一行），
     放到 1080+ 就变成「第一行 chip+计数、第二行只剩一个检索框、右边全空」。
     宽屏改成可伸缩的一行：chip | 检索 | 计数。 */
  .qsearch{order:2; flex:1 1 200px; min-width:160px; max-width:440px}
  .tools-count{order:3}
  /* 分区标题右侧的「N 条」原本靠 margin-left:auto 推到版心最右（860 宽时只隔 600px，
     像个右对齐的页码）。1240 之下会隔到 1000px 开外，标题与条数读起来像两个无关的东西。
     宽屏改成紧跟描述，扫读时「标题 → 说明 → 几条」是连着的。 */
  h3.gh .gc{margin-left:14px}
  /* 列宽：名称 42 / 额度 31 / 时间 27。
     第三列不是一行短日期，是「失效时间 + 领取限制」的长句，
     按 24% 分会把 288px 塞成四五行；第一列反倒常剩大段空白。 */
  table.qt th:nth-child(1){width:42%}
  table.qt th:nth-child(2){width:31%}
  table.qt th:nth-child(3){width:27%}
}

${vs_css}
${db_css}
${ts_css}
</style>
</head>
<body>
<div class="wrap">

<header>
  <div class="kicker">
    <span class="kick-t">免费速查 · Free Tier Index</span>
    <span class="kick-tools"><a class="arc" href="archive.html">往期总目录 &#8594;</a>${ts_btn}</span>
  </div>
  ${datebar}
  <h1>AI 免费额度，一条一行</h1>
  <p class="lede">只回答四个问题：<b>给什么</b>、<b>能拿多少</b>、<b>到什么时候结束</b>、<b>要什么门槛</b>。不写沿革、不写期号、不写论证过程。</p>
  <hr class="rule">
  ${viewswitch}
</header>

<p class="pulse">
  <span class="pulse-lead"><b>${n_live}</b> 条现在能拿，</span>
  <span class="pulse-rest">其中 <b class="hot">${n_week}</b> 条 7 天内截止，<b class="done">${n_over}</b> 条已结束</span>
</p>

<p class="legend">
  <b>右列怎么读：</b>写<b>具体日期</b>的是限时活动，过期就没了；写<b>「长期 / 每日重置 / 按月」</b>的是常驻，
  额度可能调整、但不会到期；写<b>「领后 N 天」</b>的是领到手才开始算 —— 早领早用，放着不算数。
</p>

<div class="tools">
  <div class="chips" role="group" aria-label="按状态筛选">
    <span class="chips-label">按状态筛</span>
    <button class="chip on" data-f="all" aria-pressed="true">全部<b data-c="all">0</b></button>
    <button class="chip" data-f="crit" aria-pressed="false"><i class="cd" aria-hidden="true"></i>今天或已过<b data-c="crit">0</b></button>
    <button class="chip" data-f="soon" aria-pressed="false"><i class="cd" aria-hidden="true"></i>7 天内<b data-c="soon">0</b></button>
    <button class="chip" data-f="live" aria-pressed="false"><i class="cd" aria-hidden="true"></i>在期 / 长期<b data-c="live">0</b></button>
    <button class="chip" data-f="plan" aria-pressed="false"><i class="cd" aria-hidden="true"></i>未公布<b data-c="plan">0</b></button>
    <button class="chip" data-f="over" aria-pressed="false"><i class="cd" aria-hidden="true"></i>已结束<b data-c="over">0</b></button>
  </div>
  <div class="qsearch">
    <input id="q" type="search" placeholder="检索本页…" aria-label="检索本页" autocomplete="off">
    <span class="qnav"><span id="qn" aria-live="polite">0</span><button id="qprev" type="button" aria-label="上一个">&#8593;</button><button id="qnext" type="button" aria-label="下一个">&#8595;</button></span>
  </div>
  <span class="tools-count" id="qcount" aria-live="polite"></span>
</div>
<p class="qempty" id="qempty">该状态下没有条目 —— 点「全部」回来。</p>

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
  <p><b>要追证：</b>本页只收「我现在能领什么」—— 模型发布、开源公告、申报通知、停服迁移这类新闻不在此列。
     每一条的原文、原始出处、核对时点、口径与历史变更、避坑记录都在完整版日报里，本页只做「能不能白拿」的判断。
     <a href="${full_href}">读本期完整日报 &#8594;</a>　<a href="archive.html">历史各期索引 &#8594;</a></p>
  <p class="back"><span>AI 免费内容与权益速递 · 免费速查</span>${ts_btn_foot}</p>
</footer>

</div>
<button class="qtop" id="qtop" type="button" aria-label="回到顶部">&#8593;</button>
${ts_js}
<script>
/* 极速页工具条：按状态筛选 + 全文检索 + 回到顶部（2026-11-23）
   三者都不写死数字：筛选角标与「显示 N / M 条」都从表体实算，
   改 CSV 行数后自动跟上（写死的话过一期就是错的）。 */
(function(){
  "use strict";
  var tables=[].slice.call(document.querySelectorAll("table.qt")),
      chips=[].slice.call(document.querySelectorAll(".chip")),
      cnt=document.getElementById("qcount"),
      empty=document.getElementById("qempty"),
      q=document.getElementById("q"),
      qn=document.getElementById("qn"),
      filter="all", total=0, marks=[], cur=-1;

  /* ---------- 筛选 ---------- */
  var counts={all:0};
  tables.forEach(function(t){
    [].slice.call(t.querySelectorAll("tbody tr[data-t]")).forEach(function(r){
      var s=r.getAttribute("data-t");
      counts[s]=(counts[s]||0)+1; counts.all++;
    });
  });
  total=counts.all;
  [].slice.call(document.querySelectorAll("[data-c]")).forEach(function(b){
    b.textContent=(counts[b.getAttribute("data-c")]||0);
  });

  function apply(){
    var shown=0;
    tables.forEach(function(t){
      var vis=0;
      [].slice.call(t.querySelectorAll("tbody tr[data-t]")).forEach(function(r){
        var ok=(filter==="all"||r.getAttribute("data-t")===filter);
        r.hidden=!ok; if(ok) vis++;
      });
      t.hidden=(vis===0);
      shown+=vis;
    });
    /* 分区标题跟着表走：表藏了标题还留着，就是一句悬空的空话 */
    [].slice.call(document.querySelectorAll("h3.gh")).forEach(function(h){
      var n=h.nextElementSibling;
      h.hidden=!!(n&&n.tagName==="TABLE"&&n.hidden);
    });
    [].slice.call(document.querySelectorAll("h2")).forEach(function(h){
      var vis=0,n=h.nextElementSibling;
      /* 只看到下一个 h2 为止。折叠块（已结束那区）自己决定显隐，
         否则筛「已结束」时会把「长期有效」的 h2 一起点亮。 */
      while(n&&n.tagName!=="H2"){
        if(n.tagName==="TABLE"&&!n.hidden)
          vis+=n.querySelectorAll("tbody tr[data-t]:not([hidden])").length;
        n=n.nextElementSibling;
      }
      /* 分区标题旁的「6 条」是静态总数，筛选后只剩 3 行还写 6 就会自相矛盾：
         筛选态改写成「筛出 N 条」，回「全部」再还原原文（原文存在 data-orig）。 */
      var c=h.querySelector(".cnt");
      if(c){
        if(!c.getAttribute("data-orig")) c.setAttribute("data-orig",c.textContent);
        c.textContent=(filter==="all")?c.getAttribute("data-orig"):("筛出 "+vis+" 条");
      }
      h.hidden=(vis===0);
    });
    [].slice.call(document.querySelectorAll("details.fold")).forEach(function(d){
      d.hidden=![].slice.call(d.querySelectorAll("table.qt")).some(function(t){return !t.hidden;});
      /* 筛「已结束」时它成了唯一可见内容 —— 留在折叠态会像是筛空了，
         读者得再点一次才看得到那 23 行。只在这一档自动展开，其余情况尊重手动状态。 */
      if(!d.hidden&&filter==="over") d.open=true;
    });
    cnt.textContent="显示 "+shown+" / "+total+" 条";
    empty.classList.toggle("show", shown===0);
    if(q.value.trim()) paint(true);   /* 筛完重算命中，否则标记会留在看不见的行里 */
  }

  chips.forEach(function(c){
    c.addEventListener("click",function(){
      filter=c.getAttribute("data-f");
      chips.forEach(function(x){
        var on=(x===c);
        x.classList.toggle("on",on);
        x.setAttribute("aria-pressed",on?"true":"false");
      });
      apply();
    });
  });

  /* ---------- 检索 ---------- */
  function clearMarks(){
    marks.forEach(function(m){
      var p=m.parentNode; if(!p) return;
      p.replaceChild(document.createTextNode(m.textContent),m); p.normalize();
    });
    marks=[]; cur=-1;
  }
  function go(i){
    if(!marks.length) return;
    if(cur>=0&&marks[cur]) marks[cur].classList.remove("cur");
    cur=(i+marks.length)%marks.length;
    marks[cur].classList.add("cur");
    marks[cur].scrollIntoView({block:"center",behavior:"smooth"});
    qn.textContent=(cur+1)+" / "+marks.length;
  }
  function paint(silent){
    clearMarks();
    var v=q.value.trim();
    qn.textContent="0";
    if(!v) return;
    var root=document.querySelector(".wrap");
    var walk=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:function(n){
      if(!n.nodeValue||!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
      var p=n.parentNode; if(!p) return NodeFilter.FILTER_REJECT;
      if(/^(SCRIPT|STYLE|MARK|INPUT|BUTTON|TEXTAREA|SELECT)$$/.test(p.nodeName)) return NodeFilter.FILTER_REJECT;
      if(p.closest&&(p.closest(".tools")||p.closest(".qempty"))) return NodeFilter.FILTER_REJECT;
      if(p.closest&&p.closest("[hidden]")) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    }});
    var nodes=[],n;
    while((n=walk.nextNode())) nodes.push(n);
    var lv=v.toLowerCase();
    nodes.forEach(function(node){
      var val=node.nodeValue, low=val.toLowerCase(), i=low.indexOf(lv);
      if(i<0) return;
      var frag=document.createDocumentFragment(), last=0;
      while(i>=0){
        if(i>last) frag.appendChild(document.createTextNode(val.slice(last,i)));
        var m=document.createElement("mark");
        m.className="hl";
        m.textContent=val.slice(i,i+v.length);
        marks.push(m); frag.appendChild(m);
        last=i+v.length; i=low.indexOf(lv,last);
      }
      if(last<val.length) frag.appendChild(document.createTextNode(val.slice(last)));
      node.parentNode.replaceChild(frag,node);
    });
    if(!marks.length) return;
    if(silent) qn.textContent=marks.length; else go(0);
  }
  q.addEventListener("input",function(){ paint(false); });
  q.addEventListener("keydown",function(e){
    if(e.key==="Enter"){ e.preventDefault(); go(cur+1); }
    else if(e.key==="Escape"){ q.value=""; paint(false); }
  });
  document.getElementById("qnext").addEventListener("click",function(){ go(cur+1); });
  document.getElementById("qprev").addEventListener("click",function(){ go(cur-1); });

  /* ---------- 回到顶部 ---------- */
  var top=document.getElementById("qtop");
  function onScroll(){
    top.classList.toggle("show", window.scrollY>window.innerHeight*0.9);
  }
  window.addEventListener("scroll",onScroll,{passive:true});
  top.addEventListener("click",function(){
    window.scrollTo({top:0,behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});
  });

  apply();
  onScroll();
})();
</script>
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

    # 页头日期条必须在、且日期就是基准日（2026-11-23 用户反馈「找不到这是哪天的」）
    bad = datebadge.check(html, BASE.strftime("%Y-%m-%d"))
    if bad:
        raise SystemExit("页头日期条异常：%s" % "；".join(bad))

    # 皮肤切换按钮必须在（2026-11-23 用户问「极速视图为什么没有切换按钮」）
    bad = themeswitch.check(html)
    if bad:
        raise SystemExit("皮肤切换异常：%s" % bad)

    # 首页自指检测：index.html 与 quick.html 是同一份内容，页面里若还有
    # `href="index.html"`，读者点「历史各期索引」会原地打转（看起来像没反应）。
    if 'href="index.html"' in html:
        raise SystemExit("页面里出现自指链接 href=\"index.html\"（往期索引应为 archive.html）")

    io.open(OUT, "w", encoding="utf-8", newline="\n").write(html)
    io.open(OUT_HOME, "w", encoding="utf-8", newline="\n").write(html)
    print("quick.html 已生成：%d 条 / %d B / 基准日 %s"
          % (len(rows), len(html.encode("utf-8")), BASE))
    print("index.html 已生成（与 quick.html 同字节 = 站点首页就是极速视图）：%d B"
          % os.path.getsize(OUT_HOME))


if __name__ == "__main__":
    main()
