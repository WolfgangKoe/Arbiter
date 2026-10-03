# Moderation

Stand: Plan 2 (Items 1 bis 3, `handoff/plan.md`). Kein offenes Anliegen blockiert ein Item: Keins nennt OBJ-1, AUF-2 oder AUF-3, QUE-1.

## Dran
Blockiert das Inkrement: nichts.

- Stakeholder:
  - [113](anliegen/113-ordnungDerPruefskripte.md): F1 und F2 beantworten; ohne Antwort gilt die Empfehlung (A, A). Danach kann 114 beginnen.
  - [83](anliegen/83-sprungErproben.md): Runde 3/3, F1 ist beantwortet (Erweiterung löschen, dazu eine Gegenfrage zu einer Marke, die mit der Zeile mitgeht); die Gegenfrage braucht eine Antwort des Architekten, nach Runde 3 sonst `eskaliert`.
- Regelumsetzer: [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md) in der Prozessphase von Zyklus 2; wartet auf 113.
- Organisationsentwickler: [107](anliegen/107-kritikAnDenPruefungen.md) wartet auf 113 und 114; nichts zu tun.
- Architekt: [83](anliegen/83-sprungErproben.md) nach der Antwort des Stakeholders einarbeiten (Status `beantwortet`, dann Anliegen an Anforderungsautor und Regelumsetzer).
- Anforderungsautor, Testautor: nichts.

## Vorschläge
- Anliegen 111 steht auf `erledigt`: `erledigteLoeschen.py` löscht die Datei (Mechanismus, keine Rolle).
- 107, 113, 114 sind ein Thema (Prüfskripte). Zusammenlegen nicht nötig: Sie sind verlinkt und verteilen Frage und Umsetzung sauber; 107 schließt der Stakeholder als Absender, wenn 114 fertig ist.
- 83 und 114 berühren beide `rueckverfolgung.py` und `sprung/`: Der Regelumsetzer sollte die Löschung von `sprung/` und den Umbau nach 114 B in einem Zug planen (Regelumsetzer).
- Plan, Abschnitt Offene Anliegen: nennt 83, aber nicht 113 (Frage an dich); Planer kann es ergänzen (Planer).

## Fragen an dich
- [113](anliegen/113-ordnungDerPruefskripte.md) F1: Prüfskripte nach Thema ordnen (Empfehlung A)?
- [113](anliegen/113-ordnungDerPruefskripte.md) F2: Tests neben dem Modul (Empfehlung A)?
- [83](anliegen/83-sprungErproben.md) F1: beantwortet, aber nicht mit „.“; offen bleibt, ob eine Marke, die mit der Zeile mitgeht, gewollt ist. Der Architekt muss sie beantworten, dich fragt er dann neu.

Auffällig: Am Ende von 107 steht fremder Text („Was ist mit dieser Datei? …benennungRueckstand.txt“); vermutlich ein Versehen, der Organisationsentwickler sollte es prüfen.
