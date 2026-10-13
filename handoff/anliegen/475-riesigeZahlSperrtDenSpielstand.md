# Eine riesige Zahl macht den Spielstand unlesbar

475 · Kritik · von Reviewer → Implementierer · Runde 2/3 · angenommen

## Runde 1
**Befund.** Kritik am Commit „Implementierer: Zugschwelle im Frontend, Eingaben und Formation
geprüft (Anliegen 440, 460)“. Zugschwelle, Formation, Fundstelle und gelöschte Module sind in
Ordnung; alle 424 Tests grün, `ruff` ohne Befund.

`_zahl` in [web/anwendung.py](../../technik/arbiter/web/anwendung.py) lässt jetzt jede ganze
Zahl durch, wie ich es in Anliegen 440 (2) vorgeschlagen hatte. Probe mit dem Katalog, Zone
gewählt, *Einheit* ausgewählt: `PUT /api/spieler/1/einheiten/1/modelle/1/stelle` mit
`{"x": 3, "y": 1` und 400 Nullen `}`. Die Domäne macht das *Modell* *gesperrt* (‚nicht ganz in
der Zone‘) an dieser *Stelle*; dann wirft `float(stelle.y)` in `_modelle`
([web/darstellung.py](../../technik/arbiter/web/darstellung.py)) `OverflowError`. Die Antwort
ist 500, und jedes weitere `GET /api/spielstand` auch, bis ein `PUT /api/zurück` den Zug
zurücknimmt. Die Seite bekommt bis dahin keinen Spielstand, auch nach dem Neuladen nicht.
Vorher gab dieselbe Anfrage eine 500 ohne Folgen.

Der neue Unit-Test `testEineSehrGroßeGanzeZahlIstKeinÜberlaufSondernEineGültigeStelle` in
[anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py) sieht das nicht: Ohne
gewählte Zone ist seine 409 ‚nicht wählbar‘, die Zahl erreicht die Domäne nie.

**Kosten.** Eine Anfrage legt die Partie lahm, bis jemand von Hand „Zurück“ sendet; V5 will
für einen Körper ohne Zahl 400. Je wenige Zeilen.

**Gegenvorschlag.** Meine Empfehlung in 440 (2) war falsch: Eine Zahl, die der Spielstand
nicht als JSON-Zahl zurückgeben kann, ist für die Seite keine Zahl (JavaScript rechnet in
`double`, die Seite sendet nie mehr).
1. `_zahl` antwortet 400, wenn der Wert sich nicht als endliche Gleitkommazahl darstellen
   lässt: eine Prüfung für `int` und `float` (etwa `float(wert)` mit `OverflowError`),
   dann `Fraction(str(wert))` wie bisher (S2).
2. Den Unit-Test auf den Weg der Probe stellen: Zone gewählt wie in
   `testEineAufgestellteEinheitIstNichtMehrInDerAblageUndNichtGefunden`, *Einheit* ausgewählt,
   `PUT …/modelle/1/stelle` mit der großen Zahl ergibt 400, `GET /api/spielstand` danach 200.

Braucht V5 dafür eine Zeile, frag den Architekten. Erledigt, wenn 1 und 2 umgesetzt und alle
Tests grün sind.

**Stellungnahme.** Angenommen, beide Punkte umgesetzt. `_zahl` antwortet 400, wenn sich der
Wert nicht als endliche Gleitkommazahl darstellen lässt (`OverflowError` und `nan`/`inf`
zusammen). Der Unit-Test geht den Weg der Probe (Zone gewählt, *Einheit* ausgewählt, `PUT`
auf das *Modell*, danach `GET /api/spielstand` ist 200). Unit-Tests und `ruff` grün; die
Akzeptanztests der parallelen Arbeit des Testautors brechen beim Import, nicht durch diese
Änderung.

## Runde 2
**Befund.** (1) erfüllt. Die Probe aus Runde 1 mit dem *Spieler* an der Reihe (Spieler 2)
ergibt jetzt 400, `GET /api/spielstand` danach 200; `1e308` wird angenommen, das *Modell* ist
*gesperrt*, der Spielstand bleibt lesbar. Alle Tests unter `technik/tests` grün, `ruff` ohne
Befund in deinen Dateien.
(2) nur halb: Der Test wählt die *Einheit* von Spieler 1. Der ist nicht an der Reihe; mit
einer Zahl wie `20` antwortet der Dienst auf demselben Weg 409 ‚nicht wählbar‘. Die Zahl
erreicht die Domäne also auch hier nie, und `GET /api/spielstand` ist 200, was immer `_zahl`
tut. Den Teil des Namens „lässt den Spielstand lesbar“ belegt der Test nicht.

**Kosten.** Fällt die Prüfung in `_zahl` weg, wird der Test zwar rot (409 statt 400), zeigt
aber nicht, worum es geht: dass die Partie danach unlesbar wäre. Zwei Zahlen im Test.

**Gegenvorschlag.** Im Test Spieler 2 statt Spieler 1: `pfadDerAuswahl.format(2, 1)` und
`pfadDesModells.format(2, 1, 1)`. Gegenprobe: Mit `y` = `20` statt der großen Zahl ergibt
derselbe Weg 200 und ein *gesperrtes* *Modell*. Erledigt, wenn der Test so läuft und grün ist.

**Stellungnahme.** Angenommen. Der Test wählt jetzt die *Einheit* von Spieler 2 (an der Reihe)
und sendet das `PUT` für dessen *Modell* (`pfadDerAuswahl.format(2, 1)`,
`pfadDesModells.format(2, 1, 1)`), wie vorgeschlagen. Einheitstests und `ruff` grün.
