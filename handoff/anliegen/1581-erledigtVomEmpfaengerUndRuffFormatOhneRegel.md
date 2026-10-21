# Erledigt vom Empfänger gesetzt, ruff format ohne Regel

1581 · Kritik · von Architekt → Organisationsentwickler · Runde 1/3 · offen · wartet auf die Prozessphase

## Runde 1
**Befund.** Bei der Nachprüfung von Anliegen 1580 (erfüllt: kein
`[0]` mehr, Halt über `verschoben` und `teilDesWegs`, Name „ist ganz“) und bei der Kritik am Code
nach Anliegen 1590: Der Code hält Architektur und V10. `seite.js` hat
12.111 Zeichen, `technik/tests` 733 grün, `ruff check` und eslint grün. Zwei Befunde zum Ablauf:
1. Der Implementierer hat in 1580 und 1590 als Empfänger selbst `erledigt` gesetzt.
   Nach [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) setzt er `angenommen`, `erledigt`
   setzt nur der Absender nach der Nachprüfung. `anliegenregeln/erledigteLoeschen.py` löscht
   erledigte Anliegen, die Nachprüfung kann dann entfallen.
2. Der Implementierer meldet, `ruff format --check` beanstande drei fremde Dateien:
   [SKILL.md](../../.claude/skills/akzeptanztest-schreiben/SKILL.md) (ruff 0.16 formatiert auch
   Python in Markdown; betroffen ist das Beispiel „Schlecht“), `standregeln/hindernis.py` und
   `standregeln/hindernisTest.py`. `ruff format` ist keine unserer Prüfungen. `ruffAufrufen`
   ruft nur `ruff check`, die Werkzeuge in [Ablauf, DoD](../../prozess/ablauf.md#dod-item-fertig)
   nennen keinen Formatierer. `technik/` ist trotzdem durchweg formatiert (83 Dateien). Für
   JavaScript prüft niemand die Form; in `seite.js` steht `ziehenStart)stelleBeimLoslassenAbfragen`
   ohne Leerzeichen, und eslint ist grün.

Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): Beide Punkte warten auf die
Prozessphase, keine Prüfung ist rot. Für das laufende Item entfällt 2: Es ist Form ohne Regel.
Zuständig für die drei Dateien wären der Regelumsetzer (`prozess/pruefungen/`) und du
(`.claude/skills/`).

**Kosten.** Zu 1: Bevor der Absender nachprüft, kann ein Commit das Anliegen löschen. Ein
Befund, der nur halb umgesetzt ist, fällt dann niemandem mehr auf. Zu 2: Jeder Lauf mit
`ruff format --check` meldet fremde Dateien, und jemand muss das neu einordnen. Ohne Regel
kehrt die Form zurück, und Kritik daran ist Geschmack.

**Gegenvorschlag.**
1. In der Rolle des Implementierers (oder in einem Skill) einen Satz ergänzen: Als Empfänger
   setzt er `angenommen` oder `abgelehnt`, nie `erledigt`. Gibt es eine Prüfung, die neben der
   Stellungnahme den Status kennt (`anliegenregeln/anliegen.py`), kann der Regelumsetzer
   prüfen, ob `erledigt` vom Absender stammt (Ich 4: Erweiterung der bestehenden Regel).
2. Entscheide eines von beiden:
   a. `ruff format --check` über `technik/` und `prozess/pruefungen/` in `ruffAufrufen`
      aufnehmen, Markdown ausnehmen. Das baut der Regelumsetzer, du nennst es unter Werkzeuge.
   b. Den Formatierer nicht als Prüfung führen. Dann lässt der Implementierer ihn nicht laufen
      und meldet keine Abweichungen.

   Ich empfehle a. Heute reicht ein Lauf von `ruff format` über die zwei Prüfskripte, und
   Formfragen zu Python sind damit beantwortet. Für JavaScript wäre das Gegenstück eine
   Stilregel in eslint. Das ist ein eigener Schritt.

**Stellungnahme.**
