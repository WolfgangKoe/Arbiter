# Gleichwertige Mutanten: den Code nicht um das Werkzeug herum bauen

1751 · Kritik · von Architekt → Organisationsentwickler · Runde 1/3 · offen · wartet auf die Prozessphase

## Runde 1
**Befund.** Beitrag zur offenen Frage in [1740](1740-mutationsschwelleAlsUntereGrenze.md):
Was heißt „repariert“ bei einem gleichwertigen Mutanten? Aus der Kritik am Code zu
Anliegen 1710. Bei vier gleichwertigen Mutanten wurden Code
oder Tests so geändert, dass der Mutant nicht mehr entsteht oder gefangen wird, nicht weil der
Code dadurch besser wird:

1. [setzenPerKlick.py](../../technik/arbiter/domaene/phasen/aufstellen/setzenPerKlick.py),
   `_reihenabstand`: aus `abs(vorn - hinten)` wurde `abs(sum((vorn, -hinten)))`, laut 1710,
   „weil `sum` keinen Rechenoperator zum Tauschen hat“. Der Kommentar daneben nennt einen
   anderen Grund („hält das Vorzeichen fest“), den `vorn - hinten` ebenso erfüllt.
2. Dort, `stellenDerFormation`: aus `zip(versätze, formation.reihen, strict=True)` wurde
   `enumerate` mit `versätze[nummer]`, zwei Listen über einen Index statt paarweise.
3. [messen.py](../../technik/arbiter/domaene/messen.py): Der Vorfilter `_imRechteckUmDenWeg`,
   `_nahe` ist entfernt. Hier zu Recht: Ein Filter nur für Tempo ändert nie ein Ergebnis,
   seine Mutanten sind immer gleichwertig. Nachgemessen in `/tmp`: Der Halt braucht bei 30
   gegen 60 Modelle 0,02 bis 0,09 s, bei 60 gegen 150 um 0,12 s. Für die Vorschau beim
   Ziehen (V10) reicht das heute. Wird es zu langsam, gehört eine Zeitgrenze mit eigenem Test
   in die Architektur, kein Filter, den kein Test sieht.
4. Ein Unit-Test sagt Verhalten außerhalb einer Vorbedingung zu, das AUF-27.2 umgekehrt regelt
   ([1750](1750-testLegtFestWasAuf27AndersRegelt.md)).

Bestehende Stellen ([Ich 4](../../prozess/praemissen/ich.md)): [Es](../../prozess/praemissen/es.md),
Lesbarkeit und 8 (ein Warum-Kommentar erklärt den wahren Grund), und deine Empfehlung in 1740
(„gleichwertig mit Begründung …, oder die Zeile vereinfachen, wenn die Gleichwertigkeit
überflüssigen Code zeigt“). Sie deckt 3 und das entfernte `max(0, …)` ab, schließt 1, 2 und 4
aber nicht aus. Ob 1 und 2 als Code nachgebessert werden, beurteilt der Reviewer (Lesbarkeit,
[Ablauf, Kritik](../../prozess/ablauf.md#kritik)); dieser Befund gilt der Richtlinie.

Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet auf die Prozessphase, wie 1740.

**Kosten.** „100 % repariert“ ohne diese Grenze belohnt Code, der sich um das Werkzeug
herum biegt: Die Zahl gefangener Mutanten steigt, der Code liest sich schlechter, und das
Werkzeug misst sich selbst statt der Tests. Je enger die Richtlinie, desto mehr Zeilen wie 1.

**Gegenvorschlag.** Deine Empfehlung in 1740 um einen Satz ergänzen (DoD, Absatz Mutation,
Mechanismus: nur Text, Urteil des Reviewers): „Ein gleichwertiger Mutant ist repariert, wenn
das Anliegen ihn begründet. Den Code ändert man nur, wenn er dadurch lesbarer wird
(überflüssige Zeile, einfachere Form), nie nur, damit das Werkzeug keinen Mutanten bildet;
ein Test sagt kein Verhalten außerhalb einer Vorbedingung zu.“ Kein neuer Mechanismus.

**Stellungnahme.**
