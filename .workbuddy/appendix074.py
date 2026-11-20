# -*- coding: utf-8 -*-
"""第 074 期：把 slim 压掉的 13 条完整原文追加进《第四章表体明细附录.md》。

数据源 `.workbuddy/tmp_072_slim.json`（slim074.py 写出，字段 name/old/new/before/after）。
纪律：**一字不删**；只做行首管道清理与「压缩前后字数」标注。
"""
import json, io, re

APP = "第四章表体明细附录.md"
J = ".workbuddy/tmp_074_slim.json"
HEAD = "## 第 074 期（2026-11-20）"
N = 11

items = json.load(io.open(J, encoding="utf-8"))
assert len(items) == N, ("slim 归档条数", len(items))

txt = io.open(APP, encoding="utf-8").read()
assert HEAD not in txt, "074 期附录已存在，勿重复追加"

blocks = []
for it in items:
    name, old, new = it["name"].strip(), it["old"].strip(), it["new"].strip()
    before, after = it["before"], it["after"]
    assert before > after, ("归档条目的 before 应大于 after", name[:20], before, after)
    blocks.append(
        "### %s\n\n"
        "**表体精简后**（`%d` 字 → `%d` 字，`lint_table` R1 口径）：%s\n\n"
        "**完整原文**：\n\n"
        "> %s\n" % (name, before, after, new, old)
    )

add = "\n" + HEAD + "\n\n" + (
    "本章收录第 074 期第四章表体为满足 `lint_table` R1（状态列 ≤ 200 字）"
    "而被压缩的 **%d** 条条目的**压缩前完整原文**，一字未删。"
    "表体只保留判断所需的最小集，论证过程在此存证。\n\n" % N
) + "\n".join(blocks)
txt = txt.rstrip("\n") + "\n" + add
io.open(APP, "w", encoding="utf-8", newline="\n").write(txt)

# 回读断言（053/054：断言只是必要条件，必须回读落盘文件）
back = io.open(APP, encoding="utf-8").read()
assert HEAD in back, "写入失败：标题未落盘"
n_hit = sum(1 for it in items if it["old"].strip()[:60] in back)
assert n_hit == N, ("回读命中不足", n_hit)
n_h3 = back.count("### ")
print("appendix ok | 追加 %d 条 | 回读命中 %d 条 | h3 合计 %d | 文件 %.0f KB"
      % (N, n_hit, n_h3, len(back.encode()) / 1024))
