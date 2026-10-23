# AUF-23: Ein Hilfsname wie eine Methode der Domäne, Knopftexte dreifach

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen

## Runde 1
**Befund (wartet auf die nächste Technikphase).** Keine Prüfung ist rot, kein Kriterium
betroffen ([Ich 3](../../prozess/praemissen/ich.md)). In
[einheitZuruecklegenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/einheitZuruecklegenTest.py):

1. Die Vorgeschichte `ganzeEinheitAlsEbene(aufstellung, einheit, _modell)` heißt wie die
   Methode `Aufstellung.ganzeEinheitAlsEbene(einheit)` aus
   [V3](../../technik/architektur/vertrag.md), ruft aber nur `auswählen`. Wer
   `testAuf23_3…[ganzeEinheit]` liest, hält die Methode für aufgerufen; dabei ist sie genau
   das, was AUF-23.3 von `zurücklegen` erwartet.
2. Die drei Vorgeschichten von `mitJederEbene` nehmen dieselben Parameter, aber nur
   `ganzeEinheitAlsEbene` kennzeichnet den ungenutzten als `_modell`, `ohneAuswahl` nicht.
3. Der Text „Aufstellen der Einheit beenden“ steht in dieser Datei als `beendenKnopf`, in
   [sperreOhneStelleTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/sperreOhneStelleTest.py)
   als `beenden` und in [beendenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/beendenTest.py)
   zweimal wörtlich ([Wir 3](../../prozess/praemissen/wir.md)).

**Kosten.** 1 führt beim Lesen in die Irre, 2 kostet einen zweiten Blick. 3: Ändert der
Stakeholder den Text, muss man ihn an vier Stellen finden.

**Gegenvorschlag.**
1. `ausgewählt` (oder `ausgewähltMitDerEinheitAlsEbene`) statt `ganzeEinheitAlsEbene`;
   die `ids` bleiben.
2. Einheitlich `_modell` in beiden, wo der Parameter ungenutzt ist.
3. Die Knopftexte einmal in [bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py)
   neben `knopfDerSeite`, etwa `beendenKnopf` und `zurücklegenKnopf`, und von dort importieren.

**Stellungnahme.**
