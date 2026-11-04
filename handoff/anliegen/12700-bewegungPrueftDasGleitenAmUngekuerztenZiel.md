# Bewegung prüft das Gleiten am ungekürzten Ziel

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Zwei Fehler in `phasen/bewegung/__init__.py`, beide nachgestellt in
`/tmp/reviewAnhalten/probe.py` (Base 254 mm, *Bewegungsweite* 5″, Start (10, 20)):
1. `stellenMitGründenNachDemZiehen` entscheidet über das Gleiten am ungekürzten Ziel, BEW-17.1
   verlangt die *Stelle*, „wo BEW-1.7 und 6.4 sie zeigen würden“. Fremdes *Modell* bei
   (23, 20), Zeiger springt nach (35, 20): Das Ziel ist frei, also gilt V16 ab dem Beginn,
   (15, 20) *überdeckt* das fremde, Ergebnis Sperre ‚Base überdeckt‘. Die lässt sich nach
   [Ziel](../../domaene/ziel.md) nicht übergehen; der Spieler steckt fest, statt dass Arbiter
   vor der *Base* anhält. Bei schnellem Ziehen kommt das vor: Die Seite fragt erst nach der
   laufenden Antwort wieder (`abfrageLäuft`). Mit `angehaltenAufDemWeg` und freiem Ziel
   passiert dasselbe mit dem Halt nach 17.4, der auch nicht gegen *Bases* geprüft wird.
   Umgekehrt (fremdes bei (30, 20), Zeiger auf (32, 20)): Der Halt (15, 20) ist frei, die
   Antwort meldet trotzdem `angehaltenAufDemWeg`, danach gilt 17.4 ohne Grund.
2. `Schlacht.modellLoslassen` → `angebotNachDemZiehen` rechnet die Anteile auf der geraden
   Strecke von der *Stelle* vor dem Ziehen zum Punkt, nicht auf dem Weg des Gleitens.
   Fremdes bei (22, 20), Zeiger auf (25, 20): Das *Modell* hält bei (12, 20) vor der *Base*,
   also vor der *Bewegungsweite*; trotzdem bietet Arbiter *gemeinsam übergehen* an (BEW-8.3
   verlangt das nur nach 3.1 oder 6.2). Wählen die *Spieler* es, bleibt das *Modell* stehen
   und das *Protokoll* bekommt einen *Eintrag* ohne *Grund* (BEW-8.5).

Kein Akzeptanztest deckt die Fälle: Die Tests zu BEW-17 lassen das Ziel nicht frei, wenn V16
kürzt. Der Code kürzt in `übergangen` richtig zuerst und gleitet dann; dieser Weg fehlt beim
Ziehen.

**Kosten.** 1: Eine Sperre, die man nicht übergehen kann, greift zu Unrecht (hält auf). 2:
Arbiter bietet einen Knopf an, den kein Kriterium vorsieht, und protokolliert ein leeres
Übergehen.

**Gegenvorschlag.** 1: Ziel des Gleitens ist der Halt nach V16 (erst die drei Anteile, dann
gleiten), wie es [Ziehen](../../technik/architektur/vertrag/bewegung/ziehen.md) vorsieht
und wie `übergangen` es schon macht; den Halt nach 17.4 auch gegen die *Bases* prüfen. Das
trifft Anliegen 12620: Dort bitte nicht den Vertrag an den jetzigen Code anpassen, sondern
Code und Tests an den Vertrag (Architekt und Testautor dort mitnehmen). 2: Das Angebot aus
dem Ergebnis des Ziehens bestimmen: `stellenMitGründenNachDemZiehen` gibt mit, ob 3.1 oder
6.2 der kleinste Anteil war (wie der Vertrag „*Angehalten* … ist es, wenn …“ sagt), und
`angebotNachDemZiehen` nimmt das, statt neu zu rechnen. Je Fall ein Einheitstest mit den
Zahlen oben.

**Stellungnahme.** Beide Punkte angenommen und umgesetzt, nach dem berichtigten
[Ziehen](../../technik/architektur/vertrag/bewegung/ziehen.md) (12620), nicht mit dem Halt
nach V16 als Ziel des Gleitens. `Bewegungsphase._gezeigt` in
`technik/arbiter/domaene/phasen/bewegung/__init__.py`: Gegleitet wird nur, wenn die *Stellen*
nach V16 (bei `angehaltenAufDemWeg` ab zuvor, 17.4) ein fremdes *Modell* *überdecken*; dann
gleitet `gleiten` ab zuvor zum ungekürzten Punkt und prüft dabei den Halt (neuer Parameter
`geprüft`, `überdecktFremde` in `aufstellen/anhaltenAufDemWeg.py`). Hält nichts an der
*Bewegungsweite* oder *Nahkampfreichweite* an (nur die *Spielfeldkante*), gleitet es auch,
wenn der ungekürzte Punkt überdeckt: so verlangen es die Tests zu 17.3 und 17.1 (Kante).
Punkt 2: `angebotNachDemZiehen` nimmt dasselbe Ergebnis (neue Parameter `stellen`, `weiter`)
und bietet *gemeinsam übergehen* nur, wenn die gezeigte *Stelle* die des kleinsten Anteils 3.1
oder 6.2 ist. Einheitstests je Fall in `technik/tests/einheit/domaene/phasen/bewegungTest.py`.
Tests in `technik/tests` und Ruff grün.
