#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
fetch_one or_ann.html "https://openrouter.ai/announcements"
fetch_one aihot_api.html "https://aihot.news/api/v1/items?limit=30"
fetch_one oxr_gh_readme.md "https://raw.githubusercontent.com/SoMarkAI/OXR/main/LICENSE"
fetch_one h3reg_gh_api.json "https://api.github.com/repos/NVlabs/Sana"
echo DONE-054-last
