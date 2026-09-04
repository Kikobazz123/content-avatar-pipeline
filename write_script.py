#!/usr/bin/env python3
"""Assemble a writing brief for one episode.

This deliberately does not call an LLM. There is no API key configured, and
adding a paid dependency to a daily loop that currently costs nothing is the
wrong trade while the whole point is a free stack. What it does instead is
gather everything a writer needs — the voice spec, the structural beats proven
by the two 163k reference videos, the topic, and the hard rules — into one
brief. Hand that brief to Claude (or write from it yourself) and the output is
consistent because the constraints are, not because a model was clever.

When an API key does exist, this same brief becomes the prompt. Nothing is
wasted by starting here.

Usage:
    py -3.10 write_script.py                          # next unbuilt series episode
    py -3.10 write_script.py --day 5
    py -3.10 write_script.py --topic "Claude Code just shipped X" --angle build
    py -3.10 write_script.py --day 1 --out days/day01/brief.md
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))

# Windows consoles default to a legacy codepage (cp1252 here), which cannot
# encode the emoji that live in taste.md. Without this, printing a brief to the
# terminal dies on UnicodeEncodeError while writing the same text to a file
# succeeds — a confusing failure that looks like the script is broken.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# The structural beats both 163k reference videos share. These are not style
# preferences — they are what the two highest-performing videos in this niche
# actually do, measured frame by frame.
BEATS = """\
1. FRAME ZERO — the finished artifact, on screen, before a word is spoken.
   Not a title card, not your face alone, not "hey guys". Reference A opened on
   a website the viewer assumes is Apple's; Reference B opened on a terminal
   that had already printed its result.

2. THE PROMISE — complete, inside 3 seconds, spoken over that visual.
   A: "Here's how I build 3D animated websites with Claude Code."  (0.0-2.7s)
   B: "Google's new tool lets you connect to anything instantly."  (0.0-2.8s)

3. RETENTION DEVICE — pick exactly one:
   (a) DECEPTION-REVEAL — let the viewer believe something for 10-15s, then
       turn it. A spent 11 seconds narrating "Apple's site" before saying
       "this website is not Apple". Use when your result looks like it came
       from somewhere more established than you.
   (b) DELAYED AGITATION — name the pain at roughly 35% in, once they are
       already invested. B waited until 0:40 to say "it literally just looks
       like raw markdown and it's obviously horrible". Use when demoing a
       tool that fixes a known annoyance.

4. MECHANISM, NAMED AGAINST WHAT THEY TRIED — B: "not via API call, not via
   MCP, but via a bash command." Name the thing, and contrast it with the two
   approaches the audience already failed with. This is the credibility beat.

5. CLOSE — soft CTA on days 1-29, hard ask on day 30 only.
"""

HARD_RULES = """\
- Never claim a client, revenue figure, or result that has not happened.
  LordGen is pre-launch with no live agents. One invented win destroys the
  value of every honest episode.
- One idea per episode. Both references carry exactly one.
- Write for the mouth. Read it aloud; if it needs a second breath mid-sentence,
  cut it.
- Target 90-150 seconds. Both references run near two minutes, not thirty
  seconds — Shorts allow three.
- Every angle routes through the market, the build, or the reason. Generic
  global AI commentary competes with saturated content and loses.
"""

ANGLES = {
    "build": "Show it running on your machine. You are a backend developer; the terminal is the proof.",
    "cost":  "What this actually saves a Nigerian business, in naira.",
    "news":  "You are early. Explain it before the big channels get to it.",
    "pain":  "Name the thing your buyer already feels every day.",
    "story": "Something that happened to you. Wins and mistakes both count.",
}


def load_series() -> dict:
    p = os.path.join(HERE, "series.json")
    if not os.path.exists(p):
        sys.exit("series.json not found next to this script.")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pick_episode(series: dict, day: int | None) -> dict:
    eps = series["episodes"]
    if day is not None:
        for e in eps:
            if e["day"] == day:
                return e
        sys.exit(f"No episode for day {day} (series has 1-{len(eps)}).")
    for e in eps:
        if not e.get("done"):
            return e
    sys.exit("Every episode is marked done. Season complete — plan season two.")


def build_brief(topic: str, screen: str, angle: str, day: int | None,
                cta: str, warning: str | None, taste: str) -> str:
    head = f"Day {day}" if day else "Trend episode"
    angle_note = ANGLES.get(angle, angle)
    cta_line = ('HARD ASK — the offer, the price, the WhatsApp link, the community invite.'
                if cta == "hard" else
                '"I build AI automations for Nigerian businesses. Link\'s in my bio." '
                'One line, then stop talking.')

    parts = [
        f"# Writing brief — {head}\n",
        f"**Topic:** {topic}\n",
        f"**Screen recording:** {screen}\n",
        f"**Angle:** {angle_note}\n",
        f"**Close:** {cta_line}\n",
    ]
    if warning:
        parts.append(f"> **Careful:** {warning}\n")

    parts += [
        "\n---\n\n## Structure\n\n```\n" + BEATS + "```\n",
        "\n## Hard rules\n\n" + HARD_RULES + "\n",
        "\n---\n\n## Voice spec\n\n",
        taste.strip() + "\n",
        "\n---\n\n## Deliverable\n\n"
        "Write the spoken script only — no shot directions, no stage notes, no\n"
        "emoji. Plain lines, one sentence per line, exactly as it will be said.\n"
        "Save it to `days/dayNN/script.txt` so `captions.py --script` can use it\n"
        "as ground truth; Whisper mishears this accent badly and its wording must\n"
        "never reach the screen.\n",
    ]
    return "".join(parts)


def main() -> None:
    p = argparse.ArgumentParser(description="Assemble an episode writing brief")
    p.add_argument("--day", type=int, help="series episode number")
    p.add_argument("--topic", help="override with a trend topic")
    p.add_argument("--screen", default=None, help="what the top pane shows")
    p.add_argument("--angle", default="build", help=f"one of {', '.join(ANGLES)} or free text")
    p.add_argument("--out", help="write the brief here (default: stdout)")
    args = p.parse_args()

    taste_path = os.path.join(HERE, "taste.md")
    if not os.path.exists(taste_path):
        sys.exit("taste.md not found. It is the voice spec — the brief is worthless without it.")
    with open(taste_path, encoding="utf-8") as f:
        taste = f.read()

    if args.topic:
        brief = build_brief(args.topic, args.screen or "(decide: what runs on screen?)",
                            args.angle, None, "soft", None, taste)
        label = "trend episode"
    else:
        series = load_series()
        ep = pick_episode(series, args.day)
        brief = build_brief(ep["title"], args.screen or ep["screen"], args.angle,
                            ep["day"], ep.get("cta", "soft"), ep.get("warning"), taste)
        label = f"day {ep['day']} — {ep['title']}"

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(brief)
        print(f"{args.out}  ({label})")
    else:
        print(brief)


if __name__ == "__main__":
    main()
