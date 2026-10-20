# Akzeptanztests: Stellen als Zahlen unter einem Namen

1216 · Kritik · von Architekt → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik an den Tests zu Item [einheitVerschieben](../../domaene/items/einheitVerschieben.md).
Nach [Ich 3](../../prozess/praemissen/ich.md) wartet das: Namen und Ablage von
Hilfsfunktionen, keine Prüfung ist rot. Was aufhält: [1215](1215-testsZuItem2OhneSperrfelderUndOhneWiederholung.md).
1. Dieselbe Umrechnung einer *Stelle* in das Zahlenpaar des Spielstands heißt `alsZahlen`
   ([einheitVerschiebenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/einheitVerschiebenTest.py)),
   `stelleAlsPaar` ([modellPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/modellPerKlickTest.py)),
   steckt in `körperDerStelle` ([dienst.py](../../technik/tests/akzeptanz/dienst.py)) und
   steht ausgeschrieben als `(float(stelle.x), float(stelle.y))` in den Tests zu 20.2, 20.4,
   21.2, 24.2 und 26.1.
2. `wegVon` und `versetzt` rechnen mit *Stellen* wie `inZoll` in
   [handgriffe.py](../../technik/tests/akzeptanz/handgriffe.py); kürzt Item 3 den Weg (26.3),
   braucht es sie wieder.
3. `testAuf20_4DerDienstVerschiebtNurDasGezogeneModell`: Die Nummer des gezogenen *Modells*
   steht dreimal als `1` (`danach[1]`, `nummer != 1`).

**Kosten.** Wer *Stellen* im Spielstand vergleicht, wählt zwischen drei Namen und einer
ausgeschriebenen Form; eine Änderung des Formats (V1) trifft fünf Stellen.

**Gegenvorschlag.** Eine Funktion `stelleImSpielstand(stelle)` in `dienst.py`, die
`körperDerStelle` mitbenutzt, statt der drei Formen; `wegVon` und `versetzt` nach
`handgriffe.py`, sobald ein zweites Modul sie braucht; `nummerDesGezogenen = 1`. Erledigt,
wenn `grep -rn "float(stelle.x)\|def alsZahlen\|def stelleAlsPaar" technik/tests/akzeptanz/phasen`
nichts findet.

**Stellungnahme.** Angenommen und umgesetzt: `stelleImSpielstand` in `dienst.py`, von
`körperDerStelle` mitbenutzt; `alsZahlen` und `stelleAlsPaar` entfallen in den Tests zu
Item 2; `wegVon` und `versetzt` stehen in `handgriffe.py`; `nummerDesGezogenen = 1` in
`ebeneTest.py`. Das grep findet nur noch `alsZahlen` in `anhaltenAnEinerBaseTest.py` (26.2–26.4)
und `float(stelle.x)` in `setzenPerKlickTest.py` (AUF-3, nicht Item 2); beides fasse ich
nicht an, der zuständige Testautor stellt sie um.
