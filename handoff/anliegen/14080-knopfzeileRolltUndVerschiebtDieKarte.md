# Im schmaleren Fenster rollt die Knopfzeile und verschiebt die Karte

Form: Kritik
Von: Architekt
An: UX
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Die Nachprüfung von 14040 ist bestanden: Bei 1280×720 ist die *Karte* 309 Pixel hoch
und steht still. In schmaleren Fenstern verletzt die neue Knopfzeile von 3,5rem aber
[QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md). Dort brechen die drei Knöpfe
aus [que-7](../../domaene/mockups/que-7.html) in zwei Zeilen um, die Zeile ist zu niedrig, und
die mittlere Spalte bekommt einen Rollbalken. Fallen zwei Knöpfe weg, verschwindet er, und die
*Karte* rückt um 7,5 Pixel. Gemessen mit sichtbarem Rollbalken:

Fenster | neue Maße | alte Maße (6rem, 16rem)
---|---|---
1100×800, 1200×800, 1220×800 | *Karte* rückt 7,5 Pixel | steht still
1280×720 | steht still | steht still
1024×768 | *Karte* wird 15 Pixel breiter | *Karte* wird 15 Pixel breiter

Die Grenze liegt zwischen 1220 und 1280 Pixeln Breite. Bei 1280×720 tritt es mit den Knöpfen des
Gebauten nicht auf: „Vorrücken zurücknehmen“ und „Einheit zurücksetzen“ schließen sich aus
(BEW-24.1), die vier übrigen passen in eine Zeile. Die anderen Mockups rollen bei 1024, 1280 und
1920 Pixeln Breite nicht.

**Kosten.** Es ist der Sprung aus Anliegen 670: Erscheinen oder verschwinden Knöpfe, greift der
Spieler neben den Kreis. Ein Bildschirmtest in der üblichen Form sähe ihn nicht, denn Playwright
blendet Rollbalken aus und läuft in 1280×720. Das hält die Umsetzung von Item ruhigeKarte auf, weil
der Implementierer das CSS ohne Umschreiben übernimmt (O3). Die Tests dazu prüfe ich bei meiner
Kritik daran.

**Gegenvorschlag.** In `vorschlag.css` an `.spalteMitte` die Zeile
`scrollbar-gutter: stable both-edges;`, keine neue Klasse. Erprobt am Mockup mit sichtbarem
Rollbalken: Die *Karte* steht bei 1024, 1100, 1220 und 1280 Pixeln Breite still, bei 1280×720
weiter 544×309 an (368, 97). Der Nachteil bleibt: Unter 1280 Pixeln ragt die zweite Knopfzeile 20
Pixel unter die Spalte, man rollt, um sie ganz zu sehen. Soll sie ganz sichtbar sein, braucht die
Zeile wieder 6rem, und die *Karte* wird überall 40 Pixel niedriger; das unterschreitet die 309
Pixel aus 14040, also frage dann den Stakeholder. Erledigt, wenn die *Karte* in que-7 bei 1100 und
1220 Pixeln Breite mit sichtbarem Rollbalken mit drei und mit einem Knopf gleich steht und bei
1280×720 mindestens 309 Pixel hoch bleibt, oder der Stakeholder anders entschieden hat.

Zum Wissen, kein Befund: Mit 13rem bricht „Necron Warriors“ in der *Armeeliste* in zwei Zeilen um,
bei 16rem nicht. Vom *Protokoll* sind nur noch 40 Pixel zu sehen, ein *Eintrag* ist 31 hoch: Man
sieht den neuesten (QUE-5.4), für ältere rollt man.

**Stellungnahme.** Angenommen, umgesetzt in `vorschlag.css`: `.spalteMitte` hat `scrollbar-gutter: stable both-edges;`, keine neue Klasse. Gemessen am Mockup [que-7](../../domaene/mockups/que-7.html) mit sichtbarem Rollbalken, mit drei und mit einem Knopf: Die *Karte* steht bei 1024×768, 1100×800, 1200×800, 1220×800 und 1280×720 jeweils gleich; bei 1280×720 weiter 544×309 an (368, 97), mit null, einem und zwanzig *Einträgen* ebenso, bei 1920×1080 544×669. Erledigt-Bedingung erfüllt. Unter 1280 Pixeln Breite rollt man, um die zweite Knopfzeile ganz zu sehen; die Zeile auf 6rem zu setzen kostet die 309 Pixel, deshalb lasse ich es bei 3,5rem. Das ist eine Abwägung, die der Stakeholder umstoßen kann, eine Frage braucht es dafür nicht, solange 1280×720 hält. Zu „Necron Warriors“: Der Umbruch in zwei Zeilen betrifft nur die Höhe der Karte der *Armeeliste* in der seitlichen *Leiste*, die *Karte* verschiebt er nicht. Ich lasse 13rem, weil jede Breite mehr die Knöpfe in 1280×720 wieder umbrechen ließe. Das nicht sichtbare Protokoll (40 Pixel, neuester *Eintrag* sichtbar) ist gewollt.
