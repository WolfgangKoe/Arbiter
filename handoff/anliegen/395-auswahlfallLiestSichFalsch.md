# Auswahlfall liest sich falsch, AUF-5.8 im Dienst umständlich

395 · Kritik · von Architekt (Technik) → Testautor (Technik) · Runde 2/3 · erledigt

## Runde 1
**Befund.** Kritik am Code zu d5f6050,
[auswahlTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/auswahlTest.py), Lesbarkeit;
die Schnittstelle (`dienst.py`, `handgriffe.py`, V2) ist in Ordnung. Betroffen ist
`Auswahlfall` und `testAuf5_8DerDienstÄndertBeiAuswählenUndAbwählenNurDieAuswahl`, die vor
diesem Commit nie einsammelten und darum noch ungeprüft sind:
1. `Auswahlfall("Warboss", 1, auswählen)` liest sich „Warboss mit einem *gesetzten* *Modell*“.
   Die 1 zählt aber die *gesetzten* Boyz (`modelleSetzen(…, boyz, fall.gesetzteModelle)`), und
   `gesetzteModelle` klingt nach einer Sammlung, nicht nach einer Zahl. Erst die `ids`
   („warbossBeiBoyzInAufstellung…“) sagen, was gemeint ist.
2. Die sechs Zeilen und sechs `ids` sind ein Kreuzprodukt: drei Ausgangslagen mal
   auswählen/abwählen. Die Tabelle verbirgt das; dafür braucht die Datei `NamedTuple` und ein
   untypisiertes `Callable`.
3. Der Rumpf baut das Erwartete nach (`boyz if gesetzte else None`, Schleife mit
   `dict(gesetzte).get(modell)`) und prüft nur die *Modelle* von Spieler 1. Das Kriterium sagt
   „nur die Auswahl ändert sich“, also: danach wie davor. `testAuf16_4…` in
   [loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py)
   schreibt genau das mit `stellenAllerModelle` (`handgriffe.py`) und
   `einheitInAufstellungDavor`.

**Kosten.** Die Tests sind richtig, aber schwer zu lesen: Wer den Fall „Warboss, 1“ ändert,
muss den Rumpf lesen, um zu wissen, wessen *Modelle* gezählt werden (Es 9, „Code liest sich
wie Fachtext“). Spieler 2 ist ungeprüft. Ändern kostet einen kurzen Lauf, nur diese Datei.

**Gegenvorschlag.** Bestehende Regel: [Es](../../prozess/praemissen/es.md), Lesbarkeit und 9;
eine neue braucht es nicht.
1. und 2.: Zwei gestapelte Parametrierungen statt `Auswahlfall`:
   `@pytest.mark.parametrize("anfrage", [auswählen, abwählen], ids=["auswählen", "abwählen"])`
   und `@pytest.mark.parametrize(("einheitenname", "anzahlGesetzterBoyz"), [("Boyz", 0),
   ("Warboss", 1), ("Necron Warriors", 1)], ids=["boyzOhneGesetztesModell",
   "warbossBeiBoyzInAufstellung", "necronWarriorsNichtAnDerReihe"])`. Gleiche sechs Fälle,
   `NamedTuple` und `Callable` entfallen.
3.: Im Rumpf erst setzen, dann `davor = stellenAllerModelle(aufstellung)` und
   `einheitInAufstellungDavor = aufstellung.einheitInAufstellung`, danach `== davor` und
   `is einheitInAufstellungDavor`, dazu `anDerReihe is spielerEins` wie bisher.
Erledigt, wenn die sechs Fälle unter diesen Namen grün sind und `Auswahlfall` fehlt.

**Stellungnahme.** Angenommen, umgesetzt in auswahlTest.py: `Auswahlfall`, `NamedTuple` und `Callable` entfallen; zwei gestapelte Parametrierungen (`anfrage`, dann `einheitenname` mit `anzahlGesetzterBoyz`) unter den vorgeschlagenen `ids`. Der Rumpf setzt zuerst, hält `stellenAllerModelle` und `einheitInAufstellung` davor fest und prüft danach `== davor`, `is einheitInAufstellungDavor` und `anDerReihe is spielerEins`, also auch die Modelle von Spieler 2.

## Runde 2
**Befund.** Umgesetzt wie vorgeschlagen, die sechs Fälle sind grün. Mein Vorschlag bringt den
Test aber auf sieben Parameter: `ruff check` meldet PLR0913 (7 > 5) und E501,
`ruff format --check` schlägt fehl.

**Kosten.** Die Datei besteht den Linter nicht. Ändern kostet eine Fixture, nur diese Datei.

**Gegenvorschlag.** Die Ausgangslage als Fixture `einheitenname` in auswahlTest.py mit
`params` (die drei Paare und `ids` aus Runde 1): Sie setzt per `boyzSetzen` und liefert den
Namen. Der Test nimmt `dienst, aufstellungNachDerZonenwahl, spielerEins, einheitenname,
anfrage`, der Rumpf bleibt. Erledigt wie in Runde 1, dazu `ruff check` und
`ruff format --check` grün.

**Stellungnahme.** Angenommen, umgesetzt in auswahlTest.py: Die Fixture `einheitenname` (mit `params` und `ids` aus Runde 1) setzt per `boyzSetzen` und liefert den Namen; der Test nimmt nur noch `dienst, aufstellungNachDerZonenwahl, spielerEins, einheitenname, anfrage`, der Rumpf bleibt. `ruff check` und `ruff format --check` sind sauber, die ganze Datei ist grün (53 passed).
