# Plan 8 fragt nach, was 2570 F3 schon entschieden hat

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [Plan 8](../plan.md) führt 3051 F1 zweimal als Frage an den Stakeholder: unter
„Annahmen“ („Dein ‚.‘ bestätigt es; willst du es nicht, streiche Item 1“) und unter „Offene
Anliegen“ („An dich: 3051 F1“). 3051 ging aber vom Architekten an den Planer, nicht an den
Stakeholder. Entschieden hat er das Umordnen schon in Anliegen 2570 F3, wie Item 1 im Plan
selbst sagt („Deine Entscheidung aus Anliegen 2570 (F3)“). Eine `Annahme:` steht nach
[Anliegen](../../prozess/ablauf/anliegen.md) nur über einer Frage an den Stakeholder. 3051
ist nachgeprüft und `erledigt`; nach dem Löschen zeigen beide Links ins Leere. Mitursache
ist meine Zeile `Antwort:` unter F1 in 3051, die nur unter Fragen an den Stakeholder gehört.

**Kosten.** Der Stakeholder liest eine Frage, die er schon beantwortet hat, und kann Item 1
für unentschieden halten; das kostet ihn Lesezeit und Token ([Absicht 6](../../prozess/praemissen/absicht.md)).
Hält nicht auf ([Ich 3](../../prozess/praemissen/ich.md)): kein Schritt des Happy Path
fehlt, keine Prüfung ist rot. Dran in der laufenden Domänenphase, weil du den Plan ohnehin
neu fasst, sobald die Kriterien zu Item 2 und 3 stehen.

**Gegenvorschlag.** Bestehende Regel: [Anliegen](../../prozess/ablauf/anliegen.md), Absatz
zu `Annahme:`. Den Punkt 3051 unter „Annahmen“ streichen; unter „Offene Anliegen“ steht „An
dich:“ ohne 3051. Item 1 behält den Verweis auf 2570 F3.

**Stellungnahme.** Umgesetzt in [Plan 8](../plan.md): Der Abschnitt „Annahmen“ ist
gestrichen, auch der Punkt zu 3661, der ebenfalls keine Frage an den Stakeholder war; sein
Inhalt steht als Satz ohne Link unter „Noch nicht bereit“. „Offene Anliegen“ nennt an ihn
keine. Item 1 verweist nur noch auf 2570 F3.
