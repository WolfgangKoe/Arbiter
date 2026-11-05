# Hilfen und Szenen in den Tests zu Fliegen

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Hält nicht auf: Namen und Ablage von Hilfen, keine Prüfung rot. Kritik an den
Tests zu Item fliegen, in
[fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py):
1. Rund 50 Zeilen Geometrie stehen in der Testdatei: `Kreis`, `schnittpunkte`,
   `wegZumNächstenSchnitt`, `wurzelAufgerundet`, `randDerNahkampfreichweite`,
   `höchstensUmHundertstelWeiter`, `frei`, `ganzImSpielfeld`. Sie prüfen das Rücken
   allgemein, nicht nur die Spinne; `überdeckt` und `aufDerStrecke` liegen schon in
   [anhalten.py](../../technik/tests/akzeptanz/anhalten.py). So hat die Datei 686 Zeilen, und
   der Leser sucht die Tests zwischen Rechnungen.
2. Die Szene „Warrior, dahinter auf einer Linie der Warboss“ steht dreimal mit anderen Zahlen:
   `aufDemWarriorHinterDerBewegungsweiteVorDemWarbossLoslassen` (Lücke 2″),
   `aufDemWarriorInDerNahkampfreichweiteLoslassen` (1″, schräg versetzt) und ausgeschrieben in
   `testBew18_2NebenEinemModellDesAnderenSpielers…` (2″, schräg versetzt). Was sich
   unterscheidet, sieht man nur im Vergleich der Zeilen.
3. Die 18.3-Tests an `Schlacht` und an der *Karte* bauen je Paar denselben Aufbau zweimal
   (`…DurchDieNahkampfreichweiteGezogen…`, `…EndetDieStreckeInDerNahkampfreichweite…`); das
   dritte Paar nutzt schon `warbossAufDieStreckeÜbergehen`.
4. `vorDerMitte` und `hinterDerMitte` meinen „zur Spinne hin“ und „von ihr weg“, weil sie nach
   Westen zieht; das steht nirgends. Der Parameter `zurMitte` ist ein Versatz von der Mitte.
   Zahlen wie `Fraction(-8)`, `Fraction(5)`, `Fraction(13, 5)` haben keinen Namen (wie 12041,
   Punkt 3).
5. `testBew18_1DerDienstZeigt…` verzweigt mit zwei `if` im Test über einen Parameter, der
   `None` sein kann.

**Kosten.** Testautor, etwa 45 Minuten, das Verhalten der Tests bleibt. Bleibt es, liest jeder
Kritiker und der Implementierer die Szenen durch Nachrechnen.

**Gegenvorschlag.** (1) Die Geometrie nach `anhalten.py` oder in ein Hilfsmodul `ruecken.py`
neben ihm. (2) Eine Hilfe für die Szene mit der Lücke zum Warboss und dem Versatz als
benannten Parametern. (3) Je Paar eine Hilfe für den Aufbau wie `warbossAufDieStreckeÜbergehen`.
(4) `zurSpinneHin` und `vonDerSpinneWeg`, `versatzVonDerMitte`; die Zahlen benennen
(`jenseitsDerBewegungsweite`). (5) Die Eingaben je Fall als Parameter, ohne `if`. Mit 12041 in
einem Gang.

**Stellungnahme.**
