# -*- coding: utf-8 -*-
"""073 期：重写第四章脚注（四段）+ 补回 4.2 收尾段。"""
import csv
import datetime
import io
import re
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第073期-2026-11-19.md"
T = datetime.date(2026, 11, 19)

rows = list(csv.DictReader(io.open(WS + ".workbuddy/data/deadlines.csv", encoding="utf-8-sig")))
assert len(rows) == 256, len(rows)


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
assert (nA, nB, nC, nD, nE) == (38, 9, 3, 201, 5), (nA, nB, nC, nD, nE)
assert nA + nB + nC + nD + nE == len(rows) == 256, (nA, nB, nC, nD, nE, len(rows))

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
assert sum(color.values()) == 256, sum(color.values())
assert sum(cls.values()) == 256

FOOT = """### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-19` 实跑；CSV 共 `256` 条 ＝ 本章可见 `4.1` 的 `66` 行 ＋ 本章 `4.2` 与《常驻权益总账》合并去重后的 `190` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`{nA}` 条（072 期 `36`，`+2`）** —— **进 `2`、出 `0`**：进 = **`Google Antigravity` 三模型**（`11/18` 到期**未执行**）与 **`MiniMax M2.5 / M2.7` 退役**（`11/18`），两条都从 `B` 落进「已过」；`MiniMax 4K` 五折同日到期但**本期已撤净**，直接转 `C`、不进 `A`。**这 `2` 条不是「漏收口」，是「官方没动」** —— 与其余 `36` 条「过期了没人收口」的长尾性质不同。
  {listA}
- **【B】14 天内到期：`{nB}` 条（072 期 `11`）** —— **出 `3`**（`Antigravity` 三模型、`MiniMax M2.5 / M2.7` 转 `A`；`MiniMax 4K` 转 `C`）、**进 `1`**（`腾讯混元` `Reddit` `AMA`，北京 `11/21` 凌晨）；`11/22` 两条、`11/25` 的 `ERNIE 5.5` 剩 `6` 天、`11/29` 的 `Hy4 flash` 限免剩 `10` 天；`11/30` 三条仍 `T+11`。
  {listB}
- **【C】已结束：`{nC}` 条（072 期 `2`，`+1`）** —— 新增 **`MiniMax H3-Image` `4K` 五折**（`11/18 00:00` 到期、**本期价目回位 + `6` 处徽标清零**，按「货架」判收口）；另两条仍是 `Runware` 的 `30% OFF`（`11/15`）与 `4K 50% OFF`（`11/17`）。**⚠️ `MiniMax` 这次收口方式是「改价目」，`Runware` 是「卸徽标」—— 两条同类促销、两种判据（避坑 315）。**
- **【D】日期无法解析：`{nD}` 条（072 期 `197`，`+4`）** —— 本期补入 `4` 条无截止日的常驻权益（`DeepSeek` 服务端搜索不计费、`DeepSeek` 应用端限额、`Phai-A1` 开放权重、`MatOS` 开源），无归档移出，净 `+4`。`D ≠ 失效`。
- **【E】窗口外（>14 天）：`{nE}` 条** —— `12/09` 杭州全城 Coding 计划、`12/31` 四条（`Gemini 3.8 Flash` 促销价、`Moonshot K2` 下线、`Runway` 企业版、`腾讯云 TokenHub` 新人包）。
  **对账：`A{nA} + B{nB} + C{nC} + D{nD} + E{nE} = {total}`，CSV `{total}` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体与总账实算，共 `{total}`）**：

- **色标（状态列行首）**：⚪`{c_o}` / 🔴`{c_r}` / 🟢`{c_g}` / 🟡`{c_y}` / 🟠`{c_p}` / ⚠`{c_w}` / 空`{c_n}` ＝ **`{total}`**
- **`classify()`（状态列语义）**：`crit {k_crit}` / `live {k_live}` / `switch {k_switch}` / `pending {k_pend}` / `unclear {k_unc}` / `over {k_over}` ＝ **`{total}`**

**⚠️ 本期 `over` 与 `⚪` 差 `{diff_over}`（`{k_over}` 对 `{c_o}`）** —— 其余各组：`🔴{c_r}` vs `crit{k_crit}`、`🟢{c_g}` vs `live{k_live}`、`🟠{c_p}` vs `switch{k_switch}`、`🟡{c_y}` vs `pending{k_pend}`、`⚠{c_w}` vs `unclear{k_unc}`。**色标是「谁写的」，`classify()` 是「写的是什么」，不该指望相等；差额必须逐条归因、不当常数。**

**③ 逐行 diff（本期改写 `15` 行状态列 ＋ 补入 `5` 行 ＋ 收口 `1` 行 ＋ 归档 `0` 行）**：

- **改写 `15` 行**：`4.1` 里 `6` 行（`腾讯老混元`（手算天数）、`Hy4 flash 限免`、`MiniMax 4K`、`Runware 4K 50%`、`Antigravity 三模型`、`ERNIE 5.5`）、`4.2` 里 `9` 行（`OpenRouter 免费档`、`Token 羊毛`、`Antigravity 个人免费档`、`ERNIE-5.5-Flash-Base`、`Inkling`、`OpenCode 免费清单`、`LongCat-2.5`、`Hy4 开放权重`、`GPT-6.2`）。**全部走「整体替换状态列」。**
- **补入 `5` 行**：`4.1` 的 **`腾讯混元` `Reddit` `AMA`**；`4.2` 的 **`DeepSeek` 服务端搜索不计费**、**`DeepSeek` 应用端限额**、**`Phai-A1` 开放权重**、**`MatOS` 开源**，均带 `073 期补入` 标记。
- **只改天数 `43` 行**（与上面 `15` 行部分重叠）：带天数的每一处都按「截止日 − `2026-11-19`」重算，脚本末尾逐行带符号比对。`腾讯老混元` 的「`2026` 年 `9` 月底」不可解析，**手算 `已过 50` 天**（`09-30` 起算），另两处手工推进（`Q04` 第 `46` 期、高危窗口第 `37` 天）。
- **收口 `1` 行**：`MiniMax` 的 `4K` 五折 —— **价目回到 `0.4522` / `0.4809` / `0.5211`、`6` 处徽标清零、`0.2261` 与 `0.2404` 整页 `0` 命中**，按「货架」判收口。**`A` 不受影响，`B` 与 `C` 同步一减一增。**
- **归档 `0` 行** —— 过期条目里已收口的两条 `Runware` 促销（`11/15`、`11/17`）**都在 `7` 天宽限内，不移出表体**。

**⚠️ 一处口径修正（本期自查）**：`DeepSeek` 服务端搜索那行的截止列**原本写了 `11/18 12:00`**，被 `check_deadlines` 当成「有截止日」扫进 `A` 桶 —— **它是计费规则变更、没有截止日**。已把日期移进状态列、截止列改写「即时生效」，`A` 因此少 `1`、`D` 多 `1`。**这类「正文里的日期被解析器当成截止日」的坑，本期第 `2` 次踩到**（第一次是 `AMA` 行的 PT 时间被读成次日）。

**④ 下期（`074`）强制动作 —— 出刊前逐条过**：

1. **`Antigravity` 三个模型到底撤不撤**：`Will be removed on November 18, 2026.` 这句是否终于改成过去时、免费档是否只剩 `Gemini 3.8 Flash` 或补进 `Gemini 4` 系列。**本期已给「到期未执行」的结论，下期要么给「已执行」、要么写「连续 `2` 期未执行」。**
2. **`MiniMax 4K` 撤净之后有没有新促销**：同页 `即日起至` 是否重新出现、`0.2261` 是否再被挂上；若有，必须写「新一期促销」，不能与 `11/18` 那期合并。
3. **`DeepSeek` 的三件事**：服务端搜索免费是否写进 `News` / `Change Log`；应用端限额是否出正式公告；免费档是否出现 C 端付费方案（前端已有「额度耗尽」提示）。
4. **混元 `AMA`（北京 `11/21` 00:00–02:00）**：`§10` 商用门槛是否被解释、是否有明确豁免口径、是否公布 `Hy4 flash` 后续版本时间表。
5. **`Phai-A1` 的 `24` 小时**：`downloads` 是否从 `9` 起量、是否出现第三方 `GGUF` / `MLX` 转档、`Phai-M1` 仓是否上 `HF` 或 `ModelScope`。
6. **`MatOS`**：`GitHub` `stars` / `issues` 是否起量、是否有第三方复现 `ResearchClawBench +33.6%`。
7. **`ERNIE 5.5 Flash Preview`（`11/25`，剩 `6` 天）**：`?author=baidu` 是否从 `39` 变 `40`。**本季最后一个「官方给了日期」的开源承诺。**
8. **`AutoClaw` `M11W4`（`11/23` 起）**：`/blog/news/M11W4/` 是否从 `404` 变 `200`、额度是否维持 `100M`。`M11W3` 到 `11/22`。
9. **`OpenRouter`**：`480` 是否再变；`:free` 是否第 `7` 天仍 `14`；`gpt-6.2` 是否出现 `:free`；`Ling 3.2 Flash` 的 `endpoints` 是否结束 `7` 天空窗。
10. **`HF`**：`Hy4` 三仓 `downloads` 是否破 `500`、`AngelSlim` `GGUF` 是否反超主仓；`Inkling` 下期可算环比（本期已有基线 `30,082`）。
11. **`Runware` 的促销数组**：`minimax-h3-image-launch-promo` 是否被删（已连挂 `3` 期）；`pruna-p-video-2-pro-replace`（`endsAt: 2026-11-19`）到期后徽标是否归零 —— **若「徽标卸、数组留」再出现一次，就是第 `14` 次实证。**
12. **三条长期缺口**：`lmarena.ai` 是否结束第 `7` 期 `000`；`hunyuan.tencent.com` 的 `JS` 壳（第 `5` 期，`6,584` 字节）；`chatgpt.com/pricing` 是否可读（第 `2` 期 `000`）。
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

TAIL = """> **其余 `142` 条常驻权益本期无变化，未逐条重印** —— 全量见《[常驻权益总账](常驻权益总账.md)》（`190` 条）。**`4.2` 只收「本期真正动过的 `48` 条」**；这 `48` 条与总账是同源副本，**不重复计数**。⚠️ 这 `142` 条沿用上期读数、**本期未逐个重取** —— 不写成「已复核」。

"""

i = md.index("### ④ 本期第四章脚注")
md = md[:i] + TAIL + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(MD, encoding="utf-8").read()
assert "其余 `142` 条" in disk
assert "**④ 下期（`074`）强制动作" in disk
assert "A38 + B9 + C3 + D201 + E5 = 256" in disk
print("footnote ok | bytes", len(disk.encode()))
print("色标：", dict(color), "｜classify：", dict(cls))
