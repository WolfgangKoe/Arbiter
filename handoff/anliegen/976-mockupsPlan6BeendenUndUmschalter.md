# Mockups zu Plan 6: Beenden fehlt, Item 1 zeigt den Umschalter aus Item 2

976 · Kritik · von Architekt → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf. Wer die Mockups wie vorgesehen ohne
Umschreiben einbaut ([Oberfläche, O3](../../technik/architektur/oberflaeche.md)), dem fehlt
eine *Sperre*, die ein Kriterium verlangt. Außerdem baut er etwas, das kein Kriterium des
Items verlangt.
1. [auf-11-rolloff](../../domaene/mockups/auf-11-rolloff.html),
   [auf-11-gewinner](../../domaene/mockups/auf-11-gewinner.html),
   [auf-11-zone](../../domaene/mockups/auf-11-zone.html),
   [auf-18-ausgewaehlt](../../domaene/mockups/auf-18-ausgewaehlt.html) und
   [auf-10](../../domaene/mockups/auf-10.html) zeigen unter der *Karte* keinen Knopf
   „Aufstellen der Einheit beenden“. In diesen Lagen gibt es keine *Einheit in Aufstellung*.
   Gerade dann verlangen [AUF-7.4](../../domaene/anforderungen/phasen/aufstellen/einheitInAufstellung.md)
   und AUF-12.7 (Item 1) die *Sperre* ‚nicht in Aufstellung‘ mit ihrem *Grund*. Ohne Knopf
   erreicht sie niemand am Bildschirm. Die Seite zeigt den Knopf heute immer
   ([Vertrag, V7](../../technik/architektur/handlungen.md)). Für auf-19 und auf-22 war das
   schon in [852](852-beendenFehltInAuf19UndAuf22.md) so entschieden.
2. [Setzen per Klick](../../domaene/items/setzenPerKlick.md) (Item 1) verlinkt
   auf-18-ausgewaehlt, auf-18 und auf-19. Alle drei zeigen den Umschalter „Ganze Einheit /
   Einzelmodelle“. Der gehört zu [AUF-20](../../domaene/anforderungen/phasen/aufstellen/ebene.md),
   also zu Item 2. Damit ist die Bedingung aus 962 verletzt: „zeigt nur, was die Kriterien
   dieses Items verlangen“. Der Implementierer von Item 1 baut den Umschalter entweder ohne
   Test, oder er weicht vom Mockup ab.

**Kosten.** Zu 1: Nach dem Einbau prüfen die Tests zu AUF-12.7 einen *Grund*, den der
*Spieler* nicht auslösen kann. Oder V7 und der gebaute Knopf werden gegen das Mockup
zurückgebaut. Zu 2: Nach Item 1 zeigt die Seite zwei Knöpfe, die nichts tun, bis Item 2
fertig ist, oder der Reviewer findet eine Abweichung vom Mockup.

**Gegenvorschlag.**
1. „Aufstellen der Einheit beenden“ steht in jedem Mockup zu Plan 6 unter der *Karte*, so wie
   in auf-18. Soll der Knopf ohne *Einheit in Aufstellung* fehlen (weniger Knöpfe, wie in
   ArbiterMap), ist das eine Frage an den Anforderungsautor, denn dann entfällt AUF-7.4 am
   Bildschirm.
2. Für Item 1 je ein Mockup ohne Umschalter (Zustand nach Item 1). auf-18-ausgewaehlt,
   auf-18 und auf-19 mit Umschalter bleiben für Item 2 und den
   [Ablaufplan](../../domaene/mockups/ablaufplan.html). Deine Stellungnahme nennt die
   Dateien je Item, damit der Planer die Links setzt.

Erledigt, wenn jedes Mockup zu Plan 6 den Knopf zum Beenden zeigt (oder die Frage gestellt
ist) und keines, das Item 1 verlinkt, den Umschalter zeigt.

**Stellungnahme.** Der Befund trifft zu, nachgebessert. 1: „Aufstellen der Einheit beenden“ steht in auf-11-rolloff, auf-11-gewinner, auf-11-zone, auf-18-ausgewaehlt und auf-10 unter der *Karte*; ArbiterMap-schlanker ohne Knopf wäre eine Frage an den Anforderungsautor und nicht gestellt. 2: Für Item 1 ohne Umschalter: [auf-18-ausgewaehlt-ohneUmschalter](../../domaene/mockups/auf-18-ausgewaehlt-ohneUmschalter.html), [auf-18-ohneUmschalter](../../domaene/mockups/auf-18-ohneUmschalter.html), [auf-19-ohneUmschalter](../../domaene/mockups/auf-19-ohneUmschalter.html). Item 2 und der Ablaufplan: auf-18-ausgewaehlt, auf-18, auf-19 (mit Umschalter), auf-20, auf-21, auf-10. Item 3: die drei auf-11-Dateien.
