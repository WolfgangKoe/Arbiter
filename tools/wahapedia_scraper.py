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

FACTION_UNIT_SLUGS: dict[str, dict[str, str]] = {
    "necrons": {
        # HQ
        "overlord": "Overlord",
        "royal_warden": "Royal-Warden",
        "plasmancer": "Plasmancer",
        "technomancer": "Technomancer",
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
        "kutlakh": "Kutlakh-the-World-Killer",
        "toholk": "Toholk-the-Blinded",
        # Troops
        "warriors": "Necron-Warriors",
        "immortals": "Immortals",
        # Elites
        "skorpekh_destroyers": "Skorpekh-Destroyers",
        "lychguard": "Lychguard",
        "deathmarks": "Deathmarks",
        "canoptek_spyder": "Canoptek-Spyders",
        "triarch_praetorians": "Triarch-Praetorians",
        "flayed_ones": "Flayed-Ones",
        "canoptek_reanimator": "Canoptek-Reanimator",
        "cryptothralls": "Cryptothralls",
        "hexmark_destroyer": "Hexmark-Destroyer",
        "canoptek_plasmacyte": "Canoptek-Plasmacyte",
        "transcendent_c_tan": "Transcendent-C-tan",
        "triarch_stalker": "Triarch-Stalker",
        "canoptek_tombstalker": "Canoptek-Tombstalker",
        # Fast Attack
        "canoptek_scarabs": "Canoptek-Scarab-Swarms",
        "canoptek_wraiths": "Canoptek-Wraiths",
        "tomb_blades": "Tomb-Blades",
        "ophydian_destroyers": "Ophydian-Destroyers",
        "canoptek_acanthrites": "Canoptek-Acanthrites",
        "canoptek_tomb_sentinel": "Canoptek-Tomb-Sentinel",
        # Heavy Support
        "annihilation_barge": "Annihilation-Barge",
        "lokhust_heavy_destroyers": "Lokhust-Heavy-Destroyers",
        "lokhust_destroyers": "Lokhust-Destroyers",
        "canoptek_doomstalker": "Canoptek-Doomstalker",
        "doomsday_ark": "Doomsday-Ark",
        "tesseract_ark": "Tesseract-Ark",
        # Dedicated Transport
        "ghost_ark": "Ghost-Ark",
        # Flyers
        "night_scythe": "Night-Scythe",
        "doom_scythe": "Doom-Scythe",
        "night_shroud": "Night-Shroud",
        # Lords of War
        "monolith": "Monolith",
        "obelisk": "Obelisk",
        "c_tan_nightbringer": "C-tan-Shard-of-the-Nightbringer",
        "c_tan_deceiver": "C-tan-Shard-of-the-Deceiver",
        "c_tan_void_dragon": "C-tan-Shard-of-the-Void-Dragon",
        "tesseract_vault": "Tesseract-Vault",
        "gauss_pylon": "Gauss-Pylon",
        "seraptek_heavy_construct": "Seraptek-Heavy-Construct",
        # Fortifications
        "convergence_of_dominion": "Convergence-of-Dominion",
        "sentry_pylon": "Sentry-Pylon",
        "tomb_citadel_walls": "Tomb-Citadel-Walls",
    },
    "orks": {
        # HQ
        "warboss": "Warboss",
        "warboss_mega_armour": "Warboss-in-Mega-Armour",
        "warboss_warbike": "Warboss-on-Warbike",
        "big_mek": "Big-Mek",
        "big_mek_mega_armour": "Big-Mek-in-Mega-Armour",
        "big_mek_kff": "Big-Mek-with-Kustom-Force-Field",
        "big_mek_sag": "Big-Mek-with-Shokk-Attack-Gun",
        "big_mek_warbike": "Big-Mek-on-Warbike",
        "weirdboy": "Weirdboy",
        "wurrboy": "Wurrboy",
        "painboy": "Painboy",
        "painboss": "Painboss",
        "beastboss": "Beastboss",
        "beastboss_squigosaur": "Beastboss-on-Squigosaur",
        "ghazghkull": "Ghazghkull-Thraka",
        "makari": "Makari",
        "mozrog_skragbad": "Mozrog-Skragbad",
        "kaptin_badrukk": "Kaptin-Badrukk",
        "boss_zagstruk": "Boss-Zagstruk",
        "boss_snikrot": "Boss-Snikrot",
        "deffkilla_wartrike": "Deffkilla-Wartrike",
        "zodgrod_wortsnagga": "Zodgrod-Wortsnagga",
        "da_red_gobbo_on_bounca": "Da-Red-Gobbo-on-Bounca",
        "goff_rokker": "Goff-Rokker",
        "grukk_face_rippa": "Grukk-Face-rippa",
        "mek_boss_buzzgob": "Mek-Boss-Buzzgob",
        "zhadsnark_da_ripper": "Zhadsnark-da-Ripper",
        # Troops
        "boyz": "Boyz",
        "gretchin": "Gretchin",
        "beast_snagga_boyz": "Beast-Snagga-Boyz",
        # Dedicated Transport
        "trukk": "Trukk",
        "looted_wagon": "Looted-Wagon",
        # Elites
        "meganobz": "Meganobz",
        "nobz": "Nobz",
        "burna_boyz": "Burna-Boyz",
        "kommandos": "Kommandos",
        "tankbustas": "Tankbustas",
        "flash_gitz": "Flash-Gitz",
        "mad_dok_grotsnik": "Mad-Dok-Grotsnik",
        "mek": "Mek",
        "runtherd": "Runtherd",
        "painboy_warbike": "Painboy-on-Warbike",
        "nob_waaagh_banner": "Nob-with-Waaagh-Banner",
        "da_red_gobbo": "Da-Red-Gobbo",
        "skrak_skull_nobz": "Skrak-s-Skull-Nobz",
        # Fast Attack
        "warbikers": "Warbikers",
        "stormboyz": "Stormboyz",
        "deffkoptas": "Deffkoptas",
        "squighog_boyz": "Squighog-Boyz",
        "nob_smasha_squig": "Nob-on-Smasha-Squig",
        "boomdakka_snazzwagons": "Boomdakka-Snazzwagons",
        "kustom_boosta_blastas": "Kustom-Boosta-blastas",
        "megatrakk_scrapjets": "Megatrakk-Scrapjets",
        "shokkjump_dragstas": "Shokkjump-Dragstas",
        "rukkatrukk_squigbuggies": "Rukkatrukk-Squigbuggies",
        "nobz_on_warbikes": "Nobz-on-Warbikes",
        "grot_mega_tank": "Grot-Mega-tank",
        "grot_tanks": "Grot-Tanks",
        "skorchas": "Skorchas",
        "warbuggies": "Warbuggies",
        "wartrakks": "Wartrakks",
        "grot_bomm_launcha": "Grot-Bomm-Launcha",
        # Heavy Support
        "battlewagon": "Battlewagon",
        "deff_dreads": "Deff-Dreads",
        "bonebreaka": "Bonebreaka",
        "gunwagon": "Gunwagon",
        "kill_rig": "Kill-Rig",
        "hunta_rig": "Hunta-Rig",
        "killa_kans": "Killa-Kans",
        "lootas": "Lootas",
        "mek_gunz": "Mek-Gunz",
        "big_trakk": "Big-Trakk",
        "kannonwagon": "Kannonwagon",
        "mega_dread": "Mega-Dread",
        "meka_dread": "Meka-Dread",
        "squiggoth": "Squiggoth",
        "big_gunz": "Big-Gunz",
        "lifta_wagon": "Lifta-Wagon",
        # Flyers
        "dakkajet": "Dakkajet",
        "burna_bommer": "Burna-bommer",
        "blitza_bommer": "Blitza-bommer",
        "wazbom_blastajet": "Wazbom-Blastajet",
        "attack_fighta": "Attack-Fighta",
        "chinork_warkopta": "Chinork-Warkopta",
        "fighta_bommer": "Fighta-bommer",
        # Lords of War
        "gorkanaut": "Gorkanaut",
        "morkanaut": "Morkanaut",
        "stompa": "Stompa",
        "battle_fortress": "Battle-Fortress",
        "gargantuan_squiggoth": "Gargantuan-Squiggoth",
        "kill_tank": "Kill-Tank",
        "kustom_stompa": "Kustom-Stompa",
        "kill_krusha": "Kill-Krusha",
        # Fortifications
        "big_ed_bossbunka": "Big-ed-Bossbunka",
        "mekboy_workshop": "Mekboy-Workshop",
    },
    "adeptus-custodes": {
        # HQ
        "aleya": "Aleya",
        "blade_champion": "Blade-Champion",
        "knight_centura": "Knight-Centura",
        "shield_captain": "Shield-Captain",
        "shield_captain_allarus": "Shield-Captain-in-Allarus-Terminator-Armour",
        "shield_captain_jetbike": "Shield-Captain-on-Dawneagle-Jetbike",
        "trajann_valoris": "Trajann-Valoris",
        "valerian": "Valerian",
        # Troops
        "custodian_guard": "Custodian-Guard",
        "prosecutors": "Prosecutors",
        "custodian_guard_spears": "Custodian-Guard-with-Adrasite-and-Pyrithite-Spears",
        "sagittarum_custodians": "Sagittarum-Custodians",
        # Dedicated Transport
        "anathema_psykana_rhino": "Anathema-Psykana-Rhino",
        "coronus_grav_carrier": "Coronus-Grav-carrier",
        # Elites
        "allarus_custodians": "Allarus-Custodians",
        "custodian_wardens": "Custodian-Wardens",
        "venerable_contemptor": "Venerable-Contemptor-Dreadnought",
        "vexilus_praetor": "Vexilus-Praetor",
        "vexilus_praetor_allarus": "Vexilus-Praetor-in-Allarus-Terminator-Armour",
        "vigilators": "Vigilators",
        "aquilon_custodians": "Aquilon-Custodians",
        "contemptor_achillus": "Contemptor-Achillus-Dreadnought",
        "contemptor_galatus": "Contemptor-Galatus-Dreadnought",
        # Fast Attack
        "vertus_praetors": "Vertus-Praetors",
        "witchseekers": "Witchseekers",
        "agamatus_custodians": "Agamatus-Custodians",
        "pallas_grav_attack": "Pallas-Grav-attack",
        "venatari_custodians": "Venatari-Custodians",
        # Flyers
        "ares_gunship": "Ares-Gunship",
        "orion_assault_dropship": "Orion-Assault-Dropship",
        # Heavy Support
        "venerable_land_raider": "Venerable-Land-Raider",
        "caladius_grav_tank": "Caladius-Grav-tank",
        "telemon_heavy_dreadnought": "Telemon-Heavy-Dreadnought",
    },
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
                        # <DYNASTY>: take only DYDY inner span, skip dynasty-specific sub-names
                        dydy = child.find(class_="DYDY")
                        kw = dydy.get_text(strip=True) if dydy else "<DYNASTY>"
                    elif "tooltipClan" in classes:
                        # <CLAN>: take only CLCL inner span, skip clan-specific sub-names
                        clcl = child.find(class_="CLCL")
                        kw = clcl.get_text(strip=True) if clcl else "<CLAN>"
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
            print(
                f"  {w['name']:<30} {w.get('range',''):<7} {w.get('type',''):<14} "
                f"{w.get('S',''):<5} {w.get('AP',''):<5} {w.get('D',''):<5} {ab}"
            )
    for ab in data.get("abilities", []):
        print(f"  ABIL   {ab}")


def print_stratagems(stratagems: list[dict]) -> None:
    print(f"\n{'='*64}")
    print(f"  STRATAGEMS  ({len(stratagems)} found)")
    print(f"{'='*64}")
    for s in stratagems:
        name = s.get("name", "?")
        cp = s.get("cp", "?")
        typ = s.get("type", "")
        text = s.get("rule_text", "")
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
    unit_slugs = FACTION_UNIT_SLUGS.get(faction, {})

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
        if uid not in unit_slugs:
            known = (
                ", ".join(unit_slugs) if unit_slugs else "(no slugs registered for this faction)"
            )
            print(f"Unknown unit '{uid}'. Known: {known}", file=sys.stderr)
            sys.exit(1)
        units = [(uid, unit_slugs[uid])]
    elif args.all_units:
        if not unit_slugs:
            print(f"No unit slugs registered for faction '{faction}'.", file=sys.stderr)
            sys.exit(1)
        units = list(unit_slugs.items())
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
