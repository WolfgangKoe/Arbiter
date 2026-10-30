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

Du bist den Klickpfad durchgegangen und einverstanden.

## DoD
1. **Erfüllt.** Alle Tests in `technik/tests` grün, Abdeckung über 95 % (Prüfung `abdeckung`).
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 937 grün; SonarLint ohne Fund. Die
   Meldung S1172 am Parameter `vorrückwurf`, die der Implementierer in der IDE sah, gibt es
   auf ca2bda8 nicht: Dieselbe SonarLint-Version meldet in einer Kopie einen wirklich
   unbenutzten Parameter derselben Funktion, `vorrückwurf` nicht. Wohl ein veralteter Stand
   im Editor. Seither hat sich nur der Mutationslauf geändert (8122): Auf 1cafd47 sind seine
   18 Tests, die Prüfungen zu Benennung, Kommentaren und Komplexität, ruff und SonarLint grün.
3. **Erfüllt.** Alle vier Items gelöscht; die Kriterien beschreiben das Gebaute.
4. **Erfüllt.** Der Fachkritiker hat alle vier Items abgenommen.

Oberfläche: **Erfüllt.** Bildschirmtests grün; die acht Mockups des Gebauten sind gelöscht,
unter `domaene/mockups/` liegen nur noch die der offenen Items. Anliegen 8760 ist erledigt;
`erledigteLoeschen.py` hat es nach dem Commit gelöscht, wie vorgesehen.
Mutation: **offen.** Der volle Lauf mit 8 Kernen läuft seit 22:19 auf 1cafd47 und hat noch
kein Modul fertig. Danach holt der gezielte Lauf über die geänderten Zeilen seine Ergebnisse
aus dem Merkzettel; ich trage die Zahl nach, Lücken gehen an den Testautor.

## Code
`/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe seit „Freigabe Plan 9“:
nichts hält auf. Kein `noqa`, kein TODO im Produkt. Warten auf Technikphase 10: Die Suche
nach der *Einheit* eines *Modells* steht dreimal da, ein Test zu zwei *Einheiten*, von denen
nur eine *vorgerückt* ist, fehlt (Anliegen 8740); zwei Tests zur *Auswahl* prüfen zu wenig
(Anliegen 8720).

## Empfehlung
Gib Review 9 frei, sobald die Mutation die Schwelle hält: Der Klickpfad zeigt, was Plan 9 versprochen hat, Schritte 1 bis 5 des Happy Path.
Die übrigen Anliegen warten auf spätere Phasen ([Moderation](moderation.md)).

## Rundgang Prüfcode
Seit „Freigabe Review 8“ 95 Dateien in [prozess/pruefungen](../prozess/pruefungen) und
[.claude/settings.json](../.claude/settings.json), 1.317 Zeilen neu, 713 fort. Gut 60 Dateien
haben nur ihre Docstrings verloren (P4, Anliegen 6430); daran ist nichts zu prüfen. Neu oder
geändert:
- Länge der Anliegen ([anliegenLaenge.py](../prozess/pruefungen/anliegenregeln/anliegenLaenge.py)):
  rot über 4.000 Zeichen je Runde, ein Hinweis direkt nach dem Schreiben (neuer Hook nach
  Write und Edit in `settings.json`).
- Docstrings nur als Kopf einer Akzeptanztestdatei ([kommentare.py](../prozess/pruefungen/formregeln/kommentare.py)).
- Reiter „Architektur“ im Dashboard, aufklappbar bis zu den Dateien
  ([dashboardArchitektur.py](../prozess/pruefungen/rollenregeln/dashboardArchitektur.py),
  [architekturKanten.py](../prozess/pruefungen/rollenregeln/architekturKanten.py),
  [architekturMessung.py](../prozess/pruefungen/rollenregeln/architekturMessung.py)).
- Stand nennt die belegten Kriterien der Etappe ([produktstand.py](../prozess/pruefungen/standregeln/produktstand.py),
  [kriterienEtappe.py](../prozess/pruefungen/kriterienregeln/kriterienEtappe.py)) und die Rolle
  des Prozess-Items ([phasenfolge.py](../prozess/pruefungen/standregeln/phasenfolge.py)).
- Fortschritt ohne Testzeilen für ein Item ohne Kriterium ([fortschritt.py](../prozess/pruefungen/standregeln/fortschritt.py)).
- „Wartet auf“ getrennt nach Nummer, Phase, Zyklus ([anliegenKopf.py](../prozess/pruefungen/lesen/anliegenKopf.py)).
- Mutationslauf schreibt und merkt sich jedes fertige Modul und verteilt die Mutanten eines
  Moduls auf alle Kerne, je Kern eine Kopie in `/tmp` ([mutation.py](../prozess/pruefungen/mutationsregeln/mutation.py), Anliegen 8122).
- Schreibgrenze erkennt das Ziel von `cp -t` ([bashSchreiben.py](../prozess/pruefungen/rollenregeln/bashSchreiben.py)).

Probleme, keins hält auf:
1. Der Hook „Stand“ vor jeder Rolle braucht jetzt 5,3 von 10 Sekunden: `belegungAlsText`
   ([produktstand.py](../prozess/pruefungen/standregeln/produktstand.py), Zeile 34) zählt die
   Kriterien zweimal, für alle und für die Etappe, und sucht dabei jedes Mal alle Tests; das
   Dashboard tut es nach jedem Lauf noch einmal. Wächst das Repo, fällt der Stand aus.
   Empfehlung: einmal zählen und je Kriterium die Etappe mitnehmen.
2. Die Liste der Kästen steht dreimal: in [erlaubteImporte.py](../prozess/pruefungen/formregeln/erlaubteImporte.py)
   und als `zeilen` und `titel` in [dashboardArchitektur.py](../prozess/pruefungen/rollenregeln/dashboardArchitektur.py)
   (Zeilen 19 und 20). Ein neuer Kasten fehlt auf dem Reiter ohne Meldung. Dazu baut
   `kastenDesPfads` ([architekturKanten.py](../prozess/pruefungen/rollenregeln/architekturKanten.py),
   Zeile 36) `kastenDesModuls` nach. Empfehlung: Reihen und Titel aus einer Tabelle neben
   `kastenNamen`.
3. Doppelte Arbeit im Fortschritt: `hatKriterium` und `itemKriterienGetestet`
   ([fortschritt.py](../prozess/pruefungen/standregeln/fortschritt.py), Zeilen 59 und 66) suchen
   je Item zweimal dieselben Kriterien; `itemRollen` liest die Retro ein zweites Mal
   ([phasenfolge.py](../prozess/pruefungen/standregeln/phasenfolge.py), Zeile 47).
4. Klein: `längeBefund` gibt „rot“ oder „hinweis“ als Wort zurück, das der Hook nicht nutzt
   ([anliegenLaenge.py](../prozess/pruefungen/anliegenregeln/anliegenLaenge.py), Zeile 22);
   eine Bindung per Standardargument, gegen Es 7, steht weiter in
   [erledigteLoeschen.py](../prozess/pruefungen/anliegenregeln/erledigteLoeschen.py), Zeile 29.
5. Der parallele Mutationslauf wartet nach jedem Modul, bis dessen letzter Mutant fertig ist
   ([mutation.py](../prozess/pruefungen/mutationsregeln/mutation.py), Zeilen 171 bis 188).
   Ein Modul mit 3 Mutanten belegt 3 von 8 Kernen, und ein Überlebender, der sich gegen alle
   Tests nachprüft, hält die übrigen Kerne an; im gezielten Lauf über wenige geänderte Zeilen
   ist das der Normalfall. Empfehlung: alle Mutanten aller Module auf einmal einreichen und
   die Ergebnisse je Modul der Reihe nach abholen, ein Zug von wenigen Zeilen. Wie viel das
   bringt, zeigt deine laufende Messung.
6. `testMutantenLaufenParallelJeKernInEigenerKopie`
   ([mutationTest.py](../prozess/pruefungen/mutationsregeln/mutationTest.py), Zeile 247) prüft
   nur, dass zwei Kopien benutzt werden: Ein Lauf, der die Mutanten nacheinander abwechselnd in
   beiden Kopien prüft, bleibt grün. Empfehlung: Beginn und Ende je Test mitschreiben und
   prüfen, dass sich zwei Läufe überschneiden.
7. Klein: Strg+C beendet den Lauf erst, wenn alle eingereichten Mutanten des Moduls fertig
   sind; wird der Prozess beendet, laufen bis zu 8 Testläufe weiter (Zeile 170,
   `ThreadPoolExecutor` ohne `cancel_futures`).

Empfehlung: 1 und 5 mit 6 als Anliegen an den Regelumsetzer, je ein Zug von wenigen Zeilen;
2 bis 4 und 7 beim nächsten Eingriff in die Dateien, sonst bleiben sie liegen, ohne zu stören.

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
