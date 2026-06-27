# Ziel 1 — Struktursplit & Foundation ✅

## Ziel 1A — `uiLayout/` Struktursplit ✅

Ziel: `src/ui.py` wird ohne Verhaltensänderung in `src/uiLayout/` aufgeteilt.
Alle Sidebar-Komponenten erhalten dabei das neue Layout gemäß `docs/spec/ui_layout.md`.

**Abgeschlossen.** `ui.py` gelöscht. Alle Komponenten in `uiLayout/` aktiv.

- [x] `uiLayout/gameHeader.py` — VP/CP-Stepper, Phase-Navigation, Theme-CSS
- [x] `uiLayout/armyCard.py` — Fraktion/Subfraktion-Anzeige
- [x] `uiLayout/unitCard.py` — Name als Selector, Keywords, LP/Modell-Bar, State-Badges
- [x] `uiLayout/detachmentCard.py` — Detachment-Header + unitCards gruppiert nach Schlachtfeldrolle
- [x] `uiLayout/armyList.py` — Container: armyCard + 1–n detachmentCards
- [x] `uiLayout/gameProtocoll.py` — Battle-Log aus game_log.json + Deployment-Snapshot
- [x] `uiLayout/gameActionsArea.py` — Container; delegiert an phase_runner
- [x] `app.py` auf neue Imports umgestellt
- [x] Alle Tests grün

---

## Ziel 1B — `gameObjects/` Foundation ✅

Ziel: Reine Python-Grundlage für alle Spieldaten. Kein Streamlit, kein session_state.
Armeedaten fließen ausschließlich durch den Loader — keine hardcodierten Listen mehr.

**Abgeschlossen.** `models.py` gelöscht. Alles über YAML-Loader.

- [x] `gameObjects/unit.py` — `Unit` Dataclass
- [x] `gameObjects/weapon.py` — `Weapon` Dataclass
- [x] `gameObjects/faction_property.py` — `FactionProperty` Dataclass
- [x] `gameObjects/detachment.py` — `DetachmentType`, `SlotConstraint`
- [x] `gameObjects/loader.py` — liest YAML, löst Waffen-Referenzen auf
- [x] `data/wh40k_9e/_shared/detachment_types.yaml` — Patrol usw. mit Slot-Constraints
- [x] YAML-Daten für Necrons + Orks initial kuratiert (durch Ziel 5b ersetzt)
- [x] `models.py` (hardcodierte Dicts) entfernt
- [x] Unit-Tests für Loader und State-Funktionen
