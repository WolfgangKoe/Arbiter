# Vorrücken braucht jetzt die Grenzkreise

Form: Kritik
Von: Anforderungsautor
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Nach den Antworten des Stakeholders in
[Anliegen 6998](6998-grenzkreiseVorrueckenUndBegriff.md) F1 und
[7000](7000-begriffeUndFragenZurBewegung.md) wählt der Klick auf einen Kreis den *Vorrückwurf*,
mit einem Knopf „Vorrücken“ und „Vorrücken zurücknehmen“:
[BEW-5](../../domaene/anforderungen/phasen/bewegung/vorruecken.md) neu gefasst (ohne Tests),
neu [BEW-12](../../domaene/anforderungen/phasen/bewegung/vorrueckenZuruecknehmen.md) und
[BEW-13](../../domaene/anforderungen/phasen/bewegung/grenzkreiseBeimVorruecken.md);
[BEW-11](../../domaene/anforderungen/phasen/bewegung/grenzkreise.md) mit *Einhüllender*, 11.2
entfällt (jetzt BEW-13.2), neu 11.5. Veraltet: [Plan 9](../plan.md) Schritt 2 („Vorrücken mit 1“
bis „mit 6“) und die Abweichung „Grenzkreise erst in Plan 10“; BEW-5.3 nennt BEW-13.1, das
BEW-11.1 und 11.5 voraussetzt. Items `vorrueckenUndAuswahl` und `grenzkreise` nennen BEW-11.2.

**Kosten.** Bleibt der Plan, ist Item 3 ohne die Kreise nicht baubar.

**Gegenvorschlag.** Entweder BEW-11, 12 und 13 zu Item 3 in Plan 9, oder BEW-5 und 12 mit den
Grenzkreisen in Plan 10. Mockup [bew-5](../../domaene/mockups/bew-5.html) ist veraltet
(Anliegen 7001 an Ux).

**Stellungnahme.** Angenommen, erste Variante: Das Zyklusziel aus Review 8 nennt das
Vorrücken, darum BEW-11, 13, 5 und 12 in Plan 9 als eigenes Item 4
[Grenzkreise und Vorrücken](../../domaene/items/grenzkreise.md), zuletzt, damit Items 1 bis 3
nicht warten. Item 3 heißt jetzt [Anhalten und Auswahl](../../domaene/items/anhaltenUndAuswahl.md)
(BEW-6, 2.8, 7, 9, 10, AUF-30); `vorrueckenUndAuswahl` ist gelöscht, BEW-11.2 nennt kein Item
mehr. [Plan 9](../plan.md): Schritt 5 statt „Vorrücken mit 1“ bis „mit 6“, die Abweichung
„Grenzkreise erst in Plan 10“ ist ersetzt durch Kosten und Grund.
