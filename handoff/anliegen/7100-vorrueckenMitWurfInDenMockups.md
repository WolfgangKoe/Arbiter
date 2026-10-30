# Mockups bew-1, bew-2, bew-8 zeigen „Vorrücken mit 1“ bis „Vorrücken mit 6“

Form: Kritik
Von: Architekt
An: Ux
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Plan 9, Schritt 5; die Mockups sind die Vorlage für Items 2 und 3,
die jetzt gebaut werden). [bew-1](../../domaene/mockups/bew-1.html),
[bew-2](../../domaene/mockups/bew-2.html) und [bew-8](../../domaene/mockups/bew-8.html)
zeigen in der `knopfGruppe` sechs Knöpfe „Vorrücken mit 1“ bis „Vorrücken mit 6“. Das
widerspricht [BEW-5](../../domaene/anforderungen/phasen/bewegung/vorruecken.md): Arbiter
bietet einen Knopf „Vorrücken“ an (5.1), danach wartet die *Einheit* auf ihren
*Vorrückwurf* (5.2), den ein Klick auf einen der sechs *Grenzkreise* aus BEW-13.1 festlegt
(5.3). So zeigt es schon [bew-5](../../domaene/mockups/bew-5.html). Die Knöpfe stammen aus
dem Stand vor Anliegen 6998 F1; BEW-5 ist richtig, die drei Mockups sind veraltet. Der
Stakeholder dazu: „Ich sehe schon, dass bei den Mockups aufgeräumt werden muss, damit es
keine Verwirrung gibt.“ Die übrigen überholten Mockups halten nicht auf:
[7101](7101-mockupsNachDerDoDUndOhneItem.md), Zeitpunkt: [7102](7102-mockupsJetztAufraeumen.md).

Am Bildschirm hieße das: Baut der Implementierer Item 3 ([anhaltenUndAuswahl](../../domaene/items/anhaltenUndAuswahl.md))
nach bew-1 und bew-2 ein, wie die Mockups es verlangen („ohne Umschreiben“), steht nach dem
Auswählen der Boyz eine Reihe von sechs Knöpfen unter der *Karte*, die du nicht verlangt
hast und die BEW-5 nicht kennt; Schritt 5 des Plans („Vorrücken“ klicken, dann in den Ring
des Wurfs) passt nicht dazu. Für bew-8 (Item 2) fängt der
[Vertrag](../../technik/architektur/vertrag/schlacht/uebergehen.md) das nur ab („die Knöpfe ‚Vorrücken
mit <n>‘ gelten nicht“), für bew-1 und bew-2 steht kein solcher Satz.

**Kosten.** Klein: je Mockup sechs Zeilen. Unterbleibt es, bauen Items 2 und 3 nach einer
Vorlage, die BEW-5 widerspricht, und der Stakeholder beurteilt sie gegen ein Bild, das nicht
gilt; Item 4 müsste die Knöpfe wieder entfernen. Nach der Berichtigung streiche ich den
Notbehelf im Vertrag (eine Aussage, [Wir 3](../../prozess/praemissen/wir.md)).

**Gegenvorschlag.** In bew-1, bew-2 und bew-8 die sechs Knöpfe „Vorrücken mit <n>“ durch
einen Knopf „Vorrücken“ ersetzen, wie in bew-5: In allen dreien sind die Boyz *ausgewählt*
und weder *vorgerückt* noch wartend, also bietet BEW-5.1 ihn an. „gemeinsam übergehen“ und
„Phase beenden“ bleiben.

**Stellungnahme.** Angenommen. In [bew-1](../../domaene/mockups/bew-1.html),
[bew-2](../../domaene/mockups/bew-2.html) und [bew-8](../../domaene/mockups/bew-8.html)
ersetzt ein Knopf „Vorrücken“ die sechs Knöpfe „Vorrücken mit <n>“ (BEW-5.1);
„gemeinsam übergehen“ und „Phase beenden“ bleiben.

**Nachprüfung.** In Ordnung: bew-1, bew-2 und bew-8 zeigen je einen Knopf „Vorrücken“ vor
„Phase beenden“, „Vorrücken mit <n>“ steht in keinem Mockup, keiner Anforderung und keinem
Item mehr. Den Notbehelf im Vertrag habe ich gestrichen:
[Gemeinsam übergehen](../../technik/architektur/vertrag/schlacht/uebergehen.md) verweist für
„Vorrücken“ auf die *Grenzkreise*.
