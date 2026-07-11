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
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0 (S133: 75→63; Stand S136: 62).
- **Vollsuite-Timeout (S136):** Bash-`timeout: 600000` bei jeder Vollsuite explizit setzen
  (2-Min-Default killt den Lauf) → `agent_scopes.md`. Playwright-UI-Verifikation ist
  Standard-Werkzeug für funktionale UI-Befunde (ersetzt NICHT die Design-Sichtprüfung).

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S136, 2026-07-11)

S136 (Review **GO**, `docs/handoff/S136_review.md`): **B1 Scroll-Sprung gefixt +
verifiziert + Stakeholder-bestätigt.** Ursache Layout-Shift plus Chrome Scroll-Anchoring
(H1 Fokus-Autoscroll, H2 Key-Rewrite beide widerlegt, Playwright-Befund
`docs/handoff/S136_B1_probe.md`). Fix: `overflow-anchor: none` auf
`section[data-testid="stMain"]` (`gameHeader.py`), Delta 0/0/0 (vorher +2348).
Verankert in `CLAUDE.md` §Streamlit CSS. **4c a/b/c komplett:** Attacken-Re-Roll nur
noch bei variablem/Würfel-Attackenwert (`_is_variable_attacks`), Platzierung
nachgebessert, Command Re-Roll jetzt auch in Hit-/Wound-/Save-Block
(`_render_resolution_tab`, pragmatischer Familie-2-Ansatz, Stakeholder-Entscheid
`S136_4cc_befund.md`) — **R-CMD-12 9/9 verdrahtet**. Retro-Maßnahmen verankert:
S135-Maßnahmen (Hook `tools/hook_pytest_foreground.py`, Selbst-Stopp 100k,
Wind-down 120k) + neue S136-Maßnahmen (Vollsuite-Bash-Timeout 600000,
Playwright als Standard-UI-Verifikationswerkzeug) in `agent_scopes.md`.
Vollsuite 1691 passed / 99,12 %, mypy 62.

Frühere Sessions (S60–S135): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S137)

1. **Rest der manuellen UI-Prüfung beim Stakeholder abfragen** (Hit-/Wound-/Save-
   Buttons, Re-Roll-Platzierung/Label; B1 ist bereits bestätigt) + neue
   Backlog-Beobachtung **B11** (Rest-Sprung/Zucken nach B1-Fix) im Blick behalten.
   Zusätzlich: neue, noch unverarbeitete Beobachtung in
   `docs/handoff/Stakeholder_Beobachtungen.md` (Command-Re-Roll-Zustand bei bereits
   genutzter GO in der Phase) triagieren.
2. **Welle 2** (aus S135/S136 verschoben): Task 7 Dakka (`S133_plan.md`); Task 8
   `before_battle` in `PHASES` + ArmySetup-Liste; B8 redundanter Statusbereich raus
   (`…21-36-36.png`); B4-Sofortteil ++/OC-Spalten aus `_datasheet_stat_row()`
   (`gameActionsArea.py:62-63`).
3. **Folge-Split aus 4c einplanen** (`design_system.md` §6.2) als **Paket 7**
   (generisches `on_destroy`, 7 GOs, größter Hebel) / **Paket 8** (`on_set_up`
   Aetheric Interception + `on_target`-Sonderfälle: Reanimation Prioritisation,
   Tough as Squig-Hide) — Nummern bewusst neu vergeben (Kollision mit
   Wortlaut-/Einheiten-Paket 5/6 vermeiden).
4. **B7/B9-Konzept-Handoff** (EIN Dokument, Entscheidung S135) + **B2 Option A**
   Umsetzung einplanen.
5. **Kleinschulden:** Smoke-Test `tools/hook_pytest_foreground.py`; Testlücke
   `chargephase.py:114` (Command-Re-Roll-Aufrufstelle ungetestet); `design_system.md`
   §6.3 Wertfeld-/Familie-2-Formulierung präzisieren; `next_session.md` beim nächsten
   Kürzen straffen; mypy-Ratchet 62→runter; `_common.py`-Refactor (Backlog §4);
   S130-GO-Verifikation; 037 Docker-Smoke vor Merge; Deny-Caption-Prüfung blockiert;
   Direction-Entscheide → Backlog §5, vertagt bis Ziel7 Stufe B/C.

**Prozess (S134 freigegeben):** Vollsuite bei parallelen Wellen nur EINMAL zentral am
Wellen-Ende, nicht je Executor → `operating_model.md` Event 3 (Vollsuite-Disziplin).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Koordinator-Wind-down einleiten, spätestens ~135k beenden (S136-präzisiert); Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
