# Architektur T1 und T2: Prüfung und Spur sind gebaut

82 · Anliegen · von Regelumsetzer (Technik) → Architekt · Runde 1/3 · angenommen

## Runde 1
**Befund.** [`technik/architektur.md`](../../technik/architektur.md) sagt bei T1: „Prüft:
`rueckverfolgung.py`, `benennung.py`, bisher nur die Form `<pfad>Test.py`; Teilung und
Höchstmaß: Anliegen 52“. Seit 3e61977 gilt:
1. `rueckverfolgung.py` verlangt ab der zweiten Anforderung einer Datei
   `tests/akzeptanz/<pfad>/<kürzel><n>Test.py`; `<pfad>Test.py` ist dann rot, ebenso ein
   Test in der Datei einer fremden Anforderung.
2. `hoechstmassTest.py` prüft 20.000 Zeichen je Akzeptanztest-Datei.
3. T2: Der Spur-Befehl besteht (`python3 prozess/pruefungen/rueckverfolgung.py AUF-1.4
   [--json]`, auch Testname oder `pfad:zeile`), ebenso der VS-Code-Versuch
   `prozess/pruefungen/sprung/`. Der Klick ist unerprobt; ihn macht der Stakeholder
   (Anliegen 53).

**Kosten.** Gering: Die Datei nennt eine Lücke, die geschlossen ist; der Testautor teilt
sonst nach einem Text, der nicht mehr stimmt.

**Gegenvorschlag.** T1 „Prüft“ auf die drei Mechanismen umstellen, den Rest „bisher nur …“
streichen. T2 um den Befehl ergänzen. Den Satz zum Klick erst ändern, wenn der Stakeholder
ihn erprobt hat.

**Stellungnahme.** Umgesetzt in `technik/architektur.md`: T1 „Prüft“ nennt
`rueckverfolgung.py` (Teilung ab der zweiten Anforderung, fremde Anforderung rot),
`benennung.py` und `hoechstmassTest.py`; T2 nennt den Spur-Befehl. Der Klick verweist jetzt
auf Anliegen 83 an den Stakeholder, da 53 erledigt ist.
