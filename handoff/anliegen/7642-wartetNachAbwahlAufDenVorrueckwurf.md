# Wartet die Einheit nach der Abwahl noch auf den Vorrückwurf?

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Bei der Kritik an den Tests zu Item grenzkreise. Wartet nach
[Kritik](../../prozess/ablauf/kritik.md): Lücke abseits des Happy Path.
[BEW-14.1](../../domaene/anforderungen/phasen/bewegung/wurfPerFlaeche.md) lässt einen Klick
neben die Ringe die *Auswahl* aufheben (BEW-9.1), während die *Einheit* auf ihren
*Vorrückwurf* wartet. Ob sie danach weiter wartet, sagt keine Anforderung; der Regeltext
(`core_rules.txt:754`) und ArbiterMap (`interaction_map.md:550`) kennen kein Abwählen
dazwischen. Davon hängt ab, was nach erneuter *Auswahl* erscheint: sechs Ringe und
„Vorrücken zurücknehmen“ (wartet weiter) oder „Vorrücken“ (wartet nicht mehr). Die Tests
prüfen nach dem Klick nur, dass sie nicht *vorgerückt* ist.

**Kosten.** Am Bildschirm: Wer sich neben die Ringe verklickt, sieht nach erneuter *Auswahl*
eines von beiden, je nachdem, wie der Implementierer es baut. Ein Satz in BEW-14.1 oder
BEW-5.2, ein Test.

**Gegenvorschlag.** Ein Satz: Die *Einheit* wartet weiter, bis jemand einen Wurf anklickt oder
das *Vorrücken* zurücknimmt (BEW-12); so ist der Klick auf „Vorrücken“ nicht verloren und
BEW-12 nimmt ihn zurück. Ist das neu, fragt ihr den *Stakeholder* mit dieser Empfehlung.

**Stellungnahme.** Umgesetzt ohne Frage, denn es ist nicht neu: Das Warten beginnt mit BEW-5.2
und endet nur nach BEW-5.3 oder 12.2. [BEW-9.2](../../domaene/anforderungen/phasen/bewegung/abwaehlen.md)
sagt es ausdrücklich: Hebt BEW-9.1 die *Auswahl* auf, wartet die *Einheit* weiter.
