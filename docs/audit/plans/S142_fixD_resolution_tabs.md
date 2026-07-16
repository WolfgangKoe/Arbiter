# Plan S142-FixD — Resolution-Tabs in die Spieler-Spalten (Cross-Player-Area-Leak)

Status: WARTET AUF FREIGABE (kein Code vor separater Freigabe).
Quelle: `docs/handoff/S141_ui_befunde_group_a.md` Befund 3 (Root-Cause-Analyse, read-only).
Stakeholder-Entscheid: **struktureller Umbau** — Resolution-Inhalte gehören in die
jeweiligen Spieler-Spalten (Wurzelbehandlung), NICHT bloße visuelle Kennzeichnung.
Geplant gegen Branch `feature/016-protocol-rp-effects` (S142).

**Parallel/bereits separat laufend (nicht Scope dieses Plans):**
- `target_name`-Sofortlinderung in `render_reactive_stratagem_box`
  (`src/uiLayout/_common.py:876-889` übergibt kein `target_name` an `render_go_card`)
  — läuft als eigener Kurz-Fix, unabhängig vom Layout-Umbau.
- Datei-Umbenennung snake_case→camelCase in `src/` (`gameState.py`, `unitMutations.py`,
  `diceHtml.py` …). `fightPhase.py`, `shootingPhase.py`, `_common.py` sind NICHT
  betroffen. **Dieser Plan verwendet durchgehend die neuen camelCase-Modulnamen** —
  Executor prüft vor Start per `ls src/gameMechanic/`, ob die Umbenennung schon
  gemergt ist, und passt Import-Pfade entsprechend an.

---

## 1. Ziel

Während der Attacken-Auflösung (Shooting + Fight) erscheinen die Inhalte wieder
**in den festen Spieler-Spalten** (`first_player` links, `second_player` rechts —
Domänen-Constraint, nie an `active`/Angreifer gebunden): Angreifer-Anteile (Attacken,
HIT-/WOUND-Block, Angreifer-Command-Re-Roll) in der Spalte des angreifenden Spielers,
Verteidiger-Anteile (SAVE-Block, Verteidiger-Command-Re-Roll, die drei reaktiven
GO-Anker Hit/Wound/Save, RP-Block) in der Spalte des verteidigenden Spielers.
Damit verschwindet der Leak, dass Verteidiger-GOs (z. B. Whirling Onslaught) auf
einem vollbreiten Panel „über beiden Spielerbereichen" auftauchen.

## 2. Ist-Struktur (wo Angreifer- und Verteidiger-Daten heute gemischt sind)

- `render_attack_resolution(phase_key)` (`src/uiLayout/_common.py:2824-2897`) rendert
  ein **vollbreites Panel**: Header (Angreifer), Reset-Button, dann
  `st.tabs(...)` (Z. 2861) mit **einem Tab pro Waffe×Ziel**; „All done — Continue"
  + `_render_unit_rp` (Z. 2887-2897) ebenfalls vollbreit.
- Beide Phasen rufen es **vor bzw. statt** der Zwei-Spalten-Struktur auf:
  - `src/gameMechanic/fightPhase.py:395-397` — `_render_display` (Z. 558-573,
    Aufruf `render_attack_resolution("fight")` Z. 572) `return`t VOR
    `col1, col2 = st.columns(2)` (Z. 403).
  - `src/gameMechanic/shootingPhase.py:81-83` — `_render_display` (Z. 183-190,
    Aufruf Z. 187) `return`t VOR den Spalten (Z. 106-126).
- Innerhalb eines Tabs mischt `_render_resolution_tab` (`_common.py:1789-~2200`)
  beide Seiten in EINEM Render-Baum:
  - Angreifer: Attacken-Header (Z. 2007-2013), HIT-Block + Inline-Re-Roll
    (Z. 2015-2029), Dense-Cover-Checkbox (Z. 2049-2050), WOUND-Block + Inline-
    Re-Roll (Z. 2054-2071), DAMAGE-Block (`_render_damage_block`, Angreifer zahlt).
  - Verteidiger: reaktive GO-Anker `render_reactive_stratagem_box(def_faction, …)`
    Hit (Z. 2036-2046), Wound (Z. 2075-2085, hier Whirling Onslaught), Save
    (Z. 2108-2117); SAVE-Block + Verteidiger-Inline-Re-Roll (Z. 2089-2099);
    Light-/Heavy-Cover-Checkboxen.
- Präzedenzfall: S139 E7 (`0a747b1`) hat exakt dieses Muster für Cut Them Down
  behoben (Box pro Spalte statt einmal außerhalb `st.columns()`) — dort war es ein
  Ein-Zeilen-Move; hier nicht 1:1 übertragbar, weil der Tab beide Spieler mischt.

**Technischer Kernkonflikt:** `st.tabs` exponiert den aktiven Tab NICHT — zwei
gespiegelte Tab-Leisten (eine je Spalte) können nicht synchron gehalten werden.
Der Umbau braucht daher einen **session-state-getragenen Entry-Selector** (z. B.
`st.radio` horizontal / Segmented Control) statt `st.tabs`, damit beide Spalten
denselben Waffe×Ziel-Eintrag zeigen.

## 3. Soll-Struktur

- Beide Phasen rendern während der Auflösung **weiterhin `st.columns(2)`** mit
  fixer Zuordnung `first_player` links / `second_player` rechts.
- Neuer Einstieg in `_common.py`:
  `render_attack_resolution_column(faction, phase_key)` — rendert in der Spalte
  von `faction` nur deren Anteil des aktuell selektierten Entries:
  - `faction == atk_faction`: Header + Attackenzahl, Entry-Selector (Owner der
    Selector-Widgets), HIT-Block (+ Re-Roll, Dense Cover), WOUND-Block (+ Re-Roll),
    DAMAGE-Block, Reset Declaration, „All done — Continue".
  - `faction == def_faction`: Ziel-Kopf (`def_unit` + Badges), die drei reaktiven
    GO-Anker (Hit-/Wound-Debuff, Invuln-Save), SAVE-Block (+ Re-Roll, Light/Heavy
    Cover), FNP, `_render_unit_rp`-Anteil (Reanimation = Verteidiger-Mechanik),
    „applied"-Zusammenfassung + Reset des Entries.
- Die **Berechnung** (Modifier-Stacks, `resolve_attack_modifiers`/`resolve_save`/
  `resolve_fnp`, Cover-State-Read) wird aus `_render_resolution_tab` in eine
  **pure Compute-Funktion** extrahiert (ein Kontext-Objekt pro Entry), die pro
  Rerun EINMAL läuft und von beiden Spalten-Renderern konsumiert wird — kein
  doppeltes, potenziell divergierendes Rechnen.
- Blockzuordnung-Regel (deckungsgleich mit dem bestehenden Re-Roll-Payer-Muster):
  „Der Block steht in der Spalte des Spielers, der den Wurf macht bzw. die GO
  bezahlt." Cover-Checkboxen bleiben beim Block, den sie modifizieren (Dense→HIT/
  Angreifer-Spalte als Sichtbarkeit, ABER Cover ist eine Verteidiger-Position —
  **Layout-Detailfrage fürs Mockup**, s. Gate unten).
- **Mockup-Gate (README-Grundregel):** Vor Umsetzung von Teil-Brief 2 wird dem
  Stakeholder ein Kurz-Mockup der Spaltenaufteilung gezeigt (insb.: Ort der
  Cover-Checkboxen, Ort von „All done", Selector-Form). Erst nach Freigabe bauen.

## 4. Umsetzungsschritte — Teil-Briefe (je ≤ M)

### Brief 1 — Compute/Render-Trennung ohne Layout-Änderung (Effort M)
- **Dateien:** `src/uiLayout/_common.py` (nur diese Datei; KEIN Verhalten/Layout-Change).
- `_render_resolution_tab` in (a) pure Funktion
  `compute_resolution_context(entry, …) -> dict/dataclass` (Waffe/Profil-Auflösung,
  Modifier-Stacks, atk_result/save_result/fnp, Cover-Flags) und (b) Render-Teil
  splitten; Render-Teil weiter innerhalb des bestehenden Voll-Panels aufrufen.
- Den Render-Teil bereits intern in `_render_attacker_blocks(ctx, …)` und
  `_render_defender_blocks(ctx, …)` gliedern (noch nacheinander im selben Tab).
- **Test-Anteil:** Die Compute-Funktion wird Coverage-gemessener Code → Unit-Tests
  (Streamlit-frei via bestehendem Session-State-Fixture-Muster in
  `tests/uiLayout/test_common.py`): S-Bonus-Faltung, Cover-Flag-Ableitung,
  Bracket-/Gruppen-Overrides. Budget: ~6-8 Tests.
- **Manuell zu verifizieren:** Shooting- und Fight-Auflösung sehen pixelidentisch
  aus wie vorher (kein sichtbarer Unterschied); ein voller Durchstich
  Deklaration→Apply→All done je Phase.
- **Konflikt-Hinweis:** NICHT parallel zu Plan 041 (extrahiert ebenfalls aus
  `_common.py`/Phasen-Dateien) und nicht parallel zu 015/026 ausführen.

### Brief 2 — Spalten-Bindung + Entry-Selector (Effort M)
- **Dateien:** `src/uiLayout/_common.py`, `src/gameMechanic/fightPhase.py`,
  `src/gameMechanic/shootingPhase.py`, `src/gameMechanic/gameState.py`
  (Reset-Pfade für den neuen Selector-Key; camelCase-Name beachten).
- **Voraussetzung:** Mockup-Freigabe (s. §3) liegt vor.
- **DAMAGE-Block-Abweichung aus Brief 1 (S150, bewusst):** Brief 1 ließ den
  DAMAGE-Block AUSSERHALB von `_render_attacker_blocks`/`_render_defender_blocks`
  (separater `_render_damage_block`-Aufruf am Ende von `_render_resolution_tab`),
  um die Vor-Brief-2-Render-Reihenfolge (nach SAVE/FNP) pixelidentisch zu halten
  (Kommentar in `_common.py` mit Spec-Verweis). Brief 2 bindet die
  Angreifer-Spalte daher als ZWEI Aufrufe: `_render_attacker_blocks(ctx)` +
  `_render_damage_block(…)` — der DAMAGE-Block ist NICHT Teil der Block-Funktion.
- `st.tabs` durch session-state-getragenen Entry-Selector ersetzen
  (Key z. B. `resolution_entry_idx`, gescoped auf `seq`); Reset in
  `_empty_attack_declaration`-Konsumenten + `reset_group_declaration_state` +
  Phasen-/Zug-Resets in `gameState.py` verankern.
- `render_attack_resolution` → `render_attack_resolution_column(faction, phase_key)`;
  Angreifer-/Verteidiger-Zweig gemäß §3. Alte vollbreite Funktion entfernen
  (kein toter Pfad zurücklassen).
- `fightPhase._render_display` (Z. 558-573) und `shootingPhase._render_display`
  (Z. 183-190) so umbauen, dass sie NICHT mehr vor den Spalten `return`en, sondern
  einen Resolution-Modus-Flag liefern; die Spalten-Blöcke (fight Z. 403-407,
  shooting Z. 106-126) rufen im Resolution-Modus je Spalte
  `render_attack_resolution_column(first|second, …)` auf — Spaltenzuordnung über
  `first`/`second`, NIE über `active`/`fight_player`.
- **Test-Anteil:** Regressionstests für (a) Selector-Key-Reset bei Reset
  Declaration/All done/Phasenwechsel, (b) `_render_display`-Rückgabeverhalten
  (stale-Declaration-Discard in fight bleibt erhalten, Z. 568-571). Budget: ~5 Tests.
- **Manuell zu verifizieren (UI, beide Phasen):** (1) Whirling Onslaught/Quantum
  Deflection erscheinen NUR in der Verteidiger-Spalte; (2) HIT/WOUND/DAMAGE nur in
  der Angreifer-Spalte; (3) Spalten bleiben first=links/second=rechts, auch wenn der
  second_player angreift; (4) Entry-Wechsel synchronisiert beide Spalten; (5) Apply/
  Reset/All done funktionieren; (6) Fight-Phase: Wechsel `fight_current_player`
  zwischen Aktivierungen bricht die Auflösung nicht; (7) Gruppen-Flow
  (`render_group_assignment`) kollidiert nicht mit dem Resolution-Modus.

### Brief 3 — Spec-/Artefakt-Nachzug + Restpolitur (Effort S)
- **Dateien:** `docs/spec/design_system.md` (§6.2/§6.3: Render-Ort der drei
  on_target-Anker = Verteidiger-Spalte; Anker-Schema unverändert),
  `docs/spec/processes.md` (Attackenabfolge-Darstellung, falls dort das vollbreite
  Panel beschrieben ist — Executor prüft), `docs/goals/backlog.md` +
  `docs/handoff/S141_ui_befunde_group_a.md` (Befund 3 → DONE, Datei gemäß
  Lifecycle-Zeile behandeln), `docs/audit/plans/README.md` (Queue-Status).
- Kleinreste aus Brief 2: `SYM_*`-Ratchet an berührten Stellen, tote Keys/Helper
  entfernen, mypy-Baseline nicht erhöhen.
- **Test-Anteil:** keiner (Doku) außer Vollsuite-Nachweis grün.
- **Manuell zu verifizieren:** nichts Neues; Abschluss-Smoke (ein Durchstich je Phase).

Jeder Brief: Vollsuite `pytest --tb=short` (Coverage ≥ 99 %), Architektur-Gate,
`black`/`isort`/`ruff`; Selbstprüf-Checkliste inkl. Verdrahtungs-`grep`;
Test-Budget + Selbst-Stopp gemäß Stakeholder-Auflage (max. Effort M pro Brief).

## 5. Risiken

1. **`st.tabs` → Selector-Migration (größtes Risiko):** Der aktive Tab ist heute
   impliziter UI-State; der neue Session-State-Key muss in ALLEN Reset-Pfaden
   (Reset Declaration, All done, Phasen-/Zugwechsel in `gameState.py`, Game Reset)
   geleert werden, sonst zeigt eine neue Deklaration den Entry-Index der alten
   (Index-out-of-range-Gefahr). Mitigation: Key an `seq` koppeln (Brief 2).
2. **Scroll-Anchoring/Layout-Shift:** Umschalten vollbreites Panel ↔ zwei Spalten
   entfällt zwar (weniger Shift als heute), aber Entry-Wechsel ändert beide Spalten
   gleichzeitig. `overflow-anchor: none` auf `stMain` (B1-Fix S136) muss den Fall
   abdecken — manuell gegenprüfen, Beleg wie `docs/handoff/S136_B1_probe.md`.
3. **Doppel-Berechnung/Divergenz:** Wenn beide Spalten den Kontext getrennt
   berechnen, können Cover-Checkbox-Reads (Read-before-Render-Muster, Z. 1917-1929)
   divergieren. Mitigation: Compute EINMAL pro Rerun vor den Spalten (Brief 1
   erzwingt das strukturell).
4. **Fight-Phase-Sonderpfade:** `fight_current_player`-Priorität, stale-Declaration-
   Discard (Z. 568-571), Counter-Offensive-Box und Gruppen-Flow leben im selben
   Render-Ast — Regressionsgefahr bei der `return`-Umstellung. Mitigation: gezielte
   Tests + manuelle Punkte in Brief 2.
5. **Plan-041-Kollision:** 041 will Render-Orchestrierung aus denselben Dateien
   extrahieren — strikt sequenziell halten (Queue-Hinweis in README).
6. **camelCase-Rename parallel:** Import-Pfade (`gameMechanic.gameState` etc.)
   können sich zwischen Planung und Ausführung ändern — Executor verifiziert
   Modulnamen vor dem ersten Edit.

## 6. Rollback-Strategie

- Brief 1 ist ein reiner Struktur-Refactor ohne Sichtbarkeitsänderung — einzeln
  revertierbar, App identisch.
- Brief 2 ist der eigentliche Layout-Umbau: als EIN Commit schneiden; `git revert`
  stellt das vollbreite Panel vollständig wieder her (Brief 1 bleibt gültig).
- Kein Feature-Flag nötig (App hat keinen Release-Kanal); Sicherheitsnetz sind die
  Regressionstests + der Revert-Schnitt. Session-State-Altlasten nach Revert:
  der Selector-Key wird von altem Code ignoriert — unkritisch.
- Die separat laufende `target_name`-Sofortlinderung bleibt von einem Rollback
  unberührt und lindert den Leak visuell weiter.

## 7. Gesamteinschätzung

Gesamtaufwand **L**, gesplittet in M + M + S. Reihenfolge strikt 1 → (Mockup-Gate)
→ 2 → 3. Kein Code vor Freigabe dieses Plans; Brief 2 zusätzlich hinter dem
Mockup-Gate.
