# -*- coding: utf-8 -*-
"""把第 064 期执行记录追加进自动化记忆（只追加，不改既有内容）。"""

P = ".workbuddy/memory/automations/256c1349-ea4a-4721-9c5d-14067699f1f1/memory.md"

ADD = """
## 第 064 期 · 2026-11-10（窗口 北京 11/9 18:05 → 11/10 12:10，约 18.1h）

### 窗口与性质
- 隔日出刊，窗口 **18.1h**（063 期 22.8h / 062 期 33.9h）。**第一次让整段窗口落在一个完整的美西工作日** —— 起 **11/9 02:05 PT** → 止 **11/9 20:10 PT**（冬令时 `PST`，`UTC−8`，北京快 16 小时）。前四期都卡在「美西周日晚 → 周一凌晨」，美国厂商的周一发布抓不到；本期 `Anthropic` / `Meta` / `OpenAI` / `AWS` 四家的周一发布**全部进窗**。
- 实抓：清单 **285** 行 / 唯一文件名 **285** / 落盘 **285**（063 期清单里 `aihot_news.html` 重复出现 2 次，本期已去重；另新增 `aihot.news/free-tokens` 与 `aihot.virxact.com/free-tokens` 两个直采源）；`200` 共 **198**（69.5%）、`000` 共 **52**（18.2%）；解析 **3,267** 条带时间戳条目、窗口内 **101** 条（`hnrss 20` / `infoq 14` / `techcrunch 11` / `lesswrong 10` / `verge 10` / `aws_ml 7` / `decoder 7`）。

### 头条（一句是「免费档被逐字点名排除」，一句是「到了分发层、没到权重层」）
- **`Claude Fable 5.2` / `Mythos 5.2`（11/9 发布）**：`API` **$8 输入 / $40 输出**每百万 token、`fast mode` **$16 / $80**。**三档必须分开读**：`Max`/`Ultra` 逐字 `Fable included, up to half your weekly limit`；`Pro` 逐字 `Fable, paid with usage credits`；**`Free` 档 `Fable` 命中 `0`**（`claude.com/pricing` `1,325,494` 字节交叉验证）。**发布优惠另算**：`Pro`/`Team` 标准席位 `11/9–11/16 23:59 PT` 含 `Fable`（≤50% 周额度）+1 次重置；`Max`/`Ultra`/高级席位 1–3 次重置、`2027-03-08 23:59 PT` 到期。帮助中心逐字 **`They aren't available on the Free plan`** —— **`They` 指的是 `These offers`，不是模型本身**（避坑 282）。
- **`Inkling 2 Small` 免费档落 `OpenRouter`**（`thinkingmachines/inkling-2-small:free`，零价、**1M** 上下文、17B 激活 / 594B 总参数、`text+image`），而 `HF` 上 `author=thinkingmachines` **仍是 6 个仓库、仍没有 `Inkling-2`** —— **用得上、拿不走，连续第 4 期**。
- 附条：`stealth/crouton-alpha` 上线第 **8** 天**三条线同时消失**（`OpenRouter` `REM` + `llms.txt` `404`/10 字节 + `opencode` 里 `crouton` 命中 `1 → 0`）；`OpenCode` 免费清单**退一进二**（出 `crouton`，进 `LongCat 2.5 Free`、`MiniMax M3.1 Flash Free`），三套口径 `12/12/13 → 13/13/13`。

### 纠错 2 条（都指向同一件事：把「这一次的差异」写成「一般规律」）
1. **063 期「109 处核实标注」是 `HTML` 原始计数**，同一页正文文本口径是 **106**（本期同一文件 `111` vs `108`，差的 3 次落在 `aria-label` / 埋点字符串）。**本期起统一报正文文本口径，并在数字后面写明「正文文本口径」。**
2. **063 期把 `freellm.net` 的 `md5` 差异归因为「`2026-11-8 → 2026-11-9` 两处日期串」** —— 本期同一页面 `170,714` 字节**一字节不差**、日期**根本没变**、`md5` 照样不同，差的是 **`@font-face` 声明顺序**。`md5` 变化的成因至少有四种（日期串 / `Cloudflare` 混淆串 / 字体声明重排 / 服务端构签字段），**任何一种都不足以解释「下次为什么又变了」**（062 期 `OpenCode` 那次是第一次栽）。

### 避坑 282–284
- **282**：「优惠不给免费档」≠「模型不给免费档」。读代词之前先往上找它指的那句；**三个层次（模型可用 / 额度包含 / 优惠覆盖）混成一层，就会写出「免费档被禁用 `Fable`」这种错话**。
- **283**：「单日 `downloads` 不动」不是热度下降 —— `downloads` 是**滚动窗口值、按周期刷新**，`likes` 是**实时累加**，两个字段节奏不同不能并列当趋势；「`md5` 变了」也不是内容变了。**先说「哪个字段、什么口径、观测到几点」，再说「变没变」。**
- **284**：`freely available` ≠ `free` —— 媒体写 `one freely available`，官方原文是 `make it available to all users`，**`freely` 是「无差别开放」，`free` 才是「不要钱」**；中文二次传播最容易压成「免费开放」。

### 规模与对账
- 表体 **227** ＝ `4.1` **57** ＋ `4.2` **49** ＋ 常驻未变 **121**；**总账 170**（＝ 121 + 49）；`CSV 227`；`gen_table064.py` 实跑 `56 + 169 + 2 = 227`（总账基线是 063 期 `split_ledger` 之后的 **169**）。
- `check_deadlines --today 2026-11-10`：**A31 + B7 + C0 + D182 + E7 = 227** ✔。**「A 与 063 同为 31」是零进零出，不是「复核后无变化」** —— `11/9`、`11/10` 两天**没有任何一条表内条目到期**；`B 6→7` 只增 `Fable 5.2` 优惠；`D 181→182` 增 `Inkling 2 Small`（无结束日）；`E 7` 同数同成员。
- 色标 ⚪2/🔴5/🟢156/🟡23/🟠7/⚠15/空19 = 227；`classify()` crit5/live172/switch6/pending24/unclear17/over3 = 227。**`over` 上色标 ⚪2 vs `classify()` 3 差 1** —— 差的是 `crouton` 的「⚪ 已下架」被判成 `over`，**逐条归因，不做「差额是常数」的假设**。
- 改写 **29** 行状态列（`set_status()` 整体改写、字段数守恒 `Counter({3: 227})`）＋ 补入 **2** 行（`Fable 5.2` 优惠 4.1 / `Inkling 2 Small` 4.2，**两条都带「064 期」标记**）＋ 修正 **26** 处天数 token；`recalc_days064.py` 独立复核 **38 处 token 全通过**。
- 一处**口径改写（不是算术修正）**：天猫「AI 空间站」原写「距开卖 `19` 天」，而它 `10/20` 就开卖了 → 改「**已开卖**」（**去数字、不编数字**）。**⚠️ 措辞随时间失真比数字算错更难被发现** —— 算术错会被复核脚本抓住，措辞失真不会。

### 工程坑 7 条
- **① `name_of()` 命中 0 条**：`r.strip().strip("|").split("|")[0]` 带前导空格 → 必须再 `.strip()` 一次。
- **② 落盘断言失败于「数字没加反引号」**：正文写成 `今天还能领 ¥201 → ¥535` 而断言写裸 `` `465` `` → **断言整串、不断言裸数字**。
- **③ `recalc_days064.py` 报 25 处对不上** = 「已过 N 天」全部冻结在 `11/9` 口径上（**056 期避坑 252 的第二次实测**）→ 写 `fix_days064.py` 逐行按「基准日 − 截止日」改真值。
- **④ 腾讯元器多日期行**：脚本取截止列**最后一个**日期（`10/29`）算出 `12` 天，实际指 `11/9` 停服日 → 改「已满 `1` 天」**避开 token**（不编数字）。
- **⑤ `foot064.py` 抓 A 明细抓到 0 条**：`check_deadlines.py` 输出是 **CRLF** → `.replace(chr(13), "")`；行级正则缺 **`re.M`**。另：用 heredoc 替换字符串会把 `\\r\\n` 写成**真实换行**，**改用 `Edit` 工具**。
- **⑥ `audit_color.py` 传错参数**：它要的是 `build_web.py` 路径、不是 `.md` → 放弃该脚本，改用 `classify()` 实算。
- **⑦ `git commit -m @'…'@` 是 PowerShell 的 here-string**（063 期已记）→ 本期用 `git commit -F .git/COMMIT_064.txt`，不要用 `-m` 带 here-string。

### 守卫（全绿）
- `lint_table --strict` **CLEAN（227 行 / R1–R4 全 0）**；`verify_web` **ALL GREEN（18 表 / 106 状态格 / 多色标 0 / 裸 VS16 0 / `section=10 h2=10 h3=22`）**；`check_tables` **ALL GREEN（18 表 / 异常 0）**；`check_frozen` **高危 0 / 引用 29 / 首登 0 / 未出现 420，对账 449**；`check_headlines` **ALL GREEN（64 期 / 不一致 0 期）**；`check_views` / `check_site_freshness` / `chk_eol` 全 exit 0；`build_quick.py --check` **无本期漏登**（19 条相似度提示逐条认定为往期既有缺口或措辞不同）。
- 指针：正文 **106** 处 `〔附录 064〕` → `[附录 064](details.html)`；附录 `## 第 064 期` 段指针**重贴当期期号**，历史段未动（回读断言）。

### 发布
- 产物：日报 `.md` **92,236** B / `.html` **208,932** B；`index.html` = `quick.html` **45,428** B；`archive.html` **43,851** B；`standing.html` **353,374** B；`details.html` **2,957,237** B；`常驻权益总账.md` **215,816** B / **170** 条。
- `data/headlines.json` 加 `"064": "Claude Fable 5.2 发布：Max 档含 Fable、Pro 要付 credits，发布优惠逐字排除 Free 档"`；`data/quick_items.csv` **78 → 80**（补 `Inkling :free`、`LongCat 2.5 Free`；`crouton` 转 `over`；`OpenRouter` 计数更新为 `465/16/13`）。
- commit **`b1892be`** → `git push origin main` **`714e924..b1892be`** 一次成功；**线上六页 md5 逐字节全 SAME**。

### `065` 期强制动作 14 条（已写入 064 期脚注④，出刊前逐条过）
① `Fable 5.2` 的「一周包含」`11/16 23:59 PT` 到期后 `Pro` 是否真回落 `paid with usage credits`；**`Free` 档是否出现 `Fable`**（本期 `0` 命中，第 2 期）② `Inkling 2 Small` 权重是否终于上 `HF`（`6 → 7`？第 5 期）＋ `:free` 条目会不会随「limited time」一起撤 ③ `crouton` 是否以正式名回归（第 2 期）＋ `iceman-free` 是否同步下架 ④ `LongCat 2.5 Free` 的终点日（`11/22` 还是 `11/23`）＋ 厂商侧是否终于开口径（本期 `longcat.chat` 四项关键词各 `0`）⑤ `Token 羊毛` 能否连续第 3 期（`¥535` 是否再跳 + 是否出现「11月11日核实」）⑥ `OpenRouter` 免费区是否再变（`:free` `13` 条成员逐条比）＋ `465` 是否回落 ⑦ `AMD` 正式额度（第 3 期，官方页仍是 `Loading` 壳）⑧ 商汤 `6.8 Flash` 截止日（第 9 期）⑨ `Ollie` 三页（停服第 5 天，仍 `md5` 全同？）⑩ `Antigravity` 定价页能否**连续两期**拿到（本期 `200` / `142,552`）＋ `models` 页（连续第 3 期空）⑪ 豆包工作四项关键词（第 21 期）⑫ `Kimi K3.1-Highspeed`（第 6 期空）＋ `tencent/Hy4`（第 5 期 `404`）⑬ 老混元 `Q04`（第 39 期未决）、国家超算（第 15 期）⑭ 受阻项：`Mistral`（第 28 次 `000`）、`x.ai/news`（第 8 期 `000`）、`platform.reflection.ai`（第 29 期 `403`）、`platform.openai.com/docs/accounts/models`（第 21 期 `403`）、`next.opera.com/web-ai/`（第 17 期 `451`）、`docs.somark.ai/free-tier-rules.md`（第 12 期 `404`）、`ai.meta.com/blog/`（第 2 期 `000`）。
"""


def main():
    with open(P, "rb") as f:
        old = f.read()
    assert old.endswith(b"\n"), "记忆文件结尾不是换行，先人工确认"
    before = old.decode("utf-8")
    HEAD = "\n## 第 064 期 · 2026-11-10"
    if HEAD in before:
        # 幂等：已追加过就跳过（本脚本第一次执行时在断言处中断，块已落盘）
        print("已存在 064 期记录，跳过追加（幂等）")
        print("当前字节", len(old), "064 标题数", before.count(HEAD))
        return

    with open(P, "ab") as f:
        f.write(ADD.encode("utf-8"))

    with open(P, "rb") as f:
        new = f.read().decode("utf-8")

    # 落盘复读断言（053 期纪律：断言是必要条件、不是充分条件）
    assert before in new, "既有内容被破坏"
    # 只数「行首标题」：正文里还有一处 `附录 ## 第 064 期 段` 的引述，不是标题
    assert new.count(HEAD) == 1, "期号标题重复"
    for ph in [
        "## 第 064 期 · 2026-11-10",
        "A31 + B7 + C0 + D182 + E7 = 227",
        "**总账 170**",
        "commit **`b1892be`**",
        "714e924..b1892be",
        "线上六页 md5 逐字节全 SAME",
        "## 第 063 期",
        "`065` 期强制动作 14 条",
    ]:
        assert ph in new, "缺片段: " + ph

    print("OK 追加完成")
    print("旧字节", len(old), "-> 新字节", len(new.encode("utf-8")))
    print("新增行数", new.count("\n") - before.count("\n"))
    print("064 期标题数", new.count("## 第 064 期"))


if __name__ == "__main__":
    main()
