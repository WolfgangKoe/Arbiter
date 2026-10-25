# Die Architektur hat einen eigenen Reiter und öffnet sich bis zu den Dateien

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Feedback des Stakeholders zur Karte aus Anliegen 3120, im Wortlaut aus
Anliegen 2740:
> Mir gefällt nicht, dass die Architektur-Abbildung im Token-Bericht ist. Das sollte einen eigenen Reiter bekommen. Auf der ganzen Seite wäre dann auch Platz für mehr Details. Ich möchte daraus gerne nachvollziehen können, welche konkreten Dateien ausgeführt werden und diese auch im Repo finden. Sind das da immer die "init"-Dateien? Lege die Abbildung so an, dass sie interaktiv erweitert werden kann. So ähnlich wie in mammutmap. Ich will natürlich nicht alle Dateien in der Darstellung sehen, aber ich will bis auf die Dateien des Produktivcodes sehen können und welche Datei welche andere Datei aufruft. Kommen mit der Zeit Dateien hinzu, muss das Bild automatisch aktualisiert werden. Am besten wäre daher ein Skript, dass regelmäßig (z.B. nach Abschluss der Technikphase), dieses Bild aktualisiert.

Seine Frage: Nein, nicht immer die init-Dateien. `arbiter` startet `technik/arbiter/__main__.py`.
Sie holt, was sie braucht: die Ausgangslage aus dem Katalog, die Aufstellung aus der Domäne,
den Server aus Web; jede dieser Dateien holt wieder ihre. Eine `__init__.py` gehört zu einem
Ordner; Python führt sie aus, sobald der Ordner zum ersten Mal gebraucht wird. Sechs der acht
sind leer und tun nichts. Code tragen zwei: `domaene/phasen/aufstellen/__init__.py` (die Phase
Aufstellen) und `domaene/querschnitt/__init__.py` (Überdeckung der Bases).

Anliegen 4100 geht hierin auf: Seine Punkte 1 und 2 richten
die feste Lage der heutigen Kästen, die dieses Bild ersetzt; 3 und 4 stehen unten als 5 und 6.
Beide warten auf dieselbe Prozessphase, erst richten und dann ersetzen wäre doppelte Arbeit.

**Kosten.** Ohne Dateien findet der Stakeholder nicht, wo ein Pfeil beginnt und endet.
Mehr Prüfcode als heute (265 Zeilen) zählt gegen die
[Kennzahl](../../prozess/kennzahlen.md#kennzahlen).

**Gegenvorschlag.** Ein dritter Reiter „Architektur“ neben Anliegen und Tokenbericht; der
Tokenbericht verliert die Karte.
1. Beim Öffnen: die Schichten wie heute, mit Zeichen, Pfeilen, rot und gestrichelt.
2. Ein Klick öffnet einen Kasten wie in Mammutmap: Darin stehen seine Ordner und Dateien als
   Kästen, ein Ordner öffnet sich wieder, ein zweiter Klick schließt. Unterste Ebene: jede
   Datei unter `technik/arbiter/` (`.py`, ohne leere `__init__.py`) und `technik/frontend/`.
3. Ein Pfeil von A nach B: Eine Datei in A holt etwas aus einer Datei in B (Python und
   JavaScript `import`, HTML `<script src>` und `<link href>`); die Zahl zählt Importzeilen.
   Ist ein Kasten zu, endet der Pfeil an ihm. Seite → Web bleibt „HTTP“. Wann welche Funktion
   läuft, zeigt erst ein Lauf.
4. Jede Datei nennt ihren Pfad ab dem Repo (`technik/arbiter/web/server.py`) und ihre Zeichen.
5. Die Kästen folgen den Ordnern, nicht einer Tabelle: Ein Ordner, den die Architektur nicht
   kennt, bekommt einen Kasten „nicht in der Architektur“, seine Pfeile sind rot, die Seite
   bricht nicht ab.
6. `from arbiter import web` und relative Importe bis `arbiter` zählen wie `from arbiter.web
   import …`.
7. Kein eigenes Skript: Der Server misst die Karte bei jedem Öffnen des Reiters, wie heute den
   Tokenbericht. Eine neue Datei erscheint beim nächsten Laden, nicht erst nach der Technikphase.

Aufklappen und Pfeile zwischen verschachtelten Kästen sind Neuland: erst ein Wegwerf-Versuch
unter `/tmp`. Bestehende Regel: [Regeln](../../prozess/regeln/rollenregeln.md), Zeile
„Architektur“ (P7), angepasst. Erledigt, wenn Tests zu 2 bis 7 an einem Baum unter `tmp_path`
grün sind und Screenshots unter `/tmp` die Startansicht und die ganz geöffnete Domäne mit
allen Namen, Pfaden und Zahlen lesbar zeigen.

**Stellungnahme.**
