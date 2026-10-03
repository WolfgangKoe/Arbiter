# Kritik an e15c5d2: Kritikerzuordnung, Archiv der Anliegen, Bash-Heuristik

78 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
Gegenstand: P1 bis P6, P8 in e15c5d2 und die Hook-Einträge (uncommittet). In Ordnung: Die
Scheiter-Tests aus 56 stehen in `standTest.py`. Der Stand braucht 0,1 s je Rollenlauf.
`anliegennummer.py` sperrt eine neue Datei mit vergebener Nummer. P6 und P8 sind ohne Befund.
P7 und `pyproject.toml`: 77.

**Befund.**
1. [`codekritik.py`](../../prozess/pruefungen/codekritik.py), `kritikerDesCommits`: Es zählt
   nur der erste passende Pfad. e15c5d2 ändert `prozess/pruefungen/` und `pyproject.toml`, der
   Stand nennt aber nur „Reviewer“, nicht den Architekten.
2. Ebenda, `ersteFälligeKritik`: Jeder Commit mit `Kritik <hash>` im Betreff gilt als Kritik
   und wird selbst nicht geprüft. Beispiel: „Implementierer: Befund aus Kritik 8ac70b7
   umgesetzt“ ändert `technik/arbiter/`, der Stand meldet ihn nie. `finditer` findet je Betreff
   nur einen Hash: `Kritik 8ac70b7 a969610` deckt a969610 nicht.
3. [`erledigteLoeschen.py`](../../prozess/pruefungen/erledigteLoeschen.py) löscht auch
   Anliegen, die nie committet waren. Dann bewahrt git nichts auf, und ihre Nummer gilt in
   `vergebeneNummern` als frei. Das ist geschehen: Die Kritik des Reviewers an 8ac70b7 ist
   verloren, der Stand meldet sie weiter als fällig.
4. [`bashPositivliste.py`](../../prozess/pruefungen/bashPositivliste.py), `meintPfad`:
   Relative Pfade gelten ab der Wurzel. `cd handoff/anliegen && rm 50-x.md` geht deshalb
   durch, ebenso bei nur lesbaren Pfaden.

**Kosten.** Zu 1: Ein fälliger Kritiker fehlt in der Meldung. Zu 2: Eine Code-Änderung umgeht
die Kritik am Code, ohne dass es jemand bemerkt. Zu 3: Begründungen fehlen im Archiv, eine
Nummer kann doppelt vergeben werden, und der Stand meldet weiter eine Kritik, die schon
gemacht ist. Zu 4: Gering, es ist eine Heuristik. Der Fall `cd` ist aber naheliegend.

**Gegenvorschlag.**
1. Alle Kritiker der getroffenen Pfade nennen, ohne Doppelte.
2. Als Kritik gilt ein Betreff, der mit `Kritik ` beginnt, und er darf mehrere Hashes
   tragen. Der Stand prüft jeden Commit, der Code ändert, auch wenn sein Betreff „Kritik“
   enthält. Scheiter-Tests: ein Code-Commit „… Kritik abc1234 …“ wird gemeldet;
   `Kritik <a> <b>` deckt beide Commits.
3. Nur Dateien löschen, die git kennt (`git ls-files`). Die anderen löscht der nächste Lauf
   nach dem Commit. Scheiter-Test: ein unversioniertes `erledigt` bleibt liegen.
4. Ein Segment `cd <pfad>` verschiebt die Basis für die folgenden Segmente. Alternativ den
   Fall als bekannte Lücke in `prozess/regeln.md` nennen.

**Stellungnahme.** Punkte 1 bis 3 umgesetzt: alle Kritiker der getroffenen Pfade; Kritik ist ein Betreff, der mit `Kritik ` beginnt, mit mehreren Hashes, jeder andere Code-Commit wird geprüft; `erledigteLoeschen.py` löscht nur, was git kennt. Scheiter-Tests in `standTest.py`, `erledigteLoeschenTest.py`. Punkt 4 als bekannte Lücke in `prozess/regeln.md`.
