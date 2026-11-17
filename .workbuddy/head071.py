# -*- coding: utf-8 -*-
"""第 071 期：往 headlines.json 追加一行纯事件头条（插在 070 之后，给 070 补逗号）。

⚠️ 066 期坑：文件是 UTF-8、末键无尾逗号 → 插入前必须给前一行补 `,`；
   判编码只认「utf-8 严格解成功」。
⚠️ 头条只写当天发生的**事件**（谁发布/免费了什么、额度、截止），
   不写「本报告改进了什么 / 纠错 / 轮次 / 口径」—— 那类内容进正文。
"""
import io, json, subprocess

P = ".workbuddy/data/headlines.json"
txt = io.open(P, encoding="utf-8").read()
d = json.loads(txt)  # 严格解
assert "071" not in d, "071 已存在"

HEAD = ("OpenAI 把学术研究者计划扩到 20 万人：11/23 开放 5 万个名额、每人带 2 名协作者，"
        "档位从 Pro 降到 Plus")
assert len(HEAD) <= 78, len(HEAD)

anchor = '"070": '
i = txt.index(anchor)
j = txt.index("\n", i)
line070 = txt[i:j]
assert line070.rstrip().endswith('"'), line070[-40:]
assert not line070.rstrip().endswith(","), "070 行已有逗号，可能重复追加"

new = (txt[:i] + line070.rstrip() + ",\n" + '  "071": ' + json.dumps(HEAD, ensure_ascii=False)
       + txt[j:])
io.open(P, "w", encoding="utf-8", newline="\n").write(new)

back = json.loads(io.open(P, encoding="utf-8").read())   # 回读
assert back["071"] == HEAD
assert back["070"].startswith("腾讯混元 Hy4 flash")
n = len([k for k in back if not k.startswith("_")])
assert n == 71, n
print("headlines ok | %d 条（含 _readme）| 071 = %s（%d 字）" % (len(back), HEAD, len(HEAD)))

r = subprocess.run(["git", "diff", "--numstat", "--", P], capture_output=True, text=True)
print("git numstat:", r.stdout.strip() or "(仓库里尚无基线)")
