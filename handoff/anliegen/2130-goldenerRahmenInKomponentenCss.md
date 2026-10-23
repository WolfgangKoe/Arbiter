# Goldener Rahmen in komponenten.css

Form: Kritik
Von: Fachkritiker
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet. Die *ausgewählte*
*Einheit* in der *Ablage* bekommt einen goldenen Rahmen, wie [Plan 6](../plan.md), Schritt 2, und
der Kommentar des Stakeholders zur Freigabe es verlangen und wie ArbiterMap ihn zeichnet
(`ArbiterMap/frontend/static/js/deployment.js:77`, `ring-amber-400`). UX hat das in Anliegen 1480
in [vorschlag.css](../../domaene/mockups/vorschlag.css) übernommen:
`.einheitenKarte.ausgewählt` mit `outline: 2px solid var(--akzentHell);`. Im Gebauten steht noch
der Rahmen in der Farbe des *Spielers*
([komponenten.css](../../technik/frontend/komponenten.css), `.einheitenKarte.ausgewählt`,
`var(--spielerFarbe)`). Kein Mechanismus trägt die geänderte Regel in die Komponentenseite;
ohne dieses Anliegen geht sie verloren.

**Kosten.** Eine Zeile CSS, kein Test ändert sich: Kein Test prüft die Farbe. Bleibt sie aus,
sieht der Stakeholder im nächsten Review weiter einen roten oder blauen Rahmen statt des
goldenen aus seinem freigegebenen Plan.

**Gegenvorschlag.** In `technik/frontend/komponenten.css` bei `.einheitenKarte.ausgewählt`
`var(--spielerFarbe)` durch `var(--akzentHell)` ersetzen, wörtlich wie in `vorschlag.css`
([DoR 5](../../prozess/ablauf.md#dor-item-bereit)). `.modell.ausgewählt` bleibt, wie es ist.

**Stellungnahme.** Angenommen und umgesetzt: `.einheitenKarte.ausgewählt` in
[komponenten.css](../../technik/frontend/komponenten.css) nutzt `var(--akzentHell)`.
