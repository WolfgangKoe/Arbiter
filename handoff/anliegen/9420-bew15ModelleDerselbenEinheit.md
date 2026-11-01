# BEW-1.5: Modelle derselben Einheit

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Mit BEW-2 ist BEW-2.7 fort: „Gegeben die *Ebene* ist die ganze *Einheit*, dann
sperrt QUE-1.2 in BEW-1.5 kein *Modell* wegen eines anderen derselben *Einheit* an dessen
voriger oder neuer *Stelle* (wie AUF-24.2).“ 8840 hat das nicht gestrichen, es ging nur mit
der Datei. BEW-1.5 sagt jetzt „es sperrt nur QUE-1“, und QUE-1.2 sperrt jede *Base*, die
„die eines anderen *gesetzten* *Modells*“ *überdeckt*. Zieht jemand die *Boyz* als *Ebene*
um weniger als ihre Breite, landet ein *Modell* dort, wo eben noch ein anderes derselben
*Einheit* stand. Ob das sperrt, sagt kein Kriterium mehr. Das ist der Normalfall jeder
Bewegung einer ganzen *Einheit*, also Happy Path. BEW-17 hilft hier nicht: AUF-29.3 nimmt
nur das Anhalten beim Ziehen aus, nicht QUE-1.2 beim Loslassen. In der *Aufstellung* regelt
das AUF-24.2, aber nur für AUF-21.1 und 21.2. Der Test
`testBew2_7IstDieGanzeEinheitEbeneSperrtDieÜberdeckungKeinModellWegenDerselbenEinheit` ist
mit `sperrenBeimZiehenTest.py` gelöscht (9272). `testBew1_5IstDieGanzeEinheitEbene…` zieht
um `schrägOhneHindernis` (1″, 2″) und umgeht den Fall. Heute ist alles grün (22 Tests),
nur weil der Code BEW-2.7 noch hat. Baut der Implementierer im Item
[anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md) die Sperre ‚über eine Base‘
aus, merkt es kein Test, wenn diese Ausnahme mit wegfällt. Dann greift ‚Base überdeckt‘
zu Unrecht, und nach QUE-1.4 ließe sie sich nicht einmal *gemeinsam übergehen*.

**Kosten.** Ein Satz in BEW-1.5 oder ein neues BEW-1.8. Dazu ein Test beim Testautor; den
gelöschten gibt es noch in git (`HEAD:technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py:288`).
Code: keiner, er kann es schon. Ohne den Satz kann jede *Einheit*, die als Ganzes kurz
zieht, gesperrt werden, und das ohne Ausweg.

**Gegenvorschlag.** BEW-1.8 **Gegeben** die *Ebene* ist die ganze *Einheit*, **dann**
sperrt QUE-1.2 in BEW-1.5 kein *Modell* wegen eines *Modells* derselben *Einheit*, weder an
dessen voriger noch an dessen neuer *Stelle* (wie AUF-24.2, Vorbild
`ArbiterMap/…/movement_service.py:450`). Gleich danach ein Anliegen an den Testautor: Er
soll den Test zu BEW-1.8 wiederherstellen und um eine Strecke unter der Breite der *Base*
ziehen.

**Stellungnahme.** Umgesetzt, aber als eigene Anforderung
[BEW-19.1](../../domaene/anforderungen/phasen/bewegung/einheitAlsGanzes.md), Etappe 2, im
Wortlaut deines Gegenvorschlags: BEW-1 hat schon 1.185 von 1.200 Zeichen. Anliegen an den
Testautor: [9401](9401-testZuBew19.md), wartet auf die Technikphase.
