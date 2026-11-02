# Vertrag: Schlacht · Spielstand

Abschnitt der *Schlacht*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md).

Schlüssel `schlacht` (V1), nur bei beendeter *Aufstellung*, sonst fehlt er; so gelten die
Beispiele der *Aufstellung* unverändert:
`{"ersterZug": <Spieler>|null, "amZug": <Spieler>|null, "schlachtrunde": <n>, "phase":
<Phase.value>, "beendet": <bool>}`, Spieler als `nummer` nach W4. `einheitInAufstellung` ist
`null`, jede `armeeliste` leer (AUF-1.7), `anDerReihe` überall `false`. Beispiel
[schlacht.json](../schlacht.json), nur `schlacht` und `spieler`: Stand nach
`PUT /api/spieler/1/ersterZug` und `PUT /api/phaseBeenden` mit
`{"schlachtrunde": 1, "spieler": 1, "phase": "Kommandophase"}`. Dazu `protokoll` und
`gemeinsamÜbergehen` ([V18](uebergehen.md)).

Prüft wie im Querschnitt: nach den Anfragen des Beispiels `spieler` gleich `schlacht.json`, von
`schlacht` die Schlüssel, die ein Beispiel nennt; so bricht ein neuer Schlüssel (V21) kein
Beispiel (O).
