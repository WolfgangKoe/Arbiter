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

So misst du selbst: `pytest tests/architecture/ tests/docs/ tests/acceptance/ --no-cov -q`

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
  `irongob`, `gloom`, `prism`, `dakka`, `klaw`, `tesla`) in den Phasen-/Render-Modulen.
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
