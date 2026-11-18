#!/bin/bash
# 072 期专用核验：071 期「下一轮强制动作」+ 本期新发布一手（并行版）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_072_s
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
oa_gpt62.html|https://openai.com/index/introducing-gpt-6-2-astra-sol/
oa_astralaw.html|https://openai.com/index/astra-law-6-2/
oa_sales.html|https://openai.com/index/introducing-chatgpt-for-sales/
oa_pricing.html|https://openai.com/chatgpt/pricing/
oa_api_pricing.html|https://openai.com/api/pricing/
oa_academic.html|https://openai.com/index/expanding-chatgpt-for-academic-researchers/
ag_home.html|https://antigravity.google/
ag_pricing.html|https://antigravity.google/pricing
claude_pricing.html|https://claude.com/pricing
anthropic_news.html|https://www.anthropic.com/news
anthropic_eng.html|https://www.anthropic.com/engineering
minimax_pricing.html|https://platform.minimaxi.com/document/price
minimax_news.html|https://www.minimaxi.com/news
runware_pricing.html|https://runware.ai/pricing
runway_pricing.html|https://runway.com/pricing
freellm.html|https://freellm.net/
aihot_home.html|https://aihot.news/
aihot_free_tokens.html|https://aihot.news/free-tokens
opencode_zen.html|https://opencode.ai/docs/zen
or_free.json|https://openrouter.ai/api/v1/models?max_price=0
or_ling_ep.json|https://openrouter.ai/api/v1/models/inclusionai/ling-3.2-flash-20261113/endpoints
hf_kimi31.json|https://hf-mirror.com/api/models/moonshotai/Kimi-K3.1-Pro
hf_inkling.json|https://hf-mirror.com/api/models/thinkingmachines/Inkling-2-Small
hf_longcat25.json|https://hf-mirror.com/api/models/meituan-longcat/LongCat-2.5
hf_ernie_fp8.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base
hf_ernie_bf16.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base-BF16
hf_author_qwen.json|https://hf-mirror.com/api/models?author=Qwen&limit=200
hf_author_baidu.json|https://hf-mirror.com/api/models?author=baidu&limit=200
hf_trending.json|https://hf-mirror.com/api/models?sort=trendingScore&limit=40
gh_pear.json|https://api.github.com/repos/mit-han-lab/pear
gh_praxis.json|https://api.github.com/repos/runwayml/praxis-1-oss
gh_trending.html|https://github.com/trending?since=daily
autoclaw_m11w4.html|https://autoclaw.zhipuai.cn/blog/news/M11W4/
autoclaw_m11w3.html|https://autoclaw.zhipuai.cn/blog/news/M11W3/
autoclaw_home.html|https://autoclaw.zhipuai.cn/
deepseek_news.html|https://www.deepseek.com/zh/news
deepseek_pricing.html|https://api-docs.deepseek.com/quick_start/pricing
qwen_blog.html|https://qwen.ai/blog
zhipu_models.html|https://docs.bigmodel.cn/cn/guide/start/model-overview
moonshot.html|https://platform.moonshot.cn/docs
volcengine.html|https://www.volcengine.com/docs/82379/1099320
hunyuan.html|https://hunyuan.tencent.com/
ernie_release.html|https://ernie.baidu.com/zh/release/ernie-5-5-flash-preview/
stepfun.html|https://www.stepfun.com/
kling.html|https://klingai.com/
mistral_news.html|https://mistral.ai/news
xai_news.html|https://x.ai/news
deepmind_blog.html|https://deepmind.google/discover/blog/
gblog_ai.html|https://blog.google/technology/ai/
meta_blog.html|https://ai.meta.com/blog/
hf_blog.html|https://hf-mirror.com/blog
lmarena.html|https://lmarena.ai/leaderboard
aa_home.html|https://artificialanalysis.ai/
llmstats.html|https://llm-stats.com/
livebench.html|https://livebench.ai/
jiqizhixin.html|https://www.jiqizhixin.com/
qbitai.html|https://www.qbitai.com/
ithome.html|https://www.ithome.com/
leiphone.html|https://www.leiphone.com/category/aikeji
infoq.html|https://www.infoq.cn/topic/AI
36kr_ai.html|https://36kr.com/channel/ai
geekpark.html|https://www.geekpark.net/
hn_front.html|https://news.ycombinator.com/
simon.html|https://simonwillison.net/
techcrunch_ai.html|https://techcrunch.com/category/artificial-intelligence/
verge_ai.html|https://www.theverge.com/ai-artificial-intelligence
decoder.html|https://the-decoder.com/
producthunt_ai.html|https://www.producthunt.com/topics/artificial-intelligence
cac_news.html|https://www.cac.gov.cn/
miit_news.html|https://www.miit.gov.cn/
caict.html|https://www.caict.ac.cn/
LIST
cat $D/list.txt | xargs -P 12 -I{} bash -c 'IFS="|" read -r n u <<< "{}"; fetch_one "$n" "$u"'
echo "DONE 072 SPECIAL"
