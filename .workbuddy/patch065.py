# -*- coding: utf-8 -*-
"""065 期：逐行状态列改写的第二段（fix_days 只处理「已过 N 天」，处理不了相对期限与多日期行）。

由来（055 避坑 252 / 064 工程坑 ④）：多日期行的「已过 N 天」会被绑到**截止列最后一个日期**上；
`11/9（停服）；10/29（停止新建）；2027-01-09（导出）` 这一行本期被算成「已过 13 天」——
真值是 `2` 天。**处置：改成不带「已过 N 天」token 的写法（「截至本期基准日已满 N 天」）。**
"""
import io
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第065期-2026-11-11.md"
PTR = " [附录 065](details.html) |"

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
lines = md.split("\n")


def name_of(r):
    return r.strip().strip("|").split("|")[0].strip()


def set_status(row, status):
    cells = row.strip().rstrip("|").split("|")
    assert len(cells) == 4, ("字段数异常", len(cells), row[:40])
    return "|%s|%s| %s%s" % (cells[1], cells[2], status, PTR)


PATCH = [
    ("腾讯 WorkBuddy Hy3", "🟢 **已过 `11` 天（`10/31` 到期，官方未给延长口径）。 050 期实访的限免口径到 `10/31` 为止，"
                          "本期未见续期公告；`Hy4 preview` 夜间限免同批到期。**"),
    ("Laya 决策模型", "🟢 **已过 `11` 天（`10/31` 到期）。 该条自 049 期起未再复核到活动页，保留待查、不销项。**"),
    ("腾讯云 TokenHub 国际站促销", "🟢 **已过 `12` 天（`10/30 12:00` 北京到期）。 ⚠️ 国际站与国内 WorkBuddy / 国内 TokenHub 的限免是两条线，不可混算。**"),
    ("智谱清言「双节", "🟢 **已过 `11` 天（`10/31` 为领取窗口末日）。 返还是「消耗积分」，不是「送积分」。**"),
    ("腾讯轻量云专家限量", "🟢 **生效中（距今 `2` 天）**"),
    ("Google AI Plus 失去 Pro 模型选择权", "🟠 **倒计时中（距今 `2` 天）。 ⚠️ 官方支持文档此前写 `10/9`、邮件改口 `11/13`，两次日期差未说明原因。**"),
    ("MiniMax `M2.5` / `M2.7` 系列退役", "⚠️ **分两个节点、不是一天（见下），距今 `7` 天。 ⚠️「自动改路由」对做对比测试的人是陷阱：你以为在测 `M2.7`，实际测的是 `M3.1 Flash Preview`（避坑 186）。**"),
    ("Google `Gemini 4 Argon`", "🟠 **`GA` 已生效、首发优惠价倒计时中（距今 `19` 天）。 ⚠️ `87%` 是单一基准、纯推理口径、官方自披露（避坑 116）。**"),
    ("腾讯智能体平台「元器」停止服务", "🔴 **停服日（`11/9`）截至本期基准日已满 `2` 天。 三个日期继续分开排**：`10/29` 已停止新建、"
                                      "**`11/9` 停止服务**、`2027-01-09` 数据导出截止。 **本报告只报日期，不报「已停 / 未停」**。**"),
    ("智谱 `AutoClaw` 国内站 `M10W4`", "🟢 **已过 `10` 天（活动期 `10/26–11/1`）。 一周一档，本期已进入 `M11W2` 周期，官方未见新档公告。**"),
    ("智谱 `AutoClaw` 国际站 `M10W4`", "🟢 **已过 `10` 天（活动期 `10/26–11/1`，`UTC+8`）。 国际站与国内站两套积分不可互转。**"),
    ("`Moonshot` `K2` 系列模型停新注册", "🔴 **已过 `11` 天（`10/31` 停止向新注册用户开放）；`12` 月底计划下线，官方未给确切日**。 迁移口径见附录。**"),
    ("Figma `Code Layers`", "🟢 **已过 `7` 天（`11/4` 到期）。 正好在 `7` 天宽限期内，本期不归档、只留作「是否延期」的观察点。**"),
]

n = 0
for prefix, status in PATCH:
    hits = [i for i, l in enumerate(lines)
            if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")
            and prefix in name_of(l)]
    assert len(hits) == 1, ("命中数不是 1", prefix, len(hits))
    lines[hits[0]] = set_status(lines[hits[0]], status)
    n += 1

out = "\n".join(lines)
io.open(MD, "w", encoding="utf-8", newline="\n").write(out)

disk = io.open(MD, encoding="utf-8").read()
i = disk.index("### 4.1"); j = disk.index("### 4.2")
r41 = [l for l in disk[i:j].split("\n")
       if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(r41) == 57, len(r41)
assert Counter(len(r.strip().strip("|").split("|")) for r in r41) == Counter({3: 57})
assert "停服日（`11/9`）截至本期基准日已满 `2` 天" in disk
assert "停服日已过 `13` 天" not in disk
print("patch %d 行；4.1 = %d；bytes = %d" % (n, len(r41), len(disk.encode("utf-8"))))
