# -*- coding: utf-8 -*-
"""057 期：把「4.1 + 4.2 合并表体」注入正文并写出 md（inject 步骤）。

⚠️ split_ledger.py 取「第四章里最长的一块表格」当表体，再按截止列拆成 4.1 / 4.2。
   因此这里必须注入**一个合并表**（不分两张），否则 4.2 会变 0 行。
"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
A = WS + ".workbuddy/tmp_057_body_a.md"
C = WS + ".workbuddy/tmp_057_body_c.md"
TBL = WS + ".workbuddy/tmp_table057.md"
OUT = WS + "AI免费内容与权益速递-第057期-2026-11-03.md"

a = io.open(A, encoding="utf-8").read().replace("\r\n", "\n")
c = io.open(C, encoding="utf-8").read().replace("\r\n", "\n")
tbl = io.open(TBL, encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")

rows = [l for l in tbl.split("\n")
        if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(rows) == 215, ("表体总行数异常", len(rows))

CH4 = """## 四、限时活动与截止时间表（11/3 09:05 复核 · 过期 >7 天已归档）

| 活动 | 截止 | 状态 |
| --- | --- | --- |
""" + "\n".join(rows) + """

<<<FOOT057>>>
"""

out = a.rstrip("\n") + "\n\n" + c.strip("\n") + "\n\n---\n\n" + CH4
assert out.count("<<<FOOT057>>>") == 1, "脚注占位符不唯一"
assert "<<<TABLE4>>>" not in out

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)

print("written:", OUT)
print("chars:", len(out), "bytes:", len(out.encode("utf-8")))
print("表体行数:", len(rows))
