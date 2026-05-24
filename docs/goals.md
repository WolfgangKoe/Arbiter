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

## Ziel 2 — Einheitenstatus

Wunden und Modellverluste direkt auf den Karten verwalten.

- [ ] −1W / −D3 / −D6 / +1W auf jeder Einheitenkarte
- [ ] Wundbalken und Modellzahl live aktualisieren
- [ ] Einheit als "vernichtet" markieren wenn Wunden = 0

---

## Ziel 3 — Kampfphasen-Logik

Schussphase und Kampfphase mit vollständiger Würfelkette.

- [ ] Angreifer, Waffe, Ziel wählen
- [ ] Treffer (BS/WS) → Verwundung (S vs T) → Rettungswurf (SV − AP) → Schaden
- [ ] Ergebnis ins Kampfprotokoll schreiben und Wunden anwenden

---

## Ziel 4 — Armeelisten aus Daten laden

Statt Hardcode: beide Armeen aus YAML/JSON laden.

- [ ] `data/` Verzeichnis mit Armeelisten (YAML)
- [ ] Beim Start Armee wählen oder laden
- [ ] Beliebige Einheitenzusammensetzung möglich

---

## Ziel 5 — Spielende & Auswertung

- [ ] VP-Bedingungen konfigurierbar
- [ ] Siegbedingungen prüfen (nach Runde 5 oder bei Vernichtung)
- [ ] Abschluss-Screen mit Zusammenfassung
