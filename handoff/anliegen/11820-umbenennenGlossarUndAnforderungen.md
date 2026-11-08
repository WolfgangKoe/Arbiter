# Umbenennen nach 7800: Glossar und Anforderungen

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Nach [7800](7800-karteUndEbeneBenennen.md) heißt *Karte* *Spielfeld* (F1 A), *Ebene*
bleibt mit *Einheitenebene* und *Modellebene* (F2 B). [Glossar](../../domaene/glossar.md) und
Anforderungen sagen noch *Karte* und *Ebene*; sie sind damit veraltet.

**Kosten.** Rund 64 Stellen *Karte* in 28 Dateien, 29 *Ebene* in 11, Glossar 12 Zeilen (Zahlen aus
7800). Kennungen bleiben. Ohne diesen Schritt fehlt die Umbenennung in Review 10
(Anliegen 11780).

**Gegenvorschlag.** Wann: nach „Planer: Item ruhigeKarte gelöscht“, vor „Reviewer: DoD über das
Inkrement“ (7800 F3: am Ende der Technikphase, ohne laufende Arbeit zu unterbrechen). Zuerst dieses
Anliegen, dann gleichzeitig [11821](11821-umbenennenTests.md),
[11822](11822-umbenennenCode.md), [11823](11823-umbenennenArchitektur.md). Wird
`formregeln/glossar.py` rot, solange Code *Karte* oder *Ebene* sagt, bleiben die alten Zeilen bis
dahin im Glossar und fallen danach weg. Items und Etappen benenne ich mit dir um.

**Stellungnahme.** Umgesetzt, Kennungen bleiben, Sinn unverändert.
- [Glossar](../../domaene/glossar.md): Zeile *Karte* entfällt, *Spielfeld* trägt „maßstäblich in
  *Zoll*, bildet den Spielstand ab“; *Ebene* bleibt als *Einheitenebene* oder *Modellebene*, beide
  neu. Der Auftrag erlaubt die rote Glossarprüfung bis 11822, darum fallen die alten Zeilen gleich
  weg. Code-Bezeichner `Einheitenebene` und `Modellebene` folgen der Anregung des Stakeholders
  (Unterklassen); entscheiden Architekt und Implementierer anders (11823), passe ich sie an.
- Anforderungen: „die ganze *Einheit* als *Ebene*“ heißt *Einheitenebene*, „deren *Ebene* ein
  *Modell* ist“ heißt „mit der *Modellebene* eines *Modells*“; „über die Kante der *Karte*“ heißt
  „über eine *Spielfeldkante*“ (die Zeichnung ist genau das *Spielfeld*), „leere *Karte*“ heißt
  „*Spielfeld*, wo kein *Modell* steht“.
- Nach Inhalt benannt, darum umbenannt: [spielfeld.md](../../domaene/anforderungen/querschnitt/spielfeld.md)
  (QUE-2), [ruhigesSpielfeld.md](../../domaene/anforderungen/querschnitt/ruhigesSpielfeld.md) (QUE-7),
  [loslassenWoDasSpielfeldZeigt.md](../../domaene/anforderungen/phasen/aufstellen/loslassenWoDasSpielfeldZeigt.md)
  (AUF-28), [loslassenNebenDemSpielfeld.md](../../domaene/anforderungen/phasen/bewegung/loslassenNebenDemSpielfeld.md)
  (BEW-20), mit neuen Überschriften. Für 11821: Testdateien und Kopfzeilen ziehen nach
  (`karteTest.py`, `ruhigeKarteTest.py`, `loslassenWoDieKarteZeigtTest.py`,
  `loslassenNebenDerKarteTest.py`); bis dahin sind Rückverfolgung und Spiegel rot.
- Offen für dich: Links auf die alten Dateinamen in 11500, 14462, 15100; *Karte* in
  `domaene/etappen/04-fahrzeugeUndJedeBaseform.md`.
