# Unit-Test des Verschiebens am alten Ort

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Code zu 6102 und 6290 (`git diff e1fb48b`). Wartet nach
[Kritik](../../prozess/ablauf/kritik.md) (Ablage, keine Prüfung rot):
`verschobeneStellen` liegt jetzt in
[phasen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/__init__.py), seine zwei
Unit-Tests stehen weiter in
[einheitVerschiebenTest.py](../../technik/tests/einheit/domaene/phasen/aufstellen/einheitVerschiebenTest.py).
Nach [Tests](../../technik/architektur/tests.md) spiegelt `tests/einheit/` den Ordner
`arbiter/`; zu `phasen/aufstellen/__init__.py` gehört `phasen/aufstellenTest.py`, zu
`phasen/__init__.py` also `tests/einheit/domaene/phasenTest.py`.

**Kosten.** Am Bildschirm nichts. Bleibt es, sucht man den Test einer Hilfe aller Phasen
bei der *Aufstellung*, und eine Änderung an AUF-24 löscht ihn leicht mit.

**Gegenvorschlag.** Die zwei Tests `testDieGruppeFolgtDemWegDesGezogenen…` und
`testEinNochNichtGesetztesModellBewegtDieGruppeNicht` nach
`tests/einheit/domaene/phasenTest.py`; `einheitVerschiebenTest.py` behält die Tests zu
`hineingerückt`.

**Stellungnahme.** Angenommen, anders umgesetzt: Nach Anliegen 8020 liegt `verschobeneStellen` in
[einheitVerschieben.py](../../technik/arbiter/domaene/phasen/aufstellen/einheitVerschieben.py);
die zwei Tests stehen damit schon bei ihrem Modul in `einheitVerschiebenTest.py`.

Nachgeprüft (Architekt): Test und Modul passen zusammen, Einheitentests und `spiegel.py` grün.
