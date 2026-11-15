# -*- coding: utf-8 -*-
"""069 期：把 8 条 R1 超长、2 条 R3 沿革的状态列压回 200 字以内。

纪律（052/054）：
  · 键按「活动名唯一子串 + 旧状态前缀」双条件定位，命中必须恰好 1 行；
  · 改完**回读落盘文件**再断言，不信任内存变量；
  · 被裁掉的论证**一字不删**，原文进 tmp_069_slim.json，由 appendix069.py 落进附录。
"""
import io, json, re, sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第069期-2026-11-15.md"
OUT = WS + ".workbuddy/tmp_069_slim.json"

A = " [附录 069](details.html)"

# (活动名唯一子串, 旧状态前缀, 新状态)
REWRITE = [
    ("MIT 韩松团队 `PEAR`",
     "🟢 **（069 期补登）`GitHub` `mit-han-lab/pear`",
     "🟢 **已公开（069 期补登）。 权重与代码同在 `HF` / `GitHub`，`LICENSE` 原文 `11,544` 字节已读（Apache 2.0 原文）、非 `gated`；建仓到 `push` 相隔 `16` 秒。 "
     "`LIBERO` 零样本 `1.6% → 74.4%`；真机 `YAM` `30` 试成 `18`（训练前 `0`）；**不用遥操数据、不用真机数据**。" + A + "**"),

    ("美团 `LongCat-2.5` 以 `MIT`",
     "🟢 **（069 期补登）`cardData.license = mit`",
     "🟢 **已公开（069 期补登）。 `cardData.license = mit`、`gated: false`、两仓各 `231` 个文件（`W4A4` 仓 `487` 下载 / `3` 赞）。 "
     "`Terminal Bench v2.1` `88.4` / `DeepSWE` `64.6`（官方自测）；样例部署 `194` 张华为昇腾 `Atlas A2`，**无 `Nvidia` 指引**。" + A + "**"),

    ("`Google Antigravity` 个人免费档",
     "🟢 **官方定价页逐字 `$0/month`",
     "🟢 **生效中（官方定价页逐字 `$0/month`）。 含 `Unlimited Tab` / `Unlimited Command` / **`Basic weekly rate limits`**，额度无具体数字；"
     "`free` 整页 `0` 命中（免费只用 `$0` 表达）。 整页 `md5` 与上期逐字节相同（第 `4` 期同值），横幅一字未动、不写档位。" + A + "**"),

    ("MiniMax `H3-Image` `4K`",
     "🟠 **生效中（距截止 `3` 天）",
     "🟠 **生效中（距截止 `3` 天）。 `4K` 单张 `0.4522 → 0.2261` 元；`1K` / `2K` 不打折。 "
     "页面 `311,690` 字节与上期相同、`md5` 不同但可见文本逐行 `0` 差异（`511` 个字节位全在构建产物哈希上 · 避坑 300）。 "
     "⚠️ 折的是按张单价、不是额度；要求 ≥ `1660` 万像素。" + A + "**"),

    ("OpenRouter 免费档",
     "🟢 **全量 `471 → 470`",
     "🟢 **全量 `471 → 470`（`−1`）；`:free` `14` / 零价 `17` / `?max_price=0` `16` 三项不变。 "
     "进 `0` 出 `1`：出的是 `z-ai/glm-5.2:batch` —— `:batch` 变体，本体仍在。 "
     "`Ling 3.2 Flash` 的 `endpoints` 第 `2` 天仍 `[]`、`inclusionAI/Ling-3.2-flash` 仍 `404`。" + A + "**"),

    ("`Google Antigravity` 科研 / 安全 6 个月免费档",
     "🟡 **以申请通过为准（相对日期：官方逐字 `free of charge for 6 months`",
     "🟡 **以申请通过为准（官方逐字 `free of charge for 6 months`，未给统一截止日）。 "
     "首页与 `/pricing` 的 `md5` 与上期逐字节相同（`214,361` / `140,014`，第 `4` 期同值），个人档 `$0/month` 仍在、含 `Basic weekly rate limits`；`free` 整页 `0` 命中。" + A + "**"),

    ("`AIHOT` 的「Token 羊毛」",
     "🟡 **第三方聚合层 · 逐条标核实日",
     "🟡 **第三方聚合层 · 逐条标核实日 · 按官方价折人民币。 第 `7` 期：页头「今天还能领」`¥1599 → ¥2433`（`+834`）、卡册 `59 → 62` 张、"
     "日戳合计 `124`（`11/14` `108` / `11/15` `6` / `11/13` `2` / `11/9` `4` / `11/8` `4`）。 "
     "`11/14` 那 `108` 条次日一条没动 —— 四次形状全不同，本报只记读数、不推规律。" + A + "**"),

    ("`thinkingmachines/Inkling-2-Small`",
     "🟢 **`Apache-2.0` · `gated: false` · `36` 个文件",
     "🟢 **已公开。 本期 `downloads 1,064 → 7,329`（`6.3` 倍）/ `likes 280 → 327`；"
     "`MXFP8` 变体 `221 → 638` / `12 → 13`，`lastModified 11/15 05:56 UTC`（北京 `13:56`，落在窗口内）。 "
     "两日曲线 `12 → 1,064 → 7,329`：增速从 `86` 倍降到 `6.3` 倍，方向不变。" + A + "**"),
]


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def nchars(st):
    """lint_table 的 R1 口径：状态列去链接、去空白后的字符数。"""
    return len("".join(re.sub(r"\[[^\]]*\]\([^)]*\)", "", st).split()))


md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
lines = md.split("\n")
saved = []

for key, oldpfx, new in REWRITE:
    idxs = []
    for i, ln in enumerate(lines):
        if not ln.startswith("| "):
            continue
        c = cells(ln)
        if len(c) != 3 or c[0] == "活动":
            continue
        if key in c[0] and c[2].startswith(oldpfx):
            idxs.append(i)
    assert len(idxs) == 1, "%s 命中 %d 行（应为 1）" % (key, len(idxs))
    i = idxs[0]
    c = cells(lines[i])
    old = c[2]
    newn, oldn = nchars(new), nchars(old)
    assert newn < oldn, "%s 没有变短：%d -> %d" % (key, oldn, newn)
    assert newn <= 195, "%s 仍超 195 字：%d" % (key, newn)
    assert new.endswith("**"), "%s 结尾不是 **" % key
    assert new[0] in "🟢🟡🟠⚪⚠️", "%s 色标不在行首：%r" % (key, new[0])
    lines[i] = "| " + c[0] + " | " + c[1] + " | " + new + " |"
    saved.append({"name": c[0], "old": old, "new": new, "before": oldn, "after": newn})
    print("%-46s %4d -> %3d" % (key, oldn, newn))

io.open(MD, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
io.open(OUT, "w", encoding="utf-8", newline="\n").write(
    json.dumps(saved, ensure_ascii=False, indent=1))

# ---- 回读落盘文件再断言（不信任内存）----
disk = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
dl = disk.split("\n")
ok = 0
for it in saved:
    hit = [l for l in dl if l.startswith("| ") and it["name"] in cells(l)[0]]
    assert len(hit) == 1, it["name"]
    assert cells(hit[0])[2] == it["new"], "回读不符：%s" % it["name"]
    assert it["old"] not in disk, "旧状态仍在盘上：%s" % it["name"]
    ok += 1
assert disk.count("<<<TABLE4>>>") == 0
print("slim069 ok | 改写 %d 行 | bytes %d" % (ok, len(disk.encode())))
