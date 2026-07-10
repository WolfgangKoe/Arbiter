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
- **Auftragsgrößen-Gate (S130):** kein Executor-Brief > Effort M; Test-Budget (EINE Vollsuite, im selben Tool-Call abwarten, `run_in_background` für pytest VERBOTEN) + Selbst-Stopp in jedem Brief → `agent_scopes.md`.
- **Handoff-Marker-Pflicht (S131):** jeder Brief, der nach `docs/handoff/` schreibt, nennt den STATUS-Marker für Zeile 1.
- **Grundannahmen-Block (S131):** Konzept-Dokumente starten mit bestätigungspflichtigen Grundannahmen (App würfelt NICHT — Tischwürfe!) → `agent_scopes.md`.
- **Executor-Klausel:** Dateiänderungen nur über Edit/Write, Bash nur lesend/git/pytest (S123); Selbstprüfliste enthält `python tools/mypy_gate.py` (S128).
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0 (S133: 75→63).

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S135, 2026-07-10)

S135 (nach Limit-Reset voll durchgeführt, Review **GO**): S134-Entscheidungen aufgelöst
(`S134_offene_punkte.md` ANSWERED: B2=Option C, B7=Mini-Header, B7/B9=EIN Konzept-Handoff,
B10 in CLAUDE.md). **Paket 4 KOMPLETT** (`d66755e`/`0aa7dc6`/`96e7997`): Hit-/Wound-/
Save-Anker + Damage/Psychic/Deny-Reroll-Ablösung (14 Tests planmäßig migriert;
Advance/Charge behält Inline-Button, §6.3) + Attacken-Feld-Re-Roll (nur Nahkampf).
Aktivierbar: Shadows of Drazak (+Datenfix `modifier:`), Whirling Onslaught, Quantum
Deflection (inkl. invuln_save-Wirkung). Rest-Schuld 10 GOs an 3 fehlenden Fenstern →
Folge-Split s. Schritt 3. **B6 umgesetzt + Stakeholder-verifiziert** (`9993771`):
Setup-Blöcke nebeneinander, „Read directive"-Dropdown (geteilter Helper mit armyCard,
INV-4b 18→17), Trennlinie. **B1-Probe:** Patch + zweistufige Ansage
`docs/handoff/S135_B1_probe.md` — Stufe-1-Befund ausstehend. Lehre: Seed-Wörter
(„protocol") in UI-Labels meiden (INV-4b). Vollsuite 1673 passed / 99,12 %, mypy 62.

Frühere Sessions (S60–S134): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S136)

1. **B1 Scroll-Sprung — H2 WIDERLEGT (Ja/Ja, S135):** Key-Rewrite ist NICHT die
   Ursache; Patch zurückgenommen. S136: H1-Probe (Fokus-Autoscroll) bzw. Drittursache
   (Layout-Shift durch `st.columns`) mit neuer Test-Ansage untersuchen —
   Befund-Doku `S135_B1_probe.md` (ANSWERED). KEIN Fix vor Browser-Befund.
1b. **4c-Nachbesserung (Stakeholder-Befund, UI noch nicht passend):** Attacken-Re-Roll
   (a) unverständlich platziert — warum in der Kachel des ausgewählten Modells?;
   (b) erscheint auch bei FESTEM Attackenwert der Waffe (sinnlos — nur bei
   variablen/Würfel-Attacken zeigen); (c) Command Re-Roll fehlt in der Attackensequenz
   (Hit/Wound/Save) generell noch (R-CMD-12 weiter 4/9). Evtl. Beleg-Screenshot
   `…2026-07-10 21-17-14.png` (Inhalt ungeprüft, deshalb behalten).
1c. **Retro-Maßnahmen S135 (Stakeholder-GO) umsetzen:** pytest-`run_in_background`-
   Sperre als Hook prüfen; Executor-Selbst-Stopp auf ~100k; Koordinator-Wind-down
   ab ~120k einleiten.
2. **Welle 2 (aus S134/S135 verschoben, Kollision durch Paket-4-Abschluss aufgehoben):**
   Task 7 Dakka (`S133_plan.md`); Task 8 `before_battle` in `PHASES` + ArmySetup-Liste
   (GO-Zählung nach BA-Bereinigung neu verifizieren); B8 redundanter Statusbereich raus
   (`…21-36-36.png`); B4-Sofortteil ++/OC-Spalten aus `_datasheet_stat_row()`
   (`gameActionsArea.py:62-63`).
3. **Folge-Split aus 4c einplanen** (`design_system.md` §6.2): generisches `on_destroy`
   (7 GOs, größter Hebel); `on_set_up` (Aetheric Interception) + `on_target`-Sonderfälle
   (Reanimation Prioritisation, Tough as Squig-Hide — eigene Auswertungslogik).
   ACHTUNG: Backlog-Design-Roadmap hat bereits ein anderes Paket 5/6 — Nummern neu vergeben.
4. **Manuelle UI-Checkliste 4a–4c + B6-Trennlinie** (S135-Review, git `Add S135 DoD
   review`) mit dem
   Stakeholder abarbeiten (Hit-/Wound-/Save-Karten, Damage/Psychic/Deny-GO-Karten,
   Attacken-Re-Roll nur Nahkampf).
5. **B7/B9-Konzept-Handoff** (EIN Dokument, Entscheidung S135) + **B2 Option A**
   Umsetzung einplanen.

**Prozess (S134 freigegeben):** Vollsuite bei parallelen Wellen nur EINMAL zentral am
Wellen-Ende, nicht je Executor → `operating_model.md` Event 3 (Vollsuite-Disziplin).

**Offen (unverändert):** `_common.py`-Refactor (Backlog §4); S130-GO-Verifikation +
Necron-Roster-Check nach UI-Umbau (Paket 7); Scroll-Render iframe→parent in manueller
Checkliste; 037 Docker-Smoke vor Merge; Deny-Caption-Prüfung blockiert;
Direction-Entscheide → Backlog §5, vertagt bis Ziel7 Stufe B/C; Charge-Re-Roll-Karte
(neuer Scope, S133-Rest).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
