# Freigabe und Kommentare

Plan, Review und Retro enden mit diesem Abschnitt; der Autor legt ihn so an (Mechanismus:
nur Text):
```
## Freigabe
Freigabe: offen
Kommentar: .
```
- Der Stakeholder kommentiert überall in der Datei: eine eigene Zeile `Kommentar: <Text>`
  unter der Stelle, die er meint; die letzte Zeile ist für Allgemeines. Zu anderen Dateien
  kommentiert er neben ihrem Link in Plan, Review oder Retro, in Anliegen mit `Antwort:` oder
  `Kommentar:` ([Anliegen](anliegen.md)). Er gibt frei mit
  `Freigabe: ja`. Diese Zeilen ändert nur er. Mechanismus: nur Text.
- Nachkorrektur: Der Autor (Plan: Planer, Review: Reviewer, Retro: Organisationsentwickler)
  ändert die Datei nach dem Kommentar und schreibt darunter eine Zeile `Stellungnahme: <was,
  wo>`. Betrifft der Kommentar ein fremdes Artefakt oder braucht er eine Entscheidung, wird
  daraus ein Anliegen; die Stellungnahme nennt dessen Nummer. Solange ein Kommentar ohne
  Stellungnahme steht, ist der Autor dran, auch nach der Freigabe. Mechanismus: nur Text.
- „.“ im Chat heißt: Die Datei ist durchgesehen. Steht `Freigabe: ja`, committet der
  Koordinator `Freigabe <Plan|Review|Retro> <n>`, auch wenn Kommentare offen sind; die
  Nachkorrektur folgt danach. Steht `Freigabe: offen`, beauftragt er den Autor und legt die
  Datei danach wieder vor. Mechanismus: nur Text.
- In `handoff/` heißt ein Commit mit seinem Betreff in Anführung (Commit „Freigabe Plan
  4“), nicht mit der Kennung; `git log --grep` findet ihn. Betreffe sind daher für sich
  verständlich (Anliegen 354). Mechanismus: nur Text.
- Kommentare und Stellungnahmen bleiben, bis der Autor die Datei im nächsten Zyklus neu
  schreibt; Höchstmaß: [Kennzahlen](../kennzahlen.md).
- Die Etappe gibt der Stakeholder mit „.“ im Chat frei.
