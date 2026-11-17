#!/bin/bash
# 071 期专用核验：070 期「下一轮强制动作」12 条 + 本期新发布一手（并行版）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_071_s
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
or_qwen4max.json|https://openrouter.ai/api/v1/models/qwen/qwen4-max/endpoints
hf_ling_repo.json|https://hf-mirror.com/api/models/inclusionAI/Ling-3.2-flash
hf_author_inclusion.json|https://hf-mirror.com/api/models?author=inclusionAI&limit=200
hf_author_baidu.json|https://hf-mirror.com/api/models?author=baidu&limit=200
hf_author_qwen.json|https://hf-mirror.com/api/models?author=Qwen&limit=200
hf_ernie_fp8.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base
hf_ernie_bf16.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base-BF16
hf_author_longcat.json|https://hf-mirror.com/api/models?author=meituan-longcat&limit=200
hf_longcat25.json|https://hf-mirror.com/api/models/meituan-longcat/LongCat-2.5
hf_pear_main.json|https://hf-mirror.com/api/models/mit-han-lab/PEAR
gh_pear.json|https://api.github.com/repos/mit-han-lab/pear
gh_pear_commits.json|https://api.github.com/repos/mit-han-lab/pear/commits?per_page=5
hf_author_thinkingmachines.json|https://hf-mirror.com/api/models?author=thinkingmachines&limit=100
hf_inkling.json|https://hf-mirror.com/api/models/thinkingmachines/Inkling-2-Small
hf_kimi.json|https://hf-mirror.com/api/models/moonshotai/Kimi-K2.6
hf_kimi31.json|https://hf-mirror.com/api/models/moonshotai/Kimi-K3.1-Pro
hf_ripple.json|https://hf-mirror.com/api/models/ripple-ai/Ripple-3
gh_praxis.json|https://api.github.com/repos/runwayml/praxis-1-oss
ag_home.html|https://antigravity.google/
ag_pricing.html|https://antigravity.google/pricing
claude_pricing.html|https://claude.com/pricing
minimax_pricing.html|https://platform.minimaxi.com/document/price
minimax_news.html|https://www.minimaxi.com/news
runware_pricing.html|https://runware.ai/pricing
freellm.html|https://freellm.net/
aihot_free_tokens.html|https://aihot.news/free-tokens
aihot_home.html|https://aihot.news/
opencode_zen.html|https://opencode.ai/docs/zen
runway_pricing.html|https://runway.com/pricing
deepseek_news.html|https://www.deepseek.com/zh/news
deepseek_api_pricing.html|https://api-docs.deepseek.com/quick_start/pricing
ernie_release.html|https://ernie.baidu.com/zh/release/ernie-5-5-flash-preview/
qwen_blog.html|https://qwen.ai/blog
meituan_blog.html|https://tech.meituan.com/
longcat.html|https://longcat.chat/
gblog_ai.html|https://blog.google/technology/ai/
gblog_models.html|https://blog.google/products/gemini/
deepmind_blog.html|https://deepmind.google/discover/blog/
openai_news.html|https://openai.com/news/
openai_index.html|https://openai.com/index/
anthropic_news.html|https://www.anthropic.com/news
anthropic_engineering.html|https://www.anthropic.com/engineering
mistral_news.html|https://mistral.ai/news
xai_news.html|https://x.ai/news
hf_blog.html|https://hf-mirror.com/blog
hf_trending.json|https://hf-mirror.com/api/models?sort=trendingScore&limit=50
gh_trending.html|https://github.com/trending?since=daily
gh_trending_py.html|https://github.com/trending/python?since=daily
hunyuan.html|https://hunyuan.tencent.com/
hunyuan_news.html|https://hunyuan.tencent.com/news
tencent_cloud_ti.html|https://cloud.tencent.com/document/product/1729
volcengine_doubao.html|https://www.volcengine.com/docs/82379/1099320
zhipu_glm.html|https://docs.bigmodel.cn/cn/guide/start/model-overview
moonshot_kimi.html|https://platform.moonshot.cn/docs
aliyun_bailian.html|https://help.aliyun.com/zh/model-studio/models
kling.html|https://klingai.com/
stepfun.html|https://www.stepfun.com/
minicpm.html|https://www.minicpm.cn/
baai.html|https://www.baai.ac.cn/
lmarena.html|https://lmarena.ai/leaderboard
aa_home.html|https://artificialanalysis.ai/
llmstats.html|https://llm-stats.com/
livebench.html|https://livebench.ai/
swebench.html|https://www.swebench.com/
opencompass.html|https://opencompass.org.cn/
superclue.html|https://www.superclue.ai/
flageval.html|https://flageval.baai.ac.cn/
cac_news.html|https://www.cac.gov.cn/
miit_news.html|https://www.miit.gov.cn/
nda_news.html|https://www.nda.gov.cn/
caict.html|https://www.caict.ac.cn/
nist_ai.html|https://www.nist.gov/topics/artificial-intelligence
hn_newest.html|https://hnrss.org/newest?q=AI
hn_front.html|https://news.ycombinator.com/
reddit_localllama.json|https://www.reddit.com/r/LocalLLaMA/new.json?limit=60
reddit_ml.json|https://www.reddit.com/r/MachineLearning/new.json?limit=60
reddit_sd.json|https://www.reddit.com/r/StableDiffusion/new.json?limit=60
producthunt_ai.html|https://www.producthunt.com/topics/artificial-intelligence
simon.html|https://simonwillison.net/
techcrunch_ai.html|https://techcrunch.com/category/artificial-intelligence/
verge_ai.html|https://www.theverge.com/ai-artificial-intelligence
decoder.html|https://the-decoder.com/
jiqizhixin.html|https://www.jiqizhixin.com/
qbitai.html|https://www.qbitai.com/
leiphone.html|https://www.leiphone.com/category/aikeji
infoq.html|https://www.infoq.cn/topic/AI
36kr_ai.html|https://36kr.com/channel/ai
latepost.html|https://www.latepost.com/
geekpark.html|https://www.geekpark.net/
ifanr.html|https://www.ifanr.com/
huxiu.html|https://www.huxiu.com/
tmtpost.html|https://www.tmtpost.com/
pingwest.html|https://www.pingwest.com/
jiemian.html|https://www.jiemian.com/
thepaper.html|https://www.thepaper.cn/
sina_tech.html|https://tech.sina.com.cn/
163_tech.html|https://tech.163.com/
qq_tech.html|https://new.qq.com/ch/tech/
ithome.html|https://www.ithome.com/
cnbeta.html|https://www.cnbeta.com.tw/
solidot.html|https://www.solidot.org/
sspai.html|https://sspai.com/
v2ex.html|https://www.v2ex.com/
datawhale.html|https://www.datawhale.cn/
baai_hub.html|https://hub.baai.ac.cn/
LIST
cat $D/list.txt | xargs -P 12 -I{} bash -c 'IFS="|" read -r n u <<< "{}"; fetch_one "$n" "$u"'
echo "DONE 071 SPECIAL"
