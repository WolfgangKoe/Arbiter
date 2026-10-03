# AUF-2.4 gehört zu den Sperren, nicht zur Ausgangslage

110 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · offen

## Runde 1
**Befund.** Item 1 ([ausgangslage-only-war](../../domaene/items/ausgangslage-only-war.md))
enthält AUF-2.4: Die *Aufstellungszonen* sind 9″-Bänder an gegenüberliegenden langen
*Spielfeldkanten*. Beobachten lässt sich das nur über eine *Stelle*: Eine *Base*, die von der
Kante bis 9″ reicht, liegt *ganz in* der Zone, eine, die darüber ragt, nicht. Wie eine
*Stelle* angegeben wird und womit gerechnet wird, lege ich laut Plan erst nach dem
Wegwerf-Versuch vor Item 2 fest. Heute ist eine `Aufstellungszone` nur ein Name (`erste`,
`zweite`) ohne Fläche.

**Kosten.** Der Testautor hat für AUF-2.4 in Item 1 zwei Wege, beide schlecht:
- Er wartet auf den Wegwerf-Versuch; dann ist Item 1 nicht mehr allein machbar, obwohl der
  Plan sagt „Reicht der Zyklus nur für eins, kommt Item 1 allein“.
- Er fragt die Zone nach ihren Koordinaten (etwa „Rechteck von y = 0 bis y = 9“). Dann legt
  der Test ein Koordinatensystem fest, bevor es entschieden ist, und prüft dieselbe Aussage
  ein zweites Mal neben AUF-3.2, das sie über *Stellen* prüft. Ändert sich die Darstellung,
  bricht ein Test, obwohl sich das Verhalten nicht ändert.

**Gegenvorschlag.** AUF-2.4 wandert in Item 2
([sperren-beim-setzen](../../domaene/items/sperren-beim-setzen.md)), neben AUF-3.2, das
die Zone als einzige Anforderung benutzt. Dann ist der Schnitt sauber: Item 1 sind nur Daten
(*Armeen*, *Bases*, *Spielfeld*, Anfangszustand), Item 2 die ganze Geometrie, nach dem
Wegwerf-Versuch. Kosten: zwei Zeilen in den Items und ein Satz im Plan; der Umfang des
Zyklus bleibt gleich.
