# Architektur-Invarianten — messbar

> Das Gegenstück zur Test-Coverage: ein **grün/rot-Indikator**, ob der Code dem
> Architekturbild folgt. Durchgesetzt von `tests/architecture/` — läuft im
> normalen `pytest --tb=short` und im CI mit. Bricht ein Wächter, bricht der Build.
>
> **Auf dieses Dokument blickst du regelmäßig.** Es sagt, welche Invarianten gelten,
> wo der Code bewusst (noch) abweicht (Schulden-Ledger), und was *nicht* erzwungen
> wird, weil die Realität dem ursprünglichen Bild widerspricht.

Architektur-Gesamtbild: [architecture.md](architecture.md) · Prozess-Specs: [processes.md](processes.md)

---

## Status — geprüft 2026-06-16

| # | Invariante | Wächter | Status |
|---|---|---|---|
| INV-1 | `gameObjects/` importiert kein Streamlit (reine Datenebene) | `test_gameobjects_streamlit_free.py` | ✅ 0 Verstöße |
| INV-2 | YAML wird nur über den Loader gelesen (single entry point) | `test_yaml_only_in_loader.py` | ✅ (2 Ausnahmen, begründet) |
| INV-3 | `gameObjects/` hängt nicht von `gameMechanic`/`uiLayout` ab | `test_layer_imports.py` | ✅ 0 Verstöße |
| INV-4 | `src/` ist fraktions-generisch (keine Fraktions-**Namen** im Code) | `test_generic_src.py` | ✅ (Allowlist = aktuelle Schuld) |
| INV-4b | `src/` enthält kein Fraktions-**Vokabular** (datengetrieben aus YAML) | `test_generic_src_vocab.py` | ✅ (Ledger = aktuelle Schuld) |
| INV-5 | Doku-Gesundheit: Spec ↔ Tests ↔ Stand laufen nicht auseinander | `tests/docs/`, `tests/acceptance/` | ✅ |
| INV-6 | Reine HTML/SVG-Komposition liegt in `dice_compose.py` — Streamlit-frei und Coverage-gemessen | `test_render_composition_seam.py` | ✅ 0 Verstöße |

So misst du selbst: `pytest tests/architecture/ tests/docs/ tests/acceptance/ --no-cov -q`

### Schulden-Stand (Baseline — fortschreiben pro Session)

Live nach jedem `pytest`-Lauf im **Schulden-Scoreboard** (`tests/conftest.py`). Anker:

| Datum | INV-4b Vokabular (Tokens) | INV-4 Allowlist (Einträge) | INV-5 AC-IDs |
|---|---|---|---|
| 2026-06-16 | 20 | 10 | 5 |
| 2026-06-20 | 19 | 5 | 5 |

Vokabular-/Allowlist-Zahlen sollen **sinken** (Ratchet), AC-IDs **wachsen**.

---

## INV-2 — erlaubte YAML-Zugriffe (Ausnahmen)

| Datei | Grund |
|---|---|
| `gameObjects/loader.py` | **Lese-Entry-Point** für alle Armee-/Katalogdaten |
| `gameObjects/rosz_importer.py` | `.rosz`→YAML-Konverter: **schreibt** nur das konvertierte Roster (`yaml.dump`); gelesen wird weiter über `load_unit_catalog` |

Neue YAML-Zugriffe in anderen Dateien lassen den Wächter scheitern → `YAML_ALLOWED` mit Begründung ergänzen oder über den Loader leiten.

---

## INV-4 — Schulden-Ledger (Generic-src)

Die Allowlist in `test_generic_src.py` hält den Build grün **und** macht den Drift sichtbar.
Zwei Klassen:

**LEGIT (dauerhaft):**
- `gameObjects/rosz_importer.py` — mappt externe BattleScribe-Fraktionslabels auf interne Slugs (I/O-Normalisierung an der Import-Grenze, keine Spiellogik).

**DEBT (Cleanup-Aufgaben → [backlog.md](../goals/backlog.md)):**
- `gameMechanic/game_state.py` — hartcodierte Default-Roster (`necrons_alpha.yaml`/`necrons_beta.yaml`).
- `gameObjects/loader.py` — `faction_dir`-Default `"necrons"`.

  _Erledigt 2026-06-20:_ `gameHeader.py`/`gameProtocoll.py` Default-Spielerlabels
  (`"Necrons"`/`"Orks"` → `"Player 1/2"`) und `setupScreen.py` Caption (fraktions-neutral) —
  aus Allowlist entfernt (10 → 5 Einträge).

Ziel: DEBT-Einträge nach und nach auflösen (Default aus den gewählten Armeen ableiten) und aus der Allowlist entfernen.

---

## INV-4b — datengetriebenes Vokabular-Gate + Ledger

`test_generic_src_vocab.py` erntet das Fraktions-Vokabular **aus den YAML-Daten**
(`_vocab.py`): jedes Wort, das nur in *einer* Fraktion als Eigenname/ID/Keyword
vorkommt (`overlord`, `klaw`, `irongob`, `reanimation`, die Fraktionsnamen) plus
ein kleiner Seed von Konzept-Wörtern (`dynasty`, `waaagh`, `protocol` …). Taucht
so ein Token in einem `src/`-Bezeichner oder String auf → Leck.

- Neue Fraktion ⇒ Vokabular wächst automatisch mit (kein Handpflege-Block).
- `STOPWORDS` filtert generisches Englisch/Core-Regelwerk; `LEDGER` listet die
  **heutige** Schuld pro Datei. Ein neues Token bricht den Build; ein Ledger-Eintrag,
  der nicht mehr leckt, bricht ebenfalls (Ratchet → Schuld nur kleiner).
- Aktuelle Hauptschuld (DEBT): `protocol`/`protocols` als generischer Round-Choice-Begriff
  (Necron-Wort) quer durch `src/`; benannte Items (`orb`, `overlord`, `phaeron`,
  `gloom`, `prism`, `dakka`, `klaw`, `tesla`) in den Phasen-/Render-Modulen.
  (`irongob` 2026-06-20 erledigt: State-Key `pending_irongob` → `pending_triggered_relic`,
  `res_orb_*` → `revive_wargear_*`.)
- LEGIT: `gameObjects/rosz_importer.py` (Fraktionslabel-Normalisierung).

---

## INV-5 — Doku-Gate (Spec ↔ Tests ↔ Stand)

Vierte messbare Schranke neben Coverage und Architektur. Durchgesetzt von:

- `tests/acceptance/` — jede Akzeptanz-ID (`AC-…`) in `docs/spec/acceptance/index.md`
  ist von genau einem Test angepinnt und umgekehrt (fachliche Schranke, Finding #4).
- `tests/docs/` — messbare Doku-Gesundheit: `next_session.md` unter Zeilenbudget,
  Kern-Specs existieren, jede Invariante (`INV-N`) hat einen referenzierenden Wächter
  (Quer-Korrelation Doku ↔ Tests).

Eine fachliche Änderung, die ein Akzeptanzkriterium bricht, wird **rot** → Gespräch
mit dem Nutzer statt stiller Drift (genau der Fehler hinter Finding 9.2).

---

## INV-6 — Render/Composition-Seam (dice_compose.py)

**Regel:** Alle reinen HTML/SVG-Bausteine für die Angriffs-UI (SVG-Würfelgesichter,
Schwellenwert-Header, Modifier-Zeilen, Grid-Zeilen) leben in `src/uiLayout/dice_compose.py`.
Dieses Modul importiert kein Streamlit und ist vollständig durch Unit-Tests abgedeckt.
Nur die drei `st.markdown`-Wrapper-Funktionen verbleiben im ausgenommenen `dice_html.py`.

**Motivation:** Render-Logik, die in Streamlit-Render-Funktionen versteckt war, wurde nicht
von der Coverage erfasst und hat wiederholt zu schwer auffindbaren Bugs geführt (Heroic-
Intervention Duplicate-Key-Crash, Badge-Kompositions-Fehler in `dice_html.py`). Die Seam
stellt sicher, dass Kompositions-Logik immer messbar bleibt.

**Wächter:** `tests/architecture/test_render_composition_seam.py`
- Assert 1: `dice_compose.py` enthält kein `import streamlit` (AST-geprüft).
- Assert 2: `dice_compose.py` steht nicht in `[tool.coverage.run] omit`; kein
  `src/uiLayout/*`-Wildcard, der das Modul stillschweigend verschlucken würde.

**Coverage-Ratchet:** `fail_under` von 90 auf 92 angehoben (2026-06-21) — lockert die
durch diese Seam gewonnene Mess-Abdeckung fest.

---

## Typ-Ratchet — mypy-Fehlerbestand einfrieren (`tools/mypy_gate.py`)

**Regel:** `pyproject.toml` konfiguriert `[tool.mypy] strict = true`, aber der
CI-Step lief bis Plan 038 mit `continue-on-error: true` — der Fehlerbestand
konnte unbemerkt wachsen. Seit Plan 038 ist der Bestand eingefroren:
**der Zähler darf nur noch sinken.**

**Wächter:** `tools/mypy_gate.py` (eigenständiges Skript, NICHT `tests/architecture/` —
mypy braucht ~20–30 s, die lokale Vollsuite läuft viele Male pro Session und
darf nicht langsamer werden). CI-Step in `.github/workflows/deploy.yml`
(„Type check (ratchet gate)") ruft es blocking auf.

**Baseline:** 134 Fehler (gemessen 2026-07-05, Plan 038).

**Ratchet-Logik (beidseitig, INV-4b-Muster):**
- gemessen N > BASELINE → Build rot, „neue Fehler beheben, nicht Baseline erhöhen".
- gemessen N < BASELINE → Build ebenfalls rot, „BASELINE im selben Commit auf N senken"
  (Schrumpfen wird sofort eingelockt, nicht optional nachgezogen).
- gemessen N == BASELINE → Build grün.

Der Abbau des Bestands ist bewusst **kein Teil dieses Plans** — Backlog-Kandidat
(beste Reihenfolge laut `tools/mypy_gate.py`-Wartungshinweis: zuerst `gameMechanic/`
und `gameObjects/`, `uiLayout/` zuletzt wegen manueller Render-Verifikation).
mypy-Versions-Upgrades ändern die Fehlerzahl → BASELINE im selben Commit wie das
Upgrade anpassen (Richtung im Commit begründen).

---

## NICHT erzwungen — bewusste Abweichung vom Ursprungsbild

Die ursprüngliche Vision ([architecture.md](architecture.md)) wollte `gameMechanic/` Streamlit-frei.
**Realität:** Die Phasen-Module (`*Phase.py`) rendern UI und importieren Render-Helfer aus
`uiLayout._common` (6 Dateien). Ein Wächter dafür wäre am Tag 1 rot.

Statt einen falschen Wächter zu bauen, ist dies dokumentierte **Kopplung**:
- `uiLayout/_common.py` ist faktisch ein geteilter Render-Hub (vgl. Audit-Plan 008 „split _common god module").
- Aufräum-Pfad: Phasen-Render-Logik schrittweise nach `uiLayout/` ziehen, sodass `gameMechanic/`
  wieder reine Logik wird — dann kann INV als Wächter „gameMechanic importiert kein uiLayout" nachgezogen werden.

Wenn diese Kopplung bewusst aufgelöst (oder bewusst zementiert) wird, **hier und in
[architecture.md](architecture.md) nachziehen.**

---

## Eine neue Invariante hinzufügen

1. Sicherstellen, dass sie **heute grün** ist (sonst Schulden-Ledger/Allowlist nutzen).
2. Wächter-Test in `tests/architecture/` schreiben (nur Dateisystem/`ast`, keine `src`-Importe).
3. Zeile in die Status-Tabelle oben aufnehmen.
4. Falls sie das Architekturbild ändert: [architecture.md](architecture.md) angleichen.
