# sonarlint.py prüft nur Python, das Frontend bleibt ohne SonarLint

280 · Fragen · von Regelumsetzer (Prozess) → Stakeholder · Runde 1/3 · offen
Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Deine Frage aus 270: Lässt `formregeln/sonarlint.py` das Frontend still aus, weil hier
Node 18 statt 22.12 steht? Nein, aber aus anderem Grund. `sonarlint.py` startet nur
`sonarlint-ls.jar` mit `sonarpython.jar`, sammelt nur `*.py` und kennt weder `technik/frontend`
noch Node. Es schweigt also nie wegen Node; das Frontend ist schlicht nicht Teil der Prüfung.
Die Erweiterung in VS Code braucht Node ≥ 22.12 nur für ihre JavaScript-Analyse (hier
v18.19.1). Das Frontend prüfen heute ESLint und Stylelint (`frontendregeln/frontend.py`), nicht
das SonarLint-Standardprofil. „Mindestens so streng wie SonarLint“ (Ablauf, Werkzeuge) gilt für
`seite.js` damit nicht belegt.

**Kosten.** Gemessen: `sonarlint.py` braucht heute 44 s für etwa 10.600 Zeilen Python (Start des
Servers inklusive). Das Frontend hat 103 Zeilen JavaScript und 166 Zeilen CSS. Je Zeile wäre der
Zuschlag also unter 1 s. Geschätzt, nicht gemessen (Node 18 hier, `sonarjs.jar` läuft erst ab 22.12):
Start des Node-Prozesses der JS-Analyse etwa 5 bis 15 s einmalig, also 50 bis 60 s statt 44 s,
nicht 10 Minuten. Dazu: fehlt Node ≥ 22.12 auf einem Rechner, wäre die Prüfung rot. Ohne sie bleibt
die Lücke bei etwa 100 Zeilen JavaScript klein.

**F1 · Soll `sonarlint.py` das Frontend prüfen?** Empfehlung (bleibt): Nein, solange ESLint es deckt und die Lücke so klein ist; der Zuschlag wäre nicht das Problem, die Node-Voraussetzung ist es;
`regeln.md` und Ablauf nennen dann SonarLint ausdrücklich als Python-Prüfung. Wahl B: ja,
Node ≥ 22.12 wird Voraussetzung, fehlt es, ist die Prüfung rot.
Rückfrage des Stakeholders: Was bedeutet „der Lauf würde länger“? Statt 10 Sekunden 10 Minuten?
Klärung: Heute 44 s gemessen; mit JS geschätzt 50 bis 60 s (siehe Kosten), nicht Minuten.
Antwort: .

**Stellungnahme.** 
