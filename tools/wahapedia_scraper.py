#!/usr/bin/env python3
"""
Wahapedia unit datasheet scraper for WH40k 9th Edition.

Usage:
    python tools/wahapedia_scraper.py necrons --all
    python tools/wahapedia_scraper.py necrons --unit warriors
    python tools/wahapedia_scraper.py necrons --stratagems
"""

import argparse
import re
import sys
import time
from urllib.request import Request, urlopen

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    print("ERROR: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

BASE = "https://wahapedia.ru/wh40k9ed/factions"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ArbiterDataVerifier/1.0)"}

UNIT_SLUGS: dict[str, str] = {
    # HQ — already verified
    "overlord": "Overlord",
    "royal_warden": "Royal-Warden",
    "plasmancer": "Plasmancer",
    "technomancer": "Technomancer",
    # HQ — new
    "necron_lord": "Lord",
    "lokhust_lord": "Lokhust-Lord",
    "skorpekh_lord": "Skorpekh-Lord",
    "catacomb_command_barge": "Catacomb-Command-Barge",
    "psychomancer": "Psychomancer",
    "chronomancer": "Chronomancer",
    "illuminor_szeras": "Illuminor-Szeras",
    "orikan_the_diviner": "Orikan-the-Diviner",
    "trazyn_the_infinite": "Trazyn-the-Infinite",
    "nemesor_zahndrekh": "Nemesor-Zahndrekh",
    "vargard_obyron": "Vargard-Obyron",
    "anrakyr_the_traveller": "Anrakyr-the-Traveller",
    "imotekh_the_stormlord": "Imotekh-the-Stormlord",
    "the_silent_king": "The-Silent-King",
    # Troops — already verified
    "warriors": "Necron-Warriors",
    "immortals": "Immortals",
    # Elites — already verified
    "skorpekh_destroyers": "Skorpekh-Destroyers",
    "lychguard": "Lychguard",
    "deathmarks": "Deathmarks",
    "canoptek_spyder": "Canoptek-Spyders",
    # Elites — new
    "triarch_praetorians": "Triarch-Praetorians",
    "flayed_ones": "Flayed-Ones",
    "canoptek_reanimator": "Canoptek-Reanimator",
    "cryptothralls": "Cryptothralls",
    # Fast Attack — already verified
    "canoptek_scarabs": "Canoptek-Scarab-Swarms",
    "canoptek_wraiths": "Canoptek-Wraiths",
    # Fast Attack — new
    "tomb_blades": "Tomb-Blades",
    "ophydian_destroyers": "Ophydian-Destroyers",
    # Heavy Support — already verified
    "triarch_stalker": "Triarch-Stalker",
    "annihilation_barge": "Annihilation-Barge",
    "lokhust_heavy_destroyers": "Lokhust-Heavy-Destroyers",
    # Heavy Support — new
    "lokhust_destroyers": "Lokhust-Destroyers",
    "canoptek_doomstalker": "Canoptek-Doomstalker",
    "doomsday_ark": "Doomsday-Ark",
    "ghost_ark": "Ghost-Ark",
    # Flyer — new
    "night_scythe": "Night-Scythe",
    "doom_scythe": "Doom-Scythe",
    # Lord of War / Titanic — new
    "monolith": "Monolith",
    "c_tan_nightbringer": "C-tan-Shard-of-the-Nightbringer",
    "c_tan_deceiver": "C-tan-Shard-of-the-Deceiver",
    "c_tan_void_dragon": "C-tan-Shard-of-the-Void-Dragon",
    "tesseract_vault": "Tesseract-Vault",
}

STAT_COLS = ["M", "WS", "BS", "S", "T", "W", "A", "Ld", "Sv"]


def fetch(url: str) -> BeautifulSoup:
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=15) as r:
        html = r.read().decode("utf-8", errors="replace")
    return BeautifulSoup(html, "html.parser")


def cell_text(td: Tag) -> str:
    """Get text from a table cell, joining span words with spaces, stripping PriceTags."""
    # Remove PriceTag spans (points costs like "+5")
    for pt in td.find_all(class_=re.compile(r"PriceTag")):
        pt.decompose()
    return re.sub(r"\s+", " ", td.get_text(separator=" ")).strip()


def extract_keywords(soup: BeautifulSoup) -> list[str]:
    """
    Keywords are in dsKeywordData rows. Structure (per Wahapedia HTML):
    - tooltip* spans  → one complete keyword (text with separator=' ' handles
                         multi-word like QUANTUM SHIELDING)
    - tooltipDynasty  → contains DYDY inner span ("<DYNASTY>") plus hidden
                         dynasty-sub-name spans (DYMA=MEPHRIT etc.) — take only DYDY
    - bare kwb spans  → words of a multi-word keyword without a tooltip wrapper
                         (e.g. ANNIHILATION + BARGE); flushed on comma text node
    - comma text node → separates keywords
    """
    keywords: list[str] = []

    def flush(buf: list[str]) -> None:
        if buf:
            keywords.append(" ".join(buf))
            buf.clear()

    for row in soup.find_all(class_="dsKeywordData"):
        buf: list[str] = []
        for child in row.children:
            if isinstance(child, Tag):
                classes = child.get("class") or []
                if any(c.startswith("tooltip") for c in classes):
                    flush(buf)
                    if "tooltipDynasty" in classes:
                        # Get only the <DYNASTY> inner span, skip dynasty sub-names
                        dydy = child.find(class_="DYDY")
                        kw = dydy.get_text(strip=True) if dydy else "<DYNASTY>"
                    else:
                        # separator=' ' joins multi-word kwb inner spans correctly
                        kw = child.get_text(separator=" ", strip=True)
                    if kw:
                        keywords.append(kw)
                elif "kwb" in classes:
                    # Bare kwb span = one word of a multi-word keyword
                    word = child.get_text(strip=True)
                    if word:
                        buf.append(word)
            else:
                if "," in str(child):
                    flush(buf)
        flush(buf)

    # Deduplicate preserving order
    seen: set[str] = set()
    return [k for k in keywords if k and not (k in seen or seen.add(k))]  # type: ignore[func-returns-value]


def extract_stats(soup: BeautifulSoup) -> dict[str, str]:
    """
    Stat table: wTable that has a header row with M WS BS S T W A Ld Sv.
    Data rows: [no, name, M, WS, BS, S, T, W, A, Ld, Sv, base].
    For degrading profiles, the first data row is the full/best profile.
    """
    for wt in soup.find_all(class_="wTable"):
        rows = wt.find_all("tr")
        # Find header row
        header_idx = None
        for i, row in enumerate(rows):
            cells = [cell_text(td) for td in row.find_all(["td", "th"])]
            if "WS" in cells and "BS" in cells and "Ld" in cells:
                header_idx = i
                break
        if header_idx is None:
            continue
        # First data row after header = best/full profile
        for row in rows[header_idx + 1 :]:
            cells = [cell_text(td) for td in row.find_all(["td", "th"])]
            # Expect at least 11 cells: no, name, M, WS, BS, S, T, W, A, Ld, Sv[, base]
            if len(cells) >= 11 and (cells[2].endswith('"') or cells[2] == "-"):
                return dict(zip(STAT_COLS, cells[2 : 2 + len(STAT_COLS)]))
    return {}


def extract_invuln(soup: BeautifulSoup) -> str | None:
    """
    Only search within dsAbilityData elements (not page-wide, to avoid
    matching stratagem texts that mention different invuln values).
    Returns e.g. "5+" or None.
    """
    for ab in soup.find_all(class_="dsAbilityData"):
        t = re.sub(r"\s+", " ", ab.get_text(" "))
        m = re.search(r"(\d)\+\s+invulnerable save", t, re.IGNORECASE)
        if m:
            return f"{m.group(1)}+"
    return None


def extract_weapons(soup: BeautifulSoup) -> list[dict]:
    """
    Weapon table: wTable with header row WEAPON / RANGE / TYPE / S / AP / D / ABILITIES.
    Each weapon may span two rows (name-only row + full stats row); deduplicate by name.
    """
    weapons: list[dict] = []
    seen_names: set[str] = set()

    for wt in soup.find_all(class_="wTable"):
        rows = wt.find_all("tr")
        header_idx = None
        for i, row in enumerate(rows):
            cells = [cell_text(td) for td in row.find_all(["td", "th"])]
            if "RANGE" in cells and "TYPE" in cells and "ABILITIES" in cells:
                header_idx = i
                break
        if header_idx is None:
            continue

        for row in rows[header_idx + 1 :]:
            cells = [cell_text(td) for td in row.find_all(["td", "th"])]
            if not cells:
                continue
            # Full weapon row has ≥ 6 cells
            if len(cells) >= 6 and cells[1]:
                name = cells[0]
                # Skip duplicate names (Wahapedia sometimes repeats abilities row)
                if name in seen_names:
                    continue
                seen_names.add(name)
                weapons.append(
                    {
                        "name": name,
                        "range": cells[1],
                        "type": cells[2],
                        "S": cells[3],
                        "AP": cells[4],
                        "D": cells[5],
                        "abilities": cells[6] if len(cells) > 6 else "",
                    }
                )

    return weapons


def extract_abilities(soup: BeautifulSoup) -> list[str]:
    result: list[str] = []
    for ab in soup.find_all(class_="dsAbilityData"):
        t = re.sub(r"\s+", " ", ab.get_text(" ")).strip()
        if t:
            result.append(t)
    return result


def extract_unit(soup: BeautifulSoup, label: str) -> dict:
    return {
        "name": label,
        "stats": extract_stats(soup),
        "invuln_save": extract_invuln(soup),
        "keywords": extract_keywords(soup),
        "weapons": extract_weapons(soup),
        "abilities": extract_abilities(soup),
    }


def extract_stratagems(soup: BeautifulSoup) -> list[dict]:
    stratagems: list[dict] = []
    for wrapper in soup.find_all(class_="stratWrapper_CS"):
        s: dict = {}
        name_el = wrapper.find(class_="stratName_9k")
        if name_el:
            raw = re.sub(r"\s+", " ", name_el.get_text()).strip()
            # CP cost is embedded in the name text, e.g. "ENSLAVED PROTECTORS1CP" or "CURSE3CP/1CP"
            # Variable-cost format: "3CP/1CP" means max/min; capture full block.
            cp_match = re.search(r"\s*(?:(\d+)CP/)?(\d+)CP\s*$", raw)
            if cp_match:
                max_cp, min_cp = cp_match.group(1), cp_match.group(2)
                s["cp"] = f"{max_cp}/{min_cp}" if max_cp else min_cp
                s["name"] = raw[: cp_match.start()].strip()
            else:
                s["name"] = raw
        text_el = wrapper.find(class_="stratText_CS")
        if text_el:
            s["rule_text"] = re.sub(r"\s+", " ", text_el.get_text(" ")).strip()
        for cls in wrapper.get("class") or []:
            if cls.startswith("strat") and cls not in (
                "stratWrapper_CS",
                "stratName_9k",
                "stratText_CS",
                "stratLegend2",
            ):
                s["type"] = cls
        if "name" in s:
            stratagems.append(s)
    return stratagems


# ── Output ────────────────────────────────────────────────────────────────────


def print_unit(uid: str, data: dict) -> None:
    print(f"\n{'='*64}")
    print(f"  {uid}  ({data['name']})")
    print(f"{'='*64}")
    stats = data["stats"]
    if stats:
        row = "  ".join(f"{k}:{v}" for k, v in stats.items())
        print(f"  STATS  {row}")
    else:
        print("  STATS  (not parsed)")
    inv = data["invuln_save"]
    print(f"  INVULN {inv if inv else 'none'}")
    print(f"  KW     {', '.join(data['keywords'])}")
    if data["weapons"]:
        print(f"  {'WEAPON':<30} {'RNG':<7} {'TYPE':<14} {'S':<5} {'AP':<5} {'D':<5} ABILITIES")
        for w in data["weapons"]:
            ab = w.get("abilities", "")
            ab_short = (ab[:55] + "…") if len(ab) > 55 else ab
            print(
                f"  {w['name']:<30} {w.get('range',''):<7} {w.get('type',''):<14} "
                f"{w.get('S',''):<5} {w.get('AP',''):<5} {w.get('D',''):<5} {ab_short}"
            )
    for ab in data.get("abilities", [])[:5]:
        print(f"  ABIL   {ab[:110]}")


def print_stratagems(stratagems: list[dict]) -> None:
    print(f"\n{'='*64}")
    print(f"  STRATAGEMS  ({len(stratagems)} found)")
    print(f"{'='*64}")
    for s in stratagems:
        name = s.get("name", "?")
        cp = s.get("cp", "?")
        typ = s.get("type", "")
        text = s.get("rule_text", "")[:100]
        print(f"\n  [{cp} CP]  {name}  [{typ}]")
        print(f"    {text}")


# ── CLI ───────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="Wahapedia scraper")
    parser.add_argument("faction")
    parser.add_argument("--unit", help="single unit ID from UNIT_SLUGS")
    parser.add_argument("--stratagems", action="store_true")
    parser.add_argument("--all", action="store_true", dest="all_units")
    parser.add_argument("--delay", type=float, default=1.5)
    args = parser.parse_args()

    faction = args.faction

    if args.stratagems:
        url = f"{BASE}/{faction}/"
        print(f"Fetching: {url}", file=sys.stderr)
        soup = fetch(url)
        strats = extract_stratagems(soup)
        print_stratagems(strats)
        return

    units: list[tuple[str, str]]
    if args.unit:
        uid = args.unit.lower()
        if uid not in UNIT_SLUGS:
            print(f"Unknown unit '{uid}'. Known: {', '.join(UNIT_SLUGS)}", file=sys.stderr)
            sys.exit(1)
        units = [(uid, UNIT_SLUGS[uid])]
    elif args.all_units:
        units = list(UNIT_SLUGS.items())
    else:
        parser.print_help()
        sys.exit(0)

    for i, (uid, slug) in enumerate(units):
        url = f"{BASE}/{faction}/{slug}"
        print(f"[{i+1}/{len(units)}] {url}", file=sys.stderr)
        try:
            soup = fetch(url)
            data = extract_unit(soup, slug.replace("-", " "))
            print_unit(uid, data)
        except Exception as e:
            print(f"  ERROR {uid}: {e}", file=sys.stderr)
        if i < len(units) - 1:
            time.sleep(args.delay)


if __name__ == "__main__":
    main()
