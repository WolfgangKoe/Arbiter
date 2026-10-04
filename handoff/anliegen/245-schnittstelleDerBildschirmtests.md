# Schnittstelle der Bildschirmtests zur Prüfung

245 · Fragen · von Testautor (Technik) → Architekt · Runde 1/3 · offen

## Runde 1
**Befund.** Die Tests zu QUE-2 und AUF-4 legen fest, was der Implementierer bauen muss. Bitte prüfen
(`technik/tests/akzeptanz/conftest.py`, `querschnitt/que2Test.py`, `phasen/aufstellen/auf4Test.py`):
- `arbiter.web.server.serverStarten(aufstellung)` liefert einen Server mit `.adresse`
  (`http://127.0.0.1:<Port>`) und `.beenden()`; er läuft im selben Prozess, `web/` wählt den Port.
- `web/` bekommt nur die `Aufstellung`. Es braucht `spielfeld`, `tiefen` und die Reihenfolge der
  Spieler als öffentliche Properties der Domäne (D3), die es heute nicht gibt.
- `python -m arbiter` ist ein eigener Prozess; die Adresse steht allein in der ersten Zeile von
  stdout, kein Banner davor. Der Test setzt `PYTHONPATH=technik` und `PYTHONUNBUFFERED=1`.
- Klassen wie in den Mockups: `.karte`, `.spielfeld`, `.aufstellungszone`, `.modell`,
  `.kopfzeileSpieler`, `.kopfzeileAnDerReihe`, `.armeeKarte`, `.armeeKartenName`,
  `.einheitenKarte`, `.einheitenKartenModelle` (nur die Zahl als Text), `.einheitenKartenAbzeichen`
  („in Aufstellung“).
- Karte: `rect` (x, y, width, height) und `circle` (cx, cy, r), alles in Zoll, exakt als
  `float(Fraction)` (B3).
- Messung: `getScreenCTM` (`a == d`, `b == c == 0`) und Bounding-Box je Zoll bei zwei
  Fenstergrößen; Farben als `getComputedStyle` (`fill`, bei der Ablage `color`).

**Kosten.** Ändert sich die Schnittstelle nach dem Implementieren, ändern sich Tests und Code.

**Gegenvorschlag.** Gib die Schnittstelle frei oder nenne, was du anders willst.

**Stellungnahme.**
