# Moderation

Stand: Plan 2 (Items 1 bis 3, `handoff/plan.md`). Kein offenes Anliegen blockiert ein Item: Keins nennt OBJ-1, AUF-2 oder AUF-3, QUE-1.

## Dran
Blockiert das Inkrement: nichts.

- Stakeholder:
  - Anliegen 113: F1 und F2 beantworten; ohne Antwort gilt die Empfehlung (A, A). Danach kann 114 beginnen.
  - [83](anliegen/83-sprungErproben.md): Runde 3/3; deine Stellungnahme steht, die Zeile `Antwort:` unter F1 fehlt (siehe Fragen).
- Regelumsetzer: [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md) in der Prozessphase von Zyklus 2; wartet auf 113.
- Organisationsentwickler: [107](anliegen/107-kritikAnDenPruefungen.md) wartet auf 113 und 114; nichts zu tun.
- Architekt: [83](anliegen/83-sprungErproben.md) nach der Freigabe: Status `beantwortet` setzen, die Gegenfrage (Marke, die mit der Zeile mitgeht) aufnehmen.
- Anforderungsautor, Testautor: nichts.

## Vorschläge
- Anliegen 111 steht auf `erledigt`: `erledigteLoeschen.py` löscht die Datei (Mechanismus, keine Rolle).
- 107, 113, 114 sind ein Thema (Prüfskripte). Zusammenlegen nicht nötig; 107 schließt der Stakeholder als Absender, wenn 114 fertig ist.
- 83 und 114 berühren beide `rueckverfolgung.py` und `sprung/`: Der Regelumsetzer plant die Löschung von `sprung/` und den Umbau nach 114 B in einem Zug (Regelumsetzer).
- Plan, Abschnitt Offene Anliegen: nennt 83, aber nicht 113; Planer kann es ergänzen (Planer).
- Regel zu Runde 3/3, Entscheidung des Stakeholders: Nach Runde 3/3 wird ein Anliegen an ihn `eskaliert`; er entscheidet dann, auch den Rundenmarker auf 1/3 zu setzen, sonst gibt er Anweisung. Der Zähler verhindert eine ewige Diskussion zweier Subagenten. Ich darf `prozess/` nicht ändern: Der Organisationsentwickler trägt sie in [`prozess/ablauf.md`](../prozess/ablauf.md) (Anliegen) ein, bei der Tabellenzeile `eskaliert` (Organisationsentwickler). Die Lücke gilt damit als geschlossen, sobald der Eintrag steht.
- Mechanismus: [`anliegen.py`](../prozess/pruefungen/anliegen.py) kennt `eskaliert` und Runde 1 bis 3, prüft aber nicht, dass nach Runde 3/3 nur `eskaliert` folgt (und kein weiteres `offen`). Der Architekt kann es als Anliegen an den Regelumsetzer legen (Architekt, an Regelumsetzer).
- 107: Am Ende steht fremder Text („Was ist mit dieser Datei? …benennungRueckstand.txt“); vermutlich ein Versehen, der Organisationsentwickler prüft es.

## Fragen an dich
- Anliegen 113 F1: Prüfskripte nach Thema ordnen (Empfehlung A)?
- Anliegen 113 F2: Tests neben dem Modul (Empfehlung A)?
- [83](anliegen/83-sprungErproben.md) F1: Du änderst den Kopf nicht. `beantwortet` setzt der Absender, also der Architekt, nach der Freigabe; `offen` bleibt, bis dahin ist die Zeile richtig: `83 · Fragen · von Architekt (Technik) → Stakeholder · Runde 3/3 · offen`. Trage stattdessen unter F1 die Zeile `Antwort:` ein, mit dem, was gilt, etwa `Antwort: Erweiterung löschen (wie A ohne Erweiterung); Marke je Zeile klären, siehe Stellungnahme`. Ein bloßes „.“ würde A bedeuten, das trifft deine Gegenfrage nicht. Folge: Der Architekt setzt `beantwortet`, nimmt die Gegenfrage in seiner Antwort auf und legt die Anliegen an Regelumsetzer (`sprung/` löschen) und, falls du A willst, Anforderungsautor an. Bleibt die Gegenfrage danach offen, steht `eskaliert`, und du entscheidest (auch Runde zurück auf 1/3). Die Regel dafür steht oben bei den Vorschlägen.
