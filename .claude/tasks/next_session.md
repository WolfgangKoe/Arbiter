# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → ziel6.md; Backlog → backlog.md. -->
<!-- Referenzwissen NICHT hier: Architektur-Muster → architecture.md, Regel-Gotchas →
     rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start lesen:** `CLAUDE.md` (Freigabe-Pflicht, bei Unklarheit zuerst fragen)
  + `docs/goals/ziel6.md` (Aufgaben/Historie) + `docs/goals/backlog.md` (Backlog).
  Einstieg: `LEITSTAND.md`; Rollen/Tier/Events/Modi: `docs/governance/operating_model.md`.
- **Ende:** Checkboxen in `ziel6.md` + Historien-Zeile; **diese Datei** aktualisieren
  (ZUERST lesen, dann ergänzen — nie blind überschreiben).
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70**
  kürzen, nicht knapp drunter — Erledigtes → `backlog.md`/`ziel6.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Subagent/Skill ohne Freigabe; rote vorher-grüne
  Tests = STOP + fragen.** Details: `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter für WH40k 9E, Streamlit (Python). Start:
`streamlit run src/app.py` (Port 8501). Branch `dev` (Arbeit), `main` (nur per PR).

---

## Aktueller Stand (nach S78, 2026-06-21)

**S78 (Branch `feature/022-dice-display-rework`):** Befund A + CET, 1029 grün, Cov 92.35 %.
- **Pfeil-Magnitude (Befund A, Spec §2.1):** `←N`/`+N→` am Pfeilkopf bzw. (Shift 1) im
  Boundary-Gap; Label in Modifier-Farbe (`_glyph_span`/`glyph_color`). 7 neue Tests.
  Visuell bestätigt (`←4` rot, `+1→` grün). `arrow`↔„Tachyon Arrow"-INV-4b-Kollision per
  Rename gelöst (Guard nicht aufgeweicht).
- **CET-Zeiten:** `token_report.py` zeigt Zeiten in `Europe/Berlin` (DST-korrekt) statt UTC.
- **Befund B/C** (HIT-Debuff-Geometrie spreizt nicht, Slot-1-Invariante bei HIT-Buff) →
  eigener Plan, Backlog.

**🔴 Neue Bugs (S78, UI-Verifikation — NICHT umgesetzt, nur notiert):**
1. **Heroic Intervention crasht** (Ork-YAML): Button → Ork-Armeeliste verschwand komplett,
   App handlungsunfähig. Tests fehlen (Muster wie FightPhase-Crash). → Bugfix-Plan.
2. **Badge „AP-4 -4"**: Wert doppelt (Label „AP-4" + angehängtes „-4"). → entdoppeln + Test.
3. **Buff-Badge nicht grün** (Light Cover): Badge-Chip nutzt `right_color`=grau bei Buffs;
   Farb-Test fehlt; offene Perspektiv-Frage (`color_hint` für SAVE-Badge nicht ausgewertet).
4. **Invuln-Badge chaotisch** (3 Teile) → eine Badge „Invuln 4+" (mit Plan 017 lösen).
Alle 4 im Backlog. Vor Plan 014 entscheiden, welche Bugs Vorrang haben.

**S77 (Plan 022 DONE — committet, Branch `feature/022-dice-display-rework`):**
Dice Display Rework, 5 Commits (`1ce131a`..`ecad9bf`). 1022 grün, Cov 92.35 %.
- Step 1: Arrow-Direction-Fix (`rightward = value > 0`) + 2 Regressionstests.
- Step 2: Badge-Truncate (Ellipsis statt Overflow in Slot 1).
- Step 3: `_modifier_color()` — `color_hint` ('buff'|'debuff') schlägt Vorzeichen
  (für perspektivabhängige Effekte wie Quantum Shield), rückwärtskompatibel.
- Step 4: Guard-Tests (Slot-1-Invariante, Buff-gegen-1, Debuff>6) + neue Anzeige-
  Bausteine `reroll_marker_row_html`/`always_fail_marker_row_html` — **noch nicht
  verdrahtet** (warten auf Produzent: Quantum Shield, `reroll_hit_1`).
- Step 5 (INV-4b Cluster 1): `_detect_weapon_special` datengetrieben via `effect.type`
  (`extra_hits`/`alternating_fire`/`hit_roll_penalty`). YAML normalisiert: 9 Dakka-
  Profile + Beast Snagga klaw. Ledger 19→16 Tokens; `attack_math.py`+`dice_html.py`
  auf null gepinnt. Plan nannte fälschlich `ability_engine.py` für `color_hint` —
  echter Ort ist Konsument `dice_html.py` (Modifier-Dicts kommen aus combat/_common).

**INV-4b/INV-4 Restschuld (nach S77):**
- **LEGIT:** `rosz_importer._FACTION_MAP`, `typing.Protocol`
- **Schema-Urteil (Konsens nötig):** `reanimationProtocols`/`reanimation`,
  `arkana`, Items `orb`/`overlord`/`phaeron`/`gloom`/`prism`/`dynasty`,
  Default-Roster-Hardcode (`game_state.py`), `faction_dir`-Default `"necrons"` in `loader.py`
  (`dakka`/`klaw`/`tesla` in S77 erledigt)

### ▶ Nächste Session = Plan 014 (Defender Loss Allocation)

**Reihenfolge (neu 2026-06-21):** 023/022 (DONE) → 014 → 020 → 021 → 016 → 018 → 015 → 017
**014:** Refinement 2026-06-21 **neu geplant** (alte Fassung hatte
`group_wounds`-Namenskollision + Scope-Selbstwiderspruch). Neue Richtung: `group_wounds`
universell für ALLE Gruppen-Einheiten → ein Schadenspfad. **Risk HIGH** (Regressionsfläche
Heal-/Damage-Pfad) — Plan: `docs/audit/plans/014-p17-defender-loss-allocation.md`.
Beide Pläne: vor Start Freigabe einholen.

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
