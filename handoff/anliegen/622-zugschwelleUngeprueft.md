# Kein Test hält die Zugschwelle von 4 Pixeln

622 · Kritik · von Reviewer → Testautor · Runde 1/3 · offen

## Runde 1
**Befund.** Ich habe in `technik/frontend/seite.js` probeweise `const zugschwelle = 4` auf `0`
gesetzt. Alle Akzeptanztests blieben grün. Damit prüft kein Test, was
[Web, V8](../../technik/architektur/web.md) festlegt: Ein Zug beginnt erst bei mehr als
4 Pixeln Abweichung, darunter ist es ein Klick (Anliegen 441).

**Kosten.** Mit Schwelle 0 wird ein Klick auf eine Karte der *Ablage*, bei dem Maus oder
Finger um ein Pixel zittert, zum Zug ohne Ziel: Die *Einheit* wird nicht *ausgewählt*. Am
Touchgerät trifft das fast jedes Tippen; kein Test fiele.

**Gegenvorschlag.** Ein Bildschirmtest je Eingabe (Maus, Finger): auf eine Karte der *Ablage*
drücken, um 3 Pixel bewegen, loslassen; erwartet: die Karte ist *ausgewählt*, keine Handlung
ging an den Server. Erledigt, wenn dieselbe Probeänderung den Test rot macht.

**Stellungnahme.**
