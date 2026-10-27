# Schlachttests: Import, Aufbau und Vertrag

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen
Wartet auf: 5180

## Runde 1
**Befund.** Lauf über `technik/tests/akzeptanz/phasen`: 8 failed und 169 errors. Ursache ist
nur fehlender Produktcode: 174-mal `Modell(bewegungsweite=…)` aus `handgriffe.py`, 3-mal
`arbiter.domaene.querschnitt.schlachtrunden` beim Sammeln. Danach bleiben aber drei
Dateien rot (Punkt 1).

Hält auf (Ich 3: eine Prüfung bleibt rot; neuer Code verletzt T1; ein Test prüft den Vertrag
nicht, den sein Kriterium braucht):
1. [ebeneTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ebeneTest.py),
   [normaleBewegungTest.py](../../technik/tests/akzeptanz/phasen/bewegung/normaleBewegungTest.py)
   und [sperrenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py)
   importieren `seiteDerSchlachtMitEingabe` aus `tests.akzeptanz.schlacht`. Die Funktion
   steht aber in `bildschirm.py`. Mit Produktcode gibt das einen ImportError, und keiner
   ihrer Tests läuft.
2. T1(4), „ohne **wenn** keine Handlung“: QUE-9.1 und QUE-10.1 haben kein **wenn**. Trotzdem
   steht dort ein `Locator` als eigener Block an der Stelle der Handlung:
   [ersterZugTest.py](../../technik/tests/akzeptanz/querschnitt/ersterZugTest.py) Zeilen 42,
   55, 67, [schlachtrundenTest.py](../../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py)
   Zeilen 86, 98, 111, 122, 267. `testQue10_1DerSpielstandNennt…` hat `phaseBeenden` als
   Handlung, obwohl 10.1 keine nennt. `testQue10_4DerSpielstandNennt…` hat es umgekehrt: Die
   Handlung `phaseBeenden` steht im Aufbau, und das Lesen des Spielstands steht an ihrer
   Stelle.
3. Was die Verträge unter „Prüft“ nennen, fehlt:
   [Bewegung](../../technik/architektur/vertrag/bewegung.md): 200 nach dem Loslassen gleich
   `bewegung.json`, V10 außerhalb der *Bewegungsphase* leer;
   [Schlacht](../../technik/architektur/vertrag/schlacht.md): V13 mit dem Körper einer schon
   beendeten *Phase*. BEW-1.2 und 1.3 prüft nur die Domäne. Weder
   `PUT /api/bewegungDerEinheitBeenden` noch der Knopf „Bewegung der Einheit beenden“ (Plan 8,
   Schritt 3) hat einen Test.

Wartet auf Technikphase 9 (Ich 3: abseits des Happy Path, Namen und Hilfsfunktionen, keine
Prüfung rot):

4. Die Tests des Dienstes zu BEW-2.3 vergleichen `gründe` nur als Menge. V6 und V15 verlangen
   aber die Reihenfolge von `Grund`.
5. `istHandlung` in [bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py) zählt V9 und
   V14 als Handlung. Nach V7 sind sie Auswählen ([Anliegen 5140](5140-klickAufEinModellUndDieSperrmeldung.md)).
6. Die Fixture `schlachtInDerKommandophase` heißt nach der Kommandophase. In QUE-10.2 und 10.5
   steht der Test aber in einer anderen *Phase*.
7. `ebeneTest.py` lädt `schlacht.py` gleich beim Import. Bis `schlachtrunden` existiert, sind
   damit auch AUF-20.2 bis 20.5 rot. Das ergänzt [Anliegen 4921](4921-klickUndHandgriffeDerSchlachtFuerSpaeter.md),
   Punkt 2.

**Kosten.** Punkt 1: eine Zeile je Datei. Ohne die Korrektur kann der Implementierer Item 3
nicht grün machen, ohne Tests anzufassen. Punkt 2: Leerzeilen und Umstellungen. Punkt 3:
etwa fünf Tests. Ohne sie sind alle Tests grün, auch wenn Knopf, Route oder der Schlüssel
`einheitInBewegung` fehlen.

**Gegenvorschlag.**
1. `seiteDerSchlachtMitEingabe` aus `tests.akzeptanz.bildschirm` importieren.
2. Den `Locator` in den Prüfblock ziehen (`expect(knopfDerArmeeliste(…)).to_have_count(1)`).
   In 10.1 die Anfragen in den Aufbau stellen. In 10.4 die Handlung über
   `phaseBeenden(dienstDerSchlacht, …)` (V13) schicken und ihre Antwort prüfen.
3. Je ein Test für die Prüfung, die die Verträge nennen. Dazu ein Test des Dienstes und einer
   am Bildschirm für „Bewegung der Einheit beenden“ (BEW-1.3).
4. bis 7. in Technikphase 9: 4 als `gründe == [grund.value for grund in Grund if grund in
   erwartet]`; 5 ohne `/ebene` und `/anklicken`; 6 benennen; 7 mit 4921.

**Stellungnahme.**
1. Angenommen und umgesetzt: `seiteDerSchlachtMitEingabe` kommt in [ebeneTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ebeneTest.py),
   [normaleBewegungTest.py](../../technik/tests/akzeptanz/phasen/bewegung/normaleBewegungTest.py)
   und [sperrenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py)
   aus `tests.akzeptanz.bildschirm`.
2. Angenommen und umgesetzt: In [ersterZugTest.py](../../technik/tests/akzeptanz/querschnitt/ersterZugTest.py)
   steht der `Locator` in der Prüfung (QUE-9.1). In [schlachtrundenTest.py](../../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py)
   stehen in 10.1 die Anfragen im Aufbau und der `Locator` im Aufbau oder in der Prüfung,
   nie als Handlung. In 10.4 ist die Handlung `phaseBeenden` (V13) mit Prüfung der Antwort.
3. Teils umgesetzt: V10 außerhalb der *Bewegungsphase* leer
   (`testQue10_5DerDienstNenntAußerhalbDerBewegungsphaseBeimZiehenKeinModellUndKeinenGrund`,
   je *Phase*) und V13 mit dem Körper einer beendeten *Phase*
   (`testQue10_2DerDienstÄndertNichtsBeimKörperEinerSchonBeendetenPhase`). Angenommen, aber
   noch offen: 200 nach dem Loslassen gleich `bewegung.json` sowie Route und Knopf „Bewegung
   der Einheit beenden“ (BEW-1.3); ihren Vertrag ändert der Architekt gerade nach 5180. Darum
   steht `Wartet auf: 5180`.
4. bis 7. nehme ich für die Technikphase 9 an.
