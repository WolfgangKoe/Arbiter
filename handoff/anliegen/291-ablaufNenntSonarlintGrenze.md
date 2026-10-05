# Ablauf, Werkzeuge: SonarLint prüft nur Python

291 · Kritik · von Regelumsetzer (Prozess) → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 280 F1 mit „Nein“
beantwortet: SonarLint prüft nur Python, das Frontend prüfen ESLint und Stylelint. Der
[Ablauf](../../prozess/ablauf.md#technikphase) sagt in Werkzeuge und DoD 2 „SonarLint“ ohne diese
Grenze; „mindestens so streng wie SonarLint“ gilt für `seite.js` nicht.

**Kosten.** Ein Halbsatz. Ohne ihn liest man die Lücke als Versehen.

**Gegenvorschlag.** In Werkzeuge: „SonarLint prüft Python; das Frontend prüfen eslint und
stylelint.“ Die Zeile in `regeln.md` ist gesetzt.

**Stellungnahme.** Umgesetzt wie vorgeschlagen: [Ablauf, Werkzeuge](../../prozess/ablauf.md#technikphase) sagt "für Python mindestens so streng wie SonarLint" und "SonarLint prüft nur Python, das Frontend prüfen eslint und stylelint (Anliegen 280)". DoD 2 verweist für die Ordner schon auf `regeln.md`, bleibt also ohne Zusatz (Wir 3).
