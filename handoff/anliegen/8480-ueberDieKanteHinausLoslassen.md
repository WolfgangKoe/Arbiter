# Über die Spielfeldkante hinaus loslassen in der Bewegungsphase

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: 9760

## Runde 1
**Befund.** Fachliche Abnahme zu Item anhaltenUndAuswahl, wartet nach
[Kritik](../../prozess/ablauf/kritik.md) (Lücke abseits des Happy Path). Die *Karte* endet an
der *Spielfeldkante*. Zieht jemand in der *Bewegungsphase* ein *Modell* an die Kante und der
Zeiger geht dabei über sie hinaus, zeigt die *Karte* das *Modell* an der Kante angehalten
([BEW-6.4](../../domaene/anforderungen/phasen/bewegung/anhaltenVorDerGrenze.md)). Lässt er dort
los, also neben der *Karte*, steht das *Modell* wieder, wo es vor dem Ziehen war, ohne *Grund*.
Am Stand ac6b913 nachgestellt: ein Boy 3″ nach Westen über die Kante gezogen und losgelassen,
er bleibt an seiner vorigen *Stelle*.
Welche Regel hier gilt, sagen die Anforderungen nicht eindeutig:
- [BEW-6.1](../../domaene/anforderungen/phasen/bewegung/anhaltenVorDerGrenze.md) will an der
  Kante anhalten statt zu sperren, regelt aber nur eine *Stelle* auf der *Karte*.
- [AUF-16.8](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md) (*aufgestellte*
  *Einheit*: zurück, kein *Grund*) und
  [AUF-28.1](../../domaene/anforderungen/phasen/aufstellen/loslassenWoDieKarteZeigt.md)
  (*Einheit in Aufstellung*: dorthin, wo die *Karte* es zuletzt zeigte) gelten in der
  *Aufstellung*. Das Item [loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md)
  will beide auch für die *Normale Bewegung* (Anliegen 2361 F2), sagt aber nicht, welche dort
  greift.
ArbiterMap hält den Block schon beim Ziehen an der Feldkante an
(`ArbiterMap/docs/spec/interaction_map.md:384`); wie es neben dem Feld loslässt, steht dort nicht.

**Kosten.** Heute keine Prüfung rot, BEW-6 ist erfüllt, solange der Zeiger auf der *Karte*
bleibt. In einer Partie zieht man an die Kante gern darüber hinaus: Die *Karte* zeigt das
Anhalten, das Loslassen nimmt den Zug zurück. Ein Kriterium, dazu ein Bildschirmtest und eine
Änderung im Frontend (`technik/frontend/bedienung.js`, `stelleAufDerKarte` gibt neben der
*Karte* keine *Stelle*).

**Gegenvorschlag.** Eine Frage an den Stakeholder mit dem Item loslassenNebenDerKarte:
Lässt jemand in der *Bewegungsphase* ein *Modell* neben der *Karte* los, A: *setzt* Arbiter es,
wo die *Karte* es zuletzt zeigte (wie AUF-28.1, Zweck von BEW-6); B: steht jedes *Modell*, wo
es vor dem Ziehen war (wie AUF-16.8). Empfehlung: A, denn BEW-6 soll anhalten statt den Zug zu
verwerfen, und die *Karte* zeigt beim Ziehen schon das Anhalten.

**Stellungnahme.** Frage an den Stakeholder in Anliegen 9760
F1, Empfehlung A; dazu Vorbild `ArbiterMap/…/model_drag.js:1536` (Loslassen am Dokument
schickt den zuletzt gezeigten Punkt). Mit der Empfehlung steht
[BEW-20.1](../../domaene/anforderungen/phasen/bewegung/loslassenNebenDerKarte.md): *setzt*
statt nach AUF-16.8, wie AUF-28.1. `angenommen` folgt, wenn 9760 erledigt ist.
