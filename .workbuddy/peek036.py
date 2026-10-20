# -*- coding: utf-8 -*-
"""查看台账关键行的尾部锚点（只读）。"""
import io

P = "AI信息源分级清单-T0-T4.md"
t = io.open(P, encoding="utf-8", newline="").read()
assert "\r\n" not in t, "源文件不是 LF 行尾"
L = t.split("\n")

print("L3 tail:", repr(L[2][-90:]))
print()
print("L8 tail:", repr(L[7][-90:]))
print()
print("L336 tail:", repr(L[335][-90:]))
print()
row = [x for x in L if "aifree.dev" in x][0]
print("L372 tail:", repr(row[-200:]))
print()
# 州AG 行上下文
i = next(i for i, x in enumerate(L) if "总检察长办公室通稿" in x)
print("州AG 行号:", i + 1)
for j in range(i - 4, i + 3):
    print("  %4d: %s" % (j + 1, L[j][:80]))
print()
# 辽宁省行
k = next(i for i, x in enumerate(L) if "辽宁省财政厅" in x)
print("辽宁行号:", k + 1)
for j in range(k - 2, k + 4):
    print("  %4d: %s" % (j + 1, L[j][:80]))
