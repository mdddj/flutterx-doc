#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if ! command -v cwebp >/dev/null 2>&1; then
  echo "cwebp is required but not installed" >&2
  exit 1
fi

tmp_map="$(mktemp)"
trap 'rm -f "$tmp_map"' EXIT

while IFS= read -r -d '' src; do
  rel="${src#docs/assets/images/}"
  dst="${src%.*}.webp"

  cwebp -q 88 -m 6 -mt -af "$src" -o "$dst" >/dev/null 2>&1

  src_size="$(wc -c < "$src" | tr -d ' ')"
  dst_size="$(wc -c < "$dst" | tr -d ' ')"

  if [[ "$dst_size" -ge "$src_size" ]]; then
    rm -f "$dst"
    continue
  fi

  printf '%s\t%s\n' "assets/images/$rel" "assets/images/${rel%.*}.webp" >> "$tmp_map"
done < <(find docs/assets/images -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \) -print0)

if [[ ! -s "$tmp_map" ]]; then
  echo "No images were converted" >&2
  exit 0
fi

while IFS=$'\t' read -r old_path new_path; do
  while IFS= read -r -d '' doc; do
    perl -0pi -e "s#\Q$old_path\E#$new_path#g" "$doc"
  done < <(find docs -type f \( -name '*.md' -o -name '*.json' -o -name '*.yml' \) -print0)
done < "$tmp_map"

while IFS=$'\t' read -r old_path _; do
  rm -f "docs/$old_path"
done < "$tmp_map"

echo "Converted $(wc -l < "$tmp_map" | tr -d ' ') images to WebP"
