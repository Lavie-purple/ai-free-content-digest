# -*- coding: utf-8 -*-
"""078 期：重写第四章脚注（四段）+ 补回 4.2 收尾段。"""
import csv
import datetime
import io
import re
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第078期-2026-11-24.md"
T = datetime.date(2026, 11, 24)

rows = list(csv.DictReader(io.open(WS + ".workbuddy/data/deadlines.csv", encoding="utf-8-sig")))
assert len(rows) == 263, len(rows)


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
assert (nA, nB, nC, nD, nE) == (38, 7, 6, 207, 5), (nA, nB, nC, nD, nE)
assert nA + nB + nC + nD + nE == len(rows) == 263, (nA, nB, nC, nD, nE, len(rows))

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
assert sum(color.values()) == 263, sum(color.values())
assert sum(cls.values()) == 263

FOOT = """### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-24` 实跑；CSV 共 `263` 条 ＝ 本章可见 `4.1` 的 `67` 行 ＋ 本章 `4.2` 与《常驻权益总账》合并去重后的 `196` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`{nA}` 条（077 期 `38`，`0`）** —— **进出相抵**。出的是 `虎鲸文娱`「鲸锐 AI 创作大赛」（`11/22` 到期、本期已在 `C`）；**进 `0`**。桶内最该看的两条没变：`腾讯老混元` 停服（`09-30`，**已过 `55` 天，厂商仍只给「9 月底」**）、`MiniMax M2.5 / M2.7` 退役（`11/18`）。
  {listA}
- **【B】14 天内到期：`{nB}` 条（077 期 `8`，`−1`）** —— **出 `1` 进 `0`**：`ERNIE 5.5 Flash Preview`（`11/25` 前，**`11/23 17:00` 权重已上线 → 归 `C`**）。剩下 `7` 条全部落在 `T+1`–`T+6`：天猫 `T+1`、`Hy4 flash` 限免与 `M11W4` 与 `Antigravity` 与 `Runway Kling` 与 `Gemini 4 Argon` `T+6`、`Character.AI`（`11/28`）。
  {listB}
- **【C】已结束：`{nC}` 条（077 期 `5`，`+1`）** —— **进 `1` 出 `0`**：新进 **`ERNIE 5.5 Flash Preview`（`11/23 17:00` 权重上线、承诺兑现，状态改 `⚪`）**。另五条仍在：`Runware` `H3 Max`（`11/15`）、`Runware` `4K 50%`（`11/17`）、`MiniMax` `4K` 五折**旧版**（`11/18`）、`Hy4` `AMA`（`11/21`）、`AutoClaw` `M11W3`（`11/22 23:59`）。**⚠️ `MiniMax` 那条仍只是「旧版结束」** —— 现行第二版仍在架（见 `4.2`），**在 `C` 里算收口、在正文里还活着**（避坑 317）。
- **【D】日期无法解析：`{nD}` 条（077 期 `206`，`+1`）** —— 本期**补入 `1` 条无截止日的常驻权益**（`ERNIE-5.5-Flash-Preview` 开放权重，`4.2` 行数 `53 → 54`、总账 `195 → 196`）。`D ≠ 失效`。
- **【E】窗口外（>14 天）：`{nE}` 条（`0`）** —— `12/09` 杭州全城 Coding 计划、`12/31` 四条（`Gemini 3.8 Flash` 促销价、`Moonshot K2` 下线、`Runway` 企业版、`腾讯云 TokenHub` 新人包）。
  **对账：`A{nA} + B{nB} + C{nC} + D{nD} + E{nE} = {total}`，CSV `{total}` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体与总账实算，共 `{total}`）**：

- **色标（状态列行首）**：⚪`{c_o}` / 🔴`{c_r}` / 🟢`{c_g}` / 🟡`{c_y}` / 🟠`{c_p}` / ⚠`{c_w}` / 空`{c_n}` ＝ **`{total}`**
- **`classify()`（状态列语义）**：`crit {k_crit}` / `live {k_live}` / `switch {k_switch}` / `pending {k_pend}` / `unclear {k_unc}` / `over {k_over}` ＝ **`{total}`**

**⚠️ 本期 `over` 与 `⚪` 差 `{diff_over}`（`{k_over}` 对 `{c_o}`）** —— 其余各组：`🔴{c_r}` vs `crit{k_crit}`、`🟢{c_g}` vs `live{k_live}`、`🟠{c_p}` vs `switch{k_switch}`、`🟡{c_y}` vs `pending{k_pend}`、`⚠{c_w}` vs `unclear{k_unc}`。**色标是「谁写的」，`classify()` 是「写的是什么」，不该指望相等；差额必须逐条归因、不当常数。**

**③ 逐行 diff（本期改写 `26` 行状态列 ＋ 补入 `1` 行 ＋ 收口 `1` 行 ＋ 改期 `0` 行 ＋ 归档 `0` 行）**：

- **改写 `26` 行**：`4.1` 里 `12` 行（`腾讯老混元`（手算天数）、`Hy4 flash 限免`、`Hy4 AMA`、`ERNIE 5.5`（改 `⚪`）、`MiniMax 4K`、`Runway Kling 4.0`、`Runway 企业版`、`Runware 4K 50%`、`Runware H3 Max`、`AutoClaw M11W3`、`AutoClaw M11W4`、`Antigravity 三模型`）、`4.2` 里 `14` 行（`OpenRouter 免费档`（改名 `474/15/12`）、`OpenCode 免费清单`（改名「本期无进出」）、`Token 羊毛`、`Antigravity 个人免费档`、`ERNIE-5.5-Flash-Base`、`Inkling 2 Mini`、`inkling-2-mini` 的 API 入口（顶档换人）、`Inkling 2 Small`、`Hy4 flash`、`Hy4`（`770B`）、`LongCat-2.5`、`GPT-6.2`、`Ling 3.2`、`MiniMax 4K 第二版`）。**全部走「整体替换状态列」。**
- **补入 `1` 行**：**`百度 ERNIE-5.5-Flash-Preview 开放权重`**（`Apache-2.0` · `280B` / `14B` 激活 · `1M`）—— **`4.2` 由 `53` 条变 `54` 条、总账由 `195` 条变 `196` 条**。**这是本报第一次把「同一次发布」拆成两行登记**（`4.1` 的承诺行收口、`4.2` 的权重行常驻），原因是两者的**生命周期不同**：承诺会过期，权重不会。
- **只改天数 `46` 行**（与上面 `26` 行部分重叠）：带天数的每一处都按「截止日 − `2026-11-24`」重算。`腾讯老混元` 的「`2026` 年 `9` 月底」不可解析，**手算 `已过 55` 天**（`09-30` 起算），另两处手工推进（`Q04` 第 `51` 期、高危窗口第 `42` 天）。
- **收口 `1` 行**：`ERNIE 5.5 Flash Preview` **`B → C`**（承诺兑现、状态改 `⚪`）。**改期 `0`、归档 `0`** —— 过期 >7 天且已收口的条目本期没有新增（最老的一条 `Runware Kling 15% OFF` 是 `10/29`、已归档过）。
- **⚠️ 一处口径踩坑已修**：新补的那行截止列初稿写了「建仓 `11/23 09:00:29Z`」，**被 `extract_deadlines` 当成 `11/23` 解析**（`D` 少 `1`、`A` 多 `1`）。改法是把日期从截止列移到状态列 —— **截止列里不能出现任何可被解析的日期**（058 期纪律的第二次现场）。

**④ 下期（`079`）强制动作 —— 出刊前逐条过**：

1. **`Antigravity`（`11/30`，剩 `6` 天）**：**本期首页 `November 30` 已 `0` 处、`pricing` 页 `000`** —— `079` 必须换路径核实（试 `/docs`、`/blog`、或直接查免费档模型数），**若 `11/30` 后三个第三方模型仍在，就把「移除」改记为「未执行」**。
2. **`AutoClaw` `M11W4`（`11/29 23:59`，剩 `5` 天）**：`M11W5` 是否在 `11/29` 前后挂出（连续第 `3` 期 `404`）；`100M` 是否第 `3` 周维持。
3. **`OpenRouter` 的 `474 / 15 / 12 / 14`**：全量是否继续降（三条 `kimi` / `mimo` 付费模型退出是否成串）；`:free` 是否仍 `12`；**`dots-3-note-preview:free` 用 `%3A` 是否仍 `200`** —— 若某期 `%3A` 也 `404`，才能判「真下架」。
4. **`ERNIE` 三仓的后续**：`downloads` 是否从 `0` 起步、社区是否出 `GGUF`（`unsloth` 名下 `?search=ernie` 本期 `0`）；`OpenRouter` 的 `:free` 是否随权重上线改价。
5. **`HF` `downloads`**：本期整列冻结。**下期若继续冻结，写「批次周期 > 1 天」并给区间；若恢复上跳，给「一次跳多少」的量级。`likes` 是否再现「跌了精确补回」**（若第二次出现，把「周期性重算」写成定论）。
6. **`OpenCode`**：本期整页与上期逐字节相同（第 `1` 次）。**下期若仍同，写「静态期」；`Tidepool Alpha Free` 是否转正、`Jev 1.14` 是否出 `-free`。**
7. **`Runware`**：`11-23` 两条**过期一天仍在**。`079` 看是否仍在（若仍在，改记「永久留档」）；`h3-image` 是否仍 `18`。
8. **`Runway`**：`11/30` 剩 `6` 天 —— `12/01` 那天看 `Kling 4.0 25% off` 是否真撤；`<title>` 是否又被改回带价版本。
9. **`Token 羊毛` 第 `17` 期**：`¥845` 是否继续涨；卡册 `65 → ?`；**规则段是否再改**（本期已确认未改，序列可比）。
10. **`inkling-2-mini`**：顶档 `$0.15 / $0.60` 是否稳定；`Io Net` 是否跟进涨；是否出现 `:free`。
11. **`GLM-5.4` 的 API**：官方逐字已给「完成安全评估后开放」—— `079` 看 `open.bigmodel.cn` 定价页是否出 `5.4` 单价、`z.ai` 首页是否换版、`OpenRouter` 是否上架。
12. **三条长期缺口**：`lmarena.ai` 是否结束第 `12` 期 `000`；`artificialanalysis.ai` 第 `3` 期；`chatgpt.com/pricing` 第 `8` 期是否可读。**另加 `antigravity.google/pricing` 本期新增 `000`，下期用 `curl --http1.1` 再试一次。**
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

TAIL = """> **其余 `143` 条常驻权益本期无变化，未逐条重印** —— 全量见《[常驻权益总账](常驻权益总账.md)》（`196` 条）。**`4.2` 收录 `54` 条在跟踪的常驻权益，其中本期改写 `14` 条、补入 `1` 条、其余 `39` 条沿用上期读数**；这 `54` 条与总账是同源副本，**不重复计数**。⚠️ 这 `143` 条沿用上期读数、**本期未逐个重取** —— 不写成「已复核」。

"""

i = md.index("### ④ 本期第四章脚注")
md = md[:i] + TAIL + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(MD, encoding="utf-8").read()
assert "其余 `143` 条" in disk
assert "**④ 下期（`079`）强制动作" in disk
assert "A38 + B7 + C6 + D207 + E5 = 263" in disk, [l for l in disk.split("\n") if "对账：" in l]
print("footnote ok | bytes", len(disk.encode()))
print("色标：", dict(color), "｜classify：", dict(cls))
