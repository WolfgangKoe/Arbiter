# AUF-8.4 behandelt die Ablage noch als Ziel zum Hineinziehen

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet, ein Randfall
abseits des Happy Path; die Tests zu AUF-8.4 und 16.8 widersprechen sich nicht.
Das [Glossar](../../domaene/glossar.md) sagt zur *Ablage* „kein Ziel zum Hineinziehen“, der
Stakeholder in [2220](2220-knopfZuruecklegen.md): „Eine Ablage braucht es in deinem
Verständnis nicht.“ [AUF-8.4](../../domaene/anforderungen/phasen/aufstellen/ziehen.md) gibt
aber genau dem Hineinziehen eine Bedeutung: Ein Boy einer *aufgestellten* *Einheit*, auf
eine *Ablage* gezogen, bringt die *Sperre* ‚nicht wählbar‘. Daneben losgelassen springt er
still zurück ([AUF-16.8](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md),
„neben *Karte* und *Ablagen*“). ‚nicht wählbar‘ stammt aus der Zeit, als Ziehen auf die
*Ablage* *zurücklegte*. Nach der Umbenennung (2221) hieße es: Auf die *Armeeliste* ziehen ist
gesperrt, auf den Tisch daneben nicht.

**Kosten.** Bleibt es, sieht ein Spieler eine Meldung für eine Geste, die es nach dem
Stakeholder nicht mehr gibt, und 16.8 trägt eine Unterscheidung, die nur 8.4 braucht.

**Gegenvorschlag.** In der nächsten Domänenphase den Stakeholder fragen, mit Empfehlung:
AUF-8.4 streichen und AUF-16.8 auf „neben der *Karte*“ fassen, also auch auf der
*Armeeliste* still zurück. Mit dem Test zu 8.4 entfallen dann die zwei Fälle `auf8_4…` in
`sperreOhneStelleTest.py:108`, `:109`.

**Stellungnahme.**
