# Antworten durch Status und in der Moderation

254 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Dein Hinweis zu 241 und die letzte Zeile von `handoff/moderation.md`:
1. Status: Fragen gelten heute nur über eine Freigabe als beantwortet
   ([Ablauf, Anliegen](../../prozess/ablauf.md#anliegen)). Dazwischen antwortest du mit dem
   Status: `angenommen`, `Antwort: .` unverändert, gemeint: Die Empfehlungen gelten. Die
   Statustabelle kennt `angenommen` nur als „nach der Umsetzung“. Der Stand liest es schon
   richtig: Bei `angenommen` ist der Absender dran. Es fehlt nur die Regel.
2. Moderation: `## Fragen an dich` hat keine Antwortzeile; du hast „Bestätigt.“ angehängt und
   im Chat geantwortet. Der Moderator schreibt die Datei jedes Mal neu, die Antwort geht dabei
   verloren. Das Format ist eine Regel (`moderator.md`, Ablauf), keine Sache des
   Regelumsetzers; deine Bitte an ihn nehme ich hier auf.

**Kosten.** Ohne Regel rät die Rolle, was dein Status meint. Eine Antwort in der Moderation
erreicht das Anliegen nicht.

**Gegenvorschlag.**

**F1 · Was heißt dein Status an einem Anliegen mit Fragen?**
- A: `angenommen`: Jede `Antwort: .` gilt als Empfehlung, eine mit Text als deine Antwort;
  der Absender arbeitet ein und setzt `erledigt`. `abgelehnt`: Deine Antwortzeilen sagen, was
  stattdessen; der Absender schreibt die nächste Runde. Folgst du der Empfehlung, trägst du
  nichts ein.
- B: Wie A, aber jede Frage braucht eine eigene Antwort (`Antwort: A`).
- C: Wie heute: Nur die Freigabe beantwortet.
Empfehlung: A. So arbeitest du schon; B kostet je Frage eine Zeile, die Empfehlung steht
direkt darüber.
Antwort: .

**F2 · Wie beantwortest du Fragen der Moderation?**
- A: Fragen zu einem Anliegen verlinkt die Moderation nur, beantwortet wird im Anliegen (F1).
  Eigene Fragen (Reihenfolge) stehen als `**F<n> · …**` mit Empfehlung und `Antwort: .`;
  „.“ im Chat heißt, sie gelten. Der Koordinator committet die Datei mit deinen Antworten,
  bevor der Moderator sie neu schreibt; der Moderator übernimmt sie in die Reihenfolge.
- B: Die Moderation stellt keine eigenen Fragen; Reihenfolgefragen werden ein Anliegen.
- C: Wie heute: Antwort im Chat.
Empfehlung: A. Antwort neben der Frage wie in den Anliegen; der Commit hält sie fest.
Antwort: .

Nach A und A ändere ich Ablauf (Anliegen) und `moderator.md`. Mechanismen beauftragt der
Koordinator beim Regelumsetzer: Zeile `Antwort:` unter jeder Frage der Moderation (wie
`antwortVerstöße`), diese Zeilen ändert nur du (`statusrecht.py`).

**Stellungnahme.**
