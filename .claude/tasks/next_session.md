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
- **Brief-Pflichten NEU (S149-Retro M6/M7, `operating_model.md`):** Planner belegt Schema-/
  Vorbild-Behauptungen per grep/Quellzeile; Executor zählt bei UI-Bugfixes VOR dem Fix alle
  Render-Pfade des Elements per grep auf.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `dev` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S149, 2026-07-15)

S149 (Details in `session_archive.md`): used-on-Fix umgesetzt, aber UI-Verifikation
FEHLGESCHLAGEN → REOPEN (Schritt 1); GAUSS/TESLA-`conditions` + 4 Tests ✓ bestätigt;
Brief 5 geschlossen (Keyword kommt von der Waffe via `grantsKeyword`, normale Badge genügt);
B8 entfernt ✓ bestätigt, B7 → Split B7a/B7b; Handoff bereinigt (4 Dateien + B8-Screenshot
gelöscht); Boss-Nob-Kombi-Swap-Lücke gefunden. Review GO-mit-Auflagen (alle umgesetzt),
Retro M6/M7 verankert, M5 nicht freigegeben. Vollsuite **1856 passed / 99,14 %**, mypy 24.
Abschluss-Executor brach am Session-Limit in M8 ab — Rest vom Koordinator abgeschlossen,
Backlog-Archiv (M8) → Schritt 2.

Frühere Sessions (S60–S149): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S150)

1. **used-on-Bug REOPEN (Top-Priorität):** Fix traf nur die zentrale Liste; Review-Hypothese:
   weiterer Render-Pfad (Inline-Anker) zeigt weiter die Sidebar-Auswahl. ZUERST Repro beim
   Stakeholder erfragen (welche Phase/Liste, welcher GO), dann ALLE Render-Pfade des Badges
   per grep aufzählen (M7-Pflicht) und fixen. Stand: `backlog.md` §2 + B12b.
2. **M8 Backlog verschlanken (Stakeholder-Auftrag S149, wörtlich: „Alles was fertig ist, kann
   ins Archiv"):** `docs/goals/backlog_archive.md` anlegen (Kopf: KEIN zweiter Backlog, nur
   Erledigtes/Verworfenes mit Session), alle ~58 Erledigt-Marker aus `backlog.md`
   dorthin verschieben, Verweis am Backlog-Kopf; keinen offenen Eintrag verlieren.
3. **7b Boss Nob:** zweite Swap-Gruppe `kombi_rokkit`/`kombi_skorcha` als EIGENE ODER-Gruppe
   (1 Waffe ersetzt Slugga+Choppa) in `orks/units.yaml`; vorher Existenz in `weapons.yaml` prüfen.
4. **Quantum Shielding (Aufgabe 4):** neuer Effect-Typ „unmod. Wound 1–3 misslingt immer" +
   Engine-Gate im Wound-Resolve + `diceCompose.always_fail_marker_row_html` als Producer
   verdrahten; danach Snakebites-Folge-Task (gleicher Effect-Typ + S8+-Ausnahme, Backlog).
5. **K1 gekürzt (Aufgabe 5):** nur Nihilakh + Mephrit; Nihilakh-Entscheid (S145) kanonisch
   nach `ziel7.md` Stufe C, danach `S144_klan_dynastie_konzept.md` DONE+löschen;
   Novokh/Sautekh/Nephrekh explizit → K2+ (Backlog nachziehen).
6. **FixD Brief 1** (`_common.py`, Spez. war `S142_fixD_resolution_tabs.md` §4); dann **B7a/B7b**;
   dann **GO-Ausgrauen-Konsistenz** (neuer Backlog-Eintrag S149).

**Manuelle UI-Verifikation (offen):**

- 🔲 Spend-Guard (tisch-aufgelöstes Stratagem ohne Einheit) — erst im Roster-Builder prüfbar.
- 🔲 B12b-Rest (Movement-Advance-Reroll-Randfall — spec-konform, kein Bug).

**Offene Handoff-Marker:** `S147_go_audit_ork_abilities.md` + `S147_go_audit_stratagems.md`
(ANSWERED — Ork-Restpunkte prüfen, auto_wound-Lücke ist in Backlog überführt; bei nächster
Konsumierung DONE+löschen); `S141_ui_befunde_group_a.md` bis FixC+FixD;
`S144_klan_dynastie_konzept.md` bis K1.

**Erkenntnisse S149:** (a) Zwei falsche Planner-Prämissen (`has_keywords`-Schema,
`wargear_keywords`-Vorbild) → M6-Pflicht. (b) Executor-Fehlbuchung „✅ ERLEDIGT" trotz
ausstehender UI-Verifikation (S116–S118-Muster; M5 nicht freigegeben — Muster beobachten).
(c) STOP-Regeln griffen 2× korrekt (Test-Schutz Aufgabe 1, Scope B7). (d) Screenshots künftig
mit Dateinamen in Befund-Dateien verankern (Triage-Nit).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; ab ~100k nichts Neues bei ausstehendem Review; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
