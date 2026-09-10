#!/bin/bash
# Encode the hero loop from the source master.
#   ./encode-hero.sh [START_SECONDS] [DURATION_SECONDS]
# Defaults to the first 10 seconds.
set -euo pipefail

SRC="WEBSITE VIDEO.mov"
START="${1:-0}"
DUR="${2:-10}"

[ -f "$SRC" ] || { echo "Missing source: $SRC"; exit 1; }
command -v ffmpeg >/dev/null || { echo "ffmpeg not installed — run: brew install ffmpeg"; exit 1; }

echo "Encoding ${DUR}s from ${START}s of $SRC ..."

# H.264 for every browser. -an strips audio (source has none anyway, but this
# guarantees it), 1080p, CRF 28, faststart so playback can begin before the
# download finishes.
ffmpeg -y -ss "$START" -i "$SRC" -t "$DUR" -an \
  -vf "scale=1920:-2,fps=30" \
  -c:v libx264 -profile:v high -crf 28 -preset slow -pix_fmt yuv420p \
  -movflags +faststart hero.mp4

# VP9 for Chrome/Firefox — typically 30-40% smaller than the H.264.
ffmpeg -y -ss "$START" -i "$SRC" -t "$DUR" -an \
  -vf "scale=1920:-2,fps=30" \
  -c:v libvpx-vp9 -crf 36 -b:v 0 -row-mt 1 \
  hero.webm

echo
ls -lh hero.mp4 hero.webm
echo
echo "Target is under 4 MB for hero.mp4. If it is over, shorten the clip"
echo "before lowering quality:  ./encode-hero.sh 0 8"
