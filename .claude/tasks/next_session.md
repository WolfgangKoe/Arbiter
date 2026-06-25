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

## Aktueller Stand (nach S99, 2026-06-25)

**S99 — Plan 025 Step 3 (Vengeful Stars) Code+Tests FERTIG + committed.** D1 `ap_on_unmod_wound_6`
(**ranged, B**) = nur YAML-Tausch (Wiring war phasen-generisch) → `[AP-1]`-Zeile im Schuss-WOUND-Block.
D2 `ignore_cover_half_range` (**B/Hybrid**) über neue Engine-Fn `get_active_round_choice_ignores_cover_half_range`
+ reine Label-Fn `light_cover_label` → grüne `:green-badge`-Inline-Anzeige an der Light-Cover-Checkbox.
Toter `ap_bonus`-Pfad ersetzt. 1150 grün / 93,16 %. 5 Tests migriert (Sicherheitsnetz, Stakeholder-ok).

**UI-Verifikation S99 (Stakeholder):** Würfel + Effekt D1 **und** D2 korrekt — **ABER Badge-Label-Bug** (s. u.).

### ⚠️ Bug: Falsches Protokoll-Label in Würfel-Badges (Schuss-WOUND + Light-Cover) — Fix als nächstes
**Symptome:** `[AP-1]`-Trigger-Zeile und Light-Cover-Badge zeigen „Eternal Guardian" statt „Vengeful Stars",
wenn Vengeful Stars das **6./Extra-Protokoll** ist. **Ursache (Subagent S99, bestätigt):**
`_round_choice_short_label` (`_common.py:429`) liest immer den `active`-Slot (rundenzugewiesen). Effect-Dicts
aus `_active_directive_effects` tragen **keine Protokoll-Identität** (Loader `loader.py:500-501` setzt nur
{type,value,phase}). Bug tritt **nur** beim Extra-Protokoll auf; kommt der Effekt vom rundenzugewiesenen, stimmt das Label.
**Bug-Stellen:** `_common.py:916` (AP-Badge) + `_common.py:1052-1053` (Light-Cover-Badge).
**Fix-Skizze:** (1) `_active_directive_effects` reichert je Effect-Dict `"_protocol_id"` engine-seitig an;
(2) neuer Helper `get_short_label_for_effect_type(player, effect_type) -> str | None` (sucht Protokoll per ID,
gibt Kurznamen); (3) beide `_common.py`-Aufrufe umstellen; (4) Test: Vengeful als Extra → Label „Vengeful Stars".
**Scope:** 3 Dateien, additiv, kein Generic-Verstoß. ~25–35k Tokens.

**S98 (Step 2, Hungry Void):** D1 AP-on-6 melee (B) + D2 `strength_if_charged` melee (A, S blau wie WAAAGH).
Design-Korrektur: Direktiv-Effekte ins **Dice-UI-Vokabular** (kein Caption-Block; Step 2b verworfen). Detail → git.

**⚠️ Eternal-Guardian-Befund (für Step 4):** armyCard-Anzeige falsch + **vermutlich fachlich falsch** (backlog §4b):
YAML hat noch **erfundene** Effekte (save +1 / `reroll_save_1`) statt 9E-D1 (Light Cover wenn nicht bewegt) /
D2 (Hold Steady·Set to Defend). Step 4 behebt beides (Daten **und** armyCard-Render).

### Nächster Schritt
**Zuerst: Badge-Label-Bug fixen** (s. o. — kleiner, klarer Fix, eigener Freigabe-Punkt). **Danach Plan 025
Step 4 = Eternal Guardian** (Daten **und** armyCard-Render; vor Start armyCard-Direktiv-Anzeige genau ansehen).
Reihenfolge gesamt: Label-Bug → 025(Step 4→5→6, je mit Anzeige) → 016(Rest) → 018 → 015 → 017.

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
   (Eternal-Guardian-Save / Undying-Legions-RP / Living-Metal-S waren S93 ✅.)

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
