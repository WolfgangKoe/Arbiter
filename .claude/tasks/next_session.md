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

## Aktueller Stand (nach S133, 2026-07-10)

S133 (6 Executor-Tasks, 2 Wellen): S132-K1/K4 konsumiert; K3-Conditions ✓; Profilkarte
Setup (`6""`→`6"`, 9E-Reihenfolge) ✓; S133-D: GO-Karten-Anatomie neu (EIN
`st.container(border=True)`, Button nur `Use`/`↺ Undo`, CP nur Header, Akkordeon IN der
Karte), Desperate-Breakout-Gating (nicht bewegt + in ER, danach „retreated") + Zieleinheit
im Header; K2: in melee ⇒ nur Retreat, „Stay Stationary" = Reset (stellt in-melee +
Abhängigkeit wieder her), Reserven nach allen Feldbewegungen, Re-Roll als GO-Kompaktkarte;
Paket 3a Reaktiv-Box→GO-Karte (Pass-Button entfällt). `design_system.md` §6.4→§6.1
angeglichen + **NEU §6.2 Sichtbarkeits-Invariante** (GO-Karte genau 1× — inline ODER
Liste). Vollsuite 1637 passed, Cov 99,11 %, mypy 75→63. Review: GO (`S133_review.md`).

Frühere Sessions (S60–S132): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S134)

1. **UI-Befunde gegen die neue §6.2-Invariante (Stakeholder-Feedback, Prio):**
   (a) Desperate Breakout erscheint doppelt (inline + zentrale Liste) — entweder/oder;
   (b) Fire-Overwatch-Karte ohne Undo-Button; (c) Re-Roll-Karte 1× statt pro Unit.
2. **Welle 3 aus S133 (verschoben, Briefs fertig in `S133_plan.md` Tasks 7+8):**
   Task 7 K4-Dakka an die Attackenzuweisung (Badge im Hit-Block raus, Regel
   `wahapedia_orks/faction_overview.txt:626`); Task 8 Paket 3b `before_battle` in
   `PHASES` + ArmySetup-Liste. Vorher Datei-Overlap per `git diff --stat` prüfen.
3. **Refinement mit Stakeholder:** profileCard als definierter Baustein (Beobachtung ④-Rest:
   YAML→Datenkarte im Setup, tabellarische Waffenanzeige); danach Beobachtung ②
   (Spielvorbereitungsscreen); neu: Beobachtung ① Scroll-Sprung bei Command Protocols.
4. **Kleinkram/Schulden:** `reactive_declined` totes State (`game_state.py:510/576`)
   bei nächster Berührung entfernen; Charge-Re-Roll noch Inline-Offer (Karte = neuer Scope);
   `render_inline_command_reroll` hat noch 3 Call-Sites (Damage/Psychic/Deny, Paket 4).

**Retro S133 (entschieden):** NUR „§6.2-Sichtbarkeits-Invariante" angenommen (umgesetzt);
bewusst abgelehnt: pytest-Backgrounding-Brief-Baustein, Ergebnisdatei-früh-Baustein.
Beobachtung fürs Protokoll: 3 Executor-Stalls am pytest-Auto-Backgrounding (scharfe
Klausel in T6 half); 2 Agenten-Abbrüche am API-Session-Limit (Wiederaufnahme via
SendMessage funktionierte, nichts verloren).

**Offen (unverändert):** `_common.py` wächst weiter (Refactor-Notiz Backlog §4);
S130-GO-Verifikation + Necron-Roster-Check nach UI-Umbau (Paket 7); Scroll-Render
iframe→parent in manueller Checkliste; 037 Docker-Smoke vor Merge; Deny-Caption-Prüfung
blockiert; Direction-Entscheide → Backlog §5, vertagt bis Ziel7 Stufe B/C.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
