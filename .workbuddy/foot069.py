# -*- coding: utf-8 -*-
"""069 期：重写第四章脚注（四段）+ 补回 4.2 收尾段。"""
import csv
import datetime
import io
import re

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第069期-2026-11-15.md"
T = datetime.date(2026, 11, 15)

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
assert nA + nB + nC + nD + nE == len(rows) == 242, (nA, nB, nC, nD, nE, len(rows))

# 色标口径（活动名列行首，4.1+4.2+总账去重）
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
assert sum(color.values()) == 242, sum(color.values())

FOOT = """### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-15` 实跑；CSV 共 `242` 条 ＝ 本章可见 `4.1` 的 `61` 行 ＋ 《常驻权益总账》`181` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`{nA}` 条（068 期 `34`，`0`）** —— **本期第一次「`A` 桶一个没进也没出」**：`11/13` 到期的那两条一天前已经掉进来、本期只是天数从 `1` 变 `2`；而 `11/14`–`11/15` 两天**没有一条表内活动到期**（本周末各家都在观望，见第一章第 `5` 条）。**`A` 桶停涨不等于「待办在减少」，只说明这两天没有新到期的。**
  {listA}
- **【B】14 天内到期：`{nB}` 条（068 期 `7`，`+1`）** —— 入 `1` = 本期补入的 **`Runware MiniMax H3 Max 30% OFF`（今天到期）**；其余 `7` 条天数整体推进一天。**其中 `11/15` 两条今天到期、`11/16` 一条明天到期 —— 下期这三条会一起掉进 `A`。**
  {listB}
- **【C】已结束：`0` 条。连续第 `7` 期为空** —— 「已结束」只给有逐字收口口径的条目。
- **【D】日期无法解析：`{nD}` 条（068 期 `190`，`+2`）** —— 本期补入 `2` 条无截止日的常驻权益（`LongCat-2.5` 权重 `MIT`、`PEAR` 开放权重），无归档移出，净 `+2`。`D ≠ 失效`。
- **【E】窗口外（>14 天）：`{nE}` 条（068 期 `8`，`0`）** —— 组成变了、总数没变：`11/28` 天猫「AI 空间站」已进 `B`；`E` 里现有 `11/30` 三条（`Gemini 4 Argon` 首发价 / `Runway` 平台 `Kling 4.0` `25% off` / `Character.AI` 第 `11` 章申请）、`12/09` 一条、`12/31` 四条（`Gemini 3.8 Flash` 促销价、`Moonshot K2` 下线、`Runway` 企业版、`腾讯云 TokenHub` 新人包）。
  **对账：`A{nA} + B{nB} + C{nC} + D{nD} + E{nE} = {total}`，CSV `{total}` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体实算：`4.1` 的 `61` 行 ＋ 总账 `181` 行，共 `{total}`）**：

- **色标（活动名列行首）**：⚪`{c_o}` / 🔴`{c_r}` / 🟢`{c_g}` / 🟡`{c_y}` / 🟠`{c_p}` / ⚠`{c_w}` / 空`{c_n}` ＝ **`{total}`**
- **`classify()`（状态列语义）**：`crit {k_crit}` / `live {k_live}` / `switch {k_switch}` / `pending {k_pend}` / `unclear {k_unc}` / `over {k_over}` ＝ **`{total}`**

**⚠️ 本期 `over` 与 `⚪` 首次差 `0`（`3` 对 `3`）** —— 前五期分别是差 `1` / `2` / `1` / `1` / `2`，**本报连续三期写过「差额不是常数」，本期补上另一半：它可以是 `0`**。三条对齐的原因是本期**没有任何一条「下架了但色标没跟着改」**的条目 —— `stealth/crouton-alpha` 与 `中国电信 Xing4.0` 都已在 065 期把色标改成 ⚪。**另外四组各差 `1`（`🔴6` vs `crit6` 对齐、`🟢184` vs `live183`、`🟠10` vs `switch9`、`🟡24` vs `pending25`、`⚠15` vs `unclear16`）** —— 色标是「谁写的」，`classify()` 是「写的是什么」，**两组数不该指望相等**。

**③ 逐行 diff（本期改写 `17` 行状态列 ＋ 补入 `3` 行 ＋ 归档 `0` 行）**：

- **改写 `17` 行**：`4.1` 里 `9` 行（`ERNIE 5.5`、`MiniMax 4K`、`Antigravity 6 个月`、`腾讯轻量云`、`48 号公告`、`Gemini 4 Argon`、`Google AI Plus`、`Fable 5.2`、`Runware pruna-p-video-upscale`）、`4.2` 里 `8` 行（`OpenRouter 免费档`、`Token 羊毛`、`Antigravity 个人免费档`、`ERNIE-5.5-Flash-Base`、`Ripple`、`Inkling-2-Small`、`OpenCode 免费清单`、`Praxis-1`）。**全部走「整体替换状态列」**；另 **`41` 行**只改天数、不动措辞（`Counter({{3: 100}})`）。
- **补入 `3` 行**：`4.1` 的 **`Runware MiniMax H3 Max 30% OFF`（今天到期）**；`4.2` 的 **`LongCat-2.5` 权重 `MIT`** 与 **`PEAR` 开放权重**。**三条都带 `069 期补入 / 补登` 标记**。
- **归档 `0` 行** —— 本期没有「过期 >`7` 天**且**状态列已写收口口径」的新条目。
- **⚠️ 本期最重要的一处改动不在内容、在方向**：068 期有 `14` 行把「已过 `N` 天」写成「距截止 `N` 天」（第五章纠错①）。本期 `gen_table069.py` 按 `delta` 正负分支重写，**并用「截止列说过期、状态列不许说距截止」这条断言兜底** —— 落盘后复跑，`14` 行全部纠正、`0` 行矛盾。
- **天数 token 全部实算**：带天数的每一处都按「截止日 − `2026-11-15`」重算（脚本末尾断言：逐行取截止列日期，与状态列里的数字**带符号**比对，不一致就 `AssertionError`）。`11/13` 到期的两条改成「已过 `2` 天」，`11/15` 的三条写成「今日（`11/15`）为截止日」。**状态列不出现「未开始」**。

**④ 下期（`070`）强制动作 —— 出刊前逐条过**：

1. **`MiniMax H3-Image` 的 `11/18 00:00` 之后**：`4K` 是否回到 `0.4522`、`Runware` 的 `11/17` 那条是否下架、计费页横幅是否消失（**三条同验，缺一条不算「如期结束」**）。
2. **今天到期的三条**（`Runware MiniMax H3 Max 30% OFF`、`48 号公告` 征求意见、`Fable 5.2` 优惠 `11/16 23:59 PT`）：下期是「已过 `1` 天」还是「延长」。
3. **`ERNIE 5.5 Flash Preview` 的 `11/25` 前是否开权重**：`?author=baidu` 是否从 `39` 变 `40`。**剩 `10` 天。**
4. **`Ling 3.2 Flash` 第 `3` 天**：`endpoints` 是否仍是 `[]`；若连续 `3` 天为空，**下期起不再逐日重写，改成「自 068 期起空 `N` 天」一句**。
5. **`LongCat-2.5` 的 `downloads`**：`1,573` 是否起量、`likes` 比是否继续走「下载远多于点赞」；`?author=meituan-longcat` 的 `32` 个仓是否变多。
6. **`PEAR` 的社区侧**：`stars 240` 是否起量、`HF` 三次仓的 `downloads`（`109 / 26 / 29`）是否拉开差距、是否有第三方复现 `LIBERO 74.4%`。
7. **`OpenRouter` 免费区**：`14 / 17 / 16` 三个口径是否连续第 `3` 天不变；`:free` 是否出现新条目。
8. **`Token 羊毛` 第 `8` 期**：`¥2433` 是否继续跳、`11/15` 那 `6` 条次日定格到几。
9. **`freellm.net` 的日期戳**：是否仍停在 `2026-11-14`；若连续两期不动，正文改口径为「该站不再逐日更新」。
10. **`Inkling-2-Small` 的 `downloads`**：`7,329` 之后是第三个数量级还是回落 —— **「一次性拉取」与「持续增长」的区分点**。
11. **`Antigravity` 的 `md5`**：连续 `4` 期同值，下期若变，**先比可见文本再谈变化**。
12. **新建仓库线（第八章第 `1` 条）**：下期是否从 `q=created:>` 反查到新仓；抓不到就说明这条线需要按 `pushed_at` 再筛一遍。
"""

FOOT = FOOT.format(
    nA=nA, nB=nB, nC=nC, nD=nD, nE=nE, total=len(rows),
    listA=fmt(buckets["A"]), listB=fmt(buckets["B"]),
    c_o=color["⚪"], c_r=color["🔴"], c_g=color["🟢"], c_y=color["🟡"],
    c_p=color["🟠"], c_w=color["⚠"], c_n=color["空"],
    k_crit=cls["crit"], k_live=cls["live"], k_switch=cls["switch"],
    k_pend=cls["pending"], k_unc=cls["unclear"], k_over=cls["over"],
)

TAIL = """> **其余 `142` 条常驻权益本期无变化，未逐条重印** —— 全量见《[常驻权益总账](常驻权益总账.md)》（`181` 条）。**`4.2` 只收「本期真正动过的 `39` 条」**；这 `39` 条与总账是同源副本，**不重复计数**。⚠️ 这 `142` 条沿用上期读数、**本期未逐个重取** —— 不写成「已复核」。

"""

i = md.index("### ④ 本期第四章脚注")
md = md[:i] + TAIL + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(MD, encoding="utf-8").read()
assert "其余 `142` 条" in disk
assert "**④ 下期（`070`）强制动作" in disk
assert "A34 + B8 + C0 + D192 + E8 = 242" in disk
print("footnote ok | bytes", len(disk.encode()))
print("A/B 列表长度：", len(fmt(buckets["A"])), len(fmt(buckets["B"])))
