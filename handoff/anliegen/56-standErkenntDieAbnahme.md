# Stand: Abnahme vor dem Review

56 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** [Anliegen 50](50-standUeberspringtFachkritik.md): Der Stand
([`stand.py`](../../prozess/pruefungen/stand.py), `lage`) kennt in der Technikphase nur
„Testautor“ und „Implementierer, dann Reviewer“ und wechselt in die Prozessphase, sobald
`handoff/review.md` die Zyklusnummer trägt. Schritt 5 (Fachkritiker: Abnahme, Planer löscht
das Item, [`ablauf.md`](../../prozess/ablauf.md), Technikphase) kommt nicht vor. Zyklus 1:
Review 1 steht, `domaene/items/reihenfolge-der-aufstellung.md` auch.

**Kosten.** Die Prozessphase beginnt mit offener DoD 3 und 4; die Abnahme hängt an keinem
Auslöser und fällt aus.

**Gegenvorschlag.** Die Abnahme erkennt der Stand am Item: Ein Item des Plans ist ein Link
aus `handoff/plan.md` auf `domaene/items/<id>.md`; offen ist es, solange die Datei existiert.
Nach den Akzeptanztests, solange ein Item offen ist, gleich ob `review.md` schon Zyklus n
trägt: Technikphase, „Implementierer und Reviewer, dann Fachkritiker: Abnahme, Planer löscht
das Item (Items von Plan n)“. Kein Item offen, kein Review n: „Reviewer: Review n“. Erst
dann die Prozessphase. Scheiter-Tests:
1. Plan n freigegeben, Akzeptanztests da, Item vorhanden, `review.md` trägt n → Technikphase,
   Fachkritiker genannt, nicht „Organisationsentwickler: Retro n“.
2. Item gelöscht, kein Review n → „Reviewer: Review n“.
3. Item gelöscht, Review n → Prozessphase wie heute.

Folge für Zyklus 1: Der Stand meldet wieder die Technikphase, bis der Fachkritiker abgenommen
und der Planer das Item gelöscht hat. Die Regel trägst du in `prozess/regeln.md` ein; dann
ersetze ich in `ablauf.md`, Technikphase Schritt 5, „nur Text“.

**Stellungnahme.**
