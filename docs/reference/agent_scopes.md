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
| **Doku / Backlog pflegen** (briefing, Ziele, Backlog) | `.claude/tasks/briefing.md`, `docs/goals/backlog.md`, `LEITSTAND.md` | `docs/goals/ziel*.md`, `docs/audit/plans/` |
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
- **Vollständige Session-Planung (S163-Rüge):** Der Plan deckt die GESAMTE Session ab —
  von Session-Start bis Commit. Neben den Implementierungs-Tasks enthält die Plan-Tabelle
  eigene Zeilen für: manuelle UI-Verifikation (mit konkreten Prüf-Punkten), Artefakt-Nachzug
  (Backlog/Briefing/Specs/Handoff) und den Abschluss-Dreiklang Review→Retro→Commit inkl.
  Token-Schätzung für diesen Overhead. Ein Plan, der nur Feature-Tasks listet, ist
  unvollständig.
- **Vor dem Einplanen:** offene vs. erledigte Steps gegen `git log --oneline` +
  `.claude/tasks/briefing.md` abgleichen — **nichts als offen einplanen, das bereits committet ist.**
- **Checkbox-Vollständigkeit:** alle Unterabschnitte der aktiven Zieldatei durchgehen —
  jede Checkbox auf `stale` (Check gesetzt, aber Code nicht committet) vs. `wirklich offen`
  prüfen. Beleg: `git log --oneline | grep -i <stichwort>` oder `grep -rn <symbol> src/`.
  Keine Checkbox als „erledigt" markieren ohne Code-Beleg; keine als „offen" einplanen
  ohne Verifikation, dass sie nicht bereits committet ist.
- **Item-Mengen zählen statt schätzen (M1, S155):** Bei Format-Umbauten (z. B. „Suffix auf
  alle X ausweiten", Spalten-/Schema-Änderungen über mehrere Vorkommen) die betroffene
  Menge per `grep -c`/`wc -l` **zählen**, nicht schätzen — Zahl + Befehl im Plan nennen.
  Grund: B-028-Planung (S154) zeigte, dass geschätzte Mengen den echten Scope verfehlen
  können (10 Call-Sites real vs. angenommene „paar Stellen").
- **Backlog-Prio nach Session-Fokus (S155):** Bei jedem Planning die offenen Zeilen in
  `docs/goals/backlog.md` so umsortieren, dass die Items der aktuell geplanten Session
  ganz oben in Bearbeitungsreihenfolge stehen. Betrifft nur die Reihenfolge offener Items —
  die Archivierung erledigter Items bleibt die bestehende Regel (CLAUDE.md Session-Workflow
  Punkt 5), hier nicht dupliziert.
- **Entscheidungs-Timing:** Tasks mit Modus `Konsens` (aktive Stakeholder-Entscheidung nötig)
  immer **früh im Plan** platzieren — nicht ans Ende, nicht in Aufgaben verpacken, die erst
  nach > 90 k Token erreicht werden. Faustregel: jede `NEEDS-DECISION`-abhängige Aufgabe
  muss als eigenständiger erster oder zweiter Schritt erscheinen, damit der Stakeholder bei
  vollem Kontext-Headroom entscheiden kann.
- **Prüfbare Checklisten:** Manuelle Verifikations-Checklisten nur aus Punkten bauen, die
  gegen den **aktuellen Implementierungsstand** prüfbar sind; Punkte, die offene Pläne
  voraussetzen, explizit als „blockiert durch <Plan>" kennzeichnen. Grund: S121 — Punkte 3+4
  der Stufe-A-Checkliste setzten die noch fehlende Reaktiv-UI (Plan 015) voraus.
- **Testfall-Voraussetzungen beim Task-Zuschnitt prüfen (Retro-M2, S160):** Vor dem
  Einplanen einer manuellen UI-Verifikation den benötigten Daten-/Roster-Bestand per
  `ls`/`grep` verifizieren (z. B. `grep -rn "<einheit>" data/rosters/`). Fehlt eine
  Voraussetzung, wird sie als eigener Vorbereitungs-Task eingeplant oder der Testfall als
  „blockiert durch <Voraussetzung>" gekennzeichnet — nie ein nicht durchführbarer Testfall
  ausgeliefert. Anlass: S159 — B-028b Testfall 3 setzte einen Canoptek Spyder voraus, den
  kein Roster enthielt.
- **Teil-Status statt binär:** Backlog-/`briefing.md`-Einträge für teil-implementierte
  Mechaniken beschreiben „Mechanik X steht+getestet; offen = Variante Y" statt nur
  offen/erledigt. Grund: S115 — die P17-Lock-Mechanik stand, der Eintrag las aber wie
  „nichts da".
- **Scope-Discovery vor Schätzung bei unbekanntem Ist-Zustand (S157):** Trägt ein Item einen
  unbekannten/unklaren Ist-Zustand (z. B. „Suffix auf alle X ausweiten" ohne geprüften
  Bestand), erst eine Scope-Discovery durchführen (Ist-Zustand der betroffenen Stellen
  ermitteln), danach die Aufwandsschätzung abgeben — nicht umgekehrt. Anlass: B-028 —
  Schätzung ~35k (auf Basis der alten Beschreibung) wich real auf 100k+ ab, weil der Scope
  erst nach der Schätzung ermittelt wurde.
- **Definition of Ready (DoR) vor Freigabe-Reife (S165-Retro-M1):** Kein Umsetzungs-Task
  erhält Freigabe-Reife, dessen Backlog-Item die DoR nicht erfüllt — (a) „Benötigte
  Regeln-Scopes" in `docs/goals/backlog_details.md` konkret befüllt (kein „—" bei Items mit
  Regel-/UI-Bezug), (b) Akzeptanzkriterien aus den lokalen Regelquellen beigelegt, (c)
  Refinement-Fragen dokumentiert. DoR-Definition kanonisch: `docs/governance/operating_model.md`
  Event 1; Feldschema: `docs/goals/backlog_details.md`.
- **Tier + Lesedisziplin (S167, [ADR-0009](../governance/decisions/0009-planner-tier-auf-opus.md)):**
  Der Planner läuft als Default durchgehend auf **Opus** (kein Sonnet-Vorlauf) — Auflage:
  briefing.md + aktive Zieldatei + `backlog.md` + Index **gezielt** nach Scope-Zeile lesen,
  keine Volltext-Lektüre. Ausnahme: Bei großen Schreib-Artefakten (> ~300 Zeilen, z. B.
  Migrations-/Split-Dokumente) darf die Ausarbeitung nach fertigem Opus-Konzept an Sonnet
  delegiert werden. Tier-Regel kanonisch: `docs/governance/operating_model.md`
  Abschnitt „Rollen & Model-Tier", hier nicht dupliziert.

**Konventionen:**
- `Effort` (Subagent-Gesamt-Tokens, kalibriert S165-Retro-M2 — Ist-Werte S165: Task 0 XS
  ~5k geschätzt → ~50k tatsächlich, Task 1b M ~20–25k geschätzt → ~190k tatsächlich):
  XS ≈50k, S ≈100–120k, M ≈190k+, L weiterhin >M — vor Vergabe in ≤M-Teil-Briefs splitten
  (S130-Auflage). Identische Buckets nutzt seit S152 auch die Effort-Spalte in
  `docs/goals/backlog.md` (B-099b) — keine zweite, abweichende Konvention einführen; die
  Legende dort trägt dieselbe Skala.
- `Effort: test-/mock-lastige UI-Briefs (S170-Retro-M1):** Executor-Briefs, die gemeinsam
  Render-Code und Test-Mocks anfassen, werden mit Faktor **×2,5** (statt ×1,5) kalkuliert
  oder vor Vergabe in ≤M-Teil-Briefs gesplittet. Ist-Werte S170: T2 ~121k/60k-Budget,
  T4-aef ~244k/120k-Budget; Faktor ×1,5 reichte nicht aus.
- `Modus`: `Gate` = Freigabe vor Umsetzung erforderlich; `Konsent` = kein Widerspruch
  reicht; `Konsens` = aktive Zustimmung aller Beteiligten.
- `NEEDS-DECISION` im Ausgabe-Template markieren, wenn eine Stakeholder-Entscheidung
  blockiert — der Koordinator trägt sie als offene Frage aus.

---

## So nutzt der Koordinator das

Der Koordinator liest diese Tabelle, wählt den passenden Aufgabentyp, und kopiert die **Pflicht-Lesen**-Spalte direkt als `erlaubte Quellen` in den Subagent-Brief. Der Subagent liest ausschließlich diese Dateien — kein freies Repo-Wandern. Dateien aus der **Optional**-Spalte werden nur dann hinzugefügt, wenn der Koordinator sie für den konkreten Auftrag als notwendig einschätzt. Damit bleibt der Subagent-Kontext schlank und der Koordinator behält die Übersicht.

**Fertigmeldungen vollständig (S157 — PFLICHT):** Meldet der Koordinator dem Stakeholder ein
fertiggestelltes Feature/Item, nennt er im selben Zug die noch offenen Geschwister-Items
derselben Verifikation/desselben Features — nie das fertige Teilstück isoliert vermelden.
Anlass: S157 — B-103 wurde fertig gemeldet, ohne auf die noch offenen B-104/B-105 aus
derselben Quantum-Shielding-UI-Verifikation hinzuweisen.

---

## Standardsatz für UI-Executor-Briefs (Retromaßnahme S138 — PFLICHT)

Jeder Executor-Brief, der neue UI-Bezeichner/Namen einführt (CSS-Klassen, Funktions-/
Variablennamen, Badge-/Label-Text in `src/`), enthält den Satz: „Namenswahl vorab gegen
INV-4b-Vokabular prüfen (`tests/architecture/test_generic_src_vocab.py`), Fraktions-Wörter
wie ‚banner' vermeiden." Grund: verhindert nachträgliche Vokabular-Schulden statt sie erst
beim Architektur-Gate zu entdecken.

## Standardsatz für Doku-/Aufräum-Briefs (Retromaßnahme M3, S158 — PFLICHT)

Jeder Executor-Brief, der Doku-/Handoff-Aufräumarbeit beauftragt, enthält den Satz:
„Lösch-Whitelist PFLICHT — du darfst ausschließlich die in diesem Brief namentlich
genannten Dateien löschen; jede andere Löschung ist Abbruch + Rückfrage." Anlass S158:
ein Doku-Agent löschte unbeauftragt eine NEEDS-DECISION-Datei und regenerierte
Metrics-Dateien, die nicht Teil des Auftrags waren.

**(Retromaßnahme S169-M1 — PFLICHT):** Vor JEDER Whitelist-Löschung Pflicht-Grep **je Datei** (Voll- UND Kurzname, z. B. `21-29-43` als Kurzform von `Bildschirmfoto vom 2026-07-09 21-29-43.png`) über `docs/` UND `src/`; Treffer in aktiven Artefakten ⇒ Referenz erst umbiegen, dann löschen — gilt für ALLE Dateitypen (Screenshots, Mockups, Marker, Handoff-Dateien), nicht nur Screenshots.

## Standardsatz für UI-/Ability-Briefs (Retromaßnahme S165 — PFLICHT)

Anlass: S165 B-028c1 — fünf Sessions Ping-Pong (Vollbreiten-Kachel, Design-System-Bruch)
plus fachliche Fehlklassifikation (GO-Karte für eine Pflicht-Trigger-Ability, die
„Explodes"-Familie); keine Verifikationsrunde stellte die Grundfrage „ist das überhaupt
optional?" bzw. „ist das die richtige Bauform?".

- **(a) UI-Brief-Pflicht:** Jeder UI-verdrahtende Brief MUSS Komponente + Anker mit
  §-Verweis auf `docs/spec/design_system.md` benennen. Passt keine bestehende Komponente
  → STOP + NEEDS-DECISION mit Komponenten-Vorschlag, nie Ad-hoc-Bauform.
- **(b) Ability-Brief-Pflicht:** Jeder Ability-Brief MUSS die fachliche Einordnung
  (optional/GO vs. Pflicht-Trigger vs. passiv) mit wörtlichem Wahapedia-Zitat belegen.
- **(c) Spec-first-Gate (erweitert S167):** Jede **neue oder geänderte** UI-Bauform
  durchläuft erst eine Spec-Änderung (Mockup + `design_system.md`-Update) zur
  Stakeholder-Abnahme, dann Code — kein Design ohne Schema, keine Komponenten-Änderung ohne
  vorherigen Spec-Abgleich. Abgenommene Mockups/Änderungen wandern in die zuständige Spec.
- **(d) Reviewer-Checkliste:** Jede Review-Checkliste (Subagent- wie Selbstprüfung)
  bekommt den expliziten Punkt „Design-System-Konformität (Komponente, Anker, Wortlaut)
  geprüft" — s. Ergänzung in der Selbstprüf-Checkliste unten.
- **(e) Screenshot-Konvention (Retromaßnahme S166 — PFLICHT):** UI-Mockup-Briefs
  referenzieren zusätzlich zu den `design_system.md`-§-Zitaten konkrete App-Screenshots
  (Stakeholder-Vorlage oder selbst mit Playwright erstellt) als verbindliche
  Bauform-Referenz. Text-/§-Verweise allein reichen nicht. Anlass S166: Mockup V1 (nur
  §-Zitate) wich von der Ist-UI ab und wurde abgelehnt; Mockup V2 (mit Screenshot-Referenzen
  auf Psi-Flow/Heroic-Intervention) „passt deutlich besser".

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
5. `pre-commit run --files <geänderte Dateien>` laufen lassen + Ergebnis (sauber/Diff) im
   Bericht nennen (Retro-M3, S164 — DoD-Punkt 5 stand im Brief, wurde aber nicht ausgeführt:
   5× E501 + black-Diff blieben unentdeckt bis zum Review).

## Pflichten für den Executor-Subagent
- **KEIN Commit — der Koordinator committet selbst nach Review + Freigabe.** Der Executor
  macht niemals `git commit`, `git add` oder andere Verdrahtung der Git-History.
- **Werkzeug-Klausel (S123, präzisiert M2/S155):** Dateiänderungen ausschließlich über
  Edit/Write; Bash nur lesend bzw. für `git`/`pytest` — kein `sed`/`echo >`/sonstige
  Bash-Textmutation. **Ausnahme:** script-gestützte Massen-Edits (z. B. ein kurzes Python-/
  Skript-Programm für viele gleichförmige Stellen) sind zulässig, wenn (1) der Subagent das
  Werkzeug im Bericht offenlegt (welches Skript, welcher Aufruf) UND (2) danach ein grüner
  Gate-Beleg vorliegt (`pytest --tb=short` + Architektur-/Doku-Gate). Akzeptierter
  Präzedenzfall: B-099b (S153) — offengelegter Skript-Edit + grüner Gate-Beleg, im Review
  bestätigt. **Verboten (Retro-M1, S158):** repo-weite/History-verändernde Git-Kommandos
  (`git stash`, `git reset`, `git checkout` auf fremde Pfade) — Anlass: eine `git stash`-Probe
  eines Executors setzte die uncommitteten Änderungen eines parallel laufenden Executors
  zurück.
- **UI-Verifikations-Pflicht (S155, Template S156-Retro Maßnahme 5):** Offene manuelle
  UI-Verifikationen (CLAUDE.md-DoD-Punkt 6) liefert der Executor IMMER als eigene
  Handoff-Datei in `docs/handoff/` mit den exakten Prüfschritten — nie nur im Chat oder
  nur als Zeile in `briefing.md`. Jede Verifikation nennt genau drei Felder: (a)
  **Voraussetzungen** — welches Roster, wie wird der Zustand in der App erreicht; (b)
  **Klickpfad** — präziser Schritt-für-Schritt-Weg bis zum Prüfzustand; (c) **Erwartung**
  — präzise, inkl. Ausgangs-State der beteiligten Einheiten (`charged`/`in-melee`/
  `heroic-intervened` explizit nennen). Nur durchführbare Testfälle, ein Testfall pro
  Punkt, keine Sammelpunkte. Grund: der Stakeholder soll offene UI-Prüfungen unabhängig
  von der laufenden Session-Arbeit nachholen können. Marker: **`STATUS: AWAITING-VERIFICATION`**
  (nicht `NEEDS-DECISION` — eine Sichtprüfung ist keine Entscheidungsfrage; Retro-M1, S160/S161).
  **Zusätzlich drei Pflicht-Checkpunkte je Verifikation (S165-Retro-M3, ergänzt den
  Reviewer-Ratchet um die Stakeholder-Perspektive):** (1) „Ist die Interaktion regelkonform
  (optional vs. Pflicht)?", (2) „Komponente + Anker laut design_system.md-§?", (3)
  „Wortlaut-Familie korrekt?".
- **Diagnose-Ratchet „UI-Erreichbarkeit des Beweispfads" (Retromaßnahme S166 — PFLICHT):**
  Eine „kein Bug / bereits regelkonform"-Schlussfolgerung ist nur zulässig, wenn die Repro
  den echten Klickpfad nachstellt — d. h. den Session-State so aufbaut, wie die UI ihn
  erzeugt (inkl. Selector-Defaults), nicht nur bestehende Unit-Tests zitiert. Anlass S166:
  die B-123-Erstdiagnose zog „kein Bug" aus einem UI-unerreichbaren Testpfad (Tests ohne
  `damage_active_group_id` simulierten einen Zustand, den die echte UI für
  Mehrgruppen-Einheiten praktisch nie erzeugt) — erst der Stakeholder-Praxistest deckte den
  echten Bug auf.
- **Plan-Status-Pflicht:** Landet ein Executor den Fix zu einem `docs/audit/plans/`-Plan,
  setzt er dessen Status in `docs/audit/plans/README.md` **im selben Commit** auf erledigt —
  kein separater Nachtrag. Grund: stale `TODO`-Einträge (S115: Plan 031 galt als offen, war
  längst gefixt).

## Selbstprüf-Checkliste (Pflicht vor Rückgabe)
- [ ] Verdrahtung: neuer Code per grep belegt, dass Nicht-Test-Code ihn aufruft
- [ ] Anzeige-Pfad (bei Fixes mit sichtbarem UI-Effekt): Beleg umfasst den *angezeigten*
      Wert (HTML-Output-Test des Render-Pfads), nicht nur die Berechnungsfunktion —
      Anzeige-Code kann lokal neu rechnen (S122-Befund: Eff.-Zeile ignorierte resolve_save-Floor)
      — bei neuen Render-Verdrahtungen zusätzlich ein Test, der den Render-**Einstiegspfad**
      (die Spaltenfunktion selbst, inkl. ihrer Gate-Bedingung) mit einem realistischen
      `session_state`-Fixture durchläuft, nicht nur die isolierte Render-Funktion direkt
      aufruft (S164-Lehre)
- [ ] Heimat: neuer Code sitzt im richtigen Modul
- [ ] Gates: pytest grün, Coverage-Floor ≥ 99 % gehalten, keine vorher-grünen Tests rot
- [ ] mypy: `python tools/mypy_gate.py` ausgeführt, Fehlerzahl nicht gestiegen (S128)
- [ ] Generic-src: keine Fraktions-Strings/-Checks in src/
- [ ] Format: `pre-commit run --files <geänderte Dateien>` ausgeführt und sauber (nicht nur `ruff check`)
- [ ] Stakeholder-Entscheidungen: NUR über Mailbox docs/handoff/ (NEEDS-DECISION) eskaliert,
      NIE direkt im Chat mit dem Stakeholder kommuniziert
- [ ] Handoff-Marker: jede nach docs/handoff/ geschriebene Datei hat Zeile 1
      `STATUS: NEEDS-DECISION|ANSWERED|DONE|AWAITING-VERIFICATION` — der Koordinator nennt
      den Marker im Brief (S131: zwei rote Doku-Gates nur durch fehlende Marker)
- [ ] Design-System-Konformität (Komponente, Anker, Wortlaut) geprüft (Retro S165 — B-028c1
      Vollbreiten-Kachel + falsche GO-Karte für einen Pflicht-Trigger)
- [ ] Berührte UI-Bauform in `design_system.md` §1 registriert? (falls fehlend: Ist-Zustand
      im selben Change knapp nachtragen — B-124-Ratchet). Jede §1-Registrierung enthält
      PFLICHT ein schematisches Mini-Schema (ASCII/Markdown) der Bauform, nicht nur Prosa
      (Retromaßnahme S168-M1 — Stakeholder-Ablehnung von Prosa-only-§7)
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
- **Core-Logik+UI+Test-Mix als Default-Splitkriterium (Retro-M4, S158):** Aufgaben, die
  Core-Logik, UI und Tests gemeinsam anfassen, werden standardmäßig in 2 Briefs geschnitten
  — Anlass: ein Executor verbrauchte ~272k Token bei 45k Stopp-Schwelle (Selbst-Stopp griff
  erneut nicht, gleiches Muster wie S146).
- **Test-Budget je Brief:** während der Entwicklung nur gezielte Tests
  (`pytest <datei> -q --no-cov`), genau **eine** Vollsuite am Ende des Briefs.
  Die Vollsuite läuft **immer im Vordergrund** — konkret: im selben Tool-Call auf das
  Suite-Ende warten, **`Bash`-Parameter `timeout: 600000` explizit setzen** (Grund:
  der 2-Minuten-Default killt die Vollsuite mitten im Lauf, S136-Retro-Befund),
  `run_in_background` für pytest ist VERBOTEN; Endbericht in derselben Antwort wie das
  Suite-Ende (S121/S130-Befund: vorzeitige Rückkehr kostete ein ~171k-Resume; S131:
  Executor legte sich trotz Klausel mit wartendem Hintergrund-pytest schlafen → Resume
  nötig).
- **Hintergrund-Monitore verboten (Retro-M1, S160):** Subagent-Briefs dürfen keine
  Arbeitsschritte enthalten, die auf Hintergrund-Monitore oder Hintergrund-Prozesse
  warten (`run_in_background`, Monitor-Wakeups) — sämtliche Gate-Belege (pytest, mypy,
  pre-commit, Playwright) entstehen im Vordergrund, der Endbericht kommt in derselben
  Antwort wie der letzte Gate-Beleg. Gilt zusätzlich zur Vollsuite-Vordergrund-Pflicht
  oben. Anlass: S159 — 2× Nachstoß nötig, weil Executoren auf Hintergrund-Monitore
  warteten.
- **Selbstprüf-Suite im Vordergrund (S163-Retro-M3):** Executoren führen ihre
  Selbstprüf-Vollsuite im Vordergrund aus und beenden ihren Turn nie, während ein
  eigener Hintergrund-Task läuft — Abschlussbericht erst nach vorliegendem Ergebnis.
  Anlass: T1-Executor S163 benötigte zwei Weckrufe.
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
- **Parallele Code-Executor im selben Working Tree (Retro-M2, S158):** nur bei nachweislich
  disjunkten Dateien UND striktem Verbot repo-weiter Git-Operationen (s. Werkzeug-Klausel
  oben) — sonst Worktree-Isolation verwenden. Vollsuite-Ergebnisse paralleler Läufe sind
  nur für den eigenen Scope belastbar, nicht als globaler Grün-Beleg zu werten. Anlass:
  ein bewegtes Ziel (parallel laufender Executor änderte Dateien während der Vollsuite)
  erzeugte 5 Schein-Failures. **Ergänzung (Retro-M2, S162):** die belastbare Vollsuite
  läuft nach Abschluss ALLER parallelen Executoren beim **Koordinator** auf dem
  kombinierten Endstand — Executor-Vollsuiten in Parallel-Setups dienen nur der
  Selbstprüfung; Nicht-Scope-Failures melden Executoren als Befund, statt sie zu fixen.
  Anlass: S162 — Executor-Vollsuite meldete 1 Schein-Failure (bewegtes Ziel durch den
  parallelen Doku-Executor), der kombinierte Endstand war grün.

Anlass: S130 — Plan 015 (L) wurde als Einzelauftrag vergeben → 403k Subagent-Token,
entgegen dem S124-Merkposten. Stakeholder-Auflage: darf nicht wieder vorkommen.

- **Token-Schätzfaktor (Retromaßnahme S169-M2):** Executor-Token-Schätzungen werden ab sofort **×1,5** als Budget angesetzt; Selbst-Stopp-Schwelle = 2× der ursprünglichen Schätzung; bei prognostiziertem Realverbrauch **> 250k** wird der Brief VOR Vergabe gesplittet. Anlass: S168/S169 — Schätzungen wiederholt Faktor ~1,5–1,7 zu niedrig (T3 ~288k/180k, T4 ~325k/190k).

- **Budget-Profil für UI-Verdrahtungs-Tasks (Retro-M2, S164):** UI-Verdrahtungs-Briefs und
  die zugehörige Live-UI-Verifikation werden als **getrennte** Aufträge vergeben.
  Verifikations-Rückmeldungen sind auf **max. 2 Runden** gedeckelt — danach geht der Befund
  als Handoff an den Koordinator zurück statt einer dritten Nachbesserungsrunde im selben
  Executor-Kontext. Anlass: S164 — ein T2-Executor verbrauchte ~311k Token gegen ~20k
  Budget durch eine Live-Verifikations-Schleife mit 3 Runden + Session-Limit-Abbruch/Resume.

- **Budget-Profil für Backlog-Archivierung (Retro-M3, S172):** Archiv-Verschiebungen
  erledigter Items (Backlog-Zeile + Details-Block → `backlog_archive.md`/`docs/goals/archive/`)
  werden als **eigener Brief-Typ** mit realistisch **~100k** budgetiert und **nicht** mit
  übriger Artefakt-Pflege (briefing/Backlog-Sortierung) in einen XS-Brief gebündelt —
  alternativ übernimmt sie der Koordinator direkt. Anlass: S172 — Artefakt-Pflege-Brief
  (Haiku) ~138k Ist vs. ~40k Budget, weil eine 133-Zeilen-Archivverschiebung als XS
  budgetiert war.

- **Handoff-Lifecycle: STATUS: DONE = Datei löschen:** `STATUS: DONE` in einer Handoff-Datei
  bedeutet, dass der Subagent diese Datei **im selben Commit-Schritt löschen muss**, in dem
  er DONE setzt. Nicht „markiert, wird später gelöscht". Der Brief muss dies explizit anweisen.
  Grund: S142-Hygiene-Test — verwaiste DONE-Dateien ohne Löschen lassen die Doku-Gate rot.
  **Verschärfung (S144-Retro-M2):** Der Koordinator darf in Briefen niemals „DONE setzen,
  Datei nicht löschen" anweisen — genau das produzierte in S144 ein Review-NO-GO.
  Erkenntnisse VOR dem DONE in die dauerhaften Artefakte überführen, dann DONE + löschen.
- **Marker-Wechsel sofort (S170-Retro-M2, geschärft S171-M1):** Wertet der Koordinator eine
  kommentierte NEEDS-DECISION- oder AWAITING-VERIFICATION-Datei aus, setzt er den Marker im
  **selben Zug** — aber nur zu `ANSWERED`/`DONE`, wenn die Datei im selben Abschluss gelöscht
  wird. Bleibt ein Teilpunkt offen, setzt er `AWAITING-VERIFICATION` mit Auswertungsnotiz in
  Zeile 1 (kein voreiliges ANSWERED/DONE). Grund: S170 — Review-NO-GO wegen stale
  `NEEDS-DECISION`-Marker; S171 — ANSWERED bei Teil-Auswertung (Punkt d unverifiziert)
  verletzte den Hygiene-Wächter → Vollsuite rot.
- **PLANNING-Datei-Lifecycle (S171-Retro-M2):** `S<N>_PLANNING.md`-Dateien werden nach
  Umsetzung + Review im **selben Abschluss** gelöscht — nicht bis zur Folgesession liegen
  lassen. Grund: der Plan ist ein Arbeitsgerüst (Koordinator + Stakeholder + Executors);
  finale Entscheide und Sessionstand gehören in `briefing.md`/`backlog.md`. Stale
  Planning-Dateien erzeugen Unklarheit und Duplikate.
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
- **Session-Limit-Abbrüche (S137):** Bricht ein Subagent wegen Session-/Kontextlimit ab, wird
  er NICHT neu gestartet — der Koordinator weckt ihn per `SendMessage` mit intaktem Kontext.
  Das Freigabe-Gate re-armt dabei nur, wenn die Freigabe in der laufenden Session bereits
  dokumentiert erteilt wurde (Marker-Kontinuität, `operating_model.md` Event 2).

---

**Kanal-Pflicht:** Stakeholder-Entscheidungen gehen **ausschließlich** über die Mailbox
`docs/handoff/` (Marker `NEEDS-DECISION`) — nie direkt im Chat. Der Koordinator leitet weiter.
