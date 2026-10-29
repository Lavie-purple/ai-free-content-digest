# -*- coding: utf-8 -*-
"""把 tmp_051_body_a.md + PLACEHOLDER 合并成 051 期 md，并把 <<<TABLE4>>> 替换成
gen_table050 产出的表块。写出前断言占位符已清零。
"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
A = WS + ".workbuddy/tmp_051_body_a.md"
B = WS + ".workbuddy/tmp_051_body_b.md"
TBL = WS + ".workbuddy/tmp_table051.md"
OUT = WS + "AI免费内容与权益速递-第051期-2026-10-29.md"

a = io.open(A, encoding="utf-8").read().replace("\r\n", "\n")
b = ""
t = io.open(TBL, encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")

assert "<<<TABLE4>>>" in a, "A 段缺占位符"
assert a.count("<<<TABLE4>>>") == 1, "占位符不唯一"
out = a.replace("<<<TABLE4>>>", t)
assert "<<<TABLE4>>>" not in out, "占位符未清零"
assert "```" not in out.replace("```bash", "").replace("```python", ""), "残留代码块"

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)

print("written:", OUT)
print("chars:", len(out))
print("lines:", out.count("\n") + 1)
print("bytes:", len(out.encode("utf-8")))
