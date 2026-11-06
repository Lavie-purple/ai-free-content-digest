# -*- coding: utf-8 -*-
"""060 期补丁：把两个目录脚本的头条来源切到 headlines.json 台账。

按 052 期纪律：每处替换先断言「命中且只命中 1 次」，写完**回读落盘文件**
再逐条断言新文本真的进去了 —— 断言是必要条件，不是充分条件。
"""
import io
import os

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BLOCK = '''
# ---------------------------------------------------------------- 头条台账
# 2026-11-06 用户要求：往期总目录只显示「当天发生了什么」这条新闻本身，
# 不要把「本报告改进了什么 / 纠错 / 挂账 / 补登 / 口径 / 轮次 / 方法论」当头条。
# 那些内容留在正文里给读者看即可，不占头条位。
# 头条改由 data/headlines.json 显式登记；新增一期必须登记，
# check_headlines.py 会守（缺行或写回元叙述即 exit 1）。
HEADLINES_PATH = os.path.join(WS, ".workbuddy", "data", "headlines.json")


def load_headlines():
    if not os.path.exists(HEADLINES_PATH):
        return {}
    with io.open(HEADLINES_PATH, encoding="utf-8") as f:
        d = json.load(f)
    return {k: v for k, v in d.items() if not k.startswith("_")}


HEADLINES = load_headlines()
'''

JOBS = {
    ".workbuddy/build_index_web.py": [
        ("import html as H\nimport io\n", "import html as H\nimport io\nimport json\n"),
        ('ACCENT = "#bf3327"\n', 'ACCENT = "#bf3327"\n' + BLOCK),
        ("def theme_of(text):\n", "def theme_of(text, no=None):\n"),
        ("    tagline = _date_tagline(text)\n    if tagline:\n",
         "    # 台账优先：目录头条是显式登记的新闻事件，不再从刊头定位语推导\n"
         "    if no and no in HEADLINES:\n"
         "        return HEADLINES[no]\n"
         "    tagline = _date_tagline(text)\n    if tagline:\n"),
        ("theme_of(txt),", "theme_of(txt, no),"),
        ('esc(title_of(it["theme"])), ab, "".join(btns))',
         'esc(title_of(it["theme"], 80)), ab, "".join(btns))'),
        ('esc(title_of(it["theme"], 46)),', 'esc(title_of(it["theme"], 72)),'),
    ],
    ".workbuddy/build_index.py": [
        ("import io, os, re\n", "import io, json, os, re\n"),
        ('DEF = "AI免费内容与权益速递-"\n',
         'DEF = "AI免费内容与权益速递-"\n' + BLOCK),
        ("def theme_of(text):\n", "def theme_of(text, no=None):\n"),
        ("    tagline = _date_tagline(text)\n    if tagline:\n",
         "    # 台账优先：与 build_index_web.py 保持同一真源\n"
         "    if no and no in HEADLINES:\n"
         "        return HEADLINES[no]\n"
         "    tagline = _date_tagline(text)\n    if tagline:\n"),
        ("theme_of(txt),", "theme_of(txt, no),"),
    ],
}


def patch(rel, pairs):
    p = os.path.join(WS, rel)
    raw = open(p, "rb").read()
    nl = "\r\n" if raw.count(b"\r\n") == raw.count(b"\n") and raw.count(b"\n") else "\n"
    s = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, (rel, "命中次数异常", n, repr(old[:70]))
        s = s.replace(old, new, 1)
    with io.open(p, "w", encoding="utf-8", newline=nl) as f:
        f.write(s)
    # 回读落盘文件再断言（052 期纪律）
    disk = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert new in disk, (rel, "新文本未落盘", repr(new[:70]))
        assert old not in disk or old in new, (rel, "旧文本残留", repr(old[:70]))
    print("patched %-38s %d 处" % (rel, len(pairs)))


for rel, pairs in JOBS.items():
    patch(rel, pairs)

print("\n落盘复核完成")
