#!/bin/bash
# 062 期专用核验：061 期「下一轮强制动作」17 条 + 目录 diff 一手
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_062_s
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  if [ "$code" = "000" ] && [ ! -f "$D/$name" ]; then : > "$D/$name"; fi
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
# ① AI-HOT 结构化（<article>）
fetch_one ai_hot.html                  "https://aihot.news/"
# ② Inkling 2 Small 是否放权重
fetch_one hf_author_thinkingmachines.json "https://hf-mirror.com/api/models?author=thinkingmachines&limit=100"
fetch_one hf_search_inkling2.json      "https://hf-mirror.com/api/models?search=Inkling-2&limit=20"
fetch_one tinker.html                  "https://thinkingmachines.ai/tinker/"
# ③④ 免费档端点与条款
fetch_one or_models.json               "https://openrouter.ai/api/v1/models"
fetch_one or_free.json                 "https://openrouter.ai/api/v1/models?max_price=0"
fetch_one lfm_free_endpoints.json      "https://openrouter.ai/api/v1/models/liquid/lfm-3-1.7b:free/endpoints"
fetch_one lfm_free_llms.txt            "https://openrouter.ai/liquid/lfm-3-1.7b:free/llms.txt"
fetch_one nemotron_safety_endpoints.json "https://openrouter.ai/api/v1/models/nvidia/nemotron-3.5-content-safety:free/endpoints"
fetch_one nemotron_safety_llms.txt     "https://openrouter.ai/nvidia/nemotron-3.5-content-safety:free/llms.txt"
# ⑤⑥ crouton / OpenCode / iceman
fetch_one crouton_llms.txt             "https://openrouter.ai/stealth/crouton-alpha/llms.txt"
fetch_one crouton_page.html            "https://openrouter.ai/stealth/crouton-alpha"
fetch_one opencode_zen.html            "https://opencode.ai/docs/zen"
# ⑦ Runware
fetch_one runware_pricing.html         "https://runware.ai/pricing"
# ⑧ Ripple-65B 与两个变体
fetch_one hf_ripple.json               "https://hf-mirror.com/api/models/ricursiveAI/Ripple-65B-Preview"
fetch_one hf_author_ricursive.json     "https://hf-mirror.com/api/models?author=ricursiveAI&limit=100"
fetch_one ripple_site.html             "https://ricursive.com/ripple"
# ⑨ 豆包工作
fetch_one doubao_work.html             "https://www.volcengine.com/product/doubao-work"
fetch_one doubao_site.html             "https://www.doubao.com/work"
# ⑩ Ollie
fetch_one ollie_farewell.html          "https://ollie.ai/farewell"
fetch_one ollie_pricing.html           "https://ollie.ai/pricing"
fetch_one ollie_home.html              "https://ollie.ai/"
# ⑪ Antigravity
fetch_one ag_pricing.html              "https://antigravity.google/pricing"
fetch_one ag_models.html               "https://antigravity.google/models"
fetch_one ag_docs_plans.html           "https://antigravity.google/docs/plans"
# ⑫ 商汤
fetch_one sensenova_token.html         "https://www.sensenova.cn/token-plan"
fetch_one xxh_pricing.html             "https://xiaohuanxiong.com/pricing"
fetch_one sensetime_news.html          "https://www.sensetime.com/cn/news"
# ⑬ AXON
fetch_one axon.html                    "https://jrabbass.github.io/axon/"
# ⑭ freellm
fetch_one freellm.html                 "https://freellm.net/"
# ⑮ 老混元 / 超算 / AutoClaw
fetch_one hunyuan.html                 "https://hunyuan.tencent.com/"
fetch_one scnet.html                   "https://www.scnet.cn/"
fetch_one autoclaw_cn.html             "https://autoclaw.zhipuai.cn/blog/news"
fetch_one autoclaw_intl.html           "https://autoclaw.z.ai/blog/news/"
# ⑯ 受阻复测
fetch_one mistral_news.html            "https://mistral.ai/news"
fetch_one xai_news.html                "https://x.ai/news"
fetch_one reflection_pricing.html      "https://platform.reflection.ai/pricing"
fetch_one openai_models_docs.html      "https://platform.openai.com/docs/models"
fetch_one opera_webai.html             "https://next.opera.com/web-ai/"
fetch_one somark_rules.md              "https://docs.somark.ai/free-tier-rules.md"
# ERNIE / Kimi / Hy4 存量复核
fetch_one hf_ernie_fp8.json            "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base"
fetch_one hf_ernie_bf16.json           "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base-BF16"
fetch_one hf_ernie_license.txt         "https://hf-mirror.com/baidu/ERNIE-5.5-Flash-Base/raw/main/LICENSE"
fetch_one hf_search_highspeed.json     "https://hf-mirror.com/api/models?search=Kimi-K3.1-Highspeed&limit=20"
fetch_one hf_hy4.json                  "https://hf-mirror.com/api/models/tencent/Hy4"
# 新发布候选
fetch_one hf_new_models.json           "https://hf-mirror.com/api/models?sort=createdAt&direction=-1&limit=80"
fetch_one hf_trending_models.json      "https://hf-mirror.com/api/models?sort=trendingScore&direction=-1&limit=60"
fetch_one gh_trending.html             "https://github.com/trending"
fetch_one hn_front.html                "https://news.ycombinator.com/"
echo "DONE 062S"
