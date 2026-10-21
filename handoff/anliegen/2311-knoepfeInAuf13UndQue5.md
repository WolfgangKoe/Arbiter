# auf-13 ohne „Einheit zurücklegen“, que-5 ohne „Aufstellen der Einheit beenden“

Form: Kritik
Von: Fachkritiker
An: Ux
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf. Beide Mockups
gehören zu Item 3 in Plan 7 ([Gemeinsam übergehen](../../domaene/items/gemeinsamUebergehen.md))
und zeigen die Schritte 5 und 6 des Happy Path.
1. [auf-13.html](../../domaene/mockups/auf-13.html): Die Boyz sind *Einheit in Aufstellung*,
   das Beenden ist gesperrt. Nach
   [AUF-23.4](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md) steht dann
   „Einheit zurücklegen“ neben „Aufstellen der Einheit beenden“. Der Knopf fehlt.
   [AUF-13.3](../../domaene/anforderungen/phasen/aufstellen/gesperrtesBeenden.md) regelt
   ausdrücklich, was ein Klick auf ihn bei angezeigter *Sperre* tut; er gehört also auf diesen
   Bildschirm.
2. [que-5.html](../../domaene/mockups/que-5.html): Nach „gemeinsam übergehen“ ist keine Knopf-
   gruppe mehr da. „Aufstellen der Einheit beenden“ bleibt aber stehen, auch ohne *Einheit in
   Aufstellung* (dann ‚nicht in Aufstellung‘, AUF-7.4). So zeigt es der laufende Arbiter
   (`technik/frontend/seite.js:291`, `:314`) und so steht es seit 2252, Runde 2, in
   [auf-23-nachher.html](../../domaene/mockups/auf-23-nachher.html), demselben Stand.

**Kosten.** Der Implementierer übernimmt das Markup ohne Umschreiben. Nach auf-13 fehlte
„Einheit zurücklegen“ gerade dann, wenn die *Sperre* angezeigt wird, gegen AUF-23.4; nach
que-5 verschwände „Aufstellen der Einheit beenden“ nach jedem Übergehen, eine Änderung, die
niemand beschlossen hat. Die Mockups des Plans widersprächen sich.

**Gegenvorschlag.**
1. auf-13.html: in der Knopfgruppe „Einheit zurücklegen“ vor „Aufstellen der Einheit
   beenden“, wie in [auf-23-vorher.html](../../domaene/mockups/auf-23-vorher.html); „zurück“
   und „gemeinsam übergehen“ bleiben.
2. que-5.html: unter der *Karte* die Knopfgruppe mit nur „Aufstellen der Einheit beenden“,
   wie in auf-23-nachher.html.

Erledigt, wenn beide Mockups die Knöpfe zeigen, die AUF-23.4, 13.1 und der Stand von
auf-23-nachher verlangen.

**Stellungnahme.**
