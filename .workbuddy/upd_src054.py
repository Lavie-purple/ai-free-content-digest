# -*- coding: utf-8 -*-
"""054 期：把用户本轮补充清单里台账缺失的 5 条 + 本期新增的 1 条信源就地补进
《AI信息源分级清单-T0-T4.md》，并同步全部手写计数。

⚠️ 纪律（031 期立、037 期又验证过）：
   - 「再次命中 ≠ 新增信源」——加行之前必须先核「这一行是不是已经有了」。
   - **站点首页「信源 N 条」= 五个 `## T\\d …（N）` 标题求和** → 只加行不改数会让首页显示旧数字。
   - 手写计数必须**多处同步**（`## T0 · 根节点`、各 `### 子类`、`## T1/T2/T3/T4`）。

⚠️ **054 期新立的一条工程纪律（本脚本第一次跑就踩了）**：
   计数标题 `### 官方一手 · 国内（29）` 在文件里**只出现一次**，但文件开头那段
   「历史沿革」长段落里**也含同名的分类名** —— 用 `str.replace` / `re.search` 全局替换
   会改到**历史叙述段落里的数字**、而不是标题里的数字。
   **修法：所有计数改动必须按「行首标题」定位（`^## ` / `^### ` 开头的整行），逐行处理。**
"""
import io
import re

P = "AI信息源分级清单-T0-T4.md"
lines = io.open(P, encoding="utf-8").read().split("\n")

# ---------- 1) 先核「是否已经存在」 ----------
NEW_ROWS = [
    ("`SoMark` 官方文档站", "https://docs.somark.ai/", "官方一手 · 国内",
     "**054 期首次登记** —— `OXR` 开放权重文档解析模型（`1.3B`）的官方文档站。"
     "**⚠️ 本报告至今第一条「官方写明免费 API 每天/每月多少页」的一手证据**"
     "（`free-tier-rules.md` 逐字 `Up to 500 pages of free quota per day` ／ "
     "`Up to 2000 pages of free quota per month`）；"
     "**⚠️ 该站是 `Mintlify` 托管的 —— 网页版正文是 JS 渲染的、但同站 `.md` 原文直链与 `/llms.txt` 索引是纯文本**"
     "（**新立避坑 241：这类 `llms.txt` 索引值得单独入库**）。"
     "配套入口：`free-oxr.somark.ai` ／ `free-oxr.somark.cn`（**互为镜像、实访两者均 `200` / `16,341` 字节**）；"
     "`github.com/SoMarkAI/OXR`（`README.md` `200` / `19,333` 字节、`LICENSE` `200` / `2,394` 字节）"),
    ("`Moonshot` 官方文档（另一域写法）", "https://platform.moonshot.cn/docs", "官方一手 · 国内",
     "**054 期按用户本轮补充清单补入** —— 与台账既有的 `platform.moonshot.cn/docs/pricing/chat` 同站、"
     "但**域名写法不带子路径**（用户清单写法）。"
     "**⚠️ 登记时即带一条本期实测的取证纪律（新立避坑 243）**："
     "**053 期记「`K2` 系列 `10/31` 停新未核到」，而 054 期在同一份文件上实读命中** —— "
     "官方逐字 `K2 系列模型将于 2026 年 10 月 31 日起停止向新注册用户开放，已注册用户不受影响`；"
     "**即 053 期是「当期没读到那一段」、不是「官方没写」**"),
    ("`CSDN`", "https://www.csdn.net/", "国内",
     "**054 期按用户本轮补充清单补入** —— 中文技术社区（T3 媒体 · 国内）。"
     "**⚠️ 登记时即带一条边界：用户文章是二手、引用一律回一手**（避坑 154）"),
    ("`开源中国`（OSChina）", "https://www.oschina.net/", "国内",
     "**054 期按用户本轮补充清单补入** —— 中文开源社区与资讯站（T3 媒体 · 国内）。"
     "**⚠️ 登记时即带一条边界：与 `CSDN` 同类、均为二手源**（避坑 154）"),
    ("`ServeTheHome`", "https://www.servethehome.com/", "国外",
     "**054 期按用户本轮补充清单补入** —— 服务器 / 硬件评测媒体（T3 媒体 · 国外）。"
     "**⚠️ 登记时即带一条边界：它评的是硬件与整机、不是模型能力 —— "
     "引用它时只写硬件口径（GPU 整机、存储、机房），不写模型能力排名**（避坑 116 同族）"),
    ("`Feedly`", "https://feedly.com/", "T4 聚合器与工具",
     "**054 期按用户本轮补充清单补入** —— RSS 聚合器（T4 段）。"
     "**⚠️ 登记时即带一条边界：本报告只把它当「订阅源管理入口」，"
     "不用它替代任何一手的 RSS/Atom 抓取**（避坑 154）"),
]

added = []
for kw, url, bucket, desc in NEW_ROWS:
    if url in "\n".join(lines):
        print("  跳过（已存在）：%s %s" % (kw, url))
        continue
    added.append((kw, url, bucket, desc))
print("待新增 %d 条" % len(added))

# ---------- 2) 定位段落（行首标题）与插入点 ----------
def find_heading(prefix):
    """找行首等于 prefix 开头的标题行，返回其行号。"""
    for i, l in enumerate(lines):
        if l.startswith(prefix) and l.rstrip().endswith("）"):
            return i
    raise AssertionError("找不到标题：%s" % prefix)


def insert_row(prefix, row):
    """在 prefix 段落的最后一条表格行之后插入一行。"""
    h = find_heading(prefix)
    i = h + 1
    # 跳过表头与分隔行
    while i < len(lines) and not lines[i].startswith("|"):
        if lines[i].startswith("## ") or lines[i].startswith("### "):
            break
        i += 1
    while i < len(lines) and not lines[i].startswith("|"):
        i += 1
    # 找到该段最后一条以 | 开头的行
    last = i
    while last + 1 < len(lines) and lines[last + 1].startswith("|"):
        last += 1
    lines.insert(last + 1, row)
    return last + 1


for kw, url, bucket, desc in added:
    if bucket == "官方一手 · 国内":
        prefix = "### 官方一手 · 国内"
    elif bucket == "国内":
        prefix = "### 国内"
    elif bucket == "国外":
        prefix = "### 国外"
    else:
        prefix = "## T4 · 聚合器与工具"
    row = "| %s | %s | — | %s | 054 | 46 |" % (kw, url, desc)
    at = insert_row(prefix, row)
    print("  已插入（行 %d）：%s → %s" % (at, kw, prefix))

# ---------- 3) 同步手写计数（**只改行首标题**） ----------
DELTA = {
    "### 官方一手 · 国内": 2,   # SoMark 文档站 + Moonshot 文档另一域
    "### 国内": 2,             # CSDN + OSChina
    "### 国外": 1,             # ServeTheHome
    "## T4 · 聚合器与工具": 1,  # Feedly
}


def bump(prefix, delta):
    global lines
    i = find_heading(prefix)
    m = re.match(r"^(.*)（(\d+)(?:→(\d+))?）$", lines[i])
    assert m, lines[i]
    old = int(m.group(3) or m.group(2))
    new = old + delta
    lines[i] = "%s（%d）" % (m.group(1), new)
    print("  计数：%s %d → %d" % (prefix, old, new))
    return old, new


for k, d in DELTA.items():
    bump(k, d)

# 根节点与各 T 段总数
t0_old, t0_new = bump("## T0 · 根节点", 2)
t3_old, t3_new = bump("## T3 · 媒体", 3)
t1 = int(re.match(r"^## T1 · 社区与社交（(\d+)", lines[find_heading("## T1 · 社区与社交")]).group(1))
t2 = int(re.match(r"^## T2 · Newsletter（(\d+)", lines[find_heading("## T2 · Newsletter")]).group(1))
t4 = int(re.match(r"^## T4 · 聚合器与工具（(\d+)", lines[find_heading("## T4 · 聚合器与工具")]).group(1))
print("  全表合计：%d = T0 %d + T1 %d + T2 %d + T3 %d + T4 %d"
      % (t0_new + t1 + t2 + t3_new + t4, t0_new, t1, t2, t3_new, t4))

io.open(P, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("written:", P)
