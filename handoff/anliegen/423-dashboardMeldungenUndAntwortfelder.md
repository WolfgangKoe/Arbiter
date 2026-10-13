# Dashboard: Meldungen in Klartext, Antwortfelder für wer dran ist

423 · Anliegen · von Stakeholder → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder sah im Dashboard sechs rote Zeilen in Technikersprache, obwohl er
nichts falsch gemacht hatte: Es waren seine zweiten Antworten aus Anliegen 418, 420 und 384
(Fehler, den [Anliegen 422](422-sonarlintVersionHeben.md) nicht berührt). Zudem bot das
Dashboard bei Anliegen 421 (Rückfrage, er ist dran) keine Antwortfelder, weil er nicht
Empfänger ist.

**Umsetzung.**
- Was schon im Anliegen steht (gleicher Status, gleiche Antwort), wird still übergangen.
- Die Meldungen und die Zeilen „vorgemerkt“ und „nicht übernommen“ nennen die Eingabe in
  Worten („Anliegen 418 · Antwort auf F1: A“) und sagen, was los ist („Das Anliegen steht auf
  erledigt; von dort geht es nicht auf angenommen.“).
- Antwortfelder gibt es, wenn das Anliegen offen beim Stakeholder liegt oder er bei einer
  Rückfrage Absender ist; die Antwort steht unter der Frage der letzten Runde.
- Die sechs alten Zeilen sind entfernt.

Scheiter-Tests: `rollenregeln/zuegeUebernehmenTest.py`
(`testWasSchonImAnliegenStehtMeldetDasDashboardNichtAlsFehler`,
`testAufEineRückfrageAnDenStakeholderAntwortetErUnterDerFrageDerLetztenRunde`),
`rollenregeln/dashboardServerTest.py`
(`testWerBeiEinerRückfrageDranIstBekommtAntwortfelderUndDasDashboardNenntDieZügeInKlartext`).
