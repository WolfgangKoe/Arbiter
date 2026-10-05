# Drei Fälle von AUF-4 fehlen

252 · Kritik · von Fachkritiker (Domäne) → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von c007cfc (Kriterium). QUE-2.1 bis QUE-2.6 und AUF-4.2 bis
AUF-4.7 treffen ihr Kriterium, die Namen stehen im Glossar, keiner verlangt mehr als
Kriterium und Plan. Rot sind sie aus dem richtigen Grund: `arbiter.web` fehlt, und der Befehl
nennt keine Adresse. In `auf4Test.py` fehlen drei Fälle, die das Kriterium regelt:
1. AUF-4.6, „vor der Wahl nach AUF-1.1 in keiner der beiden“: Gemeint ist die Wahl der
   *Aufstellungszone*, also auch nach der Wahl des *Gewinners* allein (Lesart bestätigt in
   [244](244-nameDerEinheitFehltImGlossar.md), Stellungnahme). `…VorDerWahlZeigtDieKarteKeineZone…`
   prüft nur die *Ausgangslage*. Ein Bau, der die Zonen schon nach `gewinnerWählen` färbt,
   etwa den *Gewinner* in der ersten, bliebe grün.
2. AUF-4.5, „In der *Ablage* ist die *Einheit in Aufstellung* gekennzeichnet, solange es eine
   gibt“: geprüft nur mit 0 *gesetzten* *Modellen* und nur in der *Ablage* von Spieler 1. Es
   fehlt
   a) die *Einheit in Aufstellung* von Spieler 2, gekennzeichnet in seiner *Ablage*, nicht
      in der von Spieler 1;
   b) die *Einheit in Aufstellung* mit *gesetzten* *Modellen*, auch mit allen: Sie bleibt
      nach AUF-4.3 in der *Ablage* und ist bis zu *Aufstellen der Einheit beenden* *Einheit
      in Aufstellung*. Ein Bau, der das Abzeichen nur zeigt, solange kein *Modell* *gesetzt*
      ist, oder nur links, bliebe grün.
3. AUF-4.3, „Je *Spieler* zeigt Arbiter eine *Ablage*“, im Glossar „jeder *Spieler* hat
   eine“: Dass es genau eine gibt, prüft nur die *Ausgangslage*. Hat ein *Spieler* alle
   *Einheiten* *aufgestellt*, ist seine *Ablage* leer, aber da und nennt ihn (AUF-4.7). Ein
   Bau, der die leere *Ablage* weglässt, bliebe grün.

**Kosten.** Ohne die Fälle kann der Implementierer das Kriterium verfehlen, und es fällt erst
im Review auf, wenn der Stakeholder die Bilder sieht, oder in Etappe 1 beim Wählen und
Setzen. Je Fall ein Parameter oder ein kurzer Test, die Fixtures gibt es schon.

**Gegenvorschlag.**
1. `testAuf4_6VorDerWahl…` über „ausgangslage“ und „nachDerGewinnerwahl“ parametrisieren,
   wie `aufstellungOhneJemandAnDerReihe`.
2. a) Nach `einheitenAufstellen(aufstellungNachDerZonenwahl, 1)` setzt Spieler 2 mit
   `modelleSetzen(…, necronWarriors, 0)`; das Abzeichen steht genau einmal, in der
   *Ablage* von Spieler 2 an den Necron Warriors.
   b) `testAuf4_5DieEinheitInAufstellungIstInDerAblageGekennzeichnet` über die Zahl der
   *gesetzten* *Modelle* parametrisieren: 0, 3, 10.
3. Nach dem Aufstellen aller *Einheiten* (Zustand „nachDerAufstellung“): je *Spieler* genau
   eine *Ablage* mit seinem Namen und ohne `.einheitenKarte`.

Erledigt, wenn die Fälle stehen und aus dem richtigen Grund rot sind.

**Stellungnahme.** Angenommen, alle drei Fälle stehen in `auf4Test.py`:
1. `…VorDerWahl…` läuft über „ausgangslage“ und „nachDerGewinnerwahl“.
2. a) Neuer Test für die *Einheit in Aufstellung* von Spieler 2; b) der Test der Kennzeichnung
   läuft über 0, 3 und 10 *gesetzte* *Modelle*.
3. Neuer Test: nach dem Aufstellen aller *Einheiten* hat jeder *Spieler* genau eine *Ablage*
   ohne `.einheitenKarte`.
