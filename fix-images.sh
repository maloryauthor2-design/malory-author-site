#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# Fix broken images — rename uppercase .JPG / Logo.jpg
# references to match the actual lowercase filenames.
#
# Run from the repo root:  bash fix-images.sh
# ──────────────────────────────────────────────────────────────

set -euo pipefail

FILES=(index.html books.html about.html)

echo "=== Fixing image filename case in HTML ==="

for f in "${FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "  ⚠ $f not found — skipping"
    continue
  fi

  # Fix uppercase .JPG → .jpg
  sed -i '' 's/hero-bg\.JPG/hero-bg.jpg/g' "$f"
  sed -i '' 's/welcome-cover\.JPG/welcome-cover.jpg/g' "$f"
  sed -i '' 's/murder-cover\.JPG/murder-cover.jpg/g' "$f"
  sed -i '' 's/psyker-1\.JPG/psyker-1.jpg/g' "$f"
  sed -i '' 's/pts-cover\.JPG/pts-cover.jpg/g' "$f"
  sed -i '' 's/curator-cover\.JPG/curator-cover.jpg/g' "$f"
  sed -i '' 's/cuckoo-cover\.JPG/cuckoo-cover.jpg/g' "$f"

  # Fix Logo.jpg → logo.jpg (capital L)
  sed -i '' 's/Logo\.jpg/logo.jpg/g' "$f"

  echo "  ✓ $f"
done

echo ""
echo "──────────────────────────────────────────────────"
echo "Done. Now run:"
echo "  git add index.html books.html about.html"
echo "  git commit -m \"Fix broken images: uppercase to lowercase filenames\""
echo "  git push"
echo "──────────────────────────────────────────────────"
