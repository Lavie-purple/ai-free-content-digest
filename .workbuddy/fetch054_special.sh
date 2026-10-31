#!/bin/bash
# 054 期：053 期脚注③「下一轮强制动作」21 条专项实访（销项优先）
# ⚠️ 合规 UA：SEC EDGAR 等站点要求带联系方式的 User-Agent（避坑 232）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
UA_SEC="AI-Free-Content-Report research@example.com"
D=tmp_054
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"; ua="${3:-$UA}"
  code=$(curl -sS -m 45 -A "$ua" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
export -f fetch_one
export UA UA_SEC D

# ① 豆包工作 30 天订阅（连续第 7 期零命中）
fetch_one vol_doubao_e.html "https://www.volcengine.com/activity/doubao"
fetch_one vol_doubao_f.html "https://www.volcengine.com/activity/doubao/"
fetch_one vol_doubao_g.html "https://www.volcengine.com/product/doubao"
fetch_one vol_doubao_h.html "https://www.volcengine.com/activity/doubao?tab=detail"
# ② 国家超算互联网 官方页「夜间免费」栏
fetch_one scnet_home.html "https://www.scnet.cn/"
fetch_one scnet_home2.html "https://scnet.cn/"
fetch_one scnet_price.html "https://www.scnet.cn/price"
fetch_one scnet_token.html "https://www.scnet.cn/token"
# ③ Mistral 官方公告页（连续第 13 次 000）
fetch_one mistral_news3.html "https://mistral.ai/news"
fetch_one mistral_oss.html "https://mistral.ai/news/mistral-large-4-oss/"
fetch_one mistral_docs.html "https://docs.mistral.ai/"
fetch_one mistral_console.html "https://console.mistral.ai/"
# ④ Mistral Large 4 模型卡与许可证（更新检查）
fetch_one hf_mistral_full.json "https://hf-mirror.com/api/models/mistralai/Mistral-Large-4-1T-A52B"
fetch_one hf_mistral_readme.md "https://hf-mirror.com/mistralai/Mistral-Large-4-1T-A52B/raw/main/README.md"
fetch_one hf_mistral_license.md "https://hf-mirror.com/mistralai/Mistral-Large-4-1T-A52B/raw/main/LICENSE"
fetch_one hf_mistral_commits.json "https://hf-mirror.com/api/models/mistralai/Mistral-Large-4-1T-A52B/commits/main"
fetch_one hf_mistral_tree.json "https://hf-mirror.com/api/models/mistralai/Mistral-Large-4-1T-A52B/tree/main"
# ⑤ AutoClaw 国际站 M10W4 残留文案 / 国内站 M10W5
fetch_one ac_cn_m10w5b.html "https://autoclaw.zhipuai.cn/blog/news/M10W5"
fetch_one ac_cn_m10w4b.html "https://autoclaw.zhipuai.cn/blog/news/M10W4"
fetch_one ac_cn_news.html "https://autoclaw.zhipuai.cn/blog/news"
fetch_one ac_intl_m10w4b.html "https://autoclaw.z.ai/blog/news/M10W4"
fetch_one ac_intl_news2.html "https://autoclaw.z.ai/blog/news"
# ⑥ Kimi K3.1 Pro 权重是否在 11/4 前放出 + K2 系列 10/31 停新
fetch_one hf_moonshot3.json "https://hf-mirror.com/api/models?author=moonshotai&limit=100&sort=createdAt&direction=-1"
fetch_one hf_k3b.json "https://hf-mirror.com/api/models?search=Kimi-K3&limit=50"
fetch_one kimi_k2_stop.html "https://platform.moonshot.cn/docs/guide/kimi-k2-thinking-deprecation"
fetch_one kimi_k2_stop2.html "https://platform.moonshot.cn/docs/guide/kimi-k2-deprecation"
fetch_one kimi_pricing2.html "https://platform.kimi.com/docs/pricing/chat"
# ⑦ OpenRouter 全量逐条 diff
fetch_one or_models4.json "https://openrouter.ai/api/v1/models"
fetch_one or_free6.json "https://openrouter.ai/api/v1/models?max_price=0"
# ⑧ OpenCode 免费档清单 + LongCat 是否回归
fetch_one opencode_zen3.html "https://opencode.ai/docs/zen"
fetch_one longcat2.html "https://github.com/meituan-longcat"
# ⑨ Runware 促销表 14 条 + 9 条过期条目是否被清理
fetch_one runware_pricing5.html "https://runware.ai/pricing"
fetch_one runware_kling6.html "https://runware.ai/kling-4"
# ⑩ Unsloth 官网量化基准页
fetch_one unsloth_docs2.html "https://docs.unsloth.ai/"
# ⑪⑫ 反复失败的源
fetch_one reflection3.html "https://platform.reflection.ai/pricing"
fetch_one googleai_pricing.html "https://ai.google.dev/gemini-api/docs/pricing"
fetch_one aistudio2.html "https://aistudio.google.com/"
fetch_one gblog_ai2.html "https://blog.google/technology/ai/"
fetch_one deepmind2.html "https://deepmind.google/discover/blog/"
# ⑬ 老混元 Q04
fetch_one hunyuan_q04b.html "https://hunyuan.tencent.com/"
# ⑭ freellm 计数器
fetch_one freellm3.html "https://freellm.net/"
fetch_one freellm_or3.html "https://freellm.net/providers/openrouter"
# ⑮ 文心 Unlimited OCR 2 下载量
fetch_one hf_baidu_ocr3.json "https://hf-mirror.com/api/models?search=Unlimited-OCR&limit=20"
fetch_one gh_baidu_ocr3.json "https://api.github.com/repos/baidu/Unlimited-OCR"
# ⑯ Gemini 4 Carbon 公告页 + Antigravity 免费档
fetch_one gemini_models2.html "https://ai.google.dev/gemini-api/docs/models"
fetch_one antigravity_pricing2.html "https://antigravity.google/pricing"
fetch_one antigravity_models2.html "https://antigravity.google/models"
# ⑰ OpenRouter CSAM 公告 + GPT-6.1 Terra Free 档
fetch_one or_csam2.html "https://openrouter.ai/announcements/csam-screening-across-openrouter"
fetch_one oai_models2.html "https://platform.openai.com/docs/models"
fetch_one oai_pricing2.html "https://openai.com/api/pricing/"
fetch_one oai_gpt61b.html "https://openai.com/index/introducing-gpt-6-1/"
# ⑱ WebAI 完整 API 文档
fetch_one opera_webai3.html "https://next.opera.com/web-ai/"
fetch_one opera_webai4.html "https://blogs.opera.com/webai/"
# ⑲ Character.ai 破产案原始报道
fetch_one techdirt_cai.html "https://techdirt.com/"
# ⑳ 新增：Mistral Large 4 demo 免费预算的额度数字 / 日历日
fetch_one hf_mistral_disc.html "https://hf-mirror.com/mistralai/Mistral-Large-4-1T-A52B/discussions"
# 附加：SEC 全库检索（合规 UA）
fetch_one sec_fulltext.html "https://efts.sec.gov/LATEST/search-index?q=%22free+tier%22&forms=S-1" "$UA_SEC"
fetch_one sec_anthropic.json "https://data.sec.gov/submissions/CIK0002130357.json" "$UA_SEC"
# 附加：Mistral Large 4 官方 X / GitHub
fetch_one mistral_github.html "https://github.com/mistralai"
fetch_one mistral_vibe.html "https://github.com/mistralai/mistral-vibe"
echo "DONE 054-special"
