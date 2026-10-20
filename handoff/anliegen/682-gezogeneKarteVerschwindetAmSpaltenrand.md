# Die gezogene Karte verschwindet am Rand ihrer Spalte

682 · Kritik · von Ux → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder meldet: „Beim zweiten Spieler blockiert der Text nämlich am Rand der
Spielfläche.“ Nachgestellt am laufenden `arbiter` mit Chromium, Fenster 990×930, rohe
Mausereignisse, frische Seite: „Necron Warriors“ (Spieler 2) greifen und 150 px nach links zur
*Karte* ziehen. Die Karte folgt dem Zeiger nur, solange sie in der rechten Spalte liegt; was über
deren linken Rand hinausragt, wird nicht gezeichnet. Nach 150 px sieht man von der Karte nur
noch den rechten Zipfel („stellung“ vom Abzeichen „in Aufstellung“), nach weiteren Pixeln nichts.
Loslassen auf der *Karte* setzt die zehn Kreise trotzdem. Bei „Boyz“ (Spieler 1) dasselbe am
rechten Rand der linken Spalte, dort steht die Karte 70 px über, sie wird am Spaltenrand
abgeschnitten. Daneben ist beim Ziehen Text markiert (blauer Balken auf dem „z“ von „Boyz“):
[680](680-markierterTextSperrtDasZiehen.md).
Ursache, soweit sichtbar: `.spalte` in
[komponenten.css](../../technik/frontend/komponenten.css) hat `overflow-y: auto`, damit
ist `overflow-x` ebenfalls `auto` und beschneidet das per `transform` verschobene Kind. Das ist
ein anderer Fehler als 680 (Markieren) und 670 (Karte springt).

**Kosten.** Der Spieler zieht eine Karte, die er nicht mehr sieht; er weiß nicht, ob er sie noch
hält, und lässt sie los, bevor sie auf der *Karte* ist. Ziehen ist heute der einzige Weg zu
*setzen* (AUF-8.5); die Rückmeldung während des Ziehens ist das Einzige, was ihm den Weg zeigt.
Am Touchgerät deckt der Finger den Rest ab. Der Stakeholder hat entschieden
([683](683-aufstellenKlickenOderZiehen.md), F1 A): Das Ziehen der Karte entfällt, sobald das
Setzen per Klick gebaut ist. Bis dahin ist es der einzige Weg; ob sich die Berichtigung
lohnt, entscheidet der Implementierer mit dem Plan.

**Gegenvorschlag.** Die gezogene Karte bleibt auf der ganzen Seite sichtbar, solange sie
gehalten wird, über Spalte und *Karte* hinweg; wie, entscheidest du (Spalte beschneidet nur in
der Höhe, oder die Karte löst sich während des Ziehens aus der Spalte). Eine neue Komponente
oder ein neues Merkmal an `.einheitenKarte` ist ein Anliegen an den Architekten. Absichern mit
einem Test, der mit rohen Mausereignissen mitten im Ziehen prüft, dass die Karte am linken Rand
von Spieler 2 und am rechten Rand von Spieler 1 sichtbar ist (Playwright mit der Maus: Liegt
die Karte halb außerhalb der Spalte, liefert `elementFromPoint` an ihrer Mitte die Karte
selbst). Erledigt, wenn die Karte am
laufenden Arbiter in beiden Spalten bis auf die *Karte* sichtbar bleibt.

**Stellungnahme.** Angenommen, die Berichtigung ist klein und lohnt bis zum Klick-Setzen:
Solange eine Karte gezogen wird, beschneidet die Spalte nicht mehr (`.zieht .spalte` in
[komponenten.css](../../technik/frontend/komponenten.css)) und die Karte liegt obenauf
(`.gezogen`). Wegwerf-Versuch mit rohen Mausereignissen: Spieler 2 zieht 150 px nach links, die
Karte ist dort sichtbar. Der Test gehört dem Testautor. Nebenwirkung: Eine gescrollte Spalte
kann beim Ziehen springen; ohne Anlass nicht behandelt.
