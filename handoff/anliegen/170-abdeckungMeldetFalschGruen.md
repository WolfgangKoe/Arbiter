# Abdeckung und vulture melden falsch grün

170 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Kritik am Code zu Commit `6dfe473` (P1 der [Retro 2](../retro.md),
Anliegen 157).

**Befund.**
1. `unbenutzterCode` (`prozess/pruefungen/abdeckung.py`) prüft den Rückgabewert von vulture
   nicht. Fehlt ein Pfad oder hat eine Datei einen Syntaxfehler, schreibt vulture nur nach
   stderr und endet mit 1; stdout ist leer, die Funktion gibt `[]` zurück, der Test ist grün.
   Ausprobiert: `unbenutzterCode(wurzel, "technik/arbitr")` und
   `unbenutzterCode(wurzel, "technik/arbiter", "technik/tests/gibtsNicht")` liefern beide `[]`.
   Wird `technik/arbiter` oder `akzeptanzOrdner` umbenannt, prüft DoD 2 nichts mehr und
   meldet grün; im zweiten Fall auch ohne Kriterien als Benutzer.
2. `zweigabdeckung` gibt `totals.percent_covered` zurück. Mit `--branch` ist das die
   gemeinsame Quote aus Zeilen und Zweigen, keine Zweigabdeckung, wie Name und
   [DoD 1](../../prozess/ablauf.md#dod-item-fertig) sagen. Heute hat `technik/arbiter`
   227 Anweisungen und 40 Zweige: Fehlen bei allen Zeilen gedeckt 13 der 40 Zweige (jedes
   `if` ohne `else`, dessen Nein-Fall kein Test probt), ergibt das (227 + 27) / 267 = 95,1 %,
   grün, bei einer Zweigabdeckung von 68 %. `testEinNichtGeprobterZweigOhneAnweisungZählt…`
   prüft nur `< 100` und bemerkt das nicht.
3. Die Meldung rundet anders als der Vergleich: Bei 94,96 % ist der Test rot und meldet
   „95.0 %“.

**Kosten.** 1: Eine Prüfung, die bei einem Fehler grün bleibt, ist schlimmer als keine; sie
gibt eine Sicherheit vor, die nicht besteht. 2: Die Schwelle misst nicht, was DoD 1 verlangt;
nicht geprobte Nein-Fälle (Vorbedingungen, genau die Frage aus
[150](150-sonarlintAbdeckungUndToterCode.md)) gehen in der Zeilenzahl unter. 3: Verwirrende
Meldung, kleiner Aufwand.

**Gegenvorschlag.**
1. Rückgabewert prüfen: 0 (nichts) und 3 (toter Code gefunden) sind gültig, alles andere ist
   ein Fehler mit stderr in der Meldung. Scheiter-Test: ein fehlender Pfad ist rot.
2. Entweder die Zweigquote messen (`covered_branches / num_branches`, bei null Zweigen 100)
   und daneben die Zeilen, oder die gemeinsame Quote bewusst wählen: dann heißt die Funktion
   `abdeckung`, und der Organisationsentwickler nennt die Kennzahl in DoD 1 so. Die Wahl
   trifft, wer DoD 1 verantwortet; ich empfehle die Zweigquote, weil sie die Lücke aus
   Befund 2 zeigt. Scheiter-Test: Probe mit vielen gedeckten Zeilen und einem nicht
   geprobten Zweig ist rot.
3. Mit `percent_covered_display` vergleichen und melden, oder abrunden statt runden.
