# Neue Docstrings im Umzug zu 6102 und 6290

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Code zu 6102 und 6290 (`git diff e1fb48b`). Hält auf nach
[Kritik](../../prozess/ablauf/kritik.md): neuer Code verletzt
[Es 8](../../prozess/praemissen/es.md) (Docstring nur als Kopf einer Akzeptanztestdatei),
die Prüfung `testDasRepoHältDieDocstringregelUnterTechnik` ist rot. In Technikphase 9 neu
geschrieben, nicht nur verschoben:
1. [messen.py](../../technik/arbiter/domaene/messen.py): Docstrings an
   `_anteilDesNächstenPunkts` und `ersterSchrittMit`.
2. [phasen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/__init__.py): der Kopf
   „Was mehrere Phasen brauchen …“.

**Kosten.** Am Bildschirm nichts. Bleibt es, wächst der Bestand aus
[6982](6982-docstringsImProduktcode.md), den dieselbe Technikphase wieder abbaut; das
Gesetz von `ersterSchrittMit` (`trifft` ist monoton) steht dann nirgends.

**Gegenvorschlag.** Die drei Docstrings streichen. Was nur der Docstring trägt, in den Namen:
etwa `ersterSchrittMit(abDemTrifft, bis)` oder ein Parametername, der „ab dem gilt es“
sagt. Die verschobenen Docstrings (`verschobeneStellen`, `querschnitt/setzen.py`) gehören zu
6982. Erledigt: `python3 -m pytest prozess/pruefungen/formregeln/kommentareTest.py` meldet
`messen.py` und `phasen/__init__.py` nicht mehr.

**Stellungnahme.** Angenommen, umgesetzt. In
[messen.py](../../technik/arbiter/domaene/messen.py) sind die Docstrings an
`_anteilDesNächstenPunkts` und `ersterSchrittMit` gestrichen; das Gesetz steht im Parameternamen
(`ersterSchrittMit(trifftMonotonAb, bis)`). Der Kopf in
[phasen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/__init__.py) ist gestrichen.
`kommentareTest.py` meldet beide Dateien nicht mehr; die übrigen Meldungen sind die 6981/6982.
