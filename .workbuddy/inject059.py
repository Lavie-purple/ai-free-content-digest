# -*- coding: utf-8 -*-
"""059 期：把「4.1 + 4.2 合并表体」注入正文并写出 md（inject 步骤）。

⚠️ split_ledger.py 取「第四章里最长的一块表格」当表体，再按截止列拆成 4.1 / 4.2。
   因此这里必须注入**一个合并表**（不分两张），否则 4.2 会变 0 行。
"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
A = WS + ".workbuddy/tmp_059_body_a.md"
C = WS + ".workbuddy/tmp_059_body_c.md"
TBL = WS + ".workbuddy/tmp_table059.md"
OUT = WS + "AI免费内容与权益速递-第059期-2026-11-05.md"

a = io.open(A, encoding="utf-8").read().replace("\r\n", "\n")
c = io.open(C, encoding="utf-8").read().replace("\r\n", "\n")
tbl = io.open(TBL, encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")

rows = [l for l in tbl.split("\n")
        if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(rows) == 218, ("表体总行数异常", len(rows))

CH4 = """## 四、限时活动与截止时间表（正文之后 · 11/5 12:35 复核 · 过期 >7 天已归档）

> **本章自 047 期修订起移到正文九章之后** —— 前面九章可以连贯读完，本章与《常驻权益总账》作为参考资料放在后面。**本章即往期所称「第四章」，编号与全部历史引用不变。**
>
> **本章只留两类**：**4.1 有确切截止日的限时动作** ／ **4.2 无截止日但本期有变化**。**未变动的常驻权益不再逐期重印**，全量移入《[常驻权益总账](常驻权益总账.md)》；**已过期 >7 天且已收口**的条目移入归档（`.workbuddy/data/deadline_archive.md`）—— 规则见脚注 ④。

| 活动 | 截止 | 状态 |
| --- | --- | --- |
""" + "\n".join(rows) + """

<<<FOOT059>>>
"""

out = a.rstrip("\n") + "\n\n" + c.strip("\n") + "\n\n---\n\n" + CH4
assert out.count("<<<FOOT059>>>") == 1, "脚注占位符不唯一"
assert "<<<TABLE4>>>" not in out

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)

print("written:", OUT)
print("chars:", len(out), "bytes:", len(out.encode("utf-8")))
print("表体行数:", len(rows))
