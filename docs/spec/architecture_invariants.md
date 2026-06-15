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

## Status — geprüft 2026-06-15

| # | Invariante | Wächter | Status |
|---|---|---|---|
| INV-1 | `gameObjects/` importiert kein Streamlit (reine Datenebene) | `test_gameobjects_streamlit_free.py` | ✅ 0 Verstöße |
| INV-2 | YAML wird nur über den Loader gelesen (single entry point) | `test_yaml_only_in_loader.py` | ✅ (2 Ausnahmen, begründet) |
| INV-3 | `gameObjects/` hängt nicht von `gameMechanic`/`uiLayout` ab | `test_layer_imports.py` | ✅ 0 Verstöße |
| INV-4 | `src/` ist fraktions-generisch (keine Fraktions-Strings im Code) | `test_generic_src.py` | ✅ (Allowlist = aktuelle Schuld) |

So misst du selbst: `pytest tests/architecture/ --no-cov -q`

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
- `uiLayout/gameHeader.py`, `uiLayout/gameProtocoll.py` — Default-Spielerlabels `"Necrons"`/`"Orks"`.
- `uiLayout/setupScreen.py` — fraktionsspezifischer Caption-Text.

Ziel: DEBT-Einträge nach und nach auflösen (Default aus den gewählten Armeen ableiten) und aus der Allowlist entfernen.

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
