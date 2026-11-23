# -*- coding: utf-8 -*-
"""页头日期标识：一眼看出「这个网页是哪一天的」。

为什么要有这个组件（2026-11-23 用户反馈）
------------------------------------------
用户原话：「目前网页好像缺少了标识 本次网页是哪一天的……因为内容太多繁杂
一下子找不到」。实际状况是日期**到处都有、但都藏在边角**：

  · 完整日报：刊头右上角一行小字「扫描截止 2026-11-23 19:09（GMT+8）」，
    夹在 `mh-top` 那个 11px 的等宽小字行里，还要跟主题句挤在一行；
  · 极速视图（= 站点首页）：首屏**完全没有日期**，只有页脚倒数第二段写着
    「本页基准日 2026-11-23」——要滚到底才看得到；
  · 常驻总账：只有「逐期复核 · 原文照搬」，根本没有「哪天复核的」。

所以问题不是「没写日期」，是**日期不在读者第一眼扫的位置**。
修法不是把某处字号调大，而是在页头固定加一条日期条：大字日期 + 星期 +
期号 + 数据截至时刻，五页同一位置、同一外观。

口径纪律（改这个组件前先读）
----------------------------
1. **大日期只从源文件里已核实的日期取**，绝不在构建时打 `today()` ——
   那会让每次重建都改字节，破坏幂等，也会让往期页面被重建成「今天」。
2. **`data-date` 属性是守卫的锚点**（`check_views.py` 用它断言「页面上写的
   日期 == 最新一期日期」）。改 HTML 结构时这个属性必须保留。
3. **极速页页脚的「本页基准日」那句话不能删** —— `check_site_freshness.py`
   拿它做锚点。日期条是「加」，不是「换」。
4. 只用两个模板都定义了的 CSS 变量（--rule / --surface / --ink / --ink-2 /
   --faint / --accent / --accent-ink），不用 --s4 / --fs-xs 这类只有日报
   模板才有的变量。
"""

import datetime
import re

WD = ("周一", "周二", "周三", "周四", "周五", "周六", "周日")


def parse(date):
    """'2026-11-23' -> date；解不出返回 None（调用方据此跳过整块，不留空壳）。"""
    m = re.match(r"\s*(\d{4})-(\d{2})-(\d{2})", date or "")
    if not m:
        return None
    try:
        return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def render(date, issue=None, note=None, label="本页日期"):
    """渲染日期条。date 取不到就返回空串（宁可没有，也不写错的日期）。"""
    dt = parse(date)
    if not dt:
        return ""
    iso = dt.isoformat()
    y, mo, da = iso.split("-")
    bits = []
    if issue:
        bits.append("第 %s 期" % issue)
    if note:
        bits.append(note)
    meta = '<span class="db-meta">%s</span>' % " · ".join(bits) if bits else ""
    return (
        '<div class="db" data-date="%s" role="note" aria-label="本页对应的日期">'
        '<span class="db-flag">%s</span>'
        '<span class="db-date">%s<em>年</em>%d<em>月</em>%d<em>日</em></span>'
        '<span class="db-wd">%s</span>%s</div>'
        % (iso, label, y, int(mo), int(da), WD[dt.weekday()], meta)
    )


def check(html, date):
    """守卫用：页面上确实有日期条，且写的就是 date。返回错误列表。"""
    err = []
    m = re.search(r'<div class="db" data-date="([^"]+)"', html)
    if not m:
        return ["缺页头日期条（<div class=\"db\" data-date=…>）"]
    if m.group(1) != date:
        err.append("页头日期条写的是 %s，应为 %s" % (m.group(1), date))
    if 'class="db-date"' not in html:
        err.append("日期条缺 .db-date（日期没渲染出来，只剩个空框）")
    return err


# 五页共用。别改成分页面各写一套 —— 同一个组件在五个页面长相不同，
# 就会有人以为「这一页不是同一份刊物」。
CSS = """
.db{
  display:flex; align-items:baseline; flex-wrap:wrap; gap:6px 12px;
  margin:16px 0 0; padding:9px 14px 10px;
  border:1px solid var(--rule); border-left:5px solid var(--accent);
  background:var(--surface);
}
.db-flag{
  font-size:10.5px; font-weight:600; letter-spacing:.16em; color:var(--accent-ink);
  /* 只描边、不填色：填色块会跟顶栏那个同样用 --accent-soft 的「当前章节」标签撞脸，
     读者会以为这个标签也能点。 */
  border:1px solid currentColor; padding:1px 6px 2px; align-self:center;
  white-space:nowrap;
}
.db-date{
  font-size:23px; font-weight:800; line-height:1.15; letter-spacing:.01em;
  color:var(--ink); font-variant-numeric:tabular-nums;
}
.db-date em{
  font-style:normal; font-weight:500; font-size:13px; color:var(--faint);
  margin:0 2px;
}
.db-wd{font-size:13.5px; font-weight:600; color:var(--ink-2); white-space:nowrap}
.db-meta{
  margin-left:auto; font-size:11.5px; color:var(--faint);
  line-height:1.6; text-align:right;
}
@media (max-width:640px){
  .db{padding:8px 11px 9px; gap:4px 9px; margin-top:13px}
  .db-date{font-size:19px}
  .db-flag{font-size:9.5px; letter-spacing:.12em}
  /* 窄屏别把附注挤成右对齐的孤行：整行落到日期下面，左对齐 */
  .db-meta{margin-left:0; width:100%; text-align:left; font-size:11px}
}
@media print{
  /* 打印件上「这是哪一天」比什么都重要，不许被 @media print 里的隐藏规则带走 */
  .db{display:flex !important; break-inside:avoid}
}
"""
