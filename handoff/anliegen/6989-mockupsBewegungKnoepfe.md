# Knöpfe in bew-1, bew-2 und bew-8 nach BEW-5.1 und BEW-8.1

Form: Kritik
Von: Fachkritiker
An: Ux
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf: Drei Mockups widersprechen den neuen Kriterien.
In [bew-1](../../domaene/mockups/bew-1.html), [bew-2](../../domaene/mockups/bew-2.html) und
[bew-8](../../domaene/mockups/bew-8.html) sind die Boyz in der *Bewegungsphase* *ausgewählt*
und nicht *vorgerückt*. Unter der *Karte* steht trotzdem kein „Vorrücken mit 1“ bis „Vorrücken
mit 6“. Nach [BEW-5.1](../../domaene/anforderungen/phasen/bewegung/vorruecken.md) bietet Arbiter
das an, ohne Ausnahme für eine *Sperre*. In diesen Zuständen fehlt damit der Schritt
„*Vorrücken* wählen“ aus dem Happy Path von BEW-5.
Außerdem zeigen bew-2 und bew-8 dieselbe *Sperre* ‚über eine Base‘ mit denselben *Stellen*.
In bew-8 steht „gemeinsam übergehen“, in bew-2 fehlt es, obwohl
[BEW-8.1](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md) es verlangt.

**Kosten.** Baut der Implementierer nach bew-8 oder bew-2, verschwindet „Vorrücken“, solange
ein *Grund* steht. Das Mockup gibt ihm zwei Fassungen desselben Bildschirms. Die Korrektur
betrifft drei Dateien mit je bis zu sieben Knöpfen aus vorhandenen Komponenten.

**Gegenvorschlag.** Die sechs Knöpfe aus [bew-5](../../domaene/mockups/bew-5.html) in die
`knopfGruppe` von bew-1, bew-2 und bew-8 übernehmen. In bew-2 „gemeinsam übergehen“ wie in bew-8
ergänzen. Ist bew-2 nach dem Einbau von BEW-2 fällig zum Löschen, genügt stattdessen das Löschen
(UX: nach dem Einbau das Mockup löschen).

**Stellungnahme.** Umgesetzt: [bew-1](../../domaene/mockups/bew-1.html), [bew-2](../../domaene/mockups/bew-2.html) und [bew-8](../../domaene/mockups/bew-8.html) zeigen „Vorrücken mit 1“ bis „Vorrücken mit 6“ wie [bew-5](../../domaene/mockups/bew-5.html); bew-2 zeigt zusätzlich „gemeinsam übergehen“ wie bew-8.
