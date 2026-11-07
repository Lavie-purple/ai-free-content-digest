# -*- coding: utf-8 -*-
"""061 期第四章脚注：把 <<<FOOT061>>> 替换为四段脚注 + ⑤ 工程纪律。

纪律：
  · 计数与明细同源：分布数字先从 check_deadlines.py 实跑 + deadlines.csv 实算，
    断言等于脚注里要写的数字，才允许写入。
  · 写出后回读落盘文件再逐字断言。
"""
import csv
import io
import re
import subprocess
import sys
from collections import Counter

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第061期-2026-11-07.md"
CSV = WS + ".workbuddy/data/deadlines.csv"
PLACE = "<<<FOOT061>>>"

out = subprocess.check_output(
    [sys.executable, WS + ".workbuddy/check_deadlines.py", "--today", "2026-11-07"],
    stderr=subprocess.STDOUT,
).decode("utf-8", "replace")
buckets = {k: int(v) for k, v in re.findall(r"【([A-E])】[^：\n]*：(\d+)\s*条", out)}
print("实跑三态桶:", buckets)
assert buckets == {"A": 25, "B": 11, "C": 0, "D": 178, "E": 7}, buckets
assert "CSV 共 221 条 -> 一致" in out, "对账行没命中（命中 0 条不是通过）"

rows = list(csv.DictReader(io.open(CSV, encoding="utf-8-sig")))
color = Counter(r["紧急度"] for r in rows)
cls = Counter(r["状态"] for r in rows)
print("实算色标:", dict(color))
print("实算状态:", dict(cls))
assert len(rows) == 221
assert color == Counter({"🔴": 5, "🟢": 152, "🟠": 7, "🟡": 22, "⚠": 14, "": 19, "⚪": 2}), color
assert cls == Counter({"crit": 5, "live": 169, "switch": 6, "pending": 23, "unclear": 16, "over": 2}), cls
assert sum(color.values()) == sum(cls.values()) == 221

white = [r for r in rows if r["紧急度"] == "⚪"]
assert len(white) == 2 and buckets["C"] == 0
assert any("ZCode" in r["活动"] and "第 5 天到期" in r["截止原文"] for r in white)
assert any("每日登录领 credits" in r["活动"] and "10 月 12 日至 10 月 16 日" in r["截止原文"] for r in white)
print("⚪ 与 C 的差额 2：两条均逐条归因 ✔")

# 4.2 成员 diff：fx 已毕业，Ripple 与豆包额度行已进
md = io.open(MD, encoding="utf-8").read()
i = md.index("### 4.2 常驻权益本期变更")
j = md.index("> **其余")
r42 = [l for l in md[i:j].split("\n") if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]
assert len(r42) == 44, ("4.2 行数", len(r42))
assert not any("`Vercel Labs` `fx`" in r for r in r42), "fx 仍在 4.2（应已毕业）"
assert sum(1 for r in r42 if "Ripple-65B" in r) == 1, "Ripple 未进 4.2"
assert sum(1 for r in r42 if "豆包工作个人版取消" in r) == 1, "豆包额度行未进 4.2"
print("4.2 成员 diff：出 1（fx 毕业）进 2（Ripple、豆包额度）✔")

FOOT = r"""### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-07` 实跑；CSV 共 `221` 条 —— 取自日报正文表体与《常驻权益总账》两处合并，所以「`221` 条」与「本章可见 `99` 行」不是矛盾）**：

- **【A】已过期但状态仍非收口态：`25` 条 —— 较 060 期的 `23` 条多 `2` 条，逐条归因：正是两条 `11/6` 到期的 `Ollie` 行跨过了基准日**（`Ollie` 关停 ／ `Ollie` 的 `Free` 档 —— 060 期是「关停日当天 `T+0`」，本期是「已过 `1` 天」）。**其余 `23` 条与 060 期同名单、同顺序，每条只前进 `1` 天** —— ① `腾讯老混元大模型平台停服`（2026-09-30，已过 `38` 天，`crit`）② `豆包工作 30 天订阅（新一轮）`（2026-10-17，已过 `21` 天，`live`）③ `Google Nano Banana 2 停用`（2026-10-29，已过 `9` 天，`live`）④ `Runware` `Kling 4.0` 促销（2026-10-29，已过 `9` 天，`live`）⑤ `腾讯智能体平台「元器」停止服务`（2026-10-29，已过 `9` 天，`crit`）⑥ `国家超算互联网` 夜间免费（2026-10-30，已过 `8` 天，`switch`）⑦ `腾讯云 TokenHub` 国际站促销（2026-10-30，已过 `8` 天，`live`）⑧ `HeyGen Voice` 五折（2026-10-31，已过 `7` 天，`live`）⑨ `Laya` 决策模型（2026-10-31，已过 `7` 天，`live`）⑩ `WorkBuddy Intl` 的 `DeepSeek-V4.1-Flash-1017` 限免（2026-10-31，已过 `7` 天，`live`）⑪ `WorkBuddy` 学生版 `1,000` 积分（2026-10-31，已过 `7` 天，`live`）⑫ `智谱清言` 双节积分返还（2026-10-31，已过 `7` 天，`live`）⑬ `湖北算力券`（2026-10-31，已过 `7` 天，`live`）⑭ `腾讯 WorkBuddy Hy3` 限免（2026-10-31，已过 `7` 天，`live`）⑮ `DeepSeek Search` / `Fetch`（2026-11-01，已过 `6` 天，`pending`）⑯ `可灵`「看见微光」大赛（2026-11-01，已过 `6` 天，`live`）⑰ `AutoClaw` 国内站 `M10W4`（2026-11-01，已过 `6` 天，`live`）⑱ `AutoClaw` 国际站 `M10W4`（2026-11-01，已过 `6` 天，`live`）⑲ `Runware` `pruna-p-video-edit`（2026-11-03，已过 `4` 天，`live`）⑳ `Figma Code Layers` 付费计划免费（2026-11-04，已过 `3` 天，`live`）㉑ `Moonshot Kimi K3.1 Pro` 发布（2026-11-04，已过 `3` 天，`live`）㉒ `Anthropic` 生命科学 guest investigators（2026-11-05，已过 `2` 天，`pending`）㉓ `Claude Code` 云会话 credit（2026-11-05，已过 `2` 天，`live`）。
  ⚠️ **本期 A 档的 `25` 条里，仍有一条性质与其它 `24` 条不同**：**`Kimi K3.1 Pro` 那一行虽然日期已过，但事件已经发生**（059 期实核：权重已公开），**状态列在 059 期已改写成「已兑现」** —— **`check_deadlines` 仍把它算进 `A`，因为它只看「截止日 < 基准日 且 状态非收口」**。**桶是筛子，不是结论**（与 059 / 060 期同一条，处置相同：不改脚本，在脚注点名称）。
  ⚠️ **本期 `25` 条的状态列措辞逐条复核过：全程未用收口字样**（避坑 239 —— **053 期踩 `4` 次、054 期踩 `1` 次，055–061 七期均踩 `0` 次**）。
- **【B】14 天内到期：`11` 条 —— 较 060 期的 `13` 条少 `2` 条，成因是「两条 `Ollie` 出桶、无人进桶」**。**逐条按天数**：**`T+0`（`11/7`，今天）一条**：`MiniMax` 开放平台 `M3` / `M2` 免费试用（**060 期是 `T+1`，本期走到 `T+0`，明天即进 `A`**）。**`T+1`（`11/8`）五条**：`Runware pruna-p-video-upscale` `50% OFF` ／ `AutoClaw` 国内站 `M11W1`（`50M`）／ `AutoClaw` 国际站 `M11W1`（`40M`）／ `火山 Coding Plan 2.5 折` ／ `火山方舟 Agent Plan` 个人版 `1000` 次。**`T+5`（`11/12`）一条**：`Anthropic` 新版使用政策。**`T+6`（`11/13`）两条**：`Google AI Plus` 失去 `Pro` 模型选择权 ／ `腾讯轻量云` 专家限量。**`T+8`（`11/15`）一条**：商务部 / 科技部 `2026` 年第 `48` 号公告。**`T+11`（`11/18`）一条**：`MiniMax M2.5` / `M2.7` 系列退役。
  ⚠️ **本期 `B` 桶的 `−2` 与 `A` 桶的 `+2` 是同一件事的两面**：**两条 `Ollie` 从 `T+0` 走到 `已过 1 天`，一进一出，`A +2`、`B −2`，总数不变** ✔。**`MiniMax` 那条从 `T+1` 走到 `T+0` 仍在 `B` 里，所以 `B` 没有继续变薄。**
- **【C】收口态：`0` 条** —— **表体里仍有 `2` 条 `⚪` 收口行，`C` 桶却是 `0`，差额 `2`**。**⚠️ 差额不是常数，本期逐条归因**：**① `ZCode / BigModel 新用户试用`**（截止原文逐字 `连接 BigModel 账号后起算，第 5 天到期` —— **相对期限、无日历日 → 落 `D` 桶**）**② `智谱 AutoClaw「每日登录领 credits」第二期`**（截止原文逐字 `已按原定日期收口（活动期 10 月 12 日至 10 月 16 日，北京）` —— **日期藏在叙述句里、不在可解析字段 → 落 `D` 桶**）。**与 056–060 五期同一对、同一差额 `2` —— 六期连续，结构性差额，不是本期才出现的偏差**（避坑 215）。
- **【D】日期无法解析：`178` 条 —— 较 060 期的 `176` 条多 `2` 条，正是本期补入的 `2` 行**（`豆包工作个人版取消 5 小时额度限制` 与 `Ripple-65B Preview`，截止列都是「无结束日（……无活动期）」）。**`D` 桶的 `+2` 与表体 `+2` 是同一件事，不是两次变化。**
- **【E】窗口外（>14 天）：`7` 条 —— 与 060 期同名单、同顺序**（天猫「AI 空间站」`11/28`、`Character.AI` 第 11 章、`Gemini 4 Argon` `11/30`、杭州 `Coding` 计划 `12/9`、`Gemini 3.8 Flash` 促销价 `12/31`、`Moonshot K2` 停新注册、腾讯云 `TokenHub` 新人免费包）。**⚠️ 连续三期「同值且同成员」** —— **这是本报告少数几个可以同时说「没变」与「没换人」的桶。**
- **对账：`A25 + B11 + C0 + D178 + E7 = 221`，CSV 共 `221` 条 → 一致** ✔。

**②-补 双口径三态（色标口径 vs `classify()` 口径，两套都写、逐条解释差值）**：

- **色标口径（`紧急度` 列）实跑**：**⚪ `2` / 🔴 `5` / 🟢 `152` / 🟡 `22` / 🟠 `7` / ⚠ `14` / 空 `19` = `221`**。
- **`classify()` 口径（`状态` 列）实跑**（**两侧都取自 `slim` 两轮跑完之后重跑的 `deadlines.csv`**）：**`crit` `5` / `live` `169` / `over` `2` / `pending` `23` / `unclear` `16` / `switch` `6` = `221`**。
- **⚠️ 六个桶的差与 060 期同一套算术**：**① 色标 🟢 `152` → `live` `169`，差 `+17` = `19` 条「`紧急度` 列为空、状态列写「生效中」」的行 − 色标 🟢 里被文字改判的 `2` 条**（`Anthropic` 新版使用政策 → `pending` 一条、`OpenCode DeepSeek V4.1 Flash` → `unclear` 一条）；**② 色标 🟡 `22` → `pending` `23`，差 `+1`**；**③ 色标 ⚠ `14` → `unclear` `16`，差 `+2`**；**④ 色标 🟠 `7` → `switch` `6`，差 `−1`**（`Cloudflare` 收购 `Deno` 那条「未开始」归 `pending`）；**⑤ `🔴 5 = crit 5`、`⚪ 2 = over 2`，两个桶成员完全一致（差集都是空）**；**⑥ 两套总数都是 `221`**。
- **⚠️ 与 060 期的逐桶对账**：**色标 🟢 `150 → 152`（`+2`），其余六桶同值；`classify()` `live` `167 → 169`（`+2`），其余五桶同值** —— **`+2` 正是本期补入的 `2` 行（`豆包工作额度` 与 `Ripple-65B`，均 `🟢` 且判 `live`）** ✔。**⚠️ `over` 桶 `2 → 2` 且成员不变 —— 本期 `prune_table.py` 一条都没移出（见 ③）；归档区最后一段仍是 `056 期`，未改动。**
- **⚠️ 「色标亮、`状态` 却是 `pending`」本期 `23` 条**（人工逐条认定）：**055–061 七期同为 `23` 条**。

**③ 逐行 diff + ⚠️ 下一轮强制动作**：

**⚠️ 本期表体 `221` 行 ＝ 060 期 `219` 行 ＋ 本期补入 `2` 行 − 移出 `0` 行**（`gen_table061.py` 实跑 `219 + 2 = 221`、字段数分布 `Counter({3: 221})` 全为 `3` ✔；`prune_table.py` 实跑 **移出 `0` 条**（`221 → 221` 行，归档区未改动）；`split_ledger.py` 实跑 **`4.1` = `55` 行 ／ `4.2` = `44` 行 ／ 常驻未变 `122` 行 ／ 总账全量 `166` 条**）。

**⚠️ `4.2` 的 `43 → 44` 已按纪律做成员 diff，是「出 `1` 进 `2`」，不是「多写一行」**：
- **出 `1` 条**：`Vercel Labs fx` —— **060 期强制动作①本期销项**：把该行残留的 `3` 处 059 期的「本期」重贴为「059 期」，`CHANGE_RE` 不再命中，**按 059 期 `AXON` 的先例毕业进《常驻权益总账》**（`122` 条「常驻未变」里有它）。
- **进 `2` 条**：`豆包工作个人版取消 5 小时额度限制`（`061 期新登记`）、`Ripple-65B Preview`（`061 期补登`）。
- **⚠️ 这一进一出把 060 期那条「正则也是筛子」的账结清了**：060 期 `4.2` 报 `42 → 43`、出 `0` 条，其实是「有一条该毕业的被过期措辞钩住」；**本期 `43 → 44` 是「真出 `1`、真进 `2`」，`44 = 43 − 1 + 2` 可以逐项对上**（`tmp_061` 侧脚本断言过：`4.2` 里 `fx` 命中 `0`、`Ripple` 与 `豆包额度` 各命中 `1`）。**⚠️ 所以「行数变了」这件事本身仍然不说明什么 —— 必须给出「出谁、进谁」。**

**⚠️ 本期补入 `2` 行**：**① `豆包工作个人版取消 5 小时额度限制`**（`11/6` 起、**限额窗口规则变化，不是额度变多**、媒体口径、官方两页零命中）；**② `Ripple-65B Preview`**（`Apache-2.0` · `65B` 稠密 · `12` 万亿 tokens · `1M` 上下文 · `TerminalBench 2.1` `80.52` · **仓库建于 `11/4`，058–060 三期漏登**）。**两行的截止列都写「无结束日」，不写任何日期** —— 见 ⑤②。

**⚠️ 本期改写 `10` 行状态列**（每键在源表恰好命中 `1` 行、全部用 `set_status()` **整体改写**而非 `append_note()`、字段数守恒、**写出后重新读回落盘文件再断言**）：**① `OpenRouter 免费档`（`454 → 460`、零价 `16`、`:free` `12`，成员各换 `1` 个）② `stealth/crouton-alpha`（第 `5` 天仍在、`llms.txt` `4,021` 字节三期间值）③ `OpenCode` 免费清单（`11 → 12`、新增 `iceman-free`）④ `Vercel Labs fx`（**不加状态改写，只重贴 3 处期号** —— 这是归类修正，不是内容更新）⑤ `Kimi K3.1 Pro` 访问条件（`Highspeed` 连续第 `2` 期零命中）⑥ 商汤 `Token Plan`（五期逐字节相同）⑦ 小浣熊免费版（`159,731` 逐字节相同）⑧ 商汤 `6.8 Flash`（`news` 页 `−1,392` 字节、关键词仍零命中）⑨ 百度 `ERNIE`（首次复核：条款三处未变、流通量变了）⑩ `豆包工作 30 天订阅`（拿到规则变化、订阅活动仍未拿到一手）**。
**⚠️ 另有 `8` 行由 `normalize_days061.py` 归一（本期实际改写 `0` 行 —— 说明 gen_table 写入时天数已按新基准日算好），`recalc_days061.py` 独立复核 **`8` 行「距今 N 天」逐行相同、全表 `33` 处天数 token 全部满足「天数 == 截止日 − 基准日」** ✔（**归一与复核是两个脚本**）。

**⚠️ 下一轮强制动作（`062` 期出刊前必须逐条过）**：**① `AI-HOT` 按 `<article>` 解析进常规信源**（本期纠错①的落地）—— **下期要把「`20` 条里有几条落在窗口内」算出来并列进第八章**，本期只做到「能解析」（因为该页时间只有 `HH:MM`、缺日期，需另建「按抓取时刻 − 排序位置」的近似法，**别直接拿 `HH:MM` 当日期**）**② `Inkling 2 Small` 的 `Apache 2.0` 权重是否真的「下周」放** —— 核 `hf-mirror.com/api/models?author=thinkingmachines` 是否长出 `Inkling-2-Small`，**别拿 `Inkling-Small` 当它** ③ `liquid/lfm-3-1.7b:free` 的免费档能活几期 ＋ 它的「提示与输出可能被保留」条款是否改动 ④ `nvidia/nemotron-3.5-content-safety:free` 是彻底移除还是重新上架（**本期三件观测：目录 `460` 条里无、`/endpoints` `200` 且空、`/llms.txt` 未取** —— 下期补 `llms.txt`）⑤ `iceman-free` 是否长出厂商说明（`OpenCode` 页面有无新增字段）⑥ `stealth/crouton-alpha` 第 `6` 天 ＋ `OpenCode` 那份 ⑦ `Runware` `19` 条：`11/8` 的 `pruna-p-video-upscale` 与 `11/10` 两条是否按时收口 ⑧ `Ripple-65B` 的 `downloads` 与 `likes` 下一期怎么走（**并检查 `Ripple-65B-Base-Preview` / `-DFlash2` 两个变体是否也开放**）⑨ `豆包工作` 的官方页面何时长出「周额度」逐字（**目前两页各 `0` 命中**）⑩ `Ollie` 三页是否下线（**关停日次日仍逐字节同值在线**）⑪ `Antigravity` 定价页本期 `000`，下期重抓（**别把「没拿到」写成「同上期」**）＋ `Basic weekly rate limits` 的具体数字（**连续第 `5` 期未追**）⑫ 商汤 `6.8 Flash` 官方「限时免费」截止日（**第 `5` 期**）⑬ `AXON` 许可证与版本号（**连续第 `4` 期未放出**）⑭ `freellm.net` 只在该字段真变动时记一条 ⑮ 老混元 `Q04`（**连续第 `40` 期未决**）、`国家超算互联网`（**连续第 `11` 期**）、`豆包工作` 订阅活动（**第 `17` 期未拿到一手**）⑯ `Mistral` 全站（**连续第 `22` 次 `000`**）、`x.ai/news`（**连续第 `2` 期 `000`**）、`platform.reflection.ai`（**连续第 `24` 期 `403`**）、`platform.openai.com/docs/models`（**连续第 `15` 期 `403`**）、`next.opera.com/web-ai/`（**连续第 `12` 期 `451`**）、`docs.somark.ai/free-tier-rules.md`（**连续第 `7` 期 `404`**）⑰ **把本期「零命中 / 未取到」结论涉及的页面全部入档**（清单见第九章，避坑 260 的落地动作，每期必做）。

**⑤ 061 期的工程纪律（本期实测，都写在这里）**：

- **① ⚠️ 过期措辞会钩住分类正则 —— 060 期的账本期结清，但要记清「结的是什么」**：060 期 `4.2` 报 `42 → 43`、出 `0` 条，真因是 `Vercel Labs fx` 行内 `3` 处 059 期的「本期」被 `CHANGE_RE = re.compile(r"(本期|060\s*期)")` 命中。**本期在 `gen_table061.py` 里做了一次「只重贴措辞、不改语义」的修正**（`本期` → `059 期`，`3` 处），`split_ledger.py` 实跑后该行进入「常驻未变 `122` 行」。**⚠️ 处置边界：只在 `gen_table` 阶段改措辞，绝不在已固化的产物上重跑 `split_ledger`** —— 后者重建 `intro` 会丢 049 期瘦身导语、`post` 会带出重复的 `pointer` 段（060 期已实证）。**这条的本质是「机械分类器需要干净的输入」，不是「分类器错了」。**
- **② ⚠️ `00 后` 的解析器只试一种结构，会连续错很多期** —— `AI-HOT` 的 `__NEXT_DATA__` `0` 命中被连读 `27` 期，而 `<article>` 一直在（本期纠错①）。**脚本层的落法**：`aihot` 解析改成 `re.findall(r'<article[^>]*>(.*?)</article>')`，**并在脚本里对「命中 `0` 条」显式断言失败**（避坑 257：零命中不是通过，是没找到对象）。**⚠️ 时间字段只有 `HH:MM`、没有日期 —— 不要拿它算窗口，本期只用来发现线索。**
- **③ ⚠️ 同一种「空」对应两种状态** —— `"endpoints": []` 既可能是「条目在、没端点」（两个 `inkling:free`），也可能是「条目已从目录移除、端点记录还在」（本期 `nemotron-3.5-content-safety:free`）。**`gen_table061.py` 对这两条分别写了断言**（`liquid/lfm-3-1.7b:free` 的 `1` 个端点、`nemotron` 的 `0` 个端点），**不是用同一个判据写两句话**。
- **④ ⚠️ 新增行的截止列不许写 `createdAt`** —— `Ripple-65B` 的 `createdAt` 是 `11/4`、`lastModified` 是 `11/6`、`OpenRouter` 上架是 `11/5`、媒体报道是 `11/7`，**四个时间点四个含义**；截止列一律写「无结束日（`Apache-2.0` 开源权重，无活动期）」。**若误写 `11/4`，`A` 桶会凭空多一条「已过 `3` 天」，且「补登」会被读成「窗口内发布」**（避坑 265 在脚本层的落法）。
- **⑤ ⚠️ `slim_table.py` 只留状态列第一句 —— 本期 `10` 条改写全部用 `set_status()`**，没有一条用 `append_note()`；两轮 `slim` 收敛后才取分类统计（055 / 059 / 060 三期纪律的连续第 `4` 期复用）。**`lint_table.py` 实跑必须 `CLEAN`，`R1–R4` 全 `0`。**
- **⑥ ⚠️ 附录当期段的指针标签会停在上期** —— `patch061_pointers.py` 把 `## 第 061 期` 段内的 `[附录 060](details.html)` 重贴为 `[附录 061](details.html)`、历史段不回改；正文 `〔附录 061〕` 全部链接化。**两处计数都从落盘文件实算**（脚本对「命中 `0` 条」显式断言失败）。**⚠️ 页内不许出现自指链接**（`build_quick.py` 出口对 `href="index.html"` 直接 `exit 1`）。
"""

assert md.count(PLACE) == 1, ("脚注占位符不唯一", md.count(PLACE))
md2 = md.replace(PLACE, FOOT.strip("\n"))
io.open(MD, "w", encoding="utf-8", newline="\n").write(md2)

disk = io.open(MD, encoding="utf-8").read()
for ph in ["A25 + B11 + C0 + D178 + E7 = 221", "`4.1` = `55` 行", "`4.2` = `44` 行",
           "常驻未变 `122` 行", "总账全量 `166` 条", "`43 → 44`", "Vercel Labs fx",
           "Ripple-65B Preview", "iceman-free", "AI-HOT", "`454 → 460`", "`152`"]:
    assert ph in disk, ("脚注短语未落盘", ph)
assert "<<<FOOT061>>>" not in disk
print("脚注已写入，回读断言通过；bytes =", len(disk.encode("utf-8")))
