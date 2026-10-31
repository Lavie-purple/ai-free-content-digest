#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
# MiniMax H3 许可证（Open-H3-Regenerate-2K 的 license_link）
fetch_one h3_license.md "https://hf-mirror.com/MiniMaxAI/MiniMax-H3/raw/main/LICENSE"
fetch_one h3_readme.md "https://hf-mirror.com/MiniMaxAI/MiniMax-H3/raw/main/README.md"
fetch_one h3_api.json "https://hf-mirror.com/api/models/MiniMaxAI/MiniMax-H3"
# OpenAI 订阅送 API credits 官方页候选
fetch_one oai_credits1.html "https://help.openai.com/en/articles/11369540"
fetch_one oai_credits2.html "https://openai.com/index/chatgpt-api-credits/"
fetch_one oai_credits3.html "https://help.openai.com/en/articles/6825453-chatgpt-release-notes"
# Anthropic 官方 news 是否有关于 Ultra 的公告（已是 404，保留）
# aihot.news 本期复访
fetch_one aihot_news3.html "https://aihot.news/"
# 智元官方 Worken 新闻页
fetch_one agibot_worken.html "https://www.agibot.com/news"
echo DONE-054-final
