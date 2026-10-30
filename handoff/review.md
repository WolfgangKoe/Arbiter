# Review · Zyklus 9

Start der App: `.venv/bin/arbiter` aus der Wurzel ([Web, W5](../technik/architektur/web.md#aufbau)),
dann `http://127.0.0.1:8040/` im Browser öffnen.

## Am Bildschirm prüfen
Mit Maus oder Finger stellt ihr beide Armeen auf, wählt den ersten Zug, geht durch die Phasen
jeder *Schlachtrunde* und zieht in der *Bewegungsphase* eure *Einheiten*, einzeln oder als
Ganzes, normal oder mit *Vorrücken*.
1. Start: Arbiter nennt `http://127.0.0.1:8040/`.
2. Aufstellen, „Erster Zug“ bei Spieler 1, „Phase beenden“: „Schlachtrunde 1 ·
   Bewegungsphase“ wie bisher.
3. Einen Boy 5″ quer über die Boyz ziehen: Er springt zurück, Arbiter nennt ‚über eine Base‘
   und bietet „gemeinsam übergehen“ an. Klick darauf: Der Boy steht, wo du losgelassen hast;
   das *Protokoll* in der unteren *Leiste* zeigt „Boyz · Spieler 1 · über eine Base“.
4. Einen Boy anklicken: Alle Boyz sind *ausgewählt*. Noch ein Klick auf ihn: Nur er ist
   *Ebene* und zieht allein. Noch ein Klick: wieder die ganze *Einheit*. Ein Klick auf die
   leere *Karte*: keine *Auswahl* mehr.
5. Die Boyz wieder anklicken: Ein heller Bereich um sie zeigt, wie weit sie ziehen, um jede
   gegnerische *Einheit* ein Bereich für ihre *Nahkampfreichweite*.
6. „Vorrücken“: sechs Kreise +1″ bis +6″ um die Boyz. Klick in den Ring „+3“: Nur er bleibt.
7. Die Boyz weit ziehen: Sie halten an, sobald ein *Modell* *Bewegungsweite* plus 3″ von
   seiner *Stelle* zu Beginn der Phase entfernt ist (der Boy aus Schritt 3 zuerst).
8. „Vorrücken zurücknehmen“: Die Boyz stehen wieder, wo die Phase begann, ohne Wurf.

Am laufenden Arbiter mit der Maus gesehen: 2 bis 8 in Folge; die Aufstellung habe ich dafür
vorbereitet statt geklickt. Nur Tests zeigen: Anhalten an der *Spielfeldkante* und 1″ vor
einer gegnerischen *Base* ([anhaltenVorDerGrenzeTest](../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py)),
*Modelle* des Gegners lassen sich nicht ziehen ([fremdeModelleTest](../technik/tests/akzeptanz/phasen/bewegung/fremdeModelleTest.py)),
Klick auf eine *aufgestellte* *Einheit* beim Aufstellen ([aufgestellteEinheitAuswaehlenTest](../technik/tests/akzeptanz/phasen/aufstellen/aufgestellteEinheitAuswaehlenTest.py)),
*Grenzkreise* nach erneuter *Auswahl* ([grenzkreiseNachErneuterAuswahlTest](../technik/tests/akzeptanz/phasen/bewegung/grenzkreiseNachErneuterAuswahlTest.py)).
Ziehst du den Warboss nach links zur Kante, springt er zurück: Die Boyz stehen im Weg,
‚über eine Base‘.

## DoD
1. **Erfüllt.** Alle Tests in `technik/tests` grün, Abdeckung über 95 % (Prüfung `abdeckung`).
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 937 grün; SonarLint ohne Fund. Die
   Meldung S1172 am Parameter `vorrückwurf`, die der Implementierer in der IDE sah, gibt es
   auf ca2bda8 nicht: Dieselbe SonarLint-Version meldet in einer Kopie einen wirklich
   unbenutzten Parameter derselben Funktion, `vorrückwurf` nicht. Wohl ein veralteter Stand
   im Editor.
3. **Erfüllt.** Alle vier Items gelöscht; die Kriterien beschreiben das Gebaute.
4. **Erfüllt.** Der Fachkritiker hat alle vier Items abgenommen.

Oberfläche: **Nicht erfüllt.** Bildschirmtests grün, aber acht Mockups des Gebauten liegen
noch da (Anliegen 8760, an UX, acht Dateien löschen).
Mutation: offen. Mein Lauf brach nach 50 Minuten am Zeitlimit ab, ohne Ergebnis; die fertigen
Module stehen im Merkzettel, ein neuer Lauf setzt dort fort. Das Ergebnis trägt der
Koordinator nach.

## Code
`/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe seit „Freigabe Plan 9“:
nichts hält auf. Kein `noqa`, kein TODO im Produkt. Warten auf Technikphase 10: Die Suche
nach der *Einheit* eines *Modells* steht dreimal da, ein Test zu zwei *Einheiten*, von denen
nur eine *vorgerückt* ist, fehlt (Anliegen 8740); zwei Tests zur *Auswahl* prüfen zu wenig
(Anliegen 8720).

## Empfehlung
Gib Review 9 frei, sobald UX die Mockups gelöscht hat (8760) und die Mutation die Schwelle
hält: Der Klickpfad zeigt, was Plan 9 versprochen hat, Schritte 1 bis 5 des Happy Path.
Die übrigen Anliegen warten auf spätere Phasen ([Moderation](moderation.md)).

## Rundgang Prüfcode
Seit „Freigabe Review 8“ 95 Dateien in [prozess/pruefungen](../prozess/pruefungen),
`.claude/settings.json` und `pyproject.toml` geändert, rund 1.240 Zeilen neu, 690 fort. Den
Rundgang durch sie trage ich in einem eigenen Lauf nach; bis dahin ist dieser Abschnitt offen.

## Nächstes Vorgehen
- **Produktziel:** Etappe 1 von 10 ist erreicht, Etappe 2 läuft. Am meisten fehlt die Partie
  nach der *Bewegungsphase*: Schießen, Angreifen, Nahkampf, Moral.
- **Etappenziel:** Zu [Etappe 2](../domaene/etappen/02-bewegen.md) fehlt, was Plan 9 unter
  „Danach“ nennt: Zurücksetzen, Anhalten übergehen, Ork-Psioniker und Canoptek-Spinne,
  Loslassen neben der *Karte*, ruhige *Karte*, „Phase beenden“ nur im Zug; der Stand nennt
  57 von 63 Kriterien der Etappe belegt. Ich schätze zwei Zyklen.
- **Zyklusziel:** Plan 10: Eine gezogene *Einheit* setzt ihr zurück, Arbiter zeigt, welche
  schon gezogen hat; ein Anhalten übergeht ihr *gemeinsam*; „Phase beenden“ gibt es nur für
  den *Spieler* am Zug. Noch nicht: Ork-Psioniker und Canoptek-Spinne. Vorher: Anliegen 8740,
  8720 und 8620 (Schnittstelle des Ziehens).

## Fortschritt
- [ ] Anforderungsautor: Happy Paths zum Zyklusziel
- [ ] UX: Mockups, bei einer Oberfläche
- [ ] Fachkritiker: Kritik an Anforderungen und Mockups
- [ ] Planer: Plan geschrieben
- [ ] Fachkritiker: Kritik am Plan
- [ ] Architekt: Kritik am Plan
- [ ] Stakeholder: Freigabe Plan 10

## Freigabe
Freigabe:
Kommentar:
