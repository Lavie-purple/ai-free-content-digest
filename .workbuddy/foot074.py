# -*- coding: utf-8 -*-
"""074 期：重写第四章脚注（四段）+ 补回 4.2 收尾段。"""
import csv
import datetime
import io
import re
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第074期-2026-11-20.md"
T = datetime.date(2026, 11, 20)

rows = list(csv.DictReader(io.open(WS + ".workbuddy/data/deadlines.csv", encoding="utf-8-sig")))
assert len(rows) == 259, len(rows)


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
assert (nA, nB, nC, nD, nE) == (38, 10, 3, 203, 5), (nA, nB, nC, nD, nE)
assert nA + nB + nC + nD + nE == len(rows) == 259, (nA, nB, nC, nD, nE, len(rows))

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
assert sum(color.values()) == 259, sum(color.values())
assert sum(cls.values()) == 259

FOOT = """### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-20` 实跑；CSV 共 `259` 条 ＝ 本章可见 `4.1` 的 `67` 行 ＋ 本章 `4.2` 与《常驻权益总账》合并去重后的 `192` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`{nA}` 条（073 期 `38`，`0`）** —— **进 `0`、出 `0`**。本期「过期未收口」没有新增，**最该看的仍是两条「官方没动」**：`Google Antigravity` 三模型（`11/18`，**到期第 `2` 天仍未执行**）、`MiniMax M2.5 / M2.7` 退役（`11/18`）。同桶另有 `Anthropic Claude Fable 5.2`（`11/17`）、`商务部` 第 `48` 号公告（`11/15`）、`腾讯轻量云` 专家限量（`11/13`）。
  {listA}
- **【B】14 天内到期：`{nB}` 条（073 期 `9`，`+1`）** —— **进 `1`**：**`AutoClaw` `M11W4`（`11/29`，`T+9`）**；**出 `0`**。桶内前段：`腾讯混元` `AMA`（`11/21`，`T+1`）、`AutoClaw` `M11W3`（`11/22`，`T+2`）、`虎鲸文娱` 大赛（`11/22`）、`ERNIE 5.5`（`11/25`，`T+5`）、`天猫 AI 空间站`（`11/28`，`T+8`）；`11/30` 三条仍 `T+10`。
  {listB}
- **【C】已结束：`{nC}` 条（073 期 `3`，`0`）** —— **不变**。三条：`Runware` `H3 Max` `30% OFF`（`11/15`）、`Runware` `4K 50% OFF`（`11/17`）、`MiniMax` `4K` 五折**旧版**（`11/18`）。**⚠️ `MiniMax` 那条只是「旧版结束」** —— 同一促销已换文案重挂（见 `4.2`），**在 `C` 里它算收口、在正文里它又活着，两句话同时成立**（避坑 317）。
- **【D】日期无法解析：`{nD}` 条（073 期 `201`，`+2`）** —— 本期补入 `2` 条无截止日的常驻权益：**`MiniMax 4K` 五折第二版**（新文案无日期）、**`Kimi` 文件接口限时免费**。无归档移出。`D ≠ 失效`。
- **【E】窗口外（>14 天）：`{nE}` 条** —— `12/09` 杭州全城 Coding 计划、`12/31` 四条（`Gemini 3.8 Flash` 促销价、`Moonshot K2` 下线、`Runway` 企业版、`腾讯云 TokenHub` 新人包）。
  **对账：`A{nA} + B{nB} + C{nC} + D{nD} + E{nE} = {total}`，CSV `{total}` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体与总账实算，共 `{total}`）**：

- **色标（状态列行首）**：⚪`{c_o}` / 🔴`{c_r}` / 🟢`{c_g}` / 🟡`{c_y}` / 🟠`{c_p}` / ⚠`{c_w}` / 空`{c_n}` ＝ **`{total}`**
- **`classify()`（状态列语义）**：`crit {k_crit}` / `live {k_live}` / `switch {k_switch}` / `pending {k_pend}` / `unclear {k_unc}` / `over {k_over}` ＝ **`{total}`**

**⚠️ 本期 `over` 与 `⚪` 差 `{diff_over}`（`{k_over}` 对 `{c_o}`）** —— 其余各组：`🔴{c_r}` vs `crit{k_crit}`、`🟢{c_g}` vs `live{k_live}`、`🟠{c_p}` vs `switch{k_switch}`、`🟡{c_y}` vs `pending{k_pend}`、`⚠{c_w}` vs `unclear{k_unc}`。**色标是「谁写的」，`classify()` 是「写的是什么」，不该指望相等；差额必须逐条归因、不当常数。**

**③ 逐行 diff（本期改写 `17` 行状态列 ＋ 补入 `3` 行 ＋ 收口 `0` 行 ＋ 归档 `0` 行）**：

- **改写 `17` 行**：`4.1` 里 `7` 行（`腾讯老混元`（手算天数）、`Hy4 flash 限免`、`MiniMax 4K`、`Runware 4K 50%`、`Antigravity 三模型`、`ERNIE 5.5`、`AutoClaw M11W3`）、`4.2` 里 `10` 行（`OpenRouter 免费档`、`Token 羊毛`、`Antigravity 个人免费档`、`ERNIE-5.5-Flash-Base`、`Inkling`、`OpenCode 免费清单`、`LongCat-2.5`、`Hy4 开放权重`、`GPT-6.2`、`Ling 3.2`）。**全部走「整体替换状态列」。**
- **补入 `3` 行**：`4.1` 的 **`AutoClaw` `M11W4`**；`4.2` 的 **`MiniMax 4K` 五折第二版**、**`Kimi` 文件接口限时免费**，均带 `074 期补入` 标记。
- **只改天数 `45` 行**（与上面 `17` 行部分重叠）：带天数的每一处都按「截止日 − `2026-11-20`」重算，脚本末尾逐行带符号比对。`腾讯老混元` 的「`2026` 年 `9` 月底」不可解析，**手算 `已过 51` 天**（`09-30` 起算），另两处手工推进（`Q04` 第 `47` 期、高危窗口第 `38` 天）。
- **收口 `0` 行**：本期没有新的「从货架撤下」条目 —— **`MiniMax` 是反方向的（重新上架），不是收口。**
- **归档 `0` 行** —— 过期条目里已收口的 `Runware` 两条（`11/15`、`11/17`）**都在 `7` 天宽限内，不移出表体**。

**⚠️ 一处自查（本期主动对齐，非官方动作）**：`Runware` `4K 50%` 这一行，073 期的**行首色标是 `🟠`、而 CSV 里 `状态` 是 `over`** —— 两处不一致。本期按「徽标 `0` + 价目不动」判为**已收口**，色标改回 `⚪`，与 `C` 桶对齐。**这次改动让 `A` / `C` 的数字都不动**（`A38` / `C3` 与上期同值），但**口径已变，跨期不可直接相减**。

**④ 下期（`075`）强制动作 —— 出刊前逐条过**：

1. **`MiniMax` 第三版会不会再来**：新版（无截止日、`1660` 万像素门槛）是否仍在；若又被撤，**连续两次「撤了又挂」就要改判为「常态轮换」，不再当异常写**。
2. **`Antigravity` 三个模型**：`Will be removed on November 18, 2026.` 是否终于改成过去时；免费档是否只剩 `Gemini 3.8 Flash`。**本期是第 `2` 天，下期若无变化写「连续 `3` 期未执行」。**
3. **`AutoClaw` `M11W4`（`11/23` 00:00 起）**：额度是否真到账 `100M`；`M11W3` 在 `11/22 23:59` 结束后，`11/22 23:59`–`11/23 00:00` 之间是否出现「无额度」窗口。
4. **`ERNIE 5.5 Flash Preview`（`11/25`，剩 `5` 天）**：`?author=baidu` 是否从 `39` 变 `40`。**本季最后一个「官方给了日期」的开源承诺。**
5. **`OpenRouter`**：`477` 与 `:free` `12` 是否继续减；`pixtral-large-2502` 是否出现 `:free` 变体；`gpt-6.2` 是否第 `4` 天仍无免费档。
6. **`Ling 3.2 Flash`**：新接通的 `1` 条路由是否稳定、权重仓是否仍 `404`（三层只开两层）。
7. **`Hy4`**：`?search=Hy4` 是否从 `85` 继续增；主仓 `downloads` 是否破 `5,000`；官方三仓 `likes` 是否过 `500`。
8. **`Kimi`**：`K2` 系列「`12` 月底下线」是否给出确切日；文件接口「限时免费」是否改成有期限的表述。
9. **`OpenCode`**：免费段是否仍 `12` 条；`GLM-5.3-Flash Free` 的弃用表行是否终于删掉（不同步第 `3` 期）。
10. **`Runware` 数组**：`2026-11-19` 那 `5` 处到期后是否被换掉；`h3-image` 徽标是否仍 `0`。**若「徽标卸、数组留」再出现一次，就是第 `16` 次实证。**
11. **三条长期缺口**：`lmarena.ai` 是否结束第 `8` 期 `000`；`hunyuan.tencent.com` 的 `JS` 壳（第 `6` 期，`6,584` 字节）；`chatgpt.com/pricing` 是否可读（第 `3` 期 `000`）。
12. **`腾讯云` `DeepSeek` 原厂搜索计费（第三方口径）**：有中文速报称「`11/18 00:00` 起按 `100` 积分/千次（＝`5` 元）计入套餐」。**本报本期在官方文档未核到对应条文，故未进表体** —— 下期若在 `cloud.tencent.com` 抄到逐字，再补登并标「媒体转述已核实」。
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

TAIL = """> **其余 `142` 条常驻权益本期无变化，未逐条重印** —— 全量见《[常驻权益总账](常驻权益总账.md)》（`192` 条）。**`4.2` 只收「本期真正动过的 `50` 条」**；这 `50` 条与总账是同源副本，**不重复计数**。⚠️ 这 `142` 条沿用上期读数、**本期未逐个重取** —— 不写成「已复核」。

"""

i = md.index("### ④ 本期第四章脚注")
md = md[:i] + TAIL + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(MD, encoding="utf-8").read()
assert "其余 `142` 条" in disk
assert "**④ 下期（`075`）强制动作" in disk
assert "A38 + B10 + C3 + D203 + E5 = 259" in disk
print("footnote ok | bytes", len(disk.encode()))
print("色标：", dict(color), "｜classify：", dict(cls))
