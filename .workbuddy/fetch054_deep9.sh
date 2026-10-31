#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
fetch_one chatgpt_pricing.html "https://chatgpt.com/pricing"
fetch_one anthropic_support_max.html "https://support.claude.com/en/articles/11049741-what-is-the-max-plan"
fetch_one anthropic_ultra_help.html "https://support.claude.com/en/articles/12622548-claude-ultra"
fetch_one openai_codex_pricing.html "https://openai.com/codex/pricing"
fetch_one gblog_ai3.html "https://blog.google/technology/ai/"
fetch_one deepmind3.html "https://deepmind.google/discover/blog/"
fetch_one aistudio3.html "https://aistudio.google.com/"
fetch_one ai_google_dev.html "https://ai.google.dev/gemini-api/docs/pricing"
fetch_one scnet3.html "https://www.scnet.cn/index.html"
echo DONE-054-deep9
