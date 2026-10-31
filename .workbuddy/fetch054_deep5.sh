#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
# Simon API credits（053 期窗口内漏登，本期补登候选）
fetch_one simon_api_credits3.html "https://simonwillison.net/2026/Oct/29/api-credits/"
# SoMark 官方更新日志（确认 Free API 上线时点）
fetch_one oxr_changelog.html "https://docs.somark.cn/changelog"
fetch_one oxr_docs_index.html "https://docs.somark.cn/llms.txt"
# OpenAI 官方 API credits 公告页候选
fetch_one oai_api_credits.html "https://openai.com/index/api-credits-for-chatgpt-subscriptions/"
fetch_one oai_pricing3.html "https://openai.com/api/pricing/"
# 百度搜索 AI API 官方页
fetch_one baidu_api.html "https://cloud.baidu.com/product/wenxinworkshop"
fetch_one baidu_search_api.html "https://ai.baidu.com/"
# 智元官方
fetch_one agibot_news.html "https://www.agibot.com/news"
fetch_one lingqu.html "https://www.openatom.org/"
echo DONE-054-deep5
