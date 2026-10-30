# Abstand in zwei Bedeutungen beim Aufeinander-zu-Ziehen

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik an den Tests zu 6241 (`git diff e1fb48b -- technik/tests/akzeptanz`),
Schnittstelle und Lesbarkeit. Hält auf nach [Kritik](../../prozess/ablauf/kritik.md): neuer
Code, dessen Namen nicht tragen, was sie bedeuten ([Es](../../prozess/praemissen/es.md),
Lesbarkeit; [Wir 2](../../prozess/praemissen/wir.md)).
1. *Abstand* heißt im [Glossar](../../domaene/glossar.md) die Entfernung zwischen den
   *Bases*. In [schlacht.py](../../technik/tests/akzeptanz/schlacht.py) ist `abstandInX`
   (`restInX`, `aufDasAndereZu`, `aufeinanderZuZiehen`) der Unterschied der *Stellen*, also
   der Mittelpunkte, in x; darum ruft der Test `aufeinanderZuZiehen(…, radien + dreiZoll)`.
   Zwei Zeilen weiter rechnet `westlichDavorMitAbstand(…, radien, halberZoll)` in
   [anhaltenVorDerGrenzeTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py)
   mit *Abstand* im Sinn des Glossars und zieht die Radien selbst ab. Wer den Test liest,
   muss beide Hilfen öffnen, um zu sehen, dass 3″ und ½″ dasselbe meinen; einmal addiert
   der Aufrufer die Radien, einmal die Hilfe.
2. `westlichDavorMitAbstand(stelle, summeDerRadien, abstand)`: Der Parameter verdeckt die
   im selben Modul importierte Funktion `summeDerRadien` (Zeile 11 und 27). Ein Name, zwei
   Dinge in einer Datei.
3. `paare = {True: …, False: …}` mit `paare[schlacht.amZug is spielerAmZug]` ist ein
   `if`/`else` über einen Wahrheitswert, als Tabelle verkleidet (Es 9: wenige Fälle als
   `if`). Nötig ist es nicht: `zurBewegungsphaseDesNächstenZugs` wechselt den *Spieler*
   jedes Mal, das gezogene *Modell* wechselt also Zug um Zug.

**Kosten.** Am Bildschirm nichts. Bleibt es, verwechselt der nächste Test, der
`aufeinanderZuZiehen` nutzt, leicht Mittelpunkt- und *Abstand* um die Summe der Radien und
landet in oder vor der *Nahkampfreichweite*, ohne dass der Name warnt. Nachbessern: wenige
Zeilen in zwei Dateien.

**Gegenvorschlag.**
1. `aufeinanderZuZiehen(schlacht, modellAmZug, modellDesAnderenSpielers, abstand)` nimmt den
   *Abstand* nach dem Glossar und rechnet `summeDerRadien` selbst hinzu, wie
   `westlichDavorMitAbstand`; der Test ruft `aufeinanderZuZiehen(…, dreiZoll)`. Die
   Hilfsgröße heißt, was sie ist: `restDerMittelpunkteInX` oder ähnlich.
2. Parameter `radien` statt `summeDerRadien`.
3. Tauschen statt nachschlagen:
   ```python
   gezogenes, anderes = modellAmZug, modellDesAnderenSpielers
   while …:
       aufDasAndereZu(schlacht, gezogenes, anderes, …)
       zurBewegungsphaseDesNächstenZugs(schlacht)
       gezogenes, anderes = anderes, gezogenes
   ```
   Die zweite Schleife bleibt, `spielerAmZug` dient nur ihr.

**Stellungnahme.** Angenommen, alle drei Punkte umgesetzt.
1. In [schlacht.py](../../technik/tests/akzeptanz/schlacht.py) nehmen `aufeinanderZuZiehen`
   und `aufDasAndereZu` den *Abstand* nach dem Glossar; `restBisZumAbstandInX` zieht
   `summeDerRadien` selbst ab (`restInX` und `abstandInX` entfallen). Der Test ruft
   `aufeinanderZuZiehen(…, dreiZoll)`. Gerechnet wird wie vorher, nur steht die Summe der
   Radien jetzt in der Hilfe statt beim Aufrufer.
2. Der Parameter von `westlichDavorMitAbstand` in
   [anhaltenVorDerGrenzeTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py)
   heißt `radien`.
3. Die Tabelle `paare` ist ersetzt durch den Tausch `gezogenes, anderes = anderes, gezogenes`
   nach jedem Zug; die zweite Schleife bleibt.
Geprüft: ruff, `formregeln.benennung`, `formregeln.glossar`, `formregeln.kommentare` ohne
Befund. Der Test scheitert weiter am KeyError 'Einheit' aus dem Katalog (Item 1), nicht an
den Hilfen.
