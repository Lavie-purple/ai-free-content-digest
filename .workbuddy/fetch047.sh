#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_047
mkdir -p $D
get(){ curl -sS -m 45 -A "$UA" -L "$2" -o "$D/$1" -w "%{http_code} %{size_download} $1\n" 2>/dev/null; }
getjson(){ curl -sS -m 45 -A "$UA" -L "$2" -o "$D/$1" -w "%{http_code} %{size_download} $1\n" 2>/dev/null; }

# ===== 一手官方 · 国外 =====
get openai_news_rss.xml   "https://openai.com/news/rss.xml"
get openai_news.html      "https://openai.com/news/"
get anthropic_news.html   "https://www.anthropic.com/news"
get anthropic_rss.xml     "https://www.anthropic.com/news/rss.xml"
get deepmind_blog.html    "https://deepmind.google/discover/blog/"
get gblog_ai.html          "https://blog.google/technology/ai/"
get gresearch.html         "https://research.google/blog/"
get metablog.html          "https://ai.meta.com/blog/"
get msblog_ai.html         "https://blogs.microsoft.com/ai/"
get msresearch.html        "https://www.microsoft.com/en-us/research/blog/"
get nvblog.html            "https://blogs.nvidia.com/"
get mistral_news.html      "https://mistral.ai/news"
get cohere_blog.html       "https://cohere.com/blog"
get cursor_changelog.html  "https://cursor.com/changelog"
get cognition_blog.html    "https://cognition.ai/blog"
get runway_news.html       "https://runwayml.com/news"
get perplexity_blog.html   "https://www.perplexity.ai/hub/blog"
get stability_news.html    "https://stability.ai/news"
get midjourney.html        "https://www.midjourney.com/showcase"

# ===== 一手官方 · 国内 =====
get deepseek_news.html     "https://www.deepseek.com/zh/news"
get qwen_blog.html         "https://qwen.ai/blog"
get kimi_blog2.html        "https://www.kimi.com/blog"
get kimi_pricing.html      "https://platform.kimi.com/docs/pricing/chat"
get bigmodel.html          "https://docs.bigmodel.cn/cn/guide/start/model-overview"
get minimax_news.html      "https://www.minimaxi.com/news"
get volcengine.html        "https://www.volcengine.com/docs/82379"
get seed.html              "https://seed.bytedance.com/"
get baidu_doc.html         "https://cloud.baidu.com/doc/index.html"
get hunyuan.html           "https://hunyuan.tencent.com/"
get xfyun.html             "https://xfyun.cn/doc/"
get xiaomi_mimo.html       "https://www.xiaomiev.com/"
get huawei_pangu.html      "https://www.huaweicloud.com/product/pangu.html"
get minicpm.html           "https://www.minicpm.cn/"
get stepfun.html           "https://www.stepfun.com/"
get klingai.html           "https://klingai.com/"
get baai.html              "https://www.baai.ac.cn/"
get singularis.html        "https://www.singularis.ltd/"
get aliyun_models.html     "https://help.aliyun.com/zh/model-studio/models"
get moonshot_docs.html     "https://platform.moonshot.cn/docs"

# ===== 模型与开源 / 目录 API =====
getjson hf_trending.json   "https://hf-mirror.com/api/models?sort=trending&limit=100"
getjson hf_moonshot.json   "https://hf-mirror.com/api/models?author=moonshotai&limit=100"
getjson hf_minimax.json    "https://hf-mirror.com/api/models?author=MiniMaxAI&limit=100&sort=createdAt&direction=-1"
getjson or_models.json     "https://openrouter.ai/api/v1/models"
getjson hf_qwen.json       "https://hf-mirror.com/api/models?author=Qwen&limit=100&sort=createdAt&direction=-1"
getjson hf_deepseek.json   "https://hf-mirror.com/api/models?author=deepseek-ai&limit=100&sort=createdAt&direction=-1"
getjson fal_models.json    "https://fal.ai/api/models?keywords="
get hf_blog.html           "https://hf-mirror.com/blog"
get modelscope.html        "https://modelscope.cn/models"
get github_trending.html   "https://github.com/trending"

# ===== 聚合器 / 工具 =====
get aihot.html             "https://aihot.news/"
get freellm.html           "https://freellm.net/"
get freellm_or.html        "https://freellm.net/providers/openrouter"
get or_announcements.html   "https://openrouter.ai/announcements"
get autoclaw_cn.html       "https://autoclaw.zhipuai.cn/blog/news"
get autoclaw_intl.html     "https://autoclaw.z.ai/blog/news"
get reflection.html        "https://platform.reflection.ai/"
get zcode.html             "https://zcode.ai/"
get opencode_zen.html      "https://opencode.ai/docs/zen"
get opencode_go.html       "https://opencode.ai/docs/go"

# ===== 评测与榜单 =====
get lmarena.html           "https://lmarena.ai/leaderboard"
get aa.html                "https://artificialanalysis.ai/"
get llmstats.html          "https://llm-stats.com/"
get livebench.html         "https://livebench.ai/"
get superclue.html         "https://www.superclue.ai/"
get opencompass.html       "https://opencompass.org.cn/"

# ===== 政策与监管 =====
get cac.html               "https://www.cac.gov.cn/"
get miit.html              "https://www.miit.gov.cn/"
get nda.html               "https://www.nda.gov.cn/"
get caict.html             "https://www.caict.ac.cn/kxyj/qwfb/bps/"
get cninfo.html            "https://www.cninfo.com.cn/new/index"

# ===== 媒体 =====
get jiqizhixin.html        "https://www.jiqizhixin.com/"
get qbitai.html            "https://www.qbitai.com/"
get tc_ai.html             "https://techcrunch.com/category/artificial-intelligence/"
get verge_ai.html          "https://www.theverge.com/ai-artificial-intelligence"
get arstechnica_ai.html    "https://arstechnica.com/ai/"
get thedecoder.html        "https://the-decoder.com/"
get hnrss.html             "https://hnrss.org/newest?q=AI"
get reddit_llama.html      "https://www.reddit.com/r/LocalLLaMA/.rss"
get simon.html             "https://simonwillison.net/atom/everything/"
get baoyu.html             "https://baoyu.io/feed"
get latentspace.html       "https://www.latent.space/feed"
get sota.html              "https://sota.jiqizhixin.com/"

# ===== 窗口内时间戳核对用的补充 =====
get nodejs_vuln.html       "https://nodejs.org/en/blog/vulnerability"
get hf_org_moonshot.html   "https://hf-mirror.com/moonshotai"
get hf_org_minimax.html    "https://hf-mirror.com/MiniMaxAI"
echo "DONE"
