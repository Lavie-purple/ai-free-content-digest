#!/bin/bash
# 060 期主抓取：284 源（与 059 期同一清单，用户本轮再次给出 T0–T4 分级，未增删）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
D=tmp_060
mkdir -p $D
fetch_one(){
  name="$1"; url="$2"
  code=$(curl -sS -m 40 -A "$UA" -L "$url" -o "$D/$name" -w "%{http_code}" 2>/dev/null)
  # 058 期纪律：000 时 curl 根本不建文件，下游会把「没有文件」误读成「文件读不到」→ 写空占位
  if [ "$code" = "000" ] && [ ! -f "$D/$name" ]; then : > "$D/$name"; fi
  size=$(wc -c < "$D/$name" 2>/dev/null | tr -d ' ')
  echo "$code ${size:-0} $name"
}
export -f fetch_one
export UA D
cat tmp_060_list.txt | xargs -P 16 -I{} bash -c 'IFS="|" read -r n u <<< "{}"; fetch_one "$n" "$u"'
echo "DONE 060"
