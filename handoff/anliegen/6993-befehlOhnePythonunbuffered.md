# Der Test des Befehls startet Arbiter ungepuffert

Form: Kritik
Von: Reviewer
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Im vollen Mutationslauf von Zyklus 8 überlebt
[`__main__.py`](../../technik/arbiter/__main__.py) Zeile 48, `True wird False`: `print(…,
flush=True)` der Adresse. `Befehl._prozessStarten` in
[conftest.py](../../technik/tests/akzeptanz/conftest.py) Zeile 65 setzt `PYTHONUNBUFFERED=1`;
so startet niemand Arbiter, und die Tests zu QUE-8 lesen die Adresse auch ohne `flush`.

**Kosten.** Am Bildschirm nichts. Fällt `flush` weg, erscheint die Adresse über eine Pipe erst
beim Ende, und kein Test merkt es. Wir: 1 der 32 Überlebenden; eine Zeile.

**Gegenvorschlag.** `"PYTHONUNBUFFERED": "1"` aus der Umgebung streichen. Dann fängt
`Befehl.starten` den Mutanten: `select` wartet 15 Sekunden, die Adresse bleibt leer.

**Stellungnahme.** Angenommen. `Befehl._prozessStarten` in
[conftest.py](../../technik/tests/akzeptanz/conftest.py) startet Arbiter jetzt ohne
`PYTHONUNBUFFERED`. Die Variable wird auch dann entfernt, wenn sie in der Umgebung des
Testlaufs schon gesetzt ist, sonst bliebe der Mutant dort am Leben. Probe an einer Kopie in
`/tmp`: Ohne Mutant sind die Tests zu QUE-2.1, QUE-8.1 und QUE-8.2 grün. Mit `flush=False`
scheitern beide Tests zu QUE-2.1, beide zu QUE-8.2 und alle, die Arbiter über den Befehl
starten (AUF-5.9, AUF-6.1, QUE-3.3). QUE-8.1 bleibt grün, weil es den Befehl nicht startet.
Für dich zum Weitergeben an den Architekten: B4 in
[Tests](../../technik/architektur/tests.md) nennt noch „mit `PYTHONUNBUFFERED=1`, sonst käme
sie in der Pipe zu spät“. Richtig ist jetzt: Die Adresse kommt nur dank `flush` rechtzeitig
an, und der Test prüft genau das.
