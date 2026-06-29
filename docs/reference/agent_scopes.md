# Agent-Scopes — Aufgaben→Datei-Index

Schnellnavigation für den Koordinator: zu einer Aufgabe genau die nötigen Dateien finden, ohne das ganze Repo zu lesen.

**Dauerhaft** (Referenz-Artefakt, [ADR-0007](../governance/decisions/0007-duenner-koordinator-und-datei-kanal.md))

> Pflegenotiz: handgepflegt; bei größeren Refactorings nachziehen.

---

## Scope-Tabelle

| Aufgabentyp | Pflicht-Lesen | Optional |
|---|---|---|
| **Combat-/Schadens-Mechanik** (Treffer, Verwundung, Save, Schaden, Modifier) | `src/gameMechanic/combat.py`, `src/gameMechanic/attack_math.py`, `docs/spec/processes.md`, `tests/gameMechanic/test_combat.py` | `docs/spec/rules_insights.md`, `docs/work/wahapedia_core_rules/core_rules.txt` |
| **Phase-Logik ändern** (Schießen, Nahkampf, Befehl, Bewegung, Angriff, Psychiker, Moral) | `src/gameMechanic/<phase>Phase.py` bzw. `src/gameMechanic/chargephase.py`, `src/gameMechanic/phase_runner.py`, `src/gameMechanic/phase_handler.py`, `src/gameMechanic/game_state.py` | `docs/spec/processes.md`, `docs/spec/rules_insights.md`, `docs/work/schlachtrunde.md` |
| **Phase-UI anpassen** (Render, Buttons, Layout einer Phase) | `src/gameMechanic/<phase>Phase.py`, `src/uiLayout/gameActionsArea.py`, `src/uiLayout/_common.py` | `docs/spec/ui_layout.md`, `src/app.py` |
| **Stratagem-Effekt umsetzen** (Core- oder Fraktions-Stratagem) | `src/gameObjects/stratagem.py`, `data/wh40k_9e/_shared/stratagems.yaml`, `src/gameMechanic/ability_engine.py`, `src/gameMechanic/game_state.py` | `data/wh40k_9e/<fraktion>/stratagems.yaml`, `docs/spec/faction_abilities.md`, `tests/gameMechanic/test_ability_engine.py` |
| **Fraktions-/Protokoll-/Direktiv-Effekt** (Faction-Ability, Round-Choice, Triggered) | `data/wh40k_9e/<fraktion>/faction_abilities.yaml`, `src/gameObjects/ability.py`, `src/gameObjects/round_choice_ability.py`, `src/gameMechanic/ability_engine.py`, `docs/spec/faction_abilities.md` | `data/wh40k_9e/<fraktion>/unit_abilities.yaml`, `data/wh40k_9e/<fraktion>/subfaction_abilities.yaml`, `tests/test_faction_abilities_<fraktion>.py` |
| **Waffenstärke / Parsing** (`_parse_strength`, Würfelausdrücke) | `src/uiLayout/_common.py:_parse_strength`, `src/gameObjects/weapon.py`, `tests/gameObjects/test_weapon.py` | `docs/spec/rules_insights.md`, `data/wh40k_9e/<fraktion>/weapons.yaml` |
| **Unit-Zustand / Mutations** (Wunden, Modelle, Turn-Flags, Buffs) | `src/gameMechanic/unit_mutations.py`, `src/gameMechanic/game_state.py`, `tests/gameMechanic/test_unit_mutations.py`, `tests/gameMechanic/test_game_state.py` | `docs/spec/architecture.md` (session_state-Schema), `src/app.py` |
| **Neue Fraktion oder Einheit als YAML** | `data/wh40k_9e/<fraktion>/units.yaml`, `data/wh40k_9e/<fraktion>/weapons.yaml`, `src/gameObjects/loader.py`, `docs/spec/loader_contract.md` | `data/wh40k_9e/<fraktion>/faction_abilities.yaml`, `data/wh40k_9e/_shared/shared_abilities.yaml`, `tests/gameObjects/test_loader.py` |
| **Loader / YAML-Schema ändern** | `src/gameObjects/loader.py`, `docs/spec/loader_contract.md`, `tests/gameObjects/test_loader.py` | `src/gameObjects/unit.py`, `src/gameObjects/weapon.py`, `src/gameObjects/detachment.py`, `data/wh40k_9e/_shared/detachment_types.yaml` |
| **Architektur-Test / Invariante** | `tests/architecture/` (alle Dateien), `docs/spec/architecture_invariants.md`, `tests/architecture/_vocab.py` | `docs/spec/architecture.md`, `docs/governance/decisions/` |
| **Army-Sidebar / UnitCard-UI** | `src/uiLayout/armyList.py`, `src/uiLayout/unitCard.py`, `src/uiLayout/armyCard.py`, `src/uiLayout/detachmentCard.py` | `src/uiLayout/_common.py`, `docs/spec/ui_layout.md` |
| **Spielkopf / VP / CP / Log** | `src/uiLayout/gameHeader.py`, `src/uiLayout/gameProtocoll.py`, `src/gameMechanic/game_log.py`, `src/gameMechanic/game_state.py` | `src/app.py` |
| **Regel-Recherche** (9E-Kernregeln, Fraktionsregeln, Gotchas) | `docs/work/wahapedia_core_rules/core_rules.txt`, `docs/work/wahapedia_core_rules/rules_appendix.txt`, `docs/work/schlachtrunde.md` | `docs/work/wahapedia_necrons/`, `docs/work/wahapedia_orks/`, `docs/work/wahapedia_adeptus_custodes/`, `docs/spec/rules_insights.md` |
| **Doku / Backlog pflegen** (next_session, Ziele, Backlog) | `.claude/tasks/next_session.md`, `docs/goals/backlog.md`, `LEITSTAND.md` | `docs/goals/index.md`, `docs/goals/ziel*.md`, `docs/audit/plans/` |
| **Reporting / Token-Tooling** (`token_report.py`, `session_context.py`, Schwellen) | `tools/token_report.py`, `tools/session_context.py`, `docs/metrics/overview.md`, `tests/tools/test_token_report.py` | `docs/metrics/session_archive.json`, `docs/metrics/session_archive.md` |

---

## Planning — Ausgabe-Template

Planner-Subagenten legen ihre Ausgabe nach diesem Format ab (Plan 028 O7):

```
## Planning — <Datum>

**Priorität:** <P1/P2/P3>   **Scope:** <1 Satz>

| Aufgabe | Effort | Token-Schätzung | Modus | Subagent(en) + Tier | Scope-Zeile / Dateien |
|---------|--------|-----------------|-------|---------------------|----------------------|
| …       | XS/S/M | ~Nk             | Gate/Konsent/Konsens | Planner/Executor/Reviewer + Haiku/Sonnet/Opus | `Scope-Tabelle` Z. N |

**Nächster Schritt:** <Datei>/<Abschnitt>
**Offene Entscheidungen:** <NEEDS-DECISION wenn vorhanden>
```

**Pflichtschritte (Planner):**
- **Vor dem Einplanen:** offene vs. erledigte Steps gegen `git log --oneline` +
  `.claude/tasks/next_session.md` abgleichen — **nichts als offen einplanen, das bereits committet ist.**

**Konventionen:**
- `Effort`: XS (<5k Token), S (5–15k), M (15–40k), L (>40k).
- `Modus`: `Gate` = Freigabe vor Umsetzung erforderlich; `Konsent` = kein Widerspruch
  reicht; `Konsens` = aktive Zustimmung aller Beteiligten.
- `NEEDS-DECISION` im Ausgabe-Template markieren, wenn eine Stakeholder-Entscheidung
  blockiert — der Koordinator trägt sie als offene Frage aus.

---

## So nutzt der Koordinator das

Der Koordinator liest diese Tabelle, wählt den passenden Aufgabentyp, und kopiert die **Pflicht-Lesen**-Spalte direkt als `erlaubte Quellen` in den Subagent-Brief. Der Subagent liest ausschließlich diese Dateien — kein freies Repo-Wandern. Dateien aus der **Optional**-Spalte werden nur dann hinzugefügt, wenn der Koordinator sie für den konkreten Auftrag als notwendig einschätzt. Damit bleibt der Subagent-Kontext schlank und der Koordinator behält die Übersicht.

---

## Subagent-Brief — Pflichtfelder

Jeder Koordinator-Brief an einen Subagenten enthält diese Felder (keine Felder auslassen):

```
## Ziel
<1–2 Sätze: Was soll der Subagent erreichen?>

## Scope / erlaubte Quellen
<Pflicht-Lesen-Spalte aus Scope-Tabelle oben — Subagent liest NUR diese, kein freies Repo-Wandern>

## Erlaubte Tools
<z.B. Read, Bash (read-only), Write/Edit (nur mit Freigabe)>

## Output- / Rückgabeformat
Endbericht KNAPP, in fester Reihenfolge:
1. pytest-Zusammenfassungszeile (falls relevant)
2. grep-Belegzeilen (Verdrahtung)
3. git diff --stat (falls Schreib-Task)
4. Gewählte Werte / Befunde
Kein Volltext-Dump. Pfade + Marker zurückgeben, keine langen Inhalte.

## Pflichten für den Executor-Subagent
- **KEIN Commit — der Koordinator committet selbst nach Review + Freigabe.** Der Executor
  macht niemals `git commit`, `git add` oder andere Verdrahtung der Git-History.

## Selbstprüf-Checkliste (Pflicht vor Rückgabe)
- [ ] Verdrahtung: neuer Code per grep belegt, dass Nicht-Test-Code ihn aufruft
- [ ] Heimat: neuer Code sitzt im richtigen Modul
- [ ] Gates: pytest grün, Coverage-Floor ≥ 92 % gehalten, keine vorher-grünen Tests rot
- [ ] Generic-src: keine Fraktions-Strings/-Checks in src/
- [ ] Format: black + ruff (+ isort) ausgeführt
- [ ] Stakeholder-Entscheidungen: NUR über Mailbox docs/handoff/ (NEEDS-DECISION) eskaliert,
      NIE direkt im Chat mit dem Stakeholder kommuniziert
```

**Kanal-Pflicht:** Stakeholder-Entscheidungen gehen **ausschließlich** über die Mailbox
`docs/handoff/` (Marker `NEEDS-DECISION`) — nie direkt im Chat. Der Koordinator leitet weiter.
