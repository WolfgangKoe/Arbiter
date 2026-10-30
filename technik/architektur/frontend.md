# Frontend: was der Browser zeigt

[Übersicht](../architektur.md); das Backend dahinter: [Web](web.md); Bildschirmtests:
[Tests](tests.md#bildschirmtests).

- **O1** HTML, CSS mit Variablen in `.css`, JavaScript-Module in `.js`; kein `<style>`, kein
  `style=` und kein Skript im HTML; kein Framework, kein Build-Schritt, kein Tailwind. Die
  Seite holt den Spielstand per `fetch` und zeichnet ihn in einem Schritt. Das Markup steht
  in `<template>` der Seite; die Komponenten (O5) klonen und füllen es, kein Modul erzeugt
  Elemente. Die Vorlage eines Elements der Karte steht in einem `<svg>` im `<template>`, sonst
  verliert es den SVG-Namensraum. Prüft: eslint und stylelint über `.js` und `.css`
  (`frontendregeln/frontend.py`), „keine Elemente“ mit `no-restricted-properties` und
  `no-restricted-syntax`; das `<svg>` die Bildschirmtests zu QUE-2; sonst nur Text.
- **O2** Die Karte ist ein SVG in Zoll: `viewBox` aus den Seitenlängen, `cx`, `cy`, `r` aus
  Stelle und Base, `r` aus `radiusInZoll` (`messen.py`); eine zweite Baseform ändert O2 mit
  (M1). Der Browser skaliert, gleich in x und y. Prüft: Akzeptanztests zu QUE-2.
- **O3** Das Design-System gehört der Technik: die Komponentenseite
  `technik/frontend/komponenten.html` mit `komponenten.css`, gebaut aus
  `domaene/mockups/vorschlag.css`. Jede Seite verlinkt `komponenten.css`; Markup und CSS der
  Mockups übernimmt der Implementierer ohne Umschreiben und ersetzt nur Beispielinhalte.
  Klassen und Variablen deutsch, camelCase. Keine tote Klasse, keine Komponente ohne
  Vorlage; eine neue Klasse in Mockups und `technik/frontend/*.html` nur über DoR 5
  ([Ablauf](../../prozess/ablauf/dor.md)): vom Architekten entschieden, in `vorschlag.css`
  übernommen, vom Implementierer in `komponenten.css` eingetragen. Messbare
  Gestaltungsregeln werden Prüfungen (stylelint, O1). Prüft: nur Text.
- **O4** Drei Leisten wie in ArbiterMap: links, rechts, unten (Inhalt: Anliegen 366). Je
  Leiste ein `<aside class="leiste">` im festen Markup, nicht im `<template>`, mit Griff
  (`<button class="leistenGriff" aria-expanded>`). Ihr `aria-label` nennt den Inhalt mit
  Begriffen des Glossars („Armeeliste Spieler 1“, „Protokoll“), das des Griffs dazu „ein- und
  ausfahren“ (`ArbiterMap/frontend/templates/map.html:122`); ein Screenreader unterscheidet
  gleichartige Bereiche nur am Namen (SonarLint Web:S5255). Ein- und Ausfahren ist Zustand
  der Seite: `leisten.js` kennt nur Griff und Leiste, ohne `fetch` und Domäne; das Zeichnen
  füllt nur den Inhalt. Eine ausgefahrene Leiste nimmt der Karte Platz, statt eine
  *Aufstellungszone* zu verdecken (O2). Prüft: Bildschirmtests zu den Kriterien der Leisten,
  über Rolle und Namen (`get_by_role`).
- **O5** Die Seite sind JavaScript-Module mit je einer Aufgabe, Importe nur in Pfeilrichtung:
  `seite.js` → `bedienung.js` → `anfragen.js` → `zeichnen.js` → `komponenten/`, dazu
  `seite.js` → `anfragen.js`.
  - `seite.js`: Einstieg aus `index.html`; meldet die Ereignisse von `bedienung.js` am
    Dokument an und zeichnet den ersten Spielstand.
  - `bedienung.js`: was Zeiger und Klick bedeuten (V8, V10), mit dem Zustand des Zugs.
  - `anfragen.js`: Pfade, `fetch`, Antworten (V1, V2, V5, V9, V10); hält den letzten
    Spielstand und die `gründe` der letzten 409 (V7). Die Knöpfe der `knopfGruppe` als
    Tabelle Text → Handlung und wann angeboten (V7); ein neuer Knopf ist eine Zeile.
  - `zeichnen.js`: setzt aus Spielstand, `gründe` und Knöpfen die Komponenten zur Seite
    zusammen, ohne `fetch` und Zustand.
  - `komponenten/`: je Komponente ein Modul, benannt nach der Klasse ihrer Vorlage
    (`kopfzeile.js`, `armeeKarte.js`, `sperrmeldung.js`, `knopfGruppe.js`, `karte.js`,
    `grenze.js`). Es füllt seine Vorlage und kennt keine Regel, nur Formen, *Abstände* und
    Art; Komponenten importieren nur Komponenten. Das Klonen einer Vorlage, auch einer im
    `<svg>` (O1), und die Farbe des Spielers stehen einmal in `komponenten/vorlage.js`.

  Warum: Zeichnen liest sich ohne Server, Bedienung ohne Vorlagen, eine Komponente ohne die
  Seite. Prüft: Verhalten die Bildschirmtests; Richtung nur Text, Kritik am Code.
