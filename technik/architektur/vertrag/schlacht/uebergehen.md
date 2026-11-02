# Vertrag: Schlacht · Gemeinsam übergehen

Abschnitt der *Schlacht*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md).

Am Bildschirm | Anfrage (V5) | `Schlacht`
---|---|---
„gemeinsam übergehen“ (BEW-8.4) | `PUT /api/gemeinsamÜbergehen`, ohne Körper | `gemeinsamÜbergehen`

- **V18** Übergangen wird ein Anhalten, keine *Sperre* (BEW-8, QUE-5.1 erst in Etappe 7):
  - Angebot (BEW-8.3, 25.1): Hat V16 beim `modellLoslassen` nach BEW-3.1 oder 6.2 angehalten
    (deren Anteil ist der kleinste der drei und kleiner 1) und *setzt* es ohne *Sperre*, merkt
    sich die *Bewegungsphase* die gezogenen *Modelle* (die *Ebene* beim Loslassen), das
    gezogene und den Punkt des Loslassens. Abfrage `Schlacht.gemeinsamÜbergehenAngeboten`.
    Jede weitere Handlung ohne *Sperre* (die Tabellen der *Schlacht* und *Bewegungsphase*, V5)
    beendet das Angebot, ein Loslassen ersetzt es nach derselben Regel; Auswählen (V2, V14)
    und Abfragen beenden es nicht, eine *Sperre* auch nicht (D2). Warum gemerkt: Das Angebot
    hängt an den *Modellen*, die angehalten haben, nicht an der *Auswahl* danach (8261, 3);
    wiederholt (P2) entsteht es neu.
  - `gemeinsamÜbergehen()` ohne Angebot ändert nichts, ohne `Sperre` (wie `vorrücken`). Sonst
    rückt es die gemerkten *Modelle* um denselben Weg von der *Stelle* des gezogenen zum Punkt
    weiter, gekürzt nur nach BEW-6.1 (BEW-8.4 ohne BEW-17, das bringt Item anhaltenAufDemWeg),
    und prüft QUE-1 ohne QUE-1.3; jeder übrige *Grund* wirft `Sperre` wie V15, das Angebot
    bleibt. Ohne *Sperre* *setzt* es und trägt ins *Protokoll* ein (BEW-8.5): *Einheit* des
    gezogenen *Modells*, *Spieler* *am Zug*, ‚Bewegungsweite‘, wenn `anteilBisZurBewegungsweite`
    auf diesem Weg kleiner 1 ist, ‚Nahkampfreichweite‘, wenn `anteilBisZurNahkampfreichweite`
    es ist. Rechnen in `phasen/bewegung/uebergehenBeimZiehen.py`; `Protokoll`,
    `Eintrag(einheit, spieler, gründe)`: `querschnitt/uebergehen.py`, `Schlacht.protokoll`,
    der älteste Eintrag zuerst. Neu `Grund.bewegungsweite` „Bewegungsweite“ direkt vor
    `nahkampfreichweite`.
  - `modellLoslassen(modell, stelle)` trägt nie ein (QUE-5.6); der Parameter `übergehen`, der
    Körper `übergehen` und `Sperre.übergehbar` entfallen, eine 409 trägt nur `gründe` und
    `spielstand` (V6). So bietet keine *Sperre* *gemeinsam übergehen* an, auch ‚keine
    Kohärenz‘ nicht (QUE-5.5).
- Spielstand: `schlacht.gemeinsamÜbergehen` immer, `{"angeboten": <bool>}`. Beispiel
  [angehalten.json](../angehalten.json), nur `schlacht`: Stand von
  [schlacht.json](../schlacht.json), dann den Warboss
  (`/api/spieler/1/einheiten/2/modelle/1/stelle`) 10″ nach Osten loslassen; er hält nach
  5″ an. `schlacht.protokoll`, der neueste Eintrag zuerst (QUE-5.4), je Eintrag `spieler`,
  `einheit` (Kennungen nach V1), `name` wie in der *Armeeliste*, `gründe` in der Reihenfolge
  von `Grund`; beim Start leer (QUE-5.3). Beispiel [protokoll.json](../protokoll.json), nur
  `schlacht`: Stand von `angehalten.json`, dann `PUT /api/gemeinsamÜbergehen`, dann ebenso
  einen Boy (`…/einheiten/1/modelle/1`, ohne *Auswahl*) 10″ nach Osten und übergehen.
- Seite: Knopf „gemeinsam übergehen“ (V7) in der `knopfGruppe` der Mitte vor „Vorrücken“, wenn
  `angeboten` und keine `sperrmeldung` steht. Warum: Neben einer *Sperre* läse er sich als ihr
  Übergehen (QUE-5.5). Unten die *Leisten* nach [O4](../../frontend.md), je Eintrag ein
  `protokollEintrag spieler<n>` mit `protokollEinheit`, `protokollSpieler` („Spieler <n>“)
  und je *Grund* `protokollGrund`; in der *Aufstellung* leer.

Prüft wie im Querschnitt, am Dienst und am Bildschirm, `page.route` nur mit `protokoll.json`
(7321, 4; den Knopf zeigt schon der Test am echten Server): angehalten loslassen, 200, `angeboten`, *Stellen* wie V10 am selben
Punkt, *Protokoll* unverändert; `PUT /api/gemeinsamÜbergehen`: *Modelle* am Punkt, ein Eintrag
mehr mit den *Gründen* nach BEW-8.5, danach `angeboten` falsch, ein zweites `PUT` ändert
nichts; Auswählen dazwischen lässt das Angebot, eine 409 dazwischen den ganzen Stand. Die
Schlüssel nach den Anfragen der Beispiele gleich `angehalten.json` und `protokoll.json`.
