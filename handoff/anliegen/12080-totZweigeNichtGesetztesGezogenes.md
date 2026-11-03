# Tote Zweige für ein nicht gesetztes gezogenes Modell

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (DoD 2, Urteil: tot), Kritik am Code zu Item loslassenNebenDerKarte.
Seit `Aufstellung.stellenBeimLoslassen` für ein nicht *gesetztes* *Modell* vorab `Gezeigt({})`
gibt (AUF-16.7,
[\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py) Zeile 88),
ist das gezogene *Modell* in seinen beiden einzigen Aufrufen immer *gesetzt*. Damit erreichen
nur noch Unit-Tests zwei Zweige:
- `verschobeneStellen`, `if davor is None: return {gezogenes: ziel}`
  ([einheitVerschieben.py](../../technik/arbiter/domaene/phasen/aufstellen/einheitVerschieben.py)
  Zeile 20), Test `testEinNochNichtGesetztesModellBewegtDieGruppeNicht`;
- `angehalten`, `if davor is None: return dict(neue)`
  ([anhaltenAnEinerBase.py](../../technik/arbiter/domaene/phasen/aufstellen/anhaltenAnEinerBase.py)
  Zeile 11), Test `testEinNichtGesetztesGezogenesModellWirdNichtAngehaltenAuchAufEinerFremdenBase`.

Die Unit-Tests sagen ein Verhalten zu, das das Produkt nicht mehr hat: Ein nicht *gesetztes*
*Modell* wird beim Loslassen nicht mehr *gesetzt*, sondern bleibt, wo es war.

**Kosten.** Vier Zeilen Code und zwei Unit-Tests weniger. Bleiben sie, liest man darin einen
Weg, ein *Modell* per Loslassen zu *setzen*, den es nicht gibt, und Mutanten dort zählen gegen
die Schwelle.

**Gegenvorschlag.** Beide Zweige und die beiden Unit-Tests löschen; `davor = gruppe[gezogenes]`
und `davor = stellen[gezogenes]`. Die Vorbedingung *gesetzt* steht dann einmal, in
`stellenBeimLoslassen`.

**Stellungnahme.** (Implementierer) Angenommen und umgesetzt: beide Zweige und beide
Unit-Tests gelöscht, die Vorbedingung steht einmal in `stellenBeimLoslassen`.
