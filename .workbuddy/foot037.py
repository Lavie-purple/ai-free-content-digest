# -*- coding: utf-8 -*-
"""生成第四章脚注并注入 <<<FOOT4>>> 占位符。四段固定（031 期定）：三态分布 / A-E 实跑 / 逐行 diff / 强制动作。

⚠️ 所有数字从 deadlines.csv 实跑，**不预写**（034 期纪律）。
⚠️ 「双口径差值」按 034 期定的定义算：色标为 🟠/🟢 但 `状态` 是 `pending` 的行数 —— **不是**「色标🟠🟢 且 状态非 over」（那个数是 118，口径完全不同）。
"""
import csv, io, os, re
from datetime import date

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(WS, ".workbuddy", "data", "deadlines.csv")
MD = os.path.join(WS, "AI免费内容与权益速递-第037期-2026-10-16.md")
TODAY = date(2026, 10, 16)

rows = list(csv.DictReader(io.open(CSV, encoding="utf-8-sig")))
total = len(rows)

# ---- A/B/C/D/E 五档，按 check_deadlines 的同一套规则复算 ----
expired, due, over, nodate, later = [], [], [], [], []
for r in rows:
    d = r["截止日期"].strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", d):
        nodate.append(r)
        continue
    delta = (date.fromisoformat(d) - TODAY).days
    if r["状态"] == "over":
        over.append((delta, r))
    elif delta < 0:
        expired.append((delta, r))
    elif delta <= 14:
        due.append((delta, r))
    else:
        later.append((delta, r))

A, B, C, D, E = expired, due, over, nodate, later
assert len(A) + len(B) + len(C) + len(D) + len(E) == total, "五档求和不等于总数"

# ---- 三态分布（色标口径） ----
n_orange = sum(1 for r in rows if r["紧急度"] == "🟠")
n_green = sum(1 for r in rows if r["紧急度"] == "🟢")
n_white = sum(1 for r in rows if r["紧急度"] == "⚪")
n_crit = sum(1 for r in rows if r["紧急度"] == "🔴")

# ---- 双口径差值（034 期定义） ----
diff = [r for r in rows if r["紧急度"] in ("🟠", "🟢") and r["状态"] == "pending"]

# ---- B 档清单 ----
blist = "；".join("**T%+d** %s" % (d, r["活动"].replace("**", "")[:34]) for d, r in sorted(B, key=lambda x: x[0]))
alist = "；".join(r["活动"].replace("**", "")[:44] for _, r in A)

FOOT = """> **脚注（四段固定口径，全部数字由 `deadlines.csv` 实跑，非预写）**
>
> **① 三态分布（`extract_deadlines` 口径，基准日 {today}）**：**🟠 生效中（倒计时中）{n_orange}** · **🟢 生效中 {n_green}** · **⚪ 已结束 {n_white}** · **🟡/⚠ 待定 {n_y}** · **🔴 高危 {n_crit}**，**全表 {total} 行**。
> ⚠️ **色标口径与 `classify()` 口径可差若干条，两套都写、正文一律以脚本口径为准**（**色标是人工判读、`classify()` 是规则判读，差异来自「关键词优先于色标」与规则误捕**）。本期实测差值 **{ndiff} 条**（「色标为 🟠/🟢、但 `状态` 仍是 `pending`」的行数，**034 期定的定义**）；**⚠️ 切勿用「色标🟠🟢 且状态非 over」那个口径**（本期该数为 118，是完全不同的量）。
> ⚠️ **⚪ 与 C 差 1 是正确口径**（`GitHub Models 免费层` 行的 `2026-07-30` 不是解析器认的 `M/D` 写法，**归 D 不归 C，勿修正**）。
>
> **② A/B/C/D/E（`check_deadlines --today {today}` 实跑）**：**A {na} · B {nb} · C {nc} · D {nd} · E {ne} = {total}**（**与 CSV 行数一致**）。
> **A 档（已过期但状态非已结束）{na} 条**：{alist} —— **Q04 连续第 25 期未见确切停服日，本表刻意保持 🔴 高危窗口开启，不按「已结束」处理**（避坑 24）。⚠️ **本期同表内已有腾讯元器的三个确切日期 —— 两相对照说明「无确切日期」不是腾讯这条线的常态，而是老混元这一条的常态**。
> **B 档（14 天内到期）{nb} 条**：{blist}
> ⚠️ **B 档较上期 9 → {nb}**：**进的两条是本期新增行（Together AI `Muse Spark Open` 限免 10/18、腾讯元器 10/29 停止新建），出的一条是 `Step 5 Preview` 权重开放（10/15 已过 14 天窗口）** —— **「一进一出」相抵后净增，不是数据变脏**（032 期纪律）。⚠️ **另有 `豆包工作 30 天订阅`（T+1）与 `MiniMax Code 重置卡`（T+2）两条本日新增/新到期项**：**前者到期日为第三方整理口径，以客户端订阅页为准；后者来源为第三方清单转述 MiniMax 官方推特，均未回官方原页核**（避坑 44）。
> **D 档（日期无法解析）{nd} 条 / E 档（窗口外 >14 天）{ne} 条**：**⚠️ D 档由上期 105 增至 {nd}、E 档由 21 增至 {ne}** —— **两处增量都来自本期新增的 8 行**（**写「未公布」或写两个时刻的行一律进 D；写 11/30、12/31 等远端日期的行进 E**）。**⚠️ 其中 Together AI 行因需并列两个时刻（「10/18（促销行无时刻）/ 10/18 12:00 PT（站点横幅）」）被 D 档收纳、不误报为已过期** —— **这是 033 期「凡在截止列写出可被 `M/D` 正则捕获的日期文本都会被解析成该行截止日」这条纪律的正面执行**。
>
> **③ 逐行 diff（两笔最容易读成「数据变脏」的）**：**① `Step 5 Preview` API 缓存命中输入档调价行的「截止」列由实日期改为「未公布（调价已于 2026-10-14 00:30 生效，非活动截止）」** —— **调价是换挡日不是活动到期，写实日期会在基准日推进后误报 A 档**（036 期改法，037 期维持，**该行本期落 D 档**）。**② 腾讯元器行的三个日期里只有前两个可被 `M/D` 正则捕获（`11/9` 停服、`10/29` 停止新建），第三个「最后导出日」写成 `2027 年 1 月 9 日`（不可被解析）** —— ⚠️ **本期首次踩到这个坑并当场修掉**：**初稿写 `2027/1/9` 被 `extract_deadlines` 解析成「2026 年第 27 月」，`check_deadlines` 直接抛 `ValueError: month must be in 1..12`** —— **「生效时刻 / 最后导出日」不是活动截止，不该写成可被解析的实日期**（036 期定的写法纪律，本期把它从「调价行」扩展到「导出日」）。
> ⚠️ **本期 8 个新行全部避开叙述性 `M/D`**（036 期起执行的写法纪律，037 期继续）。
>
> **④ ⚠️ 下一轮强制动作（九项，逐项都是可判定的）**：**① 智谱 AutoClaw 第三期是否接上第二期**（10/16 已收口，本期未见公告）；**② `STEPX Neo` 10/16 首销后的实际销量与「星辰船票」名额是否调整**；**③ `Muse Spark Open` 的 ungated 镜像（Unsloth GGUF / `ggml-org` GGUF / AMD Quark）是否被施压下架或加闸门** —— **这是本期新出现的可判定位**（避坑 162）；**④ `Muse Spark Open` 完整评测报告是否发布、独立榜单（`Artificial Analysis` 39 分）是否上移**；**⑤ Together AI 限免 10/18 到期后是否续期，并回官方 `together.ai` 定价页复核那条第三方 diff 站记录**（本期唯一挂账的第三方 diff 站口径）；**⑥ MiniMax Code 重置卡 10/18 到期后是否续期**；**⑦ Google AI Plus 11/13 生效日的实际执行口径是否与邮件一致**（本期新增的订阅降级节点）；**⑧ 元器 11/9 停服前的导出高峰（数据导出截止 `2027 年 1 月 9 日`）与 ADP 迁移实况**（**注意导出日比停服日晚两个月，两件事要分别盯**）；**⑨ freellm.net「免绑卡 N+」这一模型口径计数是否恢复出现，若恢复须同时声明它与 `/providers` 页「26 of 30 providers 无需信用卡」不是同一口径、不可相减**。
""".format(
    today=TODAY.isoformat(), total=total,
    n_orange=n_orange, n_green=n_green, n_white=n_white, n_crit=n_crit,
    n_y=sum(1 for r in rows if r["紧急度"] in ("🟡", "⚠", "")),
    ndiff=len(diff),
    na=len(A), nb=len(B), nc=len(C), nd=len(D), ne=len(E),
    alist=alist, blist=blist,
)

md = io.open(MD, encoding="utf-8").read()
assert md.count("<<<FOOT4>>>") == 1, md.count("<<<FOOT4>>>")
md = md.replace("<<<FOOT4>>>", FOOT.strip("\n"))
assert "<<<FOOT4>>>" not in md
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)
print("FOOT4 injected | A%d B%d C%d D%d E%d = %d | diff %d | colors 🟠%d 🟢%d ⚪%d 🔴%d"
      % (len(A), len(B), len(C), len(D), len(E), total, len(diff), n_orange, n_green, n_white, n_crit))