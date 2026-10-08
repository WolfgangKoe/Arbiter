# Tests zu entfallenen Kriterien der Aufstellung

310 · Kritik · von Anforderungsautor (Domäne) → Testautor (Technik) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Nach [309](309-sperreDerWahlUndNeustart.md) F1 B wählt ein Klick in der *Ablage*
nur aus; *Einheit in Aufstellung* wird eine *Einheit* mit ihrem ersten *gesetzten* *Modell*.
Darum entfallen AUF-1.4, AUF-1.5, AUF-1.6 und AUF-3.6; an ihre Stelle treten AUF-1.8 bis
AUF-1.11 und AUF-3.8, und AUF-5.1, AUF-5.2 (noch ohne Test) sind durch AUF-5.3 bis AUF-5.9
ersetzt ([aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md)). Die Tests
`testAuf1_4…`, `testAuf1_5…`, `testAuf1_6…` in
`technik/tests/akzeptanz/phasen/aufstellen/auf1Test.py` und `testAuf3_6…` in
`technik/tests/akzeptanz/phasen/aufstellen/auf3Test.py` haben damit kein Kriterium mehr.

**Kosten.** `testDasRepoHältDieRückverfolgung` in `prozess/pruefungen` ist rot, bis die Tests
ersetzt sind.

**Gegenvorschlag.** Die vier Gruppen durch Tests zu AUF-1.8 bis AUF-1.11 und AUF-3.8 ersetzen.
Was früher ‚nicht in Aufstellung‘ beim *Setzen* war, ist jetzt ‚nicht wählbar‘ (AUF-1.9),
‚Einheit begonnen‘ (AUF-1.10) oder erlaubt und macht die *Einheit* zur *Einheit in
Aufstellung* (AUF-1.8); ‚nicht in Aufstellung‘ bleibt nur beim *Aufstellen der Einheit
beenden* (AUF-1.11).

**Stellungnahme.** Angenommen und umgesetzt: In `auf1Test.py` ersetzen Tests zu AUF-1.8
bis AUF-1.11 die alten zu AUF-1.4 bis AUF-1.6, in `auf3Test.py` Tests zu AUF-3.8 die zu
AUF-3.6. Die Handgriffe und Fixtures setzen kein `einheitInAufstellungWählen` mehr voraus; die
Fixture `einheitInAufstellung` heißt `ersteEinheitAnDerReihe`, weil noch kein *Modell*
*gesetzt* ist. Die Tests sind rot, weil `modellSetzen` die *Einheit* noch nicht selbst zur
*Einheit in Aufstellung* macht. Offen, nicht Teil dieses Anliegens: Die Tests zu AUF-4.5 in
`auf4Test.py` rufen noch `einheitInAufstellungWählen` auf und brauchen eine Anpassung, sobald
der Architekt die Schnittstelle der Aufstellung nach 309 festlegt.
