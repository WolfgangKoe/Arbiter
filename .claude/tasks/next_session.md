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

## Aktueller Stand (nach S147, 2026-07-15)

S147: (1) **GO-Audit abgeschlossen** — 3 Kataloge `docs/handoff/S147_go_audit_*.md` mit
Fixing-Plänen ≤ M + snake_case-Inventaren (Kernbefunde: 5 CP-Fresser-Stratagems ohne
`modifier:`-Block, Apply-Button-Bug ~15 Necron-Abilities, 7 `activated`-Abilities ohne
Renderer, Speedwaaagh ohne Engine-Konsument, Fire Overwatch ohne Waffentyp-/Range-Check).
(2) **Entscheide** (`S147_planning.md`): `grantsKeyword` (camelCase) als Waffen-Keyword-
Konvention inkl. unitCard-Anzeige; camelCase-Migration als Inventar+Plan; B1 = Ziel-Kachel
einziger Ort. (3) **Code:** MWBD-Instanz-Fix (`_buff_ability_state_key`) + B1-Umsetzung
(Hit-/Save-Anker entfernt, Negativ-Tests B2, `design_system.md` §6.2/6.3) + Roster
`necrons_b1_verification.yaml` (Flayed Ones, Annihilation Barge, 2× Overlord). (4) Handoff
bereinigt (S145 migriert+gelöscht, S146 gelöscht, Retro-M4 in `agent_scopes.md`).
(5) Review: **GO mit Auflagen** (A-1 manuelle UI-Verifikation offen, B-1 behoben).
Vollsuite 1831 passed, Coverage 99,12 %, mypy 24, Architektur-/Doku-Gate grün.

Frühere Sessions (S60–S146): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S148)

Reihenfolge/Priorität nur noch in `docs/goals/backlog.md` §Prioritätenliste — hier nur der
unmittelbar nächste Schritt:

1. **Audit-Fixing-Pläne umsetzen** (3 Kataloge in `docs/handoff/`, Häppchen ≤ M; prioritär:
   Apply-Button-Bug, CP-Fresser-Stratagems, `grantsKeyword`-Konvention + unitCard-Anzeige,
   Fire-Overwatch-Bedingungen) + **camelCase-Migrationstask** (Inventare in den Katalogen).
2. **Welle 2 (S147 freigegeben, am Review-Budget-Gate auf S148 verschoben):** Klan/Dynastie
   Brief K1 inkl. Nihilakh ∥ FixD Brief 1 (`docs/audit/plans/S142_fixD_resolution_tabs.md`;
   FixD erst NACH ggf. weiterer `_common.py`-Arbeit koordinieren).

**Manuelle UI-Verifikation (offen):**

- 🔲 **S147 B1 + MWBD** (backlog §3, Roster `necrons_b1_verification.yaml`) — Stakeholder
  nach S147-Retro angekündigt.
- 🔲 Spend-Guard (tisch-aufgelöstes Stratagem ohne Einheit) — erst im Roster-Builder prüfbar.
- 🔲 B12b-Punkte (3) weiter offen.

**Offene Handoff-Marker:** `S147_planning.md` + 3 `S147_go_audit_*.md` = ANSWERED, behalten
bis S148-Umsetzung; `S147_review.md` nach Überführung gelöscht (S147);
`S141_ui_befunde_group_a.md` bleibt bis FixC+FixD; `S144_klan_dynastie_konzept.md` bleibt bis K2.

**Erkenntnisse S147:** (a) Befund-Kataloge, die liegen bleiben = ANSWERED — DONE nur bei
Löschung im selben Schritt (Hygiene-Gate fing falsches DONE-Briefing des Koordinators; die
generelle Marker-Regel-Präzisierung in `agent_scopes.md` wurde als Retro-M2 NICHT freigegeben,
ebenso Rückgabe-Deckel M3). (b) Review-B-2: `effect_stat`-kwarg nach B1 ohne Aufrufer —
generische Infrastruktur, kein Handlungszwang. (c) Haiku für Roster-/Datenarbeit bewährt
(2 Aufträge, 68k). (d) Review-Nit B4 (zwei lange Warum-Kommentare `_common.py`) weiter offen.

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
