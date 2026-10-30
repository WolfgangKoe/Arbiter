# Docstrings in den neuen Modulen des Katalogs

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Code zu Item katalogwerteGliedern (`git diff e1fb48b`). Hält auf nach
[Kritik](../../prozess/ablauf/kritik.md): neuer Code verletzt
[Es 8](../../prozess/praemissen/es.md), `testDasRepoHältDieDocstringregelUnterTechnik` ist
rot. Neu in diesem Item, nicht Bestand aus [6982](6982-docstringsImProduktcode.md):
1. [datenblaetter.py](../../technik/arbiter/katalog/datenblaetter.py): der Kopf und der
   Docstring an `eintragLesen`.
2. [yamlLesen.py](../../technik/arbiter/katalog/yamlLesen.py): der Kopf.

Der Kopf von [ausgangslage.py](../../technik/arbiter/katalog/ausgangslage.py) ist Bestand
(6982).

**Kosten.** Am Bildschirm nichts. Bleiben sie, wächst der Bestand, den 6982 in derselben
Technikphase abbaut.

**Gegenvorschlag.** Die drei Docstrings streichen. Was nur der Docstring von `eintragLesen`
trägt („genau diese Schlüssel“), in den Namen, etwa `genauDieseSchlüsselLesen`. Erledigt:
`python3 -m pytest prozess/pruefungen/formregeln/kommentareTest.py` meldet keine der beiden
Dateien.

**Stellungnahme.** Angenommen und umgesetzt: Die Köpfe von
[datenblaetter.py](../../technik/arbiter/katalog/datenblaetter.py) und
[yamlLesen.py](../../technik/arbiter/katalog/yamlLesen.py) und der Docstring an
`eintragLesen` sind gestrichen; die Funktion heißt jetzt `genauDieseSchlüsselLesen` (auch in
[ausgangslage.py](../../technik/arbiter/katalog/ausgangslage.py) und den Einheitstests). Die
Docstring-Prüfung meldet keine der beiden Dateien mehr; der Kopf von ausgangslage.py bleibt
Bestand (6982).
