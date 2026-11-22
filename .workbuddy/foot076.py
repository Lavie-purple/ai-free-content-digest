# -*- coding: utf-8 -*-
"""076 期：重写第四章脚注（四段）+ 补回 4.2 收尾段。"""
import csv
import datetime
import io
import re
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第076期-2026-11-22.md"
T = datetime.date(2026, 11, 22)

rows = list(csv.DictReader(io.open(WS + ".workbuddy/data/deadlines.csv", encoding="utf-8-sig")))
assert len(rows) == 262, len(rows)


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
assert (nA, nB, nC, nD, nE) == (37, 10, 4, 206, 5), (nA, nB, nC, nD, nE)
assert nA + nB + nC + nD + nE == len(rows) == 262, (nA, nB, nC, nD, nE, len(rows))

KEEP = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff]+")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF]\uFE0F?")


def key(s):
    return KEEP.sub("", s).lower()[:40]


def plain(s):
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s).strip()


md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
sec = md[md.index("## 四、"):]
led = io.open(WS + "常驻权益总账.md", encoding="utf-8").read()
color, seen = Counter(), set()
for block in (sec, led):
    for l in block.split("\n"):
        if not l.startswith("|"):
            continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) < 3 or c[0] == "活动" or c[0].startswith("---"):
            continue
        k = key(plain(EMOJI.sub("", c[0])))
        if k in seen:
            continue
        seen.add(k)
        m = re.match(r"[⚪🔴🟢🟡🟠⚠]", c[2].strip())
        color[m.group(0) if m else "空"] += 1

cls = Counter(r["状态"] for r in rows)
assert sum(color.values()) == 262, sum(color.values())
assert sum(cls.values()) == 262

FOOT = """### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-22` 实跑；CSV 共 `262` 条 ＝ 本章可见 `4.1` 的 `67` 行 ＋ 本章 `4.2` 与《常驻权益总账》合并去重后的 `195` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`{nA}` 条（075 期 `37`，`0`）** —— **进 `0` 出 `0`**。桶内最该看的两条：`腾讯老混元` 停服（`09-30`，**已过 `53` 天，厂商仍只给「9 月底」**）、`MiniMax M2.5 / M2.7` 退役（`11/18`）。
  {listA}
- **【B】14 天内到期：`{nB}` 条（075 期 `10`，`0`）** —— **名单没换人，只是全员往前挪了一天**：`AutoClaw M11W3` 与 `虎鲸文娱` 大赛都到 `T+0`（今天），`ERNIE 5.5` 到 `T+3`，`Hy4 flash` 限免与 `M11W4` 到 `T+7`，`Antigravity` / `Runway Kling` / `Gemini 4 Argon` 到 `T+8`。
  {listB}
- **【C】已结束：`{nC}` 条（075 期 `4`，`0`）** —— **进 `0` 出 `0`**。四条：`Runware` `H3 Max` `30% OFF`（`11/15`）、`Runware` `4K 50% OFF`（`11/17`）、`MiniMax` `4K` 五折**旧版**（`11/18`）、`Hy4` `AMA`（`11/21`）。**⚠️ `MiniMax` 那条仍只是「旧版结束」** —— 现行第二版仍在架（见 `4.2`），**在 `C` 里算收口、在正文里还活着**（避坑 317）。
- **【D】日期无法解析：`{nD}` 条（075 期 `205`，`+1`）** —— 本期补入 `1` 条无截止日的常驻权益：**`thinkingmachines/inkling-2-mini` 的 `OpenRouter` 入口**（按量计费、无免费档）。无归档移出。`D ≠ 失效`。
- **【E】窗口外（>14 天）：`{nE}` 条** —— `12/09` 杭州全城 Coding 计划、`12/31` 四条（`Gemini 3.8 Flash` 促销价、`Moonshot K2` 下线、`Runway` 企业版、`腾讯云 TokenHub` 新人包）。
  **对账：`A{nA} + B{nB} + C{nC} + D{nD} + E{nE} = {total}`，CSV `{total}` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体与总账实算，共 `{total}`）**：

- **色标（状态列行首）**：⚪`{c_o}` / 🔴`{c_r}` / 🟢`{c_g}` / 🟡`{c_y}` / 🟠`{c_p}` / ⚠`{c_w}` / 空`{c_n}` ＝ **`{total}`**
- **`classify()`（状态列语义）**：`crit {k_crit}` / `live {k_live}` / `switch {k_switch}` / `pending {k_pend}` / `unclear {k_unc}` / `over {k_over}` ＝ **`{total}`**

**⚠️ 本期 `over` 与 `⚪` 差 `{diff_over}`（`{k_over}` 对 `{c_o}`）** —— 其余各组：`🔴{c_r}` vs `crit{k_crit}`、`🟢{c_g}` vs `live{k_live}`、`🟠{c_p}` vs `switch{k_switch}`、`🟡{c_y}` vs `pending{k_pend}`、`⚠{c_w}` vs `unclear{k_unc}`。**色标是「谁写的」，`classify()` 是「写的是什么」，不该指望相等；差额必须逐条归因、不当常数。**

**③ 逐行 diff（本期改写 `25` 行状态列 ＋ 补入 `1` 行 ＋ 收口 `0` 行 ＋ 改期 `0` 行 ＋ 归档 `0` 行）**：

- **改写 `25` 行**：`4.1` 里 `12` 行（`腾讯老混元`（手算天数）、`Hy4 flash 限免`、`Hy4 AMA`、`ERNIE 5.5`、`MiniMax 4K`、`Runway Kling 4.0`、`Runway 企业版`、`Runware 4K 50%`、`Runware H3 Max`、`AutoClaw M11W3`、`AutoClaw M11W4`、`Antigravity 三模型`）、`4.2` 里 `13` 行（`OpenRouter 免费档`、`OpenCode 免费清单`、`Token 羊毛`、`Antigravity 个人免费档`、`ERNIE-5.5-Flash-Base`、`Inkling 2 Mini`、`Inkling 2 Small`、`Hy4 flash 开放权重`、`Hy4`（`770B`）、`LongCat-2.5`、`GPT-6.2`、`Ling 3.2`、`MiniMax 4K 第二版`）。**全部走「整体替换状态列」。**
- **补入 `1` 行**：`4.2` 的 **`thinkingmachines/inkling-2-mini` 的 `OpenRouter` 入口**，带 `076 期新增观测位` 标记。**无截止日 → 进 `D` 桶。**
- **只改天数 `46` 行**（与上面 `25` 行部分重叠）：带天数的每一处都按「截止日 − `2026-11-22`」重算，脚本末尾逐行带符号比对。`腾讯老混元` 的「`2026` 年 `9` 月底」不可解析，**手算 `已过 53` 天**（`09-30` 起算），另两处手工推进（`Q04` 第 `49` 期、高危窗口第 `40` 天）。
- **收口 `0` 行、改期 `0` 行、归档 `0` 行** —— 本期没有任何一行换桶。**`AutoClaw M11W3` 是「今天到期」、不是「已收口」，所以它仍在 `B` 桶的 `T+0`，等 `077` 期再归 `C`。**

**④ 下期（`077`）强制动作 —— 出刊前逐条过**：

1. **`AutoClaw M11W3` 今晚 `23:59` 收口**：`11/23 00:00` 后 `M11W4` 是否真到账 `100M`；**`M11W5` 是否在 `11/27` 前后挂出**（照 `M11W4` 提前 `3` 天的规律）。`M11W3` 应在 `077` 期归 `C`。
2. **`ERNIE 5.5 Flash Preview`（`11/25` 前，剩 `3` 天）**：**本期是最后窗口，`077` 期必须给结论** —— 放权重或承认延期；`?author=baidu` 是否从 `39` 变 `40`。
3. **`OpenRouter` 的 `476 / 14 / 11 / 13`**：`:free` 是否继续降；`dots-3-note-preview:free` 是否回归；`inkling-2-mini` 是否出现 `:free`；`gpt-6.2` 第 `6` 天是否仍无免费档。
4. **`OpenCode` 免费池**：`Tidepool Alpha Free` 是否转正或再撤；`Inkling 2 Small Free` 是否彻底消失；弃用表是否再加行。**`DeepSeek V4.1 Flash Free` 本期首次点名，下期核它是否被弃用。**
5. **`HF` 的 `downloads`**：本期 `12` 仓同批上跳。**下期若继续动，说明批次周期短于一天；若全冻，写「第 `2` 次冻结」。`likes` 四仓下降是否延续 —— 若连续两期下降，就不是重算、是清理。**
6. **`Antigravity`（`11/30`，剩 `8` 天）**：脚注是否仍 `11/30`；`November 18` 是否仍 `0`；**`11/30` 过后三个第三方模型是否真移除** —— 这是它第三次给日期。
7. **`MiniMax` 第二版第 `4` 天**：是否仍在架、页字节是否继续微增。**若再撤再挂，按「常态轮换」记，不再当异常。**
8. **`Runware` 数组**：本期首次「一整期没动」；`11-23` 那 `2` 处到期后是否被换掉 —— **这是「账本会不会滚动」的第一次反向检验**；`h3-image` 是否仍 `18`。
9. **`Inkling 2 Mini`**：`Tinker` 侧免费额度是否可查（**已挂两期**）；`HF` `downloads` 是否继续涨；`OpenRouter` 是否加第三个 provider。
10. **`Token 羊毛` 第 `15` 期 / `freellm` 第 `6` 期**：面额与卡册数；`freellm` 的字节、`md5`、可见文本三项是否再次分离。
11. **三条长期缺口**：`lmarena.ai` 是否结束第 `10` 期 `000`；`hunyuan.tencent.com` 的 `JS` 壳（第 `9` 期）；`chatgpt.com/pricing` 第 `6` 期是否可读。
12. **工作流口径**：本期「先改 4.2 名字、后重建 CSV」踩过一次坑（同一权益在 CSV 里出现两行）。**下期顺序固定为：改表 → 改总账 → 重建 CSV → 跑巡检。**
"""

FOOT = FOOT.format(
    nA=nA, nB=nB, nC=nC, nD=nD, nE=nE, total=len(rows),
    listA=fmt(buckets["A"]), listB=fmt(buckets["B"]),
    c_o=color["⚪"], c_r=color["🔴"], c_g=color["🟢"], c_y=color["🟡"],
    c_p=color["🟠"], c_w=color["⚠"], c_n=color["空"],
    k_crit=cls["crit"], k_live=cls["live"], k_switch=cls["switch"],
    k_pend=cls["pending"], k_unc=cls["unclear"], k_over=cls["over"],
    diff_over=cls["over"] - color["⚪"],
)

TAIL = """> **其余 `142` 条常驻权益本期无变化，未逐条重印** —— 全量见《[常驻权益总账](常驻权益总账.md)》（`195` 条）。**`4.2` 收录 `53` 条在跟踪的常驻权益，其中本期改写 `25` 条、补入 `1` 条、其余 `27` 条沿用上期读数**；这 `53` 条与总账是同源副本，**不重复计数**。⚠️ 这 `142` 条沿用上期读数、**本期未逐个重取** —— 不写成「已复核」。

"""

i = md.index("### ④ 本期第四章脚注")
md = md[:i] + TAIL + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(MD, encoding="utf-8").read()
assert "其余 `142` 条" in disk
assert "**④ 下期（`077`）强制动作" in disk
assert "A37 + B10 + C4 + D206 + E5 = 262" in disk, [l for l in disk.split("\n") if "对账：" in l]
print("footnote ok | bytes", len(disk.encode()))
print("色标：", dict(color), "｜classify：", dict(cls))
