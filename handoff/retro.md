# Retro · Zyklus 5

Dashboard öffnen: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten, im
Browser `http://127.0.0.1:8765/` öffnen, beenden mit Strg+C.

Etappe 1 · Aufstellen, Plan 5 mit drei Items. Grundlage: [Review 5](review.md), git seit
Commit „Freigabe Retro 4“, Anliegen, Belegung je Lauf.

## Fortschritt des Produkts
Etappe 1 von 7, keine erreicht. 74 von 94 Kriterien belegt
([Kennzahlen](../prozess/kennzahlen.md); Retro 4 ohne Zählung). Neu am Bildschirm:
*Einheiten* auf die *Karte* ziehen, *Modelle* verschieben, *gesperrt* stehen mit *Grund*,
„zurück“, „Aufstellen der Einheit beenden“. Für Etappe 1 fehlen „gemeinsam übergehen“ mit
*Protokoll*, *Gewinner* und Zone, *Leisten* und, nach deiner Antwort in 683, das Aufstellen
per Klick wie ArbiterMap.

## Befunde
1. Eine Bedienung fehlte, bis du sie am Bildschirm getestet hast (685, 683): Kein Schritt
   verglich die Gesten mit ArbiterMap. Gebaut wurde Ziehen aus der *Ablage*, das entfällt.
2. Mehr Prüfcode als Produktcode: 2.668 neue Zeilen in `prozess/pruefungen/` gegen 1.035 in
   `technik/arbiter` und `technik/frontend` (Review 5, Rundgang).
3. 114 Commits, 8 mit Produktcode, 14 nur Kritik; jeder wartete 7 bis 8 Minuten auf alle
   Prüfungen (600).
4. 89 neue Anliegen in fünf Tagen; 20 an Regelumsetzer oder mich, 22 % (Retro 4: 16 %,
   Schwelle ein Drittel). Viele betrafen Feinschliff, der nichts aufhielt (630).
5. Der Stand nannte Regelumsetzer und mich in jeder Phase als dran; wir liefen neben dem
   Produkt (630). „wartet auf“, das der Ablauf verlangt, lehnt die Prüfung ab (686).
6. Belegung: 16 von 175 Läufen über 120.000 Token, 2 über 150.000 (Retro 4: 2 und 0).
   Ursache unbekannt; einer kam durch Sperren der Schreibgrenze dorthin (650).
7. Die Probe des Reviewers fand zwei Lücken in den Tests (621, 622).

## Geändert
- Nach 630: Ein Anliegen nur, wenn etwas aufhält ([Ich 3](../prozess/praemissen/ich.md),
  Reviewer, Fachkritiker, Architekt); Prozessarbeit nur in der Prozessphase, die Retro
  beginnt mit dem Produkt, höchstens zwei Items ([Ablauf](../prozess/ablauf.md#prozessphase));
  die Probe des Reviewers je Zyklus (Technikphase, Schritt 4); zwei neue
  [Kennzahlen](../prozess/kennzahlen.md); Mutationstests im [Backlog](../prozess/backlog.md).
- Nach 600 und 691: kein eigener Commit für Kritik und gelöschte Anliegen, Textläufe
  gemeinsam, jeder Lauf mit Code (auch Tests) für sich, der Koordinator prüft nicht vorher
  ([Ablauf, Commits](../prozess/ablauf.md#commits)).
- Nach 685: [DoR 6](../prozess/ablauf.md#dor-item-bereit), UX vergleicht die Gesten mit
  ArbiterMap und Arbiter-old vor den Mockups. Mechanismus: nur Text.

Befund 2 liegt über der Schwelle; beide Items gehen auf deine Antworten in 630 zurück.

## Prozess-Items
- P1 Fortschritt des Produkts als erste Zeile von Stand und Dashboard, „Etappe 1 von 7 · 74
  von 94 Kriterien belegt“ nach den Kennzahlen, ohne Testlauf; darunter die Schritte der
  Phase (490, Teil 3). Gezählt über alle Kriterien, heute die der Etappe 1 (691).
  Bordmittel: `statusLine` zeigt die Zeile ständig. Aus Befund 4 und 630, F3.
- P2 Wartende Anliegen im Kopf und nicht als dran im Stand: [686](anliegen/686-wartetAufImKopf.md).
  Aus Befund 5.

## Anliegen
- An mich: 685, 690 und 691 angenommen; 421 wartet auf 490, den Kopf setze ich nach P2.
- An dich: 600 und 630 erledigt. [687](anliegen/687-backlogUndVorbild.md): wohin Feinschliff,
  ob fachliche Fehler und Verstöße gegen die Architektur aufhalten (690, 691), „wie
  ArbiterMap und Arbiter-old“ für jede Rolle.
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
