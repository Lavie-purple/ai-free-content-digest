#!/bin/bash
# 060 期专用核验：059 期「下一轮强制动作」五条 + 目录 diff 的一手反证
# ① Ollie 11/6 关停当天 ② Kimi K3.1 Pro 自定义许可 / Highspeed 权重
# ③ 两个 inkling:free 是否回归 ④ crouton 第4天 + OpenCode crouton-alpha-free
# ⑤ freellm 更新日 / Runware 促销 / Antigravity / 商汤 / 超算互联网 / 豆包工作
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_060_s
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  if [ "$code" = "000" ] && [ ! -f "$D/$name" ]; then : > "$D/$name"; fi
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
fetch_one ollie_farewell.html          "https://ollie.ai/farewell"
fetch_one ollie_pricing.html           "https://ollie.ai/pricing"
fetch_one ollie_home.html              "https://ollie.ai/"
fetch_one or_models.json               "https://openrouter.ai/api/v1/models"
fetch_one or_announcements.html        "https://openrouter.ai/announcements"
fetch_one inkling_free_llms.txt        "https://openrouter.ai/thinkingmachines/inkling:free/llms.txt"
fetch_one inkling_free_endpoints.json  "https://openrouter.ai/api/v1/models/thinkingmachines/inkling:free/endpoints"
fetch_one inklingsmall_free_llms.txt   "https://openrouter.ai/thinkingmachines/inkling-small:free/llms.txt"
fetch_one crouton_llms.txt             "https://openrouter.ai/stealth/crouton-alpha/llms.txt"
fetch_one crouton_page.html            "https://openrouter.ai/stealth/crouton-alpha"
fetch_one opencode_zen.html            "https://opencode.ai/docs/zen"
fetch_one hf_kimi_k31.json             "https://hf-mirror.com/api/models/moonshotai/Kimi-K3.1-Pro"
fetch_one hf_kimi_k31_license.txt      "https://hf-mirror.com/moonshotai/Kimi-K3.1-Pro/raw/main/LICENSE"
fetch_one hf_kimi_k31_readme.md        "https://hf-mirror.com/moonshotai/Kimi-K3.1-Pro/raw/main/README.md"
fetch_one hf_moonshot_list.json        "https://hf-mirror.com/api/models?author=moonshotai&limit=100"
fetch_one hf_search_highspeed.json     "https://hf-mirror.com/api/models?search=Kimi-K3.1-Highspeed&limit=20"
fetch_one kimi_k31_quickstart.html     "https://platform.moonshot.cn/docs/guide/kimi-k3-1-pro-quickstart"
fetch_one freellm.html                 "https://freellm.net/"
fetch_one freellm_models.html          "https://freellm.net/models"
fetch_one runware_pricing.html         "https://runware.ai/pricing"
fetch_one ag_pricing.html              "https://antigravity.google/pricing"
fetch_one ag_models.html               "https://antigravity.google/models"
fetch_one sensenova_token.html         "https://www.sensenova.cn/token-plan"
fetch_one xxh_pricing.html             "https://xiaohuanxiong.com/pricing"
fetch_one sensetime_news.html          "https://www.sensetime.com/cn/news"
fetch_one scnet.html                   "https://www.scnet.cn/"
fetch_one doubao_work.html             "https://www.volcengine.com/product/doubao-work"
fetch_one somark_rules.md              "https://docs.somark.ai/free-tier-rules.md"
fetch_one axon.html                    "https://jrabbass.github.io/axon/"
fetch_one autoclaw_cn.html             "https://autoclaw.zhipuai.cn/blog/news"
fetch_one autoclaw_intl.html           "https://autoclaw.z.ai/blog/news/"
fetch_one mistral_news.html            "https://mistral.ai/news"
fetch_one xai_news.html                "https://x.ai/news"
fetch_one ai_hot.html                  "https://aihot.news/"
echo "DONE 060S"
