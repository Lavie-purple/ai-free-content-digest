# -*- coding: utf-8 -*-
"""082 期总账同步：只改两行的名字与状态（OpenRouter 计数、Ling 退出免费区）。"""
import io
import sys

WS = "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
LED = WS + "常驻权益总账.md"
MD = WS + "AI免费内容与权益速递-第082期-2026-11-28.md"
PTR = " [附录 082](details.html) |"

led = io.open(LED, encoding="utf-8").read().replace("\r\n", "\n")
n_rows = sum(1 for l in led.split("\n") if l.startswith("|")) - 2
print("总账表行（去表头/分隔）=", n_rows)

# ---------- ① OpenRouter 行
old_name = "🟢 **OpenRouter 免费档（**官方 API 目录口径 · `477/14/11`**）**"
new_name = "🟢 **OpenRouter 免费档（**官方 API 目录口径 · `475/13/10`**）**"
assert led.count(old_name) == 1, led.count(old_name)
i = led.index(old_name)
j = led.index("\n", i)
old_line = led[i:j]
new_line = (new_name + "| 未公布（动态目录） | 🟢 **全量 `477 → 475`（进 `1` / 出 `3`）、免费三项 `11 / 14 / 13` → `10 / 13 / 12`（同向 `−1`）**。 "
            "唯一进项是 `inclusionai/ling-3.2-flash:free` 摘掉 `:free` 后缀后的本体，同档案改按 `$0.30 / $0.90` 收费；真下架只有 `qwen/qwen3-235b-a22b-thinking-2507`。 "
            "`:batch` `96 → 95`、`4` 条贵价第 `3` 期未改。 `gpt-6.2` 仍 `8` 条、无 `:free`（第 `11` 天）。" + PTR)
led = led.replace(old_line, new_line, 1)

# ---------- ② Ling 3.2 Flash 行（色标 🟡 → 🟠）
old2 = "🟡 **`inclusionAI` `Ling 3.2 Flash` 进入 `OpenRouter` 免费区"
assert led.count(old2) == 1, led.count(old2)
i = led.index(old2)
j = led.index("\n", i)
old_line2 = led[i:j]
new_line2 = ("🟠 **`inclusionAI` `Ling 3.2 Flash` 退出 `OpenRouter` 免费区（`:free` 摘除 · 改按 `$0.30 / $0.90` 计费）**| "
             "**无截止日（已退出免费区，改按量计费；官方未给上下线时间）** | "
             "🟠 **本期退出（`082` 期）：`:free` 后缀被摘掉，同一档案改为 `inclusionai/ling-3.2-flash` 并收费**；`created` 仍 `2026-11-13 17:45Z`。 "
             "权重仓 `inclusionAI/Ling-3.2-air`（`MIT`、`2,403` 下载 / `309` 赞）。 **这就是免费池 `11 → 10` 的唯一原因。**" + PTR)
led = led.replace(old_line2, new_line2, 1)

if "--apply" not in sys.argv:
    print("DRY：未写盘")
    sys.exit(0)

io.open(LED, "w", encoding="utf-8", newline="\n").write(led)

back = io.open(LED, encoding="utf-8").read()
n2 = sum(1 for l in back.split("\n") if l.startswith("|")) - 2
print("落盘：行数 %d → %d，字节 %d" % (n_rows, n2, len(back.encode("utf-8"))))
assert n2 == n_rows == 196
assert "`475/13/10`" in back and "`477/14/11`" not in back
assert "退出 `OpenRouter` 免费区" in back

# ---------- ③ md 里 Ling 行的截止列
md = io.open(MD, encoding="utf-8").read().replace("\r\n", "\n")
old_dl = "**无截止日（进入免费列表，官方未给上下线时间）**"
assert md.count(old_dl) == 1, md.count(old_dl)
md = md.replace(old_dl, "**无截止日（已退出免费区，改按量计费；官方未给上下线时间）**")
io.open(MD, "w", encoding="utf-8", newline="\n").write(md)
print("md 截止列已更新")
