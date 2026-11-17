#!/bin/bash
# 071 期 RSS 补抓：主清单里多数是站点首页（HTML shell），真正的 RSS 端点单列一份
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_071_r
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 40 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  if [ ! -f "$D/$name" ]; then : > "$D/$name"; fi
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
export -f fetch_one
export UA D
cat > $D/list.txt <<'LIST'
r01_openai_news|https://openai.com/news/rss.xml
r02_anthropic_news|https://www.anthropic.com/rss.xml
r03_deepmind|https://deepmind.google/blog/rss.xml
r04_gblog_ai|https://blog.google/technology/ai/rss/
r05_gresearch|https://research.google/blog/rss/
r06_meta_ai|https://ai.meta.com/blog/rss/
r07_ms_ai|https://blogs.microsoft.com/ai/feed/
r08_nvidia|https://blogs.nvidia.com/feed/
r09_hf_blog|https://huggingface.co/blog/feed.xml
r10_mistral|https://mistral.ai/news/rss.xml
r11_xai|https://x.ai/news/rss.xml
r12_techcrunch|https://techcrunch.com/category/artificial-intelligence/feed/
r13_verge|https://www.theverge.com/rss/ai-artificial-intelligence/index.xml
r14_venturebeat|https://venturebeat.com/category/ai/feed/
r15_technologyreview|https://www.technologyreview.com/topic/artificial-intelligence/feed
r16_arstechnica|https://feeds.arstechnica.com/arstechnica/technology-lab
r17_wired|https://www.wired.com/feed/tag/ai/latest/rss
r18_decoder|https://the-decoder.com/feed/
r19_marktechpost|https://www.marktechpost.com/feed/
r20_zdnet|https://www.zdnet.com/topic/artificial-intelligence/rss.xml
r21_register|https://www.theregister.com/software/ai_ml/headlines.atom
r22_jiqizhixin|https://www.jiqizhixin.com/rss
r23_qbitai|https://www.qbitai.com/feed
r24_leiphone|https://www.leiphone.com/feed
r25_infoq|https://www.infoq.cn/feed
r26_36kr|https://36kr.com/feed
r27_geekpark|https://www.geekpark.net/rss
r28_ifanr|https://www.ifanr.com/feed
r29_huxiu|https://www.huxiu.com/rss/0.xml
r30_tmtpost|https://www.tmtpost.com/rss.xml
r31_sspai|https://sspai.com/feed
r32_solidot|https://www.solidot.org/index.rss
r33_cnbeta|https://www.cnbeta.com.tw/backend.php
r34_ithome|https://www.ithome.com/rss/
r35_lesswrong|https://www.lesswrong.com/feed.xml
r36_alignmentforum|https://www.alignmentforum.org/feed.xml
r37_importai|https://importai.substack.com/feed
r38_thesequence|https://thesequence.substack.com/feed
r39_ahead|https://magazine.sebastianraschka.com/feed
r40_aisnakeoil|https://www.aisnakeoil.com/feed
r41_simon|https://simonwillison.net/atom/everything/
r42_interconnects|https://www.interconnects.ai/feed
r43_baoyu|https://baoyu.io/feed.xml
r44_lastweekin|https://lastweekin.ai/feed
r45_hn_front|https://hnrss.org/frontpage
r46_hn_ai|https://hnrss.org/newest?q=LLM
r47_reddit_localllama|https://www.reddit.com/r/LocalLLaMA/.rss
r48_reddit_ml|https://www.reddit.com/r/MachineLearning/.rss
r49_reddit_openai|https://www.reddit.com/r/OpenAI/.rss
r50_reddit_singularity|https://www.reddit.com/r/singularity/.rss
r51_reddit_sd|https://www.reddit.com/r/StableDiffusion/.rss
r52_reddit_artificial|https://www.reddit.com/r/artificial/.rss
r53_producthunt|https://www.producthunt.com/feed
r54_arxiv_ai|https://rss.arxiv.org/rss/cs.AI
r55_arxiv_cl|https://rss.arxiv.org/rss/cs.CL
r56_arxiv_lg|https://rss.arxiv.org/rss/cs.LG
r57_hf_papers|https://huggingface.co/papers/rss
r58_stability|https://stability.ai/news/rss.xml
r59_cohere|https://cohere.com/blog/rss.xml
r60_runway|https://runwayml.com/news/rss.xml
r61_perplexity|https://www.perplexity.ai/hub/blog/rss.xml
r62_cursor|https://cursor.com/changelog/rss.xml
r63_latentspace|https://www.latent.space/feed
r64_therundown|https://www.therundown.ai/feed
r65_bensbites|https://www.bensbites.co/feed
r66_tldr_ai|https://tldr.tech/api/rss/ai
r67_venturebeat_ai|https://venturebeat.com/feed/
r68_artificialintelligence_news|https://www.artificialintelligence-news.com/feed/
r69_spectrum|https://spectrum.ieee.org/feeds/topic/artificial-intelligence.rss
r70_quanta|https://www.quantamagazine.org/feed/
r71_nature_ml|https://www.nature.com/natmachintell.rss
r72_scmp_tech|https://www.scmp.com/rss/318208/feed
r73_restofworld|https://restofworld.org/feed/latest/
r74_technologyreview_ai|https://www.technologyreview.com/feed/
r75_axios_ai|https://api.axios.com/feed/technology
r76_semafor|https://www.semafor.com/rss.xml
r77_economist|https://www.economist.com/science-and-technology/rss.xml
r78_theinformation|https://www.theinformation.com/feed
r79_bloomberg_ai|https://feeds.bloomberg.com/technology/news.rss
r80_reuters_tech|https://www.reutersagency.com/feed/?best-topics=tech
LIST
cat $D/list.txt | xargs -P 14 -I{} bash -c 'IFS="|" read -r n u <<< "{}"; fetch_one "$n" "$u"'
echo "DONE 071 RSS"
