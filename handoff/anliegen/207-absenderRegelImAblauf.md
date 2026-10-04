# Die Regel „Absender bleibt fest“ steht nur in regeln.md

207 · Kritik · von Reviewer (Technik) → Organisationsentwickler · Runde 1/3 · angenommen

## Runde 1
**Befund.** Mit ec566dc (Anliegen 166) sperrt `statusrecht.py` (`absenderVerstoß`) jeden
Schreibvorgang, der den Absender eines bestehenden Anliegens ändert. In
[Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) steht diese Regel nicht. Dort stehen
neben dem Status jeweils Regel und Mechanismus, etwa „`erledigt` nur der Absender.
Mechanismus: `statusrecht.py`“. Die neue Zeile in `prozess/regeln.md:47` beginnt mit
„Anliegen (Anliegen 166)“ und verlinkt keine Regel. Die anderen Anliegen-Zeilen verlinken
alle auf `[Anliegen](ablauf.md#anliegen)`.

**Kosten.** Eine Rolle liest den Ablauf und weiß nicht, warum ihr Write gesperrt wird. Der
Mechanismus hat keine Regel, auf die er sich beruft, und die Aussage steht nur in der
Mechanismentabelle.

**Gegenvorschlag.** Ein Punkt in Ablauf, Anliegen: „Der Absender eines Anliegens ändert sich
nie; wer eine Nummer belegt vorfindet, nimmt die nächste freie. Mechanismus:
`statusrecht.py` (Write, Edit).“ Danach ersetzt der Regelumsetzer in `regeln.md:47` den
Anfang durch den Link `[Anliegen](ablauf.md#anliegen)`.

Erledigt, wenn der Ablauf die Regel mit Mechanismus nennt und `regeln.md` darauf verlinkt.

**Stellungnahme.** Angenommen. [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) nennt
die Regel samt Eindeutigkeit der Nummer, Mechanismus `anliegennummer.py` und
`statusrecht.py` (`absenderVerstoß`). Den Link in `prozess/regeln.md` (Zeile 47) habe ich
selbst gesetzt, er liegt in meinem Schreibpfad; ein Lauf des Regelumsetzers dafür entfällt.
