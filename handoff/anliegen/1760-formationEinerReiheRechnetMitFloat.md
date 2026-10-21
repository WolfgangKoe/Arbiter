# Eine Formation aus einer Reihe rechnet mit float

1760 · Kritik · von Reviewer → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code (Lesbarkeit) zu [1710](1710-unitTestsFuerZweiMutantenAusPlan6.md),
[setzenPerKlick.py](../../technik/arbiter/domaene/phasen/aufstellen/setzenPerKlick.py):
1. `_versätzeDerReihen`, `initial=-sum(abstände) / 2`: Bei einer Reihe ist `abstände` leer,
   `sum([])` die ganze Zahl 0 und `0 / 2` das float `0.0`. Jede *Stelle* der *Formation* ist dann
   float: `Fraction + float` ergibt float. Das trifft Warboss und Overlord (Reihen `[1]` in
   `domaene/daten/formation.yaml`), also Schritt 6 des Happy Path. Nachgestellt:
   `stellenDerFormation` mit Reihen `(2,)` gibt `x` als `float 20.0`, mit `(2, 1)` als `Fraction`.
   Das verletzt [Architektur, S2](../../technik/architektur.md) („Gerechnet wird exakt mit
   `Fraction`“). Mit Rändern, die keine ganzen Zoll sind (Zone ab `n + 1/10`), liegt die
   gerückte *Base* danach in 50 von 80 Fällen nach `ganzIn` nicht ganz in der Fläche. Kein Test
   merkt es: `testEineFormationStelltEineReiheMittigBaseAnBaseAuf` vergleicht mit
   `Fraction(20)`, und `Fraction(20) == 20.0` ist wahr.
2. `_reihenabstand`, `abs(sum((vorn, -hinten)))`: Steht nur da, damit das Werkzeug keinen
   Mutanten „Sub wird Add“ bildet ([1710](1710-unitTestsFuerZweiMutantenAusPlan6.md), Punkt
   14 und 15). Fachlich ist das `abs(vorn - hinten)`. Der Kommentar nennt einen anderen Grund
   („hält das Vorzeichen fest“), den `vorn - hinten` genauso erfüllt; nach
   [Es](../../prozess/praemissen/es.md) 8 erklärt ein `Warum` den wahren Grund.
3. `stellenDerFormation`, `versätze[nummer]` mit `enumerate`: Zwei Listen über einen Index statt
   paarweise ([Es](../../prozess/praemissen/es.md) 6: benennen oder entpacken). Vorher stand
   `zip(versätze, formation.reihen, strict=True)` da.

Allgemein zu 2 und 3: [1751](1751-gleichwertigeMutantenNichtUmDasWerkzeugBauen.md) (Architekt).

Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf. 1 verletzt die Architektur
(S2), 2 und 3 die Lesbarkeit, alles in neuem Code.

**Kosten.** Bei 1 rechnet jeder Klick mit einer Einheit aus einer Reihe ungenau weiter, bis
zum Anhalten und zum *Setzen*, an Rändern, die keine ganzen Zoll sind, auch mit einer *Sperre*
zu Unrecht. 2 und 3 kosten jeden Leser einen zweiten Blick und einen falschen Grund. Die
Abhilfe sind drei Zeilen und ein Test.

**Gegenvorschlag.**
1. `initial=-sum(abstände, Fraction(0)) / 2`. Dazu ein Unit-Test, den float nicht besteht:
   eine Reihe um `mitte` mit `x=Fraction(1, 3)`. Dann ist `Fraction(1, 3) == 1/3` falsch.
2. `abs(vorn - hinten)` ohne Kommentar. Der Mutant „vorn + hinten“ ist gleichwertig, der
   Grund steht in [1632](1632-mutationslaufUnterDerSchwelle.md).
3. `for versatz, anzahl in zip(versätze, formation.reihen, strict=True)`. Der Mutant
   `strict=False` ist gleichwertig: `_versätzeDerReihen` gibt für jede Reihe genau einen
   Versatz zurück.

Erledigt: drei Zeilen wie oben, der neue Test grün, `technik/tests` und ruff grün.

**Stellungnahme.** Angenommen, alle drei Punkte, wie vorgeschlagen umgesetzt in
[setzenPerKlick.py](../../technik/arbiter/domaene/phasen/aufstellen/setzenPerKlick.py):
1. `sum(abstände, Fraction(0))`; neuer Unit-Test `testEineFormationAusEinerReiheRechnetExaktMitBruchzahlen`
   (`mitte.x = 1/3`, Reihe `(2,)`), den float nicht besteht (`Fraction(1, 3) + 0.0 == Fraction(1, 3)` ist falsch).
2. `abs(vorn - hinten)`, der Kommentar entfällt. Der Mutant „vorn + hinten“ ist gleichwertig (Grund in 1632).
3. `zip(versätze, formation.reihen, strict=True)`. Der Mutant `strict=False` ist gleichwertig: Es gibt je Reihe genau einen Versatz.
`technik/tests` (744) und ruff grün. Kein voller Mutationslauf, nach Vorgabe des Stakeholders.

Status: umgesetzt, wartet auf die Nachprüfung des Reviewers.
Nachprüfung: Der neue Test fängt die alte Zeile; 17 Mutanten gezielt, 15 gefangen, 2 gleichwertig (2, 3).
