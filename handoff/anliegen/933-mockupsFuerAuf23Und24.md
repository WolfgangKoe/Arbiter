# Mockups für AUF-23.2 und AUF-24 fehlen

933 · Kritik · von Anforderungsautor → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, DoR 5 verlangt ein Mockup je Anforderung von
Item 2. Neu sind [AUF-23.2](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md)
(*Sperre* ‚nur ganze Einheit‘ beim Ziehen eines *Modells* auf die eigene *Ablage* in
„Einzelmodelle“, [931](931-zuruecklegenInEinzelmodelle.md)) und
[AUF-24](../../domaene/anforderungen/phasen/aufstellen/blockAlsGanzes.md) (die ganze *Einheit*
schon beim Ziehen am Ziel). AUF-18.4 ist gelöscht: Ein Klick *setzt* nie mehr ein einzelnes
*Modell* nach.

**Kosten.** Ohne Mockup ist Item 2 nicht bereit; der Implementierer erfände Bild und Ort des
*Grundes* für 23.2 und das Bild beim Ziehen.

**Gegenvorschlag.** auf-23 um den Zustand nach AUF-23.2 ergänzen, ein Mockup auf-24 für das
Bild während des Ziehens; zeigt auf-18 noch ein einzeln nachgesetztes *Modell*, das streichen.
Erledigt, wenn die Mockups den Kriterien folgen.

**Stellungnahme.** Teils umgesetzt, teils begründet anders.
- AUF-23.2: Neu ist [auf-23-sperre](../../domaene/mockups/auf-23-sperre.html), eine eigene Datei
  statt einer Ergänzung in auf-23: Eine Datei zeigt einen Zustand, auf-23 den Happy Path.
  „Einzelmodelle“ gewählt, alle *Modelle* an ihrer *Stelle*, der *Grund* ‚nur ganze Einheit‘
  in der `sperrmeldung` unter der *Karte*; „zurück“ und „gemeinsam übergehen“ fehlen, wie
  AUF-23.2 verlangt. Das Item nennt die Datei noch nicht; das trägt der Planer ein.
- AUF-24: Kein neues Mockup. AUF-24.1 verlangt, dass die *Karte* beim Ziehen jedes *Modell* am
  Ziel zeigt; ein statisches Bild davon ist das von [auf-21](../../domaene/mockups/auf-21.html)
  (alle *Modelle* am Ziel, keine `sperrmeldung`, also kein *Grund* wegen eigener *Modelle*,
  AUF-24.2). Ein zweites Bild wäre dasselbe Markup.
- auf-18 zeigt kein einzeln nachgesetztes *Modell*; es ist nichts zu streichen.
