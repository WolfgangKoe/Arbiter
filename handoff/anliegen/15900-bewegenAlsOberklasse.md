# Warum Fliegen eine Klasse ist und Bewegen nicht

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: rückfrage

## Runde 1
**Befund.** Deine Frage zu `phasen/bewegung/`: Warum ist *Fliegen* eine Klasse, Bewegen nicht?
Wären nicht alle Bewegungsformen Unterklassen von Bewegen?

Heute: Die Klasse für das Ziehen ohne *Fliegen* gibt es, sie heißt `Gleiten` und steht in
[anhaltenVorFremdenBases.py](../../technik/arbiter/domaene/phasen/bewegung/anhaltenVorFremdenBases.py),
weil sie BEW-17 umsetzt (je Anforderung ein Modul, [Domäne](../../technik/architektur/domaene.md)).
`Gleiten` und `Fliegen` beantworten dieselben fünf Fragen der `Bewegungsphase` verschieden: wo
das *Spielfeld* die *Modelle* beim Ziehen zeigt, ob ‚Base überdeckt‘ dabei zählt, wo sie beim
Loslassen und beim Übergehen landen, was beim Übergehen anhält. `_art` in
[\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py) wählt einmal. Eine
gemeinsame Oberklasse gab es (Anliegen 13740); sie entfiel mit 13920, weil kein Fachbegriff sie
nennt. Dass du Bewegen nicht fandest, ist ein Befund an mich: Name und Ort verbergen den
Normalfall.

Warum nicht dein Schnitt: Im Regeltext ist *Fliegen* keine Bewegungsart, sondern eine
Fähigkeit, die in mehreren gilt: *Normale Bewegung*, *Vorrücken*, Fall Back
(`core_rules.txt:871`) und Charge (`:1886`), nicht bei Pile In und Consolidate. Es sind zwei
Achsen:
1. Bewegungsart: wie weit ein *Modell* zieht und wo es enden muss (Normal Move, Advance,
   Fall Back, Charge, Pile In, Consolidate).
2. Art zu ziehen: wie der Weg fremde *Bases* behandelt, `Gleiten` oder `Fliegen`.

Beispiel: In Etappe 3 greift die Spinne an. Als Unterklasse ist sie `Angreifen` oder
`Fliegen`; es bräuchte `FliegendesAngreifen`, `FliegendesZurückfallen`, je
Bewegungsart eine Klasse mehr. Und `Fliegen` schaltete als Unterklasse das Anhalten vor
fremden *Bases* ab, das die Oberklasse zusagt; das bricht [Es L](../../prozess/praemissen/es.md).

Heute gibt es nur *Normale Bewegung* und *Vorrücken*; sie unterscheiden sich im
*Vorrückwurf*, nach Es 9 Daten, keine Typen. ArbiterMap zeigt den Schnitt für später: [movement_kind.py](../../ArbiterMap/backend/app/domain/movement_kind.py) ordnet zehn
Bewegungsarten in einer Tabelle drei Gruppen zu, je nachdem, was den Weg und was nur das Ende
sperrt. Einen eigenen Typ braucht nur eine Art mit eigenem Verhalten, etwa Charge: Sie muss in
*Nahkampfreichweite* ihrer Ziele enden.

Warum bei dir: Du hast gefragt, und B oder C änderten den Bau von Etappe 3.

**Kosten.** Am Bildschirm in keiner Option ein Unterschied.
A: jetzt nichts; die Aufräumarbeiten 13761, 14240, 14261 (etwa 60 Zeilen) laufen wie geplant
in Technikphase 11. Schuld: `Gezogen.fliegen` bleibt ein Schalter, die Wahl hat im Code
keinen Namen.
B: Umbau von etwa 300 Zeilen samt Einheitstests, ein Lauf des Implementierers mit Kritik;
ab Etappe 3 je Bewegungsart mit *Fliegen* eine Klasse mehr.
C: wie B, dazu Typen für Bewegungsarten aus Etappe 3; ihre Schnittstelle wäre geraten
(Absicht 3), Nacharbeit wahrscheinlich.

**Gegenvorschlag.** Siehe Empfehlung.

**F1 · Wie bauen wir Bewegungsarten und Fliegen?**
Annahme: A; in Technikphase 11 schreibe ich die zwei Achsen als Regel in die
[Domäne](../../technik/architektur/domaene.md), der Vertrag zu Etappe 3 legt je Bewegungsart Zeile
oder Typ fest.
A: Zwei Achsen: `Gleiten` und `Fliegen` bleiben die Arten zu ziehen; Bewegungsarten kommen mit Etappe 3 als Tabellenzeile oder, mit eigenem Verhalten, als Typ, der eine Art zu ziehen erhält (Regeltext, Anliegen 13740, 13920, Es 9)
B: Oberklasse `Bewegen`, Unterklassen `Fliegen`, `Angreifen`, `Nachrücken` und so fort (neu)
C: Zwei Achsen wie A, die Bewegungsarten aber jetzt schon als Typen, zuerst *Normale Bewegung* und *Vorrücken* (neu)
Empfehlung: A, denn *Fliegen* gilt im Regeltext quer über mehrere Bewegungsarten, und die beiden von heute unterscheiden sich nur in einer Zahl.
Antwort: .

**Stellungnahme.**
Kommentar: Ich nehme deinen Vorschlag zur Kenntnis, finde diesen so aber noch nicht gut. Wenn ich dich richtig verstanden habe, ist die Grundsätzliche Klasse "Gleiten". Das ist für mich noch kein gutes Wort. Ich würde diese Klasse eher "Ziehen" nennen. Am liebsten sogar "Modellziehen", aber dann ist es vielleiecht nur auf das MOdell eingeschränkt. Du hast recht, dass Fliegen eine Fähigkeit ist. Doch aus fachlicher SIcht ist es am Ende eine Art von Ziehen eines Modells über Gelände oder für uns überhaupt relevant ziehen über Bases und Nahkampfreichweiten ab. Aktuell funktioniert es auch so. Ich bin mir lediglich nicht sicher, ob die Aufteilung der Dateien gut ist, wie sie und einzelne Klassen benannt sind und wie die Dateien benannt sind. Sollten die Klasse "Gleiten" oder "Ziehen" wirklich im Ordner "Bewegen" sein oder ist es nicht vielmehr so etwas wie "messen"? Bitte mache dir hierzu nochmal genau Gedanken und sprich ggf. auch nochmal mit dem Anforderungsautor. Mich stört vermutlich einfach, dass du einmal "Gleiten" genommen hast, dass es als regelwort nicht gibt und als zweites "Fliegen", was ein fachliches Wort ist und dabei sehr prominent beim Spielen. Fliegen taucht als eigene Datei auf, aber "gleiten" oder "Ziehen" nicht. Dabei ist "Zug" ja schon ein Stück weit vergeben, wobei man in einem "Zug" auch Einheiten oder Modell "zieht", selbst wenn sie stationär bleiben bzw. handeln können ohne sich zu bewegen. Also nochmal gut mit dem Anforderungsautor diskutieren, wie ihr das besser hinbekommt und voneinander differenziert. 
