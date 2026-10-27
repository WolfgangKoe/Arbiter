# Schlüssel einheitInBewegung entfällt

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: neuer Code verletzt die Architektur, hier den Vertrag). Nach
[5180](5180-annahmenZurBewegungsphase.md) F5 gibt es keine *Einheit in Bewegung* mehr
([Bewegung](../../technik/architektur/vertrag/bewegung.md), V15). Trotzdem verlangen
[ersterZugTest.py](../../technik/tests/akzeptanz/querschnitt/ersterZugTest.py), Zeile 112,
und die Tests zu BEW-1 und BEW-2 noch `einheitInBewegung`. Das Gleiche gilt für
`bewegungDerEinheitBeenden`, `Grund.weiterAlsB` und `weiterAlsBDesVertrags` in
[dienst.py](../../technik/tests/akzeptanz/dienst.py); `weiterAlsB.json` und `bewegung.json`
sind gelöscht.

**Kosten.** Eine Zeile in QUE-9.2. Die übrigen Stellen ändern sich ohnehin mit BEW-1 und
BEW-2. Bleibt die Zeile, muss der Implementierer einen Schlüssel bauen, der immer `null` ist.

**Gegenvorschlag.** Erst, wenn der Implementierer Item phasenUndSchlachtrunden grün hat:
Ich streiche den Schlüssel in [schlacht.md](../../technik/architektur/vertrag/schlacht.md)
und [schlacht.json](../../technik/architektur/vertrag/schlacht.json), du die Zeile 112.
Wenn der Anforderungsautor BEW-1 und BEW-2 neu gefasst hat, entfällt der Rest mit
[5240](5240-rundennummerUndBildBeimHaltenUeberB.md) und
[5260](5260-schlachttestsImportUndVertrag.md).

**Stellungnahme.** Angenommen und umgesetzt: Zeile 112 in ersterZugTest.py ist gestrichen,
`weiterAlsBDesVertrags` aus dienst.py entfernt. Die Tests zu BEW-1 und BEW-2 sind auf
BEW-1.5 bis 1.7 und BEW-2.5 bis 2.7 abgelöst und kennen weder `einheitInBewegung`,
`bewegungDerEinheitBeenden` noch `Grund.weiterAlsB`; BEW-3 und BEW-4 haben eigene Dateien.
Die Streichung in schlacht.md und schlacht.json bleibt beim Architekten.
