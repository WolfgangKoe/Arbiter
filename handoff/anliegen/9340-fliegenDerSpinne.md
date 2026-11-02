# Fliegen der Canoptek-Spinne

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

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

**Stellungnahme.** Teils umgesetzt:
[BEW-18](../../domaene/anforderungen/phasen/bewegung/fliegen.md) hat `Etappe: 2` (9271 F2,
Annahme A) und BEW-18.3: BEW-6.2 hält ein fliegendes *Modell* nur an, wenn die Strecke in
*Nahkampfreichweite* endet (`core_rules.txt:884`, `:888`); *Fliegen* im Glossar mit `:888`.
Das *Datenblatt* der Spinne fehlt: Keine Quelle nennt ihre *Base*, ich frage in
Anliegen 9400. Danach schreibe ich es, aber erst zum Start des
Items fliegen: Der Katalog lehnt den neuen Schlüssel `fliegen` ab, bis die Technik ihn kennt
(`technik/architektur/katalog.md` K3), sonst wird jeder Akzeptanztest rot. Den
Ork-Psioniker: MIV-2, 10180.
Nach 9400: *Durchmesser* 60 (F1 A), Ende des Flugs wie BEW-18.3 (F2 A). Zum Start des
Items fliegen (Plan 10, Reihenfolge in 10340) schreibe ich das *Datenblatt* `Canoptek Spyder`:
`bewegungsweite: 6` (`units.yaml:417`), `durchmesser: 60` (Anliegen 9400 F1 A), `fliegen`
(`units.yaml:410`), dazu die Spinne in der *Armee* (`necrons_test.yaml:17`).
