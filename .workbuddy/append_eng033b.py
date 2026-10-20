import io

ADD = """
### 033 期发布归档时补记 · 第 4 条（行尾 / EOL）

- ⚠️ **`.workbuddy/memory/` 下的 md 全部是 LF；追加内容时必须用二进制模式写，否则整个文件变 CRLF**：
  033 期归档时用了会在 Windows 下做 `\\n → \\r\\n` 转换的追加方式，后果分三种 ——
  · `ENGINEERING.md` 278 → 295 行 **全部**变 CRLF；
  · `automations/<id>/memory.md` 1073 → 1108 行 **全部**变 CRLF；
  · `2026-10-12.md` 只有新增的 43 行是 CRLF（**混合行尾**，最难看出来）。
  **症状**：`git diff --stat` 显示 **1446 插入 / 1351 删除（≈ 全文件重写）**，而真实新增只有 **95 行** —— **相差近 30 倍**。
  **「一次记忆归档 commit 显示几千行变化」就是这个原因，不要误判成内容被重写或历史丢失。**
- **诊断一行命令**：`git diff --ignore-cr-at-eol --stat` —— 若数字骤降到几十行，即为**纯行尾差异**。
  **不要用 `grep -c $'\\r'` 判断行尾**：Git Bash 下 `$'\\r'` 被当成空模式，**结果恒等于总行数**（033 期据此误判过一轮）。
  正确做法是用 Python：`open(f,'rb').read().count(13)`。
- **修法**：`raw = open(f,'rb').read(); open(f,'wb').write(raw.replace(b'\\r\\n', b'\\n'))`。
  **本仓库 `.gitattributes` 不存在、`core.autocrlf=false`** → git 不会自动归一，**只能靠自己**。
  **今后纪律：追加记忆前先断言 `raw.count(13) == 0`，追加后再断言一次。**
"""

with io.open('.workbuddy/memory/ENGINEERING.md', 'ab') as fh:
    fh.write(ADD.encode('utf-8'))

raw = open('.workbuddy/memory/ENGINEERING.md', 'rb').read()
print('ENGINEERING.md now: bytes=%d CR=%d LF=%d' % (len(raw), raw.count(13), raw.count(10)))
