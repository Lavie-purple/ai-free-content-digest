# -*- coding: utf-8 -*-
"""工具链统一入口：一把跑完编译 / 测量 / 校验 / 截图，并把输出以 UTF-8 落盘。

为什么需要它
------------
在 PowerShell 里用 `> log` 或 `Set-Content` 捕获 Python 的 stdout，会先把 UTF-8
字节按 GBK 解码、再按目标编码写回——日志里的中文全是乱码，等于没法读。
让 Python 自己 subprocess 捕获、自己写 UTF-8 文件，就绕开了这一层转换。

用法：
    python .workbuddy/run_all.py                     # 默认一把跑完出刊所需全部
                                                     # build + probe + verify + index + indexmd + fresh
    python .workbuddy/run_all.py build probe verify snap
    python .workbuddy/run_all.py index indexmd fresh # 站点首页与新鲜度守卫
日志落在 .workbuddy/_shot/_<任务名>.log（该目录已被 .gitignore 忽略）。

⚠️ 2026-09-19：默认任务里**必须有 index 与 fresh**。008 期就是默认只跑
   build/probe/verify 时漏掉了 index，导致站点首页卡在 007 期一天。
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
SHOT = os.path.join(HERE, "_shot")
PY = sys.executable

JOBS = {
    "build": [os.path.join(HERE, "build_web.py")],
    "probe": [os.path.join(HERE, "probe_mobile.py")],
    "verify": [os.path.join(HERE, "verify_web.py")],
    "layout": [os.path.join(HERE, "probe_layout.py"), "--widths", "1440,1024"],
    "color": [os.path.join(HERE, "audit_color.py")],
    "index": [os.path.join(HERE, "build_index_web.py")],
    "indexmd": [os.path.join(HERE, "build_index.py")],
    "fresh": [os.path.join(HERE, "check_site_freshness.py")],
    "indexprobe": [os.path.join(HERE, "probe_mobile.py"),
                   os.path.join(WS, "index.html"), "--out",
                   os.path.join(SHOT, "mobile_probe_index.txt")],
    "snap": [os.path.join(HERE, "snap_mobile.py")],
}

names = sys.argv[1:] or ["build", "probe", "verify", "index", "indexmd", "fresh"]
for name in names:
    if name not in JOBS:
        print("跳过未知任务 %s" % name)
        continue
    r = subprocess.run([PY] + JOBS[name], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=WS)
    p = os.path.join(SHOT, "_%s.log" % name)
    with open(p, "w", encoding="utf-8") as f:
        f.write((r.stdout or "") + (r.stderr or ""))
    print("%-10s -> _%s.log  rc=%d  %d chars" % (name, name, r.returncode, len(r.stdout or "")))
