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

## Aktueller Stand (nach S81, 2026-06-21)

**S81 (Branch `feature/014-defender-loss-allocation`) — 3 Retro-Maßnahmen (Prozess) DONE:**
Doku-/Memory-Arbeit, keine src-Änderung; Doku-/Architektur-Gates grün (16 passed).
- **M1 — Maßnahmen-Entscheid:** Event 5 bekommt Schritt „Maßnahmen-Entscheid" (Review & Retro
  getrennt, Retro endet mit nummerierter Liste → Stakeholder wählt → Abschluss schreibt nur
  Freigegebenes). `operating_model.md` E5 · `CLAUDE.md` Standard-Prompts.
- **M2 — Planning-Default:** „start next session" ⇒ Planning vorlegen (Prioritäten + Token-
  Schätzung), auf Freigabe warten; Shortcut „Plan ist freigegeben" bleibt. `operating_model.md` E1.
- **M3 — Stehende Subagent-Freigabe (ADR-0005):** Subagenten ohne Einzel-Freigabe selbst
  starten; Edit-Pflicht hängt am *Effekt*, nicht am Werkzeug. **Offene Lücke** (ADR-Review-Termin):
  feuert `freigabe_gate.py` auch im Subagent-Kontext? Sonst Regel „Subagent liefert nur Entwürfe".

## Aktueller Stand (nach S80, 2026-06-21)

**S80 (Branch `feature/014-defender-loss-allocation`) — Plan 014 Teil A (Logik) DONE:**
Vollsuite 1080 grün, Cov **92,85 %**, Gate 92 %, ruff/black/isort/Architektur grün.
- **Step 1 — `group_wounds` universell:** `game_state._unit_state` befüllt den Per-Gruppen-
  HP-Pool jetzt für **jede** Einheit mit `model_groups` (nicht mehr nur bei gemischten
  Wundenwerten). `current_wounds` homogener Einheiten **unverändert** (Summe identisch);
  neues State-Feld `damage_active_group_id` (default None). Szarekh/Menhir-Regression grün.
- **Step 2 — Lock + gerichteter Schaden (`unit_mutations`):** `select_damage_target_group()`,
  `get_locked_group()` (`pool % wval != 0` ⇒ angeschlagenes Frontmodell), `_group_front_hp`,
  `_apply_directed_group_damage`. `apply_damage`: **Default-Pfad byte-identisch** (kein
  `damage_active_group_id` ⇒ alter Priority-Spill) — nur bei gewählter Gruppe gerichtet +
  Lock-Check (falsche Gruppe → ValueError); `mortal=True` ignoriert Lock (Overflow). 12 neue
  Tests (Schicht 1 + 1b). **Designnote:** `get_locked_group` nahm `unit` als Param (Plan-
  Pseudocode ohne — `group_wound_value` braucht die Unit).
- **▶ Teil B offen (nächste Session):** Step 3 UI Zustand A/B/C in `_common.py` +
  Schicht-2-Acceptance (`test_group_flow.py`) + manuelle Nobz/Szarekh-Verifikation.
- **Parallel erledigt:** LinkedIn-Grundlagendatei `Refinement/operating_model_luhmann_wilber_graves.md`
  (Luhmann/Wilber/Graves + Gates/Hooks); 2 Subagenten-Befunde in `docs/inbox/` (s. u.).

### S80-Subagenten-Befunde (Backlog, NICHT umgesetzt)
- **Silent-King Zielaufteilung — REGEL GEKLÄRT:** Core Rules: „If a model has more than one
  ranged weapon, it can split the weapons between different enemy units." → Waffen-Split auf
  **verschiedene** Ziele ist erlaubt; alle Attacken **einer** Waffe auf dieselbe Einheit.
  **Aktuelle App-Beschränkung (1 Ziel) ist regelwidrig** → UI auf „Ziel pro Waffe" + Staff-of-
  Stars-Sperre ≤8 W beachten. Detail: `docs/inbox/finding-silent-king-target-split.md`.
- **Dice-Display 7+/Magnitude — Gap-Analyse:** `threshold_header_html` ohne threshold=7-Logik;
  Magnitude `←N` landet bei shift>1 rechts neben dem Grenz-Slot statt darin. Optionen +
  Regressionsfläche: `docs/inbox/finding-dice-display-7plus.md` (Design-Entscheid offen → Opus).

**S77–S79 (Historie, verdichtet):** Plan 022 Dice Display Rework DONE (`1ce131a`..`ecad9bf`);
S79 Renderer ins Sicherheitsnetz (`dice_compose.py`-Naht 100 %, HI-Crash-Fix, Badge-Fix,
**INV-6** + Ratchet `fail_under`→92). Alle S79-UI-Findings (Silent-King-Ziel, 7+-Grenze,
Magnitude-Position, Invuln-Badge, Befund B/C) liegen im **Backlog** (`backlog.md` §UI). Noch
nicht verdrahtet: `reroll_marker_row_html`/`always_fail_marker_row_html` (warten auf Produzent).

**INV-4b/INV-4 Restschuld (nach S77):**
- **LEGIT:** `rosz_importer._FACTION_MAP`, `typing.Protocol`
- **Schema-Urteil (Konsens nötig):** `reanimationProtocols`/`reanimation`,
  `arkana`, Items `orb`/`overlord`/`phaeron`/`gloom`/`prism`/`dynasty`,
  Default-Roster-Hardcode (`game_state.py`), `faction_dir`-Default `"necrons"` in `loader.py`
  (`dakka`/`klaw`/`tesla` in S77 erledigt)

### ▶ Nächste Session = Plan 014 **Teil B** (UI Zustand A/B/C)

**Reihenfolge (neu 2026-06-21):** 023/022 (DONE) → 014 **Teil A DONE** → 014 Teil B → 020 →
021 → 016 → 018 → 015 → 017
**014 Teil B:** Step 3 aus `docs/audit/plans/014-p17-defender-loss-allocation.md` — in
`_common.py:_render_damage_block()` Subgruppen-Auswahl VOR dem Apply-Button (nur bei
`len(aktive Gruppen) > 1`): Zustand A (freie Wahl, `select_damage_target_group`), B (Lock auf
`get_locked_group()`), C (Zerstörungs-/Fähigkeitsverlust-Warnung). Dann Schicht-2-Tests
(`test_group_flow.py`: A→B→C-Transition Nobz) + manuelle Verifikation (Nobz 3 Zustände,
Warriors ohne UI, Szarekh-Pools). Die Logik (`damage_active_group_id`, Lock, gerichteter
Schaden) steht bereits aus Teil A — Teil B verdrahtet nur das Render-UI.

### Offene Fragen / Retro-Vormerke
- **Output ↔ cache_read als Tempo-Indikator:** Zielwert-Feintuning `token_report.py`-Legende.

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
