# Neue Tests zu 15462: Fixture `spinne` und Hilfe zum Übergehen doppelt

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Ablage der Hilfen in den neuen Akzeptanztests seit `5ffc953`. Keine Prüfung
ist rot, deshalb wartet es ([Kritik](../../prozess/ablauf/kritik.md)). Gegen
[Wir 3](../../prozess/praemissen/wir.md) steht beides zweimal:
1. Die Fixture `spinne` gibt es zweimal. Neu ist sie in
   [weiterziehenNachDemUebergehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/weiterziehenNachDemUebergehenTest.py)
   als eigener Generator über `spielerZwei.armee.einheiten`. Schon da war sie in
   [fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py) über
   `einheitDerSpinne` und `einheitMitDemNamen`. `overlord` und `spielerZwei` stehen in
   `tests/akzeptanz/conftest.py`.
2. `übergehenBisZumNächstenZugDerNecrons` in `fliegenTest.py` wiederholt den Rumpf von
   `orksÜbergehenBisZumZugDerNecrons` aus
   [schlacht.py](../../technik/tests/akzeptanz/schlacht.py) Zeile für Zeile, Prüfung und
   Meldung inbegriffen, und hängt nur einen weiteren `zurBewegungsphaseDesNächstenZugs` an.
   Den Namen `orks…` kann sie nicht nutzen, denn sie zieht *Modelle* der Necrons.

**Kosten.** Je Punkt ein paar Zeilen, das Verhalten bleibt gleich. Ohne die Änderung ändert
man bei der nächsten Änderung an der Suche nach einer *Einheit* oder an der Vorbedingung
„steht am Ort des Tests“ nur eine der beiden Fassungen.

**Gegenvorschlag.**
1. `einheitDerSpinne` und `spinne` nach `tests/akzeptanz/conftest.py`, neben `overlord`.
   Beide Testdateien nutzen dann diese.
2. In `schlacht.py` eine Hilfe ohne Armee im Namen, die *Modelle* anhält, *gemeinsam übergeht*
   und die Vorbedingung prüft (etwa `übergehenAmOrtDesTests(schlacht, stellen)`).
   `orksÜbergehenBisZumZugDerNecrons` und die neue Hilfe rufen sie auf und fügen nur ihre
   Züge hinzu.

**Stellungnahme.**
