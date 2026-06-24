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

## Aktueller Stand (nach S92, 2026-06-24)

**S92 (auf `feature/016`) — UI-Verifikation: 1a ✅; 1b+1c als ECHTE Bugs bestätigt, Wurzel eingegrenzt, NICHT gefixt.**
0b (Mirror-Match: Spieler-2-Karte unverändert) ✅ · 1a (Eternal Guardian Save „(defender)" im Gegnerzug) ✅.
**1b** (Undying-Legions-P RP-Reroll-Hint im Gegnerzug) + **1c** (Undying-Legions-S Living-Metal +1 Heilung) erscheinen
NICHT — Setup vom User korrekt (Primary/Secondary aktiv, Modell zerstört, Living-Metal-Einheit). Diagnose: **Engine
ist korrekt** — Wegwerf-Repro (`scratchpad/repro.py`) liefert `get_active_rp_modifiers`→`{rp_reroll:True}` und
`get_active_heal_bonus`→`1` bei direkt gesetztem State; `target_rule livingMetal` steht in `unit.rules` (kein
Mismatch); statische Write/Read-Kette nutzt durchgängig denselben `faction`-Key (Roster-Name, `render_army_card`).
⇒ Ursache ist ein **Laufzeit-State-Unterschied** (Direktiv-Keys real anders gesetzt als gelesen), nur mit
Live-`session_state`-Werten pinbar. Widerspruch: 1a (gleicher Gegnerzug-Verteidiger-Kontext) funktioniert.
**NÄCHSTER SCHRITT (vom Stakeholder FREIGEGEBEN):** temporären Debug-Probe in `render_army_card`
([armyCard.py:426](../../src/uiLayout/armyCard.py#L426)) — `st.expander` mit `faction`, `session_state.active`,
4× `round_choice_*_<faction>`-Keys (active/directive/used_ids/extra_directive). User reproduziert 1b+1c **einmal**
→ Wurzel pinnen → Fix + Regressionstest → Probe entfernen → Vollsuite → Re-Verify. Bugs gehören zu **016**.

**S92 — Branch-Befund (wichtig):** `main` ist **331 Commits** hinter `feature/016`; aktiver Integrations-Branch
ist `dev` (=016−35). Branch `chore/context-engineering-and-test-fixture` von `dev` angelegt für die unten vertagten
chore-Aufgaben; „schnell mergen→dev→Branch löschen". Aufgabe 1 (Mock-Fixture) berührt Tests → die 016-only
`test_round_choice_player_keyed.py` beim späteren 016→dev-Merge nachmigrieren.

**S91 (historisch):** Mirror-Match-Kollision gefixt (`round_choice_state_key(player,kind)`, pro Spieler-Slot;
1129 grün/93 %). Kontext-Engineering-Initiative gestartet (Write/Select/Compress/Isolate; je Session Auditor+
Optimierer; Regeldateien verbatim heilig; `docs/handoff/context-audit-S91.md`).

**S90 (historisch):** 3 Direktiv-/State-Bugs gefixt (Direktive im 2. Zug · Zielauswahl Runde 2 · Living Metal).

### ⚠️ Carry-over (offen)
0. **Kontext-Engineering-Setup (NEU, frische Session):** governance-Doc `context_engineering.md` + SessionStart-Hook
   (Auditor auto) + Regel-Index (Stichwort→Datei:Zeilen, verbatim heilig) + ziel6.md-Kompression (Auditor-Top-Finding).
   `docs/handoff/context-audit-S91.md` durch Optimierer verarbeiten + danach löschen. Je eigene Freigabe.
0b. **Manuelle UI-Verifikation S91 (PFLICHT, Render-Code):** Necron-vs-Necron, Befehlsphase — Spieler-1-Protokoll/
   Direktive wählen → Spieler-2-Karte bleibt unverändert (eigene Wahl/Badge). Das war das Original-Symptom.
1. **Manuelle UI-Verifikation (S92-Stand):** (a) Eternal-Guardian-Save „(defender)" im Gegnerzug ✅;
   (b) Undying-Legions-P RP-Reroll-Hint ❌ + (c) Living-Metal-S heilt 2 ❌ → **echte 016-Bugs, Debug-Probe siehe
   Stand oben**; (d) Bug 5: Runde-2-Fernkampf Zielwahl — **noch nicht geprüft**.
1b. **Vertagter S92-chore-Plan (Branch `chore/context-engineering-and-test-fixture` von `dev`, je Freigabe):**
   *Aufg. 4* Sonnet-Subagent zieht Präsentation (`curl -u andrena:slides4all
   https://peter-wegner-slides.pages.dev/context-engineering-andrena-v2/`, Inhalt = minifiziertes Vue-JS → Text
   extrahieren) → `docs/reference/context-engineering-slides.md` + Ideen für auto-`overview.md`. *Aufg. 3* neuer
   read-only Auditor (Sonnet) → `docs/handoff/context-audit-S92.md` (neue Dateien, NICHT die 8 aus S91); Optimierer
   arbeitet `context-audit-S91.md`-Findings #3/#4/#6/#7 ab (XS/S) + danach S91-Datei löschen; #1 ziel6.md-Kompression
   (L) eigener Slot. *Aufg. 1* Mock-Fixture: geteilte streamlit-Fixture in `tests/conftest.py`, 17 Testdateien von
   `_st_mock` auf `module.st` (Opus-Pilot 1 Datei → Sonnet-Subagent Rest → Opus-Review). Reihenfolge: 1b/1c-Fix zuerst.
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
- **S92-Lehre Repro-zuerst:** bei „Engine oder Verdrahtung?" sofort Isolations-Repro schreiben statt langer statischer Analyse (spart Kontext).
- **S92-Lehre Branch-Check:** vor `git checkout -b … <base>` den aktiven Branch prüfen (`main` war 331 zurück; aktiv = `dev`).
- **S92-Lehre Plan-Realismus:** nicht 4 Aufgaben + Pflicht-Verifikation in einen Korridor; konservativer schneiden.
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
