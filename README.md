# Short-form production pipeline

Turns a script + two recordings into a finished vertical short in the format that
outperforms in this niche. Everything here runs locally on this machine.

**The scripts now live in the `avatar-video-engine` skill**
(`~/.claude/skills/avatar-video-engine/scripts/`), not in this folder, so one copy
is shared across projects and fixes land everywhere at once. The old local copies
are kept as `*.py.superseded` and can be deleted. `make.bat` already points at the
skill; only the paths below changed.

## The format

Both 163k-view reference videos (Nate Herk) use the same structure, and neither
ever cuts to a full-frame face:

- **Top ~55%** — screen recording. Something is always happening.
- **Bottom ~45%** — you, talking.
- **Captions** — bold uppercase, heavy outline, one word accented at a time.
- **Open on the finished artifact**, not on the setup or a greeting.
- **Full promise inside 3 seconds.**
- **Close on a CTA** to the long-form version.

The split is also why an AI-avatar lower pane is viable: your face occupies ~45%
of frame height while attention sits on the terminal above it. Lip-sync artifacts
that would be obvious full-frame survive easily at that scale.

## Daily workflow

```bash
# 0. What should today's episode be about?
py -3.10 trend_watch.py

#    Ranks two signals: videos beating their own channel's median (what performs
#    in this niche) and recent Hacker News stories (what broke, before anyone
#    has covered it). If nothing clears the bar, use the next episode in the
#    30-day plan - that is the intended fallback, not a failure.

# 1. Record two things: your screen doing the thing, and you talking.
#    Frame yourself for a LOWER-THIRD pane, not a full-frame hero shot.

# 2. Captions from the voiceover (word timings come from the audio itself)
set SKILL=%USERPROFILE%\.claude\skillsvatar-video-engine\scripts
py -3.10 "%SKILL%\captions.py" me.mov -o captions.ass --model small --cache transcript.json

#    Pass the script so the wording on screen is yours, not the ASR's. Alignment
#    is a diff against real word timings, and it EXITS NON-ZERO when too few
#    words anchor. Do not pass --force to silence that - it means the captions
#    would be guesses. Fix the script or raise --model instead.
py -3.10 "%SKILL%\captions.py" me.mov -o captions.ass --script script.txt --model small

# 3. Compose  (warns if a source has to be upscaled into its pane - read it)
py -3.10 "%SKILL%\compose.py" --top screen.mp4 --bottom me.mov --captions captions.ass -o ep03.mp4
```

Output is 1080x1920, H.264/AAC, faststart — accepted as-is by TikTok, Reels and Shorts.

## Options worth knowing

| Flag | Where | Why |
|---|---|---|
| `--words-per-line 3` | captions.py | Fewer words = larger text = better on small screens |
| `--margin-v` | captions.py | Distance from top. Default 420 keeps captions clear of the pane seam |
| `--model small` | captions.py | Better accuracy than `base`. Slower on CPU; `turbo` needs ~6 GB and will not fit |
| `--cache f.json` | captions.py | Saves the transcript. Re-runs that only change styling or the script are then instant instead of minutes |
| `--min-align-ratio` | captions.py | Floor for how much of the script must anchor to real timings before it refuses (default 0.60) |
| `--split 0.6` | compose.py | More room for the screen recording when the terminal is dense |
| `--audio vo.wav` | compose.py | Use a separate voiceover instead of the camera's audio |
| (omit `--top`) | compose.py | Talking-head only, still 1080x1920 with captions |

Or in one command once the clips are in `days/dayNN/`:

```
.\make.bat day01
```

## taste.md

`taste.md` is the voice spec the script writer reads before drafting anything.
It is currently **v0 and inferred** — pulled from the two published TikToks, not
confirmed by you. Days 1–3 exist to correct it.

When you reject a draft line, record *why* in its corrections log. A rejection
with no reason teaches the writer nothing, and this file is the only thing
standing between scripts in your voice and generic AI copy.

## What the caption warnings mean

Measured on day01: `base` anchored 56% of the script's 167 words, `small` 63%.
The shortfall is **not** all accent. The diff showed two different causes:

- **Orthography** - `I'm` vs `I am`, `9` vs `Nine`. Heard correctly, spelled
  differently. The aligner now normalises both sides, which recovered 4 points.
- **Script drift** - at 13.1s the script says "An AI" and the take contains ~13
  seconds of improvised speech that is not in `script.txt` at all.

So when the ratio is low, check that `script.txt` matches the take *before*
reaching for a bigger model. `script.txt` is meant to be what was actually said.

This stops mattering once the voice is generated rather than recorded: the model
speaks the script exactly, so alignment goes to ~100%.

## Notes

Captions are burned in, which is deliberate — every platform strips or restyles
soft subtitles, and silent autoplay means unread captions are lost views.

`compose.py` escapes the `.ass` path before handing it to ffmpeg. On Windows a bare
path breaks the filtergraph twice (drive-letter colon read as an option separator,
backslashes eaten as escapes). This is the same class of bug that silently disables
`--adaptive` in crv on this platform.

## Not yet wired: publishing

Production is automated; publishing is deliberately not. See the parent notes —
full auto-posting needs platform API approval that takes days to weeks, and at one
post per day a manual upload costs about two minutes with zero account risk.
Revisit when volume actually justifies it.
