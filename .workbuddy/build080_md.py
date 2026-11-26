# -*- coding: utf-8 -*-
"""组装 080 期 md：新写的正文 + 079 期的第四章（表体随后由 gen_table080 改写）。"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
OLD = WS + "AI免费内容与权益速递-第079期-2026-11-25.md"
NEW = WS + "AI免费内容与权益速递-第080期-2026-11-26.md"

old = io.open(OLD, encoding="utf-8").read().replace("\r\n", "\n")
i = old.index("## 四、限时活动与截止时间表")
sec4 = old[i:]

assert "11/25 13:00 复核" in sec4
sec4 = sec4.replace("## 四、限时活动与截止时间表（正文之后 · 11/25 13:00 复核）",
                    "## 四、限时活动与截止时间表（正文之后 · 11/26 09:00 复核）")
assert "11/26 09:00 复核" in sec4

n_ptr = sec4.count("附录 079")
assert n_ptr > 80, n_ptr
sec4 = sec4.replace("附录 079", "附录 080")

# 「其余 142 条」那句：本期总账仍 196、4.2 仍 54 → 142 不变，只把「改写 25」交给 gen_table080
assert "本期改写 `25` 条" in sec4

parts = []
for name in ("a", "b", "c"):
    p = WS + ".workbuddy/parts080_" + name + ".md"
    parts.append(io.open(p, encoding="utf-8").read().rstrip("\n"))

md = "\n\n".join(parts) + "\n\n" + sec4
io.open(NEW, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(NEW, encoding="utf-8").read()
assert "第 080 期" in disk
assert "####" not in disk
for h in ("## 摘要（3 秒版）", "## 一、", "## 二、", "## 三、", "## 四、限时活动与截止时间表",
          "## 五、", "## 六、", "## 七、", "## 八、", "## 九、"):
    assert disk.count(h) == 1, (h, disk.count(h))
assert "附录 079" not in disk
print("written", NEW, len(disk.encode("utf-8")), "bytes; 附录指针", disk.count("附录 080"))
