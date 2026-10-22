# Die Spalte, in der du eine Einheit anklickst, heißt Armeeliste statt Ablage

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Du hast recht: Ein Ort, an dem *Modelle* liegen und in den man sie zurückzieht,
braucht es nicht. Was am Bildschirm bleibt, ist dies: Links und rechts neben der *Karte*
steht je eine Spalte. Oben steht „Spieler 1“ oder „Spieler 2“, darunter je *Einheit* ein
Kästchen mit Namen und Anzahl, etwa „Boyz“ mit 10. Du klickst „Boyz“ an, der Rahmen wird
golden, dann klickst du in deine Zone. Steht eine *Einheit* fertig auf der *Karte*,
verschwindet ihr Kästchen. In den Anforderungen heißt diese Spalte bisher „Ablage“. Das Wort
führt in die Irre.

Die Reserve ist etwas anderes: ein Bereich neben dem Spielfeld für *Einheiten*, die du in
Reserve stellst. Keine Etappe verlangt sie bisher; sie kommt erst, wenn eine Etappe sie
nennt.

**Kosten.** Mit dem alten Wort liest du in Plan und Review etwas, das es nicht gibt.

**Gegenvorschlag.** Die Spalte bekommt einen Namen, der sagt, was sie zeigt.

**F1 · Wie heißt die Spalte?**
- A: „Armeeliste“, wie in Arbiter-old (`Arbiter-old/src/uiLayout/armyList.py`, die ganze
  Seitenleiste) und in ArbiterMap („Armylist“, Item 031).
- B: „Armeekarte“, wie in deiner Skizze „unitSelection (unit- & armyCard)“.

Empfehlung: A. Das Wort *Karte* steht schon für das Spielfeld, „Armeekarte“ ließe sich damit
verwechseln.
Antwort: A

Annahme: A. Bis zur Freigabe des Plans heißt die Spalte im Glossar weiter *Ablage*, neu
beschrieben als Spalte, in der du eine *Einheit* anklickst, und nicht als Ziel zum
Hineinziehen ([Glossar](../../domaene/glossar.md)). Nach deinem Ja:
- Anforderungsautor: *Ablage* wird überall *Armeeliste*, in Glossar und Anforderungen
  (13 Dateien).
- Testautor: Testnamen mit „Ablage“, etwa `testAuf8_4…AufEinerAblage…` in
  `technik/tests/akzeptanz/phasen/aufstellen/ziehenTest.py`.
- Implementierer: Bezeichner `ablage` im Code, etwa `modellAufAblageLoslassen`.
- UX: Beschriftungen in `domaene/mockups/`, die „Ablage“ nennen.

**Stellungnahme.**
