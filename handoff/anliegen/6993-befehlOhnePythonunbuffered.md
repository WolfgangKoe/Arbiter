# Der Test des Befehls startet Arbiter ungepuffert

Form: Kritik
Von: Reviewer
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

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

**Stellungnahme.**
