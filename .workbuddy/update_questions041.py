# -*- coding: utf-8 -*-
"""041 期待澄清项（Q29–Q31）追加到 .workbuddy/data/open_questions.md。
⚠️ 行尾纪律：`data/` 下是 CRLF，二进制追加。
⚠️ 先读现有最大编号，避免撞号。
"""
import re
from collections import Counter

F = ".workbuddy/data/open_questions.md"
text = open(F, encoding="utf-8").read()
nums = [int(m.group(1)) for m in re.finditer(r"^\| Q(\d+) \|", text, re.M)]
print("existing Q ids:", min(nums), "-", max(nums), "count", len(nums))
assert max(nums) < 29, ("撞号：Q29 已被占用", max(nums))

ROWS = [
    ("Q29",
     "`AutoClaw` M10W3 活动页「同 URL 被改写」的两个未定项（是否还会有下一次改写 / 旧版截图的处置）",
     "**041 期首次登记的条目类型「同一 URL 的活动内容被官方就地改写」，留下三个只能等后续动作才能判定的未定项**："
     "**① 官方是否会公布这次改写的说明 —— 即 85M 是「活动加码」还是「把原定给会员的那部分并进了全体档」？"
     "本轮只看到标题与规则变了，没有任何一句解释**；"
     "**② 10/19 之前按旧版（60M / 10/19 单日 3000 万）已经领过的账号，是否按新档位补差 —— 官方页未写**；"
     "**③ 已经按旧版截图发过文的第三方（本期核到至少两处），是否会更正 —— 本轮核到其中一篇已在另一篇里更正了"
     "「付费会员加赠」那一条，但未更正档位那一条**。"
     "**为什么挂账**：**这三条每一条都会改变「读者今天该不该按截图行动」的判断，而目前只能确定「页面内容已变」这一条**。"
     "**回扫节点：活动期结束（10/25）之后官方是否发收口说明，以及 M10W4 或后续档期页是否再次发生改写**"),
    ("Q30",
     "`Bolt` Builders Week 的官方细则页在哪（本轮站内两个候选 URL 均未取到）",
     "**041 期补登 `Bolt` Builders Week 时遇到取料面问题**："
     "**`bolt.new/blog/builders-week` 返回的是产品首页、`support.bolt.new/Builders-Week` 返回 404，"
     "官方 X 只给了三句核心信息（免费范围 / 周末日期 Oct 17 + 18 / 投稿截止 Oct 20）**。"
     "**因此以下字段全部只有第三方规则整理站的口径，本轮未能取到一手表述**："
     "**① 免费周末的确切起止时刻（美西 10/17 00:00 → 10/18 23:59）与时区写法**；"
     "**② 六小时分块的具体 token 数（官方未公布）与「付费档 5×」的口径**；"
     "**③ 竞赛的三档奖金 10,000 / 5,000 / 2,500 美元、四项等权评审、免费档即可参赛**；"
     "**④ 地区排除名单（明确含中国大陆）与 18 岁门槛**；"
     "**⑤ `Bolt Forge` 的数据训练条款（提示词 / 代码 / 项目文件的去标识化版本用于训练开放权重模型，"
     "EEA / 英国 / 瑞士除外）与「Model training 开关管不到 Forge」这一条**。"
     "**为什么挂账**：**第 ⑤ 条是要签字之前必须知道的事（数据是否被用于训练），其余四条是额度与资格的事，"
     "而五项目前都只有一个非一手来源**（避坑 116）。"
     "**回扫节点：`Bolt` 站内出现可访问的 Builders Week 细则页或官方规则 PDF 之时；"
     "或 `support.bolt.new` 恢复该条目之时**"),
    ("Q31",
     "`OpenAI` `Rosalind Academic Plan` 的两个未定项（申请截止日 / 名额与审批时点）",
     "**041 期首次成条登记 `OpenAI` `Rosalind Academic Plan` 时留下两个官方页没有回答、但决定「现在申请还赶不赶得上」的问题**："
     "**① 申请截止日期 —— 官方页既没有写申请截止日，也没有写名额上限或「先到先得」**；"
     "**② 审批时点与结果的通知周期 —— 官方只写「trusted access process」与四步流程"
     "（explore / sign in + apply / complete verification / start research），没有写审批要多久、也没有写通过率**。"
     "**为什么挂账**：**这两条合起来决定了「早申请 vs 晚申请」的策略 —— "
     "若名额制且先到先得，则晚申请等于申请不到；若审批周期长，则早申请才有意义；"
     "而目前两种可能都排除不掉**（避坑 182）。"
     "**附一条同族待澄清**：`Anthropic` 10/18 公告里的「discounts on Claude for nonprofits and scientific institutions」"
     "同样没有折扣幅度 / 适用地区 / 申请条件 / 有效期 —— **但官方在同一段里把它列为「公司内部仍在做的事」，"
     "不是本公告的新承诺**，故不另立 Q，只在此处记一笔同族**（避坑 41 第一层）。"
     "**回扫节点：官方页出现申请截止日或名额说明之时；或出现第一份获批名单 / 申请指引页之时**"),
]

lines = []
for qid, title, body in ROWS:
    assert "|" not in title and "|" not in body, qid
    lines.append("| %s | **%s** | %s |" % (qid, title, body))

with open(F, "ab") as f:
    f.write(("\r\n".join(lines) + "\r\n").encode("utf-8"))

rows = [l for l in open(F, encoding="utf-8").read().split("\n") if l.startswith("| Q")]
print("Q rows now:", len(rows))
print("appended:", len(ROWS))
