#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
fetch_one fk_repo_api.json "https://api.github.com/repos/OpenBMB/ForgeKernel"
fetch_one fk_readme.md "https://raw.githubusercontent.com/OpenBMB/ForgeKernel/main/README.md"
fetch_one fk_page.html "https://github.com/OpenBMB/ForgeKernel"
fetch_one h3reg_page2.html "https://nvlabs.github.io/Sana/Open-H3-Regenerate-2K/"
fetch_one agibot_2.html "https://www.agibot.com/news/1"
fetch_one openatom_oxr.html "https://www.openatom.org/"
echo DONE-054-deep8
