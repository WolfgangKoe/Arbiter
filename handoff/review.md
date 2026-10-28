# Review · Zyklus 8

Start der App: `.venv/bin/arbiter` aus der Wurzel ([Web, W5](../technik/architektur/web.md#aufbau)),
dann `http://127.0.0.1:8040/` im Browser öffnen.

## Am Bildschirm prüfen
Mit Maus oder Finger stellt ihr beide Armeen auf, wählt den ersten Zug, geht durch die
Phasen jeder *Schlachtrunde* und zieht in der *Bewegungsphase* eure *Einheiten*.
1. Start: Arbiter nennt `http://127.0.0.1:8040/`.
2. Beide Armeen aufstellen wie bisher. Danach steht in beiden *Armeelisten* „Erster Zug“.
3. „Erster Zug“ bei Spieler 1: Die Kopfzeile zeigt „Schlachtrunde 1 · Kommandophase“, unter
   der *Karte* steht nur „Phase beenden“.
4. „Phase beenden“: „Schlachtrunde 1 · Bewegungsphase“.
5. Den Warboss 8″ weit ziehen: Er hält nach 5″ an, seiner *Bewegungsweite*, ohne *Grund*.
6. Einen Boy anklicken: Alle Boyz sind *ausgewählt*. Einen ziehen: Alle rücken um denselben
   Weg.
7. Einen Boy allein ziehen geht nur über einen Umweg: erst den Warboss anklicken, dann ist
   kein *Modell* der Boyz mehr *ausgewählt*. Ein Klick auf die leere *Karte* hebt die Auswahl
   nicht auf ([Anliegen 6240](anliegen/6240-abwaehlenInDerSchlacht.md)).
8. Einen Boy über einen anderen hinweg ziehen: Er springt zurück, Arbiter nennt ‚über eine Base‘.
9. Einen Boy weit weg aus der *Kohärenz* ziehen, „Phase beenden“: ‚keine Kohärenz‘, nichts
   zum Übergehen.
10. Phasen beenden bis zur Moralphase: Spieler 2 ist *am Zug*; nach der fünften
    *Schlachtrunde* endet die *Schlacht*.

Am laufenden Arbiter gesehen: 1 bis 8, auf Port 8091 (`--port`). 9 zeigt nur
[beendenTest](../technik/tests/akzeptanz/phasen/bewegung/beendenTest.py), 10 nur
[schlachtrundenTest](../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py).
Greifst du ein *Modell* am Rand, springt es nicht mehr mit der Mitte unter den Zeiger
(AUF-8.7, [ziehenTest](../technik/tests/akzeptanz/phasen/aufstellen/ziehenTest.py)).

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 845 grün; Abdeckung über 95 %.
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 820 grün; SonarLint ohne Fund.
3. **Erfüllt.** Alle drei Items gelöscht; BEW-1 bis BEW-4 beschreiben das Gebaute.
4. **Erfüllt.** Der Fachkritiker hat alle drei Items abgenommen.

Oberfläche: **Erfüllt.** Bildschirmtests grün.
Mutation: **Nicht erfüllt.** 94 Mutanten der geänderten Domänenzeilen, 84 % gefangen,
Schwelle 95 %; 15 überleben, vor allem in der Bewegungsphase. Der Testautor fängt sie oder
begründet sie als gleichwertig ([Anliegen 6291](anliegen/6291-hindernisDodUeberDasInkrement.md)).

## Code
`/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe seit „Freigabe Plan 8“:
nichts hält auf. Zwei Nachbauten in der Messung und *Distanz* ohne Namen im Code warten auf
Technikphase 9 ([Anliegen 6290](anliegen/6290-reviewNachbauUndDistanz.md)).

## Empfehlung
Die DoD hält an der Mutation (Anliegen 6291): Gib Review 8 frei, sobald der Testautor sie
über 95 % gebracht hat; ich trage das Ergebnis dann hier ein. Am Bildschirm ändert sich
dadurch nichts. Den Umweg aus Schritt 7 klärt die
Domänenphase 9 mit dir (Anliegen 6240). Die übrigen offenen Anliegen warten auf spätere
Phasen ([Moderation](moderation.md)).

## Rundgang Prüfcode
Seit „Freigabe Review 7“ rund 930 Zeilen neu in [prozess/pruefungen](../prozess/pruefungen),
280 fort, dazu 10 Zeilen Hooks in `.claude/settings.json`: die Architekturkarte im Dashboard,
Hindernisse mit Nummernbereich, neue Fassung des Plans, Bash-Verbote.
1. Rundgang 1 aus Review 7 ist erledigt: `anliegenregeln/kopfUmschreiben.py` ist fort,
   `lesen/anliegenKopf.py` liest nur noch den Kopf als Felder.
2. Rundgang 3 aus Review 7 ist erledigt: `standregeln/hindernis.py` nimmt eine freie Nummer
   aus dem Bereich des Auftrags. Dafür hat `hindernisMelden` sechs Parameter und schaltet die
   Regel dagegen ab (`hindernis.py`, `# noqa: PLR0913`); ein Aufruf als ein Objekt genügte.
3. `rollenregeln/dashboardArchitektur.py` (166 Zeilen) und `architekturMessung.py` (99) sind
   der größte Zuwachs: Sie zeichnen die Architektur als Bild ins Dashboard. Ob du es nutzt,
   entscheidet, ob es bleibt.

## Nächstes Vorgehen
- **Produktziel:** Etappe 1 von 10 ist erreicht, Etappe 2 läuft. Am meisten fehlt die Partie
  nach der Bewegungsphase: Schießen, Angreifen, Nahkampf, Moral.
- **Etappenziel:** Zu [Etappe 2](../domaene/etappen/02-bewegen.md) fehlt, was Plan 8 unter
  „Noch nicht“ nennt: jede *Einheit* nur einmal ziehen, Advance, Zurücksetzen, über die Kante,
  *gemeinsam übergehen* mit *Protokoll*, Ork-Psioniker und Canoptek-Spinne, Loslassen neben
  der *Karte*; der Stand nennt 95 von 123 Kriterien belegt. Ich schätze zwei Zyklen.
- **Zyklusziel:** Plan 9: In der *Bewegungsphase* zieht jede *Einheit* nur einmal, mit Advance
  weiter nach eurem Würfelwurf, nicht über die Kante; eine *Sperre* übergeht ihr *gemeinsam*,
  das *Protokoll* hält es fest; ein Klick auf die leere *Karte* hebt die Auswahl auf (6240).
  Noch nicht: Zurücksetzen, Ork-Psioniker und Canoptek-Spinne. Vorher: Anliegen 6102
  (Ablage der Bewegung), 6241 (Tests zu QUE-1.3 und AUF-8.7 in der Bewegung) und 6290.

## Fortschritt
- [ ] Anforderungsautor: Happy Paths zum Zyklusziel
- [ ] UX: Mockups, bei einer Oberfläche
- [ ] Fachkritiker: Kritik an Anforderungen und Mockups
- [ ] Planer: Plan geschrieben
- [ ] Fachkritiker: Kritik am Plan
- [ ] Architekt: Kritik am Plan
- [ ] Stakeholder: Freigabe Plan 9

## Freigabe
Freigabe: offen
Kommentar: .
