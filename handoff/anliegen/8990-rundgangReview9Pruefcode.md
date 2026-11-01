# Rundgang Review 9: Stand langsam, Mutationslauf wartet, gleichwertig zu breit

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Vier Probleme aus dem [Rundgang Prüfcode](../review.md#rundgang-prüfcode) des
Review 9, die der Reviewer als Anliegen empfiehlt (dort Probleme 1, 5, 6 und 8, mit Zeilen):
1. Der Hook „Stand“ braucht 5,3 von 10 Sekunden: `belegungAlsText`
   ([produktstand.py](../../prozess/pruefungen/standregeln/produktstand.py)) zählt die
   Kriterien zweimal und sucht dabei jedes Mal alle Tests. Wächst das Repo, fällt der Stand aus.
5. Der parallele Mutationslauf wartet nach jedem Modul auf dessen letzten Mutanten
   ([mutation.py](../../prozess/pruefungen/mutationsregeln/mutation.py)); im gezielten Lauf
   über wenige Zeilen bleiben so die meisten Kerne leer.
6. `testMutantenLaufenParallelJeKernInEigenerKopie`
   ([mutationTest.py](../../prozess/pruefungen/mutationsregeln/mutationTest.py)) bleibt grün,
   wenn die Mutanten nacheinander laufen.
8. Ein gleichwertiger Mutant gilt für jede Zeile mit demselben Text in derselben Datei
   ([gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json)); eine neue
   Klasse mit demselben `@dataclass(…)` in `spielobjekte.py` ist ungeprüft ausgenommen.

**Kosten.** Ohne Änderung: Der Stand fällt bald aus (1), der gezielte Lauf jeder Technikphase
dauert länger als nötig (5), ein Test prüft nicht, was sein Name sagt (6, gegen
[Absicht](../../prozess/praemissen/absicht.md) 1), die Schwelle zählt einen gefangenen Mutanten
nicht (8). Änderung: je ein Zug von wenigen Zeilen mit Scheiter-Test, zusammen ein Lauf.
Bestehende Regeln, angepasst ([Ich 4](../../prozess/praemissen/ich.md)): die Mechanismen
selbst, keine neue Regel.

**Gegenvorschlag.** Wie die Empfehlungen des Reviewers:
1. Einmal zählen und je Kriterium die Etappe mitnehmen.
5. Alle Mutanten aller Module auf einmal einreichen, die Ergebnisse je Modul der Reihe nach
   abholen; 6 im selben Zug: Beginn und Ende je Testlauf mitschreiben und prüfen, dass sich
   zwei überschneiden.
8. Den Eintrag in `gleichwertig.json` an die Klasse binden, etwa mit ihrem Namen.

Die Probleme 2 bis 4 und 7 bleiben beim nächsten Eingriff in die Dateien.

**Stellungnahme.** Punkt 1 umgesetzt in Retro 9 P3: [produktstand.py](../../prozess/pruefungen/standregeln/produktstand.py)
(`belegungJeKriterium`) zählt einmal und gibt je Kriterium Etappe und Belegung zurück;
Scheiter-Test `testDerStandSuchtDieFehlendenTestsNurEinmalAuchMitEtappe` in
[standTest.py](../../prozess/pruefungen/standregeln/standTest.py). Die Punkte 5, 6 und 8 umgesetzt in Retro 9 P4:
- 5: [mutation.py](../../prozess/pruefungen/mutationsregeln/mutation.py) (`modulEinreichen`)
  reicht die Mutanten aller Module zugleich ein und holt die Ergebnisse je Modul der Reihe nach
  ab; Scheiter-Test `testDieMutantenAllerModuleLaufenZugleichNichtNachModulGetrennt` in
  [mutationTest.py](../../prozess/pruefungen/mutationsregeln/mutationTest.py).
- 6: `testMutantenLaufenParallelJeKernInEigenerKopie` schreibt Beginn und Ende je Testlauf mit
  und prüft die größte Zahl gleichzeitiger Läufe (zwei Kerne: 2, ein Kern: 1).
- 8: Jeder Eintrag in [gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json)
  nennt seinen `bereich` (Klasse oder Funktion, `bereichVon` in
  [ergebnisse.py](../../prozess/pruefungen/mutationsregeln/ergebnisse.py)); Scheiter-Tests
  `testEinGleichwertigerMutantGiltNurInSeinerFunktion` und
  `testDerBereichIstDieInnersteKlasseOderFunktionAuchAmDekorator`. Die Einträge sind auf die
  Bereiche aufgeteilt, in denen die Zeile heute steht; ein veralteter Eintrag
  (`anhaltenAnDerBewegungsweite.py`) entfiel.
Regeltext: [mutationsregeln](../../prozess/regeln/mutationsregeln.md). Status `angenommen`.
