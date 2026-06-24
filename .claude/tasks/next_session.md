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
`streamlit run src/app.py` (Port 8501; **venv aktivieren:** `source .venv/bin/activate`).
Branch `dev` (Arbeit), `main` (nur per PR).

---

## Aktueller Stand (nach S91, 2026-06-24)

**S91 (Branch `feature/016-protocol-rp-effects`) — Mirror-Match-Protokoll-Kollision gefixt** (1129 grün/93 %,
INV-4b grün, Formatter sauber). Root Cause: Protokoll-Laufzeit-State (active/directive/used_ids/extra_directive)
war per `faction_dir` gekeyt → zwei Necron-Armeen teilten `round_choice_*_necrons`; Spieler-1-Wahl überschrieb
Spieler 2 (auch die Kampf-Engine las den geteilten Key). Fix: neuer Helfer `round_choice_state_key(player, kind)`
keyt **pro Spieler-Slot**; Engine-Fns nehmen `player`, leiten `faction_dir` nur fürs Laden ab. Dateien: game_state,
ability_engine, _common, armyCard + test_ability_engine/test_game_state (Konvention, Assertions unverändert) +
neu test_round_choice_player_keyed (3 Mirror-Match-Regressionstests). Lifecycle (S90) unberührt.
**Befund:** Tests sind reihenfolgenabhängig (Backlog §4 Mock-Fragilität) — Fix selbst grün (Vollsuite+Einzeldatei).

**S91 — Kontext-Engineering-Initiative gestartet** (Stakeholder-Wunsch, Rahmen: LangChain Write/Select/Compress/
Isolate). Entscheidungen: (a) Subagent-Ergebnisse **nur bei Umfang** in `docs/handoff/`-Datei (Lebenszyklus
erzeugt→verarbeitet→gelöscht), kleine Antworten inline; (b) **jede Session automatisch** ein read-only Auditor
(schlägt vor, schreibt Findings) + Optimierer (ändert nur Freigegebenes); (c) **Regeldateien verbatim heilig** —
nur additiver Index. Auditor-Pilot lief → `docs/handoff/context-audit-S91.md` (Top: ziel6.md 1744 Z. komprimieren).
Setup-Artefakte (governance-Doc, SessionStart-Hook, Regel-Index) brauchen je eigene Freigabe → frische Session.

**S90 (historisch):** 3 Direktiv-/State-Bugs gefixt (Direktive im 2. Zug · Zielauswahl Runde 2 · Living Metal).

### ⚠️ Carry-over (offen)
0. **Kontext-Engineering-Setup (NEU, frische Session):** governance-Doc `context_engineering.md` + SessionStart-Hook
   (Auditor auto) + Regel-Index (Stichwort→Datei:Zeilen, verbatim heilig) + ziel6.md-Kompression (Auditor-Top-Finding).
   `docs/handoff/context-audit-S91.md` durch Optimierer verarbeiten + danach löschen. Je eigene Freigabe.
0b. **Manuelle UI-Verifikation S91 (PFLICHT, Render-Code):** Necron-vs-Necron, Befehlsphase — Spieler-1-Protokoll/
   Direktive wählen → Spieler-2-Karte bleibt unverändert (eigene Wahl/Badge). Das war das Original-Symptom.
1. **Manuelle UI-Verifikation (PFLICHT, Render-Code) — ERNEUT nach Fix:** (a) Eternal-Guardian-Save zeigt
   „(defender)" wenn Necrons im GEGNERZUG beschossen werden; (b) Undying-Legions-Primary: RP-Reroll-Hint
   erscheint wenn Necron-Einheit im Gegnerzug Modelle verliert; (c) Living-Metal-Secondary: heilt 2 bei
   livingMetal-Einheit mit ≥2 verlorenen Wunden; (d) Bug 5: Runde-2-Fernkampf, Warrior wählen → Ziel sofort wählbar.
2. **Bug 3 — Zweitspieler-Direktiv-Wahl (NEUER Plan-016-Step, Stakeholder „später"):** Direktive nur für
   aktiven Spieler in Befehlsphase wählbar (armyCard.py:296,307). Zweitspieler kann am Rundenanfang
   (= Gegner-Befehlsphase) nicht wählen. Step: Direktiv-Buttons entkoppeln (wählbar sobald Protokoll aktiv
   + Direktive offen, jede Phase) — neue UI-Logik, **eigene Freigabe**.
3. **Plan 016 Anzeige-Rest (Subagent-Slicing → `docs/audit/plans/016`):** *Group A* (~35k) Eternal Guardian S
   + Conquering Tyrant S reroll-Captions, gemeinsamer `_round_choice_reroll_hints`-Helper (Muster: `_rp_directive_hints`).
   *Group C* (~20k) Sudden Storm P „+N\" Move"-Badge (movementPhase) + Conquering Tyrant P Morale (Morale-UI fehlt evtl. → prüfen).
   **Steps 4/5 (Hungry Void S +1S, Vengeful Stars S AP-1) → Plan 017** (Stakeholder-Entscheid: Mathe+Anzeige
   unverdrahtet, überschneidet SAVE-AP-Badge). Dynastiebonus-Anzeige bereits erledigt (`_render_extra_round_choice`).
   Voice of the Triarch = eigener Plan.
4. **Reihenfolge:** Plan 016 Anzeige-Rest (Group A → C) → 018 → 015 → 017 (017 nimmt Steps 4/5 auf).

### Offene Fragen / Retro-Vormerke
- **Doku-Sync ausstehend:** backlog #2 / ziel6 6e um Bug-3-Step + „Reset kampfrunden-weit" ergänzen (in S90 nur
  in dieser Datei). Bei nächstem Full-Wind-down nachziehen.
- **ADR-0006-Verweis (S86):** `CLAUDE.md` Token-Disziplin um Verweis auf ADR-0006 ergänzen (Subagent-Großausgaben als Datei).
- **INV-4b Restschuld:** `dynasty` (movementPhase), `gloom/prism` (psychicPhase → Cluster 5), `necrons`-Defaults
  (game_state/loader). Ratchet weiter schrumpfen.
- **Mock-Fragilität (backlog §4):** geteilte streamlit-Fixture (conftest) statt per-Datei-Mock.

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
