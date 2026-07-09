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
- **Auftragsgrößen-Gate (S130, harte Stakeholder-Auflage):** kein Executor-Brief > Effort M — L VOR Vergabe splitten; Test-Budget (EINE Vollsuite, im Vordergrund, nie Hintergrund-pytest) + Selbst-Stopp-Klausel in jedem Brief → `agent_scopes.md`.
- **Executor-Klausel:** Dateiänderungen nur über Edit/Write, Bash nur lesend/git/pytest (S123); Selbstprüfliste enthält `python tools/mypy_gate.py` (S128).
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0, Abweichung nach oben nur mit Begründung im Commit.
- **Retro-Merkposten:** GO-UI VOR Implementierung festlegen (wenige Standard-Komponenten: „Liste unten" + „Inline"; Mockup-Gate einhalten — S130 M5); App VOR jeder UI-Verifikation neu starten + Prüfanleitungen gegen Roster-Realität validieren (S126); Lösch-Pläne auch über `docs/spec/` greppen (S126).

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). **App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S130, 2026-07-09)

S130: Alle 7 `_shared`-Gefechtsoptionen integriert — 4 reaktive anwählbar (Plan 015 TEILWEISE: Fire Overwatch, Counter-Offensive, Cut Them Down, Emergency Disembarkation), Insane Bravery auto-pass (R-MORALE-09), Desperate Breakout (R-MOVE-14, Klasse C), Command Re-Roll inline Option (c) für Damage/Psychic/Deny (R-CMD-12, 3/9 — Ausweitung = Stakeholder-Auflage, Backlog §2). Review: GO; Retro-Maßnahmen 1–5 verankert (Auftragsgrößen-Gate nach 403k-Vorfall, Vordergrund-pytest, Selbst-Stopp-Intervall, Freigabe-Gate-Ausnahme außerhalb Repo, GO-UI-Design-Merkposten). Commits `b5c774b`, `1861d9d`, `2e3aa98`, `9922555`. Vollsuite 1582 passed, Coverage 99,14 %, mypy 75 == Baseline.

Frühere Sessions (S60–S129): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

1. **Manuelle UI-Verifikation S130 (PFLICHT, blockiert „fertig"):** ① Fire Overwatch: Charge-Phase, Ziel deklarieren → Box in Gegner-Spalte (1 CP). ② Counter-Offensive: Fight-Phase nach Kampf → Box beim Gerade-gekämpft-Spieler (2 CP). ③ Cut Them Down: Retreat einer Melee-Einheit → Box beim Gegner. ④ Emergency Disembarkation: TRANSPORT zerstören → Box beim Besitzer. ⑤ Insane Bravery: Stratagems-Tab aktivieren → Morale zeigt „automatisch bestanden". ⑥ Desperate Breakout: Movement fragt Verlustzahl ab, Einheit auf Retreat. ⑦ Command Re-Roll: `↻`-Button nach Damage-Apply/Psychic-Wurf/Deny-Wurf; unsichtbar bei CP 0 oder Zweiteinsatz in derselben Phase. Dazu Ziel7-Stufe-B-Punkt: Necron-Roster-Verifikation.
2. **GO-UI-Design-Entscheid (Stakeholder, VOR weiterer GO-Arbeit):** Standard-Komponenten festlegen („Liste unten" + „Inline"), Undo-Standard ergänzen — Command Re-Roll hat keinen Undo-Button wie die anderen GOs (Backlog §2).
3. **Fraktions-Stratagems:** `before_battle`-Sichtbarkeit (6 Necron + 7 Ork), danach §6e-Modifier-Engine (~56 teilintegrierte proaktive). Details Backlog §2 + Ziel7 §6e.
4. **Command Re-Roll ausweiten (Stakeholder-AUFLAGE):** Charge/Advance zuerst, Attackenfolge nach UI-Design-Entscheid — Backlog §2.
5. rp/directive-Vokabular ausschreiben (S129-freigegeben, in S130 zugunsten GO-Integration zurückgestellt — Details Session-Archiv S129) + mypy-Ledger senken (Rest `gameMechanic/`, dann `uiLayout/`).

**Offen:** 037 Docker-Smoke vor Merge; Deny-Caption-Prüfung blockiert (braucht Roster mit Deny-Einheit auf Gegenseite); Direction-Entscheide (Ziel9-Fetcher/Deployment/Mission-Scoring) → Backlog §5 — in S130 NICHT entschieden, wieder vorlegen.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M!).
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, Pfade außerhalb des Repos).
