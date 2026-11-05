# Fliegen: Baseform außerhalb von messen.py, messen.py am Höchstmaß

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Kritik am Code zu Item fliegen, Abschnitt 1 (vorgemerkter Stand). Nichts hält
auf: A1 und der Spiegel sind grün, die 44 Einheitstests zu `messen.py` und `fliegen.py`
grün; Rücken einer Spinne mitten in 36 Boyz 13 ms, drei Flieger 73 ms. Es wartet:
1. M1 sagt: Die Baseform kennt nur `messen.py`. `fliegen.py` baut aus `radiusInZoll`
   die gemiedenen Kreise (`_gemiedenerRadius`: Summe der Radien) und die Ränder des
   Spielfelds (`_randDesSpielfelds`: Kante minus Radius). Beides setzt runde *Bases*
   voraus. Bei ovalen *Bases* (Etappe 6) wären sie falsch, ohne dass ein Test im Modul
   der Messung rot wird. `grenzkreise.py` macht es heute schon genauso. Darum wartet es
   bis zum Auslöser von M1.
2. `messen.py` hat 11.808 von 12.000 Zeichen ([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße))
   und zwei Aufgaben. Die eine misst exakt (S2). Die andere sucht mit `float` und Toleranz
   in die freie Fläche (`Rand`, `wegInDieFreieFläche`, sieben Hilfsfunktionen). Holt man
   Punkt 1 dorthin, ist das Höchstmaß überschritten.
3. Schalter statt Begriff: `Geradenrand(inX, aufwärts)` und `Kreisrand(darin)`. Wer liest
   `Kreisrand(..., darin=True)`, sieht nicht, dass das der Kreis der *Bewegungsweite* ist
   und dass `darin=False` „meiden“ heißt.

**Kosten.** Etwa 120 Zeilen verschieben, keine neue Logik. Aufrufer sind nur `fliegen.py`
und `messenTest.py`. Das Entscheiden über den Schnitt in M1 kostet mich einen Lauf.

**Gegenvorschlag.** In Technikphase 11, bevor `messen.py` wieder wächst:
1. Ich lege in M1 ein drittes Werkzeug ohne Anforderung fest:
   `domaene/freieFlaeche.py`. Darin stehen `Rand` und `wegInDieFreieFläche` und die Ränder
   aus *Bases*: `gemiedenerKreis(bewegt, hindernis, abstand)` und
   `ränderDerFläche(bewegt, grenzenInX, grenzenInY)`. Die Baseform liest es nur über
   `messen.py`.
2. Danach verschiebst du das und ziehst `messenTest.py` nach, mit
   `freieFlaecheTest.py`. `fliegen.py` und `grenzkreise.py` rufen dann nur noch diese
   Funktionen auf.
3. Statt der Schalter benennst du die Begriffe als Typen: `GemiedenerKreis` und
   `KreisDerWeite`, `Geradenrand` mit `achse` und `freieSeite`. Die genauen Namen
   prüft der Reviewer.

**Stellungnahme.**
