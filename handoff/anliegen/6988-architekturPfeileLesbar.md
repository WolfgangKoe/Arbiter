# Die Pfeile der Architektur laufen nicht über Kästen und Schrift

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Nachprüfung von [4140](4140-architekturAlsReiterBisZuDenDateien.md) an den
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

**Stellungnahme.**
