# Vertrag: Schlacht · Handlungen

Abschnitt der *Schlacht*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md).

Am Bildschirm | Anfrage (V5) | `Schlacht`
---|---|---
„Erster Zug“ in einer *Armeeliste* (QUE-9.2) | `PUT /api/spieler/<s>/ersterZug` | `ersterZugWählen`
„Phase beenden“ (QUE-10.2 bis 10.4) | `PUT /api/phaseBeenden`, Körper wie in [Spielstand](spielstand.md) | `phaseBeenden`

- **V12** Hat schon ein *Spieler* den *ersten Zug*, ändert `ersterZugWählen` nichts, ohne
  `Sperre` (V5: doppelt gesendet ändert nichts). Unbekannter *Spieler*: 404.
- **V13** Der Körper nennt die *Phase*, die die Seite beenden will: `schlachtrunde`,
  `spieler` (*am Zug*) und `phase` aus ihrem letzten Spielstand. Ist es nicht die laufende,
  ändert `web/` nichts: 200 mit dem Spielstand. Warum: Ein doppelter Klick oder eine zweite
  Seite (QUE-3.2) übersprängen sonst eine *Phase* (V5). Fehlt eine Zahl oder ist `phase`
  kein Wert von `Phase`: 400.

Prüft wie im Querschnitt: V13 mit dem Körper einer schon beendeten *Phase*: Spielstand
unverändert.
