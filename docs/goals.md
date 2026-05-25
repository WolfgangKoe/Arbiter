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
- [ ] Einheit als „vernichtet" markieren wenn Wunden = 0

---

## Ziel 3 — Zentralbereich: Durchstich

> **Regelgrundlage:** [`docs/rules/schlachtrunde.md`](rules/schlachtrunde.md)  
> Jede Phase im Code entspricht einem Abschnitt dort. Vor der Implementierung einer Phase immer den zugehörigen Abschnitt einlesen.

Jede der 7 Phasen zeigt die wesentlichen Informationen, die laut Grundregeln in ihr benötigt werden. Keine Würfellogik — nur Struktur, Status-Anzeigen und Ablauf als Orientierung für den Spieler.

### Befehlsphase
→ Regelreferenz: [schlachtrunde.md — Befehlsphase](rules/schlachtrunde.md#1-befehlsphase)
- [ ] BP-Anzeige mit Button „+1 BP (Schlachtordnung)" für den aktiven Spieler
- [ ] Textkasten: „Handle etwaige phasenspezifische Regeln ab, dann weiter."

### Bewegungsphase
→ Regelreferenz: [schlachtrunde.md — Bewegungsphase](rules/schlachtrunde.md#2-bewegungsphase)
- [ ] Liste aller Einheiten des aktiven Spielers mit Bewegungswert (B)
- [ ] Statusbadge pro Einheit: Normale Bewegung / Vorrückt / Stationär / Rückzug (wählbar)
- [ ] Hinweis: Einheiten in Nahkampfreichweite können nur Stationär bleiben oder sich zurückziehen
- [ ] Einheiten, die Vorrückt oder Rückzug gewählt haben, als für Fernkampf/Angriff gesperrt markieren

### Psiphase
→ Regelreferenz: [schlachtrunde.md — Psiphase](rules/schlachtrunde.md#3-psiphase)
- [ ] Liste aller PSIONIKER-Einheiten des aktiven Spielers
- [ ] Pro Psioniker: verfügbare Psikräfte anzeigen (inkl. Warpenergiewert)
- [ ] Schmetterschlag immer vorhanden; weitere aus Datenblatt
- [ ] Statusanzeige: bereits manifestiert / noch nicht / gebannt

### Fernkampfphase
→ Regelreferenz: [schlachtrunde.md — Fernkampfphase](rules/schlachtrunde.md#4-fernkampfphase)
- [ ] Liste der schussfähigen Einheiten (nicht Vorrückt, nicht Rückzug — außer TITANISCH)
- [ ] Pro Einheit: Fernkampfwaffen mit Typ, Reichweite, S, DS, SW anzeigen
- [ ] Anzeige: „Im Nahkampf gebunden" wenn Einheit in Nahkampfreichweite

### Angriffsphase
→ Regelreferenz: [schlachtrunde.md — Angriffsphase](rules/schlachtrunde.md#5-angriffsphase)
- [ ] Liste der angriffsfähigen Einheiten (innerhalb 12 Zoll, nicht Vorrückt/Rückzug)
- [ ] Pro Einheit: mögliche Ziele anzeigen (feindliche Einheiten innerhalb 12 Zoll)
- [ ] Hinweis: Ziele müssen nicht sichtbar sein

### Nahkampfphase
→ Regelreferenz: [schlachtrunde.md — Nahkampfphase](rules/schlachtrunde.md#6-nahkampfphase)
- [ ] Anzeige: aktiver Spieler beginnt NICHT — Gegner wählt zuerst
- [ ] Liste aller nahkampffähigen Einheiten beider Seiten (in Nahkampfreichweite oder Angriffsbewegung ausgeführt)
- [ ] Hervorhebung: Einheiten, die eine Angriffsbewegung ausgeführt haben, kämpfen zuerst

### Moralphase
→ Regelreferenz: [schlachtrunde.md — Moralphase](rules/schlachtrunde.md#7-moralphase)
- [ ] Liste aller Einheiten, die in diesem Zug Modellverluste erlitten haben
- [ ] Pro betroffener Einheit: Moralwert (Ld) anzeigen
- [ ] Hinweis auf Testablauf: W6 + Verluste vs. Ld

---

## Ziel 4 — Zentralbereich: Phasenlogik

Jede Phase erhält vollständige Würfel- und Regellogik. Reihenfolge entspricht der Spielabfolge.

### Befehlsphase
- [ ] BP automatisch gutschreiben wenn Schlachtordnung aktiv
- [ ] Missionsregeln (konfigurierbar) in der Phase auslösen können

### Bewegungsphase
- [ ] Vorrückenwurf (W6) würfeln und auf B addieren
- [ ] Bewegungsstatus schreibt Einschränkungen in den State (gesperrt für Schuss/Angriff)
- [ ] Verstärkungen aufstellen: Einheit aus Reserve auf das Feld setzen (Position, Regeln)

### Psiphase
- [ ] Psitest würfeln (2W6 ≥ Warpenergiewert): bestanden / misslingt
- [ ] Doppel-1 / Doppel-6: Gefahren des Warp auslösen (W3 tödliche Verwundungen, ggf. Explosion)
- [ ] Psibanntest: Gegner würfelt 2W6 gegen Psitestergebnis
- [ ] Schmetterschlag-Schaden anwenden (W3 / W6 bei 11+)
- [ ] Warpenergiewert-Steigerung bei mehrfachem Schmetterschlag in einer Phase

### Fernkampfphase
- [ ] Ziel wählen (sichtbar + in Reichweite prüfen)
- [ ] Trefferwurf (W6 ≥ BF, Modifikator max. ±1)
- [ ] Verwundungswurf (W6 nach S-vs-T-Tabelle, Modifikator max. ±1)
- [ ] Attacke zuweisen (Spieler mit Zieleinheit; verwundetes Modell zuerst)
- [ ] Schutzwurf (W6 + DS ≥ RW) oder Rettungswurf
- [ ] Schaden anwenden (SW Lebenspunkte abziehen; überschüssiger Schaden verfällt)
- [ ] Tödliche Verwundungen gesondert abhandeln (kein Schutzwurf, überschüssiger Schaden übertragen)
- [ ] Schnelles Würfeln: gleiche Attacken zusammenfassen

### Angriffsphase
- [ ] Angriffswurf (2W6) würfeln
- [ ] Angriff erfolgreich wenn Reichweite bis in Nahkampfreichweite aller Ziele reicht
- [ ] Abwehrfeuer auslösen (nur unmodifizierter 6er trifft)
- [ ] Heroische Intervention: Gegner bewegt CHARAKTERMODELL bis 3 Zoll näher

### Nahkampfphase
- [ ] Nachrücken: bis 3 Zoll, muss näher am nächsten Feind enden
- [ ] Kämpfende Einheiten bestimmen (innerhalb 1 Zoll nach Nachrücken)
- [ ] Vollständige Attackenkette (KG → S vs T → Zuweisung → RW → SW)
- [ ] Abwechselnde Aktivierung korrekt umsetzen (Gegner beginnt; Angreifer zuerst)
- [ ] Neuordnen nach dem Kampf

### Moralphase
- [ ] Moraltest würfeln (W6 + Modellverluste vs. Ld)
- [ ] Modelle bei misslingendem Test entfernen (Differenz, mind. 1)
- [ ] Einheiten mit 1 Modell überspringen

---

## Ziel 5 — Zentralbereich: Armeeninteraktion

Phasenübergreifende Mechaniken, bei denen beide Spieler aktiv eingebunden sind.

- [ ] **Zielauswahl Fernkampf:** Angreifer wählt Einheit + Waffe; Verteidiger weist Attacken seinen Modellen zu (bei Mehrfachmodell-Einheiten)
- [ ] **Sichtlinie prüfen:** visueller Hinweis welche feindlichen Einheiten für eine schießende Einheit in Reichweite und sichtbar sind
- [ ] **Abwehrfeuer (Overwatch):** Gegner-Einheit schießt bei Angriffsansage zurück; nur 6er treffen
- [ ] **Psibann:** Gegner-Psioniker versucht Psikraft zu bannen — beide Spieler würfeln nacheinander
- [ ] **Heroische Intervention:** Gegner bewegt CHARAKTERMODELL in der eigenen Angriffsphase des aktiven Spielers
- [ ] **Alternating Activation (Nahkampf):** klare UI, wer gerade dran ist; Spielerwechsel nach jeder Einheit
- [ ] **Moraltest Zuschauen:** Gegner sieht welche Einheiten des aktiven Spielers gerade testen müssen
- [ ] **Regeln außerhalb der Phase:** Fähigkeiten die „wie in Fernkampfphase" oder „wie in Nahkampfphase" wirken — korrekt mit/ohne Gefechtsoptionen abhandeln

---

## Ziel 6 — Armeelisten aus Daten laden

Statt Hardcode: beide Armeen aus YAML/JSON laden.

- [ ] `data/` Verzeichnis mit Armeelisten (YAML)
- [ ] Beim Start Armee wählen oder laden
- [ ] Beliebige Einheitenzusammensetzung möglich

---

## Ziel 7 — Spielende & Auswertung

- [ ] VP-Bedingungen konfigurierbar
- [ ] Siegbedingungen prüfen (nach Runde 5 oder bei Vernichtung)
- [ ] Abschluss-Screen mit Zusammenfassung
