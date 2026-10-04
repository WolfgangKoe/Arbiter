# que-2.html: Die Karte steht allein in der linken Spalte

236 · Kritik · von Architekt (Technik) → UX · Runde 1/3 · angenommen

## Runde 1
**Befund.** In [que-2.html](../../domaene/mockups/que-2.html) hat `main.spielbereich` ein
einziges Kind, `div.spalte.spalteMitte`. [vorschlag.css](../../domaene/mockups/vorschlag.css)
gibt `.spielbereich` drei Spalten (`1fr 2fr 1fr`); das Raster setzt das einzige Kind in die
erste, schmale Spalte. Ein Bildschirmfoto mit Chromium (1400×900) zeigt die Karte links,
gut 300 px breit, rechts davon eine leere Fläche; in
[auf-4-ausgangslage.html](../../domaene/mockups/auf-4-ausgangslage.html) steht sie richtig
in der Mitte, weil dort die zwei `aside` davor und dahinter stehen.

**Kosten.** Plan 3: „Reicht der Zyklus nicht, fällt Item 2.“ Dann übernimmt der
Implementierer que-2.html ohne Umschreiben (Anliegen 151), und die Karte des Inkrements
steht am linken Rand. Auch mit Item 2 hängt die Lage der Karte an ihren Geschwistern: Eine
Komponente, die nur richtig sitzt, wenn andere da sind, ist auf der Komponentenseite nicht
für sich zu zeigen.

**Gegenvorschlag.** In `vorschlag.css` eine Zeile, `.spalteMitte { grid-column: 2; }`: Die
Mitte sitzt dann immer in der Mitte, mit und ohne `aside`; in einer Kopie unter `/tmp`
geprüft, beide Bilder wie erwartet. Erledigt, wenn que-2.html die
Karte in der mittleren Spalte zeigt und auf-4-ausgangslage.html unverändert aussieht.

**Stellungnahme.** (UX) Angenommen. `.spalteMitte` hat in [vorschlag.css](../../domaene/mockups/vorschlag.css) jetzt `grid-column: 2;`. que-2.html bleibt unverändert und zeigt die Karte in der Mitte; auf-4-ausgangslage.html sieht gleich aus, da dort die Mitte ohnehin die zweite Spalte ist.
