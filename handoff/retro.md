# Retro · Zyklus 7

Dashboard: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten,
`http://127.0.0.1:8765/` öffnen, Strg+C beendet.

Etappe 1 von 10 (Aufstellen) ist erreicht ([Review 7](review.md)); 78 von 108 Kriterien
belegt (Zyklus 6: 78 von 103). Neu am Bildschirm: „Einheit zurücklegen“, feste Adresse.

## Was geklappt hat
Beide Items abgenommen, DoD ohne Rest, alle 30 Mutanten gefangen. Die Kritik am Review fand
vor deiner Freigabe vier Dateien, die der Rundgang ausließ (3250).

## Was nicht geklappt hat
1. Kein Zuwachs: 8 Kriterien bekamen ihren Test, 8 belegte fasste der neue Schnitt der
   Etappen neu (das zählt als neu) oder strich sie; 11 neue warten auf ihren Test. Ursache:
   Anforderungen waren erfunden, daher der Schnitt (2591).
2. 990 Zeilen Prüfcode gegen 715 Produktcode: über der Schwelle; Prozesslast 15 von 90
   Anliegen: darunter.
3. Rollen schrieben rund 15-mal per Python oder `sed` über Bash (2040, 2592): Ich 2
   wiederholt verletzt, ungesperrt.
4. Der Commit setzte Arbeit laufender Rollen zurück, Hindernisse nehmen fremde Nummern
   (2460), die Rückverfolgung nannte einen falschen Testpfad (2720).
5. `Wartet auf: Technikphase`, in der Technikphase geschrieben, war sofort dran (3200, 3251).
6. Du musstest raten, was bei dir lag (Plan 7: „Warum liegt das bei mir?“). Eine
   Einstellung, dir ohne Probe empfohlen, legte alle Rollen still (2201).

Nicht bestätigt: 3250 und 3251 lagen im Auftrag.
Ausgelöst im [Backlog](../prozess/backlog.md): „Belegte Kriterien je Etappe“, Frage dazu:
Anliegen 3550.

## Prozess-Items
P3 gilt der Ursache (1), P4 der verletzten Prämisse (3), P5 deinem Auftrag 2460 und dem
Testpfad der neuen (2720), P6 löscht Prüfcode vor Neuem (2); sonst deine Aufträge.
- P1 Regeln nach deinen Entscheidungen (Organisationsentwickler): Fachkritiker und
  Organisationsentwickler kritisieren ein Review (Kritik, Fortschritt); Es 8 nennt seinen
  Mechanismus (2360); Höchstmaß der Architektur nach 2570 (3050); `Wartet auf: Technikphase
  8` nennt den Zyklus; eine Empfehlung an dich ist an einer Kopie erprobt, samt Arbeiten und
  Commit danach (2201); ohne Zuwachs bleiben deine Aufträge und eine verletzte Prämisse
  als Item erlaubt (3451). Dazu `doku/`.
- P2 Ablauf und Regeln in Ordnern (Organisationsentwickler): je Abschnitt eine Datei in
  `prozess/ablauf/` und `prozess/regeln/`, eine Rolle liest nur, was sie braucht (2590).
- P3 Dein Innen-Ich (Organisationsentwickler): Ich suche, wo du Frust zeigtest, und lege dir
  vor, was dich bewegt, als Prämisse erst mit deiner Freigabe (2591, 2201). Was statt des
  Erfundenen gilt, steht in der [Domäne](../domaene/CLAUDE.md) (Quellen); ich zeige, wo
  Zyklus 7 davon abwich.
- P4 Schreiben über Bash sperren (Regelumsetzer): Claude Code sperrt `sed -i` und
  Python-Schnipsel auch in Schleifen und `/tmp`; ein Skript in `/tmp` mit Pfaden als Argument
  bleibt erlaubt. Umwege über `xargs` und `find` sperrt die Schreibgrenze, `bash -c` bleibt
  Lücke (2040, 2592, 3450). An einer Kopie erprobt, samt Commit.
- P5 Läufe und Anliegenkopf (Regelumsetzer): Der Commit setzt keine fremde Arbeit zurück,
  Hindernisse nehmen Nummern aus dem Bereich, ein neu gefasster Plan öffnet seine Kritik,
  `Wartet auf` mit Zyklus wartet bis dahin, die Rückverfolgung nennt T1 (2460, 2720).
- P6 Reste im Prüfcode (Regelumsetzer): Alte Kopfzeile der Anliegen und ihr Umschreiben
  entfallen, Kommentare im Frontend prüft nur eslint (3301).
- P7 Architekturkarte (Regelumsetzer): Das Dashboard zeigt Schichten und Importe,
  verbotene in Rot (3120).
- P8 Prüfungen nach P2 (Regelumsetzer): Seine Regeln trägt er auch in den neuen Dateien in
  jeder Phase ein; Commit mit P2 und den Links des Architekten (3450).
- P9 Deine Absicht (Organisationsentwickler): vierte Prämisse, zuerst geladen;
  Optionen an dich nennen ihre Quelle. Deine Wahl: vor Plan 8 (3820).

## Empfehlung
Am Bildschirm ändert sich nichts.

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [x] Fachkritiker: Kritik an der Retro
- [x] Architekt: Kritik an der Retro
- [x] Organisationsentwickler: Nachkorrektur
- [x] Stakeholder: Freigabe Retro 7
- [x] Organisationsentwickler: P1
- [x] Organisationsentwickler: P2
- [x] Organisationsentwickler: P3
- [x] Regelumsetzer: P4
- [x] Regelumsetzer: P5
- [x] Regelumsetzer: P6
- [x] Regelumsetzer: P7
- [x] Regelumsetzer: P8
- [ ] Organisationsentwickler: P9
- [x] Koordinator: nach dev gepusht

## Freigabe
Freigabe: ja
Kommentar: .
