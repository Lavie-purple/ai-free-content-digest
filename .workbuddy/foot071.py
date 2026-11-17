# -*- coding: utf-8 -*-
"""071 期：重写第四章脚注（四段）+ 补回 4.2 收尾段。"""
import csv
import datetime
import io
import re

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第071期-2026-11-17.md"
T = datetime.date(2026, 11, 17)

rows = list(csv.DictReader(io.open(WS + ".workbuddy/data/deadlines.csv", encoding="utf-8-sig")))
assert len(rows) == 249, len(rows)


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
assert (nA, nB, nC, nD, nE) == (36, 12, 1, 195, 5), (nA, nB, nC, nD, nE)
assert nA + nB + nC + nD + nE == len(rows) == 249, (nA, nB, nC, nD, nE, len(rows))

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
assert sum(color.values()) == 249, sum(color.values())

FOOT = """### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-17` 实跑；CSV 共 `249` 条 ＝ 本章可见 `4.1` 的 `65` 行 ＋ 《常驻权益总账》`184` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`{nA}` 条（070 期 `35`，`+1`）** —— 新进 `1` = **`Fable 5.2` 发布优惠**（官方逐字 `11/16 23:59 PT`，按 PT 日期落进 `A`；折算北京是 `11/17 15:59`，**同一个截止两套日期，CSV 只能取一个**）；其余 `35` 条只是天数推进。**`A` 桶连续三期只增不减 —— 这批是「过期了但没人收口」的长尾，不是待办清单。**
  {listA}
- **【B】14 天内到期：`{nB}` 条（070 期 `11`，`+1`）** —— 进 `3` 出 `2`：进 = **`Antigravity` 三模型移除（`1` 天）**、**`AutoClaw M11W3`（`5` 天）**、**`11/30` 那批里 `Character.AI` 掉进 `14` 天内**；出 = `Fable 5.2` 转 `A`、`Runware 30% OFF` 转 `C`。**今天到期的只有一条：`Runware` 的 `4K 50% OFF`。**
  {listB}
- **【C】已结束：`{nC}` 条** —— 仍是 `Runware` 的 `30% OFF`（`11/15` 到期、⚪ 收口）。本期新增的「`11/17` 到期」两条**都还在等下一个观测点**，不提前收口。
- **【D】日期无法解析：`{nD}` 条（070 期 `193`，`+2`）** —— 本期补入 `2` 条无截止日的常驻权益（`OpenAI` 学术计划、`tencent/hy4-flash` 目录标价），无归档移出，净 `+2`。`D ≠ 失效`。**⚠️ 其中 `OpenAI` 那一行的日期（`11/23` 开放申请）已被本报从「截止列」移到「状态列」** —— 否则 `extract_deadlines` 会把它读成「`11/23` 到期」，凭空多出一条 `T+6`（`058` 期同型坑）。
- **【E】窗口外（>14 天）：`{nE}` 条** —— `12/09` 杭州全城 Coding 计划、`12/31` 四条（`Gemini 3.8 Flash` 促销价、`Moonshot K2` 下线、`Runway` 企业版、`腾讯云 TokenHub` 新人包）。
  **对账：`A{nA} + B{nB} + C{nC} + D{nD} + E{nE} = {total}`，CSV `{total}` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体实算：`4.1` 的 `65` 行 ＋ 总账 `184` 行，共 `{total}`）**：

- **色标（活动名列行首）**：⚪`{c_o}` / 🔴`{c_r}` / 🟢`{c_g}` / 🟡`{c_y}` / 🟠`{c_p}` / ⚠`{c_w}` / 空`{c_n}` ＝ **`{total}`**
- **`classify()`（状态列语义）**：`crit {k_crit}` / `live {k_live}` / `switch {k_switch}` / `pending {k_pend}` / `unclear {k_unc}` / `over {k_over}` ＝ **`{total}`**

**⚠️ 本期 `over` 与 `⚪` 差 `0`（`{k_over}` 对 `{c_o}`）** —— **另外四组仍各差 `1` 上下（`🔴{c_r}` vs `crit{k_crit}`、`🟢{c_g}` vs `live{k_live}`、`🟠{c_p}` vs `switch{k_switch}`、`🟡{c_y}` vs `pending{k_pend}`、`⚠{c_w}` vs `unclear{k_unc}`）—— 色标是「谁写的」，`classify()` 是「写的是什么」，不该指望相等。**
**⚠️ 本期顺手修掉了两条历史遗留的「解释即触发」**：`ZCode` 行原写「……而不是「已结束」」、`Cloudflare` 行原写「未开始（距今约 6 个月）」—— 两处都让 `classify()` 读成了别的状态（`054` 期同型坑）。**改成「只记登记项失效」「倒计时进行中」之后，两行的语义分类才与色标一致。**

**③ 逐行 diff（本期改写 `20` 行状态列 ＋ 补入 `4` 行 ＋ 归档 `0` 行）**：

- **改写 `20` 行**：`4.1` 里 `10` 行（`腾讯老混元`（手算天数）、`MiniMax 4K`、`Runware 4K 50%`、`Runware 30%`、`ERNIE 5.5`、`48 号公告`、`Gemini 4 Argon`、`Google AI Plus`、`Fable 5.2`、`Runware pruna-p-video-upscale`）、`4.2` 里 `10` 行（`OpenRouter 免费档`、`Token 羊毛`、`Antigravity 个人免费档`、`ERNIE-5.5-Flash-Base`、`Inkling-2-Small`、`OpenCode 免费清单`、`Praxis-1`、`PEAR`、`LongCat-2.5`、`Qwen4-Max`）。**全部走「整体替换状态列」。**
- **补入 `4` 行**：`4.1` 的 **`AutoClaw M11W3 100M`** 与 **`Antigravity 三模型 11/18 移除`**；`4.2` 的 **`OpenAI 学术计划扩容`** 与 **`tencent/hy4-flash 入目录`**。**四条分别带 `071 期补入` / `071 期新增观测位` 标记。**
- **只改天数 `44` 行**（与上面 `20` 行部分重叠）：带天数的每一处都按「截止日 − `2026-11-17`」重算，脚本末尾逐行带符号比对。`腾讯老混元` 的「`2026` 年 `9` 月底」不可解析，**手算 `已过 48` 天**（`09-30` 起算），另两处期数手工推进（`Q04` 第 `44` 期、高危窗口第 `35` 天）。
- **归档 `0` 行** —— `prune_table` 判「表体 `107` 行 ＝ 保留 `107` + 移出 `0`」：过期条目里唯一已收口的是 `Runware 30% OFF`（`11/15`，仍在 `7` 天宽限内）。
- **⚠️ 本期最关键的一处不是改数字、是「把日期挪出截止列」**：`OpenAI` 学术计划的 `11/23` 是**申请开放日**、不是截止日，留在截止列会让 CSV 多出一条假到期（见 ① 的 `D` 桶说明）。

**④ 下期（`072`）强制动作 —— 出刊前逐条过**：

1. **`Antigravity` 的 `11/18` 之后**：免费档模型清单是否只剩 `Gemini 3.8 Flash`；那三串旧措辞（`Unlimited Tab` / `Unlimited Command` / `Basic weekly rate limits`）是否再出现；**首页能否取到**（本期 `000`，「双同」观测已断一期）。
2. **`MiniMax H3-Image` 的 `11/18 00:00` 之后**：`4K` 是否回到 `0.4522`、`Runware` 的 `11/17` 那条是否卸下徽标、数组里的 `endsAt: "2026-11-17"` 是否还在 —— **这条已挂第 `3` 期，`072` 必须给结论。**
3. **`AutoClaw` 的 `M11W4`（`11/23` 起）**：官方页是否续档、额度回到 `50M` 还是维持 `100M`；`/blog/news/M11W4/` 这个路径能否直接构造成功（本期第一次按周编号抓到）。
4. **`OpenAI` 学术计划 `11/23` 开放后**：名额是否真是 `50,000`、申请页是否给出关闭日、`Plus` 的额度与可用模型是否出现数字。
5. **`OpenCode` 的 `-free` 池**：是否继续净减；`hy4-flash-free` 是否第 `5` 天仍在；`minimax` 那条是否换成新 `id` 回归。
6. **`OpenRouter`**：`470` 是否再变；`:free` 是否第 `5` 天仍 `14`；`qwen4-max` 是否出现 `:free` 变体；`hy4-flash` 标价是否维持「官方五折」这个位置。
7. **`HF` 的 `downloads`**：解冻后是否连续 `2` 天正常刷新；**若再停一次，本报改「只记 `likes` + 单独标注下载不可读」**，不再并排列。
8. **`ERNIE 5.5 Flash Preview` 的 `11/25`**：`?author=baidu` 是否从 `39` 变 `40`。**剩 `8` 天。**
9. **`Qwen4` 小尺寸权重**：`?author=Qwen` 是否出现 `Qwen4` 新仓；`Qwen-Live-Delivery-Plugin` 的仓库地址是否公布（**要 `spdx`，不是要新闻稿**）。
10. **`PEAR` 的 stars（`574`）之后是否有代码提交**（本期那唯一一次推送是文档修链接）；第三方是否复现 `LIBERO 74.4%`。
11. **`Token 羊毛` 第 `10` 期**：`¥1758` 与 `61` 张之后是否继续走平；`11/17` 那 `2` 次（`1` 张卡）次日定格到几。
12. **两条长期缺口**：`hunyuan.tencent.com` 是否仍是 `JS` 壳（第 `3` 期）；`Ripple-65B-Preview` 用正确 slug（`ricursiveAI/Ripple-65B-Preview`）重取一次。
"""

FOOT = FOOT.format(
    nA=nA, nB=nB, nC=nC, nD=nD, nE=nE, total=len(rows),
    listA=fmt(buckets["A"]), listB=fmt(buckets["B"]),
    c_o=color["⚪"], c_r=color["🔴"], c_g=color["🟢"], c_y=color["🟡"],
    c_p=color["🟠"], c_w=color["⚠"], c_n=color["空"],
    k_crit=cls["crit"], k_live=cls["live"], k_switch=cls["switch"],
    k_pend=cls["pending"], k_unc=cls["unclear"], k_over=cls["over"],
)

TAIL = """> **其余 `142` 条常驻权益本期无变化，未逐条重印** —— 全量见《[常驻权益总账](常驻权益总账.md)》（`184` 条）。**`4.2` 只收「本期真正动过的 `42` 条」**；这 `42` 条与总账是同源副本，**不重复计数**。⚠️ 这 `142` 条沿用上期读数、**本期未逐个重取** —— 不写成「已复核」。

"""

i = md.index("### ④ 本期第四章脚注")
md = md[:i] + TAIL + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(MD, encoding="utf-8").read()
assert "其余 `142` 条" in disk
assert "**④ 下期（`072`）强制动作" in disk
assert "A36 + B12 + C1 + D195 + E5 = 249" in disk
print("footnote ok | bytes", len(disk.encode()))
print("色标：", dict(color), "｜classify：", dict(cls))
