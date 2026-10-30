# Voller Mutationslauf parallel

Form: Kritik
Von: Reviewer
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Wunsch des Stakeholders aus der DoD (Wortlaut in
Anliegen 8043, Runde 1): Mutationstests gezielt, „und falls
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
Umgesetzt: `mutationsregeln/mutation.py` verteilt die Mutanten eines Moduls auf alle Kerne,
je Kern eine Kopie in `/tmp`, im gezielten wie im vollen Lauf; die Zeile je fertigem Modul
bleibt. Scheiter-Test: `testMutantenLaufenParallelJeKernInEigenerKopie`.

**Probe.** `messen.py` Zeilen 1-70, 45 Mutanten: 1 Kern 1129 s, 8 Kerne 667 s (1,7-mal
schneller). Gleiche Überlebende (0 und 0), 0 Zeitüberschreitungen in beiden Läufen; das
Timeout-Risiko hat sich nicht gezeigt.

**Ursache des geringen Gewinns** (nur teilweise belegt). Gemessen: Die Browser-Tests der
Akzeptanz skalieren nicht mit der Kernzahl; `bedienungTest.py` allein 10 s, achtmal gleichzeitig
18,5 s, das ist 4,6-fach statt 8-fach (Chromium belegt selbst mehrere Kerne). Nicht gemessen,
aber wahrscheinlich: Die Messung unter coverage über alle Tests und das Anlegen der Kopien
laufen vorab einmal seriell und stecken in beiden Zeiten; dazu verteilen sich 45 Mutanten
ungleich (ein Überlebender prüft sich gegen alle Tests nach). Billig behebbar ist das nicht:
Die Last der Browser-Tests bleibt, und die Messung zu verteilen hieße, die Abdeckungskarte
zu zerlegen. Bei einem vollen Lauf mit vielen Mutanten fällt der serielle Vorlauf weniger ins
Gewicht; dort ist mehr Gewinn zu erwarten, ungemessen.

**Rückweg.** `git checkout prozess/pruefungen/mutationsregeln/mutation.py
prozess/pruefungen/mutationsregeln/mutationTest.py prozess/regeln/mutationsregeln.md`; das
Anliegen wieder auf `Status: offen`, `Wartet auf: Prozessphase 9`.
