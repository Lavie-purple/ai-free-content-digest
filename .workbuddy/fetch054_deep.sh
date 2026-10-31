#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
mkdir -p $D
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
# 量子位窗口内七篇
fetch_one qb_claude5h.html "https://www.qbitai.com/2026/10/506855.html"
fetch_one qb_nv_minimax.html "https://www.qbitai.com/2026/10/506743.html"
fetch_one qb_oxr.html "https://www.qbitai.com/2026/10/506686.html"
fetch_one qb_opr.html "https://www.qbitai.com/2026/10/506785.html"
fetch_one qb_baidu.html "https://www.qbitai.com/2026/10/506771.html"
fetch_one qb_zhiyuan.html "https://www.qbitai.com/2026/10/506819.html"
fetch_one qb_chip.html "https://www.qbitai.com/2026/10/506866.html"
# OpenAI 官方三条（窗口内）
fetch_one oai_train_prefs.html "https://openai.com/index/making-it-easier-for-websites-to-express-ai-training-preferences/"
fetch_one oai_teen_safety.html "https://openai.com/index/community-safety-report-and-new-protections-for-teens/"
fetch_one oai_fairuse.html "https://openai.com/index/fair-use-benefits-everyone/"
fetch_one oai_news_rss3.xml "https://openai.com/news/rss.xml"
# InfoQ 无限 Token 那条
fetch_one infoq_inf_token.html "https://www.infoq.cn/article/2026_10_31"
# The Decoder GLM 5.3 漏洞链
fetch_one dec_glm_exploit.html "https://the-decoder.com/open-weight-model-glm-5-3-built-full-firefox-exploit-chains-with-zero-human-input-in-under-48-hours/"
# Simon Willison API credits
fetch_one simon_api_credits.html "https://simonwillison.net/2026/Oct/30/api-credits-benefit-for-eligible-chatgpt-subscriptions/"
# TechCrunch Ollie 关停
fetch_one tc_ollie.html "https://techcrunch.com/2026/10/30/ollie-a-privacy-focused-ai-assistant-is-shutting-down/"
# 智元 / 联想天禧 / Apple Intelligence
fetch_one qb_lenovo.html "https://www.qbitai.com/2026/10/506866.html"
# Claude Code 恶意扩展
fetch_one dec_cursor_ext.html "https://the-decoder.com/malicious-claude-code-extension-in-cursors-marketplace-attempted-remote-access-and-data-theft/"
echo DONE-054-deep
