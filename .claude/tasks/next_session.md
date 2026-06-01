# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session passiert ist

**Ziel: Schritt 2 — Schema-Bereinigung (vollständig abgeschlossen)**

### Erledigte Design-Entscheidungen
- `WeaponGroup` (Option B): Einheiten mit gemischten Loadouts nutzen `weapon_groups: list[WeaponGroup]` statt flacher `weapons`-Liste
- `Army.unmatched` (Option A): Unbekannte `unit_id` im Roster landet in `unmatched`-Liste + Warnung, kein harter Fehler

### Erledigte Korrekturen
- `army_rules.yaml` — Command Protocols: `assign_count: 5` → `assign_to_rounds: 5` + `permanent_count: 1` (permanentes Protokoll muss ebenfalls gewählt werden)

### Erledigte Bereinigungen

**Gruppe A — YAML:**
| Datei | Änderung |
|-------|----------|
| `command_protocols.yaml` | Alle 6 IDs auf Namespace-Präfix `wh40k_9e.necrons.protocol.*` |
| `wargear.yaml` | 3 Relic-Einträge entfernt (`orb_of_eternity`, `nanoscarab_casket`, `veil_of_darkness`) |
| `wargear_abilities.yaml` | 3 Relic-Ability-Einträge entfernt (gleiche 3) |
| `points.yaml` | `arkana:`-Abschnitt mit 12 Einträgen ergänzt |
| `arkana.yaml` | Alle `points_cost`-Felder entfernt (jetzt in `points.yaml`) |

**Gruppe B — Waffen-Migration:**
| Datei | Änderung |
|-------|----------|
| `weapons.yaml` | Komplett auf `profiles: list[WeaponProfile]` umgestellt; 15 Dual-Profile-Paare zusammengeführt (`staff_of_light`, `heat_ray`, `doomsday_cannon`, etc.); `resurrection_orb` als Weapon entfernt |
| `units.yaml` | Alle `_shooting`/`_melee`-Refs zusammengeführt; `wh40k_9e.necrons.weapon.resurrection_orb` → `wh40k_9e.necrons.wargear.resurrection_orb` |

**Gruppe C — Python:**
| Datei | Änderung |
|-------|----------|
| `weapon.py` | `WeaponProfile`, `WeaponGroup`, `Weapon` neu strukturiert |
| `loader.py` | `_weapon_profile_from_dict`, `_weapon_from_dict` (Profile-Parsing), `load_weapon_catalog`, `_unit_from_dict` (Ref-Auflösung mit weapon_catalog), `load_army` gibt jetzt `(list[Unit], list[str])` zurück |

---

## Aktueller Status Necrons-Datensatz

| Datei | Status |
|-------|--------|
| `units.yaml` | ✅ 51 Einheiten — Refs auf einzelne Weapon-IDs (keine Splits mehr) |
| `weapons.yaml` | ✅ Profile-Schema; alle Dual-Profile zusammengeführt |
| `stratagems.yaml` | ✅ 59 Stratagems |
| `faction_abilities.yaml` | ✅ |
| `unit_abilities.yaml` | ✅ |
| `wargear_abilities.yaml` | ✅ Relic-Duplikate entfernt |
| `wargear.yaml` | ✅ Relic-Duplikate entfernt |
| `subfaction_abilities.yaml` | ✅ 6 Dynastien |
| `command_protocols.yaml` | ✅ Namespace-Präfix gesetzt |
| `warlord_traits.yaml` | ✅ |
| `arkana.yaml` | ✅ `points_cost` entfernt |
| `relics.yaml` | ✅ |
| `weapon_abilities.yaml` | ✅ |
| `army_rules.yaml` | ✅ Command Protocols korrigiert |
| `points.yaml` | ✅ `arkana:`-Abschnitt vorhanden |

---

## Nächster konkreter Schritt: Schritt 3 — Forge World Einheiten

**Voraussetzung: explizite Freigabe durch Nutzer vor jeder Dateiänderung.**

Forge World Einheiten für Necrons, die noch fehlen:
- Night Shroud
- Canoptek Tombstalker
- Canoptek Acanthrites
- Tesseract Ark
- Canoptek Tomb Sentinel
- Gauss Pylon
- Seraptek Heavy Construct
- Sentry Pylon

**Vorgehen:**
1. Subagent: Daten für alle 8 Einheiten von Wahapedia fetchen (Stats, Waffen, Keywords, Regeln)
2. Neue Sektion `# ── Forge World ──` in `units.yaml` ergänzen
3. Neue Waffen-Einträge in `weapons.yaml` (Profile-Format)
4. Punkte-Einträge in `points.yaml`

---

## Danach: Schritt 4 — Loader implementieren (Ziel 5c)

`src/gameObjects/loader.py` vollständig auf neues Schema umschreiben:
- Roster-first: erst Roster parsen + validieren, dann Catalog-Einträge laden
- `Unit.weapon_groups: list[WeaponGroup]` für gemischte Einheiten
- `load_army` gibt `(list[Unit], list[str])` zurück — unmatched bereits vorbereitet

Offene Design-Fragen (aus loader_contract.md §6, noch zu entscheiden vor Schritt 4):
| # | Frage | Impact |
|---|-------|--------|
| 1 | `Unit`-Dataclass: `weapon_groups: list[WeaponGroup]` für gemischte Einheiten, oder erst im Combat-System auflösen? | `unit.py`, `fightPhase.py`, `shootingPhase.py` |

---

## Wichtige Constraints
- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts
- dev-Branch — kein direktes Committen auf main
