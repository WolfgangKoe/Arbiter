# Länge eines Anliegens: Grenze nach Runde, Hinweis davor

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Dein Wortlaut: „Ein oberes Limit ist gut. Lass es 4000 sein. Aber es wäre mir
recht, wenn wir hier eine Zone hätten, die zuverlässig z.B. bei 3.900 liegt und erst bei 4000
eine Kürzung einfordert. Ich stelle mir so eine Mechanik wie bei den Kontextfenstern vor.“
Und: „wir könnten die Länge proportional zur Rundenzahl erhöhen.“ Anlass: Anliegen 6470 lag
unbemerkt über 4.000 Zeichen.

Entschieden und umgesetzt: Grenze = 4.000 Zeichen × Runde (`Runde: n/3`: 4.000 / 8.000 /
12.000); ab 100 Zeichen darunter (3.900 / 7.900 / 11.900) ein Hinweis; darüber ist die
Anliegenprüfung rot, im Hinweisbereich nicht. `Antwort:`-Zeilen zählen als `Antwort: .`.
Bestehende Regel: [Anliegen](../../prozess/ablauf/anliegen.md) („höchstens 4.000 Zeichen“,
nur Text), erweitert. Mechanismus: `anliegenregeln/anliegenLaenge.py`, rot über
`anliegenLaengeTest.py` (alle Anliegen).

**Kosten.** Am Bildschirm: nichts. Code: ein Modul, ein Test. Längere Anliegen in Runde 2 und
3 kosten die lesende Rolle Token (bis das Dreifache).

**Gegenvorschlag.** Wo erscheint der Hinweis? Das Skript `anliegenLaenge.py` liefert ihn schon
als Hook-Rückmeldung (an einer Kopie in /tmp mit Eingabe von Write erprobt: es antwortet
`additionalContext` „… hat 3950 von 4000 Zeichen … bald kürzen“, bei kurzen Anliegen
schweigt es). Verdrahtet ist es noch nicht.

**F1 · Wo erscheint der Hinweis?**
A: Direkt nach Write und Edit auf ein Anliegen, als Rückmeldung an die schreibende Rolle
(neu). Arbeit: Eine Zeile PostToolUse in `.claude/settings.json` (Matcher `Write|Edit`,
`anliegenregeln.anliegenLaenge`); der Verfasser kürzt sofort. Rückweg: die Zeile streichen.
B: Erst beim Commit, im pre-commit (neu). Arbeit: Hinweis erscheint spät, wenn der Verfasser
nicht mehr schreibt; er wird übersehen.
Empfehlung: A. Der Verfasser sieht es in dem Moment, in dem er kürzen kann.
Antwort: .

**Annahme:** A. Der Ablauf wartet nicht darauf. Zwei Dinge liegen außerhalb meiner
Schreibpfade und brauchen den, der sie darf: die Hook-Zeile in `.claude/settings.json` und
der Satz „höchstens 4.000 Zeichen je Runde, Hinweis ab 100 darunter“ in
[Anliegen](../../prozess/ablauf/anliegen.md) (Organisationsentwickler).

**Stellungnahme.**
