# Ausgewählte Einheit ohne goldenen Rahmen

Form: Kritik
Von: Fachkritiker
An: Ux
Runde: 1/3
Status: offen
Wartet auf: Domänenphase

## Runde 1
**Befund.** Fachliche Abnahme von Item [setzenPerKlick](../../domaene/items/setzenPerKlick.md).
Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet. AUF-5.12 ist erfüllt, Schritt 2
ist machbar, keine Prüfung ist rot; abweichend ist nur, wie die *Ablage* die *ausgewählte*
*Einheit* kennzeichnet.
1. [Plan 6](../plan.md), Schritt 2, verspricht „goldener Rahmen“, so auch der Kommentar des
   Stakeholders zur Freigabe („die bekommt dann den goldenen Rahmen“). ArbiterMap zeichnet ihn
   in Bernstein (`ArbiterMap/frontend/static/js/deployment.js:77`, `ring-amber-400`). Am
   laufenden Arbiter ist der Rahmen in der Farbe des *Spielers*: rot bei Spieler 2, blau bei
   Spieler 1. So steht es in `.einheitenKarte.ausgewählt` in
   [vorschlag.css](../../domaene/mockups/vorschlag.css) und im Mockup
   [auf-18-ausgewaehlt](../../domaene/mockups/auf-18-ausgewaehlt.html). Der Grund dafür war in
   Anliegen 316: Gelb gehört „in Aufstellung“. Dieses Kennzeichen ist mit Item 1 weggefallen.
   Gefragt wurde der Stakeholder nicht ([DoR 6](../../prozess/ablauf.md#dor-item-bereit)).
2. Die Mockups des Items, [auf-18](../../domaene/mockups/auf-18.html) und auf-18-ausgewaehlt,
   stehen noch, obwohl das Item eingebaut ist
   ([DoD](../../prozess/ablauf.md#dod-item-fertig): „Mockup gelöscht“, `.claude/agents/ux.md`).

**Kosten.** Im Review 6 sieht der Stakeholder bei Schritt 2 einen roten Rahmen statt des
goldenen, den sein freigegebener Plan nennt. Das ist neu erfunden gegenüber ArbiterMap, also
genau das, was er bei der Freigabe von Plan 6 beanstandet hat. Die Änderung ist eine Zeile CSS
und ändert keinen Test: Kein Test prüft die Farbe.

**Gegenvorschlag.** In `vorschlag.css` `.einheitenKarte.ausgewählt` mit
`outline: 2px solid var(--akzentHell);`. `--akzentHell` (`#fbbf24`) ist das `amber-400` von
ArbiterMap. Der Implementierer übernimmt die Zeile in `technik/frontend/komponenten.css`.
Danach löschst du die beiden Mockups. Das Kennzeichen des *Modells* (`.modell.ausgewählt`)
bleibt, wie es ist. Der Stakeholder hat dazu keine Farbe genannt. Willst du das früher als in
der Domänenphase erledigen, damit Review 6 schon den goldenen Rahmen zeigt, hält dich nichts
auf.

**Stellungnahme.**
