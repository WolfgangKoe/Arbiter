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
- **Brief-Session-Nummer (S150-Retro M3):** Jeder Executor-/Planner-Brief nennt die aktuelle
  Session-Nummer; Statusvermerke nutzen genau diese (Anlass: Fehlbuchung „ERLEDIGT (S145)"
  in S150) → `agent_scopes.md`.
- **UI-Bug-Recherche vollständig (S150-Retro M4):** Recherche-Briefs zu UI-Bugs zählen ALLE
  Datenfelder des gerenderten Elements auf, nicht nur den vermuteten State (Anlass:
  `target_name` übersehen) → `agent_scopes.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `dev` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S150, 2026-07-16)

S150 (Details in `session_archive.md`): M8-Backlog-Archiv angelegt (`backlog_archive.md`,
21 Einträge; kein offener 🔲-Eintrag verloren, 53→53 vor legitimem Kategorie-6-Neuzugang);
K1 kanonisiert nach `ziel7.md` §K1, `S144_klan_dynastie_konzept.md` gelöscht (**Daten-Fix
OFFEN → Rang 6**); FixD Brief 1 erledigt (`compute_resolution_context` + Attacker-/
Defender-Block-Split, 8 Tests, kein Layout-Change); used-on-Fix: `used`-Zustand las
`target_name` live aus der Sidebar statt aus dem gespeicherten Anker — gefixt +
Regressionstest; **beide manuellen UI-Verifikationen (used-on-Badge, FixD-Pixelidentität)
vom Stakeholder BESTÄTIGT**. Backlog Rang 11 neu (Restrukturierung). Review
GO-mit-Auflagen — alle 4 Auflagen umgesetzt (S150). Vollsuite **1865 passed / 99,14 %**,
mypy 24.

Frühere Sessions (S60–S150): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S151) — Stakeholder-Priorisierung S150

1. **Backlog-Restrukturierung VORGEZOGEN (Top-Priorität, Rang 11):** Planner-Brief mit
   Stakeholder-Anforderungen: (a) schlanke Index-Liste, Details in separate Datei(en);
   (b) Rangliste bekommt **Status-Spalte** (ToDo / In Progress / Review / UI-Verifikation /
   Done, …); (c) Abhängigkeiten klarer darstellen — „Parallel?"-Spalte erfüllt die Funktion,
   aber die Zeichen sind kaum hilfreich; (d) §4c mit archivieren. Strukturvorschlag →
   Stakeholder-Freigabe → Umsetzung.
2. **NEUE Routine-Regel (Stakeholder S150):** Backlog-Bereinigung an jedem Session-Ende
   oder -Start (Done-Items → `backlog_archive.md`) — in den Regeln-Block aufnehmen.
3. **Klärung in S151 (Stakeholder S150):** Funktion von `next_session.md` bestimmen — ggf.
   umbenennen oder als Zwischenspeicher fürs Kontextfenster-Limit nutzen; UND festlegen,
   welche Dateien/Regeln je Session-Aufgabe in den Kontext geladen werden müssen.
4. **used-on-Generalkonzept-Planner:** Suffix auf alle reaktiven GOs ausweiten (Feature-
   Wunsch S148, `backlog.md` §2 🟢); Notizen: `docs/handoff/S150_usedon_renderpaths.md`
   (bleibt ANSWERED bis Konsumierung → dann DONE+löschen).
5. **K1-Daten-Fix** (Nihilakh/Mephrit-Wortlaute, Rang 6); **Boss Nob 7b** (Kombi-
   Waffenprofile fehlen in `orks/weapons.yaml` — zweigeteilt: erst Profile, dann
   ODER-Gruppe); **Quantum-Shielding-Zuschnitt** (Mini-Konzept, dann Briefs ≤ M).

**Manuelle UI-Verifikation (offen):**

- 🔲 Spend-Guard (tisch-aufgelöstes Stratagem ohne Einheit) — erst im Roster-Builder prüfbar.
- 🔲 B12b-Rest (Movement-Advance-Reroll-Randfall — spec-konform, kein Bug).

**Offene Handoff-Marker:** `S147_go_audit_ork_abilities.md` + `S147_go_audit_stratagems.md`
(ANSWERED — behalten bis Fixing-Plan; bei Konsumierung DONE+löschen);
`S141_ui_befunde_group_a.md` (ANSWERED — behalten bis FixC + FixD Brief 2+3);
`S150_usedon_renderpaths.md` (ANSWERED, NEU — behalten bis used-on-Generalkonzept S151).

**Erkenntnisse S150:** (a) Haiku-Recherche zu UI-Bugs war unvollständig (`target_name`
übersehen) → M4-Regel. (b) Executor-Fehlbuchung „ERLEDIGT (S145)" in S150 → M3-Regel
(Brief nennt Session-Nummer). (c) Reviewer-Session-Limit per SendMessage-Resume
überbrückt — S137-Regel bewährt.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; ab ~100k nichts Neues bei ausstehendem Review; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
