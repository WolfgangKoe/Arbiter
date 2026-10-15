# Moderation

Stand vor Freigabe Retro 5: 21 Anliegen im Ordner. Blockiert die Freigabe: nur deine Antwort
in 687. Blockiert Zyklus 6: 684 vor 681 (Aufstellen per Klick).

## Dran
- Stakeholder: [687](anliegen/687-backlogUndVorbild.md), F1 bis F3 (unten).
- Anforderungsautor: [684](anliegen/684-anforderungenFuerKlickenBlockUndGrund.md) zuerst, das
  Item in Plan 6 hängt daran; dazu [670](anliegen/670-karteSpringtWennEinGrundErscheint.md).
- Ux: [681](anliegen/681-zeigenWasDerSpielerTunKann.md) nach 684;
  [620](anliegen/620-mockupsNachDemEinbauLoeschen.md) (fünf Mockups löschen). Nachprüfung
  [683](anliegen/683-aufstellenKlickenOderZiehen.md) (deine Rückfrage steht noch darin) und
  [685](anliegen/685-bedienungVorDemBildschirmTestPruefen.md).
- Implementierer: [680](anliegen/680-markierterTextSperrtDasZiehen.md),
  [682](anliegen/682-gezogeneKarteVerschwindetAmSpaltenrand.md).
- Reviewer: [640](anliegen/640-review5BelegeUndWorteDesSpielers.md),
  [660](anliegen/660-klickpfadZeigtNichtAllesNeue.md).
- Testautor: [621](anliegen/621-restDerEinheitOhneGesperrte.md),
  [622](anliegen/622-zugschwelleUngeprueft.md); Nachprüfung
  [580](anliegen/580-auswahlPyAlsHilfsmodul.md).
- Regelumsetzer: [650](anliegen/650-schreibgrenzeSperrtTmpUndLesen.md),
  [601](anliegen/601-commitHooksNachPfad.md),
  [686](anliegen/686-wartetAufImKopf.md) (P2),
  [490](anliegen/490-fortschrittInPlanReviewRetro.md) (P1; Teil 2 erst Prozessphase 6);
  Nachprüfung [610](anliegen/610-erledigteLoeschenImPreCommitVernichtetArbeit.md).
- Organisationsentwickler: [421](anliegen/421-schritteAbhaken.md), deine Antworten F1 A und
  F2 A liegen vor, es wartet auf 490. Architekt: Nachprüfung
  [550](anliegen/550-auswahlGehoertNichtZumZiehen.md).

## Vorschläge
- Zusammen (Anforderungsautor): 684 und 670 in einem Lauf, beide betreffen die Anforderungen
  zum Aufstellen und zum Grund; 670 erweitert QUE-2.5, kein neues Kriterium.
- Zusammen (Reviewer): 640 und 660, gleiche Datei `review.md`.
- Zusammen (Testautor): 621 und 622, getrennte Testdateien.
- Zusammen (Implementierer): 680 und 682, wenn beide dieselbe Frontend-Datei zum Ziehen
  ändern, ein Lauf; sonst gleichzeitig nach `git status`. 680 und 682 hängen nicht an 684.
- Ux: 681 wartet auf 684 (Kopf `· wartet auf 684`, Anliegen 686), 620 geht sofort.
- Schließen: 550, 580, 610, 683, 685 schließt der Verfasser nach der Nachprüfung; 421 nach
  Umsetzung von 490.
- Stränge Regelumsetzer, ein Hook-Code-Lauf zugleich
  ([Ablauf](../prozess/ablauf.md#gleichzeitige-läufe)): 650, dann 601, dann 686 (P2) und 490
  (P1) als Kette.
- Stränge Zyklus 6 gleichzeitig: Anforderungsautor (684/670), Implementierer (680/682),
  Testautor (621/622), Reviewer (640/660); nur Ux ist eine Kette (684, dann 681).

## Fragen an dich
Alle in [687](anliegen/687-backlogUndVorbild.md), Empfehlung jeweils A:
- F1: Wohin kommt Feinschliff (je Perspektive `feinschliff.md`)?
- F2: Gilt „wie ArbiterMap und Arbiter-old“ für jede Rolle, als Absatz in der Root-CLAUDE.md?
- F3: Halten fachliche Fehler und Verstöße gegen die Architektur auf (Ich 3)?
