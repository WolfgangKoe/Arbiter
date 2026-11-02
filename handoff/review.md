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
9. Den *Griff* der unteren *Leiste* (▼ am unteren Rand) klicken: Sie fährt ein, nur der
   *Griff* ▲ bleibt. Noch ein Klick: Sie fährt aus und zeigt wieder das *Protokoll*. Links und
   rechts geht es ebenso.
10. Ein Klick auf die leere *Karte*, dann den untersten Boy 5″ nach rechts ziehen, weg von
   den Boyz, und „Phase beenden“: Arbiter nennt ‚keine Kohärenz‘, bietet „gemeinsam
   übergehen“ nicht an, die *Bewegungsphase* bleibt.

Am laufenden Arbiter mit der Maus gesehen: 2 bis 10 in Folge; die Aufstellung habe ich dafür
vorbereitet statt geklickt. Nur Tests zeigen: Anhalten an der *Spielfeldkante* und 1″ vor
einer gegnerischen *Base* ([anhaltenVorDerGrenzeTest](../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py)),
*Modelle* des Gegners lassen sich nicht ziehen ([fremdeModelleTest](../technik/tests/akzeptanz/phasen/bewegung/fremdeModelleTest.py)),
Klick auf eine *aufgestellte* *Einheit* beim Aufstellen ([aufgestellteEinheitAuswaehlenTest](../technik/tests/akzeptanz/phasen/aufstellen/aufgestellteEinheitAuswaehlenTest.py)),
*Grenzkreise* nach erneuter *Auswahl* ([grenzkreiseNachErneuterAuswahlTest](../technik/tests/akzeptanz/phasen/bewegung/grenzkreiseNachErneuterAuswahlTest.py)).
Ziehst du den Warboss nach links zur Kante, springt er zurück: Die Boyz stehen im Weg,
‚über eine Base‘.

Du bist den Klickpfad durchgegangen und einverstanden; Schritte 9 und 10 sind danach
dazugekommen (Anliegen 8950), sieh sie dir bitte noch an.

## DoD
1. **Erfüllt.** Alle Tests in `technik/tests` grün, Abdeckung über 95 % (Prüfung `abdeckung`).
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 937 grün; SonarLint ohne Fund. Die
   Meldung S1172 am Parameter `vorrückwurf`, die der Implementierer in der IDE sah, gibt es
   nach dem Commit „grenzkreise: Kritik am Code zu 8640, Item gelöscht“ nicht: Dieselbe
   SonarLint-Version meldet in einer Kopie einen wirklich unbenutzten Parameter derselben
   Funktion, `vorrückwurf` nicht. Wohl ein veralteter Stand im Editor. Seither hat sich nur
   der Mutationslauf geändert, Commit „Mutationslauf parallel auf allen Kernen (Anliegen
   8122)“: Danach sind seine 18 Tests, die Prüfungen zu Benennung, Kommentaren und
   Komplexität, ruff und SonarLint grün.
3. **Erfüllt.** Alle vier Items gelöscht; die Kriterien beschreiben das Gebaute.
4. **Erfüllt.** Der Fachkritiker hat alle vier Items abgenommen.

Oberfläche: **Erfüllt.** Bildschirmtests grün; die acht Mockups des Gebauten sind gelöscht,
unter `domaene/mockups/` liegen nur noch die der offenen Items. Anliegen 8760 ist erledigt;
`erledigteLoeschen.py` hat es nach dem Commit gelöscht, wie vorgesehen.
Mutation: **nicht erfüllt.** Der gezielte Lauf über die geänderten Zeilen fängt 93 % von 190
Mutanten, die Schwelle ist 95 %; der volle 96 % von 628
(Anliegen 8970). Am Bildschirm ändert das
nichts. Von den 21 Überlebenden sind zwölf gleichwertig, Begründung trägt der
Organisationsentwickler ein (Anliegen 8973);
danach 98 %. Acht Tests fehlen, Technikphase 10 ([8971](anliegen/8971-mutationslueckenMessenUndKatalog.md)),
und ein Kriterium, Domänenphase 10 (Anliegen 8972).

## Code
`/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe seit „Freigabe Plan 9“:
nichts hält auf. Kein `noqa`, kein TODO im Produkt. Warten auf Technikphase 10: Die Suche
nach der *Einheit* eines *Modells* steht dreimal da, ein Test zu zwei *Einheiten*, von denen
nur eine *vorgerückt* ist, fehlt (Anliegen 8740); zwei Tests zur *Auswahl* prüfen zu wenig
(Anliegen 8720).

## Empfehlung
Gib Review 9 frei, sobald die Mutation die Schwelle hält: Der Klickpfad zeigt, was Plan 9
versprochen hat, Schritte 1 bis 5 des Happy Path. Beantworte vor der Domänenphase 10 die
Fragen in Anliegen 8840, sie ändern den Umfang von Plan 10 (Nächstes Vorgehen). Die übrigen
Anliegen warten auf spätere Phasen ([Moderation](moderation.md)).

## Rundgang Prüfcode
Seit „Freigabe Review 8“ 96 Dateien in [prozess/pruefungen](../prozess/pruefungen),
[.claude/settings.json](../.claude/settings.json) und [eslint.config.mjs](../eslint.config.mjs),
1.318 Zeilen neu, 713 fort. Gut 60 Dateien
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
  Ein Hook mit leerer Eingabe gilt als Aufruf ohne Angaben und lässt durch
  ([hookProtokoll.py](../prozess/pruefungen/gemeinsam/hookProtokoll.py), Zeile 56); vorher
  brach er mit einem Fehler ab, der ebenso nicht sperrte. Claude Code schickt nie leer.
- ESLint verbietet Kommentare hinter Code ([eslint.config.mjs](../eslint.config.mjs),
  Zeile 32, `no-inline-comments`), passend zu Es 8.
- Elf Mutanten zählen als gleichwertig nicht gegen die Schwelle
  ([gleichwertig.json](../prozess/pruefungen/mutationsregeln/gleichwertig.json), Anliegen
  6994): vier in `ausgangslage.py`, drei in `spielobjekte.py`, zwei in `setzenPerKlick.py`,
  je einer in `web/darstellung.py` und `web/server.py`. Sechs davon, je drei in `spielobjekte.py` und `ausgangslage.py`, nehmen `frozen` oder
  `eq=False` aus `@dataclass`, weil kein Code die Felder neu setzt oder die Objekte
  vergleicht; die übrigen fünf begründen je einen Wert, der nicht wirken kann. Die Gründe
  halte ich für stichhaltig.

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
8. Ein gleichwertiger Mutant gilt für jede Zeile mit demselben Text in derselben Datei
   ([gleichwertig.json](../prozess/pruefungen/mutationsregeln/gleichwertig.json)). Eine neue
   Klasse mit `@dataclass(frozen=True, eq=False)` in `spielobjekte.py` ist damit ungeprüft
   ausgenommen, auch wenn Code sie vergleicht; bei `Modell` zählt so schon ein gefangener
   Mutant nicht. Empfehlung: den Eintrag an die Klasse binden, etwa mit ihrem Namen.

Empfehlung: 1, 5 mit 6 und 8 als Anliegen an den Regelumsetzer, je ein Zug von wenigen
Zeilen; 2 bis 4 und 7 beim nächsten Eingriff in die Dateien, sonst bleiben sie liegen, ohne
zu stören.

## Nächstes Vorgehen
- **Produktziel:** Etappe 1 von 10 ist erreicht (Commit „Freigabe Etappe 1“), Etappe 2 läuft.
  Am meisten fehlt die Partie nach der *Bewegungsphase*: Schießen, Angreifen, Nahkampf, Moral.
- **Etappenziel:** Zu [Etappe 2](../domaene/etappen/02-bewegen.md) fehlt nach deiner Antwort
  A in Anliegen 8880: Zurücksetzen, Loslassen neben der *Karte* (mit 8480),
  *Nahkampfreichweite* auf der ganzen Strecke und kein *Vorrücken* aus ihr (Anliegen 6986),
  „Phase beenden“ nur im Zug, Ork-Psioniker und Canoptek-Spinne, die ruhige *Karte*; der
  Stand nennt 57 von 63 Kriterien der Etappe belegt. Ein Zyklus, zwei, wenn die ruhige *Karte*
  hängt. Anliegen 8840 wartet auf deine Antworten: Mit F1 kann in der Etappe Anhalten vor
  fremden *Bases* die *Sperre* ‚über eine Base‘ ersetzen, F2 entscheidet, ob sich ein
  Anhalten übergehen lässt.
- **Zyklusziel:** Plan 10 schließt Etappe 2 ab. Danach setzt ihr eine gezogene *Einheit*
  zurück, lasst ein *Modell* neben der *Karte* los, durch die *Nahkampfreichweite* eines
  Gegners zieht kein *Modell* mehr hindurch, eine *Einheit* in ihr rückt nicht vor,
  „Phase beenden“ gibt es nur für den *Spieler* am Zug, Ork-Psioniker und Canoptek-Spinne
  stehen in den Armeen, zuletzt bleibt die *Karte* ruhig. Noch nicht: sehen, welche
  *Einheit* schon gezogen hat, und ein Anhalten übergehen (Etappe 3). Reihenfolge nach der
  Klärung in 8880, von dir mit F2 A bestätigt: erst diese Teile, dann das Aufräumen aus 22
  Anliegen der Technikphase 10 und 7800; braucht ein Teil eines davon vorher, zieht der
  Planer es vor und nennt es.

## Fortschritt
- [x] Anforderungsautor: Happy Paths zum Zyklusziel
- [x] UX: Mockups, bei einer Oberfläche
- [x] Fachkritiker: Kritik an Anforderungen und Mockups
- [x] Planer: Plan geschrieben
- [x] Fachkritiker: Kritik am Plan
  Hindernis: Fachkritiker → Planer: Schritte 2 und 6 und die Empfehlung beschreiben anderes, als Arbiter zeigen wird (Anliegen 10300); beseitigt: Commit „Plan 10: Fixtures vor den Daten der dritten Einheit, 10280 erledigt“
  Hindernis: Fachkritiker → Anforderungsautor: Das Datenblatt der Canoptek-Spinne ist erst für Zyklus 11 vorgemerkt, Item fliegen liegt in Zyklus 10 (Anliegen 10301); beseitigt: Commit „Kritik an Plan 10 und Nachbesserung, Ork-Psioniker als MIV-2“
  Hindernis: Fachkritiker → Anforderungsautor: Wie „Einheit zurücksetzen“ bedient wird, weicht von ArbiterMap ab, ohne dass du es entschieden hast; der Anforderungsautor fragt dich. (Anliegen 10400)
- [x] Architekt: Kritik am Plan
  Hindernis: Architekt → Planer: Der Plan sagt, hängt Item 3, rücke nur dieses nach Zyklus 11; die Canoptek-Spinne aus Item 4 rückt dann mit. (Anliegen 10420); beseitigt: Commit „Plan 10: Item 4 rückt mit Item 3, Frage 10480 zum Zurücksetzen“
- [ ] Stakeholder: Freigabe Plan 10

## Freigabe
Freigabe: ja
Kommentar:
