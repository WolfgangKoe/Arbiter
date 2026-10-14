# Aufstellen: in die Zone klicken, ziehen oder beides?

683 · Fragen · von Ux → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Dein Test am Bildschirm: Das Ziehen der Karte aus der *Ablage* ist nicht intuitiv.
Du erwartest: *Einheit* in der *Ablage* auswählen, in die *Aufstellungszone* klicken, die *Einheit*
steht dort in *Kohärenz*, dann setzt du sie als Ganzes an die gewünschte *Stelle*; so macht es
ArbiterMap (`deployment.js`, `docs/spec/interaction_map.md`: „Ganze Einheit“, Zeile 360).
Heute: Klick wählt nur aus (AUF-5.3, ohne Handlung); *setzen* geht nur durch Ziehen aus der
*Ablage* (AUF-8.5, 8.6); einzelne *Modelle* lassen sich ziehen (AUF-8.2), die *Einheit* als
Block nicht (Plan 5, „Komfort“). Der Fehler am Spaltenrand beim Ziehen steht in
[682](682-gezogeneKarteVerschwindetAmSpaltenrand.md), das Markieren in
[680](680-markierterTextSperrtDasZiehen.md).

**Kosten.** Ohne Antwort baut keiner die Bedienung, die du erwartest; jede Phase danach
(Bewegen) beginnt mit der Frage „wie greife ich eine *Einheit*“. Anliegen
[681](681-zeigenWasDerSpielerTunKann.md) bleibt offen.

**Gegenvorschlag.** Ich empfehle B.

**F1 · Wie stellt der *Spieler* eine *Einheit* auf?**
- A · Nur klicken, wie ArbiterMap. Auswählen, in die Zone klicken: Die *Formation* steht mittig,
  ragt sie aus der Zone, rückt Arbiter sie hinein (AUF-8.6). Das Ziehen aus der *Ablage* entfällt.
  Ändert: AUF-8.5 neu gefasst (Klick statt Ziehen), AUF-16.1, 16.4, 16.5 entfallen, AUF-5.8 und
  AUF-7.2 gelten für den Klick; neu: *Einheit* als Block verschieben (F2). Betroffen: die
  abgenommenen Items „ziehen“ (AUF-8.5, 8.6, 16.1, 16.2, 16.4) und „gesperrtStehenUndZurueck“
  (AUF-16.5, 15.1); Tests `ziehenTest`, `loslassenOhneZielTest`, `gesperrteFormationTest`
  müssen neu; ein neues Item in Plan 6. Größter Eingriff.
- B · Klicken und Ziehen. Der Klick in die Zone kommt dazu, das Ziehen aus der *Ablage* bleibt;
  die *Einheit* lässt sich als Block verschieben (F2). Ändert: zwei neue Kriterien (Klick
  setzt, Block verschieben), keines entfällt. Betroffen: nur ein neues Item in Plan 6; die
  abgenommenen Tests bleiben. Kleinster Eingriff; du kannst beide Wege prüfen und später einen
  streichen.
- C · Nur Ziehen wie heute, besser erklärt. Hinweis „auf die *Karte* ziehen“ und Greif-Zeiger
  (681), 680 und 682 behoben, Block verschieben neu (F2). Ändert: ein Kriterium für den
  Hinweis, eins für den Block. Betroffen: ein neues Item in Plan 6. Dein Wunsch zu klicken
  bliebe offen.

Antwort: .

**F2 · Wie wählt der *Spieler*, ob Ziehen die ganze *Einheit* oder ein *Modell* verschiebt?**
- a · Umschalter „Ganze Einheit / Einzelmodelle“ wie ArbiterMap (`interaction_map.md:191`).
  Empfohlen: Die Anforderung gibt es dort, sie ist geprüft.
- b · Dein eigener Vorschlag.

Antwort: .
