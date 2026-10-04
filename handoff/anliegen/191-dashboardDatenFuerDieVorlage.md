# Dashboard: Welche Daten sollen für die Vorlage hinzukommen

191 · Fragen · von Regelumsetzer (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Du hast zu P4 bemängelt, `dashboard.html` sehe anders aus als
`ArbiterMap/steering/metrics/process_dashboard.html`. Das Aussehen ist nachgezogen: dunkles
Gold-Thema, je Sitzung eine Karte mit senkrechtem Säulendiagramm, gestrichelten
Schwellenlinien mit Beschriftung und Tabelle, rechts die Verteilung (Klassen von 25k, Median)
und die Legende mit Farbfeldern. Das Lauf-Log kennt nur Zeit, Rolle, Lauf, Sitzung und
Belegung bei Laufende. Nicht erfunden, daher nicht gezeigt:

- Orchestrator-Stand (erste, golden umrandete Säule): braucht eine Messung des Hauptkontexts.
- Cache-Anteil, frische Eingabe, Ausgabe (gestapelte Säule): `belegung.py` liest nur einen
  Wert aus dem Transkript; die Aufteilung müsste es mitliefern.
- Modell, Auftrag, Verbrauch (Tabelle): `SubagentStop` liefert sie nicht; Auftrag und Modell
  stehen im Aufruf des Koordinators (`PreToolUse` auf `Agent`).

**Kosten.** Je Spalte ein Hook oder eine Transkriptauswertung mehr, dazu Rauschen.
Ohne sie bleibt die Seite im Aufbau gleich, aber ohne diese Spalten und Segmente.

**Empfehlung.** A: Orchestrator-Stand und Cache-Anteil nachliefern (Kern der Vorlage),
Modell, Auftrag und Verbrauch weglassen. B: alles. C: so lassen.

Frage F1: A, B oder C?
Antwort: Ich bin mir nicht sicher, ob ich mit deiner Auswahl zufrieden bin. Orchestrator auf jeden Fall von den anderen farblich unterscheiden. Es fehlt die y-Achse in alle Diagrammen. "Beginn" und "Belegung" haben so keine Aussagekraft. Es bräuchte eher so etwas wie Task und Kontextfenster in der Form:
- Die Task gibt an, was der Subagent gemacht hat. Und bitte nicht nur die Anliegennummer. Zum Beispiel "Erstellung des Dashboads"
- Die Angabe des Kontextfensters sollte statt "38.247" auf "38k" gerundet werden. 
- Die Angabe des dahinter liegenden Modells ist notwendig (z.B. Opus, Sonnet,...)
Nach Umsetzung dieser Punkte, nehme ich das Dashboard ab.

**Stellungnahme.** Für den nächsten Zyklus: Was mir Dashboard noch fehlt sind die Daten z.B. aus Sonarlint oder den Metriken unserer Prüfungen. Ich hätte gerne sinnvolle Kennzahlen, die den aktuellen Stand darstellen. Das wäre aus meiner Sicht auf einer neuen Seite. Das kann im nächsten Zyklus umgesetzt werden.
Im übernächsten Zyklus könnten wir die Anliegen dort hineinbringen. Da kann ich dann kommentieren und nach "Enter" wird mein Text hier in die Anliegen geschrieben. Wenn Anliegen meine Aufmerksamkeit brauchen und ich etwas "annehmen" möchte, steht da nur ein Schalter und der überschreibt hier den Status. Entsprechend auch für "erledigt". Auf diese Weise überschreibe ich nicht aus Versehen Status und Inhalt anderer Anliegen. 
