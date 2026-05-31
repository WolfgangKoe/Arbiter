# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session gemacht wurde

Alle 6 Teile des Necrons-Datensatz-Abschlusses implementiert:

- **Teil A** — `weapons.yaml`: Gauntlet of the Conflagrator auf Pistol 1 / `*`-Stats / vollständigen Wahapedia-Text korrigiert; Synaptic Disintegrator Look-Out-Sir-Regel ergänzt; Voltaic Staff (Shooting + Melee) und Voidreaper als neue Relic-Waffen (`is_relic: true`) hinzugefügt
- **Teil B** — `weapon_abilities.yaml`: Neue Datei mit 44 structured abilities (Tesla, Extra Attacks, Blast, Invuln-Bypass, Auto-Hit, Half-Range, Unique)
- **Teil C** — `wargear.yaml`: 3 Relic-Items ergänzt (Orb of Eternity, Nanoscarab Casket, Veil of Darkness)
- **Teil D** — `wargear_abilities.yaml`: 3 structured Entries für die neuen Relic-Items
- **Teil E** — `relics.yaml`: Voidreaper `abilities_en` auf exakten Wahapedia-Wortlaut korrigiert
- **Teil F** — `army_rules.yaml`: Neue Datei mit Warlord-Anforderung, Dynastic Advisors, Silent King, Command Protocols, Matched-Play-Limits

---

## Aktueller Status Necrons-Datensatz

| Datei | Status |
|-------|--------|
| `units.yaml` | ✅ 46 Einheiten |
| `stratagems.yaml` | ✅ 59 Stratagems |
| `faction_abilities.yaml` | ✅ 7 abilities |
| `unit_abilities.yaml` | ✅ 8 abilities |
| `wargear_abilities.yaml` | ✅ 12 abilities (inkl. 3 neue Relic-Items) |
| `wargear.yaml` | ✅ 13 Items (inkl. 3 neue Relic-Items) |
| `subfaction_abilities.yaml` | ✅ 6 Dynastien |
| `command_protocols.yaml` | ✅ 6 Protokolle |
| `warlord_traits.yaml` | ✅ 13 Traits |
| `arkana.yaml` | ✅ 12 Cryptek-Arkana |
| `relics.yaml` | ✅ 6 Relikte — Voidreaper-Text korrigiert |
| `weapons.yaml` | ✅ 93 Waffen — Gauntlet + Synaptic Dis. korrigiert, Voltaic Staff + Voidreaper neu |
| `weapon_abilities.yaml` | ✅ 44 structured abilities (neue Datei) |
| `army_rules.yaml` | ✅ Armeebau-Regeln (neue Datei) |

**Datensatz vollständig.** Nächster Schritt: Ziel 5c — Loader Refactoring.

---

## Offene Kleinigkeit vor Ziel 5c

### relics.yaml — Source-Blöcke verschlanken

User-Feedback: Die `source:`-Blöcke in `relics.yaml` sind zu ausführlich. `capture_status` und `image_files` sind nicht nützlich.

**Aktuell (jeder Relikt-Eintrag):**
```yaml
    source:
      publication: Codex Necrons
      page: "66"
      capture_status: draft_from_user_image
      image_files:
        - IMG_3896.png
        - IMG_3897.png
```

**Soll so aussehen (schlank):**
```yaml
    source:
      publication: Codex Necrons 9e
      page: "66"
```

Betrifft alle 6 Relikte in `relics.yaml`. Schnelle Aufräumaktion vor dem Loader-Refactoring.

---

## Nächste Aufgabe: Ziel 5c — Loader Refactoring

Der Necrons-Datensatz ist vollständig. Jetzt den Loader aufräumen und auf die neuen YAML-Dateien ausrichten.

**Betroffene Datei:** `src/gameObjects/loader.py`

Der aktuelle Loader lädt `army.yaml` — er muss refactored werden, um den vollständigen Datensatz (units, weapons, wargear, abilities etc.) zu nutzen.

Vor dem Start: `loader.py` vollständig lesen und den aktuellen Zustand verstehen, dann Plan zeigen.

---

## Architektur-Kurzreferenz

```
src/gameObjects/loader.py     ← aktiv, lädt army.yaml (bis Ziel 5c)
data/wh40k_9e/necrons/        ← alle Necron-Daten (jetzt vollständig)
data/wh40k_9e/_shared/        ← detachment_types.yaml
```

## Wichtige Constraints
- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts
- dev-Branch — kein direktes Committen auf main
