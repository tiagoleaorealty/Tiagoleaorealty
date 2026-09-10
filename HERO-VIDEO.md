# Hero video

The homepage hero plays a short silent loop over the still photo. The still
(`Real Estate Photo.jpg`) is the fast path and never moves — it is what paints
first and what search engines measure. The video is layered on top and is
skipped entirely whenever playing it would cost more than it gives.

## Adding or replacing the video

Drop two files in the repo root: **`hero.mp4`** and **`hero.webm`**. Nothing
else to wire up. If they are absent the element removes itself and the still
simply stays, so the site is never broken by a missing file.

macOS's built-in `avconvert` is **not** usable here: its presets have no
bitrate control, so even 540p came out at 6.4 MB for 10 seconds. Install
ffmpeg once (Homebrew is not installed on this machine either):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
brew install ffmpeg
```

Then run the helper, which wraps both encodes with the settings below:

```bash
./encode-hero.sh 0 10
```

The arguments are start-second and duration. The raw commands it runs, from a
source clip (trim to the 6–10 seconds you actually want first — a short loop
beats a long clip):

```bash
ffmpeg -i source.mov -t 8 -an -vf "scale=1920:-2,fps=30" -c:v libx264 -profile:v high -crf 28 -preset slow -movflags +faststart hero.mp4
```

```bash
ffmpeg -i source.mov -t 8 -an -vf "scale=1920:-2,fps=30" -c:v libvpx-vp9 -crf 36 -b:v 0 -row-mt 1 hero.webm
```

What each part is doing, since these are the settings that decide whether it
feels laggy:

- `-an` strips the audio track. It halves the file and it is also what makes
  browsers allow autoplay at all.
- `-t 8` caps the length. A loop that reads as ambient does not need to be long.
- `scale=1920:-2` — 1080p. 4K in a hero is invisible and costs several times
  the bytes and the decode.
- `-crf 28` (H.264) / `-crf 36` (VP9) are the quality dials. Higher number,
  smaller file. Nudge down if it looks soft on your footage.
- `-movflags +faststart` moves the index to the front of the MP4 so it can
  start playing before it has finished downloading.

**Target under 4 MB for the MP4.** Check with `ls -lh hero.*`. If it is far
over, shorten the clip before you lower the quality.

The poster is the existing hero still. If you change the hero photo, update the
`poster` attribute on `#hero-video` in `index.html` to match, or the fade will
jump.

## What the loader does

- Never sets `src` in the markup, so the video is off the page's critical path.
- Waits for the browser to be idle (`requestIdleCallback`, 2.5s timeout) before
  fetching anything.
- Fades in only on `canplay`, over the still — no flash, no layout shift.
- Serves WebM/VP9 where supported and MP4 to Safari.
- Pauses when scrolled out of view and when the tab is hidden, so a looping
  decode is not burning CPU and battery down the page.
- Skips the video entirely on: screens under 900px, `prefers-reduced-motion`,
  and `Save-Data` / 2g connections.
- Removes itself on any load error.
