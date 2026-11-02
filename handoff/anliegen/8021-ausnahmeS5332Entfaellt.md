# Ausnahme von S5332 entfällt

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Folge aus Anliegen 8020, Punkt 2: Schreibt
[server.py](../../technik/arbiter/web/server.py) die Adresse `127.0.0.1` in den Text der URL,
meldet SonarLint `python:S5332` nicht mehr (erprobt in `/tmp`, siehe 8020). Dann ist die
Ausnahme `(f"{webOrdner}/server.py", "python:S5332")` in
[sonarlint.py](../../prozess/pruefungen/formregeln/sonarlint.py) überflüssig; nach
[Formregeln](../../prozess/regeln/formregeln.md) („Ausgenommen genau zwei Funde“) soll es nur
Ausnahmen geben, die nötig sind.

**Kosten.** Bleibt sie, deckt sie still eine spätere echte Klartext-URL in `server.py` zu, etwa
zu einem anderen Gerät, die W5 ausschließt. Token: gering.

**Gegenvorschlag.** Nach 8020: den Eintrag aus `ausnahmen` streichen; in
[formregeln.md](../../prozess/regeln/formregeln.md) „genau zwei Funde“ auf den einen von
`python:S4502` in `anwendung.py` kürzen und W5 dort nicht mehr nennen. Der Test „Ausnahme gilt
nur für ihre Datei“ in `sonarlintTest.py` setzt `ausnahmen` per `monkeypatch` und bleibt.
Prüfen: `python3 prozess/pruefungen/gemeinsam/lauf.py formregeln.sonarlint` grün.

**Stellungnahme.** Umgesetzt: Eintrag für `server.py` aus `ausnahmen` in
[sonarlint.py](../../prozess/pruefungen/formregeln/sonarlint.py) gestrichen;
[formregeln.md](../../prozess/regeln/formregeln.md) nennt nur noch den Fund `python:S4502`.
Scheiter-Test `testDerServerBrauchtKeineAusnahmeVonS5332` in `sonarlintTest.py`.
