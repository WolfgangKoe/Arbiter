# Test von verschobeneStellen am alten Ort

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Wartet (Namen und Ablage, keine Prüfung rot). `verschobeneStellen` liegt jetzt in
[phasen/__init__.py](../../technik/arbiter/domaene/phasen/__init__.py), seine zwei Tests stehen
weiter in
[einheitVerschiebenTest.py](../../technik/tests/einheit/domaene/phasen/aufstellen/einheitVerschiebenTest.py),
dem Test von `einheitVerschieben.py` ([Es 2](../../prozess/praemissen/es.md): Test zu einem
Modul `<modul>Test.py`).

**Kosten.** Wer den Test zu `verschobeneStellen` sucht, findet ihn nicht neben dem Modul.

**Gegenvorschlag.** Die beiden Tests nach `tests/einheit/domaene/phasenTest.py`, sobald der
Architekt die Ablage der Helfer in `phasen/__init__.py` entschieden hat (6122, Punkt 2 und 3).

**Stellungnahme.** Angenommen, anders umgesetzt nach Anliegen 8020: `verschobeneStellen` liegt jetzt
in [einheitVerschieben.py](../../technik/arbiter/domaene/phasen/aufstellen/einheitVerschieben.py),
seine Tests stehen im passenden `einheitVerschiebenTest.py`.

Status: angenommen
