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

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S144, 2026-07-12)

S144: (1) **Review+Retro S143 nachgeholt** (GO m. Auflagen); alle 4 Maßnahmen umgesetzt:
Klan-Affinität-Doku-Drift geschlossen (`ziel7.md`/`backlog.md`), Cap-DRY-Backlogschuld,
Worktree-Prune, **Review-Budget-Regel** in `CLAUDE.md`. (2) **Stratagem-Datenpflege:**
Necrons 56→40 (16 White-Dwarf: Cult of the Cryptek + Annihilation Legion), Orks 28→17
(**11** Vigilus statt geplanter 8 — Abgleichliste hatte sich verzählt, 3 Folge-Stratagems
wären sonst verwaist; Executor-Selbst-Stopp hat das gefangen). (3) **mypy 28→24:**
abilityEngine/stratagemEngine Option A+B, Helfer `_sum_effect_value` (6 Call-Sites,
`combine=min` für `ability_invuln_save` mit Seed-aus-erstem-Treffer), 8 Regressionstests;
Punkt-4-Befund als Backlog §4 „DRY Directive-Aktiv-Logik". (4) **Klan-/Dynastie-Konzept**
(`docs/handoff/S144_klan_dynastie_konzept.md`, NEEDS-DECISION): Prämisse „Rohtexte fehlen"
war falsch — `subfaction_abilities.yaml` existiert seit ~S100 samt Engine-Anbindung, ABER
5/13 Einträge inhaltlich falsch (Nihilakh/Sautekh/Mephrit/Nephrekh/Novokh/Snakebites) und
Engine macht alle 13 wirkungslos (kein Subfraktions-Filter, 4 tote Handler, kein UI-Konsument)
→ eher Bugfix+Engine-Lücke als neues Feature. (5) **S144-Review: GO nach Auflage**
(DONE-Handoffs sofort löschen); Vollsuite **1816 passed / 99,12 %**, Architektur-Gate 8/8,
mypy 24 == Baseline. Handoff bereinigt (S141/S142/S143-Altdateien + 2 Screenshots weg).
Aufgaben on_target-Anker + FixD Brief 1 per Review-Budget-Regel **nach S145 verschoben**.

Frühere Sessions (S60–S143): `docs/metrics/session_archive.md`.

### ▶ Nächster Schritt (S145, Reihenfolge)

1. **Klan-/Dynastie-Konzept entscheiden:** 6 Entscheidungsfragen + 7 Grundannahmen aus
   `S144_klan_dynastie_konzept.md` in den Planning-Entwurf aufnehmen (Stakeholder-Entscheid,
   danach Umsetzungsplan als eigene Briefs).
2. **on_target-Anker Option A** (`S143_on_target_anker_konzept.md`, freigegeben S143):
   `render_reactive_stratagem_box` in `render_group_assignment` (`_common.py:~2506`),
   Verschwinde-Regel bei Ziel-Toggle. Kollisionsfrei mit FixD.
3. **FixD Brief 1** (Plan freigegeben S144, `docs/audit/plans/S142_fixD_resolution_tabs.md`):
   Compute/Render-Trennung in `_common.py` — README-Status auf FREIGEGEBEN setzen.
4. **Vigilus-Warlord-Traits entfernen** (Entscheid S144): 5 Einträge in
   `data/wh40k_9e/orks/warlord_traits.yaml` (Keywords BLITZ BRIGADE, DREAD WAAAGH!,
   KULT OF SPEED, STOMPA MOB ×2), analog Stratagem-Muster inkl. grep-Absicherung.
5. **mypy-Ratchet uiLayout** (17 Fehler) — erst nach FixD Brief 1–3 (Datei-Überschneidung
   `_common.py`).

**Manuelle UI-Verifikation (offen):**
- 🔲 Ziel 7 Stufe B: Necron-Roster-Verifikation (`ziel7.md:76`).
- 🔲 Spend-Guard (tisch-aufgelöstes Stratagem ohne Einheit) — erst im Roster-Builder prüfbar.
- 🔲 B12b-Punkte (3) weiter offen.

**Offene Handoff-Marker:** `S144_klan_dynastie_konzept.md` NEEDS-DECISION;
`S141_ui_befunde_group_a.md` bleibt bis FixC+FixD; `S144_planning.md`/`S144_review*.md`
ANSWERED → nach S145-Start-Sichtung per Lifecycle löschen.

**Erkenntnisse S144:** (a) Retro-M1 Bestandsaufnahme-Pflicht + M2 DONE-sofort-löschen in
`agent_scopes.md` verankert. (b) rotate_history-Marker-Drift behoben durch Angleichung der
Überschrift hier auf Singular („Nächster Schritt") — Tool läuft wieder; Erkenntnis (d) aus
S143 damit erledigt. (c) Parallel-Executoren brauchen getrennte `COVERAGE_FILE` — hat in
S144 kollisionsfrei funktioniert (4 Agenten gleichzeitig).

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
