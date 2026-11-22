#!/bin/bash
# 075 期核验：073 期强制动作 + 本期新发布一手（并行版）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_076_s
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
minimax_pricing.html|https://platform.minimaxi.com/document/price
minimax_news.html|https://www.minimaxi.com/news
ag_home.html|https://antigravity.google/
ag_pricing.html|https://antigravity.google/pricing
oa_pricing.html|https://openai.com/chatgpt/pricing/
oa_api_pricing.html|https://openai.com/api/pricing/
oa_news.html|https://openai.com/news/
oa_academic.html|https://openai.com/index/expanding-chatgpt-for-academic-researchers/
hf_hy4.json|https://hf-mirror.com/api/models/tencent/Hy4-flash
hf_hy4_fp8.json|https://hf-mirror.com/api/models/tencent/Hy4-flash-FP8
hf_hy4_base.json|https://hf-mirror.com/api/models/tencent/Hy4-flash-base
hf_hy4_search.json|https://hf-mirror.com/api/models?search=Hy4&limit=100
ms_hy4.html|https://modelscope.cn/models/Tencent-Hunyuan/Hy4-flash
gh_hy4.json|https://api.github.com/repos/Tencent-Hunyuan/Hy4-flash
opencode_zen.html|https://opencode.ai/docs/zen
or_free.json|https://openrouter.ai/api/v1/models?max_price=0
or_all.json|https://openrouter.ai/api/v1/models
or_ling_ep.json|https://openrouter.ai/api/v1/models/inclusionai/ling-3.2-flash-20261113/endpoints
hf_kimi31.json|https://hf-mirror.com/api/models/moonshotai/Kimi-K3.1-Pro
hf_inkling.json|https://hf-mirror.com/api/models/thinkingmachines/Inkling-2-Small
hf_longcat25.json|https://hf-mirror.com/api/models/meituan-longcat/LongCat-2.5
hf_ernie_fp8.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base
hf_ernie_bf16.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base-BF16
hf_author_baidu.json|https://hf-mirror.com/api/models?author=baidu&limit=200
hf_trending.json|https://hf-mirror.com/api/models?sort=trendingScore&limit=40
hf_blog.html|https://hf-mirror.com/blog
freellm.html|https://freellm.net/
aihot_home.html|https://aihot.news/
aihot_free_tokens.html|https://aihot.news/free-tokens
runware_pricing.html|https://runware.ai/pricing
runway_pricing.html|https://runway.com/pricing
claude_pricing.html|https://claude.com/pricing
anthropic_news.html|https://www.anthropic.com/news
deepmind_blog.html|https://deepmind.google/discover/blog/
gblog_ai.html|https://blog.google/technology/ai/
meta_blog.html|https://ai.meta.com/blog/
mistral_news.html|https://mistral.ai/news
xai_news.html|https://x.ai/news
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
autoclaw_m11w4.html|https://autoclaw.zhipuai.cn/blog/news/M11W4/
autoclaw_m11w3.html|https://autoclaw.zhipuai.cn/blog/news/M11W3/
autoclaw_home.html|https://autoclaw.zhipuai.cn/
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
sf_models.html|https://siliconflow.cn/models
ms_models.html|https://modelscope.cn/models
gh_trending.html|https://github.com/trending
hf_papers.html|https://hf-mirror.com/papers
hf_spaces.html|https://hf-mirror.com/spaces
oa_index.html|https://openai.com/index/
anthropic_news2.html|https://www.anthropic.com/news
geminiapp.html|https://gemini.google.com/
perplexity_pricing.html|https://www.perplexity.ai/pro
cursor_pricing.html|https://cursor.com/pricing
copilot_pricing.html|https://github.com/features/copilot/plans
windsurf_pricing.html|https://windsurf.com/pricing
trae.html|https://www.trae.ai/
kimi_pricing.html|https://platform.moonshot.cn/docs/pricing/chat
zhipu_pricing.html|https://docs.bigmodel.cn/cn/guide/start/model-overview
dashscope.html|https://help.aliyun.com/zh/model-studio/models
doubao_pricing.html|https://www.volcengine.com/docs/82379/1099320
tencent_tokenhub.html|https://cloud.tencent.com/document/product/1729
xfyun_pricing.html|https://www.xfyun.cn/doc/spark/price.html
baichuan.html|https://www.baichuan-ai.com/
minimax_platform.html|https://platform.minimaxi.com/document/price
sensenova.html|https://platform.sensenova.cn/
stepfun_pricing.html|https://platform.stepfun.com/docs/pricing
01ai.html|https://www.lingyiwanwu.com/
moonshot_news.html|https://www.moonshot.cn/
deepseek_api.html|https://api-docs.deepseek.com/zh-cn/quick_start/pricing
qwen_chat.html|https://chat.qwen.ai/
glm_chat.html|https://chat.z.ai/
openrouter_free2.json|https://openrouter.ai/api/v1/models?max_price=0
hf_trending2.json|https://hf-mirror.com/api/models?sort=trendingScore&limit=60
v2ex.html|https://www.v2ex.com/
sspai.html|https://sspai.com/
weibo_ai.html|https://s.weibo.com/top/summary
zhihu_ai.html|https://www.zhihu.com/topic/19556664/hot
juejin.html|https://juejin.cn/ai
bilibili.html|https://www.bilibili.com/
x_trend.html|https://x.com/
reddit_localllama.html|https://www.reddit.com/r/LocalLLaMA/
reddit_singularity.html|https://www.reddit.com/r/singularity/
hnalgolia.json|https://hn.algolia.com/api/v1/search_by_date?query=free%20AI&tags=story
LIST
cat $D/list.txt | xargs -P 12 -I{} bash -c 'IFS="|" read -r n u <<< "{}"; fetch_one "$n" "$u"'

# ---- 076 期追加观测位（075 强制动作逐条落地） ----
fetch_one autoclaw_m11w5 "https://autoclaw.zhipuai.cn/blog/news/M11W5/"
fetch_one hf_hy4_770.json "https://hf-mirror.com/api/models/tencent/Hy4"
fetch_one hf_hy4_770_fp8.json "https://hf-mirror.com/api/models/tencent/Hy4-FP8"
fetch_one hf_hy4_770_base.json "https://hf-mirror.com/api/models/tencent/Hy4-base"
fetch_one hf_inkling_mini.json "https://hf-mirror.com/api/models/thinkingmachines/Inkling-2-Mini"
fetch_one tm_news.html "https://thinkingmachines.ai/news/"
fetch_one tm_mini.html "https://thinkingmachines.ai/news/inkling-2-mini/"
fetch_one or_ling_free_ep.json "https://openrouter.ai/api/v1/models/inclusionai/ling-3.2-flash:free/endpoints"
fetch_one or_ling_base_ep.json "https://openrouter.ai/api/v1/models/inclusionai/ling-3.2-flash/endpoints"
fetch_one or_inkling_mini_ep.json "https://openrouter.ai/api/v1/models/thinkingmachines/inkling-2-mini/endpoints"
fetch_one oa_index2.html "https://openai.com/index/"
fetch_one anthropic_news3.html "https://www.anthropic.com/news"
fetch_one gh_trending2.html "https://github.com/trending?since=daily"
fetch_one hf_papers2.html "https://hf-mirror.com/papers"
fetch_one aihot_free2.html "https://aihot.news/free-tokens"
echo "DONE 075 SPECIAL"
