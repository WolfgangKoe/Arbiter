# Anliegen

Anliegen ist der Oberbegriff: eine Datei je Diskussion, `handoff/anliegen/<nr>-<kurz>.md`,
höchstens 4.000 Zeichen; jede Zeile `Antwort:` zählt als `Antwort: .` (Anliegen 161).
Mechanismus: nur Text.
Erste Zeile `# <Titel>`, ab der dritten der Kopf, ein Feld je Zeile (Anliegen 1670):
```
Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: Prozessphase
```
Die Nummer steht nur im Dateinamen. `Wartet auf:` steht, solange erst ein anderes Anliegen
erledigt sein muss (`Wartet auf: 1213`) oder es nach der [Kritik](kritik.md) auf eine
Phase wartet (`Domänenphase`, `Technikphase`, `Prozessphase`). Ohne Zyklus ist es dran,
sobald die Phase läuft, auch die laufende; die Phase eines späteren Zyklus nennt ihn
(`Technikphase 8`), dann wartet es bis dahin (Anliegen 3200, 3251). Rolle: Name aus
`.claude/agents/` oder Stakeholder, ohne Perspektive (Anliegen 420). Ein Modul liest und
schreibt den Kopf für alle Skripte.
Mechanismus: `anliegenregeln/anliegen.py`, `lesen/anliegenKopf.py`
([Anliegenregeln](../regeln/anliegenregeln.md)); eine Perspektive in Klammern lässt es durch, ohne
Perspektive: nur Text; `Wartet auf`, auch mit Zyklus: `anliegenregeln/anliegenDran.py`
([Standregeln](../regeln/standregeln.md)).

Form | der Empfänger soll | Absender
---|---|---
Kritik | sein Artefakt berichtigen, es ist falsch oder veraltet | jede Rolle, Stakeholder
Fragen | entscheiden | jede Rolle
Auftrag | Neues umsetzen; er fragt nach, lehnt aber nicht ab | Stakeholder

Je Runde (`## Runde <n>`) die Absätze `**Befund.**`, `**Kosten.**`, `**Gegenvorschlag.**`,
`**Stellungnahme.**`, vor dem Punkt darf die Rolle in Klammern stehen; die Stellungnahme legt
der Absender leer an. Eine Rückfrage steht in der Stellungnahme, die Antwort des Absenders
darunter als `**Klärung.**`; beide kosten keine Runde. Unter jeder Frage an den Stakeholder
(`**F<n> · …**`) steht eine eigene Zeile `Antwort: .`; „.“ heißt bei `angenommen`: Die
Empfehlung gilt. Arbeitet der Absender mit der Empfehlung weiter ([Ich 1](../praemissen/ich.md)),
steht darüber `Annahme: <was er damit tut>`. Mechanismus: nur Text.
Hinter jeder Antwortmöglichkeit einer Frage an den Stakeholder steht in Klammern ihre Quelle
nach der [Domäne](../../domaene/CLAUDE.md) oder eine bestehende Regel, etwa „(Regeltext)“,
„(ArbiterMap)“, „(Anliegen 2362)“, „(Ich 4)“, sonst „(neu)“; eine neue empfiehlt die Rolle nur
mit Grund aus dem Ziel ([Absicht 3](../praemissen/absicht.md), Anliegen 3820). Ja oder Nein
zum Gegenvorschlag desselben Anliegens trägt dessen Quelle, so die Frage aus
`standregeln/hindernis.py`. Mechanismus: nur Text.

Status, Züge und wer dran ist: [Status der Anliegen](anliegenStatus.md).
