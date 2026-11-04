# Fliegen: Tests zu 18.2 und 18.3 mit Warboss und Weirdboy statt eines Boys

Form: Kritik
Von: Testautor
An: Architekt
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält den Happy Path nicht auf. Der [Vertrag Fliegen](../../technik/architektur/vertrag/bewegung/fliegen.md),
Absatz „Prüft“, nennt für 18.2 „neben einem Boy“ und für 18.3 „durch die
*Nahkampfreichweite* eines Boys gezogen“. Die Tests in
[fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py) weichen ab:
1. Statt eines Boys steht der Warboss neben der Spinne
   (`testBew18_2NebenEinemModellDesAnderenSpielersRücktArbiterDieSpinneNichtInDieNahkampfreichweite`,
   beide Tests zu 18.3). Warum: Ein einzelner Boy, der zur Spinne gezogen wird, verlässt die
   *Kohärenz* seiner *Einheit*; ‚keine Kohärenz‘ lässt sich nicht übergehen (`domaene/ziel.md`).
   Der Warboss ist eine *Einheit* aus einem *Modell*.
2. Im Test „Ende darin“ zu 18.3 steht zusätzlich der Weirdboy an der Strecke, vor dem Warboss.
   Warum: Ohne ihn hielte schon BEW-6.2 die Spinne an derselben *Stelle* an wie 18.3; der Test
   wäre vor dem Code grün. Mit ihm hält 6.2 vor dem Weirdboy an, 18.3 erst vor dem Warboss.
3. Zu 18.4 steht ein Test mehr als im Vertrag: nach dem Übergehen rückt Arbiter die Spinne auch
   in die *Nahkampfreichweite* des Warboss („ohne 6.2“).

**Kosten.** Drei Halbsätze im Absatz „Prüft“; im Code nichts.

**Gegenvorschlag.** „Prüft“ nennt den Warboss statt eines Boys, für 18.3 „Ende darin“ den
Weirdboy davor, für 18.4 die *Nahkampfreichweite* des Warboss. Hältst du den Boy für nötig,
nenne, wie er ohne Bruch der *Kohärenz* an die Stelle kommt.

**Stellungnahme.** 1 und 2 umgesetzt im Absatz „Prüft“ des
[Vertrags](../../technik/architektur/vertrag/bewegung/fliegen.md): Warboss statt Boy, mit dem
Grund; für 18.3 „Ende darin“ der Weirdboy davor. Nachgerechnet: Die Strecke führt durch seine
*Nahkampfreichweite*, 6.2 allein hielte vor ihm an, 18.3 erst vor dem Warboss. Dazu passt
„Prüft“ jetzt die Ebene der Tests an: Am Dienst nur 18.1 (nur V10 ändert seine Antwort),
18.2 und 18.3 an `Schlacht`, 18.2 auch an der *Spielfeldkante*. 3 nicht übernommen: Nach der
Antwort des Stakeholders in [13010](13010-fliegenNachDemUebergehen.md) gelten *Bewegungsweite*
und *Nahkampfreichweite* auch nach dem Übergehen; der Test „auch in die
*Nahkampfreichweite*“ widerspricht ihr. „Prüft“ nennt für 18.4 nur noch 13010; die Tests zu
18.4 folgen der neuen Fassung von BEW-18.4.
