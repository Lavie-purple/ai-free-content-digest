#!/bin/bash
# 049 期完整流水线重跑（瘦身 MVP 落地后的定稿链）。
# 顺序：gen_table -> inject -> prune -> split_ledger -> 脚注 -> slim -> 链接化 -> extract/check -> build/verify -> lint
set -e
cd "C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15"
WS="$PWD"
cd .workbuddy

echo "=== 0) 恢复 048 期总账（gen_table 的输入之一）==="
cd "$WS" && git show HEAD:常驻权益总账.md > .workbuddy/tmp_048_ledger.md && cp .workbuddy/tmp_048_ledger.md 常驻权益总账.md
cd .workbuddy

echo "=== 1) gen_table049 ==="
python gen_table049.py | tail -3
echo "=== 2) inject049 ==="
python inject049.py | tail -3
echo "=== 3) prune ==="
python prune_table.py --md "../AI免费内容与权益速递-第049期-2026-10-27.md" --today 2026-10-27 --issue 049 | tail -2
echo "=== 4) split_ledger ==="
python split_ledger.py "../AI免费内容与权益速递-第049期-2026-10-27.md" --issue 049 | tail -6
echo "=== 5) 追加脚注 ==="
python - <<'PYEOF'
import io
WS="C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
p=WS+"AI免费内容与权益速递-第049期-2026-10-27.md"
md=io.open(p,encoding='utf-8').read()
foot=io.open(WS+".workbuddy/tmp_049_foot.md",encoding='utf-8').read()
md=md.replace("\n---\n\n*本期完。*\n","\n")
assert "*本期完。*" not in md
io.open(p,'w',encoding='utf-8',newline='\n').write(md.rstrip("\n")+"\n"+foot)
print("foot ok")
PYEOF
echo "=== 6) slim_table ==="
# ⚠️ 049 期实测：slim 需两轮才收敛（第一轮按句边界裁，第二轮把残余长段再切一刀）。
#    两轮都是幂等的：附录与 table_full 按「第 049 期」判定不重复写，table_full 保留的是第一轮的原文行。
for _R in 1 2; do
  python slim_table.py "../AI免费内容与权益速递-第049期-2026-10-27.md" --issue 049 --max 100 | tail -2
done
echo "=== 7) 指针链接化 + 导语 ==="
python - <<'PYEOF'
import io
WS="C:/Users/lavie/WorkBuddy/automation-2026-09-14-00-49-15/"
p=WS+"AI免费内容与权益速递-第049期-2026-10-27.md"
s=io.open(p,encoding='utf-8').read()
n=s.count("〔附录 049〕")
s=s.replace("〔附录 049〕","[附录 049](details.html)")
anchor="> **本章只留两类**"
i=s.index(anchor); j=s.index("\n", i)
add=("\n>\n> **049 期起第四章表体已瘦身**：**每行只留「谁 / 到什么时候 / 要不要动手」+ 一句边界**，"
     "**被裁掉的长论证一字未删地存放在 [`details.html`](details.html)（《第四章表体明细附录》，本期 %d 行）** —— "
     "**「表体里没有」不等于「没有写过」。**" % n)
s=s[:j]+add+s[j:]
io.open(p,'w',encoding='utf-8',newline='\n').write(s)
print("指针 %d 处" % n)
PYEOF
echo "=== 8) extract + check ==="
python extract_deadlines.py "../AI免费内容与权益速递-第049期-2026-10-27.md" >/dev/null
python check_deadlines.py --today 2026-10-27 | tail -2
echo "=== 9) build_web + verify ==="
python build_web.py "../AI免费内容与权益速递-第049期-2026-10-27.md" "../AI免费内容与权益速递-第049期-2026-10-27.html" | tail -2
python verify_web.py "../AI免费内容与权益速递-第049期-2026-10-27.md" "../AI免费内容与权益速递-第049期-2026-10-27.html" | tail -6
echo "=== 10) lint --strict ==="
python lint_table.py "../AI免费内容与权益速递-第049期-2026-10-27.md" --strict | grep -E "^R[0-9]|VERDICT|STRICT"
echo "ALL DONE"
