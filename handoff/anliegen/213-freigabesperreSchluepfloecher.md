# Freigabesperre: Schlupflöcher und Leseort

213 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von b2a5221 (Anliegen 168). `python3 -m pytest prozess/pruefungen`
ist grün (600), die Scheiter-Tests aus 168 gehen so aus wie gefordert. Folgende Punkte habe ich mit
Proben geprüft:

1. `freigabeVerstoß` gibt bei jeder Änderung der Zyklusnummer alles frei, auch wenn die
   Nummer entfernt oder gesenkt wird. Probe: Edit `# Plan · Zyklus 3` → `# Plan · Zyklus` und
   dabei `Kommentar: warum so?` löschen, ist frei. Danach die Nummer zurücksetzen, auch frei.
2. `Freigabe: ja` → `offen` oder ganz entfernen ist frei, ebenso eine neue Zeile
   `Kommentar: <Text>` einer Rolle. [Ablauf](../../prozess/ablauf.md#freigabe-und-kommentare):
   „Diese Zeilen ändert nur er.“
3. `commitBetreff` erkennt `git commit -qm"Freigabe Plan 3"` nicht (shlex: ein Wort
   `-qmFreigabe Plan 3`), ebenso `-amFreigabe…`. Der Freigabe-Commit geht bei `offen` durch.
   `-C`/`--reuse-message` fehlen in der Grenze der Stellungnahme, dort steht nur `-F`.
4. `statusrecht.entscheide` liest jetzt jede Datei, bevor der Pfad geprüft ist (Zeile 37).
   Probe: Edit auf eine Datei, die kein UTF-8 ist, endet mit `UnicodeDecodeError`. Der Hook
   bricht ab, statt nichts zu tun.
5. Bash: Rollen können Plan, Review und Retro mit `sed -i` oder einer Umleitung ändern
   (Grenze der Stellungnahme). Für Anliegen gibt es den Mechanismus schon:
   `ändertPfad(befehl, wurzel, istAnliegen)`.
6. Wiederverwendung: `freigabeCommitVerstoß` baut die Bedingung aus `freigabeZuCommitten` nach
   (Zyklus und `freigabeJa in zeilenDer`) und liest die Datei dafür zweimal. `stakeholderZeilen`
   wiederholt die Kommentarprüfung aus `hatKommentarOhneStellungnahme`. Den Pfad
   `wurzel / "handoff" / artefakt.datei` bauen jetzt sechs Stellen (siehe
   [210](210-freigabefeldNurImAbschnittLesen.md), Punkt 3). Die Commit-Sperre prüft `ja`
   irgendwo in der Datei, nicht nur unter `## Freigabe` (210, Punkt 1).

**Kosten.** Zu 1 bis 3: Die Sperre soll eine Rolle aufhalten, die aufräumt. Diese Wege kommen
ohne Warnung durch. Zu 2: Eine Rolle nimmt eine Freigabe zurück, und der Stand nennt
keinen Commit mehr. Ein Kommentar, den eine Rolle schreibt, macht den Autor dran. Zu 4: Ein Hook,
der abbricht, macht bei jeder Bearbeitung Lärm. Zu 5: Die Sperre umgehen kostet nur einen
Befehl. Zu 6: Das Feld wird an drei Stellen gelesen, ein Fix aus 210 erreicht die
Commit-Sperre nicht.

**Gegenvorschlag.**
1. Abgelöst wird die Datei nur, wenn die neue Nummer größer ist als die alte. Ohne alte
   Nummer bleibt es wie bisher. Ablauf: „bis der Autor die Datei im nächsten Zyklus neu
   schreibt“.
2. Statt drei Abfragen genügt ein Vergleich: Zeilen `Freigabe: ja` und Kommentare mit Text
   bleiben als Multimenge gleich (`Counter` alt == neu). `Freigabe: offen` darf
   hinzukommen, aber nicht wegfallen.
3. Ein Muster `-[a-zA-Z]*m(.*)`: Bleibt die Gruppe leer, gilt das nächste Wort, sonst die
   Gruppe. Damit fallen zwei Zweige weg. `-C` und `--reuse-message` kommen in die Grenze oder
   werden beim Koordinator gesperrt.
4. Erst prüfen, ob das Ziel Freigabe-Artefakt oder Anliegen ist, dann lesen.
5. In `bashPositivliste.entscheide` für Rollen `ändertPfad(…, istFreigabeArtefakt)` mit
   eigener Meldung.
6. Mit 210 entsteht eine Funktion `freigegebenerZyklus(wurzel, artefakt) -> int | None`
   (Zyklus, wenn das Feld unter `## Freigabe` `ja` ist). Stand und Commit-Sperre nutzen sie.
   Dazu `istStakeholderKommentar(zeile)` für beide Kommentarprüfungen.

Scheiter-Tests: Nummer entfernt oder gesenkt und Kommentar gelöscht rot. `ja` → `offen` rot.
Neuer Kommentar einer Rolle rot. `-qm"Freigabe Plan 3"` bei `offen` rot. Edit auf eine
Datei, die kein UTF-8 ist, ergibt `None`. `sed -i … handoff/plan.md` einer Rolle rot.

Erledigt, wenn die Scheiter-Tests grün sind, `python3 -m pytest prozess/pruefungen` grün ist
und der Reviewer den Commit geprüft hat.
