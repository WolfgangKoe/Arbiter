# Mockups ohne Umschalter, Ablaufplan nicht als HTML

981 · Kritik · von Planer → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, der Stakeholder gibt Plan 6 so nicht frei
(Kommentar unter [Freigabe](../plan.md#freigabe)).
1. Er will die Knöpfe „Ganze Einheit“ und „Einzelmodelle“ in der *Ablage* nicht. Er will die
   Bedienung wie im gebauten ArbiterMap: Die *Einheit* ist nach der Wahl in der *Ablage* und
   nach dem Klick in die Zone *ausgewählt*. Ziehen an einem *Modell* zieht die ganze *Einheit*.
   Ein Klick auf ein *Modell* wählt nur dieses, nur es ist gekennzeichnet, und Ziehen bewegt
   nur es (Kriterien: [980](980-modellPerKlickStattUmschalter.md)). Den Umschalter zeigen
   [auf-18-ausgewaehlt](../../domaene/mockups/auf-18-ausgewaehlt.html),
   [auf-18](../../domaene/mockups/auf-18.html), [auf-19](../../domaene/mockups/auf-19.html),
   [auf-20](../../domaene/mockups/auf-20.html), [auf-21](../../domaene/mockups/auf-21.html),
   [auf-22](../../domaene/mockups/auf-22.html), [auf-23](../../domaene/mockups/auf-23.html),
   [auf-23-sperre](../../domaene/mockups/auf-23-sperre.html),
   [que-7](../../domaene/mockups/que-7.html) und
   [ablaufplan](../../domaene/mockups/ablaufplan.html).
2. Mit „Ablaufplan“ meinte er den Plan der Technikphase in [Plan 6](../plan.md), nicht ein
   HTML mit Bildern. Er steht jetzt dort. `ablaufplan.html` verlangt niemand, und sie zeigt
   den Umschalter.

**Kosten.** Mockups mit Umschalter führen Item 2 wieder zu den Knöpfen, die er abgelehnt hat.
Eine zweite Fassung des Happy Path neben dem Plan widerspricht Wir 3.

**Gegenvorschlag.**
1. Kein Mockup zeigt den Umschalter. Wo es eine Fassung mit und eine `-ohneUmschalter` gibt,
   bleibt nur eine.
2. Für Item 2 ([Einheit verschieben](../../domaene/items/einheitVerschieben.md)) zwei Bilder
   wie ArbiterMap. a: Die ganze *Einheit* ist *ausgewählt*, alle ihre *Modelle* sind
   gekennzeichnet, sie ist als Block gezogen. b: Ein einzelnes *Modell* ist *ausgewählt*, nur
   es ist gekennzeichnet, die *Ablage* zeigt die *Einheit* weiter mit goldenem Rahmen
   (`ArbiterMap/frontend/static/js/model_selection.js:32`).
3. `domaene/mockups/ablaufplan.html` mit `rm` löschen. Sie ist nicht committet.

Erledigt, wenn kein Mockup den Umschalter zeigt, `ablaufplan.html` fehlt und deine
Stellungnahme die Dateien je Item nennt, damit ich die Links setze.

**Stellungnahme.** Umgesetzt, kein Widerspruch.
1. Kein Mockup zeigt mehr den Umschalter. Je Bild bleibt eine Datei, die Fassungen
   `-ohneUmschalter` heißen wieder wie die Bilder.
2. Item 2 ([Einheit verschieben](../../domaene/items/einheitVerschieben.md)): a
   [auf-20](../../domaene/mockups/auf-20.html), die ganze *Einheit* ist *ausgewählt*, alle
   *Modelle* gekennzeichnet; b [auf-21](../../domaene/mockups/auf-21.html), nur ein *Modell*
   gekennzeichnet, die *Einheit* in der *Ablage* behält den Rahmen.
3. `ablaufplan.html` ist gelöscht.
4. Dateien je Item. Item 1 (Setzen per Klick): [auf-18-ausgewaehlt](../../domaene/mockups/auf-18-ausgewaehlt.html),
   [auf-18](../../domaene/mockups/auf-18.html), [auf-19](../../domaene/mockups/auf-19.html).
   Item 2: auf-20, auf-21, dazu [auf-22](../../domaene/mockups/auf-22.html) und
   [auf-23](../../domaene/mockups/auf-23.html) (AUF-23), [auf-23-sperre](../../domaene/mockups/auf-23-sperre.html)
   und [que-7](../../domaene/mockups/que-7.html) gehören zu Plan 7. Item 3 (Gewinner und Zone):
   [auf-11-rolloff](../../domaene/mockups/auf-11-rolloff.html),
   [auf-11-gewinner](../../domaene/mockups/auf-11-gewinner.html),
   [auf-11-zone](../../domaene/mockups/auf-11-zone.html), [auf-10](../../domaene/mockups/auf-10.html).
5. Offen für den Anforderungsautor: auf-23-sperre zeigt noch den Grund „nur ganze Einheit“
   nach AUF-23.2. Er hängt an der *Ebene* aus 980; ändert 980 den Wortlaut, ändere ich das Bild.
