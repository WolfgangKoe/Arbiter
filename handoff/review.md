# Review · Zyklus 6

Start der App: `.venv/bin/arbiter` aus der Wurzel ([Web, W5](../technik/architektur/web.md#aufbau)),
die genannte Adresse im Browser öffnen.

## Am Bildschirm prüfen
Mit Maus oder Finger: *Einheit* in der *Ablage* anklicken, per Klick in die Zone *setzen*, als
Block oder ein *Modell* allein verschieben, beenden, bis alle vier stehen.
1. Start: oben „Spieler 2 · an der Reihe“, links blaue, rechts rote *Aufstellungszone*.
2. „Necron Warriors“ in der rechten *Ablage* anklicken: goldener Rahmen, nur sie ist
   *ausgewählt*. Keine Knöpfe auf der *Einheitenkarte*, kein „in Aufstellung“.
3. In die rote Zone klicken: zehn Kreise als *Formation* um den Klick, alle golden umrandet;
   nahe am Rand rücken sie ganz hinein.
4. Einen Kreis gedrückt halten und ziehen: alle zehn wandern mit. Am Rand der Zone und vor einem
   fremden Kreis halten sie schon beim Ziehen an; Loslassen *setzt* sie dort.
5. Einen Kreis anklicken: nur er ist golden umrandet, Ziehen bewegt nur ihn, er hält ebenso an.
   Erneut anklicken: wieder alle golden, Ziehen bewegt den Block.
6. „Aufstellen der Einheit beenden“: Spieler 1 ist *an der Reihe*.

Belegt durch die Bildschirmtests gegen den echten Server, mit Maus und Finger (ebeneTest,
blockAlsGanzesTest, modellPerKlickTest, anhaltenAnEinerBaseTest). Von Hand am laufenden Arbiter
habe ich den Pfad in diesem Lauf nicht durchgespielt; der Fachkritiker hat Schritte 4 und 5
mit der Maus nachgespielt ([1610](anliegen/1610-ziehenUeberDieKanteUndGreifpunkt.md)).
Abweichungen von ArbiterMap: Loslassen über der Kante der *Karte* springt zurück, Greifpunkt
springt in die Mitte (1610, wartet auf die Domänenphase).

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 744 grün, mit Bildschirm-, Querschnitts- und
   Missionsvorbereitungstests; Abdeckung über 95 % (`abdeckung.py`
   grün). Nur Unit-Tests erreichen in den neuen Modulen: Weg der Länge null
   (`messen.py:132`), Loslassen eines nicht *gesetzten* *Modells* (`anhaltenAnEinerBase.py:15`,
   `einheitVerschieben.py:17`; die Seite schickt es nicht, der Dienst nimmt es an), Prüfungen
   der *Auswahl* auf fremde Objekte: Vorbedingungen. `_loslassen` mit *Sperre* (`__init__.py:159`)
   erreicht nur ein Klick, dessen *Formation* fremde *Bases* überdeckt: Kriterium fehlt, Plan 7
   (AUF-18.7, 27).
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 763 grün, ruff sauber; SonarLint: keine
   Funde, nachdem der Implementierer `anwendung.py:26` angepasst hat (Anliegen 1630,
   erledigt).
3. **Erfüllt mit Vorbehalt.** Items gelöscht; der Zweck von AUF-26 verspricht mehr, als gebaut
   ist ([1610](anliegen/1610-ziehenUeberDieKanteUndGreifpunkt.md), Punkt 3, wartet).
4. **Erfüllt.** Der Fachkritiker hat beide Items abgenommen (1610).

Oberfläche: **Erfüllt.** Bildschirmtests grün; die Mockups der Items hat Ux gelöscht
(Anliegen 1631, erledigt).

Mutation: **Erfüllt.** Der volle Lauf ergab 93 %, 15 Mutanten überlebten. Alle 15 sind
angegangen. Gezielt nachgeprüft, ohne vollen Lauf, wie von dir vorgegeben: Die Tests fangen
alle 83 Mutanten der umgeschriebenen Zeilen. Das sind über 95 %
(Anliegen 1632, erledigt). Nach 1760 ebenso gezielt: Von
17 Mutanten der geänderten Zeilen fangen die Tests 15, die zwei übrigen ändern das Ergebnis
nicht (gleichwertig, Begründung in 1760). Der volle Lauf folgt in der Retro.

## Code
`/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe über den Diff seit Commit
„Item setzenPerKlick: …“: kein weiterer Befund. Die Rückung steht einmal in `messen.py` und dient
Formation und Block; das *Gesperrte* ist ohne Rest aus Code, Vertrag und Seite. Die Abfrage
beim Ziehen läuft höchstens einmal zugleich (0,02 bis 0,09 s je Antwort, 1551).

Kritik am Code zu 1640, 1656 und 1710: Der aufhaltende Befund
Anliegen 1760 ist erledigt. Klickt man einen
Warboss oder Overlord in die Zone, rechnet Arbiter seine *Stelle* wieder exakt; ein neuer
Unit-Test fängt den alten Fehler. Die zwei nur umgeformten Zeilen lesen sich wieder fachlich.
Die Änderung selbst: kein weiterer Befund. Der Architekt schlägt dazu eine Prüfung vor, die
eine ungenaue *Stelle* künftig sofort meldet
([1752](anliegen/1752-stellePrueftFractionSelbst.md), wartet auf die Technikphase). Ein Befund
wartet:
[1761](anliegen/1761-loslassenOhneAntwortBleibtInDerVorschau.md). Antwortet Arbiter beim
Loslassen nicht, bleiben die Kreise an der Vorschau stehen. 1656 ist umgesetzt.

## Empfehlung
Die DoD ist erfüllt; kein Befund hält mehr auf. Die Items einheitVerschieben und
anhaltenAnBases können committet werden. 1610 wartet auf die Domänenphase, 1752 und 1761
auf die Technikphase.

## Rundgang Prüfcode
Seit Commit „Freigabe Review 5“: rund 1.670 Zeilen neu in `prozess/pruefungen/`, vor allem
Fortschritt und Hindernis (`standregeln/fortschritt.py`, `hindernis.py`, `abhaken.py`,
`beseitigt.py`, `produktstand.py`), Mutationstests (`mutationsregeln/mutation.py`,
`mutanten.py`), Schreibgrenze und Prozessphase (`rollenregeln/schreibgrenze.py`,
`regelnNurInProzessphase.py`), Commit-Hooks (`formregeln/commitHooksTest.py`).
1. `standregeln/fortschritt.py:100` hakt „DoD über das Inkrement“ als Fakt ab, sobald kein
   Item offen ist; die Tabelle im [Ablauf](../prozess/ablauf.md#fortschritt) verlangt den Befehl
   des Reviewers. Im Plan stand der Haken vor diesem Lauf, obwohl SonarLint rot ist.
2. `mutationsregeln/mutation.py`: Jeder Mutant startet Unit- und alle Akzeptanztests samt
   Bildschirmtests; gleichwertige Mutanten zählen gegen die Schwelle, ohne Weg, sie zu
   kennzeichnen (1551, 1570). Mutiert werden nur Domänenmodule, nicht `web/`.
3. `standregeln/hindernis.py`, `nächsteNummer`: höchste Nummer plus eins; liegt sie in einem
   Nummernbereich, den der Koordinator einer anderen Rolle gab, kollidieren die Läufe.

## Nächstes Vorgehen
- **Produktziel:** keine der 7 Etappen erreicht; am meisten fehlt das Bewegen (Etappe 2).
- **Etappenziel:** Dein Happy Path aus Plan 6 ist machbar (Schritte 1 bis 6 oben). Es fehlen
  die Randfälle aus „Randfälle, Plan 7“ im [Plan](plan.md): „gemeinsam übergehen“ mit
  *Protokoll*, *zurücklegen*, Klick auf ein *Modell* einer nicht *ausgewählten* *Einheit*,
  *Formation* über fremden *Bases*; dazu 1610. Ein Zyklus.
- **Zyklusziel:** Plan 7: Ihr könnt eine *Einheit* auf ihre *Ablage* *zurücklegen*, eine
  *Sperre* gemeinsam übergehen, und Loslassen über der Kante *setzt* dort, wo die *Karte* zuletzt
  zeigte, wie in ArbiterMap. Danach ist Etappe 1 erreicht. Vorher: 1632.

## Fortschritt
- [ ] Anforderungsautor: Happy Paths zum Zyklusziel
- [ ] UX: Mockups, bei einer Oberfläche
- [ ] Fachkritiker: Kritik an Anforderungen und Mockups
- [ ] Planer: Plan geschrieben
- [ ] Fachkritiker: Kritik am Plan
- [ ] Architekt: Kritik am Plan
- [ ] Stakeholder: Freigabe Plan 7

## Freigabe
Freigabe: ja
Kommentar: Ich habe alles mal geprüft und auch ein paar Code-Dateien überflogen. der Koordinator hat entsprechend ein paar Anliegen in meinem Namen aufgesetzt. Im Blick darauf gebe ich die Review frei. Hier im Fortschrittplan fehlt noch der Fortschritt für die Prozessphase und retro.md selbst. Kann das sein? -> Organisationsentwickler
Stellungnahme: Ja, so gewollt; am Review ändert sich nichts. Das Review trägt nur den Fortschritt der Domänenphase 7, die Prozessphase steht in der [Retro](retro.md) ([Ablauf, Fortschritt](../prozess/ablauf.md#fortschritt)). Die Retro 6 liegt als Entwurf vor; ihren Fortschritt schreibt das Skript erst mit dem Commit „Freigabe Review 6“, der noch aussteht. Der Organisationsentwickler hat das in Anliegen 1671 beantwortet (Absatz unter dem Befund).
