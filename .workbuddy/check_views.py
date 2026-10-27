# -*- coding: utf-8 -*-
"""三视图守卫：确认「极速 / 完整 / 总账」始终是同一份刊物的三个视图。

为什么需要它（2026-10-27，048 期）
----------------------------------
三页切换器是 048 期才收拢的。此前的形态是三个孤岛：日报页头有一条指向
quick 的横幅，quick 与 standing **没有任何回链**，进去就出不来；quick 里
「完整版日报」还错指到 index.html（首页）。那次的根因不是某个人忘了加链接，
而是**根本没有一个地方规定「三页必须同构」**。

只要这条约定只写在记忆里，它就会在某次赶时间的出刊里悄悄破掉：
重建 quick 时忘了跑 build_web、改了期号忘了重建 standing、
新一期日报生成后「完整日报」那一格还指着上一期……
这些都不会报错，页面照常打开，只是读者点进去看到的是过期的内容。

本脚本把「三页同构」变成可计算判定：
  · 文件与链接都到位（切换器里的每个 href 都真实存在）
  · 三格齐全、当前格唯一、aria-current 与实心块一一对应
  · 「完整日报」一律指向最新一期，不许指首页、不许指上期
  · 页面上显示的条数与源文件实算一致（手写的数字过一期就是错的）
  · 三页内嵌同一段 viewswitch CSS（否则同一个组件在三个页面长相不同）

用法：
    python .workbuddy/check_views.py
退出码：
    0 = 三页同构（**推送 GitHub Pages 前必须为 0**）
    1 = 有一页掉队
"""
import csv
import io
import os
import re
import sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.join(WS, ".workbuddy"))
import viewswitch  # noqa: E402

NAV_RE = re.compile(r'<nav class="vs".*?</nav>', re.S)
# 当前格：`<span class="vs-i vs-quick is-on" aria-current="page">`。
# 不限定 span/a、也不假定属性顺序 —— 报错时要能说清「高亮跑到哪一格去了」，
# 而不是只会说「is-on 数量不对」。
ON_RE = re.compile(r'<(?:span|a) class="vs-i vs-(\w+)[^"]*is-on"')
CUR_RE = re.compile(r'aria-current="page"')
# 一格 = 起始标签（可能带 href / aria-current）+ 标题行 + 副标题行。
# class 后面不能假定紧跟 `>`：普通格是 `<a class="vs-i vs-full" href="...">`，
# 当前格是 `<span class="vs-i vs-full is-on" aria-current="page">`，两种都要吃。
CELL_RE = re.compile(r'class="vs-i vs-(\w+)[^"]*"[^>]*>'
                     r'\s*<span class="vs-k">.*?<span class="vs-d">(.*?)</span>', re.S)
FULL_HREF_RE = re.compile(r'class="vs-i vs-full"\s+href="([^"]+)"')
FULL_ON_RE = re.compile(r'class="vs-i vs-full[^"]*is-on"[^>]*aria-current="page"')


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def code(s):
    m = re.match(r"(\d+)\s*条", (s or "").strip())
    return int(m.group(1)) if m else None


def count_quick():
    p = os.path.join(WS, ".workbuddy", "data", "quick_items.csv")
    if not os.path.exists(p):
        return None
    with io.open(p, encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.reader(f) if any(x.strip() for x in r)]
    return max(len(rows) - 1, 0)


def count_ledger():
    p = os.path.join(WS, "常驻权益总账.md")
    if not os.path.exists(p):
        return None
    t = read(p)
    return max(sum(1 for l in t.split("\n")
                   if l.strip().startswith("|")
                   and not re.match(r"^\|\s*-", l.strip())) - 1, 0)


def check_page(path, expect, n_quick, n_ledger, latest):
    """返回 (ok 列表, err 列表)。expect=None 表示首页（三格都不该高亮）。"""
    ok, err = [], []
    name = os.path.basename(path)
    if not path or not os.path.exists(path):
        return ok, ["%s：文件不存在" % (name or path)]

    s = read(path)
    m = NAV_RE.search(s)
    if not m:
        return ok, ["%s：找不到三视图切换器（<nav class=\"vs\">）" % name]
    nav = m.group(0)

    # 1. 三格齐全且顺序不变
    cells = CELL_RE.findall(nav)
    got = [k for k, _ in cells]
    if got != list(viewswitch.ORDER):
        err.append("%s：三格不齐或顺序变了 —— 实际 %s，应为 %s"
                   % (name, got, list(viewswitch.ORDER)))
    else:
        ok.append("三格齐全（极速 / 完整 / 总账）")

    # 2. 当前格唯一，且与页面身份一致
    ons = ON_RE.findall(nav)
    n_cur = len(CUR_RE.findall(nav))
    if expect is None:
        if ons or n_cur:
            err.append("%s：首页三格都不该高亮，实际高亮了 %s"
                       % (name, ons or "aria-current"))
        else:
            ok.append("三格均不高亮（首页正确）")
    elif len(ons) != 1 or n_cur != 1:
        err.append("%s：当前格必须唯一 —— is-on %d 个、aria-current %d 个"
                   % (name, len(ons), n_cur))
    elif ons[0] != expect:
        err.append("%s：高亮错格 —— 高亮的是 %s，应为 %s" % (name, ons[0], expect))
    else:
        ok.append("当前格 = %s（唯一高亮 + aria-current）" % expect)

    # 3. 「完整日报」必须指向最新一期
    #    —— 唯独「当前就在完整日报这一页」时它不该是链接（点了没反应会以为坏了），
    #    这是 viewswitch 的既有设计，不算掉队。
    fh = FULL_HREF_RE.search(nav)
    if not fh:
        if expect == "full" and FULL_ON_RE.search(nav):
            ok.append("「完整日报」为当前页（不加自链接）")
        else:
            err.append("%s：「完整日报」那一格不是链接（读者点不动）" % name)
    else:
        href = fh.group(1)
        if href == "index.html":
            err.append("%s：「完整日报」错指首页 index.html" % name)
        elif latest and href != latest:
            err.append("%s：「完整日报」指向 %s，最新一期是 %s" % (name, href, latest))
        elif not os.path.exists(os.path.join(WS, href)):
            err.append("%s：「完整日报」链接目标不存在 —— %s" % (name, href))
        else:
            ok.append("「完整日报」→ %s" % href)

    # 4. 切换器里其余本地链接都要存在
    for h in re.findall(r'href="([^"#?]+\.html)"', nav):
        if h != latest and not os.path.exists(os.path.join(WS, h)):
            err.append("%s：切换器链接目标不存在 —— %s" % (name, h))

    # 5. 页面显示的条数 == 源文件实算
    #    规则是「**写出来的数字必须对**」，不是「必须写数字」：
    #    首页三格是纯入口，本来就不带条数（「只答四个问题」），那是设计不是错。
    shown = dict(cells)
    q, lg = code(shown.get("quick")), code(shown.get("standing"))
    if q is not None and n_quick is not None and q != n_quick:
        err.append("%s：极速格写「%s 条」，quick_items.csv 实算 %d 条"
                   % (name, q, n_quick))
    if lg is not None and n_ledger is not None and lg != n_ledger:
        err.append("%s：总账格写「%s 条」，常驻权益总账.md 实算 %d 条"
                   % (name, lg, n_ledger))
    if q is not None and lg is not None:
        ok.append("条数实算一致（极速 %d / 总账 %d）" % (q, lg))

    # 6. 内嵌同一段 CSS
    if ".vs-i.is-on{background" not in s:
        err.append("%s：缺 viewswitch 的样式（切换器会裸奔成三行纯文字）" % name)
    else:
        ok.append("内嵌 viewswitch 样式")

    return ok, err


def main():
    global WS
    argv = sys.argv[1:]
    if "--ws" in argv:
        WS = os.path.abspath(argv[argv.index("--ws") + 1])

    latest = viewswitch.latest_issue_html(WS)
    n_quick, n_ledger = count_quick(), count_ledger()

    print("=" * 64)
    print("三视图守卫 · 最新一期 = %s" % (latest or "（没找到）"))
    print("源文件实算：极速 %s 条 / 总账 %s 条" % (n_quick, n_ledger))
    print("=" * 64)

    pages = [
        ("index.html", None, "首页"),
        ("quick.html", "quick", "极速视图"),
        (latest, "full", "完整日报"),
        ("standing.html", "standing", "常驻总账"),
    ]

    errs = []
    if not latest:
        errs.append("找不到任何一期日报 html（`AI免费内容与权益速递-第NNN期-*.html`）")

    for fn, expect, label in pages:
        if not fn:
            continue
        ok, err = check_page(os.path.join(WS, fn), expect,
                             n_quick, n_ledger, latest)
        print("\n[%s] %s" % (label, fn))
        for x in ok:
            print("  OK   " + x)
        for x in err:
            print("  FAIL " + x)
        errs.extend(err)

    print("\n" + "=" * 64)
    if errs:
        print("VERDICT: %d 处不一致 —— 推送前必须修" % len(errs))
        for x in errs:
            print("  · " + x)
        return 1
    print("VERDICT: ALL GREEN（四页同构，条数与源文件一致）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
