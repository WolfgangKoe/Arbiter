# Zwei Erklärungen in messen.py fehlen, ein Docstring in auswahl.py widerspricht dem Glossar

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf, denn der
geänderte Code verletzt Lesbarkeit ([Es 8](../../prozess/praemissen/es.md): „Der Code
erklärt sich selbst“), und [Plan 7](../plan.md) verlangt für Schritt 1: „Was ein Kommentar
erklärt, steht danach im Namen, in einem einzeiligen Docstring oder in der Architektur“.
Kein Verhalten hat sich geändert: `python3 -m pytest technik/tests` 620 bestanden;
`prozess/pruefungen` grün bis auf die fehlenden Tests von Item 2 (`auf23Test.py`), die nicht
hierher gehören. Die übrigen 46 Kommentare durften ersatzlos fallen: was sie sagten, steht
in S1 bis S3, V4, V5, V8, V10, O1, AUF-6 oder im Namen. Drei Stellen nicht:

1. `_ersterÜberdeckenderSchritt` in
   [messen.py](../../technik/arbiter/domaene/messen.py): Gestrichen ist die einzige
   Begründung, warum der Code richtig ist: Der Abstand der Mittelpunkte fällt bis zum
   nächsten Punkt des Wegs und steigt danach, darum reicht hinter ihm ein Blick auf `davor`
   und `danach`, und vor ihm ist die Überdeckung ab einem Schritt durchgehend, was
   `bisect_left` erst zulässig macht. [S3](../../technik/architektur.md#stelle-und-rechnen)
   nennt nur das Raster, nicht dieses Argument. Die Funktion hat keinen Docstring.
2. `_rückung` in derselben Datei: `max(von - vorn, 0) or min(bis - hinten, 0)` sagt nicht,
   was gilt, wenn die Bases breiter sind als die Fläche; gestrichen ist „passt beides nicht,
   gilt vorn“. Der Docstring von `rückungInDieFläche` („soweit die Bases zusammen
   hineinpassen“) deckt diesen Fall nicht.
3. Der neue Docstring von `modellAusgewählt` in
   [auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py) sagt „mit Ebene
   nur deren Modell“. Laut [Glossar](../../domaene/glossar.md) (*Ebene*) hat jede
   *ausgewählte* *Einheit* eine *Ebene*, oft die ganze *Einheit*; dann sind alle ihre
   *Modelle* ausgewählt. Der Satz verspricht das Gegenteil des Codes.

**Kosten.** Ohne 1 hält der nächste Leser das `bisect_left` über `range(davor)` für
willkürlich und „vereinfacht“ es zu einer Schleife oder bricht die Monotonie, die er nicht
kennt; Mutanten in diesen Zeilen sind ohne Wissen um das Argument schwer zu beurteilen. Ohne
2 liest sich `or` auf `Fraction` wie ein Versehen. 3 führt beim Entflechten der *Auswahl*
(1652, gleiches Item) in die Irre. Zusammen drei Docstrings, am Bildschirm nichts.

**Gegenvorschlag.** Je ein einzeiliger Docstring, etwa:
1. `"""Der erste Schritt mit Überdeckung: Bis zum nächsten Punkt des Wegs fällt der Abstand, dann steigt er."""`
   (oder kürzer; geht es nicht in eine Zeile, ein Satz in S3, auf den der Docstring zeigt;
   dann Architekt). Ein Name wie `schrittVorDemNächstenPunkt` statt `davor` trägt den Rest.
2. `"""Der Weg einer Seite in die Grenzen; passen beide Seiten nicht, gilt vorn."""`
3. `"""Alle Modelle der ausgewählten Einheit; ist ein Modell die Ebene, nur dieses (AUF-5.7, AUF-25.4)."""`

**Stellungnahme.** Angenommen, alle drei. 1 und 2 als einzeilige Docstrings in
[messen.py](../../technik/arbiter/domaene/messen.py) (`_ersterÜberdeckenderSchritt`, `_rückung`),
3 in [auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py) im Wortlaut des
Gegenvorschlags, gekürzt auf 100 Zeichen. Die Umbenennung `davor` bleibt aus: der Docstring
trägt das Argument, ein Namenswechsel wäre Geschmack.
