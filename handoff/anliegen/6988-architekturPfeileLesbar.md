# Die Pfeile der Architektur laufen nicht über Kästen und Schrift

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 2/3
Status: angenommen

## Runde 1
**Befund.** Nachprüfung von Anliegen 4140 an den
Screenshots des Regelumsetzers (`/tmp/arch/start.png`, `/tmp/arch/offen.png`): Die Punkte 1 bis 7
sind umgesetzt, die 22 Tests grün, 4140 ist erledigt. Offen bleibt die Lesbarkeit aus seinem
Erledigt-Kriterium:
1. Startansicht: Der Pfeil Start → Domäne läuft mitten durch Anwendung, die 2 steht auf dessen
   oberem Rand. Man liest einen Pfeil Start → Anwendung. Das ist Punkt 2 aus 4100, der in 4140
   aufging.
2. Ganz geöffnet: Rund 80 Pfeile laufen quer über die Kästen. Linien und Zahlen liegen auf
   Namen und Pfaden (`darstellung.py`, `kennungen.py`, `einheitInAufstellung.py`), und welche
   „1“ zu welchem Pfeil gehört, ist nicht zu sehen. Welche Datei welche andere aufruft, kann der
   Stakeholder so nicht verfolgen; das war der Kern seines Wunsches aus 2740.
3. Den Klick (Punkt 2 aus 4140) und „Ist ein Kasten zu, endet der Pfeil an ihm“ (Punkt 3) prüft
   kein Test: `testEinOrdnerÖffnetSichBisZurDateiUndLeereInitDateienFehlen` sucht nur den Text
   `classList.toggle("offen")` in der Seite. Das Verhalten belegen allein die Screenshots.

**Kosten.** Ohne 1 liest er die Startansicht falsch, ohne 2 zeigt der Reiter die Dateien, aber
nicht ihre Beziehungen. Hält nicht auf: Das Produkt ist nicht betroffen, keine Prüfung ist rot;
darum wartet es auf die Prozessphase. Jede Lösung zu 2 vergrößert das Skript (heute 123 Zeilen)
und zählt gegen die [Kennzahl](../../prozess/kennzahlen.md#kennzahlen).

**Gegenvorschlag.**
1. Startansicht: Kein Pfeil schneidet einen Kasten, der nicht sein Anfang oder Ende ist, und
   keine Zahl steht auf einem Kasten, etwa durch eine andere Ordnung in `zeilen`.
2. Geöffnet: Die Pfeile laufen hinter den Kästen, die Kästen decken sie; die Zahl steht dort, wo
   der Pfeil frei liegt.
3. Ein Klick auf eine Datei hebt ihre Pfeile hervor, hinein und hinaus, die übrigen werden blass;
   ein zweiter Klick hebt das auf. Ein Klick auf einen Ordner öffnet und schließt wie bisher.
   Neuland: erst ein Wegwerf-Versuch unter `/tmp`.
4. Den Test auf `classList.toggle` ersetzen oder streichen: Er prüft Text, nicht Verhalten
   ([Absicht 1](../../prozess/praemissen/absicht.md)). Was das Skript zeichnet, belegen
   Screenshots.

Bestehende Regel: [Regeln](../../prozess/regeln/rollenregeln.md), Zeile „Architektur“ (P7).
Erledigt, wenn Screenshots unter `/tmp` die Startansicht ohne geschnittenen Kasten, die ganz
geöffnete Domäne mit allen Namen, Pfaden und Zahlen frei von Linien und eine hervorgehobene
Datei zeigen, deren Pfeile man bis zu ihren Zielen verfolgen kann.

**Stellungnahme.** Umgesetzt mit Retro 9, P6 (Anliegen 8860, F2 mit Stakeholder-Kommentar):
1 und 2 gelöst durch weniger Pfeile: Sie erscheinen nur beim Überfahren oder Antippen eines
Kastens, Verbotene und Zyklen immer. Pfeile hinter den Kästen: nein, ein offener Ordner
deckte die Pfeile seiner Kinder. 3: statt Klick auf die Datei das Überfahren. 4: der
Textsuch-Test ist gestrichen; neu getestet ist die Zyklus-Markierung
(`testEinZyklusZwischenKästenIstAnDenKantenMarkiert`). Das Skript im Browser prüft kein Test;
Startansicht an `/tmp/arch6/start.png` ohne Pfeile gesehen, Überfahren nicht gesehen.

## Runde 2
**Befund.** Nachprüfung im Browser mit einem Wegwerf-Versuch (`/tmp/arch7/probe.py`, Chromium
über Playwright, 1400 Pixel breit; er misst, welche Linie welchen Kasten und welchen Text
schneidet). Umgesetzt: Ohne Überfahren steht kein Pfeil, auch die ganz geöffnete Domäne ist
frei von Linien (`start.png`, `offen.png`); der Textsuch-Test ist gestrichen. Die Ablehnung
„Pfeile hinter den Kästen“ ist begründet. Offen:
1. Fährt die Maus über Start oder Domäne, läuft Start → Domäne wie vorher mitten durch
   Anwendung, die 2 steht auf „Anwendung“ (`start-ueber-domaene.png`). „Kästen nach Schicht“
   hat daran nichts geändert: Die mittlere Zeile hat fünf Kästen, der mittlere liegt immer auf
   der Achse Start–Domäne. Das ist Punkt 1 aus Runde 1 und der Wunsch des Stakeholders in
   8860, F2 („so anordnen, dass die Pfeile dies nicht überkreuzen“); einen Zyklus gibt es hier nicht.
2. Fährt die Maus über eine Datei, laufen ihre Pfeile weiter über fremde Dateien, Pfade und
   Zahlen. `setzenPerKlick.py` (4 Pfeile, `ueber-setzenPerKlick.png`): Der Pfeil nach
   `spielobjekte.py` quert `grenzkreise.py` und `schlachtrunden.py`, man liest ihn als Pfeil
   nach `schlachtrunden.py`; eine 1 steht auf „anhaltenAnEinerBase.py“. `spielobjekte.py`
   (24 Pfeile, `ueber-spielobjekte.png`): Jede Linie quert bis zu elf Kästen; ob eine Linie an
   `ausgangslage.py` beginnt oder nur hindurchläuft, ist nicht zu sehen.

**Kosten.** Ohne 1 liest der Stakeholder beim Überfahren weiter Start → Anwendung; ohne 2
verfolgt er die Pfeile einer Datei nur, solange sie wenige hat und nichts dazwischen liegt.
Hält nicht auf: Das Produkt ist nicht betroffen. Das Skript hat 149 Zeilen; jede Lösung
zählt gegen die [Kennzahl](../../prozess/kennzahlen.md#kennzahlen).

**Gegenvorschlag.**
1. Ein Pfeil, der eine Zeile überspringt, knickt durch die nächste Lücke dieser Zeile
   (`polyline` statt `line`). Gilt für jede Anordnung, auch wenn ein Kasten dazukommt.
2. Eine Linie läuft hinter den Dateikästen und geschlossenen Ordnern: Ein offener Ordner
   bekommt keinen Hintergrund (wie `.ak.leer`), dann deckt er die Pfeile seiner Kinder nicht,
   die Kästen der Dateien decken die Linie; die Zahl steht neben der Spitze am Ziel, nicht
   bei 40 % der Strecke. Das löst auch 1, wenn die Linie hinter Anwendung läuft und dort
   nicht endet; dann entfällt der Knick aus 1.
3. Den Wegwerf-Versuch weiterverwenden, um die Screenshots zu erzeugen; ob daraus ein Test
   wird, entscheidet der Regelumsetzer: Er braucht Chromium und kostet einige Sekunden.

Bestehende Regel: [Regeln](../../prozess/regeln/rollenregeln.md), Zeile „Architektur“ (P6, P7).
Erledigt, wenn `/tmp/arch7/probe.py` (oder sein Nachfolger) nach dem Überfahren von Domäne
und von `setzenPerKlick.py` keine sichtbare Linie über einem fremden Kasten und keine Zahl
auf einem Namen oder Pfad meldet (läuft eine Linie hinter einem Kasten, zählt er die Stelle
nicht), und an `spielobjekte.py` jede Linie sichtbar an ihrem Kasten beginnt.

**Stellungnahme.** Gegenvorschlag 2 umgesetzt in
`prozess/pruefungen/rollenregeln/dashboardArchitekturSkript.py`: Die Pfeile liegen hinter den
Kästen (Dateien und geschlossene Ordner decken sie), ein offener Ordner hat keinen Hintergrund,
nur seine Kopfzeile deckt; die Zahl steht 16 Pixel vor der Spitze am Ziel. Damit läuft
Start → Domäne hinter Anwendung und endet dort nicht; der Knick aus 1 entfällt. 3: Ich habe
den Versuch als `/tmp/arch8/probe.py` weitergeführt (zählt Stellen hinter deckenden Kästen und
Zahlen unter ihnen nicht); Screenshots in `/tmp/arch8/` (`start-ueber-domaene.png`,
`ueber-spielobjekte.png`, `offen.png`). Ergebnis: Start, Überfahren von Start, Domäne,
Anwendung und Web, ganz geöffnet: keine Meldung. `setzenPerKlick.py` (Pfad
`domaene/phasen/aufstellen/setzenPerKlick.py`, `ueber-setzenPerKlick.png`): Im Bild laufen die
4 Linien in den Lücken offener Ordner und hinter den Kästen; der Versuch meldet 2 Linien wegen
des Endpunkts, den er 2 Pixel hinter der Spitze in einer Lücke sucht. `spielobjekte.py`: Dort meldet der Versuch nur noch Linien in den Lücken offener Ordner
(`bewegung`, `querschnitt`, `aufstellen`), die ohne Hintergrund bleiben müssen, und
Anfangspunkte, die er in der Lücke des Ordners statt an der Datei findet; im Bild beginnt
jede Linie an ihrer Datei. Die Zahlen von 24 Pfeilen liegen am Ziel übereinander. Kein Test:
Er bräuchte Chromium; 286 Tests in `rollenregeln` grün.
