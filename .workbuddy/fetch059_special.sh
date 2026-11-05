#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_059_s
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
fetch_one kimi_k31_quickstart.html "https://platform.moonshot.cn/docs/guide/kimi-k3-1-pro-quickstart"
fetch_one ag_pricing.html "https://antigravity.google/pricing"
fetch_one ag_plans.html "https://antigravity.google/docs/plans"
fetch_one ag_models.html "https://antigravity.google/models"
fetch_one ollie_farewell.html "https://ollie.ai/farewell"
fetch_one ollie_pricing.html "https://ollie.ai/pricing"
fetch_one sensenova_token.html "https://www.sensenova.cn/token-plan"
fetch_one xxh_pricing.html "https://xiaohuanxiong.com/pricing"
fetch_one sensetime_news.html "https://www.sensetime.com/cn/news"
fetch_one axon.html "https://jrabbass.github.io/axon/"
fetch_one crouton_llms.txt "https://openrouter.ai/stealth/crouton-alpha/llms.txt"
fetch_one crouton_page.html "https://openrouter.ai/stealth/crouton-alpha"
fetch_one gh_moonshot_repos.json "https://api.github.com/orgs/MoonshotAI/repos"
fetch_one gh_kimi_k3_releases.json "https://api.github.com/repos/MoonshotAI/Kimi-K3/releases"
fetch_one hf_search_k31.json "https://huggingface.co/api/models?search=Kimi-K3.1&limit=20"
fetch_one somark_rules.md "https://docs.somark.ai/free-tier-rules.md"
fetch_one mistral_news.html "https://mistral.ai/news"
fetch_one tencent_hunyuan_doc.html "https://cloud.tencent.com/document/product/1729"
fetch_one xai_news.html "https://x.ai/news"
fetch_one or_models.json "https://openrouter.ai/api/v1/models"
echo "DONE 059S"
