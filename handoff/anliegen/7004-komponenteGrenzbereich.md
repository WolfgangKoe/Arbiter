# Komponente für Grenzen als leichter Bereich

Form: Fragen
Von: Ux
An: Architekt
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Der Stakeholder wünscht in [Anliegen 6410](6410-grenzkreiseNahkampfUndBewegung.md) eine
wiederverwendbare Oberflächenkomponente: Sie zeigt die Grenze eines Bereichs leicht an, bei einem
*Modell* als Kreis, bei einer *Einheit* als Einhüllende der Kreise ihrer *Modelle*, später auch
für den Abstand zu einer *Aufstellungszone*. Farbe, Linienart und -dicke sind Parameter. Er
regt an, den Akzeptanztest dem Frontend zuzuordnen. In
[komponenten.css](../../technik/frontend/komponenten.css) steht sie noch nicht; die Regeln für
`grenzkreis` liegen vorläufig in [vorschlag.css](../../domaene/mockups/vorschlag.css).

**Kosten.** Bis zur Antwort bleibt `grenzkreis` im Vorschlag.

**Gegenvorschlag.** Komponente allgemein benennen, Parameter als Klassen, Einhüllende im Frontend
berechnet; wo der Test liegt, entscheidet der Architekt.

**Stellungnahme.**
