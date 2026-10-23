# AUF-23.3: Der Name des Dienst-Tests lässt die Ebene offen

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund (wartet auf die nächste Technikphase).** Keine Prüfung ist rot, das Kriterium ist
geprüft ([Ich 3](../../prozess/praemissen/ich.md): Namen). In
[einheitZuruecklegenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/einheitZuruecklegenTest.py)
heißt der Test
`testAuf23_3DerDienstLässtNachDemZurücklegenDieEinheitMitEinemModellAlsEbeneAusgewählt`.
Man kann ihn lesen als „nach dem Zurücklegen ist ein Modell die Ebene“. AUF-23.3 verlangt
das Gegenteil: Nach dem Zurücklegen ist die ganze Einheit die Ebene. Gemeint ist der
Ausgangszustand, also ein Modell als Ebene *vor* dem Zurücklegen.

**Kosten.** Wer nur die Testliste liest, etwa im Bericht von pytest, versteht das Kriterium
falsch und muss erst den Rumpf lesen.

**Gegenvorschlag.** Der Name nennt Ausgangszustand und Ergebnis, etwa
`testAuf23_3MitEinemModellAlsEbeneLässtDerDienstDieEinheitMitDerGanzenEinheitAlsEbeneAusgewählt`.

**Stellungnahme.** Angenommen, der Name ist der Vorschlag:
`testAuf23_3MitEinemModellAlsEbeneLässtDerDienstDieEinheitMitDerGanzenEinheitAlsEbeneAusgewählt`.
