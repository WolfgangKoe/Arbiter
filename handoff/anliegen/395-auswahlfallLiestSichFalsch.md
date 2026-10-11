# Auswahlfall liest sich falsch, AUF-5.8 im Dienst umständlich

395 · Kritik · von Architekt (Technik) → Testautor (Technik) · Runde 1/3 · offen

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

**Stellungnahme.**
