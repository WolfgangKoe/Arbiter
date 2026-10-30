# Katalog liest mehrfach und vergleicht Schlüssel am Text

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Kritik am Code zu Item katalogwerteGliedern (`git diff e1fb48b`). Wartet nach
[Kritik](../../prozess/ablauf/kritik.md) (Randfälle, Form von Hilfen, keine Prüfung rot).
Ablage von `eintragLesen` und zusammengesetzte Schlüssel: [7191](7191-ablageDerTabellenpruefungImKatalog.md).
1. `_schlüsselPrüfen` in [yamlLesen.py](../../technik/arbiter/katalog/yamlLesen.py)
   vergleicht den Text der Schlüssel, `safe_load` den gelesenen Wert. Erprobt an `yamlPrüfen`:
   `yes: 1` und `true: 2` gehen durch und werden `{True: 2}`, ebenso `1: a` und `0x1: b`
   zu `{1: 'b'}`; das zweite überschreibt still das erste, was K5 ausschließen will.
2. `_einheitLesen` in [ausgangslage.py](../../technik/arbiter/katalog/ausgangslage.py) ruft
   `datenblätterVon` je *Einheit*: Für vier Einheiten zweier *Fraktionen* liest
   `ausgangslageLaden()` die Datei viermal statt zweimal, jedes Mal dreifach geparst
   (`parse`, `compose`, `safe_load`).
3. `datenblätterLesen` in [datenblaetter.py](../../technik/arbiter/katalog/datenblaetter.py):
   Ist `datenblaetter.yaml` leer oder eine Liste, endet `.items()` im `AttributeError` statt im
   `ValueError` (K7); fehlt nur die Datei im vorhandenen Ordner, meldet es „hat keinen Ordner“.
4. `_modellzahlenLesen` und `_modellartenLesen` prüfen dasselbe (nicht leere Abbildung, je
   Wert eine Prüfung) mit zwei Meldungen.
5. `testEineEinheitMitVerschiedenenDurchmessernIstEinFehlerBeimLaden` in
   [ausgangslageTest.py](../../technik/tests/einheit/katalog/ausgangslageTest.py) umgeht
   `laden` und übergibt `gemischt.__getitem__`; eine unbekannte *Fraktion* gäbe dort
   `KeyError`. Dass neue Einheitstests wieder echte Dateien mit kopierten Werten lesen
   (`datenblaetterTest.py`, `yamlLesenTest.py`), gehört zu
   [5380](5380-testmodellUndKopierteWerteImKatalogtest.md), Befund 2.

**Kosten.** Am Bildschirm nichts. Zu 1: Ein Tippfehler in einem späteren Katalog fällt nicht
auf. Zu 2: ein Lesen je *Einheit* statt je *Fraktion*, wächst mit der Armee. Zu 3: eine
Meldung ohne Datei. Zu 4 und 5: zwei Stellen für dieselbe Regel, ein Test anders gebaut als
seine Nachbarn. Je Punkt wenige Zeilen.

**Gegenvorschlag.**
1. Mit 7191, 2: Ein Schlüssel ist ein `yaml.ScalarNode` mit dem Tag
   `tag:yaml.org,2002:str`, sonst `ValueError` mit dem Dateinamen; alle Schlüssel in
   `domaene/daten/` sind heute Text. Zwei Fälle mehr in `yamlLesenTest.py`.
2. `ausgangslageLaden()` übergibt `functools.cache(datenblätterLesen)`.
3. Die oberste Ebene über dieselbe Prüfung wie 4; die Meldung nennt die fehlende Datei.
4. Eine Hilfe `abbildungLesen(werte, lesen, was)` für beide.
5. `laden` bekommt die Datenblätter als Parameter, der Test ruft `laden`.

**Stellungnahme.**
