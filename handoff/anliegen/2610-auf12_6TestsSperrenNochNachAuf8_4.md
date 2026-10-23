# Zwei Tests zu AUF-12.6 verlangen noch die Sperre aus AUF-8.4

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf, denn die
Tests prüfen ihr Kriterium nicht und verlangen eine *Sperre*, die es nicht mehr gibt.

Die Fälle `auf8_4…` und `testAuf8_4…` sind sauber entfernt. Die übrigen Fälle `auf7_2…`
treffen AUF-12.5 und 12.6 weiter. Entfernt wurden darüber hinaus nur Kommentare, und dabei
fiel keine Annahme eines Tests weg. Zwei Tests in
[sperreOhneStelleTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/sperreOhneStelleTest.py)
bauen ihre *Sperre* aber weiter über AUF-8.4: `einAufgestelltesModellAufDieEigeneAblageZiehen`
zieht ein *Modell* der *aufgestellten* Boyz auf die *Armeeliste* von „Spieler 1“ und wartet
auf ‚nicht wählbar‘.
- `testAuf12_6DieSeiteNenntDenGrundNochNachDemAuswählen`
- `testAuf12_6DieSeiteNenntDenGrundNichtMehrNachDerNächstenHandlung`

[AUF-12.6](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md) setzt „eine
*Sperre* nach AUF-12.5“ voraus, und AUF-12.5 nennt nur noch AUF-7.2. Für genau dieses
Loslassen verlangt [AUF-16.8](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md)
jetzt das Gegenteil: Das *Modell* springt still zurück, Arbiter nennt keinen *Grund*
(2220 F4 A, 2410). Heute sind beide Tests grün (498 bestanden). Entfernt der Implementierer
in diesem Item die *Sperre* aus AUF-8.4, wie [Plan 7](../plan.md) es verlangt, werden sie
rot. Bleiben sie, zwingen sie ihn, die *Sperre* zu behalten.

**Kosten.** Bleibt es so, kann das Item nicht fertig werden: entweder rote Tests oder eine
*Sperre* gegen AUF-16.8. Die Änderung ist klein, nur der Aufbau zweier Tests, und die
Annahmen bleiben.

**Gegenvorschlag.** Die *Sperre* in beiden Tests nach AUF-7.2 auf der *Karte* bauen statt
auf der *Armeeliste*: Das *Modell* der *aufgestellten* Boyz an eine freie *Stelle* der Zone
von „Spieler 1“ ziehen, wie es der Fall `auf7_2ModellEinerAufgestelltenEinheit` tut
(`freieStelleDesSpielersAnDerReihe`), und auf ‚nicht wählbar‘ warten. Klick auf den Warboss
und Zug des Warboss bleiben. Danach braucht kein Fall mehr den Zweig `ablage` in `Loslassen`,
`inDerDomäneLoslassen`, `imDienstLoslassen` und `amBildschirmLoslassen`, ebenso wenig den
Helfer `modellAufAblageLoslassen` in `dienst.py`, der nur hier verwendet wird. Ob sie
entfallen, entscheidest du mit dem Architekten. `modellAufDieAblageZiehen` braucht QUE-3.4
weiter (`bedienungTest.py`).
Erledigt, wenn kein Akzeptanztest mehr ‚nicht wählbar‘ beim Loslassen auf einer
*Armeeliste* verlangt.

**Stellungnahme.**
Angenommen. Beide Tests ziehen jetzt ein *Modell* der *aufgestellten* Boyz auf eine freie
*Stelle* der Zone auf der *Karte* (AUF-7.2). Der Zweig `ablage` in `Loslassen` und seinen drei
Helfern ist entfernt, ebenso `modellAufAblageLoslassen` in `dienst.py`;
`modellAufDieAblageZiehen` bleibt für QUE-3.4. Kein Akzeptanztest verlangt mehr ‚nicht
wählbar‘ beim Loslassen auf einer *Armeeliste*. Die Tests von `sperreOhneStelleTest.py` und
`bedienungTest.py` sind grün (29).
