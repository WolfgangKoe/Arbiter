# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — aktueller Gesamtstatus aller Ziele
3. `src/gameMechanic/movementPhase.py` — Movement Phase (Bugs dokumentiert)
4. `src/gameMechanic/commandPhase.py` — fertig umgebaut, als Referenz für Flows
5. `src/uiLayout/unitCard.py` — MWBD/ResOrb-Awaiting-Logik als Referenz

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.
Starten: `streamlit run src/app.py`
Aktueller Branch: `dev`

---

## Was in dieser Session gemacht wurde

### Command Phase UX-Refactor (erledigt)
- MWBD + ResOrb erscheinen nur wenn Overlord als Einheit ausgewählt ist
- LP-Buttons (Wound Adjustment) aus dem selected-unit-Block der Command Phase entfernt
- MWBD-Zielauswahl via unitCard: `mwbd_awaiting_target = True` → CORE-Einheiten in der Armeeliste werden zu klickbaren Zielen; Nicht-CORE als Plaintext
- ResOrb-Zielauswahl analog: `res_orb_awaiting_target = True` → alle Einheiten (außer Overlord) werden zu Zielen
- Cancel-Buttons für beide Flows
- MWBD-Dauer-Fix: `mwbd_active_since_round` gespeichert; Reset am Anfang der nächsten Necron-Command-Phase

### MWBD-Badge (erledigt)
- Badge "MWBD" (`#60a5fa` auf `#0a1020`) in `_common.py` und `unitCard.py` ergänzt
- Erscheint sobald `my_will_be_done_active = True` auf der Einheit

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A — uiLayout/ Struktursplit | ✅ fertig |
| Ziel 1B — gameObjects/ Foundation | ✅ fertig |
| Ziel 2 — Command Phase | ✅ fertig inkl. UX-Refactor |
| Ziel 3a — Phase-Infrastruktur | ✅ fertig |
| Ziel 3b — combat.py Kernel | ⏳ Foundation vorhanden, AttackSequence fehlt |
| Ziel 3c — Shooting + Fight Phase | ⏳ Stubs vorhanden, wartet auf 3b |
| Bewegungsphase Bugs | 🐛 zwei bekannte Fehler (siehe unten) |

---

## Nächste Schritte (Prioritätsreihenfolge)

### A — Bewegungsphase Bugs (höchste Priorität, kleine Fixes)

**Datei:** `src/gameMechanic/movementPhase.py`

**Bug 1 — In-Melee-Lock:**
- Wenn `in_melee = True`: Normal und Advance müssen disabled sein
- Nur Stationary und Retreat erlaubt
- Aktuell: nur Retreat wird disabled wenn NICHT in melee (Zeile 84); umgekehrt fehlt der Lock

**Bug 2 — Post-Retreat-Lock:**
- Wenn `turn_flags["retreated"] = True`: Normal und Advance müssen disabled sein
- Einheit kann sich nach einem Retreat in dieser Phase nicht anders bewegen
- Aktuell: kein Lock nach Retreat gesetzt

**Fix-Logik** (beide Bugs, ~5 Zeilen in `_active_movement`):
```python
flags = unit_state.get("turn_flags", {})
already_retreated = flags.get("retreated", False)
disabled_normal   = (in_melee or already_retreated)
disabled_advance  = (in_melee or already_retreated)
disabled_retreat  = not in_melee
# disabled_stationary = False (immer erlaubt)
```

**Erforderliche Änderungen:**
- `src/gameMechanic/movementPhase.py` — `disabled`-Logik pro Button erweitern
- Die Caption "Unit is in melee — only Stationary or Retreat allowed." bleibt

---

### B — Ziel 3b: combat.py Kernel

**Datei:** `src/gameMechanic/combat.py`
**Tests:** `tests/gameMechanic/test_combat.py` (neu anlegen, ≥ 40 Tests)

Zentrale army-agnostische Datei. Keine Streamlit-Abhängigkeiten.

**Was fehlt:**
- `AttackParams` Dataclass: `attacks`, `skill`, `strength`, `ap`, `damage`, `hit_modifier`, `wound_modifier`, `mwbd_active`
- `DefendParams` Dataclass: `toughness`, `save`, `invul_save`, `wounds`
- `resolve_attack(params: AttackParams, defender: DefendParams) → tuple[int, list[str]]`
  - Gibt `(total_damage, log_lines)` zurück
  - Nimmt physisch gewürfelte Zählwerte vom Spieler entgegen (kein Auto-Würfeln)

**Regeldetails (unveränderlich festgelegt):**
- AP modifiziert den Würfelwurf: `effective_roll = raw_roll + ap_modifier` (kein Save-Threshold-Abzug)
- Roll-Modifier für Hit/Wound gecappt bei ±1 (9E-Regel); AP hat keinen Cap
- Unmodifizierter 1 = immer Fehler; unmodifizierter 6 = immer Treffer/Verwundung
- `"User"`-Stärke wird vor Übergabe aufgelöst — Funktion sieht nur `int`
- `mwbd_active` auf Angreifer → `hit_modifier +1`

---

## Offene Punkte / bekannte Schwächen

### Bewegungsphase (nächste Session fixen)
- In-Melee-Einheiten können Normal/Advance wählen — falsch
- Nach Retreat sind Normal/Advance noch wählbar — falsch

### Deprecated resolve_attack() in combat.py
- Erst löschen wenn Ziel 3b vollständig

---

## Designentscheidungen (unveränderlich)

- `turn_flags` = Spielmechanik-Checks only
- `movement_choice` = Display only; nicht angezeigt wenn `charged=True` oder `in_reserve=True`
- `melee_with` bidirektional (enter_melee / leave_melee)
- `selected_targets: list[tuple[str, str]]` — nie wieder single-target
- `can_fight()` prüft `melee_with` ODER `charged` flag
- LP-Buttons: aktive Seite kein Button in Command Phase; inaktive Seite (Ziele) ja
- `render_player_column()` bleibt in `_common.py`
- Alle engine-Importe direkt aus `gameMechanic.*` — kein `engine.py` Shim mehr
- Aktionen erscheinen NUR kontextabhängig zur ausgewählten Einheit
- Buff-Zustände (MWBD etc.) müssen als Badge sichtbar sein
- MWBD/ResOrb Zielauswahl via unitCard (awaiting-target-Flow), nicht via Inline-Buttons
