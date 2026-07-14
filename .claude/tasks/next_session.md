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

## Aktueller Stand (nach S146, 2026-07-14)

S146: (1) **Welle 1 umgesetzt:** 1a on_target-Anker Option A (`_common.py`: reaktive GOs an
der Ziel-Kachel) + zwei Folgefixes nach Stakeholder-Live-Verifikation: Wound-Anker zeigt
keine on_target-Karten mehr (Ziel-Kachel = einziger Ort), neue Stärke-Modifikator-Namens-
Chips am S-vs-T-Vergleich (`stratagem_strength_labels` in `stratagemEngine.py` +
`diceHtml.py`; Grenze dokumentiert: `buff_stat_bonus`-Fraktions-Buffs ohne Namens-Chip).
1b: 5 Vigilus-Warlord-Traits entfernt (referenzfrei belegt). Alles manuell verifiziert.
(2) **Ziel 7 Stufe B ABGESCHLOSSEN:** alle 7 Prüfschritte bestanden (`ziel7.md` Z. 76 ✅);
3 Verifikations-Befunde + 2 Badge-Bugs + Review-B1 nach `backlog.md` §2 überführt.
(3) **Nihilakh geklärt:** K1 schließt Nihilakh EIN — YAML-Eintrag ist 8E-Altbestand
(`S146_planning.md` Entscheid 3). (4) Review: **GO mit Auflage B1**. Vollsuite 1825 passed,
Coverage 99,12 %, mypy-Baseline 24, Architektur-/Doku-Gate grün.

Frühere Sessions (S60–S145): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S147)

Reihenfolge/Priorität nur noch in `docs/goals/backlog.md` §Prioritätenliste — hier nur der
unmittelbar nächste Schritt:

1. **B1-Design-Entscheid an den Session-Anfang** (Review-Auflage, backlog §2): Deklarations-
   Anker auf `effect_stat="wound"` filtern ODER Hit-/Save-Anker analog Wound abschaffen —
   danach Umsetzung inkl. Negativ-Tests (B2).
2. **Welle 2 (S146 freigegeben, nur am Headroom-Gate gescheitert):** Klan/Dynastie Brief K1
   inkl. Nihilakh (Rang 6) ∥ FixD Brief 1 (Rang 4, `docs/audit/plans/S142_fixD_resolution_tabs.md`).
3. Dahinter: **MWBD-Instanz-Fix** (Effort S) + **GO-Effekt-Badge-Lücke** (4 GOs) — beide
   `backlog.md` §2, Stakeholder-priorisiert für S147.

**Manuelle UI-Verifikation (offen):**

- 🔲 Spend-Guard (tisch-aufgelöstes Stratagem ohne Einheit) — erst im Roster-Builder prüfbar.
- 🔲 B12b-Punkte (3) weiter offen.

**Offene Handoff-Marker:** `S146_planning.md` → ANSWERED (in S147 nach Überführung löschen);
`S141_ui_befunde_group_a.md` bleibt bis FixC+FixD; gelöscht S146 (Lifecycle erfüllt):
`S145_planning.md`/`S145_stufeB_verifikation.md`/`S143_on_target_anker_konzept.md`/
`S146_review.md` (Befunde in `backlog.md` §2 + Erkenntnisse überführt).

**Erkenntnisse S146:** (a) Session-Limit-Abbruch eines Executors → SendMessage-Resume
funktionierte nahtlos (S137-Regel bewährt). (b) Selbst-Stopp-Budget wurde im Resume
überzogen (Auflage 60k, real ~177k) — Klausel „Budget gilt auch nach Resume" für
`agent_scopes.md` vorgeschlagen, **Stakeholder-Freigabe offen** (Retro-M4). (c) Review-Nit
B4 (zwei lange Warum-Kommentare `_common.py`) offen. (d) Parallel-Executoren brauchen
getrennte `COVERAGE_FILE` (S144, erneut bewährt).

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
