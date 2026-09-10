# Hero video

The homepage hero plays a short silent loop over the still photo. The still
(`Real Estate Photo.jpg`) is the fast path and never moves — it is what paints
first and what search engines measure. The video is layered on top and is
skipped entirely whenever playing it would cost more than it gives.

## Adding or replacing the video

Run `./encode-hero.sh`, which produces all five files: **`hero.mp4`** and
**`hero.webm`** for desktop, **`hero-mobile.mp4`** and **`hero-mobile.webm`**
(same 1080p frame, more compressed) for phones, and **`hero-poster.jpg`**.
Nothing else to wire up. If they are absent the element removes itself and the still
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

Current files, from a 1920x1080 10.8s master (19 MB): **hero.mp4 3.8 MB,
hero.webm 2.6 MB**, both exactly 10.00s.

Two things worth knowing for next time:

- **VP9's CRF scale is not H.264's.** At `-crf 36` the WebM came out at 5.1 MB,
  *larger* than the 3.8 MB MP4, which defeats the point of shipping it. 44 is
  the value that actually wins, and the first frames of the two files differ by
  about 2/255 per channel, so nothing visible is lost.
- **macOS's built-in `avconvert` cannot do this.** Its presets have no bitrate
  control: the same clip came out 12 MB at 1080p and still 8.8 MB at 720p.

**The poster is a frame of the video itself** (`hero-poster.jpg`, extracted
from `hero.mp4` frame 0), used both as `#hero`'s `background-image` and the
video's `poster`. That is deliberate: with a different photo there, the hero
visibly cross-faded from one image to another when the video arrived. Matching
them means the still simply starts moving.

Regenerate it whenever the clip changes:

```bash
ffmpeg -y -i hero.mp4 -frames:v 1 -q:v 3 hero-poster.jpg
```

## What the loader does

- Never sets `src` in the markup, so the video is off the page's critical path.
- Waits for the browser to be idle (`requestIdleCallback`, 2.5s timeout) before
  fetching anything.
- Fades in only on `canplay`, over the still — no flash, no layout shift.
- Serves WebM/VP9 where supported and MP4 to Safari.
- Pauses when scrolled out of view and when the tab is hidden, so a looping
  decode is not burning CPU and battery down the page.
- Serves the lighter mobile cut under 900px. Resolution is not reduced there:
  portrait crops to roughly the centre third of a 16:9 frame, so a smaller
  encode would look soft exactly where it is magnified. The saving comes from
  compression — 2.3 MB / 1.6 MB against 3.8 MB / 2.6 MB.
- Skips the video entirely on `prefers-reduced-motion` and on `Save-Data` or
  2g connections.
- iOS autoplay needs `muted`, `playsinline` and a programmatic `play()`. The
  order matters: with `preload="none"` Safari will not fetch on `load()`
  alone, so waiting for `canplay` before calling `play()` deadlocks — the
  fetch never starts, `canplay` never fires, nothing plays. The loader sets
  `preload='auto'`, calls `play()` immediately, and reveals on whichever of
  `loadeddata`/`playing` arrives first.
- Low Power Mode refuses muted autoplay outright. The first `touchstart`,
  `pointerdown` or `scroll` starts it instead of leaving a frozen frame.
- Feature tests use `typeof x === 'function'`, not `'x' in window`: Safari has
  no `requestIdleCallback`, and an `in` check passes on a property that exists
  but is not callable.
- Removes itself on any load error.
