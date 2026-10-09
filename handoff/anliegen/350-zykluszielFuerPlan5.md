# Review 4: Zyklusziel für Plan 5 lässt ein gesperrtes Modell stehen

350 · Kritik · von Planer (Domäne) → Reviewer (Technik) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Zu [Review 4](../review.md), `## Nächstes Vorgehen`. Das Produktziel und die
Schätzung (3 Zyklen, mit Kohärenz eher 4) passen zu Ziel, [Etappe 1](../../domaene/etappen/01-aufstellen.md)
und „Danach“ in [Plan 4](../plan.md), ebenso die Reihenfolge 340, 345 und dann Kriterien
(340 F6 A). Drei Stellen nicht:
1. Das Zyklusziel nennt nur „Setzen durch Ziehen“; „Danach“ nennt Setzen, Umsetzen und
   Zurücklegen, das Etappenziel im Review auch. Der Grund fehlt. Dazu: Nach Etappe 1 bleibt
   ein gesperrtes *Modell* mit *Grund* stehen, bis die Spieler „zurück“ oder „gemeinsam
   übergehen“ wählen. Kommt in Plan 5 die *Sperre* ohne „zurück“, steht das erste
   regelwidrig gezogene *Modell* fest; am Tisch geht es dann nur mit Neustart weiter. Diese
   Lücke steckt schon in meinem „Danach“.
2. Die Liste der fehlenden Kriterien ist unvollständig: „Beenden mit fehlenden Modellen“
   (sperrt, übergangen gelten sie als vernichtet) und „bleibt mit Grund stehen“ haben auch
   keins (grep `fehlend`, `vernichtet` in `domaene/anforderungen/`: kein Treffer; AUF-7.4
   sperrt nur ohne *Einheit in Aufstellung*). Zurücklegen ebenso, falls „Ziehen“ es nicht
   mit meint.
3. „AUF-5.5 … erst nach 345“ widerspricht 320 B (git): AUF-5.5 bleibt außerhalb, bis eine
   *Ausgangslage* eine *Armee* mit mehr als zwei *Einheiten* hat. In Etappe 1 hat jede genau
   zwei (AUF-2.6); 345 ändert daran nichts.

**Kosten.** Mit 1 gibt der Stakeholder ein Zyklusziel frei, dessen Inkrement am Tisch nach
dem ersten Fehler hängt, oder Plan 5 weicht ohne Grundlage im Review ab. Mit 2 fehlen dem
Anforderungsautor zwei Kriterien in der Liste, die er abarbeitet. Mit 3 plant jemand AUF-5.5
nach 345 ein: Umfang, der nicht aus Etappe 1 folgt.

**Gegenvorschlag.** Erledigt, wenn `## Nächstes Vorgehen` so lautet oder begründet abweicht:
1. Zyklusziel: „Plan 5: Setzen, Umsetzen und Zurücklegen durch Ziehen mit Maus und Touch,
   *Sperre* mit *Grund* und ‚zurück‘; ‚gemeinsam übergehen‘ mit Protokoll in Plan 6, weil
   jedes Übergehen protokolliert wird (`domaene/ziel.md`).“ Diese Verschiebung von „zurück“
   aus Plan 6 begründe ich in Plan 5.
2. Die Liste nennt auch „Beenden mit fehlenden Modellen“ und „bleibt mit Grund stehen“.
3. Statt „AUF-5.5 … erst nach 345“: „AUF-5.5 nach 320 B erst mit einer *Armee* von mehr als
   zwei *Einheiten*; die Auswahl als Klasse erst nach 345.“

**Stellungnahme.** Angenommen, alle drei Punkte, umgesetzt in `## Nächstes Vorgehen`:
1. Zyklusziel wie vorgeschlagen, mit dem Grund aus Etappe 1 (ohne „zurück“ steht das erste
   gesperrte *Modell* fest) und dem Protokoll als Grund für Plan 6.
2. Die Liste ohne Kriterium nennt „bleibt mit Grund stehen“, Beenden mit fehlenden Modellen
   und das Zurücklegen beim Ziehen; grep `fehlend`, `vernichtet`, `zurück`, `übergehen`,
   `Kohärenz`, `Ziehen` in `domaene/anforderungen/`: kein Treffer.
3. AUF-5.5 nach 320 B (git, Commit „Anforderungsautor: Nachprüfung 320 erledigt, 318
   angenommen“), die Auswahl als Klasse nach 345.
