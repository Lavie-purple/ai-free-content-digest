# -*- coding: utf-8 -*-
r"""信源台账「括号计数 vs 实际行数」逐节核对（036 期新增，因本期真派上一次用场）。

背景：`AI信息源分级清单-T0-T4.md` 的首页口径是「信源 N 条」= 五个
`## T\d …（N）` 标题括号求和；每个 `###` 子节标题里的括号数必须等于该节
实际数据行数（**表内行 + 表外补登行都算**——033 期以来新增行按既有惯例以
「表外补登行」追加在表格之后，它们是合法信源行，必须计入括号）。

036 期实例：`src036.py` 把「美国各州总检察长办公室通稿」一行误追加到 T0 块
末尾（落在「评测与榜单」节内），本脚本当场报出两处「括号 vs 实际」不一致
（政策与监管 21 vs 20、评测与榜单 17 vs 18），错位行被挪回正确小节。

用法：
    python audit_src036.py            # 核对并打印；不一致时 exit 1

判定口径：
  - 数据行 = 以 `|` 开头、非 `| 信源 | 地址 |` 表头、非 `---` 分隔行的行；
  - `## T0` / `## T3` 这类 T 级标题自身不直接挂行，其括号数 = 全部子节之和；
  - 「扫描路由规则」与「清单缺口」两张表不是信源表，不参与核对。
"""
import io
import re
import sys

P = "AI信息源分级清单-T0-T4.md"


def main():
    t = io.open(P, encoding="utf-8", newline="").read()
    assert "\r\n" not in t, "台账不是 LF 行尾，先查清再改"
    L = t.split("\n")

    secs = []
    for i, x in enumerate(L):
        m = re.match(r"^(#{2,3})\s+(.*)$", x.strip())
        if m:
            secs.append((i, m.group(1), m.group(2)))

    bad = 0
    t_of = {}          # 子节下标 -> 所属 T 级标题
    cur_t = None
    for idx, (i, lvl, title) in enumerate(secs):
        if lvl == "##" and re.match(r"^T\d", title):
            cur_t = title
        elif lvl == "###" and cur_t is not None:
            t_of[idx] = cur_t

    agg = {}
    for idx, (i, lvl, title) in enumerate(secs):
        end = secs[idx + 1][0] if idx + 1 < len(secs) else len(L)
        rows = 0
        for x in L[i + 1:end]:
            s = x.strip()
            if not s.startswith("|"):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            if cells[:2] == ["信源", "地址"]:
                continue
            rows += 1
        b = re.search(r"（(\d+)）", title)
        if not b:
            continue
        b = int(b.group(1))
        if lvl == "##":
            print("%s（T 级：括号数应 = 全部子节之和）" % title)
            continue
        flag = "" if b == rows else "   <<< 不一致"
        if b != rows:
            bad += 1
        print("  %-26s 括号=%-4s 实际=%-4d%s" % (title[:26], b, rows, flag))
        agg.setdefault(t_of.get(idx, "（无 T 级归属）"), []).append((b, rows))

    print()
    for tname, lst in agg.items():
        sb = sum(x[0] for x in lst)
        sr = sum(x[1] for x in lst)
        tb = int(re.search(r"（(\d+)）", tname).group(1))
        ok = (tb == sb == sr)
        if not ok:
            bad += 1
        print("%-24s T级括号=%-4d 子节括号和=%-4d 子节实际和=%-4d %s"
              % (tname[:24], tb, sb, sr, "OK" if ok else "<<< 不一致"))

    five = [int(re.search(r"（(\d+)）", x).group(1))
            for x in L if re.match(r"^## T\d · .*（\d+）\s*$", x)]
    print()
    print("五个 T 级标题括号：%s = %d（站点首页「信源 N 条」）"
          % (" + ".join(str(x) for x in five), sum(five)))
    print()
    if bad:
        print("VERDICT: %d 处不一致" % bad)
        return 1
    print("VERDICT: ALL GREEN（逐节括号数 = 实际行数；T 级 = 子节和）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
