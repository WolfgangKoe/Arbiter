# Vertrag: Schlacht

Die *Schlacht* nach der *Aufstellung* (QUE-9, QUE-10); was alle Phasen teilen:
[Querschnitt](querschnitt.md), die *Bewegungsphase*: [Bewegung](bewegung.md).

## Tür
- **V11** Die Tür der Domäne nach der *Aufstellung* ist `Schlacht(aufstellung)` in
  `arbiter/domaene/querschnitt/schlachtrunden.py`, mit `Phase` (Wert: Name aus dem Glossar,
  `Phase.kommandophase.value == "Kommandophase"`, wie `Grund`). Sie übernimmt beim Bau die
  *Stellen* der beendeten *Aufstellung* (AUF-1.7); danach gehören sie ihr, gelesen mit
  `schlacht.stelle(modell)`. Die *Aufstellung* ändert sich nicht mehr; Zonen und Ausgangslage
  liest `web/` weiter an ihr (W2). Abfragen: `ausgangslage` (wie `Aufstellung`), `ersterZug`, `amZug`,
  `schlachtrunde`, `phase`, `beendet`, `inKohärenz(einheit)` (QUE-4), dazu die der *Auswahl* wie `Aufstellung` (V3). Die Regeln der *Bewegungsphase*
  liegen in `phasen/bewegung/` ([Grundschnitt](../domaene.md)); `Schlacht` gibt ihnen Ziehen
  und Beenden weiter, außerhalb der *Bewegungsphase* ändert Loslassen nichts, ohne `Sperre`
  (QUE-10.5).
- `web/` hält die *Aufstellung* und, sobald sie beendet ist, genau eine `Schlacht` aus ihr;
  `anwendungFür(aufstellung, schlacht=None)`, `serverStarten(aufstellung, port=0, *,
  schlacht=None)`. Fehlt `schlacht` bei beendeter *Aufstellung*, baut `web/` sie beim ersten
  Bedarf. Danach gehen V5, V10 und V14 an die `Schlacht`, nicht mehr an die
  *Aufstellung*; V9: [Bewegung](bewegung.md#auswahl). Vor dem Ende der *Aufstellung*: V12 und V13 404. Warum in `web/`: Es steckt
  nur zusammen wie `__main__.py`; mit dem Umbau ([Anwendung](../anwendung.md)) zieht es in
  den Dienst.

## Spielstand
Schlüssel `schlacht` (V1), nur bei beendeter *Aufstellung*, sonst fehlt er; so gelten die
Beispiele der *Aufstellung* unverändert:
`{"ersterZug": <Spieler>|null, "amZug": <Spieler>|null, "schlachtrunde": <n>, "phase":
<Phase.value>, "beendet": <bool>}`, Spieler als `nummer` nach W4. `einheitInAufstellung` ist `null`,
jede `armeeliste` leer (AUF-1.7), `anDerReihe` überall `false`. Beispiel
[schlacht.json](schlacht.json), nur `schlacht` und `spieler`: Stand nach
`PUT /api/spieler/1/ersterZug` und `PUT /api/phaseBeenden` mit
`{"schlachtrunde": 1, "spieler": 1, "phase": "Kommandophase"}`.

## Handlungen
Am Bildschirm | Anfrage (V5) | `Schlacht`
---|---|---
„Erster Zug“ in einer *Armeeliste* (QUE-9.2) | `PUT /api/spieler/<s>/ersterZug` | `ersterZugWählen`
„Phase beenden“ (QUE-10.2 bis 10.4) | `PUT /api/phaseBeenden`, Körper wie oben | `phaseBeenden`

- **V12** Hat schon ein *Spieler* den *ersten Zug*, ändert `ersterZugWählen` nichts, ohne
  `Sperre` (V5: doppelt gesendet ändert nichts). Unbekannter *Spieler*: 404.
- **V13** Der Körper nennt die *Phase*, die die Seite beenden will: `schlachtrunde`,
  `spieler` (*am Zug*) und `phase` aus ihrem letzten Spielstand. Ist es nicht die laufende,
  ändert `web/` nichts: 200 mit dem Spielstand. Warum: Ein doppelter Klick oder eine zweite
  Seite (QUE-3.2) übersprängen sonst eine *Phase* (V5). Fehlt eine Zahl oder ist `phase`
  kein Wert von `Phase`: 400.

## Seite
- Kopfzeile (QUE-10.1, Mockup que-10): Die `kopfzeileSpieler` des *Spielers* `amZug` trägt
  `amZug` und `kopfzeileAmZug` „Schlachtrunde <n> · <phase>“. `beendet` (QUE-10.4, Mockup
  que-10-ende): `kopfzeileSchlachtBeendet` „Schlacht beendet“ im `kopfzeileTitel`.
- Knöpfe (V7): „Erster Zug“ in der `knopfGruppe` jeder `armeeKarte`, wenn `ersterZug`
  `null` ist (QUE-9.1, Mockup que-9); „Phase beenden“ in der `knopfGruppe` der Mitte, wenn
  `amZug` nicht `null` ist.
- Zug (V8, V10) und Klick: [Bewegung](bewegung.md), in jeder *Phase* gleich; außerhalb der
  *Bewegungsphase* nennt V10 kein *Modell* (QUE-10.5), keines bewegt sich.

Prüft wie im Querschnitt: `schlacht` und `spieler` nach den Anfragen des Beispiels gleich
`schlacht.json`; V13 mit dem Körper einer schon beendeten *Phase*: Spielstand unverändert.
