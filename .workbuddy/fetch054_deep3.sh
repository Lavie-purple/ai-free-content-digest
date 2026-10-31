#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
# Simon Willison API credits（053 期窗口内，本期补记）
fetch_one simon_api_credits2.html "https://simonwillison.net/2026/Oct/30/api-credits-benefit-for-eligible-chatgpt-subscriptions/"
fetch_one simon_atom.xml "https://simonwillison.net/atom/everything/"
# Anthropic 官方公告（Ultra）
fetch_one anth_ultra.html "https://www.anthropic.com/news/claude-ultra"
fetch_one anth_pricing2.html "https://www.anthropic.com/pricing"
fetch_one anth_support2.html "https://support.claude.com/en/articles/8324991-about-claude-s-max-plan-usage"
# OXR GitHub API + ModelScope + 官方 API 端点探测
fetch_one oxr_gh_api.json "https://api.github.com/repos/SoMarkAI/OXR"
fetch_one oxr_ms.html "https://modelscope.cn/models/SoMark/OXR-1.0"
fetch_one oxr_docs_en.html "https://docs.somark.cn/api-reference"
# H3-Regenerate 官方 HF
fetch_one h3reg_hfpage.html "https://hf-mirror.com/Efficient-Large-Model/Open-H3-Regenerate-2K"
fetch_one h3reg_readme.md "https://hf-mirror.com/Efficient-Large-Model/Open-H3-Regenerate-2K/raw/main/README.md"
fetch_one h3reg_api.json "https://hf-mirror.com/api/models/Efficient-Large-Model/Open-H3-Regenerate-2K"
# OpenAI robots.txt 官方文
fetch_one oai_prefs.html "https://openai.com/index/helping-websites-express-ai-training-preferences"
# 智元官网 / 灵渠OS
fetch_one agibot.html "https://www.agibot.com/"
fetch_one zhiyuan.html "https://www.zhiyuan-robot.com/"
# ForgeKernel 开源
fetch_one fk_gh.json "https://api.github.com/search/repositories?q=ForgeKernel&sort=updated&order=desc&per_page=20"
fetch_one fk_arxiv.html "https://arxiv.org/abs/2510.12345"
echo DONE-054-deep3
