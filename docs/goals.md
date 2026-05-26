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

## Ziel 3 — Combat Loop: Shooting & Fight Phase ⬜

Ziel: Vollständige Treffersequenz (Treffer → Verwundung → Rettung → Schaden) im Zentralbereich.
Zwei Phasen auf einmal, da sie dieselbe `combat.py`-Grundlage teilen.

**Voraussetzung:** Ziel 2 abgeschlossen.

- [ ] `gameMechanic/combat.py` — `hit_roll`, `wound_roll`, `save_roll`, `apply_damage` als pure functions
- [ ] `gameMechanic/shootingPhase.py` — Logik + gameActionsArea-Layout (Angreifer | Ziel)
- [ ] `gameMechanic/fightPhase.py` — Logik + gameActionsArea-Layout, Fights-first-Reihenfolge
- [ ] Weapon-Profile-Anzeige aus gameObjects (kein Hardcode mehr)
- [ ] Modifier-Buttons (+1/−1, capped ±1), Result-Anzeige
- [ ] Log-Einträge für beide Phasen
- [ ] Tests für combat.py + beide Phasen

---

## Ziel 4 — Restliche Phasen + Army Builder ⬜

**Voraussetzung:** Ziel 3 abgeschlossen.

### Phasen
- [ ] `gameMechanic/movementPhase.py` — Move-Typ-Selector, Advance-Roll, Reserve-Deploy
- [ ] `gameMechanic/chargephase.py` — Charge-Roll, Overwatch, Heroic Intervention
- [ ] `gameMechanic/moralePhase.py` — D6 + Verluste vs. Leadership
- [ ] `gameMechanic/psychicPhase.py` — Manifest/Deny/Perils (Scope: TBD)

### Army Builder
- [ ] Entscheidung: Datei-Import vs. In-App-Builder vs. hardcodierte Presets (TBD)
- [ ] Setup-Screen: Spielgröße, Spieltyp, Armeeauswahl, Erster Spieler
- [ ] Detachment-Slot-Constraints als Referenz im Setup anzeigen

---

## Offene Designfragen

Dokumentiert in `docs/architecture.md` — Abschnitt "Open Design Questions".
