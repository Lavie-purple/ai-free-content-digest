# -*- coding: utf-8 -*-
"""068 期：把 7 行超长状态列压到 ≤195 字（lint R1 口径：状态列去链接去空白后的字数）。"""
import io
import re

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第068期-2026-11-14.md"
PTR = " [附录 068](details.html) |"

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")


def rows_of(text, start, end):
    i = text.index(start)
    j = text.index(end)
    return [l for l in text[i:j].split("\n")
            if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]


r41 = rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
r42 = rows_of(md, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")


def name_of(r):
    return r.strip().strip("|").split("|")[0].strip()


def cells_of(r):
    return r.strip().strip("|").split("|")


def metric(st):
    return len("".join(re.sub(r"\[[^\]]*\]\([^)]*\)", "", st).split()))


PATCH = [
    ("Runway `Praxis-1` 开放权重",
     "🟢 **已开放权重（068 期补登）。 三个时间点全在本期窗口前，066–067 两期漏报。 `RoboLab-120` `46.2%`（官方自测）。**", r42),
    ("`inclusionAI` `Ling 3.2 Flash` 进入",
     "🟡 **生效中（068 期补入）。 三层只开一层：列表有、`/endpoints` 为 `[]`、权重仓 `404`。**", r42),
    ("MiniMax `H3-Image` `4K` 生图限时",
     "🟠 **生效中（距截止 `4` 天）。 （067 期补入）`4K` `0.4522 → 0.2261` 元；`1K` / `2K` **不打折**。 页面 `−19,852` 字节但可见文本逐字相同。 需 ≥ `1660` 万像素。**", r41),
    ("`Google Antigravity` 个人免费档",
     "🟢 **生效中（官方逐字 `$0/month`，本期首次真正读到）。 含 `Basic weekly rate limits`；`free` 整页 `0` 命中；额度无数字。**", r42),
    ("`thinkingmachines/Inkling-2-Small` 开放权重",
     "🟢 **`Apache-2.0` · `36` 个文件。 本期 `downloads 12 → 1,064`（`86` 倍）、`likes 166 → 280`；`lastModified 11/13 21:12 UTC`。**", r42),
    ("OpenRouter 免费档（**官方 API 目录口径",
     "🟢 **全量 `471`（`−1`）；`:free` `14`；零价 `17`；`max_price=0` `16`。 进 `ling-3.2-flash:free`（端点空）；出 `liquid/lfm-2.5-2.6b` 两条。**", r42),
    ("`Google Antigravity` 科研 / 安全 6 个月免费档",
     "🟡 **以申请通过为准（官方逐字 `free of charge for 6 months`）。 本期站点恢复可达（首页 `200` / `214,361` 字节），个人档 `$0/month` 仍在。**", r41),
]

for prefix, status, bucket in PATCH:
    hits = [k for k, r in enumerate(bucket) if prefix in name_of(r)]
    assert len(hits) == 1, ("命中数不是 1", prefix, len(hits))
    c = cells_of(bucket[hits[0]])
    assert len(c) == 3
    assert "|" not in status
    new = "|%s|%s| %s%s" % (c[0], c[1], status, PTR)
    assert metric(status) <= 195, (prefix, metric(status))
    bucket[hits[0]] = new

i = md.index("### 4.1 限时动作")
k2 = md.index("### ④ 本期第四章脚注")
HEAD = "| 活动 | 截止 | 状态 |\n| --- | --- | --- |\n"
new_md = (md[:i]
          + "### 4.1 限时动作（有确切截止日 · %d 条）\n\n" % len(r41)
          + HEAD + "\n".join(r41) + "\n\n"
          + "### 4.2 常驻权益本期变更（无截止日 · 本期有变化 %d 条）\n\n" % len(r42)
          + HEAD + "\n".join(r42) + "\n\n"
          + md[k2:])
io.open(MD, "w", encoding="utf-8", newline="\n").write(new_md)

disk = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
d41 = rows_of(disk, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
d42 = rows_of(disk, "### 4.2 常驻权益本期变更", "### ④ 本期第四章脚注")
assert len(d41) == 60 and len(d42) == 37, (len(d41), len(d42))
over = [(metric(cells_of(r)[2]), name_of(r)[:30]) for r in d41 + d42 if metric(cells_of(r)[2]) > 200]
print("超长剩余", over)
assert not over
print("压缩完成 | bytes", len(disk.encode()))
