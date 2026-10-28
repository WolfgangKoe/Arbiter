# Review · Zyklus 8

Start der App: `.venv/bin/arbiter` aus der Wurzel ([Web, W5](../technik/architektur/web.md#aufbau)),
dann `http://127.0.0.1:8040/` im Browser öffnen.

## Am Bildschirm prüfen
Mit Maus oder Finger stellt ihr beide Armeen auf, wählt den ersten Zug, geht durch die
Phasen jeder *Schlachtrunde* und zieht in der *Bewegungsphase* eure *Einheiten*.
1. Start: Arbiter nennt `http://127.0.0.1:8040/`.
2. Beide Armeen aufstellen wie bisher. Danach steht in beiden *Armeelisten* „Erster Zug“.
3. „Erster Zug“ bei Spieler 1: Auf seiner Seite der Kopfzeile, links, steht
   „Schlachtrunde 1 · Kommandophase“, unter der *Karte* nur „Phase beenden“.
4. Den Warboss ziehen und loslassen: Er steht wieder, wo er war, ohne *Grund*. So ist es in
   jeder *Phase* außer der *Bewegungsphase*.
5. „Phase beenden“: „Schlachtrunde 1 · Bewegungsphase“.
6. Den Warboss 3″ ziehen, loslassen, dann noch 3″: Er hält 5″ von seinem Ausgangspunkt an,
   seiner *Bewegungsweite*, ohne *Grund*; die *Distanz* zählt von der *Stelle* zu Beginn der
   *Bewegungsphase*. 8″ auf einmal: ebenso.
7. Einen Boy anklicken: Alle Boyz sind *ausgewählt*. Einen ziehen: Alle rücken um denselben
   Weg.
8. Danach den Warboss noch einmal 2″ zurückziehen: Das geht, er steht, wo du ihn loslässt.
9. Einen einzelnen Boy *auswählen* geht in der *Schlacht* noch nicht: Ein Klick auf einen Boy
   wählt immer alle Boyz (Plan 8, Item 3). Ein *Modell* als *Ebene* auch in der *Schlacht*
   hast du für Domänenphase 9 gewählt
   ([Anliegen 5520](anliegen/5520-bewegungsphaseFuerSpaeter.md), F3 B). Einen Boy allein
   ziehen geht nur über einen Umweg: erst den Warboss anklicken, dann ist kein *Modell* der
   Boyz mehr *ausgewählt*; dann einen Boy greifen und ziehen, ohne ihn vorher anzuklicken.
   Ein Klick auf die leere *Karte* hebt die Auswahl nicht auf
   ([Anliegen 6240](anliegen/6240-abwaehlenInDerSchlacht.md)).
10. Wie in 9 einen Boy über einen anderen hinweg ziehen: Er springt zurück, Arbiter nennt
    ‚über eine Base‘.
11. Wie in 9 einen Boy weit weg aus der *Kohärenz* ziehen: Nur er rückt. „Phase beenden“:
    ‚keine Kohärenz‘, nichts zum Übergehen.
12. Phasen beenden bis zur Moralphase: Spieler 2 ist *am Zug*. Nach der fünften
    *Schlachtrunde* steht in der Kopfzeile „Schlacht beendet“, „Phase beenden“ ist fort.

Am laufenden Arbiter gesehen: 1 bis 12, 6 bis 11 in Folge mit der Maus.
Greifst du ein *Modell* am Rand, springt es nicht mehr mit der Mitte unter den Zeiger
(AUF-8.7, [ziehenTest](../technik/tests/akzeptanz/phasen/aufstellen/ziehenTest.py)).
Lässt du ein *Modell* in *Nahkampfreichweite* eines gegnerischen los, sperrt Arbiter schon
‚Nahkampfreichweite‘, obwohl Plan 8 sie unter „Noch nicht“ nennt; ein Test dazu fehlt noch
([Anliegen 6241](anliegen/6241-bewegungOhneTestZuQue1_3UndAuf8_7.md)).

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 845 grün; Abdeckung über 95 %.
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 820 grün; SonarLint ohne Fund.
3. **Erfüllt.** Alle drei Items gelöscht; BEW-1 bis BEW-4 beschreiben das Gebaute.
4. **Erfüllt.** Der Fachkritiker hat alle drei Items abgenommen.

Oberfläche: **Erfüllt.** Bildschirmtests grün.
Mutation: **Erfüllt.** 89 Mutanten der geänderten Domänenzeilen, 97 % gefangen, Schwelle
95 %; 5 sind gleichwertig begründet und zählen nicht. Zwei überleben, weil ihr Fall
ungeregelt ist ([Anliegen 6300](anliegen/6300-anklickenUndFremdesModellLoslassen.md)); die
Mutanten zur *Kohärenz* nach dem neuen Test aus Anliegen 6330: alle gefangen.

## Code
`/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe seit „Freigabe Plan 8“:
nichts hält auf. Zwei Nachbauten in der Messung und *Distanz* ohne Namen im Code warten auf
Technikphase 9 ([Anliegen 6290](anliegen/6290-reviewNachbauUndDistanz.md)).

## Empfehlung
Gib Review 8 frei: Die DoD ist erfüllt, und der Klickpfad zeigt, was Plan 8 versprochen hat.
Den Umweg aus Schritt 9 klärt die Domänenphase 9 mit dir (Anliegen 6240). Die übrigen
offenen Anliegen warten auf spätere Phasen ([Moderation](moderation.md)).

## Rundgang Prüfcode
Seit „Freigabe Review 7“ rund 960 Zeilen neu in [prozess/pruefungen](../prozess/pruefungen)
und `pyproject.toml`, 280 fort, dazu 10 Verbote in `.claude/settings.json`. Wo ich kein
wesentliches Problem nenne, sehe ich keines.
1. Rundgang 1 aus Review 7 ist erledigt: `anliegenregeln/kopfUmschreiben.py` ist fort,
   [lesen/anliegenKopf.py](../prozess/pruefungen/lesen/anliegenKopf.py) liest nur noch den Kopf
   als Felder.
2. Rundgang 3 aus Review 7 ist erledigt:
   [standregeln/hindernis.py](../prozess/pruefungen/standregeln/hindernis.py) nimmt eine freie
   Nummer aus dem Bereich des Auftrags. Dafür hat `hindernisMelden` sechs Parameter und
   schaltet die Regel dagegen ab (`# noqa: PLR0913`); ein Aufruf als ein Objekt genügte.
3. Architekturkarte im Dashboard, wie du sie in Anliegen 2740 gewählt hast:
   [rollenregeln/dashboardArchitektur.py](../prozess/pruefungen/rollenregeln/dashboardArchitektur.py)
   (166 Zeilen) und [architekturMessung.py](../prozess/pruefungen/rollenregeln/architekturMessung.py)
   (99) zeichnen sie, [formregeln/erlaubteImporte.py](../prozess/pruefungen/formregeln/erlaubteImporte.py)
   (29) hält die erlaubten Pfeile einmal für Karte und Importvertrag. Ich empfehle, sie zu
   behalten: Eine falsche Abhängigkeit siehst du dort, ohne Code zu lesen. Willst du sie
   nicht, schreib im Kommentar „Architekturkarte entfernen“; dann entfernt der Regelumsetzer
   in der Nachkorrektur 265 Zeilen, `erlaubteImporte.py` bleibt für den Importvertrag.
4. Neue Fassung des Plans: [standregeln/planFassung.py](../prozess/pruefungen/standregeln/planFassung.py)
   (38, neu) merkt sich den Plan; ändert er sich, öffnet
   [fortschritt.py](../prozess/pruefungen/standregeln/fortschritt.py) (+27) die Kritik am Plan
   wieder und führt die Kritik am Review als eigene Zeilen;
   [abhaken.py](../prozess/pruefungen/standregeln/abhaken.py) (+37) meldet einen schon
   abgehakten Schritt, statt zu scheitern. Klein: `neuGefasst` (`planFassung.py:30`) fragt und
   schreibt dabei den Merkzettel, der Name sagt nur die Frage.
5. Bash-Verbote: [rollenregeln/bashSchreiben.py](../prozess/pruefungen/rollenregeln/bashSchreiben.py)
   (+40) erkennt Schreibbefehle auch hinter `find -exec`, `xargs`, `if` und `while`;
   `.claude/settings.json:42-51` verbietet `sed -i`, `python3 -c` und `python3 -`.
   Wesentlich: Die Verbote greifen nur, wenn der Befehl mit `python3` oder `python` beginnt;
   `.venv/bin/python -c` bleibt frei. Willst du die Lücke schließen, schreib im Kommentar
   „Python-Verbote auch für .venv/bin/python“; das geht dann an den Regelumsetzer, der es an
   einer Kopie erprobt (von mir ohne Probe).

## Nächstes Vorgehen
- **Produktziel:** Etappe 1 von 10 ist erreicht, Etappe 2 läuft. Am meisten fehlt die Partie
  nach der Bewegungsphase: Schießen, Angreifen, Nahkampf, Moral.
- **Etappenziel:** Zu [Etappe 2](../domaene/etappen/02-bewegen.md) fehlt, was Plan 8 unter
  „Noch nicht“ nennt: jede *Einheit* nur einmal ziehen, Advance, Zurücksetzen, über die Kante,
  *Nahkampfreichweite* (sperrt schon, ohne Test), *gemeinsam übergehen* mit *Protokoll*,
  Ork-Psioniker und Canoptek-Spinne, Loslassen neben der *Karte*; der Stand nennt 95 von 123
  Kriterien belegt. Ich schätze zwei Zyklen.
- **Zyklusziel:** Plan 9: In der *Bewegungsphase* zieht jede *Einheit* nur einmal, mit Advance
  weiter nach eurem Würfelwurf, nicht über die Kante; eine *Sperre* übergeht ihr *gemeinsam*,
  das *Protokoll* hält es fest; ‚Nahkampfreichweite‘ sperrt mit Test (6241); ein Klick auf
  die leere *Karte* hebt die Auswahl auf (6240). Noch nicht: Zurücksetzen, Ork-Psioniker und
  Canoptek-Spinne, Loslassen neben der *Karte*. Vorher: Anliegen 6102
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
Freigabe: ja
Kommentar: .
Stellungnahme: Zu deiner Frage im Chat zu Schritt 11: Ja, das ist so in Zyklus 8. Ein
einzelnes *Modell* *auswählen* geht in der *Schlacht* noch nicht (Anliegen 5520, F3 B, für
Domänenphase 9); allein ziehen geht nur, solange seine *Einheit* nicht *ausgewählt* ist. Der
Klickpfad sagte nicht, wie; Schritte 9 bis 11 unter „Am Bildschirm prüfen“ sagen es jetzt.
Schritte 6 bis 11 habe ich am laufenden Arbiter nachgestellt: Nur der Boy rückt, „Phase
beenden“ nennt ‚keine Kohärenz‘. Im Produkt fehlt kein Schritt, kein neues Anliegen.
