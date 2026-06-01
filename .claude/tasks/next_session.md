# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session passiert ist

**Ziel: Schritt 1 — Loader-Vertrag definieren**

Der Loader-Vertrag ist vollständig ausgearbeitet und in `docs/spec/loader_contract.md` festgehalten.

Analyse-Grundlage: Alle 15 Necrons-YAML-Dateien gelesen, `docs/spec/architecture.md`,
`docs/spec/processes.md`, `docs/work/schlachtrunde.md`, `src/gameObjects/loader.py`,
`data/wh40k_9e/necrons/army_rules.yaml` und `docs/spec/setup.md`.

**Design-Entscheidungen dieser Session:**
- `Weapon`-Dataclass bekommt `profiles: list[WeaponProfile]` (auch Single-Profile-Waffen)
- Roster-Format definiert (inkl. `weapon_loadout` mit `model_count` für gemischte Einheiten)
- Loader läuft Roster-first: erst Roster parsen + validieren, dann nur benötigte Catalog-Einträge laden
- Arkana haben Punktekosten in Matched Play → `arkana:`-Abschnitt in `points.yaml`
- Relics, Warlord Traits, Arkana → werden als `Ability`-Objekte an Einheit gehängt
- `points.yaml` und Power Level nur im Setup-Screen, nicht im laufenden Spiel

---

## Aktueller Status Necrons-Datensatz

| Datei | Status |
|-------|--------|
| `units.yaml` | ✅ 51 Einheiten — Refs auf `_shooting`/`_melee` + `resurrection_orb` (weapon) noch alt |
| `weapons.yaml` | ⚠️ Dual-Profile-Waffen als 2 Objekte; `resurrection_orb` fälschlich drin |
| `stratagems.yaml` | ✅ 59 Stratagems |
| `faction_abilities.yaml` | ✅ |
| `unit_abilities.yaml` | ✅ |
| `wargear_abilities.yaml` | ⚠️ 3 Relic-Ability-Einträge drin (Duplikation) |
| `wargear.yaml` | ⚠️ 3 Einträge mit `is_relic: true` (Duplikation zu relics.yaml) |
| `subfaction_abilities.yaml` | ✅ 6 Dynastien |
| `command_protocols.yaml` | ⚠️ IDs ohne Namespace-Präfix (`eternal_guardian` statt `wh40k_9e.necrons.protocol.eternal_guardian`) |
| `warlord_traits.yaml` | ✅ Struktur klar — nur Anzeige + Ability-Objekt bei Freigabe |
| `arkana.yaml` | ⚠️ `points_cost` direkt in Datei statt in `points.yaml` |
| `relics.yaml` | ✅ Struktur klar |
| `weapon_abilities.yaml` | ✅ |
| `army_rules.yaml` | ✅ |
| `points.yaml` | ⚠️ `arkana:`-Abschnitt fehlt noch |

---

## Nächster konkreter Schritt: Schritt 2 — Schema-Bereinigung

**Voraussetzung: explizite Freigabe durch Nutzer vor jeder Dateiänderung.**

Die vollständige Spezifikation steht in `docs/spec/loader_contract.md`.

### Reihenfolge (Abhängigkeiten beachten)

**Gruppe A — YAML-Bereinigung (keine Python-Änderungen nötig):**

1. `command_protocols.yaml` — IDs auf Namespace-Präfix `wh40k_9e.necrons.protocol.<slug>` updaten
2. `wargear.yaml` — 3 `is_relic: true`-Einträge entfernen (orb_of_eternity, nanoscarab_casket, veil_of_darkness)
3. `wargear_abilities.yaml` — 3 Relic-Ability-Einträge entfernen (orb_of_eternity, nanoscarab_casket, veil_of_darkness)
4. `points.yaml` — `arkana:`-Abschnitt mit 12 Einträgen ergänzen (Kosten aus arkana.yaml)
5. `arkana.yaml` — `points_cost`-Felder entfernen (jetzt in points.yaml)

**Gruppe B — weapons.yaml Migration (größte Änderung):**

6. `weapons.yaml` — Alle Waffen auf `profiles:`-Liste umstellen:
   - Dual-Profile-Waffen (z.B. `staff_of_light_shooting` + `staff_of_light_melee`) → ein Objekt `staff_of_light` mit zwei Profilen
   - Single-Profile-Waffen → ein Profil in der Liste (nur einpacken)
   - `resurrection_orb` entfernen (kein Weapon)
   - Scope: alle Waffen in der Datei (~97 Einträge, davon ~20–25 Dual-Profile)

7. `units.yaml` — Referenzen anpassen:
   - `staff_of_light_shooting` / `staff_of_light_melee` → `staff_of_light`
   - Alle weiteren `_shooting`/`_melee`-Split-Refs finden und zusammenführen
   - `wargear_options.add: wh40k_9e.necrons.weapon.resurrection_orb` → `wh40k_9e.necrons.wargear.resurrection_orb`

**Gruppe C — Python (nach YAML-Bereinigung):**

8. `src/gameObjects/weapon.py` — Dataclass auf `profiles: list[WeaponProfile]` umstellen
9. `src/gameObjects/loader.py` — `_weapon_from_dict` auf Profile-Parsing umschreiben

### Betroffene Dateien (vollständige Liste)

| Datei | Aktion |
|-------|--------|
| `docs/spec/loader_contract.md` | ✅ Fertig (diese Session) |
| `docs/spec/army_builder.md` | Weapon-Schema + Roster-Format aktualisieren |
| `data/wh40k_9e/necrons/command_protocols.yaml` | IDs → Namespace-Präfix |
| `data/wh40k_9e/necrons/wargear.yaml` | 3 Relic-Einträge entfernen |
| `data/wh40k_9e/necrons/wargear_abilities.yaml` | 3 Relic-Ability-Einträge entfernen |
| `data/wh40k_9e/necrons/points.yaml` | `arkana:`-Abschnitt ergänzen |
| `data/wh40k_9e/necrons/arkana.yaml` | `points_cost`-Felder entfernen |
| `data/wh40k_9e/necrons/weapons.yaml` | Alle Waffen → `profiles:`-Liste; `resurrection_orb` entfernen |
| `data/wh40k_9e/necrons/units.yaml` | `_shooting`/`_melee`-Refs + `resurrection_orb`-Ref anpassen |
| `src/gameObjects/weapon.py` | Dataclass + `WeaponProfile` |
| `src/gameObjects/loader.py` | `_weapon_from_dict` auf Profile-Parsing |

---

## Offene Design-Fragen (aus loader_contract.md §6)

| # | Frage | Impact |
|---|-------|--------|
| 1 | `Unit`-Dataclass: Braucht es `weapon_groups: list[WeaponGroup]` für gemischte Einheiten (z.B. 7 Lychguard Schwert+Schild, 3 Kriegssense), oder reicht die flache `weapons: list[Weapon]`-Liste mit Combat-System-seitiger Auswahl? | `unit.py`, `fightPhase.py`, `shootingPhase.py` |
| 2 | Roster ohne passendem Catalog-Eintrag (unit_id nicht in units.yaml): `Army.unmatched` + Warnung oder `LoaderError`? | `load_army()` API |

---

## Danach: Schritt 3 + 4

**Schritt 3 — Forge World Einheiten** (nach Schema-Bereinigung):
Night Shroud, Canoptek Tombstalker, Canoptek Acanthrites, Tesseract Ark,
Canoptek Tomb Sentinel, Gauss Pylon, Seraptek Heavy Construct, Sentry Pylon.
Daten von Wahapedia fetchen (Subagent), als eigene Sektion in `units.yaml`.

**Schritt 4 — Loader implementieren (Ziel 5c)**:
`src/gameObjects/loader.py` vollständig auf neues Schema umschreiben.
Erst nach Freigabe des bereinigten Schemas.

---

## Wichtige Constraints
- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts
- dev-Branch — kein direktes Committen auf main
