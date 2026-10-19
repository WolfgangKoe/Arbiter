# Ruhige Karte: kein Mockup, und die Mockups lassen die Karte springen

922 · Kritik · von Architekt → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.** Item 3 [Ruhige Karte](../../domaene/items/ruhigeKarte.md) ändert die Oberfläche,
hat aber kein Mockup (DoR 5). Die Mockups von Item 1 und 2 zeigen genau den Sprung, den
[QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md) verbietet: In
`vorschlag.css` hat `.spalteMitte` die Zeilen `minmax(0, 1fr)` für die *Karte* und `auto`
darunter. In [auf-19](../../domaene/mockups/auf-19.html) und
[auf-22](../../domaene/mockups/auf-22.html) steht die `sperrmeldung` in einer solchen Zeile,
in [auf-18](../../domaene/mockups/auf-18.html) fehlt sie; die *Karte* ist in auf-19 also
niedriger, das *Spielfeld* kleiner gezeichnet (gemessen in
[670](670-karteSpringtWennEinGrundErscheint.md): 741 gegen 689 Pixel). Ebenso
`kopfzeileAnDerReihe`, das nach der letzten *Einheit* fehlt. Markup und CSS der Mockups
übernimmt der Implementierer ohne Umschreiben (O3); wo *Grund* und Knöpfe stattdessen stehen,
entscheiden nach 670 UX und Architekt, und das hat niemand getan.

Einordnung nach Ich 3: hält auf für Item 3. Ohne Mockup erfindet der Implementierer die
Anordnung oder schreibt das CSS der Mockups um, beides gegen O3; der Plan nennt das Item
trotzdem bereit.

**Kosten.** Ein Mockup mit festem Platz unter der *Karte* (oder anderswo) für den längsten
Fall: drei *Gründe* (AUF-3.5) oder *Grund* mit Zusatz ([921](921-zeileUnterDemGrundIstKeinGrund.md)),
dazu „zurück“, „gemeinsam übergehen“, „Aufstellen der Einheit beenden“; die Kopfzeile in
fester Höhe. Leerer Platz, solange nichts gesperrt ist, ist der Preis.

**Gegenvorschlag.** Ein Mockup `que-7.html`, das die Lage von auf-18 und auf-19 mit gleich
großer *Karte* zeigt, Gerüst aus vorhandenen Klassen, die Höhen in `vorschlag.css`. Mein
Vorschlag fürs Gerüst: `.spalteMitte` mit `grid-template-rows: minmax(0, 1fr)` und einer
zweiten Zeile fester Höhe, in der `sperrmeldung` und `knopfGruppe` liegen, sichtbar oder
nicht; die Kopfzeile behält ihre Höhe auch ohne „an der Reihe“. Eine neue Klasse entscheide
ich hier, wenn du eine brauchst. Reicht das vor der Freigabe nicht, rückt Item 3 in Plan 7,
wie der Plan es für den Engpass schon vorsieht; das sagst du dem Planer. Erledigt, wenn das
Mockup im Item verlinkt ist oder Item 3 nicht mehr im Plan steht.

**Stellungnahme.** Einverstanden, ohne neue Klasse. [que-7](../../domaene/mockups/que-7.html)
zeigt den längsten Fall: drei *Gründe* (Namen aus QUE-1.2, QUE-1.3, AUF-3.2), „zurück“,
„gemeinsam übergehen“, „Aufstellen der Einheit beenden“. In `vorschlag.css` hat `.spalteMitte`
drei feste Zeilen (*Karte*, `sperrmeldung` 7,5 rem, `knopfGruppe` 6 rem); beide liegen per
`grid-row` in ihrer Zeile, auch wenn die andere fehlt. `kopfzeileSpieler` hat feste Mindesthöhe,
so ändert „an der Reihe“ die Kopfzeile nicht. Die Höhen sind geschätzt, nicht im Browser
gemessen; der Architekt oder der Implementierer messen sie gegen 670. Empfehlung: Item 3 braucht
nur noch den Link auf que-7 im Item; das Item verlinkt der Planer, Plan 7 ist nicht nötig.
