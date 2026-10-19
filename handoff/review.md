# Review · Zyklus 5

Start der App: `.venv/bin/arbiter` aus der Wurzel ([Web, W5](../technik/architektur/web.md#aufbau)),
die genannte Adresse im Browser öffnen.

## Am Bildschirm prüfen
Mit Maus oder Finger: *Einheiten* aus der *Ablage* auf die *Karte* ziehen, *Modelle* verschieben
und zurücklegen, „zurück“, „Aufstellen der Einheit beenden“, bis alle vier stehen.
1. Start: oben „Spieler 2 · an der Reihe“, links blaue, rechts rote *Aufstellungszone*.
   „Boyz“ auf die Karte oder „Overlord“ auf die linke Ablage ziehen: „nicht wählbar“, springt zurück.
2. „Necron Warriors“ rechts auf die rote Zone ziehen: zehn Kreise in Reihen, mittig am Zeiger;
   am Rand rücken sie hinein. Karte zeigt „in Aufstellung“.
3. Einen Kreis auf die Ablage rechts ziehen: er verschwindet, Zahl 1. „Aufstellen der Einheit
   beenden“: „Modelle fehlen“. Die Karte erneut ziehen: genau ein Kreis kommt dazu.
4. Einen Kreis auf einen anderen ziehen: er bleibt blass und gestrichelt stehen, darunter
   „Base überdeckt“, Knopf „zurück“; neu laden ändert nichts; „zurück“ stellt ihn an seinen Platz.
5. Einen Kreis über 2″ weg ziehen, beenden: „keine Kohärenz“. Zurückziehen, beenden:
   Spieler 1 ist an der Reihe.

Von Hand nur die Anfragen hinter 1 bis 4 am laufenden Arbiter; das Ziehen im Browser
prüfen die Bildschirmtests gegen den echten Server, mit Maus und Finger.

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 424 grün; Abdeckung über 95 % (`abdeckung.py` grün).
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 606 grün; SonarLint: keine Funde.
3. **Erfüllt.** Items gelöscht (Fortschritt im [Plan](plan.md)), Anforderungen nachgezogen.
4. **Erfüllt.** Der Fachkritiker hat alle drei Items abgenommen, kein Anliegen offen.

Oberfläche: **Nicht erfüllt.** Bildschirmtests grün, aber fünf Mockups liegen noch: [620](anliegen/620-mockupsNachDemEinbauLoeschen.md) (UX).

## Rufen die Tests den gebauten Code?
Ja. Sie rufen `Aufstellung` direkt, den Dienst über Flask oder die Seite im Browser gegen den
gestarteten Server. Probe: 18 Fehler je einzeln eingebaut (Kohärenz, Formation, „zurück“, Sperren, Seite); 17 machten
Tests rot. Lücken: Zugschwelle 0 bleibt grün, [622](anliegen/622-zugschwelleUngeprueft.md);
AUF-14.1 fiel nur über einen anderen Test, [621](anliegen/621-restDerEinheitOhneGesperrte.md) (beide Testautor).

## Code
`/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe: kein weiterer Befund.
Die Domäne kennt Flask nicht, die Gründe kommen aus Tabellen.

## Empfehlung
Freigeben; 620 bis 622 laufen nach.

## Rundgang Prüfcode
Seit Commit „Freigabe Retro 4“: 2.681 Zeilen neu in `prozess/pruefungen/`, fast die Hälfte für
das Dashboard (`rollenregeln/dashboard*.py`, `zuegeUebernehmen.py`), dazu `fortschritt.py`,
`bashSchreiben.py`, `entfernen.py`, `spiegel.py`, `gruendeTabellen.py`.
1. Mehr Prüfcode als Produktcode: 1.035 Zeilen neu in `technik/arbiter` und `frontend`, 1.254 allein im Dashboard.
2. `bashSchreiben.py` sperrt auch Lesen und /tmp: `python3 -c`, `rm -rf /tmp/…`, Write in /tmp
   ([Ich 2](../prozess/praemissen/ich.md) erlaubt /tmp).

## Nächstes Vorgehen
- **Produktziel:** keine der 7 Etappen erreicht; am meisten fehlt das Bewegen (Etappe 2).
- **Etappenziel:** Es fehlen „gemeinsam übergehen“ mit *Protokoll*, *Gewinner* und Zone am
  Bildschirm, *Leisten* („Danach“ im Plan); die Kriterien haben noch keinen Test. Ein Zyklus.
- **Zyklusziel:** Plan 6: Nach dem Start wählt ihr *Gewinner* und Zone selbst; eine *Sperre*
  übergeht ihr gemeinsam, das *Protokoll* zeigt es. Damit ist Etappe 1 erreicht. Vorher: 620 bis 622.

## Fortschritt
- [x] Anforderungsautor: Happy Paths zum Zyklusziel
- [x] UX: Mockups, bei einer Oberfläche
- [x] Fachkritiker: Kritik an Anforderungen und Mockups
- [x] Planer: Plan geschrieben
- [x] Fachkritiker: Kritik am Plan
- [x] Architekt: Kritik am Plan
- [ ] Stakeholder: Freigabe Plan 6

## Freigabe
Freigabe: ja
Kommentar: .
