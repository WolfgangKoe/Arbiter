# Einen umbenannten Ordner per Test bemerken

165 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
Kritik am Code zu Commit 6a64835. Hier steht, was Anliegen 163 noch
nicht abdeckt.

**Befund.** Nach B3 aus 163 nennt ein Test jeden Altbestand-Ordner einmal und prüft, dass ruff,
git und Benennung ihn auslassen. So bleibt die Liste in sich stimmig. Eine Umbenennung wie die
des Stakeholders bemerkt dieser Test aber nicht. Nach dem Umbenennen von `Arbiter/` in
`Arbiter-old/` hätten alle Stellen weiter übereinstimmend `Arbiter/` genannt, und der Test
wäre grün geblieben. `Arbiter-old/` blieb bis 6a64835 ohne Schreibschutz. Aufgefallen ist das
nur über die Folgen bei ruff und Benennung, nicht über den Schutz. Kein Test vergleicht die
Liste mit den Ordnern, die es tatsächlich gibt.

**Kosten.** Ein neuer oder umbenannter Ordner auf oberster Ebene steht weder unter Schreibschutz
noch unter den Prüfungen, und kein Test wird rot. Das passiert wieder, wenn der Stakeholder
einen Ordner ablegt oder eine Rolle einen anlegt (`doku/` steht schon in den Schreibpfaden des
Organisationsentwicklers). Ein Test kostet etwa eine halbe Stunde.

**Gegenvorschlag.** Ein Test prüft: Jeder sichtbare Ordner auf oberster Ebene ist eine
Perspektive (`domaene`, `technik`, `prozess`), `handoff` oder Altbestand aus `agenten.nurLesbar`.
Ordner mit Punkt zählen nicht (`.venv`, Caches, `.claude`). Die Meldung fragt: „Neuer Ordner
<name>: Perspektive oder Altbestand?“ Wer `doku/` einführt, trägt ihn ein.

Zur Abwägung: Ein Test „jeder Altbestand-Ordner existiert“ wäre einfacher. Er würde aber in
einem frischen Klon rot (der Altbestand ist von git ignoriert) und ebenso nach dem Löschen bei
E8. Der vorgeschlagene Test bleibt in beiden Fällen grün.

Die Liste der Perspektiven steht heute viermal (`benennung.py:199`, `erledigteLoeschen.py:13`,
`hoechstmassTest.py:46`, `rollenkontext.perspektiven`). Kommt sie für den Test nach `pfade.py`,
sollen die anderen sie von dort nehmen. Das ist erwünscht, aber nicht Bedingung.

Erledigt, wenn ein Probeordner `Neu/` auf oberster Ebene (in `tmp_path`) den Test rot macht,
ein Ordner `.probe/` ihn grün lässt, ein fehlender Altbestand-Ordner ihn grün lässt,
`python3 -m pytest prozess/pruefungen` grün ist, `prozess/regeln.md` den Test nennt und der
Reviewer den Code geprüft hat ([Kritik am Code](../../prozess/ablauf.md#kritik-am-code)).

**Stellungnahme.** Umgesetzt: `oberordner.py` mit `oberordnerTest.py` (Probeordner `Neu/` rot, `.probe/` und fehlender Altbestand grün); `perspektiven` steht nur noch in `pfade.py`, `rollenkontext.py`, `benennung.py` und `hoechstmassTest.py` nehmen sie von dort. `regeln.md` nennt den Test.

**Kritik am Code (Reviewer, 96ea7b7).** Was unter „Erledigt, wenn“ steht, ist erfüllt: `Neu/` rot, `.probe/` und fehlender Altbestand grün, die Suite grün (553), `regeln.md` nennt den Test. Neue Befunde: [205](205-oberordnerNachschliff.md). `erledigt` setzt der Architekt.
