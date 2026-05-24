# Projektziele — Arbiter

## Vision
Arbiter ist ein WH40k-Battle-Tracker als Web-App (Flask), der Spieler durch eine Partie 9. Edition führt und Spielzustände (Leben, Phasen, Aktionen) verwaltet.

---

## Ziel 1 — Grundstruktur: Spielphasen-Navigation ✅ abgeschlossen

**Scope: minimal, keine Spiellogik, nur Layout und Navigation**

### Layout
```
┌──────────────────────────────────────────────────────┐
│  VP 0  CP 0      RUNDE 1 / 5      VP 0  CP 0        │
│                  BEFEHLSPHASE                        │
├─────────────┬────────────────────────┬───────────────┤
│  Armee 1    │   ←  1 / 7  →         │  Armee 2      │
│  (Sidebar)  │   [Spiel beenden]      │  (Sidebar)    │
└─────────────┴────────────────────────┴───────────────┘
```

### 40k 9e Spielphasen (in Reihenfolge)
1. Befehlsphase
2. Bewegungsphase
3. Psiphase
4. Fernkampfphase
5. Angriffphase
6. Nahkampfphase
7. Moralphase

### Umgesetzte Features
- [x] 3-Spalten-Layout: Sidebar links (Armee 1), Mitte (Navigation), Sidebar rechts (Armee 2)
- [x] Header mit Rundenzähler (Runde X / Y), Siegpunkten (VP) und Befehlspunkten (CP) je Armee
- [x] Phasen vorwärts und rückwärts durchklicken
- [x] Rundenübergang: Moralphase → nächste Runde Befehlsphase
- [x] Konfigurierbare maximale Rundenzahl (Standard: 5)
- [x] "Spiel beenden"-Button springt jederzeit zum Abschluss-Screen
- [x] Abschluss-Screen mit Rücksprung zur genauen Phase/Runde und Neustart-Button
- [x] 21 automatisierte Tests (domain + routes)
- [x] Streamlit-Prototyp bleibt unberührt in `prototype/`

---

## Ziel 2 — Armeeverwaltung (geplant)
Armeen aus YAML-Dateien laden und in den Sidebars anzeigen (Name, Fraktion, Einheiten).

## Ziel 3 — Fernkampfphase (geplant)
Schussangriffe berechnen (Treffer, Verwundung, Rüstung) analog Streamlit-Prototyp.

## Ziel 4 — Nahkampfphase (geplant)
Nahkampfangriffe berechnen.

## Ziel 5 — Moralphase & Spielende (geplant)
Moraltests, Siegbedingungen, Spielzusammenfassung.
