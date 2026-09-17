# -*- coding: utf-8 -*-
"""移动端适配实测探针：量 DOM，不看截图。

为什么不能用 --window-size 直接测手机宽度
----------------------------------------
Edge/Chrome 在 Windows 上有**最小窗口宽度**（本机实测 ~490px）。把
--window-size 设成 320 / 375 / 414，三档都会被静默抬到 489px，量出来
的数字一模一样——看起来测了三档，其实一档都没测到。
--force-device-scale-factor 也救不了：它只改 devicePixelRatio，不改
CSS 视口宽度（实测 scale=2 + window=750 得到 clientWidth=720，仍是 720）。

本脚本的办法：把目标页塞进**指定宽度的 iframe**。媒体查询按 iframe 的
视口宽度求值，所以一个 320px 宽的 iframe 就是一个真正的 320px 视口。
父页面收集各 iframe postMessage 回来的指标，写进自己的 document.title，
再用 --dump-dom 抓回来。

检查项
------
1. 横向溢出（整页 + 逐元素，排除有意横滑的表格/顶栏导航）
2. 字号（正文 / 表格 / 摘要 / 说明 / 页脚）—— 低于 16px 的正文在手机上偏小
3. 触控目标（按钮、chip、导航项）—— 低于 40px 高不好点
4. 表格：表宽 vs 视口、需横滑多少、首列是否被压成逐字换行
5. 顶栏内容是否溢出、是否被压扁
6. 搜索框是否存在、可用文本宽
7. 刊头主标题占几行、装饰大数字是否压字
8. 长文段落的最大行宽（手机上行宽过短会频繁换行）

用法：
    python .workbuddy/probe_mobile.py [目标.html] [--widths 320,360,375,414]
                                      [--out 报告.txt]
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

# ---------------------------------------------------------------- 子页探针
PROBE = r"""
<script>
(function(){
  function fs(sel){
    var e=document.querySelector(sel);
    return e?Math.round(parseFloat(getComputedStyle(e).fontSize)*10)/10:null;
  }
  function lines(e){
    if(!e) return 0;
    var rg=document.createRange(); rg.selectNodeContents(e);
    var rs=rg.getClientRects(), top=null, n=0;
    for(var i=0;i<rs.length;i++){
      if(rs[i].width<=0||rs[i].height<=0) continue;
      if(top===null||rs[i].top-top>4){n++; top=rs[i].top;}
    }
    return n;
  }
  function run(){
    var de=document.documentElement, VW=de.clientWidth, o=[];
    var SW=de.scrollWidth;
    o.push("视口 "+VW+"px ｜ 文档宽 "+SW+(SW>VW+1?"  <<< 横向溢出 "+(SW-VW)+"px":"  [无横向溢出]"));

    /* --- 1. 逐元素找非预期溢出（有意横滑的容器不算） --- */
    var bad=[], all=document.querySelectorAll("body *");
    for(var i=0;i<all.length;i++){
      var e=all[i];
      if(e.closest(".tblwrap")||e.closest(".tb-nav")||e.closest(".drawerwrap")) continue;
      var r=e.getBoundingClientRect();
      if(r.width<=0||r.height<=0) continue;
      var cs=getComputedStyle(e);
      if(cs.position==="fixed") continue;
      if(r.right>VW+1){
        var cl=(typeof e.className==="string"&&e.className)?("."+e.className.split(/\s+/)[0]):"";
        bad.push(e.tagName.toLowerCase()+cl+"→"+Math.round(r.right));
      }
    }
    o.push("溢出元素 "+(bad.length? bad.length+" 个  <<< "+bad.slice(0,6).join(" / ") : "0 个"));

    /* --- 2. 字号（每个选择器单独取，不要写成一串逗号选择器——
           那样只会返回文档里第一个匹配的元素，读数会张冠李戴） --- */
    o.push("字号 摘要="+fs(".summary .ul li")+" 正文="+fs("main p, .lede")
           +" 卡片="+fs("ul.abs li")+" 表格="+fs(".tbl:not(.c2) tbody td")
           +" 堆叠表="+fs(".tbl.c2 tbody td")+" 说明="+fs(".pubnote p, .warn, footer")
           +" 按钮="+fs(".btn, .chip, .iconbtn"));

    /* --- 3. 触控目标（结构性可点区域；正文里的行内链接不算，天然又小又密） --- */
    var taps=[].slice.call(document.querySelectorAll(
      "button,.iconbtn,.chip,.btn,.tb-nav a,.rail a,ul.list li.row a")),
        n=0, sm=[];
    taps.forEach(function(e){
      var r=e.getBoundingClientRect();
      if(r.width<=0||r.height<=0) return;
      if(getComputedStyle(e).visibility==="hidden") return;
      n++;
      if(r.height<40||r.width<32){
        sm.push((e.textContent||e.getAttribute("aria-label")||"?").replace(/\s+/g," ").trim().slice(0,8)
                +" "+Math.round(r.width)+"x"+Math.round(r.height));
      }
    });
    o.push("触控目标 共 "+n+" 个，偏小 "+sm.length+" 个"
           +(sm.length? "  <<< "+sm.slice(0,6).join(" / ") : "  [均 >=40px 高]"));

    /* --- 4. 表格 --- */
    var tbs=document.querySelectorAll("table.tbl");
    for(var t=0;t<tbs.length;t++){
      var tb=tbs[t], wr=tb.closest(".tblwrap");
      var bw=Math.round(tb.getBoundingClientRect().width);
      var ths=tb.querySelectorAll("thead th"), w=[];
      for(var j=0;j<ths.length;j++) w.push(Math.round(ths[j].getBoundingClientRect().width));
      var tds=tb.querySelectorAll("tbody td:first-child"), mn=1e9, need=0, mh=0, samp="";
      for(var k=0;k<tds.length;k++){
        var c=tds[k], r2=c.getBoundingClientRect(), ow=c.style.whiteSpace;
        c.style.whiteSpace="nowrap"; if(c.scrollWidth>need) need=c.scrollWidth; c.style.whiteSpace=ow;
        if(r2.width<mn){mn=r2.width; samp=c.textContent.replace(/\s+/g," ").trim().slice(0,12);}
        if(r2.height>mh) mh=r2.height;
      }
      var ratio=need?(mn/need):1;
      var scrollable = wr && wr.scrollWidth > wr.clientWidth+1;
      var alarm = mn<140 && mh>130 && samp.length>=4 && ratio<0.9;
      var th0=tb.querySelector("thead");
      var stacked = !!(th0 && getComputedStyle(th0).display==="none");
      o.push("表"+(t+1)+(tb.classList.contains("ledger")?"[截止表]":"")+(stacked?"[已堆叠]":"")
             +" 表宽="+bw+(bw>VW+1?"(超视口 "+(bw-VW)+"px，需横滑)":"(不超视口)")
             +" 列宽="+w.join("/")
             +" 首列实宽="+(mn===1e9?"-":Math.round(mn))+" 需求="+Math.round(need)
             +" 满足度="+(ratio*100).toFixed(0)+"% 最高="+(mh?Math.round(mh)+"px":"-")
             +(scrollable?" [容器可横滑]":" [容器不可横滑]")
             +(alarm?"  <<< 首列被压 " + Math.round((1-ratio)*100) + "%，逐字换行："+samp:""));
    }

    /* --- 4b. 首列粘性：横滑时首列必须钉住，否则看不出这一行是哪一条 ---
           注意 .tbl 若带 overflow:hidden（常是为了裁圆角），它自己就成了滚动容器，
           td 的 sticky 会以它为参照而静默失效——所以这项必须实测，不能只看 CSS。 */
    var wst=null, tst=null, walls=document.querySelectorAll(".tblwrap");
    for(var z=0;z<walls.length;z++){
      var t2=walls[z].querySelector("table.tbl");
      if(t2 && !t2.classList.contains("c2") && walls[z].scrollWidth>walls[z].clientWidth+1){
        wst=walls[z]; tst=t2; break;
      }
    }
    if(wst){
      var td0=tst.querySelector("tbody td:first-child");
      if(td0){
        var csp=getComputedStyle(td0);
        var b0=td0.getBoundingClientRect().left, old0=wst.scrollLeft;
        wst.scrollLeft=120;
        var a0=td0.getBoundingClientRect().left;
        wst.scrollLeft=old0;
        var stuck=(csp.position==="sticky" && Math.abs(a0-b0)<2);
        o.push("首列粘性 position="+csp.position+" 横滑 120px 后 left "+Math.round(b0)+"→"+Math.round(a0)
               +(stuck?"  [粘住]":"  <<< 未粘住：横滑时首列会跟着滚走"));
      }
    } else {
      o.push("首列粘性 无需横滑的表，未检查");
    }

    /* --- 5. 顶栏 --- */
    var tb2=document.querySelector(".topbar");
    if(tb2){
      var ti=document.querySelector(".tb-in");
      o.push("顶栏 高="+Math.round(tb2.getBoundingClientRect().height)
             +" 内容宽="+Math.round(ti.scrollWidth)+" / 视口 "+VW
             +(ti.scrollWidth>VW+1?"  <<< 内容超出 (溢出 "+(ti.scrollWidth-VW)+"px)":"  [未溢出]"));
    }

    /* --- 6. 搜索框：手机上收成一个图标，点开才是全宽栏——必须模拟点开再量，
           否则会把它误判成「已隐藏 / 过窄」 --- */
    var si=document.querySelector(".search input"), sBtn2=document.getElementById("searchBtn");
    if(si){
      var boxW=si.clientWidth, opened=false;
      if(boxW<=0 && sBtn2 && getComputedStyle(sBtn2).display!=="none"){
        sBtn2.click(); opened=true; boxW=si.clientWidth;
      }
      if(boxW<=0){
        o.push("搜索框 不可用  <<< 既没显示、也没有可点开的入口");
      } else {
        var cs2=getComputedStyle(si);
        var u=Math.round(boxW-parseFloat(cs2.paddingLeft)-parseFloat(cs2.paddingRight));
        var fsz=parseFloat(cs2.fontSize);
        o.push("搜索框 "+(opened?"收成图标，点开后":"")+"盒宽="+boxW+"px 可用文本宽="+u
               +"px（约 "+(u/16).toFixed(1)+" 个中文字）"+(u<90?"  <<< 过窄":"")
               +" ｜ 字号="+cs2.fontSize+(fsz<16?"  <<< <16px，iOS 聚焦会自动放大整页":""));
      }
      if(opened) sBtn2.click();
    } else {
      o.push("搜索框 节点不存在");
    }

    /* --- 7. 刊头 --- */
    var h1=document.querySelector("h1.mh-t");
    if(h1) o.push("主标题 "+fs("h1.mh-t")+"px 占 "+lines(h1)+" 行");
    var num=document.querySelector(".mh-num");
    if(num){
      var a=num.getBoundingClientRect();
      if(a.width===0||getComputedStyle(num).display==="none") o.push("刊头大数字 已收起");
      else{
        var tg=[["元信息行",".mh-top"],["主标题","h1.mh-t"],["副题",".mh-sub"],["刊例说明",".pubnote"]], hits=[];
        function rects(e){
          var out=[], w2=document.createTreeWalker(e, NodeFilter.SHOW_TEXT, null), nd;
          while((nd=w2.nextNode())){
            if(!nd.nodeValue.replace(/\s+/g,"")) continue;
            var rg2=document.createRange(); rg2.selectNodeContents(nd);
            var rl=rg2.getClientRects();
            for(var q=0;q<rl.length;q++){ if(rl[q].width>0&&rl[q].height>0) out.push(rl[q]); }
          }
          return out;
        }
        for(var q2=0;q2<tg.length;q2++){
          var el=document.querySelector(tg[q2][1]); if(!el) continue;
          var rs=rects(el), hit=0;
          for(var m=0;m<rs.length;m++){
            var b=rs[m];
            var ox=Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left));
            var oy=Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));
            hit=Math.max(hit,Math.round(ox*oy));
          }
          if(hit>0) hits.push(tg[q2][0]+" 交集"+hit+"px2");
        }
        o.push("刊头大数字 "+Math.round(a.width)+"x"+Math.round(a.height)+"px"
               +(hits.length?"  <<< 压住文字 "+hits.join(" / "):"  [未压字]"));
      }
    }

    /* --- 8. 正文行宽 --- */
    var ps=[].slice.call(document.querySelectorAll("main p, .lede, .summary .ul li, ul.abs li")), mx=0, med=[];
    ps.forEach(function(e){
      var r=e.getBoundingClientRect();
      if(r.width>mx) mx=r.width;
      if(r.width>0) med.push(r.width);
    });
    if(med.length){
      med.sort(function(a,b){return a-b;});
      o.push("正文段落 共 "+med.length+" 段 最大宽="+Math.round(mx)+"px 中位宽="+Math.round(med[med.length>>1])+"px");
    }
    return o.join("||");
  }

  function post(){
    var t;
    try { t=run(); } catch(err){ t="探针异常："+err.message; }
    if(window.parent!==window){ try{ window.parent.postMessage({k:"M",w:window.innerWidth,txt:t},"*"); }catch(e){} }
    document.title="METRICS|"+t;
  }
  addEventListener("message",function(e){ if(e.data&&e.data.k==="GO") post(); });
  addEventListener("load",function(){ setTimeout(post,60); });
})();
</script>
"""

WRAP = """<!doctype html>
<html><head><meta charset="utf-8"><title>WAIT</title>
<style>
html,body{margin:0;background:#4a4a4a}
#host{display:flex;gap:14px;align-items:flex-start;padding:14px}
iframe{border:0;background:#fff;display:block;flex:0 0 auto}
</style></head>
<body><div id="host"></div>
<script>
var WIDTHS=__WIDTHS__;
var res={};
addEventListener("message",function(e){
  var d=e.data;
  if(d&&d.k==="M"){ res[d.w]=d.txt; }
});
addEventListener("load",function(){
  var host=document.getElementById("host");
  WIDTHS.forEach(function(w){
    var f=document.createElement("iframe");
    f.setAttribute("scrolling","no");
    f.style.width=w+"px"; f.style.height="2600px";
    f.src="__SRC__";
    f.onload=function(){ try{ f.contentWindow.postMessage({k:"GO",w:w},"*"); }catch(err){} };
    host.appendChild(f);
  });
  setTimeout(function(){
    document.title="METRICS|"+WIDTHS.map(function(w){
      return "W"+w+";;"+(res[w]||"（无回传）");
    }).join(";;");
  },4000);
});
</script></body></html>
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
    args = sys.argv[1:]
    widths = [320, 360, 375, 414]
    out = os.path.join(SHOT, "mobile_probe.txt")
    if "--widths" in args:
        i = args.index("--widths")
        widths = [int(x) for x in args[i + 1].split(",")]
        del args[i:i + 2]
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        del args[i:i + 2]
    src = args[0] if args else pick_default()
    if not os.path.isfile(src):
        raise SystemExit("找不到目标：" + src)

    os.makedirs(SHOT, exist_ok=True)
    body = io.open(src, encoding="utf-8").read()
    # 关掉入场动画，否则 animation:both 会把内容冻结在 opacity:0
    kill = ("<style>*{animation:none!important;transition:none!important}"
            ".rise{opacity:1!important;transform:none!important}</style></head>")
    tmp = os.path.join(SHOT, "_m_probe.html")
    io.open(tmp, "w", encoding="utf-8").write(
        body.replace("</head>", kill).replace("</body>", PROBE + "</body>"))

    wrap = os.path.join(SHOT, "_m_wrap.html")
    io.open(wrap, "w", encoding="utf-8").write(
        WRAP.replace("__WIDTHS__", "[" + ",".join(str(w) for w in widths) + "]")
            .replace("__SRC__", "_m_probe.html"))

    prof = os.path.join(SHOT, "_m_wrap_prof")
    r = subprocess.run(
        [EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--allow-file-access-from-files",
         "--window-size=1400,1000", "--user-data-dir=" + prof,
         "--virtual-time-budget=12000", "--dump-dom",
         "file:///" + wrap.replace("\\", "/")],
        capture_output=True, text=True, encoding="utf-8", errors="replace")

    m = re.search(r"<title>(METRICS\|.*?)</title>", r.stdout, re.S)
    lines = []
    lines.append("目标：%s" % os.path.basename(src))
    lines.append("")
    if not m:
        lines.append("! 指标抓取失败")
    else:
        payload = m.group(1)[len("METRICS|"):]
        parts = re.split(r"(?:^|;;)W(\d+);;", payload)
        if len(parts) < 3:
            lines.append("! 回传格式异常：%s" % payload[:200])
        for i in range(1, len(parts) - 1, 2):
            w, txt = parts[i], parts[i + 1]
            lines.append("=" * 76)
            lines.append("视口 %spx" % w)
            lines.append("=" * 76)
            for it in txt.split("||"):
                lines.append("  " + it)
            lines.append("")

    io.open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("报告 -> %s" % out)


if __name__ == "__main__":
    main()
