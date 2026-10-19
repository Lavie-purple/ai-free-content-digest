# -*- coding: utf-8 -*-
"""041 期台账更新：新增 2 条信源 + 就地更新 freellm.net 表外补登行 + 同步三处手写计数。

⚠️ **036 期纪律**：加行必须落在正确小节里；改完括号计数要做逐节「括号数 vs 实际行数」核对。
⚠️ **035 期纪律**：台账是 LF（与 data/ 下的 CRLF 不同）。
⚠️ **036 期纪律**：`freellm.net` 是**表外补登行**（`| **免费额度垂直追踪站**：freellm.net` 起头的复合长行），
   **不进 `build_source_hits.py` 的计数、也不进括号口径** —— 本期就地更新写在它自己那一行里。
⚠️ **039 期已记的静默陷阱**：正文里不能有裸 `|`，否则把行切成 10 字段。
"""
import re
from collections import Counter

F = "AI信息源分级清单-T0-T4.md"
md = open(F, encoding="utf-8").read()

# ---------- ① 手写计数三处同步 ----------
COUNTS = [
    ("## T0 · 根节点（153）", "## T0 · 根节点（154）"),
    ("### 官方一手 · 国外（43）", "### 官方一手 · 国外（44）"),
    ("## T4 · 聚合器与工具（32）", "## T4 · 聚合器与工具（33）"),
]
for old, new in COUNTS:
    assert md.count(old) == 1, ("计数标记未唯一命中", old, md.count(old))
    md = md.replace(old, new)

# ---------- ② 新增 2 行 ----------
ROW_X = (
    "| **🆕 `Bolt` 官方 X（`@boltdotnew`）** | https://x.com/boltdotnew | — | "
    "**限时活动的唯一一手出处**。**041 期首次命中（10/19）**：Builders Week 免费周末三句原文"
    "（`Bolt is free for EVERYONE for an ENTIRE weekend.` / `Build all weekend Oct 17 + 18.` / "
    "`submit by Oct 20.`）。⚠️ **`bolt.new/blog/builders-week` 本轮实访返回产品首页、"
    "`support.bolt.new/Builders-Week` 返回 404 —— 站内无对应细则页，而官方 X 只给了三句核心信息**，"
    "其余字段（美西起止时刻 / 六小时分块 token 数 / 三档奖金 / 地区排除名单 / `Forge` 数据训练条款）"
    "**本轮只能取自第三方规则整理站**（避坑 143：活动细则只发在 X、站内无页，是「发布方式追踪位」的新样本）。"
    "**这是本报告第一次登记一条「040 期全漏登、且一手面只有一个 X 账号」的权益类活动** → 已立 Q30 挂账 | 041 | 4 |"
)
ROW_T4 = (
    "| **🆕 `freellm.net` 新 URL 形态（`/providers/<provider>`）** | "
    "https://freellm.net/providers/openrouter | — | "
    "**补上 040 期遗留动作⑤的新 URL**。**040 期记「`OpenRouter` 专页 URL 改版返回 404、`:free` 清单本期未重取」；"
    "041 期用新形态 `freellm.net/providers/<provider>` 取到了完整数据**（19 个 `:free` 模型、上下文区间 `66K – 1.0M`、"
    "`Last Updated 2026-10-19`、`200 req/day` 口径与 FAQ 里的 `$10` 换 `1,000 RPD`）。"
    "⚠️ **旧形态 `/models/provider/openrouter/` 仍 404 —— 站点改版期的旧链接不可复用，须重新发现 URL 形态**"
    "（033 期以来「表外补登行」之外的第一个「同一站两个 URL 形态并存」样本） | 041 | 3 |"
)

def insert_after(md, anchor, row):
    assert md.count(anchor) == 1, ("锚点未唯一命中", anchor[:50], md.count(anchor))
    i = md.index(anchor)
    j = md.index("\n", i) + 1
    return md[:j] + row + "\n" + md[j:]

md = insert_after(md, "| **🆕 Ollama 官方博客**", ROW_X)
md = insert_after(md, "| 🆕 ClawLabsAI/free-ai-models", ROW_T4)

# ---------- ③ 就地更新 freellm.net 表外补登行（计数器逐期记账）----------
i = md.index("| **免费额度垂直追踪站**：freellm.net")
j = md.index("\n", i)
fm_line = md[i:j]
assert fm_line.endswith(" |"), repr(fm_line[-20:])
tail_add = (
    "。**⚠️ 041 期重取（首页读于 2026-10-19）：505+ 模型 / 30 提供方 / **237** 经实时 API 验证 / "
    "**422+** 免绑卡 / `checked 2026-10-19` —— 四个字段里三个升、一个同值（提供方数未动），"
    "按纪律逐项记账、不得据任一单项写趋势**；"
    "**041 期起该站把「经实时 API 验证数」从标题里的 `verified` 字样中单列为独立字段，本报告起逐期单独记账**；"
    "**`OpenRouter` 专页本轮 19 个 `:free` 模型与 038 期同值、只有日期推进；"
    "且首页 `checked 2026-10-19` 与专页 `Last Updated 2026-10-19` 本期同值 —— 但这是本期实测结果、不是稳定规律，"
    "引用时仍须点名是哪一页**；"
    "**「200 req/day」与 `OpenRouter` 官方「50 次/日（累计充值满 $10 后 1,000 次/日）」仍是两个口径，两说并列**"
    "（避坑 161，033 期以来连续登记、本期继续挂账）"
)
fm_new = fm_line[:-2] + tail_add + " |"
md = md[:i] + fm_new + md[j:]

open(F, "w", encoding="utf-8", newline="\n").write(md)

# ---------- ④ 逐节「括号数 vs 实际行数」核对 ----------
print("=== 逐节核对 ===")
sec_re = re.compile(r"^(#{2,3}) (.+?)（(\d+)）\s*$", re.M)
marks = [(m.start(), m.end(), m.group(2), int(m.group(3))) for m in sec_re.finditer(md)]
all_rows = [l for l in md.split("\n") if l.startswith("|")]
dist_all = Counter(len(l.split("|")) - 2 for l in all_rows)
print("全表行字段数分布:", dict(dist_all))
for idx, (s, e, name, n) in enumerate(marks):
    end = marks[idx + 1][0] if idx + 1 < len(marks) else len(md)
    seg = md[e:end]
    rows = [l for l in seg.split("\n") if l.startswith("|")]
    data = [l for l in rows if not re.match(r"^\|[\s:\-\|]+\|$", l)]
    data = data[1:] if data else []
    ok = "OK" if n == len(data) else "<<< 不一致"
    print("  %-24s 括号=%-4d 实际=%-4d %s" % (name, n, len(data), ok))
