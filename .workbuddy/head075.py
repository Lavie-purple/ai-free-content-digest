# -*- coding: utf-8 -*-
"""第 075 期：往 headlines.json 追加一行纯事件头条（插在 074 之后，给 074 补逗号）。

⚠️ 066 期坑：文件是 UTF-8、末键无尾逗号 → 插入前必须给前一行补 `,`；
   判编码只认「utf-8 严格解成功」。
⚠️ 073 期坑：改期号脚本漏改 `new` 里的键名 → JSON 出现重复键。本期所有 `"0NN"` 一起改，
   并在回读时断言 075 存在、074 未被覆盖。
⚠️ 头条只写当天发生的**事件**（谁发布/免费了什么、额度、截止），
   不写「本报告改进了什么 / 纠错 / 口径」—— 那类内容进正文。
"""
import io
import json
import subprocess

P = ".workbuddy/data/headlines.json"
txt = io.open(P, encoding="utf-8").read()
d = json.loads(txt)  # 严格解
assert "075" not in d, "075 已存在"
assert "074" in d

HEAD = ("Thinking Machines 开源 Inkling 2 Mini：26.4B/3.4B、权重约 20GB、Apache-2.0，可在笔记本离线跑")
assert len(HEAD) <= 78, len(HEAD)

anchor = '"074": '
i = txt.index(anchor)
j = txt.index("\n", i)
line = txt[i:j]
assert line.rstrip().endswith('"'), line[-40:]
assert not line.rstrip().endswith(","), "074 行已有逗号，可能重复追加"

new = (txt[:i] + line.rstrip() + ",\n" + '  "075": ' + json.dumps(HEAD, ensure_ascii=False)
       + txt[j:])
io.open(P, "w", encoding="utf-8", newline="\n").write(new)

back = json.loads(io.open(P, encoding="utf-8").read())   # 回读
assert back["075"] == HEAD
assert back["074"].startswith("AutoClaw 11/23-11/29")
n = len([k for k in back if not k.startswith("_")])
assert n == 75, n
print("headlines ok | %d 条（含 _readme）| 075 = %s（%d 字）" % (len(back), HEAD, len(HEAD)))

r = subprocess.run(["git", "diff", "--numstat", "--", P], capture_output=True, text=True)
print("git numstat:", r.stdout.strip() or "(仓库里尚无基线)")
