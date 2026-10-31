#!/bin/bash
# 054 期完整流水线（一键重跑 · 定稿顺序）
#
# ⚠️ 053 期立的纪律，本期全部沿用：
#   ① `recalc_days054.py` 必须在 `split_ledger` 之前跑 —— 它改的是日报 md 里的「距今 N 天」；
#      若在 split_ledger 之后跑，总账（由 split_ledger 从日报重建）里留的还是旧值。
#   ② `slim_table` 必须在 `split_ledger` 之后跑，且必须跑两轮才收敛。
#   ③ 指针链接化必须在 `slim` 之后跑 —— slim 会追加「〔附录 NNN〕」标记。
#
# 顺序：gen_table → inject → recalc → prune → split_ledger → 脚注 → slim(两轮)
#       → 指针链接化 → extract/check → build/verify → lint --strict
set -e
cd "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15"
WS="$PWD"
MD="../AI免费内容与权益速递-第054期-2026-10-31.md"
cd .workbuddy

echo "=== 0) 恢复 053 期总账（gen_table 的输入之一）==="
cd "$WS" && git checkout 常驻权益总账.md && cd .workbuddy

echo "=== 1) gen_table054 ==="
python gen_table054.py | tail -3
echo "=== 2) inject054 ==="
python inject054.py | tail -2
echo "=== 3) recalc_days054（必须在 split_ledger 之前）==="
python recalc_days054.py | tail -3
echo "=== 4) prune ==="
python prune_table.py --md "$MD" --today 2026-10-31 --issue 054 --archive "$WS/.workbuddy/data/deadline_archive.md" | tail -2
echo "=== 5) split_ledger ==="
python split_ledger.py "$MD" --issue 054 | tail -5
echo "=== 6) 追加脚注 ==="
python foot054.py | tail -2
echo "=== 7) slim_table（两轮才收敛）==="
for _R in 1 2; do
  python slim_table.py "$MD" --issue 054 --max 100 | tail -2
done
echo "=== 8) 指针链接化 + 导语 ==="
python - <<'PYEOF'
import io, re
WS="C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
p=WS+"AI免费内容与权益速递-第054期-2026-10-31.md"
s=io.open(p,encoding='utf-8').read()
n=s.count("〔附录 054〕")
s=s.replace("〔附录 054〕","[附录 054](details.html)")
add=("\n>\n> **054 期起第四章表体已瘦身**：**每行只留「谁 / 到什么时候 / 要不要动手」+ 一句边界**，"
     "**被裁掉的长论证一字未删地存放在 [`details.html`](details.html)（《第四章表体明细附录》，本期 %d 行）** —— "
     "**「表体里没有」不等于「没有写过」。**" % n)
m=re.search(r"\n>\n> \*\*054 期起第四章表体已瘦身\*\*[^\n]*\n", s)
if m:
    s=s[:m.start()]+add+s[m.end():]
else:
    anchor="> **本章只留两类**"
    i=s.index(anchor); j=s.index("\n", i)
    s=s[:j]+add+s[j:]
io.open(p,'w',encoding='utf-8',newline='\n').write(s)
print("指针 %d 处" % n)
PYEOF
echo "=== 9) extract + check ==="
python extract_deadlines.py "$MD" >/dev/null
python check_deadlines.py --today 2026-10-31 | tail -2
echo "=== 10) build_web + verify ==="
python build_web.py "$MD" "../AI免费内容与权益速递-第054期-2026-10-31.html" | tail -2
python verify_web.py "$MD" "../AI免费内容与权益速递-第054期-2026-10-31.html" | tail -8
echo "=== 11) lint --strict ==="
python lint_table.py "$MD" --strict | grep -E "^R[0-9]|VERDICT|STRICT"
echo "ALL DONE 054"
