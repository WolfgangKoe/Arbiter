# Das Höchstmaß der Architektur folgt der Entscheidung in 2570

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Die [Höchstmaße](../../prozess/kennzahlen.md#höchstmaße) erlauben der Architektur
je Datei 6.000 Zeichen, zusammen 24.000. Der Stakeholder hat in Anliegen 2570 (F2, C)
entschieden: Die Regeln je Datei 6.000, zusammen 24.000; der Vertrag je Phase eine Datei
(Aufstellen, Bewegen …) zu je 6.000, ohne Summe. Gegliedert wird nach F1 wie `technik/`:
eine Übersicht, je Ordner eine Datei. Heute hat die Architektur 32.664 Zeichen, davon
Vertrag 12.906 ([vertrag.md](../../technik/architektur/vertrag.md),
[handlungen.md](../../technik/architektur/handlungen.md)).

**Kosten.** Bis die Kennzahl folgt, ist die Architektur nach ihrem Wortlaut 8.664 Zeichen zu
lang, obwohl sie der Entscheidung entspricht, sobald ich sie in Plan 8 umordne
([3051](3051-architekturUmordnenInPlan8.md)). Hält nicht auf.

**Gegenvorschlag.** In den Höchstmaßen statt „Architektur (`technik/architektur.md` und je
Datei in `technik/architektur/`) 6.000, zusammen 24.000“: „Architektur: Regeln
(`technik/architektur.md` und je Datei in `technik/architektur/`) je 6.000, zusammen
24.000; Vertrag je Phase eine Datei in `technik/architektur/vertrag/` zu je 6.000, ohne
Summe (Anliegen 2570)“. Den Ordner `vertrag/` lege ich beim Umordnen an. Bestehende Regel,
die das abdeckt: die Zeile selbst, angepasst.

**Stellungnahme.** Angenommen mit Retro 7, P1, wörtlich nach dem Gegenvorschlag in den
[Höchstmaßen](../../prozess/kennzahlen.md#höchstmaße): Regeln je 6.000, zusammen 24.000;
Vertrag je Phase eine Datei in `technik/architektur/vertrag/` zu je 6.000, ohne Summe.
