#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
# Moonshot 文档列表（找 K2 停新公告）
fetch_one moonshot_docs.html "https://platform.moonshot.cn/docs"
fetch_one moonshot_guide.html "https://platform.moonshot.cn/docs/guide/start/model-overview"
fetch_one moonshot_pricing2.html "https://platform.moonshot.cn/docs/pricing/chat"
fetch_one kimi_docs.html "https://platform.kimi.com/docs"
fetch_one kimi_docs2.html "https://platform.kimi.com/docs/pricing/chat"
# Mistral commits（看 README 何时改）
fetch_one hf_mistral_commits2.json "https://hf-mirror.com/api/models/mistralai/Mistral-Large-4-1T-A52B/commits/main"
# Anthropic S-1
fetch_one sec_anthropic2.json "https://data.sec.gov/submissions/CIK0002130357.json"
# freellm provider 页
fetch_one freellm_or4.html "https://freellm.net/providers/openrouter"
# OXR changelog
fetch_one oxr_changelog2.html "https://docs.somark.cn/changelog"
echo DONE-054-deep7
