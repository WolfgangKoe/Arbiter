# Abhaken misst nachgereichte Tests am Stand vor der Umsetzung

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: angenommen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Abhaken prüft jeden Test eines Items gegen den Produktstand vor der ersten
Umsetzung (Zeile Retro 9 P1 in [standregeln](../../prozess/regeln/standregeln.md),
`ersteUmsetzung` in
[standVorDerUmsetzung.py](../../prozess/pruefungen/standregeln/standVorDerUmsetzung.py),
Anliegen 12600). Das passt nicht zu Tests, die der Testautor erst nach der Umsetzung
nachreicht, weil die Umsetzung einen Fehler brachte: Vorher war der Fall richtig, also ist
der Test dort grün. So geschehen mit
`testBew17_1EineBaseHinterDerBewegungsweiteLenktDasModellNichtAb` aus Anliegen 12682:
committet in 2054c5c, an diesem Produktstand rot (in einer Kopie in `/tmp` geprüft), vor
096dfed grün. Abhaken meldete ihn als grün vor dem Code (Anliegen 12704).

**Kosten.** Je nachgereichtem Test gegen einen Fehler der Umsetzung eine Runde Testautor und
eine Nachprüfung ohne Fehler im Test. Der Ausweg „nenne die Stelle“ wirkt, kostet aber
jedes Mal diese Runde.

**Gegenvorschlag.** Die bestehende Regel Retro 9 P1 erweitern statt einer neuen: Kam ein
Test erst nach dem ersten Commit der Umsetzung hinzu, prüft Abhaken ihn gegen den
Produktstand des Commits, der ihn hinzufügte, ein uncommitteter gegen HEAD; rot dort
genügt. Mit einem Scheiter-Test in
[abhakenTest.py](../../prozess/pruefungen/standregeln/abhakenTest.py). Nicht in `/tmp`
erprobt; das übernimmt, wer es baut. Rückweg: die Zeile Retro 9 P1 wie bisher.

**Stellungnahme.** Zugestimmt, als P3 der [Retro 10](../retro.md), mit deinem Gegenvorschlag.
`angenommen`, sobald die Regel steht.
