# Freigabefeld und Kommentare ändert nur der Stakeholder

168 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Nach [Ablauf, Freigabe und
Kommentare](../../prozess/ablauf.md#freigabe-und-kommentare) ändert nur der Stakeholder die
Zeilen `Freigabe:` und `Kommentar:` in Plan, Review und Retro, und der Koordinator committet
`Freigabe <Plan|Review|Retro> <n>` nur bei `Freigabe: ja`. Beides ist nur Text.

**Kosten.** Eine Rolle, die bei der Nachkorrektur einen Kommentar „aufräumt“ oder `ja`
setzt, nimmt dem Stakeholder die Steuerung, und niemand merkt es. Ein Freigabe-Commit ohne
`ja` in der Datei widerspricht dem, was der Stakeholder sieht.

**Gegenvorschlag.** Bordmittel ist der Hook `PreToolUse`; Berechtigungen prüfen keine
Zeileninhalte. Der Stakeholder schreibt außerhalb von Claude Code, ihn trifft keiner der
Hooks.
1. Wie `statusrecht.py` (Write, Edit) für `handoff/plan.md`, `review.md`, `retro.md`: Gesperrt
   ist eine Änderung, die `Freigabe: offen` in etwas anderes ändert oder eine Zeile
   `Kommentar:` mit anderem Text als `.` ändert oder entfernt. Erlaubt ist sie, wenn sich die
   Zyklusnummer der ersten Zeile ändert (die Datei des nächsten Zyklus). Zeilen
   `Stellungnahme:` bleiben frei.
2. `bashPositivliste.py`, beim `git commit` des Koordinators: Betreff `Freigabe Plan|Review|
   Retro <n>` nur, wenn die Datei `Freigabe: ja` trägt und ihre erste Zeile Zyklus n nennt.
   `Freigabe Etappe <n>` bleibt frei.

Scheiter-Tests: Edit `Freigabe: offen` → `Freigabe: ja` rot; Kommentartext entfernt rot;
neue Zeile `Stellungnahme:` grün; Write von Plan 4 über Plan 3 mit Kommentaren grün; Commit
`Freigabe Plan 3` bei `Freigabe: offen` rot, bei `Freigabe: ja` grün.

Reihenfolge: nach Anliegen 167; wirkt nicht auf Plan 3,
deshalb nicht vor dessen Freigabe ([Prozessphase](../../prozess/ablauf.md#prozessphase) 1).

Erledigt, wenn beide Teile gebaut sind, die Scheiter-Tests so ausgehen,
`python3 -m pytest prozess/pruefungen` grün ist und der Reviewer den Code geprüft hat.

**Stellungnahme.** Beide Teile gebaut, wie vorgeschlagen.
1. `statusrecht.py` ruft `freigabeKommentare.freigabeVerstoß` für `handoff/plan.md`,
   `review.md`, `retro.md` (Write, Edit): gesperrt sind `Freigabe: ja` neu, `Freigabe: offen`
   entfernt, ein Kommentar mit anderem Text als `.` geändert oder entfernt. Bei neuer
   Zyklusnummer in der ersten Zeile sind Kommentare frei; die neue Datei darf aber nicht
   `Freigabe: ja` tragen (Zusatz zum Vorschlag, sonst wäre das ein Schlupfloch).
2. `bashPositivliste.py` (`freigabeCommitVerstoß`): Betreff `Freigabe Plan|Review|Retro <n>`
   (`-m`, `-qm`, `-m<text>`, `--message`) nur mit `Freigabe: ja` und Zyklus n.
Scheiter-Tests wie gefordert in `statusrechtTest.py` und `bashPositivlisteTest.py`.
Grenzen: Bash-Änderungen an Plan, Review, Retro (`sed -i`) und `git commit -F` sperrt
nichts; Reviewer prüft den Code.
