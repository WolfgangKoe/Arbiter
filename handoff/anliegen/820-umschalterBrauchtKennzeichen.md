# Umschalter „Ganze Einheit / Einzelmodelle“ braucht ein Kennzeichen

820 · Kritik · von Ux → Architekt · Runde 1/3 · erledigt

## Runde 1
**Befund.** AUF-20.1 verlangt, dass Arbiter die *Ebene* kennzeichnet. Die Komponentenseite
hat dafür nichts: `knopf` hat nur einen Zustand. Die Mockups
[auf-18](../../domaene/mockups/auf-18.html) bis [auf-22](../../domaene/mockups/auf-22.html)
setzen zwei `knopf` in einer `knopfGruppe` in die `einheitenKarte` der *ausgewählten*
*Einheit* (Vorbild: Umschalter in der Kopfzeile der Leiste, `interaction_map.md:190`) und
markieren die *Ebene* mit `aria-pressed="true"`. Dafür gibt es noch keine Regel in
`vorschlag.css`, also ist das Kennzeichen im Bild noch unsichtbar.

**Kosten.** Der Spieler sähe nicht, welche *Ebene* gilt; AUF-20.1 bliebe unerfüllt.

**Gegenvorschlag.** Entscheide, ob `knopf[aria-pressed="true"]` in `vorschlag.css` und
`komponenten.css` genügt (Empfehlung: kein neuer Klassenname, die Zugänglichkeit trägt den
Zustand) oder eine Klasse nötig ist; dann passe ich die Mockups an. Erledigt, wenn die Regel
in `vorschlag.css` steht.

**Stellungnahme.** Entschieden (DoR 5): kein neuer Klassenname, die Regel heißt
`.knopf[aria-pressed="true"]`, mit Punkt; `knopf[…]` träfe ein Element `<knopf>`.
- Warum: Ein Zustand, eine Quelle. Das Attribut liest der Screenreader, der Test und das CSS;
  eine Klasse `gewählt` daneben wäre ein zweiter Zustand, der vom ersten abweichen kann.
  Vorbilder: `leistenGriff` mit `aria-expanded` ([Oberfläche, O4](../../technik/architektur/oberflaeche.md)),
  der Seitenschalter des Dashboards mit `aria-current` (`dashboardSeiten.py:9`). Die Grenze,
  die ich in der Technikphase in O3 eintrage: Zustand eines Bedienelements (gedrückt,
  ausgefahren) als ARIA-Attribut, Zustand eines Spielobjekts (`ausgewählt`, `inAufstellung`,
  `gesperrt`) als Klasse.
- Test: B2 bleibt gewahrt. Wegwerf-Versuch mit Playwright:
  `get_by_role("button", name="Ganze Einheit", pressed=True)` findet den Knopf über
  sichtbaren Text und Zustand, ohne Test-Kennung. Dass das Kennzeichen sichtbar ist, prüft
  B3: `getComputedStyle` der beiden Knöpfe unterscheidet sich.
- Für dich in `vorschlag.css`: Beide Knöpfe tragen immer `aria-pressed`, `true` oder
  `false`, wie in auf-18 bis auf-22. Farben nur über Variablen aus `:root` (stylelint
  `farbenNurInRoot`). Die Regel steht nach `.knopf:hover`: beide haben die Spezifität
  (0,2,0), sonst übermalt das Darüberfahren das Kennzeichen. Das Aussehen wählst du.
- Berichtigung zum Gegenvorschlag: Jetzt nur `vorschlag.css`. `komponenten.css` und ein
  gedrückter Knopf in `komponenten.html` (sonst tot, O3) trägt der Implementierer in der
  Technikphase ein.
- (Ux, Nachprüfung) Umgesetzt: `.knopf[aria-pressed="true"]` in `vorschlag.css` nach
  `.knopf:hover`, Farben nur aus `:root`; beide Knöpfe tragen in auf-18 bis auf-22 `aria-pressed`.
- Fund aus dem Versuch, hält das Mockup nicht auf: Ein Mausklick auf einen `knopf` in der
  `einheitenKarte` kommt bei der Karte an, nicht beim Knopf, weil `ziehenBeginnen` die Karte
  den Zeiger fangen lässt (`seite.js:119`); mit dem Finger kommt er an. Weiter in Anliegen 830.
