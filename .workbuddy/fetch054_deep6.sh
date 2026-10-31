#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_054
fetch_one(){ name="$1"; url="$2"; code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null); size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' '); echo "$code ${size:-0} $name"; }
export -f fetch_one; export UA D
# OXR README 早期版本（确定 Free API 何时进仓库）
fetch_one oxr_readme_1005.md "https://raw.githubusercontent.com/SoMarkAI/OXR/10-05-2026/README.md"
fetch_one oxr_readme_init.md "https://raw.githubusercontent.com/SoMarkAI/OXR/main/README.md"
# OpenAI API credits 官方页候选
fetch_one oai_help_credits.html "https://help.openai.com/en/articles/11481898-chatgpt-api-credits"
fetch_one oai_billing.html "https://help.openai.com/en/articles/8156019"
fetch_one oai_pricing_api.html "https://openai.com/api/pricing/"
# ForgeKernel
fetch_one fk_repo.html "https://github.com/ModelEngine-Group/ForgeKernel"
fetch_one fk_search2.json "https://api.github.com/search/repositories?q=ForgeKernel+in:name&sort=stars&order=desc&per_page=20"
fetch_one fk_hf.json "https://hf-mirror.com/api/models?search=ForgeKernel&limit=20"
# OpenBMB 智能进化实验室
fetch_one openbmb.html "https://github.com/OpenBMB"
echo DONE-054-deep6
