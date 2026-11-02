# Übergehen: aus der Nahkampfreichweite weiterziehen, Kante vor der Bewegungsweite

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 11

## Runde 1
**Befund.** Lücken abseits des Happy Path, darum wartend; sie halten Plan 10 nicht auf:
1. Widerspruch. Nach [BEW-8.4](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md)
   steht ein *Modell* in *Nahkampfreichweite*. Zieht es jemand danach wieder
   (BEW-1.6), hält [BEW-6.2](../../domaene/anforderungen/phasen/bewegung/anhaltenVorDerGrenze.md)
   es sofort an, denn es ist schon darin. Dann verlangt BEW-8.3 „gemeinsam übergehen“ ohne
   *Grund*, [BEW-21.1](../../domaene/anforderungen/phasen/bewegung/sperreBeimLoslassen.md)
   aber die *Sperre* nach QUE-1.3 mit *Grund*. Der Testautor könnte nur eines prüfen.
2. Unklar, wann BEW-3.1 „angehalten hat“ (BEW-8.3) oder „angehalten hätte“ (BEW-8.5), wenn
   nach BEW-6.3 die Kante früher anhält. Beispiel: Die Boyz halten vor einem Gegner (6.2);
   beim Übergehen hielte erst die Kante (6.1), dahinter läge ihre *Bewegungsweite*. Steht
   ‚Bewegungsweite‘ im *Eintrag* oder nicht? Ebenso: Hält die Kante zuerst, bietet Arbiter
   dann übergehen an, obwohl die Boyz danach dort stehen, wo sie schon stehen?

**Kosten.** Je ein Satz. Bleibt 1 offen, entscheidet der Testautor, ob Arbiter sperrt oder
übergehen anbietet; bleibt 2 offen, ob das *Protokoll* einen *Grund* nennt, den niemand
übergangen hat.

**Gegenvorschlag.** 1: Das klärt Plan 11 mit der *Nahkampfreichweite* auf der ganzen
Strecke (Anliegen 6986); dort festlegen, was das Weiterziehen aus ihr heraus und in ihr
macht, Regeltext `core_rules.txt:724`. 2: In BEW-8.3 und 8.5 „angehalten“ als „nach BEW-6.3
die kürzeste Strecke bestimmt“ fassen; dann zählt nur, was wirklich anhält, und bei der
Kante zuerst bietet Arbiter nichts an.

**Stellungnahme.**
