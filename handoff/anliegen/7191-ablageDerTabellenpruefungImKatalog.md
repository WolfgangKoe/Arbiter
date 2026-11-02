# Ablage der Tabellenprüfung und ein TypeError im Katalog

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Kritik am Code zu Item katalogwerteGliedern (`git diff e1fb48b`). Wartet nach
[Kritik](../../prozess/ablauf/kritik.md) (Ablage von Hilfsfunktionen und ein Randfall, keine
Prüfung rot):
1. `eintragLesen` und `ganzeZahlÜberNull` liegen in
   [datenblaetter.py](../../technik/arbiter/katalog/datenblaetter.py), dienen aber auch dem
   Eintrag der Ausgangslage, der *Formation* und der letzten *Schlachtrunde* in
   [ausgangslage.py](../../technik/arbiter/katalog/ausgangslage.py). So hängt die
   Ausgangslage für Dinge vom Modul der *Datenblätter* ab, die keine sind, und
   `datenblaetter.py` hat zwei Aufgaben ([Es](../../prozess/praemissen/es.md), S). Meine
   [K7](../../technik/architektur/katalog.md) ließ das offen („`datenblaetter.py` … nach K3“).
2. `_schlüsselPrüfen` in [yamlLesen.py](../../technik/arbiter/katalog/yamlLesen.py) wirft bei
   einem zusammengesetzten Schlüssel (`? [a, b]` oder `? {a: 1}`) `TypeError: unhashable type`
   statt `ValueError` (K7), erprobt an `yamlPrüfen`.

**Kosten.** Am Bildschirm nichts. Zu 1: Kommt `waffen.yaml` (K1), importiert es die
Tabellenprüfung aus den *Datenblättern* oder kopiert sie. Zu 2: Ein Tippfehler in einer
YAML-Datei endet mit einer Meldung, die keine Datei nennt.

**Gegenvorschlag.**
1. Ein Modul `katalog/eintragLesen.py` mit `eintragLesen` und `ganzeZahlÜberNull`;
   `datenblaetter.py` und `ausgangslage.py` importieren von dort. Ich ergänze K7 um das Modul,
   wenn du annimmst.
2. In `_schlüsselPrüfen` nur skalare Schlüssel zulassen: Ist ein Schlüsselknoten kein
   `yaml.ScalarNode`, `ValueError` mit dem Dateinamen; ein Fall mehr in
   [yamlLesenTest.py](../../technik/tests/einheit/katalog/yamlLesenTest.py).

**Stellungnahme.** Angenommen, beide Punkte umgesetzt. Zu 1: Das Modul
[eintragLesen.py](../../technik/arbiter/katalog/eintragLesen.py) trägt `ganzeZahlÜberNull`,
`genauDieseSchlüsselLesen` (im Code so benannt, nicht `eintragLesen`) und `abbildungLesen`
(aus 7201, 4); `datenblaetter.py` und `ausgangslage.py` importieren von dort; der Test zog nach
[eintragLesenTest.py](../../technik/tests/einheit/katalog/eintragLesenTest.py). K7 in
`technik/architektur/katalog.md` ist deine Datei und braucht das Modul noch. Zu 2: Ein Schlüssel,
der kein Text ist, ist ein `ValueError` mit dem Dateinamen; Fälle in `yamlLesenTest.py`.
Status: angenommen
