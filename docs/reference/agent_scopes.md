# Agent-Scopes — Aufgaben→Datei-Index

Schnellnavigation für den Koordinator: zu einer Aufgabe genau die nötigen Dateien finden, ohne das ganze Repo zu lesen.

**Dauerhaft** (Referenz-Artefakt, [ADR-0007](../governance/decisions/0007-duenner-koordinator-und-datei-kanal.md))

> Pflegenotiz: handgepflegt; bei größeren Refactorings nachziehen.

---

## Scope-Tabelle

| Aufgabentyp | Pflicht-Lesen | Optional |
|---|---|---|
| **Combat-/Schadens-Mechanik** (Treffer, Verwundung, Save, Schaden, Modifier) | `src/gameMechanic/combat.py`, `src/gameMechanic/attackMath.py`, `docs/spec/processes.md`, `tests/gameMechanic/test_combat.py` | `docs/spec/rules_insights.md`, `docs/work/wahapedia_core_rules/core_rules.txt` |
| **Phase-Logik ändern** (Schießen, Nahkampf, Befehl, Bewegung, Angriff, Psychiker, Moral) | `src/gameMechanic/<phase>Phase.py` bzw. `src/gameMechanic/chargePhase.py`, `src/gameMechanic/phaseRunner.py`, `src/gameMechanic/phaseHandler.py`, `src/gameMechanic/gameState.py` | `docs/spec/processes.md`, `docs/spec/rules_insights.md`, `docs/work/schlachtrunde.md` |
| **Phase-UI anpassen** (Render, Buttons, Layout einer Phase) | `src/gameMechanic/<phase>Phase.py`, `src/uiLayout/gameActionsArea.py`, `src/uiLayout/_common.py` | `docs/spec/ui_layout.md`, `src/app.py` |
| **Stratagem-Effekt umsetzen** (Core- oder Fraktions-Stratagem) | `src/gameObjects/stratagem.py`, `data/wh40k_9e/_shared/stratagems.yaml`, `src/gameMechanic/abilityEngine.py`, `src/gameMechanic/gameState.py` | `data/wh40k_9e/<fraktion>/stratagems.yaml`, `docs/spec/faction_abilities.md`, `tests/gameMechanic/test_ability_engine.py` |
| **Fraktions-/Protokoll-/Direktiv-Effekt** (Faction-Ability, Round-Choice, Triggered) | `data/wh40k_9e/<fraktion>/faction_abilities.yaml`, `src/gameObjects/ability.py`, `src/gameObjects/roundChoiceAbility.py`, `src/gameMechanic/abilityEngine.py`, `docs/spec/faction_abilities.md` | `data/wh40k_9e/<fraktion>/unit_abilities.yaml`, `data/wh40k_9e/<fraktion>/subfaction_abilities.yaml`, `tests/test_faction_abilities_<fraktion>.py` |
| **Waffenstärke / Parsing** (`_parse_strength`, Würfelausdrücke) | `src/uiLayout/_common.py:_parse_strength`, `src/gameObjects/weapon.py`, `tests/gameObjects/test_weapon.py` | `docs/spec/rules_insights.md`, `data/wh40k_9e/<fraktion>/weapons.yaml` |
| **Unit-Zustand / Mutations** (Wunden, Modelle, Turn-Flags, Buffs) | `src/gameMechanic/unitMutations.py`, `src/gameMechanic/gameState.py`, `tests/gameMechanic/test_unit_mutations.py`, `tests/gameMechanic/test_game_state.py` | `docs/spec/architecture.md` (session_state-Schema), `src/app.py` |
| **Neue Fraktion oder Einheit als YAML** | `data/wh40k_9e/<fraktion>/units.yaml`, `data/wh40k_9e/<fraktion>/weapons.yaml`, `src/gameObjects/loader.py`, `docs/spec/loader_contract.md` | `data/wh40k_9e/<fraktion>/faction_abilities.yaml`, `data/wh40k_9e/_shared/shared_abilities.yaml`, `tests/gameObjects/test_loader.py` |
| **Loader / YAML-Schema ändern** | `src/gameObjects/loader.py`, `docs/spec/loader_contract.md`, `tests/gameObjects/test_loader.py` | `src/gameObjects/unit.py`, `src/gameObjects/weapon.py`, `src/gameObjects/detachment.py`, `data/wh40k_9e/_shared/detachment_types.yaml` |
| **Architektur-Test / Invariante** | `tests/architecture/` (alle Dateien), `docs/spec/architecture_invariants.md`, `tests/architecture/_vocab.py` | `docs/spec/architecture.md`, `docs/governance/decisions/` |
| **Army-Sidebar / UnitCard-UI** | `src/uiLayout/armyList.py`, `src/uiLayout/unitCard.py`, `src/uiLayout/armyCard.py`, `src/uiLayout/detachmentCard.py` | `src/uiLayout/_common.py`, `docs/spec/ui_layout.md` |
| **Spielkopf / VP / CP / Log** | `src/uiLayout/gameHeader.py`, `src/uiLayout/gameProtocoll.py`, `src/gameMechanic/gameLog.py`, `src/gameMechanic/gameState.py` | `src/app.py` |
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
- **Checkbox-Vollständigkeit:** alle Unterabschnitte der aktiven Zieldatei durchgehen —
  jede Checkbox auf `stale` (Check gesetzt, aber Code nicht committet) vs. `wirklich offen`
  prüfen. Beleg: `git log --oneline | grep -i <stichwort>` oder `grep -rn <symbol> src/`.
  Keine Checkbox als „erledigt" markieren ohne Code-Beleg; keine als „offen" einplanen
  ohne Verifikation, dass sie nicht bereits committet ist.
- **Entscheidungs-Timing:** Tasks mit Modus `Konsens` (aktive Stakeholder-Entscheidung nötig)
  immer **früh im Plan** platzieren — nicht ans Ende, nicht in Aufgaben verpacken, die erst
  nach > 90 k Token erreicht werden. Faustregel: jede `NEEDS-DECISION`-abhängige Aufgabe
  muss als eigenständiger erster oder zweiter Schritt erscheinen, damit der Stakeholder bei
  vollem Kontext-Headroom entscheiden kann.
- **Prüfbare Checklisten:** Manuelle Verifikations-Checklisten nur aus Punkten bauen, die
  gegen den **aktuellen Implementierungsstand** prüfbar sind; Punkte, die offene Pläne
  voraussetzen, explizit als „blockiert durch <Plan>" kennzeichnen. Grund: S121 — Punkte 3+4
  der Stufe-A-Checkliste setzten die noch fehlende Reaktiv-UI (Plan 015) voraus.
- **Teil-Status statt binär:** Backlog-/`next_session.md`-Einträge für teil-implementierte
  Mechaniken beschreiben „Mechanik X steht+getestet; offen = Variante Y" statt nur
  offen/erledigt. Grund: S115 — die P17-Lock-Mechanik stand, der Eintrag las aber wie
  „nichts da".

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

## Standardsatz für UI-Executor-Briefs (Retromaßnahme S138 — PFLICHT)

Jeder Executor-Brief, der neue UI-Bezeichner/Namen einführt (CSS-Klassen, Funktions-/
Variablennamen, Badge-/Label-Text in `src/`), enthält den Satz: „Namenswahl vorab gegen
INV-4b-Vokabular prüfen (`tests/architecture/test_generic_src_vocab.py`), Fraktions-Wörter
wie ‚banner' vermeiden." Grund: verhindert nachträgliche Vokabular-Schulden statt sie erst
beim Architektur-Gate zu entdecken.

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
Vollsuite/Langläufer im VORDERGRUND abwarten — Endbericht in DERSELBEN Antwort
wie das Suite-Ende, nie vorher zurückkehren (S121: zwei Leerläufe durch
vorzeitige Rückkehr bei Hintergrund-pytest).

## Pflichten für den Executor-Subagent
- **KEIN Commit — der Koordinator committet selbst nach Review + Freigabe.** Der Executor
  macht niemals `git commit`, `git add` oder andere Verdrahtung der Git-History.
- **Plan-Status-Pflicht:** Landet ein Executor den Fix zu einem `docs/audit/plans/`-Plan,
  setzt er dessen Status in `docs/audit/plans/README.md` **im selben Commit** auf erledigt —
  kein separater Nachtrag. Grund: stale `TODO`-Einträge (S115: Plan 031 galt als offen, war
  längst gefixt).

## Selbstprüf-Checkliste (Pflicht vor Rückgabe)
- [ ] Verdrahtung: neuer Code per grep belegt, dass Nicht-Test-Code ihn aufruft
- [ ] Anzeige-Pfad (bei Fixes mit sichtbarem UI-Effekt): Beleg umfasst den *angezeigten*
      Wert (HTML-Output-Test des Render-Pfads), nicht nur die Berechnungsfunktion —
      Anzeige-Code kann lokal neu rechnen (S122-Befund: Eff.-Zeile ignorierte resolve_save-Floor)
- [ ] Heimat: neuer Code sitzt im richtigen Modul
- [ ] Gates: pytest grün, Coverage-Floor ≥ 99 % gehalten, keine vorher-grünen Tests rot
- [ ] Generic-src: keine Fraktions-Strings/-Checks in src/
- [ ] Format: `pre-commit run --files <geänderte Dateien>` ausgeführt und sauber (nicht nur `ruff check`)
- [ ] Stakeholder-Entscheidungen: NUR über Mailbox docs/handoff/ (NEEDS-DECISION) eskaliert,
      NIE direkt im Chat mit dem Stakeholder kommuniziert
- [ ] Handoff-Marker: jede nach docs/handoff/ geschriebene Datei hat Zeile 1
      `STATUS: NEEDS-DECISION|ANSWERED|DONE` — der Koordinator nennt den Marker im Brief
      (S131: zwei rote Doku-Gates nur durch fehlende Marker)
```

## Grundannahmen-Block in Konzept-Aufträgen (Retromaßnahme S131 — PFLICHT)

Jedes Konzept-/Design-Dokument beginnt mit einem Abschnitt **„Grundannahmen"**
(Weltbild, das dem Entwurf zugrunde liegt — z. B. „gewürfelt wird am Tisch, nicht in
der App"), den der Stakeholder VOR den Detail-Entscheidungen bestätigt. Anlass: S131 —
die Fehlannahme „App würfelt" kostete eine komplette Konzept-Iteration. Bewährter
Rückkanal: Stakeholder kommentiert direkt in der Handoff-Datei.

## Auftragsgrößen-Gate (Retromaßnahme S130 — PFLICHT)

- **Kein Executor-Brief über Effort M.** L-Aufgaben MÜSSEN vor Vergabe in 2–3 in sich
  abgeschlossene Teil-Briefs ≤ M geschnitten werden (ein Schritt = ein Brief, jeweils
  eigenständig grün). Der Koordinator prüft das VOR jedem `Agent`-Aufruf.
- **Test-Budget je Brief:** während der Entwicklung nur gezielte Tests
  (`pytest <datei> -q --no-cov`), genau **eine** Vollsuite am Ende des Briefs.
  Die Vollsuite läuft **immer im Vordergrund** — konkret: im selben Tool-Call auf das
  Suite-Ende warten, **`Bash`-Parameter `timeout: 600000` explizit setzen** (Grund:
  der 2-Minuten-Default killt die Vollsuite mitten im Lauf, S136-Retro-Befund),
  `run_in_background` für pytest ist VERBOTEN; Endbericht in derselben Antwort wie das
  Suite-Ende (S121/S130-Befund: vorzeitige Rückkehr kostete ein ~171k-Resume; S131:
  Executor legte sich trotz Klausel mit wartendem Hintergrund-pytest schlafen → Resume
  nötig).
- **Playwright-UI-Verifikation (Standard-Werkzeug seit S136):** Playwright 1.60 +
  Chromium stehen im venv bereit — funktionale UI-Verifikation (Scroll-Position,
  Layout-Shift-Messung, Klick-Abläufe, Konsolen-Snippets wie in `S136_B1_probe.md`
  vorgeführt) ist damit automatisierbar und für Executor-Briefs das Standard-Werkzeug,
  sobald ein Befund reines Beobachten im Browser braucht. **Ersetzt NICHT** die
  Design-Sichtprüfung des Stakeholders (Layout-/Wortlaut-/Ästhetik-Urteil bleibt
  manuell) — deckt nur messbares/funktionales Verhalten ab.
- **Selbst-Stopp-Klausel in jedem Brief:** jeder Brief nennt explizit sein Token-Budget
  und eine harte Stopp-Schwelle (ca. 1,5× des Budgets). Überschreitet der Subagent
  diese Schwelle, **bricht er sofort ab und gibt Zwischenstand zurück** (geänderte Dateien +
  offene Schritte) statt weiterzuarbeiten. Prüfintervall: nach jedem ~20. Tool-Call den
  Eigenverbrauch schätzen; ab 80 % des Budgets nur noch abschließen, nichts Neues beginnen.
  **Gilt auch nach einem `SendMessage`-Resume weiter** (Retro-M4, S146: Auflage 60k Token,
  real ~177k verbraucht — Budget/Schwelle bleiben über den Resume hinweg scharf, keine
  Rücksetzung durch den Kontext-Neustart).

Anlass: S130 — Plan 015 (L) wurde als Einzelauftrag vergeben → 403k Subagent-Token,
entgegen dem S124-Merkposten. Stakeholder-Auflage: darf nicht wieder vorkommen.

- **Handoff-Lifecycle: STATUS: DONE = Datei löschen:** `STATUS: DONE` in einer Handoff-Datei
  bedeutet, dass der Subagent diese Datei **im selben Commit-Schritt löschen muss**, in dem
  er DONE setzt. Nicht „markiert, wird später gelöscht". Der Brief muss dies explizit anweisen.
  Grund: S142-Hygiene-Test — verwaiste DONE-Dateien ohne Löschen lassen die Doku-Gate rot.
  **Verschärfung (S144-Retro-M2):** Der Koordinator darf in Briefen niemals „DONE setzen,
  Datei nicht löschen" anweisen — genau das produzierte in S144 ein Review-NO-GO.
  Erkenntnisse VOR dem DONE in die dauerhaften Artefakte überführen, dann DONE + löschen.
- **Bestandsaufnahme-Pflicht (S144-Retro-M1):** Recherche-/Planner-Briefs müssen vor jeder
  „X fehlt"-Aussage den Ist-Bestand prüfen — `ls`/`grep` über `data/wh40k_9e/<fraktion>/`
  (alle YAML-Dateien, nicht nur die naheliegende) UND `docs/work/`. Grund: S144 — die
  Prämisse „Klan-/Dynastie-Rohtexte fehlen" war falsch; `subfaction_abilities.yaml`
  existierte samt Engine-Anbindung, nur fehlerhaft/wirkungslos.
- **Brief-Session-Nummer (S150-Retro-M3):** Jeder Executor-/Planner-Brief nennt die aktuelle
  Session-Nummer; Statusvermerke des Subagenten nutzen genau diese — keine andere erfinden.
  Anlass: Fehlbuchung „ERLEDIGT (S145)" in S150.
- **UI-Bug-Recherche vollständig (S150-Retro-M4):** Recherche-Briefs zu UI-Bugs zählen ALLE
  Datenfelder des gerenderten Elements auf (nicht nur den vermuteten State). Anlass: S150 —
  `target_name` wurde übersehen, nur `locked_reason` betrachtet.

---

**Kanal-Pflicht:** Stakeholder-Entscheidungen gehen **ausschließlich** über die Mailbox
`docs/handoff/` (Marker `NEEDS-DECISION`) — nie direkt im Chat. Der Koordinator leitet weiter.
