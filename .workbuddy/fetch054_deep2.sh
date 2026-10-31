#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
# OXR 官方一手
fetch_one oxr_gh.html "https://github.com/SoMarkAI/OXR"
fetch_one oxr_hf.json "https://hf-mirror.com/api/models?author=SoMarkAI&limit=50&sort=createdAt&direction=-1"
fetch_one oxr_hf_search.json "https://hf-mirror.com/api/models?search=OXR&limit=30"
fetch_one oxr_free.html "https://free-oxr.somark.cn/"
fetch_one oxr_api.html "https://free-oxr.somark.cn/api/v1"
fetch_one oxr_site.html "https://www.somark.cn/"
fetch_one oxr_hf_page.html "https://hf-mirror.com/SoMarkAI/OXR-1.0"
fetch_one oxr_readme.md "https://hf-mirror.com/SoMarkAI/OXR-1.0/raw/main/README.md"
fetch_one oxr_license.md "https://hf-mirror.com/SoMarkAI/OXR-1.0/raw/main/LICENSE"
# Open-H3-Regenerate-2K 官方一手
fetch_one h3reg_hf.json "https://hf-mirror.com/api/models?search=Open-H3-Regenerate&limit=30"
fetch_one h3reg_gh.html "https://github.com/NVlabs/Sana"
fetch_one sana_hf.json "https://hf-mirror.com/api/models?search=Regenerate-2K&limit=30"
# Anthropic 官方订阅公告
fetch_one anth_support.html "https://support.anthropic.com/en/articles/9797557-usage-limit-FAQ"
fetch_one anth_news.html "https://www.anthropic.com/news"
fetch_one anth_pricing.html "https://www.anthropic.com/pricing"
fetch_one claude_pricing.html "https://claude.ai/pricing"
# OpenAI robots.txt 训练偏好
fetch_one oai_train_prefs2.html "https://openai.com/index/helping-websites-express-ai-training-preferences"
echo DONE-054-deep2
