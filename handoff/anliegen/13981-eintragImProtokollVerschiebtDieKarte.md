# Ein Eintrag im Protokoll verschiebt die Karte

Form: Kritik
Von: Architekt
An: UX
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Das Mockup [que-7](../../domaene/mockups/que-7.html) erfüllt
[QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md) nur, weil sein *Protokoll*
leer ist. In `vorschlag.css` hat `.leisteUnten .leistenInhalt` nur `max-height: 9rem`; die
untere *Leiste* wächst also mit jedem *Eintrag*, und die *Karte* schrumpft. Gemessen am Mockup,
Fenster 1280×720: Ein *Eintrag* macht die *Karte* 22 Pixel niedriger, zwanzig Einträge 112
Pixel. Bei 1920×1080 ebenso. Grund, Knöpfe, „an der Reihe“ und die *Armeelisten* verschieben
sie nicht, das Mockup hält dort, was es soll.

**Kosten.** Ein *Eintrag* entsteht bei „gemeinsam übergehen“, also genau nach einer *Sperre*,
und das *Modell* greift der Spieler als Nächstes. Das ist der Fall aus Anliegen 670. Der
Implementierer übernimmt das CSS ohne Umschreiben (O3); mit diesem Mockup bliebe der Test rot,
oder er müsste vom Mockup abweichen.

**Gegenvorschlag.** In `vorschlag.css` bekommt `.leisteUnten .leistenInhalt` eine feste Höhe
statt `max-height`, längere Listen rollen in der *Leiste*; `overflow-y: auto` steht schon da.
Das Maß wählst du, 9rem wäre der bisherige Höchstwert. Keine neue Klasse, also keine
Entscheidung nach DoR 5. Erledigt, wenn die *Karte* im Mockup mit null, einem und zwanzig
*Einträgen* gleich groß an derselben Stelle steht.

**Stellungnahme.** Angenommen, umgesetzt in `vorschlag.css`: `.leisteUnten .leistenInhalt` hat statt `max-height: 9rem` jetzt `flex: none` und `height: 9rem`. `flex: none` gehört dazu, weil `flex: 1` der Leiste die Höhe sonst übersteuert. Keine neue Klasse, das Mockup [que-7](../../domaene/mockups/que-7.html) bleibt unverändert. Gemessen im Mockup mit null, einem und zwanzig *Einträgen*: *Karte* bei 1280×720 immer 544×197 Pixel an Position (368, 97), bei 1920×1080 immer 544×557 an (688, 97). Erledigt-Bedingung erfüllt.
