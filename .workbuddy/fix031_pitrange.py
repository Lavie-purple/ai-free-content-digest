# -*- coding: utf-8 -*-
"""修 031 期一个真实缺陷：正文第 71 行有个 ### 小标题里含「避坑」，
把 build_index.py 的 pit_range() 抢走了（`^##+[^\n]*避坑` 会命中 ### 级），
导致索引里 031 期显示「避坑—」。

纪律：改措辞，不放宽守卫。
"""
import io

REPORT = "AI免费内容与权益速递-第031期-2026-10-11.md"

def rep(s, old, new, cnt=1):
    got = s.count(old)
    assert got == cnt, f"anchor expect={cnt} got={got}\n{old[:200]}"
    return s.replace(old, new)

s = io.open(REPORT, encoding="utf-8").read()

s = rep(
    s,
    "### 4. ⚡ Cloudflare 收购 Deno：本期最重要的一条「运维避坑」",
    "### 4. ⚡ Cloudflare 收购 Deno：本期最重要的一条「运维风险」",
    1,
)

# 断言：正文里再无「### 级标题含避坑」
import re
bad = [l for l in s.split("\n") if re.match(r"^#{3,6}[^\n]*避坑", l)]
assert not bad, bad
# 断言：只剩二级标题那一条
h2 = [l for l in s.split("\n") if re.match(r"^## [^\n]*避坑", l)]
assert len(h2) == 1 and "138–141" in h2[0], h2

io.open(REPORT, "w", encoding="utf-8").write(s)
print("已改：### 运维避坑 -> ### 运维风险 ; 二级避坑标题唯一 =", h2[0])
