# Akzeptanztests: drei Namen und ein doppelter Wert nach dem Aufräumen der Kommentare

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund (wartet auf die Technikphase).** Mit den Kommentaren nach
[Es 8](../../prozess/praemissen/es.md) ging in Hilfsmodulen und Aufbauten etwas verloren, das
kein Kriterium betrifft:

1. [ziehen.py](../../technik/tests/akzeptanz/ziehen.py), `aufDieAntwortenWarten`: ohne
   Docstring; warum vier ruhige Proben zu 50 ms (erst dann zeigt die *Karte* den Stand zum
   Zeigerpunkt), sagt nur noch die Fehlermeldung halb.
2. [handgriffe.py](../../technik/tests/akzeptanz/handgriffe.py), `schräg = (3/5, 4/5)`: dass
   3-4-5 die Entfernung ohne Wurzel exakt hält (S2), liest man nicht.
3. [einheitVerschiebenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/einheitVerschiebenTest.py),
   `testAuf21_2…`: `versatz` sagt nicht, dass man das gezogene *Modell* so loslässt, dass
   der Block als Ganzes am Ziel ankommt.
4. [kohaerenzTest.py](../../technik/tests/akzeptanz/querschnitt/kohaerenzTest.py) definiert
   `millionstel` ein zweites Mal; `handgriffe.py` hat ihn schon
   ([Wir 3](../../prozess/praemissen/wir.md)).

**Kosten.** Wer den Test ändert, rekonstruiert die Absicht aus der Rechnung; 4 kann
auseinanderlaufen.

**Gegenvorschlag.** 1 ein einzeiliger Docstring; 2 und 3 ein sprechender Name
(`schrägOhneWurzel`, `versatzDesGezogenenImBlock`); 4 aus `handgriffe.py` importieren.

**Stellungnahme.** Angenommen, alle vier umgesetzt.
1. `aufDieAntwortenWarten` hat einen einzeiligen Docstring.
2. `schräg` heißt `schrägOhneWurzel` (`handgriffe.py`, `setzenTest.py`).
3. `versatz` heißt `versatzDesGezogenenImBlock`.
4. `kohaerenzTest.py` importiert `millionstel` aus `handgriffe.py`.
