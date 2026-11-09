# -*- coding: utf-8 -*-
"""063 期：指针链接化 + 导语补瘦身段 + 脚注行数校正 + 附录当期段期号重贴。

四件事（061/062 期纪律的延续）：
  ① 第四章导语补回「049 期起第四章表体已瘦身」段（本期第四章是脚本 append 的，
     原先缺这一段 —— **表体瘦身后不写这句，读者会以为长论证被删了**）；
  ② 日报正文里的 `〔附录 063〕` -> `[附录 063](details.html)`；
  ③ 脚注 ① 的「本章可见 `121` 行」按落盘实算改成 `103` 行（56 + 47）；
  ④ 《第四章表体明细附录.md》的 `## 第 063 期` 段内，把上期留下的 `[附录 062]` 重贴为 `[附录 063]`；
     历史段（第 049–062 期）一字不改。

**所有计数都从落盘文件实算，且对「命中 0 条」显式断言失败**（058 期：零命中不是通过，是没找到对象）。
"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第063期-2026-11-09.md"
APP = WS + "第四章表体明细附录.md"

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
app = io.open(APP, encoding="utf-8").read().replace("\r\n", "\n")

# ---------- ⓪ 实算本章可见行数 ----------
i41 = md.index("### 4.1 限时动作")
i42 = md.index("### 4.2 常驻权益本期变更")
i_end = md.index("> **其余", i42)
seg41 = md[i41:i42]
seg42 = md[i42:i_end]


def n_rows(seg):
    return len([l for l in seg.split("\n")
                if l.startswith("| ") and not l.startswith("| 活动 |")
                and not l.startswith("| --- |")])


n41, n42 = n_rows(seg41), n_rows(seg42)
visible = n41 + n42
assert (n41, n42) == (56, 47), ("本章行数与预期不符", n41, n42)
print("本章可见行：4.1 = %d + 4.2 = %d = %d" % (n41, n42, visible))

# ---------- ① 导语补瘦身段 ----------
anchor = "### 4.1 限时动作（有确切截止日 · %d 条）" % n41
assert md.count(anchor) == 1, ("4.1 标题不唯一", md.count(anchor))
SILM = (
    "> **049 期起第四章表体已瘦身**：**每行只留「谁 / 到什么时候 / 要不要动手」+ 一句边界**，"
    "**被裁掉的长论证一字未删地存放在 [`details.html`](details.html)（《第四章表体明细附录》，本期 %d 行）** —— "
    "**「表体里没有」不等于「没有写过」。**" % visible
)
assert "第四章表体已瘦身" not in md, "导语里已经有瘦身段（会重复插入）"
md = md.replace(anchor, SILM + "\n\n" + anchor, 1)
assert "049 期起第四章表体已瘦身" in md
print("① 导语补瘦身段：1 处（本期 %d 行）" % visible)

# ---------- ② 正文 〔附录 063〕 链接化 ----------
plain = md.count("〔附录 063〕")
assert plain > 0, "正文里一条 〔附录 063〕 都没有（没找到对象）"
assert plain == visible, ("指针数与可见行数不等", plain, visible)
md = md.replace("〔附录 063〕", "[附录 063](details.html)")
assert md.count("〔附录 063〕") == 0, "仍有未链接化的指针"
print("② 正文链接化：%d 处" % plain)

# ---------- ③ 脚注「本章可见 121 行」校正 ----------
bad = "本章可见 `121` 行"
assert md.count(bad) == 1, ("脚注旧行数未找到", md.count(bad))
md = md.replace(bad, "本章可见 `%d` 行" % visible)
assert "本章可见 `%d` 行" % visible in md
print("③ 脚注行数：121 -> %d" % visible)

io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

# ---------- ④ 附录当期段期号重贴 ----------
i = app.index("## 第 063 期（2026-11-09）")
head, seg = app[:i], app[i:]
n_old = seg.count("[附录 062]")
assert n_old > 0, "当期段里没有 [附录 062]（没找到对象）"
seg2 = seg.replace("[附录 062]", "[附录 063]")
assert seg2.count("[附录 062]") == 0
assert seg2.count("[附录 063]") == n_old
hist_before = head.count("[附录 062]")
app2 = head + seg2
assert app2[:i] == app[:i], "历史段被改动"
assert app2.count("[附录 062]") == hist_before, "历史段的 [附录 062] 数量变了"
io.open(APP, "w", encoding="utf-8", newline="\n").write(app2)
print("④ 附录当期段重贴：%d 处（历史段 %d 处未动）" % (n_old, hist_before))

# ---------- 回读断言 ----------
disk = io.open(MD, encoding="utf-8").read()
assert "〔附录 063〕" not in disk
assert disk.count("[附录 063](details.html)") == visible, (
    "回读指针数", disk.count("[附录 063](details.html)"))
assert "本章可见 `%d` 行" % visible in disk
dapp = io.open(APP, encoding="utf-8").read()
j = dapp.index("## 第 063 期（2026-11-09）")
assert "[附录 062]" not in dapp[j:]
print("回读通过：正文 %d 处、附录当期段 %d 处、脚注 %d 行"
      % (disk.count("[附录 063](details.html)"), n_old, visible))
