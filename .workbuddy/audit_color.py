# -*- coding: utf-8 -*-
"""配色量化审计：直接读 build_web.py 里的令牌，算三件事——
   ① 语义色之间的色距（查「两个不同语义其实用了同一个颜色」）
   ② WCAG 对比度（查小字 / 弱化文字是否达标）
   ③ 整行 opacity 叠加后，实际对比度被拉到多少

用法：python .workbuddy/audit_color.py [build_web.py 路径]
"""
import io
import os
import re
import sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = os.path.join(WS, ".workbuddy", "build_web.py")

# 语义上必须能互相区分的令牌（品牌强调色 vs 五个状态色）
SEM = ["accent", "accent-ink", "crit", "soon", "live", "plan", "over"]

# (显示名, 前景令牌, 背景令牌, AA 要求)
PAIRS = [
    ("正文 ink-2", "ink-2", "surface", 4.5),
    ("弱化 muted", "muted", "surface", 4.5),
    ("最弱 faint", "faint", "surface", 4.5),
    ("faint on bg", "faint", "bg", 4.5),
    ("muted on bg", "muted", "bg", 4.5),
    ("标题 ink", "ink", "bg", 4.5),
    ("强调 accent", "accent", "surface", 4.5),
    ("accent-ink", "accent-ink", "surface", 4.5),
    ("状态 live", "live", "surface", 4.5),
    ("状态 soon", "soon", "surface", 4.5),
    ("状态 crit", "crit", "surface", 4.5),
    ("状态 plan", "plan", "surface", 4.5),
    ("状态 over", "over", "surface", 4.5),
]


def rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(c):
    def f(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def cr(fg, bg):
    L1, L2 = lum(fg), lum(bg)
    if L1 < L2:
        L1, L2 = L2, L1
    return (L1 + 0.05) / (L2 + 0.05)


def mix(fg, bg, a):
    return tuple(round(a * f + (1 - a) * b) for f, b in zip(fg, bg))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    css = io.open(path, encoding="utf-8").read()
    i1 = css.index(":root{")
    i2 = css.index('html[data-theme="dark"]{')
    i3 = css.index("@media print{")

    def tok(a, b):
        d = {}
        for m in re.finditer(r"--([a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{3,6})\s*;", css[a:b]):
            d[m.group(1)] = m.group(2)
        return d

    themes = [("亮色", tok(i1, i2)), ("暗色", tok(i2, i3))]

    print("=" * 78)
    print("① 语义色色距（欧氏距离；<40 基本无法区分，=0 即完全同色）")
    print("=" * 78)
    bad = 0
    for name, t in themes:
        print("-- %s主题 --" % name)
        for i in range(len(SEM)):
            for j in range(i + 1, len(SEM)):
                a, b = SEM[i], SEM[j]
                if a not in t or b not in t:
                    continue
                d = sum((x - y) ** 2 for x, y in zip(rgb(t[a]), rgb(t[b]))) ** 0.5
                if d < 40:
                    flag = "  <<< 完全相同" if d == 0 else "  <<< 几乎无法区分"
                    bad += 1
                    print("   %-10s%s  vs  %-10s%s   距离 %6.1f%s" % (a, t[a], b, t[b], d, flag))
        print()

    print("=" * 78)
    print("② WCAG 对比度（AA：正文 4.5 / 大字 3.0）")
    print("=" * 78)
    for name, t in themes:
        print("-- %s主题 --" % name)
        for label, fk, bk, need in PAIRS:
            if fk not in t or bk not in t:
                continue
            v = cr(rgb(t[fk]), rgb(t[bk]))
            mark = "OK      " if v >= need else ("小字不足" if v >= 3.0 else "不足    ")
            print("   %-14s %s on %s   对比度 %5.2f   [%s]" % (label, t[fk], t[bk], v, mark))
        print()

    print("=" * 78)
    print("③ 整行 opacity:.55（「已结束」行）叠加后的实际对比度")
    print("=" * 78)
    for name, t in themes:
        fg, bg = rgb(t["over"]), rgb(t["surface"])
        eff = mix(fg, bg, 0.55)
        print("   %s: %s 原对比度 %5.2f  ->  opacity .55 后 %s 对比度 %5.2f%s"
              % (name, t["over"], cr(fg, bg), eff, cr(eff, bg),
                 "   <<< 已低于可读线" if cr(eff, bg) < 3.0 else ""))
    print()


if __name__ == "__main__":
    main()
