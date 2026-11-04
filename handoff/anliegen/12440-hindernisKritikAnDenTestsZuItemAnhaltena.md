# Hindernis: Kritik an den Tests zu Item anhaltenAufDemWeg

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Abhaken scheitert, obwohl 12082 erledigt und committet ist: Der Hook erledigteLoeschen löscht die Datei nach dem nächsten Bash-Aufruf, noch bevor der Hook fortschritt die Zeile als beseitigt markiert; solange die Löschung uncommittet ist, gilt das Hindernis in beseitigt.py als offen (erprobt an einer Kopie in /tmp: nach dem Commit der Löschung erkennt es den Commit). Sofort hilft, die Löschung zu committen; dauerhaft muss eine uncommittete Löschung eines erledigten Anliegens als beseitigt gelten, sonst trifft das jedes Hindernis, das im selben Commit entsteht und erledigt wird. Das hält den Schritt „Kritik an den Tests zu Item anhaltenAufDemWeg“ von Architekt im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Regelumsetzer beseitigt das Hindernis.

**Stellungnahme.** Umgesetzt in `prozess/pruefungen/standregeln/beseitigt.py`: Eine vom Hook uncommittet gelöschte, erledigte Anliegendatei gilt als beseitigt, mit dem Commit der Erledigung; eine gelöschte offene nicht. Scheiter-Tests: `standregeln/hindernisTest.py` (`testEineUncommittetGelöschteErledigteDateiBeseitigtMitDemCommitDerErledigung`, `testEineUncommittetGelöschteOffeneDateiBeseitigtNichts`). Eintrag in `prozess/regeln/standregeln.md`.
