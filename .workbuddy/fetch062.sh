#!/bin/bash
# 062 期主抓取：284 源（与 060 期同一清单）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_062
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 40 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  if [ "$code" = "000" ] && [ ! -f "$D/$name" ]; then : > "$D/$name"; fi
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
export -f fetch_one
export UA D
cat tmp_062_list.txt | xargs -P 16 -I{} bash -c 'IFS="|" read -r n u <<< "{}"; fetch_one "$n" "$u"'
echo "DONE 062"
