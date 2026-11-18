# -*- coding: utf-8 -*-
"""第 072 期：往 headlines.json 追加一行纯事件头条（插在 071 之后，给 071 补逗号）。

⚠️ 066 期坑：文件是 UTF-8、末键无尾逗号 → 插入前必须给前一行补 `,`；
   判编码只认「utf-8 严格解成功」。
⚠️ 头条只写当天发生的**事件**（谁发布/免费了什么、额度、截止），
   不写「本报告改进了什么 / 纠错 / 轮次 / 口径」—— 那类内容进正文。
"""
import io, json, subprocess

P = ".workbuddy/data/headlines.json"
txt = io.open(P, encoding="utf-8").read()
d = json.loads(txt)  # 严格解
assert "072" not in d, "072 已存在"

HEAD = ("腾讯混元 Hy4 flash 开放权重：220.25B 总参 / 激活 11.3B / 1M 上下文，"
        "Tencent Hy License 附商用门槛")
assert len(HEAD) <= 78, len(HEAD)

anchor = '"071": '
i = txt.index(anchor)
j = txt.index("\n", i)
line071 = txt[i:j]
assert line071.rstrip().endswith('"'), line071[-40:]
assert not line071.rstrip().endswith(","), "071 行已有逗号，可能重复追加"

new = (txt[:i] + line071.rstrip() + ",\n" + '  "072": ' + json.dumps(HEAD, ensure_ascii=False)
       + txt[j:])
io.open(P, "w", encoding="utf-8", newline="\n").write(new)

back = json.loads(io.open(P, encoding="utf-8").read())   # 回读
assert back["072"] == HEAD
assert back["071"].startswith("OpenAI 把学术研究者计划")
n = len([k for k in back if not k.startswith("_")])
assert n == 72, n
print("headlines ok | %d 条（含 _readme）| 072 = %s（%d 字）" % (len(back), HEAD, len(HEAD)))

r = subprocess.run(["git", "diff", "--numstat", "--", P], capture_output=True, text=True)
print("git numstat:", r.stdout.strip() or "(仓库里尚无基线)")
