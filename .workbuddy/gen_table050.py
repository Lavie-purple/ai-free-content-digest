# -*- coding: utf-8 -*-
"""从 049 期 md 的 4.1 表体 + 《常驻权益总账》全量表体 -> 基准日 2026-10-28 -> 行级改写 -> 追加本期新行。
输出 .workbuddy/tmp_table050.md（纯表格块，供 050 期正文嵌入）。

本期（050）与 049 的差别：
  1) **基准日 10/28（隔日出刊）** —— 「距今 N 天」按「截止日 − 基准日」重算，**每行都变**（基准日推进一天）。
  2) 输入结构沿用 047 期起的结构：上期 4.1 表体（57 行）+ 总账全量表体（132 行）= 189 行。
     **4.2 的 19 行已含在总账里、不可重复加**。
  3) 本期重点改写：OpenRouter 免费档（464/19/16，:free 无增无减）、Kling 4.0 / Runware 促销表 12->13、
     NVIDIA nemotron-3-super-120b-a12b 厂商侧 Free Endpoint=Deprecated（049 挂账项⑮销项）、
     百度 Unlimited OCR 2 官方基准分实读（049 挂账项⑯销项）、Unsloth GGUF 模型卡原文（049 挂账项⑨销项）、
     OpenCode 免费清单 10 项（LongCat 连续第 4 期未回归）、freellm 六项计数器全同值。
  4) 本期新增 4 行：Opera WebAI（浏览器本地 AI 标准）、OpenRouter CSAM 筛查与 ZDR 例外、
     Runware pruna-p-video-upscale 50% 促销（至 11/8）、NVIDIA 厂商侧 nemotron 免费端点弃用。
"""
import io
import re
from datetime import date

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
SRC_MD = WS + "AI免费内容与权益速递-第049期-2026-10-27.md"
SRC_LED = WS + "常驻权益总账.md"
OUT = WS + ".workbuddy/tmp_table050.md"
BASE = date(2026, 10, 28)
PREV = 189


def rows_of(md, start_marker, end_marker=None):
    i = md.index(start_marker)
    j = md.index(end_marker) if end_marker else len(md)
    seg = md[i:j]
    return [l for l in seg.split("\n")
            if l.startswith("| ") and not l.startswith("| 活动 |") and not l.startswith("| --- |")]


md = io.open(SRC_MD, encoding="utf-8").read().replace("\r\n", "\n")
led = io.open(SRC_LED, encoding="utf-8").read().replace("\r\n", "\n")

rows_41 = rows_of(md, "### 4.1 限时动作", "### 4.2 常驻权益本期变更")
rows_led = rows_of(led, "## 一、全量表")
assert len(rows_41) == 57, ("049 期 4.1 表体行数", len(rows_41))
assert len(rows_led) == 132, ("总账全量行数", len(rows_led))
body = rows_41 + rows_led
assert len(body) == PREV, (len(body), PREV)

header = "| 活动 | 截止 | 状态 |"
sep = "| --- | --- | --- |"

REWRITE = {}


def build(key, subs, tail=None):
    hits = [l for l in body if key in l]
    assert len(hits) == 1, ("键未唯一命中", key, len(hits))
    out = hits[0]
    for a, b in subs:
        assert a in out, ("片段未命中", key, a[:60])
        out = out.replace(a, b)
    if tail:
        assert out.rstrip().endswith("|")
        out = out.rstrip()[:-1].rstrip() + " " + tail + " |"
    return out


# ---- 1) OpenRouter 免费档：本期 464/19/16，全量 +1、:free 与零价同值 ----
REWRITE["🟢 **OpenRouter 免费档（**官方 API 目录口径"] = build(
    "🟢 **OpenRouter 免费档（**官方 API 目录口径",
    [
        ("**官方 API 目录口径 · `463/19/16`**", "**官方 API 目录口径 · `464/19/16`**"),
        ("**⚠️ （049 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-27 19:4x，"
         "**本轮连抓三次、三次读数完全一致**）**：**全量 `463` / 零价 `19` / `:free` `16`**；"
         "**与 048 期（463/20/17）比：全量同值、零价 `−1`、`:free` `−1`**。",
         "**⚠️ （050 期）官方 API 目录重取（`openrouter.ai/api/v1/models`，读于 2026-10-28 09:0x，"
         "**本轮连抓四次、四次读数完全一致**）**：**全量 `464` / 零价 `19` / `:free` `16`**；"
         "**与 049 期（463/19/16）比：全量 `+1`、零价同值、`:free` 同值**。"),
        ("**⚠️ `:free` 16 条逐条 diff：消失 `1` 条 —— `nvidia/nemotron-3-super-120b-a12b:free`、无新增**；",
         "**⚠️ `:free` 16 条逐条 diff：新增 `0` 条、消失 `0` 条（连续第 2 期无变动）**；"),
        ("**⚠️ `openrouter.ai/announcements` 本轮实访仍停在 `October 14, 2026`**（041–049 连续九期无新限免公告）。",
         "**⚠️ `openrouter.ai/announcements` 本轮实访出现新条目（`October 27, 2026`）——"
         "041–049 连续九期「停在 `October 14, 2026`」的连续计数本期结束**；"
         "**⚠️ 但这条新公告的内容是 `CSAM Screening Across OpenRouter`（内容安全筛查与数据留存），不是限免** —— "
         "**「终于有新公告」不等于「有新的免费活动」**（避坑 116）；"
         "**其对 ZDR 承诺的影响已单独成行登记（见下）**。"),
    ],
    tail="**⚠️ （050 期）全量逐条 diff**：**新增 `1` 条 —— `prism-ml/ternary-bonsai-2-9b`**"
         "（一手字段：`prompt $0.00000008` / `completion $0.00000013` 每 1M、`ctx 262,144`、"
         "`created 1792130995` ＝ **北京 10/16 14:09**）；**消失 `0` 条**；"
         "**`+1 −0 = +1`，与总数差 `463 → 464` 完全对得上** ✔（避坑 100 存档版：要 diff 什么，就先存档什么）。"
         "**⚠️ 这是避坑 215 的反向样本 —— 总数变了、免费档一分没变**："
         "**只报「全量 464」会让读者以为免费档也动了；只报「`:free` 16 条无变化」会让读者以为目录没动**。"
         "**因此三个数必须一起报（全量 / 零价 / `:free`）**（避坑 220）。"
         "**⚠️ 「零价 19」与「`:free` 16」差 `3` 个 —— `google/lyria-3-pro-preview`、`google/lyria-3-clip-preview`、"
         "`openrouter/free`（路由器）—— 本期实跑复核，与 049 期结论一致；"
         "**反向差集仍为空**（所有 `:free` 后缀模型的 `prompt` 与 `completion` 都确实是 `0`）✔。"
         "**⚠️ `freellm.net` 首页计数器（读于 2026-10-28 09:0x）逐项记账**："
         "**Hero `534+`（同值）；`Models Tracked` `534`（同值）；`Free & Online` `303`（同值）；"
         "`Providers` `31`（同值）；`No Credit Card` `452`（同值）；「经实时 API 验证」`243`（同值）；"
         "`Latest free LLM API model update: 2026-10-27`（同值）** —— "
         "**六项全部同值，即 048→049 的 `+3` 是一次性推进、此后连续两期未再动**（避坑 216）。"
         "**⚠️ `freellm` 的 `OpenRouter` 页标题仍写「`20` 个免费模型在线」**（`Last Updated 2026-10-27`、"
         "`Free Tier` 限 `200 req/day`、上下文 `66K – 1.0M`）—— "
         "**与官方目录 `:free 16` 的差额本期是 `4`（不再是 `1`），第 7 次记账，两个数都带来源、不折算**（避坑 161）。",
)

# ---- 2) Kling 4.0 / Runware 促销表：12 -> 13 条 ----
REWRITE["🟢 **快手可灵 Kling 4.0（**"] = build(
    "🟢 **快手可灵 Kling 4.0（**",
    [
        ("**⚠️ 官方给的截止日是 `10 月 29 日`，不是社媒口径的「7 天」**",
         "**⚠️ （050 期）促销数组逐条 diff（两期同一套结构化解析，避坑 212）：`12` 条 → `13` 条 —— "
         "新增 `1` 条、消失 `0` 条、其余 `12` 条的 `id`/`title`/`endsAt` 逐条同值** —— "
         "**即 `Kling 4.0` 的 `15% OFF` 截止日仍是 `endsAt: \"2026-10-29\"`（未改），"
         "`heygen-video-1-0-launch-promo` 仍是 `50% OFF` 至 `10/31`，"
         "`minimax-h3-max-october-promo` 仍是 `35% OFF` 至 `10/31`**。"
         "**新增的那一条是 `pruna-p-video-upscale` 的 `50% OFF`（至 `11/8`），已单独成行登记**。"
         "**⚠️ 官方给的截止日是 `10 月 29 日`，不是社媒口径的「7 天」**"),
    ],
    tail="**⚠️ （050 期）`Runware` 的 `models/prunaai-p-video-upscale` 模型页实访 `200` / `210,461` 字节，"
         "**但页面正文里 `prunaai-p-video-upscale`、`price`、`per second`、`$` 四个关键词全部零命中** —— "
         "**即「模型页存在」不等于「模型页给出了价格」**（模型页是 `SPA`，价格只在整站 `pricing` 页的返回体里；"
         "这是 048 期避坑 209 的延伸，本期再次实测）**。",
)

# ---- 3) 百度 Unlimited OCR 2：049 挂账项⑯销项（官方基准分实读） ----
REWRITE["🟢 **`百度` 开源 `文心 Unlimited OCR 2`（**MIT 许可"] = build(
    "🟢 **`百度` 开源 `文心 Unlimited OCR 2`（**MIT 许可",
    [
        ("`createdAt 2026-10-26T03:57:46Z`（＝北京 10/26 11:57）、`lastModified 2026-10-26T14:05:44Z`、",
         "`createdAt 2026-10-26T03:57:46Z`（＝北京 10/26 11:57）、**`lastModified 2026-10-27T13:35:48Z`（北京 10/27 21:35，落在本期窗口内）**、"
         "**`downloads 513`（049 期 `0`）、`likes 228`（049 期 `0`）**、"),
        ("**② 官方基准分只在 `assets/leaderboard.png` 图片里，正文无数字** —— "
         "「`MPDocBench` / `MarathonDocBench` 达 SOTA」是官方定性表述，"
         "「`84.6` / `77.1` 分」与被超越模型清单目前只有媒体转述（避坑 116）；",
         "**② 官方基准分已在 050 期实读到（049 期挂账项⑯销项）—— 但取图踩了一个坑** —— "
         "**`raw.githubusercontent.com/.../assets/leaderboard.png` 返回的是 `132` 字节的 git-LFS 指针**"
         "（逐字节为 `version https://git-lfs.github.com/spec/v1` / `oid sha256:aca406f6…` / `size 1481070`），"
         "**真图要走 `media.githubusercontent.com/media/baidu/Unlimited-OCR/main/assets/leaderboard.png` "
         "才拿得到（`1,481,070` 字节真 PNG，签名 `89 50 4E 47`）**（本期新立避坑 218）；"
         "**官方图 `Overall Score` 逐条（050 期实读）**：`Unlimited OCR 2` = "
         "`MPDocBench`（Dozens of Pages）**`84.6`** / `MarathonDocBench`（Hundreds of Pages）**`77.1`**，"
         "**官方标注逐字「+6.1 on MPDocBench, +8.5% on MarathonDocBench」**；"
         "**对照 10 个模型逐条**：`Qwen3.8-Max` `78.3`/`22.9`、`Qwen-3.8-Flash-Next` `77.4`/`27.8`、"
         "`Gemini-3.8-Flash` `76.2`/`28.6`、`Gemini-3.1-Pro-Preview` `71.8`/`27.0`、"
         "`GLM-5.3-Flash` `68.0`/`7.5`、`DeepSeek-4.1-Flash` `66.2`/`12.3`、"
         "`Minimax-M3` `62.6`/`18.0`、`Unlimited-OCR`（上一代）`61.9`/`0.0`、`Kimi-K3` `60.8`/`33.7` —— "
         "**媒体转述的 `84.6`/`77.1` 本期得到官方一手证实**（避坑 116 的销项）；"
         "**⚠️ 上一代在 `MarathonDocBench` 是 `0.0`（不是「没上榜」）—— "
         "「任意页数文档解析」是这一代才第一次拿到的能力**；"
         "**⚠️ 官方图另有八张子表**（`Text` `93.8`/`94.6`、`Formula` `89.4`/`89.2`、`Table` `87.8`/`84.8`、"
         "`Figure` `72.9`/`71.8`、`ReadOrder` `92.3`/`89.3`、`Heading` `60.1`/`48.2`、"
         "`T-Text` `90.0`/`87.8`、`T-Table` `89.5`/`71.1`），**`Unlimited OCR 2` 在八张子表上都是第一** —— "
         "**但「`Overall Score` 第一」与「每个子表第一」是两个口径，两个都写**（避坑 222）；"
         "**⚠️ 官方图自带评测说明逐字「Blank = no official result (CLI-only excluded), not zero.」**"
         "（**空值是「无官方结果」不是「零分」**，避坑 44 同族）；"),
        ("**③ `HF` 上 `downloads 0` 是仓库创建不足一天，不是没人用**（避坑 165；对照上一代 `baidu/Unlimited-OCR` "
         "已 `2,771,148` 下载 / `4,901` like）**。",
         "**③ `HF` 上 `downloads` 从 049 期的 `0` 升到本期的 `513`、`likes` 从 `0` 升到 `228` —— "
         "049 期记的「`downloads 0` 是仓库创建不足一天，不是没人用」本期得到实证**"
         "（避坑 165；对照上一代 `baidu/Unlimited-OCR` 已 `3,058,783` 下载 / `4,918` like）。"),
    ],
)

# ---- 4) MiniMax M3.1 Flash 开放权重：Unsloth GGUF 模型卡原文（049 挂账项⑨销项）+ 流通量 ----
REWRITE["🟢 **`MiniMax` `M3.1 Flash` 开放权重（**权重 10/17 就已在 `HF`"] = build(
    "🟢 **`MiniMax` `M3.1 Flash` 开放权重（**权重 10/17 就已在 `HF`",
    [
        ("**⚠️ （049 期）`HF` 字段重取（`hf-mirror.com`，读于 2026-10-27 19:4x",
         "**⚠️ （050 期）`HF` 字段重取（`hf-mirror.com`，读于 2026-10-28 09:0x"),
    ],
    tail="**⚠️ （050 期）流通量记账（升降都写）**：**详情端点两次实读完全一致 —— "
         "`downloads 11,075`（049 期 `8,782`，**+2,293**）、`likes 413`（049 期 `371`，**+42**）、"
         "`createdAt 2026-10-17T06:37:50.000Z`、`lastModified 2026-10-26T07:08:15Z`、`gated false`、`siblings 72`**；"
         "**列表端点 `author=MiniMaxAI` 仍为 `22` 个仓库**。"
         "**⚠️ `HF` 列表端点与详情端点的 `likes` 本期分别是 `400` 与 `413` —— 这是同一天的两次读数差，"
         "`HF` 自己的计数器在异步刷新，本报告两个都写、不取中间值**（避坑 161）。"
         "**⚠️ （050 期）销项：049 期挂账项⑨「`Unsloth` GGUF 模型卡原文」本期已销项** —— "
         "**一手 `hf-mirror.com/unsloth/MiniMax-M3.1-Flash-GGUF/raw/main/README.md`（`200` / `25,242` 字节）**。"
         "**逐字要点**：**`license_name: minimax-community`**（**⚠️ 不是 `MIT`**，与官方仓库的 `license:other` "
         "也不是同一个字符串 —— 这两条许可要分开记，避坑 158）、`base_model: MiniMaxAI/MiniMax-M3.1-Flash`、"
         "**`dspark-MiniMax-M3.1-Flash-Q8_0.gguf` 约 `2.1 GB`**（官方 `DSpark` draft head 转 `Q8_0`）、"
         "**需要 `llama.cpp` 的 `MiniMax-M3.1` 支持（含 `--spec-type draft-dspark`）**、"
         "**逐字「Results are for the official weights; third-party quantizations may differ.」**。"
         "**⚠️ 048 期转述的那组数（`2-bit` 体积 `−45%`、保留 `91.5%` top-1、`1-bit` 约 `89.9%`、"
         "`4-bit UD-Q4_K_XL` 达 `98.0%`、可在 `150GB` 内存上本地运行）—— "
         "本期把模型卡原文读完了，这组数在原文里一个都没有找到**"
         "（`91.5`/`89.9`/`45%`/`98.0`/`150GB`/`2-bit`/`1-bit`/`4-bit` 全部零命中）；"
         "**原文里能找到的量化档只有 `UD-Q4_K_XL`（出现在 `llama-server` 示例命令里）与 `Q8_0` 的 DSpark draft**。"
         "**本报告因此把这条从「未核到」推进到「官方模型卡原文里没有这组数」**（避坑 200）—— "
         "**⚠️ 但仍不写「这些数字是错的」**：它们可能出自 `Unsloth` 官网的量化基准页"
         "（模型卡给了链接 `unsloth.ai/docs/models/minimax-m3.1-flash` 与 "
         "`unsloth.ai/docs/basics/unsloth-dynamic-v3.0-gguf`），**本轮未实访这两个链接**。",
)

# ---- 5) OpenCode 免费模型清单：10 项同值、LongCat 连续第 4 期未回归 ----
REWRITE["🟡 **`OpenCode` 免费模型清单 10 → 11 项（`LongCat"] = build(
    "🟡 **`OpenCode` 免费模型清单 10 → 11 项（`LongCat",
    [
        ("**⚠️ 下架本身没有任何官方说明**：**`OpenCode` 两侧均未发布关于 `LongCat` 上/下架的公告，"
         "本报告因此不写「官方宣布上架/下架」，只写「两页出现/不再出现」**（避坑 154）。",
         "**⚠️ 下架本身没有任何官方说明**：**`OpenCode` 两侧均未发布关于 `LongCat` 上/下架的公告，"
         "本报告因此不写「官方宣布上架/下架」，只写「两页出现/不再出现」**（避坑 154）。"
         "**⚠️ （050 期）本轮复读**：**`zen` 页 `Free models` 段仍是 `10` 项、逐条与 049 期一致、无新增无消失**；"
         "**`LongCat` 关键词在 `zen` 页 `0` 处（049 期同值 `0`）、在 `go` 页 `9` 处（049 期 `8` 处）** —— "
         "**⚠️ `go` 页命中数 `8 → 9` 变了，但变的是 `go` 页的上下文行数、不是 `zen` 页的清单**；"
         "**`go` 页出现的是付费档 `LongCat-2.0`（`$0.30`/`$1.20`/缓存 `$0.006`，上下文 `920` 输入 / "
         "`88,900` 缓存 / `200` 输出 tokens 每请求），不是 `LongCat 2.5 Preview Free`** —— "
         "**两页合读确认：`LongCat` 系列只剩付费的 `-2.0`，`LongCat 2.5 Preview Free` 连续第 4 期未回归**。"
         "**⚠️ 这是避坑 210 的又一次活样本：换一个 URL/页面读同一个关键词，命中数就会变 —— "
         "判定「上没上架」只能看 `zen` 页的清单本身**。"),
    ],
)

# ---- 6) 豆包工作 30 天订阅：React 空壳连续第 4 期 ----
REWRITE["🟢 **豆包工作 30 天订阅（新一轮）**"] = build(
    "🟢 **豆包工作 30 天订阅（新一轮）**",
    [
        ("🟢 生效中（022 期登记）。⚠️ 第三方整理口径，以客户端订阅页为准",
         "🟢 生效中（022 期登记）。⚠️ 第三方整理口径，以客户端订阅页为准。"
         "**⚠️ （050 期）本轮实访 `volcengine.com/activity/doubao` 返回 `200` / `67,651` 字节，"
         "但页面是 React 空壳、正文仅 `176` 字、无任何可读字段 —— 连续第 4 期只推天数，"
         "本期仍未拿到一手**（避坑 180）"),
    ],
)

# ---- 7) 智谱 AutoClaw 国际站 M10W4：矛盾第 4 次实读未改 ----
REWRITE["🟢 **智谱 `AutoClaw` 国际站 `M10W4` `Weekly Perk`：登录领 **40M** Tokens（10/26–1"] = build(
    "🟢 **智谱 `AutoClaw` 国际站 `M10W4` `Weekly Perk`：登录领 **40M** Tokens（10/26–1",
    [("🟢 **生效中（活动第 2 天 · 046 期该行记「距开始 1 天」，本期按活动期推进）。",
      "🟢 **生效中（活动第 3 天 · 046 期该行记「距开始 1 天」，本期按活动期推进）。"
      "**⚠️ （050 期）本轮复读：国际站「40M vs 100M」矛盾第 4 次实读仍未改正** —— "
      "**正文仍是「From October 26 to November 1, log in to AutoClaw and get 40 million Tokens.」与 "
      "「worth 4,000 credits」，结尾句仍是「Remember to log in to AutoClaw on October 26 — "
      "100 million Tokens are waiting for you!」** —— **追踪项不销项**（避坑 202）；"
      "**国内站同页规则逐字未变（`1 亿` Tokens / `10,000` 积分 / 10/26 00:00–11/1 23:59 北京时间）**。"),
    ],
)

# ---- 8) Anthropic S-1 附信与 news 页日期（049 期挂账项⑬本期仍未销项） ----
REWRITE["🟢 **Anthropic `Claude Startup Stack`（029 期登记）**"] = build(
    "🟢 **Anthropic `Claude Startup Stack`（029 期登记）**",
    [("⚠️ 与 10/1 已闭环的 Claude Tag Credits、与云会话 credit **不是同一笔**",
      "⚠️ 与 10/1 已闭环的 Claude Tag Credits、与云会话 credit **不是同一笔**。"
      "**⚠️ （050 期）`Anthropic` 侧两处补记（与本行口径无关，仅备查）**："
      "**① `anthropic.com/news` 的区块标题栏日期本期由 `October 27, 2026` 推进到 `October 28, 2026`，"
      "而列表里最新条目是 `Oct 27, 2026` 的两条（`Science` 药物研发 + `Partnerships` GSA `40%` 折扣）—— "
      "**这正是避坑 208 的活样本：区块标题栏日期 ≠ 条目日期**；"
      "**② `anthropic.com/news/s1-sec` 本轮实访 `200` / `151,532` 字节，但该页只是 S-1 公告正文，"
      "**`S-1` 附信原文（300+ 页）仍未读到 —— 049 期挂账项⑬本期仍未销项**（避坑 180）")],
)

# ---- 10) 腾讯 WorkBuddy Hy3 限免：距今重算由脚本处理；这里补一句窗口外复读 ----
REWRITE["🟢 **腾讯 WorkBuddy Hy3 限免 + Hy4 preview 夜间限免（已延期）**"] = build(
    "🟢 **腾讯 WorkBuddy Hy3 限免 + Hy4 preview 夜间限免（已延期）**",
    [("🟢 **生效中。 ⚠️ 官方确认繁忙时进入排队。**",
      "🟢 **生效中。 ⚠️ 官方确认繁忙时进入排队。**"
      "**⚠️ （050 期）本轮实访官方页面，限免口径未变（至 `10/31`）** —— "
      "**距今天数由脚本按基准日 `10/28` 重算**（避坑 208：**天数按「截止日 − 基准日」算，不是「推进一天就 −1」**）。")],
)

# ---- NEW 行 1：Opera WebAI（浏览器本地 AI 标准，无 API key、无按次云费用）----
NEW = []

NEW.append(
    "| 🟢 **`Opera` `WebAI`（**浏览器本地 `AI` 的拟议 Web 标准 · **本地推理内置 · 无需 `API key` · "
    "**无按次云端费用** · `Opera One`/`GX`/`Neon` 三浏览器 early preview**）** | "
    "**未公布（early preview，官方未给任何时间表）** | "
    "🟢 **生效中（本期新登记 · 官方公告 `October 27th, 2026`）**。"
    "**官方一手（`blogs.opera.com/news/2026/10/webai-local-ai-for-the-web-now-in-opera/`）逐字**："
    "「**WebAI is a proposed web standard, backed by companies including Google and Microsoft.**」；"
    "「**The first step is WebAI, now in early preview across Opera One, Opera GX and Opera Neon.**」；"
    "「**Local inference is built into the browser, so there’s no separate AI app to install, "
    "no local server to configure and no API key to get.**」；"
    "「**WebAI is opt-in. Nothing is downloaded until you turn it on in Settings, "
    "and you can turn it off at any time.**」；"
    "「**No per-request cloud costs, and no AI infrastructure to run.**」。"
    "**⚠️ 三个 API（官方逐字）**：「**WebAI introduces the `Prompt`, `Decision` and `Semantic Embeddings` APIs. "
    "With them, developers can generate text, classify information and find relationships between "
    "pieces of content.**」。"
    "**⚠️ 四层开放（避坑 41）**：**① 能用 —— early preview 已上三浏览器**；"
    "**可用平台逐字「available on Windows PC (64-bit, Intel/AMD) and Macs with Apple silicon. "
    "It isn’t available on Intel-based Macs, Linux or Windows on Arm.」**"
    "② 能下载 —— **「open-weight models provided through Opera and compatible models already on your device」**"
    "（**`Gemma` 为示例、`Mac` 上另支持 `Apple` 端侧模型这两条出自媒体转述、非官方公告原文**）"
    "③ 能跑 —— **「Running AI locally uses your computer’s own processing power, so how quickly it responds "
    "depends on your device. Local AI performance is still improving」**（**官方不做速度承诺**）"
    "④ 能商用 —— **官方公告未写商用条款**（本报告只写「官方未写」，避坑 154）。"
    "**⚠️ 本报告不写「Opera 免费提供 AI」** —— **它的免费性来自「本地推理不产生云端按次费用」，"
    "不是厂商送的额度**（避坑 41/161）。"
    "**⚠️ 官方自陈边界**：**early preview 而非 GA**；**官方声明六个示范扩展「are examples to spark ideas, "
    "not Opera features」**；**官方给的开发者文档地址 `next.opera.com/web-ai/` 本轮 `451`、未核到**。 |",
)

# ---- NEW 行 2：OpenRouter CSAM 筛查与 ZDR 例外（对所有 :free 档用户有直接影响）----
NEW.append(
    "| 🟡 **`OpenRouter` 的 `CSAM` 在途筛查与 `ZDR` 例外（**10/27 官方公告 · "
    "**「零数据留存」承诺首次出现官方写明的例外**）** | "
    "**未公布（政策条款，官方未给任何时间表）** | "
    "🟡 **生效中（本期新登记 · 官方公告 `October 27, 2026`）**。"
    "**官方一手（`openrouter.ai/blog/announcements/csam-screening/`）逐字**："
    "「**OpenRouter will screen all inference requests for child sexual abuse material (CSAM) as they "
    "pass through our service. Screening happens in flight, during request processing.**」；"
    "「**Known CSAM detection. In-flight screening will include comparing applicable content against hashes "
    "(digital fingerprints) of previously identified CSAM.**」；"
    "「**We may begin retaining content flagged as potential CSAM for human review, including content that "
    "does not match a known hash. A flag indicates suspected material; it is not itself a determination that "
    "the content is CSAM.**」；"
    "**「Screening also applies to ZDR traffic」**；"
    "**「For inference content covered by OpenRouter’s ZDR policy, we do not retain prompts or responses "
    "after processing, except when you explicitly choose to have us store them or when retention is needed "
    "for CSAM review, reporting, and related legal preservation.」**；"
    "**「These CSAM provisions do not authorize general retention of ZDR inference content for unrelated "
    "purposes.」**；"
    "「**Under U.S. law, covered providers must report to NCMEC’s CyberTipline as soon as reasonably "
    "possible after obtaining actual knowledge…**」；"
    "「**That requirement applies to reported material, rather than every item flagged for review "
    "(18 U.S.C. § 2258A(a) and (h)).」**；"
    "「**Model labs and providers may use different screening and retention methods… Review those policies "
    "when choosing a model or provider, especially if your organization has specific data-retention "
    "requirements.**」。"
    "**⚠️ 对免费档读者的三条可判定影响**：**① 筛查是「在途」的、发生在请求处理过程中 —— "
    "不等于「全部请求都被留存」**；**② 例外的范围是「被标记为疑似 `CSAM` 的内容」—— 不是普遍留存**"
    "（**官方自己写了 `does not authorize general retention`**）；"
    "**③ 官方明确要求「按模型/提供方逐个核对留存政策」—— 同平台不同模型的留存口径可能不同**（避坑 41）。"
    "**⚠️ 本报告不写「`OpenRouter` 开始留存用户数据」** —— 那是不准确的概括（避坑 116/161）。"
    "**⚠️ 公告页的连续期数也变了**：041–049 连续九期「停在 `October 14, 2026`」，本期出现新条目 —— "
    "**但这条公告是内容安全与留存，不是限免**（避坑 116）。 |",
)

# ---- NEW 行 3：Runware pruna-p-video-upscale 50% 促销（至 11/8，有确切截止日）----
NEW.append(
    "| 🟢 **`Runware` 分发层 `pruna-p-video-upscale` 促销 `50% OFF`（**官方 `pricing` 页促销数组 · "
    "**一手核到** · **截止 `11/8`**）** | "
    "**11/8（官方促销数组 `endsAt: \"2026-11-08\"` 逐字；描述逐字「until November 8, 2026」）** | "
    "🟢 **生效中（本期新核到一手 · **距结束 11 天**）**。"
    "**官方一手（`runware.ai/pricing`，本轮实访 `200` / `745,835` 字节）逐字**："
    "`\"id\":\"pruna-p-video-upscale-launch-promo\",\"title\":\"50% OFF\","
    "\"description\":\"50% off all generations until November 8, 2026\","
    "\"models\":[\"prunaai-p-video-upscale\"],\"endsAt\":\"2026-11-08\"`。"
    "**⚠️ 这是「打 5 折」、不是免费** —— **进价格位、不进免费额度位**；"
    "**且是 `Runware` 分发层的价格活动、不是厂商侧（`Pruna`）的免费政策**（避坑 41：多站点口径要拆开写）。"
    "**⚠️ 同期促销表逐条 diff：`12` 条 → `13` 条** —— **新增 `1` 条、消失 `0` 条、其余 `12` 条逐条同值**。"
    "**⚠️ 「模型页存在」不等于「模型页给出价格」**："
    "`runware.ai/models/prunaai-p-video-upscale` 本轮实访 `200` / `210,461` 字节，"
    "**但页面正文里 `prunaai-p-video-upscale`、`price`、`per second`、`$` 四个关键词全部零命中** —— "
    "**价格只在整站 `pricing` 页的返回体里**（048 期避坑 209 的延伸，本期再次实测）。"
    "**⚠️ `Runware` 的新用户免费额度是另一条线**（官方 FAQ 逐字「**New users who sign up with a business "
    "email receive $2 in free credits**」）—— **不要与本行的折扣相加**。 |",
)

# ---- NEW 行 4：NVIDIA 厂商侧 nemotron-3-super-120b-a12b 免费端点弃用（049 挂账项⑮销项）----
NEW.append(
    "| ⚠️ **`NVIDIA` 官方 `nemotron-3-super-120b-a12b` 的免费端点已标 `Deprecated`（**"
    "**一手核到 · 049 期挂账项⑮销项** · **但权重与合作端点仍 `Available`**）** | "
    "**未公布（`Deprecated` 是状态标注，不是活动截止）** | "
    "⚠️ **生效中但免费端点已弃用（本期新登记 · 一手 `build.nvidia.com`）**。"
    "**官方一手（`build.nvidia.com/nvidia/nemotron-3-super-120b-a12b`，本轮实访 `200` / `284,691` 字节）"
    "「Model Availability」四格逐字**：`Free Endpoint` → **`Deprecated`**（⚠️ 警示样式）、"
    "`Partner Endpoint` → `Available`、`Download Available` → `Available`、`Available`。"
    "**同页其他逐字字段**：「**Provider NVIDIA**」「**Context Length 1M**」「**Parameters 124B**」"
    "「**Last Modified 7 months ago**」「**API calls in last 30 days 65M**」。"
    "**⚠️ 与 049 期记录的「`nvidia/nemotron-3-super-120b-a12b:free` 从 `OpenRouter` 目录消失」在时间上对得上** —— "
    "**本报告写「对得上」，不写「因为」**（官方没有把两件事连起来说，避坑 116）。"
    "**⚠️ 三条边界（避坑 221：状态矩阵必须逐格对应）**："
    "**① 弃用的是「`Free Endpoint`」这一格，不是模型本身 —— 权重与 `Partner Endpoint` 都仍 `Available`**；"
    "**② 本报告不写「厂商撤下模型」「停止服务」「退役」—— 官方用的词是 `Deprecated` 且只挂在免费端点这一格上**"
    "（避坑 154/198/214）；"
    "**③ 「`API calls in last 30 days 65M`」是 `NVIDIA` 自家端点的调用量，不是 `OpenRouter` 的** —— "
    "**两个站点的数字不可混用**（避坑 202）。"
    "**⚠️ 同系列其余 5 条 `:free` 档在 `OpenRouter` 本期健在**（`:free` `16` 条无增无减）。 |",
)

# ---- 应用 REWRITE ----
out = []
rw = 0
for l in body:
    hit = None
    for k, v in REWRITE.items():
        if k in l:
            assert hit is None, ("一行命中多个 REWRITE 键", k)
            hit = (k, v)
    if hit:
        assert hit[1] != l, ("REWRITE 与源行相同（等于没改）", hit[0][:40])
        out.append(hit[1])
        rw += 1
    else:
        out.append(l)
assert rw == len(REWRITE), ("命中的 REWRITE 数量不对", rw, len(REWRITE))
for k, v in REWRITE.items():
    assert sum(1 for l in out if l == v) == 1, ("REWRITE 值未唯一出现在输出中", k[:40])

# ---- 天数重算：基准日 10/28（比上期推进一天，每行都应变） ----
DAYS_RE = re.compile(r"距今\s*(-?\d+)\s*天")


def parse_cut(l):
    cells = [c.strip() for c in l.strip().strip("|").split("|")]
    if len(cells) < 2:
        return None
    due = cells[1].replace("**", "")
    for pat in (r"(\d{4})[-年](\d{1,2})[-月](\d{1,2})", r"(\d{1,2})/(\d{1,2})"):
        m = re.search(pat, due)
        if m:
            try:
                if m.group(0)[0].isdigit() and len(m.group(0)) > 4 and "/" in m.group(0):
                    return date(2026, int(m.group(1)), int(m.group(2)))
                if len(m.groups()) == 3:
                    return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                return date(2026, int(m.group(1)), int(m.group(2)))
            except ValueError:
                continue
    return None


def recompute(l):
    if "距今" not in l:
        return l
    d = parse_cut(l)
    if d is None:
        return l
    return DAYS_RE.sub("**距今 %d 天**" % (d - BASE).days, l)


before_snapshot = list(out)
out = [recompute(l) if l not in REWRITE.values() else l for l in out]

diff = []
for before, after in zip(before_snapshot, out):
    m = DAYS_RE.search(before)
    if not m or before in REWRITE.values():
        continue
    d = parse_cut(before)
    if d is None:
        continue
    truth = (d - BASE).days
    if int(m.group(1)) != truth:
        diff.append((after.split("|")[1][:46].strip(), m.group(1), truth))

bad = []
for l in out:
    m = DAYS_RE.search(l)
    if not m or l in REWRITE.values():
        continue
    d = parse_cut(l)
    if d is None:
        continue
    truth = (d - BASE).days
    if int(m.group(1)) != truth:
        bad.append((m.group(1), truth, l.split("|")[1][:40]))

neg = [l.split("|")[1][:40] for l in out
       if "距今 -" in l and l not in REWRITE.values() and l not in NEW]
assert not neg, ("出现负值天数", neg)

print("recomputed rows with 距今:", len([l for l in out if DAYS_RE.search(l)]))
print("before -> after diff (行名 / 旧值 -> 真值), 共 %d 行:" % len(diff))
for name, a, b in diff:
    print("   %-46s %s -> %s" % (name, a, b))
assert not bad, ("重算结果不等于按截止列算出的真值", bad)

# ---- 新行插在 ⚪ 存档块锚点之前 ----
anchor_idx = None
for i, l in enumerate(out):
    if l.startswith("| ⚪ **DeepSeek 10/15"):
        anchor_idx = i
        break
if anchor_idx is None:
    for i, l in enumerate(out):
        if l.startswith("| ⚪ **"):
            anchor_idx = i
            break
assert anchor_idx is not None, "未找到 ⚪ 存档块锚点"
out = out[:anchor_idx] + NEW + out[anchor_idx:]

assert len(out) == PREV + len(NEW), (len(out), PREV + len(NEW))

from collections import Counter

print("field-count distribution:", Counter(len(l.split("|")) - 2 for l in out))

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(header + "\n" + sep + "\n")
    f.write("\n".join(out) + "\n")

print("rows: %d (%d + %d new) / rewrites: %d" % (len(out), PREV, len(NEW), rw))
