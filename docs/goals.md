# Projektziele — Arbiter

## Vision

Arbiter ist ein digitaler Spielbegleiter für WH40k 9. Edition (Streamlit).  
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

---

## Ziel 1 — Grundstruktur & Layout ✅

3-Spalten-Layout mit eingeklappten Einheitenkarten, Phasen-Stepper und VP/CP-Header.

- [x] Header: VP · CP · Runde · aktive Phase · aktive Fraktion
- [x] Linke Spalte: Necron-Einheiten als Akkordeon (eingeklappt)
- [x] Rechte Spalte: Ork-Einheiten als Akkordeon (eingeklappt)
- [x] Mitte: Phasen-Stepper + leere Phasenfläche + Navigation + Kampfprotokoll
- [x] Phasen vorwärts/rückwärts, Rundenübergang, Spielreset

---

## Ziel 2 — Einheitenstatus ✅

Wunden und Modellverluste direkt auf den Karten verwalten.

- [x] 6 Schaden-Buttons (−3/−2/−1/+1/+2/+3) auf jeder Einheitenkarte
- [x] −1 (tödliche Wunde, golden): läuft auf nächstes Modell über
- [x] −2/−3 (normaler Schaden): wird am HP des aktuellen Modells gekappt
- [x] Drei Anzeigemodi: 1 Modell / Mehrere à 1LP / Mehrere mit mehreren LP (2 Balken)
- [x] Einheit als „vernichtet" markieren wenn Modellzahl = 0

---

## Ziel 3 — Durchstich

> **Regelgrundlage:** [`docs/rules/schlachtrunde.md`](rules/schlachtrunde.md) ist bindend.  
> Vor der Implementierung einer Phase immer den zugehörigen Abschnitt einlesen.

Kein Würfeln — nur Struktur, Zustandsanzeigen und Ablauf als Orientierung für den Spieler.

### Kernprinzipien

**Einheitenkarte** — zwei Sektionen:
- **Permanent** (immer sichtbar): HP-Balken, Modellzahl, State-Badges (z.B. „Vorgerückt", „Im Nahkampf", „Reserve")
- **Dynamisch** (phasenabhängig): nur die laut `schlachtrunde.md` relevanten Profilwerte. Hat eine Einheit in einer Phase keine Aktion: „Keine Aktion möglich."

**Zentralbereich** — dreistufig:
1. Keine Einheit gewählt → Phasenübersicht + Regelzusammenfassung
2. Einheit gewählt (aktiver Spieler) → mögliche Aktionen für diese Einheit
3. Zwei Einheiten gewählt (z.B. Schütze + Ziel) → Interaktionssequenz

**Einheitenstate** — wird um folgende Felder erweitert:
- `movement_status`: `normal` | `advanced` | `stationary` | `retreated`
- `in_melee`: bool
- `in_reserve`: bool
- `acted_this_phase`: bool

**Protokoll** — persistent als JSON in `data/log/`: Runde, Phase, Einheit, Aktion.

---

### Setup-Phase (vor der Schlachtrunde)
→ Regelreferenz: [schlachtrunde.md — Vor dem Spiel](rules/schlachtrunde.md)

- [ ] Startspieler manuell bestimmen → Sidebars füllen sich korrekt (aktiver Spieler links)
- [ ] Aufstellungsstatus pro Einheit wählen: Normal / Stationär / Reserve
- [ ] Einheiten in Reserve: erst ab Runde 2 verfügbar
- [ ] Setup-Zusammenfassung jederzeit einsehbar (eingeklappt im Zentralbereich)

### Befehlsphase
→ Regelreferenz: [schlachtrunde.md — Befehlsphase](rules/schlachtrunde.md#1-befehlsphase)

- [ ] CP +1 Button für aktiven Spieler
- [ ] Hinweistext: phasenspezifische Regeln abhandeln
- [ ] Dynamische Karte: keine phasenspezifischen Profilwerte (nur State-Badges)

### Bewegungsphase
→ Regelreferenz: [schlachtrunde.md — Bewegungsphase](rules/schlachtrunde.md#2-bewegungsphase)

- [ ] Einheit wählen → Bewegungsstatus setzen: Normal / Vorgerückt / Stationär / Rückzug
- [ ] Dynamische Karte: M-Wert anzeigen
- [ ] Einheiten in Nahkampfreichweite (`in_melee = true`): nur Stationär oder Rückzug möglich
- [ ] Vorgerückt / Rückzug → `movement_status` sperrt Einheit für Fernkampf und Angriff

### Psiphase
→ Regelreferenz: [schlachtrunde.md — Psiphase](rules/schlachtrunde.md#3-psiphase)

- [ ] Nur PSIONIKER-Einheiten aktiv, Rest: „Keine Aktion möglich"
- [ ] Dynamische Karte: Psikräfte + Warpenergiewert anzeigen
- [ ] Status pro Kraft: manifestiert / nicht manifestiert / gebannt

### Fernkampfphase
→ Regelreferenz: [schlachtrunde.md — Fernkampfphase](rules/schlachtrunde.md#4-fernkampfphase)

- [ ] Schütze wählen (aktiver Spieler) → Ziel wählen (Gegner-Sidebar)
- [ ] Dynamische Karte Schütze: Fernkampfwaffen mit Profil
- [ ] Dynamische Karte Ziel: T · Sv · ++ anzeigen
- [ ] Zentralbereich: Sequenzübersicht (Treffer → Verwundung → Rettung → Schaden), noch ohne Würfel
- [ ] Einheiten ohne Fernkampfwaffe / Vorgerückt / Rückzug: „Keine Aktion möglich"
- [ ] Im Nahkampf gebundene Einheiten entsprechend markieren

### Angriffsphase
→ Regelreferenz: [schlachtrunde.md — Angriffsphase](rules/schlachtrunde.md#5-angriffsphase)

- [ ] Angreifer wählen → Ziele in Reichweite (≤ 12 Zoll) anzeigen
- [ ] Angriff bestätigen → `in_melee = true` für Angreifer und Ziel (nach erfolgreichem Angriff)
- [ ] Einheiten, die Vorgerückt / Rückzug: „Keine Aktion möglich"
- [ ] Dynamische Karte: keine spezifischen Profilwerte (State-Badges relevant)

### Nahkampfphase
→ Regelreferenz: [schlachtrunde.md — Nahkampfphase](rules/schlachtrunde.md#6-nahkampfphase)

- [ ] Reihenfolge anzeigen: Einheiten mit Angriff zuerst, dann Gegner beginnt
- [ ] Dynamische Karte: Nahkampfwaffen mit Profil
- [ ] Einheiten ohne `in_melee` und ohne Angriff: „Keine Aktion möglich"
- [ ] Sequenzübersicht analog Fernkampf (noch ohne Würfel)

### Moralphase
→ Regelreferenz: [schlachtrunde.md — Moralphase](rules/schlachtrunde.md#7-moralphase)

- [ ] Einheiten mit Verlusten in dieser Runde auflisten
- [ ] Ld-Wert pro Einheit anzeigen
- [ ] Einheit mit 1 Modell: automatisch bestanden, überspringen
- [ ] Dynamische Karte: Ld-Wert anzeigen

---

## Nächste Schritte (nach Ziel 3)

**Armeelisten aus Daten laden** — Einheiten und Werte werden aus YAML geladen statt hart im Code verdrahtet. Ziel: beliebige Armeen spielen können.

- [ ] `data/wh40k_9e/necrons/units.yaml` und `data/wh40k_9e/orks/units.yaml`
- [ ] Generischer YAML-Loader in `src/`
- [ ] Hardcodierte Listen aus `models.py` entfernen
- [ ] Einheitenlogik so abstrahieren, dass sie armeenunabhängig funktioniert

**Spielende & Auswertung**

- [ ] VP-Bedingungen konfigurierbar
- [ ] Siegbedingungen prüfen (nach Runde 5 oder bei Vernichtung)
- [ ] Abschluss-Screen mit Zusammenfassung
- [ ] Fortlaufendes Log aus `data/log/` anzeigen
