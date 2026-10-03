# Rollenläufe nicht mehr zählen

120 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder, zum zweiten Mal: „Auf die Rollenläufe kommt es nicht an, nur
auf das Kontextfenster.“ Der Stand meldet trotzdem „Rollenläufe 9/10“; der Koordinator las
das als Budget und empfahl bei rund 33.000 von 120.000 Token einen neuen Chat.
[Ablauf, Budget](../../prozess/ablauf.md#budget) und die Koordinator-Definition nennen jetzt
nur die Belegung; die Kennzahl Rollenläufe ist aus
[`prozess/kennzahlen.md`](../../prozess/kennzahlen.md) gestrichen. Der Mechanismus zählt
noch.

**Kosten.** Eine Zahl mit Schwelle im Stand wirkt wie ein Budget: unnötige Chatwechsel, und
jeder neue Chat lädt den Kontext neu.

**Gegenvorschlag.** Den Zähler ganz entfernen:
1. `stand.py`: `rollenlaufKennzahl`, `protokoll`, `rollenläufe`, `kennzahlRollenläufe` und
   der Teil im Stand.
2. `rollenzaehler.py`, `rollenzaehlerTest.py` und der Hook `SubagentStart` darauf in
   `.claude/settings.json` (der Hook auf `rollenkontext.py` bleibt).
3. `kennzahlen.py`: Rollenläufe je Phase und Rolle; offene Anliegen je Rolle mit Alter
   bleiben. Tests in `kennzahlenTest.py` und `standTest.py` entsprechend.
4. `prozess/regeln.md`: die Zeilen „Rollenläufe als Kennzahl“ und „Rollenläufe je Phase und
   Rolle“.
`.git/arbiter/rollenlaeufe.jsonl` darf weg. Scheiter-Test: Der Stand enthält kein
„Rollenläufe“, auch wenn das alte Protokoll noch liegt.

Kollidiert das mit dem Umzug aus [114](114-pruefskripteOrdnenUndLesbarMachen.md), geht 120
vor: weniger Code zum Umziehen.

Erledigt, wenn der Stand keine Rollenläufe mehr nennt, kein Hook sie zählt und
`python3 -m pytest prozess/pruefungen` grün ist; den Vermerk in `ablauf.md` setze ich.
