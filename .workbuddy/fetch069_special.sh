#!/bin/bash
# 069 期专用核验：068 期「下一轮强制动作」14 条 + 本期新发布一手（并行版）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_069_s
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
cat > $D/list.txt <<'LIST'
or_models.json|https://openrouter.ai/api/v1/models
or_free.json|https://openrouter.ai/api/v1/models?max_price=0
or_ling_ep.json|https://openrouter.ai/api/v1/models/inclusionai/ling-3.2-flash-20261113/endpoints
hf_ling_repo.json|https://hf-mirror.com/api/models/inclusionAI/Ling-3.2-flash
hf_author_inclusion.json|https://hf-mirror.com/api/models?author=inclusionAI&limit=200
hf_author_baidu.json|https://hf-mirror.com/api/models?author=baidu&limit=200
hf_ernie_fp8.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base
hf_ernie_bf16.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base-BF16
hf_inkling.json|https://hf-mirror.com/api/models/thinkingmachines/Inkling-2-Small
hf_author_thinkingmachines.json|https://hf-mirror.com/api/models?author=thinkingmachines&limit=100
hf_praxis_base.json|https://hf-mirror.com/api/models/runwayml/praxis-1-base
gh_praxis.json|https://api.github.com/repos/runwayml/praxis-1-oss
ag_home.html|https://antigravity.google/
ag_pricing.html|https://antigravity.google/pricing
claude_pricing.html|https://claude.com/pricing
minimax_pricing.html|https://platform.minimaxi.com/document/price
runware_pricing.html|https://runware.ai/pricing
freellm.html|https://freellm.net/
aihot_free_tokens.html|https://aihot.news/free-tokens
aihot_home.html|https://aihot.news/
opencode_zen.html|https://opencode.ai/docs/zen
runway_pricing.html|https://runway.com/pricing
runway_company_news.html|https://runway.com/news/company-news
deepseek_news.html|https://www.deepseek.com/zh/news
deepseek_api_pricing.html|https://api-docs.deepseek.com/quick_start/pricing
ernie_release.html|https://ernie.baidu.com/zh/release/ernie-5-5-flash-preview/
qwen_blog.html|https://qwen.ai/blog
minimax_news.html|https://www.minimaxi.com/news
meituan_blog.html|https://tech.meituan.com/
meituan_ai.html|https://www.meituan.com/news/
longcat.html|https://longcat.chat/
gblog_ai.html|https://blog.google/technology/ai/
gblog_models.html|https://blog.google/products/gemini/
deepmind_blog.html|https://deepmind.google/discover/blog/
openai_news.html|https://openai.com/news/
anthropic_news.html|https://www.anthropic.com/news
mistral_news.html|https://mistral.ai/news
xai_news.html|https://x.ai/news
hf_blog.html|https://hf-mirror.com/blog
volcengine_pricing.html|https://www.volcengine.com/docs/82379/1099320
bigmodel_pricing.html|https://docs.bigmodel.cn/cn/guide/start/model-overview
kimi_pricing.html|https://platform.kimi.com/docs/pricing/chat
siliconflow_models.html|https://siliconflow.cn/models
modelscope.html|https://modelscope.cn/models
LIST
cat $D/list.txt | xargs -P 12 -I{} bash -c 'IFS="|" read -r n u <<< "{}"; fetch_one "$n" "$u"'
echo "DONE 069 special"
