# Fliegen: doppelte Typnamen und ein Import über den falschen Ort

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Kritik am Code zu Item fliegen, Abschnitt B (`3c78499`). Wartet nach
[Kritik](../../prozess/ablauf/kritik.md): Namen und Ablage, keine Prüfung rot, am Bildschirm
kein Unterschied.
1. [fliegenTest.py](../../technik/tests/einheit/domaene/phasen/bewegung/fliegenTest.py) Zeile 5
   importiert `Umgebung` und `Weite` aus `fliegen.py`. Beide stehen seit dem Umbau in
   `normaleBewegung.py`; `fliegen.py` importiert sie nur selbst. Braucht `fliegen.py` einen
   der Namen nicht mehr, bricht der Test, obwohl sich nichts Fachliches geändert hat.
2. `normaleBewegung.py` Zeile 11 und 12 führen `type Stellen` und `AnteilAufDemWeg` neu ein.
   `anhaltenAufDemWeg.py` Zeile 9 und 10 hat beide schon: dasselbe `Stellen` und, nur anders
   benannt, `AnteilBisZumAnhalten`. Vor dem Umbau kam `Stellen` von dort. Das Gleiche steht
   nun zweimal ([Wir 3](../../prozess/praemissen/wir.md)). `normaleBewegung.py` importiert
   aus dieser Datei schon `Weiterrücken`, ein Kreis entstünde also nicht.
3. `fliegen.py` Zeile 96 und 112 schreiben `verschobenUm` aus, das die Datei importiert und
   in Zeile 45 und 68 nutzt. Zeile 70 bis 72 bauen die *Umgebung* von Hand neu, um `weiten`
   zu leeren; `_art` in `__init__.py` nutzt dafür `replace`.

**Kosten.** Bleibt es so: Wer `Stellen` ändert, muss zwei Stellen finden, und der Test führt
beim Lesen an den falschen Ort. Der Umbau sind etwa acht Zeilen ohne neue Logik; die
Einheitstests unter `phasen/bewegung` bleiben gültig.

**Gegenvorschlag.**
1. In `fliegenTest.py` `Umgebung` und `Weite` aus `normaleBewegung` importieren.
2. `normaleBewegung.py` importiert `Stellen` aus `anhaltenAufDemWeg.py`; `AnteilAufDemWeg`
   entfällt zugunsten von `AnteilBisZumAnhalten`.
3. In `fliegen.py` Zeile 96 und 112 `verschobenUm` aufrufen, in Zeile 70 bis 72
   `replace(self._umgebung, weiten={})`.

**Stellungnahme.**
