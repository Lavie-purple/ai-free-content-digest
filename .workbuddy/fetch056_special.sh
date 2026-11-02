#!/bin/bash
# 055 期：054 期脚注③「下一轮强制动作」31 条专项实访（销项优先）
# ⚠️ 合规 UA：SEC EDGAR 等站点要求带联系方式的 User-Agent（避坑 232）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
UA_SEC="AI-Free-Content-Report research@example.com"
D=tmp_056
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"; ua="${3:-$UA}"
  code=$(curl -sS -m 45 -A "$ua" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
export -f fetch_one
export UA UA_SEC D

# ① 豆包工作 30 天订阅（连续第 8 期零命中 · 换路径 + 换 UA）
fetch_one vol_dw_1.html "https://www.volcengine.com/product/doubao-work"
fetch_one vol_dw_2.html "https://www.volcengine.com/docs/82379/1099320"
fetch_one vol_dw_3.html "https://www.volcengine.com/activity/doubao-work"
fetch_one vol_dw_4.html "https://www.volcengine.com/docs/82379"
fetch_one vol_doubao_api.json "https://www.volcengine.com/api/v1/activity/doubao"

# ② 国家超算互联网 夜间免费（找「夜间免费」那一栏）
fetch_one scnet_h1.html "https://www.scnet.cn/"
fetch_one scnet_h2.html "https://scnet.cn/"
fetch_one scnet_h3.html "https://www.scnet.cn/model"
fetch_one scnet_h4.html "https://www.scnet.cn/docs"
fetch_one scnet_h5.html "https://www.scnet.cn/activity"

# ③ MOSS-Image ModelScope 侧下载量
fetch_one ms_moss.html "https://modelscope.cn/models/OpenMOSS/MOSS-Image"
fetch_one ms_moss_api.json "https://modelscope.cn/api/v1/models/OpenMOSS/MOSS-Image"
fetch_one ms_moss2.html "https://www.modelscope.cn/models/OpenMOSS/MOSS-Image"

# ④⑤ Mistral 官方单价与公告页（连续第 14 次 000 · 再试）
fetch_one mistral_n1.html "https://mistral.ai/news/mistral-large-4-oss/"
fetch_one mistral_n2.html "https://mistral.ai/news/"
fetch_one mistral_pr1.html "https://docs.mistral.ai/getting-started/models/models_overview/"
fetch_one mistral_pr2.html "https://console.mistral.ai/"

# ⑥ Mistral Large 4 demo 免费预算额度数字 / 日历日
fetch_one hf_mistral_disc2.html "https://hf-mirror.com/mistralai/Mistral-Large-4-1T-A52B/discussions"
fetch_one hf_mistral_readme2.md "https://hf-mirror.com/mistralai/Mistral-Large-4-1T-A52B/raw/main/README.md"
fetch_one hf_mistral_commits2.json "https://hf-mirror.com/api/models/mistralai/Mistral-Large-4-1T-A52B/commits/main"

# ⑦⑨⑩ AutoClaw M10W4 残留文案 / Kimi K3.1 Pro 权重 / K2 停新
fetch_one ac_intl_m10w4c.html "https://autoclaw.z.ai/blog/news/M10W4/"
fetch_one ac_intl_news3.html "https://autoclaw.z.ai/blog/news/"
fetch_one ac_cn_m11w1c.html "https://autoclaw.zhipuai.cn/blog/news/M11W1/"
fetch_one hf_moonshot4.json "https://hf-mirror.com/api/models?author=moonshotai&limit=100&sort=createdAt&direction=-1"
fetch_one hf_k3c.json "https://hf-mirror.com/api/models?search=Kimi-K3&limit=50"
fetch_one hf_kimi_search.json "https://hf-mirror.com/api/models?search=moonshotai&limit=100"
fetch_one kimi_pricing3.html "https://platform.kimi.com/docs/pricing/chat"
fetch_one kimi_k2_stop3.html "https://platform.moonshot.cn/docs/guide/kimi-k2-thinking-deprecation"

# ⑧⑪ OpenRouter 全量逐条 diff + 公告
fetch_one or_models5.json "https://openrouter.ai/api/v1/models"
fetch_one or_free7.json "https://openrouter.ai/api/v1/models?max_price=0"
fetch_one or_ann2.html "https://openrouter.ai/announcements"
fetch_one or_csam3.html "https://openrouter.ai/announcements/csam-screening"
fetch_one or_csam4.html "https://openrouter.ai/blog/csam-screening"
fetch_one or_ow.html "https://openrouter.ai/blog/open-weight-vs-closed-weight-models"
fetch_one or_cost.html "https://openrouter.ai/blog/how-much-does-claude-code-cost"

# ⑫ OpenCode zen 免费档 + LongCat 是否回归
fetch_one opencode_zen4.html "https://opencode.ai/docs/zen"
fetch_one longcat3.html "https://github.com/meituan-longcat"

# ⑬ Runware 促销表 + 过期条目清理
fetch_one runware_pricing6.html "https://runware.ai/pricing"
fetch_one runware_models3.html "https://runware.ai/models"
fetch_one runware_sync4.html "https://runware.ai/sync-3"

# ⑭ Unsloth 量化基准页
fetch_one unsloth_docs3.html "https://docs.unsloth.ai/"
fetch_one unsloth_bench.html "https://docs.unsloth.ai/baselines/unsloth-benchmarks"

# ⑯⑲ platform.reflection.ai 定价 + freellm
fetch_one reflection4.html "https://platform.reflection.ai/pricing"
fetch_one freellm4.html "https://freellm.net/"
fetch_one freellm_or4.html "https://freellm.net/providers/openrouter"

# ⑰ 老混元 Q04
fetch_one hunyuan_q04c.html "https://hunyuan.tencent.com/"

# ⑱ Anthropic S-1 修订件
fetch_one sec_anthropic2.json "https://data.sec.gov/submissions/CIK0002130357.json" "$UA_SEC"
fetch_one sec_fulltext2.html "https://efts.sec.gov/LATEST/search-index?q=%22free+tier%22&forms=S-1" "$UA_SEC"

# ⑳ 文心 Unlimited OCR 2 下载量
fetch_one hf_baidu_ocr4.json "https://hf-mirror.com/api/models?search=Unlimited-OCR&limit=20"
fetch_one gh_baidu_ocr4.json "https://api.github.com/repos/baidu/Unlimited-OCR"

# ㉑㉒㉓ WebAI / Gemini 4 Carbon / Antigravity
fetch_one opera_webai5.html "https://next.opera.com/web-ai/"
fetch_one opera_webai6.html "https://blogs.opera.com/webai/"
fetch_one gem_carbon1.html "https://deepmind.google/discover/blog/gemini-4-carbon/"
fetch_one gem_carbon2.html "https://blog.google/technology/google-deepmind/gemini-4-carbon/"
fetch_one gem_models3.html "https://ai.google.dev/gemini-api/docs/models"
fetch_one antigravity_pricing3.html "https://antigravity.google/pricing"
fetch_one antigravity_models3.html "https://antigravity.google/models"
fetch_one antigravity_home.html "https://antigravity.google/"

# ㉕ GPT-6.1 Terra Free 档
fetch_one oai_models3.html "https://platform.openai.com/docs/models"
fetch_one oai_pricing3.html "https://openai.com/api/pricing/"
fetch_one oai_gpt61c.html "https://openai.com/index/introducing-gpt-6-1/"

# ㉗㉘ OXR 免费 API 实测
fetch_one oxr_rules2.md "https://docs.somark.ai/free-tier-rules.md"
fetch_one oxr_index2.md "https://docs.somark.ai/oxr/index.md"
fetch_one oxr_llms2.txt "https://docs.somark.ai/llms.txt"
fetch_one oxr_readme2.md "https://raw.githubusercontent.com/SoMarkAI/OXR/main/README.md"
fetch_one oxr_license2.md "https://raw.githubusercontent.com/SoMarkAI/OXR/main/LICENSE"
fetch_one oxr_api1.html "https://api.somark.ai/"
fetch_one oxr_pricing.html "https://docs.somark.ai/pricing.md"

# ㉛ Ollie 官方关停公告原文
fetch_one techdirt_cai2.html "https://techdirt.com/"
fetch_one ollie_site.html "https://ollie.ai/"
fetch_one ollie_blog.html "https://ollie.ai/blog"

# 附加：Anthropic / OpenAI / Google 一手公告（窗口内可能新发）
fetch_one anthropic_pricing2.html "https://claude.com/pricing"
fetch_one anthropic_news3.html "https://www.anthropic.com/news"
fetch_one openai_news2.html "https://openai.com/news/"
fetch_one google_blog2.html "https://blog.google/technology/ai/"
fetch_one hf_blog2.html "https://hf-mirror.com/blog"
fetch_one github_trending2.html "https://github.com/trending"
fetch_one aihot2.html "https://aihot.news/"
echo "DONE 056-special"

# ================= 056 期新增专项 =================
# ① OpenAI 官方「ChatGPT 与 Codex 共用额度」文档（本期头条）
fetch_one oai_hc_codex.html "https://help.openai.com/en/articles/20001625-understanding-chatgpt-and-codex-usage-limits"
fetch_one oai_hc_codex_plans.html "https://help.openai.com/en/articles/11369540-codex-in-chatgpt"
fetch_one oai_hc_plus.html "https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus"
fetch_one oai_hc_ratecard.html "https://help.openai.com/en/articles/11481834-chatgpt-rate-card-business-enterpriseedu-credit-based-pricing"
fetch_one oai_work2.html "https://openai.com/chatgpt-work/"
fetch_one oai_pricing2.html "https://openai.com/api/pricing/"
fetch_one oai_home2.html "https://openai.com/"

# ② OpenAI 付费账号「设备 / 支付卡」上限
fetch_one oai_hc_device1.html "https://help.openai.com/en/articles/10471992-why-can-t-i-create-multiple-accounts"
fetch_one oai_hc_device2.html "https://help.openai.com/en/articles/11381614-chatgpt-security-and-privacy"

# ③ Anthropic Claude Code 系统提示词新增禁令（游戏复刻）
fetch_one anth_code2.html "https://www.anthropic.com/claude-code"
fetch_one anth_support.html "https://support.claude.com/en/articles/9517075-what-is-claude-code"

# ④ 小米 HachimoDock 开源硬件（一手仓库）
fetch_one gh_hach_repo2.json "https://api.github.com/repos/YizhengWw/HachimoDock"
fetch_one gh_hach_readme2.md "https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/README.md"
fetch_one gh_hach_lic2.json "https://api.github.com/repos/YizhengWw/HachimoDock/license"
fetch_one gh_hach_releases.json "https://api.github.com/repos/YizhengWw/HachimoDock/releases?per_page=5"
fetch_one gh_hach_commits.json "https://api.github.com/repos/YizhengWw/HachimoDock/commits?per_page=5"

# ⑤ 量子位窗口内三篇（转述源，对照用）
fetch_one qb_harness2.html "https://www.qbitai.com/2026/11/507038.html"
fetch_one qb_gpt622.html "https://www.qbitai.com/2026/11/507082.html"
fetch_one qb_xiaomi2.html "https://www.qbitai.com/2026/11/507107.html"

# ⑥ decoder 两篇窗口内 OpenAI 报道
fetch_one dec_merger2.html "https://the-decoder.com/openais-upcoming-chat-and-work-merger-in-chatgpt-signals-the-end-of-all-you-can-prompt-pricing/"
fetch_one dec_cap2.html "https://the-decoder.com/openai-is-steering-chatgpt-users-toward-more-paid-usage/"

# ⑦ 055 期挂账项复核
fetch_one ollie_site2.html "https://ollie.ai/"
fetch_one ollie_farewell2.html "https://ollie.ai/farewell"
fetch_one ollie_pricing2.html "https://ollie.ai/pricing"
fetch_one hf_moonshot5.json "https://hf-mirror.com/api/models?author=moonshotai&limit=100&sort=createdAt&direction=-1"
fetch_one hf_k3d.json "https://hf-mirror.com/api/models?search=Kimi-K3&limit=50"
fetch_one sec_anthropic3.json "https://data.sec.gov/submissions/CIK0002130357.json" "$UA_SEC"
fetch_one hf_baidu_ocr5.json "https://hf-mirror.com/api/models?search=Unlimited-OCR&limit=20"
fetch_one gh_baidu_ocr5.json "https://api.github.com/repos/baidu/Unlimited-OCR"
fetch_one or_models6.json "https://openrouter.ai/api/v1/models"
fetch_one or_free8.json "https://openrouter.ai/api/v1/models?max_price=0"
fetch_one opencode_zen5.html "https://opencode.ai/docs/zen"
fetch_one freellm5.html "https://freellm.net/"
fetch_one freellm_or5.html "https://freellm.net/providers/openrouter"
fetch_one runware_pricing7.html "https://runware.ai/pricing"
fetch_one scnet_h6.html "https://www.scnet.cn/"
fetch_one vol_dw_5.html "https://www.volcengine.com/product/doubao-work"
fetch_one mistral_n3.html "https://mistral.ai/news/"
fetch_one mistral_pr3.html "https://docs.mistral.ai/getting-started/models/models_overview/"
fetch_one hf_mistral_readme3.md "https://hf-mirror.com/mistralai/Mistral-Large-4-1T-A52B/raw/main/README.md"
fetch_one autoclaw_cn_m11w2.html "https://autoclaw.zhipuai.cn/blog/news/M11W1/"
fetch_one autoclaw_intl_m11w2.html "https://autoclaw.z.ai/blog/news/M11W1/"
fetch_one kimi_pricing4.html "https://platform.moonshot.cn/docs/pricing/chat"
fetch_one oai_models4.html "https://platform.openai.com/docs/models"
fetch_one deepmind_blog2.html "https://deepmind.google/discover/blog/"
fetch_one gem_carbon3.html "https://deepmind.google/discover/blog/gemini-4-carbon/"
fetch_one gem_carbon4.html "https://blog.google/technology/google-deepmind/gemini-4-carbon/"
fetch_one opera_webai7.html "https://next.opera.com/web-ai/"
fetch_one antigravity_models4.html "https://antigravity.google/models"
fetch_one reflection5.html "https://platform.reflection.ai/pricing"
fetch_one unsloth_bench2.html "https://docs.unsloth.ai/baselines/unsloth-benchmarks"
fetch_one techdirt3.html "https://techdirt.com/"
fetch_one oxr_rules3.md "https://docs.somark.ai/free-tier-rules.md"
fetch_one claude_pricing2.html "https://claude.com/pricing"
fetch_one anthropic_news4.html "https://www.anthropic.com/news"
echo "DONE 056-special-b"
