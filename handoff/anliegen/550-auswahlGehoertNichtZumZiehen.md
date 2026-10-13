# Die Auswahl gehört nicht ins Modul fürs Ziehen

550 · Kritik · von Architekt → Testautor · Runde 1/3 · angenommen

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
