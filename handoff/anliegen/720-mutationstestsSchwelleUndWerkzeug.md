# Mutationstests: Schwelle, Laufzeit und eigenes Werkzeug statt Paket

720 · Fragen · von Regelumsetzer → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** P3 ist gebaut ([Regeln](../../prozess/regeln.md#mutationsregeln)): Das Werkzeug
baut je einen Fehler in geänderte Domänenmodule und nennt die Lücken. Es nutzt nur die
Standardbibliothek (`ast`), kein neues Paket. Erster Lauf über `messen.py` und
`querschnitt/kohaerenz.py`: 52 Mutanten, 98 % gefangen. Die eine Lücke:
`kohaerenz.py:29`, `<=` statt `<` bei der Grenze der größten Einheit mit einem Partner
bemerkt kein Test (Fall an der Grenze fehlt; sie geht an den Testautor). Ein Lauf kostete
gut 9 Minuten, weil jeder Mutant die Akzeptanztests im Browser startet.

**Kosten.** Ohne Schwelle sperrt das Werkzeug nie (heute 0 %). Ein fertiges Paket (mutmut,
cosmic-ray) fände mehr Mutanten und kennt Zwischenspeicher, brächte aber eine
Abhängigkeit, die der Stakeholder entscheidet.

**Gegenvorschlag.**
**F1 · Schwelle.** Mindestens 95 % gefangene Mutanten je Lauf, rot darunter; beim ersten
Lauf lag der Wert bei 98 %. Empfehlung: 95 %.
Antwort: .

**F2 · Werkzeug.** Das eigene Werkzeug behalten, statt mutmut ins Projekt zu nehmen.
Empfehlung: behalten, bis eine Operatorart fehlt; zuerst genügt es.
Antwort: .

**F3 · Zeitpunkt.** Der Lauf dauert Minuten und gehört nicht zum Commit. Empfehlung: einmal
je Item vor dem Review, Lücken an den Testautor.
Antwort: .

**Stellungnahme.**
Schwelle 95 % steht in `mutationsregeln/mutation.py` mit Scheiter-Test; eigenes Werkzeug bleibt; Lauf je Item vor dem Review ([Regeln](../../prozess/regeln.md#mutationsregeln)).
