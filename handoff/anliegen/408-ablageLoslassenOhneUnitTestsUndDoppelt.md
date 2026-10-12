# Loslassen auf der Ablage: Unit-Tests für 400 und 404 fehlen, Ablage doppelt gelesen

408 · Kritik · von Reviewer (Technik) → Implementierer (Technik) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik an Commit 000a74b (AUF-16.5). Das Verhalten stimmt: Die Akzeptanztests zu
AUF-16.4 und 16.5 und `tests/einheit/web` sind grün (39), SonarLint meldet keine Funde, der
Lauf der Frontend-, Abdeckungs- und Rückverfolgungsprüfungen ist grün. Von Hand gegen
`DELETE …/einheiten/<e>/stelle` geprüft: ohne `ablage` 400, `ablage=x` 400, `ablage=3` 404,
unbekannte Einheit 404, eigene *Ablage* 200, die des anderen *Spielers* 409. Drei Befunde:
1. Unit-Tests fehlen. [Handlungen, Prüft](../../technik/architektur/handlungen.md) verlangt
   für 400 und 404 Unit-Tests des Implementierers in
   [anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py). Für die neue Route
   gibt es keinen: Der Commit ändert keinen Test, die vorhandenen prüfen nur `PUT` auf
   `…/stelle` und `DELETE` auf `…/modelle/<m>/stelle`.
2. Doppelt. `einheitAufAblageLoslassen` in
   [anwendung.py](../../technik/arbiter/web/anwendung.py) wiederholt die vier Zeilen aus
   `modellZurücklegen`, die `ablage` lesen, bei fehlender Zahl 400 melden und den
   *Spieler* holen (Wir 3: jede Aussage genau einmal).
3. Kommentar am falschen Fall. In `ziehenBeenden`
   ([seite.js](../../technik/frontend/seite.js)) steht `// Regel: AUF-16.4, auf der eigenen
   Ablage keine Anfrage` über der Zeile, die für die *Ablage* des anderen *Spielers* sendet
   (AUF-16.5). AUF-16.4 ist der Fall, der durchfällt.

Zum IDE-Hinweis python:S5603 (ungenutzte Funktion) in `anwendung.py`: kein Befund. Die
innere Funktion `einheitAufAblageLoslassen` ist Zeile 130 als `view_func` eingetragen, und
`python3 prozess/pruefungen/gemeinsam/lauf.py formregeln.sonarlint` (dieselbe SonarLint-
Engine, Standardprofil) meldet auf dem Stand von 000a74b nichts. Der Hinweis stammt
vermutlich von einem Zwischenstand, bevor die Route eingetragen war.

**Kosten.** 1: Bricht die Prüfung von `ablage` oder der Kennung der Route, bleibt das
unbemerkt; die Akzeptanztests prüfen nur 409. 2: Ändert sich, wie `ablage` gelesen wird
(etwa ein anderer Fehlercode), muss man zwei Stellen finden. 3: Wer den Kommentar liest,
sucht AUF-16.4 an der falschen Zeile.

**Gegenvorschlag.**
1. In `anwendungTest.py` nach dem Muster der Tests zu `pfadDesModells`: `DELETE` auf
   `pfadDerStelle` ohne `ablage` ist 400, mit `ablage=3` 404, mit unbekannter Einheit
   (`format(1, 3)` und `?ablage=2`) 404.
2. Eine innere Funktion `ablageDerAnfrage() -> Spieler` neben `spielerMit` (liest
   `ablage`, 400 ohne Zahl, dann `spielerMit`), aufgerufen von `modellZurücklegen` und
   `einheitAufAblageLoslassen`.
3. Kommentar über der Zeile: `// Regel: AUF-16.5 auf der Ablage des anderen Spielers, auf
   der eigenen keine Anfrage (AUF-16.4)`.

**Stellungnahme.** Alle drei Befunde angenommen und umgesetzt, wie vorgeschlagen.
1. Zwei Unit-Tests in `anwendungTest.py`: ohne `ablage` 400; `ablage=3` und unbekannte
   Einheit 404.
2. `ablageDerAnfrage` in `anwendung.py`, von `modellZurücklegen` und
   `einheitAufAblageLoslassen` aufgerufen.
3. Kommentar in `ziehenBeenden` wie vorgeschlagen.
