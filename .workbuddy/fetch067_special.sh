#!/bin/bash
# 067 期专用核验：066 期「下一轮强制动作」+ 本期新发布一手（并行版）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_067_s
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  if [ ! -f "$D/$name" ]; then : > "$D/$name"; fi
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
export -f fetch_one
export UA D
cat > $D/list.txt <<'EOF'
or_models.json|https://openrouter.ai/api/v1/models
or_free.json|https://openrouter.ai/api/v1/models?max_price=0
claude_pricing.html|https://claude.com/pricing
anth_promo.html|https://support.claude.com/en/articles/17506594
aihot_free_tokens.html|https://aihot.news/free-tokens
aihot_home.html|https://aihot.news/
amd_modelapis.html|https://developer.amd.com.cn/radeon/modelapis
amd_tokenfactory.html|https://developer.amd.com.cn/radeon/tokenfactory
opencode_zen.html|https://opencode.ai/docs/zen
hf_author_thinkingmachines.json|https://hf-mirror.com/api/models?author=thinkingmachines&limit=100
hf_author_ricursive.json|https://hf-mirror.com/api/models?author=ricursiveAI&limit=100
hf_kimi_pro.json|https://hf-mirror.com/api/models/moonshotai/Kimi-K3.1-Pro
hf_ripple.json|https://hf-mirror.com/api/models/ricursiveAI/Ripple-65B-Preview
hf_ernie_fp8.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base
hf_ernie_bf16.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base-BF16
hf_ernie_license.txt|https://hf-mirror.com/baidu/ERNIE-5.5-Flash-Base/raw/main/LICENSE
hf_author_baidu.json|https://hf-mirror.com/api/models?author=baidu&limit=200
hf_author_tencent.json|https://hf-mirror.com/api/models?author=tencent&limit=200
runware_pricing.html|https://runware.ai/pricing
freellm.html|https://freellm.net/
axon.html|https://jrabbass.github.io/axon/
sensenova_token.html|https://www.sensenova.cn/token-plan
xxh_pricing.html|https://xiaohuanxiong.com/pricing
sensetime_news.html|https://www.sensetime.com/cn/news
ollie_farewell.html|https://ollie.ai/farewell
ollie_pricing.html|https://ollie.ai/pricing
ollie_home.html|https://ollie.ai/
ag_home.html|https://antigravity.google/
ag_pricing.html|https://antigravity.google/pricing
ag_models.html|https://antigravity.google/models
doubao_work.html|https://www.volcengine.com/product/doubao-work
doubao_site.html|https://www.doubao.com/work
volc_doubao_pricing.html|https://www.volcengine.com/docs/82379/1099320
hunyuan.html|https://hunyuan.tencent.com/
scnet.html|https://www.scnet.cn/
mistral_news.html|https://mistral.ai/news
xai_news.html|https://x.ai/news
reflection_pricing.html|https://platform.reflection.ai/pricing
openai_models_docs.html|https://platform.openai.com/docs/models
opera_webai.html|https://next.opera.com/web-ai/
somark_rules.md|https://docs.somark.ai/free-tier-rules.md
meta_blog.html|https://ai.meta.com/blog/
ernie_release.html|https://ernie.baidu.com/zh/release/ernie-5-5-flash-preview/
openai_veterans.html|https://openai.com/index/chatgpt-plus-for-veterans/
or_ernie.json|https://openrouter.ai/api/v1/models?search=ernie
hf_search_ernie_preview.json|https://hf-mirror.com/api/models?search=ERNIE-5.5-Flash-Preview&limit=50
EOF
cat $D/list.txt | xargs -P 12 -I{} bash -c 'IFS="|" read -r n u <<< "{}"; fetch_one "$n" "$u"'
echo "DONE 067 special"
