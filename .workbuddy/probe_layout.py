# -*- coding: utf-8 -*-
"""布局实测探针：把 DOM 指标写进 document.title，再用 --dump-dom 抓回来。
回答「表格列宽合理吗 / 搜索框装得下字吗 / 装饰元素压住文字了吗」这类
光看截图只能靠像素估算的问题。

用法：
    python .workbuddy/probe_layout.py [目标.html] [--widths 1440,560]
不传参自动取工作区里最新一期日报的 html。
"""
import io
import os
import re
import subprocess
import sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = os.path.join(WS, ".workbuddy", "_shot")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

PROBE = r"""
<script>addEventListener("load",function(){
  var o=[];
  o.push("页面 视口/文档宽 = "+document.documentElement.clientWidth+" / "+document.documentElement.scrollWidth
         + (document.documentElement.scrollWidth>document.documentElement.clientWidth ? "  [有横向溢出]" : "  [无横向溢出]"));
  // 逐张表量列宽。
  // 判断「首列过窄」不能只看宽度——# 序号列天然就是 41px。要看**内容需要多宽**：
  // 临时给首列单元格加 nowrap，量出 scrollWidth 即需求宽度，再算压缩比。
  var tbs=document.querySelectorAll("table.tbl");
  for(var t=0;t<tbs.length;t++){
    var ths=tbs[t].querySelectorAll("thead th"), w=[];
    for(var i=0;i<ths.length;i++){w.push(Math.round(ths[i].getBoundingClientRect().width));}
    var cells=tbs[t].querySelectorAll("tbody td:first-child");
    var mn=1e9, need=0, mh=0, samp="";
    for(var k=0;k<cells.length;k++){
      var c=cells[k], r=c.getBoundingClientRect();
      var ow=c.style.whiteSpace;
      c.style.whiteSpace="nowrap";
      if(c.scrollWidth>need){need=c.scrollWidth;}
      c.style.whiteSpace=ow;
      if(r.width<mn){mn=r.width; samp=c.textContent.replace(/\s+/g," ").trim().slice(0,14);}
      if(r.height>mh){mh=r.height;}
    }
    var ratio=need?(mn/need):1;
    var kind=tbs[t].className.indexOf("ledger")>=0?"截止表":"普通表";
    // 告警规则：列够窄(实宽<140px) + 行够高(>90px) + 首列是真文字(>=4字)，
    // 三条同时成立才算「被挤成逐字换行」。单看满足度会把「#」序号列和
    // 「抖音」这类短值列误报（它们列窄是合理的）。
    var alarm = mn < 140 && mh > 90 && samp.length >= 4;
    o.push("表"+(t+1)+" "+kind+(tbs[t].closest(".tblwrap.scrolly")?" [可滚动]":"")
           +" 列宽="+w.join("/")+"  表宽="+Math.round(tbs[t].getBoundingClientRect().width)
           +"  首列实宽="+(mn===1e9?"-":Math.round(mn))+"px 需求="+Math.round(need)+"px 满足度="+(ratio*100).toFixed(0)+"%"
           +"  首列最高="+(mh?Math.round(mh)+"px":"-")
           +(alarm?"   <<< 首列被压掉 "+Math.round((1-ratio)*100)+"%，中文逐字换行，例：["+samp+"]":""));
  }
  // 搜索框真正能显示多少字
  var si=document.querySelector(".search input");
  if(si){
    var cs=getComputedStyle(si);
    var u=Math.round(si.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight));
    o.push("搜索框 盒宽="+si.clientWidth+"px 左右内边距="+cs.paddingLeft+"/"+cs.paddingRight
           +"  可用文本宽="+u+"px"+("（约 "+(u/16).toFixed(1)+" 个中文字）")
           +(u<90?"   <<< 过窄，输入内容看不见":""));
  } else { o.push("搜索框 已隐藏（<=520px 断点）"); }
  // 装饰元素是否压住文字
  var n=document.querySelector(".mh-num"), top=document.querySelector(".mh-top");
  if(n&&top){
    var a=n.getBoundingClientRect();
    if(a.width===0){o.push("刊头大数字 已收起（不占位）");}
    else{
      var b=top.getBoundingClientRect();
      var ox=Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left));
      var oy=Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));
      o.push("刊头大数字 vs 元信息行 重叠="+Math.round(ox)+"x"+Math.round(oy)+"px"
             +(ox>0&&oy>0?"   <<< 压住文字":""));
    }
  }
  document.title="METRICS|"+o.join("||");
});</script>
"""


def pick_default():
    cands = []
    for fn in os.listdir(WS):
        m = re.match(r"^(AI免费内容与权益速递.*?(\d{4}-\d{2}-\d{2}))\.html$", fn)
        if m:
            cands.append((m.group(2), fn))
    if not cands:
        raise SystemExit("工作区里没找到日报 html，先跑 build_web.py")
    cands.sort()
    return os.path.join(WS, cands[-1][1])


def main():
    args = [a for a in sys.argv[1:]]
    widths = [1440, 560]
    if "--widths" in args:
        i = args.index("--widths")
        widths = [int(x) for x in args[i + 1].split(",")]
        del args[i:i + 2]
    src = args[0] if args else pick_default()
    if not os.path.isfile(src):
        raise SystemExit("找不到目标：" + src)

    os.makedirs(SHOT, exist_ok=True)
    body = io.open(src, encoding="utf-8").read()
    # 关掉入场动画，否则 animation:both 会把内容冻结在 opacity:0（截图全白的老坑）
    kill = "<style>*{animation:none!important;transition:none!important}.rise{opacity:1!important;transform:none!important}</style></head>"
    tmp = os.path.join(SHOT, "_probe.html")
    io.open(tmp, "w", encoding="utf-8").write(body.replace("</head>", kill).replace("</body>", PROBE + "</body>"))

    print("目标：%s" % os.path.basename(src))
    for w in widths:
        prof = os.path.join(SHOT, "_probe_%d" % w)
        r = subprocess.run(
            [EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--window-size=%d,1100" % w, "--user-data-dir=" + prof,
             "--virtual-time-budget=6000", "--dump-dom",
             "file:///" + tmp.replace("\\", "/")],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        m = re.search(r"<title>(METRICS\|.*?)</title>", r.stdout, re.S)
        print("\n" + "=" * 76)
        print("视口 %dpx" % w)
        print("=" * 76)
        if not m:
            print("  ! 指标抓取失败")
            continue
        for line in m.group(1)[len("METRICS|"):].split("||"):
            print("  " + line)
    print()


if __name__ == "__main__":
    main()
