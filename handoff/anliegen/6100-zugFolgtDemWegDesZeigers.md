# Ein gezogenes Modell folgt dem Weg des Zeigers (AUF-8.7) schon mit der Normalen Bewegung

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Bisher legt Arbiter ein gezogenes *Modell* genau unter den Zeiger. Der Browser
rechnet den Zeiger auf etwa ein Zehnmillionstel Zoll ungenau in Zoll um. Arbiter rechnet
exakt ([S2](../../technik/architektur/domaene.md)). Zieht man einen Boy an einem anderen
entlang, an dessen *Base* er anliegt, rückt er so um diesen Bruchteil auf die andere *Base*.
Dann sperrt Arbiter mit ‚über eine Base‘ (BEW-2.5), obwohl man gerade gezogen hat. Daran
scheitern Tests der Normalen Bewegung. Der Implementierer hat es in
[bedienung.js](../../technik/frontend/bedienung.js) behoben, im Code `stelleDesZugs`.
Die neue *Stelle* ist die vorige *Stelle* plus der Weg, den der Zeiger seit dem Greifen
zurückgelegt hat. Ein Zug genau nach rechts lässt die Höhe also exakt gleich. Das ist
[AUF-8.7](../../domaene/anforderungen/phasen/aufstellen/ziehen.md) aus deinem Anliegen 1610.
AUF-8.7 gehört aber nicht zum Item normalMove, und es gibt noch keinen Test dafür.
Außerdem gleicht `web/` jede gesendete Zahl auf den nächsten Bruch mit Nenner bis
1.000.000 ab, höchstens ein halbes Millionstel Zoll. So kommt eine *Stelle*, die die Seite
aus dem Spielstand übernimmt, exakt zurück. Ich habe es an einer Kopie in `/tmp` geprüft:
Ohne den Abgleich scheitern zwei Tests zu BEW-1.7 und BEW-2.6. Den
[Vertrag](../../technik/architektur/vertrag/querschnitt.md) (V5, V8, V10) habe ich
nachgezogen.

**Kosten.** Mit A schreibt der Testautor einen Test, Code kommt nicht dazu. Er arbeitet
ohnehin an `ziehenTest.py` (Anliegen 6060). Bis der Test grün ist, bleibt meine Kritik am
Code offen (Anliegen 6101).

**Gegenvorschlag.** Siehe F1.

**F1 · Kommt AUF-8.7 mit dem Item normalMove?**
A: Ja (Anliegen 1610). Am Bildschirm: Greifst du ein *Modell* am Rand, springt es nicht mehr
mit der Mitte unter den Zeiger, in *Aufstellung* und *Bewegungsphase*. Der Testautor prüft
das, bevor das Item abgenommen wird.
B: Nein, stattdessen eine Toleranz in `streckeÜberdeckt` (neu). Dagegen spricht: Sie bricht
S2 (exakt, ohne Toleranz). Endet ein Zug genau an einer *Base*, sperrt QUE-1 aus demselben
Grund. Die Toleranz müsste also auch in `überdecken` und änderte das Aufstellen. Außerdem
verdeckte sie echte Überdeckungen in ihrer Größe. Das wäre technische Schuld.
Empfehlung: A. Die Bedienung, die du in Anliegen 1610 verlangt hast, behebt die Ursache.
Gemessen wird weiter exakt.
Annahme: Wir arbeiten mit A weiter. Das Item behält `stelleDesZugs`, der Testautor schreibt
den Test zu AUF-8.7 (Anliegen 6101).
Antwort: A

Was bleibt: Ziehst du von Hand, weicht deine Hand um Pixel ab. Ein Boy, der an einem
fremden anliegt und leicht auf ihn zu gezogen wird, ist nach BEW-2.5 weiter gesperrt. So
verlangt es die Regel. Ob anliegende *Bases* aneinander entlanggleiten dürfen, ist eine
Frage für eine spätere Domänenphase.

**Stellungnahme.**
