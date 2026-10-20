import subprocess

files = [
    '.workbuddy/memory/2026-10-12.md',
    '.workbuddy/memory/ENGINEERING.md',
    '.workbuddy/memory/automations/256c1349-ea4a-4721-9c5d-14067699f1f1/memory.md',
]

for f in files:
    raw = open(f, 'rb').read()
    fixed = raw.replace(b'\r\n', b'\n')
    if fixed != raw:
        open(f, 'wb').write(fixed)
        print('FIXED %s  %d -> %d bytes (CR removed: %d)' % (f, len(raw), len(fixed), raw.count(13)))
    else:
        print('CLEAN %s' % f)

print('--- verify vs HEAD (byte diff) ---')
for f in files:
    work = open(f, 'rb').read()
    head = subprocess.run(['git', 'show', 'HEAD:' + f], capture_output=True).stdout
    print('%-72s work=%d bytes CR=%d | added_lines=%d' % (
        f, len(work), work.count(13),
        len(work.split(b'\n')) - len(head.split(b'\n'))))
