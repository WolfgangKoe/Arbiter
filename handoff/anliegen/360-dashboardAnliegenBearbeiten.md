# Dashboard: Anliegen ansehen, zurück und bearbeiten

360 · Fragen · von Regelumsetzer (Prozess) → Stakeholder · Runde 2/3 · offen

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Aus 246: Die Datei hinter einer Karte hat keinen Weg zurück; Status, Kommentare
und Antworten lassen sich nicht aus dem Dashboard geben (`dashboard.html` ist statisch).

**Kosten.** Ohne beides steuert er nur über Editor und Browser-Zurück.

**Gegenvorschlag.** Mini-Server (`http.server`, 127.0.0.1, von Hand gestartet) in
`rollenregeln/`: Dashboard, je Anliegen eine Seite mit „‹ Dashboard“ und Formular; schreibt nur
Züge des Stakeholders in `handoff/anliegen/*.md`; Zähler „Du bist dran: n“.

**F1 · Weg zum Schreiben.** A: lokaler Mini-Server (Empfehlung). B: nur statische Seiten.
Antwort: .

**F2 · Welche Züge.** A: Status aus der Tabelle des Ablaufs je nach Rolle, Runde senken,
`eskaliert` ändern, `Kommentar:` und `Antwort:` (Empfehlung). B: nur Antwort und Kommentar.
Antwort: .

**F3 · Schutz.** A: nur Anliegen mit ihm als Absender oder Empfänger (Empfehlung). B: alle.
Antwort: Ja, bei diesen Anliegen auf jeden Fall. Bei den anderen möchte ich eine Kommentarfunktion, damit ich intervenieren kann.

**Stellungnahme.** Was hier ggf. noch fehlt ist eine Art Skript, dass die Kommentare und das setzen der Status "abholt", wenn es in den Ablauf passt. Es gab ja immer mal wieder Probleme, dass ich in die Anliegen geschrieben habe und du ebenfalls und dann kam es zu einem Konflikt. Es braucht also noch etwas, das diese Sachen zu einem passenden Zeitpunkt in die Datei schreibt, damit du es dann lesen und commiten kannst. Dafür müssen die Informationen im Dashboard natürlich gehalten werden.
Und was ebenfall noch gemacht werden muss. Die Anliegen und der Tokenbericht sollten voneinander getrennt, also auf zwei Seiten sein. So ähnlich, wie in ArbiterMap, dass Baklog über einen Reiter getrennt war.
Und schließlich fehlt auch ein Aktualisierungszyklus in die andere Richtung. Jedes Mal, wenn es eine Änderung in Handoff gibt, sollte es im Dashboard angezeigt werden. 

## Runde 2
**Befund.** F1 bis F3 gelten wie empfohlen. Offen ist der Zeitpunkt, an dem die Züge in die
Dateien kommen; das ist ein Eingriff in den Ablauf, den der Organisationsentwickler setzt.

**Kosten.** Schreibt der Server sofort, trifft er eine Rolle mitten im Edit (der Konflikt von früher).

**Gegenvorschlag.** Der Server schreibt Züge nur in `prozess/dashboard/eingang.jsonl`, das
Dashboard zeigt sie als „vorgemerkt“. Ein Skript legt sie in die Dateien, sobald keine Rolle
läuft (Hook vor dem nächsten Rollenstart, danach vor dem Commit); es verwirft Züge, die nicht
mehr zum Status passen, und meldet sie im Dashboard. Zwei Seiten: Anliegen und Tokenbericht
(Reiter), Anliegen nach Änderung in `handoff/` neu geladen. Kommentare zu fremden Anliegen:
Feld `Kommentar:` am Ende der Stellungnahme.

**F4 · Zeitpunkt.** A: wie beschrieben (Empfehlung). B: nur auf Knopfdruck „Jetzt übernehmen“.
Antwort: .

**Stellungnahme.**
