# Sprung-Versuch: Der Stakeholder probiert das alte Paket

133 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Gegenstand: 2c5d09a (Kritik am Code), Rest aus [127](127-sprungversuchKlickbereichUndLesbarkeit.md).

**Befund.**
1. In HEAD liegt weiter `prozess/pruefungen/sprung/arbiter-sprung.vsix`, Version 0.0.2, mit
   dem faulen `testMuster` (`git show HEAD:…` geöffnet, `extension/suche.js`). Löschung und
   `.gitignore`-Zeile liegen nur im Arbeitsbaum; die Entscheidung liegt beim Stakeholder. Die
   Rückmeldung in [124](124-sprungPerKlickErproben.md) zeigt: Er hat genau dieses Paket
   installiert. Die neue Installationszeile steht nur in 127, die Anleitung in 124 nennt die
   alte.
2. Der Paketname wechselte von `arbiter-sprung` zu `arbitersprung`. VS Code führt beide als
   verschiedene Erweiterungen (`arbiter.arbiter-sprung`, `arbiter.arbitersprung`); wer die
   neue installiert, behält die alte, und zwei DefinitionProvider antworten auf denselben
   Klick.
3. `suche.js`: `const fs` hat zwei Zeichen (wir.md 5); der `// Warum:`-Kommentar begründet mit
   „beim Stakeholder“ (wir.md 8: kein Prozessverweis). `kommentare.py` und `benennung.py`
   prüfen nur Python; wir.md gilt auch fürs Frontend.

**Kosten.** Zu 1 und 2: Der Stakeholder prüft den Klick mit dem Bereich, der nur
`testAuf1_4` deckt, oder mit doppelten Zielen; 83 hält einen Befund fest, den 127.1 vermeiden
sollte. Zu 3: klein, solange der Versuch Wegwerf ist; ab `web/` bleibt jedes JS ungeprüft.

**Gegenvorschlag.**
1. und 2. Die Anleitung dorthin, wo der Stakeholder liest (deine Stellungnahme in 124
   ergänzen, sobald der Koordinator den Arbeitsbaum von 124 committet hat):
   `code --uninstall-extension arbiter.arbiter-sprung`, dann
   `python3 prozess/pruefungen/sprung/baue.py && code --install-extension
   prozess/pruefungen/sprung/arbitersprung.vsix`, dann „Developer: Reload Window“.
3. `dateisystem` statt `fs`; Kommentar ohne Stakeholder (etwa „Warum: ohne Python und ohne
   Sprachserver“); die JS-Lücke in `prozess/regeln.md` als bekannte Lücke nennen, bis `web/`
   kommt (dann eslint, siehe Werkzeugliste in `ablauf.md`).

Erledigt, wenn die Anleitung mit Deinstallation in 124 steht und 3 umgesetzt ist.
