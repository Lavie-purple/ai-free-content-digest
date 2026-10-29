#!/bin/bash
# 052 期：051 期强制动作专项实访（销项优先）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_052
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 40 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
export -f fetch_one
export UA D

# ① 豆包工作 30 天订阅（连续第 5 期 React 空壳）—— 换四条路径试
fetch_one vol_doubao_a.html "https://www.volcengine.com/activity/doubao"
fetch_one vol_doubao_b.html "https://www.volcengine.com/activity/doubao/"
fetch_one vol_doubao_c.html "https://www.volcengine.com/activity/2024doubao"
fetch_one vol_doubao_d.html "https://www.volcengine.com/product/doubao"
# ② AutoClaw 国际站 40M vs 100 million 矛盾
fetch_one ac_intl.html "https://autoclaw.z.ai/blog/news"
fetch_one ac_intl_m10w4.html "https://autoclaw.z.ai/blog/news/M10W4"
fetch_one ac_intl_m10w3.html "https://autoclaw.z.ai/blog/news/M10W3"
fetch_one ac_cn_m10w5.html "https://autoclaw.zhipuai.cn/blog/news/M10W5"
fetch_one ac_cn_m10w4.html "https://autoclaw.zhipuai.cn/blog/news/M10W4"
# ③ GPT-6.1 Terra Free 档细表（连续 4 期 403）
fetch_one oai_models.html "https://platform.openai.com/docs/models"
fetch_one oai_pricing.html "https://openai.com/api/pricing/"
fetch_one oai_gpt61.html "https://openai.com/index/introducing-gpt-6-1/"
# ④ Kimi K3.1 Pro 权重是否放出
fetch_one hf_moonshot2.json "https://hf-mirror.com/api/models?author=moonshotai&limit=100&sort=createdAt&direction=-1"
fetch_one hf_k3search.json "https://hf-mirror.com/api/models?search=Kimi-K3&limit=50"
fetch_one kimi_k3_1.html "https://platform.kimi.com/docs/guide/kimi-k3-1-pro-quickstart"
# ⑥ OpenRouter 全量 + free 逐条 diff
fetch_one or_models3.json "https://openrouter.ai/api/v1/models"
fetch_one or_free5.json "https://openrouter.ai/api/v1/models?maxPrice=0"
# ⑦ OpenCode 清单 + LongCat 是否回归
fetch_one opencode_zen2.html "https://opencode.ai/docs/zen"
fetch_one longcat.html "https://github.com/meituan-longcat"
# ⑧ Runware 促销表是否稳定 + Kling 15% 是否移除
fetch_one runware_pricing4.html "https://runware.ai/pricing"
fetch_one runware_kling5.html "https://runware.ai/kling-4"
# ⑨ Unsloth 官网量化基准页
fetch_one unsloth_docs.html "https://docs.unsloth.ai/"
fetch_one unsloth_gguf.html "https://huggingface.co/unsloth"
# ⑩⑪ 反复失败的源
fetch_one mistral_news2.html "https://mistral.ai/news"
fetch_one reflection2.html "https://platform.reflection.ai/pricing"
# ⑫ 老混元 Q04
fetch_one hunyuan_q04.html "https://hunyuan.tencent.com/"
# ⑬ Anthropic S-1 附信
fetch_one anthropic_s1.html "https://www.anthropic.com/news/claude-s-1"
# ⑭ freellm 9 条归因
fetch_one freellm2.html "https://freellm.net/"
fetch_one freellm_or2.html "https://freellm.net/providers/openrouter"
# ⑮ 文心 OCR2 下载量
fetch_one hf_baidu_ocr2.json "https://hf-mirror.com/api/models?search=Unlimited-OCR&limit=20"
# ⑯ WebAI 完整 API 文档
fetch_one opera_webai.html "https://next.opera.com/web-ai/"
fetch_one opera_webai2.html "https://blogs.opera.com/webai/"
# ⑰ Gemini 4 Carbon 发布公告 + Gemini API 定价
fetch_one gemini_pricing.html "https://ai.google.dev/gemini-api/docs/pricing"
fetch_one aistudio.html "https://aistudio.google.com/"
fetch_one gblog_gemini.html "https://blog.google/technology/google-deepmind/"
fetch_one gemini_models.html "https://ai.google.dev/gemini-api/docs/models"
# ⑱ Antigravity 免费档模型清单
fetch_one antigravity_pricing.html "https://antigravity.google/pricing"
fetch_one antigravity_models.html "https://antigravity.google/models"
# ⑳ OpenRouter CSAM 公告逐模型
fetch_one or_csam.html "https://openrouter.ai/announcements/csam-screening-across-openrouter"
echo "DONE 052-special"
