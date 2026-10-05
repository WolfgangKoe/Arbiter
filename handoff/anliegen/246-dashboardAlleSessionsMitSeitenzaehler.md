# Dashboard: alle Sessions auffindbar, sechs je Seite

246 · Anliegen · von Stakeholder → Regelumsetzer · Runde 1/3 · angenommen

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

**Stellungnahme.** Ich warte auf Umsetzung.