# -*- coding: utf-8 -*-
"""066 期第四章脚注④：三态分布（A/B 明细由 check_deadlines --all 输出解析生成，不手抄）"""
import io
import re
import subprocess

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
MD = WS + "AI免费内容与权益速递-第066期-2026-11-12.md"

out = subprocess.run(["python", WS + ".workbuddy/check_deadlines.py", "--today", "2026-11-12", "--all"],
                     capture_output=True, text=True, encoding="utf-8").stdout.replace("\r", "")


def block(tag_start, tag_end):
    i = out.index(tag_start)
    j = out.index(tag_end)
    return out[i:j]


A = [l for l in block("【A】", "【B】").split("\n") if re.match(r"^  \d{4}-\d{2}-\d{2} ", l)]
B = [l for l in block("【B】", "【C】").split("\n") if re.match(r"^  \d{4}-\d{2}-\d{2} ", l)]
assert len(A) == 31, len(A)
assert len(B) == 8, len(B)


def parse(lines):
    items = []
    for l in lines:
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2}) \((.+?)\)\s+\S+\s+(.*)$", l.strip())
        assert m, l
        items.append((m.group(2) + "-" + m.group(3), m.group(4), m.group(5)))
    return items


def short(d):
    return {"今天": "今天"}.get(d, d.replace("已过 ", "").replace(" 天", " 天") if d.startswith("已过") else d)


ai = parse(A)
bi = parse(B)

a_line = "　".join("`%s`（%s）%s" % (d, t, n) for d, t, n in ai)
b_line = "　".join("`%s`（%s）%s" % (d, t, n) for d, t, n in bi)

FOOT = """### ④ 本期第四章脚注（口径、逐行 diff、强制动作）

**① 三态分布（`check_deadlines.py --today 2026-11-12` 实跑；CSV 共 `232` 条 ＝ 本章可见 `4.1` 的 `57` 行 ＋ 《常驻权益总账》`175` 条，`4.2` 与总账同源不重复计）**：

- **【A】已过期但状态仍非收口态：`31` 条 —— 与 065 期同为 `31` 条，且是同一批成员：连续第 `2` 期零进零出。** `11/11` 与 `11/12` 两天**没有任何一条表内条目到期**（`Runware` 的 `11/10` 两条是促销数组里的项、不在表体），所以 `A` 的「不变」是「零进零出」，**不是「复核后无变化」**；31 条的天数全部 `+1`。
  %s

- **【B】14 天内到期：`8` 条（065 期 `7` 条，`+1`）** —— 唯一新增的是本期补入的 **`11-25`（T+13）文心 `ERNIE 5.5 Flash Preview` 的权重开源承诺日**；其余 `7` 条与 065 期同成员同日期，只是天数整体 `−1`。
  %s

- **【C】已结束：`0` 条。连续第 `4` 期为空** —— **本报的「已结束」只给有逐字收口口径的条目**，其余一律留在 `A` 里等人工核。

- **【D】日期无法解析：`186` 条（065 期 `185`，`+1`）** —— 本期补入 `2` 条无截止日的常驻权益（`OpenAI` 军人一年 `Plus`、豆包 `Seedream 5.0` 输入图免费），**移出归档 `1` 条**（智谱 `AutoClaw` 第二期），净 `+1`。`D ≠ 失效`：长期档、政策文件、无结束日的动态目录都在这一桶。

- **【E】窗口外（>14 天）：`7` 条，与 065 期同数同成员**（`11/28` 天猫、`11/30`×2、`12/9`、`12/31`×3）。**对账：`A31 + B8 + C0 + D186 + E7 = 232`，CSV `232` 条 —— 一致。**

**② 色标与状态双口径（两侧都取自改表后的表体实算：`4.1` 的 `57` 行 ＋ 总账 `175` 行，共 `232`）**：

- **色标（活动名列行首）**：⚪`1` / 🔴`5` / 🟢`161` / 🟡`24` / 🟠`7` / ⚠`15` / 空`19` ＝ **`232`**
- **`classify()`（状态列语义）**：`crit 5` / `live 178` / `switch 6` / `pending 24` / `unclear 17` / `over 2` ＝ **`232`**

**⚠️ 两侧必须分开报，不能互相替代**：色标是**人写给人看的优先级标记**，`classify()` 是**脚本按状态列关键词判的**。本期两者在 `over` 上差 `1`（色标 ⚪`1` vs `classify over 2`），**逐条归因**：

- `ZCode / BigModel 新用户试用`：色标 ⚪、状态列「登记项已失效（域名变更）」、`classify()` 判 `over`
- **`stealth/crouton-alpha`：色标 🟢、状态列 `⚪ 已下架`、`classify()` 判 `over`** —— **差的这 `1` 条就是它**

**⚠️ 这条差项与 065 期同因**：状态列改了 `⚪`、活动名前的色标没跟着改。**「⚪ 有几条」永远不能直接当「下架了几条」用**（064 期差 `1`、065 期差 `2`、本期差 `1` 且方向相反 —— **差额不是常数，也不能只看符号**）。

**③ 逐行 diff（本期改写 `56` 行状态列 ＋ 补入 `3` 行 ＋ 移出归档 `1` 行）**：

- **改写 `56` 行**：`4.1` 里 `41` 行、`4.2` 里 `15` 行。**全部走「整体替换状态列」，不做追加**（059 期纪律），字段数守恒（两侧逐行 `|` 计数＝`4`）。
- **补入 `3` 行**：`4.1` 的 **文心 `ERNIE 5.5 Flash Preview`**（带 `066 期补入` 标记）、`4.2` 的 **`OpenAI` 军人一年 `Plus`** 与 **豆包 `Seedream 5.0` 输入图免费**（均带 `066 期补入`）。**三条都带当期标记** —— 否则会被下一期判成「常驻未变」移进总账（054 期纪律）。
- **移出归档 `1` 行**：**智谱 `AutoClaw`「每日登录领 credits」第二期**（活动期 `10/12–10/16`、`⚪` 已收口、过期 `27` 天）—— **065 期挂的账本期销项**，原文逐行写入 `.workbuddy/data/deadline_archive.md` 的 `066 期` 段。**移出前后对账：CSV 少 `1` 条、`4.1` 少 `1` 行、归档多 `1` 行，三处同一个数。**
- **天数 token 全部实算**：`56` 行里带天数的每一处都按「截止日 − 2026-11-12」重算，**不是「上期数字 +1」**；`11/12` 当天生效的 `Anthropic` 使用政策改写为「今日（`11/12`）生效」，**状态列不出现「未开始」**（053 期纪律）。

**④ `067` 期强制动作（`14` 条，出刊前逐条过）**：

① 文心 `ERNIE 5.5 Flash Preview`：`11/25` **前**权重是否真上 `HF`（`author=baidu` 是否从 `39` 变 `40`）；`OpenRouter` 的 `:free` 是否随「限时」撤；千帆侧「限时五折」是否仍在（**媒体口径，官方页仍 `0` 命中就继续写媒体口径**）
② `OpenRouter` 免费区：`:free` `13` 条成员逐条比（本期净增来自 `SKU` 迁移，看下期是否有**真新增**）；`bytedance-seed` 三条会不会回来；`deepseek-v4.1-flash-1017` 的 `×25` 是促销结束还是标错改正（**只有两个观测点，不许写「调价」**）
③ `OpenAI` 军人一年 `Plus` 的资格页：能否读到申请条件与截止日（本期只有「See if you're eligible」入口）；`20,000` 这个数会不会更新
④ `Claude` 定价页：`Sheets` / `Whiteboards` 的 `Free` 列**连续第三期**是否仍 `No`；`Claude Meetings` 会不会终于进表（本期整页 `0` 命中）
⑤ `Token 羊毛` 第 `5` 期：`¥598` 是否继续下行、卡册是否再到 `58`、**`11/12` 那 `4` 条之后当天是否能补到 `90+`**（本期只核了 `4` 条）
⑥ `freellm` 三个计数器是否连续第三期同向 `+1`（`536+` / `245` / `11-12`）；`providers` 会不会从 `31` 变
⑦ `tencent/Hy4-preview` 的 `downloads` / `likes` 是否继续涨；正式版 `Hy4` 仓库名会不会出现（**这是本期纠错后的第一条追踪**）
⑧ `Seedream 5.0` 的「输入图免费」是否变；`pro` 的「首张免费」是否仍逐字在
⑨ `Runware` 促销数组：`11/15` 到期后是否仍留在数组（**第七次验证「数组里还在 ≠ 在售」**）
⑩ `小浣熊` 双十一价第 `3` 天是否回落 `¥29.9`；`md5` 是否仍同值
⑪ `AMD` 额度（第 `5` 期）；`Antigravity` 整站能否恢复（本期四个 `URL` 全 `000`）
⑫ `豆包工作` 四项关键词（第 `23` 期）；`doubao.com/work` 是否会给出订阅口径
⑬ 老混元 `Q04`（第 `41` 期未决）、国家超算（第 `17` 期）、`Mistral`（第 `31` 次 `000`）、`x.ai/news`（第 `11` 期 `000`）
⑭ 受阻项：`platform.reflection.ai`（第 `32` 期 `403`）、`platform.openai.com/docs/models`（第 `24` 期 `403`）、`next.opera.com/web-ai/`（第 `20` 期 `451`）、`docs.somark.ai/free-tier-rules.md`（第 `15` 期 `404`）、`ai.meta.com/blog/`（第 `5` 期 `000`）
""" % (a_line, b_line)

md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
i = md.index("### ④ 本期第四章脚注")
new = md[:i] + FOOT
io.open(MD, "w", encoding="utf-8", newline="\n").write(new)

disk = io.open(MD, encoding="utf-8").read()
for p in ("A31 + B8 + C0 + D186 + E7 = 232", "⚪`1`", "`live 178`", "今日（`11/12`）生效", "`067` 期强制动作"):
    assert p in disk, ("脚注缺", p)
print("footnote written | bytes", len(disk.encode()))
print("A:", a_line[:120], "...")
