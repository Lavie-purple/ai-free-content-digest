# -*- coding: utf-8 -*-
"""明暗皮肤切换 —— 极速视图 / 往期总目录共用（第三件共享件，前两件是 viewswitch / datebadge）

为什么要有这个文件
------------------
2026-11-23 用户问「极速视图为什么不像是完整日报、常驻台账，没有了皮肤切换的按钮的？」。
答案不是功能缺失，是**入口缺失**：极速页与目录页只有 `@media (prefers-color-scheme:dark)`，
跟着系统走，读者自己没法切。日报 / 总账 / 附录（build_web.py）一直有右上角那枚 ◑。

四条纪律（改这里之前先读完）
----------------------------
1. **localStorage 键必须是 `aihs-theme`** —— 与 build_web.py 内联的那份相同。
   键不同 = 在日报里选了暗色，点回极速页又变亮，读者会以为设置丢了。
2. **防闪烁脚本必须内联在 <style> 之前**：外链或放到 body 末尾都会先画一帧亮色再翻黑，
   夜里刺眼。所以它以 ${...} 占位符进模板，位置不能挪到样式之后。
3. **只许用各页都有的 CSS 变量**（--muted / --accent / --accent-ink / --rule / --fm）。
   这里写的样式会被注入到三种不同模板里，用一个某页没有的变量就会静默变透明。
4. **图标固定 U+25D1「◑」**，与日报顶栏那枚同字符 —— 跨页认的是同一个记号。

⚠️ build_web.py 里有一份等价的内联实现（`#themeBtn` + `aihs-theme`）。
   改这里的行为（换键名、换图标、改存值格式）必须同步那边，否则两套皮肤记忆会打架。
   `check_views.py` 第 8 项就是用来抓这种漂移的。
"""

KEY = "aihs-theme"
ICON = "\u25d1"

# 内联在 <head> 里、<style> 之前。
# 与 build_web.py 那份的差别：这里对 localStorage 的值做了 light/dark 白名单 ——
# 存过脏值（改键名、手工改坏）时不会把 data-theme 设成非法值而退化成无样式。
# 白名单同时让「没存过」与「存了脏值」都回落到系统偏好，行为比原来的 `if(!t)` 更稳。
HEAD_JS = """<script>
/* 防闪烁：先定主题，再渲染（与日报页共用 localStorage 键 %(key)s） */
(function(){try{
  var t=localStorage.getItem("%(key)s");
  if(t!=="light"&&t!=="dark"){
    t=window.matchMedia&&window.matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light";
  }
  document.documentElement.setAttribute("data-theme",t);
}catch(e){}})();
</script>""" % {"key": KEY}

CSS = """.themebtn{
  /* 定成固定小方块而不是靠 padding 撑：◑ 在等距字体里的实际字宽不到 1em，
     用 padding 算出来的框会变成竖长条（页脚那枚实测如此）。固定宽高 + 居中一劳永逸。 */
  display:inline-flex; align-items:center; justify-content:center;
  width:27px; height:24px; padding:0;
  font-family:var(--fm); font-size:13px; line-height:1; letter-spacing:0;
  color:var(--muted); background:transparent;
  border:1px solid var(--rule-2); border-radius:3px;
  cursor:pointer; text-transform:none;
  /* 页头那行字只有 11.5px，按钮若同号会小到像标点；独立成 13px + 描边才读得出「可以点」 */
  transition:color .16s,border-color .16s,background .16s;
}
.themebtn:hover{color:var(--accent-ink); border-color:var(--accent); background:var(--accent-soft)}
.themebtn:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
@media print{.themebtn{display:none !important}}
"""


def button(extra_class="", bid="themeBtn"):
    """页头那枚按钮。aria-pressed 由 JS 按当前状态改写。

    bid=None 时不写 id —— 同一页可能有第二枚（极速视图页脚那枚），
    重复 id 不合法；脚本靠 `.themebtn` 类选择器，能同时绑上两枚。
    """
    cls = "themebtn" + (" " + extra_class if extra_class else "")
    idattr = ' id="%s"' % bid if bid else ""
    return (
        '<button class="%s"%s type="button" '
        'aria-label="切换明暗主题" aria-pressed="false" title="切换明暗主题">%s</button>'
        % (cls, idattr, ICON)
    )


# 放在 </body> 之前。没有按钮的页面会静默跳过（不报错），
# 这样脚本可以无脑塞进所有模板而不必逐页判断。
# 用 querySelectorAll 而不是 getElementById：将来在页脚补第二枚按钮时零改动，
# 两枚的状态（aria-pressed / title）会自动保持一致。
JS = """<script>
(function(){
  var root=document.documentElement;
  var btns=Array.prototype.slice.call(document.querySelectorAll(".themebtn"));
  if(!btns.length) return;
  function paint(){
    var dark=root.getAttribute("data-theme")==="dark";
    btns.forEach(function(b){
      b.setAttribute("aria-pressed", dark?"true":"false");
      b.setAttribute("title", dark?"当前暗色，点击切到亮色":"当前亮色，点击切到暗色");
    });
  }
  btns.forEach(function(b){
    b.addEventListener("click",function(){
      var t=root.getAttribute("data-theme")==="dark"?"light":"dark";
      root.setAttribute("data-theme",t);
      try{localStorage.setItem("%s",t);}catch(e){}
      paint();
    });
  });
  paint();
})();
</script>""" % KEY


def dark_block(dark_vars):
    """把一段暗色变量声明包成「手动主题 + 系统兜底」两条选择器。

    为什么要两条：
      - `html[data-theme="dark"]`  —— 手动切换（读者点了按钮）
      - `@media ... html:not([data-theme])` —— 内联脚本没跑起来时（CSP / JS 关闭）
        仍然跟随系统。脚本正常时总会在渲染前写 data-theme，所以这条只会兜底。
    传进来的 dark_vars 是 `--bg:#14120e; --surface:#1b1813; ...` 这样的纯声明串。
    """
    body = dark_vars.strip()
    # 按分号拆成单条声明再统一缩进 —— 调用处可以写成多行自然文本，
    # 不必手工维护缩进（本函数会把换行折平）。
    decls = [d.strip() for d in body.replace("\n", " ").split(";") if d.strip()]
    body = "\n".join("  %s;" % d for d in decls)
    return (
        'html[data-theme="dark"]{\n%s\n}\n'
        "@media (prefers-color-scheme:dark){\n"
        "  /* 兜底：内联脚本未执行时不至于整页亮白 */\n"
        "  html:not([data-theme]){\n%s\n  }\n}\n" % (body, body)
    )


def check(html):
    """出口自检：页面必须有按钮、有 JS、有防闪烁脚本，否则返回错误串。"""
    errs = []
    if 'id="themeBtn"' not in html:
        errs.append("缺皮肤切换按钮 #themeBtn")
    if KEY not in html:
        errs.append("缺 localStorage 键 %s（防闪烁脚本没进页面）" % KEY)
    if "data-theme" not in html:
        errs.append("缺 data-theme（暗色变量不会生效）")
    return "；".join(errs)
