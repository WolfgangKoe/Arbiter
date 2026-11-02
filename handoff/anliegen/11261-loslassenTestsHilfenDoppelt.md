# Tests zum Loslassen neben der Karte: Hilfen doppelt, Ziel als Text

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Kritik an den Tests zu Item loslassenNebenDerKarte (Commit 6812e74). Wartet nach
[Kritik](../../prozess/ablauf/kritik.md): Namen und Ablage von Hilfen, keine Prüfung rot.

1. [loslassenWoDieKarteZeigtTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenWoDieKarteZeigtTest.py)
   und [loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py)
   definieren beide `pfadDesGezogenenImBeispiel`, `punktDesLoslassensImBeispiel`,
   `einenZollJenseitsDerKante`, `längeDesHaltens`, `zieleNebenDerKarte` und
   `punktNebenDerKarte` (dort mit `spieler`, hier ohne). Pfad und Punkt des Beispiels stehen
   ein drittes Mal als Text in `blockAlsGanzesTest.py` (Zeilen 227, 311) ([Wir 3](../../prozess/praemissen/wir.md)).
2. `punktNebenDerKarte(…, ziel: str)` nimmt einen *Spielernamen* oder den Sonderwert
   `"nebenDerKarte"`; die Fixture `zugOhneBewegung` in
   [loslassenNebenDerKarteTest.py](../../technik/tests/akzeptanz/phasen/bewegung/loslassenNebenDerKarteTest.py)
   verzweigt an `request.param`. Daneben, in denselben Dateien, sind die Fälle Funktionen
   (`loslassen`, `danach`, `ebeneLegen`); ein Text steht hier für einen Ort, der keinen Namen hat.

**Kosten.** Am Bildschirm nichts. Ändert sich das Beispiel `stelleBeimLoslassen.json`, sind
drei Dateien nachzuziehen; ein weiteres Ziel neben der *Karte* braucht einen Zweig in zwei Kopien.

**Gegenvorschlag.** Pfad und Punkt des Beispiels einmal in `dienst.py` neben
`stelleBeimLoslassenDesVertrags`, die Ziele einmal in `ziehen.py` als Funktionen
`(seite, aufstellung, spieler) -> Bildpunkt`, je eine für jede *Armeeliste* und eine für
neben der *Karte*; `zugOhneBewegung` als zwei Funktionen wie `danach`.

**Stellungnahme.**
