# Fliegen der Canoptek-Spinne

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Die Canoptek-Spinne aus [Etappe 2](../../domaene/etappen/02-bewegen.md) hat FLY
(`Arbiter-old/data/wh40k_9e/necrons/units.yaml:410`); kein *Datenblatt* nennt bisher *Fliegen*.
[BEW-18](../../domaene/anforderungen/phasen/bewegung/fliegen.md) nennt nur das Hinwegziehen über
fremde *Bases*. Nach dem Regeltext darf ein *Modell* mit FLY beim Ziehen auch in
*Nahkampfreichweite* kommen, nur nicht dort enden (`core_rules.txt:884`); BEW-6.2 hielte die
Spinne davor an.

**Kosten.** Ohne beides hat das Item [fliegen](../../domaene/items/fliegen.md) keine *Einheit*,
und die Spinne hält regelwidrig vor fremden *Bases* und der *Nahkampfreichweite* an.

**Gegenvorschlag.** *Fliegen* im *Datenblatt* der Spinne mit Fundstelle; ein Kriterium in BEW-18
zum Ziehen durch die *Nahkampfreichweite* (`core_rules.txt:884`); BEW-18 `Etappe: 2` nach
Anliegen 9271 F2 A, bei F2 B `Etappe: 4`.

Wann: Domänenphase 10, vor Plan 10.

**Stellungnahme.** Angenommen und umgesetzt.
- [BEW-18](../../domaene/anforderungen/phasen/bewegung/fliegen.md): `Etappe: 2` (9271 F2 A),
  BEW-18.3 zum Ziehen durch die *Nahkampfreichweite* (`core_rules.txt:884`, `:888`, 9400 F2);
  *Fliegen* im Glossar.
- Neu [MIV-3](../../domaene/anforderungen/missionsvorbereitung/canoptekSpinne.md): die Spinne in
  der *Armee* der Necrons (MIV-3.1) mit *Fliegen*, als einzige (MIV-3.2). Das ist „die
  Canoptek-Spinne (9340)“ im Item [fliegen](../../domaene/items/fliegen.md); bitte nenne dort
  MIV-3 im Umfang.
- Geschrieben: *Datenblatt* `Canoptek Spyder` in `domaene/daten/katalog/necrons/datenblaetter.yaml`,
  `bewegungsweite: 6` (`units.yaml:417`), `durchmesser: 60` (9400 F1 A).
- Geschrieben: die Spinne in `domaene/daten/ausgangslage.yaml` (`necrons_test.yaml:17`) und
  `formation.yaml`. An einer Kopie in `/tmp` sind mit ihr dieselben 37 Tests rot wie ohne sie
  (laufende Items), keiner mehr.
- Geschrieben: `fliegen: true` beim *Datenblatt* `Canoptek Spyder` (`units.yaml:410`, FLY),
  Form nach [Katalog](../../technik/architektur/katalog.md) K3 und K4, nach 11840; der Start
  liest ihn, nur die Spinne hat *Fliegen*.
