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

## Aktueller Stand (nach S145, 2026-07-14)

S145: Planungs-/Konsolidierungs-Session (kein Code). (1) **Branches konsolidiert:** nur noch
`dev` + `main`, `dev` gepusht (`942e1ba`). (2) **Alle 6 Klan-/Dynastie-Fragen aus
`S144_klan_dynastie_konzept.md` entschieden** (`S145_planning.md`, Stakeholder-Entscheide
2026-07-14): Frage 1 (Nihilakh) faktisch geklärt gegen `faction_overview.txt`; Frage 2
(Reihenfolge Daten vs. Engine) zweistufig K1→K2 entschieden; **Frage 3: Option B**
(`ability_type: subfaction_passive`, neuer Typ statt `triggered`-Reparatur) — K2-Scope zusätzlich
erweitert um YAML-Aufräumen (totes `source`-Feld u. ä., per grep im K2-Brief zu verifizieren),
UI-Sichtbarkeit der passiven Effekte (Nephrekh 6+-Invuln, Nihilakh AP-1→0 als Badge/Hinweis),
Doppel-Direktiven-Klausel muss für alle 6 Dynastien-Protokolle funktionieren; **Option C**
(abilityEngine als Paket aufdröseln) **zurückgestellt** mit Schwellwert (~800 Zeilen
`abilityEngine.py` oder DRY-Schuld-Angang `backlog.md §4`) — K2-Neucode kommt von Anfang an in
ein eigenes Modul `gameMechanic/subfactionPassives.py`; NEU als paralleles Planungspaket
aufgenommen: „abilityEngine-Refactor-Vorplanung" (analog FixD-Vorplanung, nur Planung/Handoff,
kein Code, jederzeit parallel startbar). Frage 4 (Klasse-C-Fälle) nach Bestandsmuster gelöst,
Frage 5 (Spec-Nachzug) wird Pflichtteil von K2. (3) **Prioritäten konsolidiert:** vier
driftende Prio-Quellen zusammengeführt — kanonischer Ort der Gesamt-Reihenfolge ist jetzt
**`docs/goals/backlog.md` §Prioritätenliste** (10 Ränge + Refactor-Vorplanung parallel);
`docs/audit/plans/README.md` führt nur noch Status je Plan; stale Tag `[PRIO-NÄCHSTE]` bei
Backlog-Eintrag #2b entfernt (Text blieb, Rang 10).

Frühere Sessions (S60–S144): `docs/metrics/session_archive.md`.

### ▶ Nächster Schritt (S146)

Reihenfolge/Priorität nur noch in `docs/goals/backlog.md` §Prioritätenliste — hier nur der
unmittelbar nächste Schritt:

1. **Vigilus-Warlord-Traits entfernen** (Rang 3) ∥ **on_target-Anker Option A** (Rang 2,
   `S143_on_target_anker_konzept.md`) — dateidisjunkt, parallelisierbar.
2. Danach: **Klan/Dynastie Brief K1** (Wortlaut-Fixes, Rang 6) ∥ **FixD Brief 1** (Rang 4,
   `docs/audit/plans/S142_fixD_resolution_tabs.md`).
3. **Stufe-B-Verifikation** (Rang 8) läuft stakeholderseitig laufend, Anleitung in
   `docs/handoff/S145_stufeB_verifikation.md`.

**Manuelle UI-Verifikation (offen):**

- 🔲 Ziel 7 Stufe B: Necron-Roster-Verifikation (`ziel7.md:76`) — s. Punkt 3 oben.
- 🔲 Spend-Guard (tisch-aufgelöstes Stratagem ohne Einheit) — erst im Roster-Builder prüfbar.
- 🔲 B12b-Punkte (3) weiter offen.

**Offene Handoff-Marker:** `S144_klan_dynastie_konzept.md` → ANSWERED (S145-Entscheid, s.o.);
`S145_planning.md` → ANSWERED; `S141_ui_befunde_group_a.md` bleibt bis FixC+FixD;
`S144_planning.md`/`S144_review.md`/`S144_review_s143.md` gelöscht (S145, Lifecycle erfüllt).

**Erkenntnisse S144 (unverändert gültig):** (a) Retro-M1 Bestandsaufnahme-Pflicht + M2
DONE-sofort-löschen in `agent_scopes.md` verankert. (b) rotate_history-Marker-Drift behoben
durch Angleichung der Überschrift hier auf Singular („Nächster Schritt") — Tool läuft wieder.
(c) Parallel-Executoren brauchen getrennte `COVERAGE_FILE` — kollisionsfrei getestet
(4 Agenten gleichzeitig).

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
