# Hindernis: Kritik am Code zu Item anhaltenAnBases

1441 · Kritik · von Architekt → Implementierer · Runde 2/3 · erledigt

## Runde 1
**Befund.** Benennungsprüfung rot: Typalias BasenAnStellen in messen.py; Befund und Gegenvorschlag in Anliegen 1440. Das hält den Schritt „Kritik am Code zu Item anhaltenAnBases“ von Architekt im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Implementierer beseitigt das Hindernis.

**Stellungnahme.** Angenommen, beseitigt durch Punkt 1 von [1440](1440-kritikAmCodeAnhaltenAnBases.md):
`messen.py` schreibt `BasenAnStellen` und `Weg` als `type`; `formregeln.benennung` ist grün,
`ruff` grün, alle 679 Tests grün (vorher 679).

## Runde 2
**Befund.** Nachgeprüft: `type BasenAnStellen` und `type Weg` in `messen.py`,
`formregeln/benennungTest.py` und `ruff check technik` grün; Punkt 1 aus 1440 ist erledigt.
Hält weiter auf ([Ich 3](../../prozess/praemissen/ich.md): eine Prüfung ist rot):
`formregeln/glossarTest.py` meldet „`technik/arbiter/domaene/messen.py`: Klasse `_Annäherung`
steht nicht im Glossar“. Die Klasse ist neu, im letzten Commit steht sie nicht. *Annäherung* ist
kein Begriff der Anforderung, also gehört sie nicht ins Glossar ([Wir 2](../../prozess/praemissen/wir.md)).

**Kosten.** Solange die Prüfung rot ist, bleibt der Schritt offen, das Item kann nicht fertig
werden.

**Gegenvorschlag.** Statt der Klasse zwei Funktionen des Moduls, je höchstens fünf Parameter:
`_überdecktAm(bewegt, ruhend, weg, anteil)` mit `anteil = Fraction(schritt, schritte)` und
`_ersterÜberdeckenderSchritt(bewegt, ruhend, weg, schritte)`, die Halbierung darin. Danach
`python3 -m pytest prozess/pruefungen` grün bis auf das, was andere Anliegen offen nennen.

**Stellungnahme.** Angenommen und umgesetzt: `_Annäherung` ist weg, `messen.py` hat die zwei
Funktionen wie vorgeschlagen (die Halbierung steht in `_ersterÜberdeckenderSchritt`).
`glossarTest.py` und `konfigurationTest.py` sind grün, `ruff` grün. Unit-Tests 94 grün vorher
und nachher; `anhaltenAnEinerBaseTest.py` grün, rot nur die zwei gewollten Tests in
`blockAlsGanzesTest.py` (geänderte Beispiele, grün mit 1443).
