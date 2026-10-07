# Kriterium und Spur nachschärfen

203 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von c3cd6d5 (Anliegen 114, B 7). Verhalten unverändert:
`python3 -m pytest prozess/pruefungen` 540 grün, ruff grün,
`python3 prozess/pruefungen/rueckverfolgung.py AUF-1.1` nennt Kriterium und drei Tests.
Offen bleiben:
1. `prozess/regeln.md:32` (Spur) nennt als Mechanismus noch `rueckverfolgung.py` (`spur`);
   `spur` steht jetzt in `spur.py`. Die Zeile 7 ist nachgezogen, die Zeile 32 nicht.
2. `kriterium.py` enthält mehr, als sein Docstring sagt („Kriterien und Tests lesen“), und
   Teile davon gehören woandershin:
   - `Fundstelle` und `kriteriumKennung` braucht nur `spur.py`. Die Fundstelle ist das
     Ergebnis der Spur und kein Baustein des Lesens.
   - `doppelte` braucht nur `rueckverfolgung.py` (`doppelteKennungen`). Mit Kriterien hat es
     nichts zu tun.
   - `pfadVon` ist ein allgemeiner Repo-Pfad. `datei.relative_to(wurzel).as_posix()` steht
     außerdem ausgeschrieben in `benennung.py` (4×), `erledigteLoeschen.py` (3×),
     `kommentare.py`, `glossar.py`, `schreibgrenze.py`.
3. Die Spur-Tests (`spurProbe`, `testSpur…`, `rueckverfolgungTest.py:196–230`) liegen weiter
   in `rueckverfolgungTest.py`, obwohl sie `spur.py` prüfen. wir.md: „Testdateien zu einem
   Modul: `<modul>Test.py`“. `rueckverfolgungTest.py` hat 13.002 Zeichen und steht wegen
   seiner Größe im Backlog. `kriterium.py` hat keine eigene Testdatei; `kriterien` und
   `getesteKriterien` werden über `rueckverfolgungTest.py` importiert.
4. Klein: Das Modul `kriterium` heißt so wie die lokale Variable `kriterium`, die in allen
   drei Modulen vorkommt. Bei `from spur import spur` heißen Modul und Funktion gleich. Wer
   später `import kriterium` schreibt, verdeckt das Modul in jeder Schleife
   `for kriterium in …`.

**Kosten.** 1: `regeln.md` schickt den Leser zum falschen Modul. Das ist genau das, was
107/114 beheben sollen. 2: Wer `kriterium.py` liest, findet Spur- und Prüfungsteile darin.
Die Teilung nach Aufgaben (114, B 7) ist nur halb vollzogen. 3: Die Zuordnung Modul ↔ Test
stimmt für `spur.py` nicht. Wer `spurTest.py` sucht, findet nichts. 4: Das Verdecken bricht
still, wenn sich der Importstil ändert.

**Gegenvorschlag.**
1. `regeln.md:32`: Mechanismus `spur.py` (`spur`), Befehl weiter über `rueckverfolgung.py`.
   Scheiter-Test `spurTest.py`.
2. `Fundstelle` und `kriteriumKennung` nach `spur.py`, `doppelte` nach `rueckverfolgung.py`,
   `pfadVon` nach `pfade.py`. Die ausgeschriebenen Stellen darfst du darauf umstellen, wenn
   du ohnehin dort bist.
3. Spur-Tests nach `spurTest.py` verschieben. Der Test der Kommandozeile
   (`testSpurZuUnbekanntemKriteriumIstEinFehler`, über `hauptprogramm`) darf bleiben.
4. Wahlweise: ein Modulname, der nicht als Variable vorkommt (etwa `kriterienLesen.py`).
   Sonst begründet ablehnen.

Erledigt, wenn 1 bis 3 umgesetzt sind und 4 umgesetzt oder begründet abgelehnt ist,
`python3 -m pytest prozess/pruefungen` grün ist und der Reviewer den Commit geprüft hat.

**Stellungnahme.**
Entfällt: Kritik am Prüfcode geht in den Rundgang (Retro 3).
