# Einheitstests zu fliegen prüfen, was ihr Name sagt

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Kritik am Code (Lesbarkeit), vorgemerkter Stand von Item fliegen, Abschnitt 1
(`git diff --cached -- technik/`). Hält auf nach [Kritik](../../prozess/ablauf/kritik.md):
neue Tests, die nicht prüfen, was ihr Name verspricht (Absicht 1, Anliegen 692), und
[Es 6](../../prozess/praemissen/es.md). Beide Mutanten habe ich an einer Kopie in `/tmp`
laufen lassen.
1. `testDasEndeVorDemWegendeBestimmtDieNahkampfreichweiteAmEnde` in
   [fliegenTest.py](../../technik/tests/einheit/domaene/phasen/bewegung/fliegenTest.py): Bei
   `weglänge` 30 steht auch das Wegende (x 30, Abstand 10″) in *Nahkampfreichweite*, also
   liefert `ende` = 1 dasselbe wie 1/2. Mutant `anteilVorDerLetztenBerührung(…, weg,
   Fraction(1), …)` in `anteilBisZurNahkampfreichweite`: alle 10 Tests grün.
2. `testRänderWeiterAlsDerWegZurückZählenNicht` in
   [messenTest.py](../../technik/tests/einheit/domaene/messenTest.py): Der Ursprung liegt
   außerhalb des fernen Kreises, ist also frei; `None` folgt schon aus dem Filter
   `_länge(punkt) <= reichweite`. Mutant `nahe = list(ränder)`: alle 34 Tests grün. Der
   Vorfilter ändert kein Ergebnis, nur die Laufzeit; kein Test kann ihn am Ergebnis zeigen.
3. Indizes auf *Wege* in messenTest.py: `länge` (`weg[0]`, `weg[1]`), `außerhalbVon` und
   `frei` im Test zu Kreis und Gerade (`weg[1] >= oberhalb.wert`).

**Kosten.** Am Bildschirm nichts. Ohne 1 bliebe 18.3 mit einem `ende` vor dem Wegende
ungeprüft, sobald jemand den Parameter verliert; 2 verspricht eine Prüfung, die es nicht
gibt. Umbau etwa zehn Zeilen in zwei Testdateien, kein Produktcode.

**Gegenvorschlag.**
1. In diesem Test `wegNachRechts(50)`: Ende x 50 außerhalb (Abstand 30″), bei 1/2 x 25 darin;
   erwartet weiter knapp vor x 9.
2. Den Test löschen oder umbenennen nach dem, was er prüft: „Ein Kandidat weiter als der Weg
   zurück gilt nicht“, mit einem Rand, dessen Lotpunkt `frei` bestätigen würde (Ursprung im
   gemiedenen Kreis, Radius größer als `zurück`).
3. Entpacken: `wegInX, wegInY = weg`.

**Stellungnahme.** Angenommen, alle drei Punkte umgesetzt.
1. Der Test nutzt `wegNachRechts(50)`; der Mutant `Fraction(1)` statt `ende` macht ihn rot.
2. Der Test heißt jetzt `testEinRandWeiterAlsDerWegZurückSchränktDieKandidatenNichtEin`: Ein
   naher Rand liefert den Lotpunkt, ein ferner Kreis mit dem Ursprung darin würde ihn
   ausschließen. Der Mutant `nahe = list(ränder)` macht ihn rot; die Wirkung des Vorfilters ist
   damit am Ergebnis gezeigt.
3. `länge`, `außerhalbVon` und `frei` entpacken den Weg.
Beide Mutanten an Kopien in `/tmp` geprüft, `technik/tests/einheit` grün (273).
