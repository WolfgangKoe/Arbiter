# Bewegungstests: Ablage und Pakete für später

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

## Runde 1
**Befund.** Wartet (Ich 3: Namen und Ablage von Hilfsfunktionen, keine Prüfung rot).

1. `phaseBeendenKnopf = "Phase beenden"` steht zweimal, in
   [schlachtrundenTest.py](../../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py)
   und [beendenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/beendenTest.py)
   (Wir 3).
2. Nur `phasen/bewegung/` hat ein `__init__.py`, damit die zwei `beendenTest.py` nicht
   kollidieren. `phasen/aufstellen/` und `querschnitt/` haben keins. Die nächste gleich
   benannte Datei in einem dieser Ordner bricht `pytest technik/tests` wieder ab.
   [Tests](../../technik/architektur/tests.md) regelt das bisher nur für `tests/einheit/`.
3. Aus Anliegen 5260, von dir für Technikphase 9 angenommen:
   `istHandlung` in [bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py) zählt V9 und
   V14 als Handlung; nach V7 sind sie Auswählen (Anliegen 5140).
4. Aus 5260: Die Fixture `schlachtInDerKommandophase` heißt nach der Kommandophase. Die Tests
   zu QUE-10.2 und 10.5 laufen aber in einer anderen *Phase*.
5. Aus 5260: `ebeneTest.py` lädt `schlacht.py` gleich beim Import (zusammen mit
   [4921](4921-klickUndHandgriffeDerSchlachtFuerSpaeter.md), Punkt 2).

**Kosten.** Punkt 1: eine Zeile verschieben. Punkt 2: je Ordner unter `tests/akzeptanz/` ein
leeres `__init__.py`; die Regel in Tests erweitere ich. Punkte 3 bis 5 wie in 5260.

**Gegenvorschlag.**
1. Nach `bildschirm.py` neben `beendenKnopf`.
2. Ein `__init__.py` in jedem Ordner unter `tests/akzeptanz/`, wie in `tests/einheit/`. Ich
   fasse die Regel in [Tests](../../technik/architektur/tests.md) für beide Bäume.
3. `istHandlung` ohne `/ebene` und `/anklicken`.
4. Nach dem Zustand benennen, den sie liefert.
5. Mit 4921.
