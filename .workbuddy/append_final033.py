import io
import subprocess
import time

AUTO = '.workbuddy/memory/automations/256c1349-ea4a-4721-9c5d-14067699f1f1/memory.md'
DAILY = '.workbuddy/memory/2026-10-12.md'

stamp = time.strftime('%Y-%m-%d %H:%M')

AUTO_ADD = r"""
**记忆归档（本轮收官）**：commit **`3cfb2bf`**（**只含 `.workbuddy/memory/` 三件套 · 111 insertions**）
→ push **`4628c6e..3cfb2bf`**（**内联凭据助手第十次生效**，token len=40）；
**远端 API sha 与本地 HEAD 逐字一致**、`pages/builds/latest` → **`built 3cfb2bf`**、
**线上 `index.html` 31,621 B 与 033 单期页 232,551 B 仍与本地 `cmp` 逐字节一致、首页仍显示「第 033 期」** ——
**证明「只动 `.workbuddy/memory/` 的 commit」不会破坏站点产物**（这条本轮首次实测）。

**⚠️ 归档时发现并修复：记忆文件被写成 CRLF（第 4 条工程教训的由来）** ——
`ENGINEERING.md`（278→295 行全部）、automem（1073→1108 行全部）、当日日志（**只有新增的 43 行**）都变成 CRLF，
`git diff --stat` 因此显示 **1446 插入 / 1351 删除**，**与真实新增 95 行相差近 30 倍**。
**诊断**：`git diff --ignore-cr-at-eol --stat`（数字骤降到 95 行即证）。
**教训**：`.workbuddy/memory/` 下 md 全是 LF，**追加必须二进制模式 `'ab'` + `raw.count(13)==0` 断言**。
"""

DAILY_ADD = "\n## 记忆归档（" + stamp + " · 本轮第 33 期收官）\n\n" + r"""- commit **`3cfb2bf`**：`.workbuddy/memory/` 三件套（当日日志 43 行 / `ENGINEERING.md` 33 行 / 自动化 memory 35 行），共 **111 insertions**。
- push **`4628c6e..3cfb2bf`**（内联凭据助手第十次生效，token len=40）；**远端 API sha 与本地 HEAD 一致**。
- `pages/builds/latest` 轮询 2 次 → **`built 3cfb2bf`**；**线上 `index.html`（31,621 B）与第 033 期单期页（232,551 B）均与本地 `cmp` 逐字节一致**，首页仍显示「第 033 期」
  —— **只改 `.workbuddy/memory/` 的提交不会影响站点产物**（本轮首次实测，可写进流程认知）。
- **归档过程中发现并修复：三个记忆文件被写成了 CRLF** —— `ENGINEERING.md` 与 automem **整个文件**变 CRLF、当日日志 **只有新增的 43 行**变 CRLF（混合行尾最难发现）。
  `git diff --stat` 显示 **1446 插入 / 1351 删除 / 2797 行变化**，而真实新增只有 **95 行**。
  诊断命令：`git diff --ignore-cr-at-eol --stat`；**不要用 `grep -c` 配 `$'\r'` 判断**（Git Bash 下结果恒等于总行数，本轮据此误判过一轮）。
  修法：`raw.replace(b'\r\n', b'\n')` 后以 `'wb'` 写回。**已作为 033 期第 4 条工程教训入档 `ENGINEERING.md`。**
"""

with io.open(AUTO, 'ab') as fh:
    fh.write(AUTO_ADD.encode('utf-8'))
with io.open(DAILY, 'ab') as fh:
    fh.write(DAILY_ADD.encode('utf-8'))

for p in (AUTO, DAILY):
    raw = open(p, 'rb').read()
    print('%-70s bytes=%d CR=%d LF=%d' % (p, len(raw), raw.count(13), raw.count(10)))
