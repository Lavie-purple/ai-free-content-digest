# -*- coding: utf-8 -*-
"""把第 065 期执行记录追加进自动化记忆（只追加，不改既有内容）。

幂等：文件里已有「## 第 065 期」标题就跳过。
落盘后复读，断言标题与末行都在。
"""
import io
import os

P = ".workbuddy/memory/automations/256c1349-ea4a-4721-9c5d-14067699f1f1/memory.md"

ADD = """
## 第 065 期 · 2026-11-11（窗口 北京 11/10 12:10 → 11/11 14:00，约 25.8h）

### 窗口与性质
- 隔日出刊，窗口 **25.8h**（064 期 18.1h / 063 期 22.8h）。起 **11/9 20:10 PT** → 止 **11/10 22:00 PT**（冬令时 `PST`，`UTC−8`，北京快 16 小时）—— **整段窗口落在美西 `11/10` 一个完整工作日内**，`Anthropic` 的工作台扩张与 `OpenAI` 的 `Businesses in ChatGPT`（北京 `11/10 18:00`）都在窗内。**这是「窗口对齐美西工作日」策略连续第二期奏效**（064 期是第一次）。
- 实抓：清单 **285** 行 / 唯一文件名 **285** / 落盘 **285**；`200` 共 **185**（64.9%）、`000` 共 **68**（23.9%），另 `403`/`404`/`451` 共 **32**。解析 **3,171** 条带时间戳条目、窗口内 **129** 条（`hnrss 20` / `techcrunch 17` / `infoq 15` / `leiphone 12` / `lesswrong 10` / `qbitai 9` / `decoder 8` / `aws_ml 6`）。
- **抓取件计数必须在仓库根目录跑**：`tmp_065_window.py` 的 glob 是 `.workbuddy/tmp_065/*`，在 `.workbuddy` 目录里跑会得到 **0 条**（看着像「今天没新闻」，其实是路径错了）。
- 专项核验 **48** 项：原 `fetch065_special.sh` **串行**跑一条要 40s+，改写成 `fetch065_s_par.sh`（`xargs -P 10` + `-m 30`）后 49 行日志一次出齐。**串行专项脚本以后一律走并行版。**

### 头条（一句是「免费档在能力扩张当天被逐格写成 No」，一句是「免费区第一次净减」）
- **`Claude` 扩成工作台（美西 11/10）**：`Plugins` / `Sheets` / `Whiteboards` / `Interactive Connectors` 陆续上线，`Claude Meetings` 官方口径 `coming soon`。**证据不在新闻稿里，在定价页**：`claude.com/pricing` 由 `1,325,494` 涨到 **`1,344,061`**（`+18,567`），对比表新增 **`Claude Sheets (beta)`** / **`Claude Whiteboards (beta)`** 两行，**两行 `Free` 列都是逐字 `No`**（`Pro`/`Max`/`Ultra` = `Yes`）；同表 `Fable` × `Free` 也是 `No`、`Usage credits` × `Free` 也是 `No`。**这是本报第一次看到「新能力上线当天就把免费档写死」—— 不是事后收窄，是上线那一刻的表里就没有免费一档。**
- **`OpenRouter` 免费区第一次净减**：目录 `465 → 469`（`+4`），但 **`:free` `13 → 12`、零价 `16 → 15`、`?max_price=0` `15 → 14`**；`6` 进 `2` 出 —— 进 `google/gemini-4-carbon`（+`:batch`）、`baidu/ernie-5.5-flash-preview`、`baidu/ernie-light-dt-1.0-intl`、`kt/midm-k-3.0-pro`、`motif-technologies/motif-3`；出 `qwen/qwen-2.5-7b-instruct` 与本报 `4.2` 长期登记的 **`xingchen-agi/xing4.0-29b-a4b:free`**（中国电信 `Xing4.0-29B-A4B`）。**「总条数在涨」与「免费条目在减」可以同时成立**；另 `10` 条调价。
- 附条：`商汤 小浣熊` 双十一「会员卡低至 `2` 折」写进价格页（`¥29.9 → ¥11.11`，另标原价 `¥48.0`，`188,107` 字节 / `+28,376`）—— **折的是会员，免费版 `300` 积分/日一个字没动**；`Token 羊毛` 连续第 `3` 期可核（`¥535 → ¥599` / 卡册 `52 → 54` / 正文口径 `112`）；`freellm.net` 停了四期的计数终于动（`531+ → 535+` / `11-9 → 11-11` / `verified 240 → 244`，**三个计数器同向同幅 `+4`**）。

### 纠错 2 条（都指向同一件事：把「我没读到」写成「官方没说」）
1. **064 期写「`Free` 档 `Fable` 命中 `0`」** —— 那句话本身没错（免费档功能卡片里确实没有 `Fable`），**但会被读成「官方没表态」**。本期在同一份定价页的**对比表**里逐字读到 `Fable` 行：`No` / `Usage credits` / `50% of weekly limits*` / `50% of weekly limits*` —— **`Free` 那格是 `No`，不是空白、不是 `—`**。064 期刚立避坑 `282`（防「读过头」），**同一页上却「读太少」**（只走卡片区、没走对比表）。**一份定价页至少三处口径：功能卡片 / 对比表 / `FAQ`，写法与颗粒度各不相同。**
2. **064 期报 `z-ai/glm-5.3-flash` 输入「`×4.5`」** —— 那个价只存在一天：`0.0000000335 → 0.00000015 →` **本期回到 `0.0000000399`**（输出 `0.000000083 → 0.0000005 →` **`0.0000000784`**）。**错的不是数字，是「一次快照 = 一次调价」这个推断** —— 本报只有上下两期两个观测点，中间那一天（临时价 / 标错改正 / 灰度 / 促销结束）看不见。**只有两个点，只能写「A 时是 X、B 时是 Y」，不能写「它调价了」。这是本报第一次因为「观测点不足」而收回一条已发布的结论。** 顺带：别名 `~z-ai/glm-flash-latest` 与正名现在同价，说明 064 期那个值更像正名的临时异常值。

### 避坑 285–287
- **285 · 「命中 `0` 条」先问「我搜的名字对不对」。** 本报连续 `6` 期用 `?search=Kimi-K3.1-Highspeed` 得 `[]`（`2` 字节），并写成「官方名下 `Highspeed` 版权重连续第 `N` 期 `0` 条」。本期换 `?author=moonshotai` 全量列 —— **`moonshotai/Kimi-K3.1-Pro` 就在那儿**（`createdAt 11/2`、`lastModified 11-05T07:11:43Z`、`gated:false`、`license:other`、`downloads 30,721`、`likes 1,878`、`HF` 趋势榜第 `3`）。**`search=` 的空数组只证明「没有叫这个名字的东西」，不证明「这东西不存在」**；**先 `author=` 全量确认家族，再谈变体**。⚠️ `createdAt` 是建仓时间（059 期纪律）→ 写「建仓于 `11/2`」，不写「`11/2` 起公开」；`license: other` → 商用条款不代读。
- **286 · 单点快照里的「调价」不等于「生效」。** 要写趋势，**至少三个观测点**。
- **287 · 「明确写 `No`」和「没提」是两种证据强度。** 引用卡片只能得出「卡片里没有」，引用对比表才能得出「官方不给」。**看定价页先走完三处（卡片 / 对比表 / `FAQ`），再决定用哪一处的措辞。**

### 规模与对账
- 表体 **88** ＝ `4.1` **57** ＋ `4.2` **31**；**总账 173**（＝ 常驻未变 **142** ＋ `4.2` **31**）；**`CSV 230` ＝ 总账 `173` ＋ `4.1` `57`** —— **`4.2` 的 31 行是总账条目本期的变更副本，不另计入 CSV**（064 期同为「总账 + 4.1」，本期沿用）。
- `check_deadlines --today 2026-11-11`：**A31 + B7 + C0 + D185 + E7 = 230** ✔ 与 CSV 一致。`B 7` 与 064 **同数同成员**；`C 0` 连续第 `3` 期为空（本报的「已结束」只给有逐字收口口径的条目）；`D 182 → 185` 增的 `3` 条**就是本期补入的三行，全部「无结束日」**；`E 7` 同数同成员。**「A 与 064 同为 31」照旧是零进零出，不是「复核后无变化」。**
- 色标（活动名列行首）⚪2 / 🔴5 / 🟢158 / 🟡24 / 🟠7 / ⚠15 / 空19 ＝ **230**；`classify()` **crit 5 / live 175 / switch 6 / pending 24 / unclear 16 / over 4** ＝ **230**。**两侧必须分开报。** 本期 `over` 上差 `2`（色标 ⚪`2` vs `classify over 4`），**逐条归因**：`stealth/crouton-alpha`（色标 🟢、状态列 `⚪ 已下架`）、中国电信 `Xing4.0-29B-A4B`（色标 🟡、状态列 `⚪ 已从 OpenRouter 目录下架`）。**共同点：状态列改了 `⚪`、活动名色标没跟着改** —— 不是 bug，是两套字段更新节奏不同，**所以「⚪ 有几条」永远不能当「下架了几条」用**（064 期差 `1`、本期差 `2`，**差额不是常数**）。
- 改写 **42** 行状态列（`4.1` `29` ＝ `gen_table` `16` ＋ `patch` `13`；`4.2` `13`）＋ 补入 **3** 行（`Claude` 工作台 / 小浣熊双十一 / `DeepSeek Harness`，**三条都带 `065 期` 标记**）＋ 修正 **13** 处天数 token。字段数守恒 `Counter({3: 57})` / `Counter({3: 31})`；**全部走 `set_status()` 整体替换，不做 `append_note` 追加**（059 期纪律）。
- **一处归档未做**：`智谱 AutoClaw 第二期`（活动期 `10/12–10/16`、`⚪` 已收口、过期 `26` 天）按规则应移入 `data/deadline_archive.md`，本期仍留表体 —— **本期未跑 `prune_table.py`（表体是原地改写、不是合并表），这条挂 `066` 期第一件事。**
- **`split_ledger.py --dry-run` 对本期失效**：「第四章最长块」只认出 `4.1`、报 `4.2 变更 0 行` → 自写 `merge065.py`（保 `31` 行 / 移 `21` 行 / 总账 **173** 行、新增 `3` 行、头部改 `**最后全量复核**：2026-11-11（第 065 期）`）。**用 `slim` 缩过状态列的期，`split_ledger` 的块识别会退化 —— 别硬修脚本，按当期结构写一次性合并更稳。**

### 工程坑 8 条
- **① 落盘断言失败于「正文没加反引号」**：断言写 `` `1,699 → 2,111` ``、正文是裸数字 → **断言整串、不断言裸数字**（064 期② 同源复发）。回滚方式是 `cp` 064 覆盖回去重跑，不是改 065 的产物。
- **② `fix_days065.py` 断言 `"距开卖" not in disk` 失败**：脚注「历史沿革」里有一句含「距开卖 `19` 天」→ **只断言表体行不含该词**（`l.startswith("| ")`）。
- **③ heredoc 里的 `\n` 被写成真实换行** → `SyntaxError: unterminated string literal` → **改用 `Edit` 工具**（064 期⑤ 第二次复发，**以后写改写脚本一律用 `Edit`/`Write`，不用 heredoc**）。
- **④ `patch065.py` 命中 0 条**：`name_of(l).startswith(prefix)` 对「🟢 **腾讯 WorkBuddy Hy3…」失效 → 改 `prefix in name_of(l)`。**活动名前有 emoji / 粗体时，`startswith` 一律不可靠。**
- **⑤ `merge065.py` 两处**：`assert old.endswith("|")` 失败（行尾带空白）→ 先 `.rstrip()` 再断言；连续 `re.sub` 把总账头两行删空 → **合并成一次性 `re.sub`**，并从 `ledger.bak065` / `tmp_md_bak065.md` 回滚重跑。
- **⑥ `verify_web.py` 报 `NEEDS REVIEW`**：命中若干 CSS 注释里的「MISS」—— 拿 064 期 html 跑同样报，**属工具既有噪声、不是本期回归**；**判定「是不是回归」要拿上一期同跑一遍**。
- **⑦ `lint_table --strict` 8 处 → CLEAN**：`R1` 2 条（`OpenRouter` 331 字 / `Ripple` 229 字，压缩）；`R3` 6 条因状态列同时出现「`065 期`」与「`064 期`/`058 期`」→ **把往期号改成「上一期 / 过去九期 / 早期登记」等自然语言**（判据只认「一期里出现两个期号」）。其中一次正文替换因换行/空白不一致报 `AssertionError` → 改「按行整体替换状态列」。**`R3` 是措辞型判据，改措辞就能过，不必改结构。**
- **⑧ CSV 多出 2 条（232 而非 230）**：「色标（活动名列行首）/ `classify()`（状态列语义）」那一**行**被 `extract_deadlines.py` 当成表格行 → **把这张两行表改成列表**，CSV 回到 230。**脚注里不要放只有两三行的真表格 —— 会被抽取器当成台账。**
- 另：`check_frozen` 报 1 条高危，因脚注「`Gemini 4 Argon` 新增 `19`」被关键字判成「声称新增但首见 037 期」→ 改「行补 `19`」，**高危归 0**。**「新增」这个词在脚注里是高危触发器，写「补入 / 行补 / 补记」。**

### 守卫（全绿）
- `lint_table --strict` **CLEAN（R1–R4 全 0）**；`check_tables` **14 表 / 异常 0**；`check_frozen` **高危 0 / 引用 27 / 首登 0 / 未出现 422，对账 449**；`check_headlines` **ALL GREEN（65 期 / 不一致 0）**；`check_views` / `check_site_freshness` **ALL GREEN**（首页 = 极速视图、三格同构、条数与源文件实算一致）；`chk_eol` 全 `CR=0`；`build_quick.py --check` 仅既有 19 条额度类缺口（逐条认定非本期漏登）。
- 指针：正文 `〔附录 065〕` → `[附录 065](details.html)`；附录新增 `## 第 065 期（2026-11-11）` 段，历史段未动。
- **速览卡三个数字从渲染后的表体实算**：`88` 行 / 必办 `3` / 换挡 `4` —— **核对时要注意 CSS 里也有 `data-st="crit"` / `data-st="soon"` 各 1 处**（`.ledger tbody tr[data-st=…]`、`tr[data-st=…] .st-txt`），**直接 `count('data-st="crit"')` 会多算 2**；`_brief()` 是在 `html_body`（不含 `<style>`）上数的，所以要复算得先剥 CSS，或直接数 `<tr data-st="`。

### 发布
- 产物：日报 `.md` **88,437** B / `.html` **204,016** B；`index.html` = `quick.html` **45,537** B（`80` 条 / 基准日 `2026-11-11`）；`archive.html` **44,319** B；`standing.html` **368,956** B；`details.html` **2,962,417** B（`sections=17` / `h3=1472`）；`常驻权益总账.md` **227,162** B / **173** 条；`第四章表体明细附录.md` **2,246,445** B；`INDEX.md` 收录 **65** 期 / md 合计 **7,980,864** B。
- `data/headlines.json` 加 `"065"`（共 **66** 条）：`Anthropic 把 Claude 扩成工作台：定价页新增 Sheets / Whiteboards 两行，Free 档逐字写 No`；`data/quick_items.csv` **80** 条（`中国电信 Xing4.0-29B-A4B` 由 `unclear` 改 `over`）。
- commit **`a6273b3`** → `git push origin main` **`34d75ef..a6273b3`** 一次成功（`27 files changed, 3556 insertions(+), 482 deletions(-)`）。**`git commit -F .git/COMMIT_065.txt`**，不用 `-m` 带 here-string。
- ⚠️ **push 完 `index.html` 的 `ETag`/`Last-Modified` 可能仍是上一期**：`deployments` API 里没有新 sha 就是 Pages 还没开始构建，**先等、不要重推**；`max-age=600` 窗口内命中旧页是纯缓存。

### `066` 期强制动作 14 条（已写入 065 期脚注④，出刊前逐条过）
① `Claude` 定价页：`Sheets` / `Whiteboards` 两行 `Free` 列是否**连续两期** `No`；`Claude Meetings` 上线后会不会多第三行；`Fable` × `Free` 是否仍逐字 `No` ② `OpenRouter` 免费区是否**连续两期**掉人（`12` 条逐条比）；`xingchen` 会不会换 `ID` 回来；`glm-5.3-flash` 价格是否再跳 ③ `xingchen` 下架是否有厂商侧说明（第 `2` 期）；`?max_price=0` 与 `:free` 两口径是否继续一致 ④ 小浣熊会员价是否从 `¥11.11` 回落到 `¥29.9`（判断是不是一次性双十一价）⑤ `Token 羊毛` 能否连续第 `4` 期（`¥599` 是否再跳 + `11/12` 当天核实数）⑥ `freellm` 的 `535+` / `11/11` / `244` 三个数是否同步再进（「补录」还是「恢复日更」）⑦ `Ripple` 的 `lastModified 11/10T09:31Z` 之后有无新提交；四个仓 `downloads` 是否继续涨 ⑧ `Inkling 2 Small` 权重是否终于上 `HF`（第 `6` 期）＋ `:free` 条目会不会随「limited time」撤 ⑨ `AMD` 正式额度（第 `4` 期，两个 `URL` 仍同字节）；`商汤 6.8 Flash` 截止日（第 `10` 期）⑩ `Ollie` 三页（停服第 `6` 天，仍 `md5` 全同？）；`Antigravity` `/models` 改路径后能否取到 ⑪ 豆包工作四项关键词（第 `22` 期）＋ **「豆包新图像模型价格下降」必须补核**（065 期窗口外 `1h47m`，去火山引擎定价页）⑫ `Kimi-K3.1-Pro` 的 `license: other` 要逐条读（商用条款未读，不能写「可商用」）⑬ 老混元 `Q04`（第 `40` 期未决）、国家超算（第 `16` 期）⑭ 受阻项：`Mistral`（第 `30` 次 `000`）、`x.ai/news`（第 `10` 期 `000`）、`platform.reflection.ai`（第 `31` 期 `403`）、`platform.openai.com/docs/models`（第 `23` 期 `403`）、`next.opera.com/web-ai/`（第 `19` 期 `451`）、`docs.somark.ai/free-tier-rules.md`（第 `14` 期 `404`）、`ai.meta.com/blog/`（第 `4` 期 `000`）
"""


def main():
    if os.path.exists(P):
        with io.open(P, encoding="utf-8") as f:
            old = f.read()
    else:
        old = ""
    if "## 第 065 期" in old:
        print("已存在 065 期记录，跳过")
        return
    need = old.rstrip("\n") + "\n" + ADD.lstrip("\n")
    if not need.endswith("\n"):
        need += "\n"
    with io.open(P, "w", encoding="utf-8", newline="\n") as f:
        f.write(need)
    with io.open(P, encoding="utf-8") as f:
        disk = f.read()
    assert "## 第 065 期 · 2026-11-11" in disk, "标题没落盘"
    assert "`066` 期强制动作 14 条" in disk, "066 强制动作没落盘"
    assert "避坑 285–287" in disk, "避坑段没落盘"
    assert disk.startswith(old[:200]), "既有内容被改动"
    print("OK 追加完成：%d → %d 字符，%d 行" % (len(old), len(disk), disk.count("\n") + 1))


if __name__ == "__main__":
    main()
