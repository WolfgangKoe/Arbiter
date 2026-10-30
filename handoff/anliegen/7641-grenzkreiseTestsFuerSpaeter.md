# Tests zu den Grenzkreisen: Einhüllende am Bildschirm, Modell im Ring

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Kritik an den Tests zu Item grenzkreise. Wartet nach
[Kritik](../../prozess/ablauf/kritik.md): Lücken abseits des Happy Path, Namen.

1. BEW-11.5 und das [Glossar](../../domaene/glossar.md) verlangen, dass die *Karte* die
   *Einhüllende* „statt dieser *Grenzkreise*“ zeigt. Die Tests der Seite zählen nur die
   `g.grenze` und ihre Klassen (wie der [Vertrag](../../technik/architektur/vertrag/bewegung/grenzkreise.md)
   es vorgibt); zehn einzelne Kreise in einer `g.grenze` bestünden sie auch.
2. BEW-14.1 gilt nur, „wo kein *Modell* ist“. Mit einem *Modell* als *Ebene* stehen die
   übrigen *Modelle* derselben *Einheit* in den Ringen 1 bis 6. Kein Test klickt, während sie
   auf den *Vorrückwurf* wartet, ein solches an und stellt fest, dass kein Wurf gilt.
3. „Ring“ und „Grenze“ stehen in Namen von Tests und Hilfen (`stelleImRing`,
   `…ZwischenRingDreiUndVier…`, `…KeineGrenze`), nicht im Glossar; die Anforderungen sagen
   *Grenzkreis* und *Einhüllende*. Keine Prüfung ist rot.

**Kosten.** Am Bildschirm nichts, solange die Seite richtig zeichnet; der *Stakeholder* sieht
1 im Review. Ohne Test kann 1 oder 2 später unbemerkt brechen. Je ein Test.

**Gegenvorschlag.** 1: prüfen, dass jede `g.grenze` ihre `grenzeMaske` nutzt (Attribut
`mask`), mit dem Architekten abgestimmt. 2: ein Test zu BEW-14.1 mit einem *Modell* als
*Ebene*, Klick auf ein anderes *Modell* der *Einheit* im Ring: kein *Vorrückwurf*, die
*Einheit* wartet weiter. 3: Namen aus Anforderung und Glossar, oder „Ring“ über den
Anforderungsautor ins Glossar (der Plan nutzt es schon).

**Stellungnahme.**
