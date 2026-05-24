# Projektziele — Arbiter

## Vision
Arbiter ist ein WH40k-Battle-Tracker als Web-App (Flask), der Spieler durch eine Partie 9. Edition führt und Spielzustände (Leben, Phasen, Aktionen) verwaltet.

---

## Ziel 1 — Grundstruktur: Spielphasen-Navigation ✅ geplant
**Scope: minimal, keine Spiellogik, nur Layout und Navigation**

### Layout
```
┌─────────────┬──────────────────────┬─────────────────┐
│  Armee 1    │    Aktuelle Phase    │    Armee 2      │
│  (Sidebar)  │  [← Zurück] [Vor →] │    (Sidebar)    │
│             │                      │                 │
│  Name       │  z.B. Schussphase    │  Name           │
│  Fraktion   │                      │  Fraktion       │
└─────────────┴──────────────────────┴─────────────────┘
```

### 40k 9e Spielphasen (in Reihenfolge)
1. Befehlsphase
2. Bewegungsphase
3. Psychische Phase
4. Schussphase
5. Angriffphase
6. Kampfphase
7. Moralphase

### Akzeptanzkriterien
- [ ] Seite zeigt linke Sidebar (Armee 1), Mitte (Phase), rechte Sidebar (Armee 2)
- [ ] Phasen lassen sich vorwärts und rückwärts durchklicken
- [ ] Aktuelle Phase wird klar angezeigt (Name + Nummer)
- [ ] Kein JavaScript-Framework, kein State-Management, kein Spiellogik
- [ ] Streamlit-Prototyp bleibt unberührt

---

## Ziel 2 — Armeeverwaltung (geplant)
Armeen aus YAML-Dateien laden und in den Sidebars anzeigen.

## Ziel 3 — Schussphase (geplant)
Schussangriffe berechnen (Treffer, Verwundung, Rüstung) analog Streamlit-Prototype.

## Ziel 4 — Kampfphase (geplant)
Nahkampfangriffe berechnen.

## Ziel 5 — Moralphase & Spielende (geplant)
Moraltests, Siegbedingungen, Spielzusammenfassung.
