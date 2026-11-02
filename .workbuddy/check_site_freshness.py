# -*- coding: utf-8 -*-
"""站点新鲜度守卫：确认 archive.html / index.html / INDEX.md 都跟上了最新一期日报。

2026-11-02 起站点结构变了：**根路径 index.html 就是极速视图本体**（与 quick.html
同字节，由 build_quick.py 生成），往期总目录搬到 archive.html（build_index_web.py）。
所以「首页有没有跟上最新一期」现在要查三件事：
  · archive.html 的期号、最新卡片、是否链到最新一期网页版
  · index.html 与 quick.html 是否同字节（首页必须就是极速视图）
  · 极速视图的「本页基准日」是否等于最新一期日期

为什么需要它（2026-09-19 事故，第 008 期）
--------------------------------------------
008 期出刊时流水线跑了 build_index.py（→ `INDEX.md`），却漏跑
build_index_web.py（→ `index.html`）。后果：`INDEX.md` 里已是 008，
**站点首页还停在 007**，读者打开
https://lavie-purple.github.io/ai-free-content-digest/
看到的「最新一期」是昨天的（截图确认：更新至 第 007 期）。

根因不是脚本坏了，是**约定措辞有问题**：工具表里 build_index_web.py 的
触发条件写的是「改首页后」——可每新增一期都等于改了首页，这条措辞本身
就在鼓励漏跑。本脚本把「首页有没有跟上最新一期」从"记得跑"变成可计算判定。

用法：
    python .workbuddy/check_site_freshness.py
退出码：
    0 = 三个产物一致
    1 = 有产物落后于最新一期（**推送 GitHub Pages 前必须为 0**）
"""
import glob
import io
import os
import re
import sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ERR = []
WARN = []
OK = []


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def scan_issues():
    """扫目录里的日报 md，返回 {期号: (路径, 日期)}。只认带「第NNN期」的。"""
    out = {}
    pat = re.compile(r"^AI免费内容与权益速递-第(\d+)期-(\d{4}-\d{2}-\d{2})")
    for p in glob.glob(os.path.join(WS, "AI免费内容与权益速递-第*期-*.md")):
        m = pat.match(os.path.basename(p))
        if not m:
            continue
        no = int(m.group(1))
        # 同一期若有多份（如「复核版」），保留文件名更长的以外不关心，取路径排序最后一份
        if no not in out or p > out[no][0]:
            out[no] = (p, m.group(2))
    return out


def main():
    issues = scan_issues()
    if not issues:
        print("找不到任何「第NNN期」日报，检查是否在错误目录下运行")
        return 1
    latest = max(issues)
    latest_path, latest_date = issues[latest]
    print("=== 站点新鲜度守卫 ===")
    print("最新一期（按文件名）：第 %03d 期 · %s" % (latest, latest_date))
    print("  %s" % os.path.basename(latest_path))
    print("")

    # ---- INDEX.md ----
    idx = os.path.join(WS, "INDEX.md")
    if not os.path.exists(idx):
        ERR.append("INDEX.md 不存在 → 跑 build_index.py")
    else:
        nums = [int(x) for x in re.findall(r"(?m)^\|\s*\*\*(\d{3})\*\*\s*\|", read(idx))]
        top = max(nums) if nums else None
        if top == latest:
            OK.append("INDEX.md 最大期号 = %03d" % top)
        else:
            ERR.append("INDEX.md 最大期号 = %s，落后于最新一期 %03d → 跑 build_index.py"
                       % ("%03d" % top if top else "无", latest))

    # ---- archive.html（往期总目录，2026-11-02 起原 index.html 的位置）----
    web = os.path.join(WS, "archive.html")
    if not os.path.exists(web):
        ERR.append("archive.html 不存在 → 跑 build_index_web.py")
    else:
        h = read(web)
        m = re.search(r"更新至\s*<em>第\s*(\d+)\s*期</em>", h)
        if not m:
            ERR.append("archive.html 里找不到「更新至 第 N 期」锚点（页面结构可能变了）")
        elif int(m.group(1)) == latest:
            OK.append("archive.html 更新至 = %03d" % int(m.group(1)))
        else:
            ERR.append("archive.html 更新至 = %03d，落后于最新一期 %03d → 跑 build_index_web.py"
                       % (int(m.group(1)), latest))

        m2 = re.search(r'class="metaline"><b>第\s*(\d+)\s*期</b>.*?(\d{4}-\d{2}-\d{2})', h, re.S)
        if m2:
            if int(m2.group(1)) == latest and m2.group(2) == latest_date:
                OK.append("archive.html 最新卡片 = %03d · %s" % (int(m2.group(1)), m2.group(2)))
            else:
                ERR.append("archive.html 最新卡片 = %03d · %s，与最新一期不符（%03d · %s）"
                           % (int(m2.group(1)), m2.group(2), latest, latest_date))
        else:
            ERR.append("archive.html 里找不到最新一期卡片（metaline）")

        # 最新一期的网页版若已生成，目录页必须链到它
        fh = os.path.join(WS, "AI免费内容与权益速递-第%03d期-%s.html" % (latest, latest_date))
        if os.path.exists(fh):
            from urllib.parse import quote
            enc = quote(os.path.basename(fh))
            if enc in h or os.path.basename(fh) in h:
                OK.append("archive.html 已链到最新一期网页版")
            else:
                ERR.append("最新一期网页版已存在，但 archive.html 没有链到它 → 跑 build_index_web.py")
        else:
            WARN.append("最新一期没有网页版（%s 不存在），目录页只能给 Markdown"
                        % os.path.basename(fh))

        # mtime 提示（非致命）
        try:
            if os.path.getmtime(web) < os.path.getmtime(latest_path):
                WARN.append("archive.html 的修改时间早于最新一期 md，建议确认内容确实一致")
        except OSError:
            pass

    # ---- index.html（2026-11-02 起 = 极速视图本体，与 quick.html 同字节）----
    home = os.path.join(WS, "index.html")
    quick = os.path.join(WS, "quick.html")
    if not os.path.exists(home):
        ERR.append("index.html 不存在 → 跑 build_quick.py")
    elif not os.path.exists(quick):
        ERR.append("quick.html 不存在 → 跑 build_quick.py")
    else:
        a = io.open(home, "rb").read()
        b = io.open(quick, "rb").read()
        if a != b:
            ERR.append("index.html 与 quick.html 不同字节（%d B vs %d B）"
                       "—— 首页必须就是极速视图 → 跑 build_quick.py" % (len(a), len(b)))
        else:
            OK.append("index.html == quick.html（%d B，首页即极速视图）" % len(a))
        mq = re.search(r"本页基准日\s*<b>(\d{4}-\d{2}-\d{2})</b>", b.decode("utf-8", "replace"))
        if not mq:
            ERR.append("quick.html 里找不到「本页基准日」锚点（页面结构可能变了）")
        elif mq.group(1) == latest_date:
            OK.append("极速视图基准日 = %s" % mq.group(1))
        else:
            ERR.append("极速视图基准日 = %s，落后于最新一期 %s → 跑 build_quick.py"
                       % (mq.group(1), latest_date))

    # ---- 输出 ----
    for s in OK:
        print("  [OK]   %s" % s)
    for s in WARN:
        print("  [提示] %s" % s)
    for s in ERR:
        print("  [落后] %s" % s)
    print("")
    if ERR:
        print("VERDICT: 🔴 %d 项落后 —— 推送到 GitHub Pages 前必须重建" % len(ERR))
        return 1
    print("VERDICT: ALL GREEN%s" % ("（%d 项提示）" % len(WARN) if WARN else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
