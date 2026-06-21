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

## Aktueller Stand (nach S82, 2026-06-21)

**S82 (Branch `feature/014-defender-loss-allocation`) — Plan 014 Teil B (UI A/B/C) DONE:**
Vollsuite **1082 grün**, Cov **92,85 %**, Gate 92 %, ruff/black/isort grün.
- **Step 3 UI** in `_common.py`: `_render_subgroup_selector()` (neu) + Verdrahtung in
  `_render_damage_block()`. Nur bei `len(aktive Gruppen) > 1`: **A** freie Radio-Wahl
  (→ `select_damage_target_group` beim Apply), **B** Lock-Warnung auf `get_locked_group()`
  (gerichtetes Ziel erzwungen), **C** „Subgruppe verloren"-Warnung in der Apply-Zusammenfassung
  (über `wiped_groups` im `res_key`-State). Single-Group/legacy → `damage_active_group_id=None`.
- **Schicht 2** (Sonnet-Subagent, ADR-0005): `test_group_flow.py` +2 (A→B→C-Transition +
  Kill-Saw-Zerstörung), 31 grün. Werte: Kill Saw 6 HP, +1→5 (Lock), +2→3 (Release).
- **▶ Manuelle UI-Verifikation NOCH OFFEN** (Render-Code nicht test-gedeckt): Nobz 3 Zustände
  (App), Warriors/homogen ohne Selektor, Szarekh+Menhirs-Pools unverändert. Klick-Schritte:
  `docs/audit/plans/014-...md` Step 4 Schicht 4.
- **Doku-Drift TODO:** `architecture.md` §session_state-Schema — `group_wounds` jetzt universell
  (backlog §4b).

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

**S80 (Historie) — Plan 014 Teil A (Logik) DONE:** `group_wounds` universell (jede Einheit mit
`model_groups`), `damage_active_group_id`, `select_damage_target_group`/`get_locked_group`
(`pool % wval != 0` ⇒ Lock), gerichteter Schaden + Lock-Check; Default-Pfad byte-identisch. 12
Tests (Schicht 1/1b). Subagenten-Befunde (Silent-King-Zielsplit regelwidrig, Dice 7+/Magnitude)
liegen im **Backlog §UI**; LinkedIn-Grundlagendatei `Refinement/operating_model_luhmann_wilber_graves.md`.

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

### ▶ Nächste Session = Plan 020 (nach manueller 014-Verifikation)

**Reihenfolge (2026-06-21):** 023/022 (DONE) → 014 **Teil A+B DONE** → 020 → 021 → 016 → 018 →
015 → 017. **Zuerst** die offene manuelle UI-Verifikation für 014 erledigen (s. S82-Block:
Nobz 3 Zustände, Warriors ohne Selektor, Szarekh-Pools) — Render-Code ist nicht test-gedeckt.
Danach Plan 020 aus `docs/audit/plans/README.md` (Queue/Status) ziehen.

### Offene Fragen / Retro-Vormerke
- **ADR-0005-Lücke testen (S82-Maßnahme):** Einmal verifizieren, ob `freigabe_gate.py` im
  Subagent-Kontext feuert (kleiner Probelauf). Wenn nicht → Regel „Subagent liefert nur Entwürfe".
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
