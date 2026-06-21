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

## Aktueller Stand (nach S86, 2026-06-22)

**S86 (Branch `feature/024-arkana-protocol-effect-modeling`) — Plan 024 Steps 1–4 + Drift-Cleanup:**
- **Plan 024 Steps 1–4 DONE** (4 Commits, +13 Unit-Tests, 1109 grün/93 %, INV-4b grün): Direktiv-Wiring
  in `ability_engine.py` — `strength/ap/move/leadership_modifier` in `_WIRED_EFFECT_TYPES`; neue
  `get_active_round_choice_rerolls` (Eternal Guardian S / Conquering Tyrant S); `charge_after_advance_allowed`
  ehrt jetzt die `advance_and_charge`-Direktive (Sudden Storm S); neue `get_active_rp_modifiers`
  (Undying Legions P/S). Shared Helfer `_active_directive_effect`/`_directive_phase_excluded` extrahiert.
  **⚠️ Manuelle UI-Verifikation offen** (Render): S+1/AP/Move/Reroll/RP-Anzeigen — Engine liefert die Werte,
  Display-Verdrahtung ist nicht von Tests gedeckt.
- **Doku-Drift bereinigt** (Sonnet-Sweep, 5 Befunde): 019/023 DONE nachgetragen, 024 IN PROGRESS, #PSI/dice/orb-
  Status korrigiert. Commit `2a0b195`.
- **Deutsch-Präferenz** als Memory festgehalten (`feedback-language-german`).

### ▶ Nächste Session
1. **Plan 024 Steps 5–7 — frischer Start.** Step 5 = Failsafe-Overcharger-Dispatch-Pilot (verifiziert die
   `buff_stat`-Annahme gegen den echten Handler — bricht sie, bleibt das Arkanum `descriptive`, STOP).
   Step 6 = strukturiertes Schema + Punktkosten für die übrigen 11 Arkana. **Vorarbeit liegt vor:**
   `docs/audit/plans/024-arkana-research-digest.md` (Sonnet, Schema je Arkanum + Begründungen).
   **✅ ENTSCHEIDEN (S86):** **alle 12** Punktkosten in Step 6 auf die Wahapedia-Werte korrigieren (+5-Offset
   aus Plan-021-Migration), nicht nur die 3 im Plan. Werte-Tabelle im Digest.
   **PFLICHT-TESTNETZ pro Step:** (a) Unit; (b) Acceptance/State; (c) INV-4b-Gate; (d) manuelle UI; (e) Doku.
2. **Manuelle UI-Verifikationen einsammeln** (Render, von Tests nicht gedeckt): Step-1–4-Anzeigen (S+1/AP/
   Move/Reroll/RP); Orb-Zwei-Orb-Fix (necrons_1500pts_silent_king); 014 Nobz Zustand A/B/C; 022 „Power Klaw".
3. Danach Queue: 016 → 018 → 015 → 017.

**Drift-Lehre:** Drift-Check IMMER vor Effort-Schätzung (S84/S85 hing Status der Realität hinterher). S86
proaktiv per Sonnet-Sweep abgefangen — Muster beibehalten.

**Historie verdichtet:** S85 Orb-Zwei-Orb-Key-Fix + Plan 024 angelegt + 022/014-Drift. S84 Plan 021
(Arkana-Migration). S83 Plan 020. Details → `docs/goals/ziel6.md`.

### Offene Fragen / Retro-Vormerke
- **Follow-up ADR-0006 (S86):** `CLAUDE.md` (Token-Disziplin/Subagent-Muster) um einen Verweis auf
  [ADR-0006](../../docs/governance/decisions/0006-subagent-grossausgaben-als-datei.md) ergänzen —
  Subagent-Großausgaben als Datei zurückgeben (Verweis statt Volltext) + Permanent/Temporär-Deklaration.
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
