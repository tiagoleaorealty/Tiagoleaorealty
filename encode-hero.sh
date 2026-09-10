#!/bin/bash
# Encode the hero loop from the source master.
#   ./encode-hero.sh [START_SECONDS] [DURATION_SECONDS]
# Defaults to the first 10 seconds.
set -euo pipefail

# Newest .mov/.mp4 master in this folder that is not the encoded output.
SRC="${SRC:-$(ls -t *.mov *.MOV *.mp4 2>/dev/null | grep -viE '^hero\.(mp4|webm)$' | head -1 || true)}"
START="${1:-0}"
DUR="${2:-10}"

[ -n "$SRC" ] && [ -f "$SRC" ] || { echo "No source video found in this folder."; exit 1; }

# Prefer a real ffmpeg; fall back to the one bundled with imageio-ffmpeg.
FFMPEG="$(command -v ffmpeg || true)"
if [ -z "$FFMPEG" ]; then
  FFMPEG="$(python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())' 2>/dev/null || true)"
fi
[ -n "$FFMPEG" ] || { echo "ffmpeg not found. Install it with:  python3 -m pip install --user imageio-ffmpeg"; exit 1; }

echo "Source: $SRC"

echo "Encoding ${DUR}s from ${START}s of $SRC ..."

# H.264 for every browser. -an strips audio (source has none anyway, but this
# guarantees it), 1080p, CRF 28, faststart so playback can begin before the
# download finishes.
"$FFMPEG" -y -ss "$START" -i "$SRC" -t "$DUR" -an \
  -vf "scale=1920:-2,fps=30" \
  -c:v libx264 -profile:v high -crf 28 -preset slow -pix_fmt yuv420p \
  -movflags +faststart hero.mp4

# VP9 for Chrome/Firefox — ~a third smaller than the H.264 at these settings.
# Note VP9's CRF scale is not H.264's: 36 produced a BIGGER file than the MP4.
"$FFMPEG" -y -ss "$START" -i "$SRC" -t "$DUR" -an \
  -vf "scale=1920:-2,fps=30" \
  -c:v libvpx-vp9 -crf 44 -b:v 0 -row-mt 1 -deadline good -cpu-used 2 \
  hero.webm

# Lighter cuts for phones. Resolution stays 1080p because portrait crops to
# roughly the centre third, where downscaling shows; the saving is bought
# with compression instead.
"$FFMPEG" -y -ss "$START" -i "$SRC" -t "$DUR" -an \
  -vf "scale=1920:-2,fps=30" \
  -c:v libx264 -profile:v high -crf 32 -preset slow -pix_fmt yuv420p \
  -movflags +faststart hero-mobile.mp4

"$FFMPEG" -y -ss "$START" -i "$SRC" -t "$DUR" -an \
  -vf "scale=1920:-2,fps=30" \
  -c:v libvpx-vp9 -crf 50 -b:v 0 -row-mt 1 -deadline good -cpu-used 2 \
  hero-mobile.webm

# Poster is frame 0 of the desktop cut, so the still and the video's first
# frame match and nothing visibly changes when playback starts.
"$FFMPEG" -y -i hero.mp4 -frames:v 1 -q:v 3 hero-poster.jpg

echo
ls -lh hero.mp4 hero.webm hero-mobile.mp4 hero-mobile.webm hero-poster.jpg
echo
echo "Target is under 4 MB for hero.mp4. If it is over, shorten the clip"
echo "before lowering quality:  ./encode-hero.sh 0 8"
