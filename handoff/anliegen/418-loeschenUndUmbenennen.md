# Wer darf Dateien löschen und umbenennen?

418 · Fragen · von Organisationsentwickler → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Seit deinem Auftrag 384 (Commit „Regelumsetzer und Organisationsentwickler:
Schreibgrenze gilt auch für Bash (Anliegen 385, 384)“) legt eine Rolle Dateien nur an und
überschreibt sie; löschen und umbenennen sperrt
[bashSchreiben.py](../../prozess/pruefungen/rollenregeln/bashSchreiben.py), ein anderes
Werkzeug dafür hat Claude Code nicht. Der [Ablauf](../../prozess/ablauf.md#technikphase)
verlangt es aber: Der Planer löscht abgenommene Items (die drei von Plan 5 stehen noch,
Anliegen 417), UX ein Mockup nach dem Bau, der Implementierer ein überholtes Modul;
Anforderungsautor und Testautor benennen eine Anforderung samt Testdatei um.

**Kosten.** Plan 5 gilt als nicht fertig, das Review wartet; jeder Zyklus trifft es wieder.

**Gegenvorschlag.** Bestehende Regel (Ich 4): [Ich 2](../../prozess/praemissen/ich.md)
angepasst.

**F1 · Wer löscht und benennt um?**
A: Jede Rolle, nur in ihren eigenen Schreibpfaden. Ich 2 bekommt: „Löschen und Umbenennen mit
`rm` und `mv` nur in deinen Schreibpfaden; in `handoff/anliegen/` nur, was noch nicht committet
ist.“ Der Regelumsetzer gibt dafür `rm` und `mv` in der Sperre frei; fremde Dateien bleiben
gesperrt. Risiko: Eine Rolle löscht in ihrem Bereich etwas, das noch gebraucht wird. Das fällt
auf: Prüfungen werden rot, der Koordinator sieht die Löschung vor dem Commit, git bewahrt die
Datei.
B: Der Koordinator: Die Rolle nennt, was wegfällt oder wie es heißen soll, er führt es beim
Commit aus. Risiko: Er bekommt Schreibrechte, und niemand prüft ihn; nach einem Umbenennen
sind die Prüfungen der Rolle rot, bis er es ausführt.
C: Wie B, nur für Items (Vorschlag des Planers in 417). Risiko: Alles andere bleibt gesperrt.
Empfehlung: A. Ein Weg für alle Fälle, nur wo die Rolle ohnehin schreibt, und die Sperre prüft
ihn.
Antwort: .

**F2 · Die drei Items von Plan 5 jetzt?**
A: Der Koordinator löscht sie einmalig, als deine Ausnahme. Empfehlung: Das Review wartet nicht,
bis F1 gebaut ist.
B: Der Planer löscht sie, sobald F1 umgesetzt ist.
Antwort: .

**Stellungnahme.**
Kommentar: Mir sind die potentiellen Risiken nicht klar. Ich habe erstmal verstanden, dass manche Anliegen "an den Regeln vorbei löschen können". Gerade das sollte ja ausgeschlossen sein. Auf der anderen Seite ist der Ablauf geblockt, weil etwas gelöscht werden soll, dass eigentlich durch einen automatischen Prozess gelöscht wird, der dann nicht läuft. Ich bin hier sehr unschlüssig über die Antworten zu deinen Fragen. Bei Frage F1 fehlt mir auch eine Empfehlung deinerseits. Außerdem verstehe ich nicht, was Plan 5 damit zu tun haben soll.... Und eine weitere Kleinigkeit: Den Kopf im Anliegen "418 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`" braucht es in dieser Form nicht mehr, weil das Formular im Dashboard das erledigt. Das könnten wir etwas reduzieren. Wirklich übersichtlich war es nie.

**Klärung.**
- Ausgeschlossen bleibt: Keine Rolle ändert oder löscht eine fremde Datei, nach jeder Option.
  „Vorbei“ hieß: Im Commit „Implementierer: Aufstellen als Paket, Eingaben geprüft, Ziehen mit
  Bewegung (Anliegen 396–399, 401)“ fehlen nach der Sperre zwei Module, und keiner weiß, wie.
  Ohne erlaubten Weg sucht eine Rolle einen anderen; A gibt ihr einen, den die Sperre prüft.
- Automatisch löscht Arbiter nur erledigte Anliegen, das läuft; Items löscht der Planer von
  Hand.
- Plan 5 gilt als fertig, wenn seine drei Items gelöscht sind; sie sind gebaut und abgenommen,
  stehen aber noch da. Darum kommt das Review mit dem Klickpfad nicht.
- Risiken und Empfehlung stehen jetzt je Option unter F1; „.“ unter F1 und F2 heißt A.
- Kopf und Legende: Anliegen 420.
