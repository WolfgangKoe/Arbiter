# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planning vorlegen** (Prioritäten + Token-Schätzung), erst nach
  Freigabe los; Shortcut „Plan ist freigegeben" = direkt los. **Lesen:** `CLAUDE.md` +
  `docs/goals/ziel6.md` + `docs/goals/backlog.md`. Einstieg `LEITSTAND.md`; Rollen/Tier/Modi:
  `docs/governance/operating_model.md`.
- **Ende:** Review → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) → Abschluss: **diese
  Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. ziel6-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).

---

## Aktueller Stand (nach S100, 2026-06-26)

**S100 — Badge-Label-Bug FIXED + committed (UI-verifiziert).** `_active_directive_effects` /
`_extra_directive_effects` taggen jedes Effect-Dict mit `_source_id` (Kopie statt Mutation des
gecachten Dicts); neuer Helper `get_short_label_for_effect_type(player, effect_type)` löst das Label
über `_source_id` auf (gleiche Kurzname-Quelle `short_round_choice_label`). Beide `_common.py`-Badges
(AP Z. 918, Light-Cover Z. 1060) nutzen ihn mit Fallback. 1154 grün / 93,20 %; +4 Regressionstests.
INV-4b leicht reduziert (Rename generisch). Sonnet-Subagent (65 % Token-Anteil), Opus-reviewt.

**S99 — Plan 025 Step 3 (Vengeful Stars) Code+Tests FERTIG + committed.** D1 `ap_on_unmod_wound_6`
(**ranged, B**) → `[AP-1]`-Zeile im Schuss-WOUND-Block. D2 `ignore_cover_half_range` (**B/Hybrid**) über
`get_active_round_choice_ignores_cover_half_range` + `light_cover_label` → grüne Badge an Light-Cover-Checkbox.

**S98 (Step 2, Hungry Void):** D1 AP-on-6 melee (B) + D2 `strength_if_charged` melee (A, S blau wie WAAAGH).
Design-Korrektur: Direktiv-Effekte ins **Dice-UI-Vokabular** (kein Caption-Block; Step 2b verworfen). Detail → git.

**⚠️ Eternal-Guardian-Befund (für Step 4):** armyCard-Anzeige falsch + **vermutlich fachlich falsch** (backlog §4b):
YAML hat noch **erfundene** Effekte (save +1 / `reroll_save_1`) statt 9E-D1 (Light Cover wenn nicht bewegt) /
D2 (Hold Steady·Set to Defend). Step 4 behebt beides (Daten **und** armyCard-Render).

### Nächster Schritt
**Plan 025 Step 4 = Eternal Guardian** (Daten **und** armyCard-Render; vor Start armyCard-Direktiv-Anzeige
genau ansehen — YAML hat noch erfundene Effekte save +1 / `reroll_save_1` statt 9E-D1 Light-Cover-wenn-nicht-
bewegt / D2 Hold Steady·Set to Defend). D1 `light_cover_if_stationary` (Klasse A, SAVE-Block) + D2 B-Hinweis.
Reihenfolge gesamt: 025(Step 4→5→6, je mit Anzeige) → 016(Rest) → 018 → 015 → 017.

### ⚠️ Carry-over (offen)
0. **Kontext-Engineering / Regel-Kuratierung (eigene Session, Maßnahme C).** Quelle:
   `docs/reference/context-engineering-slides.md`. (a) SessionStart-Regel-Injektion (relevante Regeln je
   Ziel verbatim in den Kontext) — behebt Tiering-/Regel-Lücken. (b) Subagent-Ergebnis → `docs/handoff/`-
   Datei statt in Orchestrator-Kontext. (c) Handoff-Lebenszyklus (lesen→arbeiten→auslagern→löschen).
   (d) governance-Doc `context_engineering.md`; `docs/handoff/context-audit-S91.md` verarbeiten + löschen.
   **S95-Beleg (warum Kern):** Die Regelprüfung griff nur, weil sie *expliziter Plan-Schritt* war — nicht
   aus zuverlässiger Gewohnheit. Assurance braucht **Injektion oder Gate**, nicht „zufällig im Kontext".
1. **Plan 025** = aktive Hauptlinie (s. o.). Bug 3 (Zweitspieler-Direktiv-Wahl, armyCard.py:296/307) +
   INV-4b-Restschuld (`dynasty`/`gloom`/`prism`/`necrons`-Defaults) laufen nebenher, je eigene Freigabe.
2. **Manuelle UI-Verifikation (offen, PFLICHT, Render-Code):** (a) S91 Mirror-Protokoll — Necron-vs-Necron
   Befehlsphase: Spieler-1-Wahl lässt Spieler-2-Karte unverändert. (b) Bug 5: Runde-2-Fernkampf-Zielwahl.
   (Eternal-Guardian-Save / Undying-Legions-RP / Living-Metal-S waren S93 ✅; **Badge-Label Vengeful Stars
   als 6./Extra-Protokoll war S100 ✅** — AP- und Light-Cover-Badge zeigen korrekt „Vengeful Stars".)

### Offene Fragen / Vormerke
- **Design-System-Crew (eigene Session):** Subagenten-Gespann Designsystem + Buff-/Direktiv-Hinweis-
  Komponente (RP-Hint deutlicher, konsistent mit MWBD/SAVE). Greift, sobald 025 die Effekte festlegt.
- **S95-Prozess-Vormerk (nicht entschieden):** Regelkonformität evtl. schon **beim YAML-Modellieren**
  prüfen, nicht erst bei Anzeige — als DoD-#1-Ergänzung erwägen.
- **Lehren:** „Engine oder Verdrahtung?" → erst prüfen, welche State-Klassen der Resolver liest (S93);
  Repro-zuerst (S92); Branch-Check (aktiv = `feature/016`).
- **Kleine Doku-Vormerke:** backlog #2 / ziel6 6e um Bug-3-Step + „Reset kampfrunden-weit" (S90);
  Freigabe-Gate Re-Arm nur bei echtem SessionStart prüfen; `CLAUDE.md` um ADR-0006-Verweis ergänzen.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 90 %, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report:** `python tools/token_report.py --write`. **History:** `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
