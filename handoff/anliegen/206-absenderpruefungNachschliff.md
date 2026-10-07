# Absenderprüfung: kaputter Kopf, Nummer nur bei Bedarf

206 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von ec566dc (Anliegen 166). Die Suite ist grün (557 Tests). Zwei
Befunde in `prozess/pruefungen/statusrecht.py`:

**B1 · Ein Write mit unlesbarem Kopf ersetzt ein fremdes Anliegen weiter.** `entscheide`
gibt bei `neu is None` frei, auch wenn `alt` ein gültiges Anliegen ist (`statusrecht.py:42`).
Beispiel: Ein paralleler Lauf schreibt ein Anliegen gleicher Nummer und verschreibt sich im
Kopf, etwa `->` statt `→` oder ohne Typ. Dann überschreibt er das fremde Anliegen, ohne dass
`absenderVerstoß` greift. Das ist der Fall aus 166, nur mit Tippfehler.
Kosten: Der fremde Text ist verloren, bevor `anliegenTest.py` den Kopf bemängelt. Das gilt
auch für die Sperren aus `erledigtVerstoß` und `rundenVerstoß`: Ein Kopf, den der Hook nicht
lesen kann, umgeht alle drei.
Gegenvorschlag: Ist `alt` gesetzt und `neu` nicht, wird verweigert, mit der Meldung
„Kopf fehlt oder ist falsch (prozess/ablauf.md, Anliegen)“. Scheiter-Test: ein Write mit
kaputtem Kopf auf ein bestehendes Anliegen wird verweigert.

**B2 · `nächsteFreieNummer` läuft bei jedem Schreibvorgang.** `statusrecht.py:45` berechnet
die Nummer, bevor feststeht, dass es einen Verstoß gibt. Dahinter steckt ein
`git log --all --name-only` (`anliegen.vergebeneNummern`), gemessen 0,18 s. Er läuft bei
jedem Write und Edit einer Rolle auf ein Anliegen, und die Dauer wächst mit dem Verlauf.
Kosten: Wartezeit bei jeder Stellungnahme und jeder neuen Runde. Gebraucht wird die Nummer
nur, wenn gesperrt wird.
Gegenvorschlag: `absenderVerstoß(alt, neu, wurzel)` ruft `nächsteFreieNummer` erst im Zweig
des Verstoßes auf. Alternativ meldet `absenderVerstoß` nur den Absender, und `entscheide`
hängt die Nummer an.

Erledigt, wenn B1 mit Scheiter-Test umgesetzt ist, B2 umgesetzt oder begründet abgelehnt
ist, `python3 -m pytest prozess/pruefungen` grün ist und der Reviewer den Commit geprüft hat.

Stellungnahme: Entfällt mit dem Rückbau.
