# -*- coding: utf-8 -*-
"""第七次压缩 MEMORY.md：
1) 把「期纪律速查」050/052/053/054/055/058/059/065/066/067 十条原文逐字搬进
   ENGINEERING.md 的 §十·37（搬完逐行断言十条全在新位置）；
2) MEMORY.md 只留「触发词」级索引；
3) 回读断言：文件变小、十条原文不再在 MEMORY.md、索引十条齐全、CR=0。
"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, ".workbuddy", "memory", "MEMORY.md")
ENG = os.path.join(ROOT, ".workbuddy", "memory", "ENGINEERING.md")

mem = io.open(MEM, encoding="utf-8").read()
eng = io.open(ENG, encoding="utf-8").read()
before = len(mem.encode("utf-8"))

lines = mem.split("\n")
# 定位期纪律十条：以 '- **050**' 起、到文件末尾最后一条 '- **067**'
i_start = next(i for i, l in enumerate(lines) if l.startswith("- **050**"))
block = lines[i_start:]
block = [l for l in block if l.strip()]
assert len(block) == 10, len(block)
assert block[0].startswith("- **050**") and block[-1].startswith("- **067**")

# ---------- 1) 原文搬进附卷 ----------
sec = []
sec.append("")
sec.append("## §十·37 · MEMORY.md 期纪律速查全文归位（第七次压缩 · 2026-11-14）")
sec.append("")
sec.append("> **来源**：2026-11-14 第七次压缩（`19,575` 字节触顶被截断，末条 `067` 断在半句）。")
sec.append("> 下列十条是压缩前 `MEMORY.md`「期纪律速查」的**逐字原文**，一个字未改；")
sec.append("> `MEMORY.md` 侧只保留「触发词」级索引。**索引与原文冲突时，以本节原文为准。**")
sec.append("> 第六次压缩搬进来的 `050/052/053/054/055/058` 更早的全文见 §十·29–36，本节是它们的**速查版**。")
sec.append("")
for l in block:
    sec.append(l)
    sec.append("")
add = "\n".join(sec)

assert "## §十·37" not in eng, "§十·37 已存在"
eng2 = eng.rstrip("\n") + "\n" + add
io.open(ENG, "w", encoding="utf-8", newline="\n").write(eng2)
eng_chk = io.open(ENG, encoding="utf-8").read()
miss = [l for l in block if l not in eng_chk]
assert not miss, ["附卷缺行", miss]
assert "\r" not in eng_chk

# ---------- 2) MEMORY.md 换索引 ----------
NEW_INDEX = [
    "## 期纪律索引（全十条原文见附卷 §十·37）",
    "",
    "> 每条只留**触发词**；写脚本/脚注/断言前**按需去 §十·37 读原文**，不要凭索引扩写。",
    "",
    "- **050**（§十·37）：`prune_table --archive` 默认**相对路径** → 幽灵 `.workbuddy/.workbuddy/` · `split_ledger` 判「无截止日常驻档」靠**截止列开头关键词** · `REWRITE` 键逐字符一致、`NEW` 行末必带 ` |`。",
    "- **052**（§十·37）：改写后**回读落盘文件**再断言 · `inject` 源必须与产物同步 · `slim` 前先剥历史指针 · **硬裁预算 = `maxc − 16`** · `403` 先换合规 UA。",
    "- **053**（§十·37）：**断言是必要条件、不是充分条件**（回读）· `recalc_days` 必须跑在 `split_ledger` **之前** · 状态列禁「未开始/已结束」、截止列禁「月底」· 🔴 常是措辞触发（「新增」→「补入」）。",
    "- **054**（§十·37）：在状态列解释「本行不是某状态」= **解释即触发** · 单元格禁 `|`（守门＝**字段数分布**）· `NEW` 行必带「本期」· **记忆只能追加** · 总账基线取**上期 commit**。",
    "- **055**（§十·37）：截止日跨基准日 → 状态列改「**已过 N 天**」，不写负值 · HTML grep 数字分**三档**报告 · 断言用**逐字短语** · 分类统计必须在 `slim` **之后**取。",
    "- **058**（§十·37）：**「命中 0 条」= 没找到对象，不是通过** · 截止列不可解析会被 `normalize` 跳过 → 在 `gen_table` **显式替换** · `curl 000` **不建文件** · CSV 字段禁半角逗号。",
    "- **059**（§十·37）：**`slim` 只留状态列首句** → 当期事实用 `set_status()` 整体改写 · `split(\"|\")` 首段是空串（`1/2/3`）· `HF createdAt` = **建仓时间** · **免费条目靠目录 diff、不靠标题** · 附录指针**重贴当期期号**。",
    "- **065**（§十·37）：**`search=` 空数组 ≠ 不存在**（先 `?author=<org>` 拉全量）· **两个观测点不能写「调价」** · `CSV = 总账 + 4.1`（`4.2` 是总账副本）· 脚注真表格会被当台账 → 改列表。",
    "- **066**（§十·37）：`headlines.json` 是 **UTF-8**（判编码只认 **utf-8 严格解成功**）· 末键**无尾逗号** → 插前补 `,` · push 后「期页 `404` + 其余页变小」= **部署还没跑**（查 `deployments` 的 `sha`）· **SKU 迁移 ≠ 新增模型**。",
    "- **067**（§十·37）：**纠错前先换一条与解析器无关的正则复核** · 「当天核实 N 条」是**进行值** · `license: other` **必须读 `LICENSE` 原文** · **`4.2` 行名须与《总账》逐字一致**（对不上先查名字、别先怀疑抽取器）。",
]

new_lines = lines[:i_start] + NEW_INDEX + [""]
mem2 = "\n".join(new_lines)

# 头部压缩说明同步
old_head = """**⚠️ 本文件 2026-11-05 第六次压缩**（`22,155 → 10,016` 字节）：`050 / 052 / 053 / 054 / 055 / 058`
> 六段期纪律原文**逐字搬进附卷 §十·36**（搬运后逐行断言「原文每一行都在新位置」，`122` 行全中），
> 本文件只留一行一条的压缩速查。**要原文去 §十·36，不要凭这一行扩写。**"""
new_head = """**⚠️ 本文件 2026-11-14 第七次压缩**（`19,575 → 约 14,100` 字节，前一次已触顶被截断）：
> `050/052/053/054/055/058/059/065/066/067` 十条速查**逐字搬进附卷 §十·37**（搬后断言十条全在新位置），
> 本文件只留「触发词」级索引。**要原文去 §十·37**；第六次搬的六段更早原文在 §十·36。
> **索引与原文冲突，以附卷原文为准。**"""
assert old_head in mem2
mem2 = mem2.replace(old_head, new_head)

io.open(MEM, "w", encoding="utf-8", newline="\n").write(mem2)

# ---------- 3) 回读断言 ----------
chk = io.open(MEM, encoding="utf-8").read()
after = len(chk.encode("utf-8"))
assert "\r" not in chk
assert after < before, (before, after)
assert after < 16000, after
for l in block:  # 原文必须已不在 MEMORY.md
    assert l not in chk, l[:30]
for tag in ("050", "052", "053", "054", "055", "058", "059", "065", "066", "067"):
    assert ("- **%s**" % tag) in chk, tag
assert "§十·37" in chk
assert "## 期纪律索引" in chk

print("MEMORY.md %d -> %d bytes (-%d) | lines %d -> %d" %
      (before, after, before - after, len(lines), chk.count("\n")))
print("ENGINEERING.md %d -> %d bytes | 搬入 %d 行" %
      (len(eng.encode("utf-8")), len(eng_chk.encode("utf-8")), len(block)))
