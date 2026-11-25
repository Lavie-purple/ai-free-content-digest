#!/bin/bash
# 078 期核验：077 期强制动作 12 条 + 本期新发布一手（并行版）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_079_s
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
or_free.json|https://openrouter.ai/api/v1/models?max_price=0
or_all.json|https://openrouter.ai/api/v1/models
or_dots_note.json|https://openrouter.ai/api/v1/models/dots-studio/dots-3-note-preview:free
or_inkling_mini_ep.json|https://openrouter.ai/api/v1/models/thinkingmachines/inkling-2-mini/endpoints
or_ling_free_ep.json|https://openrouter.ai/api/v1/models/inclusionai/ling-3.2-flash:free/endpoints
or_gpt62.json|https://openrouter.ai/api/v1/models?q=gpt-6.2
or_glm54.json|https://openrouter.ai/api/v1/models?q=glm-5.4
opencode_zen.html|https://opencode.ai/docs/zen
autoclaw_m11w4.html|https://autoclaw.zhipuai.cn/blog/news/M11W4/
autoclaw_m11w5.html|https://autoclaw.zhipuai.cn/blog/news/M11W5/
autoclaw_home.html|https://autoclaw.zhipuai.cn/
ernie_release.html|https://ernie.baidu.com/zh/release/ernie-5-5-flash-preview/
ernie_home.html|https://ernie.baidu.com/
hf_author_baidu.json|https://hf-mirror.com/api/models?author=baidu&limit=200
hf_hy4_770.json|https://hf-mirror.com/api/models/tencent/Hy4
hf_hy4_770_fp8.json|https://hf-mirror.com/api/models/tencent/Hy4-FP8
hf_hy4_770_base.json|https://hf-mirror.com/api/models/tencent/Hy4-base
hf_hy4_flash.json|https://hf-mirror.com/api/models/tencent/Hy4-flash
hf_hy4_flash_fp8.json|https://hf-mirror.com/api/models/tencent/Hy4-flash-FP8
hf_hy4_flash_base.json|https://hf-mirror.com/api/models/tencent/Hy4-flash-base
hf_inkling_mini.json|https://hf-mirror.com/api/models/thinkingmachines/Inkling-2-Mini
hf_inkling_small.json|https://hf-mirror.com/api/models/thinkingmachines/Inkling-2-Small
hf_kimi31.json|https://hf-mirror.com/api/models/moonshotai/Kimi-K3.1-Pro
hf_longcat25.json|https://hf-mirror.com/api/models/meituan-longcat/LongCat-2.5
hf_longcat20.json|https://hf-mirror.com/api/models/meituan-longcat/LongCat-2.0
hf_ernie_fp8.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base
hf_ernie_bf16.json|https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base-BF16
hf_trending.json|https://hf-mirror.com/api/models?sort=trendingScore&limit=40
hf_blog.html|https://hf-mirror.com/blog
hf_papers.html|https://hf-mirror.com/papers
ag_home.html|https://antigravity.google/
ag_pricing.html|https://antigravity.google/pricing
minimax_pricing.html|https://platform.minimaxi.com/document/price
minimax_h3.html|https://www.minimaxi.com/news
runware_pricing.html|https://runware.ai/pricing
runway_pricing.html|https://runway.com/pricing
oa_pricing.html|https://openai.com/chatgpt/pricing/
oa_api_pricing.html|https://openai.com/api/pricing/
oa_news.html|https://openai.com/news/
oa_index.html|https://openai.com/index/
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
zhipu_coding.html|https://docs.bigmodel.cn/cn/coding-plan/overview
zai_home.html|https://z.ai/
moonshot.html|https://platform.moonshot.cn/docs
volcengine.html|https://www.volcengine.com/docs/82379/1099320
hunyuan.html|https://hunyuan.tencent.com/
stepfun.html|https://www.stepfun.com/
kling.html|https://klingai.com/
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
gh_trending.html|https://github.com/trending?since=daily
aihot_home.html|https://aihot.news/
aihot_free.html|https://aihot.news/free-tokens
freellm.html|https://freellm.net/
lmarena.html|https://lmarena.ai/leaderboard
aa_home.html|https://artificialanalysis.ai/
llmstats.html|https://llm-stats.com/
livebench.html|https://livebench.ai/
claude_pricing.html|https://claude.com/pricing
cursor_pricing.html|https://cursor.com/pricing
copilot_pricing.html|https://github.com/features/copilot/plans
windsurf_pricing.html|https://windsurf.com/pricing
trae.html|https://www.trae.ai/
kimi_pricing.html|https://platform.moonshot.cn/docs/pricing/chat
dashscope.html|https://help.aliyun.com/zh/model-studio/models
tencent_tokenhub.html|https://cloud.tencent.com/document/product/1729
xfyun_pricing.html|https://www.xfyun.cn/doc/spark/price.html
stepfun_pricing.html|https://platform.stepfun.com/docs/pricing
01ai.html|https://www.lingyiwanwu.com/
perplexity_pricing.html|https://www.perplexity.ai/pro
reddit_localllama.html|https://www.reddit.com/r/LocalLLaMA/
hnalgolia.json|https://hn.algolia.com/api/v1/search_by_date?query=free%20AI&tags=story
LIST
cat $D/list.txt | xargs -P 12 -I{} bash -c 'IFS="|" read -r n u <<< "{}"; fetch_one "$n" "$u"'
echo "DONE 079 SPECIAL"

# ---- 079 追加：上期强制动作里读不到的路径换法 ----
D=tmp_079_s
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
fetch2(){ name="$1"; url="$2"; shift 2; code=$(curl -sS -m 40 -A "$UA" -L "$@" -o "$D/$name" -w "%{http_code}" 2>/dev/null); [ -f "$D/$name" ] || : > "$D/$name"; size=$(wc -c < "$D/$name" | tr -d ' '); echo "$code ${size:-0} $name"; }
echo "--- extra ---"
fetch2 ag_pricing_h11.html https://antigravity.google/pricing --http1.1
fetch2 ag_docs.html https://antigravity.google/docs
fetch2 ag_blog.html https://antigravity.google/blog
fetch2 openrouter_home.html https://openrouter.ai/models
fetch2 glm_pricing.html https://open.bigmodel.cn/pricing
fetch2 zai_pricing.html https://z.ai/subscribe
fetch2 ernie_or_free.json "https://openrouter.ai/api/v1/models?q=ernie"
fetch2 or_dots_note_enc.json "https://openrouter.ai/api/v1/models/dots-studio/dots-3-note-preview%3Afree/endpoints"
fetch2 or_free_all_again.json "https://openrouter.ai/api/v1/models?max_price=0"
fetch2 hf_ernie_prev.json "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Preview"
fetch2 hf_ernie_prev_fp8.json "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Preview-FP8"
fetch2 hf_ernie_prev_bf16.json "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Preview-BF16"
fetch2 hf_author_baidu2.json "https://hf-mirror.com/api/models?author=baidu&limit=200"
