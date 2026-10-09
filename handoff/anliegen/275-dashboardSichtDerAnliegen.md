# Dashboard: Sicht auf die Anliegen

275 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Der Stakeholder will die Anliegen im Dashboard beobachten und steuern
(Anliegen 254, F4 A): erst eine Sicht mit Filter, die Züge setzt er in der Datei. Das
Dashboard (`rollenregeln/dashboard.py`, `dashboard.html`) zeigt nur Läufe.

**Kosten.** Wer dran ist und was wartet, sieht er nur im Stand oder in der Moderation.

**Gegenvorschlag.** Erledigt, wenn, je mit Scheiter-Test und Zeile in
[Regeln](../../prozess/regeln.md):
1. Ein Abschnitt Anliegen mit einer Spalte je Zuständigem nach
   [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) (`anliegenregeln/anliegen.py`, `dran`),
   dazu eine Spalte für wartende.
2. Je Anliegen eine Karte: Nummer als Link auf die Datei, Titel, Form, Runde, wartet auf.
3. Filter nach Rolle und Form, im Browser, ohne Server.
Mit Anliegen 246 (dieselbe Datei) in einem Lauf möglich; die Formen und `wartet auf` liest
die Sicht erst nach Anliegen 274. Knöpfe für die Züge stehen im
[Backlog](../../prozess/backlog.md).

**Stellungnahme.** Teilweise umgesetzt: Punkte 1 (ohne die Spalte der wartenden), 2 (ohne `wartet auf`) und 3. `dashboard.html` zeigt oben den Abschnitt Anliegen mit einer Spalte je Zuständigem (`dran` und `nachprüfungen`), Karten mit Nummer als Link, Titel, Form und Runde, und Filter nach Rolle und Form im Browser. Code `rollenregeln/dashboardAnliegen.py`, Scheiter-Test `dashboardAnliegenTest.py`, Zeile in [Regeln](../../prozess/regeln.md). Offen bleibt die Spalte der wartenden und `wartet auf` auf der Karte: Anliegen 274 gibt es noch nicht, `kopfLesen` überspringt Köpfe mit `· wartet auf`. Sobald 274 liest, ergänze ich beides in einer neuen Runde.