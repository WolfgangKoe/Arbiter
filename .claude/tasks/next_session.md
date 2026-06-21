# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → ziel6.md; Backlog → backlog.md. -->
<!-- Referenzwissen NICHT hier: Architektur-Muster → architecture.md, Regel-Gotchas →
     rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start "start next session" → Planning vorlegen** (Prioritäten + Token-Schätzung), erst nach
  Freigabe los; Shortcut „Plan ist freigegeben" = direkt los. **Lesen:** `CLAUDE.md` (Freigabe,
  bei Unklarheit fragen) + `docs/goals/ziel6.md` (Aufgaben/Historie) + `docs/goals/backlog.md`.
  Einstieg: `LEITSTAND.md`; Rollen/Tier/Events/Modi: `docs/governance/operating_model.md`.
- **Ende:** Review → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) → Abschluss: Checkboxen
  in `ziel6.md` + Historien-Zeile; **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen).
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70**
  kürzen, nicht knapp drunter — Erledigtes → `backlog.md`/`ziel6.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten
  = stehende Freigabe (proaktiv, ohne Nachfrage, ADR-0005); rote vorher-grüne Tests =
  STOP + fragen.** Details: `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter für WH40k 9E, Streamlit (Python). Start:
`streamlit run src/app.py` (Port 8501). Branch `dev` (Arbeit), `main` (nur per PR).

---

## Aktueller Stand (nach S85, 2026-06-21)

**S85 (Branch `feature/014-defender-loss-allocation`) — Doku-Drift bereinigt + Orb-Bug fertig + Plan 024 angelegt:**
- **Drift-Befund:** Pläne **022 (DONE S77)** und **014 (DONE S82, Teil A+B)** waren längst code-fertig +
  getestet + committet, aber `backlog.md`/README zeigten noch TODO/IN-PROGRESS. Status korrigiert.
  **Offen bei beiden nur:** manuelle UI-Verifikation (Render-Code).
- **Orb-Bug (S84-Fix war unvollständig) GEFIXT:** zweiter Overlord-ResOrb zeigte keine Reanimations-
  Buttons. Wurzel: drei **Streamlit-Widget-Keys** in `commandPhase._render_activated_wargear`
  (`cmd_revive_wargear*`) nur nach `wargear_id` geschlüsselt → Duplikat-Key bei zwei Trägern →
  „Use"-Button kollidiert, `pending_target_request` für Orb #2 nie gesetzt. Fix: Keys über das bereits
  bearer-scoped `request_id` führen; +Test `test_two_orb_bearers_render_distinct_button_keys`.
  `test_command_phase.py` 16 grün. **⚠️ Manuelle Tisch-Re-Verifikation offen** (Render).
- **Plan 024 angelegt** (`docs/audit/plans/024-arkana-protocol-effect-modeling.md`), per Sonnet-Subagent
  recherchiert + von Opus verifiziert. **Ehrlicher Befund:** aus der YAML sind alle 12 Arkana identische
  `descriptive`-Stubs — Dispatchbarkeit folgt allein aus dem **Regeltext** vs. vorhandene Handler. **Nur
  9 Protokoll-Direktiven + 1 Arkanum (Failsafe, Annahme) real machbar**; 10/12 Arkana brauchen neue
  Engine-Subsysteme → bleiben begründet `descriptive`. Bonus: 3 Punktkosten weichen ab (failsafe 30→25,
  atavindicator 25→20, nanomines 30→25).

### ▶ Nächste Session
1. **Plan 024 umsetzen — frischer Start** (Step 1 = `strength_modifier`-Direktiv-Pilot end-to-end).
   ⚠️⚠️ **PFLICHT-TESTNETZ pro Step — NICHT optional, ausdrücklich gefordert (S85):** (a) **Unit**-Tests
   je neue Funktion/Verzweigung; (b) **Acceptance/State**-Tests; (c) **INV-4b-Architektur-Gate** (kein
   neuer Faction-String in `src/`); (d) **manuelle UI-Verifikation** (Render-Code); (e) **Doku-Pflege**
   (`faction_abilities.md`, `backlog.md` #2, Plans-README, Akzeptanzkatalog). Done-Kriterien des Plans
   abarbeiten. Step 5 (Failsafe) verifiziert die `buff_stat`-Annahme gegen den echten Handler — bricht
   sie, bleibt das Arkanum `descriptive` (STOP).
2. **Manuelle UI-Verifikationen einsammeln** (Render-Code, von Tests nicht gedeckt): Orb-Zwei-Orb-Fix am
   Tisch (necrons_1500pts_silent_king); 014 Nobz Zustand A/B/C + Szarekh-Pools; 022 „Power Klaw"-Truncation.
3. Danach Queue: 016 → 018 → 015 → 017.

**Drift-Lehre (verstärkt S85):** Schon zum **zweiten** Mal hing Plan-Status der Realität hinterher (S84:
`load_faction_abilities`; S85: 022/014 längst DONE). **Drift-Check IMMER vor Effort-Schätzung** — Code-
Stand selbst prüfen, Pläne als „Stand kann veraltet sein" lesen.

**Historie verdichtet:** S84 Plan 021 (Arkana-Daten-Migration) + Orb-State-Key-Fix. S83 Plan 020.
S82 Plan 014 Teil B. Details → `docs/goals/ziel6.md`.

### Offene Fragen / Retro-Vormerke
- **ADR-0005-Lücke:** Freigabe-Gate feuert sauber im **Opus-Hauptkontext**; offen: auch im **Subagent**?
- **Doku-Drift:** `architecture.md` §session_state — `group_wounds` universell (backlog §4b).
- **INV-4b Restschuld:** noch `dynasty` (movementPhase), `gloom/prism` (psychicPhase → Cluster 5),
  `necrons`-Defaults (game_state/loader). `arkana` erledigt (S84). Ratchet weiter schrumpfen.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 90 %, `pyproject.toml`).
- **Schulden-Scoreboard** nach jedem `pytest` (`tests/conftest.py`).
- Architektur (INV-1..4b): `pytest tests/architecture/ --no-cov -q`.
- Doku/Akzeptanz (INV-5): `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor:** <150k, bei ~135k Session beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report:** `python tools/token_report.py --write` → `docs/metrics/overview.md`.
- **History-Rotation:** `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
</content>
</invoke>
