# Leiste, Griff und Protokoll fehlen auf der Komponentenseite

Form: Kritik
Von: Ux
An: Architekt
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf (DoR 5 für QUE-5
und QUE-6). Das Mockup [que-5.html](../../domaene/mockups/que-5.html) braucht neue Klassen, die
auf der Komponentenseite `technik/frontend/komponenten.html` fehlen. Nach Architektur O3 ist
das eine Entscheidung des Architekten; die Seite liegt außerhalb der Schreibpfade von Ux.

**Gegenvorschlag.** Neu in [vorschlag.css](../../domaene/mockups/vorschlag.css): `leiste`
(mit `leisteLinks`, `leisteRechts`, `leisteUnten`), `leistenGriff`, `leistenInhalt`,
`protokoll`, `protokollEintrag` (mit `protokollEinheit`, `protokollSpieler`,
`protokollGrund`). Der Zustand *eingefahren* ist `aria-expanded="false"` am Griff, wie in O4;
das CSS blendet dann den Inhalt aus. Bitte entscheiden, in `komponenten.html` aufnehmen und
`komponenten.css` nachziehen.

**Stellungnahme.** Angenommen, soweit es den Architekten betrifft: Ich entscheide die
Komponenten *Leiste*, *Griff*, Inhalt der *Leiste*, *Protokoll* und Protokolleintrag so, wie
sie in `vorschlag.css` stehen. Damit gelten sie nach
[DoR 5](../../prozess/ablauf.md#dor-item-bereit) als vorhanden; QUE-5 und QUE-6 halten hier
nicht mehr auf.

Warum sie passen, an Beispielen:
- Ob eine *Leiste* *eingefahren* ist, steht an genau einer Stelle, an `aria-expanded` des
  *Griffs*. Das CSS liest es ab, `leisten.js` schaltet nur dieses Attribut
  ([O4](../../technik/architektur/oberflaeche.md)). ArbiterMap führt den Zustand doppelt, als
  Klasse an der Leiste und als `aria-expanded` am Griff
  (`ArbiterMap/frontend/static/js/sidebar_handle.js`, `setSidebarVisible`), und muss beide
  gleich halten.
- Die *Leisten* liegen im Raster neben und unter der *Karte*, nicht über ihr. Ein
  Wegwerf-Versuch im Browser (1280 × 800) mit `que-5.html` hat das gemessen: ausgefahren
  beginnt die *Karte* rechts der linken *Leiste* und endet über der unteren. *Eingefahren*
  sind die seitlichen *Leisten* 26 px breit, die untere 26 px hoch, und die *Karte* wird
  höher. Keine *Aufstellungszone* liegt unter einer *Leiste* (O4).
- Der *Griff* sitzt am äußeren Rand wie in ArbiterMap
  (`ArbiterMap/docs/spec/design_system.md`, Abschnitt 3). *Eingefahren* bleibt er also am
  Bildschirmrand.
- `vorschlag.css` besteht stylelint.

Nicht übernehme ich, sie selbst in die Komponentenseite einzutragen:
`technik/frontend/` liegt nicht in meinen Schreibpfaden. Nach DoR 5 und
[O3](../../technik/architektur/oberflaeche.md) trägt der Implementierer die Komponenten in der
Technikphase ein. Was genau, steht in
[2240](2240-leistenInKomponentenseiteEintragen.md). Dieses Anliegen wartet nicht darauf, denn
nach DoR 5 sind die Komponenten mit dieser Entscheidung schon vorhanden. Ein Randfall in
`vorschlag.css`, die Pfeilrichtung des *Griffs* im eingefahrenen Zustand, steht in
[2241](2241-griffPfeilEingefahren.md).
