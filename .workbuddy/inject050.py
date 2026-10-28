# -*- coding: utf-8 -*-
"""把 tmp_050_body_a.md + tmp_050_body_b.md 合并成 050 期 md，并把 <<<TABLE4>>> 替换成
gen_table050 产出的表块。写出前断言占位符已清零。
"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
A = WS + ".workbuddy/tmp_050_body_a.md"
B = WS + ".workbuddy/tmp_050_body_b.md"
TBL = WS + ".workbuddy/tmp_table050.md"
OUT = WS + "AI免费内容与权益速递-第050期-2026-10-28.md"

a = io.open(A, encoding="utf-8").read().replace("\r\n", "\n")
b = io.open(B, encoding="utf-8").read().replace("\r\n", "\n")
t = io.open(TBL, encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")

assert "<<<TABLE4>>>" in b, "B 段缺占位符"
assert b.count("<<<TABLE4>>>") == 1, "占位符不唯一"
out = a.rstrip("\n") + "\n\n" + b.replace("<<<TABLE4>>>", t)
assert "<<<TABLE4>>>" not in out, "占位符未清零"
assert "```" not in out.replace("```bash", "").replace("```python", ""), "残留代码块"

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)

print("written:", OUT)
print("chars:", len(out))
print("lines:", out.count("\n") + 1)
print("bytes:", len(out.encode("utf-8")))
