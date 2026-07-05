# Plan 041: Regel-Orchestrierung aus Render-Funktionen extrahieren (INV-6-Muster) — Stufe 1: drei gefährlichste Cluster

> **Executor instructions**: Schritt für Schritt folgen, jede Verifikation
> ausführen. Bei STOP-Bedingung: stoppen und berichten. Am Ende Status-Zeile in
> `docs/audit/plans/README.md` aktualisieren. Dieser Plan ist bewusst auf DREI
> Cluster begrenzt — keine weiteren Funktionen „mitnehmen".
>
> **Drift check (zuerst ausführen)**:
> `git diff --stat f6c464a..HEAD -- src/gameMechanic/fightPhase.py src/gameMechanic/psychicPhase.py src/gameMechanic/movementPhase.py pyproject.toml tests/`
> Bei Änderungen: Exzerpte gegen Live-Code prüfen; Abweichung → STOP.
> (Diffs aus Plänen 034/040 in diesen Dateien sind erwartete Drift — nur die
> dort beschriebenen Änderungen.)

## Status

- **Priority**: P2
- **Effort**: L
- **Risk**: MED (Refactoring an spielkritischen Pfaden — deshalb Characterization-First)
- **Depends on**: 034, 040 (gleiche Dateien — strikt nacheinander). NICHT
  parallel zu Plan 015/026 ausführen (ändern `fightPhase.py`/`chargephase.py`).
- **Category**: tests / tech-debt
- **Planned at**: commit `f6c464a`, 2026-07-05

## Why this matters

Die Coverage-Ausnahme für Render-Code ist bewusst — aber in den ausgenommenen
Dateien liegt nicht nur Rendering: Die **Sequenzierung** von Regelfolgen (wann
welche Mutation erlaubt ist, in welcher Reihenfolge Gates greifen) lebt in
`_render_*`-Funktionen mit **null Testabdeckung**, während die darunterliegenden
Primitiven gut getestet sind. Genau in dieser Schicht saßen drei der vier
Correctness-Befunde des Audits 2026-07-05. Das Repo hat für dieses Problem
bereits ein bewährtes Muster: die INV-6-Extraktion (`dice_compose.py` — pure
Kompositionslogik in ein Streamlit-freies, coverage-gemessenes Modul, Render
bleibt dünne Schale, Wächter `tests/architecture/test_render_composition_seam.py`).
Dieser Plan wendet das Muster auf die drei gefährlichsten Cluster an.

## Die drei Cluster (Stand `f6c464a`)

1. **Mortal-Wounds nach Melee** — `src/gameMechanic/fightPhase.py:124-275`
   (`_render_mortal_after_melee`): Schwellenwurf-Gate, Zielfilter
   (`_is_target_engaged`), `apply_mortal_wounds(...)`-Aufruf, `turn_flags`-
   und `pending_mortal_undo`-Mutationen. 0 Testreferenzen.
2. **Smite/Perils/Deny-Sequenz** — `src/gameMechanic/psychicPhase.py:208-366`
   (`_render_smite_flow`, `_render_psi_result`): Perils-muss-zuerst-Gate,
   Deny-Ausgang, Smite-Schaden (`apply_damage`), `turn_flags["cast"]`.
   0 Testreferenzen (die 13 puren Regelfunktionen der Datei sind getestet —
   die Sequenz nicht).
3. **Teleport-Gate** — `src/gameMechanic/movementPhase.py:110-207`
   (`_render_teleport_effect`): „already moved blockiert Teleport"-Gate +
   Prepare→Confirm-Zweischritt um `_lock_teleport_movement`.
   0 Testreferenzen (die Lock/Undo-Primitiven sind getestet).

**Exemplar des Zielmusters**: `src/uiLayout/dice_compose.py` (pure, gemessene
Kompositionslogik; entstanden aus Plan 008/INV-6) und sein Wächter
`tests/architecture/test_render_composition_seam.py`. Vor Beginn beide lesen.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Vollsuite + Coverage | `pytest --tb=short` | exit 0, Coverage ≥ 99 % |
| Architektur-Gate | `pytest tests/architecture/ --no-cov -q` | all pass |
| Cluster-Tests | `pytest tests/gameMechanic/ --no-cov -q` | all pass |
| Lint | `ruff check src/ && black --check src/ && isort --check-only src/` | exit 0 |

## Scope

**In scope:**
- `src/gameMechanic/fightPhase.py`, `psychicPhase.py`, `movementPhase.py`
  (NUR die drei genannten Funktions-Cluster)
- Neue Streamlit-freie Module für die extrahierten Kerne (Namensvorschlag:
  `src/gameMechanic/mortal_flow.py`, `psychic_flow.py`, `teleport_flow.py` —
  oder Erweiterung passender bestehender gemessener Module, wenn < 50 Zeilen)
- Neue Tests unter `tests/gameMechanic/`
- `pyproject.toml` NICHT anfassen: neue `gameMechanic/`-Module sind automatisch
  coverage-gemessen (nur die `*Phase.py`-Dateien stehen in der omit-Liste) —
  das ist der Kern des Musters.

**Out of scope:**
- Die ~12 weiteren ungetesteten `_render_*`-Funktionen (u. a. `_common.py`
  `_render_damage_block`, `_render_resolution_tab`) — explizit **Stufe 2+**,
  erst nach Review dieser Stufe planen.
- Verhaltensänderungen jeglicher Art — reines Characterize-then-Extract;
  jeder im Zuge gefundene Bug wird GEMELDET, nicht gefixt.
- `chargephase.py`, `_common.py`, `uiLayout/` insgesamt.

## Git workflow

- Branch: `refactor/041-render-orchestration-seams`
- Ein Commit **pro Cluster** (Characterization + Extraktion zusammen), z. B.
  `Extract mortal-wound flow into measured module with characterization tests`
- Nicht pushen ohne Anweisung.

## Steps (pro Cluster identisch — Reihenfolge: Teleport → Mortal → Psychic, aufsteigende Komplexität)

### Step A: Characterization-Tests gegen die BESTEHENDE Render-Funktion

Mit dem etablierten Streamlit-Mock (Vorbild: `tests/uiLayout/test_group_flow.py`
und die st-Mock-Fixture in `tests/gameMechanic/conftest.py`) das aktuelle
Verhalten festnageln — pro Cluster mindestens:

- Happy Path (Gate offen → Mutation passiert, State-Effekte asserten),
- jedes Gate einzeln (z. B. „already moved" → kein Teleport-Button-Effekt;
  „Perils offen" → Smite-Pfad blockiert; „Ziel nicht engaged" → kein
  Mortal-Wound-Ziel),
- Undo-/Refund-Pfad, wo vorhanden.

**Verify**: neue Tests grün GEGEN den unveränderten Code
(`pytest tests/gameMechanic/ --no-cov -q`).

### Step B: Kern extrahieren

Entscheidungs- und Mutations-Logik in eine pure Funktion im neuen Modul ziehen
(Signatur: nimmt State-Dicts/Werte, gibt Ergebnis/Änderungen zurück oder
mutiert übergebene Dicts — KEIN `import streamlit`). Die Render-Funktion wird
Schale: liest Widgets, ruft Kern, zeigt Ergebnis.

**Verify**: `pytest tests/gameMechanic/ --no-cov -q` → Characterization-Tests
aus Step A weiterhin grün (das ist der Beweis der Verhaltenstreue);
`pytest tests/architecture/ --no-cov -q` → all pass (neues Modul ist
Streamlit-frei, Layer-Richtung hält).

### Step C: Kern-Tests direkt (ohne Mock) ergänzen

Die Gate-Kombinationen aus Step A zusätzlich als direkte Unit-Tests gegen das
neue Modul (schneller, mock-frei — die Characterization-Tests bleiben als
Schalen-Wächter bestehen).

**Verify**: `pytest --tb=short` → exit 0, Coverage ≥ 99 % (die neuen Module
zählen in den Nenner — sie MÜSSEN voll gedeckt sein).

### Abschluss-Step: Vollsuite, Architektur-Gate, Lint, manuelle UI-Prüfliste

**Verify**: `pytest --tb=short` → exit 0; `pytest tests/architecture/ --no-cov -q`
→ all pass; Lint-Dreier → exit 0.
Manuelle UI-Verifikation im Abschlussbericht auflisten: Teleport-Ablauf
(Prepare→Confirm→Undo), Mortal-Wounds nach Melee (inkl. Undo), Psychic-Sequenz
(Manifest→Perils→Deny→Smite) einmal durchspielen.

## Test plan

Siehe Steps A/C — pro Cluster ~6–10 Tests (Characterization über Mock + direkte
Kern-Tests). Namenskonvention des Repos: Verhalten beschreiben, z. B.
`test_teleport_blocked_after_unit_already_moved`.

## Done criteria

- [ ] 3 neue Streamlit-freie Module existieren, sind voll coverage-gedeckt
- [ ] Die 3 Render-Funktionen enthalten keine Regel-Entscheidungslogik mehr
      (nur Widget-I/O + Kern-Aufruf)
- [ ] `pytest --tb=short` exit 0, Coverage ≥ 99 %; `tests/architecture/` grün
- [ ] Kein Verhaltensunterschied: alle Characterization-Tests aus Step A
      unverändert grün seit Step B
- [ ] `git status`: nur In-Scope-Dateien geändert
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert; manuelle
      UI-Prüfpunkte im Abschlussbericht gelistet

## STOP conditions

- Ein Characterization-Test aus Step A wird durch die Extraktion rot und die
  Ursache ist nicht binnen eines Fix-Versuchs klar → Cluster zurückrollen,
  berichten.
- Beim Characterizen zeigt sich ein **Bug im Ist-Verhalten** (z. B. ein Gate,
  das laut Wahapedia-Regeln falsch sitzt) → Ist-Verhalten festnageln, Bug
  separat MELDEN — in diesem Plan wird kein Verhalten geändert.
- Die Extraktion eines Kerns erfordert > ~150 verschobene Zeilen oder Zugriff
  auf `uiLayout/`-Interna → Cluster als „zu verwachsen für Stufe 1" melden,
  mit den anderen fortfahren.
- Plan 015 hat zwischenzeitlich `fightPhase.py` umgebaut und Cluster 1 passt
  nicht mehr auf die Exzerpte → nur Cluster 2+3 ausführen, Cluster 1 melden.

## Maintenance notes

- Stufe 2+ (weitere ~12 Funktionen, v. a. `_common.py:663-864`
  `_render_damage_block` und `_render_resolution_tab`) bewusst zurückgestellt —
  erst nach Review dieser Stufe und NACH Abschluss von Plan 015/017/018
  (dieselben Dateien) planen.
- Jede künftige neue `_render_*`-Funktion mit Regelentscheidungen sollte den
  Kern von Anfang an im gemessenen Modul haben (INV-6-Muster als Default) —
  Reviewer-Checkpunkt.
- Wenn alle Phase-Orchestrierungen extrahiert sind, kann die coverage-omit-Liste
  in `pyproject.toml` um die `*Phase.py`-Einträge schrumpfen (Ratchet-Idee für
  später — nicht Teil dieses Plans).
