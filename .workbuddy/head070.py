# -*- coding: utf-8 -*-
"""第 070 期：往 headlines.json 追加一行纯事件头条（插在 069 之后，给 069 补逗号）。"""
import io, json

P = ".workbuddy/data/headlines.json"
txt = io.open(P, encoding="utf-8").read()
d = json.loads(txt)  # 严格解，判编码只认这个
assert "070" not in d, "070 已存在"

HEAD = ("腾讯混元 Hy4 flash 发布并在 WorkBuddy 内限免：224B 总参（含 64B Engram）/ 激活 12B / "
        "1M 上下文，聚合层写到 11/29、媒体写「11 月 30 日前」")

anchor = '"069": '
i = txt.index(anchor)
j = txt.index("\n", i)                            # 069 那一行的行尾
line069 = txt[i:j]
assert line069.rstrip().endswith('"'), line069[-40:]
assert not line069.rstrip().endswith(","), "069 行已有逗号，可能重复追加"

new = (txt[:i] + line069.rstrip() + ",\n" + '  "070": ' + json.dumps(HEAD, ensure_ascii=False)
       + txt[j:])
io.open(P, "w", encoding="utf-8", newline="\n").write(new)

back = json.loads(io.open(P, encoding="utf-8").read())
assert back["070"] == HEAD
assert back["069"].startswith("美团 LongCat-2.5")
assert len([k for k in back if not k.startswith("_")]) == 70, len(back)
print("headlines ok | %d 条（含 _readme）| 070 = %s" % (len(back), HEAD))

# diff 收敛检查：只应多 2 行（069 补逗号 + 新行）
import subprocess
r = subprocess.run(["git", "diff", "--numstat", "--", P], capture_output=True, text=True)
print("git numstat:", r.stdout.strip())
