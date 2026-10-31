#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
fetch_one oxr_commits.json "https://api.github.com/repos/SoMarkAI/OXR/commits?per_page=100"
fetch_one oxr_releases.json "https://api.github.com/repos/SoMarkAI/OXR/releases?per_page=20"
fetch_one oxr_tags.json "https://api.github.com/repos/SoMarkAI/OXR/tags?per_page=20"
fetch_one oxr_doc_free.html "https://docs.somark.cn/documentation/free-api"
fetch_one anth_pricing3.html "https://www.anthropic.com/pricing"
fetch_one anth_news2.html "https://www.anthropic.com/news"
echo DONE-054-deep4
