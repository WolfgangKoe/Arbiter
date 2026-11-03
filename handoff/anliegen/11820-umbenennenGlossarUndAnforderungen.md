# Umbenennen nach 7800: Glossar und Anforderungen

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

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

**Stellungnahme.**
