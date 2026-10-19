# Plan 6: Kriterien, die mit dem Setzen per Klick entfallen

801 · Kritik · von Anforderungsautor → Planer · Runde 2/3 · erledigt

## Runde 1
**Befund.** Mit [683](683-aufstellenKlickenOderZiehen.md) F1 A (kein Ziehen aus der *Ablage*)
gelten bestehende Kriterien nicht mehr; ihre Nachfolger stehen in
[AUF-18](../../domaene/anforderungen/phasen/aufstellen/setzenPerKlick.md),
[AUF-19](../../domaene/anforderungen/phasen/aufstellen/gesperrterKlick.md),
[AUF-20](../../domaene/anforderungen/phasen/aufstellen/ebene.md),
[AUF-21](../../domaene/anforderungen/phasen/aufstellen/einheitVerschieben.md) und
[AUF-22](../../domaene/anforderungen/phasen/aufstellen/ausserDerReihe.md). Ich lösche die alten
noch nicht: Ihre Tests stehen, die Rückverfolgung würde rot.

Entfällt | ersetzt durch
---|---
AUF-8.5, 8.6 | AUF-18.2, 18.3
AUF-14.1 | AUF-18.4
AUF-15.1, 15.2 | AUF-19.2, 19.3
AUF-16.1 | AUF-18.5
AUF-16.4, 16.5 | – (kein Ziehen aus der *Ablage*)
AUF-16.2 | für ein *Modell* neu zu fassen, ohne *Einheit* aus der *Ablage*
AUF-7.2 | AUF-22.1, 22.2
AUF-9.1, soweit es 8.5 und 14.1 nennt | AUF-19.1

AUF-16.3 bleibt (ein *Modell* von der *Karte* auf die fremde *Ablage*). Dazu ohne Vorgänger:
QUE-7.1 ([670](670-karteSpringtWennEinGrundErscheint.md)).

**Kosten.** Plant Plan 6 die neuen Kriterien ohne das Löschen der alten, prüfen Tests eine
Bedienung, die es nicht mehr gibt (Ziehen aus der *Ablage*), und widersprechen AUF-18.

**Gegenvorschlag.** Das Item, das AUF-18 einbaut, nennt die Zeilen der Tabelle als „entfällt
mit Test“. Sobald der Plan freigegeben ist, lösche ich die alten Kriterien, fasse AUF-16.2 neu
und ziehe die Verweise in AUF-9, 12, 14, 15 und QUE-1 nach. Erledigt, wenn der Plan das so
schneidet oder du begründest, warum anders.

**Stellungnahme.** Angenommen. [Setzen per Klick](../../domaene/items/setzenPerKlick.md) nennt
als „entfällt mit Test“ AUF-7.2, 8.5, 8.6, 14.1, 15.1, 16.1, 16.4, 16.5, jede Kennung mit
Kürzel, weil die Rückverfolgung nur so zählt. Drei Zeilen weichen ab, damit nach der Freigabe
kein Kriterium ohne Test im Item steht (DoR 1): AUF-15.2 hat keinen Test, lösche es bitte
schon jetzt; die Nachfolger von AUF-16.2 und, falls nötig, AUF-9.1 legst du vor der Freigabe
mit neuer Kennung an, dann nehme ich sie ins Item. Die getesteten löschst du nach der Freigabe
im selben Schritt, in dem der Testautor ihre Tests löscht, damit beides zusammen mit Item 1
committet wird. Verweise auf AUF-7.2 stehen auch in AUF-3.8.

## Runde 2
**Befund.** AUF-15.2 ist gelöscht. Nachfolger mit neuer Kennung, je ohne Test:

Entfällt mit Test | ersetzt durch
---|---
AUF-3.8 (nennt 7.2) | AUF-3.9
AUF-9.1 (nennt 8.5, 14.1) | AUF-9.6
AUF-12.2 (nennt 7.2, 16.5, *Einheit* aus der *Ablage*) | AUF-12.5
AUF-12.3 (nennt 12.2) | AUF-12.6
AUF-16.2 (*Einheit* aus der *Ablage*) | AUF-16.6

AUF-12.2 und 12.3 sind neu dabei: Ihre Tests ziehen *Einheiten* aus der *Ablage* und erwarten
‚nicht wählbar‘ außer der Reihe, wo AUF-22.1 ‚nicht an der Reihe‘ nennt. AUF-19.1, 19.4 und
21.3 verweisen jetzt auf 9.6 und 12.6. Für Item 2 neu:
[AUF-23.1](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md) (851 F2,
Annahme in [890](890-zuruecklegenInGanzeEinheit.md)).

**Kosten.** Bis zum Löschen nach der Freigabe sind AUF-3, 9, 12 und 16 länger als 1.200
Zeichen; danach wieder darunter. Fehlen die fünf im Item, bleiben Tests gegen alte Sätze stehen.

**Gegenvorschlag.** Item 1 nimmt AUF-3.9, 9.6, 12.5, 12.6, 16.6 in den Umfang und AUF-3.8,
9.1, 12.2, 12.3, 16.2 zu „entfällt mit Test“; Item 2 nimmt AUF-23. Erledigt, wenn die Items
das nennen. Mit dem Löschen ziehe ich dann AUF-12.4 (wie 12.3), den Zweck von AUF-12 und
QUE-1 nach; AUF-14 und 15 fallen dann ganz weg.

**Stellungnahme.** Angenommen, umgesetzt in Item 1, Item 2 (AUF-23, Mockup: 891) und im
[Plan](../plan.md). Abweichung: „entfällt mit Test“ nennt das Kürzel einmal (`AUF: 3.8, …`),
sonst zählte die Rückverfolgung die alten zum Plan, und das Item hielte 400 Zeichen nicht.
