# -*- coding: utf-8 -*-
"""043 期：台账（AI信息源分级清单-T0-T4.md）就地更新。
⚠️ **纪律（036 期立）**：
   ① **改台账正文加信源行时，必须同步改清单章节标题里的手写计数**（`## T0 · 根节点（N）`、`### 官方一手 · 国外（N）` 等五处）；
   ② **站点首页「信源 N 条」= 五个 `## T\\d …（N）` 括号求和** —— 只加行不改数会导致首页显示旧数字；
   ③ **逐节核对**（036 期纪律）：每节的「括号数」必须等于该节表内实际行数；
   ④ **加行后必须重算区间**（042 期自造 bug：把插入点当唯一定位，导致三行全落进「国内」节）。
⚠️ **data/ 下是 CRLF，根目录下这份台账是 LF** —— 用 newline="\\n" 写回。
"""
import re

F = "AI信息源分级清单-T0-T4.md"

NEW_ROWS = [
    # (锚点行前缀, 新行全文) —— 插入到该锚点行之后
    ("| **🆕 `MiniMax` 国际开放平台 Models 页** |",
     "| **🆕 `MiniMax` 官方博客** | https://www.minimax.io/blog/minimax-m31f | — | "
     "**「开放权重」四种状态里第 ②③ 级的唯一一手出处**。**043 期首次取用（发布日 2026-10-19）**——"
     "逐字只有「`M3.1 Flash is now available through the MiniMax API, M Plan, and MiniMax Code. "
     "Model weights will be released later.`」**——全篇无任何日期**；**而「10 月 23 日」只出自官方 X 与第三方媒体**"
     "（`RITS` 逐字「`The reported October 23 date is a plan, not a checkpoint.`」）。"
     "⚠️ **本报告据此判定「写『`MiniMax` 官方确认 10 月 23 日开放权重』是失实的」**（043 期新立避坑 188）。"
     "⚠️ **与同一厂商的官方 API 文档站相比，承诺强度不一致** —— 文档站已在模型表里标 `open-weight`，博客只说 `later`"
     "（避坑 143 同族的新形态：**同一家厂商的博客与文档站可以给出强度不同的承诺**）。"
     "补入 **T0 官方一手 · 国外** —— 本清单第一个「**发布公告里只写 `later`、不给日期**」的样本 | 043 | 1 |"),

    ("| **🆕 `MiniMax` 国际开放平台 Models 页** |",
     "| **🆕 `Hugging Face` `MiniMaxAI` 组织页** | https://huggingface.co/MiniMaxAI | — | "
     "**「权重到底在不在」的唯一判据，也是本清单第一个「**许可字段逐字可读**」的国外样本**。**043 期首次取用**——"
     "**本轮实访确认组织页当前不存在任何 `M3.1` / `M3.1-Flash` 仓库**（20 个仓库逐个核过：`MiniMax-H3`、"
     "`MiniMax-Music3`、`MiniMax-M3`、`MiniMax-M3-MXFP8`、`MiniMax-M2`/`M2.1`/`M2.5`/`M2.7`、"
     "`VTP-Small`/`Base`/`Large`、`Text-01`、`Text-01-hf`、`VL-01`、`M1-40k`/`M1-80k`/`M1-40k-hf`/`M1-80k-hf`、"
     "`SynLogic-32B`/`Mix-3-32B`/`7B`），`gated` 均为 `false`** —— **即「权重未上传」这一条，一手的 `HF` 组织页是空的**。"
     "⚠️ **同时是 `MiniMax-H3` 的许可字段出处**：`license: other`、`license_name: minimax-h3-community-license-agreement`、"
     "`downloads: 4,890,714`、`gated: false`、`createdAt: 2026-07-28`、`lastModified: 2026-08-13`；"
     "许可原文（`LICENSE`，许可日 2026-08-02）的**地域排除条款逐字为「`the European Union, the United Kingdom, "
     "the Republic of Korea and the United States of America`」、商业门槛为年营收超 `US$20,000,000` 需事先书面授权、"
     "并要求商业产品显著标注「`MiniMax H3`」**。"
     "⚠️ **这推翻了「国产视频模型开源 = Apache-2.0」的默认预期**（043 期新立避坑 189：**许可是五层**："
     "下载闸门 / 许可类型 / 地域范围 / 商业门槛 / 衍生义务）。补入 **T0 官方一手 · 国外** | 043 | 1 |"),

    ("| **🆕 `MiniMax` 国际开放平台 Models 页** |",
     "| **🆕 `Hugging Face` `openbmb` 组织页** | https://huggingface.co/openbmb | — | "
     "**本期唯一的「最宽松一档」反例**（043 期首次取用）——**`MiniCPM-V 4.7`**："
     "`openbmb/MiniCPM-V-4.7-35B-A3B` 与 `openbmb/MiniCPM-V-4.7-1B` 两个仓库，"
     "**`gated: false` / `disabled: false` / `private: false`（无下载闸门、无需人工审核）、`license: apache-2.0`（可商用）**、"
     "实际参数量 `35,212,875,824` 与 `1,554,476,272`、下载量 `95,240` 与 `46,506`、**13 个衍生仓库全部 Apache-2.0**、"
     "量化格式含 GGUF / GPTQ / AWQ / int4 / FP8（另有 `-DSpark` 推测解码草稿模型）。"
     "⚠️ **仓库名用点号不是下划线**（`MiniCPM-V-4.7-35B-A3B`）—— **搜 `MiniCPM-V-4_7` 会 404**。"
     "⚠️ **上下文长度 HF API 与 config 均未给出，第三方说法冲突（`256K` vs 约 `976K`），不可取中间值**。"
     "⚠️ **必须有它** —— **否则读者容易把「某家的模型有地域排除」误推成「这类的模型都有」**"
     "（避坑 163 的多站点面同样适用于**同一家的不同模型**）。补入 **T0 官方一手 · 国外** | 043 | 1 |"),

    ("| **🆕 `MiniMax` 国际开放平台 Models 页** |",
     "| **🆕 `Federal Register`（DHS `Docket No. DHS-2026-0628`）** | https://www.govinfo.gov/content/pkg/FR-2026-10-20/html/2026-21447.htm | — | "
     "**本清单第一个「以官方公报全文为准的政策信源」**。**043 期首次取用**——"
     "标题「`Notice of Order Regarding Exclusion and Removal of DeepSeek Products From Federal Civilian Executive Branch "
     "Information Technology Systems and Procurements`」、`FR Doc No. 2026-21447`、`Filed 10-19-26 8:45 am`、"
     "法定依据「`Federal Acquisition Supply Chain Security Act of 2018`, 41 U.S.C. 1321-1328」与 `41 CFR 201-1`；"
     "**命令两条**：**① 将 `Hangzhou DeepSeek Artificial Intelligence Co., Ltd` 及其关联方开发的 IT 产品与服务排除出联邦民事机构采购；"
     "② 从民事机构 IT 系统中移除全部 `DeepSeek` 及关联方产品，**以及「使用 `DeepSeek` 实现开发的第三方产品与服务」**」。"
     "⚠️ **命令第 ② 条的后半句最易读漏** —— **「我没直接用 `DeepSeek`」不构成豁免**。"
     "⚠️ **命令全文未给移除完成期限**（避坑 142：**每个日期都要问它是哪一种；没有日期就是没有日期**）。"
     "补入 **T0 官方一手 · 国外（政策）** —— 本清单此前记的多条美国监管口径都是**媒体转述**，本期第一次拿到公报原文 | 043 | 1 |"),
]

md = open(F, encoding="utf-8", newline="").read()
lines = md.split("\n")

# ---- 逐条插入到锚点之后（每插完一条重算区间）----
for anchor, row in NEW_ROWS:
    idx = None
    for i, l in enumerate(lines):
        if l.startswith(anchor):
            idx = i
            break
    assert idx is not None, ("未找到锚点", anchor)
    lines.insert(idx + 1, row)

md = "\n".join(lines)

# ---- 同步手写计数五处 ----
def bump(pat, newn, text):
    """只替换**括号里的计数**。
    ⚠️ 043 期自造 bug：先前用 re.sub(r"\d+", ..., count=1) 替换整行，
       结果把标题里的**第一个数字**（"## T0" 里的 0）替换掉，
       标题变成「## T161 · 根节点（157）」—— 计数反而没改。
       正确做法：只对括号内的数字做 re.sub。
    """
    m = re.search(pat, text)
    assert m, ("未找到计数标题", pat)
    whole = m.group(0)
    i = whole.rindex("（")
    head, inner = whole[:i], whole[i + 1:-1]
    assert whole.endswith("）"), whole
    return text[:m.start()] + head + "（" + re.sub(r"\d+", str(newn), inner) + "）" + text[m.end():]

# ## T0 · 根节点（157 -> 161）
md = bump(r"## T0 · 根节点（\d+）", 161, md)
# ### 官方一手 · 国外（45 -> 49）
md = bump(r"### 官方一手 · 国外（\d+）", 49, md)

open(F, "w", encoding="utf-8", newline="\n").write(md)

# ---- 逐节核对：括号数 vs 表内行数 ----
lines2 = open(F, encoding="utf-8", newline="").read().split("\n")
sec = None
rows_in = 0
results = []
for l in lines2:
    m = re.match(r"^#{2,3} (.+?)（(\d+)）\s*$", l)
    if m:
        if sec:
            results.append((sec, declared, rows_in))
        sec = m.group(1)
        declared = int(m.group(2))
        rows_in = 0
        continue
    if sec and l.startswith("|") and not re.match(r"^\|[\s\-:|]+\|$", l) and "上次命中" not in l:
        rows_in += 1
if sec:
    results.append((sec, declared, rows_in))

print("逐节核对（节名 / 括号声明 / 表内行数）：")
for name, dec, cnt in results:
    mark = "OK" if name in ("T0 · 根节点",) or True else ""
    print("  %-24s 声明 %3d  实跑 %3d  差 %+d" % (name, dec, cnt, cnt - dec))

# 根节点 = 六个子节之和
subs = [(n, d, c) for n, d, c in results if n != "T0 · 根节点" and n.startswith(("论文与预印本", "模型与开源", "官方一手 · 国外", "官方一手 · 国内", "政策与监管", "评测与榜单"))]
print("T0 六个子节求和 =", sum(c for _, _, c in subs), "（根节点声明 161）")
