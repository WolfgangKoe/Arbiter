# Dashboard: alle Sessions auffindbar, sechs je Seite

246 · Anliegen · von Stakeholder → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Das Dashboard (`dashboard.html`, erzeugt von `prozess/pruefungen/rollenregeln/dashboard.py`)
zeigt nur die letzten 5 Sessions (`sichtbareSitzungen = 5`, Zeile `list(nachSitzung(läufe).items())[-sichtbareSitzungen:]`).
Ältere „verschwinden“. Stakeholder, wörtlich: „Das Dashboard zeigt lediglich die letzten 5
Sessions. Darüber hinaus ‚verschwinden‘ sie. Ich möchte gerne, dass alle Sessions zu finden
sind. Und zwar über einen Seitencounter. Auf jeder Seite sollen 6 Sessions sichtbar sein.
Dieses Feature war bereits im Dashboard von ArbiterMap implementiert.“

**Kosten.** Ohne Blättern sind ältere Läufe und ihre Tokenstände nicht mehr einsehbar.

**Gegenvorschlag.** Vorlage: `ArbiterMap/harness/report_page.js` (nur lesbar), Abschnitt
„Seitenschalter“ ab Zeile 483 (`seitenAnzahl`, `zeichneSeitenschalter`; Konstante
`SEITENGROESSE` Zeile 27, dort 8) und Kopfkommentar Zeile 24; Markup `<nav id="seitenschalter">` in
`ArbiterMap/harness/report_page.html` Zeile 37, Stil `.seitenschalter` in
`ArbiterMap/steering/metrics/process_dashboard.html` ab Zeile 111.
- Alle Sessions erreichbar, neueste zuerst, 6 Sessions je Seite (in ArbiterMap 8).
- Seitenschalter mit „‹ Zurück“, Seitenzahlen, „Weiter ›“ und Stand („Session 1–6 von n“);
  bei nur einer Seite entfällt er.
- Mit Scheiter-Test nach [Ablauf](../../prozess/ablauf.md) und Eintrag in
  [Regeln](../../prozess/regeln.md) (Zeile Dashboard).
- Offen für den Regelumsetzer: ob der Zähler im Browser (wie ArbiterMap, Skript in der HTML)
  oder als vorab erzeugte Seiten läuft; die Stellungnahme entscheidet.

**Stellungnahme.** Umgesetzt, Browser-Variante wie ArbiterMap: `dashboard.html` enthält alle Sitzungskarten, neueste zuerst; ein kleines Skript in der Seite zeigt sechs je Seite und baut den Seitenschalter („‹ Zurück“, Seitenzahlen, „Weiter ›“, „Session 1–6 von n“). Bis sechs Sitzungen entfallen Schalter und Skript, ohne Skript sind alle Karten sichtbar. Konstante und Markup in `prozess/pruefungen/rollenregeln/dashboardSeiten.py`, Scheiter-Test `dashboardSeitenTest.py` (der alte Deckel von fünf ließe ihn rot werden), Zeile in [Regeln](../../prozess/regeln.md). Das Blättern im Browser selbst ist nicht automatisch getestet, nur Markup und Skripteinbindung.

Die Umsetzung bisher gefällt mir recht gut. Folgendes Feedback
1. Der Klick auf den Link einer Anliegenkarte führt auch zu dem Text in der Datei selbst. Was dort dann aber fehlt ist ein "Zurück"-Button. Ich muss das über den Browser machen. 
2. Ich bin mir nicht sicher, ob die Karten-Ansicht nicht unübersichtlich wird, wenn es wieder viele Anliegen werden. Aber lassen wir es so.
3. Mir fehlt noch komplett das Bearbeiten der Anliegen aus dem Dashboard heraus. Ich möchte den Status des Anliegens als Stakeholder bearbeiten können, wenn ich involviert bin. Ich möchte Kommentare und Antworten auf Fragen aus dem Dashboard heraus gegen können. Mir fehlt hier einfach die Bearbeitungsmöglichkeit. 
Für diesen Zyklus würde ich das Dashboard erstmal so abnehmen. Öffne bitte ein neues Anliegen, in welchem du mein Feedback berücksichtigst und sinnvoll ergänzt, um eine Steuerbarkeit aus dem Dashboard heraus zu ermöglichen.