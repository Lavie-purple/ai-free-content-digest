import sys,re,io,html
def text(p):
    s=io.open(p,encoding='utf-8',errors='replace').read()
    s=re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>',' ',s)
    s=re.sub(r'(?s)<[^>]+>',' ',s)
    s=html.unescape(s)
    s=re.sub(r'[ \t\u00a0]+',' ',s)
    return s
if __name__=='__main__':
    p=sys.argv[1]
    print(len(text(p).encode('utf-8')))
