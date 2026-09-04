#!/usr/bin/env python3
"""Set up a repurposing job: one episode becomes a drafts folder per platform.

Like write_script.py, this does not call an LLM. It builds the folder structure
and a brief per platform carrying the source script, the voice spec, and that
platform's conventions. Claude then writes each post.txt from the brief. The
constraints are what make the output consistent, and they cost nothing to run.

Nothing here publishes. Everything lands in drafts/ for review — the rule the
source video is explicit about: never publish without the human seeing it.

Usage:
    py -3.10 post_generator.py --day 1
    py -3.10 post_generator.py --script ../days/day01/script.txt --slug why-i-stopped
    py -3.10 post_generator.py --day 1 --platforms linkedin,x
"""
from __future__ import annotations
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# What each platform actually rewards. Drawn from the source video's own prompt
# (professional on LinkedIn, conversational on X, visual-first on Instagram)
# plus each platform's hard limits.
PLATFORMS = {
    "linkedin": {
        "voice": "Thought leader, but not corporate. First person, plain words. "
                 "The lesson comes before the story, not after it.",
        "limit": "3000 characters; the first 2 lines show before 'see more', so "
                 "the hook must land there",
        "form": "3-6 short paragraphs. One blank line between each. No hashtag "
                "block - two at most, at the end.",
        "visual": "quote card, 1200x1200",
    },
    "x": {
        "voice": "Casual and direct. Contractions. The way you would say it to "
                 "one person who already knows the space.",
        "limit": "280 characters for the opening post",
        "form": "Either one self-contained post, or a thread where post 1 stands "
                "alone and earns the rest. Never a thread that needs post 2 to "
                "make sense.",
        "visual": "quote card, 1600x900",
    },
    "instagram": {
        "voice": "Visual-first. The caption supports the image, it does not "
                 "carry the post alone.",
        "limit": "2200 characters, but only the first line shows in feed",
        "form": "Hook line, then 2-4 short lines, then a question. Hashtags on "
                "their own line at the end: #fyp plus niche tags.",
        "visual": "quote card, 1080x1350",
    },
    "facebook": {
        "voice": "More personal than LinkedIn, less clipped than X. Written for "
                 "people who know you, not strangers.",
        "limit": "no practical limit, but under 500 characters performs",
        "form": "Short paragraphs. A direct question at the end.",
        "visual": "quote card, 1200x1200",
    },
    "tiktok": {
        "voice": "Same voice as the video itself.",
        "limit": "2200 characters, first line matters most",
        "form": "One hook line, a line of context, then hashtags.",
        "visual": "the episode video",
    },
    "reels": {
        "voice": "Same as TikTok, slightly less slang.",
        "limit": "2200 characters",
        "form": "Hook line, context, hashtags.",
        "visual": "the episode video",
    },
    "shorts": {
        "voice": "Plainer than TikTok. YouTube titles are searched, not scrolled.",
        "limit": "100 character title, 5000 character description",
        "form": "A searchable title, then a short description with a link.",
        "visual": "the episode video",
    },
}

DEFAULT = ["linkedin", "x", "instagram", "facebook", "tiktok", "reels", "shorts"]


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:60] or "episode"


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def brief_for(platform: str, script: str, taste: str, slug: str, video: str | None) -> str:
    p = PLATFORMS[platform]
    vis = (f"Attach the episode video: {video}" if video and p["visual"] == "the episode video"
           else f"Generate with visuals.py -- {p['visual']}")
    return f"""# {platform} - {slug}

**Voice for this platform:** {p['voice']}

**Limit:** {p['limit']}

**Form:** {p['form']}

**Visual:** {vis}

---

## Source script (the episode this comes from)

{script.strip()}

---

## Hard rules

- This is a repurpose, not a transcript. Do not paste the script. Pull the one
  idea that travels to this platform and write it natively.
- Never claim a client, revenue, or result that has not happened.
- Soft CTA only: "I build AI automations for Nigerian businesses." The hard ask
  is day 30.
- If the episode has no idea worth carrying to this platform, say so and write
  nothing. A skipped post costs nothing; a filler post costs trust.

---

## Voice spec

{taste.strip()}

---

## Deliverable

Write the post to `post.txt` in this folder. Plain text, exactly as it will be
posted. Then pick the single strongest line and put it in `visual.txt` on its
own - that line becomes the quote card.
"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Set up a repurposing job")
    ap.add_argument("--day", type=int, help="episode number from series.json")
    ap.add_argument("--script", help="path to a script.txt instead")
    ap.add_argument("--slug", help="folder name (derived from the script if omitted)")
    ap.add_argument("--platforms", default=",".join(DEFAULT))
    ap.add_argument("--video", help="path to the finished episode video")
    args = ap.parse_args()

    series_title = None
    if args.day:
        d = os.path.join(PIPELINE, "days", f"day{args.day:02d}")
        script_path = os.path.join(d, "script.txt")
        video = args.video or (os.path.join(d, "out.mp4")
                               if os.path.exists(os.path.join(d, "out.mp4")) else None)
        # Prefer the series title for the folder name. Slugging the first spoken
        # line produces something unreadable, and these folders are browsed by hand.
        sp = os.path.join(PIPELINE, "series.json")
        if os.path.exists(sp):
            import json
            for e in json.load(open(sp, encoding="utf-8"))["episodes"]:
                if e["day"] == args.day:
                    series_title = f"day{args.day:02d}-{e['title']}"
                    break
    elif args.script:
        script_path = args.script
        video = args.video
    else:
        sys.exit("Give --day or --script.")

    if not os.path.exists(script_path):
        sys.exit(f"No script at {script_path}")
    script = read(script_path)

    taste_path = os.path.join(PIPELINE, "taste.md")
    if not os.path.exists(taste_path):
        sys.exit("taste.md missing - the voice spec is what keeps these in your voice.")
    taste = read(taste_path)

    slug = args.slug or slugify(series_title or script.strip().splitlines()[0])
    plats = [p.strip() for p in args.platforms.split(",") if p.strip()]
    for p in plats:
        if p not in PLATFORMS:
            sys.exit(f"Unknown platform {p!r}. Known: {', '.join(PLATFORMS)}")

    root = os.path.join(HERE, "drafts", slug)
    for p in plats:
        folder = os.path.join(root, p)
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "BRIEF.md"), "w", encoding="utf-8") as f:
            f.write(brief_for(p, script, taste, slug, video))

    print(f"drafts/{slug}/  ({len(plats)} platforms)")
    for p in plats:
        print(f"  {p}/BRIEF.md")
    print("\nNext: Claude writes post.txt and visual.txt in each folder,")
    print("then visuals.py renders the cards, then publish.py stages them.")


if __name__ == "__main__":
    main()
