# -*- coding: utf-8 -*-
"""054 期：把「4.1 + 4.2 合并表体」注入正文并写出 md（inject 步骤）。

⚠️ 关键：split_ledger.py 取「第四章里最长的一块表格」当表体，再按截止列拆成 4.1 / 4.2。
   因此 inject 这一步必须注入**一个合并表**（4.1 的行 + 4.2 的行顺序混排均可，
   split_ledger 会按「截止列能否解析出确切日期」重新分流）。
   若在这里就分成两张表，split_ledger 会挑错块、导致 4.2 变 0 行。

流水线顺序：gen_table -> inject -> prune -> split_ledger -> 脚注 -> slim(两轮) -> 指针链接化
          -> extract/check -> build/verify -> lint --strict
"""
import io
import re

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
A = WS + ".workbuddy/tmp_054_body_a.md"
C = WS + ".workbuddy/tmp_054_body_c.md"
TBL = WS + ".workbuddy/tmp_table054.md"
OUT = WS + "AI免费内容与权益速递-第054期-2026-10-31.md"

a = io.open(A, encoding="utf-8").read().replace("\r\n", "\n")
c = io.open(C, encoding="utf-8").read().replace("\r\n", "\n")
tbl = io.open(TBL, encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")

rows = [l for l in tbl.split("\n")
        if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(rows) == 205, ("表体总行数异常", len(rows))

header = "| 活动 | 截止 | 状态 |"
sep = "| --- | --- | --- |"

# ---- 第四章骨架（表体与脚注都在这里，脚注在 split_ledger 之后由 foot054.py 注入）----
CH4_HEAD = """## 四、限时活动与截止时间表（正文之后 · 10/31 19:00 复核 · 过期 >7 天已归档）

> **本章自 047 期修订起移到正文九章之后** —— 前面九章可以连贯读完，本章与《常驻权益总账》作为参考资料放在后面。**本章即往期所称「第四章」，编号与全部历史引用不变。**
>
> **本章只留两类**：**4.1 有确切截止日的限时动作** ／ **4.2 无截止日但本期有变化**。**未变动的常驻权益不再逐期重印**，全量 144 条移入《[常驻权益总账](常驻权益总账.md)》；**已过期 >7 天且已收口**的条目移入归档（`.workbuddy/data/deadline_archive.md`）—— 规则见脚注 ④。
>
> **052 期起第四章表体已瘦身**：**每行只留「谁 / 到什么时候 / 要不要动手」+ 一句边界**，**被裁掉的长论证一字未删地存放在 [`details.html`](details.html)（《第四章表体明细附录》）** —— **「表体里没有」不等于「没有写过」。**

"""

CH4_TABLE = header + "\n" + sep + "\n" + "\n".join(rows) + "\n"

CH4_TAIL = """
<<<FOOT054>>>
"""

ch4 = CH4_HEAD + CH4_TABLE + CH4_TAIL

out = a + c
out = out.rstrip("\n") + "\n\n" + ch4

assert out.count("<<<FOOT054>>>") == 1, "脚注占位符不唯一"
assert "<<<TABLE4>>>" not in out and "<<<CHAPTER4>>>" not in out

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)

print("written:", OUT)
print("chars:", len(out))
print("bytes:", len(out.encode("utf-8")))
print("表体行数:", len(rows))
