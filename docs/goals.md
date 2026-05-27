# Projektziele — Arbiter

## Vision

Arbiter ist ein digitaler Spielbegleiter für WH40k 9. Edition (Streamlit).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Zielarchitektur: `app.py` + `uiLayout/` + `gameObjects/` + `gameMechanic/`
Details: `docs/architecture.md` · UI-Spec: `docs/ui_layout.md`

---

## Ziel 1A — `uiLayout/` Struktursplit ⏳

Ziel: `src/ui.py` wird ohne Verhaltensänderung in `src/uiLayout/` aufgeteilt.
Alle Sidebar-Komponenten erhalten dabei das neue Layout gemäß `docs/ui_layout.md`.
`gameActionsArea.py` bleibt ein dünner Container-Stub — keine Verhaltensänderung, kein neues Layout.

**Voraussetzung:** keine — kann sofort starten.

- [ ] `uiLayout/gameHeader.py` — VP/CP-Stepper, game params display
- [ ] `uiLayout/armyCard.py` — armyName, faction/subfaction-Badges, battleForged, properties (read-only)
- [ ] `uiLayout/unitCard.py` — neues Layout: Name als Select-Trigger (visuell), Keywords, LP/Modell-Bar, State-Badges, phase area (collapsible); Select-Logik als Stub
- [ ] `uiLayout/detachmentCard.py` — Detachment-Header + unitCards gruppiert nach Schlachtfeldrolle
- [ ] `uiLayout/armyList.py` — Container: armyCard + 1–n detachmentCards
- [ ] `uiLayout/gameProtocoll.py` — Runden/Phasen-Navigation, Log-Anzeige, Download-Button
- [ ] `uiLayout/gameActionsArea.py` — Stub-Container; delegiert an gameMechanic (noch leer)
- [ ] `app.py` auf neue Imports umstellen
- [ ] Alle bestehenden Tests bleiben grün

---

## Ziel 1B — `gameObjects/` Foundation ⏳

Ziel: Reine Python-Grundlage für alle Spieldaten. Kein Streamlit, kein session_state.
Armeedaten fließen künftig ausschließlich durch den Loader — keine hardcodierten Listen mehr.

**Voraussetzung:** keine — kann parallel zu 1A starten.

- [ ] `gameObjects/unit.py` — `Unit` Dataclass
- [ ] `gameObjects/weapon.py` — `Weapon` Dataclass
- [ ] `gameObjects/faction_property.py` — `FactionProperty` Dataclass
- [ ] `gameObjects/detachment.py` — `Detachment` Dataclass inkl. Slot-Constraints
- [ ] `gameObjects/loader.py` — liest YAML, löst Waffen-Referenzen auf
- [ ] `data/wh40k_9e/_shared/detachment_types.yaml` — Patrol, Battalion, Brigade usw. mit Slot-Constraints (verifiziert gegen Wahapedia)
- [ ] `data/wh40k_9e/necrons/faction_properties.yaml` — Living Metal, Reanimation Protocols usw.
- [ ] `data/wh40k_9e/necrons/subfaction_properties.yaml` — Dynasty-Regeln (Nephrekh, Sautekh usw.)
- [ ] Necrons + Orks über Loader laden; hardcodierte Dicts aus `models.py` entfernen
- [ ] Unit-Tests für Loader und Dataclasses

---

## Ziel 2 — `gameMechanic/` Einstieg: Command Phase ⬜

Ziel: Erste vollständige Phase als Blaupause für alle weiteren.
Bewusst die einfachste Phase gewählt: kein Combat-Roll, aber vollständige Mechanik inkl. gameActionsArea-Layout.
Danach ist das Zusammenspiel gameMechanic ↔ gameActionsArea für alle Folgephasen klar.

**Voraussetzung:** Ziel 1B abgeschlossen.

- [ ] `gameMechanic/state.py` — session_state-Schema, `init_state`, `reset_game`, `next_phase`
- [ ] `gameMechanic/protocol.py` — Log-Append, Unveränderlichkeit nach Zug-Ende
- [ ] `gameMechanic/commandPhase.py` — BP-Bonus, factionProperty-Trigger (Living Metal etc.), CP-Verwaltung
- [ ] `uiLayout/gameActionsArea.py` — Layout für commandPhase fertigstellen (füllt den Stub aus 1A)
- [ ] Select-Logik in `unitCard.py` vollständig verdrahten (Stub aus 1A wird aktiviert)
- [ ] gameProtocoll: Log-Einträge für commandPhase definieren und schreiben
- [ ] Tests für commandPhase (state transitions, factionProperty-Trigger)

---

## Ziel 3 — Combat Foundation: Phase-Infrastruktur + Attack Sequence ⬜

Ziel: Das Fundament der Spielmechanik legen. Jede weitere Phase, jede Armee und jede Ability dockt an diese Infrastruktur an — ohne neue Code-Strukturen einzuführen.

**Kern-Einsicht:** Action ≠ Phase. Die `AttackSequence` ist eine wiederverwendbare Aktion, die von der Fernkampf- *und* der Nahkampfphase (und später Overwatch in der Angriffsphase) mit unterschiedlichen Bedingungen aufgerufen wird. Abilities sind Parameter-Modifier für diese Sequenz.

**Voraussetzung:** Ziel 2 abgeschlossen.

---

### 3a — Phase-Infrastruktur

- [ ] `gameMechanic/phase_handler.py` — `PhaseHandler` Protocol (Abstract Base für alle Phasen)
- [ ] `gameMechanic/phase_runner.py` — zentraler Dispatcher; treibt `start → active → end` für alle Phasen; feuert Ability-Hooks an Übergängen; hält `PHASE_REGISTRY`
- [ ] `engine.py` — `turn_flags` dict in `_unit_state()` einführen (`advanced`, `retreated`, `charged`, `shot`, `fought`); ad-hoc-Felder ersetzen; `reset_turn_flags()` für Zuganfang
- [ ] `gameMechanic/ability_engine.py` — neue Timing-Konstanten: `before_unit_acts`, `after_unit_attacked`
- [ ] `gameMechanic/commandPhase.py` — auf `PhaseHandler`-Protocol migrieren (`CommandPhaseHandler`)
- [ ] `uiLayout/gameActionsArea.py` — Routing-Logik ersetzen durch `phase_runner.render_current_phase(state)`
- [ ] 4 Stub-Handler: `movementPhase.py`, `chargephase.py`, `psychicPhase.py`, `moralePhase.py` — zeigen Phasennamen, setzen/lesen `turn_flags`, erlauben Weiterklicken

---

### 3b — Combat-Kernel (`combat.py`) — KRITISCH

Zentrale, army-agnostische Datei. Jede Änderung an dieser Datei **muss** von einem vollständig grünen Test-Suite abgesichert sein.

- [ ] `gameMechanic/combat.py` — Dataclasses `Modifier`, `AttackParams`, `AttackResult`; Funktionen `s_vs_t_table`, `resolve_attack_sequence`, `build_attack_display`
- [ ] `tests/gameMechanic/test_combat.py` — **≥ 40 Tests** — vollständige Spezifikation in `next_session.md`

Grundsätze:
- `resolve_attack_sequence` nimmt **vom Spieler eingegebene Zählwerte** (physisch gewürfelt), keine Auto-Würfel
- AP modifiziert den **Würfelwurf**, nicht den Threshold — `effective_roll = raw_roll + ap_modifier`
- Roll-Modifier für Treffer/Verwundung **gecappt bei ±1** (9E-Regel); AP hat keinen Cap
- Unmodifizierter 1 = immer Fehler, unmodifizierter 6 = immer Treffer/Verwundung (Sonderregel)
- `"User"`-Stärke wird **vor** Übergabe an die Funktion aufgelöst — Funktion sieht nur `int`

---

### 3c — Shooting Phase + Fight Phase

**Voraussetzung:** 3a und 3b vollständig und alle Tests grün.

- [ ] `gameMechanic/shootingPhase.py` — `ShootingPhaseHandler`; `can_shoot(unit_state)` als pure function; Parameter aus Waffenprofil; UI: Angreifer-Waffe | Ziel-Stats | AttackDisplay | Spieler-Input
- [ ] `gameMechanic/fightPhase.py` — `FightPhaseHandler`; Parameter aus Einheits- + Waffenprofil (A-Stat, WS, `"User"`-Auflösung); Fights-First-Reihenfolge; UI analog Shooting
- [ ] `data/wh40k_9e/necrons/unit_abilities.yaml` — RP-Timing aktualisieren auf `after_unit_attacked` (Phase: `[shooting, fight]`, Player: `inactive`) — als **Testfall** für das Ability-Hook-System, kein Hardcode in den Phasendateien
- [ ] `tests/gameMechanic/test_shooting_phase.py` — `can_shoot`-Fälle, Parameter-Auflösung, MWBD-Modifier
- [ ] `tests/gameMechanic/test_fight_phase.py` — `can_fight`-Fälle, `"User"`-Stärkeauflösung, Fights-First-Reihenfolge
- [ ] `engine.py` — alten `resolve_attack()` deprecaten/entfernen

---

## Ziel 4 — Phasen ausbauen + Army Builder ⬜

**Voraussetzung:** Ziel 3 abgeschlossen (Infrastruktur steht, Stubs existieren).

### Phasen (Stubs → vollständige Implementierung)
- [ ] `movementPhase.py` — Move-Typ-Selector, Advance-Roll, Reserve-Deploy; `turn_flags` korrekt setzen
- [ ] `chargephase.py` — Charge-Roll (2D6), Overwatch via `ShootingAction` mit `hit_modifier="only_6s"`
- [ ] `moralePhase.py` — D6 + Verluste vs. Leadership
- [ ] `psychicPhase.py` — Manifest (2D6 ≥ WC), Deny, Perils (Scope: TBD)

### Army Builder
- [ ] Entscheidung: Datei-Import vs. In-App-Builder vs. hardcodierte Presets (TBD)
- [ ] Setup-Screen: Spielgröße, Spieltyp, Armeeauswahl, Erster Spieler
- [ ] Detachment-Slot-Constraints als Referenz im Setup anzeigen

---

## Offene Designfragen

Dokumentiert in `docs/architecture.md` — Abschnitt "Open Design Questions".
