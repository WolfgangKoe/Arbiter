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

## Aktueller Stand (nach S84, 2026-06-21)

**S84 (Branch `feature/014-defender-loss-allocation`) — Plan 021 (Teil) + Orb-Bug-Fix:**
Vollsuite **1092 grün**, Cov **92,96 %**, alle Gates grün.
- **Plan 021 (NUR Daten-Migration + Loader, NICHT „Arkana fertig"):** 12 Arkana →
  `faction_abilities.yaml` (mit `power_delta` **und** `cost_pts`); `load_faction_abilities`
  überspringt `descriptive`; `load_points` liest `cost_pts` generisch (`_add_faction_ability_costs`);
  `points.yaml`-`arkana:`-Sektion entfernt; INV-4b-Literal `"arkana"` aus `loader.py` raus.
- **⚠️ Arkana-Effekte NICHT modelliert** — `ability_type: descriptive` ist ein **Stopgap**
  („nicht engine-dispatchbar"). Die Regeltexte enthalten echte trigger/conditions/effect → Plan 024.
- **Orb-Bug gefixt:** zwei Träger **derselben** Unit-Id (zwei Overlords m. Res-Orb) teilten den
  once-per-battle-State, weil `wargear_used`/`request_id` nur nach `wargear_id` geschlüsselt waren.
  Fix: `_wargear_state_key(bearer_uid, wargear_id)` in `commandPhase.py` → State je Träger-Instanz;
  +Regressionstest `test_same_wargear_two_instances_get_distinct_state_keys`.

### ▶ Nächste Session
1. **Manueller Orb-Tisch-Re-Check** (Render-Code, nicht test-gedeckt): Roster
   `necrons_1500pts_silent_king.yaml` hat **zwei Overlord-Orbs** — prüfen, dass Aktivierung #1
   den Orb von #2 jetzt **nicht mehr** sperrt (Fix verifizieren).
2. **Plan 024 anlegen + umsetzen — „Arkana + Protokoll: Effekt-Modellierung & Bedingungssichtbarkeit":**
   Arkana `descriptive` → echte `trigger`/`conditions`/`effect` (engine-dispatchbar), **gemeinsam**
   mit den fehlenden Protokoll-Direktiven-Bedingungen (Backlog #2: 9/12 Direktiv-Effekte unverdrahtet,
   Bedingungen im UI unsichtbar). Das ist das **eigentliche Ziel** hinter Plan 021.
3. Danach Queue: 016 → 018 → 015 → 017.

**Drift-Lehre S84:** Plan 021 nahm an `load_faction_abilities` existiere nicht — existierte aber
(STOP-Bedingung). Künftig Drift-Check **vor** der Token-/Effort-Schätzung gewichten; Pläne als
„Stand kann veraltet sein" lesen.

**Historie verdichtet:** S83 Plan 020 (generic activated wargear). S82 Plan 014 Teil B (UI A/B/C).
S81 3 Retro-Maßnahmen. Details → `docs/goals/ziel6.md`.

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
