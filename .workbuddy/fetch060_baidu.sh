#!/bin/bash
# 060 期专项：百度 ERNIE-5.5-Flash-Base 开源一手核验（窗口内 11/5 发布）
# 四层开放：能用 / 能下载 / 能跑 / 能商用 —— 前三层看仓库，第四层看 LICENSE 条款
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_060_s
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 50 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  if [ "$code" = "000" ] && [ ! -f "$D/$name" ]; then : > "$D/$name"; fi
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
fetch_one ernie_official_blog.html   "https://ernie.baidu.com/release/ernie-5-5-flash-base/"
fetch_one ernie_official_zh.html     "https://ernie.baidu.com/zh/release/ernie-5-5-flash-base/"
fetch_one hf_ernie_fp8.json          "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base"
fetch_one hf_ernie_bf16.json         "https://hf-mirror.com/api/models/baidu/ERNIE-5.5-Flash-Base-BF16"
fetch_one hf_ernie_readme.md         "https://hf-mirror.com/baidu/ERNIE-5.5-Flash-Base/raw/main/README.md"
fetch_one hf_ernie_license.txt       "https://hf-mirror.com/baidu/ERNIE-5.5-Flash-Base/raw/main/LICENSE"
fetch_one hf_baidu_list.json         "https://hf-mirror.com/api/models?author=baidu&limit=100&sort=createdAt&direction=-1"
fetch_one gh_vllm_ernie.json         "https://api.github.com/repos/baidu/vLLM-ERNIE"
# 腾讯 Hy4 开源核验（乌镇峰会「发布即全面开源」口径）
fetch_one hf_tencent_list.json       "https://hf-mirror.com/api/models?author=tencent&limit=100&sort=createdAt&direction=-1"
fetch_one hf_search_hy4.json         "https://hf-mirror.com/api/models?search=Hy4&limit=30"
fetch_one gh_tencent_hy4.json        "https://api.github.com/repos/Tencent-Hunyuan/Hy4"
echo "DONE 060BAIDU"
