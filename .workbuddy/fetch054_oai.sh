#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
fetch_one oai_help_credits2.html "https://help.openai.com/en/articles/11487787"
fetch_one oai_credits_api.html "https://help.openai.com/en/articles/8264777-what-is-the-chatgpt-plus-plan"
fetch_one oai_pricing_biz.html "https://openai.com/business/pricing/"
fetch_one chatgpt_pricing2.html "https://chatgpt.com/pricing/"
fetch_one oai_api_pricing2.html "https://platform.openai.com/docs/pricing"
echo DONE-054-oai
