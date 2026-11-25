# -*- coding: utf-8 -*-
"""组装 079 期 md：新写的正文 + 078 期的第四章（表体随后由 gen_table079 改写）。

纪律：
  ① 第四章（表体+脚注）从 078 整段取，只改「复核时点」与「附录指针期号」；
  ② 078 期有一段重复了三遍的「其余 N 条」blockquote（075–078 的遗留 bug），
     **本期收敛成一行**，数字以「总账 196 − 4.2 54 = 142」实算；
  ③ 章节编号不能变（build_web 的 FOLD_SECTIONS 认 sNN，TOC 认标题）。
"""
import io, re, sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
OLD = WS + "AI免费内容与权益速递-第078期-2026-11-24.md"
NEW = WS + "AI免费内容与权益速递-第079期-2026-11-25.md"

old = io.open(OLD, encoding="utf-8").read().replace("\r\n", "\n")
i = old.index("## 四、限时活动与截止时间表")
sec4 = old[i:]

assert "11/24 12:12 复核" in sec4
sec4 = sec4.replace("## 四、限时活动与截止时间表（正文之后 · 11/24 12:12 复核）",
                    "## 四、限时活动与截止时间表（正文之后 · 11/25 13:00 复核）")
assert "11/25 13:00 复核" in sec4

# 附录指针重贴当期期号（064/066 属历史指针，不动）
n_ptr = sec4.count("附录 078")
assert n_ptr > 60, n_ptr
sec4 = sec4.replace("附录 078", "附录 079")

# 收敛重复的「其余 N 条」blockquote（078 里有 3 行，数字还不一致）
lines = sec4.split("\n")
keep, dropped = [], 0
for l in lines:
    if l.startswith("> **其余 `1") and "条常驻权益本期无变化" in l:
        dropped += 1
        if dropped == 1:
            keep.append(
                "> **其余 `142` 条常驻权益本期无变化，未逐条重印** —— 全量见《[常驻权益总账](常驻权益总账.md)》（`196` 条）。"
                "**`4.2` 收录 `54` 条在跟踪的常驻权益，其中本期改写 `0` 条、补入 `0` 条、其余 `54` 条沿用上期读数**；"
                "这 `54` 条与总账是同源副本，**不重复计数**。⚠️ 这 `142` 条沿用上期读数、**本期未逐个重取** —— 不写成「已复核」。")
        continue
    keep.append(l)
assert dropped == 3, dropped
sec4 = "\n".join(keep)

parts = []
for name in ("a", "b", "c"):
    p = WS + ".workbuddy/parts079_" + name + ".md"
    parts.append(io.open(p, encoding="utf-8").read().rstrip("\n"))

md = "\n\n".join(parts) + "\n\n" + sec4
io.open(NEW, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(NEW, encoding="utf-8").read()
assert "第 079 期" in disk
assert "####" not in disk
for h in ("## 摘要（3 秒版）", "## 一、", "## 二、", "## 三、", "## 四、限时活动与截止时间表",
          "## 五、", "## 六、", "## 七、", "## 八、", "## 九、"):
    assert disk.count(h) == 1, (h, disk.count(h))
assert disk.count("> **其余 `142` 条常驻权益本期无变化") == 1
assert "附录 078" not in disk
print("written", NEW, len(disk.encode("utf-8")), "bytes; 附录指针", n_ptr)
