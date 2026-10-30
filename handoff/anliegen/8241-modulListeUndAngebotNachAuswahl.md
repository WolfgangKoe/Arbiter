# Modulliste der Seite und Angebot nach Auswählen

Form: Kritik
Von: Architekt
An: Architekt
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wartet (Architektur nachziehen, keine Prüfung rot), Diff `039da85..b14cdf7`,
Item gemeinsamUebergehen; Hinweis des Implementierers. Ich schreibe es, sobald der
Implementierer `technik/` freigibt.
1. [O5](../../technik/architektur/frontend.md) kennt `leisten.js` nicht, obwohl O4 es
   verlangt: Es fehlen der Pfeil `seite.js` → `leisten.js`, beim Einstieg „meldet das Ein-
   und Ausfahren an“, bei `anfragen.js` „hält die übergehbare Anfrage der letzten 409
   (V18)“ und unter `komponenten/` `protokoll.js`. Der Code hält O4 und die Richtung ein.
2. [V18](../../technik/architektur/vertrag/schlacht/uebergehen.md) bindet „gemeinsam
   übergehen“ an die `sperrmeldung`, die nach V7 auch ein Auswählen überdauert. Danach ist
   die Ebene eine andere, der Klick schickt die alte Anfrage, und Arbiter *setzt* die neue
   Ebene unter dem Einvernehmen über die alte *Sperre*
   ([8261](8261-uebergehenNachVertragUndAuswahl.md) Punkt 3).

**Kosten.** 1: Ein Leser sucht das Modul der *Leisten* in O5 vergeblich, drei Zeilen. 2: Am
Bildschirm selten; ohne Satz in V18 hat 8261 Punkt 3 keinen Maßstab. Ein Satz; im Code eine
Zeile in `anfragen.js` (Technikphase 10 nach 8261).

**Gegenvorschlag.**
1. O5 wie oben ergänzen.
2. V18: „Das Angebot endet mit der nächsten Antwort auf eine Handlung oder ein Auswählen
   (V2, V14); die `sperrmeldung` bleibt nach V7.“ Warum: Das Einvernehmen gilt der *Sperre*,
   die beide gesehen haben.

**Stellungnahme.** Angenommen, beide Punkte umgesetzt.
1. [O5](../../technik/architektur/frontend.md): Pfeil `seite.js` → `leisten.js` (O4),
   `seite.js` meldet das Ein- und Ausfahren an, `anfragen.js` hält die übergehbare Anfrage
   der letzten 409 (V18), unter `komponenten/` steht `protokoll.js`.
2. [V18](../../technik/architektur/vertrag/schlacht/uebergehen.md): Das Angebot endet mit der
   nächsten Antwort auf eine Handlung oder ein Auswählen (V2, V14), die `sperrmeldung` bleibt
   nach V7; Prüft: das Ende nach einem Auswählen nur Text. Der Code folgt mit
   [8261](8261-uebergehenNachVertragUndAuswahl.md) Punkt 3 (Technikphase 10).
