# Antwortmöglichkeiten tragen Buchstaben

Form: Fragen
Von: Organisationsentwickler
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Dein Befund in Anliegen 8840: Die Antwortmöglichkeiten trugen keine Buchstaben
A, B, C, das erschwerte dir das Antworten. In der committeten Fassung stehen sie als
Aufzählung mit „· empfohlen“ am Ende; der Anforderungsautor stellt 8840 schon um.
[Anliegen](../../prozess/ablauf/anliegen.md) regelt nur die Zeile `Antwort: .` und die Quelle
in Klammern hinter jeder Möglichkeit, nicht ihre Form. Darum schreibt jede Rolle sie anders:
`A: … B: …` und `Empfehlung: A` in Anliegen 6987 und in der Frage aus
`standregeln/hindernis.py`, Aufzählung ohne Buchstaben in 8840.

**Kosten.** Ohne Buchstaben musst du die Möglichkeit in eigenen Worten nennen; die Rolle
muss deine Antwort deuten, und eine Fehldeutung geht als Entscheidung durch
([Absicht 4](../../prozess/praemissen/absicht.md)).

**Gegenvorschlag.** Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)): der Absatz
zur Quelle in [Anliegen](../../prozess/ablauf/anliegen.md), ergänzt um einen Satz: Jede
Möglichkeit steht in einer eigenen Zeile `A: …`, `B: …`, `C: …` mit ihrer Quelle, darunter
`Empfehlung: <Buchstabe>, <Grund>`, dann `Antwort: .`; du antwortest mit dem Buchstaben.
Das ist die Form, die `hindernis.py` schon schreibt.

**Stellungnahme.**
Annahme: Bis zu deiner Antwort ändere ich nichts; danach schreibe ich den Satz in dieser
Prozessphase, bei A beauftragt der Koordinator den Regelumsetzer.

**F1 · Wie wird die Form gesichert?**
A: Satz in Anliegen, dazu eine Prüfung in `anliegenregeln/anliegen.py`: rot, wenn unter einer
Frage an dich keine Zeile `A:` oder keine Zeile `Empfehlung:` steht (Anliegen 8840, dein
Befund). Am Bildschirm: nichts. Arbeit: ein Lauf des Regelumsetzers samt Test. Token: keine
je Lauf, die Prüfung läuft beim Commit. Nachteil: Eine falsche Form fällt erst beim Commit
auf; dann bessert die Rolle in einem weiteren Lauf nach.
B: Nur der Satz, Mechanismus „nur Text“ (Anliegen, Absatz zur Quelle). Kein Bauaufwand;
die Form hängt am Gedächtnis jeder Rolle, wie bisher bei 8840.
C: Wie bisher, keine Regel (Anliegen, wie heute). Jede Rolle wählt die Form selbst.
Empfehlung: A, denn die Form lässt sich berechnen, und eine Rolle ist schon davon abgewichen.
Antwort: A

Umgesetzt: der Satz in [Anliegen](../../prozess/ablauf/anliegen.md), Absatz zur Quelle,
Mechanismus „nur Text“ bis zur Prüfung. Auftrag an den Regelumsetzer, nach P6:
`anliegenregeln/anliegen.py` meldet rot, wenn zwischen einer Zeile `**F<n> · …**` und ihrer
Zeile `Antwort:` keine Zeile mit `A:` oder keine mit `Empfehlung:` beginnt; Test in
`anliegenTest.py` mit je einem Fall ohne `A:` und ohne `Empfehlung:`. Dazu schreibt
`standregeln/hindernis.py` `B:` in eine eigene Zeile, heute steht es hinter `A:` in Zeile 48.
Steht sie, ersetze ich „nur Text“ im Satz durch die Prüfung und setze `erledigt`.
