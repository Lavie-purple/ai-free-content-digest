# -*- coding: utf-8 -*-
"""逐表核对 md 表格列数：每行竖线个数必须与分隔行一致。"""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent

def count_cols(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return len(s.split("|"))

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    if src:
        p = root / src
    else:
        cands = sorted(root.glob("AI免费内容与权益速递-第*期-*.md"), key=lambda x: x.name)
        p = cands[-1]
    print("核对文件:", p.name)
    lines = p.read_text(encoding="utf-8").splitlines()

    tables = 0
    bad = 0
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines):
            sep = lines[i + 1].strip()
            if re.fullmatch(r"\|[\s:\-\|]+\|", sep):
                tables += 1
                ncol = count_cols(sep)
                hdr = count_cols(lines[i])
                rows = 0
                j = i
                issues = []
                if hdr != ncol:
                    issues.append("表头 %d 列 != 分隔行 %d 列" % (hdr, ncol))
                while j < len(lines) and lines[j].strip().startswith("|"):
                    if j != i + 1:
                        c = count_cols(lines[j])
                        rows += 1
                        if c != ncol:
                            issues.append("第 %d 行 %d 列 (应 %d)" % (j + 1, c, ncol))
                    j += 1
                status = "OK" if not issues else "异常"
                if issues:
                    bad += 1
                print("  表%-3d 行%-5d %2d 列  %s  %s" % (tables, rows, ncol, status, "; ".join(issues[:4])))
                i = j
                continue
        i += 1

    # 避坑编号连续性
    nums = []
    for ln in lines:
        m = re.match(r"^(\d{1,3})\.\s*⚠️", ln.strip())
        if m:
            nums.append(int(m.group(1)))
    if nums:
        exp = list(range(nums[0], nums[0] + len(nums)))
        print("避坑编号:", nums[0], "-", nums[-1], "连续" if nums == exp else "不连续! " + str(nums))

    print("表格合计 %d 个，异常 %d 个" % (tables, bad))
    print("VERDICT:", "ALL GREEN" if bad == 0 else "HAS ISSUES")
    return 0 if bad == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
