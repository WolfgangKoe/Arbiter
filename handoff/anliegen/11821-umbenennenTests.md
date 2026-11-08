# Umbenennen nach 7800: Akzeptanztests

Form: Kritik
Von: Planer
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Nach [7800](7800-karteUndEbeneBenennen.md) heißt *Karte* *Spielfeld* (F1 A), *Ebene*
bleibt mit *Einheitenebene* und *Modellebene* (F2 B). Die Akzeptanztests sagen noch *Karte* und
*Ebene*, auch in Testnamen ([Wir 2](../../prozess/praemissen/wir.md)).

**Kosten.** Laut 7800 rund 112 Stellen *Karte* (49 Testnamen) und 309 *Ebene* (37 Testnamen) in
den Tests, mechanisch. Ohne diesen Schritt fehlt die Umbenennung in Review 10
(Anliegen 11780).

**Gegenvorschlag.** Wann: nach [11820](11820-umbenennenGlossarUndAnforderungen.md) (Glossar),
gleichzeitig mit [11822](11822-umbenennenCode.md); vor „Reviewer: DoD über das Inkrement“
(7800 F3), damit Tests und Code zusammen umbenannt sind.

**Stellungnahme.** Angenommen und umgesetzt: In allen 47 betroffenen Dateien unter
[technik/tests/akzeptanz](../../technik/tests/akzeptanz/) heißt *Karte* jetzt *Spielfeld*
(etwa `kreiseDesSpielfelds`, `punktAufDemSpielfeld`, `nebenDemSpielfeldLoslassen`), die
alte *Spielfeld*-Fläche `.spielfläche`; *Ebene* heißt *Einheitenebene* oder *Modellebene*
(`modellebeneWählen`, `alleinUndMitEinheitenebene`). Vier Dateien tragen den neuen Namen:
[spielfeldTest.py](../../technik/tests/akzeptanz/querschnitt/spielfeldTest.py),
[ruhigesSpielfeldTest.py](../../technik/tests/akzeptanz/querschnitt/ruhigesSpielfeldTest.py),
[loslassenWoDasSpielfeldZeigtTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenWoDasSpielfeldZeigtTest.py),
[loslassenNebenDemSpielfeldTest.py](../../technik/tests/akzeptanz/phasen/bewegung/loslassenNebenDemSpielfeldTest.py).
Geblieben sind *Einheitenkarte* und *Armeekarte* der Armeeliste, die 7800 nicht umbenennt.
Benennungs- und Rückverfolgungsprüfung grün, 1384 Tests werden gesammelt.
