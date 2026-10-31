#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
fetch_one kimi_model_list.html "https://platform.moonshot.cn/docs/api/models"
fetch_one kimi_models2.html "https://platform.kimi.com/docs/guide/models"
fetch_one moonshot_home.html "https://platform.moonshot.cn/"
fetch_one moonshot_changelog.html "https://platform.moonshot.cn/docs/changelog"
fetch_one kimi_api_models.html "https://api.moonshot.cn/v1/models"
fetch_one moonshot_k2_pricing.html "https://platform.moonshot.cn/docs/pricing/chat"
fetch_one moonshot_k2b.html "https://platform.moonshot.cn/docs/guide/kimi-k2-thinking-deprecation"
echo DONE-054-k2
