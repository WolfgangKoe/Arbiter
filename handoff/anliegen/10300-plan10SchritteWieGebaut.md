# Plan 10: Schritte 2 und 6 und die Empfehlung beschreiben anderes, als gebaut wird

Form: Kritik
Von: Fachkritiker
An: Planer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält die Freigabe auf: Der Stakeholder gibt frei, „wenn Schritte 1 bis 7 deinem
Bild entsprechen“. Drei Stellen geben ihm ein anderes Bild als die Kriterien
([Wir 5](../../prozess/praemissen/wir.md)). Sonst passt der Plan zur
[Etappe](../../domaene/etappen/02-bewegen.md): Jedes Kriterium der Etappe 2 ohne Test steht in
einem der sechs Items.
1. Schritt 6: „„Phase beenden“ nur dem *Spieler* *am Zug*“.
   [QUE-11.1](../../domaene/anforderungen/querschnitt/phaseBeenden.md) bietet es an, solange
   ein *Spieler* *am Zug* ist, also nicht vor dem *ersten Zug* und nicht nach dem Ende der
   *Schlacht*. An einem Gerät gibt es keinen Knopf, den nur einer der beiden bekommt.
2. Schritt 2: „Zieht ihr sie weiter, hält Arbiter sie wieder an.“ Nach
   [BEW-25.1](../../domaene/anforderungen/phasen/bewegung/weiterziehenNachDemUebergehen.md)
   bewegen sie sich gar nicht mehr, auch nicht zurück oder vom Gegner weg: Arbiter hält sie
   an ihrer *Stelle* an und bietet wieder „gemeinsam übergehen“ an. An ihren Ausgangspunkt
   kommen sie mit „Einheit zurücksetzen“ (BEW-24). Das folgt dem Regeltext
   (`core_rules.txt:739`, `:745`), der Stakeholder sollte es aber so lesen, bevor er freigibt.
3. Empfehlung und „Offene Anliegen“ verlangen noch seine Antwort auf
   [10240](10240-baseDesWeirdboys.md); er hat sie gegeben (A, 50 mm).

**Kosten.** Je ein Satz im Plan, keine Zeile Code. Bleibt 1 oder 2, gibt der Stakeholder ein
Bild frei, das Arbiter nicht zeigt, und sucht es im Review 10 vergeblich; bleibt 3, sucht er
eine Frage, die es nicht mehr gibt.

**Gegenvorschlag.**
1. Schritt 6: „… „Phase beenden“ erst ab dem *ersten Zug* und nicht mehr nach dem Ende der
   *Schlacht*. (Item 5)“
2. Schritt 2, letzter Satz: „Zieht ihr sie danach noch einmal, bleiben sie stehen, auch wenn
   ihr sie zurückzieht, und Arbiter bietet wieder „gemeinsam übergehen“ an; an ihren
   Ausgangspunkt bringt sie „Einheit zurücksetzen“ (Schritt 6).“ Ändert
   [10320](10320-bew25UndBew18Pruefbar.md) Punkt 1 BEW-25.1, passt du den Satz an.
3. Die Empfehlung ohne 10240; „An dich: 10240“ entfällt.

**Stellungnahme.** Umgesetzt in [Plan 10](../plan.md): 1 in Schritt 6 („nur vom *ersten
Zug* bis zum Ende der *Schlacht*“), 2 in Schritt 2 nach deinem Gegenvorschlag, gekürzt auf
die Längengrenze; 10320 Punkt 1 ändert daran nichts, solange BEW-25.1 an der vorigen *Stelle*
anhält, sonst passe ich ihn an. 3: Die Empfehlung nennt 10240 nicht mehr, „An dich“ entfällt.
