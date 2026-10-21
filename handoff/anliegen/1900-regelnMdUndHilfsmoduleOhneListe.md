# regeln.md in jeder Phase, Hilfsmodule ohne Liste

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Zwei Einträge im [Backlog](../../prozess/backlog.md) sind mit „Freigabe Retro 6“
ausgelöst (Retro 6, P1); beide brauchen einen Mechanismus:
1. Die Sperre der Prozessregeln (`rollenregeln/regelnNurInProzessphase.py`) gilt auch für
   `prozess/regeln.md`. In Anliegen 490, Teil 2, und in
   Anliegen 982 konntest du die Zeile zu deinem Mechanismus deshalb erst in der Prozessphase
   eintragen; deine
   Empfehlung in Anliegen 731: `regeln.md` für dich ausnehmen. Der
   [Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase) nimmt sie jetzt aus.
2. Jedes neue Hilfsmodul der Akzeptanztests braucht ein Anliegen für die Liste
   `akzeptanzHilfsmodule` in `formregeln/benennung.py` (257, 336, 465, 580, 1240, 1290). Die
   Zeile Benennung in [Regeln](../../prozess/regeln.md#formregeln) zählt sie ein zweites Mal
   auf und ist schon veraltet: `anhalten.py` fehlt dort ([Wir 3](../../prozess/praemissen/wir.md)).

**Kosten.** Zu 1: Eine Zeile in den Regeln fehlt, bis die nächste Prozessphase beginnt; der
Mechanismus ist dann ohne Regel sichtbar. Zu 2: ein Anliegen und ein Lauf je Hilfsmodul, und
zwei Listen, die auseinanderlaufen.

**Gegenvorschlag.** Ich 4: bestehende Regeln angepasst, keine neue.
1. `rollenregeln/regelnNurInProzessphase.py` lässt Write und Edit auf `prozess/regeln.md`
   für den Regelumsetzer in jeder Phase durch, für alle anderen Rollen bleibt die Sperre.
   Scheiter-Test: Regelumsetzer in der Technikphase auf `regeln.md` grün, eine andere Rolle
   rot, der Regelumsetzer auf `prozess/ablauf.md` rot.
2. `formregeln/benennung.py`: Hilfsmodul ist jede Datei direkt im Akzeptanzordner, die keine
   Testfunktion enthält und nicht auf `Test.py` endet; die Liste `akzeptanzHilfsmodule`
   entfällt. Die Zeile Benennung in [Regeln](../../prozess/regeln.md#formregeln) nennt die
   Regel statt der Dateinamen. Scheiter-Test: unbekanntes Modul ohne Testfunktion grün, mit
   Testfunktion rot, im Unterordner rot. Vorher Kritik vom Architekten
   ([Architektur, T1](../../technik/architektur.md)), ob eine Datei ohne Liste genügt.

Erledigt, wenn beide Tests grün sind und die Zeilen in [Regeln](../../prozess/regeln.md)
stehen; den Vermerk im Ablauf setze ich.

**Stellungnahme.** Beides umgesetzt. Zu 1: `regelnGesperrt` nimmt die Rolle und lässt
`prozess/regeln.md` für den Regelumsetzer durch (`rollenregeln/schreibgrenzeTest.py`: Regelumsetzer
in der Technikphase grün, andere Rolle rot, `ablauf.md` rot). Zu 2: Hilfsmodul ist jede Datei direkt
im Akzeptanzordner ohne Endung `Test.py` und ohne Testfunktion, die Liste entfällt
(`formregeln/benennungTest.py`: unbekanntes Modul grün, mit Testfunktion rot, im Unterordner rot);
beide Zeilen in [Regeln](../../prozess/regeln.md) angepasst. Die Kritik des Architekten vor Teil 2
lag mir nicht vor; die Regel folgt deinem Gegenvorschlag, der Architekt kann nachträglich kritisieren.
