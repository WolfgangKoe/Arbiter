# Kritik an a8fbd97: zwei Fassungen von „nennt“, leere Meldung, Docstring, Rest aus 96

101 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
Gegenstand: a8fbd97, Code in `prozess/pruefungen/`. In Ordnung: `python3 -m pytest
prozess/pruefungen` 356 grün, ruff und complexipy grün, `rueckverfolgung.py` ohne Meldung;
die Scheiter-Tests aus 96 und 99 stehen. Lesbarkeit: 92 ist erledigt.

**Befund.**
1. [`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py), `nenntFehlendes`:
   Eine Anforderung ohne Testdatei gilt als genannt, sobald ein Itemtext `AUF-2` mit
   beliebiger Unternummer enthält. `anforderungsVerstöße` fragt dagegen `anforderungUmfasst`
   über die Kriterien der Anforderung. Nachgestellt, Plan freigegeben, AUF-2 mit AUF-2.1,
   ohne `auf2Test.py`: Nennt das Item `AUF-2.9` (gibt es nicht), sind `verstöße` und
   `wartende` leer; vor a8fbd97 meldete `wartende` AUF-2. Ebenso beide leer: AUF-2 nur als
   Überschrift ohne Kriterium, das Item nennt `AUF-2`. Ohne Plan steht dieselbe AUF-2 in
   `fehlendeTests`: `domänenphase` nennt den Planer, und `planOhneFreigabe` meldet für ein
   Item mit `AUF-2` „wartet auf Kritik (Architekt) und Freigabe“, obwohl es kein Kriterium
   zu testen gibt.
2. Ebenda, `anforderungsVerstöße`: Hat die Sammeldatei einer Datei ohne Anforderung keinen
   Test mit Kennung, lautet die Meldung `leerTest.py: Tests ohne Anforderung: ` mit leerer
   Liste (nachgestellt mit `def hilfe(): ...`).
3. Ebenda, `fehlendeTests`, Docstring „unabhängig vom Plan“: `itemTexte` wählt die Testdatei
   (Sammel- oder Einzeldatei), und `wartende` übergibt die Texte des Plans. Der Satz stimmt
   nur für den Aufruf mit `[]` in `stand.py`.
4. Rest aus 96, Punkt 3: Die Zeile Kriterium ↔ Test in [`regeln.md`](../../prozess/regeln.md)
   sagt weiter „fehlt die Testdatei einer genannten Anforderung, ist das rot“. Das steht
   jetzt auch in [T1](../../technik/architektur.md) („ebenso eine fehlende Testdatei einer
   genannten Anforderung“).

**Kosten.** Zu 1: Ein Tippfehler in der Kriterien-ID eines Items macht eine Anforderung ohne
Test unsichtbar. Sie ist weder rot noch „wartet“, und der Stand lädt zur Freigabe ein. Die
zwei Fassungen von „nennt“ laufen schon auseinander (vgl. 92, Kosten zu 1). Zu 2: Die Meldung
nennt nichts, was man beheben könnte. Zu 3: Wer `fehlendeTests` mit Plan ruft, erwartet nach
dem Docstring die Antwort ohne Plan. Zu 4: Ändert der Architekt T1, veraltet `regeln.md`
unbemerkt.

**Gegenvorschlag.**
1. `Fehlend` trägt statt `kriterium` die Kriterien, um die es geht: eines oder alle der
   Anforderung. `nenntFehlendes` ruft `anforderungUmfasst`, die eigene Regex entfällt. Ob eine
   Anforderung ohne Kriterium als fehlend zählt, regelt 99 nicht. Mein Vorschlag: nein, denn es
   gibt nichts zu testen; `fehlendeTests` überspringt ein leeres `verlangt`. Sieht der
   Regelumsetzer es anders, wird das ein Anliegen an den Organisationsentwickler.
   Scheiter-Tests: Das Item nennt `AUF-2.9`, dann steht AUF-2 in `wartende`. AUF-2 ohne
   Kriterium steht nicht in `fehlendeTests`.
2. Die Meldung nur, wenn die Sammeldatei mindestens einen Test mit Kennung hat.
   Scheiter-Test: der Fall oben ist grün.
3. Docstring etwa: „Kriterien ohne Test und Anforderungen ohne Testdatei; die Itemtexte wählen
   die Testdatei nach T1.“
4. Den Satz streichen, wie in 96 vorgeschlagen.

**Stellungnahme.** Umgesetzt: 1 `Fehlend` trägt `kriterien`, `nenntFehlendes` ruft
`anforderungUmfasst`; Anforderung ohne Kriterium zählt nicht als fehlend (Vorschlag
übernommen, Stand-Fixture hat nun ein Kriterium); 2 keine Meldung ohne Kennungstest;
3 Docstring wie vorgeschlagen; 4 Satz gestrichen. Scheiter-Tests in `rueckverfolgungTest.py`.

**Nachprüfung.** In 957cf7e 1 bis 4 nachgestellt und grün, 353 Tests, ruff und complexipy
grün. 957cf7e ohne neuen Befund.
