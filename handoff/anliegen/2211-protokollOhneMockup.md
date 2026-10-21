# Gemeinsam übergehen: kein Mockup zeigt das Protokoll

Form: Kritik
Von: Fachkritiker
An: Ux
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf. Das Zyklusziel
aus [Review 6](../review.md) ist „eine *Sperre* gemeinsam übergehen“. Die Etappe verlangt
„Das *Protokoll* zeigt stets jedes Übergehen“. [auf-13.html](../../domaene/mockups/auf-13.html)
passt zu AUF-13.1 und 12.7 und zeigt den Stand vor dem Klick. Nach dem Klick auf „gemeinsam
übergehen“ hat das *Protokoll* einen neuen Eintrag
([QUE-5.1](../../domaene/anforderungen/querschnitt/uebergehen.md)). Er steht in der *Leiste*
unten ([QUE-6.1](../../domaene/anforderungen/querschnitt/leisten.md)). Zu QUE-5 und QUE-6 gibt es
kein Mockup. In `vorschlag.css` und in der Komponentenseite fehlen *Leiste*, *Griff* und
*Protokoll*.

**Kosten.** Ohne Mockup ist DoR 5 für das Item zu QUE-5 nicht erfüllt. Die Technik müsste dann
selbst festlegen, wie der Eintrag am Bildschirm aussieht.

**Gegenvorschlag.** Ein Mockup zu QUE-5 und QUE-6: der Stand nach „gemeinsam übergehen“ aus
auf-13.html. Die Boyz sind *aufgestellt*, Spieler 2 ist *an der Reihe*. Unten steht die *Leiste*
mit dem *Protokoll*, darin ein Eintrag mit *Einheit*, *Spieler* und *Grund*. Links und rechts
stehen die *Leisten* mit *Griff*. Vorbild ist der untere Bereich in
`ArbiterMap/docs/spec/design_system.md:55`. Neue Regeln gehören nach `vorschlag.css`, die
Komponente entscheidet der Architekt (DoR 5).

**Stellungnahme.** Angenommen, soweit es Ux betrifft. [que-5.html](../../domaene/mockups/que-5.html)
zeigt den Stand nach „gemeinsam übergehen“ (QUE-5 und QUE-6): Boyz *aufgestellt*, Spieler 2 *an
der Reihe*, links und rechts die *Leisten* mit den *Ablagen*, unten die *Leiste* mit dem
*Protokoll* und einem Eintrag aus *Einheit*, *Spieler* und *Grund*. Alle *Leisten* sind
ausgefahren (QUE-6.2). `vorschlag.css` hat neu `leiste`, `leistenGriff`, `leistenInhalt`,
`protokoll` und `protokollEintrag`; Markup nach Architektur O4. Die Komponentenseite
`technik/frontend/komponenten.html` gehört der Technik und liegt nicht in Ux' Schreibpfaden;
die Aufnahme steht in [2230](2230-leistenAufKomponentenseite.md).
