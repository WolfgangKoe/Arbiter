# Akzeptanztests nach dem Aufräumen: Doppeltes und ein Helfer mit einem Aufrufer

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund (wartet auf die Technikphase).** Bei der Nachprüfung von 2572 und 2573 fiel auf,
was kein Kriterium betrifft und keine Prüfung rot macht:

1. [ziehen.py](../../technik/tests/akzeptanz/ziehen.py), `aufDieAntwortenWarten`: Der
   Docstring nennt „vier ruhige Proben zu 50 ms“; dieselben Zahlen stehen darüber als
   `_ruhigeProben` und `_pausenInMillisekunden` ([Wir 3](../../prozess/praemissen/wir.md)).
   Ändert jemand eine Konstante, stimmt der Docstring nicht mehr.
2. Ebenda: `_ziehenBisZurAntwort` hat nach dem Löschen von `modellAufDieAblageZiehen` nur noch
   einen Aufrufer, `modellZiehen`.
3. [sperreOhneStelleTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/sperreOhneStelleTest.py):
   `einModellDesSpielersNichtAnDerReihe` und `einModellEinerAufgestelltenEinheit` haben
   denselben Rumpf; nur die *Einheit* aus der Fixture unterscheidet die Fälle, und das sagen
   schon die `ids`.
4. [bedienungTest.py](../../technik/tests/akzeptanz/querschnitt/bedienungTest.py),
   `testQue3_4EinModellAufDieArmeeliste…`: Nach `assert anfragen == []` können die beiden
   Prüfungen der *Stellen* in der Domäne nicht mehr fehlschlagen, denn ohne Anfrage ändert
   die Seite dort nichts. „Lässt jedes Modell, wo es war“ zeigte nur die *Karte*. Ob der
   Test sein Kriterium so prüft, entscheidet der Fachkritiker; hier geht es nur darum, dass
   die Prüfung mehr verspricht, als sie belegt.

**Kosten.** 1 kann auseinanderlaufen. 2 und 3 sind je eine Funktion, die man liest und
vergleicht, ohne dass sie etwas Eigenes trägt. 4 lässt den Leser glauben, die Rückkehr sei
geprüft.

**Gegenvorschlag.**
1. Docstring ohne Zahlen: „Wartet, bis die Abfragen eine Weile ruhen; erst dann zeigt die
   Karte den Stand zum Zeigerpunkt.“
2. `_ziehenBisZurAntwort` in `modellZiehen` aufgehen lassen.
3. Eine Funktion, etwa `einModellAnEinerFreienStelle`, für beide Fälle; die `ids` bleiben.
4. Statt der beiden Prüfungen in der Domäne prüfen, dass die *Karte* das gezogene *Modell*
   wieder an `stelleDavor` zeigt (`kreiseDerKarte`), oder sie streichen und den Namen auf
   „…SendetNichts“ kürzen.

Erledigt, wenn 1 bis 3 umgesetzt sind und 4 entweder die *Karte* prüft oder der Name nur
verspricht, was geprüft wird.

**Stellungnahme.** Angenommen, alle vier umgesetzt. 1: Der Docstring von
`aufDieAntwortenWarten` nennt keine Zahlen mehr. 2: `_ziehenBisZurAntwort` ist in
`modellZiehen` aufgegangen. 3: `einModellAnEinerFreienStelle` ersetzt beide Aufbauten; die
Fixture `sperrendesLoslassen` hat nur noch die Einheitennamen als Parameter, die `ids`
bleiben. 4: Der Test prüft jetzt die *Karte* (`kreiseDerKarte` zeigt beide *Modelle* an
ihren *Stellen*); der Name bleibt, denn er verspricht nur das.
