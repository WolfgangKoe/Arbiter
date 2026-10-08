# Auswahl: Der Deckel von zwei Einheiten greift in Etappe 1 nie

320 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 1/3 · erledigt

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Ihr habt in 309 F2 B entschieden: je *Spieler* bis zu zwei *ausgewählte*
*Einheiten*, eine dritte verdrängt die älteste (AUF-5.5,
[Aufstellen](../../domaene/anforderungen/phasen/aufstellen.md)). In der *Ausgangslage* hat jede
*Armee* genau zwei *Einheiten* (AUF-2.6,
[ausgangslage.yaml](../../domaene/daten/ausgangslage.yaml)), eine andere kennt Etappe 1 nicht.
Eine dritte *Einheit* desselben *Spielers* gibt es also nie; der Fall ist am Bildschirm, im
Mockup und in Review 4 nicht zu sehen (Kritik
[318](318-dritteEinheitGibtEsNicht.md) des Fachkritikers).

**Kosten.** Ohne Antwort verlangt Item 2 einen Test zu AUF-5.5, für den der Testautor eine
*Armee* mit drei *Einheiten* erfinden müsste; der Code dazu wäre in Etappe 1 ein toter Zweig.

**Gegenvorschlag.** Keiner.

**F1 · Was wird aus AUF-5.5, solange keine Armee mehr als zwei Einheiten hat?**
- A: Es bleibt in Item 2; sein Test verwendet eine *Armee* außerhalb der *Ausgangslage*.
- B: Es bleibt als Kriterium stehen, der Planer nimmt es aus Item 2, bis eine *Ausgangslage*
  eine *Armee* mit mehr als zwei *Einheiten* hat.
- C: Es entfällt; den Deckel fragen wir neu, wenn eine *Armee* mehr als zwei *Einheiten* hat.

Empfehlung B: Eure Entscheidung aus 309 bleibt stehen, niemand erfindet eine *Armee*, und
gebaut wird der Fall erst, wenn ihr ihn sehen könnt.

Antwort: .

**Stellungnahme.**
