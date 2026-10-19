# Ein Knopf in der Einheitenkarte bekommt keinen Mausklick

830 · Kritik · von Architekt → Implementierer · Runde 1/3 · offen · wartet auf die Technikphase

## Runde 1
**Befund.** Die Mockups [auf-18](../../domaene/mockups/auf-18.html) bis
[auf-22](../../domaene/mockups/auf-22.html) setzen „Ganze Einheit“ und „Einzelmodelle“ als
`knopf` in die `einheitenKarte` (AUF-20.1, Anliegen 820). `ziehenBeginnen` in
[seite.js](../../technik/frontend/seite.js) sucht beim Drücken mit
`closest(".karte .modell, .einheitenKarte")` die Karte und lässt sie den Zeiger fangen
(`setPointerCapture`). Ein Wegwerf-Versuch mit Playwright und Chromium zeigt: Ein Mausklick
auf „Einzelmodelle“ kommt dann bei der Karte an (`SECTION`), nicht beim Knopf; ein Tippen
mit dem Finger kommt beim Knopf an. `ziehenBeenden` ruft danach `klicken` der Karte auf.

**Kosten.** Mit der Maus wechselt der *Spieler* die *Ebene* nie (AUF-20.3); stattdessen
geschieht, was ein Klick auf die Karte tut. Maus und Touch verhielten sich verschieden
(`domaene/ziel.md`).

**Gegenvorschlag.** Ein Druck auf einen `knopf` beginnt keinen Zug: `ziehenBeginnen` kehrt
früh zurück, wenn `ereignis.target.closest(".knopf")` etwas findet. Den Satz trage ich in
der Technikphase in [V8](../../technik/architektur/handlungen.md) ein. Erledigt, wenn ein
Bildschirmtest zu AUF-20.3 mit der Maus (`page.mouse`, B5) und mit dem Finger grün ist.

**Stellungnahme.**
