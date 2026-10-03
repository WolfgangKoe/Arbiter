# AUF-1.3: Welche Wahl meint der Testname?

84 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · angenommen

## Runde 1
Gegenstand: 34516f1, `technik/tests/akzeptanz/phasen/aufstellenTest.py`. Schnittstelle in
Ordnung: Der neue Test nutzt nur `gewinnerWählen` und `anDerReihe`, wie seine Nachbarn.

**Befund.** AUF-1.3 kennt zwei Wahlen: erst den *Gewinner*, dann die *Aufstellungszone*
(AUF-1.2). Die drei Tests zu AUF-1.3 lesen sich jetzt so:
- `testAuf1_3VorDerWahlIstKeinerAnDerReihe`
- `testAuf1_3SolangeDieAufstellungszoneOffenIstIstKeinerAnDerReihe`
- `testAuf1_3NachDerWahlIstAnDerReiheWerNichtGewinnerIst`

„Vor der Wahl“ und „nach der Wahl“ sagen nicht, welche; „offen“ steht weder im Kriterium noch
im Glossar, und „IstIst“ stolpert. Wer die Liste der Testnamen liest (Spur-Befehl,
pytest-Ausgabe), muss den Rumpf lesen, um den Fall zu verstehen (`prozess/praemissen/wir.md`:
„der Name trägt die Bedeutung“).

**Kosten.** Gering, zwei Umbenennungen. Ohne sie wirkt der erste und der zweite Test wie
derselbe Fall, und ein Leser hält einen für überflüssig.

**Gegenvorschlag.** Die Wörter des Kriteriums („Bis zur Wahl der *Aufstellungszone*“):
- `testAuf1_3VorDerWahlDesGewinnersIstKeinerAnDerReihe`
- `testAuf1_3NachDerWahlDesGewinnersIstNochKeinerAnDerReihe`
- `testAuf1_3NachDerWahlDerAufstellungszoneIstAnDerReiheWerNichtGewinnerIst`

Die Hilfsfunktion `nachDerWahl` entsprechend `nachDerWahlDerAufstellungszone`.
Erledigt, wenn die drei Namen sagen, welche Wahl gemeint ist. Verhalten unverändert. Blockiert
nichts; der Test ist grün.

**Stellungnahme.**
Angenommen. Die drei Namen tragen jetzt die Wörter des Kriteriums wie vorgeschlagen, die
Hilfsfunktion heißt `nachDerWahlDerAufstellungszone`. Verhalten unverändert, 42 Akzeptanztests
grün.
