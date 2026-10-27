# Schlacht im Code: Gegner über gegnerVon, Name eines Einheitstests

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

## Runde 1
**Befund.** Wartet (Ich 3: Namen und Ablage von Hilfsfunktionen), Diff `9be7f37..7aa6698`.
1. Nachbau: `_zugBeenden` bestimmt den Gegner des *ersten Zugs* selbst
   (`zweiterSpieler if self._ersterZug is ersterSpieler else ersterSpieler`,
   [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py), Z. 126 bis
   127). Das tut schon `gegnerVon` in
   [reihenfolge.py](../../technik/arbiter/domaene/phasen/aufstellen/reihenfolge.py); die
   Aussage steht zweimal ([Wir 3](../../prozess/praemissen/wir.md)).
2. `testPhaseBeendenMitUnvollständigemKörperIstEineFalscheAnfrage`
   ([anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py)) prüft auch
   vollständige Körper mit falschem Wert (`True`, `1.5`, `"Spielphase"`, eine Liste); der Name
   nennt nur den fehlenden Schlüssel.

**Kosten.** Keine in Zyklus 8. Bleibt 1, ändert sich die Regel für den Gegner an zwei
Stellen; bleibt 2, sucht ein Leser den Fall „falscher Wert“ vergeblich.

**Gegenvorschlag.**
1. `self._amZug = gegnerVon(self._beideSpieler, ersterZug)`; liegt `gegnerVon` dann besser
   bei den Spielobjekten als in der *Aufstellung*, entscheidet der Architekt.
2. Umbenennen in `testPhaseBeendenMitFalschemKörperIstEineFalscheAnfrage`.

**Stellungnahme.**
