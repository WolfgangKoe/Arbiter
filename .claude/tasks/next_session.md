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

## Aktueller Stand (nach S131, 2026-07-09)

S131 = Design-Session: GO-UI-Design-System entschieden + verankert (`docs/spec/design_system.md` §6 — EINE GO-Karte, 4 Zustände ruhend/bereit/verwendet/gesperrt, 3 Orte, Tisch-Wurf-Baustein, Vollrückgängig-Undo, Wortlaut Use/Undo/Confirm, Englisch). Referenzen: `docs/reference/go_klassifikation.md` (95 GOs, 3 Achsen) + `docs/reference/ui_inventar_gameactionarea.md` (17 Muster). Roadmap 6 Pakete S132–S134+ in `backlog.md` §2. **Fixierte Grundannahme: App würfelt NICHT** — Tischwürfe, App erinnert/bucht; Undo = Versehens-Korrektur, Schiedsrichter erst am Phasen-/Zug-/Rundenende. Scroll-Bug Setup→Spielstart gefixt (`_scroll_to_top`-Flag, `render_scroll_to_top()`), **manuell verifiziert**. Review GO; Vollsuite 1582 passed, Coverage 99,14 %, mypy 75 = Baseline.

Frühere Sessions (S60–S130): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S132)

1. **Paket 1 (M):** GO-Karten-Baustein bauen (4 Zustände, Voll-/Kompaktform, Akkordeon-Fix: klappt nie selbst zu) + zentrale Stratagems-Liste darauf umstellen. Spec: `design_system.md` §6.
2. **Paket 2 (M):** Tisch-Wurf-Eingabe-Baustein + Command Re-Roll für Advance/Charge (Stakeholder-Auflage; Mockup in `design_system.md` §6).
3. **Klein (S):** „Start Game"-Button unter die Erstspieler-Auswahl verschieben (Stakeholder-Beobachtung ③, `docs/handoff/Stakeholder_Beobachtungen.md` — Datei NICHT löschen!).
4. **Refinement:** Spielvorbereitungs-Screen überarbeiten (Beobachtung ②, unkonkret) — erst Mockup-Schritt mit Stakeholder, dann Auftrag (Backlog §2).

**Offen:** S130-GO-Verifikation + Necron-Roster-Check bewusst auf nach dem UI-Umbau verschoben (Roadmap-Paket 7); Scroll-Render iframe→parent coverage-frei → in die manuelle Checkliste nach Umbau; `before_battle`-Fix jetzt Teil von Paket 3 (S133); 037 Docker-Smoke vor Merge; Deny-Caption-Prüfung blockiert (braucht Roster mit Deny-Einheit); Direction-Entscheide (Ziel9/Deployment/Mission-Scoring) → Backlog §5, weiter vertagt bis Ziel7 Stufe B/C.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
