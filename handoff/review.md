# Review · Zyklus 7

Start der App: `.venv/bin/arbiter` aus der Wurzel ([Web, W5](../technik/architektur/web.md#aufbau)),
dann `http://127.0.0.1:8040/` im Browser öffnen.

## Am Bildschirm prüfen
Mit Maus oder Finger stellt ihr beide Armeen auf: auswählen, setzen, verschieben,
zurücklegen, beenden.
1. Start: Arbiter nennt `http://127.0.0.1:8040/`. Ein zweiter Start sagt „Die Adresse … ist
   belegt. Läuft Arbiter schon?“ und startet nicht.
2. „Necron Warriors“ anklicken, in die rote Zone klicken: *Formation*, daneben „Einheit
   zurücklegen“ und „Aufstellen der Einheit beenden“.
3. „Einheit zurücklegen“: *Karte* leer, der Knopf ist fort, die Necron Warriors bleiben
   *ausgewählt*; ein Klick in die Zone stellt sie neu auf.
4. Einen Kreis anklicken, weit wegziehen, beenden: ‚keine Kohärenz‘, nichts zum Übergehen.
5. „Einheit zurücklegen“, neu klicken, beenden: Spieler 1 ist *an der Reihe*.

Ich bin 1 bis 5 am laufenden Arbiter im Browser durchgegangen (auf `--port`, Port 8040 belegt
`festeAdresseTest`); jedes Bild wie beschrieben.

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 655 grün; Abdeckung über 95 %.
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 771 grün, mit ruff, eslint,
   stylelint und der Kommentarregel; SonarLint: keine Funde. Kein Kommentar, kein TODO
   unter `technik/`.
3. **Erfüllt.** Beide Items gelöscht;
   [AUF-23](../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md) beschreibt das
   Gebaute, AUF-17 und AUF-8.4 sind samt Tests fort.
4. **Erfüllt.** Der Fachkritiker hat beide Items abgenommen.

Oberfläche: **Erfüllt.** Bildschirmtests grün, Mockups auf-23 gelöscht.
Mutation: **Erfüllt.** Alle 30 Mutanten der seit „Freigabe Plan 7“ geänderten Domänenzeilen
gefangen.

## Code
`/code-review`, Wiederverwendung, Vereinfachung, Effizienz, Flughöhe seit „Freigabe Plan 7“:
kein Befund. „zurück“ und Loslassen auf die *Armeeliste* sind ohne Rest fort, die *Auswahl*
kennt nur *Einheit* und *Ebene*. Anliegen 3140 (Vertrag V3) ist erledigt.

## Empfehlung
Die DoD ist erfüllt, nichts hält auf: Gib Review 7 frei. Die offenen Anliegen warten auf
spätere Phasen ([Moderation](moderation.md)).

## Rundgang Prüfcode
Seit „Freigabe Review 6“ rund 1.800 Zeilen in `prozess/pruefungen/`: gezielte Mutation
(`mutationsregeln/`), Kommentarregel ab Technikphase 7 (`formregeln/kommentare.py`,
`technikphase.py`), Fortschritt im Dashboard (`rollenregeln/dashboardFortschritt.py`,
`standregeln/zeilenZug.py`), `anliegenregeln/freieNummer.py`.
1. Aus Review 6 behoben: „DoD über das Inkrement“ hakt nur der Befehl ab
   (`standregeln/fortschritt.py:100`); ein Mutant startet nur die Tests seiner Zeile.
2. `standregeln/hindernis.py` (`nächsteNummer`) und `zeilenZug.py` nehmen die höchste Nummer
   plus eins statt `freieNummer`; laufen zwei Rollen, belegt ein Hindernis womöglich eine
   Nummer der anderen (2460).
3. `mutationsregeln/ergebnisse.py`: Ein gleichwertiger Mutant gilt je Quelltext der Zeile;
   zwei gleiche Zeilen im Modul deckt eine Begründung.

## Nächstes Vorgehen
- **Produktziel:** Etappe 1 von 10 ist erreicht
  ([Aufstellen](../domaene/etappen/01-aufstellen.md)). Am meisten fehlt die Partie selbst:
  Schlachtrunden, Phasen, Bewegen.
- **Etappenziel:** Etappe 1 ist gebaut und abgenommen; ihre Randfälle warten auf Etappe 7.
  Etappe 2 ([Bewegen](../domaene/etappen/02-bewegen.md)) schätze ich auf drei bis vier Zyklen.
- **Zyklusziel:** Plan 8: Nach dem Aufstellen wählt ihr, wer den ersten Zug hat; Arbiter zeigt
  Schlachtrunde, Spieler am Zug und Phase, ihr beendet die leeren Phasen, und in der
  Bewegungsphase macht eine *Einheit* einen Normal Move, gesperrt über M und über fremde
  *Bases*. Noch nicht: Advance, gemeinsam übergehen mit *Protokoll*, Loslassen neben der
  *Karte*. Vorher: die Architektur umordnen, ohne sichtbare Änderung
  ([3051](anliegen/3051-architekturUmordnenInPlan8.md)).

## Fortschritt
- [ ] Anforderungsautor: Happy Paths zum Zyklusziel
- [ ] UX: Mockups, bei einer Oberfläche
- [ ] Fachkritiker: Kritik an Anforderungen und Mockups
- [ ] Planer: Plan geschrieben
- [ ] Fachkritiker: Kritik am Plan
- [ ] Architekt: Kritik am Plan
- [ ] Stakeholder: Freigabe Plan 8

## Freigabe
Freigabe: offen
Kommentar: .
