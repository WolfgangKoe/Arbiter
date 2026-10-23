# Retro · Zyklus 7

Dashboard: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten,
`http://127.0.0.1:8765/` öffnen, Strg+C beendet.

Etappe 1 von 10 (Aufstellen) ist erreicht ([Review 7](review.md)); 78 von 108 Kriterien
belegt (Zyklus 6: 78 von 103). Neu am Bildschirm: „Einheit zurücklegen“, feste Adresse.

## Was geklappt hat
Beide Items abgenommen, DoD ohne Rest, alle 30 Mutanten gefangen. Die erste Kritik am Review
fing vor deiner Freigabe ab, dass der Rundgang vier Dateien ausließ (3250).

## Was nicht geklappt hat
1. Kein Zuwachs an belegten Kriterien: Der Zyklus räumte 78 verbotene Kommentare auf (Retro
   6, P5), AUF-17 und AUF-8.4 entfielen, der neue Schnitt brachte 5 Kriterien ohne Test.
2. Seit „Freigabe Retro 6“ 990 Zeilen Prüfcode gegen 715 Produktcode: über der Schwelle.
   Prozesslast 15 von 90 Anliegen, unter einem Drittel.
3. Rollen schrieben per Python oder `sed` über Bash statt mit Edit, in Zyklus 7 rund 15-mal,
   fast jede Rolle, gegen den Auftrag (2040, 2592): Ich 2 wiederholt verletzt, ungesperrt.
4. Der Commit setzte Dateien laufender Rollen kurz zurück, ein Anliegen wurde doppelt
   gelöscht; Hindernisse nehmen fremde Nummern (2460). Die Rückverfolgung nannte einen
   falschen Testpfad (2720).
5. `Wartet auf: Technikphase`, in der Technikphase geschrieben, war sofort dran (3200, 3251).
6. Du musstest raten, was bei dir lag (Plan 7: „Warum liegt das bei mir?“); die Etappen
   wurden zweimal geschnitten, weil Anforderungen erfunden waren (2591). Eine Einstellung,
   dir ohne Probe empfohlen, legte alle Rollen still (2201).

Nicht bestätigt: 3250 und 3251 lagen im Bereich ihres Auftrags.
Ausgelöst im [Backlog](../prozess/backlog.md): „Belegte Kriterien je Etappe“.

## Prozess-Items
Aus Befunden P4 (3) und P5 (4, 5), sonst deine Aufträge. P6 löscht Prüfcode vor Neuem (2).
- P1 Regeln nach deinen Entscheidungen (Organisationsentwickler): Ein Review kritisieren
  Fachkritiker und Organisationsentwickler, als Zeile in Kritik und Fortschritt; Es 8 nennt
  seinen Mechanismus (2360); Höchstmaß der Architektur nach 2570 (3050); `Wartet auf:
  Technikphase 8` nennt den Zyklus. Eine Empfehlung an dich sagt, was danach anders ist,
  auch ob wir dann noch arbeiten und committen, an einer Kopie erprobt (2201). Den
  Backlog-Eintrag streiche ich: Der Stand zählt alle Kriterien. Dazu `doku/` (Etappe 1).
- P2 Ablauf und Regeln in Ordnern (Organisationsentwickler): je Abschnitt eine Datei in
  `prozess/ablauf/` und `prozess/regeln/`, eine Rolle liest nur, was sie braucht (2590);
  die Pfade in den Prüfungen stellt danach der Regelumsetzer um.
- P3 Dein Innen-Ich (Organisationsentwickler): Ich suche, wo du Frust zeigtest, und lege dir
  vor, was dich bewegt und was statt des Erfundenen gilt (2591, 2201). Prämisse wird es erst
  mit deiner Freigabe.
- P4 Schreiben über Bash sperren (Regelumsetzer): Python aus der Eingabe oder mit `-c` und
  `sed -i` sind im Projekt gesperrt, auch in Schleifen, `find -exec` und `xargs`, in `/tmp`
  erlaubt (2040, 2592). Zuerst Verbotsregeln von Claude Code, die laut Doku jeden
  Teilbefehl prüfen; vorher an einer Kopie erprobt, samt Commit.
- P5 Läufe und Anliegenkopf (Regelumsetzer): Der Commit setzt keine fremde Arbeit zurück,
  Hindernisse nehmen Nummern aus dem Bereich, ein neu gefasster Plan öffnet seine Kritik,
  `Wartet auf` mit Zyklus wartet bis dahin, die Rückverfolgung nennt T1 (2460, 2720).
- P6 Reste im Prüfcode (Regelumsetzer): Alte Kopfzeile der Anliegen und ihr Umschreiben
  entfallen, Kommentare im Frontend prüft nur eslint (3301).
- P7 Architekturkarte (Regelumsetzer): Das Dashboard zeigt Schichten und Importe,
  verbotene in Rot (3120).

## Empfehlung
Gib frei. Dann P6 neben P1, danach P2, dann P3 neben P4, P5, P7 nacheinander (Prüfcode).
Am Bildschirm ändert sich nichts.

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [ ] Fachkritiker: Kritik an der Retro
- [ ] Architekt: Kritik an der Retro
- [ ] Organisationsentwickler: Nachkorrektur
- [ ] Stakeholder: Freigabe Retro 7
- [ ] Organisationsentwickler: P1
- [ ] Organisationsentwickler: P2
- [ ] Organisationsentwickler: P3
- [ ] Regelumsetzer: P4
- [ ] Regelumsetzer: P5
- [ ] Regelumsetzer: P6
- [ ] Regelumsetzer: P7
- [ ] Koordinator: nach dev gepusht

## Freigabe
Freigabe: offen
Kommentar: .
