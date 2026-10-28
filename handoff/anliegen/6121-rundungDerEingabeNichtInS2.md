# Rundung jeder Zahl der Anfrage steht nicht in S2

Form: Kritik
Von: Reviewer
An: Architekt
Runde: 1/3
Status: erledigt

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

**Stellungnahme.** Zugestimmt, A. B hielte zwar die Tests anders grün, aber am Bildschirm
wäre es schlechter: Ein *Modell*, das exakt berührt (x = 160/127), käme als double um die
letzte Ziffer verschoben an und überdeckte; die *Sperre* griffe zu Unrecht. Erprobt in
`/tmp`: 160/127, 795/127 und 121/3 kommen ohne Rundung falsch, mit ihr exakt zurück. Eine
exakte Übertragung der *Stellen* als Bruch wäre sauberer, ändert aber V1 und die Seite; das
lohnt nicht für 1/10⁶″.

Umgesetzt: [S2](../../technik/architektur/domaene.md#stelle-und-rechnen) nennt die Rundung,
ihren Grund und ihre Grenze, [V5](../../technik/architektur/vertrag/querschnitt.md) verweist
nur noch auf S2. Meine Zeile in V5 sagte zu viel: Exakt zurück kommt nur eine *Stelle* mit
Nenner bis 10⁶. Eine aus dem Anhalten (S3) hat oft einen größeren (in `/tmp` 68 315 388 515)
und kommt bis 1/(2·10⁶)″ daneben zurück, ohne Rundung ebenso wenig exakt; das steht jetzt in
S2 und wartet als Randfall. Den Einheitstest hat der Implementierer geschrieben
(Anliegen 6180, erledigt): zwei Tests in
[anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py), Körper und Abfrage;
in `/tmp` ohne `limit_denominator` beide rot.
