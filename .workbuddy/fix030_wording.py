# -*- coding: utf-8 -*-
"""按 check_frozen 判定修正措辞：把「新增」换成「登记」，去掉紧邻关键词的 🆕。"""
MD = "AI免费内容与权益速递-第030期-2026-10-11.md"
s = open(MD, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (old, s.count(old))
    s = s.replace(old, new)

# 行22：🆕 紧邻既存条目「珠海算力券」-> 去掉 🆕
rep("**🆕 珠海算力券剩 3 天**", "**珠海算力券剩 3 天**")
# 行314：行尾「本期新增追踪位」被 cond_b 命中
rep("（本期新增追踪位）", "（本期登记追踪位）", 2)
# 行398：行尾「本期无新增券」被 cond_b 命中
rep("本期无新增券，仍不关闭", "本期无新券，仍不关闭")
open(MD, "w", encoding="utf-8").write(s)
print("ok")
