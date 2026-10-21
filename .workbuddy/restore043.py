# -*- coding: utf-8 -*-
"""把 043 期 md 的第四章表格整块还原成 <<<TABLE4>>> 占位符（供 gen_table043 + inject043 重跑）。
⚠️ **第四章脚注里的「口径 | 分布」小表必须保留** —— 它在表格之后、脚注之前，边界靠「**第四章脚注」标题定位。
"""
import re

SRC = "AI免费内容与权益速递-第043期-2026-10-21.md"

md = open(SRC, encoding="utf-8").read()
lines = md.split("\n")

s = e = None
for i, l in enumerate(lines):
    if l.startswith("## 四、"):
        s = i
    if s is not None and l.startswith("**第四章脚注"):
        e = i
        break
assert s is not None and e is not None and s < e, (s, e)

block = lines[s:e]
# 保留块内非表格行（第四章标题行、脚注引导语等），删掉所有以 | 开头的表格行
kept = [l for l in block if not l.startswith("|")]
# 在块内找一个合适位置插入占位符：紧跟第四章标题与引导语之后
ins = None
for i, l in enumerate(kept):
    if l.startswith("## 四、"):
        ins = i + 1
        break
assert ins is not None
new_block = kept[:ins] + ["<<<TABLE4>>>"] + kept[ins:]

lines[s:e] = new_block
md = "\n".join(lines)
assert md.count("<<<TABLE4>>>") == 1, md.count("<<<TABLE4>>>")
assert "| 活动 | 截止 | 状态 |" not in md
open(SRC, "w", encoding="utf-8", newline="\n").write(md)
print("restored to placeholder; TABLE4 count:", md.count("<<<TABLE4>>>"))
