# BEW-3 und BEW-4 ins Item Normale Bewegung

Form: Kritik
Von: Anforderungsautor
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: ein Schritt des Happy Path fehlt im Item). Nach
[5180](5180-annahmenZurBewegungsphase.md) F5, F6 und der Annahme aus
[5400](5400-wieWeitEinKorrigiertesModellStehenDarf.md) passte BEW-1 nicht mehr in 1.200
Zeichen. Darum stehen Anhalten am *B* und die *Sperre* bei „Phase beenden“ in zwei neuen
Anforderungen: [BEW-3 · Anhalten am B](../../domaene/anforderungen/phasen/bewegung/anhaltenAmB.md)
und [BEW-4 · Bewegungsphase beenden](../../domaene/anforderungen/phasen/bewegung/beenden.md).
[Item normalMove](../../domaene/items/normalMove.md) nennt nur BEW-1 und BEW-2; ohne BEW-3
und BEW-4 fordert keine Prüfung Tests für diese beiden Schritte. Neu gefasst, mit neuen
Kennungen: BEW-1.5 bis 1.7, BEW-2.5 bis 2.7; BEW-1.1 bis 1.4 und BEW-2.1 bis 2.4 entfallen.

**Kosten.** Eine Zeile im Item; zwei neue Testdateien für den Testautor
(`anhaltenAmBTest.py`, `beendenTest.py`).

**Gegenvorschlag.** Umfang des Items: BEW-1 bis BEW-4, AUF-20.6; Schritt 3 von
[plan.md](../plan.md) nennt BEW-3 und BEW-4.

**Stellungnahme.** Umgesetzt wie vorgeschlagen.
[Item normalMove](../../domaene/items/normalMove.md): Umfang BEW-1 bis BEW-4, AUF-20.6.
[plan.md](../plan.md): Item 3 verlinkt BEW-3 und BEW-4; Schritt 3 ohne den Knopf „Bewegung
der Einheit beenden“, den keine Anforderung mehr nennt: korrigieren nach Belieben (BEW-1.6),
Anhalten am *B* (BEW-3), Sperre über eine fremde *Base* (BEW-2), „Phase beenden“ ohne
*Kohärenz* (BEW-4).
