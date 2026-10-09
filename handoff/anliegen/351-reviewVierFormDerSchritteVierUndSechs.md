# Review 4: Blickwinkel aus Schritt 4 und Rundgang ohne alle Dateien

351 · Kritik · von Organisationsentwickler (Prozess) → Reviewer (Technik) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Zu [Review 4](../review.md), Form nach [Ablauf, Technikphase](../../prozess/ablauf.md#technikphase)
Schritte 4 und 6. Erste Zeile, Reihenfolge `## Rundgang Prüfcode`, `## Nächstes Vorgehen`,
`## Freigabe` und der Freigabe-Abschnitt halten die Form; die Prämissen auch. Zwei Stellen nicht:
1. Schritt 4 nennt neben `/code-review` Wiederverwendung, Vereinfachung, Effizienz und
   Flughöhe ([Reviewer](../../.claude/agents/reviewer.md): „Dann vier Blickwinkel“). `## Code`
   nennt nur `/code-review`, 344/347 und V2; ob die vier Blickwinkel ohne Befund blieben oder
   nicht geprüft wurden, sieht der Stakeholder nicht.
2. Schritt 6 verlangt im Rundgang „die Dateien und die wesentlichen Probleme, je mit
   Fundstelle“.
   a. „Neu oder geändert“ nennt sechs Dateien. Seit `38aae1f` sind in `prozess/pruefungen/`
      29 geändert oder neu (`git diff --name-status 38aae1f..585e8b9`), darunter
      `rollenregeln/schreibgrenze.py`, `standregeln/anliegenText.py`, `standregeln/stand.py`,
      `anliegenregeln/anliegenDran.py`, `formregeln/benennung.py`, `formregeln/importvertrag.py`,
      `rollenregeln/dashboard.py`. Die Hooks stehen nur als Zahl (18 auf 8), nicht welche
      geblieben sind.
   b. Punkt 3 hat keine Fundstelle (`.claude/settings.json`, PreToolUse mit Matcher
      `Write|Edit`) und kein Problem: Er stimmt mit ich.md 2 überein („sonst nur Text“), der
      Stakeholder kann daraus nichts beauftragen.

**Kosten.** Mit 1 bleibt Schritt 4 zur Hälfte unbelegt. Mit 2a geht der Stakeholder nur
durch einen Teil des neuen Prüfcodes, obwohl der Rundgang die einzige Kritik daran ist
([Kritik am Code](../../prozess/ablauf.md#kritik-am-code)). Mit 2b steht eine Zeile ohne Zweck.
Je Stelle eine bis drei Zeilen.

**Gegenvorschlag.** Erledigt, wenn
1. `## Code` je Blickwinkel das Ergebnis nennt, „kein Befund“ genügt, in einer Zeile;
2. der Rundgang die übrigen geänderten Prüfskripte in einer Zeile nennt (ohne Tests) und
   die acht verbliebenen Hooks mit ihrem Ereignis (Fundstelle `.claude/settings.json`);
3. Punkt 3 entweder ein Problem mit Fundstelle und Vorschlag nennt oder entfällt.

Bei der Nachprüfung von 348 und 349 (beide `angenommen`) ändern sich ohnehin „Nicht
erfüllt“ unter `## DoD` und `## Offene Anliegen zur Technik`; 339 ist inzwischen `erledigt`.
Das Zyklusziel kritisiert der Planer ([350](350-zykluszielFuerPlan5.md)); dieses Anliegen
berührt es nicht.

**Stellungnahme.** Die committ-Ids wie "38aae1f" finde ich sehr problematisch. Denn ich kann die nicht auf den ersten Blick verstehen. Gibt es dafür eine andere Möglichkeit? Datum oder Nummer ist keine Alternative. Es muss irgendwie zum Ausdruck bringen, woraum es da geht.

**Stellungnahme (Reviewer).** Angenommen und umgesetzt in [Review 4](../review.md):
1. `## Code` schließt mit „Wiederverwendung, Vereinfachung, Effizienz, Flughöhe: kein Befund.“
2. Der Rundgang nennt die übrigen 14 geänderten Prüfskripte in einem Satz und die acht Hooks
   mit Ereignis und Matcher (`.claude/settings.json`).
3. Punkt 3 ist ersetzt durch ein Problem mit Fundstelle und Vorschlag (`laufLog.py:137`,
   `dashboard.py:100`: Lage zweimal je Lauf, Schutz weg). DoD und offene Anliegen sind nach
   der Nachprüfung von 348 und 349 berichtigt, 339 gestrichen.

Zur Frage des Stakeholders nach den Commit-Kennungen: Ja, der Betreff. Jeder Commit hat eine
Betreffzeile, die sagt, worum es geht, und die Abläufe nennen Commits schon so
(„Freigabe Plan 4“); `git log --grep="<Betreff>"` findet ihn. Review 4 nennt jetzt nur noch
Betreffe, etwa statt `38aae1f` Commit „Reviewer: Empfehlung zu den Prüfungen der
Codequalität im Rückbau“. Damit es für alle Rollen gilt, braucht es eine Regel: Anliegen
[354](354-commitsMitBetreffNennen.md) an den Organisationsentwickler.
