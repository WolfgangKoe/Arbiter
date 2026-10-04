# Die Zählregel für Antworten greift im Höchstmaß-Test nicht

190 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von 4f9ce03 ([162](162-antwortenNichtZaehlen.md)).
`testDateiHältIhrHöchstmaß` prüft zwei Dinge: `länge <= grenze` mit der Länge aus `fälle()`,
also für Anliegen `zeichenOhneAntworten`, und danach `not überschreitet(datei, grenze)`.
`überschreitet` zählt mit `zeichen` alle Zeichen samt Antworten. Ein Anliegen mit 3.980
Zeichen eigenem Text und einer Antwort von 500 Zeichen bleibt damit rot. Nachgeprüft: Ich habe
`testDateiHältIhrHöchstmaß` mit genau der Datei aus `anliegenMitAntwort(…, 3980, 500)`
aufgerufen, und die zweite Zusicherung schlägt fehl. Der Fall aus 162 (145 mit 4.063 Zeichen)
wäre heute noch genauso rot.

Die beiden Scheiter-Tests sehen das nicht. Sie rufen nur `zeichenOhneAntworten` auf, nicht
den Weg über `fälle()` und `testDateiHältIhrHöchstmaß`. Der grüne Fall sichert sogar
`überschreitet(datei, anliegen)` zu, also genau die Bedingung, an der die echte Prüfung
scheitert. `python3 -m pytest prozess/pruefungen` ist nur grün, weil im Moment kein Anliegen
mit Antworten über 4.000 Zeichen kommt (das größte, 114, hat 3.982).

Nebenbei: 162 verlangt, dass 3.990 Zeichen grün sind. Mit `\nAntwort: .` (11 Zeichen) kommt
man dabei auf 4.001, also rot. Der Test nimmt deshalb 3.980. Das ist richtig, steht aber
nicht in der Stellungnahme.

**Kosten.** Was 162 verhindern soll, geschieht weiter: Eine ausführliche Antwort des
Stakeholders macht den Commit der Freigabe rot, und eine Rolle kürzt fremden Text. Der
Scheiter-Test meldet dabei grün.

**Gegenvorschlag.**
1. In `testDateiHältIhrHöchstmaß` bleibt nur `assert länge <= grenze, …`. Die zweite
   Zusicherung ist für die anderen Dateien überflüssig (dort ist `länge` gleich
   `zeichen(datei)`), und für Anliegen ist sie falsch.
2. Die Scheiter-Tests gehen den echten Weg. Der grüne Fall ruft
   `testDateiHältIhrHöchstmaß(datei, zeichenOhneAntworten(datei), anliegen)` auf und bleibt
   ohne `pytest.raises`. Der rote Fall ruft dasselbe in `pytest.raises(AssertionError)` auf.
   Noch besser: Die Länge kommt aus derselben Zuordnung wie in `fälle()`, etwa einer Funktion
   `länge(datei)`, damit Test und Lauf nicht auseinanderlaufen. Die Zusicherung
   `überschreitet(datei, anliegen)` im grünen Fall fällt weg. Wird `überschreitet` dann nur
   noch von den drei alten Scheiter-Tests gebraucht, prüfen die direkt `zeichen(…) > grenze`,
   und die Funktion entfällt.
3. In der Stellungnahme steht ein Satz dazu, warum es 3.980 statt 3.990 sind, damit der
   Organisationsentwickler bei der Nachprüfung die Abweichung von seinem Erledigt-Kriterium
   annehmen kann.

Erledigt, wenn ein Anliegen mit 3.980 Zeichen eigenem Text und 500 Zeichen Antwort durch
`testDateiHältIhrHöchstmaß` grün kommt, 4.010 Zeichen dort rot sind und
`python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.** Umgesetzt nach Gegenvorschlag 1 und 2: nur noch `länge <= grenze`,
`überschreitet` entfernt, beide Scheiter-Tests rufen `testDateiHältIhrHöchstmaß` mit
`zeichenOhneAntworten` auf. 3.980 statt 3.990: die Zeile `Antwort: .` und ihr Zeilenumbruch
zählen mit (11 Zeichen). Die Meldung nennt Dateien außerhalb des Repos mit vollem Pfad.
