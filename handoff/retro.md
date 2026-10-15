# Retro · Zyklus 5

Dashboard öffnen: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten, im
Browser `http://127.0.0.1:8765/` öffnen, beenden mit Strg+C.

Etappe 1 · Aufstellen, Plan 5 mit drei Items. Grundlage: [Review 5](review.md), git seit
Commit „Freigabe Retro 4“, Anliegen, Belegung je Lauf.

## Fortschritt des Produkts
Keine der sieben Etappen ist erreicht. 74 von 94 Kriterien belegt ein grüner Akzeptanztest
(Retro 4 ohne Zählung). Neu am Bildschirm: *Einheiten* auf die *Karte* ziehen, *Modelle*
verschieben, *gesperrt* stehen mit *Grund*, „zurück“, „Aufstellen der Einheit beenden“.
Für Etappe 1 fehlen „gemeinsam übergehen“ mit *Protokoll*, *Gewinner* und Zone, *Leisten*
und, nach deiner Antwort in 683, das Aufstellen per Klick wie ArbiterMap.

## Befunde
1. Eine Bedienung fehlte, bis du sie am Bildschirm getestet hast (Anliegen 685, 683): Kein
   Schritt verglich die Gesten mit ArbiterMap. Die Technikphase baute Ziehen aus der *Ablage*,
   das jetzt entfällt.
2. Mehr Prüfcode als Produktcode: 2.668 neue Zeilen in `prozess/pruefungen/` gegen 1.035 in
   `technik/arbiter` und `technik/frontend` (Review 5, Rundgang).
3. 114 Commits, 8 mit Produktcode, 14 nur Kritik; jeder wartete 7 bis 8 Minuten auf alle
   Prüfungen (Anliegen 600).
4. 89 neue Anliegen in fünf Tagen; 20 an Regelumsetzer oder mich, 22 % (Retro 4: 16 %,
   Schwelle ein Drittel). Viele betrafen Feinschliff, der nichts aufhielt (Anliegen 630).
5. Der Stand nannte Regelumsetzer und mich in jeder Phase als dran; wir liefen neben dem
   Produkt (630). Ein wartendes Anliegen kann man nicht kennzeichnen: Die Prüfung lehnt
   „wartet auf“ ab, das der Ablauf verlangt (Hinweis des Koordinators, Anliegen 686).
6. Belegung: 16 von 175 Läufen über 120.000 Token, 2 über 150.000 (Retro 4: 2 und 0).
   Die Ursache kenne ich nicht; dieser Lauf kam durch Sperren der Schreibgrenze dorthin (650).
7. Die Probe des Reviewers fand zwei Lücken in den Tests (621, 622).

## Geändert
- Nach 630: Ein Anliegen nur, wenn etwas aufhält, Feinschliff in den Backlog
  ([Ich 3](../prozess/praemissen/ich.md), Reviewer, Fachkritiker, Architekt); Prozessarbeit
  nur in der Prozessphase, die Retro beginnt mit dem Produkt und hat höchstens zwei Items
  ([Ablauf](../prozess/ablauf.md#prozessphase)); die Probe des Reviewers je Zyklus
  (Technikphase, Schritt 4); zwei neue [Kennzahlen](../prozess/kennzahlen.md); Mutationstests
  vorgemerkt ([Backlog](../prozess/backlog.md)).
- Nach 600: kein eigener Commit für Kritik und gelöschte Anliegen, Textläufe gemeinsam, der
  Koordinator prüft nicht vorher ([Ablauf, Commits](../prozess/ablauf.md#commits)).
- Nach 685: [DoR 6](../prozess/ablauf.md#dor-item-bereit), UX vergleicht die Gesten mit
  ArbiterMap und Arbiter-old vor den Mockups. Mechanismus: nur Text.

Befund 2 liegt über der Schwelle; beide Items gehen auf deine Antworten in 630 zurück.

## Prozess-Items
- P1 Fortschritt des Produkts als erste Zeile von Stand und Dashboard: erreichte Etappen von
  sieben, Kriterien der Etappe mit grünem Test; darunter die Schritte der Phase (490, Teil 3).
  Bordmittel: Die Statuszeile von Claude Code (`statusLine`) kann dieselbe Zeile ständig
  zeigen. Aus Befund 4 und 630, F3.
- P2 Wartende Anliegen im Kopf und nicht als dran im Stand: [686](anliegen/686-wartetAufImKopf.md).
  Aus Befund 5.

## Anliegen
- An mich: 685 angenommen; 421 wartet auf 490, den Kopf setze ich nach P2.
- Von mir an dich: 600 und 630 erledigt. Neu [687](anliegen/687-backlogUndVorbild.md): wer
  den Backlog schreibt (Folge von 630 F1) und „wie ArbiterMap und Arbiter-old“ für jede Rolle.
- Regelumsetzer: zuerst [601](anliegen/601-commitHooksNachPfad.md) und
  [650](anliegen/650-schreibgrenzeSperrtTmpUndLesen.md) (halten jede Rolle auf), dann P1, P2;
  [490](anliegen/490-fortschrittInPlanReviewRetro.md) Teil 2 wartet auf die Prozessphase 6.

## Empfehlung
Beantworte 687, dann freigeben. Danach Domänenphase 6 mit 684 (Aufstellen per Klick).

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [ ] Fachkritiker: Kritik an Regeländerungen
- [ ] Architekt: Kritik an Regeländerungen
- [ ] Organisationsentwickler: Nachkorrektur
- [ ] Stakeholder: Freigabe Retro 5
- [ ] Regelumsetzer: P1
- [ ] Regelumsetzer: P2
- [ ] Koordinator: nach dev gepusht

## Freigabe
Freigabe: offen
Kommentar: .
