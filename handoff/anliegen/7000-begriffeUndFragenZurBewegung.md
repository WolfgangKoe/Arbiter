# Begriffe und Fragen zur Bewegungsphase in Plan 9

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 1/3
Status: rückfrage

## Runde 1
**Befund.** Zum Zyklusziel aus [Review 8](../review.md) stehen neu
[BEW-5](../../domaene/anforderungen/phasen/bewegung/vorruecken.md) bis
[BEW-10](../../domaene/anforderungen/phasen/bewegung/fremdeModelle.md). Drei Stellen sagen
Regeltext und Ziel nicht eindeutig.

Neue Begriffe, Freigabe mit Plan 9: *Vorrücken* (Advance, `core_rules.txt:754`), *Vorrückwurf*
(Advance roll, `:754`), wie du „vorgerückt“ in Anliegen 5180 F5 sagtest. Für Anliegen 4881:
Datenblatt (datasheet, `:552`), Profil (profile, `:561`), Modellart (eine Zeile des Profils, `:562`).

**Kosten.** Ohne Antwort baut Plan 9 nach den Annahmen unten.

**Gegenvorschlag.** Je Frage antworten; „.“ heißt, die Empfehlung gilt.

**F1 · Was heißt „jede Einheit nur einmal“?** A: Jede *Einheit* macht in der
*Bewegungsphase* eine *Normale Bewegung* oder *Vorrücken*; korrigieren bleibt erlaubt, die
*Distanz* zählt vom Beginn der Phase, BEW-1.6 bleibt (Anliegen 5180 F5, Etappe 2). B: Nach dem
Ziehen einer anderen *Einheit* sperrt die erste mit ‚schon bewegt‘ (Regeltext `:734`).
Empfehlung: A. So hast du es in 5180 F5 beschrieben; B bricht BEW-1.6 und ließe eine
*Einheit* ohne *Kohärenz* stecken, bis das Zurücksetzen kommt.
Annahme: A, kein Kriterium ‚schon bewegt‘.
Antwort: Ich bin mir nicht sicher, ob ich die Frage richtig verstehe. Ich wähle eine Einheit aus, entscheide dann, ob sie sich normal bewegt oder vorrückt (darum ein Button unten), befindet sie sich in Nahkampfreichweiter feindlicher Modelle, wird ein zurückziehen-Button angeboten. Es braucht dann eben noch eine UX-Darstellung, wie die Zustände der Einheiten angezeigt werden (z.B. wie in Arbiter-old)

**F2 · Ein Anhalten (Bewegungsweite, Kante, Nahkampfreichweite) gemeinsam übergehen?**
A: In Plan 9 nicht; *gemeinsam übergehen* nur bei einer *Sperre* (BEW-8) (Anliegen 5180 F6 A).
B: Beim Anhalten nennt Arbiter den *Grund* und bietet *gemeinsam übergehen* an; dann steht
das *Modell*, wo du loslässt (Anliegen 5180 F2, Ziel). Empfehlung: A jetzt, B in einem
späteren Zyklus von Etappe 2; der Happy Path braucht es nicht.
Annahme: A.
Antwort: .

**F3 · Was zeigt Arbiter an einer gezogenen Einheit?** A: nichts Neues in Plan 9 (Absicht 3).
B: je *Einheit* des *Spielers* *am Zug*, wie sie sich bewegt hat und wie weit, dazu jedes
*Modell* ohne *Kohärenz* (ArbiterMap `model_selection.js:443`, `rule_check_overlay.js:19`,
Anliegen 5180 F1). Empfehlung: A jetzt, B mit dem Zurücksetzen; wo es steht, zeigt dann ein
Mockup.
Annahme: A.
Antwort: .

**Stellungnahme.**
Kommentar: Ich habe im Mockup mehrere Buttons mit "vorrücken" gesehen. Ich verstehe die Absicht dahinter nicht. Nach meinem Dafür halten braucht es da nur einen Button, nachdem eine Einheit gewählt wurde. Einzelne Modelle in einer Einheit können nicht vorrücken, ohne dass auch alle anderen Modelle vorrücken, falls das die IDee war. Das Vorrücken muss rückgängig gemacht werden können. Beachte auch die Auswahl des jeweiligen Kreises, wie ich es in einem anderen Anliegen beschrieben habe
