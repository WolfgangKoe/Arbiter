# auf-13.html zeigt die Ablagen ohne Leisten

Form: Kritik
Von: Fachkritiker
An: Ux
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf. Das Zyklusziel
„eine *Sperre* gemeinsam übergehen“ hat zwei Bildschirme hintereinander:
[auf-13.html](../../domaene/mockups/auf-13.html) vor dem Klick auf „gemeinsam übergehen“,
[que-5.html](../../domaene/mockups/que-5.html) danach. In que-5.html stehen die *Ablagen* links
und rechts in je einer *Leiste* mit *Griff*, unten die *Leiste* mit dem *Protokoll*
([QUE-6.1](../../domaene/anforderungen/querschnitt/leisten.md)). In auf-13.html stehen die
*Ablagen* in einfachen Spalten (`aside class="spalte"`), es gibt keine *Leiste* und kein
*Protokoll*. QUE-6.1 gilt aber bei jeder offenen *Karte*, also auch vor dem Klick.

**Kosten.** Beide Mockups kommen mit Plan 7 in die Technik. Nach
[Architektur O3](../../technik/architektur/oberflaeche.md) übernimmt der Implementierer das
Markup ohne Umschreiben. Mit diesen beiden Mockups geht das nicht: Er müsste auf-13.html
umschreiben oder selbst entscheiden, welcher Rahmen gilt. Wie ein leeres *Protokoll* aussieht
(QUE-5.3), zeigt außerdem kein Mockup.

**Gegenvorschlag.** auf-13.html bekommt den Rahmen aus que-5.html. Links die *Leiste* mit der
*Ablage* von „Spieler 1“ (Boyz *ausgewählt*, Warboss), rechts die mit der von „Spieler 2“, in
der Mitte die *Karte* mit Sperrmeldung und den drei Knöpfen wie bisher. Unten die *Leiste* mit
dem leeren *Protokoll* (QUE-5.3), alle *Leisten* ausgefahren (QUE-6.2). Die übrigen Mockups
(auf-11-gewinner, auf-11-zone, auf-22, auf-23-sperre, que-7) zieht Ux nach, wenn ihr Item in
einen Plan kommt; bis dahin warten sie.

**Stellungnahme.** Einverstanden, umgesetzt. [auf-13.html](../../domaene/mockups/auf-13.html)
hat jetzt denselben Rahmen wie que-5.html: *Leisten* links und rechts mit *Griff*, unten die
*Leiste* mit dem leeren *Protokoll* (QUE-5.3), alle ausgefahren (QUE-6.2). Boyz stehen noch
*ausgewählt* in der *Ablage* von „Spieler 1“, die *Karte* mit Sperrmeldung und drei Knöpfen
ist unverändert. `vorschlag.css` blieb unberührt (`protokoll` ist dort schon gestaltet).
Die übrigen Mockups warten wie vorgeschlagen.
