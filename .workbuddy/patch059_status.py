# -*- coding: utf-8 -*-
"""把 gen_table059.py 的 append_note 改成 set_status（整体改写状态列）。

原因：slim_table 只保留「第一句边界」，追加在尾部的注会被裁掉
（054 期纪律③的第三种形态，本期第二次踩到）。
"""
import io

p = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/.workbuddy/gen_table059.py"
s = io.open(p, encoding="utf-8").read()

HELPER = '''def set_status(row, status):
    """整体改写状态列（不是追加）。

    ⚠️ 059 期踩到的坑：slim_table.py 只保留「第一句边界」，追加在尾部的注
       会在瘦身时被裁掉（054 期纪律③的第三种形态）。所以本期改成直接改写状态列，
       让当期事实成为「第一句边界」。
    """
    cells = row.strip().rstrip("|").split("|")
    assert len(cells) == 4, ("字段数异常", len(cells))
    return "|%s|%s| %s |" % (cells[0], cells[1], status)


'''
s = s.replace("def find_one(pred, tag):", HELPER + "def find_one(pred, tag):", 1)

PAIRS = []

PAIRS.append((
    '全量 `455 → 454`（新增 `1`、消失 `2`）、零价 `18 → 16`、`:free` `14 → 12`',
    '''    return set_status(r,
        "🟢 **生效中（动态目录）。 ⚠️（059 期）全量 `455 → 454`、零价 `18 → 16`、`:free` `14 → 12`；"
        "**两个 `:free` 档整批摘下**（`thinkingmachines/inkling:free` 与 `inkling-small:free`），"
        "**付费版原价原上下文一字未动**；新增 `ricursiveai/ripple-65b-preview`（付费 · 北京 `11/5 03:03`）；"
        "**`announcements` 全文 `inkling` 命中 `0` 次**。**")'''))

PAIRS.append((
    '上架第 `3` 天仍在',
    '''    return set_status(r,
        "🟢 **生效中。 ⚠️（059 期）上架第 `3` 天仍在**：`created 1793669930` 未变、`pricing` 仍 `0/0`、"
        "`1,048,576` 上下文、`llms.txt` `4,021` 字节逐字节相同；**并且多了第二个入口** —— "
        "`opencode.ai/docs/zen` 新增 `Crouton Alpha Free`（id `crouton-alpha-free`），清单 `10 → 11`，"
        "**同一隐身模型第一次带 `-free` 后缀出现在别家目录**。**")'''))

PAIRS.append((
    '清单 `10 → 11`：新增 `crouton-alpha-free`',
    '''    return set_status(r,
        "🟡 **生效中（清单动态）。 ⚠️（059 期）`10 → 11`：新增 `crouton-alpha-free`（行名 `Crouton Alpha Free`）；"
        "`LongCat 2.5 Preview Free` 仍 `0` 命中；页面 `57,838 → 58,736` 字节（`+898`）。**")'''))

PAIRS.append((
    '`HF` 官方 `moonshotai/Kimi-K3.1-Pro` 已公开',
    '''    assert "权重未落地" in r
    return set_status(r,
        "🟢 **已兑现（059 期实核：权重已公开）。 ⚠️ `HF` 官方 `moonshotai/Kimi-K3.1-Pro`：`112` 个文件、"
        "`96` 个 `safetensors` 分片、`gated:false`、`private:false`、`license: other`（`kimi-k3.1-pro`）、"
        "仓库卡一手 `2.8T` 总参 / `104B` 激活 / `93` 层** —— **第 ④ 级「能下载」已到，"
        "「能商用」仍要看自定义许可条款（未逐条读）**。⚠️ **官方文档页那句承诺仍逐字未改**（`740,462` 字节、命中 `3` 次）。**")'''))

PAIRS.append((
    '权重已公开，本行的「充值 `10` 元解锁」',
    '''    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（059 期）权重已公开，「充值 `10` 元解锁」现在只约束 API / 在线体验，"
        "不约束下载与自托管** —— 仓库 `gated:false`、`private:false`，无需申请即可拉取。**")'''))

PAIRS.append((
    '`Basic weekly rate limits` 三处命中数仍是 `1`/`1`/`1`',
    '''    return set_status(r,
        "🟡 **生效中（申请制）。 ⚠️（059 期）定价页 `137,595` 字节 —— 与上期逐字节相同**，"
        "`Generally Available` / `$0/month` / `Basic weekly rate limits` 命中数仍是 `1`/`1`/`1`；"
        "**本期首抓的 `12,408` 字节是传输被截断**（文件断在 `CSS` 中间），不是页面变小（避坑 263）；"
        "`/models` 连续第 `7` 期 `404`。**")'''))

PAIRS.append((
    '官方促销数组 `14 → 18`',
    '''    return set_status(r,
        "🟢 **生效中（距结束 `3` 天）。 ⚠️（059 期）官方促销数组 `14 → 18`**（新增 `4`、消失 `0`）："
        "`klingai-video-4-0-flash` / `krea-3`（`11/10`）、`minimax-h3-max-november`（`11/15`）、"
        "`pruna-p-video-2-pro-replace`（`11/19`）；**`pruna-p-video-2-pro-avatar` 的 `endsAt` 就是今天（`11/5`）**。**")'''))

PAIRS.append((
    '告别信 `35,662` 字节',
    '''    return set_status(r,
        "⚠️ **生效中（关停倒计时 · 距今 `1` 天）。 ⚠️（059 期）告别信 `35,662` 字节（上期 `39,747`，`−4,085`）"
        "而 `sunsetting` `5` / `Nov 6` `7` / `effective` `2` 逐字未变** —— **又一次「字节变了、口径没变」**。**")'''))

PAIRS.append((
    '定价页 `41,791` 字节',
    '''    return set_status(r,
        "⚠️ **生效中（距今 `1` 天）。 ⚠️（059 期）定价页 `41,791` 字节 —— 与上期逐字节相同**，"
        "`Free` `9` / `$0` `6` / `50 messages` `6` / `6 free additional` `3` 逐字同值；"
        "**⚠️ `Free` 档是否一并停服，公告里仍没有逐字写**。**")'''))

PAIRS.append((
    '`sensetime.com/cn/news` 现在读得到',
    '''    return set_status(r,
        "⚠️ **生效中（口径）。 ⚠️（059 期）`sensetime.com/cn/news` 读到 `2026/11/03` 的「`SenseNova 6.8 Flash` 正式版发布」条目**"
        "（上期记「无条目」）；**但该页 `限时` 与 `免费` 各 `0` 命中**，`token-plan` `20,820` 字节逐字节同、`截止` `0` 命中"
        " —— **「限时免费」仍只是媒体口径**；**上期未归档该页，无法判定后上架还是漏读**（避坑 260）。**")'''))

PAIRS.append((
    '`20,820` 字节 —— 与 057 / 058 两期逐字节相同',
    '''    return set_status(r,
        "🟢 **生效中。 ⚠️（059 期）`20,820` 字节 —— 与 057 / 058 两期逐字节相同**，"
        "`公测期完全免费开放`／`限时放量`／`6.8 Flash Lite`／`U1 Fast` 各 `1` 次，**仍无截止日**。**")'''))

PAIRS.append((
    '`xiaohuanxiong.com/pricing` `158,318` 字节',
    '''    return set_status(r,
        "🟢 **生效中。 ⚠️（059 期）`158,318` 字节 —— 与上期逐字节相同**；`免费版` `7` / `积分/日` `6` 仍在，"
        "`6.8` / `Flash` / `Lite` 仍各 `0` 命中。**")'''))

lines = s.split("\n")
out = []
i = 0
used = 0
while i < len(lines):
    # 找到 return append_note(r,  开始、以 ")" 结束的块，且块内含某个 PAIRS key
    if lines[i].strip().startswith("return append_note(r,"):
        j = i
        while j < len(lines) and not lines[j].rstrip().endswith(")"):
            j += 1
        block = "\n".join(lines[i:j + 1])
        hit = None
        for key, new in PAIRS:
            if key in block:
                hit = (key, new)
                break
        assert hit, ("未匹配到 PAIRS 的块", block[:120])
        out.append(hit[1])
        used += 1
        i = j + 1
        continue
    out.append(lines[i])
    i += 1

assert used == len(PAIRS), ("替换块数不一致", used, len(PAIRS))
s2 = "\n".join(out)
s2 = s2.replace("print(\"改写行：%d 条 -> %s\" % (len(NOTES), \"、\".join(NOTES)))",
                "print(\"改写行：%d 条 -> %s\" % (len(NOTES), \"、\".join(NOTES)))")
io.open(p, "w", encoding="utf-8", newline="\n").write(s2)
print("patched blocks:", used)
