# Oberfläche

Was der Browser zeigt; Aufbau von `web/` und Bildschirmtests: [Web](web.md).

Das Design-System gehört der Technik: die Komponentenseite (O3) als Doku und Vorlage der
Mockups. Eine neue Komponente ist ein Anliegen an die Technik.
Tot ist eine Komponente ohne Template. Messbare Gestaltungsregeln werden Prüfungen.
- **O1** HTML, CSS mit Variablen in `.css`, JavaScript-Module in `.js`; kein `<style>`, kein
  `style=` und kein Skript im HTML; kein Framework, kein Build-Schritt, kein Tailwind. Die
  Seite holt den Spielstand per `fetch` und zeichnet ihn in einem Schritt. Das Markup steht
  in `<template>` der Seite; `zeichnen.js` (O5) klont und füllt es, kein Modul erzeugt Elemente. Die
  Vorlage eines Elements der Karte steht in einem `<svg>` im `<template>`, sonst verliert es
  den SVG-Namensraum. Prüft: eslint und stylelint über `.js` und `.css`
  (`frontendregeln/frontend.py`), „keine Elemente“ mit `no-restricted-properties` und
  `no-restricted-syntax`; das `<svg>` die Bildschirmtests zu QUE-2; sonst nur Text.
- **O2** Die Karte ist ein SVG in Zoll: `viewBox` aus den Seitenlängen, `cx`, `cy`, `r` aus
  Stelle und Base, `r` aus `radiusInZoll` (`messen.py`); eine zweite Baseform ändert O2 mit
  (M1). Der Browser skaliert, gleich in x und y. Prüft: Akzeptanztests zu QUE-2.
- **O3** Die Komponentenseite ist `technik/frontend/komponenten.html` mit `komponenten.css`,
  gebaut aus `domaene/mockups/vorschlag.css`. Jede Seite verlinkt `komponenten.css`;
  Markup und CSS der Mockups übernimmt der Implementierer ohne Umschreiben. Klassen und
  Variablen deutsch, camelCase (`prozess/praemissen/wir.md`). Keine tote Klasse; eine neue
  Klasse in Mockups und `technik/frontend/*.html` nur über DoR 5
  ([Ablauf](../../prozess/ablauf.md#dor-item-bereit)): vom Architekten entschieden, in
  `vorschlag.css` übernommen, vom Implementierer in `komponenten.css` eingetragen. Prüft: nur
  Text.
- **O4** Drei Leisten wie in ArbiterMap: links, rechts, unten (Inhalt: Anliegen 366). Je
  Leiste ein `<aside class="leiste">` im festen Markup, nicht im `<template>`, mit Griff
  (`<button class="leistenGriff" aria-expanded>`). Ein- und Ausfahren ist Zustand der Seite,
  nicht des Spiels: ohne `fetch`, ohne Domäne; `leisten.js` kennt nur Griff und Leiste, wie
  `ArbiterMap/frontend/static/js/sidebar_handle.js`. Das Zeichnen füllt nur den Inhalt und
  lässt den Zustand; beim Laden gilt das Markup. Eine ausgefahrene Leiste nimmt der Karte
  Platz und verdeckt sie nicht, sonst läge eine *Aufstellungszone* darunter; die Karte
  skaliert (O2). Prüft: Bildschirmtests zu den Kriterien der Leisten.
- **O5** Die Seite sind JavaScript-Module mit je einer Aufgabe, je höchstens 8.000 Zeichen
  ([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße)), Importe nur in Pfeilrichtung:
  `seite.js` → `bedienung.js` → `anfragen.js` → `zeichnen.js`, dazu `seite.js` → `anfragen.js`.
  - `seite.js`: Einstieg aus `index.html`; meldet die Ereignisse von `bedienung.js` am
    Dokument an und zeichnet den ersten Spielstand.
  - `bedienung.js`: was Zeiger und Klick bedeuten (V8, V10), mit dem Zustand des Zugs.
  - `anfragen.js`: Pfade, `fetch`, Antworten (V1, V2, V5, V9, V10); hält den letzten
    Spielstand und die `gründe` der letzten 409 (V7). Die Knöpfe der `knopfGruppe` als
    Tabelle Text → Handlung und wann angeboten (V7); ein neuer Knopf ist eine Zeile, kein
    Zweig in `zeichnen.js`.
  - `zeichnen.js`: Spielstand, `gründe` und Knöpfe → Markup (O1), ohne `fetch` und Zustand.

  Warum: Zeichnen liest sich ohne Server, Bedienung ohne Vorlagen. Prüft: Verhalten die
  Bildschirmtests; Richtung und Größe nur Text, Kritik am Code.
