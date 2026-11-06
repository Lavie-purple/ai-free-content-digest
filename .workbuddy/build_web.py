# -*- coding: utf-8 -*-
"""
把 AI 免费内容与权益速递（Markdown）编译成单文件网页版简报。
- 保真：md 里的每个字、每张表都原样落进 HTML，只做结构化增强
- 增强：刊头、章节编号、可筛选的截止时间表、搜索高亮、明暗主题、打印样式
产物：与 md 同名的 .html（自包含，零外部资源）

用法：
    python build_web.py                     # 自动取工作区日期最新的一期
    python build_web.py <source.md>         # 指定期
    python build_web.py <source.md> <out.html>
"""
import io, os, re, sys, html

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import viewswitch
import json

# ---------------------------------------------------------------- 30 秒速览 / 审计层折叠
# 060 期 A 方案（用户 2026-11-06 选定）：完整日报首屏只留「新闻 + 一张速览卡」，
# 权益台账与审计层默认折叠。**信息一条不删** —— 只是换落点，展开后与原文逐字一致。
# 仅对「第 NNN 期」日报生效；《常驻权益总账》与《第四章表体明细附录》同样用本
# 编译器生成，保持原样（它们本来就是「专门来查」的页面，不需要再折一层）。
FOLD_SECTIONS = {
    "s04": "第四章 · 权益台账与脚注",
    "s05": "第五章 · 本期纠错清单",
    "s06": "第六章 · 避坑提示",
    "s08": "第八章 · 信源体系更新",
    "s09": "第九章 · 来源与核查说明",
}


def _headline(issue, src_text):
    """目录头条的唯一真源是 data/headlines.json（check_headlines 保证每期登记）。"""
    p = os.path.join(WS, ".workbuddy", "data", "headlines.json")
    key = str(int(issue)).zfill(3)
    try:
        d = json.load(io.open(p, encoding="utf-8-sig"))
        v = (d.get(key) or "").strip()
        if v:
            return v
    except Exception as e:
        print("[brief] 台账读取失败：%s" % e)
    # 兜底：摘要章首段，剥掉行内 Markdown 后截 80 字
    m = re.search(r"(?ms)^## 摘要[^\n]*\n(.*?)(?=^## )", src_text)
    fb = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", m.group(1) if m else "")
    fb = re.sub(r"\*\*|`|\s+", " ", fb).strip()[:80]
    assert fb, "头条兜底也为空（避坑 058：零命中不是通过，是没找到对象）"
    print("[brief] 台账缺 %s 期，已用摘要兜底" % key)
    return fb


def _fold(html_body):
    """把 FOLD_SECTIONS 里的章节正文（h2 之后）包进 <details>。

    ① section / h2 的数量与结构不变 —— verify_web 的计数判据照旧通过；
    ② 正文一字不删，只移进 details —— 保真检查照旧通过；
    ③ 命中数必须等于预期，少一个就报错，不允许「零命中也算通过」。
    """
    hit = []

    def one(m):
        sid, extra, h2, inner = m.group(1), m.group(2), m.group(3), m.group(4)
        if sid not in FOLD_SECTIONS:
            return m.group(0)
        hit.append(sid)
        return ('<section id="%s" class="sec%s folded">\n%s\n'
                '<details class="audit-fold" id="fold-%s">\n'
                '<summary><span class="fold-t">展开：%s</span>'
                '<span class="fold-hint">默认收起 · 点此展开</span></summary>\n'
                '%s\n</details>\n</section>'
                % (sid, extra, h2, sid, FOLD_SECTIONS[sid], inner))

    pat = re.compile(
        r'<section id="(s\d{2}|s-abs)" class="sec([^"]*)">\n'
        r'(<h2[\s\S]*?</h2>)\n([\s\S]*?)\n</section>')
    out = pat.sub(one, html_body)
    missing = [k for k in FOLD_SECTIONS if k not in hit]
    assert not missing, ("折叠章节缺命中（零命中不是通过）", missing, hit)
    return out


def _brief(issue, date_line, headline, html_body):
    """30 秒速览卡：三个数字全部从已渲染表体实算，与正文同源。"""
    n_crit = html_body.count('data-st="crit"')
    n_soon = html_body.count('data-st="soon"')
    n_rows = len(re.findall(r'<tr data-st="', html_body))
    m = re.search(r"\d{4}-\d{2}-\d{2}", date_line or "")
    day = m.group(0) if m else ""
    return ('<div class="brief" data-no-print>\n'
            '<p class="brief-k">30 秒速览 · 第 %s 期%s</p>\n'
            '<p class="brief-h">%s</p>\n'
            '<div class="brief-m"><span>本期表体 <b>%d</b> 行</span>'
            '<span>其中必办 <b>%d</b> 条</span>'
            '<span>今明换挡 <b>%d</b> 条</span></div>\n'
            '<div class="brief-a"><a href="#s04" data-open="s04">看必办清单</a>'
            '<a href="quick.html">只看极速版</a>'
            '<button type="button" id="foldAll" aria-expanded="false">展开全部章节</button></div>\n'
            '<p class="brief-n">下方是本期新闻正文（未折叠）；第四章权益台账与纠错、避坑、'
            '信源、核查等审计层默认收起，点标题展开。目录跳转、全文检索命中与打印时会自动展开。'
            '卡片数字是本期表体口径，全量三态分布以第四章脚注为准。原文一字未删。</p>\n'
            '</div>\n'
            % (esc(issue), (" · " + day) if day else "", esc(headline),
               n_rows, n_crit, n_soon))


def pick_default():
    """取工作区里日期最新的一期日报（按文件名里的 YYYY-MM-DD 排序）。"""
    cands = []
    for fn in os.listdir(WS):
        m = re.match(r"^(AI免费内容与权益速递.*?(\d{4}-\d{2}-\d{2}))\.md$", fn)
        if m:
            cands.append((m.group(2), fn))
    if not cands:
        raise SystemExit("工作区里没找到日报 md")
    cands.sort()
    return os.path.join(WS, cands[-1][1])


# 命令行优先： python build_web.py [source.md [out.html]]
# 不传参时自动取日期最新的一期——不再需要每期手改路径
if len(sys.argv) > 1:
    SRC = sys.argv[1]
    OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(SRC)[0] + ".html"
else:
    SRC = pick_default()
    OUT = os.path.splitext(SRC)[0] + ".html"

CN_NUM = {"一": "01", "二": "02", "三": "03", "四": "04", "五": "05",
          "六": "06", "七": "07", "八": "08", "九": "09", "十": "10"}
ST_MAP = {"\U0001F534": "crit", "\U0001F7E0": "soon", "\U0001F7E2": "live"}
# 状态色标（含变体选择符 VS16 U+FE0F）——用于从正文里摘除色标，避免与徽章重复
ST_ANY_RE = re.compile("[\U0001F534\U0001F7E0\U0001F7E2\u26AA\u26A0]\uFE0F?")


def st_of(cell):
    """按日报自己的色标体系判定状态。

    规则（006 期修订）：**以状态格里最先出现的色标为准**，因为编辑写这一格时
    总是把主状态放在最前面，⚠️ 只是跟在后面的注解（例：'🟢 生效中……⚠️ 另有口径'）。
    旧实现是 ⚠️ 无条件优先，会把这类行错判成"口径存疑"、并从"生效中"筛选里漏掉。
    仅当 ⚠️ 出现在任何颜色标之前时，才判为 warn。
    """
    if "已结束" in cell:
        return "over", "\u25CB"
    hit = None
    for m in ST_ANY_RE.finditer(cell):
        hit = m
        break
    if hit is None:
        return "live", "\U0001F7E2"
    ch = hit.group(0)
    for k, key in ST_MAP.items():
        if ch.startswith(k):
            return key, k
    if ch.startswith("\u26AA"):
        return "over", "\u25CB"
    return "warn", "\u26A0"


def st_strip(cell):
    """摘掉状态格里的所有色标（保留文字），供徽章外侧的正文使用。"""
    return ST_ANY_RE.sub("", cell).strip()


def esc(t):
    return html.escape(t, quote=False)


def inline(t):
    """行内 Markdown -> HTML（先转义，再处理 code / bold / link）

    链接放最后：047 期起正文要指到《常驻权益总账》与 standing.html，
    不转的话读者会看到一堆 `[常驻权益总账](常驻权益总账.md)` 原文。
    只认相对路径与非空白字符，不引入外链。
    """
    t = esc(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return t


def cells(line):
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    return [c.strip() for c in raw.split("|")]


def is_sep(line):
    return bool(re.match(r"^\|[\s:\-\|]+\|$", line.strip()))


def disp_w(s):
    """估算一段文字在 14px 正文字号下的显示宽度（px），供首列下限使用。"""
    t = re.sub(r"\*\*|`", "", s or "")
    # 去掉 emoji / 变体选择符 / 零宽连接符：它们不占正文字宽
    t = re.sub(r"[\U0001F000-\U0001FAFF\U0001F1E6-\U0001F1FF"
               r"\u2190-\u21FF\u2300-\u27BF\u2B00-\u2BFF\uFE0F\u200D]", "", t)
    w = 0.0
    for ch in t:
        w += 14.0 if ord(ch) > 0x2E80 else 7.4
    return w


def render_table(rows, section_no, chips=True):
    head = cells(rows[0])
    body = [cells(r) for r in rows[2:]]
    ncol = len(head)
    # 截止表判据：**按表头认，不按章节号认**。
    # 047 期修订后第四章移到文末（仍是「四」），且新增《常驻权益总账》里同样一张表，
    # 写死 section_no=="04" 会让两张表都失去筛选条。
    ledger = (ncol == 3 and head[0].strip() == "活动"
              and "截止" in head[1] and "状态" in head[2])
    cls = "tbl" + (" ledger" if ledger else "") + (" c%d" % ncol)
    # 《常驻权益总账》的「全量表」三列都是长文本（活动名 / 未公布+长说明 / 状态小作文），
    # 日报 4.1 的 date=76px 定宽是从「2026-11-08」这种短日历日来的，套到总账会把
    # 中文压成一字一行。给这张表单独一个类名，CSS 里按内容配比分三列宽。
    # 判源文件名而不是表头：日报 4.1 / 4.2 / 附录同样是「活动|截止|状态」，不能一起改。
    if ledger and os.path.basename(SRC).startswith("常驻权益总账"):
        cls += " ledger-full"
    out = ['<div class="tblwrap%s">' % (" scrolly" if ledger else "")]
    # chips 只给本章的**第一张**截止表：同一节里第二张（4.2 本期变更）只有十几行、
    # 状态又单一，再挂一条筛选条是纯噪音，而且 id="ledgerCount" 会重复。
    if ledger and chips:
        out.append(
            '<div class="chips" role="group" aria-label="按状态筛选">'
            '<span class="chips-label">按状态筛</span>'
            '<button class="chip on" data-f="all" aria-pressed="true">全部<b data-c="all">0</b></button>'
            '<button class="chip" data-f="crit" aria-pressed="false">\U0001F534 必办<b data-c="crit">0</b></button>'
            '<button class="chip" data-f="soon" aria-pressed="false">\U0001F7E0 今明换挡<b data-c="soon">0</b></button>'
            '<button class="chip" data-f="live" aria-pressed="false">\U0001F7E2 生效中<b data-c="live">0</b></button>'
            '<button class="chip" data-f="warn" aria-pressed="false">\u26A0 口径存疑<b data-c="warn">0</b></button>'
            '<button class="chip" data-f="over" aria-pressed="false">\u25CB 已结束<b data-c="over">0</b></button>'
            '<span class="chips-count" id="ledgerCount" aria-live="polite"></span>'
            "</div>"
        )
    # 列语义分类：截止表靠表头文字认日期列/状态列，用于固定列宽
    if ledger:
        kinds = []
        for h in head:
            if any(k in h for k in ("截止", "日期", "时间")):
                kinds.append("date")
            elif "状态" in h:
                kinds.append("st")
            else:
                kinds.append("body")
    else:
        kinds = [""] * ncol

    # 首列条目名若属于「中短专名」区间，给一个按内容估出的最小宽度，
    # 避免被其它长列挤到中文逐字换行。序号列（#）与超长说明列不处理。
    #
    # 上限 210 是**桌面端**的约束：正文栏就 900 来 px，首列再宽会把整表撑出容器
    # （没有横滑兜底）。手机端则相反——表格本来就待在横滑容器里，横滑 200px 和
    # 340px 都是横滑，但把「ZDTaichu5.0」这种无空格专名压成逐字竖排是没法读的。
    # 所以 210 < need <= 320 这段只输出手机端下限 --w1m，不动桌面版。
    w1 = 0
    w1m = 0
    first_head = head[0].strip() if head else ""
    if first_head not in ("#", "序号", "") and body:
        need = max(disp_w(r[0]) for r in body)
        if 92 <= need <= 210:
            w1 = int(need + 33)
        # 手机端下限门槛压到 40px（约 3 个中文字）：手机屏只有 375px，
        # 「小红书」这种 3 字列会被压到 58px、只能放 2 个字而折成两行。
        # 上限仍是 320px —— 更长的说明性首列折行是正常排版，不该为它把表撑到离谱。
        # 序号列（#）已在上面按表头名排除，不受影响。
        if 40 <= need <= 320:
            w1m = int(need + 33)

    tcls = cls + (" w1" if w1 else "") + (" w1m" if w1m else "")
    vars_ = []
    if w1:
        vars_.append("--w1:%dpx" % w1)
    if w1m:
        vars_.append("--w1m:%dpx" % w1m)
    style = (' style="%s"' % ";".join(vars_)) if vars_ else ""
    out.append('<table class="%s"%s>' % (tcls, style))
    out.append("<thead><tr>" + "".join(
        "<th%s>%s</th>" % (' data-col="%s"' % kinds[i] if kinds[i] else "", inline(h))
        for i, h in enumerate(head)) + "</tr></thead><tbody>")
    if ledger:
        for r in body:
            r = (r + [""] * ncol)[:ncol]
            last = r[ncol - 1]
            st, badge = st_of(last)
            rest = st_strip(last) if badge else last
            tds = []
            for i, c in enumerate(r):
                if i == ncol - 1:
                    # 长状态格默认收成 4 行：040 期起表体里出现 2,000+ 字的小作文
                    # （发布类条目被塞进「截止表」），一行顶一篇文章。
                    # 全量文字仍在 HTML 里 —— verify_web 的保真检查照常能查到，
                    # 只是默认折叠，点一下展开，不删任何字。
                    if len(rest) > 260:
                        body_html = ('<span class="st-txt cbody clamp" '
                                     'title="点击展开全文">%s</span>' % inline(rest))
                    else:
                        body_html = '<span class="st-txt">%s</span>' % inline(rest)
                    tds.append(
                        '<td data-col="st"><span class="st st-%s">%s</span>%s</td>'
                        % (st, badge or "\u25CB", body_html)
                    )
                else:
                    # 手机端会把截止表拆成一张张卡片，靠 data-col 认列——比 nth-child 稳，
                    # 换一期表头顺序变了也不会错位
                    tds.append('<td data-col="%s">%s</td>' % (kinds[i], inline(c)))
            out.append('<tr data-st="%s">%s</tr>' % (st, "".join(tds)))
    else:
        for r in body:
            r = (r + [""] * ncol)[:ncol]
            out.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
    out.append("</tbody></table>")
    # 手机端 2 列表会被改成纵向堆叠、不再横滑，所以只给 >=3 列的表输出滑动手势提示
    if ncol > 2:
        out.append('<p class="scrollhint" aria-hidden="true">\u2194 表格可左右滑动</p>')
    out.append("</div>")
    return "\n".join(out)


def h2_title(raw):
    """拆出章节号与标题：'一、AI 免费内容发布（本期扩版 · 重点）'"""
    m = re.match(r"^([一二三四五六七八九十])、\s*(.+)$", raw)
    if m:
        no = CN_NUM.get(m.group(1), "00")
        rest = m.group(2)
    else:
        no, rest = "00", raw
    sub = ""
    mm = re.match(r"^(.*?)（(.+)）$", rest)
    if mm and len(mm.group(2)) <= 30:
        rest, sub = mm.group(1), mm.group(2)
    return no, rest, sub


def build():
    src = io.open(SRC, encoding="utf-8").read().replace("\r\n", "\n")
    lines = src.split("\n")

    title = ""
    metas = []
    note = []
    toc = []          # (id, no, title, is_h3, anchor)
    body = []
    cur_no = "00"
    started = False
    sec_open = False
    ledger_used = False   # 本节是否已经输出过一张带 chips 的截止表
    i = 0
    n = len(lines)

    while i < n:
        ln = lines[i]
        s = ln.strip()

        if s.startswith("# ") and not title:
            title = s[2:].strip()
            i += 1
            continue
        if s.startswith("### "):
            t = s[4:].strip()
            aid = "h3-%d" % len(toc)
            m = re.match(r"^(\d+)\.\s*(.*)$", t)
            if m:
                head_html = '<span class="h3n">%s</span>%s' % (m.group(1), inline(m.group(2)))
            else:
                head_html = inline(t)
            toc.append((aid, "", t, True, None))
            body.append('<h3 id="%s">%s</h3>' % (aid, head_html))
            i += 1
            continue
        if s.startswith("## "):
            started = True
            no, t, sub = h2_title(s[3:].strip())
            cur_no = no
            ledger_used = False
            aid = "s%s" % no if no != "00" else "s-abs"
            toc.append((aid, no, t, False, sub))
            if sec_open:
                body.append("</section>")
            sec_open = True
            body.append('<section id="%s" class="sec">' % aid)
            body.append(
                '<h2><span class="sn">%s</span><span class="h2t">%s</span>%s</h2>'
                % (no if no != "00" else "\u00b7\u00b7", esc(t),
                   '<span class="h2sub">（%s）</span>' % inline(sub) if sub else "")
            )
            i += 1
            continue
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            if started:
                body.append('<blockquote class="bq">' + "".join(
                    "<p>%s</p>" % inline(x) for x in buf) + "</blockquote>")
            else:
                note.extend(buf)      # 刊头之前的引用 = 刊例说明
            continue
        if s == "---":
            i += 1
            continue
        if (not started) and s.startswith("**") and s.endswith("**") and s.count("**") == 2:
            metas.append(s)
            i += 1
            continue
        if s.startswith("|") and i + 1 < n and is_sep(lines[i + 1]):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            body.append(render_table(rows, cur_no, chips=not ledger_used))
            if len(cells(rows[0])) == 3 and cells(rows[0])[0].strip() == "活动":
                ledger_used = True
            continue
        if re.match(r"^[-*]\s+", s):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip()))
                i += 1
            body.append('<ul class="ul">' + "".join("<li>%s</li>" % inline(x) for x in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", s):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                m = re.match(r"^(\d+)\.\s+(.*)$", lines[i].strip())
                items.append((m.group(1), m.group(2)))
                i += 1
            big = cur_no == "06"
            cls = "ol big" if big else "ol"
            body.append('<ol class="%s">' % cls + "".join(
                '<li><span class="lin">%s</span><span class="lit">%s</span></li>' % (a, inline(b))
                for a, b in items) + "</ol>")
            continue
        if not s:
            i += 1
            continue
        # 普通段落（连续非空行合并为一段）
        buf = []
        while i < n:
            t = lines[i].strip()
            if not t or t.startswith(("#", "|", ">", "---")) or re.match(r"^[-*]\s+", t) or re.match(r"^\d+\.\s+", t):
                break
            buf.append(t)
            i += 1
        if not buf:
            # 防御：走到这里说明本行既没被上面的分支认领、又会被本分支的跳出条件
            # 拦住（历史踩坑：`#### ` 四级标题——`# `/`## `/`### ` 三个分支都不匹配，
            # 段落分支又因 `startswith("#")` 立刻 break，`i` 不前进 → 外层 while 死循环，
            # 025 期实测挂死 8 分钟无产出）。宁可渲染成一段朴素文本，也不要静默挂死。
            buf.append(s)
            i += 1
        body.append("<p>%s</p>" % inline(" ".join(buf)))

    # 收尾：闭合最后一个 section
    if sec_open:
        body.append("</section>")
    html_body = "\n".join(body)

    # 摘要区（第一段无 section 的 ul）加封面卡片样式
    html_body = html_body.replace('<section id="s-abs" class="sec">', '<section id="s-abs" class="sec summary">', 1)

    # 060 期 A 方案：权益台账与审计层默认折叠（仅完整日报；总账 / 附录不走这一步）
    is_digest = bool(re.search(r"第\d{3}期", os.path.basename(SRC)))
    if is_digest:
        html_body = _fold(html_body)

    # 刊头解析
    m = re.search(r"第\s*(\d+)\s*期", title)
    issue = m.group(1) if m else "001"
    # 总账不是「一期」，它没有期号。此前 fallback 成 001，页头就写出了
    # 「AI 免费内容与权益速递 · 第 001 期」和「#001」—— 读者会以为这是创刊号。
    is_ledger = os.path.basename(SRC).startswith("常驻权益总账")
    if is_ledger:
        issue_line, issue_badge, mh_num = "常驻权益总账", "总账", ""
    elif os.path.basename(SRC).startswith("第四章表体明细附录"):
        # 附录逐期累积，不属于任何一期；写「第 001 期」会让读者以为翻到了创刊号
        issue_line, issue_badge, mh_num = "第四章表体明细附录", "附录", ""
    else:
        issue_line, issue_badge, mh_num = "第 %s 期" % issue, issue, issue
    mast = title.split("·")[0].strip() if "·" in title else title
    date_line = re.sub(r"\*\*", "", metas[0]) if metas else ""
    # 分隔符跟着内容走：总账没有日期行，若还照打一个「·」，
    # 右上角就会孤零零挂一个点（实测就是这么挂上去的）。
    if is_ledger:
        date_block = "<em>逐期复核 · 原文照搬</em>"
    elif date_line:
        date_block = esc(date_line) + " \u00b7 <em>增量与纠错口径</em>"
    else:
        date_block = "<em>增量与纠错口径</em>"
    theme_line = re.sub(r"\*\*", "", metas[1]) if len(metas) > 1 else ""

    # 页脚右上的日期戳：模板里的 __DATELINE__ 一直没有被替换，读者看到的是字面量
    # （用户 2026-11-07 截图里它就挂在页脚右下）。取值只从源 md 抄已核实的时点，
    # 不在构建时打「当前时间」—— 那样每重建一次字节都会变，破坏幂等。
    m_dl = re.search(r"扫描截止\s*\**\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})", src)
    if m_dl:
        dateline = "扫描截止 %s %s（GMT+8）" % (m_dl.group(1), m_dl.group(2))
    else:
        m_dl = re.search(r"最后全量复核\**：\s*(\d{4}-\d{2}-\d{2})", src)
        dateline = ("最后全量复核 " + m_dl.group(1)) if m_dl else ""

    # 目录显示顺序（2026-11-07 用户选定方案 A）：
    # 正文物理顺序、章节编号、折叠分组一律不动，只重排「目录 / 顶栏」的呈现次序 ——
    # 04 是读者最该先看的行动清单，从文末提到第四位；07「按任务选型速查」是给读者
    # 做决策用的，从审计层里提出来；05/06/08/09 归到最后。代价是点 04 会跳到文末
    # （A 方案已接受，跳转时由 openFold 自动展开该章）。
    TOC_ORDER = ["s-abs", "s01", "s02", "s03", "s04", "s07",
                 "s05", "s06", "s08", "s09"]
    TOC_GROUPS = {"s-abs": "本期内容", "s04": "马上要办",
                  "s07": "怎么用", "s05": "审计层 · 默认折叠"}

    def _toc_rank(x):
        return TOC_ORDER.index(x[0]) if x[0] in TOC_ORDER else len(TOC_ORDER)

    # 重排与分组只对「第 NNN 期」日报生效：《第四章表体明细附录》是 12 个
    # 「第 NNN 期」小节、aid 全是 s-abs，套这组规则会插入 12 个「本期内容」标签。
    toc_view = [x for x in toc if x[1] or x[0] == "s-abs"]
    if is_digest:
        toc_view = sorted(toc_view, key=_toc_rank)
    groups = TOC_GROUPS if is_digest else {}

    # 目录行只留章节名：标题尾部那串括号是写给人看的口径注解（复核时点、补入条数、
    # 「正文之后」等），正文 h2 里原样保留。用户 2026-11-07 反馈「括号内的内容太长了」
    # —— 04 那条在 196px 侧栏里被折成三行。唯一影响点击预期的是「正文之后」（点它
    # 会跳到文末），留成一个弱化小标记，不占括号。
    # 只对日报生效：附录的小节标题是「第 049 期（2026-10-27）」，括号里是日期，
    # 剥掉等于把期次弄丢。
    def _toc_label(t):
        hint = "正文之后" if re.search(r"（[^）]*正文之后[^）]*）\s*$", t) else ""
        return esc(re.sub(r"（[^）]*）\s*$", "", t)), hint

    items = []
    for aid, no, t, is_h3, sub in toc_view:
        if aid in groups:
            items.append('<p class="toc-g">%s</p>' % groups[aid])
        label, hint = _toc_label(t) if is_digest else (esc(t), "")
        items.append(
            '<a class="toc-a" href="#%s"><span class="toc-n">%s</span>'
            '<span class="toc-t">%s%s</span></a>'
            % (aid, no if no != "00" else "\u00b7\u00b7", label,
               ('<span class="toc-hint">%s</span>' % hint) if hint else "")
        )
    toc_html = "\n".join(items)

    # 目录呈现：日报 / 附录照旧挂 196px 左侧栏；《常驻权益总账》只有「全量表」一节，
    # 侧栏纯占宽度 —— 收成主区顶部一行可展开控件，表格铺满，目录条目一条不删。
    if is_ledger:
        rail_block = (
            '  <details class="toc-fold" id="tocFold">'
            '<summary>本期目录<span class="fold-hint">　点开查看</span></summary>'
            '<nav class="toc-fold-nav">%s</nav></details>' % toc_html)
        shell_cls, body_cls = " shell-wide", ' class="ledger-page"'
    else:
        rail_block = (
            '  <div class="drawerwrap" id="drawerwrap"><aside class="rail" id="rail" aria-label="目录">\n'
            '    <p class="rail-t">本期目录</p>\n'
            '    <nav>%s</nav>\n'
            '  </aside></div>' % toc_html)
        shell_cls, body_cls = "", ""

    # 导航条：标题截短（去掉尾部括号里的复核口径），并把「四」标成尾段
    # —— 047 期修订后第四章物理位置在文末，编号仍是 04，不加分隔读者会以为是排序错了
    def _nav_t(t):
        return esc(re.sub(r"（[^）]*）\s*$", "", t))
    # 顶栏与目录同序；分隔竖线从「文末的第四章」移到「审计层」起点（s05）——
    # 04 现在是第四位，再挂 tail 就成了一条没有意义的竖线。
    nav_html = "".join(
        '<a href="#%s"%s><b>%s</b>%s</a>' % (
            aid, ' class="tail"' if aid == "s05" else "",
            no if no != "00" else "\u00b7\u00b7", _nav_t(t))
        for aid, no, t, is_h3, sub in toc_view
    )

    note_html = "".join("<p>%s</p>" % inline(x) for x in note)

    doc = PAGE.replace("__TITLE__", esc(mast)).replace("__ISSUE__", esc(issue))
    doc = doc.replace("__DATEBLOCK__", date_block).replace("__THEME__", esc(theme_line))
    doc = doc.replace("__NOTE__", note_html)
    doc = (doc.replace("__RAILBLOCK__", rail_block)
              .replace("__SHELLCLASS__", shell_cls)
              .replace("__BODYCLASS__", body_cls))
    if is_digest:
        html_body = _brief(issue, date_line, _headline(issue, src), html_body) + html_body
    doc = doc.replace("__NAV__", nav_html).replace("__BODY__", html_body)
    doc = doc.replace("__METAS__", esc(" \u00b7 ".join(re.sub(r"\*\*", "", x) for x in metas)))
    # 没抓到复核时点就整段去掉，不把占位符留在页面上
    doc = doc.replace("<span>__DATELINE__</span>",
                      ("<span>%s</span>" % esc(dateline)) if dateline else "")

    # 三档视图切换器（极速 / 完整 / 总账）：三页同一位置、同一外观，当前页高亮。
    # 条数都从文件实算，不手写 —— 手写的数字过一期就是错的。
    n_quick = n_ledger = None
    _q = os.path.join(WS, ".workbuddy", "data", "quick_items.csv")
    if os.path.exists(_q):
        n_quick = max(sum(1 for _ in io.open(_q, encoding="utf-8-sig")) - 1, 0)
    if is_ledger:
        n_ledger = sum(1 for _l in src.split("\n")
                       if _l.strip().startswith("|") and not re.match(r"^\|\s*-", _l.strip()))
        n_ledger = max(n_ledger - 1, 0)
    else:
        _lp = os.path.join(WS, "常驻权益总账.md")
        if os.path.exists(_lp):
            _lt = io.open(_lp, encoding="utf-8").read()
            n_ledger = max(sum(1 for _l in _lt.split("\n")
                               if _l.strip().startswith("|")
                               and not re.match(r"^\|\s*-", _l.strip())) - 1, 0)
    doc = doc.replace("__VS_CSS__", viewswitch.CSS)
    doc = doc.replace("__VIEWSWITCH__", viewswitch.render(
        "standing" if is_ledger else "full",
        issue_no=None if is_ledger else issue,
        n_quick=n_quick, n_ledger=n_ledger, ws=WS))
    doc = doc.replace("__ISSUE_LINE__", esc(issue_line))
    # 总账 / 附录的刊名就是页名，模板拼「刊名 · 页名」会写出
    # 「常驻权益总账 · 常驻权益总账」这种重复标题
    if issue_line == mast:
        doc = doc.replace("<title>%s · %s</title>" % (esc(mast), esc(issue_line)),
                          "<title>%s</title>" % esc(mast))
    doc = doc.replace("__ISSUE_BADGE__", esc(issue_badge))
    doc = doc.replace("__MH_NUM__", esc(mh_num))

    io.open(OUT, "w", encoding="utf-8", newline="\n").write(doc)
    print("written %s  %d bytes" % (OUT, os.path.getsize(OUT)))
    print("sections=%d  h3=%d" % (len([x for x in toc if not x[3]]), len([x for x in toc if x[3]])))
    return doc


# ---------------------------------------------------------------- 页面模板

PAGE = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>__TITLE__ · __ISSUE_LINE__</title>
<meta name="description" content="__METAS__">
<meta name="color-scheme" content="light dark">
<script>
/* 防闪烁：先定主题，再渲染 */
(function(){try{
  var t=localStorage.getItem("aihs-theme");
  if(!t){t=window.matchMedia&&window.matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light";}
  document.documentElement.setAttribute("data-theme",t);
}catch(e){}})();
</script>
<style>
/* ============================================================
   令牌层 —— 报刊纸（亮） / 夜读（暗），单一强调色：朱红
   ============================================================ */
:root{
  --bg:#f2eee5; --bg-2:#eae4d7; --surface:#fbf9f3; --surface-2:#f6f2e8;
  --ink:#1b1913; --ink-2:#3a362d; --muted:#5f584a; --faint:#736a5a;
  --rule:rgba(27,25,19,.16); --rule-2:rgba(27,25,19,.34); --rule-strong:rgba(27,25,19,.62);
  --accent:#bf3327; --accent-ink:#a02a20; --accent-soft:rgba(191,51,39,.10);
  --crit:#8c1a10; --soon:#8f5e12; --live:#3b6a4d; --plan:#38587a; --over:#6e675c;
  --hl:#ffe08a; --shadow:0 1px 2px rgba(40,32,20,.10),0 8px 28px rgba(40,32,20,.07);
  --grain:.05;
  --fd:"Source Han Serif SC","Noto Serif SC","Songti SC","STSong","SimSun",Georgia,"Times New Roman",serif;
  --fu:"Source Han Sans SC","PingFang SC","Microsoft YaHei","Hiragino Sans GB",-apple-system,sans-serif;
  --fm:"JetBrains Mono","Cascadia Mono",Consolas,"SFMono-Regular",Menlo,monospace;
  --fs-xs:12px; --fs-sm:13.5px; --fs-tbl:14px; --fs-mid:15px;
  --fs-base:17px; --fs-lg:19px; --fs-xl:23px;
  --fs-2xl:30px; --fs-3xl:42px; --fs-4xl:clamp(60px,9.8vw,138px);
  --s1:4px; --s2:8px; --s3:16px; --s4:24px; --s5:40px; --s6:64px; --s7:96px;
  --r1:3px; --r2:8px; --r3:14px;
  --ease:cubic-bezier(.16,1,.3,1); --fast:170ms; --base:340ms;
  /* 顶栏与筛选条的实际高度：抽屉定位、吸顶偏移都要跟它们对齐。
     初值只是兜底，页面加载后由 JS 量出真值覆盖（字号/换行都会改变高度）。 */
  --tb-h:57px; --chips-h:47px;
}
html[data-theme="dark"]{
  --bg:#131210; --bg-2:#191713; --surface:#1c1a16; --surface-2:#232019;
  --ink:#ece7dc; --ink-2:#cec8ba; --muted:#9d9486; --faint:#8e8577;
  --rule:rgba(236,231,220,.15); --rule-2:rgba(236,231,220,.3); --rule-strong:rgba(236,231,220,.55);
  --accent:#ff6d55; --accent-ink:#ff8b76; --accent-soft:rgba(255,109,85,.14);
  --crit:#ff3b30; --soon:#e0a24a; --live:#6fbe8e; --plan:#82a9d6; --over:#9c9387;
  --hl:#6b5a12; --shadow:0 1px 2px rgba(0,0,0,.5),0 10px 30px rgba(0,0,0,.42);
  --grain:.045;
}

/* ============================================================ 基础层 */
*,*::before,*::after{box-sizing:border-box}
[hidden]{display:none !important}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:var(--fu); font-size:var(--fs-base); line-height:1.9;
  font-feature-settings:"kern" 1;
  text-rendering:optimizeLegibility;
  /* 长英文专名 / URL / 模型 ID 在窄屏会把行撑破（320px 实测溢出 4px）。
     用 break-word 而不是 anywhere：后者会改变 min-content，连带把表格列宽算歪。 */
  overflow-wrap:break-word;
}
body::before{ /* 氛围层：纸面暖光 */
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(70rem 42rem at 8% -12%, var(--accent-soft), transparent 62%),
    radial-gradient(56rem 40rem at 102% 4%, rgba(56,88,122,.10), transparent 58%);
}
.grain{position:fixed; inset:0; pointer-events:none; z-index:1; opacity:var(--grain); mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
html[data-theme="dark"] .grain{mix-blend-mode:screen}
a{
  color:inherit; text-decoration:none;
  background-image:linear-gradient(var(--accent),var(--accent)); background-size:0% 1px;
  background-repeat:no-repeat; background-position:0 100%;
  transition:background-size var(--fast) ease-out,color var(--fast) ease-out;
}
a:hover{background-size:100% 1px; color:var(--accent-ink)}
:focus-visible{outline:2px solid var(--accent); outline-offset:2px; border-radius:2px}
.skip{position:absolute; left:-9999px; top:0; z-index:99; background:var(--surface); padding:12px 18px; border:1px solid var(--rule-2)}
.skip:focus{left:12px; top:12px}
code{
  font-family:var(--fm); font-size:.87em; padding:.1em .38em; border-radius:var(--r1);
  background:var(--surface-2); border:1px solid var(--rule); color:var(--ink-2);
}

/* ============================================================ 顶部条 */
.topbar{
  position:sticky; top:0; z-index:30;
  background:color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter:blur(10px) saturate(1.1);
  border-bottom:1px solid var(--rule);
}
@supports not (backdrop-filter:blur(1px)){.topbar{background:var(--bg)}}
.tb-in{
  max-width:1240px; margin:0 auto; padding:0 var(--s4);
  display:flex; align-items:center; gap:var(--s3); min-height:56px;
}
.tb-brand{font-family:var(--fd); font-weight:700; letter-spacing:.04em; white-space:nowrap; font-size:var(--fs-sm)}
.tb-brand .tbb-short{display:none}
.tb-brand b{color:var(--accent-ink); font-family:var(--fm); font-weight:700; margin-left:6px; letter-spacing:0}
.tb-nav{display:flex; gap:2px; overflow-x:auto; scrollbar-width:none; flex:1}
.tb-nav::-webkit-scrollbar{display:none}
.tb-nav a{
  font-size:var(--fs-xs); color:var(--muted); padding:7px 9px; border-radius:var(--r1); white-space:nowrap;
  background-image:none; transition:color var(--fast),background var(--fast);
}
.tb-nav a b{font-family:var(--fm); margin-right:5px; color:var(--faint); font-weight:600}
.tb-nav a:hover{color:var(--ink); background:var(--surface-2)}
.tb-nav a.active{color:var(--accent-ink); background:var(--accent-soft)}
.tb-nav a.active b{color:var(--accent-ink)}
.tb-nav a.tail{margin-left:6px; padding-left:14px; border-left:1px solid var(--rule-2)}
.tb-tools{display:flex; align-items:center; gap:var(--s2); margin-left:auto}
.search{position:relative; display:flex; align-items:center; flex:0 0 auto}
.search input{
  font-family:var(--fu); font-size:var(--fs-sm); color:var(--ink);
  background:var(--surface); border:1px solid var(--rule-2); border-radius:99px;
  padding:8px 14px 8px 32px; width:220px;
  transition:width var(--base) var(--ease),border-color var(--fast);
}
.search input::placeholder{color:var(--faint)}
/* 计数与上下条按钮只在「有输入」时占位，空态下把这段内边距还给占位符 */
.search input:not(:placeholder-shown){padding-right:76px}
.search input:focus{width:280px; border-color:var(--accent); outline:none}
.search .si{position:absolute; left:11px; font-size:13px; color:var(--faint); pointer-events:none}
.search .sc{
  position:absolute; right:8px; font-family:var(--fm); font-size:11px; color:var(--faint);
  display:flex; gap:4px; align-items:center; opacity:0; pointer-events:none;
  transition:opacity var(--fast);
}
.search input:not(:placeholder-shown) ~ .sc,
.search input:focus ~ .sc{opacity:1; pointer-events:auto}
.search .sc button{
  border:1px solid var(--rule); background:var(--surface-2); color:var(--ink-2); cursor:pointer;
  border-radius:var(--r1); font-size:11px; padding:2px 5px; line-height:1.4;
}
.search .sc button:hover{border-color:var(--accent); color:var(--accent-ink)}
.iconbtn{
  width:38px; height:38px; display:inline-grid; place-items:center; cursor:pointer;
  background:var(--surface); border:1px solid var(--rule-2); border-radius:99px;
  color:var(--ink-2); font-size:15px; transition:transform var(--fast),border-color var(--fast),color var(--fast);
}
.iconbtn:hover{border-color:var(--accent); color:var(--accent-ink); transform:translateY(-1px)}
#menuBtn{display:none}
#searchBtn{display:none}   /* 只在手机端露出来：点开一条全宽搜索栏 */
.progress{position:fixed; top:0; left:0; height:2px; width:0; background:var(--accent); z-index:31; transition:width 90ms linear}

/* ============================================================ 刊头 */
.masthead{position:relative; z-index:2; max-width:1240px; margin:0 auto; padding:var(--s6) var(--s4) var(--s4)}
.mh-top{
  display:flex; justify-content:space-between; align-items:baseline; gap:var(--s3);
  font-family:var(--fm); font-size:var(--fs-xs); letter-spacing:.14em; color:var(--muted);
  text-transform:uppercase; padding-bottom:var(--s2); flex-wrap:wrap;
  /* 窄屏换行时避免把「…增量与纠错口径」拆成只剩一个「径」字的孤行 */
  text-wrap:pretty;
}
.mh-top em{font-style:normal; color:var(--accent-ink)}
.mh-rule{height:0; border-top:3px solid var(--ink); border-bottom:1px solid var(--ink); padding-top:3px; margin-bottom:var(--s4)}
h1.mh-t{
  font-family:var(--fu); font-weight:800; letter-spacing:-.005em;
  font-size:clamp(34px,5.4vw,62px); line-height:1.06; margin:0 0 var(--s3); text-wrap:balance;
}
.mh-sub{font-family:var(--fu); font-size:var(--fs-sm); color:var(--muted); letter-spacing:.06em; margin:0 0 var(--s5)}
.mh-sub b{color:var(--ink-2); font-weight:600}
.mh-num{
  position:absolute; right:var(--s4); top:clamp(74px,7.4vw,106px);
  font-family:var(--fd); font-weight:700; font-size:var(--fs-4xl); line-height:.8;
  color:transparent; -webkit-text-stroke:1.5px var(--rule);
  letter-spacing:-.03em; pointer-events:none; user-select:none; z-index:-1;
}
@supports not (-webkit-text-stroke:1px #000){.mh-num{color:var(--bg-2)}}
html[data-theme="dark"] .mh-num{-webkit-text-stroke-color:rgba(236,231,220,.20)}
.pubnote{
  border-left:3px solid var(--accent); background:var(--surface); box-shadow:var(--shadow);
  padding:var(--s3) var(--s4); margin:0 0 var(--s5); border-radius:0 var(--r2) var(--r2) 0;
}
.pubnote p{margin:0 0 6px; font-size:var(--fs-mid); color:var(--ink-2); font-family:var(--fu); line-height:1.75}
.pubnote p:last-child{margin-bottom:0}
__VS_CSS__
.summary-note{}

/* ============================================================ 主栅格 */
.shell{
  position:relative; z-index:2; max-width:1240px; margin:0 auto;
  padding:0 var(--s4) var(--s7); display:grid; grid-template-columns:196px minmax(0,1fr); gap:var(--s6);
}
.rail{position:sticky; top:78px; align-self:start; max-height:calc(100vh - 110px); overflow:auto; padding-bottom:var(--s4)}
.drawerwrap{min-width:0}
.rail-t{
  font-family:var(--fm); font-size:10.5px; letter-spacing:.18em; color:var(--faint);
  text-transform:uppercase; padding-bottom:var(--s2); margin-bottom:var(--s2); border-bottom:1px solid var(--rule);
}
.toc-a{
  display:grid; grid-template-columns:26px 1fr; gap:6px; align-items:baseline;
  font-size:var(--fs-sm); color:var(--muted); padding:7px 0 7px 8px; border-left:2px solid transparent;
  background-image:none; line-height:1.45;
}
.toc-n{font-family:var(--fm); font-size:11px; color:var(--faint)}
/* 「正文之后」标记：只说明点它跳到文末，不用括号、不加底色（2026-11-07）。
   单独占一行 —— 196px 侧栏里跟在章节名后面会把标题挤到折行。 */
.toc-hint{
  display:block; margin-top:1px; font-family:var(--fm); font-size:9.5px;
  letter-spacing:.06em; color:var(--faint); opacity:.8;
}
/* 目录分组标签：一条细线 + 小字，不加框（2026-11-07 方案 A） */
.toc-g{
  font-family:var(--fm); font-size:9.5px; letter-spacing:.16em; text-transform:uppercase;
  color:var(--faint); margin:14px 0 4px; padding-top:11px; border-top:1px solid var(--rule);
}
.toc-g:first-child{margin-top:0; padding-top:0; border-top:0}
.toc-a:hover{color:var(--ink); border-left-color:var(--rule-2)}
.toc-a.active{color:var(--accent-ink); border-left-color:var(--accent); background:var(--accent-soft)}
.toc-a.active .toc-n{color:var(--accent-ink)}

/* 《常驻权益总账》只有一个章节（全量表），左侧 196px 目录栏纯占宽度：
   收成主区顶部一行可展开控件，表格铺满整栏。目录条目一个不删，点开即见。 */
.shell.shell-wide{grid-template-columns:minmax(0,1fr); gap:0}
/* 总账页最后就是这张表，表格外框底 = 内容结束。再照别的页留 96px 页脚上边距，
   深色底上会读成「表格下面塌了一块空白」（用户 2026-11-07 截图框出的那块）。
   只收这一页，其它页仍是 var(--s7)。 */
body.ledger-page .shell{padding-bottom:var(--s5)}
.toc-fold{
  margin:0 0 var(--s4); padding:8px var(--s3);
  border:1px solid var(--rule); border-radius:var(--r2); background:var(--surface);
}
.toc-fold>summary{
  list-style:none; cursor:pointer; display:flex; align-items:center; gap:8px;
  font-family:var(--fm); font-size:11px; letter-spacing:.12em; color:var(--muted);
}
.toc-fold>summary::-webkit-details-marker{display:none}
.toc-fold>summary::before{content:"+"; font-size:15px; line-height:1; color:var(--accent-ink)}
.toc-fold[open]>summary::before{content:"−"}
.toc-fold-nav{display:grid; gap:2px; margin-top:8px; padding-top:8px; border-top:1px solid var(--rule)}
.toc-fold-nav .toc-a{padding-top:6px; padding-bottom:6px}
/* 总账页没有侧栏抽屉，窄屏的汉堡按钮点了会开一个空抽屉 */
body.ledger-page #menuBtn{display:none !important}
@media print{ .toc-fold{display:none !important} }

main{min-width:0}
.sec{scroll-margin-top:76px; padding-top:var(--s5)}
.sec h2{
  font-family:var(--fu); font-weight:800; font-size:var(--fs-2xl); line-height:1.24;
  margin:0 0 var(--s4); display:flex; align-items:baseline; gap:var(--s3);
  padding-bottom:var(--s3); border-bottom:2px solid var(--ink); flex-wrap:wrap;
}
.sn{font-family:var(--fm); font-size:var(--fs-sm); color:var(--accent-ink); letter-spacing:.08em; font-weight:700}
.h2sub{font-family:var(--fu); font-size:var(--fs-sm); font-weight:400; color:var(--muted); letter-spacing:.04em}
h3{
  font-family:var(--fu); font-weight:700; font-size:var(--fs-lg); line-height:1.5;
  margin:var(--s5) 0 var(--s3); text-wrap:balance;
}
.h3n{
  font-family:var(--fm); font-size:var(--fs-sm); color:var(--surface); background:var(--ink);
  padding:1px 7px; border-radius:var(--r1); margin-right:9px; vertical-align:2px;
}
main p{margin:0 0 var(--s3); font-family:var(--fd); font-size:var(--fs-base); line-height:1.92; color:var(--ink-2)}
main p:last-child{margin-bottom:0}
main strong{font-weight:700; color:var(--ink)}
.sec>p{margin-bottom:var(--s4)}

/* 摘要区：要点卡片 */
.summary .ul{list-style:none; margin:0 0 var(--s4); padding:0; display:grid; gap:var(--s2)}
.summary .ul li{
  position:relative; background:var(--surface); border:1px solid var(--rule); border-radius:var(--r2);
  padding:var(--s3) var(--s4) var(--s3) 58px; font-family:var(--fu); font-size:15.5px; line-height:1.8;
  color:var(--ink-2); box-shadow:var(--shadow);
  transition:transform var(--base) var(--ease),border-color var(--fast);
}
.summary .ul li:hover{transform:translateX(4px); border-color:var(--rule-2)}
.summary .ul li::before{
  counter-increment:sum;
  content:"0" counter(sum);
  position:absolute; left:var(--s3); top:var(--s3);
  font-family:var(--fm); font-size:20px; font-weight:700; color:var(--accent); line-height:1.1;
  white-space:nowrap;   /* 窄屏下「01」会被折成上下两个数字，竖排数字看着像排版事故 */
}
.summary .ul{counter-reset:sum}

/* 列表 */
.ul{margin:0 0 var(--s4); padding-left:0; list-style:none}
.ul li{position:relative; padding-left:22px; margin-bottom:var(--s2); font-family:var(--fd); line-height:1.9; color:var(--ink-2)}
.ul li::before{content:""; position:absolute; left:4px; top:.82em; width:7px; height:1.5px; background:var(--accent)}
.ol{list-style:none; margin:0 0 var(--s4); padding:0; display:grid; gap:var(--s3)}
.ol li{display:grid; grid-template-columns:34px 1fr; gap:var(--s3); align-items:start; font-family:var(--fd); line-height:1.9; color:var(--ink-2)}
.lin{font-family:var(--fm); font-weight:700; color:var(--accent); font-size:var(--fs-sm); padding-top:.42em; letter-spacing:.02em}
.ol.big li{
  background:var(--surface); border:1px solid var(--rule); border-left:3px solid var(--accent);
  border-radius:0 var(--r2) var(--r2) 0; padding:var(--s3) var(--s4); box-shadow:var(--shadow);
}
.ol.big .lin{font-size:22px; color:var(--accent); padding-top:.1em; line-height:1.1}
ol.ol:not(.big) li{margin-bottom:0}

/* 引用块（编者按 / 读法 / 免责声明） */
.bq{
  margin:0 0 var(--s4); padding:var(--s3) var(--s4);
  border-left:2px solid var(--rule-strong); background:var(--surface-2);
  border-radius:0 var(--r2) var(--r2) 0;
}
.bq p{
  margin:0 0 8px; font-family:var(--fd); font-size:15.5px; line-height:1.85; color:var(--muted);
}
.bq p:last-child{margin-bottom:0}
.bq p::before{content:"\u201c"; color:var(--accent); font-family:var(--fd); font-size:1.5em; line-height:0; vertical-align:-.18em; margin-right:.12em}
.bq p::after{content:"\u201d"; color:var(--accent); font-family:var(--fd); font-size:1.5em; line-height:0; vertical-align:-.18em; margin-left:.12em}
.bq strong{color:var(--ink-2)}

/* 引用块 */
blockquote{margin:0}

/* 表格 */
.tblwrap{position:relative; margin:0 0 var(--s5)}
.tblwrap.scrolly{max-height:74vh; overflow:auto; border:1px solid var(--rule); border-radius:var(--r2); background:var(--surface); box-shadow:var(--shadow)}
.tbl{
  width:100%; border-collapse:collapse; font-family:var(--fu); font-size:var(--fs-tbl); line-height:1.7;
  background:var(--surface); border:1px solid var(--rule); border-radius:var(--r2); overflow:hidden;
}
/* 表头吸顶的前提：表格自身不能 overflow:hidden。
   它会新建一个滚动容器，把 th{position:sticky} 整个废掉 —— 实测在容器内滚动
   400px 后表头跑到容器上方 305px，正好被 sticky 的筛选条压掉半行（用户
   2026-11-06「这里老是被上面截断」）。外框与圆角由 .tblwrap.scrolly 承担，
   这里不需要再裁切；非滚动容器里的 .tbl 仍保留 overflow:hidden 裁圆角。 */
.tblwrap.scrolly .tbl{border:0; border-radius:0; overflow:visible}
.tbl thead th{
  position:sticky; top:0; z-index:2; text-align:left; vertical-align:bottom;
  font-family:var(--fm); font-size:11.5px; letter-spacing:.09em; text-transform:uppercase;
  color:var(--muted); font-weight:600; padding:12px var(--s3);
  background:var(--surface-2); border-bottom:1.5px solid var(--rule-strong); white-space:nowrap;
}
.tbl tbody td{padding:11px var(--s3); border-bottom:1px solid var(--rule); vertical-align:top; color:var(--ink-2)}
.tbl tbody tr:last-child td{border-bottom:0}
.tbl tbody tr{transition:background var(--fast)}
.tbl tbody tr:hover{background:var(--surface-2)}
.tbl td:first-child{color:var(--ink); font-weight:600}
/* 首列条目名被压到逐字换行时，给一个按内容算出的下限（由编译器写入 --w1） */
.tbl.w1 tbody td:first-child{min-width:var(--w1,120px); overflow-wrap:break-word}
.tbl code{background:transparent; border-color:var(--rule); padding:.05em .3em}
.tbl strong{color:var(--ink)}
.tbl tr[hidden]{display:none}

/* 截止时间表：状态色条 + 筛选 */
.ledger{border-left:3px solid transparent}
/* 固定列宽：状态列原先 nowrap 会把该列 min-content 撑到整句宽（实测 779px），
   把「活动」列榨到 126px 逐字换行。改为固定布局 + 状态列允许换行。 */
.tbl.ledger{table-layout:fixed}
.tbl.ledger th[data-col="date"]{width:76px}
.tbl.ledger th[data-col="st"]{width:190px}
.ledger tbody tr{box-shadow:inset 3px 0 0 var(--rule-2)}
.ledger tbody tr[data-st="crit"]{box-shadow:inset 3px 0 0 var(--crit)}
.ledger tbody tr[data-st="soon"]{box-shadow:inset 3px 0 0 var(--soon)}
.ledger tbody tr[data-st="live"]{box-shadow:inset 3px 0 0 var(--live)}
.ledger tbody tr[data-st="warn"]{box-shadow:inset 3px 0 0 var(--plan)}
.ledger tbody tr[data-st="over"]{box-shadow:inset 3px 0 0 var(--over)}
.ledger tbody tr[data-st="over"] td{color:var(--muted)}
.ledger td[data-col="st"]{white-space:normal; overflow-wrap:anywhere}
/* 《常驻权益总账》全量表专用列宽（2026-11-06 用户截图：活动列一大片空白、
   截止列被挤成一字一行）。日报 4.1 的 date=76px 是给短日历日用的，不能套过来。
   三列按内容量配比分宽，仍是 fixed 布局 —— 长状态句不会把整表撑爆。 */
.tbl.ledger.ledger-full th[data-col="body"]{width:28%}
.tbl.ledger.ledger-full th[data-col="date"]{width:32%}
.tbl.ledger.ledger-full th[data-col="st"]{width:40%}
.tbl.ledger.ledger-full tbody td{overflow-wrap:anywhere}
.st{
  display:inline-block; width:9px; height:9px; border-radius:99px; margin-right:8px; vertical-align:1px;
  background:var(--rule-2);
}
.st-crit{background:var(--crit)} .st-soon{background:var(--soon)} .st-live{background:var(--live)}
.st-warn{background:var(--plan)} .st-over{background:var(--over)}
.st-txt{font-weight:600}
tr[data-st="crit"] .st-txt{color:var(--crit)}
tr[data-st="soon"] .st-txt{color:var(--soon)}
tr[data-st="live"] .st-txt{color:var(--live)}
tr[data-st="warn"] .st-txt{color:var(--plan)}
tr[data-st="over"] .st-txt{color:var(--over)}
/* 长状态格：默认收 4 行，点一下展开全文。文字一个字都不删，只是不默认铺开。 */
.st-txt.cbody.clamp{
  display:-webkit-box; -webkit-line-clamp:4; -webkit-box-orient:vertical;
  overflow:hidden; cursor:pointer; border-radius:4px;
}
.st-txt.cbody.clamp:hover{background:var(--surface-2)}
.st-txt.cbody.clamp:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
@media print{ .st-txt.cbody.clamp{display:block; overflow:visible} }
.chips{display:flex; flex-wrap:wrap; align-items:center; gap:6px; padding:10px var(--s3);
  background:var(--surface-2); border-bottom:1.5px solid var(--rule-strong); position:sticky; top:0; z-index:3}
/* 截止表待在可滚动容器里，容器顶部已经被 chips 占住——表头要吸在它下方，
   否则两者都 top:0、chips 的 z-index 更高，表头第一行会被整个盖住。 */
.tblwrap.scrolly .tbl thead th{top:var(--chips-h)}
.chips-label{font-family:var(--fm); font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--faint); margin-right:4px}
.chip{
  font-family:var(--fu); font-size:12.5px; color:var(--ink-2); cursor:pointer;
  background:var(--surface); border:1px solid var(--rule-2); border-radius:99px;
  padding:4px 11px; display:inline-flex; align-items:center; gap:6px; transition:all var(--fast) ease-out;
}
.chip b{font-family:var(--fm); font-size:10.5px; color:var(--faint); font-weight:600}
.chip:hover{border-color:var(--accent); color:var(--accent-ink)}
.chip.on{background:var(--ink); border-color:var(--ink); color:var(--bg)}
.chip.on b{color:var(--bg); opacity:.7}
.chips-count{margin-left:auto; font-family:var(--fm); font-size:11px; color:var(--faint)}
.scrollhint{display:none; font-family:var(--fm); font-size:11px; color:var(--faint); text-align:right; margin:6px 0 0}

/* 页脚 */
.foot{
  position:relative; z-index:2; max-width:1240px; margin:0 auto; padding:var(--s5) var(--s4) var(--s6);
  border-top:2px solid var(--ink); font-family:var(--fu); font-size:var(--fs-sm); color:var(--muted);
}
.foot .fr{display:flex; justify-content:space-between; gap:var(--s3); flex-wrap:wrap; padding-bottom:var(--s2);
  border-bottom:1px solid var(--rule); margin-bottom:var(--s3); font-family:var(--fm); font-size:11px; letter-spacing:.1em; text-transform:uppercase}
.foot p{margin:0 0 8px; line-height:1.8}
.foot strong{color:var(--ink-2)}

/* 悬浮控件 */
.fab{position:fixed; right:18px; bottom:18px; z-index:32; display:flex; flex-direction:column; gap:8px; opacity:.72; transition:opacity var(--fast)}
.fab:hover,.fab:focus-within{opacity:1}
@media (hover:none){.fab{opacity:1}}
.fab .iconbtn{width:44px; height:44px; box-shadow:var(--shadow); background:var(--surface)}

/* 搜索高亮 */
mark.hl{background:var(--hl); color:var(--ink); padding:0 .1em; border-radius:2px}
mark.hl.cur{background:var(--accent); color:#fff}

/* 入场：一次编排好的序列 */
@media (prefers-reduced-motion:no-preference){
  .rise{opacity:0; transform:translateY(18px)}
  .rise.in{opacity:1; transform:none; transition:opacity var(--base) var(--ease),transform var(--base) var(--ease)}
  .masthead{animation:mhIn 760ms var(--ease) both}
  @keyframes mhIn{from{opacity:0; transform:translateY(22px)}to{opacity:1;transform:none}}
  .masthead .mh-top{animation:mhIn 620ms 80ms var(--ease) both}
  .masthead .mh-t{animation:mhIn 700ms 140ms var(--ease) both}
  .masthead .pubnote{animation:mhIn 700ms 220ms var(--ease) both}
  .shell{animation:mhIn 700ms 300ms var(--ease) both}
}
@media (prefers-reduced-motion:reduce){
  *{animation:none !important; transition:none !important}
  .rise{opacity:1 !important; transform:none !important}
}

/* ============================================================ 响应式 */
@media (max-width:1080px){
  .shell{grid-template-columns:minmax(0,1fr); gap:0}
  /* 抽屉：外层 fixed + overflow:hidden 当裁剪盒，内层才平移。
     若直接平移 fixed 的 .rail，它会把文档 scrollWidth 撑宽 326px（实测）。 */
  .drawerwrap{
    position:fixed; inset:var(--tb-h) 0 0 0; overflow:hidden; z-index:29;
    visibility:hidden; pointer-events:none; transition:visibility 0s linear var(--base);
  }
  body.nav-open .drawerwrap{visibility:visible; pointer-events:auto; transition-delay:0s}
  .rail{
    position:absolute; top:0; right:0; bottom:0; width:min(86vw,320px);
    max-height:none; background:var(--surface); border-left:1px solid var(--rule-2);
    padding:var(--s4); overflow:auto; box-shadow:var(--shadow);
    transform:translateX(102%); transition:transform var(--base) var(--ease);
  }
  body.nav-open .rail{transform:none}
  #menuBtn{display:inline-grid}
  .tb-nav{display:none}
}
@media (max-width:820px){
  :root{--fs-base:16.5px; --fs-2xl:25px; --s5:32px; --s6:44px}
  .tb-in{padding:0 var(--s3); gap:var(--s2)}
  .search input{width:168px}
  .search input:focus{width:206px}
  .tb-brand .tbb-long{display:none}
  .tb-brand .tbb-short{display:inline}
  .tbl.ledger{min-width:600px}
  .tbl.ledger th[data-col="st"]{width:150px}
  .masthead,.shell,.foot{padding-left:var(--s3); padding-right:var(--s3)}
  .mh-num{right:var(--s3); -webkit-text-stroke-width:1px}
  .tblwrap:not(.scrolly){overflow-x:auto; -webkit-overflow-scrolling:touch}
  .tblwrap:not(.scrolly) .tbl{min-width:640px}
  .scrollhint{display:block}
  .ol.big li{padding:var(--s3)}
  .ol.big li{grid-template-columns:26px 1fr; gap:var(--s2)}
  .summary .ul li{padding-left:52px}
}
/* ---------- 手机（<=600px）：换一套阅读形态，不是把桌面版等比缩小 ----------
   三处结构性改动，都对着实测出来的毛病改：
   ① 搜索不再隐藏。原先 <=520px 直接 display:none，手机上等于没有搜索；
      现在收成一个图标，点开是一条全宽搜索栏（绝对定位挂在顶栏下沿，不撑高顶栏）。
   ② 2 列表改成纵向堆叠卡片。手机上横滑表格很难用，而 2 列表堆叠后既不用滑、
      又刚好把「名称 → 说明」的层级关系表达出来。
   ③ 3 列及以上继续横滑，但首列粘住——横滑时不丢参照物，知道自己看的是哪一行。
   另外把触控目标放大到 44px（图标按钮原 38px、筛选 chip 原 26px 高，都偏小）。
*/
@media (max-width:600px){
  :root{--fs-base:17px; --s3:14px; --s4:20px; --s5:26px; --s6:34px; --s7:48px}
  .mh-num{display:none}

  /* 顶栏与搜索 */
  .tb-in{min-height:52px}
  #searchBtn{display:inline-grid}
  .iconbtn{width:44px; height:44px; font-size:16px}
  .tb-tools{gap:6px}
  .search{
    position:absolute; left:0; right:0; top:100%; z-index:35;
    display:none; padding:10px var(--s3);
    background:var(--surface); border-bottom:1px solid var(--rule-2); box-shadow:var(--shadow);
  }
  body.search-open .search{display:flex}
  .search input{width:100%; font-size:16px; padding:11px 14px 11px 34px; -webkit-appearance:none; appearance:none}
  .search input:focus{width:100%}
  .search .si{left:calc(var(--s3) + 12px)}
  .search input:not(:placeholder-shown){padding-right:104px}
  /* 计数与上下条按钮要能点得中：原尺寸 11px/18px 高，手机上根本按不准 */
  .search .sc{right:10px; gap:6px; font-size:13px}
  .search .sc button{min-width:34px; min-height:34px; font-size:14px; border-radius:6px}

  /* 刊头 */
  h1.mh-t{font-size:27px; line-height:1.22}
  .mh-top{font-size:10.5px; letter-spacing:.1em; gap:var(--s2)}
  .mh-sub{font-size:13.5px; margin-bottom:var(--s4)}
  .pubnote{padding:var(--s3)}
  .pubnote p{font-size:14.5px}

  /* 目录抽屉条目放大 */
  .toc-a{padding:11px var(--s2)}

  /* 章节 */
  .sec{scroll-margin-top:calc(var(--tb-h) + 10px)}
  .sec h2{font-size:21px}
  h3{font-size:17px; margin:var(--s4) 0 var(--s3)}

  /* 摘要卡片 */
  .summary .ul li{padding:13px var(--s3) 13px 46px; font-size:15px; line-height:1.78}
  .summary .ul li::before{font-size:17px; top:13px}

  /* 列表 */
  .ul li{padding-left:19px}
  .ol{gap:var(--s2)}
  .ol li{grid-template-columns:28px 1fr; gap:10px}
  .ol.big li{padding:13px 14px; grid-template-columns:24px 1fr; gap:10px}
  .ol.big .lin{font-size:19px}

  /* 表格：3 列以上横滑 + 首列粘住 */
  /* 先解开 .tbl 自己的 overflow:hidden。它原本只为了裁圆角，但 overflow:hidden
     同样会把自己变成「滚动容器」，于是 td 的 sticky 以 table 为参照（而 table
     并不滚动）——首列粘性会静默失效，横滑时首列照样滚走（实测截图确认）。
     手机上优先保首列粘住，圆角让位（表格改直角，肉眼几乎无感）。 */
  .tbl{overflow:visible; border-radius:0}
  .tblwrap:not(.scrolly){overflow-x:auto; -webkit-overflow-scrolling:touch}
  .tblwrap:not(.scrolly) .tbl{min-width:600px}
  .tblwrap:not(.scrolly) .tbl:not(.c2) tbody td:first-child,
  .tblwrap.scrolly .tbl tbody td:first-child{
    position:sticky; left:0; z-index:1;
    background:var(--surface); box-shadow:1px 0 0 var(--rule-2);
  }
  .tblwrap:not(.scrolly) .tbl:not(.c2) thead th:first-child,
  .tblwrap.scrolly .tbl thead th:first-child{left:0; z-index:4; background:var(--surface-2)}
  /* 首列装长专名的表（桌面端放不下、只给了手机端下限）：放宽，别压成逐字竖排 */
  .tblwrap:not(.scrolly) .tbl.w1m:not(.c2) tbody td:first-child,
  .tblwrap.scrolly .tbl.w1m tbody td:first-child{
    min-width:var(--w1m); overflow-wrap:break-word;
  }
  .scrollhint{text-align:left}

  /* 表格：2 列纵向堆叠成卡片，彻底不横滑 */
  .tblwrap:not(.scrolly) .tbl.c2,
  .tblwrap.scrolly .tbl.c2{
    display:block; min-width:0; border:0; background:transparent; border-radius:0;
  }
  .tbl.c2 thead{display:none}
  .tbl.c2 tbody{display:block}
  .tbl.c2 tbody tr{
    display:block; background:var(--surface); border:1px solid var(--rule);
    border-radius:var(--r2); padding:12px 14px; margin-bottom:10px; box-shadow:var(--shadow);
  }
  .tbl.c2 tbody tr:last-child{margin-bottom:0}
  .tbl.c2 tbody tr:hover{background:var(--surface)}
  .tbl.c2 tbody td{display:block; border:0; padding:0; background:transparent; box-shadow:none}
  .tbl.c2 tbody td:first-child{
    position:relative; padding-left:15px; margin-bottom:5px;
    font-family:var(--fu); font-weight:700; font-size:14.5px; color:var(--ink);
  }
  .tbl.c2 tbody td:first-child::before{
    content:""; position:absolute; left:0; top:.62em; width:7px; height:1.5px; background:var(--accent);
  }

  /* 截止表筛选条：改成一行横滑，避免换行成三四排把表格挤下去 */
  .chips{
    flex-wrap:nowrap; overflow-x:auto; -webkit-overflow-scrolling:touch;
    scrollbar-width:none; padding:9px var(--s3); gap:7px;
    border-radius:var(--r2) var(--r2) 0 0;
  }
  .chips::-webkit-scrollbar{display:none}
  .chips-label,.chips-count{display:none}
  .chip{flex:0 0 auto; padding:9px 14px; font-size:13px; min-height:40px}
  .chip b{font-size:11px}

  /* 截止表：手机上拆成一张张卡片，不再横滑。
     两个理由：① 它最关键的信息是「什么时候到期」，而截止列在横滑视口之外，
        用户得先横滑才看得到，跟这张表的用途正好相反；
     ② 横滑时行高被状态列的长文本撑开，首列只有一行字、下面一大片空白。
     拆成卡片后「活动 / 截止 / 状态」三行一屏读完，状态色条也还在。
     列定位靠编译期打好的 data-col，不依赖第几列。 */
  .tblwrap.scrolly{
    max-height:none; overflow:visible; border:0; background:transparent; box-shadow:none;
  }
  .tblwrap.scrolly .chips{top:var(--tb-h)}   /* 吸在顶栏下沿，滚到哪都能筛 */
  .tbl.ledger{display:block; min-width:0; border:0; background:transparent; table-layout:auto}
  .tbl.ledger thead{display:none}
  .tbl.ledger tbody{display:block}
  .tbl.ledger tbody tr{
    /* 日期列用 max-content：状态列文字很长时，若两列是 1fr/auto，
       状态列会把日期列挤到几乎为 0，日期被压成「9\n/\n1\n7」逐字竖排 */
    display:grid; grid-template-columns:max-content minmax(0,1fr); gap:5px 10px; align-items:baseline;
    background:var(--surface); border:1px solid var(--rule); border-radius:var(--r2);
    padding:12px 14px; margin-bottom:9px;
  }
  .tbl.ledger tbody tr:last-child{margin-bottom:0}
  .tbl.ledger tbody td{display:block; border:0; padding:0; background:transparent; box-shadow:none}
  .tbl.ledger tbody td[data-col="body"]{grid-column:1 / -1; color:var(--ink); font-weight:600; font-size:14.5px}
  .tbl.ledger tbody td[data-col="date"]{
    grid-column:1; white-space:nowrap;
    font-family:var(--fm); font-size:12.5px; color:var(--muted);
  }
  .tbl.ledger tbody td[data-col="st"]{grid-column:2; text-align:right; font-size:13px}
  .tbl.ledger tbody tr:hover{background:var(--surface)}
  /* 截止表已经拆成卡片、不再横滑，滑动提示在这里是错的 */
  .tblwrap.scrolly .scrollhint{display:none}

  /* 悬浮控件与刘海/小白条 —— env() 在不支持时整条声明被丢弃，自动退回上面的值 */
  .fab{right:calc(14px + env(safe-area-inset-right)); bottom:calc(14px + env(safe-area-inset-bottom))}
  .tb-in{padding-left:calc(var(--s3) + env(safe-area-inset-left));
         padding-right:calc(var(--s3) + env(safe-area-inset-right))}
  .masthead,.shell,.foot{
    padding-left:calc(var(--s3) + env(safe-area-inset-left));
    padding-right:calc(var(--s3) + env(safe-area-inset-right));
  }
  .foot{padding-bottom:calc(var(--s6) + env(safe-area-inset-bottom))}
  .search{padding-left:calc(var(--s3) + env(safe-area-inset-left));
          padding-right:calc(var(--s3) + env(safe-area-inset-right))}
}
/* 超窄屏（<=360px：iPhone SE 一代、小屏安卓）再收一档。
   断点取 360 而不是 380，是为了把 375/390/414 这些在售机型都留在上面那一档
   用 27px 主标题——375 恰恰是 iPhone SE 2/3 的宽度，也是相当常见的屏幕。 */
@media (max-width:360px){
  h1.mh-t{font-size:24px}
  .mh-top{font-size:9.5px}
  .tblwrap:not(.scrolly) .tbl{min-width:560px}
  .tblwrap:not(.scrolly) .tbl.c2{min-width:0}
  .summary .ul li{padding-left:42px}
  .summary .ul li::before{font-size:16px}
}

/* ============================================================ 打印 */
@media print{
  :root{
    --bg:#fff; --bg-2:#fff; --surface:#fff; --surface-2:#fff;
    --ink:#000; --ink-2:#000; --muted:#333; --faint:#555;
    --rule:rgba(0,0,0,.25); --rule-2:rgba(0,0,0,.5); --rule-strong:#000;
    --accent:#000; --accent-ink:#000; --accent-soft:#fff; --shadow:none; --grain:0;
    --crit:#000; --soon:#000; --live:#000; --plan:#000; --over:#666;
  }
  body{border:0; background:#fff}
  body::before,.grain,.topbar,.fab,.rail,.drawerwrap,.chips,.scrollhint,.progress,[data-no-print]{display:none !important}
  .shell{display:block; max-width:none; padding:0}
  .masthead{padding:0 0 12px}
  .mh-num{display:none}
  main p,.ul li,.ol li,.tbl,.foot{font-size:10.5pt}
  .sec{padding-top:14px; break-inside:auto}
  .sec h2{font-size:16pt; border-bottom:1.5pt solid #000}
  h3{font-size:12pt}
  .tblwrap,.tblwrap.scrolly{max-height:none; overflow:visible; border:0; box-shadow:none}
  .tbl{min-width:0 !important; border:1pt solid #000}
  .tbl thead{display:table-header-group}
  .tbl thead th{position:static; background:#fff; color:#000; border-bottom:1pt solid #000; font-size:8pt}
  .tbl tbody td{border-bottom:.5pt solid #666; padding:5px 7px}
  .tbl tbody tr{box-shadow:none !important; opacity:1 !important; break-inside:avoid}
  /* 手机端那套堆叠/粘性样式在纸上要退回成真表格（窄屏下打印时两条媒体查询会同时命中，
     print 在后面所以能覆盖；仍加 !important 防字号相关的特异性意外） */
  .tbl.c2{display:table !important; border:1pt solid #000 !important}
  .tbl.c2 thead{display:table-header-group !important}
  .tbl.c2 tbody{display:table-row-group !important}
  .tbl.c2 tbody tr{display:table-row !important; margin-bottom:0 !important; padding:0 !important}
  .tbl.c2 tbody td{display:table-cell !important; padding:5px 7px !important}
  .tbl.c2 tbody td:first-child::before{content:none !important}
  .tbl.ledger{display:table !important; border:1pt solid #000 !important}
  .tbl.ledger thead{display:table-header-group !important}
  .tbl.ledger tbody{display:table-row-group !important}
  .tbl.ledger tbody tr{display:table-row !important; margin:0 !important; padding:0 !important}
  .tbl.ledger tbody td{display:table-cell !important; padding:5px 7px !important}
  .tbl tbody td:first-child,.tbl thead th:first-child{position:static !important; box-shadow:none !important}
  .st{background:#000 !important; border:0}
  .ledger tbody tr{box-shadow:none !important}
  .tbl a,.tbl a:hover{color:#000}
  tr,.ol.big li,.summary .ul li,.pubnote{break-inside:avoid}
  a{background-image:none}
  @page{size:A4 portrait; margin:12mm}
}

/* ---- 30 秒速览卡（060 期 A 方案） ---- */
.brief{
  background:var(--surface); border:1px solid var(--rule-2); border-left:4px solid var(--accent);
  border-radius:0 var(--r2) var(--r2) 0; padding:var(--s3) var(--s4);
  margin:0 0 var(--s5); box-shadow:var(--shadow);
}
.brief-k{font-family:var(--fm); font-size:var(--fs-xs); letter-spacing:.06em;
  color:var(--faint); margin:0 0 var(--s2)}
.brief-h{font-family:var(--fu); font-weight:700; font-size:var(--fs-xl); line-height:1.5;
  color:var(--ink); margin:0 0 var(--s3); text-wrap:balance}
.brief-m{display:flex; flex-wrap:wrap; gap:var(--s2); margin:0 0 var(--s3)}
.brief-m span{font-family:var(--fu); font-size:var(--fs-sm); color:var(--muted);
  background:var(--surface-2); border:1px solid var(--rule); border-radius:99px; padding:5px 12px}
.brief-m b{font-family:var(--fm); color:var(--accent-ink); font-size:var(--fs-mid)}
.brief-a{display:flex; flex-wrap:wrap; gap:var(--s2); margin:0 0 var(--s3)}
.brief-a a,.brief-a button{font-family:var(--fu); font-size:var(--fs-sm);
  color:var(--accent-ink); background:var(--accent-soft); border:1px solid var(--rule-2);
  border-radius:var(--r1); padding:8px 14px; text-decoration:none; cursor:pointer}
.brief-a a:hover,.brief-a button:hover{border-color:var(--accent)}
.brief-n{font-family:var(--fu); font-size:var(--fs-sm); line-height:1.7;
  color:var(--muted); margin:0}

/* ---- 审计层折叠：details 只做逻辑容器，展开后排版与原来完全一致 ---- */
.folded{padding-top:var(--s4)}
.audit-fold{margin:0}
.audit-fold>summary{
  display:flex; align-items:center; gap:var(--s2); flex-wrap:wrap; list-style:none;
  padding:var(--s3) var(--s4); margin:0 0 var(--s3); cursor:pointer;
  background:var(--surface-2); border:1px solid var(--rule); border-radius:var(--r2);
  font-family:var(--fu); font-size:var(--fs-mid); font-weight:700; color:var(--ink);
}
.audit-fold>summary::-webkit-details-marker{display:none}
.audit-fold>summary::before{content:"+"; font-family:var(--fm); font-size:19px;
  font-weight:400; color:var(--accent-ink); line-height:1}
.audit-fold[open]>summary::before{content:"\\2212"}
.audit-fold[open]>summary{margin-bottom:var(--s5)}
.fold-t{flex:1}
.fold-hint{font-family:var(--fm); font-size:var(--fs-xs); font-weight:400; color:var(--faint)}
.audit-fold>p{margin-bottom:var(--s4)}
.audit-fold h3:first-child{margin-top:0}
@media print{
  .audit-fold>summary{display:none !important}
  .rise{opacity:1 !important; transform:none !important}
}
</style>
</head>
<body__BODYCLASS__>
<a class="skip" href="#main">跳到正文</a>
<div class="grain" aria-hidden="true"></div>
<div class="progress" id="progress" aria-hidden="true"></div>

<header class="topbar" data-no-print>
  <div class="tb-in">
    <span class="tb-brand"><span class="tbb-long">AI 免费内容与权益速递</span><span class="tbb-short">AI 速递</span><b>#__ISSUE_BADGE__</b></span>
    <nav class="tb-nav" id="topnav" aria-label="章节导航">__NAV__</nav>
    <div class="tb-tools">
      <button class="iconbtn" id="searchBtn" type="button" aria-label="全文检索" aria-expanded="false">\u2315</button>
      <div class="search">
        <span class="si" aria-hidden="true">\u2315</span>
        <input id="q" type="search" placeholder="全文检索…" aria-label="全文检索" autocomplete="off">
        <span class="sc"><span id="qn">0</span><button id="qprev" type="button" aria-label="上一个">\u2191</button><button id="qnext" type="button" aria-label="下一个">\u2193</button></span>
      </div>
      <button class="iconbtn" id="menuBtn" type="button" aria-label="打开目录" aria-expanded="false">\u2261</button>
      <button class="iconbtn" id="themeBtn" type="button" aria-label="切换明暗主题">\u25D1</button>
    </div>
  </div>
</header>

<header class="masthead">
  <span class="mh-num" aria-hidden="true">__MH_NUM__</span>
  <div class="mh-top">
    <span>AI 免费内容与权益速递 · __ISSUE_LINE__</span>
    <span>__DATEBLOCK__</span>
  </div>
  <div class="mh-rule" aria-hidden="true"></div>
  <h1 class="mh-t">__TITLE__</h1>
  <p class="mh-sub">__THEME__</p>
  <div class="pubnote">__NOTE__</div>
  __VIEWSWITCH__
</header>

<div class="shell__SHELLCLASS__">
__RAILBLOCK__
  <main id="main">
__BODY__
  </main>
</div>

<footer class="foot">
  <div class="fr"><span>AI 免费内容与权益速递 · __ISSUE_LINE__</span><span>__DATELINE__</span></div>
  <p><strong>网页版说明：</strong>本页由同名 Markdown 日报自动编译，正文一字未改。顶部可按章节跳转、可全文检索；<strong>第四章「限时活动与截止时间表」自 047 期修订起移到正文之后</strong>（前面九章可连贯读完，不再被大表截断），其 4.1 限时表支持按状态筛选（必办 / 今明换挡 / 生效中 / 口径存疑 / 已结束）；<strong>没有确切截止日的常驻权益不再逐期重印</strong>，全量在 <a href="standing.html">《常驻权益总账》</a>（同样可筛选）；表里超过 4 行的长条目<strong>点一下即可展开全文</strong>；右上角可切换明暗主题；直接打印会输出 A4 版式。</p>
  <p><strong>免责：</strong>所有额度、活动与截止时间以各平台官方页面实时公示为准。免费档多属公测、限时活动或内测，随时可能调整、限速或下线。本页不构成付款建议。</p>
</footer>

<div class="fab" data-no-print>
  <button class="iconbtn" id="topBtn" type="button" aria-label="回到顶部">\u2191</button>
</div>

<script>
(function(){
  "use strict";
  var root=document.documentElement, main=document.getElementById("main");

  /* ---------- 主题 ---------- */
  var themeBtn=document.getElementById("themeBtn");
  themeBtn.addEventListener("click",function(){
    var t=root.getAttribute("data-theme")==="dark"?"light":"dark";
    root.setAttribute("data-theme",t);
    try{localStorage.setItem("aihs-theme",t);}catch(e){}
  });

  /* ---------- 章节高亮 ---------- */
  var secs=[].slice.call(document.querySelectorAll("main .sec")),
      navA=[].slice.call(document.querySelectorAll("#topnav a")),
      tocA=[].slice.call(document.querySelectorAll(".toc-a"));
  function sync(id){
    navA.forEach(function(a){a.classList.toggle("active",a.getAttribute("href")==="#"+id);});
    tocA.forEach(function(a){a.classList.toggle("active",a.getAttribute("href")==="#"+id);});
  }

  /* ---------- 阅读进度 + 章节高亮（确定性：取最后一个越过阈值的章节） ---------- */
  var bar=document.getElementById("progress"), ticking=false;
  function syncNow(){
    var cur=secs.length?secs[0].id:null;
    for(var i=0;i<secs.length;i++){
      if(secs[i].getBoundingClientRect().top<=150) cur=secs[i].id; else break;
    }
    if(cur) sync(cur);
  }
  function onScroll(){
    if(ticking) return; ticking=true;
    requestAnimationFrame(function(){
      var h=document.documentElement.scrollHeight-window.innerHeight;
      bar.style.width=(h>0?Math.min(100,(window.scrollY/h)*100):0)+"%";
      syncNow();
      ticking=false;
    });
  }
  window.addEventListener("scroll",onScroll,{passive:true});
  window.addEventListener("resize",onScroll);
  onScroll();

  /* ---------- 入场 ---------- */
  var rise=[].slice.call(document.querySelectorAll("main .tblwrap, main .ol, h3, .summary .ul"));
  rise.forEach(function(el,i){ el.classList.add("rise"); el.style.transitionDelay=(Math.min(i,14)*55)+"ms"; });
  if(window.IntersectionObserver && !window.matchMedia("(prefers-reduced-motion: reduce)").matches){
    var io2=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add("in"); io2.unobserve(e.target); } });
    },{rootMargin:"0px 0px -8% 0px", threshold:.05});
    rise.forEach(function(el){io2.observe(el);});
    requestAnimationFrame(function(){
      rise.forEach(function(el){
        var r=el.getBoundingClientRect();
        if(r.top<window.innerHeight*.95) el.classList.add("in");
      });
    });
  } else { rise.forEach(function(el){el.classList.add("in");}); }

  /* ---------- 截止时间表：按状态筛选 ---------- */
  var ledger=document.querySelector(".tbl.ledger");
  if(ledger){
    var rows=[].slice.call(ledger.querySelectorAll("tbody tr[data-st]")),
        chips=[].slice.call(document.querySelectorAll(".chip")),
        cnt=document.getElementById("ledgerCount"),
        counts={all:rows.length}, filter="all";
    rows.forEach(function(r){var s=r.getAttribute("data-st"); counts[s]=(counts[s]||0)+1;});
    document.querySelectorAll("[data-c]").forEach(function(b){
      var k=b.getAttribute("data-c"); b.textContent=(counts[k]||0);
    });
    function apply(){
      var shown=0;
      rows.forEach(function(r){
        var ok=(filter==="all"||r.getAttribute("data-st")===filter);
        r.hidden=!ok; if(ok) shown++;
      });
      cnt.textContent="显示 "+shown+" / "+rows.length+" 条";
    }
    chips.forEach(function(c){
      c.addEventListener("click",function(){
        filter=c.getAttribute("data-f");
        chips.forEach(function(x){
          var on=(x===c); x.classList.toggle("on",on); x.setAttribute("aria-pressed",on?"true":"false");
        });
        apply();
      });
    });
    apply();
  }

  /* ---------- 长状态格：点击展开全文 ---------- */
  [].slice.call(document.querySelectorAll(".st-txt.cbody.clamp")).forEach(function(el){
    el.setAttribute("tabindex","0");
    el.setAttribute("role","button");
    el.setAttribute("aria-expanded","false");
    function open(){
      el.classList.remove("clamp");
      el.setAttribute("aria-expanded","true");
      el.removeAttribute("title");
    }
    el.addEventListener("click", open);
    el.addEventListener("keydown", function(ev){
      if(ev.key==="Enter"||ev.key===" "){ ev.preventDefault(); open(); }
    });
  });

  /* ---------- 全文检索 ---------- */
  var q=document.getElementById("q"), qn=document.getElementById("qn"),
      marks=[], cur=-1, lastQ="";
  function clearMarks(){
    marks.forEach(function(m){
      var p=m.parentNode; if(!p) return;
      p.replaceChild(document.createTextNode(m.textContent),m); p.normalize();
    });
    marks=[]; cur=-1;
  }
  function paint(){
    clearMarks();
    var v=q.value.trim();
    qn.textContent="0";
    if(v.length<1){ lastQ=""; return; }
    var walk=document.createTreeWalker(main,NodeFilter.SHOW_TEXT,{acceptNode:function(n){
      if(!n.nodeValue || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
      var p=n.parentNode; if(!p) return NodeFilter.FILTER_REJECT;
      if(/^(SCRIPT|STYLE|MARK|INPUT|BUTTON|CODE|svg|path)$/.test(p.nodeName)) return NodeFilter.FILTER_REJECT;
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
        m.className="hl"; m.textContent=val.slice(i,i+v.length);
        marks.push(m); frag.appendChild(m);
        last=i+v.length; i=low.indexOf(lv,last);
      }
      if(last<val.length) frag.appendChild(document.createTextNode(val.slice(last)));
      node.parentNode.replaceChild(frag,node);
    });
    qn.textContent=marks.length;
    /* 折叠区内的命中也要看得见：命中即展开所在章节（toggle 事件会补做入场动画与顶栏量高） */
    marks.forEach(function(m){
      var d=m.closest?m.closest("details.audit-fold"):null;
      if(d) d.open=true;
    });
    if(marks.length){ cur=-1; jump(1); }
    lastQ=v;
  }
  function jump(d){
    if(!marks.length) return;
    if(cur>=0 && marks[cur]) marks[cur].classList.remove("cur");
    cur=(cur+d+marks.length)%marks.length;
    var el=marks[cur]; el.classList.add("cur");
    el.scrollIntoView({block:"center", behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});
  }
  var timer=null;
  q.addEventListener("input",function(){ clearTimeout(timer); timer=setTimeout(paint,140); });
  q.addEventListener("keydown",function(e){
    if(e.key==="Enter"){ e.preventDefault(); jump(e.shiftKey?-1:1); }
    if(e.key==="Escape"){ q.value=""; paint(); }
  });
  document.getElementById("qnext").addEventListener("click",function(){jump(1);});
  document.getElementById("qprev").addEventListener("click",function(){jump(-1);});

  /* ---------- 手机端搜索条：<=600px 时搜索收成一个图标，点开成全宽搜索栏 ---------- */
  var sBtn=document.getElementById("searchBtn");
  function closeSearch(){
    document.body.classList.remove("search-open");
    sBtn.textContent="\u2315";
    sBtn.setAttribute("aria-expanded","false");
  }
  sBtn.addEventListener("click",function(){
    var open=document.body.classList.toggle("search-open");
    sBtn.textContent=open?"\u2715":"\u2315";
    sBtn.setAttribute("aria-expanded",open?"true":"false");
    if(open) q.focus();
  });
  document.addEventListener("keydown",function(e){
    /* 输入框内的 Esc 交给上面那段处理（只清空，不关面板） */
    if(e.key==="Escape" && document.body.classList.contains("search-open") && document.activeElement!==q) closeSearch();
  });

  /* ---------- 量顶栏与筛选条的实际高度写回 CSS 变量 ----------
     --tb-h 决定抽屉从哪开始、锚点跳转留多少空；--chips-h 决定截止表表头吸在哪。
     两者都随字号与是否换行变化，写死数值迟早对不上。 */
  function syncMetrics(){
    var tb=document.querySelector(".topbar"), ch=document.querySelector(".chips");
    if(tb) root.style.setProperty("--tb-h", tb.offsetHeight+"px");
    if(ch) root.style.setProperty("--chips-h", ch.offsetHeight+"px");
  }
  syncMetrics();
  window.addEventListener("resize",syncMetrics);
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(syncMetrics);

  /* ---------- 移动端目录 ---------- */
  var menuBtn=document.getElementById("menuBtn");
  menuBtn.addEventListener("click",function(){
    var open=document.body.classList.toggle("nav-open");
    menuBtn.setAttribute("aria-expanded",open?"true":"false");
  });
  document.querySelectorAll(".toc-a, #topnav a").forEach(function(a){
    a.addEventListener("click",function(){
      document.body.classList.remove("nav-open");
      menuBtn.setAttribute("aria-expanded","false");
    });
  });
  document.addEventListener("keydown",function(e){
    if(e.key==="Escape" && document.body.classList.contains("nav-open")){
      document.body.classList.remove("nav-open");
      menuBtn.setAttribute("aria-expanded","false");
    }
  });
  /* 点击正文区收起抽屉 */
  main.addEventListener("click",function(){
    if(document.body.classList.contains("nav-open")){
      document.body.classList.remove("nav-open");
      menuBtn.setAttribute("aria-expanded","false");
    }
  });

  /* ---------- 审计层折叠：全部展开 / 目录跳转 / 搜索 / 打印 ----------
     折叠区在 display:none 里时，IntersectionObserver 不会给 .rise 加 .in，
     顶栏量高也会把隐藏的 .chips 读成 0 —— 展开时两样都要补做。 */
  var folds=[].slice.call(document.querySelectorAll("details.audit-fold"));
  function openFold(id){ folds.forEach(function(d){ if(!id||d.id==="fold-"+id) d.open=true; }); }
  document.querySelectorAll("[data-open]").forEach(function(a){
    a.addEventListener("click",function(){ openFold(a.getAttribute("data-open")); });
  });
  document.querySelectorAll(".toc-a, #topnav a").forEach(function(a){
    a.addEventListener("click",function(){
      var h=a.getAttribute("href")||"";
      if(/^#s\\d{2}$/.test(h)) openFold(h.slice(1));
    });
  });
  var foldAll=document.getElementById("foldAll");
  if(foldAll) foldAll.addEventListener("click",function(){
    var allOpen=folds.every(function(d){return d.open;});
    folds.forEach(function(d){ d.open=!allOpen; });
    foldAll.textContent=allOpen?"展开全部章节":"收起全部章节";
    foldAll.setAttribute("aria-expanded",allOpen?"false":"true");
  });
  folds.forEach(function(d){
    d.addEventListener("toggle",function(){
      if(!d.open) return;
      d.querySelectorAll(".rise:not(.in)").forEach(function(el){el.classList.add("in");});
      syncMetrics();
    });
  });
  var printState=[];
  window.addEventListener("beforeprint",function(){
    printState=folds.map(function(d){return d.open;});
    folds.forEach(function(d){d.open=true;});
    document.querySelectorAll(".audit-fold .rise:not(.in)").forEach(function(el){el.classList.add("in");});
  });
  window.addEventListener("afterprint",function(){
    folds.forEach(function(d,i){ d.open=printState[i]; });
  });

  /* ---------- 回到顶部 ---------- */
  document.getElementById("topBtn").addEventListener("click",function(){
    window.scrollTo({top:0,behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});
  });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
