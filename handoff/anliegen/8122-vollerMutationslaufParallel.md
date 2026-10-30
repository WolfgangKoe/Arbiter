# Voller Mutationslauf parallel

Form: Kritik
Von: Reviewer
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: Prozessphase 9

## Runde 1
**Befund.** Wunsch des Stakeholders aus der DoD (Wortlaut in
[8043](8043-leistenTestsRotOhneSchwankung.md), Runde 1): Mutationstests gezielt, „und falls
wirklich alles durchlaufen muss, dass parallelisiert und der Fortschritt protokolliert wird“.
Gezielt gibt es ([Mutationsregeln](../../prozess/regeln/mutationsregeln.md)), den Fortschritt
bringt Retro P9 (6960). Parallel fehlt: `mutationsregeln/mutation.py` prüft alle Mutanten
nacheinander in einer Kopie; der Rechner hat 8 Kerne. Annahme bis zu seiner Antwort in 8043 F1.

**Kosten.** Ohne: Der volle Lauf nach der DoD über das Inkrement dauert so lang wie heute.
Mit: mehr Prüfcode und je Kern eine Kopie in `/tmp`.

**Gegenvorschlag.** Bestehende Regel anpassen ([Ich 4](../../prozess/praemissen/ich.md)): die
Zeile der Mutationsregeln um „`--voll` verteilt die Module auf die Kerne, je Kern eine Kopie“
ergänzen, mit dem Regelumsetzer zusammen mit P9 bauen (Protokollzeile je Modul gilt dann je
fertigem Modul, gleich auf welchem Kern). Probe an einer Kopie in `/tmp` mit Dauer vorher und
nachher; Rückweg: die Zeile und den Aufruf zurücknehmen.

**Stellungnahme.**
