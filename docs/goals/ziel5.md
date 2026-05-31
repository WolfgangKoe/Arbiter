# Ziel 5 — Setup & Datenlage 🔄

**Architektur-Entscheidung (2026-05-30):**

Zwei Quellen mit klar getrennter Verantwortung:

| Quelle | Rolle | Speicherort |
|--------|-------|-------------|
| BattleScribe `.rosz` | Roster — welche Einheiten, Modellzahl, Ausrüstungswahl | `data/rosters/<name>.yaml` |
| Wahapedia | Katalog — Stats, Waffen, Stratagems, Abilities (mechanisch verdrahtet) | `data/wh40k_9e/<fraktion>/` |

Roster referenziert nur Katalog-IDs. Der Loader löst auf. Einheit ohne Katalog-Eintrag → `unmatched`, nicht spielbar.

**Implizite Regel (muss explizit sein):**
Jede Einheit besitzt mindestens eine Nahkampfwaffe. Falls nicht explizit definiert, wird automatisch ergänzt:
`Close Combat Weapon: Range=Melee, Type=Melee, S=User, AP=0, D=1`

**Bestehende `army.yaml`-Dateien werden ersetzt** — zu fehlerhaft und strukturell veraltet (Stat-Duplikate, fehlende Waffen, keine Stratagems).

---

## 5a — Neue Datenstruktur & Spec ✅

- [x] `docs/spec/army_builder.md` — Roster-Format, Katalog-Schema, Loader-Vertrag, Unmatched-Handling
- [x] `docs/spec/setup.md` — Spielmodi-Regeln (Matched/Open/Crusade)
- [x] Roster-Format definiert: `data/rosters/<name>.yaml` (ID-basiert, keine Stat-Duplizierung)
- [x] Katalog-Schema definiert: neues Format in army_builder.md v1

---

## 5b — Katalog Necrons (Grunddaten) 🔄

Stand 2026-05-30 — verifiziert gegen Wahapedia:

| Datei | Status | Inhalt |
|-------|--------|--------|
| `units.yaml` | ⚠️ | 46 Einheiten — 5 fehlen, kein PL, keine Brackets |
| `weapons.yaml` | ⚠️ | 93 Waffen — 4 neue nötig für fehlende Einheiten |
| `stratagems.yaml` | ✅ | 59 Stratagems |
| `faction_abilities.yaml` | ✅ | 7 Abilities |
| `unit_abilities.yaml` | ⚠️ | 8 Abilities — ~10 neue nötig |
| `wargear_abilities.yaml` | ✅ | 12 Abilities |
| `wargear.yaml` | ✅ | 13 Items |
| `subfaction_abilities.yaml` | ✅ | 6 Dynastien |
| `command_protocols.yaml` | ✅ | 6 Protokolle |
| `warlord_traits.yaml` | ✅ | 13 Traits |
| `arkana.yaml` | ✅ | 12 Cryptek-Arkana |
| `relics.yaml` | ✅ | 6 Relikte |
| `weapon_abilities.yaml` | ✅ | 44 Abilities |
| `army_rules.yaml` | ✅ | Armeebau-Regeln |
| `points.yaml` | ❌ | Fehlt komplett |

Wahapedia-Verifikation aller Statlines und Stratagem-Texte: ✅ abgeschlossen (2026-05-30)

---

## 5b.1 — Necrons Datensatz vervollständigen 🔄

**Fehlende Einheiten (5 Stück → 51 gesamt):**

| Einheit | Role | PL | Punkte |
|---------|------|----|--------|
| Canoptek Plasmacyte | Elites | fetchen | fetchen |
| Hexmark Destroyer | Elites | fetchen | 65 |
| Transcendent C'tan | Elites | 14 | 230 |
| Obelisk | Lords of War | 17 | 270 |
| Convergence of Dominion | Fortification | 4 | 80/Modell |

**Battlefield Role Korrektur:** Triarch Stalker `[Heavy Support]` → `[Elites]`

**Damage Brackets (10 Einheiten mit wounds > 9):**
Triarch Stalker, Canoptek Doomstalker, Ghost Ark, Doomsday Ark, Night Scythe, Doom Scythe, Obelisk, The Silent King, Monolith, Tesseract Vault

**Neue Datenfelder:**
- `power_level` inline in allen 51 Einheiten
- `damage_bracket` für Einheiten > 9W
- `points.yaml` — neue Datei, 51 Einheiten + Non-Zero-Wargear

**Umsetzungsreihenfolge:**

- [ ] Datenbeschaffung: fehlende PL/Punkte/Brackets von Wahapedia fetchen
- [ ] `weapons.yaml` — 4 neue Waffen (transdimensional_abductor, monomolecular_proboscis, enmitic_disintegrator_pistol, crackling_tendrils)
- [ ] `unit_abilities.yaml` — ~10 neue Abilities für neue Einheiten
- [ ] `units.yaml` — power_level zu 46 Einheiten, Role fix, brackets zu 10 Einheiten, 5 neue Einheiten
- [ ] `points.yaml` — neue Datei erstellen
- [ ] `army_builder.md` — power_level, damage_bracket, points.yaml-Schema dokumentieren

**Forge World / Legends (außer Scope):** Night Shroud, Canoptek Tombstalker, Canoptek Acanthrites, Tesseract Ark, Canoptek Tomb Sentinel, Gauss Pylon, Seraptek Heavy Construct, Sentry Pylon.

---

## 5c — Loader-Refactoring

Erst nach Abschluss von 5b.1. Vollständige Lektüre von `src/gameObjects/loader.py` vor Planung.

- [ ] `gameObjects/loader.py` — liest Roster, löst IDs gegen Katalog auf
- [ ] `power_level`-Skalierung: PL × (aktuelle_modelle / models_min)
- [ ] `points.yaml` einbinden
- [ ] `damage_bracket` zur Laufzeit auflösen (nach Wounds-Stand der Einheit)
- [ ] Default-Nahkampfwaffe-Logik im Loader (immer ergänzen wenn fehlend)
- [ ] Unmatched-Einheiten: Warning im Setup, nicht spielbar
- [ ] Alle bestehenden Tests anpassen (neue Datenstruktur)

---

## 5d — BattleScribe Importer

BattleScribe-Format (recherchiert 2026-05-30):
- `.rosz` = ZIP mit einer `.ros`-Datei (UTF-8 XML), Python stdlib reicht
- XML-Namespace: `http://www.battlescribe.net/schema/rosterSchema`
- Alle Statlines direkt im XML (M/WS/BS/S/T/W/A/Ld/Save + Waffenprofile)
- `invuln_save` + FNP nur per Regex aus Ability-Text
- `oc` existiert in 9E-Daten nicht (10E-Stat) → Default 0
- Weapon-Attacks stecken im `Type`-String (`"Rapid Fire 2"` → 2 Attacks)

Implementierung:
- [ ] `tools/import_rosz.py` — parst `.rosz` XML → matched gegen Katalog → `data/rosters/<name>.yaml`
- [ ] Streamlit-Upload-UI im Setup-Screen integriert
- [ ] Sicherheit: Dateiformat-Validierung (`.rosz`/`.ros`), Max-Größe, XML-Namespace-Check
- [ ] Unmatched-Kategorie: Einheiten ohne Katalog-Treffer werden explizit geflaggt
- [ ] `invuln_save` + FNP via Regex aus Ability-Text extrahieren

---

## 5e — Setup-Screen Redesign

Matched Play Spielgrößen (aus Wahapedia):

| Spielgröße | Punkte | CP |
|---|---|---|
| Combat Patrol | 500 | 3 |
| Incursion | 1000 | 6 |
| Strike Force | 2000 | 12 |
| Onslaught | 3000 | 18 |

Implementierung:
- [ ] Spielmodus-Auswahl: Matched / Open / Crusade
- [ ] Spielgröße: Combat Patrol (500 Pkt) / Incursion (1000) / Strike Force (2000) / Onslaught (3000)
- [ ] Roster-Dropdown aus `data/rosters/` — P1-Wahl sperrt für P2 (keine doppelte Armeewahl)
- [ ] Erster Spieler festlegen
- [ ] Start-Button erst aktiv wenn alle Bedingungen erfüllt
- [ ] `game_state.init_state()` mit Spielmodus + Spielgröße + Roster-Pfaden erweitern

---

## 5f — Stratagems Proof of Concept

- [x] `data/wh40k_9e/necrons/stratagems.yaml` — 59 Stratagems, verifiziert (2026-05-30)
- [ ] `data/wh40k_9e/orks/stratagems.yaml`
- [ ] Loader + `game_state` für Stratagems erweitern
- [ ] Stratagem-Anzeige: zunächst nur lesend (kein automatischer Effekt)
