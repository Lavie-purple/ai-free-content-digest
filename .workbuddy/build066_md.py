# -*- coding: utf-8 -*-
"""组装 066 期 md：新写的正文 + 065 期的第四章（表体随后由 gen_table066 改写）"""
import io

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
OLD = WS + "AI免费内容与权益速递-第065期-2026-11-11.md"
NEW = WS + "AI免费内容与权益速递-第066期-2026-11-12.md"

old = io.open(OLD, encoding="utf-8").read().replace("\r\n", "\n")
i = old.index("## 四、限时活动与截止时间表")
sec4 = old[i:]

parts = []
for name in ("a", "b", "c"):
    p = WS + ".workbuddy/parts066_" + name + ".md"
    parts.append(io.open(p, encoding="utf-8").read().rstrip("\n"))

md = "\n\n".join(parts) + "\n\n" + sec4
io.open(NEW, "w", encoding="utf-8", newline="\n").write(md)

disk = io.open(NEW, encoding="utf-8").read()
assert "## 四、限时活动与截止时间表" in disk
assert disk.count("## 一、") == 1 and disk.count("## 五、") == 1
print("written", NEW, len(disk.encode("utf-8")), "bytes")
