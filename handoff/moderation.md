# Moderation

Stand vor Freigabe Review 5: 15 Anliegen im Ordner. Maßstab: was das Produktziel voranbringt,
zuerst. Am Bildschirm fehlt nichts; die Freigabe hängt nur an Texten und einem Löschen.

## Dran
Blockiert die Freigabe Review 5 (DoD Oberfläche, Klarheit des Reviews):
- Ux: [620](anliegen/620-mockupsNachDemEinbauLoeschen.md), fünf Mockups löschen. Das ist
  der einzige rote DoD-Punkt.
- Reviewer: [660](anliegen/660-klickpfadZeigtNichtAllesNeue.md) (drei Schritte im Klickpfad)
  und [640](anliegen/640-review5BelegeUndWorteDesSpielers.md) (Belege, Leisten, Worte des
  Spielers), beide im selben Text `review.md`.

Produkt, hält das Inkrement nicht auf:
- Testautor: [621](anliegen/621-restDerEinheitOhneGesperrte.md),
  [622](anliegen/622-zugschwelleUngeprueft.md); Nachprüfung
  [550](anliegen/550-auswahlGehoertNichtZumZiehen.md),
  [580](anliegen/580-auswahlPyAlsHilfsmodul.md).
- Anforderungsautor: [670](anliegen/670-karteSpringtWennEinGrundErscheint.md), die Karte
  springt bei einem Grund; trifft Touch und ab Etappe 2 jeden Zug.

Prozess:
- Regelumsetzer: [650](anliegen/650-schreibgrenzeSperrtTmpUndLesen.md) und
  [601](anliegen/601-commitHooksNachPfad.md) (600 ist beantwortet, Warten und Sperren
  halten jede Rolle auf); Nachprüfung [610](anliegen/610-erledigteLoeschenImPreCommitVernichtetArbeit.md);
  [490](anliegen/490-fortschrittInPlanReviewRetro.md) Teile 2 und 3 erst in der Prozessphase.
- Organisationsentwickler: Anliegen 600 und
  [421](anliegen/421-schritteAbhaken.md) (Antworten liegen vor) in Ablauf und Koordinator
  umsetzen.
- Stakeholder: nur 630 (unten).

## Vorschläge
- Zusammen: 640 und 660 in einem Lauf des Reviewers, gleiche Datei. Der Satz „Von Hand nur
  die Anfragen …“ steht in beiden; 660 führt ihn aus, 640 verweist darauf.
- Zusammen: 621 und 622 in einem Lauf des Testautors, getrennte Testdateien.
- Schließen: 600 und 421, sobald der Organisationsentwickler Ablauf und Koordinator
  angepasst hat. 550, 580 und 610 schließt der Verfasser nach der Nachprüfung (Testautor,
  Regelumsetzer, Organisationsentwickler).
- 670 als kleines Item in Plan 6 neben „gemeinsam übergehen“: der Anforderungsautor erweitert
  QUE-2.5, kein neues Kriterium.
- Reihenfolge: 620, 640/660 jetzt, dann Freigabe; 621/622 laufen daneben, kein Item wartet.
- Stränge Regelumsetzer, höchstens ein Hook-Code-Lauf
  ([Ablauf](../prozess/ablauf.md#gleichzeitige-läufe)): zuerst 650 (`schreibgrenze.py`,
  `bashSchreiben.py`, Hook), dann 601 (`.pre-commit-config.yaml`); 490 danach.
- Stränge Organisationsentwickler: 600 und 421 gleichzeitig, wenn die Dateien getrennt sind
  (Koordinator gegen Ablauf).
- Gleichzeitig: Ux (620), Reviewer (640/660), Testautor (621/622) und Anforderungsautor (670)
  berühren getrennte Dateien.

## Fragen an dich
Alle in Anliegen 630, Antwort steht überall auf `.`:
- F1: Anliegen nur, wenn etwas aufhält; Empfehlung A. Das hätte 640 und 670 zu Backlog
  gemacht.
- F2: Prozessarbeit nur in der Prozessphase; Empfehlung A (601 und 650 laufen, 490 wartet).
- F3: Fortschritt des Produkts in Stand und Dashboard; Empfehlung A.
- F4: Probe der Tests je Zyklus durch den Reviewer; Empfehlung A.
