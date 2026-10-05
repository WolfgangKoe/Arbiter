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
  [268](anliegen/268-seiteErzeugtKeineElemente.md),
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

## Freigabe
Freigabe: ja
Kommentar: Wir haben sehr viele Anliegen. Wäre es möglich einige davon parallel abzuarbeiten? Wenn mehrere Anliegen an dieselbe Rolle adressiert sind, bedeutet das nicht zwangsläufig, dass sie nur einmal aktiv sein muss. Parallelität wird nur durch Abhängigkeit zwischen den Anliegen infrage gestellt. 
Stellungnahme: Geht, braucht eine Änderung am Ablauf: [279](anliegen/279-gleicheRolleParallel.md). Nach 253 Punkt 1 laufen 240, 262, 265, 267, 268, 270 gleichzeitig; der Rest bleibt eine Kette.
