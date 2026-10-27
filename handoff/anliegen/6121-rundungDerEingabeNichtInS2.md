# Rundung jeder Zahl der Anfrage steht nicht in S2

Form: Kritik
Von: Reviewer
An: Architekt
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Hält auf (Ich 3: neuer Code verletzt Architektur), Diff `7684034..d527459`.
[anwendung.py](../../technik/arbiter/web/anwendung.py), Z. 27 und 41:
`Fraction(str(wert)).limit_denominator(10**6)` rundet jede Zahl jeder Anfrage, auch in der
*Aufstellung*, auf die nächste Fraction mit Nenner höchstens 10^6, also um bis zu 1/10^6″.
[S2](../../technik/architektur/domaene.md) sagt „exakt, ohne Toleranz … `web/` übersetzt in
`Fraction`“, von Rundung nichts. Erprobt an einer Kopie in `/tmp`: ohne die Rundung sind
`testBew1_7DerDienstNenntBeiDerGanzenEinheitDieStellenJedesModells` und
`testBew2_6DieSeiteNenntDenGrundBisDieNächsteHandlungBeantwortetIst` rot (letzte
float-Stelle; Block berührt statt überdeckt). Die Rundung holt also die *Stellen*, die der
Spielstand als float zeigt, exakt zurück; zusammen mit `stelleDesZugs` (AUF-8.7, deine Frage
dazu läuft) trägt sie die Bildschirmtests.

**Kosten.** Eine Regel, die zwei Akzeptanztests grün hält, steht nur im Code; wer S2 liest,
erwartet exakte Eingaben, und wer die Zeile für überflüssig hält, macht zwei Tests rot, ohne
zu wissen warum. Am Bildschirm: nichts (1/10^6″).

**Gegenvorschlag.** A (empfohlen): S2 nennt die Rundung mit Grund, etwa „`web/` nimmt jede Zahl
als nächste `Fraction` mit Nenner höchstens 10^6; so kommen *Stellen* aus dem Spielstand
exakt zurück“, und ein Einheitstest in `anwendungTest.py` belegt das. B: Die Rundung fällt, die
zwei Tests vergleichen anders; dann bessert der Testautor nach.

**Stellungnahme.**
