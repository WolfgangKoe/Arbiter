# Prozesslast eindämmen: Deckel, Reihenfolge, Kritik an Prüfskripten

296 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Seit `Freigabe Retro 2` gingen 90 von 129 neuen Anliegen an den Regelumsetzer
oder mich (70 %, Schwelle der [Prozesslast](../../prozess/kennzahlen.md) ein Drittel). Offen
sind 38, 31 an den Regelumsetzer, gut die Hälfte Kritik am Code der Prüfskripte (202 bis
206: Nachschliff am Nachschliff). Die Reaktion der Kennzahl ist nur Text und griff nie.
Fragen aus der [Moderation](../moderation.md), zu deiner Frage in [107](107-kritikAnDenPruefungen.md).

**Kosten.** Plan 4 wartet auf eine Kette einer Rolle; Domäne und Technik sind frei.

**Gegenvorschlag.** Keine neue Prüfung; angepasst werden die Reaktion der Prozesslast und
Kritik am Code ([ich.md](../../prozess/praemissen/ich.md) 4). Der Deckel ersetzt 107 Punkt 2;
Punkt 3 bleibt im Backlog.

**F1 · Deckel und Backlog.** Höchstens 10 offene Anliegen an den Regelumsetzer. Darüber legt
niemand ein neues an ihn an, außer bei Fehlverhalten (F3) oder von dir, und der Koordinator
beauftragt keinen neuen Mechanismus. In den Backlog, Auslöser „der Regelumsetzer ändert die
Datei ohnehin“: 202 bis 206, 221, 295; er setzt `abgelehnt` mit Verweis, der Reviewer
`erledigt`. Bleiben 24; den Rest senkt der Abfluss. Mechanismus: nur Text; der Stand zählt
schon je Rolle (`Dran: Regelumsetzer (…)`).
- A (empfohlen): so.
- B: Deckel als Sperre in `anliegennummer.py` (neue Datei an ihn über 10 rot); ein neuer
  Mechanismus, vorher wird einer gelöscht.
- C: kein Deckel, nur der Backlog.

Antwort: A

**F2 · Plan 4 vor der restlichen Kette.** Vorab nur 294 (Elementverbot, prüft das Frontend,
das Plan 4 ändert) und 286, falls die laufende Nachprüfung eine Lücke findet. Retro 3 führt
294 als P1; so meldet der Stand die Domänenphase erst danach. Der Rest läuft neben Plan 4 in
den Strängen der Moderation, im Strang Hook-Code zuerst 290: Sonst bricht ein halber Hook den
Prüflauf der Rollen von Plan 4 ab (289). Mechanismus: `standregeln/phasenfolge.py`
(`offenesProzessItem`); Reihenfolge des Rests nur Text.
- A (empfohlen): so.
- B: zusätzlich 287, 290, 295 vorab, wie die Moderation zuerst vorschlug.

Antwort: A

**F3 · Kritik am Code der Prüfskripte nur bei Fehlverhalten.** Fehlverhalten: Eine Prüfung
lässt einen Verstoß durch, meldet einen, den es nicht gibt, bricht einen Lauf ab oder sperrt
eine Rolle zu Unrecht. Nur das wird ein Anliegen an den Regelumsetzer. Lesbarkeit und Form
halten die Werkzeuge der [DoD 2](../../prozess/ablauf.md#dod-item-fertig) (ruff, SonarLint,
complexipy, Benennung, Kommentare); deine Forderung aus 107 gilt weiter. Gilt für alle Pfade
des Regelumsetzers in der Tabelle. Übrige Befunde des Reviewers:
- A (empfohlen): ein Sammelanliegen je Zyklus, ein Abschnitt je Datei; der Regelumsetzer
  nimmt einen Abschnitt mit, wenn er die Datei ohnehin ändert. Zählt einmal gegen den
  Deckel; offene Abschnitte übernimmt das des nächsten Zyklus.
- B: ein Sammelanliegen je Datei und Zyklus (Moderation); viele Dateien sprengen den Deckel.
- C: entfallen; was die Werkzeuge nicht melden, gilt als gut genug.

Mechanismus: nur Text (Urteil des Reviewers, was Fehlverhalten ist).

Antwort: A

Nach deinen Antworten ändere ich Kennzahlen, Ablauf und Backlog (Retro 3, Nachkorrektur).

**Stellungnahme.** Machen wir so, kann Anliegen 107 geschlossen werden?

**Klärung.** Ja, 107 schließt du als Absender mit `erledigt`. Umgesetzt in
[Kennzahlen](../../prozess/kennzahlen.md) (Deckel),
[Ablauf, Kritik am Code](../../prozess/ablauf.md#kritik-am-code) (F3) und
[Backlog](../../prozess/backlog.md) (202 bis 206, 221). F2 ist erfüllt: 286, 287, 290, 294, 295 sind erledigt,
Retro 3 braucht kein P1. Setz bitte `angenommen`.
