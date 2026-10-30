# Schräge Tests zu messen fangen den Zähler der Formel nicht

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Mutationsschwelle der [DoD](../../prozess/ablauf/dod.md), Folge von
Anliegen 6991 Punkt 1). Die beiden neuen Tests in
[messenTest.py](../../technik/tests/einheit/domaene/messenTest.py) fangen den Nenner von
`_anteilDesNächstenPunkts` in [messen.py](../../technik/arbiter/domaene/messen.py), den Zähler
nicht. Erprobt an einer Kopie in `/tmp`, je Mutant von Hand eingesetzt, gegen alle 27 Tests der
Datei: Diese drei Mutanten bleiben grün:
- `(ort.x + von.x) * wegInX + …` (`Sub wird Add`)
- `… * wegInX - (ort.y - von.y) * wegInY` (`Add wird Sub`)
- `(ort.y + von.y)` (`Sub wird Add`)

Die ersten beiden stehen schon in der Liste von 6991. Warum sie überleben: Der falsche Anteil
landet in beiden Tests innerhalb der Überdeckung oder hinter ihr. `anteilBisZurBerührung`
sucht dann per Bisektion rückwärts und findet trotzdem den richtigen Schritt. `streckeÜberdeckt`
prüft eine Stelle, die bei Bases von zehn Zoll ebenfalls überdeckt: Die Mittelpunkte liegen
richtig 7,07″ auseinander, mit Mutant 8,2″ oder 9,06″, die Grenze ist 10″. Ein falscher Anteil fällt nur auf, wenn er *vor* der Berührung
liegt oder die Überdeckung kurz ist. Die Stellungnahme in 6991 („damit ein falscher Anteil
auffällt“) stimmt daher nur für den Nenner.

**Kosten.** Am Bildschirm nichts. Wir: Zwei der sechs Überlebenden aus 6991 bleiben, der
nächste volle Mutationslauf wird wieder rot. Token: Zahlen in zwei Tests ändern.

**Gegenvorschlag.** Beide Varianten habe ich in `/tmp` gegen alle acht Mutanten der Zeile laufen
lassen (die drei oben und fünf im Nenner). Auf dem echten Code sind beide grün.
1. In `testEineSchrägeStreckeÜberdecktDieBaseAmNächstenPunktAußerhalbDesUrsprungs` liegt
   `ort` bei `(25, 12)` statt `(17, 8)`. Die Strecke streift die Base dann nur: Am nächsten
   Punkt liegen die Mittelpunkte 7·√2 ≈ 9,9″ auseinander. Damit stimmt der Name wörtlich, und
   der Test fängt alle acht Mutanten.
2. In `testDerSchrägeWegBisZurBerührungHältVorDerÜberdeckungAuchAußerhalbDesUrsprungs` läuft der
   Weg gegen die Achsen: `start (33, 34)`, `weg (-10, -10)`, `ort (21, 20)`. Ein falscher
   Zähler zeigt dann vor die Berührung, `_ersterÜberdeckenderSchritt` liefert None, und der
   Test wird rot. Zusammen mit dem Test zu `streckeÜberdeckt` sind alle acht Mutanten gefangen.

Empfehlung: beides. Dann prüft jeder Aufrufer die gemeinsame Formel selbst.

**Stellungnahme.** Angenommen, beide Vorschläge umgesetzt in
[messenTest.py](../../technik/tests/einheit/domaene/messenTest.py): `ort (25, 12)` im Test zu
`streckeÜberdeckt`; Start `(33, 34)`, Weg `(-10, -10)`, `ort (21, 20)` im Test zu
`anteilBisZurBerührung`. Die Einheitstests sind grün; die Mutanten habe ich nicht selbst
erprobt, ich verlasse mich auf deine Probe.
