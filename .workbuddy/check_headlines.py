# -*- coding: utf-8 -*-
"""往期总目录「头条文案」守卫（2026-11-06 用户要求「以后都不要这样」后立）。

用户原话：为什么老是说这个新报告改进了什么，而不是说头条消息？改动消息用户
知道就好了，不需要作为头条。可不止我框选的，以后都不要这样。

因此判据全部实算，命中任何一条 exit 1：
  1. data/headlines.json 存在、可解析，001..最新期连续无缺号（新增一期必须登记）；
  2. 每条标题非空、不含半角竖线（会撑坏 INDEX.md 表格）、不超过 80 字
     （超过会被目录页 title_of 截断成「…」，等于又没把头条说完整）；
  3. 标题不含「报告自述 / 改动 / 纠错 / 挂账 / 口径 / 轮次 / 方法论」强特征词；
  4. 两个目录脚本的 theme_of(txt, no) 实算结果都必须等于台账值 ——
     防止脚本被改回「从刊头捞」后静默降级，或两份脚本口径分叉。

用法：python .workbuddy/check_headlines.py
"""
import importlib.util
import io
import json
import os
import re
import sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WS, ".workbuddy"))
DEF = "AI免费内容与权益速递-"
LEDGER = os.path.join(WS, ".workbuddy", "data", "headlines.json")

# 只列「报告自述」强特征；新闻事实里的「官方首次写明免费额度」等不在此列，
# 避免把真新闻误判成改动消息。
META = [
    (r"本报告", "本报告…"),
    (r"本期(?:第一次|把|拿到了|实访拿到|完成了|因此|补登|最该补)", "本期…（自述）"),
    (r"至今第一次|至今唯一|此前无人登记|一个此前", "至今/此前…"),
    (r"被追(?:了|问了)|被记了", "被追了 N 期 / 被记了 N 期"),
    (r"挂账|销项|补登|漏登", "挂账/销项/补登/漏登"),
    (r"就地更正|纠错|推翻|错不在|错的是读法|结论对、理由错|与自己的证据不一致|连续判定",
     "纠错/口径自述"),
    (r"全篇未出现|方法论级|新立避坑|避坑\s*2\d\d|逐条(?:归因|diff)|一手答案",
     "方法论/避坑自述"),
    (r"连续第\s*\d+\s*期|连续两期|期头条|期漏登|期记「", "跨期引用自述"),
    (r"三笔账|两笔账|四笔账|一笔是欠的|一笔是收的", "结案式自述"),
    (r"复核更新版|刷新版|扩版|专题版|增补轮|同日第二轮|凌晨增补轮", "版本/轮次标签"),
]
META_RE = [(re.compile(p), label) for p, label in META]


def load(name, rel):
    path = os.path.join(WS, rel)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def issues():
    """与两个 build 脚本完全一致的期号解析（文件名排序 + idx 补号）。"""
    files = sorted(fn for fn in os.listdir(WS)
                   if re.match(r"^" + re.escape(DEF) + r".*\.md$", fn))
    out = []
    for idx, fn in enumerate(files, 1):
        m = re.search(r"第\s*(\d{3})\s*期", fn)
        no = m.group(1) if m else "%03d" % idx
        out.append((no, fn))
    return out


def main():
    errs = []
    if not os.path.exists(LEDGER):
        print("VERDICT: 缺少 .workbuddy/data/headlines.json —— 头条台账是唯一真源")
        return 1
    try:
        with io.open(LEDGER, encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        print("VERDICT: 台账解析失败 —— %s" % e)
        return 1
    ledger = {k: v for k, v in raw.items() if not k.startswith("_")}
    its = issues()
    nos = [n for n, _ in its]
    latest = max(nos) if nos else "—"
    print("期数 %d（001 ~ %s）| 台账 %d 条" % (len(its), latest, len(ledger)))

    # 1) 连续覆盖 + 最新一期必须登记
    want = ["%03d" % i for i in range(1, int(latest) + 1)]
    missing = [n for n in want if n not in ledger]
    if missing:
        errs.append("台账缺期号：%s（新增一期必须登记头条）" % ", ".join(missing))
    extra = sorted(set(ledger) - set(want))
    if extra:
        errs.append("台账有不存在期号：%s" % ", ".join(extra))

    # 2/3) 每条标题的写法与安全性
    for no, _ in its:
        t = ledger.get(no)
        if t is None:
            continue
        if not isinstance(t, str) or not t.strip():
            errs.append("%s 标题为空" % no)
            continue
        if "|" in t:
            errs.append("%s 标题含半角竖线，会撑坏 INDEX.md 表格" % no)
        if len(t) > 80:
            errs.append("%s 标题 %d 字，超过目录页 80 字上限会被截断" % (no, len(t)))
        for rx, label in META_RE:
            if rx.search(t):
                errs.append("%s 标题命中元叙述「%s」：%s" % (no, label, t[:40]))
                break

    # 4) 两个脚本实算口径
    web = load("biw_guard", ".workbuddy/build_index_web.py")
    md = load("bimd_guard", ".workbuddy/build_index.py")
    mismatch = []
    for no, fn in its:
        txt = io.open(os.path.join(WS, fn), encoding="utf-8").read()
        a, b = web.theme_of(txt, no), md.theme_of(txt, no)
        if a != ledger.get(no) or b != ledger.get(no) or a != b:
            mismatch.append(no)
    if mismatch:
        errs.append("theme_of 实算与台账不一致的期次：%s" % ", ".join(mismatch))

    print("元叙述强特征 %d 组 | 两脚本实算 %d 期 | 不一致 %d 期"
          % (len(META_RE), len(its), len(mismatch)))
    print("=" * 64)
    if errs:
        print("VERDICT: %d 处不一致 —— 出刊前必须修" % len(errs))
        for x in errs:
            print("  · " + x)
        return 1
    print("VERDICT: ALL GREEN（%d 期头条均来自台账 · 无改动消息 · 两脚本口径一致）" % len(its))
    return 0


if __name__ == "__main__":
    sys.exit(main())
