#!/usr/bin/env python3
"""Find what is worth making an episode about today.

Two independent signals, deliberately kept separate because they answer
different questions:

  Channels  - what is already outperforming in this exact niche. A video is
              interesting when it beats its own channel's median, not when it
              has a big absolute number; a 40k video on a small channel is a
              stronger signal than a 200k video on a large one.

  Hacker News - what broke in the last few days. Catches releases and outages
              before any creator has covered them, which is the only window
              where a trend-reaction video is actually early.

Nothing here needs an API key. Channel data comes from yt-dlp (already used
elsewhere in this pipeline); HN uses the public Algolia endpoint.

Usage:
    py -3.10 trend_watch.py
    py -3.10 trend_watch.py --days 3 --top 8
    py -3.10 trend_watch.py --channel @nateherk --channel @someoneelse
"""
from __future__ import annotations
import argparse
import json
import re
import statistics
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

# Seeded with the one channel verified against this pipeline. Add more as you
# find them - a single channel tells you what one person's audience likes; three
# tell you what the niche likes.
DEFAULT_CHANNELS = ["@nateherk"]

# Terms that make an HN story relevant to this niche. Kept broad on purpose:
# the ranking below does the filtering, so a wide net costs nothing.
HN_TERMS = ["claude code", "anthropic claude", "ai agents"]


@dataclass
class Candidate:
    title: str
    source: str
    url: str
    signal: float          # higher = more worth covering
    why: str
    extra: dict = field(default_factory=dict)


def run(cmd: list[str], timeout: int = 180) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           errors="replace", timeout=timeout)
        return r.stdout
    except (subprocess.TimeoutExpired, OSError):
        return ""


def from_channels(handles: list[str], depth: int) -> list[Candidate]:
    """Videos beating their own channel's median view count.

    Scoring against the channel's own median rather than a global threshold is
    what stops a large channel from drowning out a small one - and small
    channels are where the un-copied ideas are.
    """
    out: list[Candidate] = []
    for handle in handles:
        for tab in ("shorts", "videos"):
            raw = run(["yt-dlp", "--flat-playlist", "--playlist-end", str(depth),
                       "--socket-timeout", "45",
                       "--print", "%(view_count)s\t%(title)s\t%(url)s",
                       f"https://www.youtube.com/{handle}/{tab}"])
            rows = []
            for line in raw.splitlines():
                parts = line.split("\t")
                if len(parts) != 3:
                    continue
                views, title, url = parts
                if not views.isdigit():
                    continue
                rows.append((int(views), title.strip(), url.strip()))
            if len(rows) < 4:
                continue
            median = statistics.median(v for v, _, _ in rows) or 1
            for pos, (views, title, url) in enumerate(rows):
                ratio = views / median
                # Recency taper: the list is newest-first, so position is age.
                # An old outlier is history; a recent one is a live trend.
                recency = max(0.35, 1.0 - pos / (len(rows) * 1.4))
                score = ratio * recency
                if score < 1.15:
                    continue
                out.append(Candidate(
                    title=title, source=f"{handle}/{tab}", url=url,
                    signal=round(score, 2),
                    why=f"{views:,} views vs {int(median):,} median ({ratio:.1f}x), position {pos + 1}",
                    extra={"views": views},
                ))
    return out


def from_hn(days: int) -> list[Candidate]:
    """Recent Hacker News stories. Points are the signal; recency is the filter."""
    since = int(time.time()) - days * 86400
    out: list[Candidate] = []
    seen: set[str] = set()
    for term in HN_TERMS:
        q = urllib.parse.urlencode({
            "query": term, "tags": "story",
            "numericFilters": f"created_at_i>{since}",
            "hitsPerPage": "20",
        })
        try:
            with urllib.request.urlopen(
                    f"https://hn.algolia.com/api/v1/search?{q}", timeout=30) as r:
                data = json.load(r)
        except Exception:
            continue
        for hit in data.get("hits", []):
            title = (hit.get("title") or "").strip()
            oid = hit.get("objectID")
            if not title or oid in seen:
                continue
            seen.add(oid)
            points = hit.get("points") or 0
            if points < 15:
                continue
            age_h = max(1.0, (time.time() - (hit.get("created_at_i") or 0)) / 3600)
            # Points per hour: rewards a story climbing now over one that
            # peaked three days ago and is already covered everywhere.
            score = points / (age_h ** 0.6)
            out.append(Candidate(
                title=title, source="hacker news",
                url=hit.get("url") or f"https://news.ycombinator.com/item?id={oid}",
                signal=round(score, 2),
                why=f"{points} points in {int(age_h)}h",
                extra={"points": points},
            ))
    return out


def angle_for(c: Candidate) -> str:
    """Suggest how he would cover it, given his positioning.

    Generic AI commentary competes with saturated global content and loses. His
    edge is the Nigerian market, his own build, and being a backend developer -
    so every angle here routes through one of those.
    """
    t = c.title.lower()
    if any(w in t for w in ("price", "cheap", "free", "cost", "$")):
        return "Cost angle - what this actually saves a Nigerian business"
    if any(w in t for w in ("skill", "agent", "mcp", "workflow", "automat")):
        return "Build angle - show it running on your machine"
    if any(w in t for w in ("vs", "tested", "compare", "better")):
        return "Skip the comparison. Cover what it changes for your build instead"
    if c.source == "hacker news":
        return "News angle - you are early, explain it before the big channels do"
    return "Reaction angle - what it means for someone building solo in Nigeria"


def main() -> None:
    p = argparse.ArgumentParser(description="Topic candidates for today's episode")
    p.add_argument("--channel", action="append", default=None,
                   help="channel handle, e.g. @nateherk (repeatable)")
    p.add_argument("--days", type=int, default=5, help="HN lookback window")
    p.add_argument("--depth", type=int, default=25, help="videos to read per tab")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = p.parse_args()

    channels = args.channel or DEFAULT_CHANNELS
    cands = from_channels(channels, args.depth) + from_hn(args.days)

    if not cands:
        print("No candidates cleared the bar. Fall back to the next unbuilt "
              "episode in the 30-day series.")
        return

    # Normalise the two signals so neither source can dominate purely because
    # its raw numbers are larger.
    for src in {c.source for c in cands}:
        group = [c for c in cands if c.source == src]
        top = max(c.signal for c in group) or 1
        for c in group:
            c.signal = round(c.signal / top, 3)

    cands.sort(key=lambda c: c.signal, reverse=True)
    cands = cands[:args.top]

    if args.json:
        print(json.dumps([{
            "title": c.title, "source": c.source, "url": c.url,
            "signal": c.signal, "why": c.why, "angle": angle_for(c),
        } for c in cands], indent=2, ensure_ascii=False))
        return

    print(f"\n  Topic candidates - {time.strftime('%d %b %Y')}")
    print(f"  channels: {', '.join(channels)}  |  HN window: {args.days}d\n")
    for i, c in enumerate(cands, 1):
        bar = "#" * max(1, round(c.signal * 12))
        print(f"  {i:2d}. {c.title[:74]}")
        print(f"      {bar}  {c.source} - {c.why}")
        print(f"      -> {angle_for(c)}")
        print(f"      {c.url}\n")
    print("  Nothing here worth covering? Use the next episode in the 30-day plan.\n")


if __name__ == "__main__":
    main()
