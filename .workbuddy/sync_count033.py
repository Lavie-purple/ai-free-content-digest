ENG = '.workbuddy/memory/ENGINEERING.md'
AUTO = '.workbuddy/memory/automations/256c1349-ea4a-4721-9c5d-14067699f1f1/memory.md'


def rep(path, old, new):
    raw = open(path, 'rb').read()
    ob, nb = old.encode('utf-8'), new.encode('utf-8')
    n = raw.count(ob)
    assert n == 1, 'hit %d for %r' % (n, old[:40])
    raw = raw.replace(ob, nb)
    open(path, 'wb').write(raw)
    assert raw.count(13) == 0, 'CRLF leaked into ' + path
    print('OK %s' % path)


rep(ENG,
    '### 033 期新增三条工程教训（2026-10-12 · 同日第二轮）',
    '### 033 期新增四条工程教训（2026-10-12 · 同日第二轮）')

rep(ENG,
    '### 033 期发布归档时补记 · 第 4 条（行尾 / EOL）',
    '### 033 期第 4 条（发布归档时发现 · 行尾 / EOL）')

rep(AUTO,
    '**\u26a0\ufe0f \u672c\u8f6e\u4e09\u6761\u65b0\u5de5\u7a0b\u6559\u8bad\uff08\u5df2\u8fdb `ENGINEERING.md`\uff09**',
    '**\u26a0\ufe0f \u672c\u8f6e\u56db\u6761\u65b0\u5de5\u7a0b\u6559\u8bad\uff08\u5df2\u8fdb `ENGINEERING.md`\uff09**')

TAIL = ("\u2463 \u672c\u5de5\u4f5c\u533a `.workbuddy/memory/` \u4e0b\u7684 md \u5168\u662f LF \u2014\u2014 "
        "\u8ffd\u52a0\u5fc5\u987b\u7528\u4e8c\u8fdb\u5236\u6a21\u5f0f\uff0c\u5426\u5219\u6574\u4e2a\u6587\u4ef6\u53d8 CRLF"
        "\uff08\u672c\u671f\u5df2\u4e2d\uff1aENGINEERING 295 \u884c\u5168 CRLF\u3001automem 1108 \u884c\u5168 CRLF\u3001"
        "\u65e5\u5fd7\u65b0\u589e 43 \u884c CRLF\uff09\uff0c`git diff --stat` \u4f1a\u663e\u793a "
        "**1446 \u63d2\u5165 / 1351 \u5220\u9664 \u2248 \u5168\u6587\u4ef6\u91cd\u5199**\uff0c"
        "**\u800c\u771f\u5b9e\u65b0\u589e\u53ea\u6709 95 \u884c\uff08\u76f8\u5dee\u8fd1 30 \u500d\uff09**\uff1b"
        "**\u8bca\u65ad\u7528 `git diff --ignore-cr-at-eol --stat`**\uff08\u6570\u5b57\u9aa4\u964d\u5373\u4e3a\u7eaf\u884c\u5c3e\u5dee\u5f02\uff09\uff0c"
        "**\u4e0d\u8981\u7528 grep -c \u914d $'\\r'**\uff08Git Bash \u4e0b\u6052\u7b49\u4e8e\u603b\u884c\u6570\uff0c\u672c\u671f\u636e\u6b64\u8bef\u5224\u8fc7\u4e00\u8f6e\uff09\uff0c"
        "**\u4fee\u6cd5\u662f replace(b'\\r\\n', b'\\n') \u540e\u4ee5 'wb' \u5199\u56de**\u3002")

rep(AUTO,
    '\uff08\u56de\u5199 234 \u800c\u975e 237\uff09\u3002',
    '\uff08\u56de\u5199 234 \u800c\u975e 237\uff09\uff1b' + TAIL)

for p in (ENG, AUTO):
    raw = open(p, 'rb').read()
    print('%-70s bytes=%d CR=%d LF=%d' % (p, len(raw), raw.count(13), raw.count(10)))
