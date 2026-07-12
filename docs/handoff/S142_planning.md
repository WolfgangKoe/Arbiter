STATUS: ANSWERED — Plan freigegeben (S142), Amendments A+B eingearbeitet.

# S142 — Planning, Revision 3 (freigegeben)

Revision 2 arbeitete die drei Stakeholder-Entscheidungen ein (Antworten unten). Revision 3:
Der Stakeholder hat den Plan (Aufgaben 1–10) **freigegeben**, mit zwei Ergänzungen per
direktem Auftrag:

- **Amendment A — Modulname:** Das neue Modul aus Aufgabe 1 heißt **`stratagemEngine.py`**.
  Transparenz-Vermerk: Der Stakeholder-Wortlaut war „strategemEngine.py"; der Koordinator hat
  die Schreibweise konsistent zu `gameObjects/stratagem.py` und dem Spielbegriff „Stratagem"
  auf `stratagemEngine.py` korrigiert.
- **Amendment B — neue Aufgabe 0 (direkter Stakeholder-Auftrag = freigegeben, läuft bereits):**
  Dateinamens-Konsistenz in `src/` — 13 snake_case-Dateien per `git mv` nach camelCase
  (Details in der Plan-Tabelle). Läuft VOR der Code-Welle (Aufgaben 1–3); die Modulnamen in
  den Aufgaben 1–2, 5, 8, 9 sind auf die neuen camelCase-Namen angepasst.

## Ausgangslage

Branch bleibt `feature/016-protocol-rp-effects` (Arbeitsbranch, `main` nur per PR). S141 hat
die mypy-Baseline auf 28 gesenkt, ein neues Ork-Transport-Roster ergänzt (Gunwagon/Evil Sunz)
und zwei UI-Verifikations-Bugs live gefixt (Emergency-Disembark-Sichtbarkeit `f36f1e7`,
Movement-Timing/Abdunkeln `7fc8b16`). Zwei weitere diagnostizierte Bugs (FixC Insane-Bravery-
Zielbindung, FixD Cross-Player-Area-Leak) wurden auf S142 vertagt — Root-Cause-Analysen fertig
in `docs/handoff/S141_ui_befunde_group_a.md`/`_group_b.md`. Das strategische Thema
(GO/Stratagem-Architektur) ist mit Revision 2 entschieden (s. u.).

## Entschiedene Konsens-Fragen (Stakeholder, S142)

1. **Architektur — Option B gewählt:** eigener, aber **konsolidierter** Stratagem-Dispatch
   (neues Modul — Name per Amendment A: `gameObjects/stratagemEngine.py`), KEINE Eingliederung in die
   Ability-Engine-Getter. Zusätzlich neuer Auftrag: **Read-only-Recherche**, ob
   `ability_engine.py` (563 Zeilen, ~30 repetitive Getter) refactored und aufgegliedert werden
   kann — Design-Vorschlag als Handoff-Datei, **keine Code-Änderung in S142** (→ Aufgabe 5).
2. **FixD — struktureller Umbau gewählt** (Resolution-Tabs in die Spieler-Spalten,
   Wurzelbehandlung statt Kennzeichnung). Der Folge-Plan wird **bereits in S142 beauftragt**
   (Detail-Plan als Datei, → Aufgabe 4); Umsetzung erst nach Plan-Freigabe, vermutlich
   Folgesession. Die `target_name`-Sofortlinderung bleibt im S142-Plan (→ Aufgabe 3).
3. **Insassen-Feature — stark runterpriorisiert:** KEINE Design-Entscheidungen jetzt.
   Erkenntnisse aus `S141_ui_befunde_group_b.md` §3–§5 (inkl. der zwei offenen Design-Fragen)
   werden als **niedrig priorisierter Backlog-Eintrag** überführt (→ Aufgabe 6).
   Stakeholder-Begründung (mit in den Eintrag aufnehmen): Transporter sind aktuell Randfälle,
   der Fokus liegt auf den Gefechtsoptionen.

## Befunde (unverändert aus Revision 1)

**Checkbox-Sync (`docs/goals/ziel7.md` gegen `git log --oneline -30`):** Alle gesetzten Haken
referenzieren Commits aus S113–S130 (`f9279fe`, `8c124c3`, `396fdec`, `e031616` u. a.) —
außerhalb des 30-Commit-Fensters (S132–S141). Sie wurden in Zwischen-Sessions (S117, S123,
S130) bereits gegengeprüft — **kein neuer Stale-Fund**; die Verifikation stützt sich auf die
dokumentierte Historie (`session_archive.md`). Alle **offenen** Punkte (Stufe B
UI-Verifikation, Stufe C komplett) sind tatsächlich offen — kein Code dazu im Log.

**Doku-Hygiene-Fund:** `docs/handoff/Stakeholder_Beobachtungen.md` führt unter „Eingang" noch
„Cut them down erstreckt sich auf beiden Spielerflächen" — bereits in Commit `0a747b1` (S139)
gefixt („Fix pre-existing Cut Them Down layout bug … now placed per column via the faction
marker"), nie nach „Zuletzt überführt" verschoben. Reine Doku-Drift (→ Aufgabe 7).

**Offene Handoff-Marker (`docs/handoff/`, kein `DONE`):**

- `S141_review.md` — ANSWERED (DoD-Review, informativ).
- `S141_ui_befunde_group_a.md` — ANSWERED; enthält die Root-Cause-Analysen zu FixC (Befund 5)
  und FixD (Befund 3) — beide in diesem Plan adressiert.
- `S141_ui_befunde_group_b.md` — ANSWERED; Teil A erledigt, Teil B geht per Aufgabe 6 ins
  Backlog (danach kann die Datei auf DONE und gemäß Lifecycle gelöscht werden).
- `Stakeholder_Beobachtungen.md` — STANDING, ein Eintrag stale (s. o.).

**Architektur-Ist-Stand GO/Stratagem (Kurzfassung, Grundlage der Option-B-Entscheidung):**
`ability.py` und `stratagem.py` teilen bereits dieselbe `Effect`-Dataclass. Die
Fraktionsfähigkeiten laufen über ~30 spezifische Getter in `ability_engine.py` (563 Zeilen,
stark repetitiv, je Effekt-Ausprägung eine Funktion); Stratagems über **drei verstreute
formbasierte Dispatcher**: `_apply_stratagem_effect()` (`uiLayout/_common.py`),
`stratagem_strength_bonus()` (`ability_engine.py`) und `_effect_gate_met()`
(`uiLayout/gameProtocoll.py:145-177` — kennt nur EINE Effekt-Form, Root Cause von FixC:
`auto_pass_morale` fällt durch). Option B bündelt diese drei an einem Ort mit vollständiger
Formentabelle und behebt FixC damit strukturell statt punktuell.

## Session-Plan (Revision 3, freigegeben)

| # | Aufgabe | Effort | Token-Schätzung (Subagent) | Modus | Tier | Scope-Zeile / Dateien |
|---|---------|--------|-----------------------------|-------|------|------------------------|
| 0 | **Dateinamens-Konsistenz `src/` (Amendment B, läuft bereits):** 13 snake_case-Dateien per `git mv` nach camelCase — `ability_engine`→`abilityEngine`, `attack_math`→`attackMath`, `chargephase`→`chargePhase`, `game_log`→`gameLog`, `game_state`→`gameState`, `phase_handler`→`phaseHandler`, `phase_runner`→`phaseRunner`, `unit_mutations`→`unitMutations`, `rosz_importer`→`roszImporter`, `round_choice_ability`→`roundChoiceAbility`, `dice_compose`→`diceCompose`, `dice_html`→`diceHtml`, `go_card`→`goCard` — inkl. Imports, `pyproject.toml`, Architektur-Wächter und lebender Doku. **Ausgenommen:** `_common.py` (Privat-Marker), `tests/test_*.py` (pytest-Konvention), `tools/` (Hook-/CLAUDE.md-Referenzen). Direkter Stakeholder-Auftrag = freigegeben; läuft VOR Aufgabe 1–3. | M | ~40k | freigegeben (direkter Auftrag) | **Sonnet** | `src/gameMechanic/`, `src/gameObjects/`, `src/uiLayout/`, `pyproject.toml`, `tests/architecture/`, betroffene Specs |
| 1 | **Stratagem-Dispatch konsolidieren (Option B, Brief A):** neues Modul `gameObjects/stratagemEngine.py` (Name per Amendment A); die drei Dispatcher (`_apply_stratagem_effect`, `_effect_gate_met`, `stratagem_strength_bonus`) dorthin umziehen — reiner Umzug, Verhalten unverändert, alle vorher-grünen Tests bleiben grün. INV-4b-Namenscheck laut Standardsatz (`agent_scopes.md`). | M | ~30-35k | Gate | **Sonnet** | `Stratagem-Effekt umsetzen`-Zeile: `src/gameObjects/stratagem.py`, `src/gameMechanic/abilityEngine.py`, `src/uiLayout/_common.py`, `src/uiLayout/gameProtocoll.py` |
| 2 | **FixC im konsolidierten Modul (Brief B):** Gate um `effect.type=="auto_pass_morale"` (generisch: jeden unit-scoped Effekttyp ohne eigene Bedingungs-Keywords) erweitern; `_use_callback` gegen `unit_key=None` härten (Klick verweigern statt CP+Verbrauch ohne Effekt); Regressionstest inkl. B12b-Suffix. Baut auf Aufgabe 1 auf (sequenziell nach Brief A). | S | ~15-20k | Gate | **Sonnet** | dieselbe Zeile + `src/uiLayout/gameProtocoll.py:249-262`, `_common.py::spend_stratagem` |
| 3 | **FixD-Sofortlinderung:** `target_name` in `render_reactive_stratagem_box` (`_common.py:876-889`) ergänzen — zeigt sofort, welchem Spieler/welcher Einheit das GO gehört, bis der strukturelle Umbau (Aufgabe 4 → Folge-Plan) greift. | XS | ~8-10k | Gate | **Sonnet** | `Phase-UI anpassen`-Zeile, `src/uiLayout/_common.py` |
| 4 | **FixD-Detail-Plan (struktureller Umbau) erstellen:** read-only Analyse von `fightPhase.py:558-573` + `shootingPhase.py:187` + Resolution-Tab-Struktur; Detail-Plan als Datei nach `docs/audit/plans/` (README-Queue im selben Schritt nachziehen). Der Plan MUSS die Umsetzung in Teil-Briefe ≤ M splitten (Gesamtaufwand vermutlich L, da Angreifer-/Verteidiger-Daten im Tab strukturell gemischt sind). Umsetzung NICHT in S142 — erst nach Plan-Freigabe. | S | ~15-20k | Gate (nur Plan-Datei) | **Sonnet** (Analyse + Plan, kein Lookup) | `fightPhase.py`, `shootingPhase.py`, `_common.py::render_attack_resolution`, `docs/spec/design_system.md` §6 |
| 5 | **abilityEngine.py-Refactor-Recherche (NEU, Stakeholder-Wunsch):** read-only prüfen, ob/wie die 563 Zeilen / ~30 repetitiven Getter aufgegliedert werden können (z. B. nach Effekt-Familien geschnittene Module oder generischer Effekt-Reader); Design-Vorschlag mit Trade-offs als Handoff-Datei (`STATUS: NEEDS-DECISION` als ERSTE Schreibaktion/Zeile 1), Grundannahmen-Block voranstellen. KEINE Code-Änderung in S142. Startet NACH Aufgabe 0–2, damit der Vorschlag die neuen Dateinamen und den Modul-Schnitt kennt. | S–M | ~20-25k | Gate (nur Handoff-Datei) | **Sonnet** — Begründung: Design-Bewertung mit Trade-offs, kein format-fixer Lookup (Haiku ungeeignet); Opus unnötig, da read-only und Entscheidung beim Stakeholder | `abilityEngine.py`, Konsumenten via grep (`_common.py`, `diceHtml.py`, `armyCard.py`, `gameState.py`), `docs/spec/faction_abilities.md` |
| 6 | **Insassen-Feature ins Backlog überführen:** Erkenntnisse aus `S141_ui_befunde_group_b.md` §3–§5 (Gap-Analyse, 4 Bausteine, 2 offene Design-Fragen) als niedrig priorisierten Eintrag nach `docs/goals/backlog.md` §2, inkl. Stakeholder-Begründung (Transporter = Randfall, Fokus Gefechtsoptionen); danach Marker der Handoff-Datei auf DONE setzen. | XS | ~5k | Gate | **Haiku** — Begründung: Quelle und Zielformat liegen fest, reine format-fixe Überführung ohne Bewertungsspielraum | `Doku / Backlog pflegen`-Zeile, `docs/goals/backlog.md`, `docs/handoff/S141_ui_befunde_group_b.md` |
| 7 | **Doku-Hygiene:** stale „Cut them down"-Eintrag in `Stakeholder_Beobachtungen.md` nach „Zuletzt überführt" verschieben (Beleg: Commit `0a747b1`). Mit Aufgabe 6 in EINEM Haiku-Brief bündelbar. | XS | ~3k (in Aufgabe 6 bündelbar) | Gate | **Haiku** | `docs/handoff/Stakeholder_Beobachtungen.md` |
| 8 | **mypy-Ratchet gameMechanic-Rest** (11 Fehler: `abilityEngine.py`/`attackMath.py` `type-arg`, `moralePhase.py`/`unitMutations.py` `no-any-return`/`arg-type`); Baseline in `tools/mypy_gate.py` im selben Schritt senken (Ratchet-Regel). Vor Aufgabe 5 nice-to-have (sauberere Recherche-Grundlage), nicht blockierend. | S | ~15-20k | Gate | **Sonnet** | `backlog.md` §4 mypy-Absatz |
| 9 | **mypy-Ratchet uiLayout-Paket** (17 Fehler: `armyCard.py`/`gameProtocoll.py`/`unitCard.py`/`armyList.py`/`detachmentCard.py`); Render-Code → manuell zu prüfende Punkte explizit benennen. | M | ~30-35k | Gate | **Sonnet** | dieselbe Backlog-Zeile |
| 10 | **Roster-Loader-Test-Lücke:** `test_loader.py:1259` auf Verzeichnis-Glob über `data/rosters/*.yaml` umstellen, damit neue Roster (z. B. `orks_transport.yaml`) automatisch mitgeprüft werden. | S | ~10-15k | Gate | **Sonnet** | `Loader / YAML-Schema ändern`-Zeile, `tests/gameObjects/test_loader.py` |

**Nicht eingeplant / Stakeholder-Aufgabe:**

- Manuelle UI-Verifikation B12b (3 Punkte) + Klan-Affinität am Ork-Transport-Roster
  (`backlog.md` §3) — durch den Stakeholder, idealerweise NACH Aufgabe 2 (FixC ändert
  denselben Code-Pfad, den B12b mitprüft).
- FixD-**Umsetzung** und Insassen-Feature-**Umsetzung** — bewusst außerhalb S142
  (Folge-Plan bzw. Backlog, Stakeholder-Entscheid).

**Reihenfolge-Begründung:** **Aufgabe 0 (Rename-Welle, Amendment B) läuft ZUERST und bereits
jetzt** — sie berührt Dateinamen quer durch `src/` und muss abgeschlossen sein, bevor die
Code-Welle (Aufgaben 1–3) startet, sonst kollidieren Briefe mit umbenannten Modulen. Danach
Option-B-Umsetzung (Aufgaben 1→2 sequenziell, Brief B setzt auf dem neuen
`stratagemEngine.py` auf). Aufgaben 3, 4 und 6+7 sind davon unabhängig und können parallel
zu 1–2 laufen (Vollsuite gemäß Auftragsgrößen-Gate nur EINMAL zentral am Wellen-Ende;
Doku-Aufgaben 6+7 sind von Aufgabe 0 unberührt). Aufgabe 5 startet NACH 0–2, damit der
Design-Vorschlag die neuen Dateinamen und den konsolidierten Modul-Schnitt einbezieht. Die
Ratchet-/Test-Aufgaben 8–10 folgen zum Schluss und sind die ersten Wind-down-Kandidaten.

**Gesamt-Token-Schätzung + Korridor-Check (inkl. Aufgabe 0):**

- Subagenten gesamt (isolierte Kontexte, zählen NICHT gegen das Hauptfenster):
  ~190–225k über alle 11 Aufgaben (davon ~40k Aufgabe 0).
- Koordinator-Hauptfenster: Plan-Handling + 9–10 Briefe (dünner Koordinator, nur Pfade/
  Marker) + Review-Runden ≈ **95–120k** — passt in den Korridor <150k, aber ohne große
  Reserve; das Wind-down-Gate bei ~120k wird mit diesem Plan realistisch erreicht →
  Wind-down-Reihenfolge unten ist verbindlich einzuhalten.
- **Wind-down-Reihenfolge (was bei ~120k zuerst entfällt):**
  1. Aufgabe 10 (Roster-Test) → nächste Session,
  2. Aufgabe 9 (mypy uiLayout, größter Brocken) → nächste Session,
  3. Aufgabe 5 (abilityEngine-Recherche) → nächste Session (read-only, verliert nichts).
  Aufgabe 8 (kleines mypy-Paket) möglichst halten, damit der Zero-Error-Ratchet
  („Baseline sinkt jede Session") nicht erneut überfällig wird. Kern-Set Aufgaben 0–4 + 6/7
  (~115–135k Subagent, ~65-75k Koordinator) hat Vorrang.

## Offene Fragen an den Stakeholder

Keine — der Plan ist **freigegeben** (Aufgaben 1–10 per Freigabe, Aufgabe 0 per direktem
Stakeholder-Auftrag; Amendments A+B oben eingearbeitet).

## Selbstprüf-Checkliste

- [x] Jeder Haken der Zieldatei (`ziel7.md`) gegen `git log --oneline -30` verifiziert — kein
      Stale-Fund im prüfbaren Bereich (Details unter Befunde); alle offenen Haken tatsächlich offen.
- [x] Keine Aufgabe > Effort M — „Modul konsolidieren + FixC" in zwei Briefe gesplittet
      (Aufgabe 1 M, Aufgabe 2 S); Aufgabe 0 (Rename) ist M; die FixD-Umsetzung (vermutlich L)
      ist als zu splittender Folge-Plan beauftragt, nicht als Einzelbrief.
- [x] Token-Schätzung pro Aufgabe genannt + Gesamt-Schätzung (inkl. Aufgabe 0) mit
      Korridor-Check und Wind-down-Reihenfolge.
- [x] Amendments A+B eingearbeitet: Modulname `stratagemEngine.py` (Schreibweise-Korrektur
      transparent vermerkt), Aufgabe 0 vor der Code-Welle, camelCase-Namen in den
      Aufgaben 1, 5, 8 nachgezogen (Aufgaben 2 und 9 referenzierten keine umbenannten Dateien).
- [x] Offene Handoff-Marker geprüft (3× ANSWERED mit Restaufträgen — alle im Plan adressiert;
      1× STANDING mit einem stale Eintrag → Aufgabe 7).
