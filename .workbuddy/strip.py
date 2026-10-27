# -*- coding: utf-8 -*-
import io,re,sys,os
def strip(fn):
    try:
        h = io.open(fn, encoding="utf-8", errors="ignore").read()
    except Exception as e:
        return "ERR "+str(e)
    h = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?is)<br\s*/?>|</p>|</div>|</li>|</h[1-6]>|</tr>", "\n", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = h.replace("&nbsp;"," ").replace("&amp;","&").replace("&lt;","<").replace("&gt;",">").replace("&#39;","'").replace("&quot;",'"')
    h = re.sub(r"[ \t]+", " ", h)
    h = re.sub(r"\n\s*\n+", "\n", h)
    return h.strip()
if __name__ == "__main__":
    print(strip(sys.argv[1]))
