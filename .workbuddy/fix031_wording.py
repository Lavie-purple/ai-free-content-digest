# -*- coding: utf-8 -*-
"""031 期措辞修正（check_frozen 的 3 条🔴高危）：一律改措辞，不放宽守卫。
只改真正触发的那两行；其余「本期新增」属正常用法（标题 / 第八节计数），不动。"""
SRC = "AI免费内容与权益速递-第031期-2026-10-11.md"
s = open(SRC, encoding="utf-8").read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, f"expect={cnt} got={s.count(old)} :: {old[:60]}"
    s = s.replace(old, new)


# 1) 第八节「视频线独立扫描位」：无新增 -> 无当期条目登记（避免撞 Kling 4.0）
rep("本期视频线无新增", "本期视频线无当期条目登记")

# 2) 第四章 Step 5 权重开放行：本期新增官方口径 -> 本期补入（避免撞「什么值得买」）
rep(
    "**本期新增官方口径（澎湃新闻经什么值得买 10/11 清单转述）**",
    "**本期补入一条官方口径（澎湃新闻，经 10/11 权益清单转述）**",
)

open(SRC, "w", encoding="utf-8").write(s)
print("fixed 2 rows")
