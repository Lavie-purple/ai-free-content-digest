#!/bin/bash
# 065 期专用核验：063 期「下一轮强制动作」14 条 + 本期新发布一手
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_065_s
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  if [ ! -f "$D/$name" ]; then : > "$D/$name"; fi
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
# ① Token 羊毛 连续两期 + 日变化
fetch_one aihot_free_tokens.html       "https://aihot.news/free-tokens"
fetch_one aihot_home.html              "https://aihot.news/"
# ② AMD Token Factory
fetch_one amd_modelapis.html           "https://developer.amd.com.cn/radeon/modelapis"
fetch_one amd_tokenfactory.html        "https://developer.amd.com.cn/radeon/tokenfactory"
# ③④ OpenRouter / OpenCode
fetch_one or_models.json               "https://openrouter.ai/api/v1/models"
fetch_one or_free.json                 "https://openrouter.ai/api/v1/models?max_price=0"
fetch_one opencode_zen.html            "https://opencode.ai/docs/zen"
fetch_one hf_author_thinkingmachines.json "https://hf-mirror.com/api/models?author=thinkingmachines&limit=100"
# ⑤ Runware 促销数组
fetch_one runware_pricing.html         "https://runware.ai/pricing"
# ⑥ freellm
fetch_one freellm.html                 "https://freellm.net/"
# ⑦ AXON
fetch_one axon.html                    "https://jrabbass.github.io/axon/"
# ⑧ 商汤三页
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
# ⑬ 老混元 / 超算
fetch_one hunyuan.html                 "https://hunyuan.tencent.com/"
fetch_one scnet.html                   "https://www.scnet.cn/"
# ⑭ 受阻复测
fetch_one mistral_news.html            "https://mistral.ai/news"
fetch_one xai_news.html                "https://x.ai/news"
fetch_one reflection_pricing.html      "https://platform.reflection.ai/pricing"
fetch_one openai_models_docs.html      "https://platform.openai.com/docs/models"
fetch_one opera_webai.html             "https://next.opera.com/web-ai/"
fetch_one somark_rules.md              "https://docs.somark.ai/free-tier-rules.md"
# 存量复核
fetch_one hf_ernie_fp8.json            "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base"
fetch_one hf_ernie_bf16.json           "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base-BF16"
fetch_one hf_ernie_license.txt         "https://hf-mirror.com/baidu/ERNIE-5.5-Flash-Base/raw/main/LICENSE"
fetch_one hf_ripple.json               "https://hf-mirror.com/api/models/ricursiveAI/Ripple-65B-Preview"
fetch_one hf_author_ricursive.json     "https://hf-mirror.com/api/models?author=ricursiveAI&limit=100"
fetch_one crouton_llms.txt             "https://openrouter.ai/stealth/crouton-alpha/llms.txt"
# 本期新发布一手
fetch_one meta_blog.html               "https://ai.meta.com/blog/"
fetch_one hf_author_meta.json          "https://hf-mirror.com/api/models?author=meta-llama&limit=100&sort=createdAt&direction=-1"
fetch_one hf_search_muse.json          "https://hf-mirror.com/api/models?search=Muse-Ember&limit=30"
fetch_one seed_blog.html               "https://seed.bytedance.com/"
fetch_one aws_quick.html               "https://aws.amazon.com/blogs/machine-learning/"
fetch_one anth_fable.html              "https://www.anthropic.com/claude-fable-and-mythos-5-2"
fetch_one anth_promo.html              "https://support.claude.com/en/articles/17506594"
fetch_one claude_pricing.html          "https://claude.com/pricing"
fetch_one hf_new_models.json           "https://hf-mirror.com/api/models?sort=createdAt&direction=-1&limit=80"
fetch_one hf_trending_models.json      "https://hf-mirror.com/api/models?sort=trendingScore&direction=-1&limit=60"
fetch_one hn_algolia_free.json         "https://hn.algolia.com/api/v1/search_by_date?query=free%20tier%20LLM&tags=story&hitsPerPage=40"
echo "DONE 065S"
