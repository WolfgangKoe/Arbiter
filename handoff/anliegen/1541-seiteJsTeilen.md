# seite.js liegt über dem Höchstmaß

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: offen
Wartet auf: Domänenphase

## Runde 1
**Befund.** [seite.js](../../technik/frontend/seite.js) hat 12.124 Zeichen, das Höchstmaß
eines Code-Moduls ist 12.000, das Kürzungsmaß 8.000 ([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße)).
Nach Anliegen 1440, Punkt 4, wächst sie nicht mehr (vorher
12.486). Kein Item nennt die Teilung, kein Backlog führt sie. Nach [Ich 3](../../prozess/praemissen/ich.md)
wartet es: Höchstmaße sind nur Text, keine Prüfung ist rot.

**Kosten.** Jedes Item mit Oberfläche (Plan 7: *zurücklegen*, „gemeinsam übergehen“) ändert
`seite.js` und darf sie nicht wachsen lassen; ohne Item steht es vor einer Sperre ohne Weg.

**Gegenvorschlag.** In Plan 7 ein Item vor dem ersten Item mit Oberfläche: `seite.js` teilen
bis höchstens 8.000 Zeichen je Datei, Verhalten unverändert (Bildschirmtests grün). Die
Schnitte nach Aufgabe (Zeichnen, Ziehen und Klicken, Anfragen) legt der Architekt im Vertrag
fest ([Oberfläche](../../technik/architektur/oberflaeche.md)).

**Stellungnahme.**
