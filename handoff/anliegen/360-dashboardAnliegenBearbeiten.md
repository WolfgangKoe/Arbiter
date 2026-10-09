# Dashboard: Anliegen ansehen, zurück und bearbeiten

360 · Fragen · von Regelumsetzer (Prozess) → Stakeholder · Runde 2/3 · offen

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Aus Anliegen 246, Rückmeldung des
Stakeholders: (1) Die Datei hinter dem Link einer Karte hat keinen Weg zurück zum Dashboard.
(2) Die Karten könnten bei vielen Anliegen unübersichtlich werden; vorerst bleibt es so.
(3) Status, Kommentare und Antworten auf Fragen lassen sich nicht aus dem Dashboard geben.
`dashboard.html` ist eine statische Datei und schreibt nichts; die Züge setzt er heute in
der Datei ([Ablauf, Anliegen](../../prozess/ablauf.md#anliegen)).

**Kosten.** Ohne Weg zurück und ohne Bearbeiten steuert er nur über Editor und Browser-Zurück.
Ein Schreibweg birgt das Risiko, dass das Dashboard Dateien ändert, die ihm nicht gehören.

**Gegenvorschlag.** Ein Mini-Server nur mit Standardbibliothek (`http.server`) in
`rollenregeln/`, gebunden an 127.0.0.1, gestartet von Hand. Er zeigt das Dashboard und je
Anliegen eine Seite mit „‹ Dashboard“ oben und Formular. Er schreibt nur in
`handoff/anliegen/*.md`, nur die Züge des Stakeholders, mit Scheiter-Test je Zug und Zeile in
[Regeln](../../prozess/regeln.md). Die Karten aus 275 behalten Filter; ergänzt wird oben
ein Zähler „Du bist dran: n“ und die Spalte Stakeholder zuerst.

**F1 · Weg zum Schreiben.** A: lokaler Mini-Server (Empfehlung). B: keine Schreibfunktion,
nur „Datei öffnen“ und „‹ Dashboard“ als statische Seite je Anliegen.
Antwort: .

**F2 · Welche Züge.** A: Status nur aus der Tabelle des Ablaufs, die dem Stakeholder je nach
Rolle (Empfänger oder Absender) zustehen; Runde senken und `eskaliert` ändern; Textfeld
`Kommentar:` und `Antwort:` unter jeder Frage (Empfehlung). B: nur Antwort und Kommentar,
Status weiter in der Datei.
Antwort: .

**F3 · Schutz.** Der Server ändert nur Anliegen, bei denen der Stakeholder Absender oder
Empfänger ist, und keinen Kopf, der nicht zur Statustabelle passt. A: ja (Empfehlung).
B: alle Anliegen frei.
Antwort: Ja, bei diesen Anliegen auf jeden Fall. Bei den anderen möchte ich eine Kommentarfunktion, damit ich intervenieren kann.

**Stellungnahme.** Was hier ggf. noch fehlt ist eine Art Skript, dass die Kommentare und das setzen der Status "abholt", wenn es in den Ablauf passt. Es gab ja immer mal wieder Probleme, dass ich in die Anliegen geschrieben habe und du ebenfalls und dann kam es zu einem Konflikt. Es braucht also noch etwas, das diese Sachen zu einem passenden Zeitpunkt in die Datei schreibt, damit du es dann lesen und commiten kannst. Dafür müssen die Informationen im Dashboard natürlich gehalten werden.
Und was ebenfall noch gemacht werden muss. Die Anliegen und der Tokenbericht sollten voneinander getrennt, also auf zwei Seiten sein. So ähnlich, wie in ArbiterMap, dass Baklog über einen Reiter getrennt war.
Und schließlich fehlt auch ein Aktualisierungszyklus in die andere Richtung. Jedes Mal, wenn es eine Änderung in Handoff gibt, sollte es im Dashboard angezeigt werden. 
