# -*- coding: utf-8 -*-
MD = "AI免费内容与权益速递-第030期-2026-10-11.md"
s = open(MD, encoding="utf-8").read()
old = "**另有本期新增事实**：**Nvidia 正洽谈加投或收购 Reflection AI**"
assert s.count(old) == 1, s.count(old)
s = s.replace(old, "**另有本期登记事实**：**Nvidia 正洽谈加投或收购 Reflection AI**")
open(MD, "w", encoding="utf-8").write(s)
print("ok")
