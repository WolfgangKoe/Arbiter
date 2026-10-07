# Schreibbilanz meldet Verstöße, die es nicht gibt

300 · Kritik · von Reviewer (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · offen

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

**Stellungnahme.**
