#!/usr/bin/env python3
"""Generate quote cards for the text-first platforms.

A short-form video does not travel to LinkedIn or X. What travels is one claim,
set well. These cards carry a single line from the episode in the same cyan-on-
dark palette as the burned-in video captions, so a card and a Reel read as the
same person.

Sizes follow each platform's native crop, so nothing is letterboxed or cropped
by the platform itself:
    instagram  1080x1350  (4:5, the tallest Instagram allows in-feed)
    x          1600x900   (16:9)
    linkedin   1200x1200  (1:1, survives both feed and mobile)

Usage:
    py -3.10 visuals.py --text "Africa is an oil well." -o out/ --platform instagram
    py -3.10 visuals.py --from-file lines.txt -o out/ --platform all
"""
from __future__ import annotations
import argparse
import json
import os
import sys

SIZES = {"instagram": (1080, 1350), "x": (1600, 900),
         "linkedin": (1200, 1200), "facebook": (1200, 1200)}
HERE = os.path.dirname(os.path.abspath(__file__))


def load_brand(path: str | None) -> dict:
    p = path or os.path.join(HERE, "brand.json")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def wrap_to_fit(draw, text: str, font_path: str, box_w: int, box_h: int,
                max_size: int, min_size: int = 28):
    """Largest font size at which the text still fits the box.

    Binary search would be faster, but the linear walk lets us keep the exact
    wrapped lines from the winning size instead of recomputing them.
    """
    from PIL import ImageFont
    for size in range(max_size, min_size - 1, -2):
        font = ImageFont.truetype(font_path, size)
        words, lines, cur = text.split(), [], ""
        for w in words:
            trial = f"{cur} {w}".strip()
            if draw.textlength(trial, font=font) <= box_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        line_h = int(size * 1.22)
        if len(lines) * line_h <= box_h:
            return font, lines, line_h
    from PIL import ImageFont
    font = ImageFont.truetype(font_path, min_size)
    return font, text.split("\n"), int(min_size * 1.22)


def make_card(text: str, platform: str, brand: dict, out_path: str,
              accent_words: int = 0) -> str:
    from PIL import Image, ImageDraw, ImageFont

    W, H = SIZES[platform]
    pad = int(W * 0.09)
    img = Image.new("RGB", (W, H), brand["bg"])
    d = ImageDraw.Draw(img)

    # Accent rule at the top left — a small fixed mark that makes a set of cards
    # recognisable as a series rather than isolated images.
    d.rounded_rectangle([pad, pad, pad + int(W * 0.11), pad + 10], radius=5,
                        fill=brand["accent"])

    foot_h = int(H * 0.11)
    box_w, box_h = W - pad * 2, H - pad * 2 - foot_h - int(H * 0.05)
    font, lines, line_h = wrap_to_fit(d, text, brand["font_display"], box_w, box_h,
                                      max_size=int(W * 0.085))

    y = pad + int(H * 0.06)
    # Accent the opening words: the eye lands there first, and it ties the card
    # to the one highlighted word in the video captions.
    accented = accent_words
    for line in lines:
        if accented > 0:
            words = line.split()
            take = min(accented, len(words))
            head, tail = " ".join(words[:take]), " ".join(words[take:])
            d.text((pad, y), head, font=font, fill=brand["accent"])
            if tail:
                off = d.textlength(head + " ", font=font)
                d.text((pad + off, y), tail, font=font, fill=brand["fg"])
            accented -= take
        else:
            d.text((pad, y), line, font=font, fill=brand["fg"])
        y += line_h

    fsize = max(20, int(W * 0.026))
    ffont = ImageFont.truetype(brand["font_body"], fsize)
    d.text((pad, H - pad - fsize * 2), brand["handle"], font=ffont, fill=brand["fg"])
    d.text((pad, H - pad - fsize // 2), brand["tagline"], font=ffont, fill=brand["muted"])

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    img.save(out_path, quality=95)
    return out_path


def main() -> None:
    p = argparse.ArgumentParser(description="Quote cards for text-first platforms")
    p.add_argument("--text", help="the line to set")
    p.add_argument("--from-file", help="one line per card")
    p.add_argument("--platform", default="all", help="instagram, x, linkedin, or all")
    p.add_argument("-o", "--out", required=True, help="output directory")
    p.add_argument("--brand", help="brand json (default: brand.json beside this script)")
    p.add_argument("--accent-words", type=int, default=2,
                   help="how many opening words take the accent colour")
    args = p.parse_args()

    if not args.text and not args.from_file:
        sys.exit("Give --text or --from-file.")
    brand = load_brand(args.brand)

    lines = [args.text] if args.text else [
        l.strip() for l in open(args.from_file, encoding="utf-8") if l.strip()]
    platforms = list(SIZES) if args.platform == "all" else [args.platform]
    for plat in platforms:
        if plat not in SIZES:
            sys.exit(f"Unknown platform {plat!r}. Known: {', '.join(SIZES)}")

    made = []
    for i, line in enumerate(lines):
        for plat in platforms:
            out = os.path.join(args.out, plat, f"visual_{i}.jpg")
            made.append(make_card(line, plat, brand, out, args.accent_words))
    for m in made:
        print(m)
    print(f"{len(made)} card(s)")


if __name__ == "__main__":
    main()
