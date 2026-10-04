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
Antwort: .

**Stellungnahme.**
