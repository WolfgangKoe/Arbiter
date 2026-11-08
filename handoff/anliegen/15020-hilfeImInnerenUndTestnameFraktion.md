# Hilfe im Inneren und Testname der Fraktion

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Wartet (Namen und Ablage von Hilfen in Einheitstests, keine Prüfung rot),
uncommitteter Stand nach 8041 und 14920.
1. Die Hilfe, die eine Stelle um 10 ins Innere des Spielfelds setzt, steht zweimal gleich
   unter dem Namen `stelleAn`: in
   [bewegungsphaseTest.py](../../technik/tests/einheit/domaene/phasen/bewegung/bewegungsphaseTest.py)
   und [bewegungTest.py](../../technik/tests/einheit/domaene/phasen/bewegungTest.py)
   ([Wir 3](../../prozess/praemissen/wir.md)). Neben `stelleAn` in
   [modelle.py](../../technik/tests/einheit/modelle.py) trägt sie denselben Namen für eine
   andere Bedeutung, wie die Stellungnahme zu 8041 selbst sagt.
2. `testEineFraktionOhneOrdnerIstEinFehler` in
   [datenblaetterTest.py](../../technik/tests/einheit/katalog/datenblaetterTest.py) hat jetzt
   den Fall `"./orks"`, dessen Ordner es gibt; der Name sagt etwas anderes, als der Fall prüft.

**Kosten.** Am Bildschirm nichts. Ein Leser hält zwei verschiedene `stelleAn` für dieselbe;
ändert sich die Hilfe, ändern sich zwei Kopien. Umbau etwa 10 Zeilen in drei Dateien.

**Gegenvorschlag.**
1. Einmal in modelle.py als `stelleImInnerenAn`, beide Tests importieren sie.
2. Den Fall in einen eigenen Test `testEineFraktionDieNichtNurAusBuchstabenBestehtIstEinFehler`
   mit `"./orks"`, oder den Namen auf beide Fälle fassen: `testEineFraktionOhneEigenenOrdnerIstEinFehler`.

**Stellungnahme.**
