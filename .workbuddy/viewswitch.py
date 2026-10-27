# -*- coding: utf-8 -*-
"""三档视图切换器：极速视图 / 完整日报 / 常驻总账。

为什么要有这个东西（048 期前用户反馈）：
三个页面（quick.html / 日报 html / standing.html）此前是三个孤岛 ——
日报页头有一条指向 quick 的横幅，但 quick 与 standing 里**没有任何一条回链**，
进去就出不来；而且 quick 页里「完整版日报」的链接错指到 index.html（首页）。

改法不是「再各加一条链接」，而是把三页收成「一份刊物的三个视图」：
同一位置、同一外观、同一套语义（当前页高亮 + aria-current），
任何一页都能一步跳到另外两页。读者不需要记哪个文件对应哪件事。
"""

import io
import os
import re
import urllib.parse

# 三档顺序固定：由「最轻」到「最全」。
# 顺序不能按字母或文件大小排 —— 它本身就是一条阅读动线：
# 先想知道现在能白拿什么（极速）→ 再看本期变了什么（完整）→ 最后查长期存量（总账）。
ORDER = ("quick", "full", "standing")

LABEL = {
    "quick": "极速视图",
    "full": "完整日报",
    "standing": "常驻总账",
}

ARROW = {
    "quick": "&#9889;",       # ⚡
    "full": "&#9678;",        # ◎
    "standing": "&#9776;",    # ☰
}

HREF = {
    "quick": "quick.html",
    "full": None,             # 运行时按最新一期填
    "standing": "standing.html",
}


def latest_issue_html(ws):
    """找最新一期的日报 html。

    按**文件名里的期号**排序，不按 mtime —— 重建往期（补样式、改错字）会把 mtime 刷新，
    用 mtime 会把旧期顶到最前，读者点「完整日报」就跳回两个月前。
    """
    best, best_no = None, -1
    try:
        names = os.listdir(ws)
    except OSError:
        return None
    for fn in names:
        m = re.match(r"^AI免费内容与权益速递-第\s*(\d{3})\s*期-.*\.html$", fn)
        if not m:
            continue
        if int(m.group(1)) > best_no:
            best, best_no = fn, int(m.group(1))
    return best


def latest_issue_no(ws):
    fn = latest_issue_html(ws)
    m = re.search(r"第\s*(\d{3})\s*期", fn or "")
    return m.group(1) if m else None


def render(current, issue_no=None, n_quick=None, n_ledger=None,
           full_href=None, ws=None):
    """渲染切换器。

    current   : "quick" | "full" | "standing"，当前页
    issue_no  : 三位期号字符串，用于「完整日报」的副标题
    n_quick   : 速查条数（数字或 None）
    n_ledger  : 总账条数（数字或 None）
    full_href : 覆盖「完整日报」的链接目标（默认自动找最新一期）
    ws        : 工作区绝对路径，用于自动找最新一期
    """
    if full_href is None:
        base = ws or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_href = latest_issue_html(base) or "index.html"

    # 期号可以从目标文件名里读出来，调用方就不用各自再算一遍 ——
    # 少一处手写，就少一处「过一期就写错」。
    if issue_no is None and full_href:
        _m = re.search(r"第\s*(\d{3})\s*期", urllib.parse.unquote(full_href))
        if _m:
            issue_no = _m.group(1)

    desc = {
        "quick": "%s 条 · 一条一行" % n_quick if n_quick else "只答四个问题",
        "full": ("第 %s 期 · 十节" % issue_no) if issue_no else "本期全文",
        "standing": "%s 条 · 无截止日" % n_ledger if n_ledger else "长期权益全量",
    }

    out = ['<nav class="vs" aria-label="视图切换">']
    for k in ORDER:
        href = full_href if k == "full" else HREF[k]
        cls = "vs-i vs-" + k + (" is-on" if k == current else "")
        inner = ('<span class="vs-k"><i aria-hidden="true">%s</i>%s</span>'
                 '<span class="vs-d">%s</span>'
                 % (ARROW[k], LABEL[k], desc[k]))
        if k == current:
            # 当前页不用 <a>：点了没反应会让人以为坏了；aria-current 让读屏软件也知道位置
            out.append('<span class="%s" aria-current="page">%s</span>' % (cls, inner))
        else:
            out.append('<a class="%s" href="%s">%s</a>' % (cls, href, inner))
    out.append("</nav>")
    return "".join(out)


# 三页共用同一段样式，避免「同一个组件在三个页面长相不同」。
# 只用三页都定义了的变量（--rule / --surface / --ink / --bg / --faint / --accent-ink），
# 不用 --s4 / --fast 这类只有日报模板才有的间距与缓动变量。
CSS = """
.vs{
  display:grid; grid-template-columns:repeat(3,1fr);
  margin:18px 0 20px; border:1px solid var(--rule); background:var(--surface);
  box-shadow:var(--shadow);
}
.vs-i{
  display:block; padding:10px 14px; text-decoration:none; color:var(--ink-2);
  border-right:1px solid var(--rule); transition:background 120ms ease;
}
.vs-i:last-child{border-right:0}
.vs-i:hover{background:var(--surface-2)}
.vs-k{display:block; font-size:13.5px; font-weight:600; line-height:1.45}
.vs-k i{font-style:normal; margin-right:5px; opacity:.75}
.vs-d{display:block; font-size:11.5px; color:var(--faint); line-height:1.5; margin-top:1px}
.vs-i.is-on{background:var(--ink); color:var(--bg); cursor:default}
.vs-i.is-on .vs-d{color:var(--bg); opacity:.6}
.vs-i.is-on .vs-k i{opacity:.85}
/* 只给「极速」的图标上强调色：整行标红会盖过当前页的实心块，反而让人以为它才是当前页 */
.vs-quick .vs-k i{color:var(--accent-ink); opacity:1}
.vs-quick.is-on .vs-k i{color:var(--bg)}
@media (max-width:640px){
  /* 窄屏不要三行堆叠：日报页顶已有固定导航条 + 刊头 + 说明框，
     再来三行切换器会把首屏全占掉。压成单行三格，副标题不出。 */
  .vs{grid-template-columns:repeat(3,1fr); margin-top:14px}
  .vs-i{
    padding:9px 6px; text-align:center;
    border-right:1px solid var(--rule); border-bottom:0;
  }
  .vs-i:last-child{border-right:0}
  .vs-k{font-size:12px; line-height:1.3}
  .vs-k i{margin-right:3px}
  .vs-d{display:none}
}
@media print{.vs{display:none !important}}
"""
