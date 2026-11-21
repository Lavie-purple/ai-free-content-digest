# -*- coding: utf-8 -*-
"""075 期：重写第四章脚注（四段）+ 补回 4.2 收尾段。"""
import csv
import datetime
import io
import re
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第075期-2026-11-21.md"
T = datetime.date(2026, 11, 21)

rows = list(csv.DictReader(io.open(WS + ".workbuddy/data/deadlines.csv", encoding="utf-8-sig")))
assert len(rows) == 261, len(rows)


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
assert (nA, nB, nC, nD, nE) == (37, 10, 4, 205, 5), (nA, nB, nC, nD, nE)
assert nA + nB + nC + nD + nE == len(rows) == 261, (nA, nB, nC, nD, nE, len(rows))

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
assert sum(color.values()) == 261, sum(color.values())
assert sum(cls.values()) == 261

FOOT = """### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-21` 实跑；CSV 共 `261` 条 ＝ 本章可见 `4.1` 的 `67` 行 ＋ 本章 `4.2` 与《常驻权益总账》合并去重后的 `194` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`{nA}` 条（074 期 `38`，`−1`）** —— **出 `1`**：`Google Antigravity` 三模型（**官方把截止日从 `11/18` 改到 `11/30`，本期已移入 `B` 桶**）；**进 `0`**。桶内最该看的两条：`腾讯老混元` 停服（`09-30`，**已过 `52` 天，厂商仍只给「9 月底」**）、`MiniMax M2.5 / M2.7` 退役（`11/18`）。
  {listA}
- **【B】14 天内到期：`{nB}` 条（074 期 `10`，`0`）** —— **进 `1`**：**`Google Antigravity` 三模型（`11/30`，`T+9`）**；**出 `1`**：`AutoClaw M11W3`（`11/22` 仍在桶内，只是天数从 `T+2` 变 `T+1`）→ 实为 **`Antigravity` 进、`MiniMax 4K` 旧版那类不占位**，**净增 `0`**。桶内最紧的三条：`AutoClaw M11W3`（`T+1`）、`虎鲸文娱` 大赛（`T+1`）、`ERNIE 5.5`（`T+4`）。
  {listB}
- **【C】已结束：`{nC}` 条（074 期 `3`，`+1`）** —— **进 `1`**：**`腾讯混元` `Hy4` / `Hy4 flash` 官方 `AMA`（`11/21 02:00` 收口）**。四条：`Runware` `H3 Max` `30% OFF`（`11/15`）、`Runware` `4K 50% OFF`（`11/17`）、`MiniMax` `4K` 五折**旧版**（`11/18`）、**`Hy4` `AMA`（`11/21`）**。**⚠️ `MiniMax` 那条仍只是「旧版结束」** —— 现行第二版仍在架（见 `4.2`），**在 `C` 里算收口、在正文里还活着**，两句话同时成立（避坑 317）。
- **【D】日期无法解析：`{nD}` 条（074 期 `203`，`+2`）** —— 本期补入 `2` 条无截止日的常驻权益：**`Inkling-2-Mini` 开放权重**、**腾讯混元 `Hy4`（`770B`）开放权重**。无归档移出。`D ≠ 失效`。
- **【E】窗口外（>14 天）：`{nE}` 条** —— `12/09` 杭州全城 Coding 计划、`12/31` 四条（`Gemini 3.8 Flash` 促销价、`Moonshot K2` 下线、`Runway` 企业版、`腾讯云 TokenHub` 新人包）。
  **对账：`A{nA} + B{nB} + C{nC} + D{nD} + E{nE} = {total}`，CSV `{total}` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体与总账实算，共 `{total}`）**：

- **色标（状态列行首）**：⚪`{c_o}` / 🔴`{c_r}` / 🟢`{c_g}` / 🟡`{c_y}` / 🟠`{c_p}` / ⚠`{c_w}` / 空`{c_n}` ＝ **`{total}`**
- **`classify()`（状态列语义）**：`crit {k_crit}` / `live {k_live}` / `switch {k_switch}` / `pending {k_pend}` / `unclear {k_unc}` / `over {k_over}` ＝ **`{total}`**

**⚠️ 本期 `over` 与 `⚪` 差 `{diff_over}`（`{k_over}` 对 `{c_o}`）** —— 其余各组：`🔴{c_r}` vs `crit{k_crit}`、`🟢{c_g}` vs `live{k_live}`、`🟠{c_p}` vs `switch{k_switch}`、`🟡{c_y}` vs `pending{k_pend}`、`⚠{c_w}` vs `unclear{k_unc}`。**色标是「谁写的」，`classify()` 是「写的是什么」，不该指望相等；差额必须逐条归因、不当常数。**

**③ 逐行 diff（本期改写 `19` 行状态列 ＋ 补入 `2` 行 ＋ 收口 `1` 行 ＋ 改期 `1` 行 ＋ 归档 `0` 行）**：

- **改写 `19` 行**：`4.1` 里 `9` 行（`腾讯老混元`（手算天数）、`Hy4 flash 限免`、`Hy4 AMA`、`ERNIE 5.5`、`MiniMax 4K`、`Runware 4K 50%`、`Antigravity 三模型`、`AutoClaw M11W3`、`AutoClaw M11W4`）、`4.2` 里 `10` 行（`OpenRouter 免费档`、`Token 羊毛`、`Antigravity 个人免费档`、`ERNIE-5.5-Flash-Base`、`Inkling 2 Small`、`OpenCode 免费清单`、`LongCat-2.5`、`Hy4 开放权重`、`GPT-6.2`、`Ling 3.2`）。**全部走「整体替换状态列」。**
- **补入 `2` 行**：`4.2` 的 **`thinkingmachines/Inkling-2-Mini` 开放权重**、**腾讯混元 `Hy4`（`770B`）开放权重**，分别带 `075 期补入` / `075 期补登` 标记。**两条都无截止日 → 进 `D` 桶，进 B 桶的是 `Antigravity` 那一行。**
- **只改天数 `46` 行**（与上面 `19` 行部分重叠）：带天数的每一处都按「截止日 − `2026-11-21`」重算，脚本末尾逐行带符号比对。`腾讯老混元` 的「`2026` 年 `9` 月底」不可解析，**手算 `已过 52` 天**（`09-30` 起算），另两处手工推进（`Q04` 第 `48` 期、高危窗口第 `39` 天）。
- **收回 `1` 行（`⚪`）**：`Hy4` `AMA` 到点收口（`11/21 02:00`）。**它不是「被撤」，是「按计划开完」** —— 与 `MiniMax` 那种「撤了又挂」不是一类。
- **改期 `1` 行**：`Antigravity` 三模型，截止日 `11/18 → 11/30`。**这是本期唯一一行「截止日被整体替换」的**，也是 `A −1 / B +1` 的唯一来源。
- **归档 `0` 行** —— 过期已收口的 `Runware` 两条（`11/15`、`11/17`）都在 `7` 天宽限内，不移出表体。

**⚠️ 一处口径自查（本期主动改，非官方动作）**：`Runware` `4K 50%` 一行，本期一开始写成了 `🟠`，`classify()` 归 `switch` → 它会被算进 `A` 桶、`C` 桶少一条。**发现后改回 `⚪`（已收口）**：三个读数（徽标 `0`、价目不动、数组留着过期条目）与 074 判「已收口」时完全一致，**没有新证据支持「它又活了」**。**改色标不改事实，但会让 `A` / `C` 各错一条 —— 这类「只影响分桶」的改动最容易漏。**

**④ 下期（`076`）强制动作 —— 出刊前逐条过**：

1. **`Inkling 2 Mini` 的 `24` 小时读数**：`HF` `likes` 是否过 `1,000`、`downloads` 是否开始计（本期 `136`）；`?search=Inkling-2-Mini` 是否从 `31` 继续涨。**另查 `Tinker` 是否有免费额度 —— 本期官方两个入口都没写。**
2. **`Hy4`（`770B`）与 `Hy4 flash` 别再混**：三仓 `downloads` 是否仍停在 `228` 合计；`?author=tencent` 是否有第四个仓（`Hy4-GGUF` 官仓）。**本期是补登，076 起按「新条目」跟踪。**
3. **`Antigravity` `11/30` 这次会不会又改**：`November 30` 是否维持；`November 18` 是否彻底消失。**073/074 连错两期，本期起该行只引用脚注原文日期，不再写「到期第 N 天」。**
4. **`AutoClaw` `M11W3` 收口（`11/22 23:59`）**：`11/22` 过后是否出现「无额度」窗口；`M11W4` 是否真在 `11/23 00:00` 到账 `100M`。**`M11W5` 是否在 `11/27` 前后挂出（照 `M11W4` 提前 `3` 天的规律）。**
5. **`ERNIE 5.5 Flash Preview`（`11/25`，剩 `4` 天）**：`?author=baidu` 是否从 `39` 变 `40`。**本季最后一个「官方给了日期」的开源承诺，076 期必须给结论。**
6. **`OpenRouter` 的 `477 / 12 / 15 / 14` 是否连续第 `2` 天不变**；`radixark/daisyrose-27b` 是否出现 `:free`；`gpt-6.2` 是否第 `5` 天仍无免费档。
7. **`Ling 3.2 Flash` 两套 `id`**：`:free` 的 `1` 条路由是否还在、基名是否仍 `0` 条；权重仓是否仍 `404`。**下期起查 `endpoints` 必须两套都查。**
8. **`HF` 的 `downloads` 何时解冻**：本期 `8` 仓全冻。**若 `076` 仍全冻，就写「连续 `2` 期未刷新」并给批次节奏（071、075 两次解冻的间隔）。**
9. **`MiniMax` 第二版（无截止日）第 `3` 天**：是否仍在架、页字节是否继续微增。**若再撤再挂，才按「常态轮换」记。**
10. **`Runware` 数组**：`11-23` 那 `2` 处到期后是否被换掉；`h3-image` 是否仍 `18`。**若「徽标卸、数组留」第 `17` 次出现，写「已成稳定行为」，不再单列实证次数。**
11. **三条长期缺口**：`lmarena.ai` 是否结束第 `9` 期 `000`；`hunyuan.tencent.com` 的 `JS` 壳（第 `8` 期，`6,584` 字节）；`chatgpt.com/pricing` 第 `5` 期是否可读。
12. **`Gemini 4 Neon` 的 API 免费额度**：`ai.google.dev/gemini-api/docs/pricing` 本期超时 `000`。**下期若仍取不到，写「连续 `2` 期不可达」，不再挂账。**
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

TAIL = """> **其余 `142` 条常驻权益本期无变化，未逐条重印** —— 全量见《[常驻权益总账](常驻权益总账.md)》（`194` 条）。**`4.2` 收录 `52` 条在跟踪的常驻权益，其中本期改写 `10` 条、补入 `2` 条、其余 `40` 条沿用上期读数**；这 `52` 条与总账是同源副本，**不重复计数**。⚠️ 这 `142` 条沿用上期读数、**本期未逐个重取** —— 不写成「已复核」。

"""

i = md.index("### ④ 本期第四章脚注")
md = md[:i] + TAIL + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(MD, encoding="utf-8").read()
assert "其余 `142` 条" in disk
assert "**④ 下期（`076`）强制动作" in disk
assert "A37 + B10 + C4 + D205 + E5 = 261" in disk, [l for l in disk.split("\n") if "对账：" in l]
print("footnote ok | bytes", len(disk.encode()))
print("色标：", dict(color), "｜classify：", dict(cls))
