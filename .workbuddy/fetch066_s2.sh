#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_066_s
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 45 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  if [ ! -f "$D/$name" ]; then : > "$D/$name"; fi
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
export -f fetch_one
export UA D
cat > $D/list2.txt <<'EOF'
openai_veterans.html|https://openai.com/index/chatgpt-plus-for-veterans
baidu_ernie_home.html|https://ernie.baidu.com/
baidu_qianfan.html|https://cloud.baidu.com/product/wenxinworkshop
baidu_qianfan_pricing.html|https://cloud.baidu.com/doc/WENXINWORKSHOP/s/hlrk4akp7
leiphone_ernie_open.html|https://www.leiphone.com/category/ai/b3ASOkGmqznTQWCH.html
leiphone_zaobao_1112.html|https://www.leiphone.com/category/zaobao/eX3oZsWdbpVbMcto.html
google_blog_ai.html|https://blog.google/technology/ai/
deepmind_models.html|https://deepmind.google/models/gemini/
cloudflare_blog.html|https://blog.cloudflare.com/
cloudflare_pricing.html|https://www.cloudflare.com/plans/developer-platform/
hf_author_baidu.json|https://hf-mirror.com/api/models?author=baidu&limit=100&sort=createdAt&direction=-1
hf_baidu_new.json|https://hf-mirror.com/api/models?search=ERNIE&limit=50&sort=createdAt&direction=-1
or_baidu.json|https://openrouter.ai/api/v1/models?search=ernie
or_gemini.json|https://openrouter.ai/api/v1/models?search=gemini-4
anthropic_newsroom.html|https://www.anthropic.com/news
openai_pricing.html|https://openai.com/chatgpt/pricing/
EOF
xargs -P 8 -I{} bash -c 'IFS="|" read -r n u <<< "{}"; fetch_one "$n" "$u"' < $D/list2.txt
echo "DONE 066S2"
