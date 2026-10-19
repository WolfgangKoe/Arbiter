# Kein Test hält die Zugschwelle von 4 Pixeln

622 · Kritik · von Reviewer → Testautor · Runde 1/3 · offen

## Runde 1
**Befund.** Ich habe in `technik/frontend/seite.js` probeweise `const zugschwelle = 4` auf `0`
gesetzt. Alle Akzeptanztests blieben grün. Damit prüft kein Test, was
[Handlungen, V8](../../technik/architektur/handlungen.md) festlegt: Ein Zug beginnt erst bei mehr als
4 Pixeln Abweichung, darunter ist es ein Klick (Anliegen 441).

**Kosten.** Mit Schwelle 0 wird jedes Drücken auf ein *gesetztes* *Modell*, bei dem Maus
oder Finger um ein Pixel zittert, zum Zug: Arbiter *setzt* das *Modell* neu, ab Item 2 von
[Plan 6](../plan.md) mit „Ganze Einheit“ die ganze *Einheit* (AUF-21.1). Am Touchgerät trifft
das fast jedes Tippen; kein Test fiele. An der *Ablage* lässt sich die Schwelle nicht mehr
prüfen: Nach Item 1 ([Setzen per Klick](../../domaene/items/setzenPerKlick.md)) zieht dort
niemand mehr eine *Einheit* (Anliegen 977).

**Gegenvorschlag.** Ein Bildschirmtest je Eingabe (Maus, Finger, B5): ein *gesetztes* *Modell*
auf der *Karte* drücken, um 3 Pixel bewegen, loslassen, mit `ziehenOhneAnfrage` aus
`tests/akzeptanz/ziehen.py`; erwartet: keine Handlung ging an den Server, jedes *Modell* steht
an seiner *Stelle* wie vorher. Das gilt heute (V8: ohne Zug auf einem *Modell* nichts) und
nach Item 1 (AUF-18.1: ein Klick auf ein *Modell* gilt keiner *Einheit*). Erledigt, wenn
dieselbe Probeänderung den Test rot macht.

**Stellungnahme.**
