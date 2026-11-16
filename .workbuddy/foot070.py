# -*- coding: utf-8 -*-
"""070 期：重写第四章脚注（四段）+ 补回 4.2 收尾段。"""
import csv
import datetime
import io
import re

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第070期-2026-11-16.md"
T = datetime.date(2026, 11, 16)

rows = list(csv.DictReader(io.open(WS + ".workbuddy/data/deadlines.csv", encoding="utf-8-sig")))


def short(name, n=24):
    name = re.sub(r"[（(].*$", "", name)
    return name.strip()[:n]


def fmt(rs):
    out = []
    for delta, d, r in sorted(rs, key=lambda x: (x[1], x[2]["活动"])):
        tag = "已过 %d 天" % (-delta) if delta < 0 else ("今天" if delta == 0 else "T+%d" % delta)
        out.append("`%02d-%02d`（%s）%s" % (d.month, d.day, tag, short(r["活动"])))
    return "　".join(out)


buckets = {"A": [], "B": [], "C": [], "D": [], "E": []}
for r in rows:
    if not r["截止日期"]:
        buckets["D"].append((0, None, r))
        continue
    d = datetime.date(*map(int, r["截止日期"].split("-")))
    delta = (d - T).days
    if r["状态"] == "over":
        buckets["C"].append((delta, d, r))
    elif delta < 0:
        buckets["A"].append((delta, d, r))
    elif delta <= 14:
        buckets["B"].append((delta, d, r))
    else:
        buckets["E"].append((delta, d, r))

nA, nB, nC, nD, nE = (len(buckets[k]) for k in "ABCDE")
assert nA + nB + nC + nD + nE == len(rows) == 245, (nA, nB, nC, nD, nE, len(rows))

KEEP = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff]+")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF]\uFE0F?")


def key(s):
    return KEEP.sub("", s).lower()[:40]


def plain(s):
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s).strip()


from collections import Counter

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
sec = md[md.index("## 四、"):]
led = io.open(WS + "常驻权益总账.md", encoding="utf-8").read()
color, seen = Counter(), set()
for block in (sec, led):
    for l in block.split("\n"):
        if not l.startswith("| ") or l.startswith("| 活动 |") or l.startswith("| --- |"):
            continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) < 3:
            continue
        k = key(plain(EMOJI.sub("", c[0])))
        if k in seen:
            continue
        seen.add(k)
        m = re.match(r"[⚪🔴🟢🟡🟠⚠]", c[2].strip())
        color[m.group(0) if m else "空"] += 1

cls = Counter(r["状态"] for r in rows)
assert sum(color.values()) == 245, sum(color.values())

FOOT = """### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-16` 实跑；CSV 共 `245` 条 ＝ 本章可见 `4.1` 的 `63` 行 ＋ 《常驻权益总账》`182` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`{nA}` 条（069 期 `34`，`+1`）** —— 新进 `1` = `48 号公告` 的征求意见截止（`11/15`，已过 `1` 天）；其余 `34` 条只是天数推进。**`A` 桶已连续两期只增不减 —— 这批是「过期了但没人收口」的长尾，不是待办清单。**
  {listA}
- **【B】14 天内到期：`{nB}` 条（069 期 `8`，`+3`）** —— 进 `5` 出 `2`：进 = 本期补入的 **`Runware H3-Image 4K 50% OFF`（`1` 天）** 与 **`Hy4 flash WorkBuddy 限免`（`13` 天）**，加上 `11/30` 三条（`Gemini 4 Argon` / `Runway Kling 4.0 25% off` / `Character.AI` 第 `11` 章）从 `E` 掉进 `14` 天内；出 = `11/15` 到期的两条（`48 号公告`、`Runware 30% OFF`）已转 `A` / `C`。**今天到期的只有一条：`Fable 5.2` 发布优惠。**
  {listB}
- **【C】已结束：`{nC}` 条。连续 `7` 期为空后本期第一次有值** —— 就是 `Runware` 的 `30% OFF`：`11/15` 到期，本期色标转 ⚪ 并写明「已过 `1` 天」。**「已结束」只给有逐字收口口径的条目，这一条的用户是「数组仍在、徽标已卸」双读之后才敢收的。**
- **【D】日期无法解析：`{nD}` 条（069 期 `192`，`+1`）** —— 本期补入 `1` 条无截止日的常驻权益（`Qwen4-Max` 付费旗舰、「小尺寸将开源」无日期），无归档移出，净 `+1`。`D ≠ 失效`。
- **【E】窗口外（>14 天）：`{nE}` 条（069 期 `8`，`−3`）** —— 减的 `3` 条就是 `11/30` 那批掉进 `B`；剩下的 `5` 条是 `12/09` 杭州全城 Coding 计划、`12/31` 四条（`Gemini 3.8 Flash` 促销价、`Moonshot K2` 下线、`Runway` 企业版、`腾讯云 TokenHub` 新人包）。
  **对账：`A{nA} + B{nB} + C{nC} + D{nD} + E{nE} = {total}`，CSV `{total}` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体实算：`4.1` 的 `63` 行 ＋ 总账 `182` 行，共 `{total}`）**：

- **色标（活动名列行首）**：⚪`{c_o}` / 🔴`{c_r}` / 🟢`{c_g}` / 🟡`{c_y}` / 🟠`{c_p}` / ⚠`{c_w}` / 空`{c_n}` ＝ **`{total}`**
- **`classify()`（状态列语义）**：`crit {k_crit}` / `live {k_live}` / `switch {k_switch}` / `pending {k_pend}` / `unclear {k_unc}` / `over {k_over}` ＝ **`{total}`**

**⚠️ 本期 `over` 与 `⚪` 差 `0`（`4` 对 `4`）** —— 连续两期差 `0`（069 期也是 `3` 对 `3`）。**这两组本期能对齐，是因为「过期且已收口」的那几条色标都改到位了**；另外四组仍各差 `1` 上下（`🔴{c_r}` vs `crit{k_crit}`、`🟢{c_g}` vs `live{k_live}`、`🟠{c_p}` vs `switch{k_switch}`、`🟡{c_y}` vs `pending{k_pend}`、`⚠{c_w}` vs `unclear{k_unc}`）—— **色标是「谁写的」，`classify()` 是「写的是什么」，不该指望相等。**

**③ 逐行 diff（本期改写 `20` 行状态列 ＋ 补入 `3` 行 ＋ 归档 `0` 行）**：

- **改写 `20` 行**：`4.1` 里 `10` 行（`腾讯老混元`（手算天数）、`ERNIE 5.5`、`MiniMax 4K`、`Runware 30%`、`腾讯轻量云`、`48 号公告`、`Gemini 4 Argon`、`Google AI Plus`、`Fable 5.2`、`Runware pruna-p-video-upscale`）、`4.2` 里 `10` 行（`OpenRouter 免费档`、`Token 羊毛`、`Antigravity 个人免费档`、`ERNIE-5.5-Flash-Base`、`Ripple`、`Inkling-2-Small`、`OpenCode 免费清单`、`Praxis-1`、`PEAR`、`LongCat-2.5`）。**全部走「整体替换状态列」**；另 **`40` 行**只改天数、不动措辞（`Counter({{3: 103}})`）。
- **补入 `3` 行**：`4.1` 的 **`Hy4 flash WorkBuddy 限免`** 与 **`Runware H3-Image 4K 50% OFF`**；`4.2` 的 **`Qwen4-Max`**。**三条都带 `070 期补入` 标记。**
- **归档 `0` 行** —— `prune_table` 本期判「表体 `103` 行 ＝ 保留 `103` + 移出 `0`」：所有过期条目要么未收口（K3），要么仍在 `7` 天宽限内。
- **⚠️ 本期最关键的一处不是改数字、是「不改」**：`Runware` 的 `2026-11-17` 与 `MiniMax` 的 `11/18 00:00` **本期并排写、不判同源**（第五章纠错①）。上一期判了「同一个截止」，本期撤回 —— **因为日粒度字段折不出时刻**。
- **天数 token 全部实算**：带天数的每一处都按「截止日 − `2026-11-16`」重算；脚本末尾断言逐行带符号比对。`腾讯老混元` 的「`2026` 年 `9` 月底」不可解析，**手算 `已过 47` 天**（`09-30` 起算），另两处期数手工推进（`Q04` 第 `43` 期、高危窗口第 `34` 天）。**状态列不出现「未开始」。**

**④ 下期（`071`）强制动作 —— 出刊前逐条过**：

1. **`MiniMax H3-Image` 的 `11/18 00:00` 之后**：`4K` 是否回到 `0.4522`、`Runware` 的 `11/17` 那条是否下架、计费页横幅是否消失（**三条同验**；这已是第 `2` 期挂这条，**下期必须给结论**）。
2. **`Hy4 flash` 的三条免费面**：`WorkBuddy` 内是否仍是 `11/29`、腾讯云 `TokenHub` 的 `5` 折有没有写明日期的页面、`OpenCode` 的 `hy4-flash-free` 是否仍在清单（**`11/17` 先看 `OpenCode` 有没有撤**）。
3. **`ERNIE 5.5 Flash Preview` 的 `11/25` 前是否开权重**：`?author=baidu` 是否从 `39` 变 `40`。**剩 `9` 天。**
4. **`Ling 3.2 Flash` 第 `4` 天**：`endpoints` 是否仍是 `[]`；**本期已停止逐日重写，只在表体写「空 `N` 天」**。
5. **`Qwen4` 小尺寸模型的权重**：官方博客只说「`coming to open source`」；下期查 `?author=Qwen` 是否出现 `Qwen4` 新仓、`Qwen-Live-Delivery-Plugin` 的仓库地址是否公布（**要 `spdx`，不是要新闻稿**）。
6. **`OpenRouter` 的 `qwen4-max`**：是否出现 `:free` 变体或降价；三个免费口径 `14 / 17 / 16` 是否连续第 `4` 天不变。
7. **`Token 羊毛` 第 `9` 期**：`¥1760` 与 `60` 张是否继续同向；`11/16` 那 `20` 条次日定格到几（**第五种形状之后，本报只记不推**）。
8. **`HF` 的 `downloads` 字段**：是否恢复刷新。**若仍冻结，本报下期起改为「只记 `likes` + 单独标注下载不可读」**，不再并排列。
9. **`Runware` 的 `4K 50% OFF`（`11/17` 到期）**：下期是否已卸徽标、数组是否还留着 `endsAt` —— **这是「卡片 / 数组」双读的第 `2` 次连续观测**。
10. **`hunyuan.tencent.com`**：是否从 `JS` 壳变成可读正文（本期 `6,894` 字节、可见文本 `1` 行）；**若下期仍读不出，`Hy4` 系列参数只能长期靠媒体**。
11. **`AutoClaw` 的「`1` 亿 Tokens」**：官方页是否出现这条（本期 `0` 命中）；出现即补登、不出现则按「聚合层读数」长期标注。
12. **`PEAR` 的 `pushed_at`**：`11/16 07:54:56Z` 这次推送改了什么（**本期未取 diff**）；是否有第三方复现 `LIBERO 74.4%`。
"""

FOOT = FOOT.format(
    nA=nA, nB=nB, nC=nC, nD=nD, nE=nE, total=len(rows),
    listA=fmt(buckets["A"]), listB=fmt(buckets["B"]),
    c_o=color["⚪"], c_r=color["🔴"], c_g=color["🟢"], c_y=color["🟡"],
    c_p=color["🟠"], c_w=color["⚠"], c_n=color["空"],
    k_crit=cls["crit"], k_live=cls["live"], k_switch=cls["switch"],
    k_pend=cls["pending"], k_unc=cls["unclear"], k_over=cls["over"],
)

TAIL = """> **其余 `142` 条常驻权益本期无变化，未逐条重印** —— 全量见《[常驻权益总账](常驻权益总账.md)》（`182` 条）。**`4.2` 只收「本期真正动过的 `40` 条」**；这 `40` 条与总账是同源副本，**不重复计数**。⚠️ 这 `142` 条沿用上期读数、**本期未逐个重取** —— 不写成「已复核」。

"""

i = md.index("### ④ 本期第四章脚注")
md = md[:i] + TAIL + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(MD, encoding="utf-8").read()
assert "其余 `142` 条" in disk
assert "**④ 下期（`071`）强制动作" in disk
assert "A35 + B11 + C1 + D193 + E5 = 245" in disk
print("footnote ok | bytes", len(disk.encode()))
print("A/B 列表长度：", len(fmt(buckets["A"])), len(fmt(buckets["B"])))
