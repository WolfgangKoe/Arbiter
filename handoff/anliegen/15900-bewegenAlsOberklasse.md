# Warum Fliegen eine Klasse ist und Bewegen nicht

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 2/3
Status: angenommen

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

Noch eine Ergänzung:
Vielleicht machen wir es so wie im Kommentar etwas angedeutet beschrieben:
1. Wir nehmen das aktuelle "Gleiten" als eine grundlegende Art des Ziehens von Spielobjekten. Darum benennen wir es beispielsweise auch zu "ziehenVonSpielobjekt" um.
2. Jegliche Form von Ziehen im Sinne einer Bewegung verwendet dann diese Klasse. 
    a. Fliegen verhält sich nun jetzt schon so wie es soll.
    b. Spielobjekte, die nicht fliegen, müssen sich anders verhalten. Stoßen sie gegen ein Hindernis (was in unserer App nur andere Modelle sein können ggf. mit Nahkampfreichweite), so müssen die Spielobjekte regeltechnisch um diese herumgeführt werden. Das zählt gegen die Bewegungsreichweite. 
    c. Vorrücken ist wie normales Bewegung mit erhöhter Bewegungsreichweite und anderem Endzustand.
    d. Usw. 
Was hältst du hiervon. 
Stellungnahme: siehe Runde 2.

## Runde 2
**Befund.** Deinen Punkten 1, 2, 2a und 2c stimme ich zu; 2b ist teils neu.
- Regeltext: Jedes *Modell* zieht „along any path, but no part of the model's base can be moved across the bases of other models“ (`core_rules.txt:729`), *Fliegen* hebt das auf (`:884`). Oberbegriff ist also *Ziehen*, wie in den Anforderungen („beim Ziehen“). `Gleiten` stammt aus ArbiterMap (`glide`); die Art ohne *Fliegen* hieße nach deinem 2b `Herumführen`. „Spielobjekt“ ließe ich weg: Gezogen werden nur *Modelle*.
- Messen ist es nicht: `messen.py` sagt ohne Regel, ob sich *Bases* *überdecken*; ob Arbiter dann anhält oder herumführt, ist Regel. Umgekehrt baut `fliegen.py` Kreise aus Radien der *Bases* (etwa 60 Zeilen), das gehört nach [M1](../../technik/architektur/domaene.md) in `messen.py`.
- Datei und Klasse heißen verschieden, weil ein Modul den Namen seiner Anforderung trägt (BEW-17). Herumführen gilt schon beim Aufstellen (AUF-29); die Bewegung holt seinen Kern aus `phasen/aufstellen/anhaltenAufDemWeg.py`.
- Gemeinsames beider Arten steht verstreut (`Gezogen`, `Umgebung` in `normaleBewegung.py`, `Anteile` in `uebergehenBeimZiehen.py`); `Gezogen.fliegen` ist ein Schalter statt der Art.
- 2b ändert Kriterien: Als *Distanz* zählt heute die gerade Strecke (Glossar, Anliegen 5180, 5400), vor *Nahkampfreichweite* hält Arbiter an (BEW-6.2).

Wörter, Ort von AUF-29 und 2b klärt der Anforderungsautor in [16080](16080-ziehenUndHerumfuehren.md): Ein Begriff steht erst in Anforderung und Glossar, dann im Code ([Wir 2](../../prozess/praemissen/wir.md)).

**Kosten.** Am Bildschirm nichts; 2b erst nach 16080.
A: Anforderungsautor in Domänenphase 11, Testautor benennt Tests um, Implementierer verschiebt etwa 400 Zeilen in Technikphase 11, samt 13761, 14240, 14261.
B: etwa 150 Zeilen; Schuld: Der Kern bleibt im Aufstellen.
C: wie A, aber `Fliegen` schaltet ab, was die Oberklasse zusagt ([Es L](../../prozess/praemissen/es.md)).

**Gegenvorschlag.** Der Ordner nach A; die Schnittstelle legt nur fest, was jede Art beantwortet (wo gezeigt, wo *gesetzt*, was sperrt):
```
querschnitt/ziehen.py        Ziehen (Schnittstelle), Gezogen, Umgebung, Anteile
querschnitt/herumfuehren.py  Herumführen (heute Gleiten und AUF-29)
phasen/bewegung/fliegen.py   Fliegen, nur Regeln
messen.py                    Weg in die freie Fläche zwischen Bases
phasen/bewegung/__init__.py  wählt die Art; Normale Bewegung, Vorrücken als Daten (2c)
```
Charge und Fall Back (Etappe 3) erhalten eine Art von Ziehen, statt eine zu sein.

**F1 · Wie schneiden wir Ziehen?** (ersetzt F1 aus Runde 1)
Annahme: A; das Item für Technikphase 11 schreibe ich nach 16080.
A: Schnittstelle `Ziehen` mit den Arten `Herumführen` und `Fliegen`, Herumführen in `querschnitt/`, Messen nach `messen.py` (Anliegen 15900, Regeltext, M1)
B: Nur `Gleiten` in `Herumführen` umbenennen, eigene Datei in `bewegung/` (Anliegen 15900)
C: Oberklasse `Ziehen` mit Herumführen als Normalfall, `Fliegen` als Unterklasse (Anliegen 15900)
Empfehlung: A, denn so steht jede Regel einmal an ihrem Ort.
Antwort: A

**Stellungnahme.**
Kommentar: Ziehe für die Domänenphase in Erwägung, den Ordner "Querschnitt" umzubenennen. Ich meine zu verstehen, weshalb er so benannt ist. Fachlich ist es aber schwer lesbar. Mir ist bewusst, dass eine Umbenennung dazu führen mag, genau diesen Pfad an vielen Stellen zu ändern. Aber der Code muss lesbar sein!
