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

## 5b — Katalog neu aufbauen (Necrons) 🔄

- [x] `data/wh40k_9e/necrons/units.yaml` — 11 Einheiten, neues Format (army_builder.md v1), Weapon-Refs
- [x] `data/wh40k_9e/necrons/weapons.yaml` — 20 Waffenprofile, neues Format
- [x] `data/wh40k_9e/necrons/stratagems.yaml` — 15 Stratagems (Dynastic, Destroyer Cult, Canoptek, Vehicle)
- [ ] Wahapedia-Verifikation aller Statlines und Stratagem-Texte (Daten aus Trainingswissen, noch nicht curl-verifiziert)
- [ ] Fehlende Einheiten ergänzen (Triarch Praetorians, Ophydian Destroyers, Lokhust Destroyers, etc.)
- [ ] Orks: `units.yaml`, `weapons.yaml`, `stratagems.yaml` (nach Necron-Verifikation)
- [ ] Alte `army.yaml`-Dateien durch Katalog + Roster ablösen (nach Ziel 5c)

---

## 5c — Loader-Refactoring

- [ ] `gameObjects/loader.py` — liest Roster, löst IDs gegen Katalog auf
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

- [x] `data/wh40k_9e/necrons/stratagems.yaml` — angelegt (15 Stratagems, Wahapedia-Verifikation ausstehend)
- [ ] `data/wh40k_9e/orks/stratagems.yaml`
- [ ] Loader + `game_state` für Stratagems erweitern
- [ ] Stratagem-Anzeige: zunächst nur lesend (kein automatischer Effekt)
