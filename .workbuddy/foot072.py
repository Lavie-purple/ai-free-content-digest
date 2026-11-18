# -*- coding: utf-8 -*-
"""072 期：重写第四章脚注（四段）+ 补回 4.2 收尾段。"""
import csv
import datetime
import io
import re
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第072期-2026-11-18.md"
T = datetime.date(2026, 11, 18)

rows = list(csv.DictReader(io.open(WS + ".workbuddy/data/deadlines.csv", encoding="utf-8-sig")))
assert len(rows) == 251, len(rows)


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
assert (nA, nB, nC, nD, nE) == (36, 11, 2, 197, 5), (nA, nB, nC, nD, nE)
assert nA + nB + nC + nD + nE == len(rows) == 251, (nA, nB, nC, nD, nE, len(rows))

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
assert sum(color.values()) == 251, sum(color.values())
assert sum(cls.values()) == 251

FOOT = """### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-18` 实跑；CSV 共 `251` 条 ＝ 本章可见 `4.1` 的 `65` 行 ＋ 本章 `4.2` 与《常驻权益总账》合并去重后的 `186` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`{nA}` 条（071 期 `36`，净持平）** —— **一进一出**：进 = **`Claude Fable 5.2` 发布优惠**（截止 `11/17 15:59` 北京，今天落进「已过」）；出 = **`Runware` 的 `4K 50% OFF`**（本期徽标清零、**已收口转 `C`**）。**其余 `35` 条只是天数推进。`A` 桶连续四期只增不减，这批是「过期了但没人收口」的长尾，不是待办清单。**
  {listA}
- **【B】14 天内到期：`{nB}` 条（071 期 `12`）** —— **今天到期 `3` 条**（`Antigravity` 三模型移除、`MiniMax 4K` 五折、`MiniMax M2.5 / M2.7` 退役）；`11/22` 两条、`11/25` 的 `ERNIE 5.5` 剩 `7` 天、`11/29` 的 `Hy4 flash` 限免剩 `11` 天；`11/30` 那批从 `T+13` 走到 `T+12`。**出 `2` = `Fable 5.2` 转 `A`、`Runware 4K` 转 `C`。**
  {listB}
- **【C】已结束：`{nC}` 条（071 期 `1`，`+1`）** —— 新增 `Runware` 的 `4K 50% OFF`（`11/17` 到期、**本期徽标 `2 → 0` 已收口**）；另一条仍是 `Runware` 的 `30% OFF`（`11/15`）。**⚠️ 这两条同属「分发层到期」，但 `MiniMax` 官方页的同一档促销 `11/18 00:00` 到期后仍在挂 —— 官方侧不收口，`C` 桶只收分发层那一条。**
- **【D】日期无法解析：`{nD}` 条（071 期 `195`，`+2`）** —— 本期补入 `2` 条无截止日的常驻权益（`腾讯 Hy4 flash` 开放权重、`OpenAI GPT-6.2` 发布），无归档移出，净 `+2`。`D ≠ 失效`。
- **【E】窗口外（>14 天）：`{nE}` 条** —— `12/09` 杭州全城 Coding 计划、`12/31` 四条（`Gemini 3.8 Flash` 促销价、`Moonshot K2` 下线、`Runway` 企业版、`腾讯云 TokenHub` 新人包）。
  **对账：`A{nA} + B{nB} + C{nC} + D{nD} + E{nE} = {total}`，CSV `{total}` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体与总账实算，共 `{total}`）**：

- **色标（状态列行首）**：⚪`{c_o}` / 🔴`{c_r}` / 🟢`{c_g}` / 🟡`{c_y}` / 🟠`{c_p}` / ⚠`{c_w}` / 空`{c_n}` ＝ **`{total}`**
- **`classify()`（状态列语义）**：`crit {k_crit}` / `live {k_live}` / `switch {k_switch}` / `pending {k_pend}` / `unclear {k_unc}` / `over {k_over}` ＝ **`{total}`**

**⚠️ 本期 `over` 与 `⚪` 差 `{diff_over}`（`{k_over}` 对 `{c_o}`）** —— 其余各组仍各差 `1` 上下（`🔴{c_r}` vs `crit{k_crit}`、`🟢{c_g}` vs `live{k_live}`、`🟠{c_p}` vs `switch{k_switch}`、`🟡{c_y}` vs `pending{k_pend}`、`⚠{c_w}` vs `unclear{k_unc}`）。**色标是「谁写的」，`classify()` 是「写的是什么」，不该指望相等；差额必须逐条归因、不当常数。**

**③ 逐行 diff（本期改写 `15` 行状态列 ＋ 补入 `2` 行 ＋ 收口 `1` 行 ＋ 归档 `0` 行）**：

- **改写 `15` 行**：`4.1` 里 `6` 行（`腾讯老混元`（手算天数）、`Hy4 flash 限免`、`MiniMax 4K`、`Runware 4K 50%`、`Antigravity 三模型`、`ERNIE 5.5`）、`4.2` 里 `9` 行（`OpenRouter 免费档`、`Token 羊毛`、`Antigravity 个人免费档`、`ERNIE-5.5-Flash-Base`、`Inkling-2-Small`、`OpenCode 免费清单`、`Praxis-1`、`PEAR`、`LongCat-2.5`）。**全部走「整体替换状态列」。**
- **补入 `2` 行**：`4.2` 的 **`腾讯 Hy4 flash 开放权重`** 与 **`OpenAI GPT-6.2 Astra / Sol 发布`**，均带 `072 期补入` 标记。
- **只改天数 `46` 行**（与上面 `15` 行部分重叠）：带天数的每一处都按「截止日 − `2026-11-18`」重算，脚本末尾逐行带符号比对。`腾讯老混元` 的「`2026` 年 `9` 月底」不可解析，**手算 `已过 49` 天**（`09-30` 起算），另两处期数手工推进（`Q04` 第 `45` 期、高危窗口第 `36` 天）。
- **收口 `1` 行**：`Runware` 的 `4K 50% OFF` —— **促销数组里那条 `endsAt: "2026-11-17"` 仍在，但卡片徽标 `2 → 0`**，按「货架」判收口（避坑 312）。**`A` 与 `C` 因此同步一减一增。**
- **归档 `0` 行** —— 过期条目里已收口的只有两条 `Runware` 促销（`11/15`、`11/17`），**都在 `7` 天宽限内，不移出表体。**

**④ 下期（`073`）强制动作 —— 出刊前逐条过**：

1. **`MiniMax 4K` 的「该撤没撤」有没有下文**：官方页那行「即日起至 `2026 年 11 月 18 日 00:00」是否被改成新日期、`6` 处「限时5折」徽标是否撤、`0.4522` 是否回到唯一价。**这是本期头条级的口径矛盾，`073` 必须给结论，不给就写「连续第 `2` 期矛盾」。**
2. **`Antigravity` 定价页能否恢复**（`000` 第 `3` 期）：恢复了就一次核完三件事 —— 三条第三方模型是否已移除、免费档是否只剩 `Gemini 3.8 Flash`、`Baseline agent quota` 是否出现数字。
3. **`GPT-6.2` 的免费档**：`chatgpt.com/pricing` 是否可读、`openai.com/api/pricing` 是否补上 `gpt-6.2`、免费档是否出现 `GPT-6.2`（哪怕限次）。
4. **`Hy4 flash` 开权重后 24 小时**：`downloads` 是否从 `0` 起量、`likes` 是否破 `200`、第三方 `GGUF` / `MLX` 转档是否增多；`ModelScope` 页是否脱离 `JS` 壳。
5. **`OpenAI` 学术计划 `11/23` 开放申请**：名额是否真是 `50,000`、申请页是否给出关闭日、`Plus` 的额度与模型是否出现数字。
6. **`OpenCode` 的 `Free models` 段**：`GLM-5.3-Flash Free` 是否已从清单消失（弃用日就是今天）、是否又有新条目补位、`hy4-flash-free` 是否第 `7` 天仍在。
7. **`AutoClaw` 的 `M11W4`（`11/23` 起）**：`/blog/news/M11W4/` 是否从 `404` 变 `200`、额度是否维持 `100M`。
8. **`OpenRouter`**：`478` 是否再变；`:free` 是否第 `6` 天仍 `14`；`gpt-6.2` 是否出现 `:free` 或折扣变体；`Ling 3.2 Flash` 的 `endpoints` 是否结束 `6` 天空窗。
9. **`ERNIE 5.5 Flash Preview` 的 `11/25`（剩 `7` 天）**：`?author=baidu` 是否从 `39` 变 `40`。**这是本季最后一个「官方给了日期」的开源承诺。**
10. **`Runware` 的促销数组**：`minimax-h3-image-launch-promo` 那条是否被删（本期只卸徽标、数组仍留）；若被删，说明「账本」也开始清扫，`12` 次实证的规律要改写。
11. **`HF` 的 `Inkling`**：`429` 是否解除；`downloads` 能否取得 —— **连续 `2` 期取不到就改「只记 `likes`」。**
12. **两条长期缺口**：`hunyuan.tencent.com` 是否仍是 `6,894` 字节的 `JS` 壳（第 `4` 期）；`lmarena.ai` 是否结束第 `6` 期 `000`（本期仍未恢复）。
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

TAIL = """> **其余 `142` 条常驻权益本期无变化，未逐条重印** —— 全量见《[常驻权益总账](常驻权益总账.md)》（`186` 条）。**`4.2` 只收「本期真正动过的 `44` 条」**；这 `44` 条与总账是同源副本，**不重复计数**。⚠️ 这 `142` 条沿用上期读数、**本期未逐个重取** —— 不写成「已复核」。

"""

i = md.index("### ④ 本期第四章脚注")
md = md[:i] + TAIL + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(MD, encoding="utf-8").read()
assert "其余 `142` 条" in disk
assert "**④ 下期（`073`）强制动作" in disk
assert "A36 + B11 + C2 + D197 + E5 = 251" in disk
print("footnote ok | bytes", len(disk.encode()))
print("色标：", dict(color), "｜classify：", dict(cls))
