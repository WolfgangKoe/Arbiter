# Review · Zyklus 10

Start der App: `.venv/bin/arbiter` aus der Wurzel ([Web, W5](../technik/architektur/web.md#aufbau)),
dann `http://127.0.0.1:8040/` im Browser öffnen.

## Am Bildschirm prüfen
Mit Maus oder Finger stellt ihr beide Armeen auf, wählt den ersten Zug, geht durch die Phasen
und zieht in der *Bewegungsphase* eure *Einheiten*: Arbiter hält an *Bewegungsweite*,
*Spielfeldkante*, *Nahkampfreichweite* und vor fremden *Bases* an, ihr könnt ein Anhalten
gemeinsam übergehen und eine *Einheit* zurücksetzen; die Canoptek-Spinne fliegt.
1. Start: Arbiter nennt `http://127.0.0.1:8040/`.
2. Beim Aufstellen einen Boy neben dem *Spielfeld* loslassen: Er steht, wo das *Spielfeld* ihn
   zuletzt zeigte.
3. Beim Aufstellen einen Boy auf eine fremde *Base* zu ziehen: Er hält davor an und gleitet an
   ihr entlang; Loslassen *setzt* ihn dort, kein ‚über eine Base‘ mehr.
4. Erster Zug, „Phase beenden“ bis zur *Bewegungsphase*. Die Boyz über ihre *Bewegungsweite*
   ziehen und loslassen: Sie stehen an der *Bewegungsweite*, „gemeinsam übergehen“ erscheint.
   Klick darauf: Sie stehen, wo ihr losgelassen habt; das *Protokoll* nennt ‚Bewegungsweite‘.
5. Die Boyz noch einmal ziehen, auch zurück: Sie bleiben stehen, „gemeinsam übergehen“
   erscheint wieder.
6. „Einheit zurücksetzen“: Die Boyz stehen, wo die Phase begann.
7. Die Boyz in *Nahkampfreichweite* eines Gegners ziehen und *auswählen*: Kein „Vorrücken“.
8. Die Canoptek-Spinne über fremde *Bases* ziehen und auf einer loslassen: Sie rückt an die
   nächste freie *Stelle*.
9. Eine *Leiste* ein- und ausfahren: Kein *Modell* auf dem *Spielfeld* verschiebt sich.

Den Klickpfad bin ich nicht am laufenden Arbiter durchgegangen; jeder Schritt ist durch die
Bildschirmtests gegen den echten Server belegt (`technik/tests/akzeptanz/`, etwa
[uebergehenBeimZiehenTest](../technik/tests/akzeptanz/phasen/bewegung/uebergehenBeimZiehenTest.py),
[anhaltenVorFremdenBasesTest](../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorFremdenBasesTest.py),
[fliegenTest](../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py)). Bitte sieh ihn dir an.

## DoD
1. **Erfüllt.** `technik/tests` und `prozess/pruefungen` auf Stand 4edbbbd: 2688 grün, darin
   die Prüfung `abdeckung` (95 % für `technik/arbiter` und `technik/frontend/`). Danach hat sich
   nur Anliegen 7800 geändert (Commit „7800 erledigt: Nachprüfung des Anforderungsautors“).
2. **Erfüllt.** Prüfungen grün (siehe 1); SonarLint auf Stand 525be63: keine Funde. Kein TODO
   und kein `noqa` im Produkt.
3. **Erfüllt.** Alle sechs Items von Plan 10 gelöscht, die Kriterien beschreiben das Gebaute.
4. **Erfüllt**, sobald dieses Review freigegeben ist: Der Fachkritiker hat alle sechs Items
   abgenommen (zuletzt Commit „ruhigeKarte: Item abgenommen“).

Oberfläche: **erfüllt.** Bildschirmtests grün; die Mockups zu BEW-8, BEW-24 und QUE-7 sind
gelöscht, unter `domaene/mockups/` liegen nur die zu gewinnerUndZone (`auf-11-*`).
Mutation: **nicht erfüllt.** Der gezielte Lauf über die seit „Freigabe Plan 10“ geänderten
Zeilen läuft noch (`/tmp/mutation10.log`); bis jetzt 63 von 327 Mutanten überlebt, 81 %, Schwelle
95 %. Am meisten in `fliegen.py` (12 von 60). Am Bildschirm ändert das nichts; jeder Überlebende
wird ein Test oder eine Begründung als gleichwertig, dafür ein Auftrag an den Testautor, sobald
der Lauf fertig ist.

## Code
`/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe seit „Freigabe Plan 10“:
nichts hält auf. Was die Kritik am Code schon fand, wartet auf Technikphase 11 (Gleiten und
Fliegen: 12681, 12702, 12904, 12962, 13640, 13661, 13761, 14240, 14261; Übergehen: 11860, 11880;
Katalog: 10720, 13540; Umbenennen: 15260, 15280, 15281). Neu:
[15320](anliegen/15320-fliegenRechnetAnteileZweimal.md): *Fliegen* rechnet zwei Anteile je
Zeigerbewegung doppelt, der Server nennt das Gerät zweimal. Dass das Ziehen die zuvor gezeigte
*Stelle* vom Browser mitschickt, hat der Architekt so entschieden
([Vertrag Ziehen](../technik/architektur/vertrag/querschnitt/ziehen.md)): Die Domäne merkt sich
kein Ziehen.

## Empfehlung
Gib Review 10 frei, sobald die Mutation die Schwelle hält. Der Happy Path von Plan 10 ist gebaut, Schritte 1 bis 7; damit ist Etappe 2
erreicht. Die übrigen Anliegen warten auf spätere Phasen ([Moderation](moderation.md)).

## Rundgang Prüfcode
Seit „Freigabe Review 9“ 45 Dateien in [prozess/pruefungen](../prozess/pruefungen) und
[.claude/settings.json](../.claude/settings.json), 1.602 Zeilen neu, 178 fort. Neu oder
wesentlich geändert:
- Abdeckung des Frontends in den Bildschirmtests ([frontendMessung.py](../prozess/pruefungen/formregeln/frontendMessung.py),
  [frontendZeilen.py](../prozess/pruefungen/formregeln/frontendZeilen.py), [abdeckung.py](../prozess/pruefungen/formregeln/abdeckung.py)).
- Hindernisse im Fortschritt: [testsRot.py](../prozess/pruefungen/standregeln/testsRot.py),
  [standVorDerUmsetzung.py](../prozess/pruefungen/standregeln/standVorDerUmsetzung.py),
  [wartendeSchritte.py](../prozess/pruefungen/standregeln/wartendeSchritte.py),
  [abhaken.py](../prozess/pruefungen/standregeln/abhaken.py), [beseitigt.py](../prozess/pruefungen/standregeln/beseitigt.py).
- Mutation: Ergebnis je Modul, gleichwertige Mutanten an ihren Bereich gebunden
  ([mutation.py](../prozess/pruefungen/mutationsregeln/mutation.py),
  [gleichwertig.json](../prozess/pruefungen/mutationsregeln/gleichwertig.json), 158 Zeilen).
- Dashboard und Schreibgrenze ([dashboardSeiten.py](../prozess/pruefungen/rollenregeln/dashboardSeiten.py),
  [bashSchreiben.py](../prozess/pruefungen/rollenregeln/bashSchreiben.py)).

Probleme:
1. Die Hindernisse machen den Plan 52.207 Zeichen lang, weil `abhaken.py` jeden grünen
   Testnamen in den Satz schreibt (Anliegen 15301, wartet auf die Prozessphase).
2. Den Prüfcode habe ich in diesem Zyklus nicht Zeile für Zeile gelesen, nur Umfang und Zweck;
   die Durchsicht der Dateien oben steht noch aus. Empfehlung: ich hole sie in der Nachkorrektur
   nach, bevor du kommentierst.

## Nächstes Vorgehen
- **Produktziel:** Etappe 1 erreicht (Commit „Freigabe Etappe 1“), Etappe 2 mit diesem Zyklus
  (Stand: 82 von 82 Kriterien der Etappe belegt). Am meisten fehlt die Partie nach der
  *Bewegungsphase*: Schießen, Angreifen, Nahkampf, Moral.
- **Etappenziel:** Zu [Etappe 2](../domaene/etappen/02-bewegen.md) fehlt nach der Abnahme des
  Fachkritikers nichts am Bildschirm; offen ist die Mutation. Null Zyklen.
- **Zyklusziel:** Plan 11 beginnt Etappe 3. Vorher müssen weg: die Aufräumarbeit an Gleiten,
  Fliegen und Übergehen aus den oben genannten Anliegen, die Umbenennungen nach 7800 (15260,
  15280, 15281, 15300, 15261) und die Lücken der Mutation; sonst wachsen sie mit jedem Item.
  Was danach am Bildschirm neu ist, schneidet der Planer aus Etappe 3.

## Fortschritt
- [ ] Anforderungsautor: Happy Paths zum Zyklusziel
- [ ] UX: Mockups, bei einer Oberfläche
- [ ] Fachkritiker: Kritik an Anforderungen und Mockups
- [ ] Anforderungsautor: Anliegen 10120 Was gemeinsam übergehen bei ‚nicht am Zug‘ nach sich zieht
- [ ] Anforderungsautor: Anliegen 10201 Übergehen: aus der Nahkampfreichweite weiterziehen, Kante vor der Bewegungsweite
- [ ] Anforderungsautor: Anliegen 10322 Zurücksetzen auf Stellen, die inzwischen eine andere Einheit belegt
- [ ] Planer: Anliegen 13842 Drei Akzeptanztest-Dateien über dem Höchstmaß, kein Item dazu
- [ ] Anforderungsautor: Anliegen 14320 Fliegen: BEW-18.3 und BEW-25.1 widersprechen sich beim Weiterziehen
- [ ] Anforderungsautor: Anliegen 15100 Auch der Griff einer Leiste verschiebt die Karte nicht
- [ ] Fachkritiker: Anliegen 15220 Link auf QUE-7 nach dem Umbenennen
- [ ] UX: Anliegen 15261 Mockups heißen noch Karte, `.spielfeld` meint dort ein anderes Element
- [ ] Anforderungsautor: Anliegen 15300 Überschrift von AUF-20 nach Einheiten- und Modellebene
- [ ] Planer: Plan geschrieben
- [ ] Fachkritiker: Kritik am Plan
- [ ] Architekt: Kritik am Plan
- [ ] Stakeholder: Freigabe Plan 11

## Freigabe
Freigabe: offen
Kommentar: .
