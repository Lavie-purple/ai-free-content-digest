# -*- coding: utf-8 -*-
"""062 期：指针链接化 + 附录当期段期号重贴。

两件事（061 期纪律⑥的延续）：
  ① 日报正文里的 `〔附录 062〕` -> `[附录 062](details.html)`；
  ② 《第四章表体明细附录.md》的 `## 第 062 期` 段内，把上期留下的 `[附录 061]` 重贴为 `[附录 062]`；
     历史段（第 049–061 期）一字不改。

**两处计数都从落盘文件实算，且对「命中 0 条」显式断言失败**（058 期：零命中不是通过，是没找到对象）。
"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第062期-2026-11-08.md"
APP = WS + "第四章表体明细附录.md"

# ---------- ① 正文 〔附录 062〕 ----------
md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
plain = md.count("〔附录 062〕")
assert plain > 0, "正文里一条 〔附录 062〕 都没有（没找到对象）"
md = md.replace("〔附录 062〕", "[附录 062](details.html)")
left = md.count("〔附录 062〕")
assert left == 0, ("仍有未链接化的指针", left)
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)
print("① 正文链接化：%d 处" % plain)

# ---------- ② 附录当期段期号重贴 ----------
app = io.open(APP, encoding="utf-8").read().replace("\r\n", "\n")
i = app.index("## 第 062 期（2026-11-08）")
head, seg = app[:i], app[i:]
n_old = seg.count("[附录 061]")
assert n_old > 0, "当期段里没有 [附录 061]（没找到对象）"
seg2 = seg.replace("[附录 061]", "[附录 062]")
assert seg2.count("[附录 061]") == 0
assert seg2.count("[附录 062]") == n_old
hist_before = head.count("[附录 061]")
app2 = head + seg2
assert app2[:i] == app[:i], "历史段被改动"
assert app2.count("[附录 061]") == hist_before, "历史段的 [附录 061] 数量变了"
io.open(APP, "w", encoding="utf-8", newline="\n").write(app2)
print("② 附录当期段重贴：%d 处（历史段 %d 处未动）" % (n_old, hist_before))

# ---------- 回读断言 ----------
disk = io.open(MD, encoding="utf-8").read()
assert "〔附录 062〕" not in disk
assert disk.count("[附录 062](details.html)") >= plain
dapp = io.open(APP, encoding="utf-8").read()
j = dapp.index("## 第 062 期（2026-11-08）")
assert "[附录 061]" not in dapp[j:]
print("回读通过：正文 %d 处、附录当期段 %d 处" % (disk.count("[附录 062](details.html)"), n_old))
