# Schnittstelle und Lesbarkeit der Tests zur Schlacht und Normalen Bewegung

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: eine Prüfung ist rot; neuer Code verletzt Lesbarkeit, Es).
Ergänzt [4900](4900-vierTestsPruefenIhrKriteriumNicht.md), ohne dessen Punkte.
1. `ruff check` ist rot mit 7 Befunden, alle in den neuen Tests: I001
   [conftest.py:3](../../technik/tests/akzeptanz/conftest.py) und
   [schlachtrundenTest.py:3](../../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py),
   E501 conftest.py:274, [schlacht.py:60](../../technik/tests/akzeptanz/schlacht.py),
   [sperrenBeimZiehenTest.py:208](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py),
   ARG001 `boyz` ungenutzt in sperrenBeimZiehenTest.py:195, PLR2004 `== 2` in
   schlachtrundenTest.py:104. `ruff format --check` will drei Dateien umformen
   (normaleBewegungTest.py, schlachtrundenTest.py, schlacht.py).
2. `Modell.bewegungsweite` ist halb festgelegt. `spielerMit` und `Platz` in
   [handgriffe.py](../../technik/tests/akzeptanz/handgriffe.py) bauen `Modell(base=…)` ohne *B*.
   Ein Pflichtfeld macht jeden Test über die Fixture `aufstellung` rot; ein Standardwert wäre
   eine erfundene Zahl (Ich 1). Den Typ lässt der Handgriff `bewegungsweite()` offen, er hüllt
   nur `Fraction(…)` um das Attribut; nach S2 ist eine Länge `Fraction`, wie
   `Spielfeld.seitenlängen`.
3. Der Erwartungswert kommt aus dem Prüfling: `bewegungsweite(modell)` liest *B* am geprüften
   Objekt. Gibt der Katalog jedem *Modell* 5, zieht `testBew2_1JedesModellHatSeinEigenesB` den
   Overlord 5 statt 6 Zoll und bleibt grün. `letzteSchlachtrunde()` macht es richtig: aus der
   YAML, „nicht kopiert“.
4. Ein Name, zwei Bedeutungen: `stellenDerEinheit` heißt in handgriffe.py die Reihe, in die
   ein Test eine *Einheit* aufstellt (Liste), in schlacht.py die jetzigen *Stellen* (dict);
   `stellenAllerModelle` steht zweimal mit anderer Signatur. Was gemeint ist, zeigt erst der
   Import.
5. Der Name sagt etwas anderes als der Aufbau: `testBew1_1IstEinModellEbene…` und
   `testBew2_2IstEinModellEbene…` wählen die Boyz nicht aus; nach dem Glossar hat nur eine
   *ausgewählte* *Einheit* eine *Ebene*. Der Fall ist AUF-20.4, „nicht *ausgewählt*“.

**Kosten.** Mit 1 bleibt die DoD rot, gleich was der Implementierer tut. Mit 2 muss er eine
Zahl erfinden oder die Tests der *Aufstellung* rot machen. Mit 3 fällt ein falscher
Katalogwert nicht auf. Mit 4 und 5 liest man einen Test falsch, ohne den Import oder das
Glossar zu prüfen. Alles zusammen sind wenige Zeilen in den Testdateien.

**Gegenvorschlag.**
1. `ruff check --fix` und `ruff format` über die genannten Dateien, den Rest von Hand: `boyz`
   streichen, für `2` ein Name wie `zweiteSchlachtrunde`, Docstrings kürzen.
2. Schnittstelle `Modell(base, bewegungsweite: Fraction)` ohne Standardwert; `spielerMit` und
   `Platz` geben eine eigene Test-B als Konstante neben `durchmesserDerTestmodelle`.
3. `bewegungsweite(einheitenname)` in schlacht.py liest *B* aus `ausgangslage.yaml` wie
   `letzteSchlachtrunde()`; die Tests nennen die *Einheit* (`"Overlord"`).
4. Die neue Fassung heißt nach ihrer Bedeutung, etwa `jetzigeStellen(spielstand, einheit)`;
   `stellenAllerModelle` gibt es einmal in handgriffe.py, wenn die `Schlacht` wie die
   `Aufstellung` ihre `ausgangslage` nennt (sie braucht sie ohnehin für die letzte
   *Schlachtrunde* und die Armeelisten).
5. Umbenennen in `…IstDieEinheitNichtAusgewählt…`; ein Test mit gewählter Modell-*Ebene*
   bräuchte `ebeneWählen` an der `Schlacht`, das kein Kriterium hier verlangt.

**Stellungnahme.** Alle fünf Punkte angenommen und umgesetzt.
1. `ruff check` und `ruff format --check` über `tests/akzeptanz` sind sauber.
2. [handgriffe.py](../../technik/tests/akzeptanz/handgriffe.py): `Modell(base, bewegungsweite)`
   ohne Standardwert; `spielerMit` und `Platz` geben `bewegungsweiteDerTestmodelle`
   (`Fraction(5)`). Die Tests der *Aufstellung* sind bis dahin rot (`TypeError`).
3. [schlacht.py](../../technik/tests/akzeptanz/schlacht.py): `bewegungsweite("Overlord")` liest
   *B* aus `ausgangslage.yaml`; die Tests nennen die *Einheit*.
4. `stellenDerEinheit` der Schlacht heißt `jetzigeStellen`; `stellenAllerModelle` steht nur
   in handgriffe.py und liest `spielstand.ausgangslage`. Schnittstelle: Die `Schlacht`
   nennt ihre `ausgangslage` wie die `Aufstellung`.
5. Umbenannt in `testBew1_1IstDieEinheitNichtAusgewählt…` und
   `testBew2_2IstDieEinheitNichtAusgewählt…`.
