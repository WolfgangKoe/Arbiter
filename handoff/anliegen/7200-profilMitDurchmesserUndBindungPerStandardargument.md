# Profil mit Durchmesser und Bindung per Standardargument im Katalog

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 2/3
Status: erledigt

## Runde 1
**Befund.** Kritik am Code zu Item katalogwerteGliedern (`git diff e1fb48b`). Hält auf nach
[Kritik](../../prozess/ablauf/kritik.md): neuer Code verletzt die Lesbarkeit
([Es](../../prozess/praemissen/es.md), „der Name trägt die Bedeutung“, Es 7). Die Docstrings
stehen schon in [7190](7190-docstringsImNeuenKatalog.md).
1. `Profil` in [datenblaetter.py](../../technik/arbiter/katalog/datenblaetter.py) hält
   `bewegungsweite` und `durchmesser`. Nach dem [Glossar](../../domaene/glossar.md) ist das
   *Profil* die Werte der *Modellart* (darunter die *Bewegungsweite*), der *Durchmesser* gehört
   der *Base* der *Modellart*; [K2](../../technik/architektur/katalog.md) trennt beide: „Das
   Profil und der Durchmesser stehen bei der Modellart“. Was der Typ abbildet, ist der Eintrag
   einer *Modellart* (die Ebene aus K2, so auch in `datenblaetter.yaml`). Ebenso `profilLesen`,
   `_profilzeilen` und der Einheitstest
   `testDieWerteJedesModellsKommenAusDemProfilSeinerModellart`.
2. `laden(armeen, formation: dict = formation, …)` in
   [ausgangslageTest.py](../../technik/tests/einheit/katalog/ausgangslageTest.py) bindet die
   Modulkonstante per Standardargument (Es 7) und verdeckt dabei die gleichnamigen
   Modulnamen `formation` und `armeen`.

**Kosten.** Am Bildschirm nichts. Zu 1: Kommt mit der nächsten Anforderung ein zweiter Wert
des *Profils* (etwa der Widerstand) oder ein Wert der *Modellart*, der keiner des Profils ist,
weiß der Leser nicht, wohin er gehört; der Name widerspricht dem Glossar, das der Reviewer
gegen den Code hält (DoD 2). Eine Umbenennung in einer Datei und zwei Tests. Zu 2: drei Zeilen.

**Gegenvorschlag.**
1. Der Typ heißt `Modellart` (Felder unverändert), `Datenblatt = Mapping[str, Modellart]`,
   dazu `modellartLesen`, `_modellartzeilen`; der Test etwa
   `testDieWerteJedesModellsKommenAusSeinerModellart`. Ein eigener Typ `Profil` erst, wenn
   ein Kriterium einen zweiten Wert des Profils liest.
2. `formation: dict | None = None` wie bei `onlyWar`, im Rumpf
   `formation or formationDerBoyz`, die Modulkonstante umbenannt (`formationDerBoyz`,
   `armeenMitBoyz`), damit kein Parameter einen Modulnamen verdeckt.

Erledigt: kein `Profil` mehr in `technik/arbiter/katalog/` und
`technik/tests/einheit/katalog/`, `python3 -m pytest technik/tests/einheit/katalog` grün.

**Stellungnahme.** Angenommen und umgesetzt, beide Punkte. 1: `Profil` heißt `Modellart`,
dazu `modellartLesen`, `_modellartzeilen` und der Test
`testDieWerteJedesModellsKommenAusSeinerModellart` ([datenblaetter.py](../../technik/arbiter/katalog/datenblaetter.py),
[datenblaetterTest.py](../../technik/tests/einheit/katalog/datenblaetterTest.py)). 2:
`laden(armeen, formation: dict | None = None, …)` mit `formation or formationDerBoyz`; die
Konstanten heißen `formationDerBoyz` und `armeenMitBoyz`
([ausgangslageTest.py](../../technik/tests/einheit/katalog/ausgangslageTest.py)). Kein
`Profil` mehr im Katalog; `technik/tests/einheit/katalog` grün.

## Runde 2
**Befund.** Nachgeprüft: Beide Punkte sind inhaltlich umgesetzt; kein `Profil` mehr in
`technik/arbiter/katalog/` und `technik/tests/einheit/katalog/`, dort 48 Tests grün; die
Akzeptanztests importieren `Profil` nicht. Hält auf nach [Kritik](../../prozess/ablauf/kritik.md)
(„eine Prüfung ist rot“): Die Umsetzung macht ruff rot.
1. `ruff check`: [datenblaetterTest.py](../../technik/tests/einheit/katalog/datenblaetterTest.py)
   Zeile 5, der Import ist 101 Zeichen lang (E501) und nicht nach isort gegliedert (I001).
2. `ruff format --check`: [ausgangslageTest.py](../../technik/tests/einheit/katalog/ausgangslageTest.py)
   sechs Aufrufe `laden(armeenMitBoyz,…)` ohne Leerzeichen nach dem Komma (Zeilen 109, 121,
   129, 134, 139, 157); dazu die Importzeile aus 1.

**Kosten.** Am Bildschirm nichts. Ohne Nachbesserung bleibt der Commit des Items rot, auch
wenn die Rückverfolgung grün ist. Zwei Befehle.

**Gegenvorschlag.** `ruff check --fix technik/tests/einheit/katalog` und
`ruff format technik/tests/einheit/katalog`. Erledigt: `ruff check` und `ruff format --check`
über `technik/tests/einheit/katalog` grün, `python3 -m pytest technik/tests/einheit/katalog`
grün.

**Stellungnahme.** Angenommen und umgesetzt: `ruff check --fix` und `ruff format` über
[technik/tests/einheit/katalog](../../technik/tests/einheit/katalog) (Import in
[datenblaetterTest.py](../../technik/tests/einheit/katalog/datenblaetterTest.py) mehrzeilig,
Aufrufe in [ausgangslageTest.py](../../technik/tests/einheit/katalog/ausgangslageTest.py)
formatiert). `ruff check`, `ruff format --check` über den Ordner und
`python3 -m pytest technik/tests/einheit/katalog` (48 Tests) grün.
