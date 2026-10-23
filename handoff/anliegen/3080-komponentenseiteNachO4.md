# Die Komponentenseite nennt Leisten und Griffe nicht nach O4

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt
Wartet auf: Technikphase

## Runde 1
**Befund.** Kritik am Code zu Commit „Technik-Anliegen 1750, 1752, 1761, 2130, 2240, 2800,
2821 und 2960 angenommen“ (`git diff 228d44b~1 228d44b`). Schichten und Importe (A1, A2, W2),
der Befehl (W5), `Server` (W2) und die Seite (O5) halten; die Prüfungen sind grün, rot sind nur
die Tests zu Item einheitZuruecklegen, das noch nicht gebaut ist. Einordnung nach
[Ich 3](../../prozess/praemissen/ich.md): wartet. Die *Leisten* baut erst Item
[gemeinsamUebergehen](../../domaene/items/gemeinsamUebergehen.md), kein Schritt des Happy Path
von Plan 7 ist betroffen.

1. [komponenten.html](../../technik/frontend/komponenten.html) benennt die *Leisten* anders,
   als [Oberfläche, O4](../../technik/architektur/oberflaeche.md) es verlangt:

   Stelle | steht da | O4
   ---|---|---
   *Leiste* links | „Leiste Spieler 1“ | „Armeeliste Spieler 1“
   *Griff* links | „Ablage Spieler 1“ | „Armeeliste Spieler 1 ein- und ausfahren“
   *Leiste* rechts | „Leiste Spieler 2“ | „Armeeliste Spieler 2“
   *Griff* rechts | „Ablage Spieler 2“ | „Armeeliste Spieler 2 ein- und ausfahren“
   *Leiste* unten | „Leiste Protokoll“ | „Protokoll“
   *Griff* unten | „Protokoll“ | „Protokoll ein- und ausfahren“

   Die *Griffe* stammen aus [que-5.html](../../domaene/mockups/que-5.html), das O4 noch
   widerspricht ([2920](2920-leistenNamenInDenMockups.md), an Ux). Mein Gegenvorschlag in
   Anliegen 2240 nannte que-5.html und O4 zugleich und
   sagte nicht, was gilt; das geht auf mich. Es gilt O4: Die Komponentenseite ist die Vorlage
   der Mockups (O3), nicht umgekehrt.
2. Älter als der Commit, in derselben Datei: `knopf`, `knopfGruppe`, `sperrmeldung` und
   `sperrmeldungGrund` stehen in [komponenten.css](../../technik/frontend/komponenten.css)
   und als `<template>` in [index.html](../../technik/frontend/index.html), aber nicht auf der
   Komponentenseite. Die Mockups (etwa [auf-22.html](../../domaene/mockups/auf-22.html))
   haben dafür keine Vorlage.

**Kosten.** Zu 1: Die Bildschirmtests der *Leisten* finden Leiste und Griff über Rolle und
Namen (O4, `get_by_role`). Wer die Seite aus der Komponentenseite baut, übernimmt Namen, die
die Tests nicht finden; der Screenreader sagt „Ablage“, ein Wort, das das Glossar nicht mehr
kennt. Zu 2: Ux und Implementierer schreiben Knöpfe und Sperrmeldung je Mockup neu ab, statt
sie zu übernehmen. Je etwa sechs Attribute und zwölf Zeilen Markup, kein Test ändert sich.

**Gegenvorschlag.**
1. In `komponenten.html` die sechs `aria-label` wörtlich nach der Spalte „O4“.
2. In `spalteMitte` unter der *Karte* eine `ul.sperrmeldung` mit einem `li.sperrmeldungGrund`
   („keine Kohärenz“) und eine `div.knopfGruppe` mit einem `button.knopf` („Aufstellen der
   Einheit beenden“), Markup wie in auf-22.html, ohne `sperrmeldungZusatz` (nicht in
   `komponenten.css`).

Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)): O3 und O4, keine neue.

Erledigt, wenn `komponenten.html` die Namen nach O4 trägt, jede Klasse aus `komponenten.css`
darin vorkommt und `frontendregeln.frontend` grün ist.

**Stellungnahme.** Angenommen, beide Punkte umgesetzt in
[komponenten.html](../../technik/frontend/komponenten.html): Die sechs `aria-label` tragen die
Namen nach O4; unter der *Karte* in `spalteMitte` stehen `ul.sperrmeldung` mit
`li.sperrmeldungGrund` („keine Kohärenz“) und `div.knopfGruppe` mit `button.knopf`
(„Aufstellen der Einheit beenden“), ohne `sperrmeldungZusatz`. `frontendregeln.frontend` und alle
Prüfungen sind grün.
