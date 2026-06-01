# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session passiert ist

**Ziel 5b.2 vollständig abgeschlossen — Schritte A, B, C ✅ — 306 Tests grün**

### Schritt A ✅ (bereits letzte Session, jetzt fertig)
- `army.yaml` gelöscht
- Alle Ability-IDs auf `wh40k_9e.`-Namespace normiert
- `loader.py` liest `units.yaml`; `ability_engine.py` Tuple-Unpacking korrigiert
- `Convergence of Dominion` (Fortification): `move/ws/leadership: null` → `"-"`
- `Unit.leadership: int | None` (None = Gebäude)

### Schritt B ✅
- Alle 16 `wargear_options`-Blöcke in `units.yaml` auf `type/with/replaces/item`-Schema
- `replace_all_with` (Monolith) → `type: replace, replaces: gauss_flux_arc`

### Schritt C ✅
- `WargearOption`, `DamageBracket` Dataclasses in `src/gameObjects/unit.py`
- `Unit` um `power_level: int`, `attacks: int | None`, `wargear_options`, `damage_bracket` erweitert
- `loader.py`: `_wargear_option_from_dict`, `_damage_bracket_from_dict`, `load_unit_catalog()`
- Orks-legacy `army.yaml` via Defaults kompatibel gehalten (`power_level=0`)
- 8 Test-Fixtures aktualisiert, 7 neue Tests in `tests/gameObjects/test_loader.py`

### UI-Status der neuen Felder
Die neuen Felder sind reine Datenschicht-Erweiterungen — kein UI-Code wurde geändert:
- `power_level`, `wargear_options` → relevant für Army Builder (Ziel 5e)
- `attacks` → relevant für Detailansichten / Kampfphase
- `damage_bracket` → **spielmechanisch dringend**: Vehicles zeigen aktuell immer Basis-Stats, auch bei niedrigem Woundstand

---

## Aktueller Status Necrons-Datensatz

Alle Dateien vollständig und normiert. ✅ 306 Tests grün.

---

## Nächster konkreter Schritt: 5c Loader-Refactoring

**Voraussetzung: explizite Freigabe durch Nutzer vor Dateiänderungen.**
**Alle Punkte gehören zu 5c — am besten zusammen angehen.**

### 1 — `damage_bracket` live auflösen (spielmechanisch dringend)

Vehicles (Triarch Stalker, Monolith, etc.) zeigen aktuell immer Basis-Stats.
Fix: Hilfsfunktion, die aus `damage_bracket` + aktuellem Woundstand die laufenden Stats zurückgibt.

```python
def resolve_bracket_stats(unit: Unit, current_wounds: int) -> dict[str, str]:
    """Gibt {move, ws, bs, attacks} für den aktuellen Woundstand zurück."""
```

Betroffene Dateien: `src/gameObjects/loader.py` + ggf. UI-Stellen, die `unit.move/ws/bs` rendern.

### 2 — Default-Nahkampfwaffe ergänzen

Jede Einheit braucht mindestens eine Nahkampfwaffe. Falls keine in `weapons` definiert, automatisch:
`Close Combat Weapon: Range=Melee, S=User, AP=0, D=1`
In `_unit_from_dict` nach dem Waffen-Laden prüfen und ergänzen.

### 3 — `points.yaml` einbinden

`src/gameObjects/loader.py` um `load_points(faction_dir)` erweitern.
Gibt `dict[str, int]` zurück (unit_id → Punkte).
`points.yaml` hat Sektionen (HQ, Troops, …) + `wargear:` + `arkana:` — flatten zu einem dict.

### 4 — `power_level`-Skalierung

Hilfsfunktion: `scaled_pl(unit: Unit, current_models: int) -> float`
Formel: `unit.power_level × (current_models / unit.models_min)`
Keine Änderung an der Dataclass — reine Berechnung im Loader oder game_state.

### 5 — Roster-Flow: `load_army` auf ID-Lookup umschreiben

Roster `data/rosters/<name>.yaml` laden, IDs gegen Katalog auflösen, `unmatched` befüllen.
Vorbedingung: ein Roster für Necrons anlegen.
`unmatched`-Einheiten: Warnung im Setup, nicht spielbar.

### 6 — Orks auf `units.yaml`-Format migrieren

Orks noch im Altformat (`army.yaml`). Migration → Orks können dann alle neuen Felder nutzen.
Bis dahin: `power_level=0` als Compat-Default im Loader.

---

## Wichtige Constraints
- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts
- dev-Branch — kein direktes Committen auf main
