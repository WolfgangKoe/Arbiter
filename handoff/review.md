# Review · Zyklus 10

Start der App: `.venv/bin/arbiter` aus der Wurzel ([Web, W5](../technik/architektur/web.md#aufbau)),
dann `http://127.0.0.1:8040/` im Browser öffnen.

## Am Bildschirm prüfen
Mit Maus oder Finger stellt ihr beide Armeen auf, wählt den ersten Zug, geht durch die Phasen
und zieht in der *Bewegungsphase* eure *Einheiten*: Arbiter hält an *Bewegungsweite*,
*Spielfeldkante*, *Nahkampfreichweite* und vor fremden *Bases* an; ein Anhalten an
*Bewegungsweite* oder *Nahkampfreichweite* könnt ihr gemeinsam übergehen, eine *Einheit*
zurücksetzen; die Canoptek-Spinne fliegt.
1. Start: Arbiter nennt `http://127.0.0.1:8040/`. Vor dem *ersten Zug* gibt es kein „Phase beenden“.
2. Beim Aufstellen die Boyz neben das *Spielfeld* ziehen und loslassen: Sie stehen, wo das
   *Spielfeld* sie zuletzt zeigte. Auch der Weirdboy lässt sich aufstellen.
3. Beim Aufstellen den Warboss auf die Boyz ziehen: Er hält vor ihren *Bases* an und gleitet
   entlang; Loslassen *setzt* ihn dort, kein ‚über eine Base‘ mehr.
4. „Erster Zug“ bei Spieler 1, „Phase beenden“ bis zur *Bewegungsphase*. Einen Boy anklicken
   (die Boyz sind *ausgewählt*), dann die Boyz weit Richtung Necrons ziehen und loslassen: Sie
   stehen an der *Bewegungsweite*, „gemeinsam übergehen“ erscheint.
5. Die Boyz noch einmal ziehen: Sie halten wieder an. Mit „Einheit zurücksetzen“ stehen sie,
   wo die Phase begann.
6. Die Boyz bis in *Nahkampfreichweite* der Necron Warriors ziehen, loslassen, „gemeinsam
   übergehen“: Sie stehen, wo ihr losgelassen habt; das *Protokoll* nennt ‚Bewegungsweite‘
   und ‚Nahkampfreichweite‘. Ausgewählt bietet Arbiter kein „Vorrücken“.
7. „Phase beenden“ bis zur *Bewegungsphase* von Spieler 2. Die Canoptek-Spinne über fremde
   *Bases* ziehen und auf einer loslassen: Sie rückt an die nächste freie *Stelle*.
8. Die linke *Leiste* einfahren: Das *Spielfeld* rückt zur Seite. So verlangt es heute
   QUE-7.1; du willst es anders (Anliegen 15460).

Schritte 1 bis 6 und 8 bin ich am laufenden Arbiter durchgegangen (per Skript im Browser,
Bildschirmfotos angesehen). Schritt 7 zeigt nur der Bildschirmtest
[fliegenTest](../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py); die Spinne kam am
Bildschirm nicht bis zu fremden *Bases*.

## DoD
1. **Erfüllt.** Alle Tests und Prüfungen grün auf Commit „Mockups gebauter Items gelöscht …“
   (Lauf vor Commit „Review 10 geschrieben“), darin `abdeckung` (95 % für `technik/arbiter`
   und `technik/frontend/`).
2. **Erfüllt.** Prüfungen grün; SonarLint ohne Funde. Kein TODO und kein `noqa` im Produkt.
3. **Erfüllt.** Alle sechs Items von Plan 10 gelöscht, die Kriterien beschreiben das Gebaute.
4. **Nicht erfüllt.** Der Fachkritiker hat alle sechs Items abgenommen, du nimmst zwei nicht
   ab: ruhiges *Spielfeld* und *gemeinsam übergehen* (Anliegen 15460).

Oberfläche: **erfüllt.** Bildschirmtests grün, die Mockups zu BEW-8, BEW-24 und QUE-7 gelöscht.
Mutation: **nicht erfüllt.** 374 Mutanten, 82 % gefangen, Schwelle 95 %; am meisten
überleben in `messen.py` (38 von 132), dann `fliegen.py` (12 von 60). Kritik an den
Testautor: Anliegen 15462.

## Code
`/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe seit „Freigabe Plan 10“:
nichts hält auf. Neu: [15320](anliegen/15320-fliegenRechnetAnteileZweimal.md), *Fliegen*
rechnet zwei Anteile je Zeigerbewegung doppelt. Was die Kritik am Code schon fand, wartet auf
Technikphase 11, Liste in der [Moderation](moderation.md).

## Empfehlung
Gib Review 10 frei, wenn `mutationsregeln.mutation` 95 % meldet; die Zahl trage ich nach.
Etappe 2 ist nicht erreicht. Leisten und Übergehen: Empfehlung B in
Anliegen 15460, als Plan 11.

## Rundgang Prüfcode
Seit Commit „Freigabe Review 9“ 45 Dateien in [prozess/pruefungen](../prozess/pruefungen) und
[.claude/settings.json](../.claude/settings.json), 1.602 Zeilen neu, 178 fort. Neu oder
wesentlich geändert:
- Abdeckung des Frontends in den Bildschirmtests ([frontendMessung.py](../prozess/pruefungen/formregeln/frontendMessung.py),
  [frontendZeilen.py](../prozess/pruefungen/formregeln/frontendZeilen.py), [abdeckung.py](../prozess/pruefungen/formregeln/abdeckung.py)).
- Hindernisse im Fortschritt ([abhaken.py](../prozess/pruefungen/standregeln/abhaken.py),
  [testsRot.py](../prozess/pruefungen/standregeln/testsRot.py), [wartendeSchritte.py](../prozess/pruefungen/standregeln/wartendeSchritte.py)).
- Mutation: gleichwertige Mutanten an ihren Bereich gebunden; in
  [gleichwertig.json](../prozess/pruefungen/mutationsregeln/gleichwertig.json) 16 neue
  Begründungen, nach denen ein Überlebender nicht zählt (Anliegen 15380).
- Beim Commit: [.pre-commit-config.yaml](../.pre-commit-config.yaml), Zeile 6, lässt die
  Prüfungen `vollstaendig` aus ([pyproject.toml](../pyproject.toml), Zeile 17); sie laufen nur
  im Lauf über alles.
- [anliegen.py](../prozess/pruefungen/anliegenregeln/anliegen.py): Zeilen `A:` und
  `Empfehlung:` unter einer Frage (Anliegen 9250);
  [architekturKanten.py](../prozess/pruefungen/rollenregeln/architekturKanten.py), Zeile 152.

Probleme:
1. Die Hindernisse machen den Plan über 50.000 Zeichen lang ([15301](anliegen/15301-hindernisseBlaehenDenPlan.md)).
2. Ein Commit prüft `vollstaendig` nicht mehr; was nur sie fängt, merkt erst der Lauf über alles.
3. Die Dateien habe ich nach Zweck und Fundstelle gesichtet, nicht Zeile für Zeile; weitere
   Probleme kann ich nicht ausschließen.

## Nächstes Vorgehen
- **Produktziel:** Etappe 1 erreicht (Commit „Freigabe Etappe 1“). Am meisten fehlt die Partie
  nach der *Bewegungsphase*: Schießen, Angreifen, Nahkampf, Moral.
- **Etappenziel:** Zu [Etappe 2](../domaene/etappen/02-bewegen.md) fehlen am Bildschirm die
  *Leisten* über dem *Spielfeld* und das freie Ziehen nach *gemeinsam übergehen*
  (Anliegen 15460), dazu die Mutation. Ein Zyklus.
- **Zyklusziel:** Nach Plan 11 fahrt ihr eine *Leiste* ein und aus, und das *Spielfeld*
  bleibt stehen; nach „gemeinsam übergehen“ zieht ihr die *Einheit* oder einzelne *Modelle*
  frei, sie folgen dem Zeiger. Noch nicht: Arbiter zeigt nicht, welche *Einheit* schon
  gezogen hat ([Etappe 3](../domaene/etappen/03-angriffUndFallBack.md)). Vorher müssen weg:
  die Lücken der Mutation (Anliegen 15462), das
  Aufräumen an Gleiten, Fliegen und Übergehen und die Umbenennungen nach 7800 (wartende
  Anliegen der Technikphase 11, [Moderation](moderation.md)). Etappe 3 formuliert der Planer
  erst aus, wenn Etappe 2 erreicht ist ([15361](anliegen/15361-etappenschritteNachErreichterEtappe.md)).

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
- [ ] Anforderungsautor: Anliegen 15461 Nach „gemeinsam übergehen“ folgen die Modelle dem Zeiger
- [ ] Planer: Plan geschrieben
- [ ] Fachkritiker: Kritik am Plan
- [ ] Architekt: Kritik am Plan
- [ ] Stakeholder: Freigabe Plan 11

## Freigabe
Freigabe: ja
Kommentar: .
