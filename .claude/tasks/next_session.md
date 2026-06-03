# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session passiert ist (2026-06-02)

### Ziel 5d — BattleScribe Importer ✅

**Neue Dateien:**
- `src/gameObjects/rosz_importer.py` — Kernlogik: ZIP-Entpack, XML-Validierung (Namespace-Check), Unit-Extraktion, Name-Matching, YAML-Ausgabe
- `tools/import_rosz.py` — CLI-Wrapper: `python tools/import_rosz.py my_army.rosz`
- `tests/gameObjects/test_rosz_importer.py` — 19 Tests

**Integriert in `src/uiLayout/setupScreen.py`:**
- Expander "Import BattleScribe Roster (.rosz / .ros)" über den Roster-Dropdowns
- Deduplizierung via `st.session_state._last_imported_rosz` verhindert Endlosschleife beim rerun

**Name-Matching-Logik:**
- Normalisiert BattleScribe-Namen (`"Necron Warriors"` → slug `"necron_warriors"`)
- Strippt Faction-Prefix: `"necron_"` → sucht in Katalog weiter
- Unterstützte Fraktionen: `necrons`, `adeptus_custodes` (Katalog fehlt noch)
- Leerer Katalog → `ValueError` mit klarer Meldung (kein stiller Fehlschlag)
- Kein Wargear-Import (bewusste Entscheidung für ersten Schritt)

### Bugfixes

**st.progress Crash (Progress > 1.0):**
- `game_state.py`: `count = min(models, u.models_max)` — verhindert zu hohe Wundinitialisierung
- `unitCard.py`: `min(1.0, ...)` auf allen drei progress-Aufrufen

**Duplicate Unit State Keys (StreamlitDuplicateElementKey):**
Roster mit mehreren Einheiten gleichen Typs (z.B. 2× Warriors) crashte mit Key-Kollision.
Ursache: `p1_units = {u.id: state}` überschrieb Duplikate, alle Widget-Keys kollidierten.

**Lösung — 6 Dateien refactored:**
- `game_state.py`: `_make_unit_state_dict()` erzeugt eindeutige Keys mit `#N`-Suffix für Duplikate (`warriors`, `warriors#1`, ...). Neue Hilfsfunktionen: `unit_keys_for()`, `unit_id_from_state_key()`
- `armyList.py`: gibt `unit_keys` an `render_detachment_card` weiter
- `detachmentCard.py`: übergibt `state_key` an `render_unit_card`
- `unitCard.py`: `state_key` Parameter — verwendet diesen für alle Widget-Keys und State-Lookups
- `_common.py`: `lookup()` strippt `#N`-Suffix beim Unit-Lookup
- `armyCard.py`: `unit_id_from_state_key()` beim Ability-Check

**Wichtig:** Mehrfache Einheiten gleichen Typs sind nun vollständig unterstützt — sowohl im Roster-YAML als auch im Game-State (eigene Wunden, eigene Buttons).

### Data-driven Keyword-Matching ✅ (neu)

**Problem:** Keyword-Vergleiche im Frontend waren hart-kodiert (`"CORE" in unit.keywords`, `"Character" in unit.keywords` etc.) — Groß-/Kleinschreibung konnte Fähigkeiten brechen.

**Lösung:**
- `Unit.has_keyword(kw: str) -> bool` — case-insensitive Vergleich direkt am Objekt
- Alle Frontend-Checks in `chargephase.py`, `shootingPhase.py`, `psychicPhase.py`, `unitCard.py` nutzen jetzt `unit.has_keyword()`
- MWBD-Zielauswahl: neue Funktion `_mwbd_required_keywords(faction)` liest `has_keywords`-Condition direkt aus der Ability-Definition; kein String im Frontend mehr
- `unit_abilities.yaml`: `Core` → `CORE` vereinheitlicht

**Constraint verschärft:** Keywords IMMER `UPPERCASE` in allen YAML-Dateien (units.yaml, unit_abilities.yaml, stratagems.yaml etc.). Checks in Python immer via `unit.has_keyword()`.

### App-Umbenennung ✅ (neu)

- `src/app.py`: `page_title` → `"Arbiter"`
- `src/uiLayout/setupScreen.py`: `st.title()` → `"Arbiter"`

---

## Aktueller Status

| Ziel | Status |
|------|--------|
| 5a — Spec | ✅ |
| 5b — Necron-Katalog | ✅ |
| 5b.2 — Datensäuberung | ✅ |
| 5c — Loader-Refactoring | ✅ |
| 5c — Bugfixes (Weapon, MWBD, ResOrb) | ✅ |
| 5e — Setup-Screen Redesign + VP-Config + Header | ✅ |
| 5g — Regelkonformer Setup-Flow | ✅ |
| 5d — BattleScribe Importer | ✅ |
| Keyword-Matching data-driven | ✅ **neu** |
| Orks-Fraktion (vollständig) | 🔄 in Arbeit |
| 5f — Stratagems PoC | ⬜ |

---

## Nächste Schritte (priorisiert)

### Priorität 1 — Orks-Fraktion vollständig scrapen

Der Scraper (`tools/wahapedia_scraper.py`) wurde auf Multi-Faction-Support umgestellt:
- `FACTION_UNIT_SLUGS = {"necrons": {...}, "orks": {...}}` statt monolithischem `UNIT_SLUGS`
- Aufruf: `python tools/wahapedia_scraper.py orks --all`

**Orks-Slugs bereits in Scraper eingetragen** (aus Wahapedia-Faction-Page abgeleitet):
HQ, Troops, Elites, Fast Attack, Heavy Support, Flyers — vollständige Liste.

**Nächste konkrete Schritte:**
1. Scraper-Output für Orks prüfen (läuft gerade oder schon gelaufen)
2. Rohdaten in `data/wh40k_9e/orks/units.yaml` konvertieren (analog zu Necrons)
3. Weapons in `data/wh40k_9e/orks/weapons.yaml`
4. Loader-Test: `load_unit_catalog("orks")` muss > 0 Units zurückgeben
5. Roster-Datei `data/rosters/orks_*.yaml` anlegen für Testspiel

**Wichtig:** Legacy `army.yaml` enthält nur 8 Units (Bad Moons Subfraktion) — der vollständige Katalog soll alle Ork-Einheiten umfassen, nicht nur diese Auswahl.

### Priorität 2 — Ziel 5f: Stratagems PoC

Infrastruktur (GO-Liste, Sichtbarkeitslogik) bereits vorbereitet in `gameProtocoll.py`.
Daten fehlen: `stratagem_conditions`, `triggers` in `data/wh40k_9e/necrons/stratagems.yaml`.

Bisheriger Stand der Stratagems-Datei prüfen:
```bash
head -50 data/wh40k_9e/necrons/stratagems.yaml
```

### Priorität 3 — BattleScribe Importer: Qualitätsverbesserungen

Bekannte Lücken aus Live-Tests:
- Adeptus Custodes Roster erkannt (`faction_dir: adeptus_custodes`) aber Katalog fehlt → klare Fehlermeldung ✅
- Wargear nicht importiert (bewusste Entscheidung) — Hinweis im UI ergänzen?
- Faction-Erkennung: andere Fraktionen (Space Marines, T'au etc.) fallen auf "necrons" zurück → Fehlermeldung statt falschem Import

---

## Bekannte offene Lücken (nicht vergessen)

| Lücke | Beschreibung |
|-------|-------------|
| `resolve_bracket_stats` unverdrahtet | Implementiert in `loader.py`, aber kein UI-Aufruf — Vehicles zeigen immer Basis-Stats |
| Orks-Fraktion fehlt | Scraping läuft — `units.yaml` / `weapons.yaml` noch zu erstellen |
| Adeptus Custodes Katalog fehlt | `data/wh40k_9e/adeptus_custodes/` hat nur Placeholder-Dateien |
| Forge World / Legends importieren | Noch nicht umgesetzt |
| Wargear im Roster-Format | Aktuell nur `id` + `models` — keine Wargear-Auswahl speicherbar |
| Punkte-Validierung | `load_points()` implementiert, aber Roster-Gesamtpunkte werden nicht gegen Spielgröße geprüft |
| Dual-Profil Datasheet | Setup-Phase zeigt nur `profiles[0]` einer Waffe im Datasheet-View |
| Faction-Dir Hardcode | `gameActionsArea._display_unit_datasheet` nutzt `"necrons" if "necrons" in unit.id else "orks"` — muss auf `faction_dir_for()` umgestellt werden |
| CP +1/Runde verifizieren | `_common.py` zeigt "+1 CP (Battle-forged)" — Wahapedia Core Rules Command Phase noch nicht abgerufen |
| Unbekannte Fraktion im Importer | Rosters für Space Marines etc. fallen auf "necrons" zurück statt sauberer Fehlermeldung |

---

## Wichtige Constraints

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts (unveränderlich während Spiel)
- dev-Branch — kein direktes Committen auf main
- **Keywords immer `UPPERCASE` in allen YAML-Dateien** — Checks in Python via `unit.has_keyword()` (niemals direkter String-Vergleich)
- Weapon-Zugriff: Nie `w.is_melee` für Filter nutzen wenn Dual-Profile möglich — `w.for_phase(use_melee)` verwenden
- Session-State Unit-Keys: `p1_units` / `p2_units` mit `#N`-Suffix für Duplikate (seit 2026-06-02)
- CP wird nur durch Game Mechanics verändert (Befehlsphase, Stratagems) — kein manueller Header-Stepper mehr

### State-Key System (seit 2026-06-02)

Mehrfach-Units gleichen Typs im Roster werden mit `#N`-Suffix disambiguiert:
- Erstes Vorkommen: `wh40k_9e.necrons.unit.warriors` (kein Suffix — Backward-Compat)
- Zweites Vorkommen: `wh40k_9e.necrons.unit.warriors#1`
- Drittes Vorkommen: `wh40k_9e.necrons.unit.warriors#2`

`unit_id_from_state_key(key)` strippt den Suffix wieder → gibt echte `unit.id` zurück.
Neue Hilfsfunktionen in `game_state.py`: `unit_keys_for()`, `unit_id_from_state_key()`.
`lookup(faction, uid)` in `_common.py` versteht State-Keys.

### Keyword-Matching (seit 2026-06-02)

`Unit.has_keyword(kw: str) -> bool` ist die einzige erlaubte Methode für Keyword-Checks.
Direkter String-Vergleich (`"CORE" in unit.keywords`) ist verboten — immer `unit.has_keyword("CORE")`.
MWBD-Zielfilter liest `has_keywords` aus Ability-Definition (data-driven, kein Hard-Code).

### Streamlit 1.57 — CSS-Selektoren (gelernte Lektionen)

Falsche Selektoren kosten Zeit. Vor dem Schreiben von CSS immer JS-Source prüfen:
`find .venv -name "*.js" | xargs grep -l "<Komponentenname>"` → dann testids aus dem Minified-JS extrahieren.

| Komponente | Korrekte Selektoren |
|---|---|
| NumberInput Container | `[data-testid="stNumberInputContainer"]` |
| NumberInput Step-Buttons | `[data-testid="stNumberInputStepUp"]`, `[data-testid="stNumberInputStepDown"]` |
| Buttons allgemein | `button[data-testid="stBaseButton-{kind}"]` (nicht `baseButton-{kind}`) |
| Container border=True | `.e1rw0b1u3` (Emotion-Klasse — kann sich bei Streamlit-Update ändern!) |
| Selectbox | `.stSelectbox [data-baseweb="select"] > div` |
