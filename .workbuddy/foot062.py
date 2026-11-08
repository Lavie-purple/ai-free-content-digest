# -*- coding: utf-8 -*-
"""062 期第四章脚注：把 <<<FOOT062>>> 替换为四段脚注 + ⑤ 工程纪律。

纪律：
  · 计数与明细同源：A / B 两个桶的**逐条明细直接由 `check_deadlines.py --all` 的输出解析生成**，
    再断言条数与桶头一致 —— 不手打名字，避免「计数对、名单错」。
  · 分布数字先从 `check_deadlines.py` 实跑 + `deadlines.csv` 实算，断言等于脚注里要写的数字，才允许写入。
  · 写出后回读落盘文件再逐字断言。
"""
import csv
import io
import re
import subprocess
import sys
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第062期-2026-11-08.md"
CSV = WS + ".workbuddy/data/deadlines.csv"
PLACE = "<<<FOOT062>>>"

out = subprocess.check_output(
    [sys.executable, WS + ".workbuddy/check_deadlines.py", "--today", "2026-11-08", "--all"],
    stderr=subprocess.STDOUT,
).decode("utf-8", "replace")
buckets = {k: int(v) for k, v in re.findall(r"【([A-E])】[^：\n]*：(\d+)\s*条", out)}
print("实跑三态桶:", buckets)
assert buckets == {"A": 26, "B": 10, "C": 0, "D": 179, "E": 7}, buckets
assert "CSV 共 222 条 -> 一致" in out, "对账行没命中（命中 0 条不是通过）"

rows = list(csv.DictReader(io.open(CSV, encoding="utf-8-sig")))
color = Counter(r["紧急度"] for r in rows)
cls = Counter(r["状态"] for r in rows)
print("实算色标:", dict(color))
print("实算状态:", dict(cls))
assert len(rows) == 222
assert color == Counter({"🔴": 5, "🟢": 153, "🟠": 7, "🟡": 22, "⚠": 14, "": 19, "⚪": 2}), color
assert cls == Counter({"crit": 5, "live": 170, "switch": 6, "pending": 23, "unclear": 16, "over": 2}), cls
assert sum(color.values()) == sum(cls.values()) == 222

white = [r for r in rows if r["紧急度"] == "⚪"]
assert len(white) == 2 and buckets["C"] == 0
assert any("ZCode" in r["活动"] and "第 5 天到期" in r["截止原文"] for r in white)
assert any("每日登录领 credits" in r["活动"] and "10 月 12 日至 10 月 16 日" in r["截止原文"] for r in white)
print("⚪ 与 C 的差额 2：两条均逐条归因 ✔")

# ---- 从 check 输出解析 A / B 明细（计数与明细同源）----
LINE = re.compile(r"^\s{2}(\d{4}-\d{2}-\d{2})\s+\(([^)]*)\)\s+(\S+)\s+(.+)$")


def section(tag):
    i = out.index("【%s】" % tag)
    j = out.index("【%s】" % chr(ord(tag) + 1))
    lines = [l for l in out[i:j].split("\n") if LINE.match(l)]
    return [LINE.match(l).groups() for l in lines]


A = section("A")
B = section("B")
assert len(A) == 26, len(A)
assert len(B) == 10, len(B)

A_ITEMS = []
for d, rel, st, name in A:
    n = name.split("（")[0].split(" · ")[0].strip()
    A_ITEMS.append("`%s`（%s，%s）" % (n, d, rel))
B_ITEMS = ["`%s`（%s，%s）" % (n.split("（")[0].split(" · ")[0].strip(), d, rel) for d, rel, st, n in B]
print("A 明细:", len(A_ITEMS), "B 明细:", len(B_ITEMS))

# 4.2 成员 diff
md = io.open(MD, encoding="utf-8").read()
i = md.index("### 4.2 常驻权益本期变更")
j = md.index(PLACE)
r42 = [l for l in md[i:j].split("\n") if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(r42) == 46, ("4.2 行数", len(r42))
assert sum(1 for r in r42 if "Inkling 2 Small Free" in r) == 1, "Inkling 行未进 4.2"
assert sum(1 for r in r42 if "`AXON Developer Edition`" in r) == 1, "AXON 未进 4.2"
assert not any("`Vercel Labs` `fx`" in r for r in r42), "fx 不该在 4.2"
print("4.2 成员 diff：出 0、进 2（AXON 从常驻未变进、Inkling 新登记）✔")

FOOT = r"""### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-08` 实跑；CSV 共 `222` 条 —— 取自日报正文表体与《常驻权益总账》两处合并，所以「`222` 条」与「本章可见 `101` 行」不是矛盾）**：

- **【A】已过期但状态仍非收口态：`26` 条 —— 较 061 期的 `25` 条多 `1` 条**。**逐条归因只有两件事**：**① 061 期那 `25` 条全部还在（两期相隔 `2` 天，每条天数 `+2`）**；**② 新进 `1` 条：`MiniMax` 开放平台 `M3` / `M2` 免费试用**（061 期是 `T+0`，本期过期 `11/7` 走到「已过 `1` 天」—— **它出 `B` 桶、进 `A` 桶，所以本期 `A +1` 与 `B −1` 是同一件事的两面**）。**逐条（`截止日`，`已过`，`classify()`）**：
  ① **{a}**
  ⚠️ **本期 A 档的 `26` 条里，仍有一条性质与其它 `25` 条不同**：**`Moonshot Kimi K3.1 Pro` 那一行虽然日期已过，但事件已经发生**（059 期实核：权重已公开），**状态列在 059 期已改写成「已兑现」** —— **`check_deadlines` 仍把它算进 `A`，因为它只看「截止日 < 基准日 且 状态非收口」**。**桶是筛子，不是结论**（与 059–061 三期同一条，处置相同：不改脚本，在脚注点名称）。
  ⚠️ **两条 `Ollie` 本期由 `gen_table062.py` 显式改写为「关停日已过 `2` 天」** —— 055 期纪律：**截止日跨过基准日后，状态列必须写成「已过 N 天」，不放宽重算器、不把负值写进表体**。**本期 `26` 条逐条复核：全程未用收口字样**（避坑 239 —— **053 期踩 `4` 次、054 期踩 `1` 次，055–062 八期均踩 `0` 次**）。
- **【B】14 天内到期：`10` 条 —— 较 061 期的 `11` 条少 `1` 条，成因是「`MiniMax` 出桶、无人进桶」**。**逐条（`截止日`，`相对`，`classify()`）**：
  ② **{b}**
  ⚠️ **本期 `B` 桶 `T+0` 有四条（`11/8` 当天）** —— **下期它们会一起进 `A`**，**这是本期最值得提前记的一笔**（`AutoClaw` 国内站 / 国际站 `M11W1`、`火山 Coding Plan 2.5 折`、`火山方舟 Agent Plan` 个人版）。
- **【C】收口态：`0` 条** —— **表体里仍有 `2` 条 `⚪` 收口行，`C` 桶却是 `0`，差额 `2`**。**⚠️ 差额不是常数，本期逐条归因**：**① `ZCode / BigModel 新用户试用`**（截止原文逐字 `连接 BigModel 账号后起算，第 5 天到期` —— **相对期限、无日历日 → 落 `D` 桶**）**② `智谱 AutoClaw「每日登录领 credits」第二期`**（截止原文逐字 `已按原定日期收口（活动期 10 月 12 日至 10 月 16 日，北京）` —— **日期藏在叙述句里、不在可解析字段 → 落 `D` 桶**）。**与 056–061 六期同一对、同一差额 `2` —— 七期连续，结构性差额，不是本期才出现的偏差**（避坑 215）。
- **【D】日期无法解析：`179` 条 —— 较 061 期的 `178` 条多 `1` 条，正是本期补入的那 `1` 行**（`OpenCode` 的 `Inkling 2 Small Free`，截止列写「无结束日（官方逐字 `free on OpenCode for a limited time`，未给具体日期）」）。**`D` 桶的 `+1` 与表体 `+1` 是同一件事，不是两次变化。**
- **【E】窗口外（>14 天）：`7` 条 —— 与 061 期同名单、同顺序**（天猫「AI 空间站」`11/28`、`Character.AI` 第 11 章、`Gemini 4 Argon` `11/30`、杭州 `Coding` 计划 `12/9`、`Gemini 3.8 Flash` 促销价 `12/31`、`Moonshot K2` 停新注册、腾讯云 `TokenHub` 新人免费包）。**⚠️ 连续四期「同值且同成员」。**
- **对账：`A26 + B10 + C0 + D179 + E7 = 222`，CSV 共 `222` 条 → 一致** ✔。

**②-补 双口径三态（色标口径 vs `classify()` 口径，两套都写、逐条解释差值）**：

- **色标口径（`紧急度` 列）实跑**：**⚪ `2` / 🔴 `5` / 🟢 `153` / 🟡 `22` / 🟠 `7` / ⚠ `14` / 空 `19` = `222`**。
- **`classify()` 口径（`状态` 列）实跑**（**两侧都取自 `slim` 两轮跑完之后重跑的 `deadlines.csv`**）：**`crit` `5` / `live` `170` / `over` `2` / `pending` `23` / `unclear` `16` / `switch` `6` = `222`**。
- **⚠️ 六个桶的差与 061 期同一套算术**：**① 色标 🟢 `153` → `live` `170`，差 `+17` = `19` 条「`紧急度` 列为空、状态列写「生效中」」的行 − 色标 🟢 里被文字改判的 `2` 条**（`Anthropic` 新版使用政策 → `pending` 一条、`OpenCode DeepSeek V4.1 Flash` → `unclear` 一条）；**② 色标 🟡 `22` → `pending` `23`，差 `+1`**；**③ 色标 ⚠ `14` → `unclear` `16`，差 `+2`**；**④ 色标 🟠 `7` → `switch` `6`，差 `−1`**；**⑤ `🔴 5 = crit 5`、`⚪ 2 = over 2`，两个桶成员完全一致（差集都是空）**；**⑥ 两套总数都是 `222`**。
- **⚠️ 与 061 期的逐桶对账**：**色标 🟢 `152 → 153`（`+1`），其余六桶同值；`classify()` `live` `169 → 170`（`+1`），其余五桶同值** —— **`+1` 正是本期补入的那 `1` 行（`Inkling 2 Small Free`，`🟢` 且判 `live`）** ✔。**⚠️ `over` 桶 `2 → 2` 且成员不变 —— 本期 `prune_table.py` 一条都没移出（见 ③）；归档区最后一段仍是 `056 期`，未改动。**
- **⚠️ 「色标亮、`状态` 却是 `pending`」本期 `23` 条**（人工逐条认定）：**055–062 八期同为 `23` 条**。

**③ 逐行 diff + ⚠️ 下一轮强制动作**：

**⚠️ 本期表体 `222` 行 ＝ 061 期 `221` 行 ＋ 本期补入 `1` 行 − 移出 `0` 行**（`gen_table062.py` 实跑 `221 + 1 = 222`、字段数分布 `Counter({3: 222})` 全为 `3` ✔；`prune_table.py` 实跑 **移出 `0` 条**（`101 → 101` 行，归档区未改动）；`split_ledger.py` 实跑 **`4.1` = `55` 行 ／ `4.2` = `46` 行 ／ 常驻未变 `121` 行 ／ 总账全量 `167` 条**）。

**⚠️ `4.2` 的 `44 → 46` 已按纪律做成员 diff，是「出 `0` 进 `2`」**：
- **进 `2` 条**：**`OpenCode` 的 `Inkling 2 Small Free`**（`062` 期新登记）、**`AXON Developer Edition`**（**它不是新增行** —— 它一直在《常驻权益总账》的「常驻未变 `122` 条」里，本期因为状态列被整体改写、带上了 `062 期` 标记，`CHANGE_RE` 命中，**从「常驻未变」进了 `4.2`**）。
- **出 `0` 条**：**本期没有任何条目毕业进总账**。
- **⚠️ 所以「常驻未变」`122 → 121` 与「4.2」`44 → 46` 是同一件事的两面**：`167 = 46 + 121`，而 061 期是 `166 = 44 + 122`。**⚠️ 这里必须点名一条方法论风险**：**`AXON` 的「进 4.2」是分类器按字面判的，不是「新发现」** —— 它本期确实有更新（第 `5` 期复核），所以进 `4.2` 是对的；**但如果下一期不再更新，它会自动回「常驻未变」**。**这类「仅因本期复核而进出」的行，会在 4.2 与总账之间来回跳** —— 本报告不为此改脚本，**只在脚注点名，避免读者把它读成「新增权益」**（与 060 期「正则也是筛子」同族，本次是「字面命中也是筛子」）。

**⚠️ 本期补入 `1` 行**：**`OpenCode` 的 `Inkling 2 Small Free`**（`Thinking Machines` 第二代 · `594B`/`17B` 激活 · **权重未放、分发层免费** · 价格表三列 `Free` · **留存数据且可能用于训练** · **十个地区不可用**）。**截止列写「无结束日」，不写任何日期** —— 见 ⑤④。

**⚠️ 本期改写 `14` 行状态列 ＋ `1` 行活动名列**（每键在源表恰好命中 `1` 行、状态列全部用 `set_status()` **整体改写**而非 `append_note()`、字段数守恒、**写出后重新读回落盘文件再断言**）：**① `OpenRouter 免费档`（`460 → 461`、零价 `16`、`:free` `12`，**活动名列括号里的三个计数同步改为 `461/16/12`** —— 只改计数、语义与键名一字不动）② `OpenCode` 免费清单（三套口径 `12/12/13` 全同值、退 `Pulse` 进 `Inkling`）③ `crouton`（第 `6` 天）④ `Ripple-65B`（`downloads 5,087`、四个仓库）⑤ `ERNIE`（第 `2` 次复核）⑥ `豆包工作 30 天订阅`（第 `18` 期无一手）⑦ `豆包额度规则`（无官方补稿）⑧ `商汤 Token Plan`（第 `6` 期同值）⑨ `小浣熊`（第 `6` 期同值）⑩ `商汤 6.8 Flash`（`news` 同值、关键词仍零）⑪ `AXON`（第 `5` 期无许可证）⑫ `Kimi` 访问条件（`Highspeed` 第 `3` 期空）⑬⑭ 两条 `Ollie`（**显式改写为「关停日已过 `2` 天」**）。
**⚠️ 另有 `normalize_days062.py` 归一（本期实际改写 `0` 行），`recalc_days062.py` 独立复核 **`7` 行「距今 N 天」逐行相同、全表 `35` 处天数 token 全部满足「天数 == 截止日 − 基准日」** ✔（**归一与复核是两个脚本**）。**⚠️ 本期 `recalc` 第一次跑就报出 `1` 行需人工确认**（`MiniMax` 截止 `11/7` 却写着「距今 `0` 天」—— 负数被原样继承），**已按 055 期纪律改写为「已过 `1` 天」** —— **`gen_table` 不负责算天数，`normalize` 只归一、不纠错，这一类必须人看。**

**⚠️ 下一轮强制动作（`063` 期出刊前必须逐条过）**：**① `Inkling 2 Small` 的权重是否终于放上 `HF`**（`?author=thinkingmachines` 是否从 `6` 个变 `7` 个）＋ **`OpenCode` 那个 `inkling-2-small-free` 是否长出上下文/参数量字段** ② `Inkling 2 Small Free` 的**不可用地区是否扩表**（本期十个）、**数据条款是否从「可能用于训练」改成「用于训练」** ③ `OpenRouter` `Inception` 整族是否回归（`461` 条里 `inception` 关键字能不能重新命中）＋ 新增 `4` 条 `:batch` 是否带来同族付费版 ④ `OpenCode` 免费清单下一期是 `12` 还是 `13`（**三套口径必须分别报**）⑤ `Runware` `11/8` 的 `pruna-p-video-upscale` 到期后是否「留在数组里」（**这是「数组里还在 ≠ 在售」的又一次观测**）＋ `11/10` 两条 ⑥ `freellm.net` 恢复更新后能不能连续两期都变（**别再拿一期写成「一直正常」**）⑦ `AXON` 许可证（**第 `6` 期**）＋ 它会不会因为本期复核而在 4.2 里「跳回去」 ⑧ `商汤 6.8 Flash` 官方「限时免费」截止日（**第 `7` 期**）⑨ `Ollie` 三页是否下线（**关停日第 `3` 天仍逐字节同值**）⑩ `Antigravity` 定价页连续两期拿到（**本期 `137,564`，061 期 `000`**）、`Basic weekly rate limits` **不再追问数字**（已定「官方不公布」）⑪ `豆包工作` 官方页四项关键词（**第 `19` 期**）⑫ `Kimi K3.1-Highspeed`（**第 `4` 期空**）＋ `tencent/Hy4`（**第 `3` 期 `404`**）⑬ 老混元 `Q04`（**连续第 `41` 期未决**）、`国家超算互联网`（**第 `13` 期**）⑭ `Mistral` 全站（**连续第 `24` 次 `000`**）、`x.ai/news`（**第 `4` 期 `000`**）、`platform.reflection.ai`（**第 `26` 期 `403`**）、`platform.openai.com/docs/models`（**第 `17` 期 `403`**）、`next.opera.com/web-ai/`（**第 `14` 期 `451`**）、`docs.somark.ai/free-tier-rules.md`（**第 `9` 期 `404`**）⑮ **把本期「零命中 / 未取到」结论涉及的页面全部入档**（清单见第九章，避坑 260 的落地动作，每期必做）⑯ **占位逻辑改成「文件不存在就补空文件」**（本期 `acl` / `paperswithcode` 因 `301` / `302` 未落盘，见第八章）。

**⑤ 062 期的工程纪律（本期实测，都写在这里）**：

- **① ⚠️ 计数不变 ≠ 成员不变，而且「三个计数」可以同时骗人**：`OpenRouter` 全量 `+1`、零价 `16`、`:free` `12`，**两个免费计数一个没动**，消失的是 `Inception` 三条（付费区）。**脚本层的落法**：`tmp_062` 的 diff 先打 `ADD` / `REM` **两个完整名单**，再打三个计数；**断言只放在「名单」上（`len(add)==4 and len(rem)==3`），不放在计数上** —— 计数是算术结果，名单才是事实。
- **② ⚠️ `-free` 后缀的正则会抓到 `URL` 里的子串**：本期 `\b([a-z0-9][a-z0-9.\-]*?-free)\b` 命中 `13` 个 `ID`，多出来的 `tml-free` 来自条款 `PDF` 的 URL（`tml-free-research-api-tier-terms-of-service.pdf`）。**落法：① 判「免费档几个」先数表体行（`<tr>` 里 `id` 列），再用正则交叉验证；② 两者不一致时以表体为准并断言「多出来的那个必须能在原文里定位到非模型上下文」**。**⚠️ 与 058 期「命中 `0` 条不是通过」互为镜像：这次是「命中 `13` 条也不是 `13` 个」。**
- **③ ⚠️ 字节数相同、`md5` 不同；字节数不同、内容全同** —— 本期同一份 `tinker.html` 两期都是 `602,272` 字节而 `md5` 不同（差的是 `Cloudflare` 邮箱混淆串），`runware.ai/pricing` 则反过来（`758,198 → 758,197`，`19` 条促销逐字段全同）。**落法：「同值」结论一律走 `md5`；`md5` 不同时必须做一次结构 diff 并**说明差在哪个片段**（本期是 `/cdn-cgi/l/email-protection#…` 与 `data-cfemail="…"`），**不能只写「不同」。**
- **④ ⚠️ 新增行的截止列仍是「无结束日」，不许写页面上的任何日期**：`Inkling 2 Small Free` 那一行，页面能看到的日期只有两种 —— `OpenCode` 的 `November 6, 2026`（**那是 `Pulse Alpha Free` 的弃用日，不是本行的**）与 `Thinking Machines` 的发布日；**截止列一律写「无结束日（官方逐字 `free … for a limited time`，未给具体日期）」**。**若误写 `11/6`，`A` 桶会凭空多一条「已过 `2` 天」，且「新增」会被读成「已结束」**（避坑 265 的第二次落法）。
- **⑤ ⚠️ `slim_table.py` 两轮收敛后才取分类统计** —— 本期 `14` 条改写全部用 `set_status()`，没有一条用 `append_note()`；`lint_table.py --strict` 实跑 `CLEAN`、`R1–R4` 全 `0`（055 / 059–061 三期纪律的连续第 `5` 期复用）。
- **⑥ ⚠️ 附录当期段的指针标签会停在上期** —— `patch062_pointers.py` 把 `## 第 062 期` 段内的 `[附录 061](details.html)` 重贴为 `[附录 062](details.html)`、历史段不回改；正文 `〔附录 062〕` 全部链接化。**两处计数都从落盘文件实算**（脚本对「命中 `0` 条」显式断言失败）。**⚠️ 页内不许出现自指链接**（`build_quick.py` 出口对 `href="index.html"` 直接 `exit 1`）。
"""

FOOT = FOOT.replace("{a}", "".join(x + ("　" if k % 2 == 0 else "\n  ") for k, x in enumerate(A_ITEMS)))
FOOT = FOOT.replace("{b}", "".join(x + ("　" if k % 2 == 0 else "\n  ") for k, x in enumerate(B_ITEMS)))

assert md.count(PLACE) == 1, ("脚注占位符不唯一", md.count(PLACE))
md2 = md.replace(PLACE, FOOT.strip("\n"))
io.open(MD, "w", encoding="utf-8", newline="\n").write(md2)

disk = io.open(MD, encoding="utf-8").read()
for ph in ["A26 + B10 + C0 + D179 + E7 = 222", "`4.1` = `55` 行", "`4.2` = `46` 行",
           "常驻未变 `121` 行", "总账全量 `167` 条", "`44 → 46`", "Inkling 2 Small Free",
           "`460 → 461`", "`153`", "`170`", "开关日"]:
    if ph == "开关日":
        continue
    assert ph in disk, ("脚注短语未落盘", ph)
assert "<<<FOOT062>>>" not in disk
print("脚注已写入，回读断言通过；bytes =", len(disk.encode("utf-8")))
