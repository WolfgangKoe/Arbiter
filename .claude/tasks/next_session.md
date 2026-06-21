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

## Aktueller Stand (nach S83, 2026-06-21)

**S83 (Branch `feature/014-defender-loss-allocation`) — Plan 020 Generic Activated Wargear DONE:**
Vollsuite **1088 grün**, Cov **92,90 %**, Gate 92 %, ruff/black/isort + Architektur-Gate grün.
- **A** `_render_resurrection_orb` → generisch `_render_activated_wargear` (Name/`once_per_battle`
  aus YAML; Lookup via `activated_wargear_ids` = `ability_type: activated`, nicht mehr Handler-String
  `"resurrection_orb"`; loggt Träger-Name statt Literal `"Overlord"`).
- **B** Zwei-Orb-Bug gefixt: `revive_wargear_target_uid` jetzt **Dict je Wargear** (Key = Request-ID)
  in `commandPhase.py` + `unitCard.py` + `game_state.py`.
- **C** Orb-YAML `max_uses: 1` → `once_per_battle: true`; Renderer liest das Flag.
- **D** INV-4b-Allowlist-Eintrag `commandPhase.py {orb,overlord,phaeron,resurrection}` **entfernt**
  (Ledger geschrumpft) → Cluster 3 (`orb/overlord/resurrection`) **und** `phaeron` erledigt.
- **E** PHAERON-Literal generalisiert: neues `extra_uses`-Feld auf `Ability` + `bonus_uses_for(unit)`;
  +1-Nutzung kommt jetzt aus den 3 MWBD-YAML-Einträgen (9E-Regel erhalten, kein src-Literal).
- **Step 4 (heal_nearby_unit-Dispatcher) bewusst verworfen** — Orb nutzt manuelle
  `wound_adjustment_buttons` am Tisch (kein Engine-Heal) → Dispatcher wäre toter Code.
- Erwartete Migration: `test_resurrection_orb_wargear_source` prüft jetzt `once_per_battle` (statt max_uses).

### ▶ Nächste Session = manueller Orb-Check + Plan 021

**Zuerst (offener manueller UI-Check zu Plan 020 — Render-Code nicht test-gedeckt):** Im
`data/rosters/necrons_1500pts_silent_king.yaml` einen **zweiten Orb-Träger (Overlord mit
Resurrection Orb)** ergänzen → damit den Zwei-Orb-State-Fix (B) am Tisch verifizieren (beide Orbs
unabhängig aktivierbar; einer aktiviert ≠ stört den anderen). Weitere Checks: Orb erscheint mit
YAML-Namen; Use→Ziel→Confirm→„Already used".
**Dann Plan 021** (Arkana → `faction_abilities.yaml` + Loader generisch) aus
`docs/audit/plans/README.md`. Reihenfolge: 014✓ 020✓ → **021** → 016 → 018 → 015 → 017.

**Historie verdichtet:** S82 Plan 014 Teil B (UI A/B/C) DONE + manuell verifiziert. S81 3 Retro-
Maßnahmen (M1 Maßnahmen-Entscheid, M2 Planning-Default, M3 ADR-0005 stehende Subagent-Freigabe).
S80 Plan 014 Teil A (`group_wounds` universell). Details → `docs/goals/ziel6.md`.

### Offene Fragen / Retro-Vormerke
- **ADR-0005-Lücke (teil-beantwortet S83):** `freigabe_gate.py` feuerte sauber im **Opus-Hauptkontext**
  (Edit blockiert bis `touch .claude/.freigabe`). Offen bleibt nur: feuert es auch im **Subagent**-Kontext?
- **Doku-Drift:** `architecture.md` §session_state — `group_wounds` universell (backlog §4b).
- **INV-4b Restschuld:** noch `dynasty` (movementPhase), `gloom/prism` (psychicPhase → Cluster 5),
  `arkana` (loader → Plan 021), `reanimation`/`protocols` (_common). Ratchet weiter schrumpfen.

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
