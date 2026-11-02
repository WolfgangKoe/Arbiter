# Plan 10: drei Kriterien am falschen Item, Kosten von Item 3

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält die Freigabe von Plan 10 auf, weil sonst ein Test sein Kriterium nicht
prüft oder nicht zu schreiben ist ([Kritik](../../prozess/ablauf/kritik.md)):
1. [BEW-8.4](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md) verlangt
   „ohne BEW-3.1 und 6.2 (auch in BEW-17)“. BEW-17 entsteht erst in Item 3, BEW-8.4 steht nur
   in [Item 1](../../domaene/items/anhaltenUebergehen.md). Der Testautor schreibt in Item 1
   entweder einen Test, der bis Item 3 rot bleibt, oder lässt den Teil weg; dann gilt
   BEW-8.4 als belegt, und den Teil prüft nie jemand.
2. Zwei Kriterien haben in Etappe 2 keinen erreichbaren Fall:
   - [AUF-12.8](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md) (Item 2):
     Beim Ziehen rückt AUF-26.1 das *Modell* in die eigene *Aufstellungszone*; die Zonen von
     Only War liegen 26″ auseinander (`domaene/daten/onlyWar.yaml`: 44″ breit, je 9″ tief).
     Kein *Modell* kommt so in *Nahkampfreichweite* (1″), QUE-1.3 sperrt beim Loslassen nie.
   - [BEW-21.1](../../domaene/anforderungen/phasen/bewegung/sperreBeimLoslassen.md) (Item 3):
     Nach Item 3 sperrt QUE-1.2 nur, wenn eine *Base* schon vor dem Ziehen eine fremde
     *überdeckt*; das macht erst AUF-27 möglich (Etappe 7), so steht es in „Am Bildschirm“.
     QUE-1.3 bliebe nur nach BEW-8.4 (ein *Modell* in *Nahkampfreichweite* wird wieder
     gezogen), und dort verlangt BEW-8.3 das Gegenteil: übergehen anbieten, keinen *Grund*.
   Ein Test müsste den Zustand erfinden, den Arbiter nie herstellt (Absicht 1: Tests, die
   wirklich prüfen).
3. Item 3 ist technisches Neuland, der Plan sagt das nicht. AUF-29.1, 29.2 und BEW-17 rechnen
   ab der zuvor gezeigten *Stelle*, also je Bewegung des Zeigers; heute rechnet Arbiter jede
   Abfrage ab der *gesetzten* *Stelle* ([Vertrag Aufstellen, Ziehen](../../technik/architektur/vertrag/aufstellen/ziehen.md),
   „nur für das erste Weiterrücken“, Anliegen 2180). Dazu lässt die Seite Zwischenpunkte
   aus, solange eine Abfrage läuft (`technik/frontend/bedienung.js`, `wartenderPunkt`). Mit
   Entlanggleiten hinge die *Stelle* dann vom Tempo des Servers ab: Dieselbe Bewegung der Maus
   kann die Boyz an verschiedenen Punkten einer *Base* enden lassen.

**Kosten.** 1 und 2: je eine Zeile in den Items, keine Zeile Code. Bleiben sie, wartet Item 1
auf Item 3 oder trägt einen halben Test, und Items 2 und 3 enthalten je ein Kriterium, das
kein Test ehrlich grün macht. 3: Item 3 ändert den Vertrag zwischen Seite und Backend in
beiden Phasen; ich rechne mit etwa doppelt so viel Token wie Item 1 und 2 zusammen. Ich
mache zuerst einen Wegwerf-Versuch (die Seite schickt die zuletzt gezeigte *Stelle* mit,
jede Abfrage wartet auf die vorige), dann den Vertrag; das liegt im Schritt „Architekt:
Vertrag zu Item anhaltenAufDemWeg“.

**Gegenvorschlag.**
1. Item 1: „BEW-8.4 ohne BEW-17“; Item 3: „BEW-8.4 in BEW-17“.
2. AUF-12.8 aus Item 2 und BEW-21.1 aus Item 3 in
   [Randfälle des Aufstellens](../../domaene/items/randfaelleDesAufstellens.md) (Etappe 7,
   neben AUF-27); der Anforderungsautor setzt bei beiden „(Etappe 7)“. Den Widerspruch mit
   BEW-8.3 führe ich in Anliegen 10201.
3. Unter „Empfehlung“ ein Satz: Item 3 ist Neuland, der Architekt prüft es vor den Tests mit
   einem Wegwerf-Versuch; geht es nicht wie gedacht, kommt ein Anliegen vor dem Vertrag.

**Stellungnahme.** Umgesetzt: 1 in beiden Items; 2 im Item randfaelleDesAufstellens,
„(Etappe 7)“ in Anliegen 10162; 3 im Plan unter
„Empfehlung“ und in den Kosten von Anliegen 10160 F1.
BEW-9.2 und BEW-22.1 stehen im Item zuruecksetzenUndLuecken. 10162 ist erledigt: AUF-12.8
und BEW-21 tragen Etappe 7.
