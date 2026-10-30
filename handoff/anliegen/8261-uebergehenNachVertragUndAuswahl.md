# Übergehen nach Vertrag, Angebot nach Auswahlwechsel

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Wartet (Kritik: Randfälle abseits des Happy Path, Form von Hilfsfunktionen, keine
Prüfung rot), Diff `039da85..b14cdf7`, Item gemeinsamUebergehen.
1. `Schlacht.modellLoslassen` in
   [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) prüft nur
   `gründe <= übergehen`. [V18](../../technik/architektur/vertrag/schlacht/uebergehen.md)
   verlangt „sind die *Gründe* übergehbar und alle in `übergehen`“; QUE-5.5 steht nur in
   `Sperre.übergehbar`, das hier nicht gefragt wird, und der Dienst nimmt „keine Kohärenz“ in
   `übergehen` an. Heute unerreichbar, weil `gründeBeimZiehen` nie ‚keine Kohärenz‘ liefert.
2. Ebenda `if gründe and self._amZug is not None`: Bei *Gründen* ist `_amZug` nie `None`
   (sonst liefert `_stellenMitGründen` keine), und `einheitVon` läuft zweimal. Toter Teil der
   Bedingung, ein gleichwertiger Mutant.
3. [anfragen.js](../../technik/frontend/anfragen.js): `übergehbareAnfrage` setzt nur
   `handlungSenden` zurück. Wählt ein *Spieler* nach der *Sperre* eine Einheit oder ein *Modell*
   an (`zeichneAntwort`), bleibt „gemeinsam übergehen“ stehen; der Klick schickt die alte
   Anfrage, und Arbiter *setzt* die neue Ebene unter dem alten Einvernehmen.
4. [komponenten.css](../../technik/frontend/komponenten.css): Seit `index.html` die *Leisten*
   fest enthält, gilt `.spielbereich:has(> .leiste)` immer; `grid-template-columns: 1fr 2fr 1fr`
   in `.spielbereich` ist tot, `.spalte` trägt nur noch die Mitte.

**Kosten.** Heute keine am Bildschirm außer 3 (selten). Bleibt 1, übergeht der Dienst
‚keine Kohärenz‘, sobald eine solche *Sperre* beim Ziehen dazukommt; bleibt 2, zählt der
Mutationslauf einen Überlebenden; bleibt 4, sucht ein Leser zwei Raster. Je Punkt wenige Zeilen.

**Gegenvorschlag.**
1. Die *Sperre* einmal bilden und fragen:
   `sperre = Sperre(*gründe, übergehbar=True)`, ausgelöst, wenn
   `not (sperre.übergehbar and gründe <= übergehen)`; ohne *Gründe* wie bisher.
2. `_stellenMitGründen` liefert *Einheit* und *Spieler* mit, die Bedingung ist nur `if gründe`.
3. `übergehbareAnfrage` (wie die *Gründe* der Meldung) auch bei einer erfolgreichen Antwort in
   `zeichneAntwort` zurücksetzen, oder V7 sagt, warum die Meldung bleibt.
4. Die beiden Regeln zu `.spielbereich` zusammenlegen, `.spalte` in `.spalteMitte` aufgehen
   lassen.

**Stellungnahme.**
