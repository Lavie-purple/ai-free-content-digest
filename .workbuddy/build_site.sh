#!/bin/bash
# 站点五页重建 + 守卫（与期号无关，任何一期出刊后都能直接跑）
#
# 2026-11-02 起（用户要求「以后每天运行都把极速视图作为首页」）：
#   根路径 index.html **就是极速视图**，与 quick.html 逐字节相同，由 build_quick.py 一次写两份；
#   往期总目录搬到 archive.html（build_index_web.py）。
#   **顺序不能反**：先 build_quick（产出 quick.html + index.html），再 build_index_web（读总数写目录）。
#
# 为什么单独抽一个脚本：
#   以前这几页散在出刊流水线末尾靠人记（run0NN.sh 各自抄一遍），
#   漏跑任何一页都不会报错、只是读者看到旧内容。抽出来 + 末尾两个守卫 exit 1，
#   就把「记得跑」变成「跑不通就推不上去」。
#
# 用法：
#   bash .workbuddy/build_site.sh
set -e
cd "$(dirname "$0")/.."
WS="$PWD"

# 最新一期：按文件名排序后取最后一个（期号是三位零填充，字典序 = 期号序；
# 不用 mtime —— 回填旧期会把 mtime 刷新，反而把旧期顶到最前）。
MD=$(ls AI免费内容与权益速递-第*.md | sort | tail -1)
BASE="${MD%.md}"
echo "最新一期：$BASE"

echo "=== 1/6 完整日报 ==="
python .workbuddy/build_web.py "$MD" "$BASE.html" | tail -2

echo "=== 2/6 常驻总账 ==="
python .workbuddy/build_web.py "常驻权益总账.md" "standing.html" | tail -1

echo "=== 3/6 第四章表体明细附录 ==="
python .workbuddy/build_web.py "第四章表体明细附录.md" "details.html" | tail -1

echo "=== 4/6 极速视图（quick.html + 首页 index.html）==="
python .workbuddy/build_quick.py

echo "=== 5/6 往期总目录（archive.html）==="
python .workbuddy/build_index_web.py | head -1
python .workbuddy/build_index.py | head -2

echo "=== 6/6 守卫 ==="
python .workbuddy/check_views.py | tail -2
python .workbuddy/check_site_freshness.py | tail -2
echo "SITE DONE"
