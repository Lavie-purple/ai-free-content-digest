#!/bin/bash
# 053 期：052 期脚注③「下一轮强制动作」21 条专项实访（销项优先）
# ⚠️ 合规 UA：SEC EDGAR 等站点要求带联系方式的 User-Agent（避坑 232）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
UA_SEC="AI-Free-Content-Report research@example.com"
D=tmp_053
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"; ua="${3:-$UA}"
  code=$(curl -sS -m 45 -A "$ua" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
export -f fetch_one
export UA UA_SEC D

# ① 豆包工作 30 天订阅（连续第 6 期零命中）
fetch_one vol_doubao_e.html "https://www.volcengine.com/activity/doubao"
fetch_one vol_doubao_f.html "https://www.volcengine.com/activity/doubao/"
fetch_one vol_doubao_g.html "https://www.volcengine.com/product/doubao"
fetch_one vol_doubao_h.html "https://www.volcengine.com/activity/doubao?tab=detail"
# ② MOSS-Image 官方一手页全文（052 期已定位，本期必须补登）
fetch_one moss_image.html "https://openmoss.ai/blog/cn/moss-image/"
fetch_one moss_cn.html "https://openmoss.ai/blog/cn/"
# ③ AutoClaw 国内站 M10W5 是否发布
fetch_one ac_cn_m10w5b.html "https://autoclaw.zhipuai.cn/blog/news/M10W5"
fetch_one ac_cn_m10w4b.html "https://autoclaw.zhipuai.cn/blog/news/M10W4"
fetch_one ac_cn_news.html "https://autoclaw.zhipuai.cn/blog/news"
# ④ AutoClaw 国际站 M10W4 残留文案是否已改
fetch_one ac_intl_m10w4b.html "https://autoclaw.z.ai/blog/news/M10W4"
fetch_one ac_intl_news2.html "https://autoclaw.z.ai/blog/news"
# ⑤ Kimi K3.1 Pro 权重是否放出
fetch_one hf_moonshot3.json "https://hf-mirror.com/api/models?author=moonshotai&limit=100&sort=createdAt&direction=-1"
fetch_one hf_k3b.json "https://hf-mirror.com/api/models?search=Kimi-K3&limit=50"
fetch_one moonshot_github2.html "https://github.com/MoonshotAI"
# ⑥ K2 系列 10/31 停新是否如期
fetch_one kimi_k2_stop.html "https://platform.moonshot.cn/docs/guide/kimi-k2-deprecation"
fetch_one kimi_pricing2.html "https://platform.kimi.com/docs/pricing/chat"
# ⑦ OpenRouter 全量 + free 逐条 diff
fetch_one or_models4.json "https://openrouter.ai/api/v1/models"
fetch_one or_free6.json "https://openrouter.ai/api/v1/models?maxPrice=0"
# ⑧ OpenCode 清单 + LongCat 是否回归
fetch_one opencode_zen3.html "https://opencode.ai/docs/zen"
fetch_one longcat2.html "https://github.com/meituan-longcat"
# ⑨ Runware 促销表 14 条 + 7 条过期条目是否被清理
fetch_one runware_pricing5.html "https://runware.ai/pricing"
fetch_one runware_kling6.html "https://runware.ai/kling-4"
# ⑩ Unsloth 官网量化基准页全文
fetch_one unsloth_docs2.html "https://docs.unsloth.ai/"
fetch_one unsloth_gguf2.html "https://hf-mirror.com/unsloth"
# ⑪⑫ 反复失败的源
fetch_one mistral_news3.html "https://mistral.ai/news"
fetch_one reflection3.html "https://platform.reflection.ai/pricing"
# ⑬ 老混元 Q04
fetch_one hunyuan_q04b.html "https://hunyuan.tencent.com/"
# ⑭ Anthropic S-1 修订件
fetch_one sec_anthropic.json "https://data.sec.gov/submissions/CIK0002130357.json" "$UA_SEC"
fetch_one sec_browse.html "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=anthropic&type=S-1" "$UA_SEC"
# ⑮ freellm 九条逐条归因
fetch_one freellm3.html "https://freellm.net/"
fetch_one freellm_or3.html "https://freellm.net/providers/openrouter"
# ⑯ 文心 Unlimited OCR 2 下载量
fetch_one hf_baidu_ocr3.json "https://hf-mirror.com/api/models?search=Unlimited-OCR&limit=20"
fetch_one modelscope_ocr.html "https://modelscope.cn/models/Baidu-ai/Unlimited-OCR"
# ⑰ WebAI 完整 API 文档
fetch_one opera_webai3.html "https://next.opera.com/web-ai/"
fetch_one opera_webai4.html "https://blogs.opera.com/webai/"
# ⑱ Gemini 4 Carbon 公告 + Gemini API 定价 + AI Studio
fetch_one gemini_pricing2.html "https://ai.google.dev/gemini-api/docs/pricing"
fetch_one aistudio2.html "https://aistudio.google.com/"
fetch_one gblog_ai2.html "https://blog.google/technology/google-deepmind/"
fetch_one gemini_models2.html "https://ai.google.dev/gemini-api/docs/models"
fetch_one gemini_models3.html "https://ai.google.dev/gemini-api/docs/models/gemini"
# ⑲ Antigravity 免费档模型清单
fetch_one antigravity_pricing2.html "https://antigravity.google/pricing"
fetch_one antigravity_models2.html "https://antigravity.google/models"
# ⑳ OpenRouter CSAM 公告逐模型
fetch_one or_csam2.html "https://openrouter.ai/announcements/csam-screening-across-openrouter"
# ㉑ GPT-6.1 Terra Free 档细表（连续第 5 期 403）
fetch_one oai_models2.html "https://platform.openai.com/docs/models"
fetch_one oai_pricing2.html "https://openai.com/api/pricing/"
fetch_one oai_gpt61b.html "https://openai.com/index/introducing-gpt-6-1/"
# 附加：aihot.news 新增入口 + 聚合器
fetch_one aihot_news2.html "https://aihot.news/"
fetch_one radarai.html "https://radarai.top/"
fetch_one aitop100.html "https://aitop100.cn/"
fetch_one bestblogs.html "https://www.bestblogs.dev/"
# 附加：SEC 全库检索（合规 UA）
fetch_one sec_fulltext.html "https://efts.sec.gov/LATEST/search-index?q=%22free+tier%22&forms=S-1" "$UA_SEC"
echo "DONE 053-special"
