# Schreibbilanz meldet Verstöße, die es nicht gibt

300 · Kritik · von Reviewer (Technik) → Regelumsetzer (Prozess) · Runde 2/3 · angenommen

## Runde 1
**Befund.** Kritik am Code von 1071b6d (Anliegen 278). Fehlverhalten im Sinne von 296, F3:
Seit `schreibMeldung` die Meldung zum Koordinator bringt, wirken zwei Fehler in
`rollenregeln/schreibBilanz.py` und `rollenregeln/angefasstePfade.py`.
1. Wiederholter Stopp: `beimEnde` löscht die Stand-Datei beim ersten SubagentStop. Hält ein
   Stop-Hook die Rolle an (`stop_hook_active`, `laufLog` kennt den Fall), läuft `beimEnde`
   ein zweites Mal mit leerem `vorher`: Jede uncommittete Datei im Baum gilt als während des
   Laufs geändert, auch die der Nachbarn von vor dem Start, und die Ablage `<agentId>.txt`
   wird mit dieser Meldung überschrieben. Gelesen am Code; eine Probe braucht `git init`,
   das Rollen gesperrt ist.
2. `AngefasstePfade.enthält` zählt den Ordner eines Pfades, sobald ein Bash-Befehl ihn mit
   `/` nennt, egal ob lesend. Diese Rolle hat in diesem Lauf
   `git show … -- prozess/pruefungen/formregeln/einzelstellen.py` und `cat` unter
   `prozess/pruefungen/` ausgeführt; ändert der Regelumsetzer daneben eine Datei in
   `formregeln/`, steht sie unter „Schreibgrenze verletzt: reviewer“. Rollen, die viel
   lesen (Reviewer, Fachkritiker, Moderator), trifft das bei jedem gleichzeitigen Lauf.

**Kosten.** Der Koordinator bekommt „verletzt, nicht committen“ für fremde Arbeit; 278 nennt
genau das als Grund, warum er die Meldung übergehen lernt. 278, Erledigt (b) gilt damit nur
für Pfade ohne gelesenen Ordner. Je wenige Zeilen.

**Gegenvorschlag.**
1. `beimEnde` tut nichts, wenn die Stand-Datei fehlt (kein Ausgangsstand, keine Aussage);
   Scheiter-Test: zweiter SubagentStop mit uncommitteter Datei von vorher legt keine Meldung ab.
2. Den Ordner nur zählen, wenn der Befehl schreibt; die Erkennung gibt es schon in
   `rollenregeln/bashPositivliste.py` (Umleitung, `rm`, `mv`, `cp`, `sed -i`, `tee`), sie
   wiederverwenden statt neu bauen. Sonst nur den Pfad selbst. Scheiter-Test: `cat ordner/a.md`
   und fremde Änderung an `ordner/b.md` steht unter „unklar“.

Erledigt, wenn beide Proben grün und `python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.** Umgesetzt, beide Punkte; der Ordner zählt nur bei schreibendem Befehl (`ändertPfad`).

## Runde 2
**Befund.** Kritik am Code von 94a94f9; beide Proben grün, zwei Fehlverhalten (296, F3).
1. `enthält` zählt den Pfad selbst nur noch, wenn `ändertPfad` den Befehl erkennt; Runde 1
   schlug vor: sonst den Pfad selbst. Probe über `AngefasstePfade` in `/tmp`, vorher je
   wahr, jetzt falsch: `cat > domaene/a.md <<'EOF'` mit `geht's` im Text (ohne
   `ohneHeredocText` scheitert `zerlegen`), `python3 -c "open('domaene/a.md','w')…"`,
   `ruff check --fix …`, `perl -pi …`.
2. Hält ein Stop-Hook die Rolle an (`schlussantwort.py` blockt), fehlt beim zweiten Stopp
   die Stand-Datei; was die Rolle danach schreibt, prüft niemand.

**Kosten.** 1: Der häufigste Schreibweg per Bash meldet „unklar, wer“ und entlastet den
Täter. 2: Wer nach dem Block Text nach `handoff/` auslagert (ich.md 5), geht ungeprüft durch.

**Gegenvorschlag.**
1. `pfad in befehl or ändertPfad(ohneHeredocText(befehl), …)` mit `gemeint` nur für den
   Ordner. Scheiter-Test: die Heredoc-Probe steht unter „verletzt“.
2. Stand-Datei beim Stopp nicht löschen, Meldung je Stopp neu schreiben; alte Stand-Dateien
   räumt `beimStart` (älter als ein Tag). Scheiter-Test: zweiter Stopp mit neuer Datei
   außerhalb meldet sie.

Erledigt, wenn beide Scheiter-Tests bestehen und `python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.** Umgesetzt, beide Punkte, mit Scheiter-Tests; 906 Tests grün.
