# Ziel 5 — Architektur-Review (2026-05-31)

## Ausgangslage

Der Necrons-Datensatz ist inhaltlich weitgehend vollständig (51 Einheiten, PL, Punkte, Brackets),
aber die YAML-Struktur wurde nie vom Loader her gedacht — sie ist organisch session-weise gewachsen.
Bevor Ziel 5c (Loader) umgesetzt wird, muss die Datenstruktur unified und konsistent sein.

---

## Identifizierte Schulden

### 1. Dual-Profile-Waffen — falsche Granularität

**Aktueller Zustand:**
```yaml
- id: wh40k_9e.necrons.weapon.staff_of_light_shooting
  weapon_type: Assault
  ...
- id: wh40k_9e.necrons.weapon.staff_of_light_melee
  weapon_type: Melee
  ...
```

**Problem:** Waffen mit Nah- und Fernkampfprofil werden als zwei separate Objekte gespeichert.
Das `_shooting`/`_melee`-Split ist ein Relikt, nie bewusst entschieden.
Der Codex zeigt sie als *eine* Waffe mit zwei Profilen.

**Ziel:**
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

Waffen mit nur einem Profil erhalten ein `profiles`-Array mit einem Eintrag.
Einheitlich. Kein `_shooting`/`_melee`-Suffix mehr.

Scope: ~50 Waffen betroffen (alle mit Doppelprofil). Einfache Migration.

---

### 2. Unvollständige `points.yaml`

Aktuell fehlen:
- Wargear-Upgrades mit Kosten (z.B. Heat Ray-Varianten, Gloom Prism etc.)
- Cryptek-Arkana (12 Einträge in arkana.yaml — haben sie Punktkosten?)
- Relics (gratis im Matched Play → alle 0, muss dokumentiert sein)
- Warlord Traits (gratis → alle 0)
- Stratagems (CP-Kosten gehören in stratagems.yaml, nicht points.yaml)

Klärungsbedarf: Welche Dinge haben Punktkosten > 0 in 9E Matched Play?
- Wargear-Optionen: Resurrection Orb (25 Pkt) ist bekannt, andere?
- Arkana: Cryptek-Arkana kosten 0 Punkte (sind Crusade-Mechanik)

---

### 3. Inkonsistente Struktur der Katalog-Dateien

Die folgenden Dateien haben keine einheitliche Struktur im Hinblick auf den Loader:

| Datei | Problem |
|-------|---------|
| `arkana.yaml` | Unklares Format — wie referenziert der Loader das? |
| `command_protocols.yaml` | Eigene Struktur, unklar wie mit Einheiten verknüpft |
| `relics.yaml` | Wie werden Relics einer Einheit zugewiesen? |
| `warlord_traits.yaml` | Dito |
| `wargear.yaml` | Referenziert von units.yaml, aber Schema unklar |
| `stratagems.yaml` | Wie werden Stratagems im Spiel verfügbar gemacht? |

**Kernfrage:** Welche Katalog-Dateien liest der Loader *aktiv* zur Laufzeit,
und welche sind nur Referenz-/Anzeigedaten?

---

### 4. Forge World / Legends (noch nicht importiert)

Entschieden: Diese Einheiten sollen nach der Architektur-Session ergänzt werden.
Separat als Abschnitt in `units.yaml` (eigene Sektion mit Kommentar).

Kandidaten (sichtbar in Wahapedia Army List, mit FW-Symbol):
Night Shroud, Canoptek Tombstalker, Canoptek Acanthrites,
Tesseract Ark, Canoptek Tomb Sentinel, Gauss Pylon,
Seraptek Heavy Construct, Sentry Pylon.

---

## Plan für die Architektur-Session

### Schritt 1 — Loader-Vertrag definieren (Hauptaufgabe)

Fragen, die beantwortet werden müssen:

**A. Was liest der Loader zur Laufzeit?**
- `units.yaml` → definitiv
- `weapons.yaml` → definitiv (per Referenz aus units.yaml)
- `points.yaml` → definitiv (für Matched Play)
- `stratagems.yaml` → ja, für Stratagem-Anzeige
- `wargear.yaml` → wie? Wargear-Optionen stehen in units.yaml — was ist in wargear.yaml zusätzlich?
- `arkana.yaml`, `relics.yaml`, `warlord_traits.yaml` → wann und wie?
- `command_protocols.yaml` → wann triggered?

**B. Welche Felder braucht der Loader an jeder Einheit?**
Genau klären — kein "könnte nützlich sein".

**C. Welche Daten werden nur angezeigt (read-only), welche sind spielmechanisch aktiv?**

### Schritt 2 — Schema-Bereinigung

Nach Klärung der Fragen aus Schritt 1:
- `weapons.yaml`: Dual-Profile-Waffen zusammenführen
- Alle Katalog-Dateien auf einheitliches ID-Schema und Struktur bringen
- `points.yaml` vervollständigen (Wargear-Optionen mit Kosten)
- `army_builder.md` als Single Source of Truth aktualisieren

### Schritt 3 — Forge World Einheiten

Nach Schema-Bereinigung: FW-Einheiten als eigene Sektion in units.yaml ergänzen.

### Schritt 4 — Loader implementieren (Ziel 5c)

Erst wenn Schema stabil ist:
`src/gameObjects/loader.py` refactoren.

---

## Empfohlener Startprompt für die Architektur-Session

```
Lies zuerst:
- docs/work/ziel5_architektur_review.md  ← dieser Plan
- docs/spec/army_builder.md              ← aktueller Loader-Vertrag
- data/wh40k_9e/necrons/                 ← alle YAML-Dateien (kurz überfliegen)

Dann: Beantworte die offenen Loader-Fragen aus Schritt 1.
Ziel ist ein vollständiger, widerspruchsfreier Loader-Vertrag in army_builder.md,
der als Basis für die Schema-Bereinigung aller YAML-Dateien dient.
Kein Code schreiben. Erst Design, dann Freigabe.
```
