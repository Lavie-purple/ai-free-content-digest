# -*- coding: utf-8 -*-
"""手机端截图：用 iframe 造窄视口，再截父页面。

为什么不能直接 --window-size=375
--------------------------------
Edge/Chrome 在 Windows 有 ~490px 的最小窗口宽度，设 375 会被静默抬到 489，
截出来根本不是手机版式（实测三档 320/375/414 的 clientWidth 全是 489）。
iframe 的宽度就是里面文档的 CSS 视口宽度，媒体查询按它求值——
所以一个 375px 宽的 iframe 就是一台 375px 的手机。

三条硬规矩（都实际踩过）
------------------------
① 先关入场动画。页面大量使用 animation:...both，起始 opacity:0，无头下会冻结在
   t=0，拍出来是「标题 + 正文整块空白」。
② 想看中段就在 iframe 内 scrollIntoView，**不要删兄弟节点**。删掉侧栏后栅格会塌，
   主内容掉进第 1 栏（196px），整页被挤成窄缝（实测 PNG 只有 15KB）。
③ 一图一个 --user-data-dir，截完比对 md5（全同 = 抓拍失败），再删掉 profile。

用法：
    python .workbuddy/snap_mobile.py            # 全部镜头
    python .workbuddy/snap_mobile.py 搜索 抽屉   # 只拍名字里含这些词的那些
"""
import hashlib
import io
import os
import subprocess
import sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = os.path.join(WS, ".workbuddy", "_shot")
OUTDIR = os.path.join(SHOT, "mobile")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

DEF = "AI免费内容与权益速递-"
WEB = os.path.join(WS, DEF + "第006期-2026-09-17.html")
IDX = os.path.join(WS, "index.html")

KILL = ("<style>*{animation:none!important;transition:none!important}"
        ".rise{opacity:1!important;transform:none!important}</style></head>")

WRAP = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;padding:0;background:#fff;overflow:hidden}
iframe{border:0;display:block;width:__W__px;height:__H__px;background:#fff}
</style></head><body>
<iframe id="fr" src="__SRC__"></iframe>
<script>
addEventListener("load",function(){
  setTimeout(function(){
    try{
      var d=document.getElementById("fr").contentDocument;
      __ACT__
    }catch(e){ document.title="ERR "+e.message; }
  },400);
});
</script></body></html>"""

W, H = 375, 812

# name, 源文件, 在 iframe 里执行的滚动/点击动作
#
# 滚动一律用「量出目标相对 iframe 视口的位置，再累加到 scrollTop」，
# 不用 scrollIntoView —— 后者在 iframe 里会被静默忽略（实测第 5 张和第 1 张字节完全相同）。
SCROLL = ("function to_(el,pad){ if(!el) return;"
          " var r=el.getBoundingClientRect();"
          " d.documentElement.scrollTop += r.top - (pad||120); }")

SHOTS = [
    ("日报-01-首屏", WEB, SCROLL),
    ("日报-02-搜索条展开", WEB, SCROLL + "d.getElementById('searchBtn').click();"),
    ("日报-03-目录抽屉", WEB, SCROLL + "d.getElementById('menuBtn').click();"),
    ("日报-04-两列表已堆叠", WEB, SCROLL + "to_(d.querySelectorAll('table.tbl')[0],140);"),
    ("日报-05-截止表与筛选条", WEB, SCROLL + "to_(d.getElementById('s04'),60);"),
    ("日报-06-截止表筛选必办", WEB,
     SCROLL + "to_(d.getElementById('s04'),60);"
     "var c=d.querySelector('.chip[data-f=crit]'); if(c) c.click();"),
    ("日报-07-宽表横滑首列粘住", WEB,
     SCROLL + "var t=d.querySelectorAll('table.tbl')[5]; to_(t,200);"
     "var w=t&&t.closest('.tblwrap'); if(w) w.scrollLeft=230;"),
    ("日报-08-页脚", WEB, SCROLL + "d.documentElement.scrollTop=1e6;"),
    ("首页-01-首屏", IDX, SCROLL),
    ("首页-02-往期列表", IDX, SCROLL + "d.documentElement.scrollTop=760;"),
    ("首页-03-页脚与说明", IDX, SCROLL + "d.documentElement.scrollTop=1e6;"),
]


def main():
    keys = sys.argv[1:]
    os.makedirs(OUTDIR, exist_ok=True)
    shots = [s for s in SHOTS if not keys or any(k in s[0] for k in keys)]
    if not shots:
        raise SystemExit("没有匹配的镜头")

    digests = []
    for name, src, act in shots:
        if not os.path.exists(src):
            print("! 缺文件 %s" % os.path.basename(src))
            continue
        body = io.open(src, encoding="utf-8").read()
        tgt = os.path.join(SHOT, "_s_probe.html")
        io.open(tgt, "w", encoding="utf-8").write(body.replace("</head>", KILL))
        wrap = os.path.join(SHOT, "_s_wrap.html")
        io.open(wrap, "w", encoding="utf-8").write(
            WRAP.replace("__W__", str(W)).replace("__H__", str(H))
                .replace("__SRC__", "_s_probe.html").replace("__ACT__", act))
        # 所有镜头共用一个 profile（截图是串行的，不会撞车）。
        # 早先的做法是「一图一个 profile，截完删掉」，但删除动作会被沙箱拦下，
        # 而且每个 profile 十几 MB、串行复用没有副作用。
        prof = os.path.join(SHOT, "_s_prof")
        png = os.path.join(OUTDIR, name + ".png")
        # --screenshot 的路径必须用正斜杠：反斜杠会被 shell 当转义，生成带字面量 $ 的垃圾文件
        subprocess.run(
            [EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--hide-scrollbars", "--allow-file-access-from-files",
             "--window-size=%d,%d" % (W + 140, H + 34),
             "--user-data-dir=" + prof, "--virtual-time-budget=9000",
             "--screenshot=" + png.replace("\\", "/"),
             "file:///" + wrap.replace("\\", "/")],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        if os.path.exists(png):
            digests.append((name, hashlib.md5(open(png, "rb").read()).hexdigest(),
                            os.path.getsize(png)))
        else:
            digests.append((name, "缺失", 0))

    print("产出 %d 张 -> %s" % (len(digests), OUTDIR))
    seen = {}
    for n, d, sz in digests:
        if d in seen:
            dup = "  <<< 与 %s 完全相同，抓拍可能失败" % seen[d]
        else:
            seen[d] = n
            dup = ""
        print("  %-28s %8d B  %s%s" % (n, sz, d[:12], dup))


if __name__ == "__main__":
    main()
