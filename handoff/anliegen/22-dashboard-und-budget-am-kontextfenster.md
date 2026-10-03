# Dashboard für alle Repos, Budget am Kontextfenster

22 · Anliegen · von Stakeholder → Organisationsentwickler · Runde 1/3 · angenommen

Bearbeitung in der Retro von Zyklus 1.

## Runde 1
**Befund.** Notiz des Stakeholders, wörtlich: „Das Dashboard aus ArbiterMap Repo-übergreifend
verfügbar machen. Ich möchte das Budget am Kontextfenster des Koordinators festlegen und die
Subagenten sollen sich ebenso daran halten.“
Heute zählt das Budget Rollenläufe je Phase (`stand.py`, `rollenzaehler.py`): ein Lauf mit
20.000 Token zählt wie einer mit 300.000. Die Belegung misst hier niemand. Das Dashboard
(`ArbiterMap/harness/process_report.py`, `report_page.*`) hängt an Pfaden und Backlog von
ArbiterMap. Bordmittel: Die Statuszeile kennt `context_window.used_percentage` nur für die
Hauptsitzung; für Subagenten gibt es kein Token-Feld (`maxTurns` zählt Runden), ihre Belegung
steht nur im Transkript. In ArbiterMap lag jede Selbstschätzung eines Subagenten zu niedrig
(`process/rules.md`, V-30).

**Kosten.** Übernahme heißt Neuschreiben: 57.000 Zeichen Seite, 65.000 Zeichen Hooks. Ein
Plugin im Nutzerbereich gilt in jedem Repo und bringt Hooks und Skript mit; jedes Repo zahlt
dann die Messung.

**Gegenvorschlag.**
1. Plugin `dashboard` (eigener Ordner, Nutzerbereich): ein Hook misst die Belegung jedes Laufs
   aus dem Transkript und schreibt je Repo nach `.git/arbiter/`; ein Skript erzeugt daraus die
   Seite. Backlog-Reiter nur, wo ein Repo ihn liefert.
2. Eine Grenze in Token für die Belegung, gesetzt vom Stakeholder, gilt für den Koordinator
   und gleich für jeden Subagenten. Der Stand zeigt sie statt der Rollenläufe; die Zählung
   bleibt Kennzahl im Dashboard.
3. Wirkung: bei 80 % eine Meldung in den Kontext der Rolle, bei 100 % sperrt ein Hook alles
   außer Schreiben im eigenen Pfad und der Schlussantwort. Beim Koordinator entscheidet der
   Stakeholder: freigeben, kürzen, neuer Chat.

Antwort: Du kannst die Html Datei aus dem Unterordner hierin kopieren ohne es komplett neu zu bauen. Es enthält auch eine Liste mit den Backlog items. Ich bin mir nicht sicher, ob und wie wir dieses hier einbringen könnten. Wäre aktuell aber nicht so relevant. Die Hooks sind von diesem Projekt ebenfalls nützlich. Ich bin mir aber nicht sicher, ob die in dem Ordner enthalten sind, sonst gehe ich nochmal suchen.

**F1 · Welche Grenze?** A: 120.000 Token (ArbiterMap R-10). B: 100.000. C: ein Anteil am
Fenster. Empfehlung A: dort an zehn Sitzungen bestätigt; absolut, also gleich bei 200.000
und 1 Mio. Fenster.

Antwort: Wie in der Html schon festgelegt. 120k Windown 150k oberste Grenze. Vielleicht passen wir es noch ein wenig an, wenn es so weiter geht wie hier. Wir sind nämlich bei 59k und es liefen 9 Subagenten. 

**F2 · Wo liegt das Plugin?** A: eigenes Repo neben beiden. B: in `Arbiter_Structure/`.
Empfehlung A: Es gehört keinem Produkt.

Antwort: B, es gehört mir, darf aber von Subagenten aus der Prozess-Sicht bearbeitet werden. 

**Stellungnahme.** Organisationsentwickler: Budget angenommen und überführt nach
[`prozess/ablauf.md`](../../prozess/ablauf.md) (Budget, Anliegen): 120.000 Token nichts Neues
beginnen, 150.000 Sperre, gleich für Koordinator und Rollen; Messung und Sperre baut der
Regelumsetzer. Dashboard und Plugin in `Arbiter_Structure/` folgen in der Retro von Zyklus 1;
darum bleibt der Status offen.
Retro 1: Das Dashboard steht mit deinen Antworten und einem Auslöser in
[`prozess/backlog.md`](../../prozess/backlog.md); die Kennzahlen liefert vorerst P8.
