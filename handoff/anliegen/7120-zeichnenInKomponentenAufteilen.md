# zeichnen.js in Komponenten aufteilen

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 6995 F3 A gewählt und kommentiert: „Wenn mehrere
Funktionen in "index" sind, wäre es so langsam an der Zeit, diese aufzuteilen. Wir werden
noch mehr Buttons, Karten, Bereiche usw. haben.“ Zugesagt war die Aufteilung für die
Technikphase 9. Die Architektur verlangt sie jetzt
([Frontend, O5](../../technik/architektur/frontend.md)): je Komponente ein Modul in
`technik/frontend/komponenten/`, benannt nach der Klasse ihrer Vorlage; es füllt seine
Vorlage und kennt keine Regel. Heute füllt
[`zeichnen.js`](../../technik/frontend/zeichnen.js) alles selbst: Kopfzeile
(`kopfzeile`, `kopfzeilenSpieler`, `kopfzeilenTitel`), *Armeeliste* (`armeeKarte`,
`einheitenKarte`), Sperrmeldung, Knöpfe (`knopf`, `knopfGruppe`), *Karte* (`karte`,
`modellKreis`). Einordnung: wartet auf die Technikphase, also jetzt; keine Prüfung ist rot,
kein Schritt des Happy Path hängt daran. Item 4 (*Grenzkreise*) legt `komponenten/grenze.js`
ohnehin an ([Vertrag](../../technik/architektur/vertrag/bewegung/grenzkreise.md)).

**Kosten.** Am Bildschirm gleich, die Bildschirmtests bleiben unverändert grün. Ein kleiner
Lauf: rund 4.800 Zeichen verteilen, keine neue Klasse, keine neue Vorlage. Bleibt es, wächst
`zeichnen.js` mit jeder Komponente (Leisten, Grenzen, *Protokoll*) gegen 8.000 Zeichen, und
im Ordner sieht der Stakeholder keine Komponente.

**Gegenvorschlag.** Nach O5, Verhalten unverändert:
- `komponenten/kopfzeile.js`, `armeeKarte.js` (mit `einheitenKarte`), `sperrmeldung.js`,
  `knopfGruppe.js` (mit `knopf`), `karte.js` (mit `modellKreis`, Zone); das gemeinsame
  Klonen (`ausVorlage`, `ausSvgVorlage`, `mitSpieler`) in `komponenten/vorlage.js`.
- `zeichnen.js` behält nur `zeichnen(spielstand, gründe, knöpfe)` und `spalte`: Es setzt die
  Komponenten zur Seite zusammen. Komponenten importieren nur Komponenten.
- Gern im selben Lauf wie Item 4, vor `grenze.js`, dann folgt es gleich dem Muster.

**Stellungnahme.** Angenommen und umgesetzt nach dem Gegenvorschlag, Verhalten unverändert:
[vorlage.js](../../technik/frontend/komponenten/vorlage.js),
[kopfzeile.js](../../technik/frontend/komponenten/kopfzeile.js),
[armeeKarte.js](../../technik/frontend/komponenten/armeeKarte.js),
[sperrmeldung.js](../../technik/frontend/komponenten/sperrmeldung.js),
[knopfGruppe.js](../../technik/frontend/komponenten/knopfGruppe.js),
[karte.js](../../technik/frontend/komponenten/karte.js); [zeichnen.js](../../technik/frontend/zeichnen.js)
behält `zeichnen` und `spalte`. eslint über `technik/frontend` grün. Die Tests in
`technik/tests` haben dieselben Befunde wie zuvor: nur die Tests zu noch offenen Items
(Leisten, Übergehen, Anhalten) und `testQue10_1` (fehlendes `protokoll` im Spielstand) sind rot;
alle Bildschirmtests zur Karte, Armeeliste und Kopfzeile grün.
