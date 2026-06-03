# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session passiert ist (2026-06-03)

### Data-driven Keyword-Matching ✅

- `Unit.has_keyword(kw: str) -> bool` — case-insensitive Vergleich direkt am Unit-Objekt
- Alle Frontend-Checks (`chargephase.py`, `shootingPhase.py`, `psychicPhase.py`, `unitCard.py`) nutzen jetzt `unit.has_keyword()` statt literaler String-Vergleiche
- MWBD-Zielauswahl: `_mwbd_required_keywords(faction)` liest `has_keywords` aus Ability-Definition — kein `"CORE"` im Frontend mehr
- `unit_abilities.yaml`: `Core` → `CORE` vereinheitlicht
- **Constraint:** Keywords IMMER `UPPERCASE` in allen YAML-Dateien; Checks via `unit.has_keyword()`

### App-Umbenennung ✅

- `page_title` und `st.title()` → `"Arbiter"` (war "Battle Tracker")

### Orks-Fraktion — Units + Weapons gescraped ✅

- `tools/wahapedia_scraper.py`: `UNIT_SLUGS` → `FACTION_UNIT_SLUGS` (Multi-Faction); `<CLAN>`-Keyword-Fix (CLCL-Span analog zu DYDY)
- `tools/convert_ork_scrape.py`: neues Konverter-Script (Parser + YAML-Generator)
- `data/wh40k_9e/orks/units.yaml`: **51 Einheiten** mit Stats, Keywords, Waffen-Refs
- `data/wh40k_9e/orks/weapons.yaml`: **82 Waffen** mit Profilen
- Loader-Test aktualisiert: `load_unit_catalog("orks")` → ≥50 Units

### Ziel 5h — Orks-Katalog vervollständigt ✅

Quelle: Wahapedia (WebFetch) — alle fehlenden Datenkategorien ergänzt:

| Datei | Inhalt |
|-------|--------|
| `faction_abilities.yaml` | WAAAGH!, Speedwaaagh!, 'Ere We Go, Mob Rule, Ramshackle, Beast Snagga, Ob.Sec, 7 Psychic Powers |
| `army_rules.yaml` | Warlord (WARBOSS), Detachments, 4 Specialist Detachments |
| `subfaction_abilities.yaml` | 7 Klans (Bad Moons, Blood Axes, Deathskulls, Evil Sunz, Freebooterz, Goffs, Snakebites) |
| `stratagems.yaml` | 29 Stratagems (Core + Klan + Specialist Detachment + Requisitions) |
| `warlord_traits.yaml` | 14 Traits (3 Generic + 7 Klan + 4 Specialist) |
| `relics.yaml` | 11 Relikte (1 pro Klan + 4 Specialist Detachment) |
| `unit_abilities.yaml` | 20 Abilities (WARBOSS, Big Mek, Weirdboy, Painboy, Ghazghkull, Kommandos, etc.) |
| `wargear.yaml` + `wargear_abilities.yaml` | 10 Wargear-Items (Cybork Body, Ammo Runt, Bomb Squig, Grot Oiler, Kustom Jobs…) |
| `weapon_abilities.yaml` | Dakka!, Skorcha, Power Klaw, Killsaw, Choppa, Shokk Attack Gun, etc. |
| `points.yaml` | Alle 51 Einheiten (MFM 2023 Mk I — bei Spielbetrieb verifizieren) |

**Constraint:** `power_level: 0` in units.yaml noch nicht befüllt — nur Punktekosten vorhanden.

---

## Aktueller Status

| Ziel | Status |
|------|--------|
| 5a — Spec | ✅ |
| 5b — Necron-Katalog | ✅ |
| 5c — Loader-Refactoring | ✅ |
| 5e — Setup-Screen Redesign + VP-Config + Header | ✅ |
| 5g — Regelkonformer Setup-Flow | ✅ |
| 5d — BattleScribe Importer | ✅ |
| Keyword-Matching data-driven | ✅ |
| Orks units.yaml + weapons.yaml | ✅ |
| Orks-Katalog vervollständigen (5h) | ✅ 2026-06-03 |
| BattleScribe Importer fraktionsunabhängig | 🔴 **nächster Schritt** |
| 5f — Stratagems PoC | ⬜ |

---

## Nächste Schritte (priorisiert)

### Priorität 1 — BattleScribe Importer fraktionsunabhängig machen 🔴

**Problem:** Beim Import einer Orks-Roster-Datei enthält das exportierte `data/rosters/orks.yaml`:
```yaml
display_name: Orks
faction_dir: necrons   ← FALSCH, sollte "orks" sein
units: []              ← leer, weil Necron-Katalog keine Ork-Namen kennt
```

**Ursachen (in `src/gameObjects/rosz_importer.py`):**

1. **`_FACTION_CATALOGUE_MAP` fehlt Orks:**
   ```python
   _FACTION_CATALOGUE_MAP = {
       "necrons": "necrons",
       "adeptus custodes": "adeptus_custodes",
       # "orks" fehlt!
   }
   ```
   → Ork-Rosters fallen auf Fallback `"necrons"` zurück.

2. **Prefix-Stripping hardcoded für Necrons:**
   ```python
   for prefix in ("necron_", "necrons_"):   # hardcoded!
       if norm.startswith(prefix):
           stripped = norm[len(prefix):]
           if stripped in name_map:
               return name_map[stripped]
   ```
   BattleScribe schreibt z.B. "Ork Boyz" → slug `"ork_boyz"` → kein Match.

3. **Fallback `"necrons"` ist falsch** — sollte Fehler werfen wenn Fraktion unbekannt.

**Fix-Plan (benötigt Freigabe):**

**Datei: `src/gameObjects/rosz_importer.py`**

a) `_FACTION_CATALOGUE_MAP` erweitern:
```python
_FACTION_CATALOGUE_MAP: dict[str, str] = {
    "necrons": "necrons",
    "adeptus custodes": "adeptus_custodes",
    "custodes": "adeptus_custodes",
    "orks": "orks",
    "ork": "orks",
}
```

b) Prefix-Stripping generisch machen — strippt `"{faction_dir}_"` und alle einbuchstabigen Faction-Wörter:
```python
def _match_unit_name(bs_name: str, name_map: dict[str, str], faction_dir: str) -> str | None:
    norm = _normalize(bs_name)
    if norm in name_map:
        return name_map[norm]
    # Strip faction prefix (e.g. "ork_boyz" → "boyz", "necron_warriors" → "warriors")
    for prefix in (f"{faction_dir}_", f"{faction_dir.rstrip('s')}_"):
        if norm.startswith(prefix):
            stripped = norm[len(prefix):]
            if stripped in name_map:
                return name_map[stripped]
    return None
```

c) Fallback von `"necrons"` auf `None` ändern → klare Fehlermeldung wenn Fraktion unbekannt:
```python
faction_dir = _detect_faction(root)
if faction_dir is None:
    raise ValueError("Unknown faction in BattleScribe roster. Add faction to _FACTION_CATALOGUE_MAP.")
```

**Betroffene Dateien:** `src/gameObjects/rosz_importer.py`, `tests/gameObjects/test_rosz_importer.py`

**Danach testen:** Ork-Roster importieren → `faction_dir: orks`, `units: [{id: ..., models: ...}]`

---

### Priorität 2 — Ork-Roster für Testspiel erstellen

Sobald Importer funktioniert: Roster-Datei `data/rosters/orks_bad_moons.yaml` anlegen.
Kann entweder manuell erstellt oder via BattleScribe importiert werden.

Minimal-Roster für Testspiel (analog zu `necrons_1000pts.yaml`):
- Warboss / Weirdboy (HQ)
- Boyz ×10 (Troops)
- Gretchin ×10 (Troops)
- Warbikers ×3 (Fast Attack)

### Priorität 3 — Ziel 5f: Stratagems PoC

Infrastruktur bereits in `gameProtocoll.py` vorbereitet.
Daten fehlen: `stratagem_conditions`, `triggers` in `data/wh40k_9e/necrons/stratagems.yaml`.

---

## Bekannte offene Lücken

| Lücke | Beschreibung |
|-------|-------------|
| Orks-Katalog (Ziel 5h) | ✅ vollständig 2026-06-03 — alle 14 Dateien vorhanden; Punktekosten aus MFM 2023, bei Spielbetrieb verifizieren |
| Importer nicht fraktionsunabhängig | Orks-Import liefert `faction_dir: necrons`, `units: []` — fix in Priorität 1 |
| `resolve_bracket_stats` unverdrahtet | In `loader.py` implementiert, kein UI-Aufruf — Vehicles zeigen immer Basis-Stats |
| Adeptus Custodes Katalog fehlt | `data/wh40k_9e/adeptus_custodes/` hat nur Placeholder-Dateien |
| Ork-Roster für Testspiel fehlt | Braucht Importer-Fix zuerst |
| Ork `power_level: 0` | Codex-Werte noch nicht eingetragen (nur TODO-Marker) |
| Waffen-Duplikate im Ork-Katalog | Kombi-Waffen (Slugga, Rokkit etc.) teilen einen Eintrag — Warboss-Variante hat Sub-Profile, Boyz-Variante nicht |
| Wargear im Roster-Format | Aktuell nur `id` + `models` — keine Wargear-Auswahl speicherbar |
| Punkte-Validierung | `load_points()` implementiert, aber Gesamtpunkte werden nicht geprüft |
| Dual-Profil Datasheet | Setup-Phase zeigt nur `profiles[0]` |
| Faction-Dir Hardcode | `gameActionsArea._display_unit_datasheet` nutzt `"necrons" if "necrons" in unit.id else "orks"` — auf `faction_dir_for()` umstellen |
| Unbekannte Fraktion im Importer | War `"necrons"` Fallback — wird in Priorität 1 behoben |

---

## Wichtige Constraints

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts (unveränderlich während Spiel)
- dev-Branch — kein direktes Committen auf main
- **Keywords immer `UPPERCASE` in allen YAML-Dateien** — Checks via `unit.has_keyword()`
- Weapon-Zugriff: Nie `w.is_melee` wenn Dual-Profile möglich — `w.for_phase(use_melee)` verwenden
- Session-State Unit-Keys: `p1_units` / `p2_units` mit `#N`-Suffix für Duplikate
- CP wird nur durch Game Mechanics verändert (Befehlsphase, Stratagems)

### State-Key System (seit 2026-06-02)

Mehrfach-Units gleichen Typs im Roster werden mit `#N`-Suffix disambiguiert:
- Erstes Vorkommen: `wh40k_9e.necrons.unit.warriors` (kein Suffix)
- Zweites Vorkommen: `wh40k_9e.necrons.unit.warriors#1`

`unit_id_from_state_key(key)` → echte `unit.id`.
`lookup(faction, uid)` in `_common.py` versteht State-Keys.

### Keyword-Matching (seit 2026-06-03)

`Unit.has_keyword(kw: str) -> bool` ist die einzige erlaubte Methode für Keyword-Checks.
Direkter String-Vergleich verboten. MWBD data-driven via `_mwbd_required_keywords(faction)`.

### Streamlit 1.57 — CSS-Selektoren

| Komponente | Korrekte Selektoren |
|---|---|
| NumberInput Container | `[data-testid="stNumberInputContainer"]` |
| NumberInput Step-Buttons | `[data-testid="stNumberInputStepUp"]`, `[data-testid="stNumberInputStepDown"]` |
| Buttons allgemein | `button[data-testid="stBaseButton-{kind}"]` |
| Container border=True | `.e1rw0b1u3` (Emotion-Klasse — prüfen bei Streamlit-Update!) |
| Selectbox | `.stSelectbox [data-baseweb="select"] > div` |
