#!/bin/bash
# 061 期专用核验：060 期「下一轮强制动作」16 条 + 目录 diff 一手
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_061_s
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  if [ "$code" = "000" ] && [ ! -f "$D/$name" ]; then : > "$D/$name"; fi
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
# ② Ollie 关停后续
fetch_one ollie_farewell.html          "https://ollie.ai/farewell"
fetch_one ollie_pricing.html           "https://ollie.ai/pricing"
fetch_one ollie_home.html              "https://ollie.ai/"
# 目录 diff
fetch_one or_models.json               "https://openrouter.ai/api/v1/models"
fetch_one or_free.json                 "https://openrouter.ai/api/v1/models?max_price=0"
fetch_one or_announcements.html        "https://openrouter.ai/announcements"
# ③ 两个 inkling:free
fetch_one inkling_free_llms.txt        "https://openrouter.ai/thinkingmachines/inkling:free/llms.txt"
fetch_one inkling_free_endpoints.json  "https://openrouter.ai/api/v1/models/thinkingmachines/inkling:free/endpoints"
fetch_one inklingsmall_free_llms.txt   "https://openrouter.ai/thinkingmachines/inkling-small:free/llms.txt"
fetch_one inklingsmall_free_endpoints.json "https://openrouter.ai/api/v1/models/thinkingmachines/inkling-small:free/endpoints"
# ④ crouton 第5天
fetch_one crouton_llms.txt             "https://openrouter.ai/stealth/crouton-alpha/llms.txt"
fetch_one crouton_page.html            "https://openrouter.ai/stealth/crouton-alpha"
fetch_one opencode_zen.html            "https://opencode.ai/docs/zen"
# ⑤ Runware
fetch_one runware_pricing.html         "https://runware.ai/pricing"
# ⑥ Kimi Highspeed + 许可复核
fetch_one hf_search_highspeed.json     "https://hf-mirror.com/api/models?search=Kimi-K3.1-Highspeed&limit=20"
fetch_one hf_kimi_k31.json             "https://hf-mirror.com/api/models/moonshotai/Kimi-K3.1-Pro"
fetch_one hf_kimi_k31_license.txt      "https://hf-mirror.com/moonshotai/Kimi-K3.1-Pro/raw/main/LICENSE"
# ⑦ ERNIE 首次复核
fetch_one hf_ernie_fp8.json            "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base"
fetch_one hf_ernie_bf16.json           "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base-BF16"
fetch_one hf_ernie_license.txt         "https://hf-mirror.com/baidu/ERNIE-5.5-Flash-Base/raw/main/LICENSE"
fetch_one hf_ernie_readme.md           "https://hf-mirror.com/baidu/ERNIE-5.5-Flash-Base/raw/main/README.md"
fetch_one ernie_release.html           "https://ernie.baidu.com/release/ernie-5-5-flash-base/"
# ⑧ tencent/hy4
fetch_one hf_hy4.json                  "https://hf-mirror.com/api/models/tencent/Hy4"
fetch_one hf_hy4_preview.json          "https://hf-mirror.com/api/models/tencent/Hy4-preview"
fetch_one hf_search_hy4.json           "https://hf-mirror.com/api/models?search=Hy4&limit=30"
# ⑨ AXON
fetch_one axon.html                    "https://jrabbass.github.io/axon/"
# ⑩ 商汤
fetch_one sensenova_token.html         "https://www.sensenova.cn/token-plan"
fetch_one xxh_pricing.html             "https://xiaohuanxiong.com/pricing"
fetch_one sensetime_news.html          "https://www.sensetime.com/cn/news"
# ⑪ freellm
fetch_one freellm.html                 "https://freellm.net/"
# ⑫ Antigravity
fetch_one ag_pricing.html              "https://antigravity.google/pricing"
fetch_one ag_models.html               "https://antigravity.google/models"
fetch_one ag_docs_plans.html           "https://antigravity.google/docs/plans"
# ⑭ 豆包工作 / 超算
fetch_one doubao_work.html             "https://www.volcengine.com/product/doubao-work"
fetch_one scnet.html                   "https://www.scnet.cn/"
# ⑮ 受阻复测
fetch_one mistral_news.html            "https://mistral.ai/news"
fetch_one xai_news.html                "https://x.ai/news"
fetch_one reflection_pricing.html      "https://platform.reflection.ai/pricing"
fetch_one openai_models_docs.html      "https://platform.openai.com/docs/models"
fetch_one opera_webai.html             "https://next.opera.com/web-ai/"
fetch_one somark_rules.md              "https://docs.somark.ai/free-tier-rules.md"
# 其他在册免费档复核
fetch_one autoclaw_cn.html             "https://autoclaw.zhipuai.cn/blog/news"
fetch_one autoclaw_intl.html           "https://autoclaw.z.ai/blog/news/"
fetch_one ai_hot.html                  "https://aihot.news/"
fetch_one aihot_virxact.html           "https://aihot.virxact.com/"
# 新发布候选：HF 近 24h 新模型 / 本周热门
fetch_one hf_new_models.json           "https://hf-mirror.com/api/models?sort=lastModified&direction=-1&limit=60"
fetch_one hf_trending_models.json      "https://hf-mirror.com/api/models?sort=trendingScore&direction=-1&limit=50"
fetch_one hf_papers.html               "https://huggingface.co/papers"
fetch_one gh_trending.html             "https://github.com/trending"
echo "DONE 061S"
