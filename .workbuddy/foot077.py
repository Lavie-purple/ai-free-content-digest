# -*- coding: utf-8 -*-
"""077 期：重写第四章脚注（四段）+ 补回 4.2 收尾段。"""
import csv
import datetime
import io
import re
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第077期-2026-11-23.md"
T = datetime.date(2026, 11, 23)

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
        buckets["D"].append((0, datetime.date(2026, 1, 1), r))
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
assert (nA, nB, nC, nD, nE) == (38, 8, 5, 206, 5), (nA, nB, nC, nD, nE)
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

**① 三态分布（`check_deadlines.py --today 2026-11-23` 实跑；CSV 共 `262` 条 ＝ 本章可见 `4.1` 的 `67` 行 ＋ 本章 `4.2` 与《常驻权益总账》合并去重后的 `195` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`{nA}` 条（076 期 `37`，`+1`）** —— **进 `1` 出 `0`**。进的是 **`虎鲸文娱`「鲸锐 AI 创作大赛」（`11/22` 到期，状态仍非收口）**。桶内最该看的两条没变：`腾讯老混元` 停服（`09-30`，**已过 `54` 天，厂商仍只给「9 月底」**）、`MiniMax M2.5 / M2.7` 退役（`11/18`）。
  {listA}
- **【B】14 天内到期：`{nB}` 条（076 期 `10`，`−2`）** —— **出 `2` 进 `0`**：`虎鲸文娱`（`11/22` → 归 `A`）、`AutoClaw M11W3`（`11/22 23:59` 收口 → 归 `C`）。剩下 `8` 条全部落在 `T+2`–`T+7`：`ERNIE 5.5` `T+2`、天猫 `T+5`、`Hy4 flash` 限免与 `M11W4` `T+6`、`Character.AI` / `Antigravity` / `Gemini 4 Argon` / `Runway Kling` `T+7`。
  {listB}
- **【C】已结束：`{nC}` 条（076 期 `4`，`+1`）** —— **进 `1` 出 `0`**：新进 **`AutoClaw M11W3`（`11/22 23:59` 收口）**。另四条仍在：`Runware` `H3 Max`（`11/15`）、`Runware` `4K 50%`（`11/17`）、`MiniMax` `4K` 五折**旧版**（`11/18`）、`Hy4` `AMA`（`11/21`）。**⚠️ `MiniMax` 那条仍只是「旧版结束」** —— 现行第二版仍在架（见 `4.2`），**在 `C` 里算收口、在正文里还活着**（避坑 317）。
- **【D】日期无法解析：`{nD}` 条（076 期 `206`，`0`）** —— 本期**没有补入任何无截止日的常驻权益**（`4.2` 行数 `53` 不变、总账 `195` 条不变）。`D ≠ 失效`。
- **【E】窗口外（>14 天）：`{nE}` 条（`0`）** —— `12/09` 杭州全城 Coding 计划、`12/31` 四条（`Gemini 3.8 Flash` 促销价、`Moonshot K2` 下线、`Runway` 企业版、`腾讯云 TokenHub` 新人包）。
  **对账：`A{nA} + B{nB} + C{nC} + D{nD} + E{nE} = {total}`，CSV `{total}` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体与总账实算，共 `{total}`）**：

- **色标（状态列行首）**：⚪`{c_o}` / 🔴`{c_r}` / 🟢`{c_g}` / 🟡`{c_y}` / 🟠`{c_p}` / ⚠`{c_w}` / 空`{c_n}` ＝ **`{total}`**
- **`classify()`（状态列语义）**：`crit {k_crit}` / `live {k_live}` / `switch {k_switch}` / `pending {k_pend}` / `unclear {k_unc}` / `over {k_over}` ＝ **`{total}`**

**⚠️ 本期 `over` 与 `⚪` 差 `{diff_over}`（`{k_over}` 对 `{c_o}`）** —— 其余各组：`🔴{c_r}` vs `crit{k_crit}`、`🟢{c_g}` vs `live{k_live}`、`🟠{c_p}` vs `switch{k_switch}`、`🟡{c_y}` vs `pending{k_pend}`、`⚠{c_w}` vs `unclear{k_unc}`。**色标是「谁写的」，`classify()` 是「写的是什么」，不该指望相等；差额必须逐条归因、不当常数。**

**③ 逐行 diff（本期改写 `26` 行状态列 ＋ 补入 `0` 行 ＋ 收口 `1` 行 ＋ 改期 `0` 行 ＋ 归档 `0` 行）**：

- **改写 `26` 行**：`4.1` 里 `12` 行（`腾讯老混元`（手算天数）、`Hy4 flash 限免`、`Hy4 AMA`、`ERNIE 5.5`、`MiniMax 4K`、`Runway Kling 4.0`、`Runway 企业版`、`Runware 4K 50%`、`Runware H3 Max`、`AutoClaw M11W3`、`AutoClaw M11W4`、`Antigravity 三模型`）、`4.2` 里 `14` 行（`OpenRouter 免费档`（改名 `477/15/12`）、`OpenCode 免费清单`（改名 `11` 条）、`Token 羊毛`、`Antigravity 个人免费档`、`ERNIE-5.5-Flash-Base`、`Inkling 2 Mini`、`inkling-2-mini` 的 API 入口（改名 `4` 个价点）、`Inkling 2 Small`、`Hy4 flash`、`Hy4`（`770B`）、`LongCat-2.5`、`GPT-6.2`、`Ling 3.2`、`MiniMax 4K 第二版`）。**全部走「整体替换状态列」。**
- **补入 `0` 行**：本期没有新的常驻权益。**`4.2` 仍是 `53` 条、总账仍是 `195` 条。**
- **只改天数 `45` 行**（与上面 `26` 行部分重叠）：带天数的每一处都按「截止日 − `2026-11-23`」重算。`腾讯老混元` 的「`2026` 年 `9` 月底」不可解析，**手算 `已过 54` 天**（`09-30` 起算），另两处手工推进（`Q04` 第 `50` 期、高危窗口第 `41` 天）。
- **收口 `1` 行**：`AutoClaw M11W3` **`B → C`**（`11/22 23:59` 到期、状态改 `⚪`）。**改期 `0`、归档 `0`** —— 过期 >7 天且已收口的条目本期没有新增（最老的一条 `Runware Kling 15% OFF` 是 `10/29`、已归档过）。

**④ 下期（`078`）强制动作 —— 出刊前逐条过**：

1. **`ERNIE 5.5 Flash Preview`（`11/25` 前，剩 `2` 天）**：**本期已是最后一次「无结论」，`078` 期必须给判定** —— 放权重，或写「官方给了日期但未做到」；`?author=baidu` 是否从 `39` 变 `40`；发布页是否出现 `权重已开源`。
2. **`OpenRouter` 的 `477 / 15 / 12 / 14`**：**`dots-3-note-preview:free` 是否连续第 `2` 期在目录里** —— 若在，把 076–077 的「消失—回归」记为「抖动一次」并结案；若再消失，改记「周期性上下架」。`gpt-6.2` 第 `7` 天是否仍无免费档。
3. **`OpenCode` 的 `11` 条**：是否继续降；`Tidepool Alpha Free` 是否转正；**`Jev 1.14` 是否出现 `-free` 变体**（若出现，是「新版本先收费、后免费」的第二次样本）；弃用表是否再换行。
4. **`inkling-2-mini` 的 `4` 个价点**：是否稳定（`$0.0375 / $0.075 / $0.12` ＋ `Io Net $0.12`）；`Io Net` 是否再涨；是否出现 `:free`；`PrimeIntellect` 的档位说明是否写进模型页。
5. **`HF` `downloads`**：本期第三次全仓同向上跳。**下期若继续动，写「批次周期 <1 天」；若全冻，写「第 `2` 次冻结」。`likes` 是否再出现「跌了又精确补回」** —— 若出现第二次，把「周期性重算」写成定论。
6. **`Antigravity`（`11/30`，剩 `7` 天）**：脚注是否仍 `11/30`；**`11/30` 过后三个第三方模型是否真移除** —— 它已给过三次日期，这次要验真。
7. **`MiniMax` 第二版第 `5` 天**：是否仍在架、六档价是否仍为 `0.2261`–`0.5073`。
8. **`Runware`**：`11-23` 那两条到期后，**`11/24` 再看数组是否仍是 `2` 条** —— 这是「账本不滚动」的第二次反向检验；`h3-image` 是否仍 `18`。
9. **`Token 羊毛` 新口径第 `2` 期**：`¥821` 是否继续降；卡册 `61 → ?`；**规则段是否再改**（若再改，序列再断一次）。
10. **`freellm`**：自述 `512+` 是否继续降；是否再补录新家。
11. **三条长期缺口**：`lmarena.ai` 是否结束第 `11` 期 `000`；`hunyuan.tencent.com` 的 `JS` 壳（第 `10` 期）；`chatgpt.com/pricing` 第 `7` 期是否可读。
12. **`GLM-5.4` 的落地核查**：`z.ai` 首页是否换成 `5.4`；`open.bigmodel.cn/pricing` 是否给出 API 单价（本期 `JS` 壳、`0` 字节）；`OpenRouter` 是否上架；**是否出现免费档或试用**。
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

TAIL = """> **其余 `142` 条常驻权益本期无变化，未逐条重印** —— 全量见《[常驻权益总账](常驻权益总账.md)》（`195` 条）。**`4.2` 收录 `53` 条在跟踪的常驻权益，其中本期改写 `14` 条、补入 `0` 条、其余 `39` 条沿用上期读数**；这 `53` 条与总账是同源副本，**不重复计数**。⚠️ 这 `142` 条沿用上期读数、**本期未逐个重取** —— 不写成「已复核」。

"""

i = md.index("### ④ 本期第四章脚注")
md = md[:i] + TAIL + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(MD, encoding="utf-8").read()
assert "其余 `142` 条" in disk
assert "**④ 下期（`078`）强制动作" in disk
assert "A38 + B8 + C5 + D206 + E5 = 262" in disk, [l for l in disk.split("\n") if "对账：" in l]
print("footnote ok | bytes", len(disk.encode()))
print("色标：", dict(color), "｜classify：", dict(cls))
