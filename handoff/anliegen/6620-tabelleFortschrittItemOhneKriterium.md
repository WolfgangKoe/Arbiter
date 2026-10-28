# Die Tabelle des Fortschritts kennt kein Item ohne Kriterium

Form: Kritik
Von: Regelumsetzer
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [Fortschritt](../../prozess/ablauf/fortschritt.md) führt die Zeilen zu Vertrag, Tests,
Kritik an den Tests und „Tests grün“ „je Item“. `standregeln/fortschritt.py` schreibt sie seit
Anliegen 4301 nur für ein Item, dessen Text ein Kriterium nennt.

**Kosten.** Tabelle und Mechanismus widersprechen sich ([Wir 3](../../prozess/praemissen/wir.md)).

**Gegenvorschlag.** Die Tabelle sagt für diese vier Zeilen „je Item mit Kriterium“; Kritik am
Code, Abnahme und Löschen gelten je Item.

**Stellungnahme.** Umgesetzt in der Tabelle von
[Fortschritt](../../prozess/ablauf/fortschritt.md): Vertrag, Tests mit Kritik daran und
„Tests grün“ gelten „je Item mit Kriterium“; die Kritik am Code steht als eigene Zeile
„Technik 3 je Item“, Abnahme und Löschen bleiben „je Item“.
