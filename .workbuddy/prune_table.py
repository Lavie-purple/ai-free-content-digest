# -*- coding: utf-8 -*-
"""第四章截止表 · 保留规则（048 期起固定步骤，047 期修订版首次执行）

规则（用户 2026-10-27 提出：过期太久的历史条目要及时剔除）
  KEEP-1  截止日不可解析（`未公布` / 相对日期 / 空白）        -> 保留（用户明确例外）
  KEEP-2  截止日 >= 基准日（未过期）                          -> 保留
  KEEP-3  已过期但未收口（状态列非 ⚪：如 🔴 必办 / 🟢 生效中）  -> 保留（是待办，不是史料）
  KEEP-4  已过期但 age <= GRACE（默认 7 天）                   -> 保留（宽限期，供查是否延期）
  DROP    已过期、已收口（⚪）、且 age > GRACE                 -> 移出表体，原文逐行归档

用法：
  python prune_table.py --md "AI免费内容与权益速递-第047期-2026-10-27.md" \
      --today 2026-10-27 --issue 047 --grace 7
  python prune_table.py ... --dry-run     # 只报告，不写文件
"""
import argparse
import io
import os
import re
import sys
from datetime import date

ARCHIVE_DEFAULT = ".workbuddy/data/deadline_archive.md"


def parse_date(raw, default_year=2026):
    """把截止列原文解析为 date；解析不了返回 None。
    覆盖：2026-09-03 / 2026/9/3 / 2026年9月3日 / 10/14 / 10/7 14:00 / 9 月底 / 「已退役 2026-07-30」。
    """
    t = (raw or "").strip()
    if not t:
        return None
    # 全日期
    m = re.search(r"(\d{4})\s*[-/年]\s*(\d{1,2})\s*[-/月]\s*(\d{1,2})", t)
    if m:
        y, mo, d = (int(x) for x in m.groups())
        try:
            return date(y, mo, d)
        except ValueError:
            return None
    # 月/日（当年）
    m = re.search(r"(?<!\d)(\d{1,2})\s*/\s*(\d{1,2})(?!\d)", t)
    if m:
        mo, d = int(m.group(1)), int(m.group(2))
        try:
            return date(default_year, mo, d)
        except ValueError:
            return None
    # 「9 月底」
    m = re.search(r"(\d{1,2})\s*月\s*底", t)
    if m:
        mo = int(m.group(1))
        nxt = date(default_year + (mo == 12), mo % 12 + 1, 1)
        return nxt.fromordinal(nxt.toordinal() - 1)
    return None


def cells(line):
    parts = line.split("|")
    return [p.strip() for p in parts]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    ap.add_argument("--today", required=True)
    ap.add_argument("--issue", required=True, help="期号，三位，如 047")
    ap.add_argument("--grace", type=int, default=7)
    ap.add_argument("--archive", default=ARCHIVE_DEFAULT)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    today = date(*map(int, a.today.split("-")))
    md = io.open(a.md, encoding="utf-8").read()
    lines = md.split("\n")

    st = en = None
    for i, l in enumerate(lines):
        if l.startswith("## 四、"):
            st = i
        elif st is not None and l.startswith("## 五、"):
            en = i
            break
    assert st is not None and en is not None, "找不到第四章边界"

    idx_body = []          # 表体行的行号
    for i in range(st, en):
        l = lines[i]
        if not l.startswith("|"):
            continue
        if l.startswith("| 口径") or l.startswith("| ---"):
            continue
        # 表头判定必须严格：只认「三个单元格依次为 活动/截止/状态」，
        # 不能用「包含这三个词」——正文行里出现「活动…截止…状态」会被误判为表头跳过（047 期实踩）。
        if [c.strip() for c in l.split("|") if c.strip()][:3] == ["活动", "截止", "状态"]:
            continue
        idx_body.append(i)
    assert idx_body, "第四章没有解析到表体行"

    keep, drop = [], []
    for i in idx_body:
        c = cells(lines[i])
        name = c[1] if len(c) > 1 else ""
        due_raw = c[2] if len(c) > 2 else ""
        status = c[3] if len(c) > 3 else ""
        d = parse_date(due_raw)
        closed = status.lstrip().startswith("⚪")
        age = (today - d).days if d else None
        if d is None:
            keep.append((i, name, due_raw, status, age, "K1 截止日不可解析"))
        elif age < 0:
            keep.append((i, name, due_raw, status, age, "K2 未过期"))
        elif not closed:
            keep.append((i, name, due_raw, status, age, "K3 已过期但未收口"))
        elif age <= a.grace:
            keep.append((i, name, due_raw, status, age, "K4 宽限期内"))
        else:
            drop.append((i, name, due_raw, status, age, "DROP 过期且已收口"))

    print(f"表体 {len(idx_body)} 行 = 保留 {len(keep)} + 移出 {len(drop)}（grace={a.grace} 天，基准日 {today}）")
    if drop:
        print("\n移出清单：")
        for _, n, r, s, age, _ in sorted(drop, key=lambda x: -x[4]):
            print(f"  过期{age:3d}天 | {r:12s} | {n[:56]}")
    edge = [k for k in keep if k[4] is not None and k[4] > a.grace]
    if edge:
        print("\n按例外保留的「过期较久」行：")
        for _, n, r, s, age, why in edge:
            print(f"  过期{age:3d}天 | {why} | {n[:52]}")

    if a.dry_run:
        print("\n[dry-run] 未写文件")
        return

    # ---- 归档：原文逐行留存，不截断 ----
    os.makedirs(os.path.dirname(a.archive), exist_ok=True)
    arch = io.open(a.archive, encoding="utf-8").read() if os.path.exists(a.archive) else (
        "# 截止时间表 · 归档区\n\n"
        "> 第四章表体移出的条目在这里逐行留存原文（不删、不截断、不改写）。\n"
        "> 移出规则：截止日可解析 **且** 已过期超过宽限期 **且** 状态为「⚪ 已收口」**且** 不是未收口待办。\n"
        "> 反向查找：想看某个历史活动，在本文件搜关键词即可（表体 - 归档 = 全部历史）。\n"
    )
    head = f"## {a.issue} 期（归档日 {a.today} · 移出 {len(drop)} 条）"
    block = [head, ""]
    if drop:
        block.append("| 活动 | 截止 | 状态 |")
        block.append("| --- | --- | --- |")
        for i, *_ in drop:
            block.append(lines[i])
    block.append("")
    pat = re.compile(r"^## " + re.escape(a.issue) + r" 期（归档日.*?）\n(?:.|\n)*?(?=\n## |\Z)")
    new_block = "\n".join(block)
    if not drop:
        # 幂等保护：重跑时若无移出项，绝不能用空块覆盖已有归档（047 期实踩边界）
        print("\n本期无移出项，归档区未改动（已有内容保留）")
    elif pat.search(arch):
        arch = pat.sub(new_block.rstrip("\n") + "\n", arch, count=1)
    else:
        arch = arch.rstrip("\n") + "\n\n" + new_block
    io.open(a.archive, "w", encoding="utf-8", newline="").write(arch)

    # ---- 重写第四章表体 ----
    drop_set = {d[0] for d in drop}
    out = [l for i, l in enumerate(lines) if i not in drop_set]
    io.open(a.md, "w", encoding="utf-8", newline="").write("\n".join(out))
    print(f"\n已写：{a.md}（{len(lines)} -> {len(out)} 行）")
    print(f"已归档：{a.archive}（{a.issue} 期 {len(drop)} 条）")


if __name__ == "__main__":
    sys.exit(main())
