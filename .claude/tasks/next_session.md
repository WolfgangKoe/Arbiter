# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start:** „start next session" → Planner-Subagent (`CLAUDE.md`+`docs/goals/ziel7.md`+`docs/goals/backlog.md`, Scope `docs/reference/agent_scopes.md`) legt Entwurf vor, Koordinator zeigt ihn, erst nach Freigabe los; „Plan ist freigegeben" = Shortcut direkt los. Einstieg `LEITSTAND.md`, Rollen/Tier `docs/governance/operating_model.md`.
- **ADR-0007:** Koordinator routet, liest keine Quelldateien/Vollergebnisse — Detail-Planung/Review laufen als Subagenten; Stakeholder-Entscheidungen async über Mailbox (`docs/handoff/`, NEEDS-DECISION→ANSWERED), nicht Chat.
- **Ende:** Review (Reviewer-SA) → Retro → Maßnahmen-Entscheid (Stakeholder) → Abschluss: diese Datei aktualisieren (ZUERST lesen) + ggf. Ziel-Checkboxen.
- **Doku-Gate:** Decke 120 Zeilen (Test rot darüber); beim Reißen tief auf ≤ 70 kürzen (Erledigtes → `backlog.md`/`session_archive.md`).
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten = stehende Freigabe (ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.
- **Review-Budget-Regel (S144 NEU):** ab ~100k Kontext keine neue Aufgabe mehr, solange Review/Retro der Session aussteht → `CLAUDE.md` (Anlass: S142+S143 Review-Nachholungen).
- **Auftragsgrößen-Gate (S130):** kein Executor-Brief > Effort M; Test-Budget (EINE Vollsuite zentral am Wellen-Ende, `run_in_background` für pytest VERBOTEN) + harter Selbst-Stopp in jedem Brief → `agent_scopes.md`.
- **DONE-Lifecycle verschärft (S144-Retro-M2):** nie „DONE setzen, Datei nicht löschen" anweisen — Erkenntnisse überführen, dann DONE + löschen im selben Schritt (S144-NO-GO-Anlass).
- **Bestandsaufnahme-Pflicht (S144-Retro-M1):** Recherche-/Planner-Briefs prüfen vor „X fehlt"-Aussagen den Ist-Bestand in `data/wh40k_9e/<fraktion>/` (alle YAMLs) UND `docs/work/` → `agent_scopes.md`.
- **Handoff-Marker-Pflicht (S131):** STATUS-Marker als ERSTE Schreibaktion, Format exakt `STATUS: <WERT>` als nackte erste Zeile — kein HTML-Kommentar (S140).
- **Planner-Schreibrecht (S140):** Planner als general-purpose-Subagent — legt Entwurf selbst nach `docs/handoff/` ab.
- **Grundannahmen-Block (S131):** Konzept-Dokumente starten mit bestätigungspflichtigen Grundannahmen (App würfelt NICHT — Tischwürfe!) → `agent_scopes.md`.
- **Executor-Klausel:** Dateiänderungen nur über Edit/Write, Bash nur lesend/git/pytest (S123); Selbstprüfliste enthält `python tools/mypy_gate.py` (S128).
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0 (Stand S144: **24** — 7 `gameMechanic/` + 17 `uiLayout/`, `backlog.md` §4; uiLayout NICHT parallel zu FixD).
- **Vollsuite-Timeout (S136):** Bash-`timeout: 600000` explizit setzen. Playwright = Standard für funktionale UI-Befunde.
- **Session-Limit-Abbrüche (S137):** Subagent nicht neu starten — per `SendMessage` resumen; Freigabe-Gate re-armt nur bei dokumentierter Chat-Freigabe.
- **markdownlint-Trial (S137–S139):** `.markdownlint.jsonc` + `npm run lint:md`; Stakeholder-Entscheid behalten/entfernen steht aus.
- **Koordinator-Pflicht (S148, Stakeholder-Entscheid F4):** Der Koordinator überwacht den
  Kontextstand aktiv und beendet die Session rechtzeitig (Wind-down-Schwellen); Verschiebungen
  meldet er mit Begründung.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S148, 2026-07-15)

S148 Welle 1 umgesetzt: **Brief 1** Apply-Button-Gate (`is_effect_executable`,
Handler-Dict `abilityEngine`); **Brief 2** modifier-Blöcke (Judgement of the Triarch,
Showin' Off, Unbridled Carnage); **Brief 3** Fire-Overwatch (`weapon_conditions: [RANGED]`,
generisches `weapon_conditions_met`, Engagement-Range-Gate in `_inactive_charge`, 9+1
Fixtures nachgezogen, R-CHARGE-08 Klasse C); **Brief 4** `grantsKeyword` generisch
(21+1 Fundstellen, `derived_keywords` + `unit.keywords`); **Brief 7** camelCase-
Migrationsplan (`loader_contract.md` §8, 107+3 Felder) + Reanimation-Entscheid im Backlog.
Welle 2 (Briefe 5+6, K1, FixD Brief 1) auf S149 verschoben (Review-Budget-Regel ~100k).
Manuelle UI-Verifikation durchgeführt: **B1 PASS**, **MWBD PASS**, **Advance-Reroll PASS**,
**Fire-Overwatch-Verhalten PASS** (inkl. `in_melee`-Ausblendung + Fernkampf-Bedingung);
6 Befunde dabei aufgedeckt (Flayed-Ones-Roster 1 Modell, Quantum-Shielding-Anzeige-Bug,
Roster-CORE-Inkonsistenz, „used on"-Bug in der zentralen Liste, Feature-Wunsch „used on"
für alle reaktiven GOs, `model_groups`-Union-Ungenauigkeit) — Details + Priorisierung s. u.
Zusätzlich: Code-Minifix (Overwatch-Hinweistext entfernt, Regeltext der GO-Karte übernimmt
das) + Roster-Fix (Flayed Ones auf 10 Modelle). Vollsuite lief vor Abschluss grün (1851
passed, 99,14 %); gezielte Nachläufe (`test_charge_phase.py`, `test_common.py`,
`tests/docs/`, `tests/acceptance/`) grün, mypy-Baseline unverändert bei 24.

Frühere Sessions (S60–S147): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S149)

Reihenfolge/Priorität nur noch in `docs/goals/backlog.md` §Prioritätenliste — hier nur der
unmittelbar nächste Schritt, priorisiert:

1. **BUG zentrale Stratagems-Liste „used on ⟨Einheit⟩"** (Stakeholder-verifiziert, Prüfblock 5
   Insane Bravery): Suffix zeigt die aktuell **gewählte** Einheit statt der Einheit, auf die die
   GO angewendet wurde. Vermutlich liest der Render-Code die Selektion statt dem gespeicherten
   `unit_key`. Fundort: `src/uiLayout/gameProtocoll.py`/`_common.py`. **VOR FixD koordinieren**
   (beide berühren `_common.py`).
2. **Briefe 5+6** (fertig spezifiziert im gelöschten S148-Plan, Kurzspezifikation hier
   gesichert): Brief 5 = `derived_keywords`-Badges in `armyCard.py` analog `wargear_keywords`-
   Anzeige (manuelle UI-Verifikation Pflicht). Brief 6 = `has_keywords: [GAUSS]` bei
   Disintegration Capacitors (`necrons/stratagems.yaml:249-263`) + `has_keywords: [TESLA]` bei
   Malevolent Arcing (`necrons/stratagems.yaml:265-275`) eintragen + Regressionstest.
3. **Quantum-Shielding-Anzeige Annihilation Barge:** unmod. Wound 1–3 misslingt immer — wird
   aktuell nicht als Debuff in der Wound-Zeile (3× ✕) noch als Buff im Save-Block angezeigt.
   Regeltext VORHER gegen `docs/work/wahapedia_necrons` verifizieren.
4. **K1** inkl. Pflicht, den bereits getroffenen Nihilakh-Entscheid aus
   `docs/handoff/S144_klan_dynastie_konzept.md` endlich kanonisch zu notieren (Stakeholder-Rüge
   F1: nicht erneut fragen).
5. **FixD Brief 1** (nach Punkt 1, gleiche Datei `_common.py`).
6. **Roster-/Daten-Konsistenz-Recherche** (Haiku-Task): CORE-Keyword-Abgleich `units.yaml` vs.
   `docs/work/wahapedia_necrons` (Annihilation Barge ist laut Stakeholder NICHT CORE, war aber
   als MWBD-Ziel wählbar; Flayed Ones mitprüfen) + Ork Boss Nob Waffen (wirklich nur Stikkbomb?).

**Manuelle UI-Verifikation (offen):**

- 🔲 Spend-Guard (tisch-aufgelöstes Stratagem ohne Einheit) — erst im Roster-Builder prüfbar.
- 🔲 B12b-Rest (Movement-Advance-Reroll-Randfall — spec-konform, kein Bug).

**Offene Handoff-Marker:** `S147_planning.md` + 3 `S147_go_audit_*.md` bleiben ANSWERED
(Briefe 5/6 offen); `S141_ui_befunde_group_a.md` bleibt bis FixC+FixD;
`S144_klan_dynastie_konzept.md` bleibt bis K1/K2; `S148_review.md` neu offen (Reviewer lief
parallel zu diesem Abschluss) — für S149 prüfen/überführen.

**Erkenntnisse S148:** (a) `grantsKeyword` generisch entschieden (F3, gilt auch für künftige
Ork-Fälle). (b) Reanimation-Konsistenz-Entscheid in `backlog.md` §2 notiert (F2 — Stratagem-
`reanimate` künftig wie Ability-Variante mitgezählt). (c) STOP-Regel griff bei Brief 3 (9
Fixtures wegen Fire-Overwatch-Bedingungsänderung nachgezogen, Option 1 gewählt). (d)
Session-Limit-Resume per `SendMessage` funktionierte (S137-Regel bestätigt). (e)
`model_groups`-Union-Ungenauigkeit wird von `grantsKeyword` geerbt (Backlog §4).

**Ratchet/Rest unverändert:** `on_declaration`-Befund (`chargePhase.py`/`fightPhase.py`);
Stil-Nit `undo_stratagem` in-place; R-PROTO-02; Rand-Design-Konzept; GO-Keyword-Nachpflege
(bis B13); 4c-Folge-Split; Fold-Heuristik; Totalvernichtungs-Spielende; Kleinschulden →
`backlog.md`. Custodes hat noch keine Stratagem-Daten (W1-F-Befund).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; ab ~100k nichts Neues bei ausstehendem Review; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
