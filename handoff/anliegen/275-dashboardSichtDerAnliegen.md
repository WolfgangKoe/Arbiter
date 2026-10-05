# Dashboard: Sicht auf die Anliegen

275 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

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

**Stellungnahme.**
