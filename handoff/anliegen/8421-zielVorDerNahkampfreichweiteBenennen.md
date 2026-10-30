# Ziel vor der Nahkampfreichweite benennen

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Wartet (Kritik: Namen von Hilfsfunktionen, keine Prüfung rot), Diff
`85fe22c..b473b0b`, Schnittstelle und Lesbarkeit. Die Änderung aus 8360 trifft das
Kriterium; die neue Prüfung in der Vorgeschichte, dass das Ziel in der *Nahkampfreichweite*
liegt, macht den Test erst aussagekräftig. Die Hilfsfunktion in
[anhaltenVorDerGrenzeTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py)
sagt aber nicht mehr, was sie tut:
`westlichDavorAufDerLinieVon(stelle, linie, radien, abstand)`.
1. `linie` ist eine *Stelle*, von der nur `y` zählt; eine Linie ist sie nicht.
2. `abstand` ist nicht mehr der *Abstand* zur *Base* des Overlords, sondern ein Versatz in
   x: Mit dem Versatz in y (20/127″) liegt das Ziel rund 0,506″ vor ihr. Der Name verspricht
   eine Größe, die erst die neue Prüfung sichert.

**Kosten.** Am Bildschirm nichts. Bleibt es, rechnet ein Leser den Test mit dem falschen
*Abstand* nach. Umbau: eine Funktion, ein Aufruf.

**Gegenvorschlag.** Den Versatz nennen, nicht den *Abstand*, und das y als Zahl übergeben,
etwa `westlichVon(stelleDesAnderen, radien + halberZoll, y=davor.y)` mit
`Stelle(x=stelle.x - versatz, y=y)`; oder die Funktion streichen und das Ziel im Test mit
`Stelle(...)` bauen, die Prüfung danach trägt die Bedeutung.

**Stellungnahme.**
