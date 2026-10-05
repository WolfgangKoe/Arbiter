# Review · Zyklus 3

Inkrement: Änderungen seit `Freigabe Plan 3` (`d592f7b`) unter `technik/`, Stand `9977e0e`.
Items aus [Plan 3](plan.md): *Karte im Browser* (QUE-2), *Anzeige der Aufstellung* (AUF-4).

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 200 grün. Abdeckung `technik/arbiter`
   99 % Zeilen, 100 % Zweige; unerreicht nur `__main__.py` 13–15 (Strg+C), von Hand
   nachgestellt (unter Code). `prozess/pruefungen` 98,6 % und 97,2 %.
2. **Erfüllt, mit Hinweisen.** `python3 -m pytest prozess/pruefungen` auf `9977e0e`: 749 grün; eslint und
   stylelint ohne Fund. SonarLint auf `2635eb8`: keine Funde. Zwei Ausnahmen gelten für
   `web/` (Anliegen 261,
   [270](anliegen/270-csrfAusnahmeOhneAusloeser.md)). Nur Einheitstests erreichen
   `aufstellen.py` 48, 50, 91, 105 und `katalog/ausgangslage.py` 21, 51, 53, 56: alles
   Vorbedingungen (`ValueError`). Glossar → Code: *Name*, *Ablage*, *an der Reihe*,
   *Einheit in Aufstellung*, *Karte* stehen wörtlich im Code.
3. **Erfüllt.** Der Planer hat beide Items aus `domaene/items/` gelöscht (uncommittet).
4. **Erfüllt.** Der Fachkritiker hat QUE-2 und AUF-4 ohne Befund abgenommen.

Oberfläche: Bildschirmtests grün; `komponenten.css` gleicht `vorschlag.css`. **Nicht erfüllt:**
„Mockup gelöscht“. Die Mockups bleiben, bis `komponenten.html` steht
([262](anliegen/262-komponentenseiteOhnePruefung.md)).

## Code
Nachgeprüft: `python3 -m arbiter` nennt die Adresse und liefert die Ausgangslage; SIGINT
beendet ihn mit Exit 0 und leerem stderr (Anliegen 266 erledigt). Die Fläche der Zone kommt
nur aus `Ausgangslage.grenzenDerZone`; `seite.js` setzt kein festes `y` mehr und erzeugt kein
Element mehr, es klont die Vorlagen in `index.html`. `web/` liest
nur Properties, wandelt `Fraction` erst für die Antwort in `float` und vergibt „Spieler 1“
und „Spieler 2“ aus der Reihenfolge (W2). Die Domäne kennt Flask nicht.
`bildschirm.py` steht im Pfad des Testautors, hat aber eine Zeile vom Implementierer: Der
Import steht jetzt oben (248 Punkt 7). Die Änderung ist richtig, liegt aber außerhalb seiner
Schreibpfade. Für Bash wirkt die Grenze nur als Text
([215](anliegen/215-bashSandboxAlsVersuch.md)).

## Offene Anliegen zur Technik
- Regelumsetzer: [262](anliegen/262-komponentenseiteOhnePruefung.md),
  [268](anliegen/268-seiteErzeugtKeineElemente.md) ESLint-Verbot für erzeugte Elemente,
  [265](anliegen/265-ausgeloestePruefungenZuWeb.md) Prüfungen zu W1, W2, D3,
  [267](anliegen/267-roteTestsNurAusDerSchlusszeile.md) Zahl der roten Tests, 270 CSRF-Ausnahme ohne Auslöser.
- Implementierer prüft nach: 261.
- Testautor: [269](anliegen/269-auf4NimmtGrenzenDerZone.md) Grenzen der Zone in AUF-4.6,
  [259](anliegen/259-handgriffeImportierenStattFixtures.md),
  [260](anliegen/260-auf4WaehlenUndAlleBenennen.md).

## Empfehlung
Freigeben: DoD 1 bis 4 sind erfüllt. Keines der offenen Anliegen ändert Verhalten. Von der
DoD der Oberfläche fehlt nur das Löschen der Mockups; es folgt nach 262.

## Nächstes Vorgehen
- **Produktziel:** Erreicht ist noch keine der 7 Etappen. Am meisten fehlt die erste Handlung
  am Bildschirm: Arbiter zeigt heute nur an
  ([Etappe 1](../domaene/etappen/01-aufstellen.md)).
- **Etappenziel:** Es fehlen die vier Punkte aus „Danach“ in Plan 3: Wählen, Ziehen, Zurück
  mit Übergehen und Protokoll, Beenden. Wenn ein Punkt je Zyklus fertig wird, sind das 4
  Zyklen. Nur für Wählen kommen Speicher und Vertrag neu hinzu (`speicher.md`, Neuland).
- **Zyklusziel:** Plan 4 soll Wählen per Klick (Gewinner, Zone, Einheit) mit Speicher
  bringen. Vorher muss 262 weg, denn das nächste Mockup baut auf Vorlagen und der
  Komponentenseite auf. Dazu 265 D3: Ab der ersten Handlung über HTTP ändert `web/` den
  Zustand. Für die Technikphase von Plan 4 gilt: Vertrag in `web.md` vor dem Testautor
  (Ablauf, Technikphase 1) und Wegwerf-Versuch zum Wiederholen der Handlungen.

## Freigabe
Freigabe: offen
Kommentar: .
