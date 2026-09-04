#!/usr/bin/env python3
"""Stage or publish a reviewed drafts folder.

One internal interface, several backends. The choice of how posts actually reach
the platforms is a config line, not a rewrite:

  checklist  (default, free)  writes TO_POST.md - everything needed to post by
                              hand, in order, with file paths. No account access,
                              no API keys, no ban risk.
  blotato                     one API to all platforms. Paid. What the source
                              video uses.
  postiz                      open source, self-hostable. Free, but needs a
                              server that is awake when posts fire.

The default is deliberate: the system is fully useful before any money is spent,
and nothing can post by accident while the backends are unconfigured.

Publishing never happens without --confirm, and never for a platform whose
post.txt is missing or empty.

Usage:
    py -3.10 publish.py --slug day01-why-i-stopped-looking-for-clients
    py -3.10 publish.py --slug <slug> --backend blotato --confirm
"""
from __future__ import annotations
import argparse
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.join(HERE, "drafts")
LOG = os.path.join(HERE, "published_log.md")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ORDER = ["tiktok", "reels", "shorts", "instagram", "x", "linkedin", "facebook"]


def collect(slug: str) -> list[dict]:
    root = os.path.join(DRAFTS, slug)
    if not os.path.isdir(root):
        sys.exit(f"No drafts folder for {slug!r}. Run post_generator.py first.")
    found = []
    for plat in ORDER:
        folder = os.path.join(root, plat)
        if not os.path.isdir(folder):
            continue
        post = os.path.join(folder, "post.txt")
        text = ""
        if os.path.exists(post):
            with open(post, encoding="utf-8") as f:
                text = f.read().strip()
        media = sorted(
            os.path.join(folder, f) for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".mp4"))
        )
        found.append({"platform": plat, "folder": folder, "text": text, "media": media})
    return found


def already_published(slug: str, platform: str) -> bool:
    if not os.path.exists(LOG):
        return False
    with open(LOG, encoding="utf-8") as f:
        return f"| {slug} | {platform} |" in f.read()


def record(slug: str, platform: str, backend: str) -> None:
    new = not os.path.exists(LOG)
    with open(LOG, "a", encoding="utf-8") as f:
        if new:
            f.write("# Published log\n\nState, so nothing posts twice.\n\n"
                    "| slug | platform | when | via |\n|---|---|---|---|\n")
        f.write(f"| {slug} | {platform} | {dt.datetime.now():%Y-%m-%d %H:%M} | {backend} |\n")


def backend_checklist(slug: str, items: list[dict], confirm: bool) -> None:
    """Write a manual posting checklist. The free path, and the default."""
    out = os.path.join(DRAFTS, slug, "TO_POST.md")
    lines = [f"# To post - {slug}\n",
             f"_Generated {dt.datetime.now():%d %b %Y %H:%M}. "
             "Tick each as you go; nothing here posts itself._\n"]
    for it in items:
        done = " (already logged)" if already_published(slug, it["platform"]) else ""
        lines.append(f"\n## {it['platform']}{done}\n")
        if not it["text"]:
            lines.append("_No post.txt yet - skipped._\n")
            continue
        lines.append("```\n" + it["text"] + "\n```\n")
        if it["media"]:
            lines.append("Attach:\n")
            for m in it["media"]:
                lines.append(f"- `{os.path.relpath(m, os.path.join(DRAFTS, slug))}`\n")
        else:
            lines.append("_No media in this folder._\n")
    with open(out, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"{out}")
    ready = sum(1 for i in items if i["text"])
    print(f"{ready}/{len(items)} platforms have copy ready.")
    if confirm:
        for it in items:
            if it["text"]:
                record(slug, it["platform"], "manual")
        print("Logged as published.")


def backend_api(slug: str, items: list[dict], confirm: bool, name: str) -> None:
    key = os.environ.get(f"{name.upper()}_API_KEY")
    if not key:
        sys.exit(
            f"{name} backend selected but {name.upper()}_API_KEY is not set.\n"
            f"Nothing was posted. Use the default checklist backend, or set the key.\n"
            f"(Adapter is stubbed - wire the HTTP calls when the account exists.)"
        )
    if not confirm:
        sys.exit("Refusing to publish without --confirm.")
    sys.exit(
        f"{name} adapter is not wired yet. The interface is here and the key was "
        f"found, but the HTTP calls are deliberately unimplemented until there is "
        f"an account to test against - a half-written publisher that posts to the "
        f"wrong account is worse than none."
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Stage or publish a drafts folder")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--backend", default="checklist",
                    choices=["checklist", "blotato", "postiz"])
    ap.add_argument("--confirm", action="store_true",
                    help="required before anything is published or logged")
    args = ap.parse_args()

    items = collect(args.slug)
    if not items:
        sys.exit("No platform folders found.")

    if args.backend == "checklist":
        backend_checklist(args.slug, items, args.confirm)
    else:
        backend_api(args.slug, items, args.confirm, args.backend)


if __name__ == "__main__":
    main()
