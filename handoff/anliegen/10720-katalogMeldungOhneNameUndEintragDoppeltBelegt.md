# Katalog: Meldung ohne Modellart, Eintrag doppelt belegt

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Kritik am Code (Lesbarkeit) zur Umsetzung von
[7191](7191-ablageDerTabellenpruefungImKatalog.md) und
[7201](7201-katalogLiestMehrfachUndPrueftSchluesselAmText.md), uncommittet. Wartet nach
[Kritik](../../prozess/ablauf/kritik.md) (Meldungen, Namen von Hilfen, keine Prüfung rot:
Einheitstests Katalog 56 grün, ruff, Benennung, Kommentare, Importvertrag, Glossar grün).
1. `_modellzahlLesen` in [ausgangslage.py](../../technik/arbiter/katalog/ausgangslage.py)
   meldet nur „Die Zahl der Modelle muss eine ganze Zahl über 0 sein: 0“; vorher nannte die
   Meldung die *Modellart*. `abbildungLesen` in
   [eintragLesen.py](../../technik/arbiter/katalog/eintragLesen.py) kennt den Namen, gibt ihn
   aber nicht weiter; ebenso fehlen *Datenblatt* und *Modellart* bei einem falschen Wert in
   `datenblaetter.yaml`.
2. Der Modulname `eintragLesen.py` nutzt den Begriff *Eintrag* des
   [Glossars](../../domaene/glossar.md) („Zeile des *Protokolls* je *gemeinsam übergehen*“)
   für etwas anderes: die Formprüfung von Katalogwerten ([Wir 2](../../prozess/praemissen/wir.md)).
3. `laden` in [ausgangslageTest.py](../../technik/tests/einheit/katalog/ausgangslageTest.py)
   bindet `fraktionen: dict = datenblätter` als Standardwert, die Nachbarparameter nehmen
   `None` mit `or`. Der Ersatz `datenblätterVon` meldet noch „hat keinen Ordner“, das Produkt
   inzwischen „hat keine datenblaetter.yaml“.

**Kosten.** Am Bildschirm nichts. Zu 1: Ein Tippfehler in `ausgangslage.yaml` mit mehreren
*Einheiten* lässt suchen, welche gemeint ist. Zu 2: Wer nach *Eintrag* sucht, landet im
Katalog statt beim *Protokoll*. Zu 3: ein Parameter anders gebaut als seine Nachbarn, eine
veraltete Meldung. Je Punkt wenige Zeilen; zu 2 zieht der Architekt K7 in
[katalog.md](../../technik/architektur/katalog.md) nach.

**Gegenvorschlag.**
1. `abbildungLesen` stellt den Namen vor die Meldung aus `lesen`
   (`except ValueError as fehler: raise ValueError(f"{was}, {name}: {fehler}") from fehler`);
   dann nennen alle drei Aufrufer den Weg (Datenblatt, Modellart, Wert), ohne eigene Zeile.
   Ein Fall in [eintragLesenTest.py](../../technik/tests/einheit/katalog/eintragLesenTest.py).
2. Ein Name ohne Glossarbegriff, etwa `katalogwerteLesen.py`, mit Test
   `katalogwerteLesenTest.py`.
3. `fraktionen: dict | None = None` und `datenblätterVon(fraktionen or datenblätter)`; die
   Meldung des Ersatzes wie im Produkt oder ohne Text.

**Stellungnahme.**
