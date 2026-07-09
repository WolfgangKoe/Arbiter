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
- **Auftragsgrößen-Gate (S130):** kein Executor-Brief > Effort M; Test-Budget (EINE Vollsuite, im selben Tool-Call abwarten, `run_in_background` für pytest VERBOTEN — S131 erneut verletzt) + Selbst-Stopp in jedem Brief → `agent_scopes.md`.
- **Handoff-Marker-Pflicht (S131):** jeder Brief, der nach `docs/handoff/` schreibt, nennt den STATUS-Marker für Zeile 1.
- **Grundannahmen-Block (S131):** Konzept-Dokumente starten mit bestätigungspflichtigen Grundannahmen (App würfelt NICHT — Tischwürfe!) → `agent_scopes.md`.
- **Executor-Klausel:** Dateiänderungen nur über Edit/Write, Bash nur lesend/git/pytest (S123); Selbstprüfliste enthält `python tools/mypy_gate.py` (S128).
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S132, 2026-07-10)

S132 (Commit `0a94adb`): GO-UI Paket 1+2 — `go_card.py` (4 Zustände, Akkordeon-Fix) + `render_go_card`/`undo_stratagem` in `_common.py`; Stratagems-Liste auf GO-Karten; Re-Roll-Angebot Advance/Charge; Start-Game-Button unter Erstspieler-Auswahl; Doku-Nachzug §6.3. Vollsuite 1608 passed, Cov 99,15 %, mypy 75 = Baseline. **Stakeholder-Review = NO-GO, 5 Befunde** → `docs/handoff/S132_defects.md`. K1 (Karten-Anatomie, Fix-Plan in `S132_K1_result.md`) + K4 (Alt.-Fire-Text) beim Abschluss als Hintergrund-Agenten neu gestartet (erster Lauf starb an Session-Limit/Freigabe-Gate) — Ergebnisse in `docs/handoff/S132_K*_result.md`, **ungeprüft**.

Frühere Sessions (S60–S131): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S133)

1. **K1/K4-Ergebnisse konsumieren:** Marker prüfen, EINE Vollsuite, manuelle UI-Prüfung (CP genau 1×, Button in Header-Zeile, Zustandsfarben, Alt.-Fire-Text), Handoffs löschen.
2. **K3 starten (XS, beauftragt+freigegeben, noch nicht gelaufen):** `orks/stratagems.yaml` „Get Stuck In, Ladz!" `conditions: [BOYZ, BEAST SNAGGA]` + Regressionstest + Vollsuite (Datenänderung!).
3. **K2 (S–M, Design ENTSCHIEDEN, noch unbeauftragt):** Re-Roll als GO-Kompaktkarte, **dauerhaft sichtbar im Einheiten-Kontext der Phase, auch vor der Entscheidung** + Undo; erfordert Bewegungsphasen-UI-Umbau. Stakeholder-State-Modell: Einheit anfangs „Stationary" → zeige Move/Advance/Command-Reroll; „in melee" → nur Retreat (kein Re-Roll); Reserve → kommt ins Spiel nachdem alle bewegt/vorgerückt; „Stay Stationary" nur als Reset-Button, ersetzt den gedrückten Moved/Advanced/Retreat-Button (Funktion existierte schon). **Planner: Regeln nachprüfen (Fall Back/Reserven) + notierte State-Änderungen sichten.**
4. **Paket 3:** reaktive Stratagem-Box (`render_reactive_stratagem_box`, `_common.py:523`) auf GO-Karte + `before_battle`-Fix.
5. **Beobachtung ④ (XS–S):** Profilkarte Setup — doppeltes `""` beim Bewegungswert, Profilwert-Reihenfolge (`Stakeholder_Beobachtungen.md` + Screenshots). Danach **Refinement Beobachtung ②** (Mockup mit Stakeholder).

**Retro-Vorschläge S132 (Entscheid ausstehend):** ① Handoff-Konvention: Stakeholder legt Beobachtungen/Screenshots asynchron ab, beeinflusst Sessionplan NICHT, Verarbeitung delegierbar. ② DONE-Handoffs sofort konsumieren+löschen BEVOR der nächste Executor die Vollsuite startet (Hygiene-Gate riss). ③ Brief-Baustein: bei Harness-Auto-Backgrounding von pytest TaskOutput abwarten statt stehenzubleiben. ④ UI-Briefs: Selbstprüfpunkt „Anatomie-Abgleich gegen design_system, keine funktionslosen Attrappen". ⑤ Freigabe-Marker setzt NUR der Stakeholder (Koordinator hat in S132 einmal selbst getouct).

**Offen:** `_common.py` wächst weiter (Refactor-Notiz Backlog §4); S130-GO-Verifikation + Necron-Roster-Check nach UI-Umbau (Paket 7); Scroll-Render iframe→parent in manuelle Checkliste; 037 Docker-Smoke vor Merge; Deny-Caption-Prüfung blockiert; Direction-Entscheide → Backlog §5, vertagt bis Ziel7 Stufe B/C.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
