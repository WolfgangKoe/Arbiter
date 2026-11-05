# Fliegen: Der Test zum Rücken bleibt mit dem alten Fehler grün

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Hält auf: Ein Test prüft nicht, wofür er steht ([Kritik](../../prozess/ablauf/kritik.md)).
Kritik am Code zu Item fliegen, Abschnitt A (`f7f8b57`). Der Code ist richtig; das zeigen die
Proben unten. Aber kein Test sichert ihn:
1. `testEinFliegerRücktBeimLoslassenAuchDannAnDieFreieStelleWennEsNichtDasErsteModellDerEbeneIst`
   bleibt grün, wenn der Fehler aus [13740](13740-fliegenAlsTypUndZweiFehler.md), Punkt 2,
   zurückkommt (`next(iter(gezeigt.stellen.values()))` in
   `stellenMitGründenNachDemLoslassen`). Grund: In seiner Lage ist der falsche Weg zurück
   13″ lang, der richtige 5″. Die Suche findet die freie *Stelle* also auch mit dem falschen.
   Der Fehler zeigt sich nur, wenn der falsche Weg kürzer ist als der nötige.
2. Den Test, den 13740 Punkt 2 verlangte, gibt es nicht: zwei Flieger in einer *Ebene*,
   übergangen. Derselbe Fehler in `übergangen` bleibt grün in `fliegenTest.py` und
   `bewegungsphaseTest.py`. Dort kommt die *Ebene* aus einem `frozenset`, die Reihenfolge ist
   also beliebig.

Heute ist die Spinne der einzige Flieger und steht allein; darum zeigt das kein Akzeptanztest.
Abschnitt B ([13740](13740-fliegenAlsTypUndZweiFehler.md), Punkt 1) verschiebt genau diese
Zeilen, und danach fiele ein Rückfall nicht auf.

**Kosten.** Rund 20 Zeilen Einheitstest, ein Test umgebaut. Am Bildschirm ändert sich nichts.

**Gegenvorschlag.** Vor Abschnitt B in `bewegungsphaseTest.py`, mit den Modellen von `modellMit`.
Vorlage: `/tmp/arch13840proben/probenTest.py` (am Commit grün; mit dem Fehler je ein Test rot,
Lauf: `/tmp/arch13840proben/mutanten.py`, M4 und M5).
1. Loslassen, das hintere *Modell* vorn im Mapping: hinten bei (20, 22), gezogen von (25, 22)
   nach (30, 22), das fremde *Modell* 1/2″ dahinter. So liegt die neue *Stelle* des hinteren
   genau auf der alten des gezogenen. Der falsche Weg hat die Länge 0 und die Suche findet
   nichts.
2. Übergehen mit derselben Lage, parametrisiert: einmal das eine *Modell* gezogen, einmal
   das andere, gegenläufig. Eines von beiden steht im `frozenset` immer vorn, also ist bei
   dem Fehler genau ein Fall rot. Erwartet je: nicht am Punkt, `gründe` leer.

**Stellungnahme.**
