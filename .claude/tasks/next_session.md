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

## Aktueller Stand (nach S134 Welle 1, 2026-07-10)

S134 Welle 1 (Review GO, 1644 passed / 99,11 % / mypy 63): (1) **Boarding-Actions-
Bereinigung** — Rapid Reanimation, Shield-Piercer Projectors, Flensing Capacitors,
`resurrection_protocols_character` aus `necrons/stratagems.yaml` entfernt (Live-Wahapedia:
BA-only; der Rapid-Reanimation-Fehlmatch „no Advance roll open" verschwand mit —
Merkposten: `phase: any`+`event: after_roll` fehlmatcht JEDEN after_roll-Anker, Events
müssen wurfspezifisch sein). (2) **§6.2 statisches Modell:** reaktiv = on-trigger aktiv
(Stakeholder-Definition, S134-Review Befund 2 — z. B. Auswahl einer in-melee-Unit) ⇒ nur
inline; proaktiv ⇒ nur Tab-Liste; Overwatch-Reaktivbox mit ↺ Undo. **Bestätigter MAJOR:**
14 `phase_reactive`-GOs (u. a. Core-RP Resurrection Protocols) bis Paket 4 nirgends
aktivierbar — Schuld-Tabelle `design_system.md` §6.2, UI-Checkliste vom Stakeholder
bestätigt. (3) B5 First-Player-Block (UI-verifiziert 5/5, Ort: `gameActionsArea.py`
`_render_setup`, NICHT setupScreen), `reactive_declined` restlos entfernt. (4) STANDING-
Eingangskanal `docs/handoff/Stakeholder_Beobachtungen.md` (NIE löschen); Beobachtungen
B1–B10 mit Vorgehen in `backlog.md` §2; Entscheidungsfragen in `S134_offene_punkte.md`.

Frühere Sessions (S60–S133): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S135)

1. **Paket 4 (TOP-PRIO — löst die 14 nicht aktivierbaren reaktiven GOs auf).** Split
   (aus S134-Plan v3, Briefs ≤ M): **4a** Hit-+Wound-Anker (`_common.py`, Kompaktkarte am
   Wurfbereich; M); **4b** Save-+Damage-Anker + Ablösung der 3
   `render_inline_command_reroll`-Call-Sites (Damage/Psychic/Deny; M); **4c**
   Anzahl-Attacken-Fenster + R-CMD-12-Restabgleich (9 Wurf-Arten) + §6.2-Schuld-Tabelle
   abbauen + go_klassifikation-Nachzug (S–M). Fehlende Ereignis-Fenster (`on_target`,
   `on_set_up`, generisches `on_destroy`) in 4c bewerten, ggf. eigener Folge-Split.
2. **Welle 2 (aus S134 verschoben):** Task 7 Dakka (`S133_plan.md`; NACH 4a/4b —
   `_common.py`-Kollision); Task 8 `before_battle` in `PHASES` + ArmySetup-Liste
   (GO-Zählung nach BA-Bereinigung neu verifizieren); B8 redundanter Statusbereich raus
   (`…21-36-36.png`); B4-Sofortteil ++/OC-Spalten aus `_datasheet_stat_row()`
   (`gameActionsArea.py:62-63`).
3. **B1 Scroll-Sprung — Hypothesen-Verifikation (XS, Stakeholder-Auftrag „Prüfe deine
   Hypothesen"):** H1 Fokus-Autoscroll vs. H2 DOM-Remount durch Sechsfach-Key-Rewrite
   (`_render_round_choice_assignment`, `gameActionsArea.py` on_change). Ablauf MIT exakter
   Test-Ansage: Executor baut Probe-Variante (Key-Rewrite deaktiviert) → Koordinator gibt
   dem Stakeholder die genaue Ansage („App neu laden → Setup-Phase → einen
   Command-Protocol-Slot ändern → springt der Screen noch? Ja/Nein") → je Befund gezielter
   Fix + Regressionstest. KEIN Fix vor dem Browser-Befund.
4. **Offene Entscheidungen (Diskussion):** `S134_offene_punkte.md` — B2/B4/B6/B7/B9 mit
   Optionen+Empfehlung; B10-CLAUDE.md-Vorschläge (Kommentar-Konvention +
   Artefakt-Landkarten-Zeile STANDING-Kanal) — beide freigabepflichtig.

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
