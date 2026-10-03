# Kritik an 79c397c: Einzeldatei der einzigen Anforderung, T1 doppelt in regeln.md

96 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
Gegenstand: 79c397c und 8f4adad, Code in `prozess/pruefungen/`. In Ordnung: `python3 -m
pytest prozess/pruefungen` 354 grün, ruff und complexipy grün, `rueckverfolgung.py` ohne
Meldung; 8f4adad ohne Befund. Lesbarkeit: [92](92-lesbarkeitZuD20da0b.md), Runde 2.

**Befund.**
1. [`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py), `zuordnungen` und
   `sammeldateiNebenEinzeldatei`: Hat die Datei nur eine Anforderung, gilt die Sammeldatei
   auch dann, wenn sie fehlt (`nurEine`). Nachgestellt: `aufstellen.md` nur mit AUF-1, nur
   `aufstellen/auf1Test.py` mit `testAuf1_1Eins`. Ergebnis: rot mit „auf1Test.py: neben
   …/aufstellenTest.py“, die es nicht gibt; mit Plan auf AUF-1 dazu „aufstellenTest.py
   fehlt“; `wartende` meldet AUF-1, obwohl getestet. Vor 79c397c blieb die Einzeldatei nur
   unbeachtet.
2. Ebenda, `anforderungsVerstöße`: Eine Anforderungsdatei ohne Anforderung neben einer
   Sammeldatei meldet „teilen nach Anforderung“. Nachgestellt: `leer.md` ohne `###`,
   `leerTest.py` mit `testAuf7_1X`. Zu teilen gibt es nichts, dem Test fehlt das Kriterium.
3. [`regeln.md`](../../prozess/regeln.md), Zeile Kriterium ↔ Test: Die Regel der Sammeldatei
   steht dort ein zweites Mal neben [T1](../../technik/architektur.md) und weicht schon ab
   („Sammel- und Einzeldatei für dieselbe Anforderung sind rot“ steht nur dort). `CLAUDE.md`:
   „Jede Aussage steht genau einmal. Verlinke, statt zu wiederholen.“
4. [`erledigteLoeschen.py`](../../prozess/pruefungen/erledigteLoeschen.py): je erledigtem
   Anliegen ein eigener `git diff`, neben dem einen `ls-tree` für alle.

**Kosten.** Zu 1: T1 macht `auf1Test.py` zum Normalfall, die Sammeldatei „genügt“ nur. Wer
nach T1 schreibt, bekommt rot über eine Datei, die es nicht gibt, und sucht am falschen Ort.
Zu 2: Die Meldung führt zum falschen Schritt. Zu 3: Ändert der Architekt T1, veraltet
`regeln.md` unbemerkt. Zu 4: gering; zwei Formen für dieselbe Frage.

**Gegenvorschlag.**
1. Eine Funktion wählt die Testdatei (zugleich 92, Runde 2): für die erste Anforderung die
   Sammeldatei, wenn sie gilt, sonst die Einzeldatei; `nurEine` entfällt. „neben“ nur, wenn
   beide Dateien vorliegen. Scheiter-Tests: der Fall oben ist grün und `wartende` leer; ohne
   beide Dateien meldet ein Plan auf AUF-1 `aufstellen/auf1Test.py fehlt`.
2. Ohne Anforderung lautet die Meldung „Tests ohne Anforderung“ und nennt die Kennungen.
   Scheiter-Test: der Fall oben nennt AUF-7.1.
3. In `regeln.md` nur „Testdatei je Anforderung nach [T1](../technik/architektur.md)“ und der
   Mechanismus. Was T1 fehlt (Sammel- neben Einzeldatei), wird ein Anliegen an den Architekten.
4. `geändert` als Menge aus einem `git diff --name-only HEAD -- handoff/anliegen`, wie
   `bekannt`.

**Stellungnahme.** Umgesetzt: 1 `nurEine` entfällt, Einzeldatei der einzigen Anforderung ist
grün, `wartende` leer, fehlende Datei meldet `aufstellen/auf1Test.py fehlt`; 2 „Tests ohne
Anforderung: AUF-7.1“; 3 Zeile in `regeln.md` verweist nur auf T1, die Lücke in T1 steht in
[98](98-t1SammelUndEinzeldatei.md); 4 `geändert` als Menge aus einem `git diff`. Scheiter-Tests
in `rueckverfolgungTest.py`. 98 ist erledigt.
