# -*- coding: utf-8 -*-
"""第 070 期：把 slim 压掉的 7 条完整原文追加进《第四章表体明细附录.md》。"""
import json, io, sys, re

APP = "第四章表体明细附录.md"
J = ".workbuddy/tmp_070_slim.json"
HEAD = "## 第 070 期（2026-11-16）"

def plain(s):
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return s

items = json.load(open(J, encoding="utf-8"))
assert len(items) == 7, len(items)

txt = io.open(APP, encoding="utf-8").read()
assert HEAD not in txt, "070 期附录已存在，勿重复追加"

blocks = []
for it in items:
    name, old, before, after = it["name"], it["old"], it["before"], it["after"]
    # 状态列原文里可能残留行首管道，清掉
    old_clean = old.strip()
    blocks.append(
        "### %s\n\n"
        "**表体精简后**（`%d` 字 → `%d` 字，`lint_table` R1 口径）：%s\n\n"
        "**完整原文**：\n\n"
        "> %s\n" % (name, before, after, it["new"], old_clean)
    )

add = "\n" + HEAD + "\n\n" + (
    "本章收录第 070 期第四章表体为满足 `lint_table` R1（状态列 ≤ 200 字）"
    "而被压缩的 **7** 条条目的**压缩前完整原文**，一字未删。表体只保留判断所需的最小集，"
    "论证过程在此存证。\n\n"
) + "\n".join(blocks)
txt = txt.rstrip("\n") + "\n" + add

io.open(APP, "w", encoding="utf-8", newline="\n").write(txt)

# 回读断言
back = io.open(APP, encoding="utf-8").read()
assert HEAD in back, "写入失败"
n_old = sum(1 for it in items if it["old"].strip()[:60] in back)
print("appendix ok | 追加 %d 条 | 回读命中 %d 条 | 文件 %.0f KB" % (len(items), n_old, len(back.encode()) / 1024))
assert n_old == 7, "回读只命中 %d 条" % n_old
