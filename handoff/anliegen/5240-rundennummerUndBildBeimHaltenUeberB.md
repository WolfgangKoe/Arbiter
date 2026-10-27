# Nummer der Schlachtrunde und das Bild beim Halten über B

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: angenommen
Wartet auf: 5180

## Runde 1
**Befund.** Hält auf (Ich 3: ein Test prüft sein Kriterium nicht).
1. QUE-10.1, „die Nummer der *Schlachtrunde*“ ([schlachtrundenTest.py](../../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py)):
   Jeder Test an der Seite und am Dienst steht in *Schlachtrunde* 1, auch das Beispiel
   [schlacht.json](../../technik/architektur/vertrag/schlacht.json) (`"schlachtrunde": 1`).
   Eine Kopfzeile mit fest „Schlachtrunde 1“ besteht alle Tests. Im Happy Path (Plan 8,
   Schritt 4) zählen die *Spieler* an dieser Anzeige bis zur fünften *Schlachtrunde*.
2. BEW-1.4, `testBew1_4DieKarteZeigtBeimHaltenWeiterAlsBDieLetzteStelleOhneSperreOhneSperrmeldung`
   ([normaleBewegungTest.py](../../technik/tests/akzeptanz/phasen/bewegung/normaleBewegungTest.py)):
   Der Zeiger geht von 3″ nach 6″ (*B* des Warboss 5″) in zehn Schritten zu 0,3″
   (`Maus.bewegen` mit `steps=10`, `Finger.bewegen` mit zehn `touchMove`,
   [ziehen.py](../../technik/tests/akzeptanz/ziehen.py)). Die Schritte bei 3,3″ bis 4,8″ sind
   erlaubt; die Seite fragt schon beim ersten nach
   ([bedienung.js](../../technik/frontend/bedienung.js), `ziehenFolgen`,
   `stelleBeimLoslassenAbfragen`) und bekommt 200. Nach V10 („die *Karte* zeigt weiter die
   letzte 200 dieses Zugs“, [Bewegung](../../technik/architektur/vertrag/bewegung.md)) steht
   der Kreis dann zwischen 3,3″ und 4,8″; der Test verlangt ihn genau bei 3″. Er ist also rot
   bei einer Umsetzung der Annahme A aus
   [5180 F2](5180-annahmenZurBewegungsphase.md), grün nur, wenn die Seite erlaubte
   Zwischenstellen nicht zeigt. Das sagt weder BEW-1.4 noch die Annahme, und der Stakeholder
   erwartet dort, dass die *Einheit* „am maximalen Wert stoppt“ (Antwort zu F2, Status
   rückfrage).

**Kosten.** Bleibt 1, kann die Abnahme nicht zeigen, dass Arbiter die *Schlachtrunde* weiterzählt.
Bleibt 2, baut der Implementierer ein Bild, das keiner verlangt hat, oder scheitert an einem
roten Test bei richtiger Umsetzung. Nachbessern kostet je Punkt wenige Zeilen mit vorhandenen
Fixtures und Handgriffen.

**Gegenvorschlag.**
1. Ein Test an der Seite, parametriert über `spielerMitDemErstenZug`: nach `zügeBeenden(…, 2)`
   zeigt die Kopfzeile des *Spielers* mit dem *ersten Zug* „Schlachtrunde 2 · Kommandophase“.
2. Der Test prüft bis zur Klärung von 5180 F2 nur, was A, B und die Antwort des Stakeholders
   gemeinsam haben: Der Kreis des Warboss liegt beim Halten höchstens *B* (auf ein Pixel,
   `zollJePixel`) von `davor`, nicht bei `zuWeit`, und die Seite nennt keinen *Grund*. Steht
   F2 fest, schärft ihn ein Test nach der Antwort.

**Stellungnahme.**
1. Angenommen und umgesetzt. [schlachtrundenTest.py](../../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py)
   hat `testQue10_1DieKopfzeileNenntNachZweiZügenDieZweiteSchlachtrunde`, parametriert über
   `spielerMitDemErstenZug`: nach `zügeBeenden(…, 2)` steht „Schlachtrunde 2 · Kommandophase“ in
   der Kopfzeile des *Spielers* mit dem *ersten Zug*. Eine feste „Schlachtrunde 1“ besteht
   ihn nicht.
2. Angenommen, aber noch nicht umgesetzt: Der Test zu BEW-1.4 beim Ziehen über *B* bleibt, wie
   er ist, bis der Architekt den Vertrag nach 5180 F2 geändert hat. Dann schreibe ich ihn
   nach dem Gegenvorschlag (Kreis höchstens *B* von `davor`, nicht bei `zuWeit`, kein *Grund*)
   oder nach der Antwort schärfer neu. Darum steht `Wartet auf: 5180`.

**Nachprüfung (Fachkritiker).** Punkt 1 in Ordnung: Der neue Test läuft für beide *Spieler*
mit dem *ersten Zug*. Nach zwei ganzen Zügen verlangt er in der Kopfzeile dieses *Spielers*
`amZug` und „Schlachtrunde 2 · Kommandophase“. Eine feste „Schlachtrunde 1“ fällt damit
durch, ebenso eine Nummer, die Züge statt *Schlachtrunden* zählt (sie zeigte 3). Punkt 2 prüfe
ich, wenn 5180 geklärt ist; bis dahin bleibt der Status.
