# -*- coding: utf-8 -*-
"""生成根目录 INDEX.md 期号索引。

用法：
    python build_index.py

为什么做这个：
    日报是平铺在根目录的，到 20 期以后没法靠肉眼找。索引把「期号 / 日期 / 主题 /
    体量 / 网页版有无 / 避坑编号区间」拉成一张表，一眼能定位到要哪期。
    这里**不做物理归档**（不把旧期挪进子目录）——因为自动化需要跨期回读历史
    日报来避免重复，挪走会打断它。索引解决"找得到"，不牺牲"读得到"。
"""
import io, os, re

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(WS, "INDEX.md")
DEF = "AI免费内容与权益速递-"


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
    """取本期定位。

    优先取日期行后面的**副题**（如「刷新版」「分发入口专题版」），因为「主题」行
    各期几乎一样（都是"AI 免费内容发布 · 免费内容 · 免费额度"），没有区分度。
    001 期的日期行没有副题（格式是「第 001 期 · 日期」），回落到主题行。
    """
    m = re.search(r"(?m)^\*\*\d{4}-\d{2}-\d{2}（[^）]*）·\s*(.+?)\*\*\s*$", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"(?m)^\*\*主题[：:]\s*(.+?)\*\*\s*$", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"(?m)^\*\*(.+?)\*\*\s*$", text.lstrip("\n").split("\n", 1)[-1])
    return m.group(1).strip() if m else "—"


def main():
    files = sorted(fn for fn in os.listdir(WS)
                   if re.match(r"^" + re.escape(DEF) + r".*\.md$", fn))
    rows, tot = [], 0
    for idx, fn in enumerate(files, 1):
        p = os.path.join(WS, fn)
        txt = io.open(p, encoding="utf-8").read()
        m = re.search(r"第\s*(\d{3})\s*期", fn)
        no = m.group(1) if m else "%03d" % idx
        d = re.search(r"(\d{4}-\d{2}-\d{2})", fn)
        size = os.path.getsize(p)
        tot += size
        hp = os.path.splitext(p)[0] + ".html"
        html = "%d B" % os.path.getsize(hp) if os.path.exists(hp) else "—"
        rows.append((no, d.group(1) if d else "—", theme_of(txt), size, tables_in(txt), html, pit_range(txt), fn))

    led = os.path.join(WS, "AI信息源分级清单-T0-T4.md")
    ledstat = "—"
    if os.path.exists(led):
        lt = io.open(led, encoding="utf-8").read()
        tiers = [int(x) for x in re.findall(r"(?m)^## T\d[^\n]*?（(\d+)）", lt)]
        ledstat = "%d 条（%s）" % (sum(tiers), " / ".join("T%d %d" % (i, n) for i, n in enumerate(tiers)))

    dl = os.path.join(WS, ".workbuddy", "data", "deadlines.csv")
    dlstat = "—"
    if os.path.exists(dl):
        n = sum(1 for _ in io.open(dl, encoding="utf-8-sig")) - 1
        dlstat = "%d 条" % n

    L = []
    L.append("# AI 免费内容与权益速递 · 期号索引")
    L.append("")
    L.append("> 本文件由 `.workbuddy/build_index.py` **自动生成，请勿手工编辑**。")
    L.append("> 重建：`python .workbuddy/build_index.py`")
    L.append("")
    L.append("共 **%d 期**（%s ~ %s），Markdown 合计 **%d B ≈ %.0f KB**。"
             % (len(rows), rows[0][1] if rows else "—", rows[-1][1] if rows else "—", tot, tot / 1024.0))
    L.append("")
    L.append("| 期号 | 日期 | 本期定位 | md 体积 | 表格 | 网页版 | 避坑编号 |")
    L.append("| --- | --- | --- | --- | --- | --- | --- |")
    for no, d, th, size, tb, html, pit, fn in rows:
        L.append("| **%s** | %s | %s | %s B | %d | %s | %s |" % (no, d, th, format(size, ","), tb, html, pit))
    L.append("")
    L.append("## 台账与结构化数据（内部，不对外展示）")
    L.append("")
    L.append("- **信源分级台账** `AI信息源分级清单-T0-T4.md`：%s" % ledstat)
    L.append("- **截止时间表** `.workbuddy/data/deadlines.csv`：%s（由 `extract_deadlines.py` 从最新一期重建）" % dlstat)
    L.append("- **已固化条目库** `.workbuddy/data/frozen_items.md`（防重复往期）")
    L.append("- **待澄清口径** `.workbuddy/data/open_questions.md`")
    L.append("- **信源命中统计** `.workbuddy/data/source_hits.csv`（品牌提及口径，用于筛零命中源）")
    L.append("")
    L.append("## 工具链（`.workbuddy/`，均可**不传参自动取最新一期**）")
    L.append("")
    L.append("| 脚本 | 作用 |")
    L.append("| --- | --- |")
    for s, d in [("build_web.py", "日报 md → 单文件网页版（自包含，0 外部引用）"),
                 ("verify_web.py", "编译后必跑：表格列数/行数、保真度、标签闭合、状态格"),
                 ("probe_layout.py", "UI 量测：表格列宽满足度 / 搜索框可用宽 / 装饰元素压字（需 Edge）"),
                 ("probe_mobile.py", "手机端量测：320–414px 四档视口 / 触控目标 / 溢出 / 首列粘性（需 Edge）"),
                 ("snap_mobile.py", "手机端截图：iframe 造窄视口，11 个镜头，md5 判重（需 Edge）"),
                 ("audit_color.py", "配色审计：语义色色距 + WCAG 对比度 + opacity 叠加后实测值"),
                 ("extract_deadlines.py", "第四章截止表 → deadlines.csv"),
                 ("check_deadlines.py", "截止巡检：过期未更新 / N 天内到期（`--days` / `--today`）"),
                 ("check_frozen.py", "出刊前防重复：比对已固化条目库，有重复则 exit 1"),
                 ("check_tables.py", "出稿后核对：逐表列数一致性 + 避坑编号跨期连续性"),
                 ("build_source_hits.py", "信源命中统计 → 回写台账 + 导出 CSV"),
                 ("build_index.py", "重建本索引（INDEX.md）"),
                 ("build_index_web.py", "生成站点首页 index.html（GitHub Pages 根路径入口）"),
                 ("run_all.py", "工具链统一入口：一把跑完并保证日志是 UTF-8（PowerShell 捕获会乱码）")]:
        L.append("| `%s` | %s |" % (s, d))
    L.append("")
    L.append("## 版本控制与线上地址")
    L.append("")
    L.append("远端仓库：`Lavie-purple/ai-free-content-digest`（GitHub，**public**）")
    L.append("")
    L.append("站点首页（GitHub Pages）：https://lavie-purple.github.io/ai-free-content-digest/")
    L.append("")
    L.append("> 根路径由 `index.html` 提供入口（`build_index_web.py` 生成）。"
             "GitHub Pages 的根路径只认 `index.html` / `index.md`，"
             "而日报文件名带中文，故必须显式生成此文件，否则根路径会 404。")
    L.append("")

    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L))
    print("索引 -> %s" % os.path.relpath(OUT, WS))
    print("收录 %d 期，md 合计 %d B" % (len(rows), tot))
    for no, d, th, size, tb, html, pit, fn in rows:
        print("  第%s期 %s %-38s %7d B 表%-3d html:%-8s 避坑%s" % (no, d, th[:38], size, tb, html, pit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
