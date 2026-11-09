#!/bin/bash
# 063 期专用核验：062 期「下一轮强制动作」16 条 + 目录 diff 一手
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_063_s
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  if [ ! -f "$D/$name" ]; then : > "$D/$name"; fi
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
# ① Inkling 2 Small 权重 / 上下文
fetch_one hf_author_thinkingmachines.json "https://hf-mirror.com/api/models?author=thinkingmachines&limit=100"
fetch_one hf_search_inkling2.json      "https://hf-mirror.com/api/models?search=Inkling-2&limit=20"
fetch_one tinker.html                  "https://thinkingmachines.ai/tinker/"
# ③④ OpenRouter / OpenCode 目录与免费档
fetch_one or_models.json               "https://openrouter.ai/api/v1/models"
fetch_one or_free.json                 "https://openrouter.ai/api/v1/models?max_price=0"
fetch_one opencode_zen.html            "https://opencode.ai/docs/zen"
fetch_one or_inception.json            "https://openrouter.ai/api/v1/models?search=inception"
fetch_one crouton_llms.txt             "https://openrouter.ai/stealth/crouton-alpha/llms.txt"
fetch_one crouton_page.html            "https://openrouter.ai/stealth/crouton-alpha"
# ⑤ Runware
fetch_one runware_pricing.html         "https://runware.ai/pricing"
# ⑥ freellm
fetch_one freellm.html                 "https://freellm.net/"
# ⑦ AXON
fetch_one axon.html                    "https://jrabbass.github.io/axon/"
# ⑧ 商汤
fetch_one sensenova_token.html         "https://www.sensenova.cn/token-plan"
fetch_one xxh_pricing.html             "https://xiaohuanxiong.com/pricing"
fetch_one sensetime_news.html          "https://www.sensetime.com/cn/news"
# ⑨ Ollie
fetch_one ollie_farewell.html          "https://ollie.ai/farewell"
fetch_one ollie_pricing.html           "https://ollie.ai/pricing"
fetch_one ollie_home.html              "https://ollie.ai/"
# ⑩ Antigravity
fetch_one ag_pricing.html              "https://antigravity.google/pricing"
fetch_one ag_models.html               "https://antigravity.google/models"
# ⑪ 豆包工作
fetch_one doubao_work.html             "https://www.volcengine.com/product/doubao-work"
fetch_one doubao_site.html             "https://www.doubao.com/work"
# ⑫ Kimi / Hy4
fetch_one hf_search_highspeed.json     "https://hf-mirror.com/api/models?search=Kimi-K3.1-Highspeed&limit=20"
fetch_one hf_hy4.json                  "https://hf-mirror.com/api/models/tencent/Hy4"
# ⑬ 老混元 / 超算 / AutoClaw
fetch_one hunyuan.html                 "https://hunyuan.tencent.com/"
fetch_one scnet.html                   "https://www.scnet.cn/"
fetch_one autoclaw_cn.html             "https://autoclaw.zhipuai.cn/blog/news"
fetch_one autoclaw_intl.html           "https://autoclaw.z.ai/blog/news/"
# ⑭ 受阻复测
fetch_one mistral_news.html            "https://mistral.ai/news"
fetch_one xai_news.html                "https://x.ai/news"
fetch_one reflection_pricing.html      "https://platform.reflection.ai/pricing"
fetch_one openai_models_docs.html      "https://platform.openai.com/docs/models"
fetch_one opera_webai.html             "https://next.opera.com/web-ai/"
fetch_one somark_rules.md              "https://docs.somark.ai/free-tier-rules.md"
# ERNIE / Ripple 存量复核
fetch_one hf_ernie_fp8.json            "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base"
fetch_one hf_ernie_bf16.json           "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base-BF16"
fetch_one hf_ernie_license.txt         "https://hf-mirror.com/baidu/ERNIE-5.5-Flash-Base/raw/main/LICENSE"
fetch_one hf_ripple.json               "https://hf-mirror.com/api/models/ricursiveAI/Ripple-65B-Preview"
fetch_one hf_author_ricursive.json     "https://hf-mirror.com/api/models?author=ricursiveAI&limit=100"
# 新品发现
fetch_one hf_new_models.json           "https://hf-mirror.com/api/models?sort=createdAt&direction=-1&limit=80"
fetch_one hf_trending_models.json      "https://hf-mirror.com/api/models?sort=trendingScore&direction=-1&limit=60"
fetch_one gh_trending.html             "https://github.com/trending"
fetch_one ai_hot.html                  "https://aihot.news/"
fetch_one hn_algolia_free.json         "https://hn.algolia.com/api/v1/search_by_date?query=free%20API%20LLM&tags=story&hitsPerPage=40"
echo "DONE 063S"
