# Namen in den Tests zu 6291

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wartet (Ich 3: Namen von Hilfsdaten, keine Prüfung rot). Die Schnittstelle ist
ohne Befund: Alle neuen Tests gehen über `stelle`, `modellLoslassen` und `inKohärenz` der
*Schlacht*.

1. [sperrenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py),
   `testBew2_5LiegtEineFremdeBaseSchrägMittenAufDerStrecke…`: Der Weg heißt
   `schrägAnDerFremdenBaseVorbei`, der Test erwartet aber die *Sperre* ‚über eine Base‘.
   Tatsächlich streift die *Base* die fremde: Ihr Mittelpunkt kommt ihr auf 1,2″ nahe, zwei
   *Bases* von 32 mm (rund 1,26″) überdecken sich also um rund 0,06″, nur zwischen Anfang und
   Ende. Das sieht der Leser erst nach Rechnen, der Name sagt das Gegenteil. Daneben heißt
   `dreiOstenUndZweiNorden` nach seinem Wert, fast wie das importierte `ostenUndNorden`
   (2 Osten, 3 Norden).
2. [anhaltenAnDerBewegungsweiteTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenAnDerBewegungsweiteTest.py),
   `testBew3_1ZiehtEinModellNurEinenHauchWeiter…`: `Fraction(1, 200)` steht ohne Namen, in
   einer Datei mit `dreiZoll` und `weiterAlsDieBewegungsweiteDesWarboss`. Warum gerade 1/200,
   nämlich weniger als die 1/100″, um die Arbiter davor anhalten darf, sagt der Code nicht.

**Kosten.** Zwei bis drei Zeilen umbenennen, kein Test ändert sein Verhalten.

**Gegenvorschlag.**
1. Nach dem, was der Weg tut: `schrägDieFremdeBaseStreifend`; die Stelle der fremden *Base*
   nach ihrer Rolle, etwa `nebenDerStrecke`.
2. `einHauch = hundertstelZoll / 2` aus [schlacht.py](../../technik/tests/akzeptanz/schlacht.py),
   neben `dreiZoll`.

**Stellungnahme.** Angenommen, beides wie vorgeschlagen; die Tests verhalten sich wie zuvor
(beide grün, Werte unverändert).
1. [sperrenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py):
   Der Weg heißt `schrägDieFremdeBaseStreifend`, die Stelle der fremden *Base*
   `nebenDerStrecke` (ihr Mittelpunkt liegt 1,2″ neben der Strecke).
2. [anhaltenAnDerBewegungsweiteTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenAnDerBewegungsweiteTest.py):
   `einHauch = hundertstelZoll / 2` steht neben `dreiZoll`, `hundertstelZoll` kommt aus
   [schlacht.py](../../technik/tests/akzeptanz/schlacht.py); `schlacht.py` selbst bleibt
   unverändert.
