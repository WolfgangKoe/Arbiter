# Review · Zyklus 3

Inkrement: Änderungen seit `Freigabe Plan 3` (`d592f7b`) unter `technik/`, Stand `18d55b8`
(Kritik `196e31c`).
Items aus [Plan 3](plan.md): *Karte im Browser* (QUE-2), *Anzeige der Aufstellung* (AUF-4).

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 200 grün. Abdeckung `technik/arbiter`
   99 % Zeilen, 100 % Zweige; unerreicht nur `__main__.py` 13–15 (Strg+C), von Hand
   nachgestellt (unter Code). `prozess/pruefungen` 98,6 % und 97,2 %.
2. **Erfüllt, mit Hinweisen.** `python3 -m pytest prozess/pruefungen` auf `779e39a`: 757
   grün; eslint und stylelint ohne Fund (Frontend unverändert). SonarLint auf
   `2635eb8`: keine Funde. Zwei Ausnahmen gelten für `web/` (261,
   Anliegen 270). Nur Einheitstests erreichen
   `aufstellen.py` 48, 50, 91, 105 und `katalog/ausgangslage.py` 21, 51, 53, 56: alles
   Vorbedingungen (`ValueError`). Glossar → Code: *Name*, *Ablage*, *an der Reihe*,
   *Einheit in Aufstellung*, *Karte* stehen wörtlich im Code.
3. **Erfüllt.** Der Planer hat beide Items aus `domaene/items/` gelöscht (`bb18997`).
4. **Erfüllt.** Der Fachkritiker hat QUE-2 und AUF-4 ohne Befund abgenommen.

Oberfläche: Bildschirmtests grün; `komponenten.css` gleicht `vorschlag.css`. **Nicht erfüllt:**
„Mockup gelöscht“. Die Mockups bleiben, bis `komponenten.html` steht
(Anliegen 262).

## Code
Nachgeprüft: `python3 -m arbiter` nennt die Adresse und liefert die Ausgangslage; SIGINT
beendet ihn mit Exit 0 und leerem stderr. Die Fläche der Zone kommt nur aus
`Ausgangslage.grenzenDerZone`; `seite.js` setzt kein festes `y` und erzeugt kein Element,
es klont die Vorlagen in `index.html`. `web/` liest nur Properties, wandelt `Fraction` erst
für die Antwort in `float` und vergibt „Spieler 1“ und „Spieler 2“ aus der Reihenfolge (W2).
Die Domäne kennt Flask nicht. `bildschirm.py` (Pfad des Testautors) hat eine richtige Zeile
vom Implementierer außerhalb seiner Schreibpfade (248 Punkt 7); für Bash wirkt die Grenze
nur als Text ([215](anliegen/215-bashSandboxAlsVersuch.md)).

## Offene Anliegen zur Technik
- Regelumsetzer: Anliegen 262,
  Anliegen 268,
  Anliegen 265,
  Anliegen 267, 270.

## Empfehlung
Freigeben: DoD 1 bis 4 sind erfüllt. Kein offenes Anliegen ändert Verhalten.

## Nächstes Vorgehen
- **Produktziel:** Noch keine der 7 Etappen erreicht. Am meisten fehlt die erste Handlung
  am Bildschirm: Arbiter zeigt heute nur an
  ([Etappe 1](../domaene/etappen/01-aufstellen.md)).
- **Etappenziel:** Es fehlen die vier Punkte aus „Danach“ in Plan 3: Wählen, Ziehen, Zurück
  mit Übergehen und Protokoll, Beenden. Für die letzten drei fehlen Kriterien und Glossar
  (grep nach Kohärenz, Protokoll, übergeh, zurück, vernichtet, ziehen in
  `domaene/anforderungen/`: kein Treffer); je Zyklus schreibt sie zuerst die Domänenphase.
  Kohärenz ist eine eigene Messregel mit zwei Fällen (`core_rules.txt:434`). Schätzung: 4
  Zyklen, mit Kohärenz eher 5. Nur für Wählen kommen Speicher
  und Vertrag neu hinzu (`speicher.md`, Neuland).
- **Zyklusziel:** Plan 4 soll Wählen per Klick (Gewinner, Zone, Einheit) mit Speicher
  bringen. Die Domäne hat dafür nur AUF-1.1, 1.2, 1.5, 1.6; die Domänenphase schreibt
  zuerst Kriterien für die Handlung am Bildschirm und die Anzeige der *Sperre* ‚nicht
  wählbar‘. Vorher muss 262 weg, das nächste Mockup baut
  auf der Komponentenseite auf. Dazu 265 D3: Ab der ersten Handlung über HTTP ändert `web/` den
  Zustand. Technikphase: Vertrag in `web.md` vor dem Testautor (Ablauf, Technikphase 1),
  Wegwerf-Versuch zum Wiederholen der Handlungen.

## Rückbau der Prüfskripte: Codequalität des Produkts
Empfehlung je Kandidat in `prozess/pruefungen/`; alle sieben laufen heute grün (Lauf am
Stand `417f30b`: 121 Tests, SonarLint ohne Funde).

- **`formregeln/kommentare.py` behalten:** einzige Prüfung von
  [es.md](../prozess/praemissen/es.md) 8 im Python-Produkt (ruff `ERA` findet nur
  auskommentierten Code), 67 Zeilen ohne fremde Abhängigkeit.
- **`formregeln/komplexitaetTest.py` behalten, gekürzt:** Prüfung ist nur
  `testDerCodeLiegtUnterDerKomplexitätsschwelle` (complexipy, Schwelle 15); die vier
  Grenzproben testen das Werkzeug, nicht unseren Code, und können weg.
- **`formregeln/abdeckung.py` behalten, gekürzt:** 95 % für `technik/arbiter` und vulture
  (toter Code) prüfen das Produkt; die Messung der Prüfskripte (`__main__`, Hook
  `abdeckungPruefskripte`) fällt mit dem Rückbau.
- **`formregeln/sonarlint.py` behalten:** dein Maßstab („mindestens so streng wie SonarLint“,
  Anliegen 150), findet, was ruff nicht findet; Kosten: rund 37 s, Java und die lokale
  VS-Code-Erweiterung, deshalb nur als eigener Aufruf, nicht im Lauf der Prüfungen.
- **`frontendregeln/frontend.py` behalten:** einzige Prüfung von JavaScript und CSS
  (SonarLint prüft nur Python), 38 Zeilen, rund 1 s.
- **`frontendregeln/eslintKommentare.mjs` behalten:** es.md 8 für JavaScript, Gegenstück zu
  `kommentare.py`; `eslint.config.mjs` bindet die Regel ein.
- **`frontendregeln/stylelintFarben.mjs` behalten:** setzt „Farbwerte nur in `:root`“ aus
  `vorschlag.css` durch, das stylelint selbst nicht kann; `.stylelintrc.json` bindet es ein.

Zwei Abhängigkeiten außerhalb der Liste:
1. ruff mit `PLR0912` (höchstens 12 Fälle) und dem übrigen Regelsatz läuft über das Repo nur in
   `testDasRepoIstRuffSauber` in `formregeln/konfigurationTest.py`: Diesen Test behalten,
   sonst fällt ruff ganz weg.
2. `abdeckung.py` importiert `standregeln.phasenfolge` (`aussetzung`): Fallen die
   Standregeln, wird ein roter Test in `technik/tests` ohne Phasenbezug übersprungen und die
   Zahl genannt. Sonst sperrt die Abdeckung jeden Commit der Technikphase, denn dort sind die
   Tests vor dem Code rot. Grün verlangt dann die Kette Anforderung → Akzeptanztest → grüner Code.

## Freigabe
Freigabe: ja
Kommentar: Wir haben sehr viele Anliegen. Wäre es möglich einige davon parallel abzuarbeiten? Wenn mehrere Anliegen an dieselbe Rolle adressiert sind, bedeutet das nicht zwangsläufig, dass sie nur einmal aktiv sein muss. Parallelität wird nur durch Abhängigkeit zwischen den Anliegen infrage gestellt. 
Stellungnahme: Geht, braucht eine Änderung am Ablauf: Anliegen 279. Nach 253 Punkt 1 laufen 240, 262, 265, 267, 268, 270 gleichzeitig; der Rest bleibt eine Kette.
