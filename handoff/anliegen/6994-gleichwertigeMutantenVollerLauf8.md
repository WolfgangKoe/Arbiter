# Gleichwertige Mutanten des vollen Laufs von Zyklus 8

Form: Kritik
Von: Reviewer
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Im vollen Mutationslauf von Zyklus 8 (93 %, [DoD](../../prozess/ablauf/dod.md))
sind 18 Überlebende gleichwertig, am Code nachgeprüft; noch nicht in
[gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json):
1. `missionsvorbereitung/ausgangslage.py` Zeile 15, `zweite = 2`, `2 wird 3`: Den Wert von
   `Aufstellungszone` liest kein Code, nur die Identität.
2. `phasen/aufstellen/setzenPerKlick.py` Zeile 28, `strict=True`, `True wird False`:
   `versätze` hat stets so viele Einträge wie `formation.reihen` (`accumulate` mit `initial`
   über die Paare der Reihen).
3. `phasen/aufstellen/setzenPerKlick.py` Zeile 55, `abs(vorn - hinten)`, `Sub wird Add`: Die
   Lagen einer Reihe liegen symmetrisch um null; mit `hinten` ist auch `-hinten` eine Lage, das
   Minimum bleibt gleich.
4. `web/darstellung.py` Zeile 83, `endeY - anfangY`, `Sub wird Add`: `grenzenDerZone` gibt
   in y stets `(0, länge)`.
5. `web/server.py` Zeile 32, `daemon=True`, `True wird False`: Der Befehl beendet den Server
   stets mit `beenden` (Strg+C), die Tests über ihre Fixture; `daemon` wirkt nur, wenn ein
   Aufrufer das auslässt.
6. 13 Argumente von `@dataclass` in `spielobjekte.py` (Zeilen 5, 12, 24, 29, 35, 41, 54) und
   `missionsvorbereitung/ausgangslage.py` (18, 26). `frozen=True` wird False (9): Kein Code
   weist einem Feld neu zu (mypy prüft das), keiner hasht Base, Stelle, Spielfeld oder
   Formation. `eq=False` wird True (4: Ausgangslage, Einheit, Armee, Spieler): Gleich wären nur
   Einheiten mit denselben Modellen oder Spieler mit derselben Armee; das verbietet
   `Ausgangslage.__post_init__`, und Armee und Ausgangslage vergleicht oder hasht kein Code.

Zwei weitere Überlebende (`aufstellen/__init__.py:170`, `schlachtrunden.py:120`) klärt
[Anliegen 6300](6300-anklickenUndFremdesModellLoslassen.md); die übrigen gehen als Lücken an
Implementierer und Testautor (6991 bis 6993).

**Kosten.** Ohne Einträge bleibt der volle Lauf rot. Mit den 18 Einträgen überleben 14 von 479,
97 %. Am Bildschirm nichts.

**Gegenvorschlag.** 1 bis 5 eintragen, Pfade wie im Lauf (`technik/arbiter/…`). Für 6 empfehle
ich statt 13 gleicher Gründe eine Regel: `mutanten.py` mutiert keine Argumente von
`@dataclass` (bestehende Regel angepasst: die Fehlerarten der
[Mutationsregeln](../../prozess/regeln/mutationsregeln.md), Ich 4). Grund: Jede neue
Datenklasse brächte sonst wieder solche Einträge. Nachteil: Der heute gefangene Mutant
`eq=False` an `Modell` fällt mit weg. Bauen würde es der Regelumsetzer mit Scheiter-Test;
nicht an einer Kopie erprobt, Rückweg: Ausnahme streichen. Sonst alle 13 eintragen.

**Stellungnahme.** Umgesetzt mit 11 Einträgen in
[gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json): 1 bis 5 je
einer, 6 als 6 Einträge. Die Begründungen habe ich am Code nachgeprüft. Die Regel in
`mutanten.py` lehne ich ab. Ein Eintrag gilt für Datei, Quellzeile und Fehler, also für jede
gleich lautende Zeile der Datei. Eine neue Datenklasse mit demselben Dekorator in derselben
Datei braucht darum keinen neuen Eintrag. Die Regel spart also kaum etwas, kostet aber Bau und
Scheiter-Test (Absicht 2: erst Bestand abbauen). Außerdem verlöre sie alle Fehler an `@dataclass` auch dort, wo sie
fangen. `frozen=False` macht eine Datenklasse mit `eq=True` unhashbar; hasht künftig Code sie,
fängt das ein Test. Denselben Nachteil wie die Regel hat
der Eintrag `@dataclass(frozen=True, eq=False)`, `False wird True`, in `spielobjekte.py`: Der
gefangene Mutant an `Modell` (Zeile 29) teilt die Quellzeile und zählt nicht mehr. Das habe ich
gegen die Mutanten von `mutanten.py` nachgezählt, ohne Testlauf: 19 statt 18 zählen nicht, 14
von 483 überleben, gut 97 %. Den vollen Lauf führt die Retro aus.
