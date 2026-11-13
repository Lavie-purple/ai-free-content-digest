# -*- coding: utf-8 -*-
"""067 期第四章脚注④：三态分布（A/B 明细由 check_deadlines --all 输出解析生成，不手抄）"""
import io
import re
import subprocess
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第067期-2026-11-13.md"

out = subprocess.run(["python", WS + ".workbuddy/check_deadlines.py", "--today", "2026-11-13", "--all"],
                     capture_output=True, text=True, encoding="utf-8").stdout.replace("\r", "")


def block(tag_start, tag_end):
    i = out.index(tag_start)
    j = out.index(tag_end)
    return out[i:j]


A = [l for l in block("【A】", "【B】").split("\n") if re.match(r"^  \d{4}-\d{2}-\d{2} ", l)]
B = [l for l in block("【B】", "【C】").split("\n") if re.match(r"^  \d{4}-\d{2}-\d{2} ", l)]
assert len(A) == 32, len(A)
assert len(B) == 8, len(B)


def parse(lines):
    items = []
    for l in lines:
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2}) \((.+?)\)\s+\S+\s+(.*)$", l.strip())
        assert m, l
        items.append((m.group(2) + "-" + m.group(3), m.group(4), m.group(5)))
    return items


ai = parse(A)
bi = parse(B)

a_line = "　".join("`%s`（%s）%s" % (d, t, n) for d, t, n in ai)
b_line = "　".join("`%s`（%s）%s" % (d, t, n) for d, t, n in bi)

FOOT = """### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-13` 实跑；CSV 共 `235` 条 ＝ 本章可见 `4.1` 的 `58` 行 ＋ 《常驻权益总账》`177` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`32` 条（066 期 `31`，`+1`）** —— 唯一进项是 **`11-12` 的 `Anthropic` 新版使用政策**（`11/12` 是它的「生效日」，一天过后就从 `B` 掉进 `A`）。**这不是「哪条活动过期了」，是「生效日也会过期」** —— 本报把「生效日」与「截止日」都塞进同一列，代价就是它们会一起走进 `A`。
  %s

- **【B】14 天内到期：`8` 条（066 期 `8`，同数但成员换了 `2` 个）** —— 出的是 `11-12` 的 `Anthropic` 使用政策（进 `A`），进的是本期补入的 **`11-18`（T+5）MiniMax `H3-Image` `4K` 生图 `5` 折**。其余 `6` 条天数整体 `−1`。
  %s

- **【C】已结束：`0` 条。连续第 `5` 期为空** —— **本报的「已结束」只给有逐字收口口径的条目**，其余一律留在 `A` 里等人工核。

- **【D】日期无法解析：`188` 条（066 期 `186`，`+2`）** —— 本期补入 `2` 条无截止日的常驻权益（`Gemini 4 Hydrogen` 免费入口、`Inkling-2-Small` 开放权重），无归档移出，净 `+2`。`D ≠ 失效`：长期档、政策文件、无结束日的动态目录都在这一桶。

- **【E】窗口外（>14 天）：`7` 条，与 066 期同数同成员**（`11/28` 天猫、`11/30`×2、`12/9`、`12/31`×3）。**对账：`A32 + B8 + C0 + D188 + E7 = 235`，CSV `235` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体实算：`4.1` 的 `58` 行 ＋ 总账 `177` 行，共 `235`）**：

- **色标（活动名列行首）**：⚪`1` / 🔴`5` / 🟢`163` / 🟡`24` / 🟠`8` / ⚠`15` / 空`19` ＝ **`235`**
- **`classify()`（状态列语义）**：`crit 5` / `live 180` / `switch 7` / `pending 24` / `unclear 17` / `over 2` ＝ **`235`**

**⚠️ 两侧必须分开报，不能互相替代**：色标是**人写给人看的优先级标记**，`classify()` 是**脚本按状态列关键词判的**。本期两者在 `over` 上仍差 `1`（色标 ⚪`1` vs `classify over 2`），**差项与 066 期同一条**：`stealth/crouton-alpha` 的状态列写着 `⚪ 已下架`、活动名前的色标还是 🟢。**「⚪ 有几条」永远不能直接当「下架了几条」用**（064 差 `1`、065 差 `2`、066 差 `1`、本期差 `1` —— **差额不是常数，也不是固定符号**）。

**③ 逐行 diff（本期改写 `55` 行状态列 ＋ 补入 `3` 行 ＋ 归档 `0` 行）**：

- **改写 `55` 行**：`4.1` 里 `42` 行、`4.2` 里 `13` 行。**全部走「整体替换状态列」，不做追加**（059 期纪律），字段数守恒（`4.1` `Counter({4: 58})`、`4.2` `Counter({4: 35})`）。
- **补入 `3` 行**：`4.1` 的 **MiniMax `H3-Image` `4K` 生图 `5` 折**；`4.2` 的 **`Gemini 4 Hydrogen` 免费入口** 与 **`Inkling-2-Small` 开放权重**。**三条都带 `067 期补入` 标记** —— 否则会被下一期判成「常驻未变」移进总账（054 期纪律）。
- **归档 `0` 行** —— 本期没有「过期 >`7` 天**且**状态列已写收口口径」的新条目。**Figma `Code Layers`（`11/4`，已过 `9` 天）状态列仍是「已过 N 天」而不是收口语，按纪律留在表体、不归档**；**这一点与 066 期脚注写的「下期按规则归档」不同，本期按实际状态判、不按上期预告判。**
- **天数 token 全部实算**：`55` 行里带天数的每一处都按「截止日 − 2026-11-13」重算，**不是「上期数字 +1」**；`11/13` 到期的两条（`Google AI Plus`、`腾讯轻量云`）改写成「今日（`11/13`）为截止日」，`11/12` 生效的那条改写成「昨日（`11/12`）生效」。**状态列不出现「未开始」**（053 期纪律）。
- **一处口径对齐**：`4.2` 的 `OpenRouter 免费档` 与 `豆包 Seedream 5.0` 两行，本期把**活动名改回与《常驻权益总账》逐字一致**（`472/17/14`、去掉「系列」二字）。**原因：这两行的名字与总账差了两个字，`extract_deadlines` 的 `key()` 认不出是同一行，CSV 会多算 `2` 条（`237` 而非 `235`）** —— **「表体行数」与「CSV 条数」对不上时，先查名字是否逐字一致，别先怀疑抽取器。**

**④ `068` 期强制动作（`12` 条，出刊前逐条过）**：

① `Gemini 4 Hydrogen` 的「自动选模」能否被观测到（免费账号里是否真的会出现 `Hydrogen` 作答）；`Gemini` 应用免费档有没有**额度页**（本期全站 `0` 命中）；`Antigravity` 是否把 `Hydrogen` 也放给免费档
② 文心 `ERNIE 5.5 Flash Preview`：`11/25` **前**权重是否真上 `HF`（`author=baidu` 是否从 `39` 变 `40`）；`OpenRouter` 的 `:free` 是否随承诺日撤下
③ `OpenRouter` 免费区：`:free` `14` 条成员逐条比；`particle-1:free` 与付费档**会不会有一条消失**（若消失就是「换档」，本期的「并排多开」判断要改写）；`gemini-4-hydrogen` 会不会出 `:free`
④ `MiniMax H3-Image`：`11/18 00:00` 后 `4K` 是否回到 `0.4522`；`Runware` 促销数组 `11/17` 那条是否随之下架；`HF` 的 `downloads` 是否起量（本期 `306,718`）
⑤ `Inkling-2-Small`：`downloads` 是否从 `12` 起量；`?author=thinkingmachines` 是否稳在 `8` 个仓库；`OpenCode` 的 `inkling-2-small-free` 是否仍在
⑥ `Claude Meetings` 是否进定价表（连续第 `4` 期 `0` 命中就跑出「上线≠进表」的完整样本）；`Team` / `Enterprise` 之外是否放 `Pro`
⑦ `Token 羊毛` 第 `6` 期：`¥598` 是否第三天持平、卡册是否到 `58`、**`11/13` 那 `12` 条次日定格到多少**（本期起按「次日复读」记账）
⑧ `freellm` 三个计数器是否连续第 `4` 天同向（`542+` / `252` / `11-13`）
⑨ `Runware` 促销数组：`11/15` 到期后是否仍留在数组（**第八次验证「数组里还在 ≠ 在售」**）；条数是否仍是 `20`
⑩ `小浣熊` 双十一价第 `4` 天：卡片 `¥11.11` 是否撤、对比表 `¥29.9` 是否变；`md5` 是否再变
⑪ `AMD` 额度（第 `6` 期）；`Antigravity` 整站能否恢复（第 `3` 期 `000`）；豆包工作四项关键词（第 `24` 期）
⑫ 老混元 `Q04`（第 `42` 期未决）、国家超算（第 `18` 期）、`Mistral`（第 `32` 次 `000`）、`x.ai/news`（第 `12` 期 `000`）、`platform.reflection.ai`（第 `33` 期 `403`）、`platform.openai.com/docs/models`（第 `25` 期 `403`）、`next.opera.com/web-ai/`（第 `21` 期 `451`）、`docs.somark.ai/free-tier-rules.md`（第 `16` 期 `404`）、`ai.meta.com/blog/`（第 `6` 期 `000`）
""" % (a_line, b_line)

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
i = md.index("### ④ 本期第四章脚注")
new = md[:i] + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(new)

disk = io.open(MD, encoding="utf-8").read()
for p in ("A32 + B8 + C0 + D188 + E7 = 235", "⚪`1`", "`live 180`", "昨日（`11/12`）生效", "`068` 期强制动作"):
    assert p in disk, ("脚注缺", p)
print("footnote written | bytes", len(disk.encode()))
print("A:", a_line[:100], "...")
