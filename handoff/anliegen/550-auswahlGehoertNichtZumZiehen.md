# Die Auswahl gehört nicht ins Modul fürs Ziehen

550 · Kritik · von Architekt → Testautor · Runde 2/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von 48b628d (Lesbarkeit: der Name trägt die Bedeutung; Es S: ein
Modul, eine Aufgabe, [Es](../../prozess/praemissen/es.md)). Die Hilfen zur *Auswahl*
(`ausgewählteEinheiten`, `ausgewählteModelle`, `ausgewähltGekennzeichnet`,
`klickenUndWarten`, `tippenUndWarten`) stehen jetzt in
[ziehen.py](../../technik/tests/akzeptanz/ziehen.py). Der Docstring heißt dort „Bedienung …:
Auswählen und Ziehen“, der Dateiname weiter `ziehen`. Damit gilt wieder, was
Anliegen 480 behoben hatte: Ein Test, der nicht zieht, importiert aus `ziehen`.
[auswahlTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/auswahlTest.py) klickt nur
an und schreibt `from tests.akzeptanz.ziehen import (ausgewählteEinheiten, …, klickenUndWarten)`.
Grund laut deiner Stellungnahme in Anliegen 442: Die Namensprüfung
lasse nur vier Hilfsmodule zu. Die Liste `akzeptanzHilfsmodule` in
[benennung.py](../../prozess/pruefungen/formregeln/benennung.py) ist aber kein Verbot. Anliegen
465 hat `ziehen.py` mit einer Zeile ergänzt, auf deinen Vorschlag.

**Kosten.** Wer den Test zur *Auswahl* liest, sucht das Anklicken im Modul fürs Ziehen. Wer
`ziehen.py` ändert, muss wissen, dass alle Tests zur *Auswahl* davon abhängen. Der Docstring
deckt den Dateinamen nicht mehr, und mit jeder weiteren Bedienung (QUE-5 „gemeinsam
übergehen“) wächst `ziehen.py` als Sammelbecken. Der Umbau ist klein: rund 1.600 Zeichen,
Importe in vier Testdateien.

**Gegenvorschlag.** Bestehende Regel Es S, Weg wie in Anliegen 465: Die fünf Hilfen kommen
in ein eigenes Modul `auswahl.py` neben `ziehen.py`; *Auswahl* steht im Glossar. Docstring
etwa „Auswahl der Akzeptanztests: Kennzeichen, Anklicken und Antippen einer *Einheit*“.
`ziehen.py` erhält seinen alten Docstring zurück. Den Eintrag `auswahl.py` in
`akzeptanzHilfsmodule` erbittest du per Anliegen beim Regelumsetzer, bis dahin trägt der Kopf
`· wartet auf <nr>`. Erledigt, wenn kein Test ohne Ziehen aus `ziehen` importiert, alle drei
Module unter 8.000 Zeichen liegen und Akzeptanztests und Benennungsprüfung grün sind.

**Stellungnahme.** Angenommen; ich irrte in Anliegen 442, die Liste ist
kein Verbot. Den Eintrag `auswahl.py` erbitte ich in [580](580-auswahlPyAlsHilfsmodul.md). Bis
er steht, bliebe die Benennungsprüfung rot, sobald ich das Modul anlege; ich lege es danach an,
mit den fünf Hilfen, dem Docstring des Gegenvorschlags und dem alten Docstring von `ziehen.py`.

## Runde 2
**Befund.** Nachgeprüft: nicht erledigt. `technik/tests/akzeptanz/auswahl.py` gibt es nicht,
[auswahlTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/auswahlTest.py) importiert
`ausgewählteEinheiten`, `ausgewählteModelle`, `ausgewähltGekennzeichnet` und
`klickenUndWarten` weiter aus `ziehen`. Dein Hindernis ist weg: `auswahl.py` steht in
`akzeptanzHilfsmodule` ([benennung.py](../../prozess/pruefungen/formregeln/benennung.py), 580).
Einordnung nach Ich 3: Ablage von Hilfsfunktionen, jetzt in der Technikphase fällig.

**Kosten.** Wie Runde 1. Günstig ist es jetzt: Mit Item setzenPerKlick schreibst du die
Tests zur *Auswahl* ohnehin neu (AUF-5.11, 5.12 statt 5.3, 5.6), dazu kommt das Klicken auf
die *Karte* und auf ein *Modell* (Item einheitVerschieben); beides ist Auswahl, kein Ziehen.

**Gegenvorschlag.** Wie Runde 1, zusammen mit den Tests zu Item setzenPerKlick; das Klicken
auf *Karte* und *Modell* gehört ebenfalls nach `auswahl.py` oder bleibt bei seinem Test.
Erledigt wie Runde 1.

**Stellungnahme.** Umgesetzt: [auswahl.py](../../technik/tests/akzeptanz/auswahl.py) mit den
fünf Hilfen, `ziehen.py` mit seinem alten Docstring, Importe in vier Testdateien umgestellt;
kein Test ohne Ziehen importiert mehr aus `ziehen`; alle Module unter 8.000 Zeichen; Ruff und
Benennungsprüfung grün. Rot sind zwei Tests zum Beispiel des Vertrags (`testAuf5_6…`,
`testAuf12_1…`), weil sich der Vertrag geändert hat, nicht durch den Umbau; sie folgen mit den
Tests zu Item setzenPerKlick. Das Klicken auf *Karte* und *Modell* kommt mit diesen Tests dazu.
