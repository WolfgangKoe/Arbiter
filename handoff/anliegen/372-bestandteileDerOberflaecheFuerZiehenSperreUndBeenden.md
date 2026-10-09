# Neue Bestandteile der Oberfläche für Sperre und Beenden

372 · Fragen · von UX (Domäne) → Architekt (Technik) · Runde 1/3 · erledigt

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde)

## Runde 1
**Befund.** Die Mockups zu AUF-8, AUF-9, AUF-10 und AUF-12
([8](../../domaene/mockups/auf-8.html), [9](../../domaene/mockups/auf-9.html),
[10](../../domaene/mockups/auf-10.html), [12](../../domaene/mockups/auf-12.html)) brauchen
drei Bestandteile, die die [Komponentenseite](../../technik/frontend/komponenten.html) nicht
hat (O3). Mein Vorschlag steht schon in
[vorschlag.css](../../domaene/mockups/vorschlag.css), damit der Stakeholder die Mockups
sieht; er gilt erst mit deiner Entscheidung:
1. `knopf`: Schaltfläche („zurück“, „Aufstellen der Einheit beenden“), `<button>` unter der
   *Karte*.
2. `sperrmeldung` mit `sperrmeldungGrund`: Liste, ein Eintrag je *Grund* (AUF-9.1, AUF-10.4,
   AUF-12.3), unter der *Karte*, `role="alert"`.
3. `modell gesperrt`: Kennzeichen an der *Karte* (AUF-9.1), halbtransparent mit gestricheltem
   Rand in `--akzentHell`; `ausgewählt` bleibt der volle weiße Rand (AUF-5.7).
Dazu eine Änderung an `spalteMitte`: `flex-wrap` und `gap`, damit Meldung und Knöpfe unter
die *Karte* rücken.

**Kosten.** Ohne Entscheidung ist DoR 5 für AUF-9, AUF-10 und AUF-12 nicht erfüllt.

**Gegenvorschlag.** Du wählst andere Namen oder Orte; ich passe Mockups und
`vorschlag.css` an. „gemeinsam übergehen“ fehlt noch (Plan 6).

**Stellungnahme.** Entschieden: Namen und Orte wie vorgeschlagen, mit diesen Änderungen; du
übernimmst sie wörtlich in `vorschlag.css` und die Mockups (DoR 5).
1. `knopf` gilt; die Knöpfe stehen gemeinsam in `<div class="knopfGruppe">` unter der
   `sperrmeldung`. Grund: Bei 1366 × 768 lagen *Grund* und Knöpfe in auf-9, auf-10 und auf-12
   unter dem Bildschirmrand (mit Playwright gemessen), weil die *Karte* die ganze Höhe nahm.
2. `spalteMitte` wird ein Raster, die *Karte* füllt die übrige Höhe. Im Wegwerf-Versuch sind
   so bei 1280 × 800 und 1366 × 768 Karte, *Grund* und Knöpfe ganz sichtbar. Folge: Erscheint
   eine Meldung, wird die *Karte* nach dem Loslassen etwas kleiner.
   ```css
   .spalteMitte {
     grid-column: 2;
     display: grid;
     grid-template-rows: minmax(0, 1fr);
     grid-auto-rows: auto;
     gap: 0.75rem;
     justify-items: center;
   }

   .knopfGruppe {
     display: flex;
     flex-wrap: wrap;
     gap: 0.75rem;
     justify-content: center;
   }
   ```
   In `.karte` steht `height: 100%;` statt `max-height: 100%;`, in `.sperrmeldung`
   `width: 100%;` statt `flex-basis: 100%;`.
3. `sperrmeldung` gilt, ohne `role="alert"`: Die Rolle ersetzt die der Liste, die Einträge
   stünden dann ohne Liste; der Bildschirmtest findet sie über die Klasse
   ([Web, B2](../../technik/architektur/web.md#bildschirmtests)).
4. `modell gesperrt` gilt so.
5. Neu, für QUE-3.4: `.karte` und `.einheitenKarte` bekommen `touch-action: none;`.
   Wegwerf-Versuch (Chromium, Finger über CDP `Input.dispatchTouchEvent`): Ohne die Zeile
   bricht der Browser das Ziehen mit dem Finger nach dem ersten Schritt ab (`pointercancel`);
   an einem `<circle>` wirkt sie nicht, nur am `<svg>`. Folge: Auf *Karte* und Einheitenkarte
   scrollt der Finger nicht.

**Nachprüfung.** Erledigt: `vorschlag.css` und alle Mockups übernehmen Raster `spalteMitte`,
`knopfGruppe`, `width: 100%` an `sperrmeldung`, `height: 100%` und `touch-action: none` an
`.karte` und `.einheitenKarte`; `role="alert"` entfällt.
