#!/usr/bin/env python3
"""
Wahapedia full-page text dumper.
Saves complete readable content from faction overview pages and core rule pages.
Covers: army rules, subfaction rules, relics, warlord traits, crusade rules, core rules.

Usage:
    python tools/wahapedia_page_scraper.py necrons
    python tools/wahapedia_page_scraper.py orks
    python tools/wahapedia_page_scraper.py adeptus-custodes
    python tools/wahapedia_page_scraper.py core-rules
"""

import argparse
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

BASE = "https://wahapedia.ru"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ArbiterDataVerifier/1.0)"}

PAGES: dict[str, list[tuple[str, str]]] = {
    "necrons": [
        ("faction_overview.txt", "/wh40k9ed/factions/necrons/"),
    ],
    "orks": [
        ("faction_overview.txt", "/wh40k9ed/factions/orks/"),
    ],
    "adeptus-custodes": [
        ("faction_overview.txt", "/wh40k9ed/factions/adeptus-custodes/"),
    ],
    "core-rules": [
        ("playing_this_game.txt", "/wh40k9ed/the-rules/playing-this-game/"),
        ("core_rules.txt", "/wh40k9ed/the-rules/core-rules/"),
        ("open_play.txt", "/wh40k9ed/the-rules/open-play/"),
        ("matched_play.txt", "/wh40k9ed/the-rules/matched-play/"),
        ("narrative_play.txt", "/wh40k9ed/the-rules/narrative-play/"),
        ("rules_appendix.txt", "/wh40k9ed/the-rules/rules-appendix/"),
    ],
}


def fetch(url: str) -> BeautifulSoup:
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", errors="replace")
    return BeautifulSoup(html, "html.parser")


def extract_text(soup: BeautifulSoup) -> str:
    for tag in soup.find_all(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    for tag in soup.find_all(class_=re.compile(r"cookie|banner|advert|popup|modal", re.I)):
        tag.decompose()
    text = soup.get_text(separator="\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Wahapedia full-page text dumper")
    parser.add_argument("target", choices=list(PAGES.keys()))
    parser.add_argument(
        "--out-dir", default=None, help="Output directory (default: docs/work/wahapedia_<target>)"
    )
    parser.add_argument("--delay", type=float, default=2.0)
    args = parser.parse_args()

    pages = PAGES[args.target]
    out_dir = (
        Path(args.out_dir)
        if args.out_dir
        else Path(f"docs/work/wahapedia_{args.target.replace('-', '_')}")
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, (filename, path) in enumerate(pages):
        url = BASE + path
        print(f"[{i+1}/{len(pages)}] {url}", file=sys.stderr)
        try:
            soup = fetch(url)
            text = extract_text(soup)
            out_file = out_dir / filename
            out_file.write_text(text, encoding="utf-8")
            print(f"  -> {out_file} ({len(text.splitlines())} lines)", file=sys.stderr)
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)
        if i < len(pages) - 1:
            time.sleep(args.delay)


if __name__ == "__main__":
    main()
