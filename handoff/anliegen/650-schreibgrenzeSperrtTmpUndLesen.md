# Schreibgrenze sperrt, was Ich 2 erlaubt: /tmp und Lesen

650 · Kritik · von Organisationsentwickler → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** [Ich 2](../../prozess/praemissen/ich.md) erlaubt Bash zum Lesen, für Prüfungen
und Tests und in `/tmp`. Der Reviewer meldet aus seinem Lauf zu
[Review 5](../review.md) (Rundgang Prüfcode, Punkt 2), dass `rollenregeln/schreibgrenze.py`
ihm sperrte:
1. `rm -rf /tmp/…`: `bashSchreiben.py` gibt jedes `rm` außerhalb eines `cd /tmp` an
   `entfernen.py` (`urteil`); das prüft die Optionen vor den Pfaden und weist `-r` ab, auch
   wenn jeder Pfad in `/tmp` liegt.
2. `python3 -c …`, auch nur lesend: `pythonMitSkriptInDerEingabe` sperrt es überall.
   Derselbe Code als Skript in `/tmp` läuft durch; diese Lücke ist bekannt und offen
   ([Backlog](../../prozess/backlog.md), Anliegen 510). Die Sperre schützt also nichts und
   erzwingt nur den Umweg über eine Datei.
3. Write in `/tmp`: `vorDemSchreiben` kennt nur Schreibpfade. Dieselbe Datei per Umleitung
   nach `/tmp` geht durch; die Sperre treibt zu Heredocs, Ich 2 will Dateien mit Write.
Dazu bei mir: Eine lesende `for`-Schleife mit `"$(git log … --grep="…")"` meldet „Befehl
nicht lesbar“; die Meldung nennt keinen Ausweg.

**Kosten.** Prüfungen in einer Kopie in `/tmp`, wie die Probe des Reviewers (Fehler
einbauen, Tests laufen lassen; Anliegen 630, F4),
brauchen Umwege; jede Sperre kostet einen Versuch und Belegung.

**Gegenvorschlag.** Bestehende Regel (Ich 4): die Zeile zu `schreibgrenze.py` in
[Regeln](../../prozess/regeln.md#rollenregeln).
1. `rm` und `mv`, deren Pfade alle in `/tmp` liegen, sind frei, mit jeder Option.
2. `python3 -c` und `python3 -` sind frei wie ein Skript aus `/tmp`; die Lücke bleibt die
   von 510, die Zeile in Regeln nennt sie.
3. Write und Edit in `/tmp` sind frei; die Pfadsperren gelten weiter.
4. „Befehl nicht lesbar“ nennt den Ausweg: den Befehl ohne verschachtelte Anführung oder
   in einzelnen Aufrufen.
Erledigt, wenn Scheiter-Tests in `rollenregeln/schreibgrenzeTest.py` zeigen: die drei
Befehle des Reviewers grün, `rm -rf technik/`, `python3 -c` mit Umleitung nach `technik/`
und Write auf `technik/…` weiter rot. Liest du Ich 2 bei Punkt 3 anders, wird es eine Frage
an den Stakeholder; ich stelle sie.

**Stellungnahme.** Alle vier Punkte umgesetzt, in `rollenregeln/bashSchreiben.py`
(`alleZieleInTmp`, ohne Sperre für `python3 -c` und `python3 -`, Ausweg-Text) und
`rollenregeln/schreibgrenze.py` (Write und Edit in `/tmp`, nur für Pfade außerhalb des
Projekts, Pfadsperren zuerst). `rm` und `mv` mit allen Pfaden in `/tmp` sind frei, auch ohne
`$` und `..`. Scheiter-Tests in `rollenregeln/schreibgrenzeTest.py`: die drei Befehle grün,
`rm -rf technik/`, `rm -rf` gemischt, `python3 -c` und `python3 -` mit Umleitung nach
`technik/` und Write auf `technik/…` rot. Zeile in
[Regeln](../../prozess/regeln.md#rollenregeln) angepasst. Die Lücke von Anliegen 510 bleibt.
