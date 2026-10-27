# Review · Zyklus 7

Start der App: `.venv/bin/arbiter` aus der Wurzel ([Web, W5](../technik/architektur/web.md#aufbau)),
dann `http://127.0.0.1:8040/` im Browser öffnen.

## Am Bildschirm prüfen
Mit Maus oder Finger stellt ihr beide Armeen auf: auswählen, setzen, verschieben,
zurücklegen, beenden.
1. Start: Arbiter nennt `http://127.0.0.1:8040/`. Ein zweiter Start sagt „Die Adresse … ist
   belegt. Läuft Arbiter schon?“ und startet nicht.
2. „Necron Warriors“ anklicken, in die rote Zone klicken: *Formation*, daneben „Einheit
   zurücklegen“ und „Aufstellen der Einheit beenden“; ein Knopf „zurück“ fehlt.
3. Ein *Modell* auf eine *Armeeliste* ziehen, loslassen: Es springt zurück, ohne *Grund*.
4. „Einheit zurücklegen“: *Karte* leer, der Knopf ist fort, die Necron Warriors bleiben
   *ausgewählt*; ein Klick in die Zone stellt sie neu auf.
5. Ein *Modell* weit wegziehen, beenden: ‚keine Kohärenz‘, nichts zum Übergehen.
6. „Einheit zurücklegen“, neu klicken, beenden: Spieler 1 ist *an der Reihe*.

Am laufenden Arbiter gesehen: 2 bis 6 auf anderem Port, da 8040 belegt war; von 1 der
zweite Start. Dass der erste 8040 nennt, zeigt nur
[festeAdresseTest](../technik/tests/akzeptanz/querschnitt/festeAdresseTest.py).

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 655 grün; Abdeckung über 95 %.
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 771 grün; SonarLint ohne Fund.
3. **Erfüllt.** Items gelöscht,
   [AUF-23](../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md) beschreibt das
   Gebaute, AUF-17 und AUF-8.4 sind fort.
4. **Erfüllt.** Der Fachkritiker hat beide Items abgenommen.

Oberfläche: **Erfüllt.** Bildschirmtests grün, Mockups auf-23 gelöscht.
Mutation: **Erfüllt.** Alle 30 Mutanten der geänderten Domänenzeilen gefangen.

## Code
`/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe seit „Freigabe Plan 7“:
kein Befund.

## Empfehlung
Die DoD ist erfüllt, nichts hält auf: Gib Review 7 frei, und gib Rundgang 1 und 2 dem
Regelumsetzer. Die offenen Anliegen warten auf spätere Phasen ([Moderation](moderation.md)).

## Rundgang Prüfcode
Seit „Freigabe Review 6“ rund 1.800 Zeilen in [prozess/pruefungen](../prozess/pruefungen):
Mutation nur geänderter Zeilen, Kommentarregel, Anliegen mit Kopf als Felder, Anliegenboard nach
Phasen, Fortschritt im Dashboard, freie Nummern.
1. `lesen/anliegenKopf.py:24, 111` liest die alte Kopfzeile,
   `anliegenregeln/kopfUmschreiben.py` schreibt sie um; kein Anliegen trägt sie mehr, auch
   nicht in „Freigabe Plan 7“. Rest, kann weg, ebenso `die ` vor der Phase
   (`anliegenKopf.py:107`, `rollenregeln/dashboardAnliegen.py:13`).
2. Kommentare im Frontend prüfen `frontendregeln/eslintKommentare.mjs` und
   `formregeln/kommentare.py:76` doppelt; eine Regel genügt.
3. `standregeln/hindernis.py:60` nimmt die höchste Nummer plus eins statt `freieNummer`;
   bei zwei Rollen womöglich eine fremde (2460).

## Nächstes Vorgehen
- **Produktziel:** Etappe 1 von 10 (Aufstellen) ist erreicht, ihre Datei löscht der Planer
  (Anliegen 3300). Am meisten fehlt die Partie selbst.
- **Etappenziel:** Ihre Randfälle, 13 AUF-Kriterien ohne Test, warten nach [Plan 7](plan.md)
  auf Etappe 7. [Etappe 2](../domaene/etappen/02-bewegen.md) nennt 14 Teile; Plan 8 nimmt 8,
  die übrigen 6 schätze ich auf zwei bis drei Zyklen.
- **Zyklusziel:** Plan 8: Nach dem Aufstellen wählt ihr, wer den ersten Zug hat; Arbiter zeigt
  Schlachtrunde, Spieler am Zug und Phase, ihr beendet die leeren Phasen, nach der fünften
  Schlachtrunde endet die Schlacht. In der Bewegungsphase macht eine *Einheit* einen Normal
  Move, gesperrt über M, über fremde *Bases* und am Ende ohne *Kohärenz*. Noch nicht: Advance,
  Zurücksetzen, über die Kante, Engagement Range, gemeinsam übergehen mit *Protokoll*, neue
  Modelle, Loslassen neben der *Karte*. Vorher: die Architektur umordnen
  (Anliegen 3051).

## Fortschritt
- [x] Anforderungsautor: Happy Paths zum Zyklusziel
- [x] UX: Mockups, bei einer Oberfläche
- [x] Fachkritiker: Kritik an Anforderungen und Mockups
  Hindernis: Fachkritiker → Anforderungsautor: BEW-1.1 lässt Aufstellregeln greifen (AUF-7.2 sperrt jedes Ziehen), Anzeige beim Ziehen und Ebene ungeklärt (Anliegen 4260); beseitigt: Commit „Anforderungen zu Plan 8 nach Kritik nachgebessert“
  Hindernis: Fachkritiker → Ux: Mockups zu Plan 8: Phase beenden fehlt in der Bewegungsphase, Armeelisten nach der Aufstellung gefüllt, Ende der Schlacht ohne Bild (Anliegen 4262); beseitigt: Commit „Mockups zu Plan 8: erster Zug, Schlachtrunden, Normal Move, Ende der Schlacht“
  Hindernis: Fachkritiker → Anforderungsautor: BEW-1.1: Block im Normal Move sperrt sich nach QUE-1.2 an den eigenen Modellen, AUF-24.2 gilt nicht mehr (Anliegen 4263); beseitigt: Commit „Anforderungen zu Plan 8 nach Kritik nachgebessert“
- [x] Planer: Plan geschrieben
- [x] Fachkritiker: Kritik am Plan
  Hindernis: Fachkritiker → Planer: Plan 8 und Items nennen Normal Move und M statt deiner Antwort zu 4280 F1, Schritt 3 ohne Bewegung der Einheit beenden, Mockups nicht verlinkt (Anliegen 4400); beseitigt: Commit „Plan 8 nach Kritik nachgebessert, Distanz je Bewegungsphase“
  Hindernis: Fachkritiker → Ux: Mockup bew-2 zeigt weiter als M statt B nach 4280 F1 (Anliegen 4401)
  Hindernis: Fachkritiker → Anforderungsautor: Distanz läuft über Phase beenden hinaus, weiter als M sperrt in einer späteren Schlachtrunde zu Unrecht (Anliegen 4402); beseitigt: Commit „Kritik am Plan 8 und Antworten zu 4280 umgesetzt“
- [x] Architekt: Kritik am Plan
  Hindernis: Architekt → Planer: Item architekturUmordnen zählt den Vertrag in die 24.000 Zeichen, gegen 2570 F2 C und die Höchstmaße (Anliegen 4600); beseitigt: Commit „Kritik des Architekten am Plan 8, 4280 geschlossen“
  Hindernis: Architekt → Anforderungsautor: Distanz zählt die Strecke ab der Stelle zu Beginn der Bewegungsphase nicht, weiter als B sperrt beim ersten Ziehen nach dem Wortlaut nie (Anliegen 4601); beseitigt: Commit „Kritik des Architekten am Plan 8, 4280 geschlossen“
- [x] Stakeholder: Freigabe Plan 8

## Freigabe
Freigabe: ja
Kommentar: Ich habe alles soweit geprüft. Wir können Etappe 1 somit auch abschließen und die Datei löschen. Auch alles für die Prozessphase habe ich soweit adressiert. Bitte Retro.md vorbereiten
Stellungnahme: Etappe 1 abschließen geht an den Planer
(Anliegen 3300), im Produktziel steht sie ohne Link
auf die Datei. Rundgang 1 und 2 gehen an den Regelumsetzer
(Anliegen 3301), Rundgang 3 steht in
Anliegen 2460. Die Retro schreibt der
Organisationsentwickler gerade.
