# Dashboard: Lücken in den Sitzungen, Titel, Dauer, Aktualisierung

194 · Anliegen · von Stakeholder → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Notiz des Stakeholders, vom Koordinator festgehalten; noch nicht umgesetzt.
Antwort: „Es gibt da offensichtlich noch ein paar Fehler im Dashboard. In der ersten Sitzung
fehlen ein paar Daten (z.B. vom Koordinator). In der zweiten Sitzung sind die Angaben bei drei
Subagenten nicht da. Der Titel der Sitzung sollte eher so etwas wie Zyklus 3 Prozessphase
heißen. Das sollte man zusammenbauen können. Die Spalte „Ende“ kann entfallen. Dafür eher
Dauer, wenn man das messen kann. Wie oft wird denn die Datei aktualisiert? Mir wäre es recht,
dass es jedes Mal geschieht, wenn ein neuer Agent gestartet wird.“

Screenshots: Abschnitt „ohne Sitzung“, 6 Läufe (regelumsetzer, organisationsentwickler,
reviewer, 10-04 14:17 bis 14:24), ohne Koordinator-Säule, Modell und Auftrag leer. Abschnitt
„Sitzung f8ebd61f“, 14 Läufe: bei den ersten drei (regelumsetzer 14:30, reviewer 14:33,
regelumsetzer 14:35) sind Modell und Auftrag leer, ab reviewer 14:51 gefüllt.

**Befunde zur Prüfung.**
1. „ohne Sitzung“: Einträge ohne `sitzung`, `koordinator`, `modell`, `ziel` (Altbestand aus
   der Zeit vor den Feldern, Anliegen 191). Prüfen, ob sie nachgetragen werden können, sonst
   als Altbestand kennzeichnen statt leer zeigen.
2. Sitzung f8ebd61f: die drei frühen Läufe haben `modell` und `ziel` leer. Vermutung: vor
   den Feldern geschrieben. Prüfen am Log, dann nachtragen oder kennzeichnen.
3. Sitzungstitel „Zyklus 3 Prozessphase“ statt Sitzungs-Id. Heute steht der Zyklus nicht im
   Eintrag; `phasenfolge.py` kennt ihn (`lage`, wie `stand.py`). Er müsste beim Eintragen
   mitgeschrieben werden, der Titel setzt sich daraus zusammen. Der Stakeholder schreibt
   „Prozessphase“, die Phase heißt in `phasenfolge.py` anders: Wortlaut dort prüfen.
4. Spalte „Ende“ entfällt, dafür „Dauer“. Messbar: Jede Transkriptzeile trägt einen
   Zeitstempel, Dauer = letzter minus erster; bei fortgesetzten Läufen je Auftrag.
5. Aktualisierung: siehe Antwort unten.

**Antwort auf die Frage nach der Aktualisierung.** Heute schreibt `laufLog.py` die Datei bei
jedem `SubagentStop`, also nach jedem beendeten Lauf, einschließlich geblockter Stopps. Beim
Start eines Agenten geschieht nichts. „Bei jedem Start“ ist möglich: `SubagentStart` hat
bereits Hooks in `.claude/settings.json`, ein weiterer Eintrag ruft `dashboardSchreiben`
auf. Das zeigt dann alle bis dahin beendeten Läufe, der neu gestartete fehlt bis zu seinem
Ende. Beides zugleich ist billig (Hook ohne Tokenkosten); Start und Stopp wären die Lösung.

**Kosten.** Mehr Felder im Log, ein weiterer Hook; Altbestand bleibt lückenhaft.

**Stellungnahme.**
Umgesetzt in `laufLog.py` und `dashboard.py`, getestet in `dashboardTest.py`:
- Befund 1 und 2: Die Transkripte der alten Läufe sind nicht mehr zu lesen, Nachtragen ist
  unmöglich. Fehlendes zeigt die Tabelle als „–“, die Karte heißt „Altbestand, ohne Sitzung“.
- Befund 3: Der Eintrag trägt `zyklus` und `phase` aus `phasenfolge.lage`; Titel „Zyklus 3
  Prozessphase · Sitzung f8ebd61f“ (die Phase heißt dort „Prozessphase“).
- Befund 4: Spalte „Ende“ entfällt, „Dauer“ = jüngster Auftrag bis letzte Transkriptzeile.
- Befund 5, Hook bei `SubagentStart`: offen. Der Eintrag in `.claude/settings.json`
  (`dashboard.py --still`, schreibt nur die Seite) wurde vom Berechtigungssystem
  abgelehnt; `--still` ist umgesetzt. Der Stakeholder setzt den Eintrag oder gibt ihn frei.
