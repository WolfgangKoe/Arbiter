# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Aktueller Status Necrons-Datensatz

| Datei | Status |
|-------|--------|
| `units.yaml` | ✅ 51 Einheiten, PL bei allen, Brackets bei 10, 5 neue Einheiten |
| `weapons.yaml` | ⚠️ 97 Waffen — aber Dual-Profile-Waffen als 2 Objekte statt `profiles`-Liste |
| `stratagems.yaml` | ✅ 59 Stratagems |
| `faction_abilities.yaml` | ✅ |
| `unit_abilities.yaml` | ✅ 8 + 13 neue Abilities |
| `wargear_abilities.yaml` | ✅ |
| `wargear.yaml` | ⚠️ Struktur unklar für Loader |
| `subfaction_abilities.yaml` | ✅ 6 Dynastien |
| `command_protocols.yaml` | ⚠️ Struktur unklar für Loader |
| `warlord_traits.yaml` | ⚠️ Struktur unklar für Loader |
| `arkana.yaml` | ⚠️ Struktur unklar für Loader |
| `relics.yaml` | ⚠️ Struktur unklar für Loader |
| `weapon_abilities.yaml` | ✅ |
| `army_rules.yaml` | ✅ |
| `points.yaml` | ⚠️ Existiert — aber Wargear-Optionen mit Kosten fehlen noch |

**Forge World / Legends Einheiten:** noch nicht importiert (bewusst zurückgestellt)

---

## Ziel dieser Session: Ziel-5-Architektur

**Kurzfassung:** Der Datensatz ist inhaltlich weit, aber die YAML-Strukturen sind organisch gewachsen — nie vom Loader her gedacht. Bevor 5c (Loader) implementiert wird, muss die Architektur klar sein.

Vollständige Analyse und Schulden-Diagnose: `docs/work/ziel5_architektur_review.md`

---

### Schritt 1 — Loader-Vertrag definieren (Hauptaufgabe)

**Vor allem anderen:** Diese Fragen beantworten und in `docs/spec/army_builder.md` festhalten.

**A. Was liest der Loader zur Laufzeit?**

Unklar bei: `wargear.yaml`, `arkana.yaml`, `relics.yaml`, `warlord_traits.yaml`, `command_protocols.yaml`

Fragen:
- Wargear-Optionen stehen in `units.yaml` — was ist in `wargear.yaml` *zusätzlich*?
- Arkana: sind das Crusade-only-Daten oder auch Matched Play relevant?
- Relics / Warlord Traits: wann werden sie geladen — immer, oder nur bei Crusade?
- Command Protocols: wann getriggert — sind das Faction Abilities oder eigene Mechanik?

**B. Welche Daten sind spielmechanisch aktiv vs. nur Anzeige?**

Spielmechanisch aktiv (Loader braucht sie zur Laufzeit):
- Units, Weapons, Points, Damage Brackets, Stratagems (CP-Kosten)

Nur Anzeige (Loader kann lazy laden):
- Warlord Traits, Relics, Arkana, Wargear-Beschreibungen

**C. Vollständige Feldliste pro Katalog-Datei**
Keine "könnte nützlich sein"-Felder — nur was der Loader braucht.

---

### Schritt 2 — Schema-Bereinigung

Nach Freigabe des Loader-Vertrags:

**weapons.yaml:** Dual-Profile-Waffen zusammenführen

Aktuell (falsch):
```yaml
- id: wh40k_9e.necrons.weapon.staff_of_light_shooting
- id: wh40k_9e.necrons.weapon.staff_of_light_melee
```

Ziel (korrekt):
```yaml
- id: wh40k_9e.necrons.weapon.staff_of_light
  name_en: Staff of Light
  profiles:
    - name: Shooting
      weapon_type: Assault
      range_inches: 18
      attacks: "3"
      strength: "5"
      ap: "-2"
      damage: "1"
      is_melee: false
    - name: Melee
      weapon_type: Melee
      range_inches: 0
      attacks: "*"
      strength: "User"
      ap: "-2"
      damage: "1"
      is_melee: true
```

Waffen mit nur einem Profil: ebenfalls `profiles`-Liste mit einem Eintrag. Einheitlich.
Scope: ~50 Waffen betroffen. Referenzen in `units.yaml` müssen angepasst werden (kein `_shooting`/`_melee` mehr).

**Alle anderen Katalog-Dateien:** Struktur auf Loader-Vertrag ausrichten.

**points.yaml:** Wargear-Optionen mit Kosten > 0 ergänzen.

---

### Schritt 3 — Forge World Einheiten ergänzen

Nach Schema-Bereinigung: FW-Einheiten als eigene Sektion in `units.yaml`.

Kandidaten (Wahapedia, mit FW-Symbol):
Night Shroud, Canoptek Tombstalker, Canoptek Acanthrites,
Tesseract Ark, Canoptek Tomb Sentinel, Gauss Pylon,
Seraptek Heavy Construct, Sentry Pylon.

Daten von Wahapedia fetchen (Subagent).

---

### Schritt 4 — Loader implementieren (Ziel 5c)

Erst wenn Schema stabil und freigegeben:
- `src/gameObjects/loader.py` vollständig lesen
- Plan zeigen, Freigabe abwarten
- Dann implementieren

---

## Betroffene Dateien (Schritt 2)

| Datei | Aktion |
|-------|--------|
| `docs/spec/army_builder.md` | Loader-Vertrag vollständig ausformulieren |
| `data/wh40k_9e/necrons/weapons.yaml` | Dual-Profile-Waffen → `profiles`-Liste |
| `data/wh40k_9e/necrons/units.yaml` | Waffen-Referenzen anpassen (kein `_shooting`/`_melee`) |
| `data/wh40k_9e/necrons/points.yaml` | Wargear-Kosten ergänzen |
| Alle anderen YAML-Dateien | Schema-Bereinigung nach Loader-Vertrag |

---

## Wichtige Constraints
- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts
- dev-Branch — kein direktes Committen auf main
