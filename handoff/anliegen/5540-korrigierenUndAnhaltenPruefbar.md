# Korrigieren und Anhalten am B prüfbar fassen

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: ein Test erfüllt sein Kriterium, ohne zu prüfen, was der
Stakeholder entschieden hat; Absicht 1).
1. Korrigieren: Laut [5400](5400-wieWeitEinKorrigiertesModellStehenDarf.md) F1 A zählt die
   *Distanz* ab der *Stelle* zu Beginn der *Bewegungsphase*, egal wie oft ein *Modell*
   dazwischen *gesetzt* wird. Das steht nur im [Glossar](../../domaene/glossar.md).
   [BEW-1.6](../../domaene/anforderungen/phasen/bewegung/normaleBewegung.md) und
   [BEW-3.1](../../domaene/anforderungen/phasen/bewegung/anhaltenAmB.md) verlangen keinen Zug,
   bei dem das einen Unterschied macht. Ein Test, der nur einmal zieht, ist auch grün, wenn
   Arbiter die Strecken zusammenzählt (die verworfene Antwort B).
2. „auf 1/100″ genau“ in BEW-3.1 hat zwei Lesarten: höchstens 1/100″ vor dem *B* oder
   1/100″ darum herum. Bei der zweiten darf ein *Modell* 1/100″ über seinem *B* stehen. Der
   [Vertrag](../../technik/architektur/vertrag/bewegung.md) (V16) meint die erste.

**Kosten.** Je ein halber Satz. Der Testautor schreibt einen Test mehr zu BEW-1.6 und prüft
in BEW-3.1 nur nach einer Seite. Für den Bau ist nichts neu: BEW-3 nutzt das Raster des
Anhaltens an einer *Base* (`messen.py`, S3), BEW-4 die *Kohärenz* wie das Beenden des
Aufstellens (`phasen/aufstellen/beenden.py`). Ohne Änderung kann die *Bewegungsphase* grün
sein, obwohl Korrigieren den Warboss zu früh anhält.

**Gegenvorschlag.**
1. BEW-1.6, am Ende: „…, *setzt* Arbiter es nach BEW-1.5, auch wenn seine Strecken in der
   *Bewegungsphase* zusammen länger als sein *B* sind (Anliegen 5400 F1 A).“ Beispiel für
   den Test: Warboss mit *B* 5″ erst 4″ vor, dann 2″ zur Seite; er steht dort, denn die
   *Distanz* ist rund 4,47″.
2. BEW-3.1: „…, wie keines eine *Distanz* über seinem *B* hat, und höchstens 1/100″ davor
   (…).“

Danach ziehe ich im Vertrag Bewegung die neuen Kennungen nach (BEW-1.5, 1.7, 2.5 bis 2.7,
3.1, 4.1).

**Stellungnahme.** Angenommen, beides umgesetzt; beide Kriterien hatten noch keinen Test,
die Kennungen bleiben.
1. [BEW-1.6](../../domaene/anforderungen/phasen/bewegung/normaleBewegung.md) endet jetzt
   „…, auch wenn seine Strecken in der *Bewegungsphase* zusammen länger als sein *B* sind
   (Anliegen 5180 F5, 5400 F1 A).“ Dein Warboss-Beispiel passt als Test.
2. [BEW-3.1](../../domaene/anforderungen/phasen/bewegung/anhaltenAmB.md): „…, wie keines eine
   *Distanz* über seinem *B* hat, höchstens 1/100″ davor, …“.
