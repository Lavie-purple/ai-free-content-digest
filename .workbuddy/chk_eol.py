import subprocess

files = [
    '.workbuddy/memory/2026-10-12.md',
    '.workbuddy/memory/ENGINEERING.md',
    '.workbuddy/memory/automations/256c1349-ea4a-4721-9c5d-14067699f1f1/memory.md',
    '.workbuddy/memory/MEMORY.md',
]

for f in files:
    raw = open(f, 'rb').read()
    head = subprocess.run(['git', 'show', 'HEAD:' + f], capture_output=True).stdout
    print(f)
    print('   work : bytes=%d CR=%d LF=%d' % (len(raw), raw.count(13), raw.count(10)))
    print('   HEAD : bytes=%d CR=%d LF=%d' % (len(head), head.count(13), head.count(10)))
