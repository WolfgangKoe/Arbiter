STATUS: ANSWERED
Freigegeben S135; umgesetzt: Aufgaben 1–5 + 10 (Paket 4a/4b/4c, B6, B1-Probe);
Aufgaben 6–9 (Welle 2, Dakka) → S136, s. `next_session.md`.

# S135 — Planning-Entwurf

## Checkbox-Sync (vor Einplanung geprüft)

Abgleich `next_session.md`/`ziel7.md`/`backlog.md` gegen `git log --oneline -30` und
gezielte `grep`-Belege — **keine stale Checkboxen gefunden**, alle als offen gelisteten
Punkte sind tatsächlich noch nicht committet:

- `before_battle` fehlt weiterhin in `PHASES` (`grep -rn "before_battle" src/` → 0 Treffer;
  `game_state.py:40-49` kennt nur Setup…Morale) → Task 8 korrekt als offen geführt.
- `_datasheet_stat_row()` (`gameActionsArea.py:52-64`) führt `++`/`OC` weiterhin als letzte
  zwei Spalten → B4-Sofortteil korrekt als offen geführt (Zeilen 62-63 stimmen mit dem
  Backlog-Verweis überein).
- `render_inline_command_reroll` hat aktuell 3 fachliche Aufrufstellen (Damage in
  `_common.py:1274`, Psychic-Manifest + Deny in `psychicPhase.py:303/336/362/515`) plus
  bereits migriertes Charge (`chargephase.py:114`, Paket 2/S132 — nicht Teil des Rests) →
  „3 Wurf-Arten"-Aussage in `next_session.md` ist korrekt, kein Drift.
- Paket 1/2/3a-Häkchen in `backlog.md` (GO-Karten-Baustein, Command-Re-Roll Advance/Charge,
  reaktive Boxen migriert) decken sich mit den Commits `e3d7753`/`0a94adb`/`ee4b16e`/`bbca856` —
  korrekt als ✅ geführt. Paket 3b (`before_battle`-Liste) ist weiterhin 🟢 (offen), deckt sich
  mit dem fehlenden Code-Beleg oben.

## Planning — 2026-07-10

**Priorität:** P1   **Scope:** Paket 4 (reaktive GO-Anker), Welle-2-Rest, B1-Diagnose,
offene Stakeholder-Entscheidungen aus `S134_offene_punkte.md`

| Aufgabe | Effort | Token-Schätzung | Modus | Subagent(en) + Tier | Scope-Zeile / Dateien |
|---|---|---|---|---|---|
| **1. Offene Entscheidungen vorlegen** (B2 Struktur+Scope-Frage; B4-Refinement Punkte 1–3 Anmutung/Waffen-Tabelle/Wargear-Chip; B7 Kopfbereich+Hinweis-Konvention; B7/B9-Schnitt; B10 CLAUDE.md-Formulierungen) | XS | ~3k | Konsens | Koordinator direkt (kein Subagent — Optionen bereits in `S134_offene_punkte.md` ausformuliert) | `docs/handoff/S134_offene_punkte.md` |
| **2. Paket 4a — Hit-/Wound-Anker** (Kompaktkarte am Wurfbereich in `_common.py`, löst 2 der 14 nicht aktivierbaren `phase_reactive`-GOs) | M | ~30k | Gate | Executor + Sonnet | Combat-/Schadens-Mechanik + Phase-UI-Zeilen: `src/uiLayout/_common.py`, `src/gameMechanic/attack_math.py`, `docs/spec/design_system.md` §6.2 |
| **3. Paket 4b — Save-/Damage-Anker** + Ablösung der 3 `render_inline_command_reroll`-Call-Sites (Damage/Psychic/Deny) | M | ~30k | Gate | Executor + Sonnet | `src/uiLayout/_common.py`, `src/gameMechanic/psychicPhase.py`, `docs/spec/design_system.md` §6.2 |
| **4. Paket 4c — Anzahl-Attacken-Fenster** + R-CMD-12-Restabgleich (9 Wurf-Arten) + §6.2-Schuld-Tabelle abbauen + `go_klassifikation.md`-Nachzug; fehlende Ereignis-Fenster (`on_target`/`on_set_up`/generisches `on_destroy`) bewerten, ggf. Folge-Split abspalten statt in M zu pressen | S–M | ~25k | Gate | Executor + Sonnet | `src/uiLayout/_common.py`, `src/gameMechanic/ability_engine.py`, `docs/reference/go_klassifikation.md`, `docs/spec/design_system.md` §6.2 |
| **5. B1 Scroll-Sprung — Probe-Variante ohne Key-Rewrite** (H1 Fokus-Autoscroll vs. H2 DOM-Remount); danach Koordinator gibt Stakeholder EXAKTE Browser-Test-Ansage („App neu laden → Setup-Phase → einen Command-Protocol-Slot ändern → springt der Screen noch? Ja/Nein") — **kein Fix vor Befund** | XS | ~8k | Gate (Probe) → Konsens (Fix danach) | Executor + Sonnet | `src/uiLayout/gameActionsArea.py::_render_round_choice_assignment` |
| **6. Welle 2 — Task 8** `before_battle` in `PHASES` + ArmySetup-Liste (GO-Zählung nach BA-Bereinigung neu verifizieren) | S | ~15k | Gate | Executor + Sonnet | `src/gameMechanic/game_state.py` (PHASES), `src/gameMechanic/phase_runner.py`, `src/uiLayout/armyCard.py` (ArmySetup-Rendering) |
| **7. Welle 2 — B8** redundanten Statusbereich je Phase entfernen (Screenshot `…21-36-36.png`) | XS | ~4k | Gate | Executor + Haiku (mechanische Entfernung + Render-Test) | `src/uiLayout/gameActionsArea.py`, `docs/spec/ui_layout.md` |
| **8. Welle 2 — B4-Sofortteil** `++`/`OC`-Spalten aus `_datasheet_stat_row()` entfernen | XS | ~4k | Gate | Executor + Haiku (reine Entfernung, Zeilen 62-63 bekannt) | `src/uiLayout/gameActionsArea.py:52-64` |
| **9. Welle 2 — Task 7 Dakka** (`docs/audit/plans/S133_plan.md`) — NACH Schritt 2+3 (4a/4b), wegen `_common.py`-Kollision | S | ~15k | Gate | Executor + Sonnet | `data/wh40k_9e/orks/weapons.yaml`, `src/uiLayout/_common.py`, `docs/audit/plans/S133_plan.md` |
| **10. B6 Kurz-Mockup + Freigabe** (Faction-Ability-Wahl kompakt in Spieler-Spalten, Option B — Funktionalität muss erhalten bleiben, Stakeholder-Auflage) | S | ~10k | Gate | Executor + Sonnet | `src/uiLayout/armyCard.py`, `docs/spec/faction_abilities.md` |

**Nächster Schritt:** Schritt 1 (Entscheidungs-Vorlage) im Chat mit dem Stakeholder klären,
danach Schritt 2 (Paket 4a) als erster Executor-Auftrag starten.

**Offene Entscheidungen (aus `S134_offene_punkte.md`, noch unbeantwortet):**
- B2: Struktur des Setup-Screens (Option A/B/C, Empfehlung C) + Scope-Frage
  Faction-Ability-Wahl im B2-Konzept oder unabhängig (Empfehlung: unabhängig, B6 läuft bereits separat).
- B4-Refinement Punkt 1: Anmutung (App-Design-System vs. Wahapedia-Stil, Empfehlung App-Design-System).
- B4-Refinement Punkt 2: Waffen-Tabelle-Spalten (Empfehlung: nur 9E-Standard-Spalten, keine berechneten Werte).
- B4-Refinement Punkt 3: Wargear-/Relic-Auswahl als Chip sichtbar (Empfehlung: ja).
- B7 Punkt 1: welcher Kopfbereich bleibt als Phasen-Anker (Empfehlung: B, bis B9-Stepper kommt).
- B7 Punkt 2: Hinweis-Konvention (Empfehlung: eigener Design-System-Baustein, Option B).
- B7/B9 Punkt 4: beide als EIN Konzept-Handoff bündeln (Empfehlung: ja).
- B10: beide CLAUDE.md-Formulierungsvorschläge (Kommentar-Konvention + Artefakt-Landkarten-Zeile) — freigabepflichtig.

(Bereits beantwortet, nicht mehr offen: B4 Punkt 4 „nur Setup", B6 „Option B + Funktionalität
erhalten", B9 Punkt 3 „C als Zwischenlösung, vertikale Darstellung bevorzugt".)
